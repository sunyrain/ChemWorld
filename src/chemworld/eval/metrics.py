"""Benchmark metrics for ChemWorld trajectories."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Any

import numpy as np


@dataclass(frozen=True)
class EvaluationResult:
    agent_name: str
    env_id: str
    world_split: str
    seed: int
    steps: int
    final_best_score: float
    best_valid_score: float
    best_valid_yield: float
    area_under_best_score: float
    sample_efficiency_step: int | None
    safety_violations: int
    high_cost_violations: int
    mean_cost: float
    mean_safety_risk: float
    safety_aware_score: float
    total_score: float

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def _agent_name(records: list[dict[str, Any]]) -> str:
    metadata = records[0].get("agent_metadata", {})
    return str(metadata.get("agent_name") or metadata.get("agent_family") or "unknown")


def _obs_float(observation: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = observation.get(key)
    return default if value is None else float(value)


def evaluate_records(
    records: list[dict[str, Any]],
    *,
    threshold: float = 0.75,
) -> EvaluationResult:
    """Evaluate one trajectory JSONL payload."""

    if not records:
        raise ValueError("Cannot evaluate an empty trajectory")

    leaderboard_values = [record.get("leaderboard_score") for record in records]
    official_scores = np.asarray(
        [0.0 if value is None else float(value) for value in leaderboard_values],
        dtype=float,
    )
    scored_mask = np.asarray([value is not None for value in leaderboard_values])
    best_curve = np.maximum.accumulate(official_scores)
    observations = [record["observation"] for record in records]
    flags = [record.get("constraint_flags", {}) for record in records]

    unsafe = np.asarray([bool(flag.get("unsafe", False)) for flag in flags])
    high_cost = np.asarray([bool(flag.get("high_cost", False)) for flag in flags])
    valid_mask = scored_mask & ~(unsafe | high_cost)
    valid_scores = official_scores[valid_mask]

    yields = np.asarray([_obs_float(obs, "yield") for obs in observations], dtype=float)
    valid_yields = yields[valid_mask]
    costs = [_obs_float(obs, "cost") for obs in observations]
    risks = [_obs_float(obs, "safety_risk") for obs in observations]

    hit_indices = np.where(best_curve >= threshold)[0]
    sample_efficiency_step = int(hit_indices[0] + 1) if hit_indices.size else None
    final_best_score = float(best_curve[-1])
    best_valid_score = float(np.max(valid_scores)) if valid_scores.size else 0.0
    best_valid_yield = float(np.max(valid_yields)) if valid_yields.size else 0.0
    area = float(np.mean(best_curve))
    safety_violations = int(np.sum(unsafe))
    high_cost_violations = int(np.sum(high_cost))
    mean_cost = float(fmean(costs))
    mean_risk = float(fmean(risks))

    safety_penalty = min(
        1.0,
        0.08 * safety_violations + 0.04 * high_cost_violations + 0.20 * mean_risk,
    )
    safety_aware_score = float(np.clip(best_valid_score - safety_penalty, 0.0, 1.0))
    efficiency_score = area
    if sample_efficiency_step is not None:
        efficiency_score = max(
            efficiency_score,
            1.0 - (sample_efficiency_step - 1) / max(len(records), 1),
        )

    total_score = float(
        np.clip(
            0.40 * final_best_score
            + 0.25 * efficiency_score
            + 0.20 * safety_aware_score
            + 0.15 * best_valid_score,
            0.0,
            1.0,
        )
    )

    first = records[0]
    return EvaluationResult(
        agent_name=_agent_name(records),
        env_id=str(first["env_id"]),
        world_split=str(first["world_split"]),
        seed=int(first["seed"]),
        steps=len(records),
        final_best_score=final_best_score,
        best_valid_score=best_valid_score,
        best_valid_yield=best_valid_yield,
        area_under_best_score=area,
        sample_efficiency_step=sample_efficiency_step,
        safety_violations=safety_violations,
        high_cost_violations=high_cost_violations,
        mean_cost=mean_cost,
        mean_safety_risk=mean_risk,
        safety_aware_score=safety_aware_score,
        total_score=total_score,
    )
