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


def _jsonish_mismatches(
    *,
    step: int,
    field: str,
    recorded: Any,
    replayed: Any,
    tolerance: float,
) -> list[dict[str, Any]]:
    """Compare replay metadata while tolerating deterministic float roundoff."""

    if isinstance(recorded, bool) or isinstance(replayed, bool):
        if recorded == replayed:
            return []
        return [
            {
                "step": step,
                "field": field,
                "recorded": recorded,
                "replayed": replayed,
                "abs_error": None,
            }
        ]
    if isinstance(recorded, float | int) and isinstance(replayed, float | int):
        error = abs(float(recorded) - float(replayed))
        if error <= tolerance:
            return []
        return [
            {
                "step": step,
                "field": field,
                "recorded": recorded,
                "replayed": replayed,
                "abs_error": error,
            }
        ]
    if isinstance(recorded, dict) and isinstance(replayed, dict):
        mismatches: list[dict[str, Any]] = []
        recorded_keys = set(recorded)
        replayed_keys = set(replayed)
        for key in sorted(recorded_keys | replayed_keys):
            child_field = f"{field}.{key}"
            if key not in recorded or key not in replayed:
                mismatches.append(
                    {
                        "step": step,
                        "field": child_field,
                        "recorded": recorded.get(key),
                        "replayed": replayed.get(key),
                        "abs_error": None,
                    }
                )
                continue
            mismatches.extend(
                _jsonish_mismatches(
                    step=step,
                    field=child_field,
                    recorded=recorded[key],
                    replayed=replayed[key],
                    tolerance=tolerance,
                )
            )
        return mismatches
    if isinstance(recorded, list) and isinstance(replayed, list):
        mismatches = []
        if len(recorded) != len(replayed):
            mismatches.append(
                {
                    "step": step,
                    "field": f"{field}.length",
                    "recorded": len(recorded),
                    "replayed": len(replayed),
                    "abs_error": None,
                }
            )
        for index, recorded_item in enumerate(recorded[: len(replayed)]):
            mismatches.extend(
                _jsonish_mismatches(
                    step=step,
                    field=f"{field}.{index}",
                    recorded=recorded_item,
                    replayed=replayed[index],
                    tolerance=tolerance,
                )
            )
        return mismatches
    if recorded != replayed:
        return [
            {
                "step": step,
                "field": field,
                "recorded": recorded,
                "replayed": replayed,
                "abs_error": None,
            }
        ]
    return []


def verify_records(
    records: list[dict[str, Any]],
    *,
    tolerance: float = 1.0e-5,
) -> VerificationResult:
    """Replay trajectory actions and compare deterministic observations/rewards."""

    validate_records(records)
    first = records[0]
    benchmark_task_id = first.get("benchmark_task_id")
    if benchmark_task_id:
        env_kwargs: dict[str, Any] = {
            "task_id": str(benchmark_task_id),
            "seed": int(first["seed"]),
        }
    else:
        env_kwargs = {
            "world_split": first["world_split"],
            "budget": int(first.get("budget", len(records))),
            "objective": _objective_from_record(first),
            "seed": int(first["seed"]),
        }
    env = gym.make(
        first["env_id"],
        **env_kwargs,
    )
    _, reset_info = env.reset(seed=int(first["seed"]))
    recorded_mechanism_hash = first.get("mechanism_hash")
    replay_mechanism_hash = reset_info.get("mechanism_hash")
    early_mismatches: list[dict[str, Any]] = []
    if recorded_mechanism_hash and replay_mechanism_hash != recorded_mechanism_hash:
        early_mismatches.append(
            {
                "step": 0,
                "field": "mechanism_hash",
                "recorded": recorded_mechanism_hash,
                "replayed": replay_mechanism_hash,
                "abs_error": None,
            }
        )

    mismatches: list[dict[str, Any]] = list(early_mismatches)
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
            replay_metadata_fields = (
                "mechanism_id",
                "mechanism_hash",
                "kernel_id",
                "kernel_version",
                "affected_ledgers",
                "world_events",
                "state_patches_summary",
                "transaction_status",
                "rollback_reason",
                "state_delta_summary",
            )
            for field in replay_metadata_fields:
                if field not in record:
                    continue
                replayed_metadata = info.get(field)
                field_mismatches = _jsonish_mismatches(
                    step=int(record["step"]),
                    field=field,
                    recorded=record[field],
                    replayed=replayed_metadata,
                    tolerance=tolerance,
                )
                mismatches.extend(field_mismatches)
                for mismatch in field_mismatches:
                    abs_error = mismatch.get("abs_error")
                    if abs_error is not None:
                        max_abs_error = max(max_abs_error, float(abs_error))
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
