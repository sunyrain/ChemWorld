"""Foundation-backed Gymnasium environment for the unified ChemWorld."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
from math import isfinite
from typing import Any
from uuid import uuid4

import gymnasium as gym
import numpy as np

from chemworld.action_codec import ActionCodec
from chemworld.envs.reports import (
    annotate_constitution_rollback,
    build_constitution_summary,
    build_evaluator_provenance,
    build_step_info,
    build_task_info,
    render_env,
    sanitize_agent_info,
)
from chemworld.envs.spaces import (
    OBSERVATION_KEYS,
    empty_observation,
    make_action_space,
    make_observation_space,
    to_observation,
    value_or_default,
)
from chemworld.foundation.state import (
    OperationRecord,
    ProcessLedger,
    WorldState,
    process_with_last_observation,
)
from chemworld.operation_validator import OperationValidation, OperationValidator
from chemworld.runtime import (
    ChemWorldObservationKernel,
    ChemWorldRuntime,
    MechanismSpeciesView,
    make_chemworld_constitution,
)
from chemworld.tasks import default_kernel_maturity, get_task
from chemworld.world.observation_contracts import TaskObservationContract
from chemworld.world.operations import (
    INSTRUMENTS,
    REACTION_OPERATIONS,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.scoring import TaskScoringContract

DEFAULT_SCENARIO_ID = "reaction-to-assay"
__all__ = ["OBSERVATION_KEYS", "ChemWorldEnv"]


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
        budget_override: int | None = None,
        episode_mode_override: str | None = None,
        safety_limit_override: float | None = None,
        observation_seed_override: int | None = None,
        world_interventions: tuple[dict[str, Any], ...] | list[dict[str, Any]] | None = None,
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
        if budget_override is not None:
            budget = int(budget_override)
        if budget <= 0:
            raise ValueError("budget must be positive")
        if episode_mode_override not in {None, "single_experiment", "campaign"}:
            raise ValueError("episode_mode_override must be single_experiment, campaign, or None")
        if safety_limit_override is not None and (
            not isfinite(float(safety_limit_override))
            or not 0.0 < float(safety_limit_override) <= 1.0
        ):
            raise ValueError("safety_limit_override must be finite and in (0, 1]")

        self.world_split = world_split
        self.budget = budget
        self.official_budget = self.task_spec.budget if self.task_spec is not None else budget
        self.objective = objective
        self.seed = seed
        self.observation_seed_override = (
            None if observation_seed_override is None else int(observation_seed_override)
        )
        self.debug_truth = debug_truth
        self.world_interventions = tuple(world_interventions or ())
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
            else default_kernel_maturity(
                tuple(sorted(self.allowed_operations)),
                allowed_instruments=tuple(sorted(self.allowed_instruments)),
            )
        )
        self.episode_mode = (
            self.task_spec.episode_mode if self.task_spec is not None else "single_experiment"
        )
        if episode_mode_override is not None:
            self.episode_mode = episode_mode_override
        self.contract_profile = (
            "extended-research"
            if budget_override is not None or episode_mode_override is not None
            else "official"
        )
        self.safety_limit = self.task_spec.safety_limit if self.task_spec is not None else 0.65
        if safety_limit_override is not None:
            self.safety_limit = float(safety_limit_override)
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
        self.scenario_instance = self.scenario_generator.generate(
            self.scenario_spec,
            seed,
            self.world_interventions,
        )
        self.world = self.scenario_instance.parameters
        self.constitution = make_chemworld_constitution(self.scenario_instance.compiled_mechanism)
        self.observation_contract = self._make_observation_contract()
        self.operation_validator = self._make_operation_validator()
        self.runtime = self._make_runtime()
        self.observation_kernel = ChemWorldObservationKernel(
            self.constitution,
            objective,
            self.scenario_instance.compiled_mechanism,
            self.scoring_contract,
            self.observation_contract,
            observation_noise_multiplier=self.world.domain_parameter(
                "observation_noise_multiplier"
            ),
        )
        self._rng = np.random.default_rng(self._observation_seed(seed))
        self._step_count = 0
        self._experiment_index = 0
        self._operation_id = 0
        self._done = False
        self._state = deepcopy(self.scenario_instance.initial_state)
        self._last_observation = empty_observation()
        self._last_operation_record: OperationRecord | None = None
        self._last_info: dict[str, Any] = {}
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
        self._rng = np.random.default_rng(self._observation_seed(self.seed))
        if options and options.get("scenario_id"):
            self.scenario_spec = get_scenario(str(options["scenario_id"]), split=self.world_split)
        self.scenario_instance = self.scenario_generator.generate(
            self.scenario_spec,
            self.seed,
            self.world_interventions,
        )
        self.world = self.scenario_instance.parameters
        self._state = deepcopy(self.scenario_instance.initial_state)
        self.constitution = make_chemworld_constitution(self.scenario_instance.compiled_mechanism)
        self.operation_validator = self._make_operation_validator()
        self.observation_contract = self._make_observation_contract()
        self.runtime = self._make_runtime()
        self.observation_kernel = ChemWorldObservationKernel(
            self.constitution,
            self.objective,
            self.scenario_instance.compiled_mechanism,
            self.scoring_contract,
            self.observation_contract,
            observation_noise_multiplier=self.world.domain_parameter(
                "observation_noise_multiplier"
            ),
        )
        self._step_count = 0
        self._experiment_index = 0
        self._operation_id = 0
        self._done = False
        self._last_observation = empty_observation()
        self._last_operation_record = None
        self._last_info = {}
        self._campaign_id = self._make_campaign_id()
        self._experiment_summaries = []
        return deepcopy(self._last_observation), self.task_info()

    def step(
        self,
        action: Any,
    ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before step().")

        # Malformed or unknown agent actions are benchmark outcomes, not runner
        # crashes. Preserve their public payload so the central validator can
        # emit a replayable invalid transaction with no physical state mutation.
        # Valid aliases and numeric Gym actions still take the canonical path.
        raw_action = dict(action) if isinstance(action, Mapping) else {"operation": "invalid"}
        try:
            action = self.action_codec.canonicalize(raw_action)
        except (IndexError, OverflowError, TypeError, ValueError):
            action = raw_action
        previous_state = self._state
        validation = self.operation_validator.validate(action, self._state)
        if validation.dispatchable_to_runtime:
            try:
                runtime_result = self.runtime.apply_transaction(self._state, action)
            except (ArithmeticError, ValueError):
                # Physically undefined proposals are part of an exploratory agent's
                # action distribution, not a reason to terminate the entire Gym job.
                # Convert only domain/numerical errors into a replayable failed
                # transaction. Programming errors such as KeyError and TypeError
                # remain visible to developers.
                validation = self._domain_failure_validation(
                    validation,
                    "runtime_domain_valid",
                )
                runtime_result = self.runtime.apply_invalid_transaction(
                    self._state,
                    action,
                    validation,
                )
        else:
            runtime_result = self.runtime.apply_invalid_transaction(
                self._state,
                action,
                validation,
            )
        self._state = runtime_result.state
        operation_record = runtime_result.operation_record
        runtime_info = runtime_result.info_payload()
        preconditions_passed = all(operation_record.preconditions.values())
        operation_committed = (
            preconditions_passed and runtime_result.kernel_result.transaction_status == "committed"
        )
        observation_checks: list[dict[str, object]] = []
        observation_rng_state = deepcopy(self._rng.bit_generator.state)
        if operation_committed:
            try:
                observation = self.observation_kernel.observe(self._state, action, self._rng)
            except (ArithmeticError, ValueError):
                self._rng.bit_generator.state = observation_rng_state
                validation = self._domain_failure_validation(
                    validation,
                    "observation_domain_valid",
                )
                runtime_result = self.runtime.apply_invalid_transaction(
                    previous_state,
                    action,
                    validation,
                )
                self._state = runtime_result.state
                operation_record = runtime_result.operation_record
                runtime_info = runtime_result.info_payload()
                preconditions_passed = False
                operation_committed = False
                observation = self.observation_kernel.failed_observation()
            else:
                candidate_observation_report = self.constitution.check_observation(
                    observation,
                    debug_truth=self.debug_truth,
                )
                if candidate_observation_report.passed:
                    observation_checks = candidate_observation_report.to_list()
                else:
                    # Observation generation is part of the atomic public
                    # transition.  A non-finite, leaking, or internally
                    # inconsistent packet invalidates the action, restores the
                    # observation RNG, and rolls physical state back to the
                    # pre-action snapshot plus the declared process penalty.
                    self._rng.bit_generator.state = observation_rng_state
                    observation_checks = candidate_observation_report.to_list()
                    validation = self._domain_failure_validation(
                        validation,
                        "observation_domain_valid",
                    )
                    runtime_result = self.runtime.apply_invalid_transaction(
                        previous_state,
                        action,
                        validation,
                    )
                    self._state = runtime_result.state
                    operation_record = runtime_result.operation_record
                    runtime_info = runtime_result.info_payload()
                    preconditions_passed = False
                    operation_committed = False
                    observation = self.observation_kernel.failed_observation()
        else:
            observation = self.observation_kernel.failed_observation()
        if not observation_checks:
            observation_checks = self.constitution.check_observation(
                observation,
                debug_truth=self.debug_truth,
            ).to_list()
        operation_record = replace(
            operation_record,
            constitution_checks=[
                *operation_record.constitution_checks,
                *observation_checks,
            ],
        )
        observation_values = observation.values
        if operation_committed and operation_record.is_instrument_measurement:
            self._state = self._state.replace(
                process=process_with_last_observation(
                    self._state.process,
                    observation_values,
                    observation.observed_mask,
                )
            )
        previous_process = previous_state.process or ProcessLedger()
        if (
            operation_committed
            and not operation_record.is_instrument_measurement
            and previous_process.last_observation
        ):
            self._state = self._state.replace(
                process=process_with_last_observation(
                    self._state.process,
                    previous_process.last_observation,
                    previous_process.last_observed_mask,
                )
            )

        self._step_count += 1
        self._operation_id += 1
        successful_final_assay = operation_committed and operation_record.is_final_assay
        truncated = self._step_count >= self.budget
        campaign_final_assay = successful_final_assay and self.episode_mode == "campaign"
        terminated = successful_final_assay and not campaign_final_assay
        self._done = terminated or truncated
        observation_dict = to_observation(observation_values)
        self._last_observation = deepcopy(observation_dict)
        # Environment reward is an event-gated public score delta.  Only a
        # successful instrument measurement creates new public information;
        # process actions may retain the last observation for Markov state but
        # must never earn that cached absolute score again.
        reward = 0.0
        if operation_committed and operation_record.is_instrument_measurement:
            previous_score = (
                value_or_default(previous_process.last_observation, "score")
                if previous_process.last_observation
                else 0.0
            )
            reward = value_or_default(observation_values, "score") - previous_score
        self._last_operation_record = operation_record
        info = self._info(operation_record, observation)
        info.update(runtime_info)
        # Operation records are assembled from the retained rollback state,
        # which is constitution-safe by construction.  The report adapter
        # preserves any failed candidate-state check as a public outcome.
        info = annotate_constitution_rollback(info)
        info["observed_reward"] = float(reward)
        info["environment_reward"] = {
            "schema_version": "chemworld-environment-reward-0.2",
            "semantics": "fresh_measurement_score_delta",
            "fresh_measurement": bool(
                operation_committed and operation_record.is_instrument_measurement
            ),
            "cached_observation_rewarded": False,
            "score_delta": float(reward),
        }
        if self.debug_truth:
            info["truth"] = self._state.to_dict(include_hidden=True)
        else:
            info = sanitize_agent_info(info)
        if campaign_final_assay:
            info["experiment_ended"] = True
            terminal_summary = {
                "experiment_index": self._experiment_index,
                "terminal_step": self._step_count,
                "leaderboard_score": info["leaderboard_score"],
                "safety_risk": value_or_default(observation_values, "safety_risk"),
                "cost": value_or_default(observation_values, "cost"),
                "final_assay": True,
            }
            self._experiment_summaries.append(deepcopy(terminal_summary))
            self._experiment_index += 1
            info["experiment_summaries"] = deepcopy(self._experiment_summaries)
            info["last_terminal_summary"] = deepcopy(terminal_summary)
            info["next_experiment_index"] = self._experiment_index
            if not truncated:
                self._state = self._fresh_initial_state()
                info["next_experiment_ready"] = True
            else:
                info["next_experiment_ready"] = False
        self._last_info = deepcopy(info)
        return observation_dict, reward, terminated, truncated, info

    def task_info(self) -> dict[str, Any]:
        return build_task_info(self)

    def evaluator_provenance(self) -> dict[str, Any]:
        """Return private replay identity for the official evaluator/logger."""

        return build_evaluator_provenance(self)

    def task_prompt(self) -> dict[str, Any]:
        from chemworld.agent_interface import task_prompt

        return task_prompt(self)

    def available_actions(self, *, include_invalid: bool = False) -> list[dict[str, Any]]:
        from chemworld.agent_interface import available_actions

        return available_actions(self, include_invalid=include_invalid)

    def action_schema(self, operation: str) -> dict[str, Any]:
        from chemworld.agent_interface import action_schema

        return action_schema(self, operation)

    def validate_action(self, action: dict[str, Any]) -> dict[str, Any]:
        from chemworld.agent_interface import validate_action

        return validate_action(self, action)

    def observation_view(self, mode: str = "tool_json") -> dict[str, Any]:
        from chemworld.agent_interface import observation_view

        return observation_view(self, mode)

    def campaign_state(self) -> dict[str, Any]:
        from chemworld.agent_interface import campaign_state

        return campaign_state(self)

    def constitution_summary(self) -> dict[str, Any]:
        return build_constitution_summary(self)

    def render(self) -> Any:
        return render_env(self)

    def _make_campaign_id(self) -> str:
        # Public episode identity must not be a reversible encoding of the
        # hidden-world seed. Replay identity is carried separately in private
        # evaluator provenance.
        return f"episode-{uuid4().hex}"

    def _make_runtime(self) -> ChemWorldRuntime:
        return ChemWorldRuntime(
            world=self.world,
            constitution=self.constitution,
            task_spec=self.task_spec,
            compiled_mechanism=self.scenario_instance.compiled_mechanism,
            debug_truth=self.debug_truth,
        )

    def _make_operation_validator(self) -> OperationValidator:
        species_view = MechanismSpeciesView(self.scenario_instance.compiled_mechanism)
        unit_charge = species_view.reagent_charge_amounts(
            self.scenario_instance.initial_state,
            limiting_amount_mol=1.0,
        )
        reagent_charge_molar_multiplier = sum(
            amount for species_id, amount in unit_charge.items() if not species_id.startswith("Cat")
        )
        return OperationValidator(
            constitution=self.constitution,
            allowed_operations=self.allowed_operations,
            allowed_instruments=self.allowed_instruments,
            task_id=None if self.task_spec is None else self.task_spec.task_id,
            target_species=species_view.target_species,
            reagent_charge_molar_multiplier=reagent_charge_molar_multiplier,
            action_codec=self.action_codec,
        )

    @staticmethod
    def _domain_failure_validation(
        validation: OperationValidation,
        failure_key: str,
    ) -> OperationValidation:
        return replace(
            validation,
            is_valid=False,
            preconditions={**validation.preconditions, failure_key: False},
            invalid_reasons=tuple(dict.fromkeys((*validation.invalid_reasons, failure_key))),
            cost_penalty=max(validation.cost_penalty, 0.10),
            safety_flags={
                **validation.safety_flags,
                "precondition_failed": True,
                failure_key: False,
            },
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
        return deepcopy(self.scenario_instance.initial_state)

    def _observation_seed(self, world_seed: int) -> int:
        """Resolve observation noise independently from hidden-world generation.

        The default preserves the historical one-seed behavior. Evaluators may
        override only the observation stream so paired no-change resets retain the
        same hidden physical laws without receiving identical measurement noise.
        """

        if self.observation_seed_override is None:
            return int(world_seed)
        return self.observation_seed_override

    def _info(self, operation_record: OperationRecord, observation: Any) -> dict[str, Any]:
        return build_step_info(self, operation_record, observation)
