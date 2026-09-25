#!/usr/bin/env python3
"""Render a real-data Figure 5 candidate for equilibrium regime failure.

Panels a and b show retained aggregate results and all five world-level values
for each information arm. Panel c shows the withheld Q08 reference and the
three original point predictions in each world. The horizontal band is the
pooled range of all 180 retained source assays, not an uncertainty interval.
No observations are sampled, imputed, or excluded.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "paper/figures/academic-ppt/retained-figure-data.json"
OUT_STEM = ROOT / "paper/figures/venue-results/figure05-regime-bars-reference-style"
SOURCE_DATA = OUT_STEM.with_name(f"{OUT_STEM.name}-source-data.csv")
PRODUCTION_PNG = ROOT / "paper/figures/final-ppt/figure05-eq-evidence.png"

INK = "#111111"
REFERENCE = "#CBD5DC"
RESEARCH_BAND = "#E9EDEF"
ARM_COLORS = {
    "Opaque": "#637482",
    "Aligned": "#277F8A",
    "MisIndexed": "#BC7850",
}
ARMS = ("Opaque", "Aligned", "MisIndexed")
GROUPS = ("other_nine", "three_most_dilute")
GROUP_LABELS = ("Other nine", "Dilute three")

EXPECTED = {
    ("Opaque", "other_nine", "mae"): 0.010076250577326171,
    ("Aligned", "other_nine", "mae"): 0.004647301928643827,
    ("MisIndexed", "other_nine", "mae"): 0.004389850205011723,
    ("Opaque", "three_most_dilute", "mae"): 0.01833210026545114,
    ("Aligned", "three_most_dilute", "mae"): 0.15862426151816295,
    ("MisIndexed", "three_most_dilute", "mae"): 0.14396808374038517,
    ("Opaque", "other_nine", "coverage"): 0.9066666666666666,
    ("Aligned", "other_nine", "coverage"): 0.9125925925925926,
    ("MisIndexed", "other_nine", "coverage"): 0.8962962962962961,
    ("Opaque", "three_most_dilute", "coverage"): 0.9333333333333333,
    ("Aligned", "three_most_dilute", "coverage"): 0.02222222222222222,
    ("MisIndexed", "three_most_dilute", "coverage"): 0.13777777777777778,
}


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.0,
            "axes.labelsize": 7.0,
            "axes.titlesize": 8.0,
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


def clean_axis(ax: plt.Axes) -> None:
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(axis="both", colors=INK, width=0.8, length=3.0, direction="out")


def rgba(hex_color: str, alpha: float = 0.84) -> tuple[float, float, float, float]:
    red, green, blue = to_rgb(hex_color)
    return red, green, blue, alpha


def regime_lookup(data: dict) -> tuple[dict[tuple[str, str], dict], dict[tuple[str, str], dict]]:
    aggregate = {
        (row["arm"], row["group"]): row
        for row in data["regimes"]["aggregate"]
    }
    cells = {
        (row["world"], row["arm"]): row
        for row in data["regimes"]["cells"]
    }
    if len(aggregate) != 6 or len(cells) != 15:
        raise RuntimeError("Figure 5 requires 6 aggregates and 15 world-arm cells")
    for (arm, group, metric), expected in EXPECTED.items():
        actual = float(aggregate[(arm, group)][metric])
        if abs(actual - expected) > 1e-12:
            raise RuntimeError(f"Retained regime value changed: {arm} / {group} / {metric}")
        world_values = [float(cells[(f"W{world:02d}", arm)]["groups"][group][metric]) for world in range(1, 6)]
        if abs(float(np.mean(world_values)) - actual) > 1e-12:
            raise RuntimeError(f"World-level values do not reproduce aggregate: {arm} / {group} / {metric}")
    return aggregate, cells


def draw_regime_panel(
    ax: plt.Axes,
    aggregate: dict,
    cells: dict,
    *,
    metric: str,
    scale: float,
    title: str,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
    panel: str,
) -> list[dict]:
    x = np.arange(2, dtype=float)
    width = 0.22
    offsets = (-width, 0.0, width)
    exported: list[dict] = []

    for offset, arm in zip(offsets, ARMS):
        means = [float(aggregate[(arm, group)][metric]) * scale for group in GROUPS]
        bars = ax.bar(
            x + offset,
            means,
            width=width * 0.91,
            color=rgba(ARM_COLORS[arm], 0.92),
            edgecolor="none",
            zorder=2,
        )
        for group_index, group in enumerate(GROUPS):
            world_values = [
                float(cells[(f"W{world:02d}", arm)]["groups"][group][metric]) * scale
                for world in range(1, 6)
            ]
            label = f"{means[group_index]:.4f}" if metric == "mae" else f"{means[group_index]:.1f}"
            label_y = means[group_index] + (0.0043 if metric == "mae" else 2.2)
            ax.text(
                bars[group_index].get_x() + bars[group_index].get_width() / 2,
                label_y,
                label,
                ha="center",
                va="bottom",
                fontsize=6.2,
                color=INK,
                clip_on=False,
            )
            for world, value in enumerate(world_values, start=1):
                exported.append(
                    {
                        "panel": panel,
                        "regime_or_world": GROUP_LABELS[group_index],
                        "arm_or_series": arm,
                        "replicate_world": f"W{world:02d}",
                        "value": value,
                        "aggregate_mean": means[group_index],
                        "unit": "fraction" if metric == "mae" else "%",
                    }
                )

    if metric == "coverage":
        ax.axhline(80.0, color="#46535B", linewidth=0.75, linestyle=(0, (4, 3)), zorder=1)
        ax.text(1.47, 81.7, "Nominal 80%", ha="right", va="bottom", fontsize=6.2, color=INK)

    ax.set_xlim(-0.48, 1.48)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_xticks(x, GROUP_LABELS)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=10.0, fontweight="bold")
    ax.text(-0.20, 1.13, panel, transform=ax.transAxes, fontsize=9.0, fontweight="bold", color=INK)
    clean_axis(ax)
    return exported


def extract_world_panel(data: dict) -> tuple[list[float], dict[str, list[float]], float, float]:
    rows = data["eq_process"]
    if len(rows) != 15 or sum(len(row["batches"]) for row in rows) != 180:
        raise RuntimeError("Figure 5 requires 15 campaigns and 180 retained source assays")

    source_observations = [
        100.0 * float(batch["final_responses"]["acid_dissociation_fraction"])
        for row in rows
        for batch in row["batches"]
    ]
    low, high = min(source_observations), max(source_observations)
    if not (5.4 < low < 5.6 and 9.1 < high < 9.3):
        raise RuntimeError("Unexpected source-observation range")

    references: list[float] = []
    predictions = {arm: [] for arm in ARMS}
    for world in range(1, 6):
        world_name = f"W{world:02d}"
        world_rows = [row for row in rows if row["world"] == world_name]
        if len(world_rows) != 3:
            raise RuntimeError(f"Incomplete world panel: {world_name}")
        reference_values = {
            float(row["q08"]["reference_means"]["acid_dissociation_fraction"])
            for row in world_rows
        }
        if len(reference_values) != 1:
            raise RuntimeError(f"Reference mismatch in {world_name}")
        references.append(100.0 * reference_values.pop())
        for arm in ARMS:
            row = next(item for item in world_rows if item["arm"] == arm)
            predictions[arm].append(
                100.0 * float(row["q08"]["predictions"]["acid_dissociation_fraction"]["estimate"])
            )
    return references, predictions, low, high


def draw_world_panel(
    ax: plt.Axes,
    references: list[float],
    predictions: dict[str, list[float]],
    low: float,
    high: float,
) -> list[dict]:
    worlds = [f"World {world}" for world in range(1, 6)]
    x = np.arange(5, dtype=float)
    width = 0.18
    offsets = np.asarray([-1.5, -0.5, 0.5, 1.5]) * width
    groups = [
        ("Withheld reference", references, REFERENCE),
        ("Opaque", predictions["Opaque"], ARM_COLORS["Opaque"]),
        ("Aligned", predictions["Aligned"], ARM_COLORS["Aligned"]),
        ("MisIndexed", predictions["MisIndexed"], ARM_COLORS["MisIndexed"]),
    ]
    exported: list[dict] = []

    ax.axhspan(low, high, color=RESEARCH_BAND, zorder=0)
    for offset, (label, values, color) in zip(offsets, groups):
        bars = ax.bar(
            x + offset,
            values,
            width=width,
            color=rgba(color, 0.92),
            edgecolor="none",
            zorder=2,
        )
        for world_index, (bar, value) in enumerate(zip(bars, values), start=1):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 1.35,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=6.0,
                color=INK,
                clip_on=False,
            )
            exported.append(
                {
                    "panel": "c",
                    "regime_or_world": f"World {world_index}",
                    "arm_or_series": label,
                    "replicate_world": "",
                    "value": value,
                    "aggregate_mean": "",
                    "unit": "%",
                }
            )

    band_mid = (low + high) / 2.0
    ax.plot([4.41, 4.53], [band_mid, band_mid], color="#56636B", linewidth=0.65, zorder=3)
    ax.text(
        4.56,
        high + 1.25,
        f"Source observations\n{low:.1f}–{high:.1f}%",
        ha="left",
        va="bottom",
        fontsize=6.0,
        color=INK,
    )

    ax.set_xlim(-0.52, 4.86)
    ax.set_ylim(0.0, 82.0)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xticks(x, worlds)
    ax.set_ylabel("Dissociation (%)")
    ax.set_title("Same dilute recipe across five worlds", pad=10.0, fontweight="bold")
    ax.text(-0.075, 1.13, "c", transform=ax.transAxes, fontsize=9.0, fontweight="bold", color=INK)
    clean_axis(ax)
    return exported


def save_all(fig: plt.Figure) -> None:
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
    PRODUCTION_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PRODUCTION_PNG, dpi=600, bbox_inches="tight")


def render() -> None:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    aggregate, cells = regime_lookup(data)
    references, predictions, low, high = extract_world_panel(data)

    fig = plt.figure(figsize=(7.2, 5.25))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.075,
        right=0.985,
        bottom=0.145,
        top=0.94,
        wspace=0.28,
        hspace=0.58,
        height_ratios=[1.0, 1.0],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, :])

    source_rows: list[dict] = []
    source_rows.extend(
        draw_regime_panel(
            ax_a,
            aggregate,
            cells,
            metric="mae",
            scale=1.0,
            title="Prediction error across regimes",
            ylabel="Macro MAE",
            ylim=(0.0, 0.205),
            yticks=[0.00, 0.05, 0.10, 0.15, 0.20],
            panel="a",
        )
    )
    source_rows.extend(
        draw_regime_panel(
            ax_b,
            aggregate,
            cells,
            metric="coverage",
            scale=100.0,
            title="Interval coverage across regimes",
            ylabel="80% interval coverage (%)",
            ylim=(0.0, 100.0),
            yticks=[0, 20, 40, 60, 80, 100],
            panel="b",
        )
    )
    source_rows.extend(draw_world_panel(ax_c, references, predictions, low, high))

    handles = [
        Patch(facecolor=rgba(REFERENCE, 0.92), edgecolor="none", label="Withheld reference"),
        *[
            Patch(
                facecolor=rgba(ARM_COLORS[arm], 0.92),
                edgecolor="none",
                label=arm,
            )
            for arm in ARMS
        ],
    ]
    legend = fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.53, 0.025),
        ncol=4,
        frameon=False,
        columnspacing=2.2,
        handlelength=1.1,
        handletextpad=0.55,
        fontsize=6.5,
    )
    for text in legend.get_texts():
        text.set_color(INK)

    with SOURCE_DATA.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(source_rows[0]))
        writer.writeheader()
        writer.writerows(source_rows)

    save_all(fig)
    plt.close(fig)
    print(OUT_STEM.relative_to(ROOT).with_suffix(".png"))
    print(SOURCE_DATA.relative_to(ROOT))
    print("Verified: 15 regime cells, 6 retained aggregates, 15 Q08 campaigns, and 180 source assays.")


if __name__ == "__main__":
    configure()
    render()
