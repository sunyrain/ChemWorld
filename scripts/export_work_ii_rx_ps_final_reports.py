#!/usr/bin/env python3
"""Export the complete public RX P/S 60-cell result and report package."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.export_work_ii_rx_ps_interim_reports as interim  # noqa: E402

STAGES = ("K1", "Q", "K2")
EXPECTED_WORLDS = tuple(f"RX-W{index:02d}" for index in range(1, 6))


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def safe_recovery(result: Mapping[str, Any], result_path: Path) -> dict[str, Any] | None:
    recovery = result.get("recovery")
    if not isinstance(recovery, Mapping):
        return None
    keys = (
        "recovery_version",
        "retained_failure_kind",
        "repair_stages",
        "source_experiments_rerun",
        "thread_reused",
        "truth_revealed_to_agent",
        "question_changed",
        "model_changed",
        "original_operations",
        "original_batches",
        "frozen_cell_reused",
        "deterministic_seeds_reused",
        "platform_fix",
    )
    return {
        "effective_result_version": result_path.parent.name,
        **{key: recovery[key] for key in keys if key in recovery},
    }


def public_result(
    result_path: Path,
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Any],
    retest: Mapping[str, Any],
) -> dict[str, Any]:
    posttests = result.get("posttests") or {}
    return {
        "schema_version": "work-ii-rx-ps-public-final-cell-1.0",
        "cell": {
            key: result.get(key)
            for key in (
                "cell_id",
                "world_id",
                "world_seed",
                "locus",
                "goal",
                "arm",
                "status",
                "source_status",
                "operations",
                "posttest_chain_sealed",
            )
        },
        "source": {
            "batches": result.get("batches") or [],
            "recommendation": result.get("recommendation") or {},
            "exact_replay": result.get("exact_replay") or {},
            "rollbacks": result.get("rollbacks") or [],
        },
        "posttests": {
            stage: {
                "payload": (posttests.get(stage) or {}).get("payload"),
                "validation": ((result.get("posttest_validation") or {}).get(stage) or {}),
            }
            for stage in STAGES
        },
        "prediction_evaluation": evaluation,
        "reference_truth": truth,
        "recommendation_retest": retest,
        "recovery": safe_recovery(result, result_path),
        "excluded_private_fields": [
            "credentials",
            "provider event streams",
            "provider stderr",
            "thread identifiers",
            "token accounting",
        ],
    }


def truth_means(truth: Mapping[str, Sequence[Mapping[str, Any]]]) -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for query_id, repeats in truth.items():
        metrics = sorted(repeats[0]) if repeats else []
        output[query_id] = {
            metric: fmean(float(row[metric]) for row in repeats) for metric in metrics
        }
    return output


def recommendation_comparison(
    result: Mapping[str, Any], retest: Mapping[str, Any]
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    selected_index = (result.get("recommendation") or {}).get("selected_experiment_index")
    selected = next(
        (
            row
            for row in result.get("batches", [])
            if row.get("lifecycle_index") == selected_index
        ),
        {},
    )
    retest_batch = (retest.get("batches") or [{}])[0]
    return selected, retest_batch


def render_final_sections(
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, Any]]],
    retest: Mapping[str, Any],
) -> list[str]:
    lines = [
        "## Blind-prediction evaluation",
        "",
        "| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |",
        "|---|---:|---:|---:|---:|",
    ]
    for metric, values in sorted((evaluation.get("metrics") or {}).items()):
        lines.append(
            f"| {metric} | {interim.fmt_number(values.get('mae_to_five_repeat_mean'))} | "
            f"{interim.fmt_number(values.get('empirical_coverage80'))} | "
            f"{interim.fmt_number(values.get('mean_width80'))} | "
            f"{interim.fmt_number(values.get('mean_interval_score_alpha_0_2'))} |"
        )

    predictions = {
        row["query_id"]: row
        for row in (((result.get("posttests") or {}).get("Q") or {}).get("payload") or {}).get(
            "predictions", []
        )
    }
    means = truth_means(truth)
    lines.extend(["", "## Predictions versus released reference truth", ""])
    for query_id in sorted(truth):
        lines.extend(
            [
                f"### {query_id}",
                "",
                "| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |",
                "|---|---:|---:|---:|---:|---|",
            ]
        )
        prediction_metrics = (predictions.get(query_id) or {}).get("metrics") or {}
        for metric in sorted(means[query_id]):
            prediction = prediction_metrics.get(metric) or {}
            repeats = ", ".join(
                interim.fmt_number(row.get(metric)) for row in truth[query_id]
            )
            lines.append(
                f"| {metric} | {interim.fmt_number(prediction.get('estimate'))} | "
                f"{interim.fmt_number(prediction.get('lower80'))} | "
                f"{interim.fmt_number(prediction.get('upper80'))} | "
                f"{interim.fmt_number(means[query_id][metric])} | {repeats} |"
            )

    selected, retest_batch = recommendation_comparison(result, retest)
    selected_metrics = selected.get("metrics") or {}
    retest_metrics = retest_batch.get("metrics") or {}
    lines.extend(
        [
            "",
            "## Recommendation retest",
            "",
            f"- Selected source batch: `{(result.get('recommendation') or {}).get('selected_experiment_index')}`",
            f"- Retest exact replay verified: `{bool((retest.get('exact_replay') or {}).get('verified'))}`",
            f"- Retest failure: `{retest.get('failure') or 'none'}`",
            "",
            "| Metric | Selected source batch | Independent retest | Retest minus source |",
            "|---|---:|---:|---:|",
        ]
    )
    for metric in sorted(set(selected_metrics) & set(retest_metrics)):
        if not isinstance(selected_metrics[metric], (int, float)) or not isinstance(
            retest_metrics[metric], (int, float)
        ):
            continue
        lines.append(
            f"| {metric} | {interim.fmt_number(selected_metrics[metric])} | "
            f"{interim.fmt_number(retest_metrics[metric])} | "
            f"{interim.fmt_number(float(retest_metrics[metric]) - float(selected_metrics[metric]))} |"
        )
    return lines


def render_final_report(
    result_path: Path,
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, Any]]],
    retest: Mapping[str, Any],
) -> str:
    report = interim.render_report(result_path, result)
    report, separator, _ = report.partition("\n## Scope note\n")
    if not separator:
        raise RuntimeError("interim report scope marker is missing")
    final_sections = render_final_sections(result, evaluation, truth, retest)
    final_sections.extend(
        [
            "",
            "## Scope note",
            "",
            "This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.",
            "",
        ]
    )
    return report.rstrip() + "\n\n" + "\n".join(final_sections)


def validate_completion(root: Path, schedule: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    completion = load(root / "recovery-v11-parallel4-transport-repair" / "completion.json")
    expected = {
        "source_sessions": 60,
        "source_batches": 720,
        "posttests": 180,
        "reference_executions": 600,
        "recommendation_retests": 60,
    }
    if len(schedule) != 60 or any(completion.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"final completion denominators do not match: {completion}")
    summary = load(root / "recovery-v11-parallel4-transport-repair" / "summary.json")
    if (
        summary.get("phase") != "complete"
        or summary.get("effective_sources") != 60
        or summary.get("effective_source_batches") != 720
        or summary.get("sealed_posttest_chains") != 60
        or summary.get("failures")
    ):
        raise RuntimeError("v11 recovery summary is not a clean 60-cell completion")
    return completion


def mean(values: Sequence[Any]) -> float:
    numeric = [float(value) for value in values if isinstance(value, (int, float))]
    if not numeric:
        raise RuntimeError("cannot summarize an empty numeric group")
    return fmean(numeric)


def render_aggregate_report(
    rows: Sequence[Mapping[str, Any]], completion: Mapping[str, Any]
) -> str:
    lines = [
        "# RX P/S five-world dual-goal block — aggregate final report",
        "",
        "## Completion and evidence boundary",
        "",
        f"The development block completed {completion['source_sessions']}/60 independent source sessions, "
        f"{completion['source_batches']}/720 experimental batches, {completion['posttests']}/180 sealed "
        f"K1/Q/K2 posttests, {completion['reference_executions']}/600 provider-free reference executions, "
        f"and {completion['recommendation_retests']}/60 independent recommendation retests. All effective "
        "cells completed without a retained final failure; original platform failures remain preserved outside "
        "the effective denominator.",
        "",
        "Reference truth was generated only after all 60 posttest chains were sealed. The aggregate values below "
        "describe the completed development block; they are not a formal causal estimate of prior-arm effects "
        "because each agent followed an adaptive experimental trajectory.",
        "",
        "## Aggregate by locus, task, and prior arm",
        "",
        "Each row averages five worlds. Prediction columns macro-average the six scored Q metrics within each cell, then average cells.",
        "",
        "| Locus | Task | Arm | Cells | Selected source score | Retest score | Retest delta | Prediction MAE | 80% coverage | Interval score |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for locus in ("P", "S"):
        for goal in ("mechanism_discovery", "safety_constrained_optimization"):
            for arm in ("Opaque", "Aligned", "MisIndexed"):
                group = [
                    row
                    for row in rows
                    if row["locus"] == locus and row["goal"] == goal and row["arm"] == arm
                ]
                if len(group) != 5:
                    raise RuntimeError(f"aggregate group is not five worlds: {locus}/{goal}/{arm}")
                lines.append(
                    f"| {locus} | {goal} | {arm} | {len(group)} | "
                    f"{interim.fmt_number(mean([row['selected_source_score'] for row in group]))} | "
                    f"{interim.fmt_number(mean([row['recommendation_retest_score'] for row in group]))} | "
                    f"{interim.fmt_number(mean([row['recommendation_score_delta'] for row in group]))} | "
                    f"{interim.fmt_number(mean([row['prediction_macro_mae'] for row in group]))} | "
                    f"{interim.fmt_number(mean([row['prediction_macro_coverage80'] for row in group]))} | "
                    f"{interim.fmt_number(mean([row['prediction_macro_interval_score'] for row in group]))} |"
                )

    lines.extend(
        [
            "",
            "## Aggregate by world",
            "",
            "| World | Cells | Selected source score | Retest score | Retest delta | Prediction MAE | 80% coverage |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for world in EXPECTED_WORLDS:
        group = [row for row in rows if row["world_id"] == world]
        lines.append(
            f"| {world} | {len(group)} | "
            f"{interim.fmt_number(mean([row['selected_source_score'] for row in group]))} | "
            f"{interim.fmt_number(mean([row['recommendation_retest_score'] for row in group]))} | "
            f"{interim.fmt_number(mean([row['recommendation_score_delta'] for row in group]))} | "
            f"{interim.fmt_number(mean([row['prediction_macro_mae'] for row in group]))} | "
            f"{interim.fmt_number(mean([row['prediction_macro_coverage80'] for row in group]))} |"
        )

    lines.extend(
        [
            "",
            "## Highest independent recommendation retests",
            "",
            "| Rank | Cell | Retest score | Selected source score | Delta |",
            "|---:|---|---:|---:|---:|",
        ]
    )
    ranked = sorted(rows, key=lambda row: float(row["recommendation_retest_score"]), reverse=True)
    for rank, row in enumerate(ranked[:10], start=1):
        lines.append(
            f"| {rank} | [{row['cell_id']}]({row['world_id']}/{row['cell_id']}/EXPERIMENT_REPORT.md) | "
            f"{interim.fmt_number(row['recommendation_retest_score'])} | "
            f"{interim.fmt_number(row['selected_source_score'])} | "
            f"{interim.fmt_number(row['recommendation_score_delta'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation constraints",
            "",
            "- `mechanism_discovery` and `safety_constrained_optimization` are separate source sessions; their outcomes should not be treated as repeated measurements of one policy.",
            "- Opaque, Aligned, and MisIndexed arms differ in prior information, but adaptive experiment choices can mediate observed score and prediction differences. The five-world means are descriptive rather than a preregistered inferential test.",
            "- Reference outcomes use five independent observation repeats per query. Coverage is empirical over 60 reference observations per metric and cell; it is not a confidence interval on population coverage.",
            "- A high selected source score is sample-internal. The independent retest and its delta are the relevant repeatability check, not proof of global optimality.",
            "- K1 and K2 remain qualitative research artifacts. This export preserves them verbatim but does not impose an after-the-fact mechanistic correctness score.",
            "",
            "For full evidence, use the per-cell reports and JSON results linked from the five world indices. [SUMMARY.json](SUMMARY.json) contains the aggregate machine-readable table.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.run_root.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"write-once export already exists: {output}")
    design = load(root / "design.json")
    schedule = design["schedule"]
    completion = validate_completion(root, schedule)
    truth_all = load(root / "truth.json")
    output.mkdir(parents=True)

    rows: list[dict[str, Any]] = []
    for cell in schedule:
        cell_id = str(cell["cell_id"])
        result_path, result = interim.resolve_result(root, cell_id)
        validations = result.get("posttest_validation") or {}
        if (
            result.get("status") != "completed"
            or result.get("source_status") != "completed"
            or len(result.get("batches", [])) != 12
            or result.get("posttest_chain_sealed") is not True
            or not all((validations.get(stage) or {}).get("valid") is True for stage in STAGES)
        ):
            raise RuntimeError(f"cell is not a sealed final result: {cell_id}")

        evaluation = load(root / "evaluations" / f"{cell_id}.json")
        truth = truth_all[result["world_id"]][result["locus"]]
        retest = load(root / "recommendation-retests" / cell_id / "result.json")
        if evaluation.get("valid") is not True:
            raise RuntimeError(f"invalid evaluation: {cell_id}")
        if len(truth) != 12 or any(len(repeats) != 5 for repeats in truth.values()):
            raise RuntimeError(f"invalid reference truth denominator: {cell_id}")
        if (
            retest.get("failure")
            or len(retest.get("batches", [])) != 1
            or retest.get("rollbacks")
            or (retest.get("exact_replay") or {}).get("verified") is not True
        ):
            raise RuntimeError(f"invalid recommendation retest: {cell_id}")

        cell_dir = output / result["world_id"] / cell_id
        cell_dir.mkdir(parents=True)
        public = public_result(result_path, result, evaluation, truth, retest)
        dump(cell_dir / "RESULT.json", public)
        (cell_dir / "EXPERIMENT_REPORT.md").write_text(
            render_final_report(result_path, result, evaluation, truth, retest),
            encoding="utf-8",
        )
        selected, retest_batch = recommendation_comparison(result, retest)
        source_score = (selected.get("metrics") or {}).get("score")
        retest_score = (retest_batch.get("metrics") or {}).get("score")
        rows.append(
            {
                "cell_id": cell_id,
                "world_id": result["world_id"],
                "locus": result["locus"],
                "goal": result["goal"],
                "arm": result["arm"],
                "source_batches": 12,
                "posttests_valid": 3,
                "reference_observations": 60,
                "recommendation_retests": 1,
                "recovered": result.get("recovery") is not None,
                "selected_source_score": source_score,
                "recommendation_retest_score": retest_score,
                "recommendation_score_delta": (
                    float(retest_score) - float(source_score)
                    if isinstance(source_score, (int, float))
                    and isinstance(retest_score, (int, float))
                    else None
                ),
                "prediction_macro_mae": mean(
                    [
                        metric["mae_to_five_repeat_mean"]
                        for metric in (evaluation.get("metrics") or {}).values()
                    ]
                ),
                "prediction_macro_coverage80": mean(
                    [
                        metric["empirical_coverage80"]
                        for metric in (evaluation.get("metrics") or {}).values()
                    ]
                ),
                "prediction_macro_interval_score": mean(
                    [
                        metric["mean_interval_score_alpha_0_2"]
                        for metric in (evaluation.get("metrics") or {}).values()
                    ]
                ),
                "prediction_evaluation": evaluation,
            }
        )

    for world in EXPECTED_WORLDS:
        world_rows = [row for row in rows if row["world_id"] == world]
        if len(world_rows) != 12:
            raise RuntimeError(f"expected 12 final reports for {world}, found {len(world_rows)}")
        lines = [f"# {world} final report index", ""]
        for row in world_rows:
            lines.append(
                f"- [{row['cell_id']}]({row['cell_id']}/EXPERIMENT_REPORT.md) — "
                f"[machine-readable result]({row['cell_id']}/RESULT.json)"
            )
        lines.append("")
        (output / world / "WORLD_INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    aggregate = {
        "schema_version": "work-ii-rx-ps-public-final-summary-1.0",
        "development_evidence": True,
        "phase": "complete",
        **{key: completion[key] for key in (
            "source_sessions",
            "source_batches",
            "posttests",
            "reference_executions",
            "recommendation_retests",
            "original_failures_preserved",
            "parallel_workers",
        )},
        "complete_cells": len(rows),
        "worlds": list(EXPECTED_WORLDS),
        "cells": rows,
        "excluded_private_fields": [
            "credentials",
            "provider event streams",
            "provider stderr",
            "thread identifiers",
            "token accounting",
            "ignored run directories",
        ],
    }
    dump(output / "SUMMARY.json", aggregate)
    (output / "REPORT.md").write_text(
        render_aggregate_report(rows, completion), encoding="utf-8"
    )
    readme = [
        "# RX P/S five-world dual-goal block — final 60-cell reports",
        "",
        "Date: 2026-09-19. Status: complete development evidence.",
        "",
        "This write-once package contains the complete sanitized result surface for the frozen RX P/S block:",
        "",
        "- 60/60 task cells across five worlds, P/S loci, two goals, and three prior arms;",
        "- 720/720 source experiments (12 per cell);",
        "- 180/180 valid sealed posttests (K1, Q, K2);",
        "- 600/600 provider-free reference executions (five repeats for each of 12 queries in each world/locus);",
        "- 60/60 independent recommendation retests;",
        "- complete experiment actions and observations, recommendations, K1 reports, Q predictions and rationales, K2 retrospectives, prediction evaluations, released reference truth, and retest comparisons.",
        "",
        "Each cell contains a readable `EXPERIMENT_REPORT.md` and an explicitly whitelisted `RESULT.json`. Raw provider streams, credentials, provider stderr, thread identifiers, token accounting, and ignored run directories are excluded.",
        "",
        "The original transport failures and all recovery evidence remain preserved in the server run; effective results are selected without overwriting the retained failures. See the [v11 recovery record](../../WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V11.md).",
        "",
        "World indices: " + ", ".join(f"[{world}]({world}/WORLD_INDEX.md)" for world in EXPECTED_WORLDS) + ".",
        "",
        "Aggregate interpretation: [REPORT.md](REPORT.md). Machine-readable aggregate: [SUMMARY.json](SUMMARY.json).",
        "",
    ]
    (output / "README.md").write_text("\n".join(readme), encoding="utf-8")


if __name__ == "__main__":
    main()
