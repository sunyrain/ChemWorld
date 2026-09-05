#!/usr/bin/env python3
"""Render the prior-correction manuscript figures."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

COLORS = {
    "ink": "#263238",
    "muted": "#667780",
    "grid": "#DCE4E8",
    "paper": "#FFFFFF",
    "opaque": "#A8B4BA",
    "aligned": "#2A9D8F",
    "misindexed": "#DD8D24",
    "blue": "#356A94",
    "blue_light": "#DCEAF4",
    "teal_light": "#DDF2EE",
    "orange_light": "#F9E8CE",
    "red": "#C95353",
    "red_light": "#F5DDDD",
    "green": "#5A9C70",
    "green_light": "#E1F0E5",
    "violet": "#7B6CAD",
    "violet_light": "#E8E3F3",
}

TASK_ORDER = [
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
]
TASK_LABEL = {
    "electrochemical-conversion": "Electrochemical\nconversion",
    "reaction-to-crystallization": "Reaction to\ncrystallization",
    "reaction-to-distillation": "Reaction to\ndistillation",
}
FULL_TASK_ORDER = [
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
]
FULL_TASK_LABEL = {
    "electrochemical-conversion": "Electrochemical",
    "reaction-to-crystallization": "Crystallization",
    "reaction-to-distillation": "Distillation",
    "partition-discovery": "Partition",
    "reaction-safety-constrained": "Safety constrained",
}
FULL_TASK_COLOR = {
    "electrochemical-conversion": "#477AA5",
    "reaction-to-crystallization": "#6F62A6",
    "reaction-to-distillation": "#4F9785",
    "partition-discovery": "#D18B3E",
    "reaction-safety-constrained": "#B85C62",
}
ARM_ORDER = ["opaque", "aligned_nominal", "misindexed_nominal"]
ARM_LABEL = {
    "opaque": "Opaque",
    "aligned_nominal": "Aligned",
    "misindexed_nominal": "Misindexed",
}
ARM_COLOR = {
    "opaque": COLORS["opaque"],
    "aligned_nominal": COLORS["aligned"],
    "misindexed_nominal": COLORS["misindexed"],
}
ROW_TASK_LABEL = {
    "electrochemical-conversion": "Electro",
    "reaction-to-crystallization": "Crystal",
    "reaction-to-distillation": "Distill",
    "reaction-safety-constrained": "Safety",
}


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").is_file() and (candidate / "workstreams").is_dir():
            return candidate
    raise RuntimeError("could not locate repository root")


SCRIPT_PATH = Path(__file__).resolve()
ROOT = find_repo_root(SCRIPT_PATH.parent)
OUTPUT_DIR = SCRIPT_PATH.parent
SOURCE_DIR = OUTPUT_DIR / "source_data"


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.4,
            "axes.titlesize": 9.2,
            "axes.labelsize": 8.2,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.75,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "chemworld-prior-discovery-figures",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def export_figure(fig: mpl.figure.Figure, stem: str) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OUTPUT_DIR / f"{stem}.svg"
    pdf_path = OUTPUT_DIR / f"{stem}.pdf"
    png_path = OUTPUT_DIR / f"{stem}.png"
    tiff_path = OUTPUT_DIR / f"{stem}.tiff"
    fig.savefig(svg_path, bbox_inches="tight", metadata={"Date": None})
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    fig.savefig(
        pdf_path,
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    fig.savefig(
        tiff_path,
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)
    return [svg_path, pdf_path, png_path, tiff_path]


def panel_label(ax: mpl.axes.Axes, label: str, x: float = -0.04, y: float = 1.03) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["ink"],
    )


def rounded_box(
    ax: mpl.axes.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    *,
    facecolor: str,
    edgecolor: str,
    fontsize: float = 7.0,
    fontweight: str = "normal",
    text_color: str | None = None,
    radius: float = 0.025,
    linewidth: float = 1.0,
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=fontweight,
        color=text_color or COLORS["ink"],
        linespacing=1.16,
    )
    return patch


def arrow(
    ax: mpl.axes.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = COLORS["muted"],
    width: float = 1.1,
    connectionstyle: str = "arc3",
    mutation_scale: float = 9,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=mutation_scale,
            linewidth=width,
            color=color,
            connectionstyle=connectionstyle,
            shrinkA=2,
            shrinkB=2,
        )
    )


def setup_schematic_ax(ax: mpl.axes.Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def render_figure_1() -> list[Path]:
    fig = plt.figure(figsize=(7.2, 4.65))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.045,
        right=0.985,
        bottom=0.08,
        top=0.86,
        wspace=0.16,
        hspace=0.28,
        width_ratios=[1.05, 0.95],
    )
    axes = [fig.add_subplot(grid[row, col]) for row in range(2) for col in range(2)]
    for ax in axes:
        setup_schematic_ax(ax)
    ax_a, ax_b, ax_c, ax_d = axes

    # a — matched initial-world-model intervention
    ax_a.set_title(
        "Vary the supplied description; keep the world fixed", loc="left", fontweight="bold", pad=5
    )
    ax_a.text(
        0.50,
        0.95,
        "Target locus: entity · structure · dynamics · observation · scope",
        ha="center",
        va="center",
        fontsize=5.8,
        color=COLORS["muted"],
    )
    arm_specs = [
        ("Opaque", "No claim at the\ntarget locus", COLORS["opaque"], "#EEF1F2"),
        ("Aligned", "Matched model\nconsistent with W", COLORS["aligned"], COLORS["teal_light"]),
        (
            "Misspecified",
            "Matched model\nwrong at one locus",
            COLORS["misindexed"],
            COLORS["orange_light"],
        ),
    ]
    for index, (name, detail, edge, face) in enumerate(arm_specs):
        x = 0.02 + index * 0.325
        rounded_box(
            ax_a,
            x,
            0.58,
            0.285,
            0.25,
            f"{name}\n{detail}",
            facecolor=face,
            edgecolor=edge,
            fontsize=6.6,
            fontweight="bold" if index else "normal",
        )
        arrow(ax_a, (x + 0.142, 0.57), (0.50, 0.40), color=edge)
    rounded_box(
        ax_a,
        0.22,
        0.14,
        0.56,
        0.23,
        "One fixed executable chemical world\n"
        "Matched operations, evidence budget, noise and safety",
        facecolor=COLORS["blue_light"],
        edgecolor=COLORS["blue"],
        fontsize=7.1,
        fontweight="bold",
    )
    ax_a.text(
        0.50,
        0.045,
        "One prespecified component of M0 changes; W and the public contract stay fixed",
        ha="center",
        va="center",
        fontsize=6.8,
        color=COLORS["muted"],
    )
    panel_label(ax_a, "a")

    # b — persistent campaign loop
    ax_b.set_title("Trace one evidence-to-action trajectory", loc="left", fontweight="bold", pad=5)
    center = (0.50, 0.54)
    nodes = [
        (0.50, 0.84, "Predict\n+ confidence", COLORS["violet_light"], COLORS["violet"]),
        (0.82, 0.56, "Choose one\noperation", COLORS["teal_light"], COLORS["aligned"]),
        (0.50, 0.25, "Observe public\noutcome", COLORS["blue_light"], COLORS["blue"]),
        (0.18, 0.56, "Update belief\nand law", COLORS["orange_light"], COLORS["misindexed"]),
    ]
    for x, y, label, face, edge in nodes:
        rounded_box(
            ax_b,
            x - 0.13,
            y - 0.075,
            0.26,
            0.15,
            label,
            facecolor=face,
            edgecolor=edge,
            fontsize=6.8,
            fontweight="bold",
        )
    rounded_box(
        ax_b,
        center[0] - 0.12,
        center[1] - 0.065,
        0.24,
        0.13,
        "Shared history\nand resources",
        facecolor="#F4F6F7",
        edgecolor=COLORS["muted"],
        fontsize=6.5,
    )
    arrow(ax_b, (0.62, 0.80), (0.75, 0.65), connectionstyle="arc3,rad=-0.18")
    arrow(ax_b, (0.76, 0.48), (0.62, 0.32), connectionstyle="arc3,rad=-0.18")
    arrow(ax_b, (0.38, 0.29), (0.24, 0.47), connectionstyle="arc3,rad=-0.18")
    arrow(ax_b, (0.25, 0.65), (0.38, 0.80), connectionstyle="arc3,rad=-0.18")
    ax_b.text(
        0.50,
        0.07,
        "Intervention-specific campaign: entity 8 · parametric 10 · structural 12 experiments",
        ha="center",
        fontsize=6.6,
        color=COLORS["muted"],
    )
    panel_label(ax_b, "b")

    # c — evidence separation
    ax_c.set_title("Score outcomes after the campaign", loc="left", fontweight="bold", pad=5)
    rounded_box(
        ax_c,
        0.03,
        0.58,
        0.38,
        0.28,
        "Participant trajectory\noperations · evidence\ncheckpoints",
        facecolor=COLORS["teal_light"],
        edgecolor=COLORS["aligned"],
        fontsize=6.1,
        fontweight="normal",
    )
    rounded_box(
        ax_c,
        0.59,
        0.58,
        0.38,
        0.28,
        "Evaluator truth\nheld-out queries\nno feedback",
        facecolor=COLORS["blue_light"],
        edgecolor=COLORS["blue"],
        fontsize=6.1,
        fontweight="normal",
    )
    rounded_box(
        ax_c,
        0.20,
        0.17,
        0.60,
        0.23,
        "Join only after execution\nprediction error · calibration\nblind recommendation",
        facecolor="#F4F6F7",
        edgecolor=COLORS["ink"],
        fontsize=6.1,
        fontweight="normal",
    )
    arrow(ax_c, (0.22, 0.56), (0.38, 0.41), color=COLORS["aligned"])
    arrow(ax_c, (0.78, 0.56), (0.62, 0.41), color=COLORS["blue"])
    ax_c.text(
        0.50,
        0.06,
        "Self-report alone is never the discovery endpoint",
        ha="center",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    panel_label(ax_c, "c")

    # d — decision rule
    ax_d.set_title("Separate prediction and decision quality", loc="left", fontweight="bold", pad=5)
    x0, y0, width, height = 0.20, 0.17, 0.72, 0.66
    ax_d.add_patch(
        Rectangle((x0, y0), width, height, facecolor="none", edgecolor=COLORS["ink"], linewidth=0.9)
    )
    ax_d.plot(
        [x0 + width / 2, x0 + width / 2], [y0, y0 + height], color=COLORS["grid"], linewidth=1.0
    )
    ax_d.plot(
        [x0, x0 + width], [y0 + height / 2, y0 + height / 2], color=COLORS["grid"], linewidth=1.0
    )
    cells = [
        (x0, y0 + height / 2, COLORS["red_light"], "Accurate prediction\npoor decision"),
        (
            x0 + width / 2,
            y0 + height / 2,
            COLORS["green_light"],
            "Accurate prediction\ngood decision",
        ),
        (x0, y0, "#F0F2F3", "Poor prediction\npoor decision"),
        (x0 + width / 2, y0, COLORS["orange_light"], "Poor prediction\ngood decision"),
    ]
    for x, y, face, label in cells:
        ax_d.add_patch(Rectangle((x, y), width / 2, height / 2, facecolor=face, edgecolor="none"))
        ax_d.text(
            x + width / 4,
            y + height / 4,
            label,
            ha="center",
            va="center",
            fontsize=6.7,
            fontweight="normal",
            color=COLORS["ink"],
        )
    ax_d.text(
        0.56, 0.06, "Decision quality →", ha="center", fontsize=6.7, color=COLORS["muted"]
    )
    ax_d.text(
        0.08,
        0.50,
        "Predictive\naccuracy →",
        ha="center",
        va="center",
        fontsize=6.7,
        color=COLORS["muted"],
        rotation=90,
    )
    panel_label(ax_d, "d")

    fig.suptitle(
        "Endpoint success does not reveal what the agent learned",
        x=0.045,
        y=0.965,
        ha="left",
        fontsize=13.0,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.045,
        0.018,
        "The supplied initial description is varied under one fixed world; search, "
        "prediction, executable law and unseen-plan selection remain separate evidence "
        "channels.",
        ha="left",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-1-prior-to-law")


def render_figure_2(design: dict[str, Any], preflight: dict[str, Any]) -> list[Path]:
    expected = preflight["expected_counts"]
    if (
        len(design["tasks"]) != 5
        or expected["independent_task_world_clusters"] != 25
        or expected["participant_cells"] != 75
    ):
        raise ValueError("entity-level design inputs do not match the figure contract")

    fig = plt.figure(figsize=(7.2, 5.05))
    grid = fig.add_gridspec(
        2,
        3,
        left=0.045,
        right=0.985,
        bottom=0.085,
        top=0.87,
        wspace=0.22,
        hspace=0.31,
        height_ratios=[0.82, 1.18],
        width_ratios=[1.25, 1.0, 0.85],
    )
    ax_a = fig.add_subplot(grid[0, :])
    ax_b = fig.add_subplot(grid[1, 0])
    ax_c = fig.add_subplot(grid[1, 1])
    ax_d = fig.add_subplot(grid[1, 2])
    for ax in (ax_a, ax_b, ax_c, ax_d):
        setup_schematic_ax(ax)

    ax_a.set_title(
        "Five task families form the entity / ontology backbone",
        loc="left",
        fontweight="bold",
        pad=5,
    )
    task_colors = [
        COLORS["blue"],
        COLORS["aligned"],
        COLORS["misindexed"],
        COLORS["violet"],
        COLORS["red"],
    ]
    short_names = [
        "Electrochemical",
        "Crystallization",
        "Distillation",
        "Partition",
        "Safety-constrained",
    ]
    mechanisms = [
        "transport + selectivity",
        "reaction + solid formation",
        "reaction + phase separation",
        "liquid partition",
        "kinetics + thermal safety",
    ]
    for index, (name, mechanism, color) in enumerate(
        zip(short_names, mechanisms, task_colors, strict=True)
    ):
        x = 0.01 + index * 0.198
        rounded_box(
            ax_a,
            x,
            0.42,
            0.18,
            0.39,
            f"{name}\n{mechanism}",
            facecolor="#F7F9FA",
            edgecolor=color,
            fontsize=6.4,
            fontweight="bold",
        )
        for seed in range(5):
            ax_a.add_patch(
                Circle(
                    (x + 0.032 + seed * 0.029, 0.25),
                    0.010,
                    facecolor=color,
                    edgecolor="white",
                    linewidth=0.35,
                )
            )
        ax_a.text(
            x + 0.09, 0.13, "5 public worlds", ha="center", fontsize=6.1, color=COLORS["muted"]
        )
    ax_a.text(
        0.50,
        0.02,
        "Five independently selected public worlds per task",
        ha="center",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    panel_label(ax_a, "a", x=-0.018)

    ax_b.set_title("Sparse locus-specific blocks", loc="left", fontweight="bold", pad=5)
    block_specs = [
        ("Entity", "Entity / ontology", "5 tasks x 5 worlds", "8 experiments", COLORS["blue"]),
        (
            "Parametric",
            "Parameters / dynamics",
            "2 tasks x 5 worlds",
            "10 experiments",
            COLORS["aligned"],
        ),
        (
            "Structural",
            "Structure / mechanism",
            "2 tasks x 5 worlds",
            "12 experiments",
            COLORS["violet"],
        ),
    ]
    for index, (block, locus, coverage, campaign, color) in enumerate(block_specs):
        y = 0.74 - index * 0.25
        rounded_box(
            ax_b,
            0.02,
            y - 0.07,
            0.18,
            0.14,
            block,
            facecolor="#F7F9FA",
            edgecolor=color,
            fontsize=5.9,
            fontweight="bold",
        )
        ax_b.text(
            0.25,
            y + 0.035,
            locus,
            ha="left",
            va="center",
            fontsize=6.5,
            fontweight="bold",
            color=COLORS["ink"],
        )
        ax_b.text(
            0.25,
            y - 0.038,
            f"{coverage} · {campaign}",
            ha="left",
            va="center",
            fontsize=6.0,
            color=COLORS["muted"],
        )
        for arm_index, arm_color in enumerate(
            (COLORS["opaque"], COLORS["aligned"], COLORS["misindexed"])
        ):
            ax_b.add_patch(
                Circle(
                    (0.78 + arm_index * 0.075, y),
                    0.026,
                    facecolor=arm_color,
                    edgecolor="white",
                    linewidth=0.5,
                )
            )
    ax_b.text(
        0.855, 0.93, "opaque · aligned · wrong", ha="center", fontsize=6.2, color=COLORS["muted"]
    )
    ax_b.text(
        0.50,
        0.08,
        "Observation-model extensions require separate validation",
        ha="center",
        fontsize=5.9,
        color=COLORS["muted"],
    )
    panel_label(ax_b, "b", x=-0.10)

    ax_c.set_title("Evidence partitions", loc="left", fontweight="bold", pad=5)
    evidence_boxes = [
        (0.03, 0.73, "Free\ndiscovery", COLORS["teal_light"], COLORS["aligned"]),
        (0.63, 0.73, "Matched\nevidence", COLORS["red_light"], COLORS["red"]),
        (0.33, 0.47, "Law +\naction", COLORS["blue_light"], COLORS["blue"]),
        (0.03, 0.20, "Unseen-plan\nselection", COLORS["violet_light"], COLORS["violet"]),
        (0.63, 0.20, "Future artifact\nportability", "#F1F3F4", COLORS["muted"]),
    ]
    for x, y, label, face, edge in evidence_boxes:
        width = 0.34
        rounded_box(
            ax_c,
            x,
            y,
            width,
            0.16,
            label,
            facecolor=face,
            edgecolor=edge,
            fontsize=6.1,
            fontweight="bold",
        )
    arrow(
        ax_c, (0.20, 0.71), (0.43, 0.64), color=COLORS["aligned"], connectionstyle="arc3,rad=-0.1"
    )
    arrow(ax_c, (0.80, 0.71), (0.57, 0.64), color=COLORS["red"], connectionstyle="arc3,rad=0.1")
    arrow(ax_c, (0.43, 0.46), (0.20, 0.37), color=COLORS["violet"], connectionstyle="arc3,rad=0.1")
    ax_c.text(
        0.50,
        0.10,
        "Evaluator outcomes remain hidden during each session",
        ha="center",
        fontsize=6.2,
        color=COLORS["muted"],
    )
    panel_label(ax_c, "c", x=-0.10)

    ax_d.set_title("Executed prospective denominators", loc="left", fontweight="bold", pad=5)
    denominator_rows = [
        ("Entity prospective", "25 · 75 · 600", COLORS["blue"]),
        ("Parametric", "10 · 30 · 300", COLORS["aligned"]),
        ("Structural", "10 · 30 · 360", COLORS["violet"]),
        ("Total", "45 · 135 · 1,260", COLORS["ink"]),
    ]
    for index, (label, value, color) in enumerate(denominator_rows):
        y = 0.80 - index * 0.19
        ax_d.add_patch(
            Rectangle(
                (0.05, y - 0.055), 0.90, 0.11, facecolor="#F7F9FA", edgecolor=color, linewidth=0.9
            )
        )
        ax_d.text(
            0.11,
            y,
            label,
            ha="left",
            va="center",
            fontsize=6.3,
            color=COLORS["ink"],
            fontweight="bold",
        )
        ax_d.text(
            0.91, y, value, ha="right", va="center", fontsize=6.2, color=color, fontweight="bold"
        )
    ax_d.text(
        0.07,
        0.08,
        "clusters · sessions · experiments",
        ha="left",
        fontsize=6.1,
        color=COLORS["muted"],
    )
    ax_d.text(
        0.07,
        0.035,
        "Evaluator counts follow the prespecified design",
        ha="left",
        fontsize=5.8,
        color=COLORS["muted"],
    )
    panel_label(ax_d, "d", x=-0.10)

    fig.suptitle(
        "The same causal intervention spans three scientific loci",
        x=0.045,
        y=0.965,
        ha="left",
        fontsize=13.0,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.045,
        0.018,
        "Executed prospective and matched-evidence blocks are foregrounded; private "
        "replication and context-reset portability remain future tests.",
        ha="left",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-2-formal-cohort")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_development_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    figure_source = (
        ROOT / "workstreams/flagship_tasks/reports/figures/work-ii-codex-development/source_data"
    )
    endpoint_rows: list[dict[str, Any]] = []
    warning_rows: list[dict[str, Any]] = []
    for provider_key, endpoint_name, warning_name in (
        (
            "WellAU configuration",
            "wellau_endpoint_contrasts.csv",
            "wellau_misindex_warning_rates.csv",
        ),
        (
            "DeepSeek-v4-flash configuration",
            "deepseek_recovery_endpoint_contrasts.csv",
            "deepseek_recovery_misindex_warning_rates.csv",
        ),
    ):
        for row in read_csv(figure_source / endpoint_name):
            endpoint_rows.append(
                {
                    "provider": provider_key,
                    "task_id": row["task_id"],
                    "comparison_arm": row.get("comparison_arm") or row["left_arm"],
                    "left_arm": row["left_arm"],
                    "right_arm": row["right_arm"],
                    "world_seed": int(row["world_seed"]),
                    "difference": float(row["difference"]),
                }
            )
        for row in read_csv(figure_source / warning_name):
            warning_rows.append(
                {
                    "provider": provider_key,
                    "task_id": row["task_id"],
                    "arm": row["arm"],
                    "flag_count": int(row["flag_count"]),
                    "denominator": int(row["denominator"]),
                    "flag_rate": float(row["flag_rate"]),
                }
            )
    return endpoint_rows, warning_rows


def deterministic_offsets(count: int, span: float = 0.05) -> np.ndarray:
    if count <= 1:
        return np.zeros(count)
    return np.linspace(-span, span, count)


def style_quant_axis(ax: mpl.axes.Axes) -> None:
    ax.spines["left"].set_color("#94A2AA")
    ax.spines["bottom"].set_color("#94A2AA")
    ax.tick_params(color="#94A2AA", length=3)
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.65, zorder=0)
    ax.set_axisbelow(True)


def style_row_axis(ax: mpl.axes.Axes) -> None:
    ax.spines["left"].set_color("#94A2AA")
    ax.spines["bottom"].set_color("#94A2AA")
    ax.tick_params(color="#94A2AA", length=3)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.65, zorder=0)
    ax.set_axisbelow(True)


def plot_endpoint_panel(
    ax: mpl.axes.Axes,
    rows: list[dict[str, Any]],
    provider: str,
    display_label: str,
    x_limits: tuple[float, float],
    *,
    show_y_labels: bool,
) -> None:
    selected = [row for row in rows if row["provider"] == provider]
    seed_offsets = np.linspace(-0.27, 0.27, 5)
    block_step = 1.28
    task_centers = [index * block_step for index in range(len(TASK_ORDER))]
    y_ticks: list[float] = []
    y_labels: list[str] = []

    for task_index, task in enumerate(TASK_ORDER):
        center = task_centers[task_index]
        y_by_seed = {seed: center + float(seed_offsets[seed]) for seed in range(5)}
        y_ticks.extend(y_by_seed.values())
        y_labels.extend(f"{ROW_TASK_LABEL[task]} world {seed + 1}" for seed in range(5))
        values_by_arm: dict[str, dict[int, float]] = {}
        for arm in ("aligned_nominal", "misindexed_nominal"):
            arm_rows = [
                row for row in selected if row["task_id"] == task and row["comparison_arm"] == arm
            ]
            values_by_arm[arm] = {
                int(row["world_seed"]): float(row["difference"]) for row in arm_rows
            }

        for seed in range(5):
            y = y_by_seed[seed]
            aligned_value = values_by_arm["aligned_nominal"].get(seed)
            misindexed_value = values_by_arm["misindexed_nominal"].get(seed)
            if aligned_value is not None and misindexed_value is not None:
                ax.plot(
                    [aligned_value, misindexed_value],
                    [y, y],
                    color="#C7D0D4",
                    linewidth=0.9,
                    alpha=0.9,
                    solid_capstyle="round",
                    zorder=1,
                )
            for arm, value in (
                ("aligned_nominal", aligned_value),
                ("misindexed_nominal", misindexed_value),
            ):
                if value is None:
                    continue
                ax.scatter(
                    value,
                    y,
                    s=34,
                    color=ARM_COLOR[arm],
                    alpha=0.95,
                    edgecolor="white",
                    linewidth=0.65,
                    zorder=3,
                )

        mean_y = center + 0.43
        for arm, text_offset in (
            ("aligned_nominal", -0.08),
            ("misindexed_nominal", 0.08),
        ):
            arm_values = list(values_by_arm[arm].values())
            if not arm_values:
                continue
            mean = float(np.mean(arm_values))
            ax.scatter(
                mean,
                mean_y,
                s=30,
                marker="D",
                color=ARM_COLOR[arm],
                edgecolor="white",
                linewidth=0.65,
                zorder=4,
            )
            ax.text(
                mean,
                mean_y + text_offset,
                f"{mean:+.3f}",
                ha="center",
                va="center",
                fontsize=4.9,
                color=ARM_COLOR[arm],
                fontweight="bold",
                zorder=5,
            )

        if task_index < len(TASK_ORDER) - 1:
            ax.axhline(
                center + 0.68,
                color="#B8C2C7",
                linewidth=0.8,
                zorder=1,
            )

    ax.axvline(0, color=COLORS["ink"], linewidth=0.85, zorder=2)
    ax.set_xlim(*x_limits)
    ax.set_ylim(task_centers[-1] + 0.74, -0.50)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels if show_y_labels else [])
    ax.tick_params(axis="y", labelsize=5.4, length=0)
    ax.set_xlabel("Paired difference in best endpoint score", labelpad=3)
    ax.set_ylabel("Task / world seed" if show_y_labels else "")
    ax.set_title(
        f"{display_label}\nRows are task-world pairs; diamonds are means",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_row_axis(ax)


def build_denominator_rows(
    wellau: dict[str, Any], deepseek: dict[str, Any]
) -> list[dict[str, Any]]:
    providers = [
        ("WellAU configuration", wellau["wellau_fallback"]["denominators"]),
        ("DeepSeek-v4-flash configuration", deepseek["denominators"]),
    ]
    rows: list[dict[str, Any]] = []
    for provider, denominator in providers:
        rows.extend(
            [
                {
                    "provider": provider,
                    "metric": "Completed cells",
                    "numerator": int(denominator["completed_cell_count"]),
                    "denominator": int(denominator["expected_cell_count"]),
                },
                {
                    "provider": provider,
                    "metric": "Complete experiments",
                    "numerator": int(denominator["complete_experiment_count"]),
                    "denominator": int(denominator["expected_cell_count"]) * 4,
                },
                {
                    "provider": provider,
                    "metric": "Exact replay",
                    "numerator": int(denominator["exact_replay_verified_count"]),
                    "denominator": int(denominator["terminal_record_count"]),
                },
            ]
        )
    for row in rows:
        row["rate"] = row["numerator"] / row["denominator"]
    return rows


def render_figure_3(
    endpoint_rows: list[dict[str, Any]],
    warning_rows: list[dict[str, Any]],
    denominator_rows: list[dict[str, Any]],
) -> list[Path]:
    y_values = [float(row["difference"]) for row in endpoint_rows]
    low = min(-0.24, min(y_values) - 0.05)
    high = max(0.44, max(y_values) + 0.08)

    fig = plt.figure(figsize=(7.2, 6.35))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.16,
        right=0.985,
        bottom=0.125,
        top=0.82,
        wspace=0.28,
        hspace=0.42,
        height_ratios=[1.42, 0.92],
        width_ratios=[1.08, 0.92],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    plot_endpoint_panel(
        ax_a,
        endpoint_rows,
        "WellAU configuration",
        "Baseline exploratory configuration",
        (low, high),
        show_y_labels=True,
    )
    plot_endpoint_panel(
        ax_b,
        endpoint_rows,
        "DeepSeek-v4-flash configuration",
        "Continuation exploratory configuration",
        (low, high),
        show_y_labels=False,
    )
    ax_b.set_ylabel("")
    panel_label(ax_a, "a", x=-0.10)
    panel_label(ax_b, "b", x=-0.10)

    # c — warning specificity matrix
    providers = ["WellAU configuration", "DeepSeek-v4-flash configuration"]
    provider_labels = {
        "WellAU configuration": "Baseline configuration",
        "DeepSeek-v4-flash configuration": "Continuation configuration",
    }
    row_labels: list[str] = []
    y_lookup: dict[tuple[str, str], int] = {}
    index = 0
    for provider in providers:
        for task in TASK_ORDER:
            y_lookup[(provider, task)] = index
            row_labels.append(
                f"{provider_labels[provider]} · {TASK_LABEL[task].replace(chr(10), ' ')}"
            )
            index += 1
    for row in warning_rows:
        y = y_lookup[(row["provider"], row["task_id"])]
        x = ARM_ORDER.index(row["arm"])
        rate = float(row["flag_rate"])
        color = ARM_COLOR[row["arm"]]
        ax_c.scatter(
            x,
            y,
            s=95 + 380 * rate,
            color=color,
            alpha=0.30 + 0.65 * rate,
            edgecolor="white",
            linewidth=0.7,
            zorder=3,
        )
        ax_c.text(
            x,
            y,
            f"{row['flag_count']}/{row['denominator']}",
            ha="center",
            va="center",
            fontsize=6.0,
            color=COLORS["ink"] if rate < 0.7 else "white",
            fontweight="bold",
            zorder=4,
        )
    ax_c.axhline(2.5, color="#B8C2C7", linewidth=0.9)
    ax_c.set_xlim(-0.55, 2.55)
    ax_c.set_ylim(len(row_labels) - 0.45, -0.55)
    ax_c.set_xticks(range(3), [ARM_LABEL[arm] for arm in ARM_ORDER])
    ax_c.set_yticks(range(len(row_labels)), row_labels)
    ax_c.tick_params(axis="y", labelsize=6.1)
    ax_c.tick_params(length=0)
    ax_c.spines[["left", "bottom"]].set_visible(False)
    ax_c.grid(axis="x", color=COLORS["grid"], linewidth=0.6)
    ax_c.set_title(
        "Final misindex warnings\nLabels are flagged cells / available cells",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    panel_label(ax_c, "c", x=-0.10)

    # d — completion and replay denominators
    metrics = ["Completed cells", "Complete experiments", "Exact replay"]
    metric_colors = [COLORS["aligned"], COLORS["misindexed"], COLORS["blue"]]
    x = np.arange(len(providers), dtype=float)
    width = 0.22
    for metric_index, (metric, color) in enumerate(zip(metrics, metric_colors, strict=True)):
        values = []
        labels = []
        for provider in providers:
            row = next(
                item
                for item in denominator_rows
                if item["provider"] == provider and item["metric"] == metric
            )
            values.append(float(row["rate"]))
            labels.append(f"{row['numerator']}/{row['denominator']}")
        positions = x + (metric_index - 1) * width
        bars = ax_d.bar(
            positions,
            values,
            width=width * 0.86,
            color=color,
            edgecolor="white",
            linewidth=0.6,
            label=metric,
        )
        for bar, label in zip(bars, labels, strict=True):
            ax_d.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.025,
                label,
                ha="center",
                va="bottom",
                fontsize=6.1,
                color=COLORS["ink"],
            )
    ax_d.set_xticks(x, ["Baseline\nconfiguration", "Continuation\nconfiguration"])
    ax_d.set_ylim(0, 1.11)
    ax_d.set_yticks(
        np.linspace(0, 1, 6), [f"{int(value * 100)}%" for value in np.linspace(0, 1, 6)]
    )
    ax_d.set_ylabel("Retained denominator reached")
    ax_d.set_title(
        "Execution completeness\nFailures remain in the denominator",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_d.legend(loc="lower left", fontsize=6.0, ncol=1)
    style_quant_axis(ax_d)
    panel_label(ax_d, "d", x=-0.10)

    fig.suptitle(
        "Explicit priors reshape exploratory behavior, but warnings are not selective",
        x=0.075,
        y=0.975,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D(
                [], [], marker="o", linestyle="", color=COLORS["aligned"], label="Aligned - opaque"
            ),
            mpl.lines.Line2D(
                [],
                [],
                marker="o",
                linestyle="",
                color=COLORS["misindexed"],
                label="Misindexed - opaque",
            ),
            mpl.lines.Line2D(
                [], [], marker="D", linestyle="", color=COLORS["ink"], label="Descriptive mean"
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(0.16, 0.905),
        ncol=3,
        fontsize=6.5,
        borderaxespad=0,
        handletextpad=0.35,
        columnspacing=1.1,
    )
    fig.text(
        0.16,
        0.025,
        "Exploratory descriptive evidence. Each row is one task-world pair; a short "
        "within-row segment links the two contrasts and diamonds show task means. No "
        "confirmatory tests or cross-system capability comparison are performed. The two "
        "configurations use separate method and interface contracts. Endpoint gains and "
        "verbal warnings do not establish law discovery, wrong-prior rejection or transfer.",
        ha="left",
        va="bottom",
        fontsize=6.5,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-3-development-prior-effects")


def normalize_open_action_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    if "open_action_rows" in summary:
        return [dict(row) for row in summary["open_action_rows"]]
    rows: list[dict[str, Any]] = []
    for raw in summary["cell_rows"]:
        cluster_parts = str(raw["cluster_id"]).split("--")
        task_id = cluster_parts[1]
        rows.append(
            {
                "cell_id": raw["cell_id"],
                "cluster_id": raw["cluster_id"],
                "task_id": task_id,
                "world_seed": int(raw["world_seed"]),
                "arm": raw["arm"],
                "status": raw["status"],
                "eligible": raw["status"] == "completed_uncontaminated",
                "selected_rank": raw.get("selected_rank"),
                "normalized_regret": raw.get("normalized_regret"),
                "top1_selected": raw.get("top1_selected"),
                "law_adequate": raw.get("law_adequate"),
                "mechanism_action_category": raw.get("mechanism_action_category"),
                "selected_minus_random_candidate_mean": raw.get(
                    "selected_minus_random_candidate_mean"
                ),
            }
        )
    return rows


def render_figure_5_cross_model_c2(
    model_rows: list[dict[str, Any]],
    locus_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
) -> list[Path]:
    model_order = ["deepseek", "codex"]
    model_labels = {
        "deepseek": "DeepSeek-v4-flash high",
        "codex": "GPT-5.6-sol medium",
    }
    model_colors = {"deepseek": COLORS["blue"], "codex": COLORS["violet"]}
    model_markers = {"deepseek": "o", "codex": "D"}
    locus_order = ["A_E", "A_P", "A_S"]
    locus_labels = {"A_E": "Entity", "A_P": "Parametric", "A_S": "Structural"}

    fig = plt.figure(figsize=(7.2, 5.7))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.115,
        right=0.985,
        bottom=0.18,
        top=0.80,
        wspace=0.34,
        hspace=0.52,
        width_ratios=[1.05, 0.95],
    )
    ax_a, ax_b, ax_c, ax_d = [
        fig.add_subplot(grid[row, column]) for row in range(2) for column in range(2)
    ]

    centers = np.arange(len(locus_order), dtype=float)
    offsets = {"deepseek": -0.13, "codex": 0.13}
    for model in model_order:
        rows = {row["locus"]: row for row in gate_rows if row["model"] == model}
        for index, locus in enumerate(locus_order):
            row = rows[locus]
            y = centers[index] + offsets[model]
            ax_a.plot(
                [row["lower_bound"], row["estimate"]],
                [y, y],
                color=model_colors[model],
                linewidth=1.3,
                alpha=0.7,
            )
            ax_a.scatter(
                row["estimate"],
                y,
                s=36,
                marker=model_markers[model],
                color=model_colors[model],
                edgecolor="white",
                linewidth=0.6,
                zorder=3,
            )
            ax_a.scatter(
                row["lower_bound"],
                y,
                s=34,
                marker="|",
                color=model_colors[model],
                linewidth=1.2,
                zorder=3,
            )
            ax_a.text(
                row["estimate"] + 0.018,
                y,
                f"p={row['p_value']:.3f}",
                ha="left",
                va="center",
                fontsize=5.2,
                color=COLORS["muted"],
            )
    ax_a.axvline(0, color=COLORS["ink"], linestyle="--", linewidth=0.8)
    ax_a.set_yticks(centers, [locus_labels[locus] for locus in locus_order])
    ax_a.set_ylim(len(locus_order) - 0.55, -0.55)
    gate_values = [float(row[key]) for row in gate_rows for key in ("lower_bound", "estimate")]
    ax_a.set_xlim(min(gate_values) - 0.06, max(0.16, max(gate_values) + 0.16))
    ax_a.set_xlabel("Selective-correction contrast")
    ax_a.set_title(
        "Both fully scheduled surfaces fail the\nselective-correction gate",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_a.legend(
        handles=[
            mpl.lines.Line2D(
                [],
                [],
                marker=model_markers[model],
                linestyle="",
                color=model_colors[model],
                label=model_labels[model],
            )
            for model in model_order
        ],
        loc="lower right",
        fontsize=5.5,
    )
    style_quant_axis(ax_a)
    panel_label(ax_a, "a", x=-0.13)

    width = 0.34
    for model_index, model in enumerate(model_order):
        rows = {row["locus"]: row for row in locus_rows if row["model"] == model}
        x = centers + (model_index - 0.5) * width
        values = [float(rows[locus]["mean_prediction_improvement"]) for locus in locus_order]
        bars = ax_b.bar(
            x,
            values,
            width=width * 0.92,
            color=model_colors[model],
            edgecolor="white",
            linewidth=0.6,
            label=model_labels[model],
        )
        for bar, value in zip(bars, values, strict=True):
            ax_b.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.006,
                f"{value:.3f}",
                ha="center",
                va="bottom",
                fontsize=5.2,
                rotation=90,
                color=COLORS["ink"],
            )
    ax_b.set_xticks(centers, [locus_labels[locus] for locus in locus_order])
    ax_b.set_ylim(0, 0.275)
    ax_b.set_ylabel("Mean prediction-error reduction")
    ax_b.set_title(
        "General numerical learning occurs\nin every locus and model",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_b.legend(loc="upper left", fontsize=5.5)
    style_quant_axis(ax_b)
    panel_label(ax_b, "b", x=-0.13)

    row_positions: list[float] = []
    row_labels: list[str] = []
    for locus_index, locus in enumerate(locus_order):
        for model_index, model in enumerate(model_order):
            y = locus_index * 2.35 + model_index * 0.72
            row_positions.append(y)
            row_labels.append(f"{locus_labels[locus]} · {model_labels[model]}")
            row = next(
                item for item in locus_rows if item["locus"] == locus and item["model"] == model
            )
            final_error = float(row["mean_effective_final_error"])
            law_error = float(row["mean_law_mae"])
            ax_c.plot(
                [final_error, law_error],
                [y, y],
                color=model_colors[model],
                linewidth=1.4,
                alpha=0.65,
            )
            ax_c.scatter(
                final_error,
                y,
                s=32,
                facecolor="white",
                edgecolor=model_colors[model],
                linewidth=1.0,
                zorder=3,
            )
            ax_c.scatter(
                law_error,
                y,
                s=32,
                color=model_colors[model],
                edgecolor="white",
                linewidth=0.5,
                zorder=3,
            )
    ax_c.set_yticks(row_positions, row_labels)
    ax_c.set_ylim(max(row_positions) + 0.55, -0.55)
    ax_c.set_xlim(0.11, 0.30)
    ax_c.set_xlabel("Normalized MAE")
    ax_c.set_title(
        "GPT-5.6-sol has lower compression error;\nthe representation gap persists",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_c.legend(
        handles=[
            mpl.lines.Line2D(
                [],
                [],
                marker="o",
                markerfacecolor="white",
                markeredgecolor=COLORS["ink"],
                linestyle="",
                label="Final predictions",
            ),
            mpl.lines.Line2D(
                [], [], marker="o", color=COLORS["ink"], linestyle="", label="Executable law"
            ),
        ],
        loc="lower right",
        fontsize=5.3,
    )
    style_row_axis(ax_c)
    panel_label(ax_c, "c", x=-0.13)

    outcome_specs = [
        ("blind_better_count", "Better", COLORS["green"]),
        ("blind_equivalent_count", "Equivalent", "#B9C0C4"),
        ("blind_worse_count", "Worse", COLORS["red"]),
    ]
    y = np.arange(len(model_order), dtype=float)
    left = np.zeros(len(model_order), dtype=float)
    model_lookup = {row["model"]: row for row in model_rows}
    for field, label, color in outcome_specs:
        values = np.array([float(model_lookup[model][field]) for model in model_order])
        percentages = values / 135.0 * 100.0
        bars = ax_d.barh(y, percentages, left=left, height=0.52, color=color, label=label)
        for index, (bar, count) in enumerate(zip(bars, values, strict=True)):
            if count > 0 and bar.get_width() > 2.2:
                ax_d.text(
                    left[index] + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    str(int(count)),
                    ha="center",
                    va="center",
                    fontsize=5.8,
                    color=COLORS["ink"],
                )
        left += percentages
    not_evaluable = np.array(
        [135 - int(model_lookup[model]["blind_gain_evaluable_count"]) for model in model_order],
        dtype=float,
    )
    not_evaluable_pct = not_evaluable / 135.0 * 100.0
    bars = ax_d.barh(
        y,
        not_evaluable_pct,
        left=left,
        height=0.52,
        color="#E4E8EA",
        label="Not evaluable",
    )
    for index, (bar, count) in enumerate(zip(bars, not_evaluable, strict=True)):
        ax_d.text(
            left[index] + bar.get_width() / 2,
            bar.get_y() + bar.get_height() / 2,
            str(int(count)),
            ha="center",
            va="center",
            fontsize=5.8,
            color=COLORS["ink"],
        )
    ax_d.set_yticks(y, [model_labels[model] for model in model_order])
    ax_d.set_xlim(0, 100)
    ax_d.set_xlabel("Share of 135 scheduled cells (%)")
    ax_d.set_title(
        "Lower observed law error coexists\nwith near-zero blind-action gain",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_d.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=2,
        fontsize=5.2,
        columnspacing=0.8,
    )
    style_quant_axis(ax_d)
    panel_label(ax_d, "d", x=-0.13)

    fig.suptitle(
        "Lower executable-law error does not coincide with better blind action",
        x=0.115,
        y=0.975,
        ha="left",
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.115,
        0.905,
        "C2 scheduled n=135/model; law n=135/129, MAE 0.237/0.175; "
        "blind n=121/126, gain -0.0010/-0.0001",
        ha="left",
        va="center",
        fontsize=7.0,
        fontweight="bold",
        color=COLORS["blue"],
        bbox={"facecolor": COLORS["blue_light"], "edgecolor": "none", "pad": 2.0},
    )
    fig.text(
        0.115,
        0.020,
        "DeepSeek-v4-flash and GPT-5.6-sol use the same 45 task-world clusters, nine tasks and "
        "three prior arms. Panels a-b retain the registered adverse-bound correction decisions; "
        "panel c is availability-conditioned and descriptive. Panel d keeps every scheduled cell: "
        "DeepSeek better/equivalent/worse/not-evaluable is 1/119/1/14 and GPT is 0/125/1/9. "
        "Model differences are not provider causal effects or a leaderboard.",
        ha="left",
        va="bottom",
        fontsize=6.15,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-5-capability-chain")


def render_figure_6_open_action(
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_closeout: dict[str, Any],
    construction_closeout: dict[str, Any],
    qualification_closeout: dict[str, Any],
    gate_alignment: dict[str, Any],
    reviewer_controls: dict[str, Any],
    causal_extension: dict[str, Any],
) -> list[Path]:
    eligible = [row for row in rows if row["eligible"]]
    task_order = [
        "electrochemical-conversion",
        "reaction-to-crystallization",
        "reaction-safety-constrained",
    ]
    fig = plt.figure(figsize=(7.2, 6.6))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.14,
        right=0.985,
        bottom=0.195,
        top=0.82,
        wspace=0.32,
        hspace=0.48,
        height_ratios=[1.18, 1.0],
        width_ratios=[1.08, 0.92],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    def plot_cell_metric(
        ax: mpl.axes.Axes,
        metric: str,
        ylabel: str,
        title: str,
        xlim: tuple[float, float],
        *,
        show_y_labels: bool,
    ) -> None:
        seed_offsets = np.linspace(-0.27, 0.27, 5)
        block_step = 1.22
        task_centers = [index * block_step for index in range(len(task_order))]
        y_ticks: list[float] = []
        y_labels: list[str] = []
        row_lookup = {(row["task_id"], int(row["world_seed"]), row["arm"]): row for row in eligible}

        for task_index, task in enumerate(task_order):
            center = task_centers[task_index]
            for seed in range(5):
                y = center + float(seed_offsets[seed])
                y_ticks.append(y)
                y_labels.append(f"{ROW_TASK_LABEL[task]} world {seed + 1}")
                for arm in ARM_ORDER:
                    row = row_lookup.get((task, seed, arm))
                    value = None if row is None else row.get(metric)
                    if value is None:
                        continue
                    marker = "*" if row.get("top1_selected") else "o"
                    ax.scatter(
                        float(value),
                        y,
                        s=38 if marker == "*" else 32,
                        marker=marker,
                        color=ARM_COLOR[arm],
                        edgecolor="white",
                        linewidth=0.65,
                        alpha=0.95,
                        zorder=3,
                    )
                if any(row_lookup.get((task, seed, arm)) is None for arm in ARM_ORDER):
                    ax.text(
                        xlim[0] + 0.018 * (xlim[1] - xlim[0]),
                        y,
                        "x",
                        ha="center",
                        va="center",
                        fontsize=7.0,
                        color=COLORS["muted"],
                        zorder=4,
                    )
            if task_index < len(task_order) - 1:
                ax.axhline(
                    center + 0.67,
                    color="#B8C2C7",
                    linewidth=0.8,
                    zorder=1,
                )

        ax.set_xlim(*xlim)
        ax.set_ylim(task_centers[-1] + 0.60, -0.50)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels if show_y_labels else [])
        ax.tick_params(axis="y", labelsize=5.4, length=0)
        ax.set_ylabel(ylabel if show_y_labels else "")
        ax.set_title(title, loc="left", fontweight="bold", pad=6)
        style_row_axis(ax)

    plot_cell_metric(
        ax_a,
        "selected_rank",
        "Selected true rank (lower is better)",
        "Unseen-plan ranking is task dependent",
        (0.5, 8.8),
        show_y_labels=True,
    )
    ax_a.axvline(
        4.5, color=COLORS["muted"], linewidth=0.8, linestyle="--", label="Random expected rank"
    )
    ax_a.legend(loc="upper right", fontsize=5.8)
    panel_label(ax_a, "a", x=-0.11)

    # Replace the descriptive rank panel with the prospectively frozen four-condition
    # action extension. The original W2-50 rows remain in the source table and panel b.
    ax_a.clear()
    condition_rows, contrast_rows = build_action_extension_rows(causal_extension)
    condition_order = [
        "no_evidence",
        "yoked_evidence",
        "learned_law_only",
        "autonomous_exploration",
    ]
    condition_labels = {
        "no_evidence": "No evidence",
        "yoked_evidence": "Yoked evidence",
        "learned_law_only": "Learned law",
        "autonomous_exploration": "Autonomous",
    }
    model_colors = {"deepseek": COLORS["blue"], "codex": COLORS["violet"]}
    model_labels = {
        "deepseek": "DeepSeek-v4-flash high",
        "codex": "GPT-5.6-sol medium",
    }
    centers = np.arange(len(condition_order), dtype=float)
    width = 0.34
    for model_index, model in enumerate(("deepseek", "codex")):
        lookup = {row["condition"]: row for row in condition_rows if row["model"] == model}
        x = centers + (model_index - 0.5) * width
        values = [
            float(lookup[condition]["mean_failure_aware_normalized_regret"])
            for condition in condition_order
        ]
        bars = ax_a.bar(
            x,
            values,
            width=width * 0.92,
            color=model_colors[model],
            edgecolor="white",
            linewidth=0.6,
            label=model_labels[model],
        )
        for bar, condition, value in zip(bars, condition_order, values, strict=True):
            row = lookup[condition]
            ax_a.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.025,
                f"{row['completed_count']}/{row['row_count']}",
                ha="center",
                va="bottom",
                fontsize=5.2,
                rotation=90,
                color=COLORS["ink"],
            )
    ax_a.set_xticks(
        centers,
        [condition_labels[condition] for condition in condition_order],
        rotation=18,
        ha="right",
    )
    ax_a.set_ylim(0, 1.02)
    ax_a.set_ylabel("Failure-aware normalized regret\n(lower is better)")
    ax_a.set_title(
        "All-scheduled action outcomes differ\nby model and information strategy",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_a.legend(loc="upper left", fontsize=5.5)
    style_quant_axis(ax_a)
    panel_label(ax_a, "a", x=-0.11)

    decision_aligned = summary["decision_aligned_law_action"]
    decision_rows = decision_aligned["cell_rows"]
    for task_id in task_order:
        task_rows = [
            row
            for row in decision_rows
            if row["task_id"] == task_id and row["law_status"] == "evaluated"
        ]
        for row in task_rows:
            marker = "*" if row["participant_top1"] else "o"
            ax_b.scatter(
                float(row["law_implied_normalized_regret"]),
                float(row["participant_normalized_regret"]),
                s=34 if marker == "*" else 24,
                marker=marker,
                color=FULL_TASK_COLOR[task_id],
                edgecolor="white",
                linewidth=0.55,
                alpha=0.88,
                zorder=3,
            )
    ax_b.plot(
        [0.0, 1.0],
        [0.0, 1.0],
        color=COLORS["muted"],
        linewidth=0.8,
        linestyle="--",
        zorder=1,
    )
    ax_b.set_xlim(-0.05, 1.05)
    ax_b.set_ylim(-0.05, 1.08)
    ax_b.set_xlabel("Law-implied Top-1 normalized regret")
    ax_b.set_ylabel("Participant normalized regret")
    ax_b.set_title(
        "DeepSeek actions often depart from\nthe executable law's candidate ordering",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_b)
    pooled = decision_aligned["overall"]
    ax_b.text(
        0.48,
        0.95,
        "law Top-1: "
        f"{pooled['law_implied_top1_count']}/{pooled['law_evaluated_count']}\n"
        "participant Top-1: "
        f"{pooled['participant_top1_count']}/{pooled['law_evaluated_count']}\n"
        "law followed: "
        f"{pooled['law_implied_top1_followed_count']}/"
        f"{pooled['law_action_agreement_evaluable_count']}",
        transform=ax_b.transAxes,
        ha="center",
        va="top",
        fontsize=5.2,
        color=COLORS["muted"],
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 1.2},
        zorder=5,
    )
    panel_label(ax_b, "b", x=-0.12)

    formal_preparation = formal_closeout["formal_preparation"]
    qualification_rows = [
        {
            "label": "96-query\nfresh",
            "planned": int(formal_closeout["frozen_design"]["planned_cluster_count"]),
            "passed": int(formal_preparation["qualified_cluster_count"]),
            "rejected": int(formal_preparation["scientifically_rejected_cluster_count"]),
            "not_started": int(formal_preparation["not_started_cluster_count"]),
            "detail": "candidate 8/8; rank 7/8; 0/225 participant sessions",
        },
        {
            "label": "320-query\nexposed",
            "planned": int(construction_closeout["planned_unit_count"]),
            "passed": int(construction_closeout["passed_unit_count"]),
            "rejected": int(construction_closeout["scientifically_rejected_unit_count"]),
            "not_started": 0,
            "detail": "7/7 pass; 4 historical failures repaired; construction only",
        },
        {
            "label": "320-query\nfresh",
            "planned": int(qualification_closeout["planned_cluster_count"]),
            "passed": int(qualification_closeout["passed_cluster_count"]),
            "rejected": int(qualification_closeout["scientifically_rejected_cluster_count"]),
            "not_started": int(qualification_closeout["not_started_cluster_count"]),
            "detail": r"$\rho$=.714; Top-1 correct; regret=0; 0 participant sessions",
        },
    ]
    y_positions = np.array([2.5, 1.25, 0.0])
    for y, row in zip(y_positions, qualification_rows, strict=True):
        left = 0
        for key, color, hatch in [
            ("passed", COLORS["green"], None),
            ("rejected", COLORS["red"], "////"),
            ("not_started", "#D8DEE1", None),
        ]:
            value = int(row[key])
            if value == 0:
                continue
            ax_c.barh(
                y,
                value,
                left=left,
                height=0.43,
                color=color,
                hatch=hatch,
                edgecolor="white" if hatch is None else COLORS["red"],
                linewidth=0.7,
                zorder=2,
            )
            ax_c.text(
                left + value / 2,
                y,
                str(value),
                ha="center",
                va="center",
                fontsize=6.2,
                fontweight="bold",
                color="white" if key != "not_started" else COLORS["ink"],
                zorder=3,
            )
            left += value
        ax_c.text(
            0,
            y - 0.36,
            str(row["detail"]),
            ha="left",
            va="top",
            fontsize=5.5,
            color=COLORS["muted"],
        )
    ax_c.set_xlim(0, 15.3)
    ax_c.set_ylim(-0.67, 3.02)
    ax_c.set_yticks(y_positions, [str(row["label"]) for row in qualification_rows])
    ax_c.tick_params(axis="y", labelsize=6.1, length=0)
    ax_c.set_xticks([0, 5, 10, 15])
    ax_c.set_xlabel("Planned task-world qualification units")
    ax_c.set_title(
        "Construction repair does not erase\nfresh-world stop decisions",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_c)
    ax_c.legend(
        handles=[
            mpl.patches.Patch(color=COLORS["green"], label="passed rank gate"),
            mpl.patches.Patch(
                facecolor=COLORS["red"],
                edgecolor=COLORS["red"],
                hatch="////",
                label="scientifically rejected",
            ),
            mpl.patches.Patch(color="#D8DEE1", label="not started"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.52, -0.22),
        ncol=3,
        fontsize=5.1,
        handlelength=1.2,
        columnspacing=0.8,
    )
    panel_label(ax_c, "c", x=-0.13)

    # The detailed W2-51/W2-52 funnel remains in the exported source table. The
    # main panel now shows the four preregistered action contrasts; panel d retains
    # all 16 oracle/gate-alignment units.
    ax_c.clear()
    contrast_order = [
        "autonomous_exploration_minus_no_evidence",
        "yoked_evidence_minus_no_evidence",
        "learned_law_only_minus_no_evidence",
        "autonomous_exploration_minus_yoked_evidence",
    ]
    contrast_labels = {
        "autonomous_exploration_minus_no_evidence": "Autonomous - none",
        "yoked_evidence_minus_no_evidence": "Yoked - none",
        "learned_law_only_minus_no_evidence": "Learned law - none",
        "autonomous_exploration_minus_yoked_evidence": "Autonomous - yoked",
    }
    centers = np.arange(len(contrast_order), dtype=float)
    offsets = {"deepseek": -0.13, "codex": 0.13}
    for model in ("deepseek", "codex"):
        lookup = {row["contrast"]: row for row in contrast_rows if row["model"] == model}
        for index, contrast in enumerate(contrast_order):
            row = lookup[contrast]
            y = centers[index] + offsets[model]
            ax_c.plot(
                [row["interval_low"], row["interval_high"]],
                [y, y],
                color=model_colors[model],
                linewidth=1.4,
                alpha=0.75,
            )
            ax_c.scatter(
                row["mean_regret_difference"],
                y,
                s=38,
                marker="o" if model == "deepseek" else "D",
                color=model_colors[model],
                edgecolor="white",
                linewidth=0.6,
                zorder=3,
            )
    ax_c.axvline(0, color=COLORS["ink"], linestyle="--", linewidth=0.8)
    ax_c.set_yticks(centers, [contrast_labels[value] for value in contrast_order])
    ax_c.set_ylim(len(contrast_order) - 0.55, -0.55)
    ax_c.set_xlim(-0.72, 0.56)
    ax_c.set_xlabel("Mean regret difference (negative favors first condition)")
    ax_c.set_title(
        "Strategy estimates differ by model;\nno consistent autonomy benefit is established",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    ax_c.text(
        0.98,
        0.04,
        "all scheduled: 45 strata per model",
        transform=ax_c.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.3,
        color=COLORS["muted"],
    )
    style_quant_axis(ax_c)
    panel_label(ax_c, "c", x=-0.13)

    group_specs = {
        "w2_51_96_grid_fresh_formal_preparation": (
            "96 fresh",
            COLORS["blue"],
            "o",
        ),
        "w2_52_320_grid_exposed_construction": (
            "320 exposed",
            COLORS["violet"],
            "s",
        ),
        "w2_52_320_grid_fresh_prospective": (
            "320 fresh",
            COLORS["red"],
            "D",
        ),
    }
    for group_id, (label, color, marker) in group_specs.items():
        group_rows = [row for row in gate_alignment["unit_rows"] if row["group_id"] == group_id]
        ax_d.scatter(
            [float(row["spearman_rank_correlation"]) for row in group_rows],
            [float(row["normalized_regret"]) for row in group_rows],
            s=38,
            marker=marker,
            color=color,
            edgecolor="white",
            linewidth=0.65,
            alpha=0.9,
            label=label,
            zorder=3,
        )
        top1_rows = [row for row in group_rows if int(row["top1"]) == 1]
        if top1_rows:
            ax_d.scatter(
                [float(row["spearman_rank_correlation"]) for row in top1_rows],
                [float(row["normalized_regret"]) for row in top1_rows],
                s=22,
                marker="*",
                color=COLORS["ink"],
                linewidth=0,
                zorder=4,
            )
    ax_d.axvline(0.80, color=COLORS["red"], linewidth=0.9, linestyle="--")
    ax_d.axhline(0.01, color=COLORS["muted"], linewidth=0.8, linestyle=":")
    ax_d.set_xlim(0.69, 1.015)
    ax_d.set_ylim(-0.004, 0.082)
    ax_d.set_xlabel(r"Complete-ranking Spearman $\rho$")
    ax_d.set_ylabel("Normalized regret")
    ax_d.set_title(
        "Full-ranking validity and action\nvalidity disagree in both directions",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_d)
    ax_d.text(
        0.835,
        0.078,
        "6 fresh 96 units:\nrank pass, Top-1 wrong",
        ha="left",
        va="top",
        fontsize=5.7,
        color=COLORS["red"],
        fontweight="bold",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 1.0},
    )
    fresh_row = next(
        row
        for row in gate_alignment["unit_rows"]
        if row["group_id"] == "w2_52_320_grid_fresh_prospective"
    )
    ax_d.annotate(
        "fresh 320:\nrank fail; Top-1",
        xy=(
            float(fresh_row["spearman_rank_correlation"]),
            float(fresh_row["normalized_regret"]),
        ),
        xytext=(0.700, 0.052),
        fontsize=5.7,
        color=COLORS["red"],
        fontweight="bold",
        arrowprops={"arrowstyle": "-", "color": COLORS["red"], "linewidth": 0.75},
    )
    ax_d.text(
        0.796,
        0.081,
        r"rank gate $\rho=.80$",
        ha="right",
        va="top",
        fontsize=5.3,
        color=COLORS["red"],
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 0.7},
        zorder=4,
    )
    ax_d.text(
        1.012,
        0.0105,
        "near-optimal boundary",
        ha="right",
        va="bottom",
        fontsize=5.2,
        color=COLORS["muted"],
    )
    handles, labels = ax_d.get_legend_handles_labels()
    handles.append(
        mpl.lines.Line2D(
            [],
            [],
            marker="*",
            linestyle="",
            color=COLORS["ink"],
            label="Top-1 selected",
        )
    )
    labels.append("Top-1 selected")
    ax_d.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.50, -0.22),
        ncol=2,
        fontsize=5.1,
        handletextpad=0.35,
        columnspacing=0.8,
    )
    panel_label(ax_d, "d", x=-0.13)

    fig.suptitle(
        "Evidence, executable laws and evaluator rankings are imperfect action proxies",
        x=0.09,
        y=0.975,
        ha="left",
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D(
                [],
                [],
                marker="o",
                linestyle="",
                color=COLORS["blue"],
                label="DeepSeek-v4-flash high",
            ),
            mpl.lines.Line2D(
                [], [], marker="D", linestyle="", color=COLORS["violet"], label="GPT-5.6-sol medium"
            ),
            mpl.lines.Line2D(
                [], [], marker="*", linestyle="", color=COLORS["ink"], label="Top-1 selected"
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(0.14, 0.905),
        ncol=3,
        fontsize=6.4,
        borderaxespad=0,
        handletextpad=0.35,
        columnspacing=1.0,
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D(
                [],
                [],
                marker="o",
                linestyle="",
                color=FULL_TASK_COLOR[task_id],
                label=ROW_TASK_LABEL[task_id],
            )
            for task_id in task_order
        ],
        loc="upper right",
        bbox_to_anchor=(0.985, 0.905),
        ncol=3,
        fontsize=5.2,
        borderaxespad=0,
        handletextpad=0.25,
        columnspacing=0.7,
    )
    fig.text(
        0.14,
        0.018,
        "Four-condition extension: 360 scheduled slots and 45 strata per model; donor, "
        "blocked-recipient "
        "and recipient failures remain in the primary strategy estimates. Open-action cohort: "
        f"45 scheduled cells and {summary['provider_free_truth_query_count']}/"
        f"{summary['provider_free_exact_replay_count']} truth/replay. Oracle diagnostics contain "
        "zero participant sessions and 16 frozen unit-version records. Full-ranking correlation is "
        "secondary; model differences are not provider causal effects.",
        ha="left",
        va="bottom",
        fontsize=6.2,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-6-open-action-formal")


def render_figure_4(confirmation: dict[str, Any]) -> list[Path]:
    cluster_rows = confirmation["cluster_rows"]
    cell_rows = confirmation["cell_rows"]
    fig = plt.figure(figsize=(7.2, 5.75))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.085,
        right=0.985,
        bottom=0.12,
        top=0.82,
        wspace=0.32,
        hspace=0.50,
        width_ratios=[1.05, 0.95],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    # a — paired aligned versus misindexed held-out prediction improvement.
    for row in cluster_rows:
        task_id = str(row["task_id"])
        aligned = float(row["arm_primary_improvements"]["aligned_nominal"])
        misindexed = float(row["arm_primary_improvements"]["misindexed_nominal"])
        color = FULL_TASK_COLOR[task_id]
        complete_case = row.get("complete_case") is True
        ax_a.scatter(
            aligned,
            misindexed,
            s=34,
            facecolor=color if complete_case else "white",
            edgecolor=color,
            linewidth=1.0,
            alpha=0.88,
            zorder=3,
        )
    low, high = -0.08, 0.38
    ax_a.plot([low, high], [low, high], color="#97A5AC", linewidth=1.0, zorder=1)
    ax_a.axhline(0, color=COLORS["grid"], linewidth=0.7, zorder=0)
    ax_a.axvline(0, color=COLORS["grid"], linewidth=0.7, zorder=0)
    ax_a.set_xlim(low, high)
    ax_a.set_ylim(low, high)
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.set_xlabel("Aligned-prior prediction improvement")
    ax_a.set_ylabel("Misindexed-prior prediction improvement")
    ax_a.set_title(
        "Misindexed correction does not exceed\naligned-prior improvement",
        loc="left",
        fontweight="bold",
        pad=7,
        fontsize=8.8,
    )
    ax_a.text(
        0.03,
        0.96,
        "7/25 clusters above identity\n18/25 below identity",
        transform=ax_a.transAxes,
        ha="left",
        va="top",
        fontsize=6.6,
        color=COLORS["muted"],
    )
    style_quant_axis(ax_a)
    panel_label(ax_a, "a", x=-0.12, y=1.10)

    # b — primary H3 contrast by task and seed.
    jitter = np.linspace(-0.16, 0.16, 5)
    for task_index, task_id in enumerate(FULL_TASK_ORDER):
        rows = sorted(
            (row for row in cluster_rows if row["task_id"] == task_id),
            key=lambda row: int(row["world_seed"]),
        )
        values = [float(row["H3_primary_contrast"]) for row in rows]
        for offset, row, value in zip(jitter, rows, values, strict=True):
            color = FULL_TASK_COLOR[task_id]
            complete_case = row.get("complete_case") is True
            ax_b.scatter(
                value,
                task_index + offset,
                s=28,
                facecolor=color if complete_case else "white",
                edgecolor=color,
                linewidth=0.9,
                alpha=0.90,
                zorder=3,
            )
        ax_b.scatter(
            float(np.mean(values)),
            task_index,
            marker="D",
            s=34,
            color=COLORS["ink"],
            edgecolor="white",
            linewidth=0.5,
            zorder=4,
        )
    ax_b.axvline(0, color="#89989F", linewidth=1.0)
    ax_b.set_yticks(
        range(len(FULL_TASK_ORDER)),
        [FULL_TASK_LABEL[task] for task in FULL_TASK_ORDER],
    )
    ax_b.set_xlim(-0.28, 0.33)
    ax_b.invert_yaxis()
    ax_b.set_xlabel("$C_{prior}$ = misindexed improvement - aligned improvement")
    ax_b.set_title(
        "Only safety has a positive\ntask-level mean $C_{prior}$",
        loc="left",
        fontweight="bold",
        pad=7,
        fontsize=8.8,
    )
    ax_b.text(
        0.98,
        0.96,
        "Overall mean -0.042\nmedian -0.039",
        transform=ax_b.transAxes,
        ha="right",
        va="top",
        fontsize=6.6,
        color=COLORS["muted"],
    )
    style_quant_axis(ax_b)
    panel_label(ax_b, "b", x=-0.10, y=1.10)

    # c — executable law-summary compression relative to final typed predictions.
    law_by_arm: list[list[float]] = []
    for arm in ARM_ORDER:
        law_by_arm.append(
            [
                float(row["law_summary_minus_final_error"])
                for row in cell_rows
                if row["prior_arm"] == arm
                and isinstance(row.get("law_summary_minus_final_error"), int | float)
            ]
        )
    boxes = ax_c.boxplot(
        law_by_arm,
        positions=np.arange(3),
        widths=0.50,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": COLORS["ink"], "linewidth": 1.1},
        whiskerprops={"color": "#87969D", "linewidth": 0.8},
        capprops={"color": "#87969D", "linewidth": 0.8},
        boxprops={"color": "#87969D", "linewidth": 0.8},
    )
    for patch, arm in zip(boxes["boxes"], ARM_ORDER, strict=True):
        patch.set_facecolor(ARM_COLOR[arm])
        patch.set_alpha(0.22)
    for arm_index, (arm, values) in enumerate(zip(ARM_ORDER, law_by_arm, strict=True)):
        offsets = np.linspace(-0.15, 0.15, len(values))
        ax_c.scatter(
            arm_index + offsets,
            values,
            s=16,
            color=ARM_COLOR[arm],
            alpha=0.72,
            edgecolor="white",
            linewidth=0.35,
            zorder=3,
        )
        better = sum(value < 0 for value in values)
        worse = sum(value > 0 for value in values)
        ax_c.text(
            arm_index,
            0.69,
            f"{better} better / {worse} worse",
            ha="center",
            va="top",
            fontsize=6.0,
            color=COLORS["muted"],
        )
    ax_c.axhline(0, color="#89989F", linewidth=1.0)
    ax_c.set_xticks(range(3), [ARM_LABEL[arm] for arm in ARM_ORDER])
    ax_c.set_ylim(-0.13, 0.72)
    ax_c.set_ylabel("Law-summary error - final-prediction error")
    ax_c.set_title(
        "Executable law compression is often\nworse than final predictions",
        loc="left",
        fontweight="bold",
        pad=7,
        fontsize=8.8,
    )
    style_quant_axis(ax_c)
    panel_label(ax_c, "c", x=-0.02, y=1.17)

    # d — blind recommendation compared with the observed incumbent.
    gains = [
        float(row["blind_recommendation_gain"])
        for row in cell_rows
        if isinstance(row.get("blind_recommendation_gain"), int | float)
    ]
    counts = [
        sum(value > 1e-12 for value in gains),
        sum(abs(value) <= 1e-12 for value in gains),
        sum(value < -1e-12 for value in gains),
    ]
    bars = ax_d.bar(
        np.arange(3),
        counts,
        width=0.62,
        color=[COLORS["green"], COLORS["opaque"], COLORS["red"]],
        edgecolor="white",
        linewidth=0.7,
    )
    for bar, count in zip(bars, counts, strict=True):
        ax_d.text(
            bar.get_x() + bar.get_width() / 2,
            count + 1.3,
            str(count),
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color=COLORS["ink"],
        )
    ax_d.set_xticks(range(3), ["Better", "Equivalent", "Worse"])
    ax_d.set_ylim(0, 73)
    ax_d.set_ylabel("Eligible participant cells")
    ax_d.set_title(
        "Recommendations do not beat\nthe observed incumbent",
        loc="left",
        fontweight="bold",
        pad=7,
        fontsize=8.8,
    )
    ax_d.text(
        0.03,
        0.91,
        "414/414 paired blind replays completed\n69 eligible cells; no additional model calls",
        transform=ax_d.transAxes,
        ha="left",
        va="top",
        fontsize=6.6,
        color=COLORS["muted"],
    )
    style_quant_axis(ax_d)
    panel_label(ax_d, "d", x=-0.10, y=1.10)

    fig.suptitle(
        "Held-out evaluation separates prediction repair from law consistency",
        x=0.075,
        y=0.975,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D(
                [],
                [],
                marker="o",
                linestyle="",
                markerfacecolor=color,
                markeredgecolor=color,
                color=color,
                label=FULL_TASK_LABEL[task],
            )
            for task, color in FULL_TASK_COLOR.items()
        ],
        loc="upper left",
        bbox_to_anchor=(0.075, 0.905),
        ncol=5,
        fontsize=6.0,
        borderaxespad=0,
        handletextpad=0.25,
        columnspacing=0.75,
    )
    fig.text(
        0.075,
        0.027,
        "Five-task exploratory evidence: 25 task x world clusters, 75 retained cells, "
        "100/100 evaluator-truth queries and 414/414 blind replays. Open points mark "
        "clusters with a retained failed arm; prespecified missing-outcome rules are retained. "
        "No confirmatory test, private transfer claim or cross-system ranking is performed.",
        ha="left",
        va="bottom",
        fontsize=6.35,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-4-development-confirmation")


def build_prospective_story_rows(
    checkpoint_rows: list[dict[str, str]],
    experiment_rows: list[dict[str, str]],
    locus_decisions: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """Build the compact, formal story layer without additional provider calls."""
    initial_rows: list[dict[str, Any]] = []
    improvement_rows: list[dict[str, Any]] = []
    for locus in ("A_E", "A_P", "A_S"):
        by_stage = {
            (row["stage"], row["prior_arm"]): float(row["mean_normalized_mae"])
            for row in checkpoint_rows
            if row["locus"] == locus
        }
        for arm in ARM_ORDER:
            pre = by_stage[("pre_evidence", arm)]
            final = by_stage[("final", arm)]
            initial_rows.append({"locus": locus, "arm": arm, "mean_normalized_mae": pre})
            improvement_rows.append(
                {
                    "locus": locus,
                    "arm": arm,
                    "mean_pre_to_final_improvement": pre - final,
                }
            )

    first_rows = [row for row in experiment_rows if int(row["experiment_index"]) == 1]
    cluster_lookup: dict[tuple[str, str, int], dict[str, dict[str, str]]] = {}
    for row in first_rows:
        key = (row["block"], row["task"], int(row["world_seed"]))
        cluster_lookup.setdefault(key, {})[row["arm"]] = row
    pair_specs = [
        ("opaque", "aligned_nominal", "Opaque vs aligned"),
        ("opaque", "misindexed_nominal", "Opaque vs misspecified"),
        ("aligned_nominal", "misindexed_nominal", "Aligned vs misspecified"),
    ]
    recipe_rows: list[dict[str, Any]] = []
    for left, right, label in pair_specs:
        comparable = [
            cells for cells in cluster_lookup.values() if left in cells and right in cells
        ]
        different = sum(
            cells[left]["recipe_sha256"] != cells[right]["recipe_sha256"] for cells in comparable
        )
        recipe_rows.append(
            {
                "comparison": label,
                "different_first_recipe_count": different,
                "matched_cluster_count": len(comparable),
                "different_fraction": different / len(comparable),
            }
        )

    decision_rows = [
        {
            "locus": locus,
            "primary_estimate": float(locus_decisions[locus]["primary_estimate"]),
            "p_value": float(locus_decisions[locus]["p_value"]),
            "passed": bool(locus_decisions[locus]["passed"]),
        }
        for locus in ("A_E", "A_P", "A_S")
    ]
    return initial_rows, recipe_rows, improvement_rows, decision_rows


def render_figure_3_prospective(
    initial_rows: list[dict[str, Any]],
    recipe_rows: list[dict[str, Any]],
    improvement_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
) -> list[Path]:
    locus_order = ["A_E", "A_P", "A_S"]
    locus_labels = ["Entity", "Parametric", "Structural"]
    fig = plt.figure(figsize=(7.2, 5.45))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.09,
        right=0.985,
        bottom=0.125,
        top=0.82,
        wspace=0.31,
        hspace=0.48,
        width_ratios=[1.05, 0.95],
    )
    ax_a, ax_b, ax_c, ax_d = [
        fig.add_subplot(grid[row, col]) for row in range(2) for col in range(2)
    ]

    x = np.arange(3, dtype=float)
    width = 0.22
    for arm_index, arm in enumerate(ARM_ORDER):
        values = [
            next(
                row["mean_normalized_mae"]
                for row in initial_rows
                if row["locus"] == locus and row["arm"] == arm
            )
            for locus in locus_order
        ]
        ax_a.bar(
            x + (arm_index - 1) * width,
            values,
            width=width * 0.88,
            color=ARM_COLOR[arm],
            edgecolor="white",
            linewidth=0.6,
            label=ARM_LABEL[arm],
        )
    ax_a.set_xticks(x, locus_labels)
    ax_a.set_ylim(0, 0.46)
    ax_a.set_ylabel("Pre-evidence normalized MAE")
    ax_a.set_title(
        "Starting predictions are arm dependent,\nnot uniformly ordered by correctness",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_a)
    panel_label(ax_a, "a", x=-0.12)

    bars = ax_b.barh(
        np.arange(3),
        [row["different_fraction"] for row in recipe_rows],
        color=[COLORS["blue"], COLORS["misindexed"], COLORS["violet"]],
        edgecolor="white",
        linewidth=0.7,
        height=0.58,
    )
    for bar, row in zip(bars, recipe_rows, strict=True):
        ax_b.text(
            0.98,
            bar.get_y() + bar.get_height() / 2,
            f"{row['different_first_recipe_count']}/{row['matched_cluster_count']}",
            ha="right",
            va="center",
            fontsize=7.0,
            color="white",
            fontweight="bold",
        )
    ax_b.set_yticks(np.arange(3), [row["comparison"] for row in recipe_rows])
    ax_b.set_xlim(0, 1.02)
    ax_b.set_xlabel("Fraction with a different first complete recipe")
    ax_b.set_title(
        "The intervention enters the first\nexperimental trajectory",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_row_axis(ax_b)
    panel_label(ax_b, "b", x=-0.12)

    for arm_index, arm in enumerate(ARM_ORDER):
        values = [
            next(
                row["mean_pre_to_final_improvement"]
                for row in improvement_rows
                if row["locus"] == locus and row["arm"] == arm
            )
            for locus in locus_order
        ]
        ax_c.bar(
            x + (arm_index - 1) * width,
            values,
            width=width * 0.88,
            color=ARM_COLOR[arm],
            edgecolor="white",
            linewidth=0.6,
        )
    ax_c.axhline(0, color="#89989F", linewidth=0.8)
    ax_c.set_xticks(x, locus_labels)
    ax_c.set_ylim(-0.02, 0.28)
    ax_c.set_ylabel("Mean pre-to-final error reduction")
    ax_c.set_title(
        "Predictions improve in every arm\nat every intervention locus",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_c)
    panel_label(ax_c, "c", x=-0.12)

    estimates = [row["primary_estimate"] for row in decision_rows]
    colors = [COLORS["red"], COLORS["aligned"], COLORS["red"]]
    y = np.arange(3)
    ax_d.axvline(0, color="#89989F", linewidth=1.0)
    ax_d.hlines(y, 0, estimates, color=colors, linewidth=2.0)
    ax_d.scatter(estimates, y, s=68, color=colors, edgecolor="white", linewidth=0.8, zorder=3)
    for index, row in enumerate(decision_rows):
        ax_d.text(
            0.095,
            index,
            f"p={row['p_value']:.3f} · not passed",
            ha="left",
            va="center",
            fontsize=6.3,
            color=COLORS["muted"],
        )
    ax_d.set_yticks(y, locus_labels)
    ax_d.set_xlim(-0.28, 0.28)
    ax_d.invert_yaxis()
    ax_d.set_xlabel("Failure-aware selective-correction contrast")
    ax_d.set_title(
        "The registered selective-correction\ncriteria are not met",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_row_axis(ax_d)
    panel_label(ax_d, "d", x=-0.12)

    fig.suptitle(
        "Search patterns differ across initial-model arms; selective repair is not established",
        x=0.09,
        y=0.975,
        ha="left",
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            mpl.patches.Patch(color=ARM_COLOR[arm], label=ARM_LABEL[arm]) for arm in ARM_ORDER
        ],
        loc="upper left",
        bbox_to_anchor=(0.09, 0.905),
        ncol=3,
        fontsize=6.4,
        borderaxespad=0,
        handletextpad=0.35,
        columnspacing=1.1,
    )
    fig.text(
        0.09,
        0.027,
        "Prospective cohort: 45 matched task-world clusters and 135 persistent campaigns. "
        "Panels a-c are descriptive manipulation and learning summaries; first-recipe "
        "divergence has no same-arm replicate baseline. Panel d reports the prespecified "
        "failure-aware locus decisions; positive values favor selective repair.",
        ha="left",
        va="bottom",
        fontsize=6.35,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-3-prior-uptake-and-correction")


def build_matched_story_rows(
    matched: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cell_rows: list[dict[str, Any]] = []
    for world in matched["world_rows"]:
        for arm in ARM_ORDER:
            cell_rows.append(
                {
                    "world_seed": int(world["world_seed"]),
                    "arm": arm,
                    "pre_error": float(world["errors"][arm]["pre"]),
                    "post_error": float(world["errors"][arm]["post"]),
                }
            )
    contrast_rows = [
        {
            "world_seed": int(row["world_seed"]),
            "primary_contrast": float(row["primary_contrast"]),
            "post_misindexed_minus_aligned": float(row["post_misindexed_minus_aligned"]),
        }
        for row in matched["world_rows"]
    ]
    audit = matched["public_summary_audit"]["by_arm"]["misindexed_nominal"]
    qualitative_rows = [
        {"transition": "Numerical convergence", "count": 5, "denominator": 5},
        {
            "transition": "Saturation / endpoint model",
            "count": int(audit["empirical_saturation_or_endpoint_model_count"]),
            "denominator": int(audit["world_count"]),
        },
        {
            "transition": "Explicitly rejected linear prior",
            "count": int(audit["explicit_supplied_linear_partition_rejection_count"]),
            "denominator": int(audit["world_count"]),
        },
        {
            "transition": "Expressed exact 1.75 law",
            "count": int(audit["exact_1_75_power_law_recovery_count"]),
            "denominator": int(audit["world_count"]),
        },
    ]
    return cell_rows, contrast_rows, qualitative_rows


def build_cross_configuration_matched_rows(
    cross_model: dict[str, Any],
    structural_deepseek: dict[str, Any],
    structural_gpt: dict[str, Any],
    structural_deepseek_low: dict[str, Any],
    structural_identifiability_audit: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    contrast_rows: list[dict[str, Any]] = []
    for block_key, block_label in (
        ("matched_a_p", "A-P"),
        ("matched_a_s_b2", "A-S B2"),
    ):
        block = cross_model["blocks"][block_key]
        for provider_key, configuration_label in (
            ("deepseek", "DeepSeek-v4-flash high"),
            ("gpt", "GPT-5.6-sol medium"),
        ):
            result = block[provider_key]
            primary = result["primary_contrast"]
            contrast_rows.append(
                {
                    "block": block_label,
                    "configuration": configuration_label,
                    "mean_primary_contrast": float(primary["mean"]),
                    "positive_world_count": int(primary["positive_world_count"]),
                    "world_count": int(result["world_count"]),
                    "exact_one_sided_p": float(primary["exact_sign_flip_p_one_sided_greater"]),
                }
            )

    low_primary = structural_deepseek_low["primary_contrast"]
    contrast_rows.append(
        {
            "block": "A-S B2",
            "configuration": "DeepSeek-v4-flash low",
            "mean_primary_contrast": float(low_primary["mean"]),
            "positive_world_count": int(low_primary["positive_world_count"]),
            "world_count": int(low_primary["n"]),
            "exact_one_sided_p": float(low_primary["exact_sign_flip_p_one_sided_greater"]),
        }
    )

    def low_post_count(payload: dict[str, Any]) -> int:
        return sum(
            float(row["errors"]["misindexed_nominal"]["post"]) <= 0.02
            for row in payload["world_rows"]
        )

    identifiability_decision = structural_identifiability_audit["decision"]
    positive_control = structural_identifiability_audit["positive_control"]
    structural_rows = [
        {
            "configuration": "B2 participant-visible design",
            "measure": "Structural-family identifiability supported",
            "count": int(
                bool(identifiability_decision["structural_family_identification_supported"])
            ),
            "denominator": 1,
        },
        {
            "configuration": "B2 free-text expression readout",
            "measure": "Positive control passed",
            "count": int(bool(positive_control["readout_positive_control_passed"])),
            "denominator": 1,
        },
    ]
    for configuration, payload in (
        ("DeepSeek-v4-flash high", structural_deepseek),
        ("GPT-5.6-sol medium", structural_gpt),
        ("DeepSeek-v4-flash low", structural_deepseek_low),
    ):
        audit = payload["public_summary_audit"]["by_arm"]["misindexed_nominal"]
        structural_rows.extend(
            [
                {
                    "configuration": configuration,
                    "measure": "Post error <= 0.02",
                    "count": low_post_count(payload),
                    "denominator": int(audit["world_count"]),
                },
                {
                    "configuration": configuration,
                    "measure": "Expressed exact 1.75 law",
                    "count": int(audit["exact_1_75_power_law_recovery_count"]),
                    "denominator": int(audit["world_count"]),
                },
            ]
        )
    return contrast_rows, structural_rows


def build_b3_cross_model_rows(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model, label in (
        ("deepseek", "DeepSeek-v4-flash high"),
        ("codex", "GPT-5.6-sol medium"),
    ):
        summary = report["models"][model]["overall"]
        measures = (
            (
                "Completed",
                int(summary["completed_cell_count"]),
                int(summary["scheduled_cell_count"]),
            ),
            (
                "Joint law recovery",
                int(summary["failure_aware_joint_recovery_count"]),
                int(summary["scheduled_cell_count"]),
            ),
            (
                "Top-1 action",
                int(summary["failure_aware_top1_count"]),
                int(summary["scheduled_cell_count"]),
            ),
            (
                "Useful action gain",
                int(summary["eligible_gain_at_least_0_02_count"]),
                18,
            ),
        )
        for measure, count, denominator in measures:
            rows.append(
                {
                    "model": model,
                    "model_label": label,
                    "measure": measure,
                    "count": count,
                    "denominator": denominator,
                    "rate": count / denominator,
                }
            )
    return rows


def _c2_gate_summary(locus: str, report: dict[str, Any]) -> dict[str, Any]:
    gate = report["prediction_correction"]["locus_results"][locus]["gate"]
    inference = gate["components"]["H3_primary_contrast"] if locus == "A_E" else gate["inference"]
    return {
        "estimate": float(inference["estimate"]),
        "lower_bound": float(inference["one_sided_95pct_lower_bound"]),
        "p_value": float(
            gate.get(
                "intersection_union_p_value",
                gate.get("effective_intersection_union_p_value"),
            )
        ),
        "passed": bool(gate["passed"]),
    }


def build_c2_cross_model_rows(
    cross_model: dict[str, Any],
    deepseek_report: dict[str, Any],
    codex_report: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    model_rows: list[dict[str, Any]] = []
    locus_rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    detailed = {"deepseek": deepseek_report, "codex": codex_report}
    labels = {
        "deepseek": "DeepSeek-v4-flash high",
        "codex": "GPT-5.6-sol medium",
    }
    summary_fields = (
        "scheduled_cell_count",
        "terminal_completion_rate",
        "prediction_scored_count",
        "mean_prediction_improvement",
        "mean_effective_final_error",
        "law_evaluated_count",
        "mean_law_mae",
        "mean_law_compression_loss",
        "blind_gain_evaluable_count",
        "mean_blind_gain",
        "blind_better_count",
        "blind_equivalent_count",
        "blind_worse_count",
    )
    for model in ("deepseek", "codex"):
        overall = cross_model["models"][model]["overall"]
        model_rows.append(
            {
                "model": model,
                "model_label": labels[model],
                **{key: overall[key] for key in summary_fields},
            }
        )
        for locus in ("A_E", "A_P", "A_S"):
            locus_summary = cross_model["models"][model]["by_locus"][locus]
            locus_rows.append(
                {
                    "model": model,
                    "model_label": labels[model],
                    "locus": locus,
                    **{key: locus_summary[key] for key in summary_fields},
                }
            )
            gate_rows.append(
                {
                    "model": model,
                    "model_label": labels[model],
                    "locus": locus,
                    **_c2_gate_summary(locus, detailed[model]),
                }
            )
    return model_rows, locus_rows, gate_rows


def build_action_extension_rows(
    report: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    condition_rows: list[dict[str, Any]] = []
    contrast_rows: list[dict[str, Any]] = []
    labels = {
        "deepseek": "DeepSeek-v4-flash high",
        "codex": "GPT-5.6-sol medium",
    }
    for model in ("deepseek", "codex"):
        primary = report["models"][model]["primary_all_scheduled"]
        for condition, summary in primary["condition_summaries"].items():
            condition_rows.append(
                {
                    "model": model,
                    "model_label": labels[model],
                    "condition": condition,
                    "row_count": int(summary["row_count"]),
                    "completed_count": int(summary["completed_count"]),
                    "mean_failure_aware_normalized_regret": float(
                        summary["mean_failure_aware_normalized_regret"]
                    ),
                    "top1_rate": float(summary["top1_rate"]),
                    "within_0_01_rate": float(summary["within_0_01_rate"]),
                }
            )
        for row in primary["contrasts"]:
            interval = row["task_stratified_task_world_cluster_bootstrap_95_interval"]
            contrast_rows.append(
                {
                    "model": model,
                    "model_label": labels[model],
                    "contrast": row["contrast"],
                    "paired_stratum_count": int(row["paired_stratum_count"]),
                    "mean_regret_difference": float(
                        row["mean_failure_aware_normalized_regret_difference"]
                    ),
                    "interval_low": float(interval[0]),
                    "interval_high": float(interval[1]),
                    "mean_top1_difference": float(row["mean_top1_difference"]),
                }
            )
    return condition_rows, contrast_rows


def render_figure_4_matched(
    cell_rows: list[dict[str, Any]],
    cross_configuration_rows: list[dict[str, Any]],
    b3_rows: list[dict[str, Any]],
) -> list[Path]:
    fig = plt.figure(figsize=(7.2, 5.70))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.105,
        right=0.985,
        bottom=0.18,
        top=0.76,
        wspace=0.34,
        hspace=0.58,
        width_ratios=[1.05, 0.95],
    )
    ax_a, ax_b, ax_c, ax_d = [
        fig.add_subplot(grid[row, col]) for row in range(2) for col in range(2)
    ]

    for arm_index, arm in enumerate(ARM_ORDER):
        rows = sorted(
            (row for row in cell_rows if row["arm"] == arm),
            key=lambda row: row["world_seed"],
        )
        offset = (arm_index - 1) * 0.045
        for row in rows:
            ax_a.plot(
                [0 + offset, 1 + offset],
                [row["pre_error"], row["post_error"]],
                color=ARM_COLOR[arm],
                alpha=0.55,
                linewidth=1.0,
            )
            ax_a.scatter(
                [0 + offset, 1 + offset],
                [row["pre_error"], row["post_error"]],
                s=18,
                color=ARM_COLOR[arm],
                edgecolor="white",
                linewidth=0.4,
                zorder=3,
            )
    ax_a.set_xticks([0, 1], ["Before matched evidence", "After matched evidence"])
    ax_a.set_ylim(0, 0.49)
    ax_a.set_ylabel("Normalized prediction error")
    ax_a.set_title(
        "DeepSeek-v4-flash high: all arms end with\nlow error after the same packet and extra turn",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_a)
    panel_label(ax_a, "a", x=-0.13)

    post_by_arm = [
        [row["post_error"] for row in cell_rows if row["arm"] == arm] for arm in ARM_ORDER
    ]
    boxes = ax_b.boxplot(
        post_by_arm,
        positions=np.arange(3),
        widths=0.52,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": COLORS["ink"], "linewidth": 1.1},
        whiskerprops={"color": "#87969D", "linewidth": 0.8},
        capprops={"color": "#87969D", "linewidth": 0.8},
        boxprops={"color": "#87969D", "linewidth": 0.8},
    )
    for patch, arm in zip(boxes["boxes"], ARM_ORDER, strict=True):
        patch.set_facecolor(ARM_COLOR[arm])
        patch.set_alpha(0.24)
    for index, (arm, values) in enumerate(zip(ARM_ORDER, post_by_arm, strict=True)):
        ax_b.scatter(
            index + deterministic_offsets(len(values), 0.13),
            values,
            s=24,
            color=ARM_COLOR[arm],
            edgecolor="white",
            linewidth=0.45,
            zorder=3,
        )
        ax_b.text(
            index,
            0.0124,
            f"mean {np.mean(values):.4f}",
            ha="center",
            va="bottom",
            fontsize=6.1,
            color=COLORS["muted"],
        )
    ax_b.set_xticks(range(3), [ARM_LABEL[arm] for arm in ARM_ORDER])
    ax_b.set_ylim(0, 0.0142)
    ax_b.set_ylabel("Post-evidence normalized error")
    ax_b.set_title(
        "DeepSeek-v4-flash high: predictions converge\nacross initial-model conditions",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_b)
    panel_label(ax_b, "b", x=-0.13)

    configuration_colors = {
        "DeepSeek-v4-flash high": COLORS["blue"],
        "GPT-5.6-sol medium": COLORS["violet"],
        "DeepSeek-v4-flash low": COLORS["misindexed"],
    }
    configuration_markers = {
        "DeepSeek-v4-flash high": "o",
        "GPT-5.6-sol medium": "D",
        "DeepSeek-v4-flash low": "^",
    }
    y_positions = np.arange(len(cross_configuration_rows))
    ax_c.axvline(0, color="#89989F", linewidth=1.0)
    for y_value, row in zip(y_positions, cross_configuration_rows, strict=True):
        value = row["mean_primary_contrast"]
        ax_c.scatter(
            value,
            y_value,
            s=48,
            marker=configuration_markers[row["configuration"]],
            color=configuration_colors[row["configuration"]],
            edgecolor="white",
            linewidth=0.7,
            zorder=3,
        )
        label_on_left = value > 0.08
        ax_c.text(
            value - 0.004 if label_on_left else value + 0.004,
            y_value,
            f"{value:+.4f} ({row['positive_world_count']}/{row['world_count']} +)",
            ha="right" if label_on_left else "left",
            va="center",
            fontsize=6.1,
            color=COLORS["muted"],
        )
    ax_c.axhline(1.5, color=COLORS["grid"], linewidth=0.8)
    ax_c.set_yticks(
        y_positions,
        [f"{row['block']} · {row['configuration']}" for row in cross_configuration_rows],
    )
    ax_c.set_xlim(-0.06, 0.13)
    ax_c.invert_yaxis()
    ax_c.set_xlabel("Mean misspecified - aligned update gain")
    ax_c.set_title(
        "Matched numerical-update contrasts\nacross replicated configurations",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_row_axis(ax_c)
    panel_label(ax_c, "c", x=-0.13)

    measure_order = [
        "Completed",
        "Joint law recovery",
        "Top-1 action",
        "Useful action gain",
    ]
    model_order = ["deepseek", "codex"]
    model_colors = {"deepseek": COLORS["blue"], "codex": COLORS["violet"]}
    centers = np.arange(len(measure_order), dtype=float)
    width = 0.34
    for model_index, model in enumerate(model_order):
        model_rows = {row["measure"]: row for row in b3_rows if row["model"] == model}
        x = centers + (model_index - 0.5) * width
        values = [float(model_rows[measure]["rate"]) for measure in measure_order]
        bars = ax_d.bar(
            x,
            values,
            width=width * 0.92,
            color=model_colors[model],
            edgecolor="white",
            linewidth=0.6,
            label=model_rows[measure_order[0]]["model_label"],
        )
        for bar, measure in zip(bars, measure_order, strict=True):
            row = model_rows[measure]
            y = max(float(row["rate"]), 0.015) + 0.025
            ax_d.text(
                bar.get_x() + bar.get_width() / 2,
                y,
                f"{row['count']}/{row['denominator']}",
                ha="center",
                va="bottom",
                fontsize=5.7,
                color=COLORS["ink"],
                rotation=90 if measure == "Completed" else 0,
            )
    ax_d.set_xticks(
        centers,
        ["Completed", "Correct\nfamily + 1.75", "Top-1", "Gain\n$\\geq .02$"],
    )
    ax_d.set_ylim(0, 1.16)
    ax_d.set_yticks(np.linspace(0, 1, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 1, 6)])
    ax_d.set_ylabel("Failure-aware rate")
    ax_d.set_title(
        "Joint law recovery coexists with\nno useful-gain successes",
        loc="left",
        fontweight="bold",
        pad=6,
    )
    style_quant_axis(ax_d)
    ax_d.legend(loc="upper right", fontsize=5.6)
    panel_label(ax_d, "d", x=-0.13)

    configuration_count = 3
    structural_session_count = 15 * configuration_count

    fig.suptitle(
        "B2 numerical-expression dissociation; B3 sparse structural recovery",
        x=0.105,
        y=0.975,
        ha="left",
        fontsize=11.4,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.105,
        0.912,
        f"B2: {structural_session_count}/{structural_session_count} post-packet summaries; "
        "family underidentified",
        ha="left",
        va="center",
        fontsize=6.6,
        fontweight="bold",
        color=COLORS["green"],
        bbox={"facecolor": "#EAF5EE", "edgecolor": "none", "pad": 2.0},
    )
    fig.text(
        0.535,
        0.912,
        "B3: 5/60 joint recoveries; 0/36 scheduled useful gains",
        ha="left",
        va="center",
        fontsize=7.0,
        fontweight="bold",
        color=COLORS["red"],
        bbox={"facecolor": "#FBEDEE", "edgecolor": "none", "pad": 2.0},
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D(
                [], [], marker="o", linestyle="", color=ARM_COLOR[arm], label=ARM_LABEL[arm]
            )
            for arm in ARM_ORDER
        ],
        loc="upper left",
        bbox_to_anchor=(0.105, 0.872),
        ncol=3,
        fontsize=6.4,
        borderaxespad=0,
        handletextpad=0.35,
        columnspacing=1.1,
    )
    fig.text(
        0.105,
        0.020,
        "Panels a-b show DeepSeek-v4-flash-high B2 conditional post-packet results; panel c adds "
        "matched GPT-5.6-sol-medium and DeepSeek-v4-flash-low results. All configurations end with "
        "low post-packet error, while misindexed summaries express the exact 1.75 law in "
        "0/5 worlds. The one-pair packet has an exact linear/power alias, so B2 does not "
        "test participant-level structural identification. Panel d reports the separate "
        "reference-fitter-identifiable B3 surface: "
        "DeepSeek has 13 retained schema failures, GPT recovers 5/30 joint laws, and "
        "neither model realizes a registered useful action gain (0/18 scheduled "
        "opportunities). Five-world and model "
        "comparisons are descriptive; no capability-ranking test is performed.",
        ha="left",
        va="bottom",
        fontsize=6.25,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-4-matched-evidence-localization")


def main() -> int:
    configure_matplotlib()
    design_path = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
    preflight_path = (
        ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json"
    )
    publication_reanalysis_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-w2-64-publication-reanalysis-v0.1.json"
    )
    open_action_audit_path = ROOT / (
        "workstreams/flagship_tasks/reports/WORK_II_MULTI_TASK_OPEN_ACTION_FORMAL_AUDIT_ZH.md"
    )
    evidence_to_action_formal_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-evidence-to-action-formal-closeout-v0.1.json"
    )
    large_grid_construction_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-evidence-to-action-large-grid-v1.0-construction-closeout.json"
    )
    large_grid_qualification_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-evidence-to-action-large-grid-v1.0-qualification-closeout.json"
    )
    gate_alignment_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-evidence-to-action-gate-alignment-v0.1.json"
    )
    reviewer_controls_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-reviewer-control-analyses-v0.1.json"
    )
    public_source_dir = ROOT / (
        "workstreams/flagship_tasks/reports/figures/work-ii-deepseek-c2-public/current/source_data"
    )
    checkpoint_summary_path = public_source_dir / "checkpoint_error_summary.csv"
    experiment_metrics_path = public_source_dir / "experiment_metrics.csv"
    story_analysis_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-deepseek-c2-paper-story-analysis-v0.1.json"
    )
    matched_evidence_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-study-b-matched-evidence-results-v0.1.json"
    )
    structural_matched_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-as-study-b2-phase-process-results-v0.1.json"
    )
    structural_matched_gpt_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-as-study-b2-gpt56-sol-medium-results-v0.1.json"
    )
    structural_matched_deepseek_low_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-as-study-b2-deepseek-v4-flash-low-results-v0.1.json"
    )
    structural_identifiability_audit_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-b2-participant-visible-identifiability-audit-v0.1.json"
    )
    cross_model_closeout_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-w2-59-cross-model-main-evidence-closeout-v0.1.json"
    )
    deepseek_c2_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
    )
    codex_c2_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json"
    )
    cross_model_c2_path = ROOT / (
        "workstreams/flagship_tasks/reports/"
        "work-ii-w2-62-c2-cross-model-current-composite-v0.1.json"
    )
    b3_cross_model_path = ROOT / (
        "workstreams/flagship_tasks/reports/work-ii-w2-63-b3-failure-aware-cross-model-v0.1.json"
    )
    source_paths = [
        SCRIPT_PATH,
        design_path,
        preflight_path,
        publication_reanalysis_path,
        open_action_audit_path,
        evidence_to_action_formal_path,
        large_grid_construction_path,
        large_grid_qualification_path,
        gate_alignment_path,
        reviewer_controls_path,
        checkpoint_summary_path,
        experiment_metrics_path,
        story_analysis_path,
        matched_evidence_path,
        structural_matched_path,
        structural_matched_gpt_path,
        structural_matched_deepseek_low_path,
        structural_identifiability_audit_path,
        cross_model_closeout_path,
        deepseek_c2_path,
        codex_c2_path,
        cross_model_c2_path,
        b3_cross_model_path,
    ]

    design = json.loads(design_path.read_text(encoding="utf-8"))
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    publication_reanalysis = json.loads(publication_reanalysis_path.read_text(encoding="utf-8"))
    open_action_summary = publication_reanalysis["w2_50"]
    evidence_to_action_formal = json.loads(
        evidence_to_action_formal_path.read_text(encoding="utf-8")
    )
    large_grid_construction = json.loads(large_grid_construction_path.read_text(encoding="utf-8"))
    large_grid_qualification = json.loads(large_grid_qualification_path.read_text(encoding="utf-8"))
    gate_alignment = json.loads(gate_alignment_path.read_text(encoding="utf-8"))
    reviewer_controls = json.loads(reviewer_controls_path.read_text(encoding="utf-8"))
    story_analysis = json.loads(story_analysis_path.read_text(encoding="utf-8"))
    structural_matched = json.loads(structural_matched_path.read_text(encoding="utf-8"))
    structural_matched_gpt = json.loads(structural_matched_gpt_path.read_text(encoding="utf-8"))
    structural_matched_deepseek_low = json.loads(
        structural_matched_deepseek_low_path.read_text(encoding="utf-8")
    )
    structural_identifiability_audit = json.loads(
        structural_identifiability_audit_path.read_text(encoding="utf-8")
    )
    cross_model_closeout = json.loads(cross_model_closeout_path.read_text(encoding="utf-8"))
    action_extension = publication_reanalysis["action_extension"]
    deepseek_c2 = json.loads(deepseek_c2_path.read_text(encoding="utf-8"))
    codex_c2 = json.loads(codex_c2_path.read_text(encoding="utf-8"))
    cross_model_c2 = json.loads(cross_model_c2_path.read_text(encoding="utf-8"))
    b3_cross_model = json.loads(b3_cross_model_path.read_text(encoding="utf-8"))
    if preflight.get("formal_execution_allowed") is not False:
        raise ValueError("expected an outcome-blind execution-blocked formal preflight")
    if open_action_summary.get("scheduled_cell_count") != 45:
        raise ValueError("unexpected W2-50 scheduled cell denominator")
    if open_action_summary.get("eligible_cell_count") != 42:
        raise ValueError("unexpected W2-50 eligible cell denominator")
    if open_action_summary.get("provider_free_truth_query_count") != 240:
        raise ValueError("unexpected W2-50 truth denominator")
    if open_action_summary.get("provider_free_exact_replay_count") != 240:
        raise ValueError("unexpected W2-50 exact-replay denominator")
    expected_w2_51_counts = {
        "attempted_cluster_count": 8,
        "qualified_cluster_count": 7,
        "scientifically_rejected_cluster_count": 1,
        "not_started_cluster_count": 7,
    }
    formal_preparation = evidence_to_action_formal["formal_preparation"]
    for field, expected in expected_w2_51_counts.items():
        if formal_preparation.get(field) != expected:
            raise ValueError(
                f"unexpected W2-51 {field}: {formal_preparation.get(field)!r} != {expected}"
            )
    if large_grid_construction.get("passed_unit_count") != 7:
        raise ValueError("unexpected W2-52 exposed construction denominator")
    if large_grid_qualification.get("complete_cluster_count") != 1:
        raise ValueError("unexpected W2-52 fresh qualification denominator")
    if large_grid_qualification.get("not_started_cluster_count") != 14:
        raise ValueError("unexpected W2-52 unstarted denominator")
    if gate_alignment.get("completed_unit_version_count") != 16:
        raise ValueError("unexpected W2-53 unit-version denominator")
    if gate_alignment.get("new_truth_execution_count") != 0:
        raise ValueError("W2-53 must remain a zero-execution diagnostic")
    if reviewer_controls["w2_50_continuous_action"].get("eligible_cell_count") != 42:
        raise ValueError("unexpected reviewer-control W2-50 denominator")
    if reviewer_controls["typed_law_schema_capacity"].get("completed_cell_count") != 135:
        raise ValueError("unexpected reviewer-control schema-capacity denominator")
    if action_extension.get("scheduled_condition_slots_total") != 360:
        raise ValueError("unexpected W2-61 four-condition denominator")
    if deepseek_c2["denominators"].get("cell_count") != 135:
        raise ValueError("unexpected DeepSeek C2 denominator")
    if codex_c2["denominators"].get("cell_count") != 135:
        raise ValueError("unexpected Codex C2 denominator")
    if b3_cross_model.get("scheduled_cells_by_model") != {
        "codex": 30,
        "deepseek": 30,
    }:
        raise ValueError("unexpected W2-63 B3 denominators")

    checkpoint_rows = read_csv(checkpoint_summary_path)
    experiment_rows = read_csv(experiment_metrics_path)
    locus_decisions = story_analysis["current_composite_evaluator"]["locus_decisions"]
    (
        initial_rows,
        recipe_rows,
        improvement_rows,
        decision_rows,
    ) = build_prospective_story_rows(
        checkpoint_rows,
        experiment_rows,
        locus_decisions,
    )
    write_csv(
        SOURCE_DIR / "figure-3-initial-prediction-error.csv",
        initial_rows,
        ["locus", "arm", "mean_normalized_mae"],
    )
    write_csv(
        SOURCE_DIR / "figure-3-first-recipe-divergence.csv",
        recipe_rows,
        [
            "comparison",
            "different_first_recipe_count",
            "matched_cluster_count",
            "different_fraction",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-3-prediction-improvement.csv",
        improvement_rows,
        ["locus", "arm", "mean_pre_to_final_improvement"],
    )
    write_csv(
        SOURCE_DIR / "figure-3-locus-decisions.csv",
        decision_rows,
        ["locus", "primary_estimate", "p_value", "passed"],
    )

    matched_cell_rows, matched_contrast_rows, matched_qualitative_rows = build_matched_story_rows(
        structural_matched
    )
    cross_configuration_rows, structural_control_rows = build_cross_configuration_matched_rows(
        cross_model_closeout,
        structural_matched,
        structural_matched_gpt,
        structural_matched_deepseek_low,
        structural_identifiability_audit,
    )
    b3_rows = build_b3_cross_model_rows(b3_cross_model)
    c2_model_rows, c2_locus_rows, c2_gate_rows = build_c2_cross_model_rows(
        cross_model_c2,
        deepseek_c2,
        codex_c2,
    )
    action_condition_rows, action_contrast_rows = build_action_extension_rows(action_extension)
    write_csv(
        SOURCE_DIR / "figure-4-matched-structural-cells.csv",
        matched_cell_rows,
        ["world_seed", "arm", "pre_error", "post_error"],
    )
    write_csv(
        SOURCE_DIR / "figure-4-matched-structural-contrasts.csv",
        matched_contrast_rows,
        ["world_seed", "primary_contrast", "post_misindexed_minus_aligned"],
    )
    write_csv(
        SOURCE_DIR / "figure-4-matched-expression-diagnostic.csv",
        matched_qualitative_rows,
        ["transition", "count", "denominator"],
    )
    write_csv(
        SOURCE_DIR / "figure-4-cross-configuration-contrasts.csv",
        cross_configuration_rows,
        [
            "block",
            "configuration",
            "mean_primary_contrast",
            "positive_world_count",
            "world_count",
            "exact_one_sided_p",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-4-structural-identification-control.csv",
        structural_control_rows,
        ["configuration", "measure", "count", "denominator"],
    )
    write_csv(
        SOURCE_DIR / "figure-4-b3-cross-model.csv",
        b3_rows,
        ["model", "model_label", "measure", "count", "denominator", "rate"],
    )
    write_csv(
        SOURCE_DIR / "figure-5-c2-model-summary.csv",
        c2_model_rows,
        [
            "model",
            "model_label",
            "scheduled_cell_count",
            "terminal_completion_rate",
            "prediction_scored_count",
            "mean_prediction_improvement",
            "mean_effective_final_error",
            "law_evaluated_count",
            "mean_law_mae",
            "mean_law_compression_loss",
            "blind_gain_evaluable_count",
            "mean_blind_gain",
            "blind_better_count",
            "blind_equivalent_count",
            "blind_worse_count",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-5-c2-locus-summary.csv",
        c2_locus_rows,
        [
            "model",
            "model_label",
            "locus",
            "scheduled_cell_count",
            "terminal_completion_rate",
            "prediction_scored_count",
            "mean_prediction_improvement",
            "mean_effective_final_error",
            "law_evaluated_count",
            "mean_law_mae",
            "mean_law_compression_loss",
            "blind_gain_evaluable_count",
            "mean_blind_gain",
            "blind_better_count",
            "blind_equivalent_count",
            "blind_worse_count",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-5-c2-selective-correction.csv",
        c2_gate_rows,
        [
            "model",
            "model_label",
            "locus",
            "estimate",
            "lower_bound",
            "p_value",
            "passed",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-6-four-condition-summary.csv",
        action_condition_rows,
        [
            "model",
            "model_label",
            "condition",
            "row_count",
            "completed_count",
            "mean_failure_aware_normalized_regret",
            "top1_rate",
            "within_0_01_rate",
        ],
    )
    write_csv(
        SOURCE_DIR / "figure-6-four-condition-contrasts.csv",
        action_contrast_rows,
        [
            "model",
            "model_label",
            "contrast",
            "paired_stratum_count",
            "mean_regret_difference",
            "interval_low",
            "interval_high",
            "mean_top1_difference",
        ],
    )
    open_action_rows = normalize_open_action_rows(open_action_summary)
    write_csv(
        SOURCE_DIR / "figure-6-open-action-formal.csv",
        open_action_rows,
        [
            "participant_model",
            "cell_id",
            "cluster_id",
            "task_id",
            "world_seed",
            "arm",
            "status",
            "eligible",
            "selected_rank",
            "normalized_regret",
            "top1_selected",
            "law_adequate",
            "law_normalized_mae",
            "mechanism_action_category",
            "selected_minus_random_candidate_mean",
        ],
    )
    qualification_funnel_rows = [
        {
            "block": "w2_51_96_grid_fresh_formal_preparation",
            "evidence_role": "fresh_formal_preparation",
            "planned": 15,
            "passed": 7,
            "scientifically_rejected": 1,
            "not_started": 7,
            "participant_sessions": 0,
        },
        {
            "block": "w2_52_320_grid_exposed_construction",
            "evidence_role": "exposed_construction_only",
            "planned": 7,
            "passed": 7,
            "scientifically_rejected": 0,
            "not_started": 0,
            "participant_sessions": 0,
        },
        {
            "block": "w2_52_320_grid_fresh_prospective",
            "evidence_role": "fresh_prospective_qualification",
            "planned": 15,
            "passed": 0,
            "scientifically_rejected": 1,
            "not_started": 14,
            "participant_sessions": 0,
        },
    ]
    write_csv(
        SOURCE_DIR / "figure-6-qualification-funnel.csv",
        qualification_funnel_rows,
        [
            "block",
            "evidence_role",
            "planned",
            "passed",
            "scientifically_rejected",
            "not_started",
            "participant_sessions",
        ],
    )
    gate_alignment_fields = [
        "group_id",
        "evidence_role",
        "grid_query_count",
        "task_id",
        "world_seed",
        "spearman_rank_correlation",
        "normalized_regret",
        "rank_gate_passed",
        "top1",
        "within_0_01_of_best",
    ]
    gate_alignment_rows = [
        {field: row[field] for field in gate_alignment_fields}
        for row in gate_alignment["unit_rows"]
    ]
    write_csv(
        SOURCE_DIR / "figure-6-gate-alignment-units.csv",
        gate_alignment_rows,
        gate_alignment_fields,
    )
    continuous_fields = [
        "cell_id",
        "cluster_id",
        "task_id",
        "world_seed",
        "arm",
        "law_normalized_mae",
        "selected_rank",
        "normalized_regret",
        "top1_selected",
    ]
    continuous_rows = [
        {field: row[field] for field in continuous_fields}
        for row in reviewer_controls["w2_50_continuous_action"]["cell_rows"]
    ]
    write_csv(
        SOURCE_DIR / "figure-6-law-action-continuous.csv",
        continuous_rows,
        continuous_fields,
    )
    threshold_fields = [
        "law_mae_threshold",
        "adequate_law_correct_action",
        "adequate_law_wrong_action",
        "inadequate_law_correct_action",
        "inadequate_law_wrong_action",
    ]
    threshold_rows = [
        {field: row[field] for field in threshold_fields}
        for row in reviewer_controls["w2_50_continuous_action"]["threshold_sensitivity"]
    ]
    write_csv(
        SOURCE_DIR / "figure-6-law-threshold-sensitivity.csv",
        threshold_rows,
        threshold_fields,
    )
    decision_aligned_fields = [
        "participant_model",
        "law_source",
        "cell_id",
        "cluster_id",
        "task_id",
        "world_seed",
        "prior_arm",
        "law_normalized_mae",
        "law_status",
        "law_implied_top1",
        "law_implied_normalized_regret",
        "participant_top1",
        "participant_normalized_regret",
        "law_implied_top1_followed",
        "law_action_spearman_rank_correlation",
        "law_action_pairwise_agreement",
        "action_utilization_delta",
        "law_action_quadrant",
    ]
    decision_aligned_rows = [
        {field: row[field] for field in decision_aligned_fields}
        for row in open_action_summary["decision_aligned_law_action"]["cell_rows"]
    ]
    write_csv(
        SOURCE_DIR / "figure-6-decision-aligned-law-action.csv",
        decision_aligned_rows,
        decision_aligned_fields,
    )

    outputs = {
        "figure_1": render_figure_1(),
        "figure_2": render_figure_2(design, preflight),
        "figure_3": render_figure_3_prospective(
            initial_rows,
            recipe_rows,
            improvement_rows,
            decision_rows,
        ),
        "figure_4": render_figure_4_matched(
            matched_cell_rows,
            cross_configuration_rows,
            b3_rows,
        ),
        "figure_5": render_figure_5_cross_model_c2(
            c2_model_rows,
            c2_locus_rows,
            c2_gate_rows,
        ),
        "figure_6": render_figure_6_open_action(
            open_action_rows,
            open_action_summary,
            evidence_to_action_formal,
            large_grid_construction,
            large_grid_qualification,
            gate_alignment,
            reviewer_controls,
            action_extension,
        ),
    }
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-prior-discovery-figure-manifest-0.1",
        "status": "formal_results_with_bounded_secondary_analyses",
        "backend": "python_matplotlib",
        "formal_hypothesis_tests_run": False,
        "provider_groups_mixed_in_scientific_contrasts": False,
        "source_bindings": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(path),
            }
            for path in source_paths
        ],
        "source_data": {
            "prospective_initial_rows": len(initial_rows),
            "prospective_recipe_comparisons": len(recipe_rows),
            "prospective_improvement_rows": len(improvement_rows),
            "prospective_locus_decisions": len(decision_rows),
            "matched_structural_cell_rows": len(matched_cell_rows),
            "matched_structural_contrast_rows": len(matched_contrast_rows),
            "matched_exact_law_expression_rows": len(matched_qualitative_rows),
            "matched_cross_configuration_rows": len(cross_configuration_rows),
            "matched_structural_control_rows": len(structural_control_rows),
            "b3_cross_model_rows": len(b3_rows),
            "c2_model_rows": len(c2_model_rows),
            "c2_locus_rows": len(c2_locus_rows),
            "c2_gate_rows": len(c2_gate_rows),
            "action_condition_rows": len(action_condition_rows),
            "action_contrast_rows": len(action_contrast_rows),
            "open_action_rows": len(open_action_rows),
            "open_action_eligible_rows": sum(row["eligible"] for row in open_action_rows),
            "qualification_funnel_rows": len(qualification_funnel_rows),
            "gate_alignment_unit_rows": len(gate_alignment_rows),
            "law_action_continuous_rows": len(continuous_rows),
            "law_threshold_rows": len(threshold_rows),
            "decision_aligned_law_action_rows": len(decision_aligned_rows),
        },
        "figures": {
            figure_id: [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
                for path in paths
            ]
            for figure_id, paths in outputs.items()
        },
        "interpretation_limits": [
            "Figure 1 states the identification problem; Figure 2 separates executed "
            "evidence from future portability studies.",
            "Figure 3 combines the prospective formal locus decisions with retrospective "
            "manipulation summaries; first-recipe divergence has no same-arm replicate "
            "baseline.",
            "Figure 4 combines conditional post-packet B2 results across three configurations with "
            "the failure-aware two-model B3 control. B2 has an exact participant-visible "
            "linear/power alias and supports an expression, not structural-identification, "
            "readout; B3 supplies the typed reference-fitter-identifiable test. No "
            "configuration-superiority test is performed.",
            "Figure 4 includes the complete DeepSeek-low A-S B2 ablation; the incomplete "
            "A-P low block is excluded.",
            "Figure 5 compares fully scheduled 135-cell DeepSeek-v4-flash and GPT-5.6-sol "
            "C2 surfaces; model differences are matched descriptive and not provider "
            "causal effects.",
            "Figure 6 combines the four-condition action successor, the DeepSeek longitudinal "
            "decision-aligned law-action analysis and the frozen gate-action diagnostic.",
            "The four-condition block is development successor evidence; yoked recipient "
            "failures remain in the failure-aware denominator and prevent a pure "
            "experiment-selection interpretation.",
            "The 96- and 320-query controls contain zero participant sessions; exposed "
            "construction and fresh qualification remain separate evidence roles.",
            "The gate-alignment diagnostic reproduces 16 frozen unit versions without new "
            "truth, provider or physical execution and does not revise historical stop "
            "decisions.",
            "No cross-provider capability ranking or context-reset portability claim is supported.",
        ],
    }
    manifest["manifest_sha256"] = canonical_sha(manifest)
    (OUTPUT_DIR / "figure_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "completed",
                "figures": len(outputs),
                "prospective_story_rows": len(initial_rows)
                + len(recipe_rows)
                + len(improvement_rows)
                + len(decision_rows),
                "matched_story_rows": len(matched_cell_rows)
                + len(matched_contrast_rows)
                + len(matched_qualitative_rows),
                "manifest_sha256": manifest["manifest_sha256"],
                "output_dir": str(OUTPUT_DIR),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
