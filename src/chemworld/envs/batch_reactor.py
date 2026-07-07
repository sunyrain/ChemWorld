"""Foundation-backed Gymnasium environment for BatchReactorWorld."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from chemworld import __version__
from chemworld.core.batch_reactor import (
    CATALYSTS,
    INSTRUMENTS,
    OPERATION_TYPES,
    SOLVENTS,
    BatchReactorObservationKernel,
    BatchReactorTransitionKernel,
    batch_reactor_instruments,
    batch_reactor_operations,
    batch_reactor_reactions,
    batch_reactor_state_variables,
    initial_batch_reactor_state,
    instrument_name,
    load_batch_reactor_world_parameters,
    make_batch_reactor_constitution,
    operation_name,
)
from chemworld.foundation.state import OperationRecord

OBSERVATION_KEYS = (
    "yield",
    "selectivity",
    "conversion",
    "cost",
    "safety_risk",
    "score",
    "byproduct_signal",
    "degradation_warning",
    "virtual_spectrum_summary",
)


class NullableScalarBox(spaces.Box):
    """A scalar Box that treats NaN as a valid missing observation."""

    def contains(self, x: object) -> bool:
        try:
            array = np.asarray(x, dtype=self.dtype)
        except (TypeError, ValueError):
            return False
        if array.shape != self.shape:
            return False
        finite = np.isfinite(array)
        if not np.any(finite):
            return True
        return bool(
            np.all(array[finite] >= self.low[finite])
            and np.all(array[finite] <= self.high[finite])
        )


class BatchReactorEnv(gym.Env[dict[str, np.ndarray], dict[str, Any]]):
    """Event-driven virtual batch reactor with ODE transition kernel."""

    metadata: dict[str, list[str]] = {"render_modes": []}  # noqa: RUF012

    def __init__(
        self,
        *,
        world_split: str = "public-dev",
        budget: int = 30,
        objective: str = "balanced",
        seed: int = 0,
        debug_truth: bool = False,
    ) -> None:
        super().__init__()
        if budget <= 0:
            raise ValueError("budget must be positive")

        self.world_split = world_split
        self.budget = budget
        self.objective = objective
        self.seed = seed
        self.debug_truth = debug_truth
        self.world = load_batch_reactor_world_parameters(world_split, seed)
        self.constitution = make_batch_reactor_constitution()
        self.transition_kernel = BatchReactorTransitionKernel(self.world, self.constitution)
        self.observation_kernel = BatchReactorObservationKernel(self.constitution, objective)
        self._rng = np.random.default_rng(seed)
        self._step_count = 0
        self._done = False
        self._state = initial_batch_reactor_state()
        self._last_observation = self._empty_observation()

        self.action_space = spaces.Dict(
            {
                "operation": spaces.Discrete(len(OPERATION_TYPES)),
                "amount_mol": spaces.Box(0.0, 0.040, shape=(1,), dtype=np.float32),
                "volume_L": spaces.Box(0.0, 0.080, shape=(1,), dtype=np.float32),
                "catalyst_amount_mol": spaces.Box(0.0, 0.005, shape=(1,), dtype=np.float32),
                "target_temperature_K": spaces.Box(250.0, 520.0, shape=(1,), dtype=np.float32),
                "duration_s": spaces.Box(0.0, 14_400.0, shape=(1,), dtype=np.float32),
                "stirring_speed_rpm": spaces.Box(100.0, 1200.0, shape=(1,), dtype=np.float32),
                "sample_volume_L": spaces.Box(0.0, 0.002, shape=(1,), dtype=np.float32),
                "instrument": spaces.Discrete(len(INSTRUMENTS)),
                "catalyst": spaces.Discrete(len(CATALYSTS)),
                "solvent": spaces.Discrete(len(SOLVENTS)),
            }
        )
        self.observation_space = spaces.Dict(
            {
                key: NullableScalarBox(low=0.0, high=1.0, shape=(1,), dtype=np.float32)
                for key in OBSERVATION_KEYS
            }
        )

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        del options
        super().reset(seed=seed)
        if seed is not None:
            self.seed = seed
            self.world = load_batch_reactor_world_parameters(self.world_split, seed)
            self.transition_kernel = BatchReactorTransitionKernel(self.world, self.constitution)
            self._rng = np.random.default_rng(seed)
        self._step_count = 0
        self._done = False
        self._state = initial_batch_reactor_state()
        self._last_observation = self._empty_observation()
        return self._last_observation, self.task_info()

    def step(
        self,
        action: dict[str, Any],
    ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before step().")

        action = self._canonical_event_action(action)
        previous_state = self._state
        self._state, operation_record = self.transition_kernel.transition(
            self._state,
            action,
            self._rng,
        )
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
        successful_final_assay = (
            preconditions_passed
            and operation_record.operation_type == "measure"
            and operation_record.instrument == "final_assay"
        )
        truncated = self._step_count >= self.budget
        terminated = successful_final_assay
        self._done = terminated or truncated
        observation_dict = self._to_observation(observation_values)
        self._last_observation = observation_dict
        reward = self._value_or_default(observation_values, "score")
        info = self._info(operation_record, observation)
        if self.debug_truth:
            info["truth"] = self._state.to_dict(include_hidden=True)
        return observation_dict, reward, terminated, truncated, info

    def task_info(self) -> dict[str, Any]:
        return {
            "env_id": "BatchReactorWorld",
            "world_split": self.world_split,
            "world_provider": self.world.provider,
            "objective": self.objective,
            "budget": self.budget,
            "seed": self.seed,
            "world_id": self.world.world_id,
            "env_version": __version__,
            "world_family_version": self.world.family_version,
            "operation_types": list(OPERATION_TYPES),
            "instruments": {
                key: item.to_dict() for key, item in batch_reactor_instruments().items()
            },
            "reactions": [reaction.to_dict() for reaction in batch_reactor_reactions()],
            "operations": [operation.to_dict() for operation in batch_reactor_operations()],
            "state_variables": [variable.to_dict() for variable in batch_reactor_state_variables()],
            "constitution": self.constitution_summary(),
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
                "observation_non_omniscient",
                "measurement_has_cost",
                "action_preconditions",
                "safety_constraints",
                "public_private_reproducibility",
            ],
        }

    @staticmethod
    def _canonical_event_action(action: dict[str, Any]) -> dict[str, Any]:
        if "operation" not in action:
            raise ValueError("Event actions must include an operation field")
        canonical = dict(action)
        canonical["operation"] = operation_name(canonical["operation"])
        if "instrument" in canonical:
            canonical["instrument"] = instrument_name(canonical["instrument"])
        return canonical

    def _info(self, operation_record: OperationRecord, observation: Any) -> dict[str, Any]:
        values = observation.values
        checks = operation_record.constitution_checks
        constitution_failed = any(not bool(check.get("passed", False)) for check in checks)
        precondition_failed = not all(operation_record.preconditions.values())
        observed_keys = [
            key for key, observed in observation.observed_mask.items() if observed
        ]
        if precondition_failed:
            reward_source = "failed_precondition"
        elif operation_record.operation_type == "measure":
            reward_source = f"instrument:{operation_record.instrument}"
        elif any(key in observed_keys for key in ("yield", "selectivity", "conversion")):
            reward_source = "carried_observation_with_public_ledger"
        else:
            reward_source = "public_ledger_only"
        score = self._value_or_default(values, "score")
        failed_preconditions = [
            key for key, passed in operation_record.preconditions.items() if not passed
        ]
        return {
            "step": self._step_count,
            "budget": self.budget,
            "remaining_budget": max(self.budget - self._step_count, 0),
            "world_id": self.world.world_id,
            "world_split": self.world_split,
            "world_provider": self.world.provider,
            "objective": self.objective,
            "operation_type": operation_record.operation_type,
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
            "error_message": (
                None
                if not failed_preconditions
                else f"Action precondition failed: {', '.join(failed_preconditions)}"
            ),
            "constraint_flags": {
                "unsafe": self._value_or_default(values, "safety_risk") >= 0.65,
                "high_cost": self._value_or_default(values, "cost") >= 0.75,
                "low_selectivity": self._value_or_default(values, "selectivity") <= 0.35,
                "degradation_detected": (
                    self._value_or_default(values, "degradation_warning") >= 0.28
                ),
                "constitution_failed": constitution_failed,
                "precondition_failed": precondition_failed,
            },
            "env_version": __version__,
            "world_family_version": self.world.family_version,
        }

    @staticmethod
    def _value_or_default(values: dict[str, float | None], key: str, default: float = 0.0) -> float:
        value = values.get(key)
        return default if value is None else float(value)

    @staticmethod
    def _to_observation(values: dict[str, float | None]) -> dict[str, np.ndarray]:
        def scalar_value(key: str) -> float:
            value = values.get(key)
            return np.nan if value is None else float(value)

        return {
            key: np.array(
                [scalar_value(key)],
                dtype=np.float32,
            )
            for key in OBSERVATION_KEYS
        }

    @staticmethod
    def _empty_observation() -> dict[str, np.ndarray]:
        return {
            key: np.array(
                [0.0 if key in {"cost", "safety_risk", "score"} else np.nan],
                dtype=np.float32,
            )
            for key in OBSERVATION_KEYS
        }
