"""Deterministic reporting for the two formal static-S0 task campaigns."""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import t

from chemworld.eval.provenance import file_sha256

STATIC_S0_REPORTABLE_SCHEMA_VERSION = "chemworld-static-s0-reportable-results-0.1"

_TASK_SOURCES = {
    "electrochemical-conversion": {
        "llm": (
            "runs/formal/"
            "static_scientific_optimization_s0_v041_single_stage_high_20_5seed_20260727/"
            "multiseed_report.json"
        ),
        "baseline": (
            "runs/development/"
            "static_scientific_optimization_s0_v04_single_stage_classic_baselines_20_5worlds_20260727/"
            "multiseed_report.json"
        ),
    },
    "reaction-to-crystallization": {
        "llm": (
            "runs/formal/"
            "static_scientific_optimization_s0_v05_crystallization_high_20_5seed_20260727/"
            "multiseed_report.json"
        ),
        "baseline": (
            "runs/development/"
            "static_scientific_optimization_s0_v05_crystallization_classic_baselines_20_5worlds_20260727/"
            "multiseed_report.json"
        ),
    },
}


def build_static_s0_reportable_results(root: Path) -> dict[str, Any]:
    """Build a world-clustered report without treating algorithm seeds as worlds."""

    root = root.resolve()
    formal_summary_path = (
        root
        / "workstreams/flagship_tasks/reports/"
        "static-s0-confirmatory-summary-v0.1.json"
    )
    formal_summary = _load_json(formal_summary_path)
    tasks: dict[str, Any] = {}
    for task_index, (task_id, source_paths) in enumerate(_TASK_SOURCES.items()):
        llm_path = root / source_paths["llm"]
        baseline_path = root / source_paths["baseline"]
        llm = _load_json(llm_path)
        baseline = _load_json(baseline_path)
        summary_result = formal_summary["results"][task_id]
        tasks[task_id] = _task_report(
            root=root,
            task_id=task_id,
            llm=llm,
            baseline=baseline,
            summary_result=summary_result,
            interval_seed=20260727 + task_index,
        )
        tasks[task_id]["sources"] = {
            "llm_multiseed_report": str(llm_path.relative_to(root)).replace("\\", "/"),
            "llm_multiseed_sha256": file_sha256(llm_path),
            "baseline_multiseed_report": str(baseline_path.relative_to(root)).replace(
                "\\", "/"
            ),
            "baseline_multiseed_sha256": file_sha256(baseline_path),
        }

    provider_calls = sum(
        int(task["resources"]["provider_call_count"]) for task in tasks.values()
    )
    provider_attempts = sum(
        int(task["resources"]["provider_attempt_count"]) for task in tasks.values()
    )
    provider_tokens = sum(
        int(task["resources"]["provider_reported_total_tokens"])
        for task in tasks.values()
    )
    physical_experiments = sum(
        int(task["resources"]["physical_experiment_count"])
        for task in tasks.values()
    )
    return {
        "schema_version": STATIC_S0_REPORTABLE_SCHEMA_VERSION,
        "status": "formal_static_s0_results_reportable",
        "formal_result": True,
        "benchmark_claim_allowed": False,
        "scope": "fixed-world scientific optimization on two confirmatory tasks",
        "reporting_unit": "world_seed_cluster",
        "world_seed_count_per_task": 5,
        "cross_task_composite_score_reported": False,
        "cross_task_composite_reason": (
            "the two task scores have different physical objectives and response surfaces"
        ),
        "statistical_methods": {
            "mean_interval": "two-sided 95% Student-t interval over five world seeds",
            "paired_difference": (
                "LLM blind final score minus the within-world mean of the descriptively "
                "best classic algorithm family"
            ),
            "paired_interval": (
                "two-sided 95% Student-t interval over five paired world differences"
            ),
            "algorithm_seed_treatment": (
                "algorithm seeds are averaged within each world and are not counted as "
                "independent worlds"
            ),
            "baseline_selection_boundary": (
                "best classic family is selected descriptively from the calibration "
                "matrix; paired intervals are descriptive, not preregistered hypothesis tests"
            ),
        },
        "tasks": tasks,
        "combined_resources": {
            "formal_llm_world_cells": 10,
            "provider_call_count": provider_calls,
            "provider_attempt_count": provider_attempts,
            "provider_reported_total_tokens": provider_tokens,
            "physical_experiment_count": physical_experiments,
            "all_replay_verified": all(
                task["resources"]["all_replay_verified"] for task in tasks.values()
            ),
            "monetary_accounting_complete": False,
        },
        "reportable_conclusions": [
            (
                "The model performs closed-loop optimization in a fixed world, but its "
                "mean blind final score is below the strongest classic calibration family "
                "on both confirmatory tasks."
            ),
            (
                "All ten best exploration points occur after experiment 10, so the "
                "20-experiment horizon contributes material search opportunity."
            ),
            (
                "All ten final submissions are tested methods; final synthesis produces "
                "no positive blind gain over the paired incumbent."
            ),
            (
                "Predictive and Declared metrics remain substantially weaker than local "
                "optimization performance, so optimization success is not evidence of "
                "correct mechanism understanding."
            ),
        ],
        "claim_boundary": [
            (
                "five world seeds and one LLM trajectory per world do not estimate a "
                "universal model effect"
            ),
            (
                "classic baselines are calibration comparisons rather than a "
                "preregistered superiority test"
            ),
            "the result does not evaluate hidden world changes or real laboratory transfer",
            (
                "the remaining thirteen registered tasks have executable designs but no "
                "formal model results"
            ),
        ],
        "sources": {
            "formal_summary": str(formal_summary_path.relative_to(root)).replace(
                "\\", "/"
            ),
            "formal_summary_sha256": file_sha256(formal_summary_path),
        },
    }


