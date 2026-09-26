"""Four-panel crystallization narrative from retained campaign data only."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from ncs_figure_style import ARM_COLORS as COLORS
from ncs_figure_style import ARMS
from render_crystal_simple_preview import SOURCE, summarize

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/figures/crystal-story-preview"
INK, MUTED, GRID = "#34434C", "#63717B", "#E5E9EC"
AGENT, OBS, REF = "#337F89", "#92A0AA", "#CDD5DA"
METRICS = ("crystal_yield", "crystal_fines_fraction", "crystal_size", "crystal_purity")


def prepare():
    rows = json.loads(SOURCE.read_text(encoding="utf-8"))["rows"]
    with (ROOT / "paper/figures/integrated-results/campaign_metrics.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        metrics = [r for r in csv.DictReader(stream) if r["system"] == "C"]
    assert len(rows) == 30 and len({r["id"] for r in rows}) == 30
    assert len(metrics) == 120
    lookup = {(r["id"], r["metric"]): r for r in metrics}
    assert len(lookup) == 120
    for row in rows:
        for metric in METRICS:
            assert abs(float(lookup[row["id"], metric]["mae"]) - row["agent_mae"][metric]) < 1e-12
    groups = []
    for budget in (12, 24):
        for arm in ARMS:
            subset = [r for r in rows if r["budget"] == budget and r["arm"] == arm]
            assert len(subset) == 5 and len({r["world"] for r in subset}) == 5
            groups.append(
                {
                    "budget": budget,
                    "arm": arm,
                    "campaigns": 5,
                    "recovery_mae_pp": 100 * fmean(r["agent_mae"]["crystal_yield"] for r in subset),
                    "purity_mae_pp": 100 * fmean(r["agent_mae"]["crystal_purity"] for r in subset),
                    "purity_coverage_percent": 100
                    * fmean(float(lookup[r["id"], "crystal_purity"]["coverage"]) for r in subset),
                    "purity_interval_width_pp": 100
                    * fmean(float(lookup[r["id"], "crystal_purity"]["width"]) for r in subset),
                }
            )
    wins = {
        m: sum(r["agent_mae"][m] < r["public_baselines"]["mae"]["public_mean"][m] for r in rows)
        for m in METRICS
    }
    assert list(wins.values()) == [26, 21, 4, 0]
    joint = []
    for budget in (12, 24):
        for arm in ARMS[1:]:
            counts = {"all": 0, "both_conforming": 0, "both_conforming_denominator": 0}
            for world in (f"W{i:02d}" for i in range(1, 6)):
                a, o = [
                    next(
                        r
                        for r in rows
                        if (r["world"], r["budget"], r["arm"]) == (world, budget, aa)
                    )
                    for aa in (arm, "Opaque")
                ]
                direction = (
                    a["agent_mae"]["crystal_yield"] < o["agent_mae"]["crystal_yield"]
                    and a["agent_mae"]["crystal_purity"] > o["agent_mae"]["crystal_purity"]
                )
                counts["all"] += int(direction)
                if a["conforming"] and o["conforming"]:
                    counts["both_conforming_denominator"] += 1
                    counts["both_conforming"] += int(direction)
            joint.append({"budget": budget, "arm_vs_opaque": arm, "denominator": 5, **counts})
    assert [r["all"] for r in joint] == [5, 5, 2, 3]
    assert [r["both_conforming"] for r in joint[:2]] == [4, 4]
    summary = summarize(rows)
    summary.update(
        {"response_wins": wins, "arm_budget_means": groups, "paired_joint_directions": joint}
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for name, rr in [("arm-budget-means", groups), ("all-campaign-metrics", metrics)]:
        with (OUT / f"{name}.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rr[0]))
            writer.writeheader()
            writer.writerows(rr)
    return summary


def axis_style(ax, horizontal=False):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left" if horizontal else "bottom"].set_visible(False)
    ax.spines["bottom" if horizontal else "left"].set_color("#A8B3BA")
    ax.grid(axis="x" if horizontal else "y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=7)


def draw(s, publish=False):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 16,
            "font.weight": "normal",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "axes.linewidth": 0.7,
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(14.4, 10.8), facecolor="white")
    for letter, x, y, title in [
        ("a", 0.025, 0.951, "Observed and predicted purity"),
        ("b", 0.531, 0.951, "Predictive value varies by response"),
        ("c", 0.025, 0.472, "Information effects differ across responses"),
        ("d", 0.531, 0.472, "Purity intervals can miss the reference"),
    ]:
        fig.text(x, y, letter, fontsize=21.5, weight="bold")
        fig.text(x + 0.027, y, title, fontsize=17.5)
    fig.text(
        0.052,
        0.906,
        "335 of 360 purity forecasts are below their reference",
        color=MUTED,
        size=15,
    )
    fig.text(
        0.558,
        0.906,
        "Campaigns with lower agent MAE\nthan the observed-mean baseline",
        color=MUTED,
        size=15,
    )
    a = fig.add_axes([0.186, 0.585, 0.293, 0.282])
    axis_style(a, horizontal=True)
    a.set(xlim=(0, 100), ylim=(-0.6, 3.7), xlabel="Mean crystal purity (%)")
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_yticks([])
    levels = s["all"]["purity_levels_percent"]
    values = [
        levels["source_observed_mean"],
        levels["reference_mean"],
        s["12"]["purity_levels_percent"]["prediction_mean"],
        s["24"]["purity_levels_percent"]["prediction_mean"],
    ]
    labels = [
        "Research observations\n30 campaigns",
        "Blind-test reference\n30 campaigns",
        "Agent: 12 batches\n15 campaigns",
        "Agent: 24 batches\n15 campaigns",
    ]
    for y, val, label, color in zip(
        [3.15, 2.15, 0.9, -0.1], values, labels, [OBS, REF, AGENT, AGENT], strict=True
    ):
        a.barh(y, val, height=0.49, color=color)
        a.text(
            -0.035,
            y,
            label,
            transform=a.get_yaxis_transform(),
            ha="right",
            va="center",
            size=16,
            linespacing=1.5,
        )
        a.text(
            val - 2,
            y,
            f"{val:.2f}%",
            ha="right",
            va="center",
            size=16,
            color="white" if color == AGENT else INK,
        )
    b = fig.add_axes([0.685, 0.585, 0.275, 0.282])
    axis_style(b, horizontal=True)
    b.set(xlim=(0, 30), ylim=(-0.6, 3.7), xlabel="Campaigns (of 30)")
    b.set_xticks([0, 10, 20, 30])
    b.set_yticks([3, 2, 1, 0], ["Recovery", "Fines fraction", "Particle size index", "Purity"])
    for y, metric in zip([3, 2, 1, 0], METRICS, strict=True):
        wins = s["response_wins"][metric]
        b.barh(y, 30, height=0.47, color="#E9EDF0")
        b.barh(y, wins, height=0.47, color=AGENT)
        b.text(
            wins - 0.6 if wins > 4 else wins + 0.6,
            y,
            f"{wins}/30",
            va="center",
            ha="right" if wins > 4 else "left",
            color="white" if wins > 4 else INK,
            size=16,
        )
    legend = [Patch(color=COLORS[arm], label=arm) for arm in ARMS]
    for anchor in (0.052, 0.558):
        fig.legend(
            handles=legend,
            loc="center left",
            bbox_to_anchor=(anchor, 0.430),
            ncol=3,
            frameon=False,
            fontsize=16,
            handlelength=1.1,
            columnspacing=1.8,
        )
    c = fig.add_axes([0.074, 0.102, 0.405, 0.282])
    d = fig.add_axes([0.610, 0.102, 0.350, 0.282])
    lookup = {(r["budget"], r["arm"]): r for r in s["arm_budget_means"]}
    for ax in (c, d):
        axis_style(ax)
    positions = np.array([0, 1, 2.6, 3.6])
    for j, arm in enumerate(ARMS):
        yy = [
            lookup[budget, arm][metric]
            for metric in ("recovery_mae_pp", "purity_mae_pp")
            for budget in (12, 24)
        ]
        bars = c.bar(positions + (j - 1) * 0.22, yy, width=0.2, color=COLORS[arm])
        c.bar_label(bars, labels=[f"{v:.1f}" for v in yy], padding=4, fontsize=15)
        cov = [lookup[budget, arm]["purity_coverage_percent"] for budget in (12, 24)]
        bars = d.bar(np.array([0, 1]) + (j - 1) * 0.22, cov, width=0.2, color=COLORS[arm], zorder=3)
        d.bar_label(
            bars,
            labels=[f"{v:.1f}" for v in cov],
            padding=4,
            fontsize=15,
            zorder=5,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5},
        )
    c.set(ylim=(0, 18.8), ylabel="Prediction MAE (percentage points)")
    c.set_yticks([0, 5, 10, 15])
    c.set_xticks(positions, ["12 batches", "24 batches", "12 batches", "24 batches"], fontsize=15)
    c.text(0.5, -0.17, "Recovery", transform=c.get_xaxis_transform(), ha="center", size=16)
    c.text(3.1, -0.17, "Purity", transform=c.get_xaxis_transform(), ha="center", size=16)
    c.axvline(1.8, color=GRID, lw=0.7)
    d.set(ylim=(0, 110), ylabel="Purity interval coverage (%)")
    d.set_yticks([0, 20, 40, 60, 80, 100])
    d.set_xticks([0, 1], ["12 batches", "24 batches"])
    d.axhline(80, color="#536570", linestyle=(0, (4, 3)), lw=1, zorder=4)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"crystal-four-panel-story.{ext}", dpi=200)
    if publish:
        destination = ROOT / "paper/figures/venue-results"
        destination.mkdir(parents=True, exist_ok=True)
        for ext in ("pdf", "png", "svg"):
            fig.savefig(destination / f"figure06-crystal-generalization.{ext}", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Export approved manuscript assets")
    args = parser.parse_args()
    result = prepare()
    draw(result, publish=args.publish)
    print(
        "Four panels rendered: 30 campaigns, 120 response summaries, "
        "6 arm-budget means; no new experiments."
    )
