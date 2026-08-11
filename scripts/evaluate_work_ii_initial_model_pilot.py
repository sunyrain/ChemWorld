#!/usr/bin/env python3
"""Evaluate one retained Work II initial-world-model pilot without provider calls."""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.work_ii_analysis import score_cell_checkpoint_errors
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    execute_blind_evaluation_plan,
    validate_blind_evaluation_report,
)
from chemworld.eval.work_ii_development_confirmation import build_cluster_rows
from chemworld.eval.work_ii_formal import EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT
from chemworld.eval.work_ii_law_summary import evaluate_final_law_summary
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
REPORT_VERSION = "chemworld-work-ii-initial-model-pilot-evaluation-0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: object) -> Sequence[Any]:
    return value if isinstance(value, Sequence) and not isinstance(value, str | bytes) else []


def _final_snapshot(analysis: Mapping[str, Any]) -> Mapping[str, Any] | None:
    for snapshot in _sequence(analysis.get("belief_snapshots")):
        if isinstance(snapshot, Mapping) and snapshot.get("stage") == "final":
            return snapshot
    return None


def _set_potential(experiment: Mapping[str, Any]) -> dict[str, float] | None:
    for operation in _sequence(experiment.get("operations")):
        if isinstance(operation, Mapping) and operation.get("operation") == "set_potential":
            return {
                "potential_V": float(operation["potential_V"]),
                "current_mA": float(operation["current_mA"]),
            }
    return None


def _electrolysis_duration(experiment: Mapping[str, Any]) -> float:
    return sum(
        float(operation["duration_s"])
        for operation in _sequence(experiment.get("operations"))
        if isinstance(operation, Mapping) and operation.get("operation") == "electrolyze"
    )


def _interval_distance(value: float, interval: Sequence[Any]) -> float:
    if len(interval) != 2:
        raise ValueError("initial-model operating window must have two bounds")
    low, high = float(interval[0]), float(interval[1])
    if not low <= high:
        raise ValueError("initial-model operating window bounds are reversed")
    return max(low - value, 0.0, value - high)


def _window_distance(
    experiment: Mapping[str, Any],
    initial_model: Mapping[str, Any],
) -> dict[str, float] | None:
    controls = _set_potential(experiment)
    model = _mapping(initial_model.get("model"))
    claim = _mapping(model.get("claim"))
    if controls is None or not claim:
        return None
    return {
        "potential_V": _interval_distance(
            controls["potential_V"], _sequence(claim.get("potential_window_V"))
        ),
        "current_mA": _interval_distance(
            controls["current_mA"], _sequence(claim.get("current_window_mA"))
        ),
    }


def _truth_replay_count(report: Mapping[str, Any]) -> int:
    return sum(
        isinstance(receipt, Mapping)
        and _mapping(receipt.get("exact_replay")).get("verified") is True
        for receipt in _sequence(report.get("receipts"))
    )


def _blind_receipts(root: Path, report: Mapping[str, Any]) -> list[dict[str, Any]]:
    loaded = [_load(path) for path in sorted((root / "executions").glob("*/receipt.json"))]
    by_hash = {str(receipt.get("receipt_sha256")): receipt for receipt in loaded}
    return [by_hash[str(digest)] for digest in _sequence(report.get("receipt_sha256"))]


def _format_value(row: Mapping[str, Any], field: str) -> str:
    item = row.get(field)
    return "NA" if item is None else f"{float(item):.4f}"


