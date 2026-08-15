#!/usr/bin/env python3
"""Render reusable Work II DeepSeek C2 result and agent-workflow figures.

Figure contract
---------------
Core conclusion: behavior is task- and locus-dependent; show completion, achieved
score, within-session improvement, prior revision, and the actual operation
vocabulary.  The caller must identify whether the input is historical pre-fix data
or terminal corrected-semantics evidence.
Archetypes: quantitative grid, operation-strategy heatmap, schematic workflow grid.
Backend: Python/matplotlib only.  Every plotted observation comes from cell summaries.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Editable text and consistent sans-serif typography are required for reuse.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
# Canonical validator notation: svg.fonttype='none'; pdf.fonttype=42.
PREVIEW_DPI = 300
SUBMISSION_DPI = 600
plt.rcParams.update(
    {
        "font.size": 7,
        "axes.labelsize": 7,
        "axes.titlesize": 8,
        "axes.linewidth": 0.8,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "legend.fontsize": 6,
        "legend.frameon": False,
    }
)

ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
ARM_LABELS = {
    "opaque": "Opaque",
    "aligned_nominal": "Aligned",
    "misindexed_nominal": "Misindexed",
}
ARM_COLORS = {
    "opaque": "#7884B4",
    "aligned_nominal": "#2B8C7E",
    "misindexed_nominal": "#C65D57",
}
BLOCK_ORDER = {"A_E_public": 0, "A_P": 1, "A_S": 2}
TASK_ORDER = {
    "electrochemical-conversion": 0,
    "reaction-to-distillation": 1,
    "partition-discovery": 2,
    "reaction-safety-constrained": 3,
    "reaction-to-crystallization": 4,
}
TASK_LABELS = {
    "electrochemical-conversion": "Electrochemistry",
    "reaction-to-distillation": "Distillation",
    "partition-discovery": "Partition",
    "reaction-safety-constrained": "Reaction safety",
    "reaction-to-crystallization": "Crystallization",
}
DEFAULT_SCHEDULED = {"A_E_public": 8, "A_P": 10, "A_S": 12}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _number(value: Any, default: float = math.nan) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return default
    return float(value)


def _int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return default
    return int(value)


def _cell_identity(cell_dir: Path) -> tuple[str, str, int, str]:
    parts = cell_dir.name.split("--")
    if len(parts) != 4 or not parts[2].startswith("seed"):
        raise ValueError(f"Unexpected cell directory: {cell_dir.name}")
    return parts[0], parts[1], int(parts[2][4:]), parts[3]


def _task_group(block: str, task: str) -> str:
    locus = {"A_E_public": "A-E", "A_P": "A-P", "A_S": "A-S"}.get(block, block)
    return f"{locus} {TASK_LABELS.get(task, task)}"


def _operation_name(operation: Mapping[str, Any]) -> str:
    name = str(operation.get("operation", "unknown"))
    if name == "measure":
        return f"measure:{operation.get('instrument', 'unknown')}"
    return name


def _compact_operation(operation: Mapping[str, Any]) -> str:
    name = str(operation.get("operation", "unknown"))
    if name == "add_solvent":
        amount = 1e3 * _number(operation.get("volume_L"), 0)
        return f"Solvent {operation.get('solvent', '?')}\n{amount:.0f} mL"
    if name == "add_reagent":
        return f"Reagent\n{1e3 * _number(operation.get('amount_mol'), 0):.1f} mmol"
    if name == "add_catalyst":
        amount = 1e3 * _number(operation.get("catalyst_amount_mol"), 0)
        return f"Catalyst {operation.get('catalyst', '?')}\n{amount:.2f} mmol"
    if name == "add_phase":
        amount = 1e3 * _number(operation.get("volume_L"), 0)
        return f"Add {operation.get('phase', '?')}\n{amount:.0f} mL"
    if name == "add_extractant":
        amount = 1e3 * _number(operation.get("volume_L"), 0)
        return f"Extractant {operation.get('extractant', '?')}\n{amount:.0f} mL"
    if name in {"heat", "cool_crystallize", "distill", "run_flow"}:
        temperature = _number(operation.get("target_temperature_K"))
        duration = _number(operation.get("duration_s"), 0) / 60.0
        return f"{name.replace('_', ' ').title()}\n{temperature:.0f} K · {duration:.0f} min"
    if name in {"mix", "wait", "settle", "electrolyze", "concentrate", "evaporate"}:
        duration = _number(operation.get("duration_s"), 0) / 60.0
        return f"{name.replace('_', ' ').title()}\n{duration:.0f} min"
    if name == "set_potential":
        return f"Set potential\n{_number(operation.get('potential_V'), 0):.2f} V"
    if name == "measure":
        return f"Measure\n{str(operation.get('instrument', '?')).replace('_', ' ')}"
    if name == "collect_fraction":
        return f"Collect cut\n{100 * _number(operation.get('transfer_fraction'), 0):.0f}%"
    if name == "separate_phase":
        return f"Separate\n{operation.get('target_phase', '?')}"
    return name.replace("_", " ").title()


def _operation_class(name: str) -> str:
    base = name.split(":", 1)[0]
    if base.startswith("add_"):
        return "charge"
    if base in {"heat", "wait", "quench", "electrolyze", "set_potential", "run_flow"}:
        return "transform"
    if base in {
        "mix",
        "settle",
        "separate_phase",
        "wash",
        "dry",
        "concentrate",
        "distill",
        "evaporate",
        "collect_fraction",
        "transfer",
        "filter_crystals",
    }:
        return "separation"
    if base == "measure":
        return "measurement"
    return "control"


def collect_rows(
    input_root: Path,
    *,
    excluded_tasks: set[str],
    included_block_tasks: set[tuple[str, str]] | None = None,
    excluded_block_tasks: set[tuple[str, str]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    cells_dir = input_root / "cells"
    if not cells_dir.is_dir():
        raise FileNotFoundError(f"Missing cells directory: {cells_dir}")
    top_summary = _load_json(input_root / "summary.json")
    scheduled_by_cell = {
        str(row.get("cell_id")): _int(row.get("scheduled_experiments"))
        for row in top_summary.get("cells", [])
        if isinstance(row, Mapping)
    }
    all_cell_dirs = sorted(path.parent for path in cells_dir.glob("*/summary.json"))
    cell_rows: list[dict[str, Any]] = []
    experiment_rows: list[dict[str, Any]] = []
    excluded_cell_count = 0
    excluded_pairs = excluded_block_tasks or set()
    for cell_dir in all_cell_dirs:
        block, task, seed, arm = _cell_identity(cell_dir)
        identity = (block, task)
        if (
            task in excluded_tasks
            or identity in excluded_pairs
            or (included_block_tasks is not None and identity not in included_block_tasks)
        ):
            excluded_cell_count += 1
            continue
        summary = _load_json(cell_dir / "summary.json")
        analysis = summary.get("analysis", {})
        analysis = analysis if isinstance(analysis, Mapping) else {}
        resources = summary.get("method_resources", {})
        resources = resources if isinstance(resources, Mapping) else {}
        experiments = analysis.get("experiments", [])
        experiments = experiments if isinstance(experiments, Sequence) else []
        score_values: list[float] = []
        for experiment in experiments:
            if not isinstance(experiment, Mapping):
                continue
            score = _number(experiment.get("leaderboard_score"))
            if math.isfinite(score):
                score_values.append(score)
            committed = experiment.get("committed_operations", [])
            committed = committed if isinstance(committed, Sequence) else []
            experiment_rows.append(
                {
                    "cell_id": cell_dir.name,
                    "block": block,
                    "task": task,
                    "task_group": _task_group(block, task),
                    "world_seed": seed,
                    "arm": arm,
                    "experiment_index": _int(experiment.get("experiment_index")),
                    "leaderboard_score": score,
                    "recipe_sha256": str(experiment.get("recipe_sha256", "")),
                    "committed_operation_count": len(committed),
                    "committed_operations": [
                        dict(value) for value in committed if isinstance(value, Mapping)
                    ],
                }
            )
        reliability = analysis.get("prior_reliability_trajectory", [])
        reliability = reliability if isinstance(reliability, Sequence) else []
        numeric_reliability = [
            float(value)
            for value in reliability
            if isinstance(value, int | float) and not isinstance(value, bool)
        ]
        scheduled = scheduled_by_cell.get(cell_dir.name, DEFAULT_SCHEDULED.get(block, 0))
        completed_experiments = _int(analysis.get("complete_experiment_count"))
        cell_rows.append(
            {
                "cell_id": cell_dir.name,
                "block": block,
                "task": task,
                "task_group": _task_group(block, task),
                "world_seed": seed,
                "arm": arm,
                "scheduled_experiments": scheduled,
                "complete_experiments": completed_experiments,
                "completion_fraction": (
                    completed_experiments / scheduled if scheduled else math.nan
                ),
                "session_completed": summary.get("completed") is True,
                "qualification_passed": summary.get("qualification", {}).get("passed") is True,
                "unique_recipe_count": _int(analysis.get("unique_recipe_count")),
                "exact_repeat_count": _int(analysis.get("exact_repeat_count")),
                "operation_attempt_count": _int(analysis.get("operation_attempt_count")),
                "committed_operation_count": _int(analysis.get("committed_operation_count")),
                "resource_rejection_count": _int(analysis.get("resource_rejection_count")),
                "dynamic_physical_failure_count": _int(
                    analysis.get("dynamic_physical_failure_count")
                ),
                "unsafe_outcome_count": _int(analysis.get("unsafe_outcome_count")),
                "mcp_recovery_episode_count": _int(
                    resources.get("scientific_compliance_mcp_tool_failure_episode_count")
                ),
                "first_score": score_values[0] if score_values else math.nan,
                "best_score": max(score_values) if score_values else math.nan,
                "best_minus_first": (
                    max(score_values) - score_values[0] if score_values else math.nan
                ),
                "prior_reliability_initial": (
                    numeric_reliability[0] if numeric_reliability else math.nan
                ),
                "prior_reliability_final": (
                    numeric_reliability[-1] if numeric_reliability else math.nan
                ),
                "prior_reliability_delta": (
                    numeric_reliability[-1] - numeric_reliability[0]
                    if numeric_reliability
                    else math.nan
                ),
                "failure": "" if summary.get("failure") is None else str(summary.get("failure")),
            }
        )
    metadata = {
        # Keep generated reports portable instead of embedding a workstation path.
        "input_run": input_root.name,
        "all_cell_summaries": len(all_cell_dirs),
        "included_cell_summaries": len(cell_rows),
        "excluded_cell_summaries": excluded_cell_count,
        "excluded_tasks": sorted(excluded_tasks),
        "included_block_tasks": (
            [f"{block}:{task}" for block, task in sorted(included_block_tasks)]
            if included_block_tasks is not None
            else None
        ),
        "excluded_block_tasks": [
            f"{block}:{task}" for block, task in sorted(excluded_pairs)
        ],
        "top_summary_status": top_summary.get("status"),
    }
    return cell_rows, experiment_rows, metadata


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            rendered = {
                key: (
                    json.dumps(value, ensure_ascii=False, sort_keys=True)
                    if isinstance(value, list | dict)
                    else value
                )
                for key, value in row.items()
            }
            writer.writerow(rendered)


def _task_groups(cell_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    identities = {(str(row["block"]), str(row["task"])) for row in cell_rows}
    ordered = sorted(
        identities,
        key=lambda item: (BLOCK_ORDER.get(item[0], 99), TASK_ORDER.get(item[1], 99)),
    )
    return [_task_group(block, task) for block, task in ordered]


def _add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.03,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        va="bottom",
    )


def _strip_panel(
    ax: plt.Axes,
    rows: Sequence[Mapping[str, Any]],
    *,
    task_groups: Sequence[str],
    field: str,
    ylabel: str,
    ylim: tuple[float, float] | None = None,
    arms: Sequence[str] = ARMS,
    zero_line: bool = False,
) -> None:
    offsets = np.linspace(-0.24, 0.24, len(arms))
    for task_index, task_group in enumerate(task_groups):
        for arm_index, arm in enumerate(arms):
            values = np.array(
                [
                    _number(row.get(field))
                    for row in rows
                    if row.get("task_group") == task_group and row.get("arm") == arm
                ],
                dtype=float,
            )
            values = values[np.isfinite(values)]
            if values.size == 0:
                continue
            x = task_index + offsets[arm_index]
            jitter = np.linspace(-0.035, 0.035, values.size) if values.size > 1 else np.array([0])
            ax.scatter(
                x + jitter,
                values,
                s=10,
                color=ARM_COLORS[arm],
                alpha=0.62,
                linewidth=0,
                zorder=2,
            )
            mean = float(values.mean())
            ax.plot(
                [x - 0.07, x + 0.07],
                [mean, mean],
                color=ARM_COLORS[arm],
                lw=2.0,
                zorder=3,
            )
    if zero_line:
        ax.axhline(0.0, color="#767676", lw=0.8, linestyle="--", zorder=0)
    ax.set_xticks(range(len(task_groups)))
    ax.set_xticklabels(task_groups, rotation=34, ha="right")
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.6)


def _export(
    fig: plt.Figure,
    output_base: Path,
    *,
    export_tiff: bool,
) -> list[str]:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    formats: list[tuple[str, dict[str, Any]]] = [
        (".svg", {}),
        (".pdf", {}),
        (".png", {"dpi": PREVIEW_DPI}),
    ]
    if export_tiff:
        formats.append((".tiff", {"dpi": SUBMISSION_DPI}))
    for suffix, kwargs in formats:
        path = output_base.with_suffix(suffix)
        fig.savefig(path, bbox_inches="tight", facecolor="white", **kwargs)
        if suffix == ".svg":
            _normalize_svg_whitespace(path)
        outputs.append(path.name)
    plt.close(fig)
    return outputs


def _normalize_svg_whitespace(path: Path) -> None:
    """Remove renderer-only line-end spaces so generated SVGs stay Git-clean."""
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip(" \t") for line in text.splitlines())
    if text.endswith(("\n", "\r")):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def plot_quantitative_grid(
    cell_rows: Sequence[Mapping[str, Any]],
    *,
    output_dir: Path,
    cohort_label: str,
    evidence_note: str,
    include_crystallization: bool,
    export_tiff: bool,
) -> list[str]:
    groups = _task_groups(cell_rows)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.0), constrained_layout=True)
    _strip_panel(
        axes[0, 0],
        cell_rows,
        task_groups=groups,
        field="completion_fraction",
        ylabel="Completed / scheduled experiments",
        ylim=(-0.03, 1.08),
    )
    _add_panel_label(axes[0, 0], "a")
    _strip_panel(
        axes[0, 1],
        cell_rows,
        task_groups=groups,
        field="best_score",
        ylabel="Best observed score per session",
        ylim=(-0.03, 1.03),
    )
    _add_panel_label(axes[0, 1], "b")
    _strip_panel(
        axes[1, 0],
        cell_rows,
        task_groups=groups,
        field="best_minus_first",
        ylabel="Best score - first score",
        zero_line=True,
    )
    _add_panel_label(axes[1, 0], "c")
    _strip_panel(
        axes[1, 1],
        cell_rows,
        task_groups=groups,
        field="prior_reliability_delta",
        ylabel="Final - initial prior reliability",
        arms=("aligned_nominal", "misindexed_nominal"),
        zero_line=True,
    )
    _add_panel_label(axes[1, 1], "d")
    handles = [
        mpl.lines.Line2D(
            [0],
            [0],
            marker="o",
            linestyle="-",
            lw=2,
            color=ARM_COLORS[arm],
            label=ARM_LABELS[arm],
            markersize=4,
        )
        for arm in ARMS
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02))
    scope = "outcomes" if include_crystallization else "non-crystallization outcomes"
    fig.suptitle(
        f"DeepSeek C2 {scope} — {cohort_label}",
        fontsize=9,
        y=1.06,
    )
    fig.text(
        0.5,
        -0.02,
        "Points are individual task/world/arm sessions; short bars are unweighted means. "
        + evidence_note,
        ha="center",
        fontsize=6,
    )
    basename = (
        "deepseek_c2_all_task_results"
        if include_crystallization
        else "deepseek_c2_noncrystallization_results"
    )
    return _export(fig, output_dir / basename, export_tiff=export_tiff)


def operation_frequency_rows(
    cell_rows: Sequence[Mapping[str, Any]],
    experiment_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    completed: Counter[tuple[str, str]] = Counter()
    for row in experiment_rows:
        key = (str(row["task_group"]), str(row["arm"]))
        completed[key] += 1
        for operation in row["committed_operations"]:
            counts[key][_operation_name(operation)] += 1
    output: list[dict[str, Any]] = []
    for task_group in _task_groups(cell_rows):
        for arm in ARMS:
            key = (task_group, arm)
            denominator = completed[key]
            for operation, count in sorted(counts[key].items()):
                output.append(
                    {
                        "task_group": task_group,
                        "arm": arm,
                        "operation": operation,
                        "count": count,
                        "complete_experiments": denominator,
                        "operations_per_complete_experiment": (
                            count / denominator if denominator else math.nan
                        ),
                    }
                )
    return output


def plot_operation_heatmap(
    frequency_rows: Sequence[Mapping[str, Any]],
    *,
    output_dir: Path,
    cohort_label: str,
    export_tiff: bool,
) -> list[str]:
    operations = sorted(
        {str(row["operation"]) for row in frequency_rows},
        key=lambda name: (_operation_class(name), name),
    )
    task_groups: list[str] = []
    for row in frequency_rows:
        value = str(row["task_group"])
        if value not in task_groups:
            task_groups.append(value)
    row_ids = [(task, arm) for task in task_groups for arm in ARMS]
    lookup = {
        (str(row["task_group"]), str(row["arm"]), str(row["operation"])): _number(
            row["operations_per_complete_experiment"], 0
        )
        for row in frequency_rows
    }
    matrix = np.array(
        [
            [lookup.get((task, arm, operation), 0.0) for operation in operations]
            for task, arm in row_ids
        ]
    )
    fig, ax = plt.subplots(figsize=(7.2, 6.4), constrained_layout=True)
    im = ax.imshow(matrix, aspect="auto", cmap="Blues", vmin=0.0)
    ax.set_xticks(range(len(operations)))
    ax.set_xticklabels(
        [value.replace("measure:", "measure\n") for value in operations],
        rotation=55,
        ha="right",
    )
    ax.set_yticks(range(len(row_ids)))
    ax.set_yticklabels([f"{task} · {ARM_LABELS[arm]}" for task, arm in row_ids])
    for boundary in range(3, len(row_ids), 3):
        ax.axhline(boundary - 0.5, color="white", lw=1.6)
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Accepted operations per complete experiment")
    ax.set_title(f"Agent operation strategy — {cohort_label}")
    ax.text(
        0.0,
        -0.18,
        "Every committed operation is counted; normalization uses completed "
        "experiments in the same task/locus/arm.",
        transform=ax.transAxes,
        fontsize=6,
    )
    return _export(
        fig,
        output_dir / "deepseek_c2_operation_strategy_heatmap",
        export_tiff=export_tiff,
    )


def representative_workflows(
    experiment_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_task: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in experiment_rows:
        score = _number(row.get("leaderboard_score"))
        if math.isfinite(score):
            by_task[str(row["task"])].append(row)
    output: list[dict[str, Any]] = []
    for task in sorted(by_task, key=lambda item: TASK_ORDER.get(item, 99)):
        selected = sorted(
            by_task[task],
            key=lambda row: (
                -_number(row.get("leaderboard_score"), -math.inf),
                str(row.get("cell_id")),
                _int(row.get("experiment_index")),
            ),
        )[0]
        output.append(
            {
                "task": task,
                "task_group": selected["task_group"],
                "cell_id": selected["cell_id"],
                "block": selected["block"],
                "arm": selected["arm"],
                "world_seed": selected["world_seed"],
                "experiment_index": selected["experiment_index"],
                "leaderboard_score": selected["leaderboard_score"],
                "committed_operations": selected["committed_operations"],
            }
        )
    return output


def plot_representative_workflows(
    workflows: Sequence[Mapping[str, Any]],
    *,
    output_dir: Path,
    cohort_label: str,
    export_tiff: bool,
) -> list[str]:
    class_colors = {
        "charge": "#DDE8F5",
        "transform": "#F3D7C7",
        "separation": "#CDE9E4",
        "measurement": "#E4D9EF",
        "control": "#D8D8D8",
    }
    fig, axes = plt.subplots(
        len(workflows),
        1,
        figsize=(11.2, max(5.4, 1.55 * len(workflows))),
        squeeze=False,
        constrained_layout=True,
    )
    for row_index, workflow in enumerate(workflows):
        ax = axes[row_index, 0]
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        operations = [
            dict(value) for value in workflow["committed_operations"] if isinstance(value, Mapping)
        ]
        count = len(operations)
        # Leave enough right-hand clearance for the rounded-box padding.
        positions = np.linspace(0.08, 0.94, max(count, 1))
        node_width = min(0.085, 0.72 / max(count, 1))
        for index, (x, operation) in enumerate(zip(positions, operations, strict=True)):
            name = _operation_name(operation)
            box = FancyBboxPatch(
                (x - node_width / 2, 0.28),
                node_width,
                0.37,
                boxstyle="round,pad=0.012,rounding_size=0.012",
                facecolor=class_colors[_operation_class(name)],
                edgecolor="#4D4D4D",
                linewidth=0.65,
            )
            ax.add_patch(box)
            ax.text(x, 0.465, _compact_operation(operation), ha="center", va="center", fontsize=5.3)
            if index < count - 1:
                ax.add_patch(
                    FancyArrowPatch(
                        (x + node_width / 2, 0.465),
                        (positions[index + 1] - node_width / 2, 0.465),
                        arrowstyle="-|>",
                        mutation_scale=7,
                        linewidth=0.7,
                        color="#606060",
                    )
                )
        title = TASK_LABELS.get(str(workflow["task"]), str(workflow["task"]))
        ax.text(0.0, 0.86, title, fontsize=8, fontweight="bold", va="center")
        ax.text(
            0.0,
            0.72,
            f"{workflow['task_group']} · {ARM_LABELS[str(workflow['arm'])]} · "
            f"world {workflow['world_seed']} · experiment {workflow['experiment_index']} · "
            f"score {_number(workflow['leaderboard_score']):.3f}",
            fontsize=6,
            color="#606060",
        )
        ax.text(-0.025, 0.46, chr(ord("a") + row_index), fontsize=9, fontweight="bold", va="center")
    handles = [
        mpl.patches.Patch(facecolor=color, edgecolor="#4D4D4D", label=label.title())
        for label, color in class_colors.items()
    ]
    fig.legend(handles=handles, ncol=len(handles), loc="upper center", bbox_to_anchor=(0.5, 1.01))
    fig.suptitle(
        f"Representative best-scoring agent workflows — {cohort_label}",
        fontsize=10,
        y=1.04,
    )
    fig.text(
        0.5,
        -0.01,
        "Deterministic selection: highest leaderboard score for each included task; "
        "ties by cell and experiment index. "
        "These are representative traces, not a claim of optimality or causal superiority.",
        ha="center",
        fontsize=6,
    )
    return _export(
        fig,
        output_dir / "deepseek_c2_representative_agent_workflows",
        export_tiff=export_tiff,
    )


def summarize(
    cell_rows: Sequence[Mapping[str, Any]],
    experiment_rows: Sequence[Mapping[str, Any]],
    *,
    metadata: Mapping[str, Any],
    cohort_label: str,
    data_status: str,
    outputs: Sequence[str],
) -> dict[str, Any]:
    scheduled = sum(_int(row.get("scheduled_experiments")) for row in cell_rows)
    complete = sum(_int(row.get("complete_experiments")) for row in cell_rows)
    completed_sessions = sum(bool(row.get("session_completed")) for row in cell_rows)
    qualification = sum(bool(row.get("qualification_passed")) for row in cell_rows)
    by_arm: dict[str, Any] = {}
    for arm in ARMS:
        subset = [row for row in cell_rows if row.get("arm") == arm]
        by_arm[arm] = {
            "sessions": len(subset),
            "completed_sessions": sum(bool(row.get("session_completed")) for row in subset),
            "complete_experiments": sum(_int(row.get("complete_experiments")) for row in subset),
            "scheduled_experiments": sum(_int(row.get("scheduled_experiments")) for row in subset),
            "mean_best_score": float(
                np.mean(
                    [
                        _number(row.get("best_score"))
                        for row in subset
                        if math.isfinite(_number(row.get("best_score")))
                    ]
                )
            ),
            "mean_best_minus_first": float(
                np.mean(
                    [
                        _number(row.get("best_minus_first"))
                        for row in subset
                        if math.isfinite(_number(row.get("best_minus_first")))
                    ]
                )
            ),
        }
    return {
        "schema_version": "chemworld-work-ii-deepseek-c2-report-figure-summary-0.2",
        "cohort_label": cohort_label,
        "data_status": data_status,
        **dict(metadata),
        "included_sessions": len(cell_rows),
        "completed_sessions": completed_sessions,
        "qualification_passed_sessions": qualification,
        "scheduled_complete_experiments": scheduled,
        "observed_complete_experiments": complete,
        "included_experiment_records": len(experiment_rows),
        "by_arm": by_arm,
        "figure_outputs": list(outputs),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument(
        "--replacement-root",
        type=Path,
        help="Terminal rerun root supplying complete block/task replacements.",
    )
    parser.add_argument(
        "--replace-block-task",
        action="append",
        default=[],
        metavar="BLOCK:TASK",
        help="Replace one complete block/task from --input-root; may be repeated.",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--cohort-label",
        default="historical pre-fix public; crystallization excluded",
    )
    parser.add_argument(
        "--include-crystallization",
        action="store_true",
        help="Include reaction-to-crystallization instead of the report default exclusion.",
    )
    parser.add_argument(
        "--evidence-status",
        choices=(
            "historical_pre_fix",
            "corrected_semantics_terminal",
            "corrected_semantics_terminal_replacement",
        ),
        default="historical_pre_fix",
        help=(
            "Label the evidence lifecycle explicitly; this changes captions and "
            "summary metadata only."
        ),
    )
    parser.add_argument(
        "--export-tiff",
        action="store_true",
        help="Also render 600-DPI TIFF files; omitted by default because they are very large.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_root = args.input_root.resolve()
    output_dir = args.output_dir.resolve()
    excluded = set() if args.include_crystallization else {"reaction-to-crystallization"}
    replacement_pairs: set[tuple[str, str]] = set()
    for value in args.replace_block_task:
        block, separator, task = value.partition(":")
        if not separator or not block or not task:
            raise ValueError("--replace-block-task must use BLOCK:TASK")
        replacement_pairs.add((block, task))
    if bool(args.replacement_root) != bool(replacement_pairs):
        raise ValueError(
            "--replacement-root and at least one --replace-block-task are required together"
        )
    if args.evidence_status == "corrected_semantics_terminal_replacement":
        if not replacement_pairs:
            raise ValueError("replacement evidence status requires a replacement block")
        data_status = "corrected_semantics_terminal_with_qualified_replacement"
        evidence_note = (
            "Terminal corrected-semantics evidence with complete affected block replacements; "
            "superseded block results are not pooled."
        )
    elif args.evidence_status == "corrected_semantics_terminal":
        data_status = "corrected_semantics_terminal_evidence"
        evidence_note = (
            "This is the terminal corrected-semantics cohort; historical pre-fix "
            "results are not pooled."
        )
    else:
        data_status = "historical_descriptive_not_corrected_semantics_evidence"
        evidence_note = (
            "Historical results are descriptive and are not pooled with the "
            "corrected-semantics rerun."
        )
    cells, experiments, metadata = collect_rows(
        input_root,
        excluded_tasks=excluded,
        excluded_block_tasks=replacement_pairs,
    )
    if args.replacement_root:
        replacement_root = args.replacement_root.resolve()
        replacement_cells, replacement_experiments, replacement_metadata = collect_rows(
            replacement_root,
            excluded_tasks=excluded,
            included_block_tasks=replacement_pairs,
        )
        if not replacement_cells:
            raise RuntimeError("Replacement root contains no requested block/task cells")
        cells.extend(replacement_cells)
        experiments.extend(replacement_experiments)
        metadata = {
            "input_runs": [input_root.name, replacement_root.name],
            "replacement_block_tasks": [
                f"{block}:{task}" for block, task in sorted(replacement_pairs)
            ],
            "all_cell_summaries": len(cells),
            "included_cell_summaries": len(cells),
            "excluded_cell_summaries": 0,
            "excluded_tasks": sorted(excluded),
            "top_summary_statuses": [
                metadata.get("top_summary_status"),
                replacement_metadata.get("top_summary_status"),
            ],
        }
    identities = [str(row["cell_id"]) for row in cells]
    if len(identities) != len(set(identities)):
        raise RuntimeError("Composite evidence contains duplicate cell identities")
    if not cells or not experiments:
        raise RuntimeError("No included terminal cell/experiment data found")
    source_dir = output_dir / "source_data"
    cell_fields = [key for key in cells[0] if key != "committed_operations"]
    experiment_fields = list(experiments[0])
    frequencies = operation_frequency_rows(cells, experiments)
    workflows = representative_workflows(experiments)
    _write_csv(source_dir / "cell_metrics.csv", cells, cell_fields)
    _write_csv(source_dir / "experiment_metrics.csv", experiments, experiment_fields)
    _write_csv(
        source_dir / "operation_frequencies.csv",
        frequencies,
        list(frequencies[0]),
    )
    _write_csv(
        source_dir / "representative_workflows.csv",
        workflows,
        list(workflows[0]),
    )
    outputs: list[str] = []
    outputs.extend(
        plot_quantitative_grid(
            cells,
            output_dir=output_dir,
            cohort_label=args.cohort_label,
            evidence_note=evidence_note,
            include_crystallization=args.include_crystallization,
            export_tiff=args.export_tiff,
        )
    )
    outputs.extend(
        plot_operation_heatmap(
            frequencies,
            output_dir=output_dir,
            cohort_label=args.cohort_label,
            export_tiff=args.export_tiff,
        )
    )
    outputs.extend(
        plot_representative_workflows(
            workflows,
            output_dir=output_dir,
            cohort_label=args.cohort_label,
            export_tiff=args.export_tiff,
        )
    )
    report = summarize(
        cells,
        experiments,
        metadata=metadata,
        cohort_label=args.cohort_label,
        data_status=data_status,
        outputs=outputs,
    )
    (output_dir / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
