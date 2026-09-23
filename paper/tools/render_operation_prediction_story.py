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
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "paper/figures/integrated-results"
OUT = ROOT / "output/figures/operation-prediction-story"
ASSETS = ROOT / "paper/figures/venue-results"
INK, MUTED, GRID = "#34434C", "#63717B", "#E5E9EC"
DISCOVERY, OPTIMIZATION, REACTION = "#94A3AD", "#337F89", "#B47857"
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
    return summary


def style(ax, horizontal=False):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left" if horizontal else "bottom"].set_visible(False)
    ax.spines["bottom" if horizontal else "left"].set_color("#A8B3BA")
    ax.tick_params(length=0, pad=8)
    ax.grid(axis="x" if horizontal else "y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def draw(s):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 16,
            "font.weight": "normal",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.linewidth": 0.7,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(14.4, 10.8), facecolor="white")
    for letter, x, y, title in [
        ("a", 0.025, 0.95, "Electrochemistry: recommendation performance"),
        ("b", 0.531, 0.95, "Electrochemistry: prediction error"),
        ("c", 0.025, 0.453, "Joint outcomes of the two commissions"),
        ("d", 0.531, 0.453, "Discordance across electrochemical worlds"),
    ]:
        fig.text(x, y, letter, size=21.5, weight="bold")
        fig.text(x + 0.027, y, title, size=17)
    ec = s["overall"]["EC"]
    fig.text(
        0.052,
        0.906,
        f"Mean score: {ec['discovery_retest_mean']:.3f} to {ec['optimization_retest_mean']:.3f}",
        size=16,
    )
    fig.text(0.052, 0.873, "Optimization improves 26/30 paired retests", size=15, color=MUTED)
    fig.text(
        0.558,
        0.906,
        f"Mean MAE: {ec['discovery_score_mae_mean']:.4f} "
        f"to {ec['optimization_score_mae_mean']:.4f}",
        size=16,
    )
    fig.text(0.558, 0.873, "Optimization improves 14/30 paired forecasts", size=15, color=MUTED)
    legend = [
        Patch(color=DISCOVERY, label="Discovery"),
        Patch(color=OPTIMIZATION, label="Optimization"),
    ]
    for x in (0.052, 0.558):
        fig.legend(
            handles=legend,
            loc="center left",
            bbox_to_anchor=(x, 0.836),
            ncol=2,
            frameon=False,
            fontsize=15,
            handlelength=1.1,
            columnspacing=2,
        )
    a = fig.add_axes([0.078, 0.552, 0.4, 0.243])
    b = fig.add_axes([0.61, 0.552, 0.35, 0.243])
    worlds = [r for r in s["world_means"] if r["system"] == "EC"]
    xx = np.arange(5)
    for ax, metric in ((a, "retest"), (b, "score_mae")):
        style(ax)
        for offset, goal, color in (
            (-0.18, "discovery", DISCOVERY),
            (0.18, "optimization", OPTIMIZATION),
        ):
            ax.bar(xx + offset, [r[f"{goal}_{metric}"] for r in worlds], width=0.32, color=color)
        ax.set_xticks(xx, [f"World {i}" for i in range(1, 6)], fontsize=14)
    a.set(ylim=(0, 0.9), ylabel="Retested score (higher is better)")
    a.set_yticks([0, 0.3, 0.6, 0.9])
    b.set(ylim=(0, 0.22), ylabel="Score MAE (lower is better)")
    b.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
    c = fig.add_axes([0.225, 0.08, 0.25, 0.265])
    style(c, horizontal=True)
    fig.legend(
        handles=[
            Patch(color=OPTIMIZATION, label="Electrochemistry"),
            Patch(color=REACTION, label="Reaction processing"),
        ],
        loc="center left",
        bbox_to_anchor=(0.052, 0.412),
        frameon=False,
        ncol=2,
        fontsize=14.5,
        handlelength=1.1,
        columnspacing=1.4,
    )
    categories = [
        "Both better",
        "Better retest,\nworse prediction",
        "Worse retest,\nbetter prediction",
        "Both worse",
    ]
    for offset, system, color in ((0.17, "EC", OPTIMIZATION), (-0.17, "RX", REACTION)):
        values = [s["overall"][system]["outcomes"][k] for k in CATEGORIES]
        bars = c.barh(np.array([3, 2, 1, 0]) + offset, values, height=0.28, color=color)
        c.bar_label(bars, labels=[f"{v}/30" for v in values], padding=4, size=14.5)
    c.set(xlim=(0, 30), ylim=(-0.6, 3.6), xlabel="Matched pairs (of 30 per system)")
    c.set_xticks([0, 10, 20, 30])
    c.set_yticks([3, 2, 1, 0], categories, fontsize=14.5)
    d = fig.add_axes([0.61, 0.08, 0.35, 0.265])
    style(d)
    fig.text(0.558, 0.412, "Better retest, worse prediction: 13/30 pairs", size=15, color=MUTED)
    values = [r["discordant"] for r in worlds]
    bars = d.bar(xx, values, width=0.57, color=OPTIMIZATION)
    d.bar_label(bars, labels=[f"{v}/6" for v in values], padding=6, size=16)
    d.set(ylim=(0, 6), ylabel="Discordant pairs (of 6 per world)")
    d.set_yticks([0, 2, 4, 6])
    d.set_xticks(xx, [f"World {i}" for i in range(1, 6)], fontsize=14)
    ASSETS.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(ASSETS / f"figure03-operation-prediction.{ext}", dpi=300)
    fig.savefig(OUT / "operation-prediction-four-panels.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    summary = prepare()
    draw(summary)
    print(
        "Rendered 4 panels from 120 campaigns / 60 pairs; "
        "exact retained deltas and restart sensitivity verified."
    )
