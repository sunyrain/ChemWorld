"""Optional Gymnasium wrappers and event-action validators."""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium.utils import RecordConstructorArgs

from chemworld.agent_interface import observation_view, rl_observation_spec, rl_observation_view
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
    """Map a stationary normalized Box onto the complete typed event action.

    Discrete fields retain fixed global semantics. Invalid operations are not
    silently replaced with a currently legal action; the public action mask is
    supplied by :class:`RLControlObservationWrapper` so the policy can learn the
    precondition structure without changing the meaning of an action coordinate.
    """

    def __init__(self, env: gym.Env[Any, Any]) -> None:
        RecordConstructorArgs.__init__(self)
        super().__init__(env)
        if not isinstance(env.action_space, gym.spaces.Dict):
            raise TypeError("ContinuousEventActionWrapper requires a Dict action space")
        self.event_action_space = env.action_space
        self.action_keys = tuple(self.event_action_space.spaces)
        self.action_space = gym.spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(len(self.action_keys),),
            dtype=np.float32,
        )

    def action_contract(self) -> dict[str, Any]:
        return {
            "schema_version": "chemworld-continuous-event-action-0.1",
            "action_keys": list(self.action_keys),
            "shape": list(self.action_space.shape or ()),
            "low": -1.0,
            "high": 1.0,
            "discrete_mapping": "fixed global index; floor(unit_coordinate * n)",
            "invalid_operation_policy": "retain environment precondition failure",
        }

    def action(self, action: Any) -> dict[str, Any]:
        vector = np.asarray(action, dtype=np.float32).reshape(-1)
        if vector.shape != self.action_space.shape or not np.all(np.isfinite(vector)):
            expected_shape = self.action_space.shape
            raise ValueError(
                f"continuous event action must be a finite vector with shape {expected_shape}"
            )
        unit = np.clip((vector + 1.0) / 2.0, 0.0, 1.0)
        payload: dict[str, Any] = {}
        for index, key in enumerate(self.action_keys):
            space = self.event_action_space[key]
            coordinate = float(unit[index])
            if isinstance(space, gym.spaces.Discrete):
                payload[key] = min(int(coordinate * space.n), space.n - 1)
            elif isinstance(space, gym.spaces.Box):
                value = space.low + coordinate * (space.high - space.low)
                payload[key] = np.asarray(value, dtype=space.dtype)
            else:
                raise TypeError(f"unsupported event action component: {key}={type(space).__name__}")
        return payload


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