def _task_report(
    *,
    root: Path,
    task_id: str,
    llm: Mapping[str, Any],
    baseline: Mapping[str, Any],
    summary_result: Mapping[str, Any],
    interval_seed: int,
) -> dict[str, Any]:
    llm_rows = []
    llm_curves: dict[int, list[float]] = {}
    for run in sorted(llm["runs"], key=lambda item: int(item["seed"])):
        cells = run["cells"]
        if len(cells) != 1:
            raise ValueError(f"{task_id} formal run must contain one cell per world")
        cell = cells[0]
        world_seed = int(cell["seed"])
        curve = [float(value) for value in cell["best_so_far_scores"]]
        llm_curves[world_seed] = curve
        llm_rows.append(
            {
                "world_seed": world_seed,
                "blind_final_score": float(cell["validated_recommendation_score"]),
                "blind_incumbent_score": float(cell["validated_incumbent_score"]),
                "blind_gain_over_incumbent": float(
                    cell["recommendation_gain_over_incumbent"]
                ),
                "best_exploration_score": float(cell["best_score"]),
                "best_exploration_index_zero_based": int(cell["best_experiment_index"]),
                "recommendation_type": str(cell["recommendation_type"]),
            }
        )

    baseline_records = baseline["aggregate"]["algorithms"]
    best_record = max(
        baseline_records,
        key=lambda item: float(item["validated_final_score"]["mean"]),
    )
    best_algorithm_id = str(best_record["algorithm_id"])
    baseline_by_world: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for source in baseline["sources"]:
        world_seed = int(source["world_seed"])
        source_report_path = (
            root / Path(str(source["run_root"]).replace("\\", "/")) / "report.json"
        )
        if file_sha256(source_report_path) != str(source["report_sha256"]):
            raise ValueError(f"baseline source report hash mismatch: {source_report_path}")
        source_report = _load_json(source_report_path)
        if int(source_report["world_seed"]) != world_seed:
            raise ValueError("baseline source world seed mismatch")
        for cell in source_report["cells"]:
            if str(cell["agent_manifest"]["algorithm_id"]) == best_algorithm_id:
                baseline_by_world[world_seed].append(cell)

    if set(baseline_by_world) != {int(row["world_seed"]) for row in llm_rows}:
        raise ValueError(f"{task_id} LLM and baseline world seeds do not align")
    baseline_world_rows: dict[int, dict[str, Any]] = {}
    baseline_world_curves: dict[int, list[float]] = {}
    for world_seed, cells in sorted(baseline_by_world.items()):
        final_scores = [float(cell["primary_score"]) for cell in cells]
        curves = [_best_so_far(cell["scores"]) for cell in cells]
        baseline_world_curves[world_seed] = _mean_curve(curves)
        baseline_world_rows[world_seed] = {
            "algorithm_seed_count": len(cells),
            "blind_final_score_mean": statistics.fmean(final_scores),
            "blind_final_score_minimum": min(final_scores),
            "blind_final_score_maximum": max(final_scores),
        }

    paired_rows = []
    for llm_row in llm_rows:
        world_seed = int(llm_row["world_seed"])
        baseline_row = baseline_world_rows[world_seed]
        difference = float(llm_row["blind_final_score"]) - float(
            baseline_row["blind_final_score_mean"]
        )
        paired_rows.append(
            {
                **llm_row,
                "best_classic_algorithm_id": best_algorithm_id,
                "best_classic_blind_score_world_mean": baseline_row[
                    "blind_final_score_mean"
                ],
                "best_classic_algorithm_seed_count": baseline_row[
                    "algorithm_seed_count"
                ],
                "llm_minus_best_classic_world_mean": difference,
                "llm_above_best_classic_world_mean": difference > 0.0,
            }
        )

    llm_scores = [float(row["blind_final_score"]) for row in paired_rows]
    baseline_scores = [
        float(row["best_classic_blind_score_world_mean"]) for row in paired_rows
    ]
    paired_differences = [
        float(row["llm_minus_best_classic_world_mean"]) for row in paired_rows
    ]
    llm_curve_summary = _curve_summary(list(llm_curves.values()))
    baseline_curve_summary = _curve_summary(list(baseline_world_curves.values()))
    recommendation_gains = [
        float(row["blind_gain_over_incumbent"]) for row in paired_rows
    ]
    return {
        "task_id": task_id,
        "world_seeds": [int(row["world_seed"]) for row in paired_rows],
        "world_seed_count": len(paired_rows),
        "llm": {
            "blind_final_score": _summary_with_interval(llm_scores),
            "best_exploration_score": _summary_with_interval(
                [float(row["best_exploration_score"]) for row in paired_rows]
            ),
            "best_exploration_index_zero_based": _summary(
                [float(row["best_exploration_index_zero_based"]) for row in paired_rows]
            ),
            "best_so_far_curve": llm_curve_summary,
            "round_8_best_so_far_mean": llm_curve_summary[7]["mean"],
            "round_20_best_so_far_mean": llm_curve_summary[19]["mean"],
            "round_20_minus_round_8": (
                llm_curve_summary[19]["mean"] - llm_curve_summary[7]["mean"]
            ),
            "recommendation_types": sorted(
                {str(row["recommendation_type"]) for row in paired_rows}
            ),
            "positive_final_synthesis_gain_count": sum(
                value > 0.0 for value in recommendation_gains
            ),
            "zero_final_synthesis_gain_count": sum(
                abs(value) <= 1.0e-15 for value in recommendation_gains
            ),
            "negative_final_synthesis_gain_count": sum(
                value < 0.0 for value in recommendation_gains
            ),
            "final_synthesis_gain": _summary_with_interval(recommendation_gains),
        },
        "best_classic_calibration": {
            "algorithm_id": best_algorithm_id,
            "selection": "highest aggregate blind mean in the six-family calibration matrix",
            "blind_final_score_over_25_algorithm_world_cells": dict(
                best_record["validated_final_score"]
            ),
            "world_clustered_blind_final_score": _summary_with_interval(
                baseline_scores
            ),
            "best_so_far_curve_world_clustered": baseline_curve_summary,
            "round_8_best_so_far_mean": baseline_curve_summary[7]["mean"],
            "round_20_best_so_far_mean": baseline_curve_summary[19]["mean"],
        },
        "paired_llm_vs_best_classic": {
            "difference": _summary_with_interval(paired_differences),
            "llm_world_win_count": sum(value > 0.0 for value in paired_differences),
            "llm_world_tie_count": sum(
                abs(value) <= 1.0e-15 for value in paired_differences
            ),
            "llm_world_loss_count": sum(value < 0.0 for value in paired_differences),
            "bootstrap_mean_difference_interval_95": _bootstrap_mean_interval(
                paired_differences, seed=interval_seed
            ),
            "per_world": paired_rows,
        },
        "world_understanding": {
            "predictive_correct": int(summary_result["predictive_correct"]),
            "predictive_total": int(summary_result["predictive_total"]),
            "predictive_directional_accuracy": (
                float(summary_result["predictive_correct"])
                / float(summary_result["predictive_total"])
            ),
            "declared_structural_edge_f1": float(
                summary_result["declared_structural_edge_f1"]
            ),
            "declared_unsupported_claim_rate": float(
                summary_result["declared_unsupported_claim_rate"]
            ),
        },
        "resources": {
            "provider_call_count": int(summary_result["provider_calls"]),
            "provider_attempt_count": int(
                summary_result.get("provider_attempts", llm["provider_attempt_count"])
            ),
            "provider_reported_total_tokens": int(
                summary_result["provider_reported_tokens"]
            ),
            "physical_experiment_count": int(llm["total_physical_experiment_count"]),
            "all_replay_verified": bool(summary_result["all_replay_verified"]),
        },
    }


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _best_so_far(values: Sequence[object]) -> list[float]:
    result = []
    best = float("-inf")
    for value in values:
        best = max(best, float(value))
        result.append(best)
    return result


