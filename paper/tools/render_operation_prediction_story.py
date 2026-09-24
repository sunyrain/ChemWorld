"""Rebuild operation/prediction comparisons from the retained paired campaigns."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "paper/figures/integrated-results"
OUT = ROOT / "output/figures/operation-prediction-story"
ASSETS = ROOT / "paper/figures/venue-results"
INK, MUTED, AXIS = "#26343D", "#63717B", "#111111"
DISCOVERY, OPTIMIZATION = "#9AABB4", "#0F858B"
ARM_COLORS = {
    "Opaque": "#187AA5",
    "Aligned": "#DB6B25",
    "MisIndexed": "#209887",
}
QUADRANT_COLORS = {
    "operation_worse_prediction_better": "#F2EEF8",
    "both_better": "#EDF6EF",
    "both_worse": "#EDF3F6",
    "operation_better_prediction_worse": "#FBEFE8",
}
KEYS = ("world", "locus", "budget", "arm")
CATEGORIES = (
    "both_better",
    "operation_better_prediction_worse",
    "operation_worse_prediction_better",
    "both_worse",
)


def classify(retest, error):
    assert retest != 0 and error != 0, "A tie must be explicitly represented"
    return CATEGORIES[(0 if retest > 0 else 2) + (0 if error < 0 else 1)]


def prepare():
    reference = json.loads((SOURCE / "analysis.json").read_text(encoding="utf-8"))
    with (SOURCE / "campaign_metrics.csv").open(encoding="utf-8", newline="") as stream:
        raw = [
            r
            for r in csv.DictReader(stream)
            if r["system"] in ("EC", "RX") and r["metric"] == "score"
        ]
    assert len(raw) == 120 and len({r["id"] for r in raw}) == 120
    pairs, world_means, overall = [], [], {}
    for system in ("EC", "RX"):
        rr = [r for r in raw if r["system"] == system]
        original = reference["goal_contrasts"][system]
        for opt in [r for r in rr if r["goal"] == "optimization"]:
            discovery = next(
                r for r in rr if r["goal"] == "discovery" and all(r[k] == opt[k] for k in KEYS)
            )
            retained = next(r for r in original if all(str(r[k]) == opt[k] for k in KEYS))
            ds, os = float(discovery["retest"]), float(opt["retest"])
            de, oe = float(discovery["mae"]), float(opt["mae"])
            assert abs((os - ds) - retained["delta_retest"]) < 1e-12
            assert abs((oe - de) - retained["delta_mae"]) < 1e-12
            pairs.append(
                {
                    "system": system,
                    **{k: opt[k] for k in KEYS},
                    "discovery_id": discovery["id"],
                    "optimization_id": opt["id"],
                    "discovery_retest": ds,
                    "optimization_retest": os,
                    "discovery_score_mae": de,
                    "optimization_score_mae": oe,
                    "delta_retest": os - ds,
                    "delta_score_mae": oe - de,
                    "outcome": classify(os - ds, oe - de),
                    "no_source_restart": retained["first_attempt"],
                    "both_conforming": discovery["conforming"] == opt["conforming"] == "True",
                }
            )
        pp = [r for r in pairs if r["system"] == system]
        counts = {k: sum(r["outcome"] == k for r in pp) for k in CATEGORIES}
        overall[system] = {
            "pairs": len(pp),
            "outcomes": counts,
            "better_retest": sum(r["delta_retest"] > 0 for r in pp),
            "lower_mae": sum(r["delta_score_mae"] < 0 for r in pp),
            **{
                f"{g}_{metric}_mean": fmean(r[f"{g}_{metric}"] for r in pp)
                for g in ("discovery", "optimization")
                for metric in ("retest", "score_mae")
            },
        }
        assert sum(counts.values()) == 30
        assert overall[system]["better_retest"] == reference["goal_counts"][system]["better_retest"]
        assert overall[system]["lower_mae"] == reference["goal_counts"][system]["lower_mae"]
        for world in sorted({r["world"] for r in pp}):
            ww = [r for r in pp if r["world"] == world]
            assert len(ww) == 6
            world_means.append(
                {
                    "system": system,
                    "world": world,
                    "pairs": len(ww),
                    **{
                        f"{g}_{metric}": fmean(r[f"{g}_{metric}"] for r in ww)
                        for g in ("discovery", "optimization")
                        for metric in ("retest", "score_mae")
                    },
                    "discordant": sum(r["outcome"] == CATEGORIES[1] for r in ww),
                    "both_better": sum(r["outcome"] == CATEGORIES[0] for r in ww),
                }
            )
    clean = [r for r in pairs if r["system"] == "EC" and r["no_source_restart"]]
    sensitivity = {
        "pairs": len(clean),
        "better_retest": sum(r["delta_retest"] > 0 for r in clean),
        "lower_mae": sum(r["delta_score_mae"] < 0 for r in clean),
        "discordant": sum(r["outcome"] == CATEGORIES[1] for r in clean),
    }
    assert list(overall["EC"]["outcomes"].values()) == [13, 13, 1, 3]
    assert list(overall["RX"]["outcomes"].values()) == [4, 5, 4, 17]
    assert list(sensitivity.values()) == [17, 15, 8, 7]
    assert [r["discordant"] for r in world_means if r["system"] == "EC"] == [3, 2, 3, 1, 4]
    summary = {"overall": overall, "world_means": world_means, "no_restart_EC": sensitivity}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for name, rr in (("all-60-pairs", pairs), ("world-means", world_means)):
        with (OUT / f"{name}.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rr[0]))
            writer.writeheader()
            writer.writerows(rr)
    return summary, pairs


def style(ax, horizontal=False):
    ax.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.6)
    ax.tick_params(
        axis="both",
        which="major",
        direction="out",
        length=2.5,
        width=0.6,
        color=AXIS,
        labelcolor=AXIS,
        pad=3,
    )
    ax.grid(False)


def quadrant_background(ax, xlim, ylim):
    xmin, xmax = xlim
    ymin, ymax = ylim
    regions = (
        ((xmin, 0), -xmin, ymax, QUADRANT_COLORS["operation_worse_prediction_better"]),
        ((0, 0), xmax, ymax, QUADRANT_COLORS["both_better"]),
        ((xmin, ymin), -xmin, -ymin, QUADRANT_COLORS["both_worse"]),
        ((0, ymin), xmax, -ymin, QUADRANT_COLORS["operation_better_prediction_worse"]),
    )
    for origin, width, height, color in regions:
        ax.add_patch(
            Rectangle(
                origin,
                width,
                height,
                facecolor=color,
                edgecolor="none",
                zorder=0,
            )
        )


def quadrant_labels(ax, counts, fontsize=5.75):
    labels = (
        (0.04, 0.95, "Prediction better\nRetest worse", counts["operation_worse_prediction_better"], "left", "top"),
        (0.54, 0.95, "Both better", counts["both_better"], "left", "top"),
        (0.04, 0.05, "Both worse", counts["both_worse"], "left", "bottom"),
        (0.96, 0.05, "Retest better\nPrediction worse", counts["operation_better_prediction_worse"], "right", "bottom"),
    )
    for x, y, label, count, ha, va in labels:
        ax.text(
            x,
            y,
            f"{label}\n{count}/30",
            transform=ax.transAxes,
            ha=ha,
            va=va,
            fontsize=fontsize,
            color=INK,
            linespacing=1.35,
            zorder=5,
        )


def draw_joint(ax, pairs, counts, *, xlim, ylim, xticks, yticks, label_fontsize=5.75):
    assert len(pairs) == 30
    assert sum(counts.values()) == 30
    assert abs(xlim[0] + xlim[1]) < 1e-12
    assert abs(ylim[0] + ylim[1]) < 1e-12
    xx = [r["delta_retest"] for r in pairs]
    yy = [-r["delta_score_mae"] for r in pairs]
    assert xlim[0] < min(xx) and max(xx) < xlim[1]
    assert ylim[0] < min(yy) and max(yy) < ylim[1]
    quadrant_background(ax, xlim, ylim)
    for arm in ("Opaque", "Aligned", "MisIndexed"):
        rows = [r for r in pairs if r["arm"] == arm]
        assert len(rows) == 10
        ax.scatter(
            [r["delta_retest"] for r in rows],
            [-r["delta_score_mae"] for r in rows],
            s=18,
            marker="o",
            color=ARM_COLORS[arm],
            edgecolor="white",
            linewidth=0.35,
            alpha=0.94,
            zorder=3,
        )
    ax.axvline(0, color="#78858D", linewidth=0.45, linestyle=(0, (4, 3)), zorder=2)
    ax.axhline(0, color="#78858D", linewidth=0.45, linestyle=(0, (4, 3)), zorder=2)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel("Change in retested score", labelpad=4)
    ax.set_ylabel("Prediction improvement", labelpad=4)
    ax.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.6)
    ax.tick_params(
        axis="both",
        which="major",
        direction="out",
        length=2.5,
        width=0.6,
        color=AXIS,
        labelcolor=AXIS,
        pad=3,
    )
    ax.grid(False)
    quadrant_labels(ax, counts, fontsize=label_fontsize)


def draw_world_bars(ax, rows, metric):
    xx = np.arange(5)
    style(ax)
    for offset, goal, color in (
        (-0.21, "discovery", DISCOVERY),
        (0.21, "optimization", OPTIMIZATION),
    ):
        ax.bar(
            xx + offset,
            [r[f"{goal}_{metric}"] for r in rows],
            width=0.38,
            color=color,
        )
    ax.set_xticks(xx, [f"W{i}" for i in range(1, 6)], fontsize=5.75)


def draw(s, pairs):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 6.5,
            "font.weight": "normal",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": AXIS,
            "ytick.color": AXIS,
            "axes.linewidth": 0.6,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )
    # Native 183-mm full-width canvas: no hidden 50% downscaling in the paper.
    # A compact landscape grid keeps each panel visually wide at 183-mm output.
    fig = plt.figure(figsize=(7.2, 4.55), facecolor="white")
    for letter, x, y, title in [
        ("a", 0.025, 0.950, "EC recommendation performance"),
        ("b", 0.355, 0.950, "EC prediction error"),
        ("c", 0.685, 0.950, "EC joint outcomes"),
        ("d", 0.025, 0.510, "RX recommendation performance"),
        ("e", 0.355, 0.510, "RX prediction error"),
        ("f", 0.685, 0.510, "RX joint outcomes"),
    ]:
        fig.text(x, y, letter, size=8.5, weight="bold", va="top")
        fig.text(x + 0.032, y, title, size=7, weight="bold", va="top")
    commission_legend = [
        Patch(color=DISCOVERY, label="Discovery"),
        Patch(color=OPTIMIZATION, label="Optimization"),
    ]
    fig.legend(
        handles=commission_legend,
        loc="upper right",
        bbox_to_anchor=(0.990, 0.995),
        ncol=2,
        frameon=False,
        fontsize=6,
        handlelength=1.1,
        columnspacing=1.5,
    )
    axes = {
        "a": fig.add_axes([0.060, 0.650, 0.255, 0.245]),
        "b": fig.add_axes([0.390, 0.650, 0.255, 0.245]),
        "c": fig.add_axes([0.720, 0.650, 0.270, 0.245]),
        "d": fig.add_axes([0.060, 0.200, 0.255, 0.250]),
        "e": fig.add_axes([0.390, 0.200, 0.255, 0.250]),
        "f": fig.add_axes([0.720, 0.200, 0.270, 0.250]),
    }
    ec_worlds = [r for r in s["world_means"] if r["system"] == "EC"]
    rx_worlds = [r for r in s["world_means"] if r["system"] == "RX"]
    draw_world_bars(axes["a"], ec_worlds, "retest")
    draw_world_bars(axes["b"], ec_worlds, "score_mae")
    draw_world_bars(axes["d"], rx_worlds, "retest")
    draw_world_bars(axes["e"], rx_worlds, "score_mae")
    axes["a"].set_ylim(0, 0.9)
    axes["a"].set_yticks([0, 0.3, 0.6, 0.9])
    axes["d"].set_ylim(0, 0.45)
    axes["d"].set_yticks([0, 0.15, 0.30, 0.45])
    for ax in (axes["a"], axes["d"]):
        ax.set_ylabel("Retested score")
    axes["b"].set_ylim(0, 0.22)
    axes["b"].set_yticks([0, 0.05, 0.10, 0.15, 0.20])
    axes["e"].set_ylim(0, 0.13)
    axes["e"].set_yticks([0, 0.04, 0.08, 0.12])
    for ax in (axes["b"], axes["e"]):
        ax.set_ylabel("Score MAE")
    ec_pairs = [r for r in pairs if r["system"] == "EC"]
    rx_pairs = [r for r in pairs if r["system"] == "RX"]
    draw_joint(
        axes["c"],
        ec_pairs,
        s["overall"]["EC"]["outcomes"],
        xlim=(-0.56, 0.56),
        ylim=(-0.25, 0.25),
        xticks=(-0.50, -0.25, 0, 0.25, 0.50),
        yticks=(-0.2, -0.1, 0, 0.1, 0.2),
        label_fontsize=5.0,
    )
    draw_joint(
        axes["f"],
        rx_pairs,
        s["overall"]["RX"]["outcomes"],
        xlim=(-0.08, 0.08),
        ylim=(-0.20, 0.20),
        xticks=(-0.06, -0.03, 0, 0.03, 0.06),
        yticks=(-0.2, -0.1, 0, 0.1, 0.2),
        label_fontsize=5.0,
    )
    arm_legend = [
        Line2D([], [], linestyle="none", marker="", label="Information arm"),
        *[
            Line2D(
                [],
                [],
                linestyle="none",
                marker="o",
                markersize=3.5,
                markerfacecolor=ARM_COLORS[arm],
                markeredgecolor="white",
                markeredgewidth=0.35,
                label=arm,
            )
            for arm in ("Opaque", "Aligned", "MisIndexed")
        ],
    ]
    fig.legend(
        handles=arm_legend,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.018),
        frameon=False,
        ncol=4,
        fontsize=5.75,
        handletextpad=0.55,
        columnspacing=1.8,
    )
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        ASSETS / "figure03-operation-prediction.pdf",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    fig.savefig(
        ASSETS / "figure03-operation-prediction.svg",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    fig.savefig(
        ASSETS / "figure03-operation-prediction.png",
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    fig.savefig(OUT / "operation-prediction-four-panels.png", dpi=600)
    plt.close(fig)


if __name__ == "__main__":
    summary, paired_rows = prepare()
    draw(summary, paired_rows)
    print(
        "Rendered 6 panels from 120 campaigns / 60 pairs; "
        "exact retained deltas and restart sensitivity verified."
    )
