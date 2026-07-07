"""Versioned trajectory schema."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

TRAJECTORY_SCHEMA_VERSION = "chemworld-trajectory-0.1"


@dataclass(frozen=True)
class TrajectoryRecordPayload:
    schema_version: str
    env_version: str
    world_family_version: str
    task_id: str
    env_id: str
    benchmark_task_id: str | None
    world_split: str
    objective: str
    budget: int
    episode_mode: str
    safety_limit: float
    world_id: str
    seed: int
    step: int
    action: dict[str, Any]
    observation: dict[str, float | None]
    reward: float
    terminated: bool
    truncated: bool
    constraint_flags: dict[str, bool]
    agent_metadata: dict[str, Any]
    timestamp: str
    operation_type: str | None = None
    preconditions: dict[str, bool] = field(default_factory=dict)
    state_delta_summary: dict[str, float] = field(default_factory=dict)
    constitution_checks: list[dict[str, Any]] = field(default_factory=list)
    instrument: str | None = None
    instrument_source: str | None = None
    observed_keys: list[str] = field(default_factory=list)
    observed_mask: dict[str, bool] = field(default_factory=dict)
    raw_signal: dict[str, Any] = field(default_factory=dict)
    processed_estimate: dict[str, float | None] = field(default_factory=dict)
    uncertainty: dict[str, float] = field(default_factory=dict)
    measurement_cost: float = 0.0
    sample_consumed: float = 0.0
    observed_reward: float = 0.0
    leaderboard_score: float | None = None
    reward_source: str | None = None
    explanation: dict[str, Any] = field(default_factory=dict)
