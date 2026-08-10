#!/usr/bin/env python3
"""Plot the full DeepSeek recovery-amended Work II development matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

import plot_work_ii_codex_development as base


def configure_matplotlib() -> None:
    """Declare the publication/export settings locally for source-level QA."""
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
            "svg.hashsalt": "chemworld-work-ii-deepseek-recovery-figure-0.1",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def export_figure(fig: mpl.figure.Figure, output_dir: Path, stem: str) -> None:
    """Write deterministic editable vector and 600 dpi raster outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_path = output_dir / f"{stem}.svg"
    fig.savefig(svg_path, bbox_inches="tight", metadata={"Date": None})
    svg_text = svg_path.read_text(encoding="utf-8")
    with svg_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n")
    fig.savefig(
        output_dir / f"{stem}.pdf",
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    fig.savefig(output_dir / f"{stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(
        output_dir / f"{stem}.tiff",
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    repo_root = base.find_repo_root(script_path.parent)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=(
            repo_root
            / "workstreams"
            / "flagship_tasks"
            / "reports"
            / "work-ii-deepseek-recovery-amended-analysis-v0.1.json"
        ),
    )
    parser.add_argument("--output-dir", type=Path, default=script_path.parent)
    return parser.parse_args()


def build_rows(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    endpoint: list[dict[str, Any]] = []
    reliability: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for task_id, task in data["task_reports"].items():
        for key in (
            "aligned_minus_opaque_best_score",
            "misindexed_minus_opaque_best_score",
        ):
            contrast = task["paired_endpoint_contrasts"][key]
            for pair in contrast["pairs"]:
                endpoint.append(
                    {
                        "task_id": task_id,
                        "comparison_arm": contrast["left_arm"],
                        "left_arm": contrast["left_arm"],
                        "right_arm": contrast["right_arm"],
                        "world_seed": int(pair["world_seed"]),
                        "difference": float(pair["difference"]),
                    }
                )
        contrast = task["paired_belief_contrasts"][
            "aligned_minus_misindexed_reliability_delta"
        ]
        for pair in contrast["pairs"]:
            reliability.append(
                {
                    "task_id": task_id,
                    "world_seed": int(pair["world_seed"]),
                    "difference": float(pair["difference"]),
                }
            )
        for arm in base.ARM_ORDER:
            belief = task["arm_summaries"][arm]["belief"]
            numerator = int(belief["final_misindex_flag_count"])
            denominator = int(belief["final_misindex_flag_denominator"])
            warnings.append(
                {
                    "task_id": task_id,
                    "arm": arm,
                    "flag_count": numerator,
                    "denominator": denominator,
                    "flag_rate": numerator / denominator if denominator else 0.0,
                }
            )
    cells = [
        {
            "task_id": row["task_id"],
            "arm": row["arm"],
            "world_seed": int(row["world_seed"]),
            "status": "completed" if row["completed"] else "failed",
            "complete_experiment_count": int(row["complete_experiment_count"]),
            "mcp_tool_failure_count": int(row["recovered_mcp_tool_failure_count"]),
            "provider_error_event_count": int(row["provider_error_event_count"]),
            "resource_rejection_count": int(row["resource_rejection_count"]),
        }
        for row in data["cell_records"]
    ]
    return {
        "endpoint": endpoint,
        "reliability": reliability,
        "warnings": warnings,
        "cells": cells,
    }


def write_source_data(output_dir: Path, rows: dict[str, list[dict[str, Any]]]) -> None:
    source_dir = output_dir / "source_data"
    base.write_csv(
        source_dir / "deepseek_recovery_endpoint_contrasts.csv",
        rows["endpoint"],
        ["task_id", "comparison_arm", "left_arm", "right_arm", "world_seed", "difference"],
    )
    base.write_csv(
        source_dir / "deepseek_recovery_prior_reliability_contrast.csv",
        rows["reliability"],
        ["task_id", "world_seed", "difference"],
    )
    base.write_csv(
        source_dir / "deepseek_recovery_misindex_warning_rates.csv",
        rows["warnings"],
        ["task_id", "arm", "flag_count", "denominator", "flag_rate"],
    )
    base.write_csv(
        source_dir / "deepseek_recovery_cell_status.csv",
        rows["cells"],
        [
            "task_id",
            "arm",
            "world_seed",
            "status",
            "complete_experiment_count",
            "mcp_tool_failure_count",
            "provider_error_event_count",
            "resource_rejection_count",
        ],
    )


def make_figure(
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

    base.plot_difference_groups(
        ax_a,
        rows["endpoint"],
        "comparison_arm",
        ["aligned_nominal", "misindexed_nominal"],
        base.COLORS,
        {"aligned_nominal": -0.16, "misindexed_nominal": 0.16},
    )
    ax_a.axhline(0, color=base.COLORS["ink"], linewidth=0.9, zorder=1)
    ax_a.set_xticks(range(len(base.TASK_ORDER)), [base.TASK_LABEL[t] for t in base.TASK_ORDER])
    ax_a.set_ylabel("Paired difference in best endpoint score")
    ax_a.set_ylim(-0.22, 0.31)
    ax_a.set_title(
        "Task-dependent endpoint contrasts\nPaired world seeds; horizontal marks = means",
        loc="left",
        fontweight="bold",
        color=base.COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    base.style_axis(ax_a)
    base.add_panel_label(ax_a, "a")

    for task_index, task in enumerate(base.TASK_ORDER):
        values = [
            float(row["difference"])
            for row in rows["reliability"]
            if row["task_id"] == task
        ]
        jitter = base.deterministic_offsets(len(values), span=0.13)
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
            mean + (0.035 if mean >= 0 else -0.035),
            f"{mean:+.3f} (n={len(values)})",
            ha="center",
            va="bottom" if mean >= 0 else "top",
            fontsize=6.7,
            color="#294F70",
            fontweight="bold",
        )
    ax_b.axhline(0, color=base.COLORS["ink"], linewidth=0.9, zorder=1)
    ax_b.set_xticks(range(len(base.TASK_ORDER)), [base.TASK_LABEL[t] for t in base.TASK_ORDER])
    ax_b.set_ylabel("Aligned − misindexed change\nin prior reliability")
    ax_b.set_ylim(-0.4, 0.42)
    ax_b.set_title(
        "Reliability reports remain weakly separated\nPositive = larger change in aligned arm",
        loc="left",
        fontweight="bold",
        color=base.COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    base.style_axis(ax_b)
    base.add_panel_label(ax_b, "b")

    x = np.arange(len(base.TASK_ORDER), dtype=float)
    width = 0.22
    for arm_index, arm in enumerate(base.ARM_ORDER):
        arm_rows = [
            next(row for row in rows["warnings"] if row["task_id"] == task and row["arm"] == arm)
            for task in base.TASK_ORDER
        ]
        positions = x + (arm_index - 1) * width
        bars = ax_c.bar(
            positions,
            [float(row["flag_rate"]) for row in arm_rows],
            width=width * 0.88,
            color=base.COLORS[arm],
            edgecolor="white",
            linewidth=0.6,
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
                color=base.COLORS["ink"],
            )
    ax_c.set_xticks(x, [base.TASK_LABEL[t] for t in base.TASK_ORDER])
    ax_c.set_ylim(0, 1.08)
    ax_c.set_yticks(np.linspace(0, 1, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 1, 6)])
    ax_c.set_ylabel("Cells with a final misindex warning")
    ax_c.set_title(
        "Warnings track dossier presence, not misindexing\nAligned cells are flagged as often as misindexed cells",
        loc="left",
        fontweight="bold",
        color=base.COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    base.style_axis(ax_c)
    base.add_panel_label(ax_c, "c")

    row_pairs = [(task, arm) for task in base.TASK_ORDER for arm in base.ARM_ORDER]
    status_lookup = {
        (row["task_id"], row["arm"], int(row["world_seed"])): row["status"]
        for row in rows["cells"]
    }
    for y, (task, arm) in enumerate(row_pairs):
        for seed in range(5):
            status = status_lookup[(task, arm, seed)]
            completed = status == "completed"
            ax_d.scatter(
                seed,
                y,
                s=112,
                marker="s" if completed else "X",
                color=base.COLORS["success"] if completed else base.COLORS["failure"],
                edgecolor="white",
                linewidth=0.8,
                zorder=3,
            )
            ax_d.text(
                seed,
                y,
                "C" if completed else "F",
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
        [f"{base.TASK_MATRIX_LABEL[task]} · {base.ARM_LABEL[arm]}" for task, arm in row_pairs],
    )
    ax_d.tick_params(axis="y", labelsize=6.4)
    ax_d.set_xlabel("World seed")
    ax_d.set_title(
        "Recovery-amended development matrix\n43/45 cells; 174/180 experiments; 45/45 replay",
        loc="left",
        fontweight="bold",
        color=base.COLORS["ink"],
        pad=7,
        fontsize=9,
    )
    ax_d.spines[["left", "bottom"]].set_visible(False)
    ax_d.tick_params(length=0)
    ax_d.grid(False)
    base.add_panel_label(ax_d, "d")

    fig.suptitle(
        "Explicit priors shift endpoints, but misindexed\ninformation is not reliably rejected",
        x=0.075,
        y=0.982,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=base.COLORS["ink"],
    )
    fig.legend(
        handles=[
            Patch(facecolor=base.COLORS["aligned_nominal"], edgecolor="white", label="Aligned − opaque"),
            Patch(facecolor=base.COLORS["misindexed_nominal"], edgecolor="white", label="Misindexed − opaque"),
            Patch(facecolor=base.COLORS["success"], edgecolor="white", label="Completed"),
            Patch(facecolor=base.COLORS["failure"], edgecolor="white", label="Failed; retained"),
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
        "Development data only: DeepSeek V4 Flash with the recovery-amended Codex harness, five world seeds per task, descriptive summaries, no formal tests. "
        "Two crystallization contract failures are retained. No evaluator-truth prediction scoring or blind replay is available; endpoint and self-report summaries do not establish law discovery, wrong-prior rejection or transfer.",
        ha="left",
        va="bottom",
        fontsize=6.6,
        color=base.COLORS["muted"],
        wrap=True,
    )
    export_figure(fig, output_dir, "deepseek_recovery_amended_prior_results")


def write_manifest(
    input_path: Path,
    output_dir: Path,
    data: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
) -> None:
    manifest = {
        "schema_version": "chemworld-work-ii-deepseek-recovery-figure-0.1",
        "analysis_id": data["analysis_id"],
        "analysis_sha256": data["analysis_sha256"],
        "input_file_sha256": base.sha256_file(input_path),
        "formal_hypothesis_tests_run": False,
        "provider_groups_mixed": False,
        "figure": {
            "stem": "deepseek_recovery_amended_prior_results",
            "formats": ["svg", "pdf", "png", "tiff"],
            "paired_endpoint_rows": len(rows["endpoint"]),
            "paired_reliability_rows": len(rows["reliability"]),
            "warning_rate_rows": len(rows["warnings"]),
            "cell_status_rows": len(rows["cells"]),
        },
        "interpretation_limits": data["audit"]["limitations"],
    }
    path = output_dir / "deepseek_recovery_figure_manifest.json"
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()
    data = base.load_json(input_path)
    if data.get("formal_result") is not False:
        raise ValueError("Expected a development-only analysis")
    if data.get("provider_group") != "deepseek_recovery_amended":
        raise ValueError("Expected the DeepSeek recovery-amended provider group")
    if data.get("audit", {}).get("provider_groups_mixed_in_prior_contrasts") is not False:
        raise ValueError("Provider groups must remain separated")
    configure_matplotlib()
    rows = build_rows(data)
    write_source_data(output_dir, rows)
    make_figure(data, rows, output_dir)
    write_manifest(input_path, output_dir, data, rows)
    print(f"Wrote DeepSeek recovery figure and source data to {output_dir}")


if __name__ == "__main__":
    main()
