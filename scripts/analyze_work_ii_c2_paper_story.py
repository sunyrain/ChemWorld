#!/usr/bin/env python3
"""Summarize participant workflow and optionally bind the completed C2 evaluator.

This authoring analysis never executes evaluator truth queries.  When an evaluator
report is supplied, it validates and binds that result instead of treating payload
collection as prediction evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
EXPECTED_QUERY_COUNT = {"A_E_public": 4, "A_P": 16, "A_S": 16}


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _mean(values: Iterable[float | int | None]) -> float | None:
    finite = [float(value) for value in values if value is not None and math.isfinite(value)]
    return sum(finite) / len(finite) if finite else None


def _operation(row: Mapping[str, Any]) -> str | None:
    operation = row.get("operation_type")
    if isinstance(operation, str):
        return operation
    action = row.get("action")
    if isinstance(action, Mapping) and isinstance(action.get("operation"), str):
        return str(action["operation"])
    return None


def _terminal_lifecycle(row: Mapping[str, Any]) -> tuple[str, int] | None:
    if row.get("transaction_status") != "committed":
        return None
    operation = _operation(row)
    if operation == "discard_batch":
        outcome = "discarded"
    elif operation == "measure" and row.get("instrument") == "final_assay":
        outcome = "completed"
    else:
        return None
    raw_index = row.get("experiment_index")
    if isinstance(raw_index, bool) or not isinstance(raw_index, int) or raw_index < 0:
        raise ValueError("terminal trajectory row lacks a zero-based experiment_index")
    return outcome, raw_index + 1


def _stable_recommendation(
    summary: Mapping[str, Any], trajectory_path: Path
) -> dict[str, Any]:
    completed: list[dict[str, Any]] = []
    discarded: list[int] = []
    closed: set[int] = set()
    with trajectory_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"expected object in {trajectory_path}")
            terminal = _terminal_lifecycle(row)
            if terminal is None:
                continue
            outcome, lifecycle_index = terminal
            if lifecycle_index in closed:
                raise ValueError(f"duplicate lifecycle index in {trajectory_path}")
            closed.add(lifecycle_index)
            if outcome == "discarded":
                discarded.append(lifecycle_index)
                continue
            score = row.get("leaderboard_score")
            completed.append(
                {
                    "lifecycle_index": lifecycle_index,
                    "score": (
                        float(score)
                        if isinstance(score, int | float) and not isinstance(score, bool)
                        else None
                    ),
                }
            )

    recommendation: Mapping[str, Any] | None = None
    host_committed = False
    receipts = summary.get("provider_receipts")
    if isinstance(receipts, list):
        for receipt in reversed(receipts):
            if not isinstance(receipt, Mapping):
                continue
            candidate = receipt.get("final_recommendation")
            if isinstance(candidate, Mapping):
                recommendation = candidate
                host_committed = receipt.get("final_recommendation_source") == "host_mcp_commit"
                break
    if recommendation is None:
        analysis = summary.get("analysis")
        if isinstance(analysis, Mapping):
            candidate = analysis.get("final_recommendation")
            if isinstance(candidate, Mapping):
                recommendation = candidate

    selected_index = (
        recommendation.get("selected_experiment_index") if recommendation is not None else None
    )
    selected = next(
        (row for row in completed if row["lifecycle_index"] == selected_index), None
    )
    scored = [row for row in completed if row["score"] is not None]
    incumbent = (
        min(scored, key=lambda row: (-float(row["score"]), row["lifecycle_index"]))
        if scored
        else None
    )
    selected_score = selected.get("score") if selected is not None else None
    incumbent_score = incumbent.get("score") if incumbent is not None else None
    regret = (
        float(incumbent_score) - float(selected_score)
        if incumbent_score is not None and selected_score is not None
        else None
    )
    return {
        "closed_batch_count": len(closed),
        "completed_experiment_count": len(completed),
        "discarded_batch_count": len(discarded),
        "timing_confounded_by_discard": bool(discarded),
        "recommendation_present": recommendation is not None,
        "recommendation_identity_valid": selected is not None,
        "host_recommendation_committed": host_committed,
        "selected_lifecycle_index": selected_index,
        "incumbent_lifecycle_index": (
            incumbent.get("lifecycle_index") if incumbent is not None else None
        ),
        "recommendation_selected_exact_incumbent": (
            selected is not None
            and incumbent is not None
            and selected["lifecycle_index"] == incumbent["lifecycle_index"]
        ),
        "recommendation_regret": regret,
    }


def _snapshot_suspects(snapshot: Mapping[str, Any] | None) -> bool:
    if not isinstance(snapshot, Mapping):
        return False
    assessment = snapshot.get("prior_assessment")
    if not isinstance(assessment, Mapping):
        return False
    fields = assessment.get("suspected_misindexed_fields")
    return isinstance(fields, list) and bool(fields)


def _snapshot_reliability(snapshot: Mapping[str, Any] | None) -> float | None:
    if not isinstance(snapshot, Mapping):
        return None
    assessment = snapshot.get("prior_assessment")
    value = assessment.get("reliability_probability") if isinstance(assessment, Mapping) else None
    return (
        float(value)
        if isinstance(value, int | float) and not isinstance(value, bool)
        else None
    )


def _best_position(experiments: Sequence[Mapping[str, Any]]) -> tuple[int, int] | None:
    score_rows: list[tuple[int, float]] = []
    for experiment in experiments:
        index = experiment.get("experiment_index")
        score = experiment.get("leaderboard_score")
        if (
            isinstance(index, int)
            and not isinstance(index, bool)
            and isinstance(score, int | float)
            and not isinstance(score, bool)
        ):
            score_rows.append((index, float(score)))
    if not score_rows:
        return None
    best_index = max(score_rows, key=lambda row: (row[1], -row[0]))[0]
    final_index = max(row[0] for row in score_rows)
    return best_index, final_index


def _load_cells(
    metrics_path: Path,
    base_root: Path,
    replacement_root: Path,
    replacement_block: str,
    replacement_task: str,
) -> list[dict[str, Any]]:
    with metrics_path.open(encoding="utf-8-sig", newline="") as handle:
        metric_rows = list(csv.DictReader(handle))
    cells: list[dict[str, Any]] = []
    for metric in metric_rows:
        use_replacement = (
            metric["block"] == replacement_block and metric["task"] == replacement_task
        )
        root = replacement_root if use_replacement else base_root
        cell_root = root / "cells" / metric["cell_id"]
        summary = _read_object(cell_root / "summary.json")
        analysis = summary.get("analysis")
        if not isinstance(analysis, Mapping):
            raise ValueError(f"analysis missing: {cell_root}")
        snapshots = analysis.get("belief_snapshots")
        if not isinstance(snapshots, list):
            snapshots = []
        snapshot_rows = [row for row in snapshots if isinstance(row, Mapping)]
        pre = next((row for row in snapshot_rows if row.get("stage") == "pre_evidence"), None)
        final = next(
            (row for row in reversed(snapshot_rows) if row.get("stage") == "final"), None
        )
        expected_queries = EXPECTED_QUERY_COUNT[metric["block"]]
        query_counts = [
            len(row.get("predictions"))
            if isinstance(row.get("predictions"), list)
            else 0
            for row in snapshot_rows
        ]
        prediction_metric_count = 0
        for snapshot in snapshot_rows:
            predictions = snapshot.get("predictions")
            if not isinstance(predictions, list):
                continue
            for prediction in predictions:
                metrics = prediction.get("metrics") if isinstance(prediction, Mapping) else None
                if isinstance(metrics, list):
                    prediction_metric_count += len(metrics)

        profile = analysis.get("process_profile")
        profile = profile if isinstance(profile, Mapping) else {}
        counts = profile.get("counts")
        counts = counts if isinstance(counts, Mapping) else {}
        axes = profile.get("construct_axes")
        axes = axes if isinstance(axes, Mapping) else {}
        evidence = axes.get("evidence_acquisition")
        evidence = evidence if isinstance(evidence, Mapping) else {}
        nonfinal = evidence.get("nonfinal_instrument_uses_per_closed_lifecycle")
        nonfinal = nonfinal if isinstance(nonfinal, Mapping) else {}
        calculation = nonfinal.get("calculation")
        calculation = calculation if isinstance(calculation, Mapping) else {}

        method_resources = summary.get("method_resources")
        method_resources = method_resources if isinstance(method_resources, Mapping) else {}
        taxonomy = method_resources.get("mcp_tool_failure_taxonomy")
        taxonomy = taxonomy if isinstance(taxonomy, Mapping) else {}
        failure_categories = taxonomy.get("counts_by_category")
        failure_categories = (
            dict(failure_categories) if isinstance(failure_categories, Mapping) else {}
        )
        failed_tool_events: Counter[str] = Counter()
        receipts = summary.get("provider_receipts")
        if isinstance(receipts, list):
            for receipt in receipts:
                events = receipt.get("tool_events") if isinstance(receipt, Mapping) else None
                if not isinstance(events, list):
                    continue
                for event in events:
                    if not isinstance(event, Mapping) or event.get("status") == "completed":
                        continue
                    failed_tool_events[
                        f"{event.get('tool')}|{event.get('classification')}"
                    ] += 1

        experiments = analysis.get("experiments")
        experiments = (
            [row for row in experiments if isinstance(row, Mapping)]
            if isinstance(experiments, list)
            else []
        )
        best_position = _best_position(experiments)
        recommendation = _stable_recommendation(summary, cell_root / "trajectory.jsonl")
        cells.append(
            {
                "cell_id": metric["cell_id"],
                "block": metric["block"],
                "task": metric["task"],
                "task_group": metric["task_group"],
                "world_seed": metric["world_seed"],
                "arm": metric["arm"],
                "scheduled_experiments": int(metric["scheduled_experiments"]),
                "complete_experiments": int(metric["complete_experiments"]),
                "qualified": metric["qualification_passed"] == "True",
                "unique_recipe_count": int(metric["unique_recipe_count"]),
                "exact_repeat_count": int(metric["exact_repeat_count"]),
                "operation_attempt_count": int(metric["operation_attempt_count"]),
                "committed_operation_count": int(metric["committed_operation_count"]),
                "resource_rejection_count": int(metric["resource_rejection_count"]),
                "dynamic_physical_failure_count": int(
                    metric["dynamic_physical_failure_count"]
                ),
                "mcp_recovery_episode_count": int(metric["mcp_recovery_episode_count"]),
                "first_score": float(metric["first_score"]),
                "best_score": float(metric["best_score"]),
                "best_minus_first": float(metric["best_minus_first"]),
                "snapshot_count": len(snapshot_rows),
                "pre_snapshot_present": pre is not None,
                "final_snapshot_present": final is not None,
                "snapshot_schema_valid_count": sum(
                    row.get("schema_version") == "chemworld-work-ii-belief-snapshot-0.1"
                    for row in snapshot_rows
                ),
                "law_summary_schema_valid_count": sum(
                    isinstance(row.get("law_summary"), Mapping)
                    and row["law_summary"].get("schema_version")
                    == "chemworld-work-ii-law-summary-0.1"
                    for row in snapshot_rows
                ),
                "prediction_bundle_count": sum(count > 0 for count in query_counts),
                "prediction_query_count": sum(query_counts),
                "prediction_metric_count": prediction_metric_count,
                "expected_query_bundle_count": sum(
                    count == expected_queries for count in query_counts
                ),
                "pre_reliability": _snapshot_reliability(pre),
                "final_reliability": _snapshot_reliability(final),
                "pre_suspects_misindex": _snapshot_suspects(pre),
                "final_suspects_misindex": _snapshot_suspects(final),
                "pre_confidence": pre.get("overall_confidence") if pre else None,
                "final_confidence": final.get("overall_confidence") if final else None,
                "closed_lifecycle_count": int(counts.get("closed_lifecycle_count", 0) or 0),
                "measured_lifecycle_count": int(
                    counts.get("measured_lifecycle_count", 0) or 0
                ),
                "nonfinal_instrument_use_count": int(
                    calculation.get("nonfinal_instrument_use_count", 0) or 0
                ),
                "best_experiment_index": best_position[0] if best_position else None,
                "last_experiment_index": best_position[1] if best_position else None,
                "failed_tool_events": dict(failed_tool_events),
                "mcp_failure_categories": failure_categories,
                **recommendation,
            }
        )
    return cells


def _group_summary(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    closed = sum(int(cell["closed_lifecycle_count"]) for cell in cells)
    completed = sum(int(cell["complete_experiments"]) for cell in cells)
    best_positions = [
        (int(cell["best_experiment_index"]), int(cell["last_experiment_index"]))
        for cell in cells
        if cell.get("best_experiment_index") is not None
        and cell.get("last_experiment_index") is not None
    ]
    nominal = [cell for cell in cells if cell["arm"] != "opaque"]
    tool_failures: Counter[str] = Counter()
    failure_categories: Counter[str] = Counter()
    for cell in cells:
        tool_failures.update(cell["failed_tool_events"])
        failure_categories.update(cell["mcp_failure_categories"])
    regrets = [
        float(cell["recommendation_regret"])
        for cell in cells
        if cell.get("recommendation_regret") is not None
    ]
    return {
        "cell_count": len(cells),
        "qualified_cell_count": sum(bool(cell["qualified"]) for cell in cells),
        "complete_experiment_count": completed,
        "scheduled_experiment_count": sum(
            int(cell["scheduled_experiments"]) for cell in cells
        ),
        "snapshot_count": sum(int(cell["snapshot_count"]) for cell in cells),
        "five_snapshot_cell_count": sum(cell["snapshot_count"] == 5 for cell in cells),
        "pre_snapshot_cell_count": sum(bool(cell["pre_snapshot_present"]) for cell in cells),
        "final_snapshot_cell_count": sum(
            bool(cell["final_snapshot_present"]) for cell in cells
        ),
        "prediction_bundle_count": sum(
            int(cell["prediction_bundle_count"]) for cell in cells
        ),
        "prediction_query_count": sum(int(cell["prediction_query_count"]) for cell in cells),
        "prediction_metric_count": sum(
            int(cell["prediction_metric_count"]) for cell in cells
        ),
        "expected_query_bundle_count": sum(
            int(cell["expected_query_bundle_count"]) for cell in cells
        ),
        "schema_valid_belief_snapshot_count": sum(
            int(cell["snapshot_schema_valid_count"]) for cell in cells
        ),
        "schema_valid_law_summary_count": sum(
            int(cell["law_summary_schema_valid_count"]) for cell in cells
        ),
        "closed_lifecycle_count": closed,
        "measured_lifecycle_count": sum(
            int(cell["measured_lifecycle_count"]) for cell in cells
        ),
        "measured_lifecycle_fraction": (
            sum(int(cell["measured_lifecycle_count"]) for cell in cells) / closed
            if closed
            else None
        ),
        "nonfinal_instrument_use_count": sum(
            int(cell["nonfinal_instrument_use_count"]) for cell in cells
        ),
        "mean_unique_recipe_fraction": _mean(
            int(cell["unique_recipe_count"]) / int(cell["complete_experiments"])
            for cell in cells
            if int(cell["complete_experiments"])
        ),
        "mean_normalized_best_position": _mean(
            best / last for best, last in best_positions if last > 0
        ),
        "best_in_second_half_fraction": _mean(
            int(best > last / 2) for best, last in best_positions
        ),
        "best_at_last_experiment_fraction": _mean(
            int(best == last) for best, last in best_positions
        ),
        "mean_pre_confidence": _mean(cell.get("pre_confidence") for cell in cells),
        "mean_final_confidence": _mean(cell.get("final_confidence") for cell in cells),
        "mean_pre_reliability_nominal": _mean(
            cell.get("pre_reliability") for cell in nominal
        ),
        "mean_final_reliability_nominal": _mean(
            cell.get("final_reliability") for cell in nominal
        ),
        "mean_reliability_delta_nominal": _mean(
            (
                float(cell["final_reliability"]) - float(cell["pre_reliability"])
                if cell.get("pre_reliability") is not None
                and cell.get("final_reliability") is not None
                else None
            )
            for cell in nominal
        ),
        "pre_suspected_misindex_fraction_nominal": _mean(
            int(bool(cell["pre_suspects_misindex"])) for cell in nominal
        ),
        "final_suspected_misindex_fraction_nominal": _mean(
            int(bool(cell["final_suspects_misindex"])) for cell in nominal
        ),
        "uncommitted_operation_attempt_count": sum(
            int(cell["operation_attempt_count"]) - int(cell["committed_operation_count"])
            for cell in cells
        ),
        "resource_rejection_count": sum(
            int(cell["resource_rejection_count"]) for cell in cells
        ),
        "dynamic_physical_failure_count": sum(
            int(cell["dynamic_physical_failure_count"]) for cell in cells
        ),
        "mcp_recovery_episode_count": sum(
            int(cell["mcp_recovery_episode_count"]) for cell in cells
        ),
        "failed_tool_event_counts": dict(sorted(tool_failures.items())),
        "mcp_failure_category_counts": dict(sorted(failure_categories.items())),
        "discarded_batch_count": sum(int(cell["discarded_batch_count"]) for cell in cells),
        "discard_timing_confounded_cell_count": sum(
            bool(cell["timing_confounded_by_discard"]) for cell in cells
        ),
        "final_recommendation_count": sum(
            bool(cell["recommendation_present"]) for cell in cells
        ),
        "recommendation_identity_valid_count": sum(
            bool(cell["recommendation_identity_valid"]) for cell in cells
        ),
        "recommendation_selected_exact_incumbent_count": sum(
            bool(cell["recommendation_selected_exact_incumbent"]) for cell in cells
        ),
        "recommendation_zero_regret_count": sum(abs(value) <= 1e-15 for value in regrets),
        "mean_recommendation_regret": _mean(regrets),
        "maximum_recommendation_regret": max(regrets) if regrets else None,
    }


def _endpoint_contrasts(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for cell in cells:
        grouped[(str(cell["task_group"]), str(cell["world_seed"]))][str(cell["arm"])] = cell
    result: dict[str, Any] = {}
    contrast_pairs = (
        ("aligned_minus_opaque", "aligned_nominal", "opaque"),
        ("misindexed_minus_opaque", "misindexed_nominal", "opaque"),
        ("aligned_minus_misindexed", "aligned_nominal", "misindexed_nominal"),
    )
    for task_group in sorted({key[0] for key in grouped}):
        clusters = [arms for (task, _), arms in grouped.items() if task == task_group]
        task_result: dict[str, Any] = {}
        for metric in ("first_score", "best_score", "best_minus_first"):
            metric_result: dict[str, Any] = {}
            for label, minuend, subtrahend in contrast_pairs:
                differences = [
                    float(arms[minuend][metric]) - float(arms[subtrahend][metric])
                    for arms in clusters
                    if set(ARMS).issubset(arms)
                ]
                metric_result[label] = {
                    "mean": _mean(differences),
                    "positive_world_count": sum(value > 0 for value in differences),
                    "zero_world_count": sum(abs(value) <= 1e-15 for value in differences),
                    "world_count": len(differences),
                    "world_differences": differences,
                }
            task_result[metric] = metric_result
        result[task_group] = task_result
    return result


def build_report(
    cells: Sequence[Mapping[str, Any]],
    *,
    base_run: str,
    replacement_run: str,
    replacement_pair: str,
    evaluator: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    by_arm = {
        arm: _group_summary([cell for cell in cells if cell["arm"] == arm])
        for arm in ARMS
    }
    by_task = {
        task: _group_summary([cell for cell in cells if cell["task_group"] == task])
        for task in sorted({str(cell["task_group"]) for cell in cells})
    }
    evaluator_complete = evaluator is not None
    if evaluator_complete:
        evaluator_denominators = evaluator["denominators"]
        if evaluator_denominators["cell_count"] != len(cells):
            raise ValueError("evaluator and participant cell denominators do not match")
        evaluator_summary: dict[str, Any] | None = {
            "status": evaluator["status"],
            "provider_call_count": evaluator["provider_call_count"],
            "denominators": evaluator_denominators,
            "locus_decisions": {
                locus: {
                    "passed": result["gate"]["passed"],
                    "p_value": result["gate"].get(
                        "intersection_union_p_value",
                        result["gate"].get("effective_intersection_union_p_value"),
                    ),
                    "primary_estimate": (
                        result["gate"]["components"]["H3_primary_contrast"]
                        if "components" in result["gate"]
                        else result["gate"]["inference"]
                    )["estimate"],
                    "observed_point_passed": result[
                        "observed_point_sensitivity_gate"
                    ]["passed"],
                }
                for locus, result in evaluator["prediction_correction"][
                    "locus_results"
                ].items()
            },
            "law_overall": evaluator["executable_law"]["overall"]["all"],
            "blind_overall": evaluator["blind_action"]["overall"],
        }
    else:
        evaluator_summary = None
    return {
        "schema_version": "chemworld-work-ii-c2-paper-story-analysis-0.1",
        "analysis_status": (
            "participant_and_current_composite_evaluator_complete"
            if evaluator_complete
            else "descriptive_participant_and_agent_behavior_prediction_truth_not_scored"
        ),
        "input_runs": [base_run, replacement_run],
        "replacement_block_task": replacement_pair,
        "prediction_task_status": {
            "participant_checkpoint_collection": "complete",
            "registered_truth_evaluator": (
                "complete" if evaluator_complete else "not_run_for_current_composite_cohort"
            ),
            "law_summary_evaluator": (
                "complete" if evaluator_complete else "not_run_for_current_composite_cohort"
            ),
            "blind_recommendation_replay": (
                "complete" if evaluator_complete else "not_run_for_current_composite_cohort"
            ),
            "confirmatory_prediction_result_available": evaluator_complete,
            "confirmatory_prediction_claim_allowed": bool(
                evaluator_complete
                and evaluator["prediction_correction"]["C2_intersection_union"][
                    "passed"
                ]
            ),
        },
        "current_composite_evaluator": evaluator_summary,
        "overall": _group_summary(cells),
        "by_arm": by_arm,
        "by_task": by_task,
        "paired_endpoint_contrasts": _endpoint_contrasts(cells),
        "interpretation_boundaries": [
            "Endpoint and workflow summaries are participant-visible descriptive outcomes.",
            (
                "General prediction improvement does not establish selective wrong-prior repair."
                if evaluator_complete
                else "Checkpoint payload completeness does not establish prediction accuracy."
            ),
            (
                "Executable law syntax does not establish faithful law compression."
                if evaluator_complete
                else (
                    "Schema-valid law summaries are not evaluator-executable "
                    "law-recovery evidence."
                )
            ),
            (
                "Blind equivalence establishes reproducibility, not action improvement."
                if evaluator_complete
                else (
                    "Recommendation identity and observed-score regret do not replace "
                    "blind replay."
                )
            ),
            "Failed checkpoint tool calls are harness burden, not independent scientific samples.",
            "No cross-provider or general-language-model inference is supported.",
        ],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell-metrics", type=Path, required=True)
    parser.add_argument("--base-run", type=Path, required=True)
    parser.add_argument("--replacement-run", type=Path, required=True)
    parser.add_argument("--replacement-block", default="A_S")
    parser.add_argument("--replacement-task", default="reaction-to-crystallization")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--evaluator",
        type=Path,
        help="Completed current-composite evaluator report to validate and bind.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    cells = _load_cells(
        args.cell_metrics.resolve(strict=True),
        args.base_run.resolve(strict=True),
        args.replacement_run.resolve(strict=True),
        args.replacement_block,
        args.replacement_task,
    )
    report = build_report(
        cells,
        base_run=args.base_run.name,
        replacement_run=args.replacement_run.name,
        replacement_pair=f"{args.replacement_block}:{args.replacement_task}",
        evaluator=(
            _read_object(args.evaluator.resolve(strict=True))
            if args.evaluator is not None
            else None
        ),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report["overall"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
