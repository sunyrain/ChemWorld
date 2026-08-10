#!/usr/bin/env python3
"""Rebuild provider-separated Work II development figures from the frozen analysis JSON.

The script deliberately keeps the complete WellAU/Codex prior contrasts separate
from the partial DeepSeek harness audit. It writes the plotted source rows, a
machine-readable figure manifest, and SVG/PDF/PNG exports.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


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
TASK_SHORT = {
    "electrochemical-conversion": "Electrochemical",
    "reaction-to-crystallization": "Crystallization",
    "reaction-to-distillation": "Distillation",
}
TASK_MATRIX_LABEL = {
    "electrochemical-conversion": "Electrochem.",
    "reaction-to-crystallization": "Cryst.",
    "reaction-to-distillation": "Distill.",
}
ARM_ORDER = ["opaque", "aligned_nominal", "misindexed_nominal"]
ARM_LABEL = {
    "opaque": "Opaque",
    "aligned_nominal": "Aligned",
    "misindexed_nominal": "Misindexed",
}

COLORS = {
    "opaque": "#7A8793",
    "aligned_nominal": "#2A9D8F",
    "misindexed_nominal": "#D99032",
    "wellau": "#3E78A8",
    "deepseek": "#7566B7",
    "success": "#66A47A",
    "failure": "#C65353",
    "neutral": "#D9E0E5",
    "ink": "#263238",
    "muted": "#66737D",
    "cached": "#6EA6CF",
    "uncached": "#D3E4F0",
}


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 8,
            "axes.titlesize": 10,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.75,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "workstreams").exists():
            return candidate
    raise RuntimeError("Could not locate the ChemWorld repository root")


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path.parent)
    default_input = (
        repo_root
        / "workstreams"
        / "flagship_tasks"
        / "reports"
        / "work-ii-development-basic-analysis-v0.1.json"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=default_input)
    parser.add_argument("--output-dir", type=Path, default=script_path.parent)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def export_figure(fig: mpl.figure.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_path = output_dir / f"{stem}.svg"
    fig.savefig(svg_path, bbox_inches="tight")
    svg_text = svg_path.read_text(encoding="utf-8")
    with svg_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n")
    fig.savefig(output_dir / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(output_dir / f"{stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(
        output_dir / f"{stem}.tiff",
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)


def add_panel_label(ax: mpl.axes.Axes, label: str) -> None:
    ax.text(
        -0.13,
        1.08,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
        color=COLORS["ink"],
    )


def style_axis(ax: mpl.axes.Axes, grid_axis: str = "y") -> None:
    ax.spines["left"].set_color("#9AA5AC")
    ax.spines["bottom"].set_color("#9AA5AC")
    ax.tick_params(color="#9AA5AC", length=3)
    ax.grid(axis=grid_axis, color="#E7EBEE", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)


def deterministic_offsets(count: int, span: float = 0.10) -> np.ndarray:
    if count <= 1:
        return np.zeros(count)
    return np.linspace(-span / 2, span / 2, count)


def extract_source_rows(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    task_reports = data["wellau_fallback"]["task_reports"]
    endpoint_rows: list[dict[str, Any]] = []
    reliability_rows: list[dict[str, Any]] = []
    warning_rows: list[dict[str, Any]] = []

    contrasts = [
        ("aligned_minus_opaque_best_score", "aligned_nominal"),
        ("misindexed_minus_opaque_best_score", "misindexed_nominal"),
    ]
    for task in TASK_ORDER:
        report = task_reports[task]
        for contrast_name, arm in contrasts:
            contrast = report["paired_endpoint_contrasts"][contrast_name]
            for pair in contrast["pairs"]:
                endpoint_rows.append(
                    {
                        "provider": "WellAU gpt-5.6-sol medium",
                        "task_id": task,
                        "contrast": contrast_name,
                        "left_arm": contrast["left_arm"],
                        "right_arm": contrast["right_arm"],
                        "world_seed": pair["world_seed"],
                        "left_value": pair["left"],
                        "right_value": pair["right"],
                        "difference": pair["difference"],
                    }
                )

        contrast = report["paired_belief_contrasts"][
            "aligned_minus_misindexed_reliability_delta"
        ]
        for pair in contrast["pairs"]:
            reliability_rows.append(
                {
                    "provider": "WellAU gpt-5.6-sol medium",
                    "task_id": task,
                    "contrast": "aligned_minus_misindexed_reliability_delta",
                    "left_arm": contrast["left_arm"],
                    "right_arm": contrast["right_arm"],
                    "world_seed": pair["world_seed"],
                    "left_value": pair["left"],
                    "right_value": pair["right"],
                    "difference": pair["difference"],
                }
            )

        for arm in ARM_ORDER:
            belief = report["arm_summaries"][arm]["belief"]
            numerator = int(belief["final_misindex_flag_count"])
            denominator = int(belief["final_misindex_flag_denominator"])
            warning_rows.append(
                {
                    "provider": "WellAU gpt-5.6-sol medium",
                    "task_id": task,
                    "arm": arm,
                    "flag_count": numerator,
                    "denominator": denominator,
                    "flag_rate": numerator / denominator if denominator else None,
                }
            )

    failed_lookup = {
        (entry["task_id"], entry["arm"], int(entry["world_seed"])): entry
        for entry in data["wellau_fallback"]["denominators"]["failed_cells"]
    }
    cell_rows: list[dict[str, Any]] = []
    for task in TASK_ORDER:
        for arm in ARM_ORDER:
            for seed in range(5):
                failure = failed_lookup.get((task, arm, seed))
                cell_rows.append(
                    {
                        "provider": "WellAU gpt-5.6-sol medium",
                        "task_id": task,
                        "arm": arm,
                        "world_seed": seed,
                        "status": "failed" if failure else "completed",
                        "complete_experiment_count": (
                            int(failure["complete_experiment_count"]) if failure else 4
                        ),
                        "failure_type": (
                            failure.get("failure", {}).get("type", "") if failure else ""
                        ),
                    }
                )

    provider_rows: list[dict[str, Any]] = []
    for provider_key, provider_label in [
        ("wellau_fallback", "WellAU gpt-5.6-sol medium"),
        ("deepseek_attempt", "DeepSeek V4 Flash partial attempts"),
    ]:
        den = data[provider_key]["denominators"]
        provider_rows.append(
            {
                "provider_key": provider_key,
                "provider": provider_label,
                "expected_cell_count": den["expected_cell_count"],
                "terminal_record_count": den["terminal_record_count"],
                "qualified_cell_count": den["qualified_cell_count"],
                "completed_cell_count": den["completed_cell_count"],
                "expected_experiment_count": den["expected_cell_count"] * 4,
                "complete_experiment_count": den["complete_experiment_count"],
                "exact_replay_verified_count": den["exact_replay_verified_count"],
                "operation_attempt_count": den["operation_attempt_count"],
                "committed_operation_count": den["committed_operation_count"],
                "validation_failure_count": den["validation_failure_count"],
                "recovered_mcp_tool_failure_count": den[
                    "recovered_mcp_tool_failure_count"
                ],
                "provider_error_event_count": den["provider_error_event_count"],
                "resource_rejection_count": den["resource_rejection_count"],
                "input_token_count": den["provider_usage_totals"]["input_token_count"],
                "cached_input_token_count": den["provider_usage_totals"][
                    "cached_input_token_count"
                ],
                "uncached_input_token_count": den["provider_usage_totals"][
                    "uncached_input_token_count"
                ],
                "output_token_count": den["provider_usage_totals"]["output_token_count"],
                "input_cache_hit_ratio": den["provider_usage_totals"][
                    "input_cache_hit_ratio"
                ],
            }
        )

    return {
        "endpoint": endpoint_rows,
        "reliability": reliability_rows,
        "warnings": warning_rows,
        "cells": cell_rows,
        "providers": provider_rows,
    }


def write_source_data(output_dir: Path, rows: dict[str, list[dict[str, Any]]]) -> None:
    source_dir = output_dir / "source_data"
    write_csv(
        source_dir / "wellau_endpoint_contrasts.csv",
        rows["endpoint"],
        [
            "provider",
            "task_id",
            "contrast",
            "left_arm",
            "right_arm",
            "world_seed",
            "left_value",
            "right_value",
            "difference",
        ],
    )
    write_csv(
        source_dir / "wellau_prior_reliability_contrast.csv",
        rows["reliability"],
        [
            "provider",
            "task_id",
            "contrast",
            "left_arm",
            "right_arm",
            "world_seed",
            "left_value",
            "right_value",
            "difference",
        ],
    )
    write_csv(
        source_dir / "wellau_misindex_warning_rates.csv",
        rows["warnings"],
        ["provider", "task_id", "arm", "flag_count", "denominator", "flag_rate"],
    )
    write_csv(
        source_dir / "wellau_cell_status.csv",
        rows["cells"],
        [
            "provider",
            "task_id",
            "arm",
            "world_seed",
            "status",
            "complete_experiment_count",
            "failure_type",
        ],
    )
    write_csv(
        source_dir / "provider_execution_audit.csv",
        rows["providers"],
        list(rows["providers"][0].keys()),
    )


def plot_difference_groups(
    ax: mpl.axes.Axes,
    rows: list[dict[str, Any]],
    group_key: str,
    group_values: list[str],
    group_colors: dict[str, str],
    offsets: dict[str, float],
) -> None:
    for task_index, task in enumerate(TASK_ORDER):
        for group in group_values:
            values = [
                float(row["difference"])
                for row in rows
                if row["task_id"] == task and row[group_key] == group
            ]
            x = task_index + offsets[group]
            jitter = deterministic_offsets(len(values), span=0.09)
            ax.scatter(
                x + jitter,
                values,
                s=25,
                color=group_colors[group],
                alpha=0.72,
                edgecolor="white",
                linewidth=0.45,
                zorder=3,
            )
            mean = float(np.mean(values))
            ax.plot(
                [x - 0.10, x + 0.10],
                [mean, mean],
                color=group_colors[group],
                linewidth=2.2,
                solid_capstyle="round",
                zorder=4,
            )
            label_offset = 0.022 if mean >= 0 else -0.026
            ax.text(
                x,
                mean + label_offset,
                f"{mean:+.3f}\n(n={len(values)})",
                ha="center",
                va="bottom" if mean >= 0 else "top",
                color=group_colors[group],
                fontsize=6.5,
                fontweight="bold",
                zorder=5,
            )


def make_wellau_figure(
    data: dict[str, Any], rows: dict[str, list[dict[str, Any]]], output_dir: Path
) -> None:
    fig = plt.figure(figsize=(7.2, 7.0), constrained_layout=False)
    grid = fig.add_gridspec(
        2,
        2,
        left=0.075,
        right=0.985,
        bottom=0.145,
        top=0.82,
        wspace=0.43,
        hspace=0.48,
        width_ratios=[1.28, 1.0],
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    # a — paired endpoint contrasts relative to the opaque arm.
    endpoint_rows = []
    for row in rows["endpoint"]:
        copied = dict(row)
        copied["comparison_arm"] = copied["left_arm"]
        endpoint_rows.append(copied)
    plot_difference_groups(
        ax_a,
        endpoint_rows,
        "comparison_arm",
        ["aligned_nominal", "misindexed_nominal"],
        COLORS,
        {"aligned_nominal": -0.16, "misindexed_nominal": 0.16},
    )
    ax_a.axhline(0, color=COLORS["ink"], linewidth=0.9, zorder=1)
    ax_a.set_xticks(range(len(TASK_ORDER)), [TASK_LABEL[t] for t in TASK_ORDER])
    ax_a.set_ylabel("Paired difference in best endpoint score")
    ax_a.set_ylim(-0.275, 0.43)
    ax_a.set_title(
        "Task-dependent endpoint contrasts\nPaired world seeds; horizontal marks = means",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    style_axis(ax_a)
    add_panel_label(ax_a, "a")

    # b — reliability discrimination between aligned and misindexed priors.
    for task_index, task in enumerate(TASK_ORDER):
        values = [
            float(row["difference"])
            for row in rows["reliability"]
            if row["task_id"] == task
        ]
        jitter = deterministic_offsets(len(values), span=0.13)
        ax_b.scatter(
            task_index + jitter,
            values,
            s=29,
            color="#4C6F91",
            alpha=0.75,
            edgecolor="white",
            linewidth=0.45,
            zorder=3,
        )
        mean = float(np.mean(values))
        ax_b.plot(
            [task_index - 0.13, task_index + 0.13],
            [mean, mean],
            color="#294F70",
            linewidth=2.3,
            solid_capstyle="round",
            zorder=4,
        )
        ax_b.text(
            task_index,
            mean + (0.045 if mean >= 0 else -0.045),
            f"{mean:+.2f} (n={len(values)})",
            ha="center",
            va="bottom" if mean >= 0 else "top",
            fontsize=6.7,
            color="#294F70",
            fontweight="bold",
        )
    ax_b.axhline(0, color=COLORS["ink"], linewidth=0.9, zorder=1)
    ax_b.set_xticks(range(len(TASK_ORDER)), [TASK_LABEL[t] for t in TASK_ORDER])
    ax_b.set_ylabel("Aligned − misindexed change\nin prior reliability")
    ax_b.set_ylim(-0.65, 0.58)
    ax_b.set_title(
        "Heterogeneous reliability updates\nPositive = larger change in aligned arm",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    style_axis(ax_b)
    add_panel_label(ax_b, "b")

    # c — explicit misindex warning rates.
    x = np.arange(len(TASK_ORDER), dtype=float)
    width = 0.22
    for arm_index, arm in enumerate(ARM_ORDER):
        arm_rows = [
            next(row for row in rows["warnings"] if row["task_id"] == task and row["arm"] == arm)
            for task in TASK_ORDER
        ]
        heights = [float(row["flag_rate"]) for row in arm_rows]
        positions = x + (arm_index - 1) * width
        bars = ax_c.bar(
            positions,
            heights,
            width=width * 0.88,
            color=COLORS[arm],
            edgecolor="white",
            linewidth=0.6,
            label=ARM_LABEL[arm],
            zorder=3,
        )
        for bar, row in zip(bars, arm_rows):
            ax_c.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.035,
                f"{row['flag_count']}/{row['denominator']}",
                ha="center",
                va="bottom",
                fontsize=6.7,
                color=COLORS["ink"],
            )
    ax_c.set_xticks(x, [TASK_LABEL[t] for t in TASK_ORDER])
    ax_c.set_ylim(0, 1.08)
    ax_c.set_yticks(np.linspace(0, 1, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 1, 6)])
    ax_c.set_ylabel("Cells with a final misindex warning")
    ax_c.set_title(
        "Misindex warnings lack specificity\nAn informative warning should concentrate in misindexed cells",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    style_axis(ax_c)
    add_panel_label(ax_c, "c")

    # d — exact WellAU cell denominator and the retained failed cell.
    row_pairs = [(task, arm) for task in TASK_ORDER for arm in ARM_ORDER]
    status_lookup = {
        (row["task_id"], row["arm"], int(row["world_seed"])): row["status"]
        for row in rows["cells"]
    }
    for y, (task, arm) in enumerate(row_pairs):
        for seed in range(5):
            status = status_lookup[(task, arm, seed)]
            color = COLORS["success"] if status == "completed" else COLORS["failure"]
            marker = "s" if status == "completed" else "X"
            ax_d.scatter(
                seed,
                y,
                s=112,
                marker=marker,
                color=color,
                edgecolor="white",
                linewidth=0.8,
                zorder=3,
            )
            ax_d.text(
                seed,
                y,
                "C" if status == "completed" else "F",
                ha="center",
                va="center",
                color="white",
                fontsize=7.2,
                fontweight="bold",
                zorder=4,
            )
    for boundary in [2.5, 5.5]:
        ax_d.axhline(boundary, color="#C8D0D5", linewidth=0.8)
    ax_d.set_xlim(-0.6, 4.6)
    ax_d.set_ylim(len(row_pairs) - 0.35, -0.65)
    ax_d.set_xticks(range(5), [f"Seed {seed}" for seed in range(5)])
    ax_d.set_yticks(
        range(len(row_pairs)),
        [
            f"{TASK_MATRIX_LABEL[task]} · {ARM_LABEL[arm]}"
            for task, arm in row_pairs
        ],
    )
    ax_d.tick_params(axis="y", labelsize=6.4)
    ax_d.set_xlabel("World seed")
    ax_d.set_title(
        "Retained development matrix\n44/45 cells; 176/180 experiments; 44/45 replay",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    ax_d.spines[["left", "bottom"]].set_visible(False)
    ax_d.tick_params(length=0)
    ax_d.grid(False)
    add_panel_label(ax_d, "d")

    fig.suptitle(
        "Endpoint behavior differs across prior conditions,\nbut current belief signals are not diagnostic",
        x=0.075,
        y=0.982,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.legend(
        handles=[
            Patch(facecolor=COLORS["aligned_nominal"], edgecolor="white", label="Aligned − opaque"),
            Patch(facecolor=COLORS["misindexed_nominal"], edgecolor="white", label="Misindexed − opaque"),
            Patch(facecolor=COLORS["success"], edgecolor="white", label="Completed"),
            Patch(facecolor=COLORS["failure"], edgecolor="white", label="Failed; retained"),
        ],
        ncol=4,
        loc="upper left",
        bbox_to_anchor=(0.075, 0.895),
        borderaxespad=0,
        fontsize=6.4,
        columnspacing=0.65,
        handlelength=1.2,
    )
    fig.text(
        0.075,
        0.027,
        "Development data only: WellAU gpt-5.6-sol (medium), five world seeds per task, descriptive summaries, no formal tests. "
        "No evaluator-truth prediction scoring or blind replay is available; these endpoint and belief summaries do not establish law discovery or transfer.",
        ha="left",
        va="bottom",
        fontsize=6.6,
        color=COLORS["muted"],
        wrap=True,
    )
    export_figure(fig, output_dir, "wellau_codex_prior_results")


def horizontal_fraction_bars(
    ax: mpl.axes.Axes,
    labels: list[str],
    numerators: list[float],
    denominators: list[float],
    color: str,
) -> None:
    y = np.arange(len(labels))
    fractions = np.divide(numerators, denominators)
    ax.barh(y, np.ones_like(fractions), color="#EDF1F3", height=0.58, zorder=1)
    ax.barh(y, fractions, color=color, height=0.58, zorder=2)
    for yi, frac, num, den in zip(y, fractions, numerators, denominators):
        ax.text(
            min(frac + 0.025, 0.94),
            yi,
            f"{int(num)}/{int(den)}",
            ha="left" if frac < 0.90 else "right",
            va="center",
            fontsize=7.2,
            fontweight="bold",
            color=COLORS["ink"],
        )
    ax.set_xlim(0, 1.04)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25", "50", "75", "100%"])
    style_axis(ax, grid_axis="x")


def event_rate_panel(ax: mpl.axes.Axes, provider: dict[str, Any], color: str) -> None:
    attempts = float(provider["operation_attempt_count"])
    events = [
        ("Validation", int(provider["validation_failure_count"])),
        ("Recovered MCP", int(provider["recovered_mcp_tool_failure_count"])),
        ("Provider errors", int(provider["provider_error_event_count"])),
        ("Resource rejects", int(provider["resource_rejection_count"])),
    ]
    labels = [name for name, _ in events]
    rates = [count / attempts * 100.0 for _, count in events]
    y = np.arange(len(events))
    bars = ax.barh(y, rates, color=color, height=0.58, zorder=3)
    for bar, (_, count), rate in zip(bars, events, rates):
        ax.text(
            bar.get_width() + 0.12,
            bar.get_y() + bar.get_height() / 2,
            f"{count}  ({rate:.2f}/100)",
            va="center",
            ha="left",
            fontsize=7.1,
            color=COLORS["ink"],
        )
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 8.0)
    ax.set_xlabel("Events per 100 operation attempts")
    style_axis(ax, grid_axis="x")


def token_panel(ax: mpl.axes.Axes, provider: dict[str, Any], color: str) -> None:
    cached = float(provider["cached_input_token_count"]) / 1_000_000
    uncached = float(provider["uncached_input_token_count"]) / 1_000_000
    total_input = float(provider["input_token_count"]) / 1_000_000
    output = float(provider["output_token_count"]) / 1_000_000
    hit = float(provider["input_cache_hit_ratio"]) * 100
    ax.barh([0], [cached], color=color, height=0.52, label="Cached input", zorder=3)
    ax.barh(
        [0],
        [uncached],
        left=[cached],
        color=COLORS["uncached"],
        edgecolor="white",
        linewidth=0.6,
        height=0.52,
        label="Uncached input",
        zorder=3,
    )
    ax.text(
        cached / 2,
        0,
        f"{cached:.2f} M cached",
        ha="center",
        va="center",
        fontsize=7,
        color="white" if cached > 12 else COLORS["ink"],
        fontweight="bold",
    )
    ax.text(
        total_input + 0.8,
        0,
        f"{total_input:.2f} M input\n{output:.3f} M output\ncache hit {hit:.1f}%",
        ha="left",
        va="center",
        fontsize=6.5,
        color=COLORS["ink"],
        clip_on=True,
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([0], ["Provider usage"])
    ax.set_xlabel("Input tokens (millions)")
    ax.text(
        0.0,
        1.03,
        "Dark = cached input; light = uncached input",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.7,
        color=COLORS["muted"],
    )
    style_axis(ax, grid_axis="x")


def make_provider_audit_figure(
    data: dict[str, Any], rows: dict[str, list[dict[str, Any]]], output_dir: Path
) -> None:
    providers = {row["provider_key"]: row for row in rows["providers"]}
    wellau = providers["wellau_fallback"]
    deepseek = providers["deepseek_attempt"]

    fig = plt.figure(figsize=(7.2, 7.5), constrained_layout=False)
    grid = fig.add_gridspec(
        3,
        2,
        left=0.095,
        right=0.985,
        bottom=0.155,
        top=0.82,
        wspace=0.42,
        hspace=0.66,
        height_ratios=[1.03, 1.03, 0.78],
    )
    axes = [fig.add_subplot(grid[row, col]) for row in range(3) for col in range(2)]
    ax_a, ax_b, ax_c, ax_d, ax_e, ax_f = axes

    horizontal_fraction_bars(
        ax_a,
        ["Terminal", "Qualified", "Experiments", "Exact replay"],
        [
            wellau["terminal_record_count"],
            wellau["qualified_cell_count"],
            wellau["complete_experiment_count"],
            wellau["exact_replay_verified_count"],
        ],
        [
            wellau["expected_cell_count"],
            wellau["expected_cell_count"],
            wellau["expected_experiment_count"],
            wellau["terminal_record_count"],
        ],
        COLORS["wellau"],
    )
    ax_a.set_title(
        "Coverage\n45 scheduled cells; four experiments per cell",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_a, "a")

    horizontal_fraction_bars(
        ax_b,
        ["Terminal", "Qualified", "Experiments", "Exact replay*"],
        [
            deepseek["terminal_record_count"],
            deepseek["qualified_cell_count"],
            deepseek["complete_experiment_count"],
            deepseek["exact_replay_verified_count"],
        ],
        [
            deepseek["expected_cell_count"],
            deepseek["expected_cell_count"],
            deepseek["expected_experiment_count"],
            deepseek["terminal_record_count"],
        ],
        COLORS["deepseek"],
    )
    ax_b.set_title(
        "Coverage\n33-cell attempt scope; four experiments per cell",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_b, "b")

    event_rate_panel(ax_c, wellau, COLORS["wellau"])
    ax_c.set_title(
        f"Technical event rates\nn={wellau['operation_attempt_count']:,} operation attempts",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_c, "c")

    event_rate_panel(ax_d, deepseek, COLORS["deepseek"])
    ax_d.set_title(
        f"Technical event rates\nn={deepseek['operation_attempt_count']:,} operation attempts",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_d, "d")

    token_panel(ax_e, wellau, COLORS["cached"])
    ax_e.set_title(
        "Token accounting",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_e, "e")

    token_panel(ax_f, deepseek, COLORS["deepseek"])
    ax_f.set_title(
        "Token accounting",
        loc="left",
        fontweight="bold",
        color=COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    add_panel_label(ax_f, "f")

    fig.suptitle(
        "Provider-separated execution audit\nfor the frozen baseline development runs",
        x=0.095,
        y=0.982,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.095,
        0.865,
        "WellAU/Codex — complete development matrix",
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
        color=COLORS["wellau"],
    )
    fig.text(
        0.555,
        0.865,
        "DeepSeek — pre-amendment attempts; harness audit only",
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
        color=COLORS["deepseek"],
    )
    fig.text(
        0.10,
        0.027,
        "Exact denominators are printed on every completion bar. *DeepSeek replay is 21/21 among terminal retained records, not 21/33 scheduled cells. "
        "Operational rates are descriptive: provider, task coverage, harness version and recovery policy differ. Cached tokens are cached input, not repeated model output; providers are not pooled into a scientific contrast. Later recovery-amended seed-0 pilots are excluded from this frozen baseline.",
        ha="left",
        va="bottom",
        fontsize=6.6,
        color=COLORS["muted"],
        wrap=True,
    )
    export_figure(fig, output_dir, "provider_separated_execution_audit")


def write_manifest(
    input_path: Path, output_dir: Path, data: dict[str, Any], rows: dict[str, list[dict[str, Any]]]
) -> None:
    manifest = {
        "schema_version": "chemworld-work-ii-development-figures-0.1",
        "analysis_id": data.get("analysis_id"),
        "analysis_date": data.get("analysis_date"),
        "embedded_analysis_sha256": data.get("analysis_sha256"),
        "input_file_sha256": sha256_file(input_path),
        "provider_groups_mixed_in_prior_contrasts": False,
        "formal_hypothesis_tests_run": False,
        "figures": {
            "wellau_codex_prior_results": {
                "formats": ["svg", "pdf", "png", "tiff"],
                "paired_endpoint_rows": len(rows["endpoint"]),
                "paired_reliability_rows": len(rows["reliability"]),
                "warning_rate_rows": len(rows["warnings"]),
                "cell_status_rows": len(rows["cells"]),
            },
            "provider_separated_execution_audit": {
                "formats": ["svg", "pdf", "png", "tiff"],
                "provider_rows": len(rows["providers"]),
            },
        },
        "interpretation_limits": [
            "development data only",
            "descriptive summaries; no formal inference",
            "DeepSeek partial attempts are harness evidence only",
            "later recovery-amended DeepSeek seed-0 pilots are excluded",
            "no evaluator-truth prediction scoring",
            "no blind recommendation replay",
            "no law-discovery or transfer claim",
        ],
    }
    (output_dir / "figure_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()
    data = load_json(input_path)
    if data.get("formal_result") is not False:
        raise ValueError("Expected a development-only analysis with formal_result=false")
    if data["audit"].get("provider_groups_mixed_in_prior_contrasts") is not False:
        raise ValueError("Provider groups must remain separated")

    configure_matplotlib()
    rows = extract_source_rows(data)
    write_source_data(output_dir, rows)
    make_wellau_figure(data, rows, output_dir)
    make_provider_audit_figure(data, rows, output_dir)
    write_manifest(input_path, output_dir, data, rows)
    print(f"Wrote figures and source data to {output_dir}")


if __name__ == "__main__":
    main()
