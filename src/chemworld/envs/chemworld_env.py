"""Foundation-backed Gymnasium environment for the unified ChemWorld."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import gymnasium as gym
import numpy as np

from chemworld.action_codec import ActionCodec
from chemworld.envs.reports import (
    build_constitution_summary,
    build_step_info,
    build_task_info,
    render_env,
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
from chemworld.operation_validator import OperationValidator
from chemworld.runtime import (
    ChemWorldObservationKernel,
    ChemWorldRuntime,
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
        self.constitution = make_chemworld_constitution(
            self.scenario_instance.compiled_mechanism
        )
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
            self._rng = np.random.default_rng(seed)
        if options and options.get("scenario_id"):
            self.scenario_spec = get_scenario(str(options["scenario_id"]), split=self.world_split)
        self.scenario_instance = self.scenario_generator.generate(self.scenario_spec, self.seed)
        self.world = self.scenario_instance.parameters
        self._state = self.scenario_instance.initial_state
        self.constitution = make_chemworld_constitution(
            self.scenario_instance.compiled_mechanism
        )
        self.operation_validator = OperationValidator(
            constitution=self.constitution,
            allowed_operations=self.allowed_operations,
            allowed_instruments=self.allowed_instruments,
            action_codec=self.action_codec,
        )
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
        self._last_info = {}
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
            self._state = self._state.replace(
                process=process_with_last_observation(
                    self._state.process,
                    observation_values,
                    observation.observed_mask,
                )
            )
        previous_process = previous_state.process or ProcessLedger()
        if preconditions_passed and previous_process.last_observation:
            self._state = self._state.replace(
                process=process_with_last_observation(
                    self._state.process,
                    previous_process.last_observation,
                    previous_process.last_observed_mask,
                )
            )

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
        self._last_info = dict(info)
        return observation_dict, reward, terminated, truncated, info

    def task_info(self) -> dict[str, Any]:
        return build_task_info(self)

    def task_prompt(self) -> dict[str, Any]:
        from chemworld.agent_interface import task_prompt

        return task_prompt(self)

    def available_actions(self) -> list[dict[str, Any]]:
        from chemworld.agent_interface import available_actions

        return available_actions(self)

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
        return build_step_info(self, operation_record, observation)
