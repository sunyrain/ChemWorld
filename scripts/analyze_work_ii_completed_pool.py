"""Detailed paired descriptive analysis of retained Work II campaigns, without new calls."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean, median

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
OUT = REPORTS / "work-ii-evidence-closeout-20260921"
ARMS = ("Opaque", "Aligned", "MisIndexed")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_pairs(pairs):
    """Negative differences favor the first member; leave one whole world out."""
    if not pairs:
        return {"n": 0}
    worlds = sorted({r["world"] for r in pairs})
    delta = [r["first"] - r["second"] for r in pairs]
    loo = (
        [fmean(r["first"] - r["second"] for r in pairs if r["world"] != w) for w in worlds]
        if len(worlds) > 1
        else []
    )
    return {
        "n": len(pairs),
        "world_clusters": len(worlds),
        "first_mean": fmean(r["first"] for r in pairs),
        "second_mean": fmean(r["second"] for r in pairs),
        "mean_difference": fmean(delta),
        "median_difference": median(delta),
        "first_lower": sum(d < -1e-12 for d in delta),
        "ties": sum(abs(d) <= 1e-12 for d in delta),
        "leave_one_world_out_difference_range": [min(loo), max(loo)] if loo else None,
        "world_mean_differences": {
            w: fmean(r["first"] - r["second"] for r in pairs if r["world"] == w) for w in worlds
        },
    }


def paired_summary(pairs):
    return {
        "all_scheduled": summarize_pairs(pairs),
        "both_conforming": summarize_pairs([r for r in pairs if r["conforming"]]),
        "pairs": pairs,
    }


def load():
    with (ROOT / "paper/figures/integrated-results/campaign_metrics.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["budget"] = int(r["budget"])
        r["conforming"] = r["conforming"] == "True"
        for k in ("mae", "coverage", "width", "nominal"):
            r[k] = float(r[k])
    assert len(rows) == 1065 and len({r["id"] for r in rows}) == 240
    return rows


def c_baseline_analysis():
    repaired = read(REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json")
    output = []
    for budget in (12, 24):
        group = [r for r in repaired["rows"] if r["budget"] == budget]
        for metric in group[0]["agent_mae"]:
            for method in ("public_mean", "public_nearest_neighbor"):
                pairs = [
                    {
                        "id": r["id"],
                        "world": r["world"],
                        "first": r["agent_mae"][metric],
                        "second": r["public_baselines"]["mae"][method][metric],
                        "conforming": r["conforming"],
                    }
                    for r in group
                ]
                output.append(
                    {
                        "budget": budget,
                        "metric": metric,
                        "reference": method,
                        **paired_summary(pairs),
                    }
                )
    return output


def c_response_diagnostics():
    repaired = read(REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json")
    groups = defaultdict(list)
    for r in repaired["rows"]:
        for metric, d in r["response_diagnostics"].items():
            groups[r["budget"], metric].append(d)
    return [
        {
            "budget": budget,
            "metric": metric,
            "sources": len(group),
            **{
                key: fmean(d[key] for d in group)
                for key in (
                    "source_observed_mean",
                    "reference_mean",
                    "prediction_mean",
                    "signed_bias",
                )
            },
            "mean_reference_span": fmean(
                d["reference_range"][1] - d["reference_range"][0] for d in group
            ),
            "underestimated_queries": sum(d["underestimated_queries"] for d in group),
            "queries": sum(d["queries"] for d in group),
        }
        for (budget, metric), group in sorted(groups.items())
    ]


def main():
    rows = load()
    within_campaign = defaultdict(list)
    for r in rows:
        if r["system"] in ("RX", "EQ"):
            within_campaign[r["id"]].append(r)
    macro = [
        {
            **group[0],
            "metric": "macro",
            **{k: fmean(r[k] for r in group) for k in ("mae", "coverage", "width")},
        }
        for group in within_campaign.values()
    ]
    groups = defaultdict(list)
    for r in rows + macro:
        groups[r["system"], r["locus"], r["goal"], r["budget"], r["metric"]].append(r)
    priors, calibration = [], []
    for key, group in sorted(groups.items()):
        system, locus, goal, budget, metric = key
        context = {
            "system": system,
            "locus": locus,
            "goal": goal,
            "budget": budget,
            "metric": metric,
        }
        lookup = {(r["world"], r["arm"]): r for r in group}
        for first, second in (
            ("Aligned", "Opaque"),
            ("MisIndexed", "Opaque"),
            ("Aligned", "MisIndexed"),
        ):
            pairs = []
            for world in sorted({r["world"] for r in group}):
                a, b = lookup[world, first], lookup[world, second]
                pairs.append(
                    {
                        "world": world,
                        "first_id": a["id"],
                        "second_id": b["id"],
                        "first": a["mae"],
                        "second": b["mae"],
                        "conforming": a["conforming"] and b["conforming"],
                    }
                )
            priors.append(
                {**context, "first_arm": first, "second_arm": second, **paired_summary(pairs)}
            )
        calibration.append(
            {
                **context,
                "n": len(group),
                "nominal": group[0]["nominal"],
                "coverage": fmean(r["coverage"] for r in group),
                "width": fmean(r["width"] for r in group),
                "mae": fmean(r["mae"] for r in group),
                "below_nominal_sources": sum(r["coverage"] < r["nominal"] for r in group),
            }
        )
    budgets = []
    for key, group in sorted(groups.items()):
        s, locus, goal, budget, metric = key
        other_key = (s, locus, goal, 24, metric)
        if budget != 12 or other_key not in groups:
            continue
        higher = {(r["world"], r["arm"]): r for r in groups[other_key]}
        pairs = []
        for b in group:
            a = higher[b["world"], b["arm"]]
            pairs.append(
                {
                    "world": a["world"],
                    "arm": a["arm"],
                    "first_id": a["id"],
                    "second_id": b["id"],
                    "first": a["mae"],
                    "second": b["mae"],
                    "conforming": a["conforming"] and b["conforming"],
                }
            )
        budgets.append(
            dict(system=s, locus=locus, goal=goal, metric=metric, **paired_summary(pairs))
        )
    goals = read(ROOT / "paper/figures/integrated-results/analysis.json")
    data = {
        "scope": "Exploratory retained-data analysis; no new agent or physics calls",
        "denominators": goals["scope"],
        "metric_rows": len(rows),
        "goal_counts": goals["goal_counts"],
        "goal_pairs": goals["goal_contrasts"],
        "budget_contrasts": budgets,
        "prior_contrasts": priors,
        "calibration": calibration,
        "c_baseline_contrasts": c_baseline_analysis(),
        "c_response_diagnostics": c_response_diagnostics(),
        "p_factor_directions": read(REPORTS / "work-ii-p-five-world-20260921-v4/analysis.json")[
            "factor_directions"
        ],
        "limitations": [
            "One model configuration and realization per cell; five worlds per condition",
            "Leave-one-world-out ranges are influence checks, not confidence intervals",
            "Full and both-conforming paired samples use the same counterpart exclusion rule",
            "No pooled cross-system MAE or outcome-selected model reruns",
            "Shared-context endpoint discordance does not identify causal compression loss",
        ],
    }
    (OUT / "DETAILED_ANALYSIS.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Completed programme: detailed quantitative analysis",
        "",
        "240 sources, 238 source-conforming assessment chains; all 720 posttest stages. "
        "Descriptive development evidence. Every prior comparison has five world pairs. "
        "Budget comparisons have fifteen pairs nested in five worlds. All response metrics "
        "are retained in the companion JSON, including unfavorable comparisons.",
        "",
        "## Goals and operating recommendations",
        "",
        "| System / prediction endpoint | Pairs | Better retest | Lower prediction MAE | "
        "Better retest but worse prediction |",
        "|---|---:|---:|---:|---:|",
    ]
    for system, r in data["goal_counts"].items():
        lines.append(
            f"| {system} | {r['pairs']} | {r['better_retest']} | {r['lower_mae']} | "
            f"{r['better_retest_worse_prediction']} |"
        )
    lines += [
        "",
        "EC and RX use score MAE; RX_macro additionally retains the original "
        "six-metric macro endpoint. These results do not support a universal goal effect.",
        "",
        "## Budget: 24 versus 12 batches",
        "",
        "Negative differences favor 24 batches. The larger condition has a larger resource "
        "envelope, not just more observations. Leave-one-world-out ranges are influence "
        "diagnostics, not confidence intervals.",
        "",
        "| System / goal | Metric | MAE 12 -> 24 | Improved pairs | Mean difference | "
        "Leave-one-world-out range | Conforming paired difference (n) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in budgets:
        a, b = r["all_scheduled"], r["both_conforming"]
        lo, hi = a["leave_one_world_out_difference_range"]
        lines.append(
            f"| {r['system']} / {r['goal']} | {r['metric']} | "
            f"{a['second_mean']:.5f} -> {a['first_mean']:.5f} | "
            f"{a['first_lower']}/{a['n']} | {a['mean_difference']:.5f} | "
            f"[{lo:.5f}, {hi:.5f}] | {b['mean_difference']:.5f} ({b['n']}) |"
        )
    lines += [
        "",
        "## C predictions versus repaired public baselines",
        "",
        "Both references use the same agent-acquired public observations. Neither is a "
        "strong mechanistic learner. The mean baseline can perform well when a response "
        "varies little over the query domain. Reference difficulty must be interpreted "
        "with target range; a larger MAE does not identify a cognitive cause.",
        "",
        "| Budget | Metric | Baseline | Agent MAE | Baseline MAE | Agent wins | "
        "Conforming mean difference (n) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in data["c_baseline_contrasts"]:
        a, b = r["all_scheduled"], r["both_conforming"]
        lines.append(
            f"| {r['budget']} | {r['metric']} | {r['reference']} | "
            f"{a['first_mean']:.5f} | {a['second_mean']:.5f} | "
            f"{a['first_lower']}/{a['n']} | {b['mean_difference']:.5f} ({b['n']}) |"
        )
    lines += [
        "",
        "## Prior contrasts and uncertainty",
        "",
        "The JSON includes every metric-specific A-O, M-O and A-M contrast, paired "
        "conforming sensitivity, leave-one-world-out ranges, and mean interval width "
        "alongside coverage. A negative error difference is not proof that the prior "
        "was understood or correctly revised. World-level trace annotation remains "
        "necessary. No tally of metric-level wins is interpreted as independent "
        "scientific replications. The selected summary below uses score for EC, organic "
        "fraction for PA, within-system macro for RX/EQ, fines/recovery for C and both P metrics.",
        "",
        "| System / locus / goal / budget | Metric | MAE O / A / M | "
        "A beats O | M beats O | A-O leave-one-world-out range |",
        "|---|---|---:|---:|---:|---:|",
    ]
    selected = {
        "EC": {"score"},
        "PA": {"product_in_organic"},
        "RX": {"macro"},
        "EQ": {"macro"},
        "C": {"crystal_yield", "crystal_fines_fraction"},
        "P": {"purity", "recovery"},
    }
    for r in priors:
        if r["metric"] not in selected[r["system"]] or (r["first_arm"], r["second_arm"]) != (
            "Aligned",
            "Opaque",
        ):
            continue
        other = next(
            p
            for p in priors
            if all(p[k] == r[k] for k in ("system", "locus", "goal", "budget", "metric"))
            and p["first_arm"] == "MisIndexed"
            and p["second_arm"] == "Opaque"
        )
        a, m = r["all_scheduled"], other["all_scheduled"]
        lo, hi = a["leave_one_world_out_difference_range"]
        lines.append(
            f"| {r['system']} / {r['locus']} / {r['goal']} / {r['budget']} | "
            f"{r['metric']} | {a['second_mean']:.5f} / {a['first_mean']:.5f} / "
            f"{m['first_mean']:.5f} | {a['first_lower']}/5 | {m['first_lower']}/5 | "
            f"[{lo:.5f}, {hi:.5f}] |"
        )
    lines += [
        "",
        "## C response range and prediction bias",
        "",
        "Means weight each campaign equally. Query counts describe predictions, not "
        "independent experimental replications. Signed bias is prediction minus target.",
        "",
        "| Budget | Metric | Source mean | Query truth mean | Prediction mean | "
        "Mean within-world query span | Signed bias | Underestimated queries |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in data["c_response_diagnostics"]:
        lines.append(
            f"| {r['budget']} | {r['metric']} | {r['source_observed_mean']:.5f} | "
            f"{r['reference_mean']:.5f} | {r['prediction_mean']:.5f} | "
            f"{r['mean_reference_span']:.5f} | {r['signed_bias']:.5f} | "
            f"{r['underestimated_queries']}/{r['queries']} |"
        )
    lines += ["", "[Author interpretation and next analyses](INTERPRETATION_ZH.md).", ""]
    (OUT / "DETAILED_ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "campaigns": 240,
                "budget_metric_contrasts": len(budgets),
                "prior_metric_contrasts": len(priors),
                "c_baseline_metric_contrasts": len(data["c_baseline_contrasts"]),
            }
        )
    )


if __name__ == "__main__":
    main()
