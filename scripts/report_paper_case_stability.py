"""Read-only descriptive stability report; no provider or simulator calls."""

from __future__ import annotations

import argparse
import json
from statistics import fmean, stdev

from scripts.report_paper_case_notebooks import export
from scripts.run_paper_case_notebooks import CASES, ROOT, read, write
from scripts.run_paper_case_stability import REPEATS


def describe(values):
    observed = [v for v in values if v is not None]
    return {
        "planned": len(values),
        "observed": len(observed),
        "missing": len(values) - len(observed),
        "mean": fmean(observed) if observed else None,
        "sample_sd": stdev(observed) if len(observed) > 1 else None,
        "minimum": min(observed) if observed else None,
        "maximum": max(observed) if observed else None,
    }


def measurements(row):
    output = {}
    evaluation = row.get("prediction_evaluation") or {}
    if evaluation.get("valid"):
        for name, value in evaluation.get("metrics", {}).items():
            output[f"{name}_mae"] = value.get("mae")
            output[f"{name}_coverage80"] = value.get("coverage80")
    retests = row.get("retest_batch_metrics", [])
    if row["system"] == "EC":
        output["recommendation_score"] = retests[0].get("score") if len(retests) == 1 else None
    if row["system"] == "EQ":
        diagnostic = row.get("equilibrium_diagnostics") or {}
        concentrations = [
            b["nominal_concentration_M"]
            for b in diagnostic.get("batch_concentrations", [])
            if b["nominal_concentration_M"] is not None and b["nominal_concentration_M"] > 0
        ]
        output["minimum_positive_concentration_M"] = min(concentrations) if concentrations else None
        output["sampled_below_1mM"] = int(min(concentrations) < 0.001) if concentrations else None
        for name, group in (diagnostic.get("prediction_groups") or {}).items():
            for metric in ("macro_mae", "covered", "coverage_denominator", "coverage80"):
                output[f"{name}_{metric}"] = group.get(metric)
    if row["system"] == "C":
        quality = evaluation.get("quality") or {}
        output["quality_correct_of_12"] = (
            quality["true_positive"] + quality["true_negative"]
            if evaluation.get("valid") and quality
            else None
        )
        truths = (row.get("retest") or {}).get("truth") or []
        for metric in ("crystal_yield", "crystal_purity", "crystal_fines_fraction"):
            output[f"recommendation_true_{metric}"] = (
                truths[0][metric] if len(truths) == 1 else None
            )
        fines = output["recommendation_true_crystal_fines_fraction"]
        output["recommendation_fines_margin"] = 0.5 - fines if fines is not None else None
        for contrast in evaluation.get("contrasts", []):
            if (
                contrast["factor"] == "thermal_history"
                and contrast["metric"] == "crystal_fines_fraction"
            ):
                for key in ("predicted_delta", "true_delta", "absolute_delta_error"):
                    output[f"thermal_fines_{key}"] = contrast[key]
                output["thermal_fines_direction_correct"] = int(contrast["direction_correct"])
        predictions = ((row.get("posttests", {}).get("Q") or {}).get("payload") or {}).get(
            "predictions", []
        )
        for prediction in predictions:
            if prediction["query_id"] in {"Q07", "Q08"}:
                prefix = prediction["query_id"]
                interval = prediction.get("crystal_fines_fraction") or {}
                output[f"{prefix}_fines_prediction"] = interval.get("estimate")
                feasible = prediction.get("quality_feasible")
                output[f"{prefix}_predicted_feasible"] = (
                    int(feasible) if isinstance(feasible, bool) else None
                )
    return output


def directional_comparison(rows, first, second, metric, greater):
    outcomes = []
    for repeat in REPEATS:
        a = rows[(repeat, first)]["measurements"].get(metric)
        b = rows[(repeat, second)]["measurements"].get(metric)
        outcomes.append(None if a is None or b is None else (b > a if greater else b < a))
    return {
        "first": first,
        "second": second,
        "metric": metric,
        "test": "second > first" if greater else "second < first",
        "by_repeat": dict(zip(REPEATS, outcomes, strict=True)),
        "holds": sum(v is True for v in outcomes),
        "observed": sum(v is not None for v in outcomes),
        "planned": 3,
    }


def number(value):
    return "—" if value is None else f"{value:.6g}"


