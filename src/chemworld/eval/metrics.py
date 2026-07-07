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
    benchmark_task_id: str | None
    world_split: str
    seed: int
    episode_mode: str
    steps: int
    final_assay_count: int
    final_best_score: float
    best_valid_score: float
    best_valid_yield: float
    area_under_best_score: float
    sample_efficiency_step: int | None
    safety_violations: int
    high_cost_violations: int
    invalid_action_count: int
    mean_cost: float
    mean_safety_risk: float
    mean_purity: float
    mean_recovery: float
    purification_score: float
    phase_mass_balance_violations: int
    process_mass_balance_violation_count: int
    instrument_policy_violation_count: int
    precondition_failure_count: int
    campaign_area_under_best_score: float
    safety_cost: float
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
    invalid_actions = np.asarray(
        [
            bool(flag.get("precondition_failed", False))
            or bool(flag.get("constitution_failed", False))
            for flag in flags
        ]
    )
    precondition_failures = np.asarray(
        [bool(flag.get("precondition_failed", False)) for flag in flags]
    )
    phase_mass_balance_failures = np.asarray(
        [bool(flag.get("phase_mass_balance_failed", False)) for flag in flags]
    )
    instrument_policy_violations = np.asarray(
        [
            record.get("operation_type") == "measure"
            and not record.get("preconditions", {}).get("instrument_allowed_by_task", True)
            for record in records
        ]
    )
    valid_mask = scored_mask & ~(unsafe | high_cost)
    valid_scores = official_scores[valid_mask]

    yields = np.asarray([_obs_float(obs, "yield") for obs in observations], dtype=float)
    valid_yields = yields[valid_mask]
    costs = [_obs_float(obs, "cost") for obs in observations]
    risks = [_obs_float(obs, "safety_risk") for obs in observations]
    purities = [_obs_float(obs, "purity") for obs in observations if obs.get("purity") is not None]
    recoveries = [
        _obs_float(obs, "recovery") for obs in observations if obs.get("recovery") is not None
    ]
    mass_balance_errors = [
        _obs_float(obs, "process_mass_balance_error")
        for obs in observations
        if obs.get("process_mass_balance_error") is not None
    ]

    hit_indices = np.where(best_curve >= threshold)[0]
    sample_efficiency_step = int(hit_indices[0] + 1) if hit_indices.size else None
    final_best_score = float(best_curve[-1])
    best_valid_score = float(np.max(valid_scores)) if valid_scores.size else 0.0
    best_valid_yield = float(np.max(valid_yields)) if valid_yields.size else 0.0
    area = float(np.mean(best_curve))
    safety_violations = int(np.sum(unsafe))
    high_cost_violations = int(np.sum(high_cost))
    invalid_action_count = int(np.sum(invalid_actions))
    mean_cost = float(fmean(costs))
    mean_risk = float(fmean(risks))
    mean_purity = float(fmean(purities)) if purities else 0.0
    mean_recovery = float(fmean(recoveries)) if recoveries else 0.0
    mean_mass_balance_error = float(fmean(mass_balance_errors)) if mass_balance_errors else 0.0
    purification_score = float(
        np.clip(
            0.55 * mean_purity + 0.35 * mean_recovery - 0.10 * mean_mass_balance_error,
            0.0,
            1.0,
        )
    )
    process_mass_balance_violation_count = int(
        sum(error > 0.05 for error in mass_balance_errors)
    )

    safety_penalty = min(
        1.0,
        0.08 * safety_violations
        + 0.04 * high_cost_violations
        + 0.05 * invalid_action_count
        + 0.20 * mean_risk,
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
        benchmark_task_id=first.get("benchmark_task_id"),
        world_split=str(first["world_split"]),
        seed=int(first["seed"]),
        episode_mode=str(first.get("episode_mode", "single_experiment")),
        steps=len(records),
        final_assay_count=int(np.sum(scored_mask)),
        final_best_score=final_best_score,
        best_valid_score=best_valid_score,
        best_valid_yield=best_valid_yield,
        area_under_best_score=area,
        sample_efficiency_step=sample_efficiency_step,
        safety_violations=safety_violations,
        high_cost_violations=high_cost_violations,
        invalid_action_count=invalid_action_count,
        mean_cost=mean_cost,
        mean_safety_risk=mean_risk,
        mean_purity=mean_purity,
        mean_recovery=mean_recovery,
        purification_score=purification_score,
        phase_mass_balance_violations=int(np.sum(phase_mass_balance_failures)),
        process_mass_balance_violation_count=process_mass_balance_violation_count,
        instrument_policy_violation_count=int(np.sum(instrument_policy_violations)),
        precondition_failure_count=int(np.sum(precondition_failures)),
        campaign_area_under_best_score=area,
        safety_cost=safety_penalty,
        safety_aware_score=safety_aware_score,
        total_score=total_score,
    )
