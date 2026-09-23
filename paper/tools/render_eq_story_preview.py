"""Preview the EQ evidence-to-prediction story using retained data only."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
OUT = ROOT / "output/figures/eq-story-preview"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = {"Opaque": "#607382", "Aligned": "#287E88", "MisIndexed": "#B87752"}
INK, MUTED, RULE = "#24323C", "#61717C", "#D6DDE1"


def main():
    process = json.loads((SOURCE / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    story = json.loads((SOURCE / "STORY_WORLD_ANALYSIS.json").read_text(encoding="utf-8"))
    rows = process["rows"]
    cells = story["eq_p_query_regimes"]["cells"]
    agg = story["eq_p_query_regimes"]["aggregate"]
    assert len(rows) == 15 and sum(len(r["batches"]) for r in rows) == 180
    assert {(r["world"], r["arm"]) for r in rows} == {
        (f"W0{i}", a) for i in range(1, 6) for a in ARMS
    }
    stats = {(r["arm"], r["group"]): r for r in agg}
    for a in ARMS:
        for group in ("other_nine", "three_most_dilute"):
            for metric in ("mae", "coverage"):
                vals = [r["groups"][group][metric] for r in cells if r["arm"] == a]
                assert abs(np.mean(vals) - stats[a, group][metric]) < 1e-12
    ordered = [
        next(r for r in rows if r["world"] == f"W0{i}" and r["arm"] == a)
        for i in range(1, 6)
        for a in ARMS
    ]
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 11,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.edgecolor": "#AAB5BC",
            "axes.linewidth": 0.7,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(13.6, 9.0), facecolor="white")
    fig.text(0.045, 0.959, "a  What was observed, and what changed?", weight="bold", size=14)
    fig.text(
        0.55, 0.959, "b  Which predictions leave the observed plateau?", weight="bold", size=14
    )
    fig.text(0.045, 0.927, "Selected matched example: World 2", color=MUTED, size=11)
    fig.text(0.55, 0.927, "Most dilute test: all five worlds, all three arms", color=MUTED, size=11)

    ax = fig.add_axes([0.085, 0.574, 0.355, 0.306])
    ax.set_xscale("log")
    queries = ("Q03", "Q08", "Q09")
    query_c = process["query_concentrations"]
    example = [r for r in rows if r["world"] == "W02"]
    source_min = min(b["nominal_concentration_mol_L"] for r in rows for b in r["batches"])
    assert source_min > max(query_c[q] for q in queries)
    ax.axvspan(8e-6, 2.2e-4, color="#EEF1F3", zorder=0)
    for a in ARMS:
        r = next(r for r in example if r["arm"] == a)
        ax.scatter(
            [b["nominal_concentration_mol_L"] for b in r["batches"]],
            [100 * b["final_responses"]["acid_dissociation_fraction"] for b in r["batches"]],
            color=COLORS[a],
            s=26,
            edgecolor="white",
            linewidth=0.35,
            zorder=3,
        )
    points = next(r for r in cells if r["world"] == "W02" and r["arm"] == "Opaque")
    refs = {
        p["query"]: p["truth_mean"]
        for p in points["groups"]["three_most_dilute"]["points"]
        if p["metric"] == "acid_dissociation_fraction"
    }
    ax.scatter(
        [query_c[q] for q in queries],
        [refs[q] * 100 for q in queries],
        color=INK,
        marker="D",
        s=45,
        zorder=4,
    )
    ax.annotate(
        "Dilute-test reference\n65.5% at 13.3 µM",
        (query_c["Q08"], refs["Q08"] * 100),
        xytext=(8e-5, 78),
        fontsize=11,
        ha="left",
        arrowprops={"arrowstyle": "-", "lw": 0.8, "color": INK},
    )
    ax.annotate(
        "Observed plateau\n36 measured batches",
        (0.15, 7),
        xytext=(0.003, 33),
        fontsize=11,
        arrowprops={"arrowstyle": "-", "lw": 0.8, "color": MUTED},
    )
    ax.text(4.2e-5, 95, "Dilute tests", ha="center", size=10, color=MUTED)
    ax.set(
        xlim=(8e-6, 3),
        ylim=(0, 100),
        ylabel="Dissociation (%)",
        xlabel="Nominal concentration (mol/L; log scale)",
    )
    ax.set_xticks([1e-5, 1e-3, 1e-1, 1], [r"$10^{-5}$", r"$10^{-3}$", r"$10^{-1}$", "1"])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=RULE, linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)
    fig.text(
        0.085,
        0.467,
        "Across all 15 campaigns, none of the 180 batches\n"
        "reached the three dilute test concentrations.",
        size=11,
        linespacing=1.6,
    )

    bx = fig.add_axes([0.614, 0.531, 0.322, 0.355])
    export = []
    yticks, ylabels = [], []
    for wi in range(5):
        center = 16 - wi * 3.5
        rr = ordered[wi * 3 : wi * 3 + 3]
        reference = rr[0]["q08"]["reference_means"]["acid_dissociation_fraction"] * 100
        assert all(
            abs(r["q08"]["reference_means"]["acid_dissociation_fraction"] * 100 - reference) < 1e-10
            for r in rr
        )
        if wi % 2 == 0:
            bx.axhspan(center - 1.5, center + 1.5, color="#F6F8F9", zorder=0)
        bx.plot([reference, reference], [center - 1.25, center + 1.25], color=INK, lw=1.2, zorder=1)
        bx.text(
            reference + 1.5, center + 1.25, f"{reference:.1f}%", color=INK, size=9.3, va="center"
        )
        bx.text(-17, center, f"World {wi + 1}", weight="bold", size=10.5, va="center", ha="right")
        for ai, r in enumerate(rr):
            y = center + 0.82 - ai * 0.82
            a = r["arm"]
            pred = r["q08"]["predictions"]["acid_dissociation_fraction"]
            v, lo, hi = (100 * pred[k] for k in ("estimate", "lower80", "upper80"))
            src = np.array(r["source_dissociation_range"]) * 100
            bx.plot(src, [y, y], color="#BEC8CE", lw=6, solid_capstyle="butt", zorder=2)
            bx.errorbar(
                v,
                y,
                xerr=[[v - lo], [hi - v]],
                color=COLORS[a],
                fmt="o",
                lw=1.25,
                markersize=4.9,
                capsize=2.6,
                zorder=3,
            )
            yticks.append(y)
            ylabels.append({"Opaque": "O", "Aligned": "A", "MisIndexed": "M"}[a])
            export.append(
                {
                    "world": r["world"],
                    "arm": a,
                    "query": "Q08",
                    "reference_mean": reference / 100,
                    "source_min": src[0] / 100,
                    "source_max": src[1] / 100,
                    **pred,
                }
            )
    bx.set(xlim=(0, 100), ylim=(0.5, 18), xlabel="Predicted dissociation (%) and 80% interval")
    bx.set_xticks([0, 25, 50, 75, 100])
    bx.set_yticks(yticks, ylabels)
    bx.tick_params(axis="y", length=0, pad=8)
    bx.spines[["top", "left", "right"]].set_visible(False)
    bx.grid(axis="x", color=RULE, lw=0.5, alpha=0.65)
    bx.set_axisbelow(True)
    fig.text(
        0.615,
        0.443,
        "Black line: withheld reference mean   Grey: source range",
        size=9.4,
        color=MUTED,
    )

    handles = [
        Line2D(
            [],
            [],
            color=COLORS[a],
            marker="o",
            lw=0,
            label=f"{a[0] if a != 'MisIndexed' else 'M'}: {a}",
        )
        for a in ARMS
    ]
    fig.legend(
        handles=handles,
        loc="center",
        bbox_to_anchor=(0.255, 0.413),
        frameon=False,
        ncol=3,
        handletextpad=0.4,
        columnspacing=1.6,
        fontsize=10.5,
    )
    fig.add_artist(
        Line2D([0.045, 0.96], [0.385, 0.385], transform=fig.transFigure, color=RULE, lw=0.8)
    )
    fig.text(
        0.045,
        0.350,
        "c  The advantage of aligned information reverses across test regimes",
        weight="bold",
        size=14,
    )
    fig.text(
        0.045,
        0.319,
        "Other nine tests: 54% lower error vs Opaque.   "
        "Dilute three: 8.7-fold error.   Both directions in 5/5 worlds.",
        size=11.5,
    )
    tx = fig.add_axes([0.045, 0.119, 0.915, 0.188])
    tx.set_axis_off()
    tx.set(xlim=(0, 1), ylim=(0, 1))
    columns = [0.0, 0.34, 0.515, 0.74, 0.92]
    tx.text(0.426, 0.95, "Prediction error (macro MAE ↓)", ha="center", size=11, weight="bold")
    tx.text(0.83, 0.95, "80% interval coverage", ha="center", size=11, weight="bold")
    for x, label in zip(
        columns,
        ["Information arm", "Other nine", "Dilute three", "Other nine", "Dilute three"],
        strict=True,
    ):
        tx.text(x, 0.74, label, ha="left" if x == 0 else "center", size=10.5, color=MUTED)
    tx.plot([0, 1], [0.65, 0.65], color=RULE, lw=0.7)
    for i, a in enumerate(ARMS):
        yy = 0.51 - 0.215 * i
        tx.text(0, yy, a, color=COLORS[a], weight="bold", size=12, va="center")
        other, dilute = stats[a, "other_nine"], stats[a, "three_most_dilute"]
        values = [
            f"{other['mae']:.4f}",
            f"{dilute['mae']:.4f}",
            f"{100 * other['coverage']:.1f}%",
            f"{100 * dilute['coverage']:.1f}%",
        ]
        for x, v in zip(columns[1:], values, strict=True):
            tx.text(
                x,
                yy,
                v,
                ha="center",
                va="center",
                size=12,
                weight="bold" if a == "Aligned" else "normal",
            )
    tx.plot([0, 1], [0.015, 0.015], color=RULE, lw=0.7)
    fig.text(
        0.045,
        0.077,
        "a,b: dissociation response. c: three-response aggregate; "
        "five worlds per arm. Groups defined post hoc by public test concentrations.",
        size=9.4,
        color=MUTED,
    )
    fig.text(
        0.045,
        0.051,
        "Reference values were not shown to the agent. "
        "No continuous response curve or internal reasoning is inferred from these points.",
        size=9.4,
        color=MUTED,
    )
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"eq-evidence-to-prediction.{ext}", dpi=180)
    plt.close(fig)
    with (OUT / "predictions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(export[0]))
        writer.writeheader()
        writer.writerows(export)
    win = sum(
        next(r for r in cells if r["world"] == w and r["arm"] == "Aligned")["groups"]["other_nine"][
            "mae"
        ]
        < next(r for r in cells if r["world"] == w and r["arm"] == "Opaque")["groups"][
            "other_nine"
        ]["mae"]
        for w in {r["world"] for r in cells}
    )
    loss = sum(
        next(r for r in cells if r["world"] == w and r["arm"] == "Aligned")["groups"][
            "three_most_dilute"
        ]["mae"]
        > next(r for r in cells if r["world"] == w and r["arm"] == "Opaque")["groups"][
            "three_most_dilute"
        ]["mae"]
        for w in {r["world"] for r in cells}
    )
    assert win == loss == 5
    reduction = 1 - stats["Aligned", "other_nine"]["mae"] / stats["Opaque", "other_nine"]["mae"]
    ratio = (
        stats["Aligned", "three_most_dilute"]["mae"] / stats["Opaque", "three_most_dilute"]["mae"]
    )
    assert round(reduction * 100) == 54 and round(ratio, 1) == 8.7
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "new_experiments": 0,
                "manuscript_replaced": False,
                "source_campaigns": 15,
                "source_batches": 180,
                "panel_a_selected_world": "W02",
                "panel_a_batches": 36,
                "panel_b_predictions": 15,
                "minimum_source_concentration_mol_L": source_min,
                "aligned_error_reduction_other_nine": reduction,
                "aligned_error_ratio_dilute_three": ratio,
                "aligned_better_other_nine_worlds": win,
                "aligned_worse_dilute_worlds": loss,
                "aggregate_values": agg,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Preview ready: 36 source observations, 3 reference means, {len(export)} sealed "
        "predictions; 5/5 reversals verified."
    )


if __name__ == "__main__":
    main()