def _descriptive_interpretation(report: Mapping[str, Any]) -> dict[str, Any]:
    by_arm = {str(row["prior_arm"]): row for row in report["cells"]}
    opaque = by_arm["opaque"]
    aligned = by_arm["aligned_nominal"]
    misspecified = by_arm["misindexed_nominal"]
    reliability = [
        float(value)
        for value in misspecified.get("prior_reliability_trajectory", [])
        if value is not None
    ]
    challenged_fields = sorted(
        {
            str(field)
            for fields in misspecified.get("suspected_misindexed_fields_trajectory", [])
            for field in fields
        }
    )
    selected_incumbent_count = sum(
        row.get("selected_experiment_index") == row.get("observed_incumbent_experiment_index")
        for row in report["cells"]
    )
    return {
        "opaque_prediction_improvement": float(opaque["checkpoint_improvement"]),
        "aligned_prediction_improvement": float(aligned["checkpoint_improvement"]),
        "misspecified_prediction_improvement": float(misspecified["checkpoint_improvement"]),
        "misspecified_initial_reliability": reliability[0] if reliability else None,
        "misspecified_final_reliability": reliability[-1] if reliability else None,
        "misspecified_challenged_fields": challenged_fields,
        "misspecified_minus_opaque_best_endpoint": float(
            misspecified["best_observed_score"]
        )
        - float(opaque["best_observed_score"]),
        "aligned_minus_opaque_best_endpoint": float(aligned["best_observed_score"])
        - float(opaque["best_observed_score"]),
        "H3_primary_contrast": report.get("cluster_contrast", {}).get(
            "H3_primary_contrast"
        ),
        "selected_observed_incumbent_count": selected_incumbent_count,
        "participant_cell_count": len(report["cells"]),
    }


def _change_phrase(value: float, *, noun: str) -> str:
    if value > 0.0:
        return f"{noun} improved by {value:.4f}"
    if value < 0.0:
        return f"{noun} worsened by {abs(value):.4f}"
    return f"{noun} was unchanged"


