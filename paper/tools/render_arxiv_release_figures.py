"""Render the six evidence figures for the ChemWorld arXiv release."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
DERIVED_SCHEMA = "chemworld-arxiv-v1-derived-data-0.1"
SENSITIVITY_SCHEMA = "chemworld-arxiv-v1-p0-sensitivity-0.1"
MANIFEST_SCHEMA = "chemworld-arxiv-release-figure-manifest-0.1"

INK = "#17222E"
MUTED = "#687481"
GRID = "#DCE3E8"
WASH = "#F4F7F8"
PAPER = "#FFFFFF"
OPAQUE = "#26577C"
NOMINAL = "#D95F52"
MISINDEXED = "#8066B3"
TEAL = "#3D9487"
AMBER = "#E3A43E"
RELEASE_TIMESTAMP = datetime(2026, 8, 2, tzinfo=UTC)


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_hashed(path: Path, *, schema: str, hash_key: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != schema:
        raise ValueError(f"unsupported schema: {path}")
    declared = data.pop(hash_key)
    actual = _canonical_sha(data)
    data[hash_key] = declared
    if declared != actual:
        raise ValueError(f"content hash is invalid: {path}")
    return data


def _configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 7.6,
            "axes.titlesize": 8.8,
            "axes.labelsize": 7.8,
            "axes.titleweight": "semibold",
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.65,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "legend.frameon": False,
            "legend.fontsize": 7.0,
            "lines.linewidth": 1.25,
            "svg.hashsalt": "chemworld-arxiv-release-v1",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": PAPER,
            "figure.facecolor": PAPER,
        }
    )


def _panel(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        -0.09,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        va="top",
        ha="left",
    )
    ax.set_title(title, loc="left", pad=7)


def _box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    edge: str = INK,
    face: str = PAPER,
    fontsize: float = 7.0,
    weight: str = "normal",
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        transform=ax.transAxes,
        fc=face,
        ec=edge,
        lw=1.0,
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
    return patch


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=ax.transAxes,
            arrowstyle="-|>",
            mutation_scale=9,
            lw=1.0,
            color=INK,
            shrinkA=2,
            shrinkB=2,
        )
    )


def _save(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for suffix in ("pdf", "svg", "png"):
        path = output_dir / f"{stem}.{suffix}"
        metadata: dict[str, Any] = {"Creator": "ChemWorld arXiv release figure pipeline"}
        if suffix == "pdf":
            metadata |= {
                "CreationDate": RELEASE_TIMESTAMP,
                "ModDate": RELEASE_TIMESTAMP,
            }
        elif suffix == "svg":
            metadata["Date"] = "2026-08-02T00:00:00Z"
        kwargs: dict[str, Any] = {
            "bbox_inches": "tight",
            "pad_inches": 0.035,
            "metadata": metadata,
        }
        if suffix == "png":
            kwargs["dpi"] = 360
        fig.savefig(path, **kwargs)
        if suffix == "svg":
            normalized = "\n".join(
                line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
            )
            path.write_text(normalized + "\n", encoding="utf-8", newline="\n")
        outputs.append(path)
    plt.close(fig)
    return outputs


def figure_1(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    qualification = data["environment_qualification"]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.55))

    ax = axes[0, 0]
    _panel(ax, "A", "The chemical world is the experimental apparatus")
    ax.axis("off")
    _box(ax, (0.02, 0.47), 0.20, 0.20, "agent\nselects action", edge=TEAL, face="#EDF7F5")
    _box(
        ax,
        (0.38, 0.43),
        0.25,
        0.28,
        "executable world\nchanges state",
        edge=OPAQUE,
        face="#ECF3F7",
        weight="semibold",
    )
    _box(ax, (0.78, 0.47), 0.20, 0.20, "public\nobservation", edge=AMBER, face="#FBF4E8")
    _arrow(ax, (0.23, 0.57), (0.37, 0.57))
    _arrow(ax, (0.64, 0.57), (0.77, 0.57))
    _arrow(ax, (0.87, 0.42), (0.13, 0.42))
    ax.text(
        0.50,
        0.33,
        "observation-conditioned next decision",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.6,
        bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 0.8},
    )
    _box(ax, (0.18, 0.07), 0.27, 0.13, "resource ledger", edge=MISINDEXED)
    _box(ax, (0.55, 0.07), 0.27, 0.13, "immutable trace", edge=MISINDEXED)
    _arrow(ax, (0.45, 0.42), (0.34, 0.21))
    _arrow(ax, (0.56, 0.42), (0.68, 0.21))

    ax = axes[0, 1]
    _panel(ax, "B", "Controlled contrasts separate agent from world")
    ax.axis("off")
    rows = [
        ("hidden physical identity", "matched", OPAQUE),
        ("material information", "intervened", NOMINAL),
        ("action authority", "compiled / primitive", TEAL),
        ("evidence access", "accounted", AMBER),
        ("resource endowment", "accounted", MISINDEXED),
    ]
    for index, (control, role, color) in enumerate(rows):
        y = 0.82 - index * 0.17
        _box(ax, (0.03, y), 0.53, 0.11, control, edge=color, fontsize=6.8)
        _box(
            ax,
            (0.64, y),
            0.31,
            0.11,
            role,
            edge=color,
            face=WASH,
            fontsize=6.5,
            weight="semibold",
        )

    ax = axes[1, 0]
    _panel(ax, "C", "Each transition remains auditable")
    ax.axis("off")
    stages = ["typed\nstate", "transaction", "resource\nreceipt", "trace", "physical\nreplay"]
    xs = np.linspace(0.08, 0.92, len(stages))
    ax.plot([xs[0], xs[-1]], [0.56, 0.56], transform=ax.transAxes, color=GRID, lw=4)
    for index, (x, label) in enumerate(zip(xs, stages, strict=True), start=1):
        ax.scatter(
            x,
            0.56,
            transform=ax.transAxes,
            s=150,
            color=OPAQUE,
            edgecolor=PAPER,
            linewidth=1.1,
            zorder=3,
        )
        ax.text(
            x,
            0.56,
            str(index),
            transform=ax.transAxes,
            color=PAPER,
            ha="center",
            va="center",
            fontsize=6.8,
            fontweight="bold",
        )
        ax.text(x, 0.37, label, transform=ax.transAxes, ha="center", va="top", fontsize=6.5)
    _box(
        ax,
        (0.12, 0.08),
        0.76,
        0.13,
        "invalid actions, failures and costs remain part of the evidence",
        edge=NOMINAL,
        fontsize=6.2,
    )

    ax = axes[1, 1]
    _panel(ax, "D", "Qualified surface and evidence scope")
    ax.axis("off")
    cards = [
        (qualification["registered_tasks"], "tasks", OPAQUE),
        (qualification["registered_operations"], "operations", TEAL),
        (qualification["registered_instruments"], "instruments", AMBER),
        (qualification["deterministic_complete_experiment_cases"], "boundary cases", MISINDEXED),
        (qualification["bound_success_endpoints"], "bound endpoints", NOMINAL),
    ]
    positions = [(0.02, 0.58), (0.35, 0.58), (0.68, 0.58), (0.18, 0.27), (0.53, 0.27)]
    for (value, label, color), (x, y) in zip(cards, positions, strict=True):
        width = 0.29 if y > 0.5 else 0.31
        _box(ax, (x, y), width, 0.22, "", edge=color, face=WASH)
        ax.text(
            x + width / 2,
            y + 0.145,
            f"{value:,}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=color,
        )
        ax.text(
            x + width / 2,
            y + 0.06,
            label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.5,
        )
    ax.text(
        0.5,
        0.09,
        "paper evidence: 2 compiled tasks · 1 autonomous task",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.6,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.06, right=0.995, top=0.94, bottom=0.08, wspace=0.27, hspace=0.50)
    return _save(fig, output_dir, "figure-1-controlled-apparatus")


def _g0_world_lookup(data: Mapping[str, Any]) -> dict[tuple[str, int, str], float]:
    return {
        (str(row["task_id"]), int(row["world_seed"]), str(row["arm"])): float(row["primary_score"])
        for row in data["g0"]["world_arm_rows"]
    }


def figure_2(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    lookup = _g0_world_lookup(data)
    task_ids = ["electrochemical-conversion", "reaction-to-crystallization"]
    contrast_rows = {
        row["task_id"]: row
        for row in data["g0"]["task_arm_rows"]
        if row["arm"] == "derived_contrasts"
    }
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.55))

    ax = axes[0, 0]
    _panel(ax, "A", "Information changes outcomes in a task-dependent way")
    for task_index, task_id in enumerate(task_ids):
        values = [
            lookup[(task_id, seed, "nominal")] - lookup[(task_id, seed, "opaque")]
            for seed in range(10)
        ]
        jitter = np.linspace(-0.12, 0.12, len(values))
        ax.scatter(values, task_index + jitter, s=19, color=INK, alpha=0.72, zorder=3)
        row = contrast_rows[task_id]
        mean = row["nominal_minus_opaque_mean"]
        low, high = row["nominal_minus_opaque_familywise_97_5_interval"]
        ax.errorbar(
            mean,
            task_index,
            xerr=[[mean - low], [high - mean]],
            fmt="s",
            ms=5.5,
            color=NOMINAL,
            capsize=2.5,
            lw=1.4,
            zorder=4,
        )
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks([0, 1], ["electrochemical\nconversion", "reaction to\ncrystallization"])
    ax.set_xlabel("nominal - opaque score (paired world)")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.invert_yaxis()

    ax = axes[0, 1]
    _panel(ax, "B", "A misindexed prior redirects experimental choices")
    world_rows = data["g0"]["world_arm_rows"]
    for task_index, task_id in enumerate(task_ids):
        rows = [
            row for row in world_rows if row["task_id"] == task_id and row["arm"] == "misindexed"
        ]
        for row in rows:
            x = [0 + task_index * 2.6, 1 + task_index * 2.6]
            y = [row["early_misleading_share"], row["late_misleading_share"]]
            ax.plot(x, y, color=MISINDEXED, alpha=0.24, lw=0.8)
            ax.scatter(x, y, color=MISINDEXED, s=11, alpha=0.55)
    ax.set_xticks([0, 1, 2.6, 3.6], ["early", "late", "early", "late"])
    ax.text(
        0.5, -0.22, "electrochemical", transform=ax.get_xaxis_transform(), ha="center", fontsize=6.4
    )
    ax.text(
        3.1, -0.22, "crystallization", transform=ax.get_xaxis_transform(), ha="center", fontsize=6.4
    )
    ax.set_ylabel("misleading-action share")
    ax.set_ylim(-0.04, 1.04)
    ax.grid(axis="y", color=GRID, lw=0.5)

    ax = axes[1, 0]
    _panel(ax, "C", "Manipulation, correction and recovery are separable")
    components = [
        "behavior\nchanged",
        "actions\ncorrected",
        "performance\nrestored",
        "joint\ncriterion",
    ]
    matrix = np.asarray(
        [
            [
                contrast_rows[task_id]["manipulation_check_passed"],
                contrast_rows[task_id]["differential_action_correction_passed"],
                contrast_rows[task_id]["performance_recovery_to_opaque_passed"],
                contrast_rows[task_id]["overall_recovery_claim_passed"],
            ]
            for task_id in task_ids
        ],
        dtype=bool,
    )
    ax.imshow(
        matrix, cmap=mpl.colors.ListedColormap(["#E7EBEE", TEAL]), vmin=0, vmax=1, aspect="auto"
    )
    ax.set_xticks(range(4), components)
    ax.set_yticks([0, 1], ["electrochemical", "crystallization"])
    ax.tick_params(length=0)
    for row_index in range(2):
        for column_index in range(4):
            passed = bool(matrix[row_index, column_index])
            ax.text(
                column_index,
                row_index,
                "PASS" if passed else "FAIL",
                ha="center",
                va="center",
                fontsize=6.2,
                fontweight="bold",
                color=PAPER if passed else MUTED,
            )
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1, 1]
    _panel(ax, "D", "Outcome and epistemic readouts form different profiles")
    opaque_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    metrics = [
        ("primary_score_mean", "endpoint\nscore", False),
        ("heldout_directional_accuracy", "held-out\naccuracy", False),
        ("heldout_brier_score", "Brier\nscore", True),
        ("unsupported_claim_rate", "unsupported\nclaims", True),
    ]
    x = np.arange(len(metrics))
    for row_index, row in enumerate(opaque_rows):
        for metric_index, (key, _label, lower_better) in enumerate(metrics):
            raw = float(row[key])
            favourable = 1.0 - raw if lower_better else raw
            ax.scatter(
                metric_index,
                row_index,
                s=42 + 90 * favourable,
                color=TEAL if row_index == 0 else AMBER,
                edgecolor=PAPER,
                linewidth=0.8,
            )
            ax.text(
                metric_index,
                row_index,
                f"{raw:.2f}",
                ha="center",
                va="center",
                fontsize=5.6,
                color=PAPER if favourable > 0.45 else INK,
                fontweight="semibold",
            )
    ax.set_xticks(x, [label for _key, label, _lower in metrics])
    ax.set_yticks([0, 1], ["electrochemical", "crystallization"])
    ax.set_xlim(-0.6, len(metrics) - 0.4)
    ax.set_ylim(-0.65, 1.65)
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(
        0.995,
        0.01,
        "circle area follows favourable direction within each column",
        ha="right",
        fontsize=5.8,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.105, right=0.995, top=0.93, bottom=0.16, wspace=0.43, hspace=0.58)
    return _save(fig, output_dir, "figure-2-compiled-controls")


def figure_3(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    demo = data["g2_v0_4"]["one_experiment_demonstration"]
    cells = data["g2_v0_4"]["cell_rows"]
    fig = plt.figure(figsize=(7.2, 3.35))
    grid = fig.add_gridspec(
        2, 2, width_ratios=[1.65, 1], height_ratios=[1, 0.72], wspace=0.29, hspace=0.48
    )
    ax = fig.add_subplot(grid[:, 0])
    bx = fig.add_subplot(grid[0, 1])
    cx = fig.add_subplot(grid[1, 1])

    _panel(ax, "A", "One vessel closes through agent-selected primitive operations")
    ax.axis("off")
    sequence = [
        ("add\nreagent", TEAL),
        ("add\nsolvent", TEAL),
        ("set\npotential", TEAL),
        ("electrolyze", TEAL),
        ("UV-vis\nobservation", AMBER),
        ("agent selects\nterminate", OPAQUE),
        ("final assay\n0.531", NOMINAL),
    ]
    positions = [
        (0.05, 0.67),
        (0.30, 0.67),
        (0.55, 0.67),
        (0.80, 0.67),
        (0.80, 0.29),
        (0.43, 0.29),
        (0.05, 0.29),
    ]
    for (label, color), (x, y) in zip(sequence, positions, strict=True):
        _box(
            ax,
            (x, y),
            0.16,
            0.16,
            label,
            edge=color,
            face=WASH,
            fontsize=6.4,
            weight="semibold" if "agent" in label else "normal",
        )
    for start, end in pairwise(positions[:4]):
        _arrow(ax, (start[0] + 0.16, start[1] + 0.08), (end[0], end[1] + 0.08))
    _arrow(ax, (0.88, 0.66), (0.88, 0.46))
    _arrow(ax, (0.80, 0.37), (0.60, 0.37))
    _arrow(ax, (0.43, 0.37), (0.22, 0.37))
    ax.text(
        0.50,
        0.12,
        "measurement enters the public state before the stop decision",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.5,
        color=MUTED,
    )

    _panel(bx, "B", "Ten campaigns completed all 60 vessels")
    bx.set_xlim(-0.8, 6.6)
    bx.set_ylim(-0.8, 9.8)
    for row_index, cell in enumerate(cells):
        color = OPAQUE if cell["arm"] == "opaque" else NOMINAL
        bx.scatter(
            np.arange(6),
            np.full(6, row_index),
            marker="s",
            s=35,
            color=color,
            edgecolor=PAPER,
            linewidth=0.6,
        )
    bx.set_xticks(range(6), [f"v{i}" for i in range(1, 7)])
    bx.set_yticks(range(10), [f"w{cell['world_seed']} {cell['arm'][0]}" for cell in cells])
    bx.invert_yaxis()
    bx.tick_params(length=0)
    for spine in bx.spines.values():
        spine.set_visible(False)
    bx.text(
        0.99,
        -0.18,
        "815 accepted primitive operations",
        transform=bx.transAxes,
        ha="right",
        fontsize=6.3,
        fontweight="semibold",
    )

    _panel(cx, "C", "The campaign ledger makes resource use reconstructable")
    cx.axis("off")
    ledger = demo["campaign_resource_endpoints"]
    rows = [
        ("vessels", ledger["vessel_starts"], 6),
        ("final assays", ledger["final_assays"], 6),
        ("instruments", ledger["nonfinal_instrument_uses"], 18),
        ("operations", ledger["operation_attempts"], 144),
    ]
    for index, (label, used, total) in enumerate(rows):
        y = 0.77 - index * 0.22
        cx.text(0.02, y + 0.06, label, transform=cx.transAxes, fontsize=6.3, color=MUTED)
        cx.text(
            0.98,
            y + 0.06,
            f"{used}/{total}",
            transform=cx.transAxes,
            fontsize=6.4,
            ha="right",
            fontweight="semibold",
        )
        cx.add_patch(Rectangle((0.02, y), 0.96, 0.055, transform=cx.transAxes, fc=GRID, ec="none"))
        cx.add_patch(
            Rectangle(
                (0.02, y),
                0.96 * min(float(used) / float(total), 1),
                0.055,
                transform=cx.transAxes,
                fc=TEAL if used < total else AMBER,
                ec="none",
            )
        )
    fig.subplots_adjust(left=0.06, right=0.995, top=0.92, bottom=0.10)
    return _save(fig, output_dir, "figure-3-autonomous-lifecycle")


def figure_4(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    cells = data["g2_v0_4"]["cell_rows"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.72), sharex=True, sharey=True)
    for panel_index, (ax, seed) in enumerate(zip(axes, (0, 2, 4), strict=True)):
        _panel(ax, chr(ord("A") + panel_index), f"Physical world {seed}")
        for arm, color in (("opaque", OPAQUE), ("nominal", NOMINAL)):
            row = next(item for item in cells if item["world_seed"] == seed and item["arm"] == arm)
            scores = np.asarray(row["final_score_sequence"], dtype=float)
            ordinals = np.arange(1, len(scores) + 1)
            ax.plot(ordinals, scores, "o-", color=color, ms=4.0, label=arm, zorder=2)
            best_index = int(np.argmax(scores))
            ax.scatter(
                ordinals[best_index],
                scores[best_index],
                s=85,
                facecolors="none",
                edgecolors=color,
                linewidth=1.4,
                zorder=3,
            )
            ax.scatter(
                ordinals[-1],
                scores[-1],
                s=30,
                marker="s",
                facecolors=PAPER,
                edgecolors=color,
                linewidth=1.2,
                zorder=4,
            )
        ax.set_xticks(range(1, 7))
        ax.set_ylim(-0.05, 0.92)
        ax.grid(color=GRID, lw=0.5)
        ax.set_xlabel("final-assay ordinal")
        if panel_index == 0:
            ax.set_ylabel("final-assay score")
            ax.legend(loc="lower right")
    handles = [
        plt.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="none",
            markeredgecolor=INK,
            linestyle="",
            label="first observed campaign best",
        ),
        plt.Line2D(
            [],
            [],
            marker="s",
            markerfacecolor=PAPER,
            markeredgecolor=INK,
            linestyle="",
            label="terminal assay",
        ),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.52, 0.055))
    fig.text(
        0.99,
        0.01,
        "selected development examples; not the replication estimand",
        ha="right",
        fontsize=5.9,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.07, right=0.995, top=0.89, bottom=0.29, wspace=0.16)
    return _save(fig, output_dir, "figure-4-trajectory-dynamics")


def figure_5(
    data: Mapping[str, Any],
    sensitivity: Mapping[str, Any],
    output_dir: Path,
) -> list[Path]:
    replication = data["g2_v0_5"]
    complete = [row for row in replication["paired_trajectories"] if row["pair_complete"]]
    classes = replication["interpretation"]["selected_branch"]["world_metric_classifications"]
    fig, (ax, bx) = plt.subplots(
        1,
        2,
        figsize=(7.2, 3.35),
        gridspec_kw={"width_ratios": (1.28, 1.0), "wspace": 0.42},
    )

    _panel(ax, "A", "Endpoint direction does not identify terminal retention")
    x_limit = 0.43
    y_limit = 0.55
    for origin, width, height in (
        ((-x_limit, 0), x_limit, y_limit),
        ((0, -y_limit), x_limit, y_limit),
    ):
        ax.add_patch(
            Rectangle(
                origin,
                width,
                height,
                facecolor=NOMINAL,
                alpha=0.055,
                edgecolor="none",
                zorder=0,
            )
        )
    endpoints = []
    terminals = []
    for row in complete:
        delta = row["nominal_minus_opaque"]
        endpoint = float(delta["best_final_score"])
        terminal = float(delta["terminal_to_global_best_ratio"])
        endpoints.append(endpoint)
        terminals.append(terminal)
        color = TEAL if int(row["world_seed"]) == 1 else AMBER
        ax.scatter(endpoint, terminal, s=54, color=color, edgecolor=PAPER, linewidth=0.8, zorder=3)
        ax.annotate(
            str(row["trajectory_replicate_id"]),
            (endpoint, terminal),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=5.8,
            color=INK,
        )
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlim(-x_limit, x_limit)
    ax.set_ylim(-y_limit, y_limit)
    ax.set_xlabel("nominal - opaque best-score contrast")
    ax.set_ylabel("nominal - opaque terminal / best contrast")
    ax.grid(color=GRID, lw=0.45, zorder=0)
    correlation = float(np.corrcoef(np.asarray(endpoints), np.asarray(terminals))[0, 1])
    opposite = sum(x * y < 0 for x, y in zip(endpoints, terminals, strict=True))
    zero_terminal = sum(abs(value) <= 1e-12 for value in terminals)
    ax.text(
        0.02,
        0.98,
        f"{opposite}/8 sign reversals + {zero_terminal} zero\nPearson r = {correlation:.3f}",
        transform=ax.transAxes,
        va="top",
        fontsize=6.4,
        fontweight="semibold",
        bbox={"facecolor": PAPER, "edgecolor": GRID, "boxstyle": "round,pad=0.25"},
    )
    ax.legend(
        handles=[
            plt.Line2D([], [], marker="o", color="none", markerfacecolor=TEAL, label="world 1"),
            plt.Line2D([], [], marker="o", color="none", markerfacecolor=AMBER, label="world 3"),
        ],
        loc="lower left",
        ncol=2,
    )

    _panel(bx, "B", "Lifecycle direction is usually not session-stable")
    metric_specs = [
        ("global_best_discovery_fraction", "earlier\ndiscovery", -1),
        ("online_incumbent_retention_rate", "retention", 1),
        ("maximum_absolute_incumbent_drawdown", "smaller\ndrawdown", -1),
        ("terminal_to_global_best_ratio", "terminal /\nbest", 1),
    ]
    matrix = np.zeros((2, len(metric_specs)), dtype=float)
    labels: list[list[str]] = []
    for row_index, seed in enumerate((1, 3)):
        row_labels = []
        for column_index, (metric, _label, direction) in enumerate(metric_specs):
            raw = str(classes[str(seed)][metric])
            value = {
                "directionally_positive": 1,
                "directionally_negative": -1,
                "mixed": 0,
                "stable_zero": 0,
            }[raw]
            value *= direction
            matrix[row_index, column_index] = value
            row_labels.append({1: "nominal", -1: "opaque", 0: "mixed"}[value])
        labels.append(row_labels)
    cmap = mpl.colors.ListedColormap(["#F5E7D0", "#EEF1F3", "#DDF0EC"])
    bx.imshow(matrix, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    bx.set_xticks(range(len(metric_specs)), [item[1] for item in metric_specs])
    bx.set_yticks((0, 1), ("world 1", "world 3"))
    bx.tick_params(length=0)
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            bx.text(
                column_index,
                row_index,
                labels[row_index][column_index],
                ha="center",
                va="center",
                fontsize=6.2,
                fontweight="semibold",
                color=INK,
            )
    for spine in bx.spines.values():
        spine.set_visible(False)
    censoring = sensitivity["g2_v0_5"]["right_censoring_missing_sign_sensitivity"]
    minimum_mixed = censoring["minimum_possible_mixed_core_classifications"]
    bx.text(
        0.5,
        -0.20,
        f"6/8 mixed; at least {minimum_mixed}/8 remain mixed\n"
        "under every sign assignment to the two censored pairs",
        transform=bx.transAxes,
        ha="center",
        va="top",
        fontsize=6.2,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.085, right=0.985, top=0.88, bottom=0.24)
    return _save(fig, output_dir, "figure-5-within-world-replication")


def figure_6(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.2, 3.28), gridspec_kw={"wspace": 0.52})
    opaque_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    compiled = [
        ("primary_score_mean", "endpoint score", False),
        ("heldout_directional_accuracy", "held-out accuracy", False),
        ("heldout_brier_score", "Brier score", True),
        ("unsupported_claim_rate", "unsupported claims", True),
    ]
    _panel(ax, "A", "Compiled control: task-conditioned readouts")
    for row_index, row in enumerate(opaque_rows):
        color = TEAL if row_index == 0 else AMBER
        for metric_index, (key, _label, lower_better) in enumerate(compiled):
            raw = float(row[key])
            favourable = 1.0 - raw if lower_better else raw
            ax.scatter(
                favourable,
                metric_index + (row_index - 0.5) * 0.16,
                s=36,
                color=color,
                edgecolor=PAPER,
                linewidth=0.6,
                label=row["task_id"].replace("-", " ") if metric_index == 0 else None,
            )
            ax.text(
                favourable + 0.025,
                metric_index + (row_index - 0.5) * 0.16,
                f"{raw:.2f}",
                va="center",
                fontsize=5.9,
                color=color,
            )
    ax.set_yticks(
        range(len(compiled)), [label + (" ↓" if lower else " ↑") for _key, label, lower in compiled]
    )
    ax.set_xlim(-0.02, 1.10)
    ax.set_xlabel("column-specific favourable direction")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.legend(loc="upper left")

    _panel(bx, "B", "Primitive control: lifecycle readouts")
    aggregate = data["g2_v0_4"]["arm_descriptive_aggregates"]
    lifecycle = [
        ("mean_completion_rate", None, "completion"),
        ("trajectory_learning", "mean_online_retention_rate", "retention"),
        ("trajectory_learning", "pooled_recovery_rate", "recovery"),
        ("trajectory_learning", "mean_terminal_to_global_best_ratio", "terminal / best"),
    ]
    for arm_index, (arm, color) in enumerate((("opaque", OPAQUE), ("nominal", NOMINAL))):
        for metric_index, (parent, child, _label) in enumerate(lifecycle):
            value = float(
                aggregate[arm][parent] if child is None else aggregate[arm][parent][child]
            )
            bx.scatter(
                value,
                metric_index + (arm_index - 0.5) * 0.16,
                s=36,
                color=color,
                edgecolor=PAPER,
                linewidth=0.6,
                label=arm if metric_index == 0 else None,
            )
            bx.text(
                value + 0.025,
                metric_index + (arm_index - 0.5) * 0.16,
                f"{value:.2f}",
                va="center",
                fontsize=5.9,
                color=color,
            )
    bx.set_yticks(range(len(lifecycle)), [label + " ↑" for _parent, _child, label in lifecycle])
    bx.set_xlim(-0.02, 1.10)
    bx.set_xlabel("reported metric value")
    bx.invert_yaxis()
    bx.grid(axis="x", color=GRID, lw=0.5)
    bx.legend(loc="upper left")
    fig.text(
        0.995,
        0.01,
        "Metrics remain separate readouts; no cross-metric composite is computed.",
        ha="right",
        fontsize=5.9,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.145, right=0.995, top=0.90, bottom=0.20)
    return _save(fig, output_dir, "figure-6-experimental-agency-profile")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--derived",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json",
    )
    parser.add_argument(
        "--sensitivity",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-p0-sensitivity.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "paper/arxiv/figures",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "paper/arxiv/figure-manifest.json",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = _load_hashed(
        args.derived.resolve(), schema=DERIVED_SCHEMA, hash_key="derived_data_sha256"
    )
    sensitivity = _load_hashed(
        args.sensitivity.resolve(), schema=SENSITIVITY_SCHEMA, hash_key="sensitivity_sha256"
    )
    _configure()
    output_dir = args.output_dir.resolve()
    outputs: list[Path] = []
    outputs.extend(figure_1(data, output_dir))
    outputs.extend(figure_2(data, output_dir))
    outputs.extend(figure_3(data, output_dir))
    outputs.extend(figure_4(data, output_dir))
    outputs.extend(figure_5(data, sensitivity, output_dir))
    outputs.extend(figure_6(data, output_dir))
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA,
        "status": "frozen_complete",
        "style_version": "arxiv-release-v1",
        "derived_data_sha256": data["derived_data_sha256"],
        "sensitivity_sha256": sensitivity["sensitivity_sha256"],
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _file_sha(path),
            }
            for path in outputs
        ],
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
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
                "figure_count": len(outputs) // 3,
                "file_count": len(outputs),
                "manifest": str(manifest_path),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
