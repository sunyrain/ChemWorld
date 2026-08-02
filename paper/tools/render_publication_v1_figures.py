"""Render publication-styled figures from the frozen arXiv derived-data object.

The release figures remain the audit-stable evidence view.  This renderer creates a
separate, typesetting-oriented view with journal-scale typography and no figure-level
headline; the full declarative legend supplies each figure title in the manuscript.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from itertools import pairwise
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
DATA_SCHEMA = "chemworld-arxiv-v1-derived-data-0.1"
STYLE_SCHEMA = "chemworld-publication-figure-manifest-0.1"

INK = "#17222E"
MUTED = "#687481"
GRID = "#DCE3E8"
PAPER = "#FFFFFF"
WASH = "#F4F7F8"
OPAQUE = "#26577C"
NOMINAL = "#D95F52"
TEAL = "#3D9487"
AMBER = "#E3A43E"
VIOLET = "#8066B3"
PALE_VIOLET = "#C3B5DF"
FAIL = "#E5E9ED"


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


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != DATA_SCHEMA:
        raise ValueError("unsupported arXiv derived-data schema")
    declared = data.pop("derived_data_sha256")
    actual = _canonical_sha(data)
    data["derived_data_sha256"] = declared
    if actual != declared:
        raise ValueError("derived-data content hash is invalid")
    return data


def _configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 7.2,
            "axes.titlesize": 8.4,
            "axes.labelsize": 7.4,
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
            "legend.fontsize": 6.8,
            "lines.linewidth": 1.25,
            "svg.hashsalt": "chemworld-publication-v1",
            "svg.fonttype": "none",
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
        fontsize=10.5,
        fontweight="bold",
        va="top",
        ha="left",
        color=INK,
    )
    ax.set_title(title, loc="left", pad=7, color=INK)


def _save(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    svg = output_dir / f"{stem}.svg"
    png = output_dir / f"{stem}.png"
    fig.savefig(
        svg,
        bbox_inches="tight",
        pad_inches=0.04,
        metadata={"Date": None, "Creator": "ChemWorld publication figure pipeline"},
    )
    normalized_svg = "\n".join(
        line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()
    )
    svg.write_text(normalized_svg + "\n", encoding="utf-8", newline="\n")
    fig.savefig(
        png,
        bbox_inches="tight",
        pad_inches=0.04,
        dpi=360,
        metadata={"Software": "ChemWorld publication figure pipeline"},
    )
    plt.close(fig)
    return [svg, png]


def _pill(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    color: str,
    *,
    filled: bool = False,
    fontsize: float = 6.8,
) -> None:
    face = color if filled else PAPER
    text_color = PAPER if filled else INK
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        transform=ax.transAxes,
        fc=face,
        ec=color,
        lw=0.9,
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
        color=text_color,
        fontweight="semibold" if filled else "normal",
    )


def _progress_bar(
    ax: plt.Axes, y: float, label: str, used: float, total: float, value: str
) -> None:
    ax.text(0.02, y + 0.035, label, transform=ax.transAxes, fontsize=6.5, color=MUTED)
    ax.text(
        0.98,
        y + 0.035,
        value,
        transform=ax.transAxes,
        fontsize=6.6,
        fontweight="semibold",
        ha="right",
    )
    ax.add_patch(
        FancyBboxPatch(
            (0.02, y - 0.005),
            0.96,
            0.025,
            boxstyle="round,pad=0,rounding_size=0.01",
            transform=ax.transAxes,
            fc=GRID,
            ec="none",
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (0.02, y - 0.005),
            0.96 * min(max(used / total, 0), 1),
            0.025,
            boxstyle="round,pad=0,rounding_size=0.01",
            transform=ax.transAxes,
            fc=TEAL if used / total < 0.85 else AMBER,
            ec="none",
        )
    )


def figure_1(data: dict[str, Any], output_dir: Path) -> list[Path]:
    q = data["environment_qualification"]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.45))

    ax = axes[0, 0]
    _panel(ax, "A", "A closed experimental loop")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    vessel = FancyBboxPatch(
        (0.40, 0.31),
        0.20,
        0.34,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        fc="#E8F2F4",
        ec=OPAQUE,
        lw=1.2,
    )
    ax.add_patch(vessel)
    ax.add_patch(Rectangle((0.42, 0.33), 0.16, 0.13, fc="#B8DEDF", ec="none"))
    ax.plot([0.46, 0.46], [0.45, 0.61], color=INK, lw=1.2)
    ax.plot([0.54, 0.54], [0.45, 0.61], color=INK, lw=1.2)
    ax.text(0.50, 0.23, "stateful process", ha="center", fontsize=6.4, color=MUTED)
    nodes = [
        (0.12, 0.60, "select\noperation", TEAL),
        (0.50, 0.86, "typed\ntransaction", AMBER),
        (0.88, 0.60, "measure\npublic state", VIOLET),
        (0.50, 0.08, "update belief\nand act again", NOMINAL),
    ]
    for x, y, label, color in nodes:
        circle = Circle((x, y), 0.095, transform=ax.transAxes, fc=WASH, ec=color, lw=1.1)
        ax.add_patch(circle)
        ax.text(x, y, label, transform=ax.transAxes, ha="center", va="center", fontsize=6.2)
    for (x1, y1, *_), (x2, y2, *_) in pairwise([*nodes, nodes[0]]):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            xycoords=ax.transAxes,
            arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 0.9, "shrinkA": 17, "shrinkB": 17},
        )

    ax = axes[0, 1]
    _panel(ax, "B", "Five controls can be intervened on separately")
    ax.axis("off")
    controls = [
        ("hidden physics", OPAQUE),
        ("material prior", NOMINAL),
        ("action authority", TEAL),
        ("evidence access", AMBER),
        ("resource endowment", VIOLET),
    ]
    for index, (label, color) in enumerate(controls):
        y = 0.81 - index * 0.16
        _pill(ax, (0.04, y), 0.42, 0.105, label, color, filled=index == 1)
        ax.plot([0.49, 0.62], [y + 0.052, y + 0.052], transform=ax.transAxes, color=color, lw=1)
        ax.add_patch(Circle((0.65, y + 0.052), 0.018, transform=ax.transAxes, fc=color, ec="none"))
    _pill(
        ax,
        (0.72, 0.37),
        0.26,
        0.20,
        "same world\ncontrolled contrast",
        INK,
        fontsize=5.9,
    )
    ax.annotate(
        "intervene",
        xy=(0.73, 0.47),
        xytext=(0.51, 0.71),
        xycoords=ax.transAxes,
        fontsize=6.2,
        color=NOMINAL,
        arrowprops={"arrowstyle": "-|>", "color": NOMINAL, "lw": 1},
    )

    ax = axes[1, 0]
    _panel(ax, "C", "Every transition leaves an auditable spine")
    ax.axis("off")
    spine = ["typed state", "transaction", "resource receipt", "immutable trace", "exact replay"]
    xs = np.linspace(0.08, 0.92, len(spine))
    ax.plot([xs[0], xs[-1]], [0.58, 0.58], color=GRID, lw=3, transform=ax.transAxes)
    for index, (x, label) in enumerate(zip(xs, spine, strict=True)):
        ax.scatter(
            x,
            0.58,
            s=130,
            color=OPAQUE,
            edgecolor=PAPER,
            linewidth=1,
            transform=ax.transAxes,
            zorder=3,
        )
        ax.text(
            x,
            0.58,
            str(index + 1),
            transform=ax.transAxes,
            color=PAPER,
            ha="center",
            va="center",
            fontsize=6.4,
            fontweight="bold",
        )
        ax.text(
            x,
            0.40,
            label.replace(" ", "\n", 1),
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=6.1,
        )
    _pill(
        ax,
        (0.13, 0.08),
        0.74,
        0.14,
        "invalid actions and failures remain evidence",
        NOMINAL,
        fontsize=5.9,
    )

    ax = axes[1, 1]
    _panel(ax, "D", "Qualified environment surface")
    labels = ["tasks", "operations", "instruments", "complete\ncases", "bound\nendpoints"]
    values = [
        q["registered_tasks"],
        q["registered_operations"],
        q["registered_instruments"],
        q["deterministic_complete_experiment_cases"],
        q["bound_success_endpoints"],
    ]
    shown = np.log10(np.asarray(values) + 1)
    colors = [OPAQUE, TEAL, AMBER, VIOLET, NOMINAL]
    x = np.arange(len(values))
    ax.vlines(x, 0, shown, color=colors, lw=3.2, alpha=0.85)
    ax.scatter(x, shown, s=42, color=colors, edgecolor=PAPER, linewidth=0.8, zorder=3)
    ax.set_xticks(x, labels)
    ax.set_ylabel("log10(count + 1)")
    ax.set_ylim(0, max(shown) + 0.35)
    ax.grid(axis="y", color=GRID, lw=0.55)
    for xi, yi, value in zip(x, shown, values, strict=True):
        ax.text(
            xi,
            yi + 0.11,
            f"{value:,}",
            ha="center",
            va="bottom",
            fontsize=6.4,
            fontweight="semibold",
        )
    fig.subplots_adjust(left=0.07, right=0.99, top=0.94, bottom=0.10, wspace=0.28, hspace=0.47)
    return _save(fig, output_dir, "figure-1-controlled-apparatus")


def figure_2(data: dict[str, Any], output_dir: Path) -> list[Path]:
    demo = data["g2_v0_4"]["one_experiment_demonstration"]
    fig, (ax, ledger_ax) = plt.subplots(
        1, 2, figsize=(7.2, 2.78), gridspec_kw={"width_ratios": [2.25, 1], "wspace": 0.22}
    )
    _panel(ax, "A", "One vessel; seven agent-selected primitive operations")
    sequence = demo["operation_signature"]
    x = np.arange(len(sequence))
    colors = [TEAL, TEAL, AMBER, OPAQUE, VIOLET, MUTED, NOMINAL]
    ax.plot(x, np.zeros_like(x), color=GRID, lw=4, zorder=1)
    ax.scatter(x, np.zeros_like(x), s=350, c=colors, edgecolor=PAPER, linewidth=1.5, zorder=3)
    for index, label in enumerate(sequence):
        ax.text(
            index,
            0,
            str(index + 1),
            ha="center",
            va="center",
            color=PAPER,
            fontsize=7.0,
            fontweight="bold",
        )
        ax.text(
            index,
            -0.27 if index % 2 == 0 else 0.27,
            label.replace("_", "\n"),
            ha="center",
            va="center",
            fontsize=6.1,
        )
    ax.text(
        0.01,
        0.03,
        f"final assay = {demo['final_score']:.3f}",
        transform=ax.transAxes,
        color=NOMINAL,
        fontweight="bold",
        fontsize=7.2,
    )
    ax.text(
        0.01,
        -0.05,
        "development demonstration; excluded from prior-effect inference",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=5.8,
    )
    ax.set_xlim(-0.55, len(x) - 0.45)
    ax.set_ylim(-0.51, 0.51)
    ax.axis("off")

    _panel(ledger_ax, "B", "Campaign resource receipt")
    ledger_ax.axis("off")
    ledger = demo["campaign_resource_endpoints"]
    rows = [
        ("vessels", ledger["vessel_starts"], 6, f"{ledger['vessel_starts']}/6"),
        ("final assays", ledger["final_assays"], 6, f"{ledger['final_assays']}/6"),
        (
            "non-final instruments",
            ledger["nonfinal_instrument_uses"],
            18,
            f"{ledger['nonfinal_instrument_uses']}/18",
        ),
        (
            "operation attempts",
            ledger["operation_attempts"],
            144,
            f"{ledger['operation_attempts']}/144",
        ),
        (
            "reagent",
            ledger["stocks_used"]["reagent_mol"],
            0.48,
            f"{ledger['stocks_used']['reagent_mol']:.2f}/0.48 mol",
        ),
        (
            "solvent",
            ledger["stocks_used"]["solvent_L"],
            0.96,
            f"{ledger['stocks_used']['solvent_L']:.2f}/0.96 L",
        ),
    ]
    for y, row in zip(np.linspace(0.83, 0.10, len(rows)), rows, strict=True):
        _progress_bar(ledger_ax, float(y), *row)
    ledger_ax.text(
        0.02,
        -0.02,
        "reconstructed from the immutable trajectory",
        transform=ledger_ax.transAxes,
        fontsize=5.8,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.07, right=0.99, top=0.90, bottom=0.12)
    return _save(fig, output_dir, "figure-2-one-autonomous-experiment")


def figure_3(data: dict[str, Any], output_dir: Path) -> list[Path]:
    cells = data["g2_v0_4"]["cell_rows"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.52), sharex=True, sharey=True)
    for panel_index, (ax, seed) in enumerate(zip(axes, (0, 2, 4), strict=True)):
        _panel(ax, chr(ord("A") + panel_index), f"Physical world {seed}")
        for arm, color in (("opaque", OPAQUE), ("nominal", NOMINAL)):
            row = next(item for item in cells if item["world_seed"] == seed and item["arm"] == arm)
            scores = np.asarray(row["final_score_sequence"], dtype=float)
            ordinals = np.arange(1, len(scores) + 1)
            ax.plot(ordinals, scores, "o-", color=color, ms=3.8, label=arm, zorder=2)
            best_index = int(np.argmax(scores))
            ax.scatter(
                ordinals[best_index],
                scores[best_index],
                s=82,
                facecolors="none",
                edgecolors=color,
                linewidth=1.4,
                zorder=3,
            )
            ax.scatter(
                ordinals[-1],
                scores[-1],
                s=26,
                marker="s",
                facecolors=PAPER,
                edgecolors=color,
                linewidth=1.2,
                zorder=4,
            )
        ax.set_xticks(range(1, 7))
        ax.set_ylim(-0.04, 0.92)
        ax.grid(color=GRID, lw=0.5)
        ax.set_xlabel("final-assay ordinal")
        if panel_index == 0:
            ax.set_ylabel("final-assay score")
            ax.legend(loc="lower right", handlelength=2.1)
    fig.subplots_adjust(left=0.07, right=0.995, top=0.88, bottom=0.19, wspace=0.16)
    return _save(fig, output_dir, "figure-3-behaviorally-distinct-trajectories")


def figure_4(data: dict[str, Any], output_dir: Path) -> list[Path]:
    g0_rows = data["g0"]["task_arm_rows"]
    contrasts = [row for row in g0_rows if row["arm"] == "derived_contrasts"]
    g2_pairs = data["g2_v0_4"]["paired_world_rows"]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.62))

    ax = axes[0, 0]
    _panel(ax, "A", "Correct material information has task-dependent effects")
    for index, row in enumerate(contrasts):
        mean = row["nominal_minus_opaque_mean"]
        low, high = row["nominal_minus_opaque_familywise_97_5_interval"]
        ax.errorbar(
            mean,
            index,
            xerr=[[mean - low], [high - mean]],
            fmt="o",
            ms=4.5,
            color=NOMINAL,
            capsize=2.5,
            lw=1.2,
        )
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks(range(len(contrasts)), [row["task_id"].replace("-", " ") for row in contrasts])
    ax.set_xlabel("nominal - opaque final score")
    ax.grid(axis="x", color=GRID, lw=0.5)

    ax = axes[0, 1]
    _panel(ax, "B", "A misindexed prior changes selected actions")
    y = np.arange(len(contrasts))
    height = 0.29
    ax.barh(
        y - height / 2,
        [r["early_misleading_share_misindexed"] for r in contrasts],
        height=height,
        color=VIOLET,
        label="early",
    )
    ax.barh(
        y + height / 2,
        [r["late_misleading_share_misindexed"] for r in contrasts],
        height=height,
        color=PALE_VIOLET,
        label="late",
    )
    ax.set_yticks(y, [row["task_id"].replace("-", " ") for row in contrasts])
    ax.set_xlim(0, 1)
    ax.set_xlabel("misleading-action share")
    ax.legend(loc="lower right", ncol=2)
    ax.grid(axis="x", color=GRID, lw=0.5)

    ax = axes[1, 0]
    _panel(ax, "C", "Manipulation, correction and recovery are distinct")
    components = [
        "behavior\nchanged",
        "actions\ncorrected",
        "performance\nrecovered",
        "joint\nrecovery",
    ]
    matrix = np.asarray(
        [
            [
                row["manipulation_check_passed"],
                row["differential_action_correction_passed"],
                row["performance_recovery_to_opaque_passed"],
                row["overall_recovery_claim_passed"],
            ]
            for row in contrasts
        ],
        dtype=float,
    )
    ax.imshow(matrix, vmin=0, vmax=1, cmap=mpl.colors.ListedColormap([FAIL, TEAL]), aspect="auto")
    ax.set_xticks(range(4), components)
    ax.set_yticks(range(len(contrasts)), [row["task_id"].replace("-", " ") for row in contrasts])
    ax.tick_params(length=0)
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            passed = bool(matrix[row_index, column_index])
            ax.text(
                column_index,
                row_index,
                "PASS" if passed else "—",
                ha="center",
                va="center",
                color=PAPER if passed else MUTED,
                fontsize=6.0,
                fontweight="bold",
            )
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1, 1]
    _panel(ax, "D", "Autonomous trajectory effects differ by physical world")
    metrics = [
        ("global_best_discovery_fraction", "discovery"),
        ("online_incumbent_retention_rate", "retention"),
        ("maximum_absolute_incumbent_drawdown", "drawdown"),
        ("terminal_to_global_best_ratio", "terminal/best"),
    ]
    seeds = [row["world_seed"] for row in g2_pairs]
    seed_colors = dict(zip(seeds, [OPAQUE, TEAL, AMBER, VIOLET, NOMINAL], strict=True))
    for metric_index, (key, _label) in enumerate(metrics):
        values = [row[key] for row in g2_pairs]
        offsets = np.linspace(-0.18, 0.18, len(values))
        for offset, value, row in zip(offsets, values, g2_pairs, strict=True):
            ax.scatter(
                metric_index + offset,
                value,
                s=29,
                color=seed_colors[row["world_seed"]],
                edgecolor=PAPER,
                linewidth=0.6,
                zorder=3,
            )
        ax.hlines(np.mean(values), metric_index - 0.23, metric_index + 0.23, color=INK, lw=1.4)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(range(len(metrics)), [label for _, label in metrics])
    ax.set_ylabel("nominal - opaque")
    ax.grid(axis="y", color=GRID, lw=0.5)
    handles = [
        plt.Line2D([], [], marker="o", linestyle="", color=color, label=str(seed), markersize=4)
        for seed, color in seed_colors.items()
    ]
    ax.legend(
        handles=handles,
        title="world",
        title_fontsize=6.4,
        ncol=5,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.36),
        columnspacing=0.7,
        handletextpad=0.25,
    )
    fig.subplots_adjust(left=0.10, right=0.995, top=0.93, bottom=0.13, wspace=0.45, hspace=0.55)
    return _save(fig, output_dir, "figure-4-prior-reshapes-behavior")


def figure_5(data: dict[str, Any], output_dir: Path) -> list[Path]:
    replication = data["g2_v0_5"]
    if replication is None:
        return []
    metrics = [
        ("best_final_score", "Best score"),
        ("global_best_discovery_fraction", "Discovery"),
        ("online_incumbent_retention_rate", "Retention"),
        ("maximum_absolute_incumbent_drawdown", "Drawdown"),
        ("terminal_to_global_best_ratio", "Terminal/best"),
    ]
    classifications = replication["interpretation"]["selected_branch"][
        "world_metric_classifications"
    ]
    fig, axes = plt.subplots(2, 5, figsize=(7.2, 3.48), sharex="col")
    for row_index, seed in enumerate((1, 3)):
        pair_rows = [row for row in replication["paired_trajectories"] if row["world_seed"] == seed]
        for column_index, (metric, label) in enumerate(metrics):
            ax = axes[row_index, column_index]
            if row_index == 0:
                _panel(ax, chr(ord("A") + column_index), label)
            values: list[float | None] = []
            labels: list[str] = []
            for row in pair_rows:
                labels.append(row["trajectory_replicate_id"])
                delta = row["nominal_minus_opaque"]
                values.append(None if delta is None else delta[metric])
            y = np.arange(len(values))
            for yi, value in zip(y, values, strict=True):
                if value is None:
                    ax.scatter(0, yi, marker="x", color=MUTED, s=27, linewidth=1.2, zorder=3)
                else:
                    ax.plot([0, value], [yi, yi], color=GRID, lw=1.2, zorder=1)
                    ax.scatter(
                        value,
                        yi,
                        color=NOMINAL if value >= 0 else OPAQUE,
                        s=25,
                        edgecolor=PAPER,
                        linewidth=0.5,
                        zorder=3,
                    )
            ax.axvline(0, color=MUTED, lw=0.7)
            classification = classifications[str(seed)][metric].replace("directionally_", "")
            pill_color = {"positive": NOMINAL, "negative": OPAQUE, "mixed": MUTED}.get(
                classification, MUTED
            )
            ax.text(
                0.97,
                1.02,
                classification,
                transform=ax.transAxes,
                ha="right",
                va="bottom",
                fontsize=5.8,
                color=pill_color,
                fontweight="semibold",
            )
            ax.set_yticks(y, labels if column_index == 0 else [])
            if column_index == 0:
                ax.set_ylabel(f"world {seed}\nreplicate")
            ax.grid(axis="x", color=GRID, lw=0.45)
            if row_index == 1:
                ax.set_xlabel("nominal - opaque", fontsize=6.1)
    fig.text(0.995, 0.01, "x right-censored", ha="right", va="bottom", fontsize=5.8, color=MUTED)
    fig.subplots_adjust(left=0.075, right=0.995, top=0.89, bottom=0.18, wspace=0.31, hspace=0.29)
    return _save(fig, output_dir, "figure-5-within-world-replication")


def _profile_panel(
    ax: plt.Axes,
    rows: list[tuple[str, list[float], str]],
    labels: list[str],
    panel: str,
    title: str,
) -> None:
    _panel(ax, panel, title)
    y = np.arange(len(labels))
    offsets = np.linspace(-0.11, 0.11, len(rows))
    for offset, (name, values, color) in zip(offsets, rows, strict=True):
        ax.plot(values, y + offset, color=color, lw=1.0, alpha=0.65, zorder=1)
        ax.scatter(
            values,
            y + offset,
            color=color,
            s=30,
            edgecolor=PAPER,
            linewidth=0.6,
            label=name,
            zorder=3,
        )
    ax.set_yticks(y, labels)
    ax.set_xlim(-0.02, 1.02)
    ax.set_xticks([0, 0.25, 0.50, 0.75, 1.0])
    ax.set_xlabel("reported metric value")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.legend(loc="lower right")


def figure_6(data: dict[str, Any], output_dir: Path) -> list[Path]:
    g0_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    g2 = data["g2_v0_4"]["arm_descriptive_aggregates"]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.2, 3.15), gridspec_kw={"wspace": 0.48})
    compiled_metrics = [
        ("primary_score_mean", "endpoint score ↑"),
        ("heldout_directional_accuracy", "held-out accuracy ↑"),
        ("heldout_brier_score", "Brier score ↓"),
        ("unsupported_claim_rate", "unsupported claims ↓"),
    ]
    compiled_rows = []
    for index, row in enumerate(g0_rows):
        compiled_rows.append(
            (
                row["task_id"].replace("-", " "),
                [row[key] for key, _ in compiled_metrics],
                OPAQUE if index == 0 else NOMINAL,
            )
        )
    _profile_panel(
        ax,
        compiled_rows,
        [label for _, label in compiled_metrics],
        "A",
        "Compiled control: task-dependent profiles",
    )

    trajectory_metrics = [
        ("mean_completion_rate", "completion ↑"),
        ("trajectory_learning.mean_online_retention_rate", "retention ↑"),
        ("trajectory_learning.pooled_recovery_rate", "recovery ↑"),
        ("trajectory_learning.mean_terminal_to_global_best_ratio", "terminal/best ↑"),
    ]
    trajectory_rows = []
    for arm, color in (("opaque", OPAQUE), ("nominal", NOMINAL)):
        values = []
        for key, _ in trajectory_metrics:
            if "." in key:
                parent, child = key.split(".")
                values.append(g2[arm][parent][child])
            else:
                values.append(g2[arm][key])
        trajectory_rows.append((arm, values, color))
    _profile_panel(
        bx,
        trajectory_rows,
        [label for _, label in trajectory_metrics],
        "B",
        "Agent-directed control: lifecycle profiles",
    )
    fig.subplots_adjust(left=0.15, right=0.995, top=0.89, bottom=0.18)
    return _save(fig, output_dir, "figure-6-experimental-intelligence-profiles")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "derived_data",
        nargs="?",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("paper/figures/experimental-intelligence-v1/publication"),
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=Path("paper/figures/experimental-intelligence-v1/publication-figure-manifest.json"),
    )
    return parser


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = _load(_resolve(args.derived_data))
    output_dir = _resolve(args.output_dir)
    _configure()
    outputs: list[Path] = []
    for renderer in (figure_1, figure_2, figure_3, figure_4, figure_5, figure_6):
        outputs.extend(renderer(data, output_dir))
    manifest: dict[str, Any] = {
        "schema_version": STYLE_SCHEMA,
        "status": data["status"],
        "derived_data_sha256": data["derived_data_sha256"],
        "style_version": "nature-editorial-v1",
        "figure_5_rendered": data["g2_v0_5"] is not None,
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": _file_sha(path),
                "bytes": path.stat().st_size,
            }
            for path in outputs
        ],
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
    manifest_path = _resolve(args.manifest_output)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": data["status"],
                "figure_file_count": len(outputs),
                "manifest": manifest_path.as_posix(),
            },
            sort_keys=True,
        )
    )
    return 0 if data["status"] == "frozen_complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
