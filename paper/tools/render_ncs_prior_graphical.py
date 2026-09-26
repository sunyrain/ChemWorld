"""Render NCS prior supplementary figures from retained campaign values."""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from ncs_figure_style import ARM_COLORS as COLORS
from ncs_figure_style import ARMS

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "paper/figures/academic-ppt/retained-figure-data.json"
OUT = ROOT / "paper/figures/venue-results"
INK, MUTED, GRID, TRACK = "#24292D", "#6A737B", "#D7DDE1", "#EEF1F3"

plt.rcParams.update(
    {
        "font.family": "Arial",
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "pdf.fonttype": 42,
    }
)

PRIOR = [
    ("EC", "E", "discovery", 12, "score", "Electrochemistry / discovery / 12", "Score MAE"),
    ("EC", "E", "discovery", 24, "score", "Electrochemistry / discovery / 24", "Score MAE"),
    ("EC", "E", "optimization", 12, "score", "Electrochemistry / optimization / 12", "Score MAE"),
    ("EC", "E", "optimization", 24, "score", "Electrochemistry / optimization / 24", "Score MAE"),
    ("PA", "E", "discovery", 12, "product_in_organic", "Partitioning / 12", "Organic-fraction MAE"),
    ("PA", "E", "discovery", 24, "product_in_organic", "Partitioning / 24", "Organic-fraction MAE"),
    ("RX", "P", "discovery", 12, "macro", "Reaction / parameter / discovery", "Macro MAE"),
    ("RX", "S", "discovery", 12, "macro", "Reaction / structural / discovery", "Macro MAE"),
    ("RX", "P", "optimization", 12, "macro", "Reaction / parameter / optimization", "Macro MAE"),
    ("RX", "S", "optimization", 12, "macro", "Reaction / structural / optimization", "Macro MAE"),
    ("EQ", "P", "characterization", 12, "macro", "Equilibrium / parameter", "Macro MAE"),
    ("EQ", "S", "characterization", 12, "macro", "Equilibrium / structural", "Macro MAE"),
    ("C", "E", "delivery", 12, "crystal_fines_fraction", "Crystallization / 12", "Fines MAE"),
    ("C", "E", "delivery", 24, "crystal_fines_fraction", "Crystallization / 24", "Fines MAE"),
    ("P", "E", "delivery", 12, "purity", "Purification / purity", "Purity MAE"),
    ("P", "E", "delivery", 12, "recovery", "Purification / recovery", "Recovery MAE"),
]


def load() -> dict:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert len(data["macro_campaigns"]) == 240
    assert len(data["regimes"]["cells"]) == 15
    return data


def rows_for(data: dict, definition: tuple) -> list[dict]:
    system, locus, goal, budget, metric, *_ = definition
    pool = data["macro_campaigns"] if metric == "macro" else data["campaigns"]
    rows = [
        r for r in pool
        if (r["system"], r["locus"], r["goal"], r["budget"], r["metric"])
        == (system, locus, goal, budget, metric)
    ]
    assert len(rows) == 15 and len({r["id"] for r in rows}) == 15
    assert all(sum(r["arm"] == arm for r in rows) == 5 for arm in ARMS)
    return rows


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{name}.pdf"
    fig.savefig(target, format="pdf", facecolor="white")
    plt.close(fig)
    print(f"prior stage=render output={target.relative_to(ROOT)}", flush=True)


def group_limit(data: dict, index: int) -> float:
    if index < 4:
        group = PRIOR[:4]
    elif index < 6:
        group = PRIOR[4:6]
    elif index < 10:
        group = PRIOR[6:10]
    elif index < 12:
        group = PRIOR[10:12]
    elif index < 14:
        group = PRIOR[12:14]
    else:
        group = PRIOR[index:index + 1]
    maximum = max(r["mae"] for definition in group for r in rows_for(data, definition))
    return math.ceil(maximum * 1.04 * 100) / 100