def _render_markdown(report: Mapping[str, Any]) -> str:
    denominators = report["denominators"]
    interpretation = report.get("descriptive_interpretation")
    if not isinstance(interpretation, Mapping):
        interpretation = _descriptive_interpretation(report)
    participant_cells = int(denominators["participant_cell_count"])
    scheduled_checkpoints = participant_cells * 4
    total_input = sum(
        int(_mapping(row.get("provider_usage")).get("input_token_count") or 0)
        for row in report["cells"]
    )
    total_cached = sum(
        int(_mapping(row.get("provider_usage")).get("cached_input_token_count") or 0)
        for row in report["cells"]
    )
    total_uncached = sum(
        int(_mapping(row.get("provider_usage")).get("uncached_input_token_count") or 0)
        for row in report["cells"]
    )
    total_output = sum(
        int(_mapping(row.get("provider_usage")).get("output_token_count") or 0)
        for row in report["cells"]
    )
    total_recovered_mcp = sum(
        int(
            _mapping(row.get("provider_usage")).get("recovered_mcp_tool_failure_count")
            or 0
        )
        for row in report["cells"]
    )
    total_provider_errors = sum(
        int(_mapping(row.get("provider_usage")).get("provider_error_event_count") or 0)
        for row in report["cells"]
    )
    max_session_elapsed = max(
        float(_mapping(row.get("provider_usage")).get("session_elapsed_s") or 0.0)
        for row in report["cells"]
    )
    challenged = interpretation["misspecified_challenged_fields"]
    challenged_text = ", ".join(challenged) if challenged else "no registered fields"
    initial_reliability = interpretation["misspecified_initial_reliability"]
    final_reliability = interpretation["misspecified_final_reliability"]
    reliability_text = (
        "was unavailable"
        if initial_reliability is None or final_reliability is None
        else f"changed from {float(initial_reliability):.2f} to {float(final_reliability):.2f}"
    )
    endpoint_delta = float(interpretation["misspecified_minus_opaque_best_endpoint"])
    endpoint_text = (
        f"exceeded the opaque endpoint by {endpoint_delta:.4f}"
        if endpoint_delta > 0.0
        else f"trailed the opaque endpoint by {abs(endpoint_delta):.4f}"
        if endpoint_delta < 0.0
        else "matched the opaque endpoint"
    )
    h3_value = interpretation.get("H3_primary_contrast")
    h3_text = "NA" if h3_value is None else f"{float(h3_value):.4f}"
    lines = [
        "# Work II parametric initial-world-model pilot evaluation",
        "",
        "Development evidence only; no formal inference or private-transfer claim.",
        "",
        "## Exact denominators",
        "",
        (
            f"- Participant cells: **{denominators['participant_completed_cell_count']}/"
            f"{denominators['participant_cell_count']}** completed and qualified."
        ),
        (
            f"- Participant experiments: **{denominators['participant_complete_experiment_count']}/"
            f"{denominators['participant_scheduled_experiment_count']}** complete; belief "
            f"checkpoints: **{denominators['participant_checkpoint_count']}/"
            f"{scheduled_checkpoints}**."
        ),
        (
            f"- Held-out truth queries: **{denominators['truth_completed_query_count']}/"
            f"{denominators['truth_query_count']}** complete and "
            f"**{denominators['truth_exact_replay_count']}/"
            f"{denominators['truth_query_count']}** exact replay."
        ),
        (
            f"- Blind replays: **{denominators['blind_completed_execution_count']}/"
            f"{denominators['blind_scheduled_execution_count']}** complete and exact replay."
        ),
        "- Evaluator provider calls: **0**; participant trajectories rerun: **0**.",
        "",
        "## Arm-level results",
        "",
        (
            "| Arm | Best observed score | Pre prediction error | Final error | "
            "Improvement | Final prior reliability | Law error | Blind gain |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["cells"]:
        lines.append(
            f"| {row['prior_arm']} | {_format_value(row, 'best_observed_score')} | "
            f"{_format_value(row, 'effective_pre_error')} | "
            f"{_format_value(row, 'effective_final_error')} | "
            f"{_format_value(row, 'checkpoint_improvement')} | "
            f"{_format_value(row, 'final_prior_reliability')} | "
            f"{_format_value(row, 'law_summary_error')} | "
            f"{_format_value(row, 'blind_recommendation_gain')} |"
        )
    lines.extend(
        [
            "",
            "## Operational profile",
            "",
            (
                f"The three persistent sessions recorded {denominators['participant_operation_attempt_count']} "
                f"operation attempts and {denominators['participant_logical_codex_turn_count']} logical Codex "
                f"turns. Provider accounting was {total_input:,} input tokens "
                f"({total_cached:,} cached; {total_uncached:,} uncached), {total_output:,} output tokens, "
                f"{total_recovered_mcp} recovered MCP failures, {total_provider_errors} provider-error events "
                f"and a maximum session time of {max_session_elapsed:.1f} s."
            ),
            "",
            "## Development interpretation",
            "",
            (
                f"In the misspecified arm, stated prior reliability {reliability_text}; the trajectory "
                f"challenged {challenged_text}. {_change_phrase(float(interpretation['misspecified_prediction_improvement']), noun='Held-out prediction')} "
                f"while its best observed endpoint {endpoint_text}. This separates endpoint search, prior "
                f"self-report and held-out predictive correction rather than treating them as one outcome."
            ),
            "",
            (
                f"Across this single development world, {_change_phrase(float(interpretation['opaque_prediction_improvement']), noun='opaque prediction')}, "
                f"{_change_phrase(float(interpretation['aligned_prediction_improvement']), noun='aligned prediction')}, "
                f"and {_change_phrase(float(interpretation['misspecified_prediction_improvement']), noun='misspecified prediction')}. "
                f"The descriptive H3 contrast was {h3_text}; it is not an inferential result."
            ),
            "",
            (
                f"{interpretation['selected_observed_incumbent_count']}/{interpretation['participant_cell_count']} "
                "final recommendations selected their own observed incumbent. Paired blind replay therefore "
                "checks reproducibility and action commitment but cannot show an additional "
                "recommendation-over-incumbent gain when the two targets are identical."
            ),
            "",
            f"Machine report SHA-256: `{report['report_sha256']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participant-run", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--design",
        type=Path,
        default=ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json",
    )
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()

    if git_worktree_dirty(ROOT):
        raise RuntimeError("initial-model evaluator requires a clean committed worktree")
    participant_root = args.participant_run.resolve()
    config_path = args.config.resolve()
    raw_root = args.raw_output.resolve()
    report_path = args.report.resolve()
    markdown_path = args.markdown.resolve()
    for output in (raw_root, report_path, markdown_path):
        if output.exists():
            raise FileExistsError(f"refusing to overwrite evaluator output: {output}")

    matrix_path = participant_root / "matrix_report.json"
    matrix = _load(matrix_path)
    config = _load(config_path)
    design = _load(args.design.resolve())
    seeds = [int(seed) for seed in _sequence(matrix.get("world_seeds"))]
    if len(seeds) != 1 or matrix.get("all_cells_completed") is not True:
        raise ValueError("participant run must be one completed seed triplet")
    if set(_mapping(config.get("prior_arms"))) != set(ARMS):
        raise ValueError("campaign config does not contain the frozen three arms")
    world_seed = seeds[0]
    task_id = str(config["task_id"])
    embedded = {
        str(result["arm"]): result
        for seed_report in _sequence(matrix.get("seed_reports"))
        if isinstance(seed_report, Mapping)
        for result in _sequence(seed_report.get("results"))
        if isinstance(result, Mapping)
    }
    summaries: dict[str, tuple[Path, dict[str, Any]]] = {}
    for arm in ARMS:
        summary_path = participant_root / f"seed-{world_seed}" / arm / "summary.json"
        summary = _load(summary_path)
        if summary != embedded.get(arm):
            raise ValueError(f"participant summary differs from matrix binding: {arm}")
        summaries[arm] = (summary_path, summary)

    raw_root.mkdir(parents=True)
    cluster_id = f"initial-model-parametric--{task_id}--seed-{world_seed}"
    print(json.dumps({"event": "truth_started", "queries": 4}), flush=True)
    truth_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": task_id,
            "world_seed": world_seed,
        },
        config,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    truth_root = raw_root / "truth"
    truth_report = execute_evaluator_truth_plan(truth_plan, config, truth_root)
    failures = [
        {"scope": "truth", "error": error}
        for error in validate_evaluator_truth_report(truth_report, truth_plan)
    ]
    evaluator_truth = _mapping(truth_report.get("truth"))
    print(
        json.dumps(
            {
                "event": "truth_completed",
                "completed": truth_report["completed_truth_query_count"],
                "total": truth_report["truth_query_count"],
            }
        ),
        flush=True,
    )

    cells: list[dict[str, Any]] = []
    total_blind_exact = 0
    for index, arm in enumerate(ARMS, start=1):
        summary_path, summary = summaries[arm]
        analysis = _mapping(summary.get("analysis"))
        checkpoint = score_cell_checkpoint_errors(
            analysis,
            evaluator_truth,
            terminal_state="completed" if summary.get("completed") is True else "failed",
        )
        final_snapshot = _final_snapshot(analysis)
        law = evaluate_final_law_summary(
            final_snapshot.get("law_summary") if final_snapshot is not None else None,
            truth_plan=truth_plan,
            evaluator_truth=evaluator_truth,
            final_checkpoint_predictions=(
                final_snapshot.get("predictions") if final_snapshot is not None else None
            ),
            effective_pre_error=checkpoint.get("effective_pre_error"),
            effective_final_error=checkpoint.get("effective_final_error"),
            evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
        )
        cell_key = canonical_json_sha256(
            {
                "participant_matrix_sha256": file_sha256(matrix_path),
                "participant_summary_sha256": file_sha256(summary_path),
                "task_id": task_id,
                "world_seed": world_seed,
                "prior_arm": arm,
            }
        )
        cell = {
            "cell_id": f"{cluster_id}--{arm}",
            "cell_key_sha256": cell_key,
            "task_id": task_id,
            "world_seed": world_seed,
        }
        blind_root = raw_root / "blind" / cell_key
        print(json.dumps({"event": "blind_started", "arm": arm, "cell": index}), flush=True)
        blind_plan = build_blind_evaluation_plan(cell, summary, design["blind_evaluator_contract"])
        blind_report = execute_blind_evaluation_plan(blind_plan, config, blind_root)
        blind_receipts = _blind_receipts(blind_root, blind_report)
        blind_errors = validate_blind_evaluation_report(
            blind_report, blind_plan, blind_receipts
        )
        failures.extend(
            {"scope": "blind", "prior_arm": arm, "error": error}
            for error in blind_errors
        )
        blind_exact = sum(
            _mapping(receipt.get("exact_replay")).get("verified") is True
            for receipt in blind_receipts
        )
        total_blind_exact += blind_exact
        print(
            json.dumps(
                {
                    "event": "blind_completed",
                    "arm": arm,
                    "completed": blind_report["completed_execution_count"],
                    "total": blind_report["scheduled_execution_count"],
                }
            ),
            flush=True,
        )

        experiments = [dict(item) for item in _sequence(analysis.get("experiments"))]
        model = _mapping(_mapping(config["prior_arms"][arm]).get("initial_world_model"))
        settings = []
        for experiment in experiments:
            controls = _set_potential(experiment)
            settings.append(
                {
                    "experiment_index": int(experiment["experiment_index"]),
                    "potential_V": controls["potential_V"] if controls else None,
                    "current_mA": controls["current_mA"] if controls else None,
                    "electrolysis_duration_s": _electrolysis_duration(experiment),
                    "leaderboard_score": float(experiment["leaderboard_score"]),
                    "distance_to_supplied_window": _window_distance(experiment, model),
                }
            )
        reliability = list(_sequence(analysis.get("prior_reliability_trajectory")))
        recommendation = _mapping(analysis.get("final_recommendation"))
        usage = _mapping(summary.get("method_resources"))
        cells.append(
            {
                **cell,
                "prior_arm": arm,
                "participant_summary": {
                    "path": summary_path.relative_to(ROOT).as_posix(),
                    "sha256": file_sha256(summary_path),
                },
                "participant_state": "completed" if summary.get("completed") is True else "failed",
                "participant_qualification_passed": _mapping(
                    summary.get("qualification")
                ).get("passed")
                is True,
                "complete_experiment_count": int(analysis.get("complete_experiment_count", 0)),
                "operation_attempt_count": int(analysis.get("operation_attempt_count", 0)),
                "checkpoint_count": len(_sequence(analysis.get("belief_snapshots"))),
                "experiments": settings,
                "best_observed_score": max(
                    float(item["leaderboard_score"]) for item in experiments
                ),
                "observed_incumbent_experiment_index": analysis.get(
                    "observed_incumbent_experiment_index"
                ),
                "selected_experiment_index": recommendation.get("selected_experiment_index"),
                "prior_reliability_trajectory": reliability,
                "final_prior_reliability": reliability[-1] if reliability else None,
                "suspected_misindexed_fields_trajectory": list(
                    _sequence(analysis.get("suspected_misindexed_fields_trajectory"))
                ),
                "effective_pre_error": checkpoint.get("effective_pre_error"),
                "effective_final_error": checkpoint.get("effective_final_error"),
                "checkpoint_improvement": checkpoint.get("primary_improvement"),
                "checkpoint_scores": checkpoint.get("checkpoint_scores"),
                "checkpoint_missing_rule": checkpoint.get("missing_failure_rule"),
                "law_summary_status": law.get("status"),
                "law_summary_error": law.get("normalized_mae"),
                "law_summary_improvement": law.get("pre_to_law_summary_improvement"),
                "law_summary_prediction_consistency_error": law.get(
                    "prediction_consistency_normalized_mae"
                ),
                "blind_scheduled_execution_count": blind_report.get("scheduled_execution_count"),
                "blind_completed_execution_count": blind_report.get("completed_execution_count"),
                "blind_exact_replay_count": blind_exact,
                "blind_recommendation_gain": blind_report.get("recommendation_gain_over_incumbent"),
                "provider_usage": {
                    "provider_session_count": usage.get("provider_session_count"),
                    "logical_codex_turn_count": usage.get("logical_codex_turn_count"),
                    "input_token_count": usage.get("input_token_count"),
                    "cached_input_token_count": usage.get("cached_input_token_count"),
                    "uncached_input_token_count": usage.get("uncached_input_token_count"),
                    "output_token_count": usage.get("output_token_count"),
                    "input_cache_hit_ratio": usage.get("input_cache_hit_ratio"),
                    "session_elapsed_s": usage.get("session_elapsed_s"),
                    "recovered_mcp_tool_failure_count": usage.get(
                        "recovered_mcp_tool_failure_count"
                    ),
                    "maximum_consecutive_mcp_tool_failure_count": usage.get(
                        "maximum_consecutive_mcp_tool_failure_count"
                    ),
                    "provider_error_event_count": usage.get("provider_error_event_count"),
                },
            }
        )

    cluster_rows = build_cluster_rows(cells)
    report: dict[str, Any] = {
        "schema_version": REPORT_VERSION,
        "analysis_date": "2026-08-11",
        "formal_result": False,
        "status": "passed" if not failures else "failed_retained",
        "source_commit": git_source_commit(ROOT),
        "participant_source_commit": matrix.get("source_commit"),
        "participant_run": {
            "path": participant_root.relative_to(ROOT).as_posix(),
            "matrix_report_sha256": file_sha256(matrix_path),
        },
        "config": {
            "path": config_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(config_path),
        },
        "task_id": task_id,
        "world_seed": world_seed,
        "provider": {
            "provider_id": matrix.get("provider_id"),
            "model": matrix.get("model"),
            "reasoning_effort": _mapping(config.get("provider")).get("reasoning_effort"),
            "session_scope": "one_persistent_codex_session_per_cell",
        },
        "denominators": {
            "participant_cell_count": len(cells),
            "participant_completed_cell_count": sum(
                row["participant_state"] == "completed"
                and row["participant_qualification_passed"] is True
                for row in cells
            ),
            "participant_scheduled_experiment_count": len(cells) * 4,
            "participant_complete_experiment_count": sum(
                int(row["complete_experiment_count"]) for row in cells
            ),
            "participant_operation_attempt_count": sum(
                int(row["operation_attempt_count"]) for row in cells
            ),
            "participant_checkpoint_count": sum(int(row["checkpoint_count"]) for row in cells),
            "participant_provider_session_count": sum(
                int(_mapping(row["provider_usage"]).get("provider_session_count") or 0)
                for row in cells
            ),
            "participant_logical_codex_turn_count": sum(
                int(_mapping(row["provider_usage"]).get("logical_codex_turn_count") or 0)
                for row in cells
            ),
            "truth_query_count": truth_report.get("truth_query_count"),
            "truth_completed_query_count": truth_report.get("completed_truth_query_count"),
            "truth_exact_replay_count": _truth_replay_count(truth_report),
            "blind_scheduled_execution_count": sum(
                int(row["blind_scheduled_execution_count"]) for row in cells
            ),
            "blind_completed_execution_count": sum(
                int(row["blind_completed_execution_count"]) for row in cells
            ),
            "blind_exact_replay_count": total_blind_exact,
            "evaluator_provider_call_count": 0,
            "participant_trajectory_rerun_count": 0,
        },
        "cluster_contrast": cluster_rows[0] if len(cluster_rows) == 1 else None,
        "truth_report_sha256": truth_report.get("report_sha256"),
        "cells": cells,
        "failures": failures,
        "interpretation_boundary": (
            "One development world and one provider/model setting. The result can admit or reject "
            "a five-seed parametric extension but cannot establish a general initial-world-model "
            "claim, cross-task transfer or cross-provider ranking."
        ),
    }
    report["descriptive_interpretation"] = _descriptive_interpretation(report)
    if not all(math.isfinite(float(row["best_observed_score"])) for row in cells):
        raise ValueError("participant score summary contains a non-finite value")
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(report_path, report)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "event": "evaluation_completed",
                "status": report["status"],
                "participant_cells": len(cells),
                "truth_queries": truth_report.get("completed_truth_query_count"),
                "blind_replays": report["denominators"]["blind_completed_execution_count"],
                "report": str(report_path),
            }
        ),
        flush=True,
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
