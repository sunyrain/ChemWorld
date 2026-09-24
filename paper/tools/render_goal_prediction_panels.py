"""Draw Figure 3 and its supporting tables from retained research, without new runs."""

from __future__ import annotations

import json
import re
from collections import Counter
from statistics import fmean

import matplotlib.pyplot as plt
import numpy as np
from analyze_operation_prediction_relationship import (
    ROOT,
    matched_pairs,
    read_json,
    selected_case,
    table,
    write_csv,
)
from matplotlib.lines import Line2D
from render_operation_prediction_story import ARM_COLORS, ASSETS, prepare, style

DISCOVERY, OPTIMIZATION, REFERENCE = "#657C99", "#19847B", "#AF542D"
INK = "#171717"


def case_paths(pairs):
    binding = read_json(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    rows, accounts = [], {}
    pair = next(r for r in pairs if r["optimization_id"] == "EC-W01-B12-optimization-E-Opaque")
    for goal, action_count in (("discovery", 86), ("optimization", 84)):
        case_id = pair[f"{goal}_id"]
        source = read_json(
            ROOT / binding["run_root"] / "sources" / case_id / f"{goal}-E-Opaque/result.json"
        )
        public = (ROOT / binding["report"]).parent / case_id
        trace = read_json(public / "public-trajectory.json")
        assert len(trace) == action_count
        selected = source["recommendation"]["selected_experiment_index"]
        retest = source["recommendation_retest"]["batches"][0]["metrics"]["score"]
        assert abs(retest - pair[f"{goal}_retest"]) < 1e-12
        for i, batch in enumerate(source["batches"], 1):
            actions = [r["action"] for r in trace if r["experiment_index"] == i - 1]
            assert actions == batch["actions"]
            recipe = {}
            for a in actions:
                recipe.update(a)
            segments = [a["duration_s"] for a in actions if a["operation"] == "electrolyze"]
            # Retain the complete public operation order, including intermediate assays.
            rows.append(
                {
                    "goal": goal,
                    "batch": i,
                    **{
                        k: recipe[k]
                        for k in (
                            "solvent",
                            "electrolyte_profile",
                            "potential_V",
                            "current_mA",
                            "amount_mol",
                            "volume_L",
                        )
                    },
                    "electrolysis_segments_s": "+".join(f"{v:g}" for v in segments),
                    "observed_score": batch["metrics"]["score"],
                    "selected_recommendation": i == selected,
                    "recommendation_retest_score": retest if i == selected else "",
                    "operation_sequence": "; ".join(
                        a["operation"] + (":" + a["instrument"] if "instrument" in a else "")
                        for a in actions
                    ),
                }
            )
        text = (public / "REPORT.md").read_text(encoding="utf-8")
        prediction = next(
            d
            for block in re.findall(r"```json\s*(.*?)```", text, re.S)
            if "predictions" in (d := json.loads(block))
        )
        accounts[goal] = prediction["rationale"]
    assert len(rows) == 24
    assert [r["batch"] for r in rows if r["selected_recommendation"]] == [12, 12]
    write_csv("case-paired-batches.csv", rows)
    return rows, accounts, pair


def save(fig, name):
    for fmt, dpi in (("pdf", 300), ("svg", 300), ("png", 450)):
        fig.savefig(ASSETS / f"{name}.{fmt}", dpi=dpi, facecolor="white")
    plt.close(fig)


def joint(ax, pairs, *, xlim, ylim, xticks, yticks):
    style(ax)
    ax.axvline(0, color="#828282", lw=0.65, ls=(0, (3, 3)))
    ax.axhline(0, color="#828282", lw=0.65, ls=(0, (3, 3)))
    for arm, color in ARM_COLORS.items():
        subset = [p for p in pairs if p["arm"] == arm]
        ax.scatter(
            [p["delta_retest"] for p in subset],
            [-p["delta_score_mae"] for p in subset],
            s=24,
            color=color,
            edgecolor="white",
            lw=0.45,
            zorder=3,
        )
    ax.set(xlim=xlim, ylim=ylim, xticks=xticks, yticks=yticks)
    assert all(
        xlim[0] < p["delta_retest"] < xlim[1] and ylim[0] < -p["delta_score_mae"] < ylim[1]
        for p in pairs
    )
    counts = Counter(p["outcome"] for p in pairs)
    for x, y, label, key, ha, va in (
        (
            0.035,
            0.97,
            "D: retest / O: prediction",
            "operation_worse_prediction_better",
            "left",
            "top",
        ),
        (0.965, 0.97, "O: both", "both_better", "right", "top"),
        (0.035, 0.03, "D: both", "both_worse", "left", "bottom"),
        (
            0.965,
            0.03,
            "O: retest / D: prediction",
            "operation_better_prediction_worse",
            "right",
            "bottom",
        ),
    ):
        ax.text(
            x,
            y,
            f"{label}\n{counts[key]}/30",
            transform=ax.transAxes,
            ha=ha,
            va=va,
            fontsize=6.7,
            color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5},
            zorder=2,
        )
    ax.set_xlabel("Retest score: Optimization - Discovery", labelpad=4)
    ax.set_ylabel("Score MAE: Discovery - Optimization", labelpad=4)