def graphical_panel(ax, data: dict, index: int) -> None:
    definition = PRIOR[index]
    rows = rows_for(data, definition)
    _, _, _, _, _, title, metric_name = definition
    limit = group_limit(data, index)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.005, 0.93, chr(97 + index), fontsize=12, weight="bold", va="center")
    ax.text(0.055, 0.93, title, fontsize=9.2, weight="bold", va="center")
    ax.text(0.985, 0.93, f"{metric_name}  0-{limit:.2f}", fontsize=8,
            color=MUTED, va="center", ha="right")
    x_starts = (0.155, 0.435, 0.715)
    bar_width = 0.175
    names = ("Opaque", "Aligned", "MisIndexed")
    for x, arm in zip(x_starts, names, strict=True):
        ax.text(x, 0.795, arm, fontsize=8.3, weight="bold", va="center")
        ax.plot([x, x + 0.248], [0.756, 0.756], color=COLORS[arm], lw=1.3)
    worlds = sorted({r["world"] for r in rows})
    assert len(worlds) == 5
    y_values = (0.66, 0.55, 0.44, 0.33, 0.22, 0.075)
    for row_index, y in enumerate(y_values):
        is_mean = row_index == 5
        ax.text(0.015, y, "Mean" if is_mean else f"W{row_index + 1:02d}",
                fontsize=8.4, weight="bold" if is_mean else "normal", va="center")
        if is_mean:
            ax.plot([0.005, 0.99], [0.157, 0.157], color=GRID, lw=0.8)
        for x, arm in zip(x_starts, ARMS, strict=True):
            subset = [r for r in rows if r["arm"] == arm]
            value = (fmean(r["mae"] for r in subset) if is_mean else
                     next(r["mae"] for r in subset if r["world"] == worlds[row_index]))
            conforming = (True if is_mean else
                          next(r["conforming"] for r in subset if r["world"] == worlds[row_index]))
            ax.add_patch(Rectangle((x, y - 0.022), bar_width, 0.044,
                                   facecolor=TRACK, edgecolor="none"))
            ax.add_patch(Rectangle((x, y - 0.022), bar_width * value / limit, 0.044,
                                   facecolor=COLORS[arm], edgecolor="none"))
            ax.text(x + bar_width + 0.006, y, f"{value:.4f}", fontsize=7.65,
                    va="center", color=INK, weight="bold" if is_mean else "normal")
            if not conforming:
                ax.text(x + bar_width - 0.005, y + 0.034, "x", fontsize=10,
                        color=INK, ha="right", va="center", weight="bold")


def render_s1(data: dict) -> None:
    for page in range(4):
        fig, axes = plt.subplots(4, 1, figsize=(7.1, 8.35))
        fig.subplots_adjust(left=0.06, right=0.99, top=0.985, bottom=0.035,
                            hspace=0.12)
        for offset, ax in enumerate(axes):
            graphical_panel(ax, data, page * 4 + offset)
        save(fig, f"figureS1-prior-graphical-table-{page + 1}")


def rx_pairs(data: dict, goal: str) -> list[tuple[str, float, float, float]]:
    rows = rows_for(data, ("RX", "P", goal, 12, "macro", "", ""))
    values = []
    for world in sorted({r["world"] for r in rows}):
        arm_values = {arm: next(r["mae"] for r in rows if r["world"] == world and r["arm"] == arm)
                      for arm in ARMS}
        values.append((world.split("-")[-1], arm_values["Opaque"],
                       arm_values["Aligned"] - arm_values["Opaque"],
                       arm_values["MisIndexed"] - arm_values["Opaque"]))
    assert sum(row[2] < 0 for row in values) == 4
    return values


def eq_pairs(data: dict, group: str, field: str) -> list[tuple[str, float, float, float]]:
    cells = data["regimes"]["cells"]
    scale = 100 if field == "coverage" else 1
    values = []
    for world in sorted({r["world"] for r in cells}):
        arm_values = {
            arm: next(r["groups"][group][field] * scale for r in cells
                      if r["world"] == world and r["arm"] == arm)
            for arm in ARMS
        }
        values.append((world, arm_values["Opaque"],
                       arm_values["Aligned"] - arm_values["Opaque"],
                       arm_values["MisIndexed"] - arm_values["Opaque"]))
    if field == "mae":
        assert all((row[2] < 0) == (group == "other_nine") for row in values)
    return values


