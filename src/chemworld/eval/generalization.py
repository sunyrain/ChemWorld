"""Public OOD diagnostics for the frozen serious benchmark."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.validity_power import audit_validity_power
from chemworld.tasks import SERIOUS_TASK_IDS, get_task

GENERALIZATION_AUDIT_VERSION = "chemworld-generalization-audit-0.1"
PUBLICATION_SHIFT_AUDIT_VERSION = "chemworld-publication-shift-audit-0.1"


def compare_public_and_ood_reports(
    public_report: dict[str, Any],
    ood_report: dict[str, Any],
    *,
    ood_seeds: tuple[int, ...],
) -> dict[str, Any]:
    """Compare official public baselines with held-out, non-leaderboard seeds."""

    public_rows = _index_rows(public_report)
    ood_rows = _index_rows(ood_report)
    tasks: dict[str, dict[str, Any]] = {}
    for task_id in SERIOUS_TASK_IDS:
        primary_field = PRIMARY_METRIC_FIELDS[task_id]
        agent_rows: list[dict[str, Any]] = []
        public_scores: list[float] = []
        ood_scores: list[float] = []
        invalid_rates: list[float] = []
        assay_counts: list[float] = []
        for agent_name in SERIOUS_BASELINE_AGENTS:
            public = public_rows[(task_id, agent_name)]
            ood = ood_rows[(task_id, agent_name)]
            public_score = float(public["mean_total_score"])
            ood_score = float(ood["mean_total_score"])
            public_primary = float(public[primary_field])
            ood_primary = float(ood[primary_field])
            public_scores.append(public_score)
            ood_scores.append(ood_score)
            invalid_rates.append(float(ood["mean_invalid_action_rate"]))
            assay_counts.append(float(ood["mean_final_assay_count"]))
            agent_rows.append(
                {
                    "agent_name": agent_name,
                    "public_mean_total_score": public_score,
                    "ood_mean_total_score": ood_score,
                    "score_shift": ood_score - public_score,
                    "public_mean_primary_metric": public_primary,
                    "ood_mean_primary_metric": ood_primary,
                    "primary_metric_shift": ood_primary - public_primary,
                }
            )
        ood_spread = max(ood_scores) - min(ood_scores)
        tasks[task_id] = {
            "task_contract_hash": get_task(task_id).contract_hash,
            "primary_metric_field": primary_field,
            "public_seeds": list(get_task(task_id).seeds),
            "ood_seeds": list(ood_seeds),
            "agent_results": agent_rows,
            "score_diagnostics": {
                "ood_strategy_spread": ood_spread,
                "mean_absolute_shift": float(
                    np.mean(np.abs(np.asarray(ood_scores) - np.asarray(public_scores)))
                ),
                "rank_correlation": _rank_correlation(public_scores, ood_scores),
                "pairwise_ranking_agreement": _pairwise_agreement(
                    public_scores, ood_scores
                ),
            },
            "operational_checks": {
                "all_actions_valid": max(invalid_rates) <= 1.0e-12,
                "campaigns_complete_multiple_assays": min(assay_counts) >= 2.0,
                "strategies_remain_distinguishable": ood_spread >= 0.01,
            },
        }
    passed = all(
        all(task["operational_checks"].values()) for task in tasks.values()
    )
    return {
        "schema_version": GENERALIZATION_AUDIT_VERSION,
        "suite_id": "chemworld-serious-v1",
        "evaluation_role": "public OOD diagnostic; excluded from leaderboard scoring",
        "task_ids": list(SERIOUS_TASK_IDS),
        "baseline_agents": list(SERIOUS_BASELINE_AGENTS),
        "ood_seeds": list(ood_seeds),
        "passed": passed,
        "tasks": tasks,
    }


def compare_publication_distribution_shift(
    reference_results: list[dict[str, Any]],
    shifted_results: list[dict[str, Any]],
    *,
    shift_id: str,
    practical_effect: float = 0.05,
    bootstrap_samples: int = 10_000,
) -> dict[str, Any]:
    """Compare adaptive value and task metrics across independent seed regimes."""

    methods = {"random", "structured_gp_bo"}
    reference = [row for row in reference_results if row.get("baseline_agent") in methods]
    shifted = [row for row in shifted_results if row.get("baseline_agent") in methods]
    reference_total = audit_validity_power(
        reference,
        task_ids=tuple(SERIOUS_TASK_IDS),
        method_pairs=(("structured_gp_bo", "random"),),
        adaptive_method_pairs=(("structured_gp_bo", "random"),),
        practical_effect=practical_effect,
        planned_seed_count=20,
        bootstrap_samples=bootstrap_samples,
    )
    shifted_total = audit_validity_power(
        shifted,
        task_ids=tuple(SERIOUS_TASK_IDS),
        method_pairs=(("structured_gp_bo", "random"),),
        adaptive_method_pairs=(("structured_gp_bo", "random"),),
        practical_effect=practical_effect,
        planned_seed_count=20,
        bootstrap_samples=bootstrap_samples,
    )
    tasks: dict[str, dict[str, Any]] = {}
    for task_id in SERIOUS_TASK_IDS:
        primary_field = PRIMARY_METRIC_FIELDS[task_id]
        reference_task = [row for row in reference if row["task_id"] == task_id]
        shifted_task = [row for row in shifted if row["task_id"] == task_id]
        reference_primary = audit_validity_power(
            reference_task,
            task_ids=(task_id,),
            method_pairs=(("structured_gp_bo", "random"),),
            adaptive_method_pairs=(("structured_gp_bo", "random"),),
            metric=primary_field,
            practical_effect=practical_effect,
            planned_seed_count=20,
            bootstrap_samples=bootstrap_samples,
        )
        shifted_primary = audit_validity_power(
            shifted_task,
            task_ids=(task_id,),
            method_pairs=(("structured_gp_bo", "random"),),
            adaptive_method_pairs=(("structured_gp_bo", "random"),),
            metric=primary_field,
            practical_effect=practical_effect,
            planned_seed_count=20,
            bootstrap_samples=bootstrap_samples,
        )
        comparison_key = "structured_gp_bo__minus__random"
        reference_score_effect = reference_total["tasks"][task_id]["comparisons"][
            comparison_key
        ]
        shifted_score_effect = shifted_total["tasks"][task_id]["comparisons"][
            comparison_key
        ]
        reference_primary_effect = reference_primary["tasks"][task_id]["comparisons"][
            comparison_key
        ]
        shifted_primary_effect = shifted_primary["tasks"][task_id]["comparisons"][
            comparison_key
        ]
        checks = {
            "total_effect_direction_preserved": reference_score_effect[
                "mean_paired_effect"
            ]
            > 0.0
            and shifted_score_effect["mean_paired_effect"] > 0.0,
            "primary_effect_direction_preserved": reference_primary_effect[
                "mean_paired_effect"
            ]
            > 0.0
            and shifted_primary_effect["mean_paired_effect"] > 0.0,
            "shifted_total_effect_ci_positive": shifted_score_effect[
                "paired_bootstrap_ci"
            ][0]
            > 0.0,
            "shifted_primary_effect_ci_positive": shifted_primary_effect[
                "paired_bootstrap_ci"
            ][0]
            > 0.0,
            "shifted_actions_valid": max(
                float(row.get("invalid_action_rate", 1.0)) for row in shifted_task
            )
            <= 1.0e-12,
            "shifted_experiment_count_complete": min(
                int(row.get("resource_usage", {}).get("complete_experiment_count", 0))
                for row in shifted_task
            )
            == 40,
        }
        tasks[task_id] = {
            "primary_result_field": primary_field,
            "reference_total_score_effect": reference_score_effect,
            "shifted_total_score_effect": shifted_score_effect,
            "total_score_effect_shift": shifted_score_effect["mean_paired_effect"]
            - reference_score_effect["mean_paired_effect"],
            "reference_primary_effect": reference_primary_effect,
            "shifted_primary_effect": shifted_primary_effect,
            "primary_effect_shift": shifted_primary_effect["mean_paired_effect"]
            - reference_primary_effect["mean_paired_effect"],
            "method_mean_score_shift": {
                method: _method_mean(shifted_task, method, "total_score")
                - _method_mean(reference_task, method, "total_score")
                for method in sorted(methods)
            },
            "checks": checks,
            "ready": all(checks.values()),
        }
    return {
        "schema_version": PUBLICATION_SHIFT_AUDIT_VERSION,
        "shift_id": shift_id,
        "methods": sorted(methods),
        "task_count": len(tasks),
        "ready_task_count": sum(task["ready"] for task in tasks.values()),
        "passed": all(task["ready"] for task in tasks.values()),
        "tasks": tasks,
    }


def _method_mean(rows: list[dict[str, Any]], method: str, metric: str) -> float:
    values = [float(row[metric]) for row in rows if row["baseline_agent"] == method]
    if len(values) != 20:
        raise ValueError(f"Expected 20 {method!r} rows for {metric!r}, got {len(values)}")
    return float(np.mean(values))


def _index_rows(report: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = report.get("summary_rows")
    if not isinstance(rows, list):
        raise ValueError("baseline report must contain summary_rows")
    indexed = {
        (str(row["task_id"]), str(row["agent_name"])): row
        for row in rows
        if isinstance(row, dict)
    }
    expected = {
        (task_id, agent_name)
        for task_id in SERIOUS_TASK_IDS
        for agent_name in SERIOUS_BASELINE_AGENTS
    }
    missing = sorted(expected - set(indexed))
    if missing:
        raise ValueError(f"baseline report is missing task/agent rows: {missing}")
    return indexed


def _rank_correlation(left: list[float], right: list[float]) -> float:
    left_rank = _average_ranks(left)
    right_rank = _average_ranks(right)
    if float(np.std(left_rank)) == 0.0 or float(np.std(right_rank)) == 0.0:
        return 0.0
    return float(np.corrcoef(left_rank, right_rank)[0, 1])


def _average_ranks(values: list[float]) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    order = np.argsort(array, kind="mergesort")
    ranks = np.empty(len(array), dtype=float)
    index = 0
    while index < len(array):
        end = index + 1
        while end < len(array) and array[order[end]] == array[order[index]]:
            end += 1
        ranks[order[index:end]] = 0.5 * (index + end - 1)
        index = end
    return ranks


def _pairwise_agreement(left: list[float], right: list[float]) -> float:
    agreements: list[bool] = []
    for first in range(len(left)):
        for second in range(first + 1, len(left)):
            left_delta = left[first] - left[second]
            right_delta = right[first] - right[second]
            if left_delta == 0.0 or right_delta == 0.0:
                continue
            agreements.append((left_delta > 0.0) == (right_delta > 0.0))
    return float(np.mean(agreements)) if agreements else 0.0


__all__ = [
    "GENERALIZATION_AUDIT_VERSION",
    "PUBLICATION_SHIFT_AUDIT_VERSION",
    "compare_public_and_ood_reports",
    "compare_publication_distribution_shift",
]