def phase_strip(ax, y, groups, color):
    for start, end, label in groups:
        ax.plot(
            [start - 0.35, end + 0.35],
            [y, y],
            color=color,
            lw=1.6,
            transform=ax.get_xaxis_transform(),
            clip_on=False,
        )
        ax.text(
            (start + end) / 2,
            y - 0.05,
            label,
            color=INK,
            ha="center",
            va="top",
            fontsize=6.7,
            transform=ax.get_xaxis_transform(),
            linespacing=1.05,
        )


def draw_main(summary, pairs, paths, queries, case):
    # Match the 164-mm manuscript text width; fonts are not reduced on insertion.
    fig = plt.figure(figsize=(164 / 25.4, 7.55), facecolor="white")
    for letter, x, y, title in (
        ("a", 0.025, 0.988, "Electrochemistry"),
        ("b", 0.545, 0.988, "Reaction processing"),
        ("c", 0.025, 0.650, "Two independent 12-batch research paths"),
        ("d", 0.025, 0.265, "The optimization agent's subsequent predictions"),
    ):
        fig.text(x, y, letter, fontsize=10, weight="bold", va="top")
        fig.text(x + 0.030, y, title, fontsize=8, va="top", color=INK)
    aa = fig.add_axes([0.095, 0.724, 0.385, 0.226])
    bb = fig.add_axes([0.615, 0.724, 0.370, 0.226])
    joint(
        aa,
        [p for p in pairs if p["system"] == "EC"],
        xlim=(-0.56, 0.56),
        ylim=(-0.27, 0.27),
        xticks=[-0.5, -0.25, 0, 0.25, 0.5],
        yticks=[-0.2, -0.1, 0, 0.1, 0.2],
    )
    joint(
        bb,
        [p for p in pairs if p["system"] == "RX"],
        xlim=(-0.08, 0.08),
        ylim=(-0.22, 0.22),
        xticks=[-0.06, -0.03, 0, 0.03, 0.06],
        yticks=[-0.2, -0.1, 0, 0.1, 0.2],
    )
    # Ring locates the retrospectively selected case without altering coordinates.
    aa.scatter(
        case["optimization_retest"] - case["discovery_retest"],
        case["discovery_score_mae"] - case["optimization_score_mae"],
        s=76,
        facecolor="none",
        edgecolor=INK,
        lw=0.8,
        zorder=4,
    )
    fig.text(0.095, 0.668, "D = Discovery; O = Optimization", fontsize=6.8)
    fig.legend(
        handles=[
            Line2D([], [], color=c, marker="o", ls="", ms=4, label=a) for a, c in ARM_COLORS.items()
        ],
        loc="center right",
        bbox_to_anchor=(0.995, 0.673),
        ncol=3,
        frameon=False,
        fontsize=6.8,
        columnspacing=1.1,
        handletextpad=0.4,
    )

    cc = fig.add_axes([0.095, 0.439, 0.785, 0.164])
    style(cc)
    cc.set(
        xlim=(0.55, 14.7), ylim=(-0.045, 0.88), yticks=[0, 0.25, 0.5, 0.75], ylabel="Observed score"
    )
    cc.set_xticks([*range(1, 13), 14], [str(i) for i in range(1, 13)] + ["Retest"])
    cc.tick_params(axis="x", pad=3)
    for goal, color, marker in (("discovery", DISCOVERY, "o"), ("optimization", OPTIMIZATION, "s")):
        rows = [r for r in paths if r["goal"] == goal]
        cc.plot(
            [r["batch"] for r in rows],
            [r["observed_score"] for r in rows],
            color=color,
            marker=marker,
            ms=3.1,
            lw=0.95,
            label=goal.capitalize(),
        )
        end = next(r for r in rows if r["selected_recommendation"])
        retest = end["recommendation_retest_score"]
        cc.plot([12, 14], [end["observed_score"], retest], color=color, lw=0.8, ls=(0, (2, 2)))
        cc.scatter(14, retest, marker=marker, color=color, s=22, zorder=4)
        cc.annotate(
            f"{retest:.3f}",
            (14, retest),
            xytext=(7, 5 if goal == "optimization" else -8),
            textcoords="offset points",
            color=INK,
            va="center",
            fontsize=7,
        )
    cc.axvline(12.8, color="#C0C0C0", lw=0.6)
    cc.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.01),
        frameon=False,
        ncol=2,
        fontsize=7,
        handlelength=1.8,
        borderaxespad=0,
    )
    cc.text(0.97, 1.08, "Both select batch 12", transform=cc.transAxes, ha="right", fontsize=7)
    # Compact chronological strips describe recorded changes, not inferred intentions.
    phase_strip(
        cc,
        -0.27,
        [
            (1, 4, "Solvents"),
            (5, 7, "Potential"),
            (8, 10, "Electrolytes"),
            (11, 12, "Duration /\ncurrent"),
        ],
        DISCOVERY,
    )
    phase_strip(
        cc,
        -0.63,
        [
            (1, 4, "Material pairs"),
            (5, 6, "Cross-pairs"),
            (7, 8, "Potential"),
            (9, 12, "Current / time / potential"),
        ],
        OPTIMIZATION,
    )
    cc.text(
        14,
        -0.38,
        "Independent\nrecommendation\nretests",
        transform=cc.get_xaxis_transform(),
        fontsize=6.7,
        ha="center",
        va="top",
        color="#505050",
    )

    fig.text(
        0.055,
        0.238,
        "Later public Q rationale (condensed): poor cross-pairs suggest material incompatibility.",
        fontsize=7,
        color=INK,
    )
    dd = fig.add_axes([0.095, 0.065, 0.890, 0.132])
    style(dd)
    xx = np.arange(1, 13)
    for i in (4, 6, 8, 10):
        dd.axvspan(i - 0.39, i + 0.39, color="#F2F1ED", zorder=0)
        query = queries[i - 1]
        dd.text(
            i,
            0.735,
            f"S{query['solvent']}/E{query['electrolyte_profile']}",
            ha="center",
            va="center",
            fontsize=6.6,
        )
    pred = np.array([q["predicted_score"] for q in queries])
    lo = np.array([q["lower80"] for q in queries])
    hi = np.array([q["upper80"] for q in queries])
    ref = np.array([q["reference_score"] for q in queries])
    dd.errorbar(
        xx - 0.09,
        pred,
        yerr=[pred - lo, hi - pred],
        fmt="o",
        color=OPTIMIZATION,
        markersize=3.3,
        elinewidth=1,
        capsize=2,
        capthick=0.8,
        zorder=3,
    )
    dd.scatter(xx + 0.10, ref, marker="D", s=13, color=REFERENCE, zorder=4)
    dd.set(xlim=(0.4, 12.6), ylim=(-0.025, 0.78), yticks=[0, 0.2, 0.4, 0.6], ylabel="Score")
    dd.set_xticks(xx, [q["query"] for q in queries])
    for label, i in zip(dd.get_xticklabels(), xx, strict=True):
        if i in (4, 6, 8, 10):
            label.set_weight("bold")
    dd.legend(
        handles=[
            Line2D([], [], color=OPTIMIZATION, marker="o", ms=3, label="Forecast + 80% interval"),
            Line2D([], [], color=REFERENCE, marker="D", ms=3, ls="", label="Withheld reference"),
        ],
        loc="lower left",
        bbox_to_anchor=(-0.01, 1.01),
        ncol=2,
        frameon=False,
        fontsize=6.8,
        handlelength=1.4,
        columnspacing=1.3,
        borderaxespad=0,
    )
    dd.text(1, 1.075, "MAE 0.229; coverage 5/12", transform=dd.transAxes, ha="right", fontsize=6.8)
    fig.text(
        0.095,
        0.021,
        "Highlighted conditions: +0.8 V, 100 mA, 7,200 s. All queries use 0.012 mol in 0.025 L.",
        fontsize=6.8,
    )
    save(fig, "figure03-goals-paths-forecasts")


