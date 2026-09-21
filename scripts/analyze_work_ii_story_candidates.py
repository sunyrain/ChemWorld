"""Exploratory story checks on all retained campaigns; no new experiments.

Readout selection is descriptive, not a preregistered hypothesis test. EQ's three
most dilute questions are selected from public recipe concentrations, not errors.
The source-mean EQ comparison is a new post hoc diagnostic, not a formal baseline.
Run with uv run --no-sync python -m scripts.analyze_work_ii_story_candidates.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from paper.tools.render_integrated_results import ARMS, goal_pairs, load_rows

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
OUT = REPORTS / "work-ii-evidence-closeout-20260921"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def value(row, metric, stat="mae"):
    if metric == "macro":
        return fmean(v[stat] for v in row["metrics"].values())
    return row["metrics"][metric][stat]


def nominal_concentration(actions):
    amount = sum(a.get("amount_mol", 0) for a in actions if a["operation"] == "add_reagent")
    volume = sum(a.get("volume_L", 0) for a in actions if a["operation"] == "add_solvent")
    return amount / volume


def eq_regime_checks():
    query_config = read(ROOT / "configs/benchmark/work_ii_eq_bounded_equilibrium_v1.1.json")
    queries = query_config["query_replacement"]
    concentrations = {q["query_id"]: nominal_concentration(q["actions"]) for q in queries}
    dilute = set(sorted(concentrations, key=concentrations.get)[:3])
    assert dilute == {"Q03", "Q08", "Q09"}
    source_root = REPORTS / "work-ii-eq-bounded-equilibrium-20260920/v2-public/sources"
    cells = []
    truth_by_world = {}
    for world in range(1, 6):
        for arm in ARMS:
            identifier = f"EQ-W{world:02d}--{arm}"
            path = source_root / identifier / "RESULT.json"
            d = read(path)
            truth = d["reference_truth"]
            if world in truth_by_world:
                assert truth == truth_by_world[world], "Arms must use the same reference targets"
            truth_by_world[world] = truth
            predictions = d["posttests"]["Q"]["payload"]["predictions"]
            metrics = tuple(predictions[0]["metrics"])
            batches = d["source"]["batches"]
            assert len(predictions) == len(batches) == 12
            source_mean = {m: fmean(b["metrics"][m] for b in batches) for m in metrics}
            source_c = [nominal_concentration(b["actions"]) for b in batches]
            groups = {}
            for group, ids in (
                ("three_most_dilute", dilute),
                ("other_nine", set(concentrations) - dilute),
            ):
                points = []
                for q in predictions:
                    qid = q["query_id"]
                    if qid not in ids:
                        continue
                    for metric in metrics:
                        v = q["metrics"][metric]
                        observations = [t[metric] for t in truth[qid]]
                        target = fmean(observations)
                        points.append(
                            {
                                "query": qid,
                                "metric": metric,
                                "truth_mean": target,
                                "estimate": v["estimate"],
                                "mae": abs(v["estimate"] - target),
                                "source_mean_mae": abs(source_mean[metric] - target),
                                "width": v["upper80"] - v["lower80"],
                                "coverage": fmean(
                                    v["lower80"] <= t <= v["upper80"] for t in observations
                                ),
                            }
                        )
                groups[group] = {
                    "questions": len(ids),
                    "metric_points": len(points),
                    **{
                        k: fmean(p[k] for p in points)
                        for k in ("mae", "source_mean_mae", "coverage", "width")
                    },
                    "points": points,
                }
            reproduced = (
                3 * groups["three_most_dilute"]["mae"] + 9 * groups["other_nine"]["mae"]
            ) / 12
            recorded = fmean(
                v["mae_to_five_repeat_mean"] for v in d["prediction_evaluation"]["metrics"].values()
            )
            assert abs(reproduced - recorded) < 1e-12
            cells.append(
                {
                    "id": identifier,
                    "world": f"W{world:02d}",
                    "arm": arm,
                    "source": path.relative_to(ROOT).as_posix(),
                    "source_nominal_concentration_range": [min(source_c), max(source_c)],
                    "source_dissociation_range": [
                        min(b["metrics"]["acid_dissociation_fraction"] for b in batches),
                        max(b["metrics"]["acid_dissociation_fraction"] for b in batches),
                    ],
                    "groups": groups,
                }
            )
    aggregate = []
    for arm in ARMS:
        for group in ("three_most_dilute", "other_nine"):
            a = [r["groups"][group] for r in cells if r["arm"] == arm]
            aggregate.append(
                {
                    "arm": arm,
                    "group": group,
                    "worlds": 5,
                    **{
                        k: fmean(r[k] for r in a)
                        for k in ("mae", "source_mean_mae", "coverage", "width")
                    },
                }
            )
    return {
        "selection": "Three smallest public nominal query concentrations; post hoc grouping",
        "query_concentrations": concentrations,
        "cells": cells,
        "aggregate": aggregate,
    }


def main():
    rows, closure = load_rows()
    assert len(rows) == 240
    groups = defaultdict(list)
    for r in rows:
        groups[r["system"], r["locus"], r["goal"], r["budget"], r["world"]].append(r)
    assert len(groups) == 80 and all(len(g) == 3 for g in groups.values())
    readouts = {
        "EC": ("score",),
        "PA": ("product_in_organic",),
        "RX": ("macro",),
        "EQ": ("macro",),
        "C": ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction"),
        "P": ("purity", "recovery"),
    }
    world_rows = []
    c_joint = []
    for (system, locus, goal, budget, world), a in sorted(groups.items()):
        by_arm = {r["arm"]: r for r in a}
        world_rows.append(
            {
                "system": system,
                "locus": locus,
                "goal": goal,
                "budget": budget,
                "world": world,
                "arms": by_arm,
            }
        )
        if system == "C":
            o = by_arm["Opaque"]
            for arm in ("Aligned", "MisIndexed"):
                r = by_arm[arm]
                c_joint.append(
                    {
                        "world": world,
                        "budget": budget,
                        "arm": arm,
                        "both_conforming": o["conforming"] and r["conforming"],
                        "recovery_delta": value(r, "crystal_yield") - value(o, "crystal_yield"),
                        "purity_delta": value(r, "crystal_purity") - value(o, "crystal_purity"),
                    }
                )
    eq = eq_regime_checks()
    goal_worlds = []
    for system in ("EC", "RX"):
        pairs = goal_pairs(rows, system)
        for world in sorted({p["world"] for p in pairs}):
            a = [p for p in pairs if p["world"] == world]
            goal_worlds.append(
                {
                    "system": system,
                    "world": world,
                    "pairs": len(a),
                    "better_retest": sum(p["delta_retest"] > 0 for p in a),
                    "better_prediction": sum(p["delta_mae"] < 0 for p in a),
                    "better_retest_worse_prediction": sum(
                        p["delta_retest"] > 0 and p["delta_mae"] > 0 for p in a
                    ),
                }
            )
    p_directions = read(REPORTS / "work-ii-p-five-world-20260921-v4/analysis.json")[
        "factor_directions"
    ]
    p_groups = defaultdict(list)
    for r in p_directions:
        p_groups[r["factor"], r["metric"]].append(r)
    p_pooled = [
        {
            "factor": factor,
            "metric": metric,
            **{
                k: sum(r[k] for r in a)
                for k in (
                    "correct",
                    "total",
                    "resolved_correct",
                    "resolved_total",
                    "small_effect_correct",
                    "small_effect_total",
                )
            },
        }
        for (factor, metric), a in sorted(p_groups.items())
    ]
    output = {
        "scope": "Exploratory retained-data reanalysis; no new experiments or confirmatory test",
        "input_snapshot": closure["generated_at"],
        "campaigns": 240,
        "world_condition_groups": 80,
        "world_rows": world_rows,
        "goal_worlds": goal_worlds,
        "c_paired_response_tradeoffs": c_joint,
        "eq_p_query_regimes": eq,
        "p_directions": p_pooled,
        "limitations": [
            "Five world clusters per block; cells and metrics are correlated",
            "Same numbered worlds across different EQ loci are not matched interventions",
            "Exploratory selection does not establish causes, prevalence or learning curves",
            "EQ source-mean forecast is a post hoc diagnostic, not a newly registered baseline",
        ],
    }
    (OUT / "STORY_WORLD_ANALYSIS.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Exploratory story analysis: complete world comparisons",
        "",
        "Retained development evidence: 240 campaigns in 80 world/condition groups, "
        "three arms each. All five worlds, unfavorable outcomes, and source shortfalls "
        "are retained. This is descriptive post hoc analysis, not a new experiment or "
        "an inferential test. The JSON keeps all response metrics and calibration values; "
        "the table shows named readouts, with no pooled cross-system score.",
        "",
        "## Goals by world",
        "",
        "Each row has six matched goal pairs: two budgets in EC, two prior loci in RX. "
        "These are clustered observations, not six independent worlds.",
        "",
        "| System | World | Pairs | Better retest | Better prediction "
        "| Better retest / worse prediction |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in goal_worlds:
        lines.append(
            f"| {r['system']} | {r['world']} | {r['pairs']} | {r['better_retest']} "
            f"| {r['better_prediction']} | {r['better_retest_worse_prediction']} |"
        )
    lines += [
        "",
        "## EQ/P: question regime",
        "",
        "The three most dilute public recipes are Q03, Q08 and Q09. The other nine include "
        "boundary questions and must not be called an in-domain set. Mean-source predictions are "
        "an additional post hoc diagnostic, not a strong learned mechanism. Coverage uses "
        "five reference observations per question; MAE uses their means. Every cell's "
        "subgroup means reproduce its original MAE.",
        "",
        "| Arm | Question group | Agent MAE | Source-mean MAE | Coverage | Width |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in eq["aggregate"]:
        lines.append(
            f"| {r['arm']} | {r['group']} | {r['mae']:.5f} | {r['source_mean_mae']:.5f} "
            f"| {r['coverage']:.1%} | {r['width']:.5f} |"
        )
    lines += [
        "",
        "## C: paired recovery/purity effects",
        "",
        "Differences are dossier arm minus Opaque MAE. Negative favors the dossier. "
        "Each budget uses five world pairs; arms and responses are correlated.",
        "",
        "| Budget | Arm | Recovery improves and purity worsens | Both-conforming pairs |",
        "|---|---|---:|---:|",
    ]
    for budget in (12, 24):
        for arm in ("Aligned", "MisIndexed"):
            a = [r for r in c_joint if r["budget"] == budget and r["arm"] == arm]
            b = [r for r in a if r["both_conforming"]]

            def count(v):
                return sum(r["recovery_delta"] < 0 < r["purity_delta"] for r in v)

            lines.append(f"| {budget} | {arm} | {count(a)}/{len(a)} | {count(b)}/{len(b)} |")
    lines += [
        "",
        "## P: intervention-specific direction correctness",
        "",
        "Uses the original fixed 0.02 resolution. Fifteen campaign answers per factor/metric, "
        "nested in five worlds. Small-effect controls do not demonstrate a universal invariance.",
        "",
        "| Factor | Metric | Correct | Resolved | Small-effect |",
        "|---|---|---:|---:|---:|",
    ]
    for r in p_pooled:
        lines.append(
            f"| {r['factor']} | {r['metric']} | {r['correct']}/{r['total']} "
            f"| {r['resolved_correct']}/{r['resolved_total']} "
            f"| {r['small_effect_correct']}/{r['small_effect_total']} |"
        )
    lines += [
        "",
        "## All 80 world/condition groups",
        "",
        "O/A/M = Opaque / Aligned / MisIndexed. An asterisk marks a source shortfall; "
        "it is not an imputed result. World identifiers remain scoped to their study block.",
        "",
    ]
    last = None
    for r in world_rows:
        group = (r["system"], r["locus"], r["goal"], r["budget"])
        if group != last:
            lines += [
                f"### {group[0]} / {group[1]} / {group[2]} / {group[3]}",
                "",
                "| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |",
                "|---|---|---:|---:|---:|",
            ]
            last = group
        for metric in readouts[r["system"]]:
            vals = [
                f"{value(r['arms'][arm], metric):.5f}"
                + ("*" if not r["arms"][arm]["conforming"] else "")
                for arm in ARMS
            ]
            lines.append(f"| {r['world']} | {metric} | " + " | ".join(vals) + " |")
        lines.append("")
    # Keep multi-row tables contiguous across worlds.
    text = "\n".join(lines).replace("|\n\n|", "|\n|").rstrip() + "\n"
    (OUT / "STORY_WORLD_ANALYSIS.md").write_text(text, encoding="utf-8")
    print(
        "Retained-data analysis complete: 240 campaigns / 80 groups; EQ 15 sources / 180 queries."
    )


if __name__ == "__main__":
    main()
