"""Trajectory replay verification."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.data.validation import validate_records


@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    checked_steps: int
    max_abs_error: float
    mismatches: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "verified": self.verified,
            "checked_steps": self.checked_steps,
            "max_abs_error": self.max_abs_error,
            "mismatches": self.mismatches,
        }


def _objective_from_record(record: dict[str, Any]) -> str:
    if "objective" in record:
        return str(record["objective"])
    parts = str(record["task_id"]).split(":")
    if len(parts) >= 3:
        return parts[2]
    return "balanced"


def _scalar_observation(observation: dict[str, Any]) -> dict[str, float | None]:
    payload: dict[str, float | None] = {}
    for key, value in observation.items():
        scalar = float(value.reshape(-1)[0])
        payload[key] = scalar if isfinite(scalar) else None
    return payload


def verify_records(
    records: list[dict[str, Any]],
    *,
    tolerance: float = 1.0e-5,
) -> VerificationResult:
    """Replay trajectory actions and compare deterministic observations/rewards."""

    validate_records(records)
    first = records[0]
    env_kwargs: dict[str, Any] = {
        "world_split": first["world_split"],
        "budget": len(records),
        "objective": _objective_from_record(first),
        "seed": int(first["seed"]),
    }
    env = gym.make(
        first["env_id"],
        **env_kwargs,
    )
    env.reset(seed=int(first["seed"]))

    mismatches: list[dict[str, Any]] = []
    max_abs_error = 0.0
    try:
        for record in records:
            observation, reward, terminated, truncated, info = env.step(record["action"])
            replay_observation = _scalar_observation(observation)
            recorded_observation = record["observation"]

            reward_error = abs(float(record["reward"]) - float(reward))
            max_abs_error = max(max_abs_error, reward_error)
            if reward_error > tolerance:
                mismatches.append(
                    {
                        "step": record["step"],
                        "field": "reward",
                        "recorded": float(record["reward"]),
                        "replayed": float(reward),
                        "abs_error": reward_error,
                    }
                )

            for key, replayed_value in replay_observation.items():
                recorded_raw = recorded_observation[key]
                if replayed_value is None or recorded_raw is None:
                    if replayed_value is not None or recorded_raw is not None:
                        mismatches.append(
                            {
                                "step": record["step"],
                                "field": f"observation.{key}",
                                "recorded": recorded_raw,
                                "replayed": replayed_value,
                                "abs_error": None,
                            }
                        )
                    continue
                recorded_value = float(recorded_raw)
                error = abs(recorded_value - replayed_value)
                max_abs_error = max(max_abs_error, error)
                if error > tolerance:
                    mismatches.append(
                        {
                            "step": record["step"],
                            "field": f"observation.{key}",
                            "recorded": recorded_value,
                            "replayed": replayed_value,
                            "abs_error": error,
                        }
                    )

            if bool(record["terminated"]) != terminated:
                mismatches.append(
                    {
                        "step": record["step"],
                        "field": "terminated",
                        "recorded": bool(record["terminated"]),
                        "replayed": terminated,
                        "abs_error": None,
                    }
                )
            if bool(record["truncated"]) != truncated:
                mismatches.append(
                    {
                        "step": record["step"],
                        "field": "truncated",
                        "recorded": bool(record["truncated"]),
                        "replayed": truncated,
                        "abs_error": None,
                    }
                )
            if record.get("operation_type") is not None:
                replay_operation = info.get("operation_type")
                if record["operation_type"] != replay_operation:
                    mismatches.append(
                        {
                            "step": record["step"],
                            "field": "operation_type",
                            "recorded": record["operation_type"],
                            "replayed": replay_operation,
                            "abs_error": None,
                        }
                    )
            if record.get("constitution_checks"):
                recorded_checks = record["constitution_checks"]
                replay_checks = info.get("constitution_checks", [])
                if len(recorded_checks) != len(replay_checks):
                    mismatches.append(
                        {
                            "step": record["step"],
                            "field": "constitution_checks.length",
                            "recorded": len(recorded_checks),
                            "replayed": len(replay_checks),
                            "abs_error": None,
                        }
                    )
                for index, recorded_check in enumerate(recorded_checks[: len(replay_checks)]):
                    replay_check = replay_checks[index]
                    recorded_pair = (recorded_check.get("name"), recorded_check.get("passed"))
                    replay_pair = (replay_check.get("name"), replay_check.get("passed"))
                    if recorded_pair != replay_pair:
                        mismatches.append(
                            {
                                "step": record["step"],
                                "field": f"constitution_checks.{index}",
                                "recorded": recorded_pair,
                                "replayed": replay_pair,
                                "abs_error": None,
                            }
                        )
    finally:
        env.close()

    return VerificationResult(
        verified=not mismatches,
        checked_steps=len(records),
        max_abs_error=max_abs_error,
        mismatches=mismatches,
    )
