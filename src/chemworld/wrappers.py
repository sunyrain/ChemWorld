"""Optional Gymnasium wrappers and event-action validators."""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium.utils import RecordConstructorArgs

from chemworld.agent_interface import observation_view, rl_observation_spec, rl_observation_view
from chemworld.data.logging import to_builtin
from chemworld.world.operations import OPERATION_TYPES
from chemworld.world.scoring import safety_cost_from_flags


def _base_env(env: gym.Env[Any, Any]) -> Any:
    return getattr(env, "unwrapped", env)


def valid_operations(env: gym.Env[Any, Any]) -> list[str]:
    """Return operation types whose current preconditions are satisfied."""

    base = _base_env(env)
    return list(base.operation_validator.valid_operations(base._state))


def action_mask(env: gym.Env[Any, Any]) -> list[bool]:
    base = _base_env(env)
    return list(base.operation_validator.action_mask(base._state))


def validate_event_action(action: dict[str, Any], env: gym.Env[Any, Any]) -> dict[str, Any]:
    """Validate one event action against the current environment state."""

    base = _base_env(env)
    return base.operation_validator.validate(action, base._state).to_dict()


def validate_operation_affordance(operation: str, env: gym.Env[Any, Any]) -> dict[str, Any]:
    """Validate current operation-level affordance without requiring payload fields."""

    base = _base_env(env)
    return base.operation_validator.operation_affordance(operation, base._state).to_dict()


def decode_continuous_event_action(
    action: Any,
    *,
    event_action_space: gym.spaces.Dict,
    operation_mask: list[bool] | np.ndarray,
) -> dict[str, Any]:
    """Decode the frozen RL vector contract using public operation affordances.

    This function is deliberately independent of an environment instance.  It
    lets frozen-policy evaluators use exactly the same mapping as the Gym
    wrapper while supplying only the public affordance mask available to every
    benchmark agent.
    """

    action_keys = tuple(event_action_space.spaces)
    parameter_keys = tuple(key for key in action_keys if key != "operation")
    operation_logit_count = len(OPERATION_TYPES)
    expected_shape = (operation_logit_count + len(parameter_keys),)
    vector = np.asarray(action, dtype=np.float32).reshape(-1)
    if vector.shape != expected_shape or not np.all(np.isfinite(vector)):
        raise ValueError(
            f"continuous event action must be a finite vector with shape {expected_shape}"
        )
    public_mask = np.asarray(operation_mask, dtype=bool)
    if public_mask.shape != (operation_logit_count,):
        raise ValueError("public operation mask does not match the frozen operation registry")
    operation_logits = vector[:operation_logit_count]
    if np.any(public_mask):
        operation_index = int(np.argmax(np.where(public_mask, operation_logits, -np.inf)))
    else:
        operation_index = int(np.argmax(operation_logits))
    payload: dict[str, Any] = {"operation": operation_index}
    unit = np.clip((vector[operation_logit_count:] + 1.0) / 2.0, 0.0, 1.0)
    for index, key in enumerate(parameter_keys):
        space = event_action_space[key]
        coordinate = float(unit[index])
        if isinstance(space, gym.spaces.Discrete):
            payload[key] = min(int(coordinate * space.n), space.n - 1)
        elif isinstance(space, gym.spaces.Box):
            value = space.low + coordinate * (space.high - space.low)
            payload[key] = to_builtin(np.asarray(value, dtype=space.dtype))
        else:
            raise TypeError(f"unsupported event action component: {key}={type(space).__name__}")
    return payload


class ActionMaskWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Add operation validity signals to reset/step info."""

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        return observation, self._with_mask(info)

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        return observation, float(reward), terminated, truncated, self._with_mask(info)

    def _with_mask(self, info: dict[str, Any]) -> dict[str, Any]:
        payload = dict(info)
        mask = action_mask(self.env)
        payload["valid_operations"] = [
            operation_type
            for operation_type, is_valid in zip(OPERATION_TYPES, mask, strict=True)
            if is_valid
        ]
        payload["action_mask"] = np.asarray(mask, dtype=bool)
        payload["operation_types"] = list(OPERATION_TYPES)
        payload["invalid_reasons"] = {
            operation_type: validate_operation_affordance(operation_type, self.env)[
                "invalid_reasons"
            ]
            for operation_type in OPERATION_TYPES
            if operation_type not in payload["valid_operations"]
        }
        return payload


class SafetyCostWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Expose safe-RL style cost signals without changing Gymnasium returns."""

    def __init__(self, env: gym.Env[Any, Any], *, constraint_budget: float = 1.0) -> None:
        RecordConstructorArgs.__init__(self, constraint_budget=constraint_budget)
        super().__init__(env)
        self.constraint_budget = float(constraint_budget)
        self._spent = 0.0

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        self._spent = 0.0
        observation, info = self.env.reset(**kwargs)
        return observation, self._with_cost(info)

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        info = self._with_cost(info)
        return observation, float(reward), terminated, truncated, info

    def _with_cost(self, info: dict[str, Any]) -> dict[str, Any]:
        payload = dict(info)
        if "cost" in payload and "cost_components" in payload:
            cost_signal = float(payload["cost"])
            self._spent += cost_signal
            payload["cost_signal"] = cost_signal
            payload["constraint_budget_remaining"] = max(self.constraint_budget - self._spent, 0.0)
            return payload
        flags = payload.get("constraint_flags", {})
        cost_signal, components = safety_cost_from_flags(flags)
        self._spent += cost_signal
        payload["cost_signal"] = cost_signal
        payload["cost_components"] = components
        payload["constraint_budget_remaining"] = max(self.constraint_budget - self._spent, 0.0)
        return payload


class NaNObservationWrapper(gym.ObservationWrapper[Any, Any, Any], RecordConstructorArgs):
    """Convert dict observations with NaN values into RL-friendly vectors."""

    def __init__(
        self,
        env: gym.Env[Any, Any],
        *,
        sentinel: float = -1.0,
        include_mask: bool = True,
    ) -> None:
        RecordConstructorArgs.__init__(
            self,
            sentinel=sentinel,
            include_mask=include_mask,
        )
        super().__init__(env)
        observation_space = env.observation_space
        if not isinstance(observation_space, gym.spaces.Dict):
            raise TypeError("NaNObservationWrapper requires a Dict observation space.")
        self.sentinel = float(sentinel)
        self.include_mask = include_mask
        self.observation_keys = list(observation_space.spaces.keys())
        width = len(self.observation_keys) * (2 if include_mask else 1)
        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(width,),
            dtype=np.float32,
        )

    def observation(self, observation: dict[str, Any]) -> np.ndarray:
        values: list[float] = []
        mask: list[float] = []
        for key in self.observation_keys:
            value = float(np.asarray(observation[key]).reshape(-1)[0])
            observed = np.isfinite(value)
            values.append(value if observed else self.sentinel)
            mask.append(1.0 if observed else 0.0)
        if self.include_mask:
            values.extend(mask)
        return np.asarray(values, dtype=np.float32)


class AgentInfoWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Attach task prompt, campaign state, and current action affordances to info."""

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        return observation, self._with_agent_info(info)

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        return observation, float(reward), terminated, truncated, self._with_agent_info(info)

    def _with_agent_info(self, info: dict[str, Any]) -> dict[str, Any]:
        base = _base_env(self.env)
        payload = dict(info)
        payload["task_prompt"] = base.task_prompt()
        payload["campaign_state"] = base.campaign_state()
        payload["available_actions"] = base.available_actions()
        return payload


class LLMObservationWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Attach deterministic LLM/student-readable observation summaries to info."""

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        return observation, self._with_views(observation, info)

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        return (
            observation,
            float(reward),
            terminated,
            truncated,
            self._with_views(observation, info),
        )

    def _with_views(self, observation: Any, info: dict[str, Any]) -> dict[str, Any]:
        payload = dict(info)
        payload["lab_report"] = observation_view(
            self.env,
            "lab_report",
            observation,
            info,
        )
        payload["tool_json"] = observation_view(
            self.env,
            "tool_json",
            observation,
            info,
        )
        return payload


class RLObservationWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Return a NaN-safe vector observation and expose mask/cost in info."""

    def __init__(
        self,
        env: gym.Env[Any, Any],
        *,
        include_mask: bool = True,
        include_cost: bool = True,
    ) -> None:
        RecordConstructorArgs.__init__(
            self,
            include_mask=include_mask,
            include_cost=include_cost,
        )
        super().__init__(env)
        self.include_mask = include_mask
        self.include_cost = include_cost
        if not isinstance(env.observation_space, gym.spaces.Dict):
            raise TypeError("RLObservationWrapper requires a Dict observation space.")
        spec = rl_observation_spec(include_cost=include_cost)
        self.observation_keys = list(spec["keys"])
        value_low = list(spec["value_bounds"]["low"])
        value_high = list(spec["value_bounds"]["high"])
        mask_low = list(spec["mask_bounds"]["low"])
        mask_high = list(spec["mask_bounds"]["high"])
        low = [*value_low, *mask_low] if include_mask else value_low
        high = [*value_high, *mask_high] if include_mask else value_high
        self.observation_space = gym.spaces.Box(
            low=np.asarray(low, dtype=np.float32),
            high=np.asarray(high, dtype=np.float32),
            shape=(len(low),),
            dtype=np.float32,
        )

    def reset(self, **kwargs: Any) -> tuple[np.ndarray, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        vector, payload = self._vectorize(observation, info)
        return vector, payload

    def step(self, action: Any) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        vector, payload = self._vectorize(observation, info)
        return vector, float(reward), terminated, truncated, payload

    def _vectorize(
        self,
        observation: Any,
        info: dict[str, Any],
    ) -> tuple[np.ndarray, dict[str, Any]]:
        view = rl_observation_view(observation, info, include_cost=self.include_cost)
        values = list(view["vector"])
        mask = list(view["mask"])
        vector_values = [*values, *mask] if self.include_mask else values
        payload = dict(info)
        payload["rl_view"] = view
        payload["observation_mask"] = np.asarray(mask, dtype=np.float32)
        payload["cost_signal"] = float(view["cost"])
        return np.asarray(vector_values, dtype=np.float32), payload


class ContinuousEventActionWrapper(gym.ActionWrapper[Any, Any, Any], RecordConstructorArgs):
    """Map masked operation logits plus parameters onto a typed event action.

    Operation coordinates retain fixed global semantics and are filtered by the
    same public affordance mask exposed in the observation. This avoids imposing
    a false ordinal geometry on operation categories while keeping a Box action
    space shared by PPO and SAC. Parameter coordinates remain stationary.
    """

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)
        if not isinstance(env.action_space, gym.spaces.Dict):
            raise TypeError("ContinuousEventActionWrapper requires a Dict action space")
        self.event_action_space = env.action_space
        self.action_keys = tuple(self.event_action_space.spaces)
        self.parameter_keys = tuple(key for key in self.action_keys if key != "operation")
        self.operation_types = tuple(OPERATION_TYPES)
        self.operation_logit_count = len(self.operation_types)
        self.action_space = gym.spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(self.operation_logit_count + len(self.parameter_keys),),
            dtype=np.float32,
        )

    def action_contract(self) -> dict[str, Any]:
        return {
            "schema_version": "chemworld-continuous-event-action-0.3",
            "action_keys": list(self.action_keys),
            "operation_types": list(self.operation_types),
            "operation_logit_count": self.operation_logit_count,
            "parameter_keys": list(self.parameter_keys),
            "shape": list(self.action_space.shape or ()),
            "low": -1.0,
            "high": 1.0,
            "operation_mapping": (
                "fixed global logits decoded by argmax after public affordance mask"
            ),
            "parameter_discrete_mapping": "fixed global index; floor(unit_coordinate * n)",
            "empty_operation_mask_policy": "retain global argmax and record the resulting failure",
            "invalid_payload_policy": "retain environment precondition or domain failure",
            "execution_numeric_policy": (
                "normalize numpy values to their JSON trajectory representation before execution"
            ),
        }

    def action(self, action: Any) -> dict[str, Any]:
        return decode_continuous_event_action(
            action,
            event_action_space=self.event_action_space,
            operation_mask=action_mask(self.env),
        )


class RLControlObservationWrapper(gym.ObservationWrapper[Any, Any, Any], RecordConstructorArgs):
    """Append operation affordances and normalized campaign progress to RL observations."""

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)
        if not isinstance(env.observation_space, gym.spaces.Box):
            raise TypeError("RLControlObservationWrapper requires a Box observation space")
        base_low = np.asarray(env.observation_space.low, dtype=np.float32).reshape(-1)
        base_high = np.asarray(env.observation_space.high, dtype=np.float32).reshape(-1)
        extra_low = np.zeros(len(OPERATION_TYPES) + 3, dtype=np.float32)
        extra_high = np.ones(len(OPERATION_TYPES) + 3, dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low=np.concatenate([base_low, extra_low]),
            high=np.concatenate([base_high, extra_high]),
            dtype=np.float32,
        )

    def observation(self, observation: Any) -> np.ndarray:
        vector = np.asarray(observation, dtype=np.float32).reshape(-1)
        base = _base_env(self.env)
        budget = max(int(getattr(base, "budget", 1)), 1)
        step = max(int(getattr(base, "_step_count", 0)), 0)
        experiment = max(int(getattr(base, "_experiment_index", 0)), 0)
        summaries = list(getattr(base, "_experiment_summaries", []))
        progress = np.asarray(
            [
                min(step / budget, 1.0),
                min(max(budget - step, 0) / budget, 1.0),
                min(len(summaries) / max(experiment + 1, 1), 1.0),
            ],
            dtype=np.float32,
        )
        affordances = np.asarray(action_mask(self.env), dtype=np.float32)
        combined = np.concatenate([vector, affordances, progress]).astype(np.float32)
        if not self.observation_space.contains(combined):
            raise ValueError("RL control observation escaped its declared finite bounds")
        return combined


class RLTrainingRewardWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Add auditable public-signal shaping for operation-level RL training.

    The wrapper never changes observations, actions, termination, or the raw
    benchmark score. Frozen-policy evaluation must omit this wrapper and use
    replayed task metrics. Shaping exists only to make invalid preconditions and
    completed experiments distinguishable to a learner.
    """

    SCHEMA_VERSION = "chemworld-rl-training-reward-0.1"

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)
        self._previous_valid_operations: set[str] = set()
        self._diagnostics = self._empty_diagnostics()

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        self._previous_valid_operations = self._valid_operations()
        self._diagnostics["episode_count"] += 1
        return observation, info

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, raw_reward, terminated, truncated, info = self.env.step(action)
        flags = dict(info.get("constraint_flags", {}))
        invalid = bool(flags.get("precondition_failed", False))
        current_valid = self._valid_operations()
        newly_unlocked = len(current_valid.difference(self._previous_valid_operations))
        operation = str(info.get("operation_type", ""))
        experiment_ended = bool(info.get("experiment_ended", False))
        shaped_reward = float(raw_reward)
        shaped_reward += -0.25 if invalid else 0.01
        shaped_reward += 0.02 * newly_unlocked
        if not invalid and operation == "measure":
            shaped_reward += 0.02
        if experiment_ended:
            shaped_reward += 1.0
        if bool(flags.get("unsafe_by_task_limit", False)):
            shaped_reward -= 0.10
        if bool(flags.get("high_cost", False)):
            shaped_reward -= 0.05

        self._previous_valid_operations = current_valid
        self._diagnostics["step_count"] += 1
        self._diagnostics["invalid_action_count"] += int(invalid)
        self._diagnostics["runtime_domain_failure_count"] += int(
            info.get("preconditions", {}).get("runtime_domain_valid") is False
        )
        self._diagnostics["measurement_count"] += int(not invalid and operation == "measure")
        self._diagnostics["completed_experiment_count"] += int(experiment_ended)
        self._diagnostics["newly_unlocked_operation_count"] += newly_unlocked
        self._diagnostics["unsafe_step_count"] += int(
            bool(flags.get("unsafe_by_task_limit", False))
        )
        self._diagnostics["high_cost_step_count"] += int(bool(flags.get("high_cost", False)))
        self._diagnostics["raw_reward_sum"] += float(raw_reward)
        self._diagnostics["shaped_reward_sum"] += shaped_reward
        payload = dict(info)
        payload["rl_training_reward"] = {
            "schema_version": self.SCHEMA_VERSION,
            "raw_reward": float(raw_reward),
            "shaped_reward": shaped_reward,
            "invalid_action": invalid,
            "newly_unlocked_operations": newly_unlocked,
            "experiment_ended": experiment_ended,
        }
        return observation, shaped_reward, terminated, truncated, payload

    def reward_contract(self) -> dict[str, Any]:
        return {
            "schema_version": self.SCHEMA_VERSION,
            "public_signals_only": True,
            "benchmark_evaluation_uses_shaped_reward": False,
            "components": {
                "raw_environment_reward": 1.0,
                "valid_operation": 0.01,
                "invalid_precondition": -0.25,
                "newly_unlocked_operation": 0.02,
                "valid_measurement": 0.02,
                "completed_experiment": 1.0,
                "unsafe_step": -0.10,
                "high_cost_step": -0.05,
            },
        }

    def training_diagnostics(self) -> dict[str, Any]:
        payload = dict(self._diagnostics)
        steps = max(int(payload["step_count"]), 1)
        payload["invalid_action_rate"] = payload["invalid_action_count"] / steps
        payload["completed_experiments_per_1000_steps"] = (
            1000.0 * payload["completed_experiment_count"] / steps
        )
        return payload

    def _valid_operations(self) -> set[str]:
        base = _base_env(self.env)
        return set(base.operation_validator.valid_operations(base._state))

    @staticmethod
    def _empty_diagnostics() -> dict[str, Any]:
        return {
            "step_count": 0,
            "episode_count": 0,
            "invalid_action_count": 0,
            "runtime_domain_failure_count": 0,
            "measurement_count": 0,
            "completed_experiment_count": 0,
            "newly_unlocked_operation_count": 0,
            "unsafe_step_count": 0,
            "high_cost_step_count": 0,
            "raw_reward_sum": 0.0,
            "shaped_reward_sum": 0.0,
        }


class ActionSuggestionWrapper(gym.Wrapper[Any, Any, Any, Any], RecordConstructorArgs):
    """Expose legal next actions without auto-correcting the submitted action."""

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)

    def reset(self, **kwargs: Any) -> tuple[Any, dict[str, Any]]:
        observation, info = self.env.reset(**kwargs)
        return observation, self._with_suggestions(info)

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.env.step(action)
        return observation, float(reward), terminated, truncated, self._with_suggestions(info)

    def _with_suggestions(self, info: dict[str, Any]) -> dict[str, Any]:
        base = _base_env(self.env)
        payload = dict(info)
        suggestions = base.available_actions()
        payload["action_suggestions"] = suggestions
        if payload.get("constraint_flags", {}).get("precondition_failed", False):
            operation_names = [entry["operation"] for entry in suggestions[:4]]
            payload["recovery_suggestion"] = "Try one of the currently valid operations: " + (
                ", ".join(operation_names) if operation_names else "none"
            )
        return payload
