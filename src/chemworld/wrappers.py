"""Optional Gymnasium wrappers and event-action validators."""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium.utils import RecordConstructorArgs

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
            operation_type: validate_event_action({"operation": operation_type}, self.env)[
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
