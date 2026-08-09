#!/usr/bin/env python3
"""Validate and bind the three direct-insert figures for the first ChemWorld paper."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_first_paper_figure_data import (  # noqa: E402
    SCHEMA as DATA_SCHEMA,
)
from scripts.build_first_paper_figure_data import (  # noqa: E402
    build_figure_data,
    canonical_sha256,
    file_sha256,
)

DEFAULT_DATA = (
    ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
)
DEFAULT_OUTPUT_DIR = ROOT / "paper/figures/first-paper-world-instrument-v1/publication"
DEFAULT_MANIFEST = (
    ROOT
    / "paper/figures/first-paper-world-instrument-v1"
    / "first-paper-publication-figure-manifest-v1.json"
)
MANIFEST_SCHEMA = "chemworld-first-paper-publication-figure-manifest-0.1"
RELEASE_TIMESTAMP = datetime(2026, 8, 5, tzinfo=UTC)
FIGSIZE = (7.08, 5.20)

INK = "#162331"
MUTED = "#607080"
GRID = "#DCE3E8"
WASH = "#F3F6F8"
PAPER = "#FFFFFF"
BLUE = "#286486"
TEAL = "#2F8F83"
AMBER = "#D99A32"
CORAL = "#D65F55"
PURPLE = "#7A69A6"
PALE_BLUE = "#DCECF4"
PALE_TEAL = "#DDF0EC"
PALE_AMBER = "#F7EACF"
PALE_CORAL = "#F6DEDB"

FIGURES = (
    (
        "F1",
        "figure-1-system-overview",
        "ChemWorld from world construction to auditable experiment.",
    ),
    (
        "F2",
        "figure-2-composition-and-qualification",
        "Compositional world design space beyond a fixed task catalogue.",
    ),
    (
        "F3",
        "figure-3-controlled-forks",
        "Execution, intervention and agent access.",
    ),
)


def _configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 7.4,
            "axes.titlesize": 8.4,
            "axes.labelsize": 7.5,
            "axes.titleweight": "semibold",
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.65,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.8,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "legend.frameon": False,
            "legend.fontsize": 6.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "chemworld-first-paper-world-instrument-v1",
            "savefig.facecolor": PAPER,
            "figure.facecolor": PAPER,
        }
    )


def _load_data(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != DATA_SCHEMA:
        raise RuntimeError("first-paper figure data schema is invalid")
    declared = data.get("figure_data_sha256")
    unhashed = {key: value for key, value in data.items() if key != "figure_data_sha256"}
    if declared != canonical_sha256(unhashed):
        raise RuntimeError("first-paper figure data hash is invalid")
    if data != build_figure_data(ROOT):
        raise RuntimeError("first-paper figure data is not current-bound")
    return data


def _panel(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        -0.08,
        1.07,
        label,
        transform=ax.transAxes,
        fontsize=10.5,
        fontweight="bold",
        va="top",
        ha="left",
    )
    ax.set_title(title, loc="left", pad=7)


def _clean_axis(ax: plt.Axes) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    face: str = PAPER,
    edge: str = BLUE,
    fontsize: float = 6.5,
    weight: str = "normal",
    linewidth: float = 0.9,
) -> None:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes,
        fc=face,
        ec=edge,
        lw=linewidth,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
    )


def _arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = INK,
    style: str = "-|>",
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=ax.transAxes,
            arrowstyle=style,
            mutation_scale=8,
            color=color,
            lw=0.9,
            shrinkA=2,
            shrinkB=2,
        )
    )


def _footer(fig: plt.Figure, text: str) -> None:
    fig.text(0.995, 0.012, text, ha="right", va="bottom", fontsize=5.7, color=MUTED)


def _new_2x2() -> tuple[plt.Figure, np.ndarray[Any, Any]]:
    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.115, right=0.975, top=0.91, bottom=0.09, wspace=0.40, hspace=0.60)
    return fig, axes


def _new_1x2(*, height: float = 2.70) -> tuple[plt.Figure, np.ndarray[Any, Any]]:
    fig, axes = plt.subplots(1, 2, figsize=(FIGSIZE[0], height))
    fig.subplots_adjust(left=0.105, right=0.975, top=0.84, bottom=0.19, wspace=0.38)
    return fig, axes


def figure_1(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_1"]
    fig, axes = _new_2x2()

    ax = axes[0, 0]
    _panel(ax, "A", "Reusable components compile into a world")
    _clean_axis(ax)
    components = values["components"]
    colors = [PALE_BLUE, PALE_TEAL, PALE_AMBER, PALE_CORAL, "#ECE7F5"]
    for index, component in enumerate(components):
        row, column = divmod(index, 3)
        _box(
            ax,
            (0.02 + 0.325 * column, 0.68 - 0.26 * row),
            0.285,
            0.16,
            component.replace("_", " "),
            face=colors[index % len(colors)],
            edge=BLUE,
        )
    _arrow(ax, (0.50, 0.16), (0.50, 0.12))
    _box(
        ax,
        (0.30, 0.03),
        0.40,
        0.10,
        "compiled executable world",
        face=PALE_BLUE,
        weight="semibold",
    )

    ax = axes[0, 1]
    _panel(ax, "B", "Public task-contract surface")
    _clean_axis(ax)
    surfaces = values["contract_surfaces"]
    for index, surface in enumerate(surfaces):
        angle = 2 * np.pi * index / len(surfaces) + np.pi / 8
        x = 0.50 + 0.34 * np.cos(angle)
        y = 0.46 + 0.33 * np.sin(angle)
        display = surface.replace("private-law boundary", "private-law\nboundary")
        _box(
            ax,
            (x - 0.105, y - 0.055),
            0.21,
            0.11,
            display,
            face=WASH,
            edge=TEAL,
            fontsize=5.5,
        )
    _box(
        ax, (0.33, 0.36), 0.22, 0.20, "task\ncontract", face=PALE_TEAL, edge=TEAL, weight="semibold"
    )
    ax.text(
        0.44,
        0.02,
        "private state and laws remain outside the public surface",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=MUTED,
    )

    ax = axes[1, 0]
    _panel(ax, "C", "Instances and records are distinct objects")
    _clean_axis(ax)
    hierarchy = values["hierarchy"]
    for index, item in enumerate(hierarchy):
        x = 0.01 + index * 0.245
        _box(
            ax,
            (x, 0.50),
            0.20,
            0.18,
            item,
            face=PALE_BLUE if index < 2 else PAPER,
            weight="semibold",
        )
        if index < len(hierarchy) - 1:
            _arrow(ax, (x + 0.205, 0.59), (x + 0.24, 0.59))
    _box(
        ax,
        (0.27, 0.12),
        0.46,
        0.18,
        "controlled fork\nsame public contract + one private intervention",
        face=PALE_AMBER,
        edge=AMBER,
    )
    _arrow(ax, (0.38, 0.49), (0.42, 0.31), color=AMBER)
    ax.text(
        0.50,
        0.00,
        "A fork is an attribution design, not a general composition.",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=MUTED,
    )

    ax = axes[1, 1]
    _panel(ax, "D", "Counts describe different denominators")
    labels = ["reference\ntasks", "typed\noperations", "instruments", "task-metric\nbindings"]
    counts = [
        values["reference_counts"]["reference_tasks"],
        values["reference_counts"]["typed_operations"],
        values["reference_counts"]["instruments"],
        values["reference_counts"]["task_metric_bindings"],
    ]
    bars = ax.bar(range(4), counts, color=[BLUE, TEAL, AMBER, PURPLE], width=0.68)
    ax.set_xticks(range(4), labels)
    ax.set_ylim(0, 68)
    ax.set_ylabel("count")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for bar, count in zip(bars, counts, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            count + 2,
            str(count),
            ha="center",
            fontweight="semibold",
        )
    construction = values["construction_counts"]
    ax.text(
        0.98,
        0.84,
        f"generated compositions  {construction['generated_compositions']}\n"
        f"controlled fork pairs  {construction['controlled_fork_pairs']}\n"
        f"provider-free fork traces  {construction['fork_traces']}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.1,
        bbox={"boxstyle": "round,pad=0.35", "fc": PAPER, "ec": GRID},
    )
    _footer(fig, "Reference tasks are landmarks across the declared surface, not its cardinality.")
    return fig


def figure_2(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_2"]
    fig, axes = _new_2x2()
    patterns = values["patterns"]
    component_order = [
        "reaction",
        "thermal",
        "phase",
        "separation",
        "crystallization",
        "distillation",
        "continuous flow",
        "electrochemistry",
        "observation",
    ]

    ax = axes[0, 0]
    _panel(ax, "A", "Eight frozen component patterns")
    matrix = np.array(
        [[component in row["components"] for component in component_order] for row in patterns],
        dtype=float,
    )
    cmap = mpl.colors.ListedColormap([PAPER, TEAL])
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(
        range(len(component_order)),
        [
            {
                "crystallization": "crystal.",
                "distillation": "distill.",
                "continuous flow": "flow",
                "electrochemistry": "electrochem.",
            }.get(item, item)
            for item in component_order
        ],
        rotation=42,
        ha="right",
    )
    ax.tick_params(axis="x", labelsize=5.7)
    ax.set_yticks(range(len(patterns)), [f"P{index + 1}" for index in range(len(patterns))])
    ax.tick_params(length=0)
    unseen_index = next(
        index for index, row in enumerate(patterns) if row["unseen_reference_identity"]
    )
    ax.add_patch(
        Rectangle(
            (-0.48, unseen_index - 0.48),
            len(component_order) - 0.04,
            0.96,
            fill=False,
            ec=AMBER,
            lw=1.7,
        )
    )
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(
        0.02,
        -0.28,
        "amber outline: reaction-distillation pattern absent from the 15 reference identities",
        transform=ax.transAxes,
        fontsize=5.7,
        color=MUTED,
    )

    ax = axes[0, 1]
    _panel(ax, "B", "Coverage targets determine the rows")
    _clean_axis(ax)
    coverage = values["aggregate_coverage_denominators"]
    steps = [
        (
            "pairwise\ndiscrete",
            f"{coverage['discrete_levels']} levels\n{coverage['discrete_pair_interactions']} pairs",
            PALE_BLUE,
            BLUE,
        ),
        ("seeded\nspace filling", f"{coverage['continuous_strata']} strata", PALE_TEAL, TEAL),
        (
            "ordered\nworkflows",
            f"{coverage['ordered_operation_interactions']} interactions",
            PALE_AMBER,
            AMBER,
        ),
    ]
    for index, (title, count, face, edge) in enumerate(steps):
        x = 0.02 + 0.325 * index
        _box(ax, (x, 0.48), 0.27, 0.25, title, face=face, edge=edge, weight="semibold")
        ax.text(x + 0.135, 0.38, count, transform=ax.transAxes, ha="center", fontsize=6.3)
        if index < 2:
            _arrow(ax, (x + 0.28, 0.60), (x + 0.32, 0.60))
    _box(
        ax,
        (0.30, 0.08),
        0.40,
        0.15,
        "52 frozen generated compositions",
        face=WASH,
        weight="semibold",
    )
    for x in (0.155, 0.48, 0.805):
        _arrow(ax, (x, 0.36), (0.50, 0.24), color=MUTED)

    ax = axes[1, 0]
    _panel(ax, "C", "Reference identities and generated worlds")
    labels = ["reference\ntasks", "generated\ncompositions", "unseen\ncompositions"]
    counts = [
        values["reference_task_count"],
        values["generated_composition_count"],
        values["unseen_composition_count"],
    ]
    colors = [BLUE, TEAL, AMBER]
    bars = ax.bar(range(3), counts, color=colors, width=0.62)
    ax.set_xticks(range(3), labels)
    ax.set_ylim(0, 58)
    ax.set_ylabel("count")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for bar, count in zip(bars, counts, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            count + 1.4,
            str(count),
            ha="center",
            fontweight="semibold",
        )
    ax.text(
        0.98,
        0.95,
        "identity overlap = 0",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=AMBER,
        fontweight="semibold",
    )

    ax = axes[1, 1]
    _panel(ax, "D", "Every frozen row completed")
    counts = [row["generated"] for row in patterns]
    y = np.arange(len(patterns))
    ax.barh(
        y,
        counts,
        color=[AMBER if row["unseen_reference_identity"] else TEAL for row in patterns],
        height=0.62,
    )
    ax.set_yticks(y, [f"P{index + 1}" for index in range(len(patterns))])
    ax.set_xlim(0, 9)
    ax.set_xlabel("generated and passed")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for row_index, count in enumerate(counts):
        ax.text(count + 0.15, row_index, f"{count}/{count}", va="center", fontsize=6.3)
    _footer(
        fig,
        "Unseen means absent from the frozen reference identities; "
        "it does not mean arbitrary or exhaustive.",
    )
    return fig


def figure_3(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_3"]
    fig, axes = _new_2x2()

    ax = axes[0, 0]
    _panel(ax, "A", "Complete execution censuses")
    rows = values["execution_censuses"]
    y = np.arange(len(rows))
    ax.barh(y, [1.0] * len(rows), color=TEAL, height=0.56)
    ax.set_yticks(y, [row["label"] for row in rows])
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0], ["0%", "50%", "100%"])
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for index, row in enumerate(rows):
        ax.text(
            0.50,
            index,
            f"{row['passed']:,}/{row['denominator']:,}",
            ha="center",
            va="center",
            color=PAPER,
            fontweight="semibold",
        )

    ax = axes[0, 1]
    _panel(ax, "B", "Module, interface and fail-closed probes")
    rows = values["qualification_censuses"]
    y = np.arange(len(rows))
    counts = [row["denominator"] for row in rows]
    ax.barh(y, counts, color=[BLUE, TEAL, AMBER, CORAL], height=0.56)
    ax.set_yticks(y, [row["label"] for row in rows])
    ax.set_xscale("log")
    ax.set_xlim(1, 400)
    ax.set_xlabel("full denominator (log scale)")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for index, row in enumerate(rows):
        ax.text(
            row["denominator"] * 1.10,
            index,
            f"{row['passed']}/{row['denominator']}",
            va="center",
            fontsize=6.3,
        )

    ax = axes[1, 0]
    _panel(ax, "C", "Invalid paths fail before state installation")
    _clean_axis(ax)
    _box(
        ax,
        (0.03, 0.62),
        0.25,
        0.18,
        "invalid\ndeclaration",
        face=PALE_CORAL,
        edge=CORAL,
        weight="semibold",
    )
    _arrow(ax, (0.29, 0.71), (0.42, 0.71), color=CORAL)
    _box(
        ax,
        (0.43, 0.62),
        0.26,
        0.18,
        "compatibility\nchecker",
        face=WASH,
        edge=CORAL,
        weight="semibold",
    )
    ax.plot([0.72, 0.91], [0.62, 0.80], transform=ax.transAxes, color=CORAL, lw=2.0)
    ax.plot([0.72, 0.91], [0.80, 0.62], transform=ax.transAxes, color=CORAL, lw=2.0)
    ax.text(
        0.815,
        0.52,
        "7/7 rejected\nbefore construction",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.2,
        color=CORAL,
    )
    _box(
        ax,
        (0.03, 0.18),
        0.25,
        0.18,
        "invalid\naction",
        face=PALE_AMBER,
        edge=AMBER,
        weight="semibold",
    )
    _arrow(ax, (0.29, 0.27), (0.42, 0.27), color=AMBER)
    _box(
        ax,
        (0.43, 0.18),
        0.26,
        0.18,
        "preflight +\ntransaction",
        face=WASH,
        edge=AMBER,
        weight="semibold",
    )
    _arrow(ax, (0.70, 0.27), (0.82, 0.27), color=AMBER)
    _box(
        ax,
        (0.82, 0.18),
        0.16,
        0.18,
        "state\npreserved",
        face=PALE_TEAL,
        edge=TEAL,
        weight="semibold",
    )
    ax.text(
        0.50,
        0.02,
        "192/192 registered negative probes produced the expected rejection.",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=MUTED,
    )

    ax = axes[1, 1]
    _panel(ax, "D", "No hidden qualification failures")
    _clean_axis(ax)
    findings = values["zero_findings"]
    labels = ["failure\nclasses", "missing\nreceipts", "public/private\nleakage"]
    for index, (label, key) in enumerate(zip(labels, findings, strict=True)):
        x = 0.03 + 0.325 * index
        _box(
            ax,
            (x, 0.42),
            0.27,
            0.30,
            f"{findings[key]}\n{label}",
            face=PALE_TEAL,
            edge=TEAL,
            fontsize=7.2,
            weight="semibold",
        )
    ax.text(
        0.50,
        0.16,
        "Counts report complete case-level qualification denominators.",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.2,
        color=MUTED,
    )
    _footer(
        fig,
        "The claim is executable-module qualification within declared model-card domains",
    )
    return fig


def figure_4(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_4"]
    fig, axes = _new_1x2(height=2.58)
    fig.subplots_adjust(left=0.135, right=0.975, top=0.84, bottom=0.19, wspace=0.42)
    cases = values["cases"]

    ax = axes[0]
    _panel(ax, "A", "Eight frozen use cases")
    y = np.arange(len(cases))
    committed = [row["committed"] for row in cases]
    rollback = [row["rolled_back"] for row in cases]
    ax.barh(y, committed, color=TEAL, height=0.58, label="committed")
    ax.barh(y, rollback, left=committed, color=AMBER, height=0.58, label="rolled back")
    ax.set_yticks(y, [row["label"] for row in cases])
    ax.set_xlim(0, 21)
    ax.set_xlabel("submitted actions")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for index, row in enumerate(cases):
        ax.text(row["submitted"] + 0.25, index, str(row["submitted"]), va="center", fontsize=6.1)
    ax.legend(loc="lower right")

    ax = axes[1]
    _panel(ax, "B", "1 rollback → 18 subsequent commits")
    recovery = values["recovery"]
    _clean_axis(ax)
    xs = np.linspace(0.06, 0.94, 19)
    for step, x in enumerate(xs, 1):
        color = AMBER if step == 1 else TEAL
        ax.scatter(
            x,
            0.58,
            s=38,
            color=color,
            edgecolor=PAPER,
            linewidth=0.6,
            transform=ax.transAxes,
            zorder=3,
        )
        if step in {1, 2, 5, 10, 15, 19}:
            ax.text(x, 0.44, str(step), transform=ax.transAxes, ha="center", fontsize=5.7)
    ax.plot(xs, [0.58] * len(xs), color=GRID, lw=2.0, transform=ax.transAxes, zorder=1)
    ax.text(
        xs[0],
        0.75,
        "step 1\nrollback",
        transform=ax.transAxes,
        ha="center",
        color=AMBER,
        fontweight="semibold",
        fontsize=6.2,
    )
    ax.text(
        0.62,
        0.75,
        f"steps 2-19\n{recovery['subsequent_commits']} commits",
        transform=ax.transAxes,
        ha="center",
        color=TEAL,
        fontweight="semibold",
    )
    ax.text(
        0.50,
        0.16,
        "the planned rollback remains inside the complete 89-action census",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=MUTED,
    )

    _footer(
        fig,
        "The planned rollback remains recorded before recovery continues from committed state.",
    )
    return fig


def figure_5(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_5"]
    fig, axes = _new_2x2()

    ax = axes[0, 0]
    _panel(ax, "A", "Parent and child share the public contract")
    _clean_axis(ax)
    _box(
        ax, (0.02, 0.34), 0.26, 0.30, "parent\nworld", face=PALE_BLUE, edge=BLUE, weight="semibold"
    )
    _box(ax, (0.72, 0.34), 0.26, 0.30, "child\nworld", face=PALE_TEAL, edge=TEAL, weight="semibold")
    _box(
        ax,
        (0.34, 0.55),
        0.32,
        0.20,
        f"same public contract\n{values['public_contract_component_count']} invariant fields",
        face=WASH,
        edge=INK,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.34, 0.18),
        0.32,
        0.20,
        "same fixed\naction sequence",
        face=WASH,
        edge=INK,
        weight="semibold",
    )
    _arrow(ax, (0.28, 0.52), (0.34, 0.65))
    _arrow(ax, (0.66, 0.65), (0.72, 0.52))
    _arrow(ax, (0.28, 0.44), (0.34, 0.28))
    _arrow(ax, (0.66, 0.28), (0.72, 0.44))

    ax = axes[0, 1]
    _panel(ax, "B", "Exactly one private component changes")
    _clean_axis(ax)
    classes = values["intervention_class_counts"]
    items = [
        ("constitutive-law\nfamily", classes["mechanism_or_constitutive_law"], PALE_AMBER, AMBER),
        ("material-law\ncounterfactual", classes["material_law_counterfactual"], PALE_CORAL, CORAL),
    ]
    for index, (label, count, face, edge) in enumerate(items):
        x = 0.08 + 0.48 * index
        _box(
            ax,
            (x, 0.38),
            0.36,
            0.32,
            f"{count} pairs\n{label}",
            face=face,
            edge=edge,
            fontsize=7.0,
            weight="semibold",
        )
    ax.text(
        0.50,
        0.16,
        "one target per fork; no multi-component attribution claim",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.0,
        color=MUTED,
    )

    ax = axes[1, 0]
    _panel(ax, "C", "All six pairs pass every registered gate")
    gates = values["gate_pass_counts"]
    labels = [
        "lineage",
        "public\nsame",
        "sequence\nsame",
        "expected\ndelta",
        "replay",
        "zero\nprovider",
    ]
    keys = [
        "single_target_lineage",
        "public_contract_invariance",
        "same_sequence_executability",
        "expected_response_divergence",
        "exact_replay",
        "zero_provider_calls",
    ]
    bars = ax.bar(
        range(6),
        [gates[key] for key in keys],
        color=[BLUE, TEAL, AMBER, CORAL, PURPLE, MUTED],
        width=0.68,
    )
    ax.set_xticks(range(6), labels)
    ax.tick_params(axis="x", labelsize=5.8)
    ax.set_ylim(0, 7.2)
    ax.set_ylabel("pairs passed")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            6.18,
            "6/6",
            ha="center",
            fontweight="semibold",
            fontsize=6.2,
        )

    ax = axes[1, 1]
    _panel(ax, "D", "Divergence appears in protocol-specified channels")
    rows = values["rows"]
    x = np.arange(len(rows))
    physical = [row["physical_relative_delta"] for row in rows]
    observation = [row["observation_relative_delta"] for row in rows]
    ax.axhline(0, color=INK, lw=0.7)
    ax.scatter(x - 0.10, physical, color=BLUE, s=24, label="physical state", zorder=3)
    ax.scatter(
        x + 0.10, observation, color=CORAL, marker="s", s=22, label="public observation", zorder=3
    )
    ax.set_xticks(x, [f"{row['seed']}" for row in rows])
    ax.set_xlabel("seed: constitutive 0-2; material law 0-2")
    ax.set_ylabel("relative difference magnitude")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    ax.legend(loc="best")
    ax.text(
        0.98,
        0.03,
        f"{values['pair_count']} pairs · {values['trace_count']} provider-free traces",
        transform=ax.transAxes,
        ha="right",
        fontsize=5.3,
        color=MUTED,
    )
    return fig


def _timeline(ax: plt.Axes, operations: Sequence[str], *, y: float, color: str, label: str) -> None:
    xs = np.linspace(0.17, 0.95, len(operations))
    categories = {
        "add_solvent": "add",
        "add_reagent": "add",
        "add_catalyst": "add",
        "heat": "heat",
        "wait": "wait",
        "evaporate": "evap",
        "distill": "distill",
        "collect_fraction": "collect",
        "measure": "measure",
        "terminate": "stop",
    }
    ax.plot(xs, [y] * len(xs), transform=ax.transAxes, color=GRID, lw=2.0, zorder=1)
    for index, (x, operation) in enumerate(zip(xs, operations, strict=True)):
        ax.scatter(
            x,
            y,
            transform=ax.transAxes,
            s=34,
            color=color,
            edgecolor=PAPER,
            linewidth=0.5,
            zorder=3,
        )
        if index in {0, len(operations) - 1} or operation in {
            "distill",
            "collect_fraction",
            "terminate",
        }:
            ax.text(
                x,
                y - 0.09,
                categories.get(operation, operation),
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontsize=5.3,
                rotation=30,
            )
    ax.text(
        0.02,
        y + 0.10,
        label,
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=6.0,
        fontweight="semibold",
        color=color,
    )


def figure_6(data: Mapping[str, Any]) -> plt.Figure:
    values = data["figure_6"]
    fig, axes = _new_2x2()
    reference = values["deterministic_reference"]
    agent = values["complete_agent"]

    ax = axes[0, 0]
    _panel(ax, "A", "One world, two independent execution units")
    _clean_axis(ax)
    _timeline(ax, reference["operations"], y=0.70, color=BLUE, label="12-step reference")
    _timeline(ax, agent["operations"], y=0.30, color=TEAL, label="15-step agent")
    ax.text(
        0.50,
        0.02,
        "The deterministic path qualifies the world; it does not replace the complete-agent unit.",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.7,
        color=MUTED,
    )

    ax = axes[0, 1]
    _panel(ax, "B", "The complete-agent lifecycle closes")
    labels = ["submitted", "committed", "rollback", "terminate", "final assay"]
    counts = [
        agent["submitted"],
        agent["committed"],
        agent["rolled_back"],
        agent["terminate"],
        agent["final_assay"],
    ]
    colors = [BLUE, TEAL, AMBER, PURPLE, CORAL]
    bars = ax.bar(range(5), counts, color=colors, width=0.64)
    ax.set_xticks(range(5), [label.replace(" ", "\n") for label in labels])
    ax.set_ylim(0, 17)
    ax.set_ylabel("actions")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for bar, count in zip(bars, counts, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            count + 0.4,
            str(count),
            ha="center",
            fontweight="semibold",
        )
    ax.text(
        0.98,
        0.94,
        "exact replay: PASS",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=TEAL,
        fontweight="semibold",
    )

    ax = axes[1, 0]
    _panel(ax, "C", "Environment and provider use separate ledgers")
    resource_labels = ["process time", "operations", "instruments", "sample", "provider input"]
    used = agent["resource_usage"]
    limits = agent["resource_limits"]
    provider = agent["provider"]
    fractions = [
        used["process_time_s"] / limits["process_time_s"],
        used["operation_attempts"] / limits["operation_attempts"],
        used["instrument_uses"] / limits["instrument_uses"],
        used["sample_consumed_L"] / limits["sample_consumed_L"],
    ]
    input_total = provider["input_tokens"]
    cache_fraction = provider["cache_hit_tokens"] / input_total
    miss_fraction = provider["cache_miss_tokens"] / input_total
    y = np.arange(5)
    ax.barh(y[:4], [1.0] * 4, color=WASH, height=0.52)
    ax.barh(y[:4], fractions, color=[BLUE, TEAL, AMBER, PURPLE], height=0.52)
    ax.barh(4, cache_fraction, color=PALE_BLUE, edgecolor=BLUE, height=0.52)
    ax.barh(
        4,
        miss_fraction,
        left=cache_fraction,
        color=PALE_CORAL,
        edgecolor=CORAL,
        height=0.52,
    )
    ax.set_yticks(y, resource_labels)
    ax.set_xlim(0, 1.05)
    ax.set_xticks([0, 0.5, 1.0], ["0%", "50%", "100%"])
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    exact = [
        f"{used['process_time_s']:,.0f}/{limits['process_time_s']:,.0f} s",
        f"{used['operation_attempts']}/{limits['operation_attempts']}",
        f"{used['instrument_uses']}/{limits['instrument_uses']}",
        f"{used['sample_consumed_L'] * 1e3:.2f}/{limits['sample_consumed_L'] * 1e3:.2f} mL",
        f"{provider['cache_hit_tokens']:,} cached + {provider['cache_miss_tokens']:,} uncached",
    ]
    for index, text in enumerate(exact):
        ax.text(1.02, index, text, ha="right", va="center", fontsize=5.9, fontweight="semibold")
    ax.text(
        0.02,
        -0.17,
        f"provider input row = context composition, not a limit · "
        f"{provider['sessions']} session · {provider['logical_turns']} logical turn · "
        f"{provider['mcp_calls']} calls · output {provider['output_tokens']:,}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=5.0,
        color=MUTED,
    )

    ax = axes[1, 1]
    _panel(ax, "D", "A near endpoint can hide a different process")
    endpoint = values["endpoint_near_example"]
    labels = [
        "raw terminal",
        "best discovery",
        "online retention",
        "max drawdown",
        "terminal / best",
    ]
    deltas = [
        endpoint["raw_terminal_score"],
        endpoint["best_discovery_fraction"],
        endpoint["online_retention_rate"],
        endpoint["maximum_drawdown"],
        endpoint["terminal_to_best_ratio"],
    ]
    y = np.arange(len(labels))
    ax.axvline(0, color=INK, lw=0.7)
    ax.barh(y, deltas, color=[MUTED, TEAL, TEAL, CORAL, PURPLE], height=0.58)
    ax.set_yticks(y, labels)
    ax.set_xlim(-0.48, 0.52)
    ax.set_xlabel("archived matched-pair contrast")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for index, value in enumerate(deltas):
        ax.text(
            value + (0.018 if value >= 0 else -0.018),
            index,
            f"{value:+.3f}",
            ha="left" if value >= 0 else "right",
            va="center",
            fontsize=6.1,
            fontweight="semibold",
        )
    ax.text(
        0.02,
        0.96,
        "world 1 · replicate 3\ndescriptive only",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=5.8,
        color=MUTED,
    )
    _footer(
        fig,
        "Process coordinates remain separate; "
        "no scalar intelligence score or model ranking is formed.",
    )
    return fig


def figure_1_system_overview(data: Mapping[str, Any]) -> plt.Figure:
    """Render the end-to-end system overview as fully editable vector artwork."""

    fig, axes = _new_2x2()
    ax = axes[0, 0]
    _clean_axis(ax)
    _panel(ax, "A", "Two complementary experimental regimes")
    _box(
        ax,
        (0.02, 0.47),
        0.40,
        0.34,
        "REAL-MATERIAL SDL\nphysical samples\nhardware + sensors\nempirical validation",
        face=PALE_CORAL,
        edge=CORAL,
        fontsize=6.5,
        weight="semibold",
    )
    _box(
        ax,
        (0.58, 0.47),
        0.40,
        0.34,
        (
            "CHEMWORLD\nexact reset + matched repeats\n"
            "private-law intervention\ncomplete simulator record"
        ),
        face=PALE_TEAL,
        edge=TEAL,
        fontsize=6.3,
        weight="semibold",
    )
    _arrow(ax, (0.44, 0.64), (0.56, 0.64), color=MUTED, style="<|-|>")
    _box(
        ax,
        (0.11, 0.15),
        0.78,
        0.15,
        "software narrows hypotheses  →  physical execution tests real matter",
        face=WASH,
        edge=GRID,
        fontsize=6.2,
    )
    ax.text(
        0.50,
        0.88,
        "shared experimental questions · different evidence regimes",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=MUTED,
    )

    ax = axes[0, 1]
    _clean_axis(ax)
    _panel(ax, "B", "Public structure + private mechanism")
    component_boxes = (
        ((0.01, 0.68), "components\nchemistry + process", PALE_BLUE, BLUE),
        ((0.01, 0.43), "interfaces\nactions + instruments", PALE_TEAL, TEAL),
        ((0.01, 0.18), "constraints\nunits + ownership\nresource budgets", PALE_AMBER, AMBER),
    )
    for xy, label, face, edge in component_boxes:
        _box(ax, xy, 0.29, 0.16, label, face=face, edge=edge, fontsize=5.2, weight="semibold")
        _arrow(ax, (0.31, xy[1] + 0.08), (0.39, 0.51), color=MUTED)
    _box(
        ax,
        (0.40, 0.39),
        0.20,
        0.23,
        "compatibility\ncompiler",
        face=WASH,
        edge=INK,
        fontsize=6.2,
        weight="semibold",
    )
    _arrow(ax, (0.61, 0.54), (0.68, 0.67), color=INK)
    _box(
        ax,
        (0.69, 0.57),
        0.29,
        0.25,
        (
            "PUBLIC CONTRACT T\nW_pub + S0,pub\noperations + instruments\n"
            "observations + resources\ntermination + evaluation"
        ),
        face=PALE_BLUE,
        edge=BLUE,
        fontsize=5.1,
        weight="semibold",
    )
    _arrow(ax, (0.61, 0.46), (0.68, 0.34), color=CORAL)
    _box(
        ax,
        (0.69, 0.20),
        0.29,
        0.25,
        ("PRIVATE theta\nconstitutive + material laws\nhidden parameters\nprivate initialization"),
        face=PALE_CORAL,
        edge=CORAL,
        fontsize=4.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.42, 0.08),
        0.54,
        0.08,
        "complete world = (W_pub, theta)",
        face=WASH,
        edge=GRID,
        fontsize=5.7,
    )

    ax = axes[1, 0]
    _clean_axis(ax)
    _panel(ax, "C", "Commit is gated at runtime")
    _box(
        ax,
        (0.01, 0.67),
        0.14,
        0.15,
        "typed\naction",
        face=PALE_AMBER,
        edge=AMBER,
        fontsize=6.2,
    )
    _box(
        ax,
        (0.20, 0.67),
        0.15,
        0.15,
        "preflight\nP",
        face=PALE_BLUE,
        edge=BLUE,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.40, 0.67),
        0.17,
        0.15,
        "candidate\nF_theta",
        face=PALE_TEAL,
        edge=TEAL,
        fontsize=5.8,
    )
    _box(
        ax,
        (0.62, 0.67),
        0.17,
        0.15,
        "commit gate\nC",
        face=WASH,
        edge=INK,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.84, 0.67),
        0.14,
        0.15,
        "COMMIT",
        face=PALE_TEAL,
        edge=TEAL,
        fontsize=6.0,
        weight="bold",
    )
    _box(
        ax,
        (0.73, 0.38),
        0.25,
        0.16,
        "committed state\nobservation + ledger",
        face=PALE_TEAL,
        edge=TEAL,
        fontsize=5.2,
    )
    for x0, x1 in ((0.16, 0.19), (0.36, 0.39), (0.58, 0.61), (0.80, 0.83)):
        _arrow(ax, (x0, 0.745), (x1, 0.745))
    ax.text(
        0.275,
        0.62,
        "schema + resources",
        transform=ax.transAxes,
        ha="center",
        fontsize=4.7,
        color=MUTED,
    )
    ax.text(
        0.705,
        0.62,
        "state + observation",
        transform=ax.transAxes,
        ha="center",
        fontsize=4.7,
        color=MUTED,
    )
    _arrow(ax, (0.91, 0.66), (0.86, 0.55), color=TEAL)
    _box(
        ax,
        (0.06, 0.27),
        0.25,
        0.16,
        "P = 0\nPREFLIGHT REJECT",
        face=PALE_CORAL,
        edge=CORAL,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.39, 0.27),
        0.27,
        0.16,
        "C = 0\nROLLBACK",
        face=PALE_CORAL,
        edge=CORAL,
        fontsize=5.8,
        weight="semibold",
    )
    _arrow(ax, (0.275, 0.66), (0.19, 0.44), color=CORAL)
    _arrow(ax, (0.705, 0.66), (0.53, 0.44), color=CORAL)
    _box(
        ax,
        (0.08, 0.04),
        0.56,
        0.10,
        "record branch + retain declared attempt cost",
        face=PALE_AMBER,
        edge=AMBER,
        fontsize=5.1,
    )
    _arrow(ax, (0.19, 0.26), (0.27, 0.18), color=CORAL)
    _arrow(ax, (0.53, 0.26), (0.47, 0.18), color=CORAL)
    ax.text(
        0.82,
        0.14,
        "candidate state\nnot installed",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=5.0,
        color=MUTED,
    )

    ax = axes[1, 1]
    _clean_axis(ax)
    _panel(ax, "D", "Layered records enable new experiments")
    for y, label, face, edge in (
        (0.66, "PUBLIC RECORD\nactions · observations · terminal flags", PALE_BLUE, BLUE),
        (0.43, "COMMITTED STATE\nphysical state · observation RNG", PALE_TEAL, TEAL),
        (0.20, "AUDIT LEDGER\ntransactions · resources · failures · lineage", PALE_AMBER, AMBER),
    ):
        _box(ax, (0.01, y), 0.47, 0.17, label, face=face, edge=edge, fontsize=5.4)
    _box(
        ax,
        (0.62, 0.68),
        0.36,
        0.14,
        "EXACT REPLAY\nreconstruct the environment",
        face=WASH,
        edge=BLUE,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.62, 0.45),
        0.36,
        0.14,
        "CONTROLLED FORK\nchange one private law",
        face=WASH,
        edge=CORAL,
        fontsize=5.8,
        weight="semibold",
    )
    _box(
        ax,
        (0.62, 0.22),
        0.36,
        0.14,
        "PROCESS READOUTS\nobserve how the result arose",
        face=WASH,
        edge=TEAL,
        fontsize=5.8,
        weight="semibold",
    )
    ax.plot([0.52, 0.52], [0.29, 0.75], transform=ax.transAxes, color=MUTED, lw=0.9)
    for y in (0.75, 0.52, 0.29):
        _arrow(ax, (0.49, y), (0.61, y), color=MUTED)
    ax.text(
        0.50,
        0.06,
        "one record · three reusable experimental operations",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.1,
        color=MUTED,
    )
    _footer(
        fig,
        (
            "Private mechanisms and evaluator-complete records remain outside the "
            "agent-facing surface."
        ),
    )
    return fig


def figure_2_composition_qualification(data: Mapping[str, Any]) -> plt.Figure:
    fig, axes = _new_1x2(height=2.82)
    coverage = data["figure_2"]
    patterns = coverage["patterns"]
    components = [
        "reaction",
        "thermal",
        "phase",
        "separation",
        "crystallization",
        "distillation",
        "continuous flow",
        "electrochemistry",
        "observation",
    ]
    matrix = np.asarray(
        [
            [1 if component in row["components"] else 0 for component in components]
            for row in patterns
        ],
        dtype=float,
    )

    ax = axes[0]
    _panel(ax, "A", "Topology and identity decompose separately")
    ax.imshow(matrix, aspect="auto", cmap=mpl.colors.ListedColormap([PAPER, TEAL]), vmin=0, vmax=1)
    ax.set_xticks(
        range(len(components)),
        ["rxn", "thermal", "phase", "sep.", "cryst.", "distill.", "flow", "electro", "obs."],
        rotation=40,
        ha="right",
    )
    ax.set_yticks(range(len(patterns)), [f"P{i}" for i in range(1, len(patterns) + 1)])
    for index, row in enumerate(patterns):
        if not row["reference_topology_overlap"]:
            ax.add_patch(
                Rectangle(
                    (-0.48, index - 0.48),
                    len(components) - 0.04,
                    0.96,
                    fill=False,
                    ec=BLUE,
                    lw=1.5,
                )
            )
        elif row["unseen_reference_identity"]:
            ax.add_patch(
                Rectangle(
                    (-0.48, index - 0.48),
                    len(components) - 0.04,
                    0.96,
                    fill=False,
                    ec=AMBER,
                    lw=1.8,
                )
            )
    ax.text(
        0.0,
        -0.25,
        (
            f"blue: {coverage['new_topology_pattern_count']} new topologies "
            f"({coverage['new_topology_case_count']} cases)  ·  "
            "amber: 8 identity-new distillation cases"
        ),
        transform=ax.transAxes,
        fontsize=5.8,
        color=MUTED,
    )
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1]
    _clean_axis(ax)
    _panel(ax, "B", "Coverage targets determine 52 rows")
    aggregate = coverage["aggregate_coverage_denominators"]
    boxes = (
        (
            (0.01, 0.55),
            "pairwise discrete",
            (
                f"{aggregate['discrete_levels']}/{aggregate['discrete_levels']} levels\n"
                f"{aggregate['discrete_pair_interactions']}/"
                f"{aggregate['discrete_pair_interactions']} pairs"
            ),
            PALE_BLUE,
            BLUE,
        ),
        (
            (0.35, 0.55),
            "seeded continuous",
            f"{aggregate['continuous_strata']}/{aggregate['continuous_strata']} strata",
            PALE_TEAL,
            TEAL,
        ),
        (
            (0.69, 0.55),
            "ordered workflows",
            (
                f"{aggregate['ordered_operation_interactions']}/"
                f"{aggregate['ordered_operation_interactions']} interactions"
            ),
            PALE_AMBER,
            AMBER,
        ),
    )
    for xy, title, detail, face, edge in boxes:
        _box(ax, xy, 0.30, 0.20, title, face=face, edge=edge, fontsize=6.5, weight="semibold")
        ax.text(xy[0] + 0.15, 0.48, detail, transform=ax.transAxes, ha="center", fontsize=6.4)
        _arrow(ax, (xy[0] + 0.15, 0.43), (0.50, 0.28), color=MUTED)
    _box(
        ax,
        (0.29, 0.13),
        0.42,
        0.17,
        "52 protocol-frozen generated compositions",
        face=WASH,
        edge=BLUE,
        fontsize=7.0,
        weight="bold",
    )

    _footer(
        fig,
        (
            "Coverage defines the qualification sample; it does not define the extent "
            "of the world space."
        ),
    )
    return fig


def _fork_effect_panel(
    ax: plt.Axes,
    rows: Sequence[Mapping[str, Any]],
    *,
    label: str,
    title: str,
    physical_label: str,
    observation_label: str,
    physical_threshold: float,
    observation_threshold: float,
) -> None:
    _panel(ax, label, title)
    ordered = sorted(rows, key=lambda row: int(row["seed"]))
    x = np.arange(len(ordered))
    physical = [float(row["physical_relative_delta"]) for row in ordered]
    observed = [float(row["observation_relative_delta"]) for row in ordered]
    ax.plot(x, physical, color=BLUE, lw=1.0, alpha=0.65)
    ax.plot(x, observed, color=CORAL, lw=1.0, alpha=0.65)
    ax.scatter(x, physical, s=30, color=BLUE, label=physical_label, zorder=3)
    ax.scatter(x, observed, s=28, color=CORAL, marker="s", label=observation_label, zorder=3)
    ax.axhline(physical_threshold, color=BLUE, lw=0.8, ls=":", alpha=0.9)
    ax.axhline(observation_threshold, color=CORAL, lw=0.8, ls=":", alpha=0.9)
    ax.set_xticks(x, [f"seed {row['seed']}" for row in ordered])
    ax.set_xlim(-0.35, len(ordered) - 0.65)
    ax.set_ylim(0.0, 0.24)
    ax.set_ylabel("relative difference magnitude")
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    ax.legend(loc="upper right", fontsize=5.7)
    ax.text(
        0.98,
        physical_threshold + 0.006,
        f"state min {physical_threshold:.2f}",
        transform=ax.get_yaxis_transform(),
        ha="right",
        va="bottom",
        fontsize=5.0,
        color=BLUE,
    )
    ax.text(
        0.98,
        observation_threshold + 0.006,
        f"public min {observation_threshold:.2f}",
        transform=ax.get_yaxis_transform(),
        ha="right",
        va="bottom",
        fontsize=5.0,
        color=CORAL,
    )


def figure_3_controlled_forks(data: Mapping[str, Any]) -> plt.Figure:
    fig, axes = _new_2x2()
    forks = data["figure_5"]

    ax = axes[0, 0]
    _clean_axis(ax)
    _panel(ax, "A", "Matched counterfactual design")
    _box(
        ax,
        (0.01, 0.54),
        0.22,
        0.25,
        "parent\nworld",
        face=PALE_BLUE,
        edge=BLUE,
        fontsize=6.8,
        weight="bold",
    )
    _box(
        ax,
        (0.31, 0.54),
        0.38,
        0.25,
        "HELD FIXED\n9 public-contract fields\nsame action sequence\n+ keyed noise",
        face=WASH,
        edge=INK,
        fontsize=5.3,
        weight="semibold",
    )
    _box(
        ax,
        (0.31, 0.17),
        0.38,
        0.20,
        "VARIED\nexactly one evaluator-owned\nprivate-law target",
        face=PALE_AMBER,
        edge=AMBER,
        fontsize=5.7,
        weight="semibold",
    )
    _box(
        ax,
        (0.77, 0.54),
        0.22,
        0.25,
        "child\nworld",
        face=PALE_TEAL,
        edge=TEAL,
        fontsize=6.8,
        weight="bold",
    )
    _arrow(ax, (0.24, 0.67), (0.30, 0.67))
    _arrow(ax, (0.70, 0.67), (0.76, 0.67))
    _arrow(ax, (0.50, 0.38), (0.76, 0.57), color=AMBER)
    ax.text(
        0.50,
        0.03,
        "6 pairs · 2 executions per variant · 24 deterministic traces",
        transform=ax.transAxes,
        ha="center",
        fontsize=5.6,
        color=MUTED,
    )

    ax = axes[0, 1]
    _clean_axis(ax)
    _panel(ax, "B", "Two protocol-frozen intervention classes")
    _box(
        ax,
        (0.02, 0.53),
        0.96,
        0.31,
        (
            "PARTITION CONSTITUTIVE LAW · 3 seeds\n"
            "$K^{1.00}\\rightarrow K^{1.75}$\n"
            "physical $P_{org}\\uparrow$  ·  public product_in_organic $\\uparrow$"
        ),
        face=PALE_AMBER,
        edge=AMBER,
        fontsize=5.5,
        weight="semibold",
    )
    _box(
        ax,
        (0.02, 0.10),
        0.96,
        0.34,
        (
            "ELECTROCHEMICAL MATERIAL LAW · 3 seeds\n"
            "hidden mapping (0,1,2,3)→(2,1,0,3)\n"
            "physical Red ↓  ·  public ohmic_efficiency ↓"
        ),
        face=PALE_CORAL,
        edge=CORAL,
        fontsize=5.3,
        weight="semibold",
    )

    rows = forks["rows"]
    constitutive = [
        row for row in rows if row["intervention_class"] == "mechanism_or_constitutive_law"
    ]
    material = [row for row in rows if row["intervention_class"] == "material_law_counterfactual"]
    _fork_effect_panel(
        axes[1, 0],
        constitutive,
        label="C",
        title="Constitutive-law effects (increase)",
        physical_label=r"physical $P_{org}$",
        observation_label="public assay",
        physical_threshold=0.05,
        observation_threshold=0.02,
    )
    _fork_effect_panel(
        axes[1, 1],
        material,
        label="D",
        title="Material-law effects (decrease)",
        physical_label="physical Red",
        observation_label="public efficiency",
        physical_threshold=0.01,
        observation_threshold=0.05,
    )
    _footer(
        fig,
        (
            "Relative-difference magnitude is shown; the frozen oracle also requires "
            "the registered absolute magnitude and direction. All six pairs replay exactly."
        ),
    )
    return fig


def _save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for suffix in ("svg", "pdf", "png"):
        path = output_dir / f"{stem}.{suffix}"
        metadata: dict[str, Any] = {"Creator": "ChemWorld first-paper figure pipeline"}
        if suffix == "pdf":
            metadata |= {"CreationDate": RELEASE_TIMESTAMP, "ModDate": RELEASE_TIMESTAMP}
        elif suffix == "svg":
            metadata["Date"] = "2026-08-05T00:00:00Z"
        fig.savefig(path, dpi=300, metadata=metadata)
        if suffix == "svg":
            normalized = "\n".join(
                line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
            )
            path.write_text(normalized + "\n", encoding="utf-8", newline="\n")
        outputs.append(path)
    plt.close(fig)
    return outputs


def build_manifest(
    data: Mapping[str, Any], outputs: Mapping[str, Sequence[Path]]
) -> dict[str, Any]:
    figures: list[dict[str, Any]] = []
    for order, (figure_id, stem, title) in enumerate(FIGURES, 1):
        rows = []
        for path in outputs[stem]:
            rows.append(
                {
                    "format": path.suffix.removeprefix("."),
                    "path": path.relative_to(ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": file_sha256(path),
                    "status": "PASS",
                }
            )
        figures.append(
            {
                "figure_id": figure_id,
                "order": order,
                "stem": stem,
                "title": title,
                "manuscript_reference": (
                    f"figures/first-paper-world-instrument-v1/publication/{stem}.pdf"
                ),
                "outputs": rows,
            }
        )
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA,
        "status": "PASS",
        "style_version": "first-paper-world-instrument-v1",
        "canonical_figure_count": len(figures),
        "canonical_asset_count": sum(len(row["outputs"]) for row in figures),
        "caption_titles": [row[2] for row in FIGURES],
        "figure_data": {
            "path": DEFAULT_DATA.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(DEFAULT_DATA),
            "content_sha256": data["figure_data_sha256"],
            "current_graph_sha256": data["current_graph_sha256"],
        },
        "source_bindings": data["source_bindings"],
        "claim_boundary": data["claim_boundary"],
        "figures": figures,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return manifest


def render(data: Mapping[str, Any], output_dir: Path) -> dict[str, Sequence[Path]]:
    # The current figures come from editable author sources. Their checked-in publication
    # assets are authoritative; running this manifest tool must never redraw or overwrite
    # them with the legacy matplotlib layouts retained above for provenance.
    del data
    outputs: dict[str, Sequence[Path]] = {}
    for _, stem, _ in FIGURES:
        paths = [output_dir / f"{stem}.{suffix}" for suffix in ("svg", "pdf", "png")]
        missing = [path for path in paths if not path.is_file()]
        if missing:
            rendered = ", ".join(str(path) for path in missing)
            raise FileNotFoundError(f"missing direct-insert publication assets: {rendered}")
        outputs[stem] = paths
    return outputs


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    _configure()
    data = _load_data(args.data.resolve())
    outputs = render(data, args.output_dir.resolve())
    manifest = build_manifest(data, outputs)
    manifest_path = args.manifest.resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "figure_count": manifest["canonical_figure_count"],
                "asset_count": manifest["canonical_asset_count"],
                "manifest": str(manifest_path),
                "manifest_sha256": manifest["manifest_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
