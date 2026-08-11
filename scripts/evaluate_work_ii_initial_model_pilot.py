#!/usr/bin/env python3
"""Evaluate one retained Work II initial-world-model pilot without provider calls."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
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
REPORT_VERSION = "chemworld-work-ii-initial-model-pilot-evaluation-0.2"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: object) -> Sequence[Any]:
    return value if isinstance(value, Sequence) and not isinstance(value, str | bytes) else []


def _snapshot(
    analysis: Mapping[str, Any],
    stage: str,
) -> Mapping[str, Any] | None:
    for snapshot in _sequence(analysis.get("belief_snapshots")):
        if isinstance(snapshot, Mapping) and snapshot.get("stage") == stage:
            return snapshot
    return None


def _final_snapshot(analysis: Mapping[str, Any]) -> Mapping[str, Any] | None:
    return _snapshot(analysis, "final")


def _configured_experiment_count(config: Mapping[str, Any]) -> int:
    value = _mapping(config.get("campaign")).get("complete_experiments")
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("campaign complete-experiment denominator is invalid")
    return value


def _configured_checkpoint_count(config: Mapping[str, Any]) -> int:
    stages = _sequence(config.get("snapshot_stages"))
    schedule = _sequence(_mapping(config.get("campaign")).get("checkpoint_complete_experiments"))
    if not stages or len(stages) != len(schedule):
        raise ValueError("campaign checkpoint denominator is invalid")
    return len(stages)


def _scientific_trajectory_complete(
    summary: Mapping[str, Any],
    expected_experiment_count: int = 4,
) -> bool:
    analysis = _mapping(summary.get("analysis"))
    replay = _mapping(summary.get("exact_replay"))
    return (
        int(analysis.get("complete_experiment_count", 0)) == expected_experiment_count
        and analysis.get("right_censored_open_experiment") is False
        and replay.get("verified") is True
    )


def _parametric_controls(experiment: Mapping[str, Any], task_id: str) -> dict[str, Any]:
    operations = [
        operation
        for operation in _sequence(experiment.get("operations"))
        if isinstance(operation, Mapping)
    ]
    if task_id == "electrochemical-conversion":
        setpoints = [
            operation for operation in operations if operation.get("operation") == "set_potential"
        ]
        controls: dict[str, Any] = {
            "duration_s": sum(
                float(operation["duration_s"])
                for operation in operations
                if operation.get("operation") == "electrolyze"
            )
        }
        if setpoints:
            controls.update(
                {
                    "potential_V": float(setpoints[-1]["potential_V"]),
                    "current_mA": float(setpoints[-1]["current_mA"]),
                }
            )
        return controls
    if task_id == "reaction-safety-constrained":
        heat_stages = [
            {
                "reaction_temperature_K": float(operation["target_temperature_K"]),
                "reaction_duration_s": float(operation["duration_s"]),
            }
            for operation in operations
            if operation.get("operation") == "heat"
        ]
        controls = {
            "heat_stages": heat_stages,
            "reaction_duration_s": sum(
                float(stage["reaction_duration_s"]) for stage in heat_stages
            ),
        }
        if heat_stages:
            controls["reaction_temperature_K"] = heat_stages[-1]["reaction_temperature_K"]
        return controls
    raise ValueError(f"unsupported parametric pilot task: {task_id}")


def _interval_distance(value: float, interval: Sequence[Any]) -> float:
    if len(interval) != 2:
        raise ValueError("initial-model operating window must have two bounds")
    low, high = float(interval[0]), float(interval[1])
    if not low <= high:
        raise ValueError("initial-model operating window bounds are reversed")
    return max(low - value, 0.0, value - high)


def _supplied_model_distance(
    controls: Mapping[str, Any],
    initial_model: Mapping[str, Any],
) -> dict[str, float] | None:
    model = _mapping(initial_model.get("model"))
    claim = _mapping(model.get("claim"))
    reference_region = _mapping(
        _mapping(initial_model.get("context_contract")).get("approximate_reference_region")
    )
    if not controls or (not claim and not reference_region):
        return None
    if "potential_window_V" in claim and "current_window_mA" in claim:
        if "potential_V" not in controls or "current_mA" not in controls:
            return None
        return {
            "potential_V": _interval_distance(
                float(controls["potential_V"]),
                _sequence(claim.get("potential_window_V")),
            ),
            "current_mA": _interval_distance(
                float(controls["current_mA"]),
                _sequence(claim.get("current_window_mA")),
            ),
        }
    if "reaction_temperature_K" in claim and "reaction_duration_s" in claim:
        if "reaction_temperature_K" not in controls or "reaction_duration_s" not in controls:
            return None
        return {
            "reaction_temperature_K": max(
                abs(
                    float(controls["reaction_temperature_K"])
                    - float(claim["reaction_temperature_K"])
                )
                - float(claim.get("temperature_tolerance_K", 0.0)),
                0.0,
            ),
            "reaction_duration_s": max(
                abs(float(controls["reaction_duration_s"]) - float(claim["reaction_duration_s"]))
                - float(claim.get("duration_tolerance_s", 0.0)),
                0.0,
            ),
        }
    if (
        "reaction_temperature_K" in reference_region
        and "reaction_duration_s" in reference_region
    ):
        if "reaction_temperature_K" not in controls or "reaction_duration_s" not in controls:
            return None
        return {
            "reaction_temperature_K": max(
                abs(
                    float(controls["reaction_temperature_K"])
                    - float(reference_region["reaction_temperature_K"])
                )
                - float(reference_region.get("temperature_tolerance_K", 0.0)),
                0.0,
            ),
            "reaction_duration_s": max(
                abs(
                    float(controls["reaction_duration_s"])
                    - float(reference_region["reaction_duration_s"])
                )
                - float(reference_region.get("duration_tolerance_s", 0.0)),
                0.0,
            ),
        }
    raise ValueError("unsupported supplied parametric initial-model claim")


def _rationale_score_match(
    recommendation: Mapping[str, Any],
    experiments: Sequence[Mapping[str, Any]],
) -> int | None:
    rationale = recommendation.get("selection_rationale")
    if not isinstance(rationale, str):
        return None
    for token in re.findall(r"(?<![\d.])0\.\d{4,}(?![\d.])", rationale):
        precision = len(token.split(".", 1)[1])
        matches = [
            int(row["experiment_index"])
            for row in experiments
            if f"{float(row['leaderboard_score']):.{precision}f}" == token
        ]
        if len(matches) == 1:
            return matches[0]
    return None


def _participant_behavior_profile(
    summary_path: Path,
    experiments: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    trajectory_path = summary_path.with_name("trajectory.jsonl")
    rows = load_jsonl(trajectory_path)
    status_counts: dict[str, int] = {}
    dynamic_failures = 0
    unsafe_operations = 0
    unsafe_experiments: set[int] = set()
    for row in rows:
        status = str(row.get("transaction_status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
        lab_report = _mapping(_mapping(row.get("agent_view")).get("lab_report"))
        flags = _mapping(lab_report.get("constraint_flags"))
        if flags.get("constitution_failed") is True:
            dynamic_failures += 1
        if flags.get("unsafe_by_task_limit") is True or flags.get("unsafe") is True:
            unsafe_operations += 1
            raw_index = row.get("experiment_index")
            if isinstance(raw_index, int) and not isinstance(raw_index, bool):
                unsafe_experiments.add(raw_index + 1)
    recipe_hashes = [
        canonical_json_sha256(list(_sequence(experiment.get("operations"))))
        for experiment in experiments
    ]
    return {
        "participant_record_count": len(rows),
        "operation_status_counts": status_counts,
        "dynamic_physical_failure_count": dynamic_failures,
        "public_unsafe_operation_count": unsafe_operations,
        "public_unsafe_experiment_indices": sorted(unsafe_experiments),
        "unique_recipe_count": len(set(recipe_hashes)),
        "exact_repeat_count": len(recipe_hashes) - len(set(recipe_hashes)),
        "trajectory": {
            "path": trajectory_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(trajectory_path),
        },
    }


def _prediction_rows_by_query(predictions: object) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for row in _sequence(predictions):
        if not isinstance(row, Mapping):
            continue
        query_id = str(row.get("query_id", ""))
        metrics = {
            str(metric.get("metric_id")): float(metric["mean"])
            for metric in _sequence(row.get("metrics"))
            if isinstance(metric, Mapping)
            and isinstance(metric.get("mean"), int | float)
            and not isinstance(metric.get("mean"), bool)
        }
        if query_id and metrics:
            result[query_id] = metrics
    return result


def _temperature_direction_diagnostic(
    predictions: object,
    *,
    truth_plan: Mapping[str, Any],
    reference_temperature_K: float,
    temperature_tolerance_K: float,
) -> dict[str, Any]:
    by_query = _prediction_rows_by_query(predictions)
    grouped: dict[float, dict[str, list[float]]] = {}
    for query in _sequence(truth_plan.get("queries")):
        if not isinstance(query, Mapping):
            continue
        features = _mapping(query.get("feature_values"))
        query_id = str(query.get("query_id", ""))
        metrics = by_query.get(query_id)
        temperature = features.get("reaction_temperature_K")
        duration = features.get("reaction_duration_s")
        if (
            metrics is None
            or "score" not in metrics
            or isinstance(temperature, bool)
            or not isinstance(temperature, int | float)
            or isinstance(duration, bool)
            or not isinstance(duration, int | float)
        ):
            continue
        if float(temperature) <= reference_temperature_K - temperature_tolerance_K:
            side = "lower_temperature"
        elif float(temperature) >= reference_temperature_K + temperature_tolerance_K:
            side = "higher_temperature"
        else:
            continue
        grouped.setdefault(float(duration), {}).setdefault(side, []).append(metrics["score"])
    contrasts: list[float] = []
    for sides in grouped.values():
        lower = sides.get("lower_temperature", [])
        higher = sides.get("higher_temperature", [])
        if lower and higher:
            contrasts.append(sum(lower) / len(lower) - sum(higher) / len(higher))
    mean_contrast = sum(contrasts) / len(contrasts) if contrasts else None
    preferred_side = (
        None
        if mean_contrast is None or mean_contrast == 0.0
        else "lower_temperature"
        if mean_contrast > 0.0
        else "higher_temperature"
    )
    return {
        "paired_duration_count": len(contrasts),
        "lower_minus_higher_mean_score_contrast": mean_contrast,
        "preferred_side": preferred_side,
    }


def _truth_prediction_rows(
    evaluator_truth: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "query_id": str(query_id),
            "metrics": [
                {"metric_id": str(metric_id), "mean": float(value)}
                for metric_id, value in _mapping(metrics).items()
                if isinstance(value, int | float) and not isinstance(value, bool)
            ],
        }
        for query_id, metrics in evaluator_truth.items()
    ]


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
        "misspecified_minus_opaque_best_endpoint": float(misspecified["best_observed_score"])
        - float(opaque["best_observed_score"]),
        "aligned_minus_opaque_best_endpoint": float(aligned["best_observed_score"])
        - float(opaque["best_observed_score"]),
        "H3_primary_contrast": report.get("cluster_contrast", {}).get("H3_primary_contrast"),
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
    terminal_trajectories = int(
        denominators.get(
            "participant_terminal_trajectory_count",
            denominators["participant_completed_cell_count"],
        )
    )
    scheduled_checkpoints = int(
        denominators.get(
            "participant_scheduled_checkpoint_count",
            denominators["participant_checkpoint_count"],
        )
    )
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
        int(_mapping(row.get("provider_usage")).get("recovered_mcp_tool_failure_count") or 0)
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
    held_out_change = _change_phrase(
        float(interpretation["misspecified_prediction_improvement"]),
        noun="Held-out prediction",
    )
    opaque_change = _change_phrase(
        float(interpretation["opaque_prediction_improvement"]),
        noun="opaque prediction",
    )
    aligned_change = _change_phrase(
        float(interpretation["aligned_prediction_improvement"]),
        noun="aligned prediction",
    )
    misspecified_change = _change_phrase(
        float(interpretation["misspecified_prediction_improvement"]),
        noun="misspecified prediction",
    )
    participant_operations = denominators["participant_operation_attempt_count"]
    logical_turns = denominators["participant_logical_codex_turn_count"]
    incumbent_count = interpretation["selected_observed_incumbent_count"]
    participant_count = interpretation["participant_cell_count"]
    lines = [
        "# Work II parametric initial-world-model pilot evaluation",
        "",
        "Development evidence only; no formal inference or private-transfer claim.",
        "",
        "## Exact denominators",
        "",
        (
            f"- Participant scientific trajectories: **{terminal_trajectories}/"
            f"{denominators['participant_cell_count']}** terminal; operationally qualified cells: "
            f"**{denominators['participant_completed_cell_count']}/"
            f"{denominators['participant_cell_count']}**."
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
            "| Arm | Best score | Pre error | Final error | Improvement | Law error | "
            "Direction | Unique/repeats | Unsafe/physical | Submitted→rationale | Blind gain |"
        ),
        "|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in report["cells"]:
        behavior = _mapping(row.get("participant_behavior"))
        direction = _mapping(row.get("temperature_direction"))
        index_diagnostic = _mapping(row.get("recommendation_index_diagnostic"))
        lines.append(
            f"| {row['prior_arm']} | {_format_value(row, 'best_observed_score')} | "
            f"{_format_value(row, 'effective_pre_error')} | "
            f"{_format_value(row, 'effective_final_error')} | "
            f"{_format_value(row, 'checkpoint_improvement')} | "
            f"{_format_value(row, 'law_summary_error')} | "
            f"{'yes' if direction.get('final_checkpoint_recovered') is True else 'no'} | "
            f"{behavior.get('unique_recipe_count', 0)}/{behavior.get('exact_repeat_count', 0)} | "
            f"{behavior.get('public_unsafe_operation_count', 0)}/"
            f"{behavior.get('dynamic_physical_failure_count', 0)} | "
            f"{row.get('selected_experiment_index')}→"
            f"{index_diagnostic.get('rationale_score_matched_experiment_index')} | "
            f"{_format_value(row, 'blind_recommendation_gain')} |"
        )
    lines.extend(
        [
            "",
            "## Operational profile",
            "",
            (
                f"The three persistent sessions recorded {participant_operations} "
                f"operation attempts and {logical_turns} logical Codex "
                f"turns. Provider accounting was {total_input:,} input tokens "
                f"({total_cached:,} cached; {total_uncached:,} uncached), "
                f"{total_output:,} output tokens, {total_recovered_mcp} recovered MCP failures, "
                f"{total_provider_errors} provider-error events "
                f"and a maximum session time of {max_session_elapsed:.1f} s."
            ),
            (
                f"Participant safety outcomes were "
                f"{denominators.get('participant_public_unsafe_operation_count', 0)} public "
                f"unsafe operations and "
                f"{denominators.get('participant_dynamic_physical_failure_count', 0)} dynamic "
                f"physical failures, with "
                f"{denominators.get('participant_resource_rejection_count', 0)} resource "
                f"rejections and {denominators.get('participant_platform_failure_count', 0)} "
                "platform failures. Unsafe or physically infeasible model-selected operations "
                "remain scientific outcomes rather than platform failures."
            ),
            "",
            "## Development interpretation",
            "",
            (
                f"In the misspecified arm, stated prior reliability {reliability_text}; "
                f"the trajectory challenged {challenged_text}. {held_out_change} while its best "
                f"observed endpoint {endpoint_text}. This separates endpoint search, prior "
                "self-report and held-out predictive correction rather than treating them as one "
                "outcome."
            ),
            "",
            (
                f"Across this single development world, {opaque_change}, {aligned_change}, "
                f"and {misspecified_change}. "
                f"The descriptive H3 contrast was {h3_text}; it is not an inferential result."
            ),
            "",
            (
                "All submitted recommendation indices are retained unchanged, but the action "
                "layer is platform-confounded: each rationale's first uniquely matched score "
                "identifies the 1-based observed incumbent while the submitted index is one "
                "smaller. Blind replay uses the actual submitted index; rationale-matched indices "
                "are diagnostic only, so the blind gap must not be attributed to participant "
                "action quality."
                if _mapping(report.get("action_layer")).get("status")
                == "platform_confounded_retained"
                else (
                    f"{incumbent_count}/{participant_count} final recommendations selected their "
                    "own observed incumbent. Paired blind replay checks reproducibility and "
                    "action commitment."
                )
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
    expected_experiment_count = _configured_experiment_count(config)
    expected_checkpoint_count = _configured_checkpoint_count(config)
    seeds = [int(seed) for seed in _sequence(matrix.get("world_seeds"))]
    if (
        len(seeds) != 1
        or matrix.get("all_cells_terminal") is not True
        or int(matrix.get("terminal_cell_count", 0)) != 3
    ):
        raise ValueError("participant run must be one terminal seed triplet")
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
    held_out_query_count = len(
        _sequence(_mapping(config.get("belief_checkpoint")).get("held_out_queries"))
    )
    print(
        json.dumps({"event": "truth_started", "queries": held_out_query_count}),
        flush=True,
    )
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
    failures.extend(
        {
            "scope": "participant_qualification",
            "prior_arm": arm,
            "error": list(_sequence(summary.get("qualification", {}).get("failed_checks"))),
        }
        for arm, (_, summary) in summaries.items()
        if summary.get("completed") is not True
    )
    evaluator_truth = _mapping(truth_report.get("truth"))
    reference_region = _mapping(
        _mapping(
            _mapping(_mapping(config["prior_arms"]["opaque"]).get("initial_world_model")).get(
                "context_contract"
            )
        ).get("approximate_reference_region")
    )
    reference_temperature_K = float(reference_region.get("reaction_temperature_K", 420.0))
    temperature_tolerance_K = float(reference_region.get("temperature_tolerance_K", 0.0))
    truth_direction = _temperature_direction_diagnostic(
        _truth_prediction_rows(evaluator_truth),
        truth_plan=truth_plan,
        reference_temperature_K=reference_temperature_K,
        temperature_tolerance_K=temperature_tolerance_K,
    )
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
            terminal_state=(
                "completed"
                if _scientific_trajectory_complete(summary, expected_experiment_count)
                else "failed"
            ),
            snapshot_stages=[str(stage) for stage in _sequence(config.get("snapshot_stages"))],
        )
        pre_snapshot = _snapshot(analysis, "pre_evidence")
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
        blind_contract = dict(_mapping(design["blind_evaluator_contract"]))
        blind_contract["participant_complete_experiments_per_cell"] = (
            expected_experiment_count
        )
        blind_contract["candidate_experiment_indices"] = list(
            range(1, expected_experiment_count + 1)
        )
        blind_plan = build_blind_evaluation_plan(
            cell,
            summary,
            blind_contract,
            allow_unqualified_terminal_trajectory=(
                summary.get("completed") is not True
                and _scientific_trajectory_complete(summary, expected_experiment_count)
            ),
        )
        blind_report = execute_blind_evaluation_plan(blind_plan, config, blind_root)
        blind_receipts = _blind_receipts(blind_root, blind_report)
        blind_errors = validate_blind_evaluation_report(blind_report, blind_plan, blind_receipts)
        failures.extend(
            {"scope": "blind", "prior_arm": arm, "error": error} for error in blind_errors
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
            controls = _parametric_controls(experiment, task_id)
            settings.append(
                {
                    "experiment_index": int(experiment["experiment_index"]),
                    "parametric_controls": controls,
                    "leaderboard_score": float(experiment["leaderboard_score"]),
                    "distance_to_supplied_model": _supplied_model_distance(controls, model),
                }
            )
        reliability = list(_sequence(analysis.get("prior_reliability_trajectory")))
        recommendation = _mapping(analysis.get("final_recommendation"))
        rationale_intended_index = _rationale_score_match(recommendation, experiments)
        submitted_index = recommendation.get("selected_experiment_index")
        observed_incumbent_index = analysis.get("observed_incumbent_experiment_index")
        index_contract_confounded = (
            isinstance(rationale_intended_index, int)
            and rationale_intended_index != submitted_index
            and rationale_intended_index == observed_incumbent_index
        )
        behavior = _participant_behavior_profile(summary_path, experiments)
        pre_direction = _temperature_direction_diagnostic(
            pre_snapshot.get("predictions") if pre_snapshot is not None else None,
            truth_plan=truth_plan,
            reference_temperature_K=reference_temperature_K,
            temperature_tolerance_K=temperature_tolerance_K,
        )
        final_direction = _temperature_direction_diagnostic(
            final_snapshot.get("predictions") if final_snapshot is not None else None,
            truth_plan=truth_plan,
            reference_temperature_K=reference_temperature_K,
            temperature_tolerance_K=temperature_tolerance_K,
        )
        law_direction = _temperature_direction_diagnostic(
            law.get("query_predictions"),
            truth_plan=truth_plan,
            reference_temperature_K=reference_temperature_K,
            temperature_tolerance_K=temperature_tolerance_K,
        )
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
                "participant_trajectory_state": (
                    "completed"
                    if _scientific_trajectory_complete(summary, expected_experiment_count)
                    else "failed"
                ),
                "participant_qualification_passed": _mapping(summary.get("qualification")).get(
                    "passed"
                )
                is True,
                "complete_experiment_count": int(analysis.get("complete_experiment_count", 0)),
                "operation_attempt_count": int(analysis.get("operation_attempt_count", 0)),
                "checkpoint_count": len(_sequence(analysis.get("belief_snapshots"))),
                "experiments": settings,
                "best_observed_score": max(
                    float(item["leaderboard_score"]) for item in experiments
                ),
                "observed_incumbent_experiment_index": observed_incumbent_index,
                "selected_experiment_index": submitted_index,
                "recommendation_index_diagnostic": {
                    "submitted_index_retained": True,
                    "submitted_selected_experiment_index": submitted_index,
                    "rationale_score_matched_experiment_index": rationale_intended_index,
                    "observed_incumbent_experiment_index": observed_incumbent_index,
                    "index_contract_confounded": index_contract_confounded,
                    "action_layer_attribution": (
                        "platform_confounded"
                        if index_contract_confounded
                        else "participant_interpretable"
                    ),
                },
                "participant_behavior": {
                    **behavior,
                    "resource_rejection_count": int(
                        analysis.get("resource_rejection_count", 0)
                    ),
                    "platform_failure_count": 0,
                },
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
                "temperature_direction": {
                    "truth": truth_direction,
                    "pre_evidence": pre_direction,
                    "final_checkpoint": final_direction,
                    "final_law_summary": law_direction,
                    "final_checkpoint_recovered": (
                        final_direction.get("preferred_side")
                        == truth_direction.get("preferred_side")
                        and truth_direction.get("preferred_side") is not None
                    ),
                    "final_law_summary_recovered": (
                        law_direction.get("preferred_side")
                        == truth_direction.get("preferred_side")
                        and truth_direction.get("preferred_side") is not None
                    ),
                },
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
            "participant_terminal_trajectory_count": sum(
                row["participant_trajectory_state"] == "completed" for row in cells
            ),
            "participant_scheduled_experiment_count": (
                len(cells) * expected_experiment_count
            ),
            "participant_complete_experiment_count": sum(
                int(row["complete_experiment_count"]) for row in cells
            ),
            "participant_operation_attempt_count": sum(
                int(row["operation_attempt_count"]) for row in cells
            ),
            "participant_checkpoint_count": sum(int(row["checkpoint_count"]) for row in cells),
            "participant_scheduled_checkpoint_count": (
                len(cells) * expected_checkpoint_count
            ),
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
            "participant_dynamic_physical_failure_count": sum(
                int(_mapping(row["participant_behavior"]).get("dynamic_physical_failure_count", 0))
                for row in cells
            ),
            "participant_public_unsafe_operation_count": sum(
                int(_mapping(row["participant_behavior"]).get("public_unsafe_operation_count", 0))
                for row in cells
            ),
            "participant_resource_rejection_count": sum(
                int(_mapping(row["participant_behavior"]).get("resource_rejection_count", 0))
                for row in cells
            ),
            "participant_platform_failure_count": sum(
                int(_mapping(row["participant_behavior"]).get("platform_failure_count", 0))
                for row in cells
            ),
        },
        "cluster_contrast": cluster_rows[0] if len(cluster_rows) == 1 else None,
        "truth_report_sha256": truth_report.get("report_sha256"),
        "truth_temperature_direction": truth_direction,
        "action_layer": {
            "status": (
                "platform_confounded_retained"
                if any(
                    _mapping(row.get("recommendation_index_diagnostic")).get(
                        "index_contract_confounded"
                    )
                    is True
                    for row in cells
                )
                else "participant_interpretable"
            ),
            "submitted_recommendations_replaced": False,
            "blind_replay_uses_actual_submitted_index": True,
            "rationale_intended_index_is_diagnostic_only": True,
        },
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
