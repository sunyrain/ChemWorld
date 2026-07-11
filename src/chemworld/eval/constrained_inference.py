"""Deterministic paired noninferiority inference for benchmark constraints."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import numpy as np

CONSTRAINED_INFERENCE_VERSION = "chemworld-constrained-inference-0.1"


def paired_constraint_decisions(
    results: Sequence[Mapping[str, Any]],
    *,
    task_ids: Iterable[str],
    candidate: str,
    comparator: str,
    paired_seeds: Sequence[int],
    bootstrap_samples: int,
    upper_quantile: float,
    safety_margin: float,
    cost_margin: float,
) -> dict[str, Any]:
    """Evaluate task-level safety and cost noninferiority on paired runs."""

    if bootstrap_samples < 5_000:
        raise ValueError("constraint inference requires at least 5,000 bootstrap samples")
    if not 0.5 < upper_quantile < 1.0:
        raise ValueError("upper_quantile must be between 0.5 and 1")
    for name, margin in (("safety_margin", safety_margin), ("cost_margin", cost_margin)):
        if not math.isfinite(margin) or margin < 0.0:
            raise ValueError(f"{name} must be finite and non-negative")
    expected_seeds = tuple(int(seed) for seed in paired_seeds)
    if not expected_seeds or len(set(expected_seeds)) != len(expected_seeds):
        raise ValueError("paired_seeds must be non-empty and unique")

    task_decisions: dict[str, Any] = {}
    for task_id in task_ids:
        paired = _paired_rows(
            results,
            task_id=str(task_id),
            candidate=candidate,
            comparator=comparator,
            expected_seeds=expected_seeds,
        )
        safety_effects: list[float] = []
        cost_effects: list[float] = []
        for seed, candidate_row, comparator_row in paired:
            candidate_safety = _risk_exceedance_rate(candidate_row)
            comparator_safety = _risk_exceedance_rate(comparator_row)
            candidate_cost = _cost_per_experiment(candidate_row)
            comparator_cost = _cost_per_experiment(comparator_row)
            if comparator_cost <= 0.0:
                raise ValueError(f"{task_id}/seed{seed} comparator cost must be positive")
            safety_effects.append(candidate_safety - comparator_safety)
            cost_effects.append((candidate_cost - comparator_cost) / comparator_cost)

        safety_card = _noninferiority_card(
            safety_effects,
            task_id=str(task_id),
            metric="risk_budget_exceedance_rate",
            effect="candidate_minus_comparator_absolute_rate",
            margin=safety_margin,
            bootstrap_samples=bootstrap_samples,
            upper_quantile=upper_quantile,
        )
        cost_card = _noninferiority_card(
            cost_effects,
            task_id=str(task_id),
            metric="campaign_total_cost_per_complete_experiment",
            effect="candidate_minus_comparator_relative_to_comparator",
            margin=cost_margin,
            bootstrap_samples=bootstrap_samples,
            upper_quantile=upper_quantile,
        )
        task_decisions[str(task_id)] = {
            "paired_seed_count": len(paired),
            "safety": safety_card,
            "cost": cost_card,
            "constraints_passed": bool(
                safety_card["noninferiority_passed"]
                and cost_card["noninferiority_passed"]
            ),
        }
    return {
        "schema_version": CONSTRAINED_INFERENCE_VERSION,
        "candidate": candidate,
        "comparator": comparator,
        "bootstrap_samples": bootstrap_samples,
        "simultaneous_upper_quantile": upper_quantile,
        "task_decisions": task_decisions,
        "all_task_constraints_passed": all(
            card["constraints_passed"] for card in task_decisions.values()
        ),
    }


def _paired_rows(
    results: Sequence[Mapping[str, Any]],
    *,
    task_id: str,
    candidate: str,
    comparator: str,
    expected_seeds: tuple[int, ...],
) -> list[tuple[int, Mapping[str, Any], Mapping[str, Any]]]:
    indexed: dict[tuple[str, int], Mapping[str, Any]] = {}
    for row in results:
        if str(row.get("task_id")) != task_id:
            continue
        method = str(row.get("baseline_agent"))
        if method not in {candidate, comparator}:
            continue
        key = (method, int(row.get("seed", -1)))
        if key in indexed:
            raise ValueError(f"duplicate result row for {task_id}/{method}/seed{key[1]}")
        indexed[key] = row
    missing = [
        (method, seed)
        for seed in expected_seeds
        for method in (candidate, comparator)
        if (method, seed) not in indexed
    ]
    unexpected = sorted(
        key for key in indexed if key[1] not in set(expected_seeds)
    )
    if missing or unexpected:
        raise ValueError(
            f"paired constraint matrix mismatch for {task_id}; missing={missing}, "
            f"unexpected={unexpected}"
        )
    return [
        (seed, indexed[(candidate, seed)], indexed[(comparator, seed)])
        for seed in expected_seeds
    ]


def _risk_exceedance_rate(result: Mapping[str, Any]) -> float:
    constraints = result.get("score_replay", {}).get("layered_evaluation", {}).get(
        "constraints", {}
    )
    value = float(constraints.get("risk_budget_exceedance_rate", math.nan))
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("result has an invalid risk-budget exceedance rate")
    return value


def _cost_per_experiment(result: Mapping[str, Any]) -> float:
    resources = result.get("score_replay", {}).get("layered_evaluation", {}).get(
        "resources", {}
    )
    cost = float(resources.get("campaign_total_cost", math.nan))
    experiments = int(resources.get("complete_experiment_count", 0))
    if not math.isfinite(cost) or cost < 0.0 or experiments <= 0:
        raise ValueError("result has an invalid campaign cost or experiment count")
    return cost / experiments


def _noninferiority_card(
    effects: Sequence[float],
    *,
    task_id: str,
    metric: str,
    effect: str,
    margin: float,
    bootstrap_samples: int,
    upper_quantile: float,
) -> dict[str, Any]:
    values = np.asarray(effects, dtype=float)
    if values.ndim != 1 or values.size < 2 or not np.all(np.isfinite(values)):
        raise ValueError("paired constraint effects must contain at least two finite values")
    seed_material = f"{CONSTRAINED_INFERENCE_VERSION}|{task_id}|{metric}".encode()
    rng_seed = int.from_bytes(hashlib.sha256(seed_material).digest()[:8], "big")
    rng = np.random.default_rng(rng_seed)
    indices = rng.integers(0, values.size, size=(bootstrap_samples, values.size))
    bootstrap_means = values[indices].mean(axis=1)
    upper_bound = float(np.quantile(bootstrap_means, upper_quantile, method="higher"))
    mean_effect = float(values.mean())
    return {
        "metric": metric,
        "effect": effect,
        "paired_effects": values.tolist(),
        "mean_paired_effect": mean_effect,
        "simultaneous_upper_confidence_bound": upper_bound,
        "maximum_noninferiority_margin": margin,
        "noninferiority_passed": upper_bound <= margin,
    }


__all__ = ["CONSTRAINED_INFERENCE_VERSION", "paired_constraint_decisions"]