def _mean_curve(curves: Sequence[Sequence[float]]) -> list[float]:
    array = np.asarray(curves, dtype=float)
    if array.ndim != 2 or array.shape[0] == 0:
        raise ValueError("curve collection must be a non-empty matrix")
    return [float(value) for value in np.mean(array, axis=0)]


def _curve_summary(curves: Sequence[Sequence[float]]) -> list[dict[str, float | int]]:
    array = np.asarray(curves, dtype=float)
    if array.ndim != 2 or array.shape[0] == 0:
        raise ValueError("curve collection must be a non-empty matrix")
    return [
        {
            "round": index + 1,
            "mean": float(np.mean(array[:, index])),
            "minimum": float(np.min(array[:, index])),
            "maximum": float(np.max(array[:, index])),
        }
        for index in range(array.shape[1])
    ]


def _summary(values: Sequence[float]) -> dict[str, float | int | None]:
    floats = [float(value) for value in values]
    if not floats:
        raise ValueError("summary values cannot be empty")
    return {
        "count": len(floats),
        "mean": statistics.fmean(floats),
        "median": statistics.median(floats),
        "sample_standard_deviation": (
            statistics.stdev(floats) if len(floats) > 1 else None
        ),
        "minimum": min(floats),
        "maximum": max(floats),
    }


def _summary_with_interval(values: Sequence[float]) -> dict[str, Any]:
    summary = _summary(values)
    floats = [float(value) for value in values]
    summary["mean_student_t_interval_95"] = _student_t_mean_interval(floats)
    return summary


def _student_t_mean_interval(values: Sequence[float]) -> list[float] | None:
    if len(values) < 2:
        return None
    mean = statistics.fmean(values)
    standard_error = statistics.stdev(values) / len(values) ** 0.5
    critical = float(t.ppf(0.975, df=len(values) - 1))
    return [mean - critical * standard_error, mean + critical * standard_error]


def _bootstrap_mean_interval(
    values: Sequence[float], *, seed: int, replicate_count: int = 20_000
) -> list[float]:
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    samples = rng.choice(array, size=(replicate_count, array.size), replace=True)
    means = np.mean(samples, axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


__all__ = [
    "STATIC_S0_REPORTABLE_SCHEMA_VERSION",
    "build_static_s0_reportable_results",
]