def draw_means(summary):
    fig, axes = plt.subplots(2, 2, figsize=(6.45, 4.1))
    fig.subplots_adjust(left=0.095, right=0.99, bottom=0.09, top=0.88, hspace=0.49, wspace=0.30)
    for i, system in enumerate(("EC", "RX")):
        rr = [r for r in summary["world_means"] if r["system"] == system]
        for j, metric in enumerate(("retest", "score_mae")):
            ax = axes[i, j]
            style(ax)
            xx = np.arange(5)
            for off, goal, color in (
                (-0.2, "discovery", DISCOVERY),
                (0.2, "optimization", OPTIMIZATION),
            ):
                ax.bar(
                    xx + off,
                    [r[f"{goal}_{metric}"] for r in rr],
                    width=0.37,
                    color=color,
                    label=goal.capitalize(),
                )
            ax.set_xticks(xx, [f"W{k}" for k in range(1, 6)])
            ax.set_ylabel("Retest score" if j == 0 else "Score MAE")
            ax.set_title(f"{chr(97 + 2 * i + j)}   {system}", loc="left", fontsize=8)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    save(fig, "figureS6-goal-world-means")


def supporting_text(summary, pairs, paths, queries, accounts, case):
    # Short tables stay on explicit pages under the existing venue renderer.
    lines = [
        r"\clearpage",
        "",
        "## E.4 Complete research-objective comparison",
        "",
        "Figure 3 uses 120 campaigns and sixty original goal pairs. Each pair fixes world, "
        "information arm, budget and prior locus. EC has five worlds, three arms and two budgets "
        "at the entity locus; RX has five worlds, three arms and two loci at twelve batches. "
        "The independent recommendation retest and twelve-query score MAE are separate endpoints. "
        "EC references are single seeded observations; RX point references are "
        "five-observation means. "
        "No new campaigns or predictions were produced for this analysis.",
        "",
        "**Table E3. All joint goal outcomes.**",
        "",
        table(
            ["Higher retest", "Lower score MAE", "EC pairs", "RX pairs"],
            [
                [
                    g.capitalize(),
                    h.capitalize(),
                    *[
                        sum(
                            p["system"] == s
                            and p["higher_retest_goal"] == g
                            and p["lower_mae_goal"] == h
                            for p in pairs
                        )
                        for s in ("EC", "RX")
                    ],
                ]
                for g, h in (
                    ("optimization", "optimization"),
                    ("optimization", "discovery"),
                    ("discovery", "optimization"),
                    ("discovery", "discovery"),
                )
            ],
        ),
        "",
        "Both endpoints favour the same campaign in 16/30 EC and 21/30 RX pairs, and opposite "
        "campaigns in 14/30 and 9/30. Strict signs define these descriptive counts; near-zero "
        "differences are not thereby significant. Each system reuses five worlds. RX score MAE "
        "favours optimization in 8/30 pairs; its separate six-response macro MAE does so in 6/30.",
        "",
        "![World-level summaries of the same goal comparison. a,b, Electrochemical recommendation "
        "retests and score-prediction MAE. c,d, Reaction-processing endpoints. "
        "Each bar averages six "
        "campaigns per goal within a world. World labels are system-specific; bar means do not "
        "replace the individual paired differences in Figure 3. Scales differ across panels.]"
        "(../../figures/venue-results/figureS6-goal-world-means.pdf){width=100%}",
        "",
        r"\clearpage",
        "",
        "## E.5 Strata and recovery sensitivity",
        "",
        "**Table E4. Endpoint orderings within design strata.**",
        "",
    ]
    strata = []
    for system in ("EC", "RX"):
        subset = [r for r in pairs if r["system"] == system]
        for dim in ("world", "budget", "arm", "locus"):
            for level in sorted({str(r[dim]) for r in subset}):
                rr = [r for r in subset if str(r[dim]) == level]
                display = level.replace("EC-", "").replace("RX-", "")
                strata.append(
                    [
                        system,
                        dim.capitalize(),
                        display,
                        len(rr),
                        sum(r["ordering"] == "same" for r in rr),
                        sum(r["ordering"] == "opposite" for r in rr),
                    ]
                )
    lines += [
        table(["System", "Factor", "Level", "Pairs", "Same", "Opposite"], strata),
        "",
        "Same means that the higher-retest campaign also has lower MAE; opposite means it "
        "has higher MAE. These overlapping strata do not add independent tests. Budget rows "
        "compare goals at a fixed budget, not a twelve-to-twenty-four-batch contrast. E denotes "
        "entity priors, P parameter priors and S structural priors.",
        "",
    ]
    clean = [p for p in pairs if p["system"] == "EC" and p["both_without_recorded_recovery"]]
    assert len(clean) == 17 and sum(p["ordering"] == "opposite" for p in clean) == 7
    lines += [
        "The EC subset with neither campaign having a recorded recovery contains seventeen "
        "pairs: ten have the same ordering and seven the opposite ordering. Optimization "
        "has higher retests in fifteen and lower MAE in eight. This subset excludes "
        "assessment-only recovery as well as source recovery; it has uneven coverage and "
        "does not replace the full cohort.",
        "",
        r"\clearpage",
        "",
        "## E.6 All batches of the selected electrochemical pair",
        "",
        "The illustration uses one retrospectively selected twelve-batch Opaque pair in "
        "the first electrochemical world. It is not an additional replication or a random "
        "sample. Both original agents retain their research context for the later assessments. "
        "Every batch uses 0.020 mol in 0.040 L; current denotes the configured cap.",
        "",
    ]
    for k, goal in enumerate(("discovery", "optimization"), 5):
        rr = [r for r in paths if r["goal"] == goal]
        lines += [
            f"**Table E{k}. {goal.capitalize()} source batches.**",
            "",
            table(
                ["Batch", "Pair", "V", "mA", "Electrolysis / s", "Score"],
                [
                    [
                        r["batch"],
                        f"S{r['solvent']}/E{r['electrolyte_profile']}",
                        f"{r['potential_V']:g}",
                        f"{r['current_mA']:g}",
                        r["electrolysis_segments_s"],
                        f"{r['observed_score']:.6f}",
                    ]
                    for r in rr
                ],
            ),
            "",
        ]
    lines += [
        f"Both campaigns select batch 12. Independent retests are {case['discovery_retest']:.6f} "
        f"for discovery and {case['optimization_retest']:.6f} for optimization; twelve-query "
        f"score MAEs are {case['discovery_score_mae']:.6f} "
        f"and {case['optimization_score_mae']:.6f}.",
        "",
        r"\clearpage",
        "",
        "## E.7 Operation sequence and subsequent public accounts",
        "",
        "All batches add reagent, add solvent, set potential/electrolyte/current, electrolyze, "
        "measure UV-visible response, terminate and obtain a final assay, in that order. "
        "Discovery batches 11 and 12 insert a second 13,200-s electrolysis after the first "
        "1,200-s electrolysis and its UV-visible measurement. Their 14,400-s totals therefore "
        "do not describe one uninterrupted operation. The records contain 86 discovery and "
        "84 optimization operations. The phase labels in Figure 3 summarize recorded choices, "
        "not contemporaneous internal thoughts.",
        "",
        "The following original public rationales accompany the sealed Q forecasts, after "
        "research and K1. They were issued without reference feedback. They are public accounts, "
        "not validated mechanisms or evidence that the acquired observations were sufficient.",
        "",
    ]
    for goal in ("discovery", "optimization"):
        lines += [f"**{goal.capitalize()} Q rationale (verbatim).**", "", "> " + accounts[goal], ""]
    lines += [
        r"\clearpage",
        "",
        "## E.8 Complete optimization forecasts",
        "",
        "All twelve forecasts use 0.012 mol in 0.025 L. Predictions and nominal 80% intervals "
        "were sealed before reference feedback. References below are the original seeded "
        "observations. The four bold query identifiers share +0.8 V, 100 mA and 7,200 s, "
        "while changing the material pair.",
        "",
        "**Table E7. Query settings, sealed forecasts and reference scores.**",
        "",
        table(
            ["Q", "Pair", "V", "mA", "s", "Forecast", "80% interval", "Reference"],
            [
                [
                    f"**{q['query'][1:]}**"
                    if q["query"] in ("Q04", "Q06", "Q08", "Q10")
                    else q["query"][1:],
                    f"S{q['solvent']}/E{q['electrolyte_profile']}",
                    f"{q['potential_V']:g}",
                    f"{q['current_mA']:g}",
                    f"{q['duration_s']:g}",
                    f"{q['predicted_score']:.3f}",
                    f"{q['lower80']:.3f}-{q['upper80']:.3f}",
                    f"{q['reference_score']:.6f}",
                ]
                for q in queries
            ],
        ),
        "",
        f"Score MAE is {fmean(q['absolute_error'] for q in queries):.6f}; interval coverage is "
        "5/12. The accurate Q04 prediction is retained alongside the large underestimates "
        "at Q06, Q08 and Q10. Source-to-query changes involve amount, volume and electrical "
        "settings, so these contrasts do not isolate one changed variable. Twelve query "
        "outcomes do not establish population calibration. No intermediate sealed prediction "
        "checkpoints were collected, so final prediction errors cannot be plotted as a "
        "within-session learning curve.",
        "",
    ]
    (ROOT / "paper/venues/ncs/goal_prediction_details.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main():
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 7.2,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    summary, goal_pairs = prepare()
    pairs = matched_pairs()
    _, queries, _ = selected_case(pairs)
    paths, accounts, case = case_paths(goal_pairs)
    draw_main(summary, goal_pairs, paths, queries, case)
    draw_means(summary)
    supporting_text(summary, pairs, paths, queries, accounts, case)
    print(
        "Verified/rendered: 60 matched pairs, 24 batch scores, 170 public actions, "
        "2 independent retests and all 12 sealed forecasts. No agent or simulator calls."
    )


if __name__ == "__main__":
    main()
