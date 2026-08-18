#!/usr/bin/env python3
"""Render the current-composite prediction, law, and action evidence.

Figure contract
---------------
Core conclusion: experimental evidence changes held-out predictions, but selective
wrong-model correction, faithful executable-law compression, and action improvement
remain distinct and can fail independently.
Figure archetype: quantitative grid with a full-width hero panel.
Target/output: venue-neutral double-column paper figure; editable SVG/PDF plus
600-dpi TIFF and 300-dpi PNG preview.
Panel map: (a) failure-aware selective-correction effects across all 45 matched
worlds; (b) pre-to-final prediction improvement across all 135 cells; (c) typed-law
error versus final explicit-prediction error in all 135 cells; (d) paired blind
action outcomes in all 121 evaluable cells, retaining 14 nonterminal cells as an
unstarted denominator.
Statistics: registered locus gates and p values only; all other summaries are
descriptive means or exact counts. No observations are excluded.
Reviewer risk: syntax/executability must not be described as law fidelity, and
equivalent blind replay must not be described as action improvement.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Mandatory editable-vector typography.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
# Canonical validator notation: svg.fonttype='none'; pdf.fonttype=42.
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

ROOT = Path(__file__).resolve().parents[5]
DEFAULT_REPORT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "current"
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
ARM_LABELS = {
    "opaque": "Opaque",
    "aligned_nominal": "Aligned",
    "misindexed_nominal": "Misindexed",
}
ARM_MARKERS = {"opaque": "o", "aligned_nominal": "s", "misindexed_nominal": "^"}
LOCI = ("A_E", "A_P", "A_S")
LOCUS_COLORS = {"A_E": "#4C72B0", "A_P": "#2A9D8F", "A_S": "#C65D57"}
LOCUS_LABELS = {"A_E": "Entity", "A_P": "Parametric", "A_S": "Structural"}
TASK_LABELS = {
    "electrochemical-conversion": "Electrochemistry",
    "partition-discovery": "Partition",
    "reaction-safety-constrained": "Reaction safety",
    "reaction-to-crystallization": "Crystallization",
    "reaction-to-distillation": "Distillation",
}
TASK_ORDER = {
    "A_E": (
        "electrochemical-conversion",
        "partition-discovery",
        "reaction-safety-constrained",
        "reaction-to-crystallization",
        "reaction-to-distillation",
    ),
    "A_P": ("electrochemical-conversion", "reaction-safety-constrained"),
    "A_S": ("partition-discovery", "reaction-to-crystallization"),
}


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _finite(values: Iterable[Any]) -> list[float]:
    return [
        float(value)
        for value in values
        if isinstance(value, int | float)
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    ]


def _mean(values: Iterable[Any]) -> float:
    finite = _finite(values)
    if not finite:
        raise ValueError("cannot compute a mean without finite values")
    return float(np.mean(finite))


def _write_csv(path: Path, fields: tuple[str, ...], rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def _source_rows(report: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    prediction_rows: list[dict[str, Any]] = []
    checkpoint_rows: list[dict[str, Any]] = []
    prediction = report["prediction_correction"]["locus_results"]
    for locus in LOCI:
        result = prediction[locus]
        for row in result["cluster_rows"]:
            prediction_rows.append(
                {
                    "locus": locus,
                    "task_id": row["task_id"],
                    "world_cluster_id": row["world_cluster_id"],
                    "world_seed": row["world_seed"],
                    "complete_case": row["complete_case"],
                    "observed_H3_primary_contrast": row["H3_primary_contrast"],
                    "failure_aware_H3_lower_bound": row[
                        "H3_primary_contrast_lower_bound"
                    ],
                }
            )
        for stage, stage_rows in result["checkpoint_trajectory"].items():
            for arm in ARMS:
                checkpoint_rows.append(
                    {
                        "locus": locus,
                        "stage": stage,
                        "prior_arm": arm,
                        "scored_cell_count": stage_rows[arm]["scored_cell_count"],
                        "mean_normalized_mae": stage_rows[arm]["mean_normalized_mae"],
                    }
                )

    law_rows: list[dict[str, Any]] = []
    blind_rows: list[dict[str, Any]] = []
    for row in report["cell_rows"]:
        checkpoint = row["checkpoint_error"]
        law = row["law_summary"]
        blind = row["blind"]
        law_rows.append(
            {
                "cell_id": row["cell_id"],
                "locus": row["locus_id"],
                "task_id": row["task_id"],
                "prior_arm": row["prior_arm"],
                "terminal_state": row["terminal_state"],
                "effective_final_error": checkpoint["effective_final_error"],
                "law_normalized_mae": law["normalized_mae"],
                "law_minus_final_error": law["summary_minus_effective_final_error"],
                "law_status": law["status"],
            }
        )
        blind_rows.append(
            {
                "cell_id": row["cell_id"],
                "locus": row["locus_id"],
                "task_id": row["task_id"],
                "prior_arm": row["prior_arm"],
                "terminal_state": row["terminal_state"],
                "blind_status": blind["status"],
                "scheduled_execution_count": blind["scheduled_execution_count"],
                "launched_execution_count": blind["launched_execution_count"],
                "completed_execution_count": blind["completed_execution_count"],
                "recommendation_gain_over_incumbent": blind[
                    "recommendation_gain_over_incumbent"
                ],
            }
        )
    return {
        "prediction": prediction_rows,
        "checkpoint": checkpoint_rows,
        "law": law_rows,
        "blind": blind_rows,
    }


def _panel_label(
    ax: mpl.axes.Axes,
    label: str,
    *,
    x: float = -0.16,
    y: float = 1.08,
) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def _plot_prediction(
    ax: mpl.axes.Axes,
    report: Mapping[str, Any],
    rows: list[dict[str, Any]],
) -> None:
    positions: dict[tuple[str, str], float] = {}
    labels: list[str] = []
    ticks: list[float] = []
    y = 0.0
    for locus in LOCI:
        start = y - 0.45
        for task in TASK_ORDER[locus]:
            positions[(locus, task)] = y
            labels.append(f"{LOCUS_LABELS[locus]}  {TASK_LABELS[task]}")
            ticks.append(y)
            y += 1.0
        ax.axhspan(start, y - 0.55, color=LOCUS_COLORS[locus], alpha=0.045, lw=0)
        y += 0.45

    for (locus, task), center in positions.items():
        task_rows = [
            row for row in rows if row["locus"] == locus and row["task_id"] == task
        ]
        task_rows.sort(key=lambda row: int(row["world_seed"]))
        offsets = np.linspace(-0.18, 0.18, len(task_rows))
        observed = [float(row["observed_H3_primary_contrast"]) for row in task_rows]
        adverse = [float(row["failure_aware_H3_lower_bound"]) for row in task_rows]
        for offset, point, lower in zip(offsets, observed, adverse, strict=True):
            ax.plot(
                [lower, point],
                [center + offset, center + offset],
                color=LOCUS_COLORS[locus],
                alpha=0.24,
                lw=0.8,
                zorder=1,
            )
        ax.scatter(
            observed,
            center + offsets,
            s=13,
            facecolor="white",
            edgecolor=LOCUS_COLORS[locus],
            linewidth=0.8,
            zorder=2,
        )
        ax.scatter(
            adverse,
            center + offsets,
            s=18,
            marker="|",
            color=LOCUS_COLORS[locus],
            linewidth=1.0,
            zorder=2,
        )
        ax.scatter(
            _mean(adverse),
            center,
            s=28,
            marker="D",
            facecolor=LOCUS_COLORS[locus],
            edgecolor="black",
            linewidth=0.5,
            zorder=3,
        )

    ax.axvline(0.0, color="#4D4D4D", ls="--", lw=0.9)
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels)
    ax.set_ylim(y - 0.6, -0.6)
    all_values = [
        float(row[field])
        for row in rows
        for field in ("observed_H3_primary_contrast", "failure_aware_H3_lower_bound")
    ]
    ax.set_xlim(min(-0.25, min(all_values) - 0.08), max(0.25, max(all_values) + 0.08))
    ax.set_xlabel(
        "Selective correction contrast, $C_{prior}$\n"
        "(misindexed improvement - aligned improvement)"
    )
    ax.set_title("Prespecified selective-correction evidence across 45 matched worlds", loc="left")
    gate = report["prediction_correction"]["locus_results"]
    p_values = {
        locus: gate[locus]["gate"].get(
            "intersection_union_p_value",
            gate[locus]["gate"].get("effective_intersection_union_p_value"),
        )
        for locus in LOCI
    }
    note = "  ".join(f"{LOCUS_LABELS[locus]}: p={p_values[locus]:.3f}" for locus in LOCI)
    ax.text(1.0, 1.02, note, transform=ax.transAxes, ha="right", va="bottom", fontsize=6)
    ax.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                markerfacecolor="white",
                markeredgecolor="#4D4D4D",
                color="none",
                markersize=4,
                label="Observed world",
            ),
            Line2D(
                [0],
                [0],
                marker="|",
                color="#4D4D4D",
                linestyle="none",
                markersize=7,
                label="Failure-aware lower bound",
            ),
            Line2D(
                [0],
                [0],
                marker="D",
                markerfacecolor="#767676",
                markeredgecolor="black",
                color="none",
                markersize=4,
                label="Task mean lower bound",
            ),
        ],
        loc="upper left",
        ncol=1,
        handletextpad=0.4,
        labelspacing=0.35,
    )
    _panel_label(ax, "a", x=-0.08, y=1.04)


def _plot_checkpoint(ax: mpl.axes.Axes, report: Mapping[str, Any]) -> None:
    matrix = np.array(
        [
            [
                report["prediction_correction"]["locus_results"][locus]["by_arm"][arm][
                    "mean_primary_improvement"
                ]
                for arm in ARMS
            ]
            for locus in LOCI
        ],
        dtype=float,
    )
    image = ax.imshow(
        matrix,
        cmap="Blues",
        vmin=0.0,
        vmax=max(0.2, float(matrix.max())),
        aspect="auto",
    )
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            value = matrix[row, column]
            color = "white" if image.norm(value) > 0.62 else "#272727"
            ax.text(column, row, f"{value:.3f}", ha="center", va="center", color=color)
    ax.set_xticks(range(len(ARMS)), [ARM_LABELS[arm] for arm in ARMS], rotation=20, ha="right")
    ax.set_yticks(range(len(LOCI)), [LOCUS_LABELS[locus] for locus in LOCI])
    ax.set_title("Prediction error reduction", loc="left", pad=8)
    ax.set_xlabel("Prior arm")
    ax.set_ylabel("Intervention locus")
    for spine in ax.spines.values():
        spine.set_visible(False)
    colorbar = ax.figure.colorbar(
        image,
        ax=ax,
        fraction=0.05,
        pad=0.03,
        ticks=(0.0, 0.1, 0.2),
    )
    colorbar.ax.tick_params(labelsize=5)
    _panel_label(ax, "b")


def _plot_law(ax: mpl.axes.Axes, law_rows: list[dict[str, Any]]) -> None:
    for locus_index, locus in enumerate(LOCI):
        for arm in ARMS:
            subset = [
                row
                for row in law_rows
                if row["locus"] == locus and row["prior_arm"] == arm
            ]
            offsets = np.linspace(-0.18, 0.18, len(subset))
            ax.scatter(
                [row["law_minus_final_error"] for row in subset],
                locus_index + offsets,
                s=14,
                marker=ARM_MARKERS[arm],
                color=LOCUS_COLORS[locus],
                alpha=0.62,
                edgecolor="white",
                linewidth=0.25,
            )
    values = _finite(row["law_minus_final_error"] for row in law_rows)
    padding = 0.04 * (max(values) - min(values))
    ax.set_xlim(min(values) - padding, max(values) + padding)
    ax.axvline(0.0, color="#4D4D4D", ls="--", lw=0.9)
    ax.set_yticks(range(len(LOCI)), [LOCUS_LABELS[locus] for locus in LOCI])
    ax.set_ylim(len(LOCI) - 0.55, -0.55)
    ax.set_xlabel("Law MAE - final prediction MAE")
    ax.set_title("Executable laws are often lossy", loc="left", pad=8)
    better = sum(float(row["law_minus_final_error"]) < -1.0e-12 for row in law_rows)
    worse = sum(float(row["law_minus_final_error"]) > 1.0e-12 for row in law_rows)
    equal = len(law_rows) - better - worse
    ax.text(
        0.98,
        0.98,
        f"better/equal/worse: {better}/{equal}/{worse}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.5,
    )
    arm_handles = [
        Line2D(
            [0],
            [0],
            marker=ARM_MARKERS[arm],
            color="none",
            markerfacecolor="#767676",
            label=ARM_LABELS[arm],
        )
        for arm in ARMS
    ]
    ax.legend(
        handles=arm_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.36),
        ncol=3,
        fontsize=5,
        borderaxespad=0.2,
        handletextpad=0.25,
        labelspacing=0.2,
    )
    _panel_label(ax, "c")


def _plot_blind(ax: mpl.axes.Axes, report: Mapping[str, Any]) -> None:
    outcomes = (
        "recommendation_better_count",
        "recommendation_equivalent_count",
        "recommendation_worse_count",
    )
    labels = ("Better", "Equivalent", "Worse")
    colors = ("#2A9D8F", "#B8B8B8", "#C65D57")
    blind = report["blind_action"]
    y = np.arange(len(LOCI))
    left = np.zeros(len(LOCI), dtype=float)
    for field, label, color in zip(outcomes, labels, colors, strict=True):
        counts = np.array([blind[locus][field] for locus in LOCI], dtype=float)
        totals = np.array([blind[locus]["completed_blind_cell_count"] for locus in LOCI])
        percentages = counts / totals * 100.0
        ax.barh(y, percentages, left=left, color=color, height=0.58, label=label)
        for index, (start, width, count) in enumerate(zip(left, percentages, counts, strict=True)):
            if count > 0:
                ax.text(
                    start + width / 2.0,
                    index,
                    f"{int(count)}",
                    ha="center",
                    va="center",
                    color="white" if color != "#B8B8B8" else "#272727",
                    fontsize=6,
                )
        left += percentages
    ax.set_yticks(y, [LOCUS_LABELS[locus] for locus in LOCI])
    ax.set_xlim(0.0, 100.0)
    ax.set_xlabel("Share of blind-evaluable cells (%)")
    ax.set_title("Final actions rarely beat the incumbent", loc="left", pad=8)
    ax.invert_yaxis()
    ax.set_ylim(len(LOCI) - 0.55, -0.75)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.36), ncol=3)
    overall = blind["overall"]
    ax.text(
        1.0,
        0.98,
        (
            f"overall {overall['recommendation_better_count']}/"
            f"{overall['recommendation_equivalent_count']}/"
            f"{overall['recommendation_worse_count']}; "
            f"14/135 cells not evaluable"
        ),
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6,
    )
    _panel_label(ax, "d")


def _save_figure(fig: mpl.figure.Figure, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    base = output / "deepseek_c2_prediction_law_action"
    svg_path = base.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches="tight")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(
        base.with_suffix(".tiff"),
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    fig.savefig(base.with_suffix(".png"), dpi=300, bbox_inches="tight")


def render(report: Mapping[str, Any], output: Path) -> None:
    source = _source_rows(report)
    source_root = output / "source_data"
    _write_csv(
        source_root / "prediction_cluster_contrasts.csv",
        (
            "locus",
            "task_id",
            "world_cluster_id",
            "world_seed",
            "complete_case",
            "observed_H3_primary_contrast",
            "failure_aware_H3_lower_bound",
        ),
        source["prediction"],
    )
    _write_csv(
        source_root / "checkpoint_error_summary.csv",
        ("locus", "stage", "prior_arm", "scored_cell_count", "mean_normalized_mae"),
        source["checkpoint"],
    )
    _write_csv(
        source_root / "law_fidelity_cells.csv",
        (
            "cell_id",
            "locus",
            "task_id",
            "prior_arm",
            "terminal_state",
            "effective_final_error",
            "law_normalized_mae",
            "law_minus_final_error",
            "law_status",
        ),
        source["law"],
    )
    _write_csv(
        source_root / "blind_action_cells.csv",
        (
            "cell_id",
            "locus",
            "task_id",
            "prior_arm",
            "terminal_state",
            "blind_status",
            "scheduled_execution_count",
            "launched_execution_count",
            "completed_execution_count",
            "recommendation_gain_over_incumbent",
        ),
        source["blind"],
    )

    # Manual placement keeps the evidence-heavy hero panel readable while giving
    # the three diagnostics identical visual weight.  Constrained layout made
    # the heat map collapse to its default square aspect and introduced a large
    # non-data gap between rows.
    fig = plt.figure(figsize=(7.2, 6.2))
    prediction_ax = fig.add_axes((0.14, 0.56, 0.83, 0.36))
    checkpoint_ax = fig.add_axes((0.09, 0.14, 0.23, 0.27))
    law_ax = fig.add_axes((0.405, 0.14, 0.23, 0.27))
    blind_ax = fig.add_axes((0.735, 0.14, 0.23, 0.27))
    _plot_prediction(prediction_ax, report, source["prediction"])
    _plot_checkpoint(checkpoint_ax, report)
    _plot_law(law_ax, source["law"])
    _plot_blind(blind_ax, report)
    _save_figure(fig, output)
    plt.close(fig)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main() -> int:
    args = _parser().parse_args()
    report = _load_object(args.report.resolve())
    render(report, args.output.resolve())
    print(
        json.dumps(
            {
                "status": "completed",
                "output": str(args.output.resolve()),
                "cell_count": report["denominators"]["cell_count"],
                "cluster_count": report["denominators"]["cluster_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