def delta_panel(ax, values: list[tuple[str, float, float, float]], panel_id: str,
                title: str, field: str) -> None:
    assert len(values) == 5
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.set_facecolor("white")
    ax.axvline(0, color=INK, lw=0.85, zorder=0)
    ys = list(range(5, 0, -1))
    for y, (_, _, aligned, misindexed) in zip(ys, values, strict=True):
        ax.plot(aligned, y + 0.12, marker="D", color=COLORS["Aligned"], ms=5,
                linestyle="none", zorder=3)
        ax.plot(misindexed, y - 0.12, marker="o", color=COLORS["MisIndexed"], ms=5,
                linestyle="none", zorder=3)
    mean_a = fmean(row[2] for row in values)
    mean_m = fmean(row[3] for row in values)
    ax.axhline(0.48, color=GRID, lw=0.8)
    ax.plot(mean_a, 0.16, marker="D", color=COLORS["Aligned"], ms=5.5)
    ax.plot(mean_m, -0.06, marker="o", color=COLORS["MisIndexed"], ms=5.5)
    fmt = (lambda v: f"{v:.1f}") if field == "coverage" else (lambda v: f"{v:.4f}")
    labels = [f"{world}   {fmt(opaque)}" for world, opaque, *_ in values]
    ax.set_yticks([*ys, 0.05], labels=[*labels, "Mean"])
    ax.tick_params(axis="y", length=0, pad=5)
    ax.tick_params(axis="x", length=3, pad=3)
    ax.set_ylim(-0.4, 5.7)
    diffs = [item for row in values for item in row[2:]]
    low, high = min([*diffs, 0]), max([*diffs, 0])
    pad = max((high - low) * 0.15, 0.002 if field == "mae" else 1.5)
    ax.set_xlim(low - pad, high + pad)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.text(-0.14, 1.13, panel_id, transform=ax.transAxes, fontsize=12, weight="bold")
    ax.set_title(title, loc="left", fontsize=9.5, pad=27, weight="bold")
    ax.text(-0.02, 1.055, f"World    Opaque {field if field == 'mae' else 'coverage (%)'}",
            transform=ax.transAxes, fontsize=7.6, color=MUTED)
    ax.set_xlabel("Δ coverage vs Opaque (pp)" if field == "coverage" else
                  "Δ MAE vs Opaque", fontsize=8.5)


def delta_legend(fig, y: float) -> None:
    fig.legend(
        handles=[
            Line2D([0], [0], marker="D", linestyle="none", color=COLORS["Aligned"],
                   markersize=5, label="Aligned - Opaque"),
            Line2D([0], [0], marker="o", linestyle="none", color=COLORS["MisIndexed"],
                   markersize=5, label="MisIndexed - Opaque"),
        ],
        loc="lower center", bbox_to_anchor=(0.5, y), ncol=2,
        frameon=False, fontsize=8.5, columnspacing=1.4,
    )


def render_s2(data: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 5.6))
    fig.subplots_adjust(left=0.16, right=0.99, top=0.82, bottom=0.18, wspace=0.36)
    for i, goal in enumerate(("discovery", "optimization")):
        delta_panel(axes[i], rx_pairs(data, goal), chr(97 + i),
                    f"Reaction / {goal}", "mae")
    delta_legend(fig, 0.01)
    save(fig, "figureS2-prior-difference-reaction")

    panels = [
        ("other_nine", "mae", "Other nine / macro MAE"),
        ("three_most_dilute", "mae", "Dilute three / macro MAE"),
        ("other_nine", "coverage", "Other nine / interval coverage"),
        ("three_most_dilute", "coverage", "Dilute three / interval coverage"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 7.55))
    fig.subplots_adjust(left=0.18, right=0.985, top=0.90, bottom=0.115,
                        wspace=0.38, hspace=0.53)
    for i, (ax, (group, field, title)) in enumerate(zip(axes.flat, panels, strict=True)):
        delta_panel(ax, eq_pairs(data, group, field), chr(99 + i), title, field)
    delta_legend(fig, 0.012)
    save(fig, "figureS2-prior-difference-equilibrium")


def main() -> None:
    data = load()
    render_s1(data)
    render_s2(data)


if __name__ == "__main__":
    main()
