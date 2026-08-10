#!/usr/bin/env python3
"""Render the first three figures for the prior-correction manuscript."""

from __future__ import annotations

import csv
import hashlib
import json
import textwrap
from pathlib import Path
from typing import Any, Iterable

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

    # a — matched prior intervention
    ax_a.set_title("Change the prior, not the world", loc="left", fontweight="bold", pad=5)
    arm_specs = [
        ("Opaque", "Anonymous IDs\nNo task dossier", COLORS["opaque"], "#EEF1F2"),
        ("Aligned", "Useful nominal\nproperties", COLORS["aligned"], COLORS["teal_light"]),
        ("Misindexed", "Same properties\nWrong ID mapping", COLORS["misindexed"], COLORS["orange_light"]),
    ]
    for index, (name, detail, edge, face) in enumerate(arm_specs):
        x = 0.02 + index * 0.325
        rounded_box(
            ax_a,
            x,
            0.61,
            0.285,
            0.25,
            f"{name}\n{detail}",
            facecolor=face,
            edgecolor=edge,
            fontsize=6.6,
            fontweight="bold" if index else "normal",
        )
        arrow(ax_a, (x + 0.142, 0.60), (0.50, 0.42), color=edge)
    rounded_box(
        ax_a,
        0.22,
        0.16,
        0.56,
        0.24,
        "One fixed executable chemical world\nMatched operations, evidence budget, noise and safety",
        facecolor=COLORS["blue_light"],
        edgecolor=COLORS["blue"],
        fontsize=7.1,
        fontweight="bold",
    )
    ax_a.text(
        0.50,
        0.07,
        "Only the agent-facing dossier changes",
        ha="center",
        va="center",
        fontsize=6.8,
        color=COLORS["muted"],
    )
    panel_label(ax_a, "a")

    # b — persistent campaign loop
    ax_b.set_title("One session controls a complete campaign", loc="left", fontweight="bold", pad=5)
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
        "Four complete experiments; checkpoints after 0, 1, 2 and 4",
        ha="center",
        fontsize=6.6,
        color=COLORS["muted"],
    )
    panel_label(ax_b, "b")

    # c — evidence separation
    ax_c.set_title("Score understanding after the campaign", loc="left", fontweight="bold", pad=5)
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
    ax_d.set_title("Classify what the agent actually achieved", loc="left", fontweight="bold", pad=5)
    x0, y0, width, height = 0.20, 0.17, 0.72, 0.66
    ax_d.add_patch(Rectangle((x0, y0), width, height, facecolor="none", edgecolor=COLORS["ink"], linewidth=0.9))
    ax_d.plot([x0 + width / 2, x0 + width / 2], [y0, y0 + height], color=COLORS["grid"], linewidth=1.0)
    ax_d.plot([x0, x0 + width], [y0 + height / 2, y0 + height / 2], color=COLORS["grid"], linewidth=1.0)
    cells = [
        (x0, y0 + height / 2, COLORS["red_light"], "States a law,\ndoes not act"),
        (x0 + width / 2, y0 + height / 2, COLORS["green_light"], "Reusable law\nunderstands + acts"),
        (x0, y0, "#F0F2F3", "Neither"),
        (x0 + width / 2, y0, COLORS["orange_light"], "Endpoint heuristic\nacts without law"),
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
            fontweight="bold" if "Reusable" in label else "normal",
            color=COLORS["ink"],
        )
    ax_d.text(0.56, 0.06, "Evidence-aligned action →", ha="center", fontsize=6.7, color=COLORS["muted"])
    ax_d.text(0.08, 0.50, "Predictive\nrecovery →", ha="center", va="center", fontsize=6.7, color=COLORS["muted"], rotation=90)
    panel_label(ax_d, "d")

    fig.suptitle(
        "A useful endpoint is not sufficient evidence of law discovery",
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
        "The prior is manipulated under one fixed world; predictions, experiments, executable summaries and blind outcomes are evaluated as separate evidence channels.",
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
        or expected["complete_experiments"] != 300
    ):
        raise ValueError("formal design denominators do not match the frozen figure contract")

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

    ax_a.set_title("Five heterogeneous task families define the public cohort", loc="left", fontweight="bold", pad=5)
    task_colors = [COLORS["blue"], COLORS["aligned"], COLORS["misindexed"], COLORS["violet"], COLORS["red"]]
    short_names = ["Electrochemical", "Crystallization", "Distillation", "Partition", "Safety-constrained"]
    mechanisms = [
        "transport + selectivity",
        "reaction + solid formation",
        "reaction + phase separation",
        "liquid partition",
        "kinetics + thermal safety",
    ]
    for index, (name, mechanism, color) in enumerate(zip(short_names, mechanisms, task_colors)):
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
            ax_a.add_patch(Circle((x + 0.032 + seed * 0.029, 0.25), 0.010, facecolor=color, edgecolor="white", linewidth=0.35))
        ax_a.text(x + 0.09, 0.13, "5 public worlds", ha="center", fontsize=6.1, color=COLORS["muted"])
    ax_a.text(
        0.50,
        0.02,
        "Development, public-formal and private-confirmation identities are disjoint",
        ha="center",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    panel_label(ax_a, "a", x=-0.018)

    ax_b.set_title("One independent world cluster", loc="left", fontweight="bold", pad=5)
    y_positions = [0.72, 0.49, 0.26]
    for arm, y in zip(ARM_ORDER, y_positions):
        color = ARM_COLOR[arm]
        rounded_box(
            ax_b,
            0.02,
            y - 0.07,
            0.22,
            0.14,
            ARM_LABEL[arm],
            facecolor="#F7F9FA",
            edgecolor=color,
            fontsize=6.6,
            fontweight="bold",
        )
        for experiment in range(4):
            x = 0.33 + experiment * 0.15
            ax_b.add_patch(
                Rectangle(
                    (x, y - 0.045),
                    0.105,
                    0.09,
                    facecolor=color,
                    edgecolor="white",
                    linewidth=0.6,
                    alpha=0.88,
                )
            )
            ax_b.text(x + 0.052, y, f"E{experiment + 1}", ha="center", va="center", fontsize=6.0, color="white", fontweight="bold")
            if experiment < 3:
                arrow(ax_b, (x + 0.108, y), (x + 0.145, y), color=COLORS["muted"], width=0.8, mutation_scale=6)
        for checkpoint_x in [0.285, 0.435, 0.585, 0.885]:
            ax_b.add_patch(Circle((checkpoint_x, y + 0.09), 0.012, facecolor="white", edgecolor=color, linewidth=1.1))
    ax_b.text(0.62, 0.93, "Checkpoints: pre · 1 · 2 · 4 experiments", ha="center", fontsize=6.3, color=COLORS["muted"])
    ax_b.text(0.50, 0.08, "Three cells share the world but never share a session", ha="center", fontsize=6.5, color=COLORS["muted"])
    panel_label(ax_b, "b", x=-0.10)

    ax_c.set_title("Evidence remains partitioned", loc="left", fontweight="bold", pad=5)
    evidence_boxes = [
        (0.10, 0.73, "Participant\ntrajectory", COLORS["teal_light"], COLORS["aligned"]),
        (0.55, 0.73, "Held-out\ntruth", COLORS["blue_light"], COLORS["blue"]),
        (0.10, 0.32, "Blind outcome\nreplay", COLORS["violet_light"], COLORS["violet"]),
        (0.55, 0.32, "Private\nconfirmation", COLORS["orange_light"], COLORS["misindexed"]),
    ]
    for x, y, label, face, edge in evidence_boxes:
        rounded_box(ax_c, x, y, 0.34, 0.18, label, facecolor=face, edgecolor=edge, fontsize=6.7, fontweight="bold")
    arrow(ax_c, (0.27, 0.70), (0.45, 0.57), color=COLORS["aligned"], connectionstyle="arc3,rad=-0.1")
    arrow(ax_c, (0.72, 0.70), (0.55, 0.57), color=COLORS["blue"], connectionstyle="arc3,rad=0.1")
    rounded_box(
        ax_c,
        0.31,
        0.48,
        0.38,
        0.14,
        "Formal join\nafter terminal state",
        facecolor="#F7F9FA",
        edgecolor=COLORS["ink"],
        fontsize=6.5,
    )
    arrow(ax_c, (0.28, 0.32), (0.42, 0.47), color=COLORS["violet"], connectionstyle="arc3,rad=0.1")
    arrow(ax_c, (0.72, 0.32), (0.58, 0.47), color=COLORS["misindexed"], connectionstyle="arc3,rad=-0.1")
    ax_c.text(0.50, 0.10, "No evaluator feedback enters the participant session", ha="center", fontsize=6.4, color=COLORS["muted"])
    panel_label(ax_c, "c", x=-0.10)

    ax_d.set_title("Frozen public denominators", loc="left", fontweight="bold", pad=5)
    denominator_rows = [
        ("Independent clusters", "25", COLORS["blue"]),
        ("Participant cells", "75", COLORS["aligned"]),
        ("Complete experiments", "300", COLORS["misindexed"]),
        ("Held-out truth runs", "100", COLORS["violet"]),
        ("Blind executions", "450", COLORS["red"]),
    ]
    for index, (label, value, color) in enumerate(denominator_rows):
        y = 0.80 - index * 0.16
        ax_d.add_patch(Circle((0.15, y), 0.042, facecolor=color, edgecolor="white", linewidth=0.6))
        ax_d.text(0.15, y, value, ha="center", va="center", fontsize=6.3, color="white", fontweight="bold")
        ax_d.text(0.25, y, label, ha="left", va="center", fontsize=6.5, color=COLORS["ink"])
    ax_d.text(0.08, 0.05, "Operations, checkpoints and repeats remain nested—not extra samples", ha="left", fontsize=6.2, color=COLORS["muted"], wrap=True)
    panel_label(ax_d, "d", x=-0.10)

    fig.suptitle(
        "Matched prior interventions preserve the world-level denominator",
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
        "The formal design contains 25 independent task × world clusters; all participant, held-out and blind observations are nested within those clusters.",
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
    figure_source = ROOT / "workstreams/flagship_tasks/reports/figures/work-ii-codex-development/source_data"
    endpoint_rows: list[dict[str, Any]] = []
    warning_rows: list[dict[str, Any]] = []
    for provider_key, endpoint_name, warning_name in (
        ("WellAU/Codex", "wellau_endpoint_contrasts.csv", "wellau_misindex_warning_rates.csv"),
        ("DeepSeek recovery", "deepseek_recovery_endpoint_contrasts.csv", "deepseek_recovery_misindex_warning_rates.csv"),
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


def plot_endpoint_panel(
    ax: mpl.axes.Axes,
    rows: list[dict[str, Any]],
    provider: str,
    y_limits: tuple[float, float],
) -> None:
    selected = [row for row in rows if row["provider"] == provider]
    offsets = {"aligned_nominal": -0.14, "misindexed_nominal": 0.14}
    for task_index, task in enumerate(TASK_ORDER):
        for arm in ("aligned_nominal", "misindexed_nominal"):
            values = [
                float(row["difference"])
                for row in selected
                if row["task_id"] == task and row["comparison_arm"] == arm
            ]
            x_center = task_index + offsets[arm]
            jitter = deterministic_offsets(len(values))
            ax.scatter(
                x_center + jitter,
                values,
                s=26,
                color=ARM_COLOR[arm],
                alpha=0.72,
                edgecolor="white",
                linewidth=0.45,
                zorder=3,
            )
            mean = float(np.mean(values))
            ax.plot(
                [x_center - 0.09, x_center + 0.09],
                [mean, mean],
                color=ARM_COLOR[arm],
                linewidth=2.1,
                solid_capstyle="round",
                zorder=4,
            )
            ax.text(
                x_center,
                mean + 0.035,
                f"{mean:+.3f}\n(n={len(values)})",
                ha="center",
                va="bottom",
                fontsize=6.0,
                color=ARM_COLOR[arm],
                fontweight="bold",
            )
    ax.axhline(0, color=COLORS["ink"], linewidth=0.85)
    ax.set_xticks(range(3), [TASK_LABEL[task] for task in TASK_ORDER])
    ax.set_ylim(*y_limits)
    ax.set_ylabel("Paired difference in best endpoint score")
    ax.set_title(f"{provider}\nPaired seeds; bars show means", loc="left", fontweight="bold", pad=6)
    style_quant_axis(ax)


def build_denominator_rows(wellau: dict[str, Any], deepseek: dict[str, Any]) -> list[dict[str, Any]]:
    providers = [
        ("WellAU/Codex", wellau["wellau_fallback"]["denominators"]),
        ("DeepSeek recovery", deepseek["denominators"]),
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

    fig = plt.figure(figsize=(7.2, 6.05))
    grid = fig.add_gridspec(
        2,
        2,
        left=0.075,
        right=0.985,
        bottom=0.125,
        top=0.82,
        wspace=0.32,
        hspace=0.45,
        height_ratios=[1.03, 1.0],
        width_ratios=[1.08, 0.92],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    plot_endpoint_panel(ax_a, endpoint_rows, "WellAU/Codex", (low, high))
    plot_endpoint_panel(ax_b, endpoint_rows, "DeepSeek recovery", (low, high))
    ax_b.set_ylabel("")
    panel_label(ax_a, "a", x=-0.10)
    panel_label(ax_b, "b", x=-0.10)

    # c — warning specificity matrix
    providers = ["WellAU/Codex", "DeepSeek recovery"]
    row_labels: list[str] = []
    y_lookup: dict[tuple[str, str], int] = {}
    index = 0
    for provider in providers:
        for task in TASK_ORDER:
            y_lookup[(provider, task)] = index
            row_labels.append(f"{provider.split('/')[0].replace(' recovery', '')} · {TASK_LABEL[task].replace(chr(10), ' ')}")
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
    ax_c.set_title("Final misindex warnings\nLabels are flagged cells / available cells", loc="left", fontweight="bold", pad=6)
    panel_label(ax_c, "c", x=-0.10)

    # d — completion and replay denominators
    metrics = ["Completed cells", "Complete experiments", "Exact replay"]
    metric_colors = [COLORS["aligned"], COLORS["misindexed"], COLORS["blue"]]
    x = np.arange(len(providers), dtype=float)
    width = 0.22
    for metric_index, (metric, color) in enumerate(zip(metrics, metric_colors)):
        values = []
        labels = []
        for provider in providers:
            row = next(item for item in denominator_rows if item["provider"] == provider and item["metric"] == metric)
            values.append(float(row["rate"]))
            labels.append(f"{row['numerator']}/{row['denominator']}")
        positions = x + (metric_index - 1) * width
        bars = ax_d.bar(positions, values, width=width * 0.86, color=color, edgecolor="white", linewidth=0.6, label=metric)
        for bar, label in zip(bars, labels):
            ax_d.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.025,
                label,
                ha="center",
                va="bottom",
                fontsize=6.1,
                color=COLORS["ink"],
            )
    ax_d.set_xticks(x, ["WellAU/\nCodex", "DeepSeek\nrecovery"])
    ax_d.set_ylim(0, 1.11)
    ax_d.set_yticks(np.linspace(0, 1, 6), [f"{int(value * 100)}%" for value in np.linspace(0, 1, 6)])
    ax_d.set_ylabel("Retained denominator reached")
    ax_d.set_title("Execution completeness\nFailures remain in the denominator", loc="left", fontweight="bold", pad=6)
    ax_d.legend(loc="lower left", fontsize=6.0, ncol=1)
    style_quant_axis(ax_d)
    panel_label(ax_d, "d", x=-0.10)

    fig.suptitle(
        "Explicit priors reshape development behavior, but warnings are not selective",
        x=0.075,
        y=0.975,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            mpl.lines.Line2D([], [], marker="o", linestyle="", color=COLORS["aligned"], label="Aligned − opaque"),
            mpl.lines.Line2D([], [], marker="o", linestyle="", color=COLORS["misindexed"], label="Misindexed − opaque"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.075, 0.905),
        ncol=2,
        fontsize=6.5,
        borderaxespad=0,
        handletextpad=0.35,
        columnspacing=1.1,
    )
    fig.text(
        0.075,
        0.025,
        "Development-only descriptive evidence. Points are paired world seeds and horizontal marks are means; no formal tests or cross-provider capability comparison are performed. "
        "The two providers use separate method/harness contracts. Endpoint gains and verbal warnings do not establish law discovery, wrong-prior rejection or transfer.",
        ha="left",
        va="bottom",
        fontsize=6.5,
        color=COLORS["muted"],
        wrap=True,
    )
    return export_figure(fig, "figure-3-development-prior-effects")


def main() -> int:
    configure_matplotlib()
    design_path = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
    analysis_path = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
    preflight_path = ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json"
    wellau_path = ROOT / "workstreams/flagship_tasks/reports/work-ii-development-basic-analysis-v0.1.json"
    deepseek_path = ROOT / "workstreams/flagship_tasks/reports/work-ii-deepseek-recovery-amended-analysis-v0.1.json"
    deepseek_closeout_path = ROOT / "workstreams/flagship_tasks/reports/work-ii-deepseek-five-task-development-complete-20260810.json"
    deepseek_closeout_sources_path = ROOT / "configs/benchmark/work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json"
    source_paths = [
        design_path,
        analysis_path,
        preflight_path,
        wellau_path,
        deepseek_path,
        deepseek_closeout_path,
        deepseek_closeout_sources_path,
    ]

    design = json.loads(design_path.read_text(encoding="utf-8"))
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    wellau = json.loads(wellau_path.read_text(encoding="utf-8"))
    deepseek = json.loads(deepseek_path.read_text(encoding="utf-8"))
    deepseek_closeout = json.loads(deepseek_closeout_path.read_text(encoding="utf-8"))
    if preflight.get("formal_execution_allowed") is not False:
        raise ValueError("expected an outcome-blind execution-blocked formal preflight")
    if wellau.get("formal_result") is not False or deepseek.get("formal_result") is not False:
        raise ValueError("development Figure 3 cannot consume formal results")
    if deepseek_closeout.get("formal_result") is not False:
        raise ValueError("DeepSeek five-task closeout must remain development-only")
    closeout_denominators = deepseek_closeout.get("denominators", {})
    if closeout_denominators.get("terminal_record_count") != 75:
        raise ValueError("unexpected DeepSeek five-task closeout terminal denominator")
    if closeout_denominators.get("qualified_cell_count") != 69:
        raise ValueError("unexpected DeepSeek five-task closeout qualified denominator")

    endpoint_rows, warning_rows = normalize_development_rows()
    denominator_rows = build_denominator_rows(wellau, deepseek_closeout)
    write_csv(
        SOURCE_DIR / "figure-3-endpoint-contrasts.csv",
        endpoint_rows,
        ["provider", "task_id", "comparison_arm", "left_arm", "right_arm", "world_seed", "difference"],
    )
    write_csv(
        SOURCE_DIR / "figure-3-warning-rates.csv",
        warning_rows,
        ["provider", "task_id", "arm", "flag_count", "denominator", "flag_rate"],
    )
    write_csv(
        SOURCE_DIR / "figure-3-execution-denominators.csv",
        denominator_rows,
        ["provider", "metric", "numerator", "denominator", "rate"],
    )

    outputs = {
        "figure_1": render_figure_1(),
        "figure_2": render_figure_2(design, preflight),
        "figure_3": render_figure_3(endpoint_rows, warning_rows, denominator_rows),
    }
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-prior-discovery-figure-manifest-0.1",
        "status": "development_and_design_figures",
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
            "endpoint_rows": len(endpoint_rows),
            "warning_rows": len(warning_rows),
            "denominator_rows": len(denominator_rows),
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
            "Figures 1 and 2 show the frozen conceptual and formal design, not participant outcomes.",
            "Figure 3 contains development-only provider-isolated descriptive evidence.",
            "Partition discovery and safety-constrained reaction complete the five-task development coverage but remain operational descriptive evidence; they are not pooled into the three-task paired endpoint panels.",
            "No formal inference, law-discovery claim, transfer claim or cross-provider capability ranking is supported.",
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
                "endpoint_rows": len(endpoint_rows),
                "warning_rows": len(warning_rows),
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
