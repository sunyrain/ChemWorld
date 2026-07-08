"""Trajectory logging utilities."""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from chemworld import __version__
from chemworld.data.schema import TRAJECTORY_SCHEMA_VERSION


def to_builtin(value: Any) -> Any:
    """Convert numpy-heavy values to JSON-safe Python objects."""

    if isinstance(value, np.ndarray):
        if value.size == 1:
            return to_builtin(float(value.reshape(-1)[0]))
        return [to_builtin(item) for item in value.tolist()]
    if isinstance(value, np.generic):
        return to_builtin(value.item())
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): to_builtin(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [to_builtin(item) for item in value]
    return value


def observation_to_json(observation: dict[str, Any]) -> dict[str, float | None]:
    payload: dict[str, float | None] = {}
    for key, value in observation.items():
        converted = to_builtin(value)
        payload[key] = None if converted is None else float(converted)
    return payload


def action_payload(action: dict[str, Any]) -> dict[str, Any]:
    return to_builtin(action)


class TrajectoryLogger:
    """Append-only JSONL logger for benchmark trajectories."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("w", encoding="utf-8")

    def close(self) -> None:
        self._handle.close()

    def __enter__(self) -> TrajectoryLogger:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        del exc_type, exc, tb
        self.close()

    def log(
        self,
        *,
        task_info: dict[str, Any],
        step: int,
        action: dict[str, Any],
        observation: dict[str, Any],
        reward: float,
        terminated: bool,
        truncated: bool,
        info: dict[str, Any],
        agent_metadata: dict[str, Any],
        explanation: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "schema_version": TRAJECTORY_SCHEMA_VERSION,
            "env_version": info.get("env_version", __version__),
            "world_family_version": info.get(
                "world_family_version",
                task_info.get("world_family_version"),
            ),
            "task_id": (
                f"{task_info['env_id']}:{task_info['world_split']}:"
                f"{task_info['objective']}:seed-{task_info['seed']}"
            ),
            "env_id": task_info["env_id"],
            "benchmark_task_id": task_info.get("task_id"),
            "world_split": task_info["world_split"],
            "world_provider": task_info.get("world_provider"),
            "objective": task_info["objective"],
            "budget": int(task_info["budget"]),
            "episode_mode": task_info.get("episode_mode", "single_experiment"),
            "safety_limit": float(task_info.get("safety_limit", 0.65)),
            "kernel_maturity": to_builtin(task_info.get("kernel_maturity", {})),
            "physics_maturity": task_info.get("physics_maturity"),
            "proxy_allowed": bool(task_info.get("proxy_allowed", False)),
            "world_id": task_info["world_id"],
            "seed": int(task_info["seed"]),
            "step": step,
            "campaign_id": info.get(
                "campaign_id",
                f"{task_info.get('task_id') or 'adhoc'}:{task_info.get('seed')}",
            ),
            "experiment_index": int(info.get("experiment_index", 0)),
            "operation_id": int(info.get("operation_id", step)),
            "scenario_id": info.get("scenario_id", task_info.get("scenario_id")),
            "initial_state_id": info.get("initial_state_id", task_info.get("initial_state_id")),
            "action": action_payload(action),
            "observation": observation_to_json(observation),
            "reward": float(reward),
            "terminated": bool(terminated),
            "truncated": bool(truncated),
            "constraint_flags": to_builtin(info.get("constraint_flags", {})),
            "operation_type": info.get("operation_type"),
            "preconditions": to_builtin(info.get("preconditions", {})),
            "state_delta_summary": to_builtin(info.get("state_delta_summary", {})),
            "constitution_checks": to_builtin(info.get("constitution_checks", [])),
            "instrument": info.get("instrument"),
            "instrument_source": info.get("instrument_source"),
            "observed_keys": to_builtin(info.get("observed_keys", [])),
            "observed_mask": to_builtin(info.get("observed_mask", {})),
            "raw_signal": to_builtin(info.get("raw_signal", {})),
            "processed_estimate": to_builtin(info.get("processed_estimate", {})),
            "uncertainty": to_builtin(info.get("uncertainty", {})),
            "measurement_cost": float(info.get("measurement_cost", 0.0)),
            "sample_consumed": float(info.get("sample_consumed", 0.0)),
            "observed_reward": float(info.get("observed_reward", reward)),
            "leaderboard_score": to_builtin(info.get("leaderboard_score")),
            "reward_source": info.get("reward_source"),
            "agent_metadata": to_builtin(agent_metadata),
            "timestamp": datetime.now(UTC).isoformat(),
            "explanation": explanation or {},
        }
        self._handle.write(json.dumps(payload, sort_keys=True) + "\n")
        self._handle.flush()


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
