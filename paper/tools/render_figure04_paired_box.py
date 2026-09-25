#!/usr/bin/env python3
"""Render the paired box-and-point candidate for manuscript Figure 4.

Each panel retains all 15 matched world-arm pairs at 12 and 24 batches. Boxes
show the interquartile range and median; the title reports campaign means and
the strict-sign improvement count. Lines join the same pair. No inferential
test or significance annotation is added.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "paper/figures/academic-ppt/retained-figure-data.json"
OUT_STEM = ROOT / "paper/figures/venue-results/figure04-research-envelope-paired-box-compact"

INK = "#111111"
BOX_EDGE = "#30363A"
BOX_12 = "#D1DCE4"
BOX_24 = "#69BDAE"
FAVORABLE = "#277F8A"
UNFAVORABLE = "#A35F42"
SHORTFALL = "#6A737B"


DEFINITIONS = [
    {
        "system": "EC",
        "goal": "discovery",
        "metric": "score",
        "field": "mae",
        "heading": "EC discovery",
        "readout": "Score MAE ↓",
        "ylabel": "Score MAE",
        "ylim": (0.0, 0.30),
        "yticks": np.arange(0.0, 0.301, 0.05),
        "expected": (0.17378, 0.11222, 11),
    },
    {
        "system": "EC",
        "goal": "optimization",
        "metric": "score",
        "field": "mae",
        "heading": "EC optimization",
        "readout": "Score MAE ↓",
        "ylabel": "Score MAE",
        "ylim": (0.0, 0.30),
        "yticks": np.arange(0.0, 0.301, 0.05),
        "expected": (0.17811, 0.10818, 12),
    },
    {
        "system": "PA",
        "goal": "discovery",
        "metric": "product_in_organic",
        "field": "mae",
        "heading": "Partitioning",
        "readout": "Organic-fraction MAE ↓",
        "ylabel": "Organic-fraction MAE",
        "ylim": (0.0, 0.22),
        "yticks": np.arange(0.0, 0.201, 0.05),
        "expected": (0.08291, 0.02379, 13),
    },
    {
        "system": "C",
        "goal": "delivery",
        "metric": "crystal_yield",
        "field": "mae",
        "heading": "Crystallization",
        "readout": "Recovery MAE ↓",
        "ylabel": "Recovery MAE",
        "ylim": (0.0, 0.42),
        "yticks": np.arange(0.0, 0.401, 0.10),
        "expected": (0.10433, 0.07937, 8),
    },
    {
        "system": "C",
        "goal": "delivery",
        "metric": "crystal_fines_fraction",
        "field": "coverage",
        "heading": "Crystallization",
        "readout": "Fines coverage ↑",
        "ylabel": "Fines coverage (%)",
        "ylim": (0.0, 80.0),
        "yticks": np.arange(0.0, 81.0, 20.0),
        "expected": (35.6, 43.9, 7),
    },
    {
        "system": "C",
        "goal": "delivery",
        "metric": "crystal_yield",
        "field": "retest",
        "heading": "Crystallization",
        "readout": "Retested recovery ↑",
        "ylabel": "Retested recovery (%)",
        "ylim": (0.0, 80.0),
        "yticks": np.arange(0.0, 81.0, 20.0),
        "expected": (0.42054, 0.39939, 7),
    },
]


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.0,
            "axes.labelsize": 7.0,
            "axes.titlesize": 7.5,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "axes.linewidth": 0.8,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )


def load_pairs(data: dict, definition: dict) -> tuple[list[dict], list[float], int]:
    rows = [
        row
        for row in data["campaigns"]
        if row["system"] == definition["system"]
        and row["goal"] == definition["goal"]
        and row["metric"] == definition["metric"]
    ]
    pairs: dict[tuple[str, str], dict[int, dict]] = defaultdict(dict)
    for row in rows:
        pairs[(row["world"], row["arm"])][int(row["budget"])] = row
    if len(pairs) != 15 or any(set(value) != {12, 24} for value in pairs.values()):
        raise RuntimeError(f"Incomplete matched data for {definition['heading']} / {definition['readout']}")

    arms = ["Opaque", "Aligned", "MisIndexed"]
    keys = sorted(pairs, key=lambda key: (key[0], arms.index(key[1])))
    scale = 100.0 if definition["field"] in {"coverage", "retest"} else 1.0
    output: list[dict] = []
    for key in keys:
        row12, row24 = pairs[key][12], pairs[key][24]
        value12 = row12[definition["field"]] * scale
        value24 = row24[definition["field"]] * scale
        if definition["field"] == "mae":
            change = row12["mae"] - row24["mae"]
        else:
            change = row24[definition["field"]] - row12[definition["field"]]
        output.append(
            {
                "key": key,
                "value12": float(value12),
                "value24": float(value24),
                "change": float(change),
                "shortfall": not bool(row12["conforming"]) or not bool(row24["conforming"]),
            }
        )
    means = [float(np.mean([row[f"value{budget}"] for row in output])) for budget in (12, 24)]
    improved = sum(row["change"] > 1e-12 for row in output)
    return output, means, improved


def style_axis(ax: plt.Axes) -> None:
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(axis="both", colors=INK, width=0.8, length=3.0, direction="out")


def format_mean(value: float, field: str) -> str:
    return f"{value:.1f}%" if field in {"coverage", "retest"} else f"{value:.3f}"


def save(fig: plt.Figure) -> None:
    OUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_STEM.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(OUT_STEM.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUT_STEM.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(
        OUT_STEM.with_suffix(".tiff"),
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )


def render() -> None:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.25))
    fig.subplots_adjust(left=0.072, right=0.995, top=0.94, bottom=0.14, wspace=0.38, hspace=0.51)
    jitter = np.asarray([-0.105, -0.075, -0.045, -0.015, 0.015, 0.045, 0.075, 0.105, -0.090, -0.060, -0.030, 0.030, 0.060, 0.090, 0.0])

    for index, (ax, definition) in enumerate(zip(axes.flat, DEFINITIONS)):
        records, means, improved = load_pairs(data, definition)
        exp12, exp24, exp_improved = definition["expected"]
        expected_means = [exp12, exp24]
        if definition["field"] == "retest":
            expected_means = [100.0 * exp12, 100.0 * exp24]
        tolerance = 0.11 if definition["field"] in {"coverage", "retest"} else 6e-5
        if any(abs(actual - expected) > tolerance for actual, expected in zip(means, expected_means)) or improved != exp_improved:
            raise RuntimeError(f"Retained values changed for {definition['heading']} / {definition['readout']}")

        values12 = [record["value12"] for record in records]
        values24 = [record["value24"] for record in records]
        raw_values = [*values12, *values24]
        y0, y1 = definition["ylim"]
        if min(raw_values) < y0 or max(raw_values) > y1:
            raise RuntimeError(f"Axis would clip retained data for {definition['heading']} / {definition['readout']}")

        boxes = ax.boxplot(
            [values12, values24],
            positions=[0, 1],
            widths=0.46,
            patch_artist=True,
            showfliers=False,
            whis=1.5,
            boxprops={"edgecolor": BOX_EDGE, "linewidth": 0.85},
            medianprops={"color": INK, "linewidth": 1.15},
            whiskerprops={"color": BOX_EDGE, "linewidth": 0.8},
            capprops={"color": BOX_EDGE, "linewidth": 0.8},
            zorder=1,
        )
        for patch, color in zip(boxes["boxes"], [BOX_12, BOX_24]):
            patch.set_facecolor(color)
            patch.set_alpha(0.80)

        for pair_index, record in enumerate(records):
            x12, x24 = 0 + jitter[pair_index], 1 + jitter[pair_index]
            if record["shortfall"]:
                line_color, line_alpha, line_style = SHORTFALL, 0.35, "--"
            else:
                line_color = FAVORABLE if record["change"] > 1e-12 else UNFAVORABLE if record["change"] < -1e-12 else SHORTFALL
                line_alpha, line_style = 0.18, "-"
            ax.plot(
                [x12, x24],
                [record["value12"], record["value24"]],
                color=line_color,
                alpha=line_alpha,
                lw=0.65,
                ls=line_style,
                zorder=2,
                clip_on=True,
            )
            if record["shortfall"]:
                ax.scatter(
                    [x12, x24],
                    [record["value12"], record["value24"]],
                    marker="x",
                    s=28,
                    linewidths=1.0,
                    color=SHORTFALL,
                    zorder=4,
                    clip_on=False,
                )
            else:
                ax.scatter(
                    [x12, x24],
                    [record["value12"], record["value24"]],
                    s=17,
                    color=line_color,
                    edgecolor="white",
                    linewidth=0.3,
                    zorder=4,
                    clip_on=False,
                )

        panel = chr(ord("a") + index)
        ax.text(-0.22, 1.13, panel, transform=ax.transAxes, fontsize=9.0, fontweight="bold", color=INK)
        ax.text(0.50, 1.14, definition["heading"], transform=ax.transAxes, ha="center", va="bottom", fontsize=7.7, fontweight="bold", color=INK)
        summary = (
            f"Mean: {format_mean(means[0], definition['field'])} → "
            f"{format_mean(means[1], definition['field'])}; improved in {improved}/15 pairs"
        )
        ax.text(0.50, 1.045, summary, transform=ax.transAxes, ha="center", va="bottom", fontsize=6.2, color=INK)

        ax.set_xlim(-0.43, 1.43)
        ax.set_ylim(*definition["ylim"])
        ax.set_yticks(definition["yticks"])
        ax.set_xticks([0, 1], ["12", "24"])
        ax.set_xlabel("Batches", labelpad=3.0, color=INK)
        ax.set_ylabel(definition["ylabel"], color=INK)
        style_axis(ax)

    handles = [
        Line2D([], [], color=FAVORABLE, alpha=0.45, lw=0.8, marker="o", markerfacecolor=FAVORABLE, markeredgecolor="white", markeredgewidth=0.3, markersize=4.5, label="Favorable pair"),
        Line2D([], [], color=UNFAVORABLE, alpha=0.45, lw=0.8, marker="o", markerfacecolor=UNFAVORABLE, markeredgecolor="white", markeredgewidth=0.3, markersize=4.5, label="Unfavorable pair"),
        Line2D([], [], color=SHORTFALL, lw=0, marker="x", markersize=5.0, label="Source-assay shortfall"),
    ]
    legend = fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.025),
        ncol=3,
        frameon=False,
        columnspacing=2.2,
        handletextpad=0.6,
        fontsize=6.5,
    )
    for text in legend.get_texts():
        text.set_color(INK)

    save(fig)
    plt.close(fig)
    print(OUT_STEM.relative_to(ROOT).with_suffix(".png"))
    print("Verified 6 panels x 15 matched real-data pairs; boxes include all observations; no inferential annotations.")


if __name__ == "__main__":
    configure()
    render()