def build(root, destination, previous):
    destination.mkdir(parents=True, exist_ok=True)
    summaries = {
        repeat: export(root / repeat, destination / repeat, review_link="../REVIEW.md")
        for repeat in REPEATS
    }
    rows = {}
    for repeat, summary in summaries.items():
        for case in CASES:
            path = destination / repeat / f"{case['id']}.json"
            row = (
                read(path)
                if path.exists()
                else next(r for r in summary["cases"] if r["id"] == case["id"])
            )
            rows[(repeat, case["id"])] = {
                "repeat": repeat,
                "case": case["id"],
                "status": row["status"],
                "failure": row["failure"],
                "completed_batches": row["completed_batches"],
                "planned_batches": case["batches"],
                "measurements": measurements(row),
                "notebook": {
                    k: row["notebook"][k]
                    for k in (
                        "version_count",
                        "read_calls",
                        "tool_failures",
                        "initial_note_before_action",
                    )
                },
                "token_accounting": row["token_accounting"],
                "prediction_valid": (row.get("prediction_evaluation") or {}).get("valid"),
                "posttest_status": {
                    stage: {
                        "submitted": bool(
                            (row.get("posttests", {}).get(stage) or {}).get("payload")
                        ),
                        "failure": (row.get("posttests", {}).get(stage) or {}).get("failure"),
                        "record_present": stage in row.get("posttests", {}),
                    }
                    for stage in ("K1", "Q", "K2", *(("EQS",) if case["system"] == "EQ" else ()))
                },
            }
    groups = {}
    for case in CASES:
        current = [rows[(repeat, case["id"])] for repeat in REPEATS]
        prior = measurements(read(previous / f"{case['id']}.json"))
        names = sorted(set(prior).union(*(r["measurements"] for r in current)))
        groups[case["id"]] = {
            "completed": sum(r["status"] == "completed" for r in current),
            "planned": 3,
            "measurements": {
                name: {
                    "previous_separate": prior.get(name),
                    "new_repeats": [r["measurements"].get(name) for r in current],
                    **describe([r["measurements"].get(name) for r in current]),
                }
                for name in names
            },
        }
    comparisons = [
        directional_comparison(
            rows, "EC-discovery", "EC-optimization", "recommendation_score", True
        ),
        directional_comparison(rows, "EC-discovery", "EC-optimization", "score_mae", False),
        directional_comparison(rows, "C-12", "C-24", "quality_correct_of_12", True),
        *[
            directional_comparison(rows, "C-12", "C-24", f"{name}_mae", False)
            for name in (
                "crystal_yield",
                "crystal_purity",
                "crystal_size",
                "crystal_fines_fraction",
            )
        ],
    ]
    counted = (
        "terminal_sources",
        "completed_sources",
        "completed_batches",
        "completed_posttests",
        "source_operations",
        "source_rollbacks",
        "laboratory_tool_failures",
        "notebook_tool_failures",
        "source_provider_process_attempts",
        "recommendation_retest_batches",
        "recommendation_retest_operations",
        "recommendation_retests_replayed",
        "source_replays_verified",
        "notebook_versions",
        "notebook_read_calls",
        "token_accounting_complete_cases",
        "observed_input_plus_output_tokens",
    )
    summary = {
        "scope": "Three fresh sessions per fixed case; descriptive development evidence",
        "planned_sources": 18,
        "planned_source_batches": 252,
        "planned_posttests": 60,
        "previous_cases_excluded_from_repeat_statistics": True,
        "counts": {key: sum(s[key] for s in summaries.values()) for key in counted},
        "reference_batches": sum(
            s["reference_accounting"]["completed_batches"] for s in summaries.values()
        ),
        "reference_operations": sum(
            s["reference_accounting"]["operations"] for s in summaries.values()
        ),
        "reference_replays_verified": sum(
            bool((row.get("exact_replay") or {}).get("verified"))
            for s in summaries.values()
            for row in s["reference_accounting"]["runs"]
        ),
        "source_commits": {repeat: s["source_commit"] for repeat, s in summaries.items()},
        "cases": list(rows.values()),
        "case_statistics": groups,
        "directional_comparisons": comparisons,
        "block_stop": read(root / "block-stop.json")
        if (root / "block-stop.json").exists()
        else None,
    }
    first = root / REPEATS[0]
    summary["fixed_inputs_equal_between_repeats"] = {
        repeat: all(
            read(first / relative) == read(root / repeat / relative)
            for relative in (
                "inputs/EC-discovery.json",
                "inputs/EC-optimization.json",
                "inputs/C.json",
                "C/design.json",
            )
        )
        and read(first / "design.json")["eq_config"]
        == read(root / repeat / "design.json")["eq_config"]
        for repeat in REPEATS[1:]
    }
    summary["reference_values_equal_between_repeats"] = {}
    for repeat in REPEATS[1:]:
        relatives = ("references/truth.json", "C/qualification/W05/queries/result.json")
        if all((root / repeat / p).exists() and (first / p).exists() for p in relatives):
            summary["reference_values_equal_between_repeats"][repeat] = (
                read(first / relatives[0]) == read(root / repeat / relatives[0])
                and read(first / relatives[1])["truth"]
                == read(root / repeat / relatives[1])["truth"]
            )
        else:
            summary["reference_values_equal_between_repeats"][repeat] = None
    write(destination / "summary.json", summary)
    counts = summary["counts"]
    lines = [
        "# Fixed-case notebook stability — three fresh repetitions",
        "",
        "Descriptive development results. The previous six cases are separate references, "
        "excluded from means and sample SDs. Each case has three planned independent sessions; "
        "batches, predictions and reference observations are not independent Agent replicates.",
        "",
        f"Terminal {counts['terminal_sources']}/18; "
        f"complete chains {counts['completed_sources']}/18; "
        f"source batches {counts['completed_batches']}/252; sealed posttests "
        f"{counts['completed_posttests']}/60.",
        "",
        "| Case | Repeat | Status | Batches | Note versions | Reads | Record |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows.values():
        prefix = f"{row['repeat']}/{row['case']}"
        lines.append(
            f"| {row['case']} | {row['repeat']} | {row['status']} | "
            f"{row['completed_batches']}/{row['planned_batches']} | "
            f"{row['notebook']['version_count']} | {row['notebook']['read_calls']} | "
            f"[notes]({prefix}-notebook.md), [reports]({prefix}-reports.md) |"
        )
    for case, group in groups.items():
        lines += [
            "",
            f"## {case}",
            "",
            "| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
        for name, stats in group["measurements"].items():
            values = " | ".join(number(v) for v in stats["new_repeats"])
            lines.append(
                f"| {name} | {number(stats['previous_separate'])} | {values} | "
                f"{stats['observed']}/3 | {number(stats['mean'])} | {number(stats['sample_sd'])} | "
                f"{number(stats['minimum'])} to {number(stats['maximum'])} |"
            )
    lines += [
        "",
        "## Direction recurrence",
        "",
        "Round labels organize comparisons; they do not pair provider sampling randomness.",
        "",
        "| Comparison | Metric | Test | Holds / planned | Observed / planned |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for comparison in comparisons:
        lines.append(
            f"| {comparison['second']} vs {comparison['first']} | {comparison['metric']} | "
            f"{comparison['test']} | {comparison['holds']}/3 | {comparison['observed']}/3 |"
        )
    lines += [
        "",
        "## Accounting and retained failures",
        "",
        "```json",
        json.dumps(counts, indent=2),
        "```",
        "",
    ]
    for row in rows.values():
        if row["failure"]:
            lines.append(f"- {row['repeat']}/{row['case']}: {row['failure']}")
        for stage, status in row["posttest_status"].items():
            if status["failure"] or not status["submitted"]:
                reason = status["failure"] or (
                    "not executed/recorded" if not status["record_present"] else "no sealed payload"
                )
                lines.append(f"- {row['repeat']}/{row['case']}/{stage}: {reason}")
    lines += [
        "",
        "Full errors, notebook citation checks, resource accounts and unchanged model text "
        "are retained in each repeat's exports. Missing values are not zeros. "
        "No significance test, population stability threshold "
        "or causal notebook effect is claimed.",
        "",
    ]
    (destination / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--previous",
        type=Path,
        default=(ROOT / "workstreams/flagship_tasks/reports/paper-case-notebooks-20261013"),
    )
    args = parser.parse_args()
    result = build(args.root.resolve(), args.output.resolve(), args.previous.resolve())
    print(result["counts"])
