"""Foundation-backed Gymnasium environment for the unified ChemWorld."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import gymnasium as gym
import numpy as np

from chemworld import __version__
from chemworld.action_codec import ActionCodec
from chemworld.backends import semi_mechanistic_backend_spec
from chemworld.envs.spaces import (
    OBSERVATION_KEYS,
    empty_observation,
    make_action_space,
    make_observation_space,
    to_observation,
    value_or_default,
)
from chemworld.foundation.state import OperationRecord, WorldState
from chemworld.operation_validator import OperationValidator
from chemworld.runtime import (
    ChemWorldObservationKernel,
    ChemWorldRuntime,
    make_chemworld_constitution,
)
from chemworld.tasks import default_kernel_maturity, get_task
from chemworld.world.instruments import instrument_contracts
from chemworld.world.observation_contracts import TaskObservationContract
from chemworld.world.operations import (
    INSTRUMENTS,
    OPERATION_TYPES,
    REACTION_OPERATIONS,
    chemworld_operations,
    chemworld_state_variable_contracts,
    operation_contracts,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.scoring import TaskScoringContract, safety_cost_from_flags
from chemworld.world.world_law import world_law_spec

DEFAULT_SCENARIO_ID = "reaction-to-assay"


class ChemWorldEnv(gym.Env[dict[str, np.ndarray], dict[str, Any]]):
    """Unified physical-chemical world sliced into benchmark tasks."""

    metadata: dict[str, Any] = {"render_modes": ["ansi", "human"], "render_fps": 4}  # noqa: RUF012

    def __init__(
        self,
        *,
        world_split: str = "public-dev",
        budget: int = 30,
        objective: str = "balanced",
        seed: int = 0,
        task_id: str | None = None,
        debug_truth: bool = False,
        render_mode: str | None = None,
    ) -> None:
        super().__init__()
        if render_mode is not None and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Unsupported render_mode={render_mode!r}")
        self.task_id = task_id
        self.task_spec = get_task(task_id) if task_id else None
        if self.task_spec is not None:
            world_split = self.task_spec.world_split
            budget = self.task_spec.budget
            objective = self.task_spec.objective
        if budget <= 0:
            raise ValueError("budget must be positive")

        self.world_split = world_split
        self.budget = budget
        self.objective = objective
        self.seed = seed
        self.debug_truth = debug_truth
        self.render_mode = render_mode
        self.allowed_operations = (
            set(self.task_spec.allowed_operations)
            if self.task_spec is not None
            else set(REACTION_OPERATIONS)
        )
        self.allowed_instruments = (
            set(self.task_spec.allowed_instruments)
            if self.task_spec is not None
            else set(INSTRUMENTS)
        )
        self.kernel_maturity = (
            self.task_spec.kernel_maturity
            if self.task_spec is not None
            else default_kernel_maturity(tuple(sorted(self.allowed_operations)))
        )
        self.episode_mode = (
            self.task_spec.episode_mode if self.task_spec is not None else "single_experiment"
        )
        self.safety_limit = self.task_spec.safety_limit if self.task_spec is not None else 0.65
        self.scoring_contract = TaskScoringContract.from_success_metrics(
            objective=objective,
            success_metrics=(
                self.task_spec.success_metrics if self.task_spec is not None else ("score",)
            ),
        )
        self.action_codec = ActionCodec()
        self.scenario_generator = DefaultScenarioGenerator()
        self.scenario_spec = (
            get_scenario(self.task_spec.scenario_id, split=world_split)
            if self.task_spec is not None
            else get_scenario(DEFAULT_SCENARIO_ID, split=world_split)
        )
        self.scenario_instance = self.scenario_generator.generate(self.scenario_spec, seed)
        self.world = self.scenario_instance.parameters
        self.constitution = make_chemworld_constitution()
        self.observation_contract = self._make_observation_contract()
        self.operation_validator = OperationValidator(
            constitution=self.constitution,
            allowed_operations=self.allowed_operations,
            allowed_instruments=self.allowed_instruments,
            action_codec=self.action_codec,
        )
        self.runtime = self._make_runtime()
        self.observation_kernel = ChemWorldObservationKernel(
            self.constitution,
            objective,
            self.scenario_instance.compiled_mechanism,
            self.scoring_contract,
            self.observation_contract,
        )
        self._rng = np.random.default_rng(seed)
        self._step_count = 0
        self._experiment_index = 0
        self._operation_id = 0
        self._done = False
        self._state = self.scenario_instance.initial_state
        self._last_observation = empty_observation()
        self._last_operation_record: OperationRecord | None = None
        self._campaign_id = self._make_campaign_id()
        self._experiment_summaries: list[dict[str, Any]] = []

        self.action_space = make_action_space()
        self.observation_space = make_observation_space()

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        super().reset(seed=seed)
        if seed is not None:
            self.seed = seed
            self._rng = np.random.default_rng(seed)
        if options and options.get("scenario_id"):
            self.scenario_spec = get_scenario(str(options["scenario_id"]), split=self.world_split)
        self.scenario_instance = self.scenario_generator.generate(self.scenario_spec, self.seed)
        self.world = self.scenario_instance.parameters
        self._state = self.scenario_instance.initial_state
        self.observation_contract = self._make_observation_contract()
        self.runtime = self._make_runtime()
        self.observation_kernel = ChemWorldObservationKernel(
            self.constitution,
            self.objective,
            self.scenario_instance.compiled_mechanism,
            self.scoring_contract,
            self.observation_contract,
        )
        self._step_count = 0
        self._experiment_index = 0
        self._operation_id = 0
        self._done = False
        self._last_observation = empty_observation()
        self._last_operation_record = None
        self._campaign_id = self._make_campaign_id()
        self._experiment_summaries = []
        return self._last_observation, self.task_info()

    def step(
        self,
        action: dict[str, Any],
    ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before step().")

        action = self.action_codec.canonicalize(action)
        previous_state = self._state
        validation = self.operation_validator.validate(action, self._state)
        if validation.dispatchable_to_runtime:
            runtime_result = self.runtime.apply_transaction(self._state, action)
            self._state = runtime_result.state
            operation_record = runtime_result.operation_record
            runtime_info = runtime_result.info_payload()
        else:
            penalized = self.runtime.domain_services.penalize_invalid(self._state)
            operation_record = self.runtime.domain_services.record_operation(
                action["operation"],
                self._state,
                penalized,
                validation.preconditions,
                action,
            )
            self._state = penalized
            runtime_info = {
                "kernel_id": "validation:invalid_action",
                "kernel_version": "runtime-v2.0",
                "affected_ledgers": ["process"],
                "world_events": [
                    {
                        "event_type": "validation_failed",
                        "operation_type": action["operation"],
                        "payload": {"invalid_reasons": list(validation.invalid_reasons)},
                    }
                ],
                "state_patches_summary": [],
                "cost_delta": 0.0,
                "risk_delta": 0.0,
                "sample_delta": 0.0,
                "transaction_status": "validation_failed",
                "rollback_reason": None,
            }
        preconditions_passed = all(operation_record.preconditions.values())
        if preconditions_passed:
            observation = self.observation_kernel.observe(self._state, action, self._rng)
        else:
            observation = self.observation_kernel.failed_observation()
        observation_report = self.constitution.check_observation(
            observation,
            debug_truth=self.debug_truth,
        )
        operation_record = replace(
            operation_record,
            constitution_checks=[
                *operation_record.constitution_checks,
                *observation_report.to_list(),
            ],
        )
        observation_values = observation.values
        if preconditions_passed and operation_record.operation_type == "measure":
            metadata = self._state.metadata.copy()
            metadata["last_observation"] = observation_values.copy()
            metadata["last_observed_mask"] = observation.observed_mask.copy()
            self._state = self._state.replace(metadata=metadata)
        elif preconditions_passed and previous_state.metadata.get("last_observation"):
            metadata = self._state.metadata.copy()
            metadata["last_observation"] = previous_state.metadata["last_observation"]
            metadata["last_observed_mask"] = previous_state.metadata.get(
                "last_observed_mask",
                {},
            )
            self._state = self._state.replace(metadata=metadata)

        self._step_count += 1
        self._operation_id += 1
        successful_final_assay = (
            preconditions_passed
            and operation_record.operation_type == "measure"
            and operation_record.instrument == "final_assay"
        )
        truncated = self._step_count >= self.budget
        campaign_final_assay = successful_final_assay and self.episode_mode == "campaign"
        terminated = successful_final_assay and not campaign_final_assay
        self._done = terminated or truncated
        observation_dict = to_observation(observation_values)
        self._last_observation = observation_dict
        reward = value_or_default(observation_values, "score")
        self._last_operation_record = operation_record
        info = self._info(operation_record, observation)
        info.update(runtime_info)
        if self.debug_truth:
            info["truth"] = self._state.to_dict(include_hidden=True)
        if campaign_final_assay:
            info["experiment_ended"] = True
            self._experiment_summaries.append(
                {
                    "experiment_index": self._experiment_index,
                    "terminal_step": self._step_count,
                    "leaderboard_score": info["leaderboard_score"],
                    "safety_risk": value_or_default(observation_values, "safety_risk"),
                    "cost": value_or_default(observation_values, "cost"),
                    "final_assay": True,
                }
            )
            self._experiment_index += 1
            if not truncated:
                self._state = self._fresh_initial_state()
                info["next_experiment_ready"] = True
            else:
                info["next_experiment_ready"] = False
        return observation_dict, reward, terminated, truncated, info

    def task_info(self) -> dict[str, Any]:
        scenario_card = self.scenario_instance.to_card()
        compiled_mechanism = self.scenario_instance.compiled_mechanism
        return {
            "env_id": "ChemWorld",
            "task_id": self.task_id,
            "world_law_id": self.world.family_version,
            "scenario_id": self.scenario_spec.scenario_id,
            "scenario": scenario_card,
            "initial_state_id": self.scenario_spec.initial_state_id,
            "world_split": self.world_split,
            "world_provider": self.world.provider,
            "objective": self.objective,
            "budget": self.budget,
            "episode_mode": self.episode_mode,
            "safety_limit": self.safety_limit,
            "seed": self.seed,
            "world_id": self.world.world_id,
            "task_contract_hash": (
                None if self.task_spec is None else self.task_spec.contract_hash
            ),
            "runtime_profile_hash": self.runtime.profile.profile_hash,
            "mechanism_id": compiled_mechanism.mechanism_id,
            "mechanism_hash": compiled_mechanism.mechanism_hash,
            "mechanism_version": compiled_mechanism.mechanism_version,
            "mechanism_manifest": compiled_mechanism.manifest.to_dict(),
            "scoring_contract": self.scoring_contract.to_dict(),
            "scoring_contract_hash": self.scoring_contract.contract_hash,
            "observation_contract": self.observation_contract.to_dict(),
            "observation_contract_hash": self.observation_contract.contract_hash,
            "env_version": __version__,
            "world_family_version": self.world.family_version,
            "runtime": self.runtime.to_dict(),
            "operation_types": list(OPERATION_TYPES),
            "allowed_operations": sorted(self.allowed_operations),
            "allowed_instruments": sorted(self.allowed_instruments),
            "kernel_maturity": self.kernel_maturity.to_dict(),
            "physics_maturity": self.kernel_maturity.lowest_level.value,
            "proxy_allowed": self.kernel_maturity.proxy_allowed,
            "instruments": {
                key: contract.to_dict() for key, contract in instrument_contracts().items()
            },
            "reactions": [
                reaction.to_dict()
                for reaction in compiled_mechanism.network.reactions
            ],
            "operations": [operation.to_dict() for operation in chemworld_operations()],
            "operation_contracts": {
                key: contract.to_dict() for key, contract in operation_contracts().items()
            },
            "state_variables": [
                variable.to_dict() for variable in chemworld_state_variable_contracts()
            ],
            "constitution": self.constitution_summary(),
            "world_law": world_law_spec().to_dict(),
            "backend": semi_mechanistic_backend_spec().to_dict(),
            "observation_keys": list(OBSERVATION_KEYS),
        }

    def constitution_summary(self) -> dict[str, Any]:
        state_report = self.constitution.check_state(self._state)
        return {
            "name": "PhysicalConstitutionChecklist",
            "passed": state_report.passed,
            "checks": state_report.to_list(),
            "rules": [
                "material_conservation",
                "nonnegative_state",
                "unit_consistency",
                "yield_upper_bound",
                "energy_balance",
                "phase_mass_balance",
                "observation_non_omniscient",
                "measurement_has_cost",
                "action_preconditions",
                "safety_constraints",
                "public_private_reproducibility",
            ],
        }

    def render(self) -> Any:
        """Render a concise visible campaign summary."""

        last_operation = (
            None
            if self._last_operation_record is None
            else self._last_operation_record.operation_type
        )
        lines = [
            "ChemWorld",
            f"  task: {self.task_id or 'ad-hoc'}",
            f"  scenario: {None if self.scenario_spec is None else self.scenario_spec.scenario_id}",
            f"  campaign: {self._campaign_id}",
            f"  step: {self._step_count}/{self.budget}",
            f"  experiment: {self._experiment_index}",
            f"  last_operation: {last_operation}",
            (
                "  ledger: "
                f"time_s={self._state.ledger.time_s:.1f}, "
                f"cost={self._state.ledger.cost:.3f}, "
                f"risk={self._state.ledger.risk:.3f}, "
                f"sample_L={self._state.ledger.sample_consumed_L:.6f}"
            ),
        ]
        visible = {
            key: float(value[0])
            for key, value in self._last_observation.items()
            if np.isfinite(float(value[0]))
        }
        lines.append(f"  visible_observation: {visible}")
        rendered = "\n".join(lines)
        if self.render_mode == "human":
            print(rendered)
            return None
        return rendered

    def _make_campaign_id(self) -> str:
        task_part = self.task_id or "adhoc"
        scenario_part = "none" if self.scenario_spec is None else self.scenario_spec.scenario_id
        return f"{task_part}:{scenario_part}:seed-{self.seed}"

    def _make_runtime(self) -> ChemWorldRuntime:
        return ChemWorldRuntime(
            world=self.world,
            constitution=self.constitution,
            task_spec=self.task_spec,
            compiled_mechanism=self.scenario_instance.compiled_mechanism,
            debug_truth=self.debug_truth,
        )

    def _make_observation_contract(self) -> TaskObservationContract:
        return TaskObservationContract.from_task(
            success_metrics=(
                self.task_spec.success_metrics if self.task_spec is not None else ("score",)
            ),
            scoring_contract=self.scoring_contract,
            allowed_instruments=tuple(sorted(self.allowed_instruments)),
            instruments=self.constitution.instruments,
            mechanism_observable_mapping=(
                self.scenario_instance.compiled_mechanism.observable_mapping
            ),
        )

    def _fresh_initial_state(self) -> WorldState:
        return self.scenario_instance.initial_state

    def _info(self, operation_record: OperationRecord, observation: Any) -> dict[str, Any]:
        values = observation.values
        checks = operation_record.constitution_checks
        constitution_failed = any(not bool(check.get("passed", False)) for check in checks)
        precondition_failed = not all(operation_record.preconditions.values())
        observed_keys = [key for key, observed in observation.observed_mask.items() if observed]
        if precondition_failed:
            reward_source = "failed_precondition"
        elif operation_record.operation_type == "measure":
            reward_source = f"instrument:{operation_record.instrument}"
        elif any(key in observed_keys for key in ("yield", "selectivity", "conversion")):
            reward_source = "carried_observation_with_public_ledger"
        else:
            reward_source = "public_ledger_only"
        score = value_or_default(values, "score")
        failed_preconditions = [
            key for key, passed in operation_record.preconditions.items() if not passed
        ]
        constraint_flags = {
            "unsafe": value_or_default(values, "safety_risk") >= self.safety_limit,
            "unsafe_by_task_limit": (
                value_or_default(values, "safety_risk") >= self.safety_limit
            ),
            "high_cost": value_or_default(values, "cost") >= 0.75,
            "low_selectivity": value_or_default(values, "selectivity") <= 0.35,
            "degradation_detected": (
                value_or_default(values, "degradation_warning") >= 0.28
            ),
            "constitution_failed": constitution_failed,
            "precondition_failed": precondition_failed,
            "phase_mass_balance_failed": any(
                check.get("name") == "phase_mass_balance" and not check.get("passed", False)
                for check in checks
            ),
        }
        cost_signal, cost_components = safety_cost_from_flags(constraint_flags)
        return {
            "step": self._step_count,
            "budget": self.budget,
            "remaining_budget": max(self.budget - self._step_count, 0),
            "campaign_id": self._campaign_id,
            "episode_mode": self.episode_mode,
            "experiment_index": self._experiment_index,
            "operation_id": self._operation_id,
            "experiment_ended": False,
            "experiment_summaries": list(self._experiment_summaries),
            "world_id": self.world.world_id,
            "task_id": self.task_id,
            "scenario_id": None if self.scenario_spec is None else self.scenario_spec.scenario_id,
            "initial_state_id": self.scenario_spec.initial_state_id,
            "world_law_id": self.world.family_version,
            "world_split": self.world_split,
            "world_provider": self.world.provider,
            "objective": self.objective,
            "safety_limit": self.safety_limit,
            "task_contract_hash": (
                None if self.task_spec is None else self.task_spec.contract_hash
            ),
            "runtime_profile_hash": self.runtime.profile.profile_hash,
            "mechanism_id": self.scenario_instance.compiled_mechanism.mechanism_id,
            "mechanism_hash": self.scenario_instance.compiled_mechanism.mechanism_hash,
            "scoring_contract_hash": self.scoring_contract.contract_hash,
            "observation_contract_hash": self.observation_contract.contract_hash,
            "operation_type": operation_record.operation_type,
            "operation_allowed_by_task": operation_record.operation_type in self.allowed_operations,
            "instrument_allowed_by_task": (
                operation_record.operation_type != "measure"
                or operation_record.instrument in self.allowed_instruments
            ),
            "preconditions": operation_record.preconditions,
            "state_delta_summary": operation_record.state_delta_summary,
            "constitution_checks": checks,
            "instrument": operation_record.instrument,
            "instrument_source": observation.instrument_id,
            "observed_keys": observed_keys,
            "observed_mask": observation.observed_mask,
            "raw_signal": observation.raw_signal,
            "processed_estimate": observation.processed_estimate,
            "uncertainty": observation.uncertainty,
            "measurement_cost": operation_record.measurement_cost,
            "sample_consumed": operation_record.sample_consumed_L,
            "observed_reward": score,
            "leaderboard_score": (
                score
                if operation_record.instrument == "final_assay" and not precondition_failed
                else None
            ),
            "reward_source": reward_source,
            "cost": cost_signal,
            "cost_components": cost_components,
            "constraint_budget_remaining": max(1.0 - cost_signal, 0.0),
            "error_message": (
                None
                if not failed_preconditions
                else f"Action precondition failed: {', '.join(failed_preconditions)}"
            ),
            "constraint_flags": constraint_flags,
            "env_version": __version__,
            "world_family_version": self.world.family_version,
        }
