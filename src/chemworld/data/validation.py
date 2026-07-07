"""Trajectory schema validation without external JSON-schema dependencies."""

from __future__ import annotations

from typing import Any

from chemworld.data.schema import TRAJECTORY_SCHEMA_VERSION

REQUIRED_RECORD_KEYS = {
    "schema_version",
    "env_version",
    "world_family_version",
    "task_id",
    "env_id",
    "world_split",
    "objective",
    "world_id",
    "seed",
    "step",
    "action",
    "observation",
    "reward",
    "terminated",
    "truncated",
    "constraint_flags",
    "constitution_checks",
    "agent_metadata",
    "instrument",
    "instrument_source",
    "measurement_cost",
    "observed_keys",
    "observed_mask",
    "raw_signal",
    "processed_estimate",
    "uncertainty",
    "observed_reward",
    "operation_type",
    "preconditions",
    "leaderboard_score",
    "reward_source",
    "sample_consumed",
    "state_delta_summary",
    "timestamp",
    "explanation",
}

EVENT_ACTION_KEYS = {"operation"}

REQUIRED_OBSERVATION_KEYS = {
    "yield",
    "selectivity",
    "conversion",
    "cost",
    "safety_risk",
    "score",
}


def validate_record(record: dict[str, Any]) -> None:
    missing = REQUIRED_RECORD_KEYS - record.keys()
    if missing:
        raise ValueError(f"Trajectory record is missing keys: {sorted(missing)}")

    if record["schema_version"] != TRAJECTORY_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported schema_version={record['schema_version']!r}; "
            f"expected {TRAJECTORY_SCHEMA_VERSION!r}"
        )

    action_missing = EVENT_ACTION_KEYS - record["action"].keys()
    if action_missing:
        raise ValueError(f"Action is missing keys: {sorted(action_missing)}")

    observation_missing = REQUIRED_OBSERVATION_KEYS - record["observation"].keys()
    if observation_missing:
        raise ValueError(f"Observation is missing keys: {sorted(observation_missing)}")

    observed_mask = record.get("observed_mask", {})
    for key in REQUIRED_OBSERVATION_KEYS:
        raw_value = record["observation"][key]
        if raw_value is None:
            if observed_mask.get(key, False):
                raise ValueError(f"Observed key {key} cannot be null")
            continue
        value = float(raw_value)
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Observation {key}={value} is outside [0, 1]")


def validate_records(records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("Trajectory is empty")

    validate_record(records[0])
    first_task = records[0]["task_id"]
    previous_step = 0
    for record in records:
        validate_record(record)
        if record["task_id"] != first_task:
            raise ValueError("A trajectory file must contain exactly one task_id")
        step = int(record["step"])
        if step != previous_step + 1:
            raise ValueError(f"Steps must be contiguous; expected {previous_step + 1}, got {step}")
        previous_step = step
