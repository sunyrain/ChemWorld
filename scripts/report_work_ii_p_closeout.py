"""Describe the terminal P cohort without provider calls or new physics."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

from scripts.run_work_ii_final_diagnostic import read, write


def analyze(summary):
    if not summary["terminal"]:
        raise ValueError("P matrix is not terminal")
    rows = summary["results"]
    assert len(rows) == len({r["id"] for r in rows}) == 15
    groups = defaultdict(list)
    for row in rows:
        groups[row["arm"]].append(row)
    aggregate = []
    factor_groups = defaultdict(list)
    for arm, entries in sorted(groups.items()):
        predictions = [
            r["prediction_evaluation"]
            for r in entries
            if r.get("prediction_evaluation", {}).get("valid")
        ]
        retests = [r["retest_metrics"][0] for r in entries if r["retest_metrics"]]
        pure = [m for m in retests if m["purity"] >= 0.80]
        for prediction in predictions:
            for pair in prediction["pairs"]:
                factor_groups[(arm, pair["factor"], pair["metric"])].append(pair)
        aggregate.append(
            {
                "arm": arm,
                "scheduled": len(entries),
                "complete_chains": sum(r["status"] == "completed" for r in entries),
                "valid_predictions": len(predictions),
                "metrics": {
                    metric: {
                        key: mean(e["metrics"][metric][key] for e in predictions)
                        for key in ("mae", "coverage80", "width80", "interval_score80")
                    }
                    for metric in ("purity", "recovery")
                }
                if predictions
                else {},
                "retests_available": len(retests),
                "purity_eligible_retests": len(pure),
                "mean_retest_recovery_all": mean(m["recovery"] for m in retests)
                if retests
                else None,
                "mean_retest_recovery_purity_eligible": mean(m["recovery"] for m in pure)
                if pure
                else None,
            }
        )
    by_key = {(r["world_id"], r["arm"]): r for r in rows}
    contrasts = []
    for first, second in (
        ("Aligned", "Opaque"),
        ("MisIndexed", "Opaque"),
        ("Aligned", "MisIndexed"),
    ):
        for metric in ("purity", "recovery"):
            pairs = []
            for world in sorted({r["world_id"] for r in rows}):
                a, b = by_key[(world, first)], by_key[(world, second)]
                ae, be = a.get("prediction_evaluation", {}), b.get("prediction_evaluation", {})
                if ae.get("valid") and be.get("valid"):
                    pairs.append(
                        {
                            "world": world,
                            "delta": ae["metrics"][metric]["mae"] - be["metrics"][metric]["mae"],
                            "both_conforming": a["status"] == b["status"] == "completed",
                        }
                    )
            conforming = [p for p in pairs if p["both_conforming"]]
            contrasts.append(
                {
                    "first": first,
                    "second": second,
                    "metric": metric,
                    "pairs": pairs,
                    "first_lower_mae": sum(p["delta"] < 0 for p in pairs),
                    "mean_difference": mean(p["delta"] for p in pairs) if pairs else None,
                    "conforming_pairs": len(conforming),
                    "conforming_first_lower_mae": sum(p["delta"] < 0 for p in conforming),
                    "conforming_mean_difference": mean(p["delta"] for p in conforming)
                    if conforming
                    else None,
                }
            )
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "interpretation": (
            "SUPERSEDED PLATFORM DIAGNOSTIC: these scores are not primary agent evidence. "
            if summary.get("disposition")
            else ""
        )
        + ("Descriptive development evidence; five world clusters, one session per arm"),
        "aggregate": aggregate,
        "factor_directions": [
            {
                "arm": arm,
                "factor": factor,
                "metric": metric,
                "correct": sum(p["correct"] for p in pairs),
                "total": len(pairs),
                "resolved_correct": sum(p["correct"] for p in pairs if p["resolved"]),
                "resolved_total": sum(p["resolved"] for p in pairs),
                "small_effect_correct": sum(p["correct"] for p in pairs if not p["resolved"]),
                "small_effect_total": sum(not p["resolved"] for p in pairs),
            }
            for (arm, factor, metric), pairs in sorted(factor_groups.items())
        ],
        "paired_contrasts": contrasts,
        "failures": [r for r in rows if r["status"] != "completed"],
        "pilot": summary["pilot"],
        "prior_integration_costs": summary.get("prior_integration_costs"),
        "extra_source_attempts": summary["extra_source_attempts"],
        "stage_time_s": {
            stage: {
                "available": len(values),
                "mean": mean(values) if values else None,
                "sum": sum(values),
            }
            for stage in ("source", "K1", "Q", "K2", "retest")
            if (values := [
                r["timing_s"][stage]
                for r in rows
                if r.get("timing_s", {}).get(stage) is not None
            ])
        },
        "effective_tokens": {
            "available": sum(bool((r.get("tokens") or {}).get("valid")) for r in rows),
            "complete": sum(bool((r.get("tokens") or {}).get("complete")) for r in rows),
            "total": {
                k: sum((r.get("tokens") or {}).get("total", {}).get(k, 0) for r in rows)
                for k in ("input", "cached_input", "uncached_input", "output")
            },
            "basis": (
                "Effective chains only; missing usage and abandoned attempts are not zero cost"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    summary = read(args.report / "summary.json")
    analysis = analyze(summary)
    write(args.report / "analysis.json", analysis)
    lines = [
        "# P completed-cohort analysis",
        "",
        analysis["interpretation"],
        "",
        f"Complete chains {summary['complete_chains']}/15; final-assayed source batches "
        f"{summary['source_batches']}/180; posttests {summary['posttests']}/45; "
        f"retests {summary['retests']}/15.",
        "",
        "Each arm contains five worlds. Purity and recovery are separate outcomes. "
        "Recovery is relative to the original reactant charge.",
        "Batch lifecycle totals: " + str(summary.get("batch_accounting")) + ".",
        "",
        "| Arm | Prediction n | Purity MAE | Recovery MAE | Purity coverage80 | "
        "Recovery coverage80 | Purity-eligible retests | Mean recovery, all retests |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in analysis["aggregate"]:
        m = r["metrics"]
        recovery = r["mean_retest_recovery_all"]
        recovery_text = f"{recovery:.5f}" if recovery is not None else "unavailable"
        if m:
            lines.append(
                f"| {r['arm']} | {r['valid_predictions']}/5 | {m['purity']['mae']:.5f} | "
                f"{m['recovery']['mae']:.5f} | {m['purity']['coverage80']:.1%} | "
                f"{m['recovery']['coverage80']:.1%} | {r['purity_eligible_retests']}/"
                f"{r['retests_available']} | {recovery_text} |"
            )
    lines += [
        "",
        "## Paired prior contrasts",
        "",
        "| Comparison | Metric | First lower MAE / all pairs | Mean difference | "
        "First lower MAE / conforming pairs | Conforming mean difference |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for c in analysis["paired_contrasts"]:
        lines.append(
            f"| {c['first']} minus {c['second']} | {c['metric']} | "
            f"{c['first_lower_mae']}/{len(c['pairs'])} | {c['mean_difference']} | "
            f"{c['conforming_first_lower_mae']}/{c['conforming_pairs']} | "
            f"{c['conforming_mean_difference']} |"
        )
    lines += [
        "",
        "## Intervention directions",
        "",
        "Directions use the fixed 0.02 resolution. Correct small-effect predictions are "
        "reported separately from resolved contrasts; query endpoints are not independent worlds.",
        "",
        "| Arm | Factor | Metric | Correct / all | Correct / resolved | Correct / small effect |",
        "|---|---|---|---:|---:|---:|",
    ]
    for r in analysis["factor_directions"]:
        lines.append(
            f"| {r['arm']} | {r['factor']} | {r['metric']} | {r['correct']}/{r['total']} | "
            f"{r['resolved_correct']}/{r['resolved_total']} | "
            f"{r['small_effect_correct']}/{r['small_effect_total']} |"
        )
    tokens = analysis["effective_tokens"]
    lines += [
        "",
        "## Computation accounting",
        "",
        f"Usage available for {tokens['available']}/15 effective cells and complete for "
        f"{tokens['complete']}/15. Reported totals: input {tokens['total']['input']:,}, "
        f"cached input {tokens['total']['cached_input']:,}, "
        f"uncached input {tokens['total']['uncached_input']:,}, "
        f"output {tokens['total']['output']:,} tokens.",
        "",
        tokens["basis"] + ". Pilot and superseded-block costs remain separate in analysis.json.",
        "",
        "| Stage | Cells with timing | Mean seconds | Sum of worker seconds |",
        "|---|---:|---:|---:|",
    ]
    for stage, timing in analysis["stage_time_s"].items():
        lines.append(
            f"| {stage} | {timing['available']}/15 | {timing['mean']:.1f} | {timing['sum']:.1f} |"
        )
    lines += [
        "",
        "Worker seconds overlap under concurrent execution and are not elapsed calendar time. "
        "Stage totals exclude pilot, qualification and earlier superseded matrices.",
    ]
    lines += [
        "",
        "## Scope and retained limitations",
        "",
        "- The independent unit is a world cluster, not each queried metric or interval.",
        "- Prior effects include adaptive experiment-selection differences. One session per "
        "condition does not isolate direct inference effects or stochastic session variance.",
        "- Primary descriptive means retain all valid planned responses, including sources "
        "with fewer than twelve final assays. Paired sensitivity results require both chains "
        "to conform; they do not erase the nonconforming source or its resource use.",
        "- Quality eligibility is retest purity >=0.80. The unconditional recovery mean "
        "must be read together with quality eligibility; it is not a quality-adjusted score.",
        "- The corrected qualification's 60 fixed Opaque reference batches are reused. "
        "Their single keyed "
        "observations are prediction targets; replays are not additional noisy repeats.",
        "- Wash staging and concentration are retained small-effect controls. "
        "Their inclusion does not establish strong mechanistic discrimination.",
        "- K1 and K2 require qualitative claim/evidence analysis. No mechanistic correctness "
        "or information-loss score is inferred from numerical prediction alone.",
        "- Integration pilots, the invalid 12-batch pre-correction pilot, deterministic "
        "regressions, qualification batches and interrupted attempts remain separate costs "
        "in the machine-readable analysis.",
        "",
        "## Failures",
        "",
        "```json",
        json.dumps(
            [
                {
                    k: r.get(k)
                    for k in ("id", "status", "failure", "source_validation", "batch_accounting")
                }
                for r in analysis["failures"]
            ],
            indent=2,
        ),
        "```",
        "",
        "Machine-readable per-world contrasts, token availability and retained "
        "failures are in [analysis.json](analysis.json). All cell reports are linked from "
        "[REPORT.md](REPORT.md).",
        "",
    ]
    (args.report / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(analysis["aggregate"]))


if __name__ == "__main__":
    main()
