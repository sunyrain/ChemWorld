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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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
            "font.size": 10.0,
            "axes.titlesize": 11.0,
            "axes.labelsize": 10.0,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


MODEL_COLORS = {"deepseek": "#286B9B", "codex": "#8755A1"}
MODEL_SHORT = {"deepseek": "DeepSeek", "codex": "GPT-5.6"}
LOCUS_NAMES = {"A_E": "Entity", "A_P": "Parameters", "A_S": "Structure"}


def clean_axis(ax, *, grid="x"):
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color("#BCC7CE")
    ax.tick_params(length=3, colors=COLORS["ink"], pad=4)
    ax.set_axisbelow(True)
    ax.grid(axis=grid, color="#E6EBEF", linewidth=0.7)


def heading(ax, letter, title):
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", pad=13)
    ax.text(
        -0.12,
        1.055,
        letter,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        va="bottom",
        color=COLORS["ink"],
    )


def model_legend(fig, *, y=0.98):
    handles = [
        mpl.lines.Line2D(
            [],
            [],
            color=MODEL_COLORS[key],
            marker="o",
            linestyle="none",
            markersize=5,
            label=MODEL_SHORT[key],
        )
        for key in ("deepseek", "codex")
    ]
    fig.legend(
        handles=handles,
        loc="upper right",
        bbox_to_anchor=(0.99, y),
        ncol=2,
        columnspacing=1.2,
        handletextpad=0.4,
        fontsize=9.5,
    )


def render_figure_1() -> list[Path]:
    fig, ax = plt.subplots(figsize=(6.6, 2.05))
    fig.subplots_adjust(left=0.005, right=0.995, top=0.96, bottom=0.04)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    ax.text(
        0.135,
        0.98,
        "Vary the supplied description",
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
    )
    for y, label, color in (
        (0.73, "Opaque", COLORS["opaque"]),
        (0.48, "Aligned", COLORS["aligned"]),
        (0.23, "Misindexed", COLORS["misindexed"]),
    ):
        rounded_box(
            ax,
            0.025,
            y - 0.08,
            0.22,
            0.16,
            label,
            facecolor="white",
            edgecolor=color,
            fontsize=10,
            linewidth=1.4,
        )
        arrow(ax, (0.258, y), (0.34, 0.49), color=color, mutation_scale=9)
    rounded_box(
        ax,
        0.35,
        0.31,
        0.24,
        0.36,
        "Fixed world\nAgent experiments\nPublic evidence",
        facecolor="#EFF4F7",
        edgecolor="#BCC7CE",
        fontsize=10,
    )
    ax.text(0.47, 0.16, "Same rules and budget", ha="center", fontsize=9, color=COLORS["muted"])
    ax.text(
        0.825, 0.98, "Measure separately", ha="center", va="top", fontsize=10, fontweight="bold"
    )
    for y, label in (
        (0.73, "Held-out predictions"),
        (0.48, "Executable knowledge"),
        (0.23, "Unseen-plan decisions"),
    ):
        arrow(ax, (0.6, 0.49), (0.69, y), mutation_scale=9)
        rounded_box(
            ax,
            0.7,
            y - 0.08,
            0.27,
            0.16,
            label,
            facecolor="white",
            edgecolor=COLORS["blue"],
            fontsize=9.6,
        )
    return export_figure(fig, "figure-1-prior-to-law")


def render_figure_2(design: dict, preflight: dict) -> list[Path]:
    if len(design["tasks"]) != 5 or preflight["expected_counts"]["participant_cells"] != 75:
        raise ValueError("unexpected entity cohort")
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    fig.subplots_adjust(left=0.025, right=0.98, top=0.95, bottom=0.06)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    columns = [0.01, 0.26, 0.70, 0.86]
    for x, text in zip(columns, ("Locus", "Task coverage", "Clusters", "Budget"), strict=True):
        ax.text(x, 0.95, text, fontsize=10, fontweight="bold")
    rows = [
        (
            "Entity",
            "Electrochemistry · crystallization\nDistillation · partition · safety",
            "25",
            "8",
        ),
        ("Parameters", "Electrochemistry · reaction safety", "10", "10"),
        ("Structure", "Partition · crystallization", "10", "12"),
    ]
    for index, row in enumerate(rows):
        y = 0.76 - index * 0.23
        ax.axhline(y + 0.125, color="#DCE4E8", lw=0.7)
        for col, (x, text) in enumerate(zip(columns, row, strict=True)):
            ax.text(
                x,
                y,
                text,
                va="center",
                fontsize=10 if col != 1 else 9.2,
                fontweight="bold" if col == 0 else "normal",
            )
    ax.text(
        0.01,
        0.03,
        "45 task-world clusters  x  3 arms  =  135 sessions",
        fontsize=11,
        fontweight="bold",
        color=COLORS["blue"],
    )
    ax.text(
        0.01,
        -0.065,
        "Budget = complete experiments per session; 1,260 planned in total.",
        fontsize=9,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-2-formal-cohort")


def render_figure_3_prospective(initial_rows, recipe_rows, improvement_rows, decision_rows):
    del recipe_rows  # complete manipulation counts remain in the caption and source data
    initial = {(row["locus"], row["arm"]): row["mean_normalized_mae"] for row in initial_rows}
    gains = {
        (row["locus"], row["arm"]): row["mean_pre_to_final_improvement"] for row in improvement_rows
    }
    if any(row["passed"] for row in decision_rows):
        raise ValueError("selective-correction caption no longer matches the evidence")
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.95), sharey=True)
    fig.subplots_adjust(left=0.11, right=0.985, top=0.79, bottom=0.22, wspace=0.22)
    for ax, locus, letter, n in zip(axes, LOCUS_NAMES, "abc", (25, 10, 10), strict=True):
        heading(ax, letter, LOCUS_NAMES[locus])
        clean_axis(ax, grid="y")
        for arm in ARM_ORDER:
            before = initial[locus, arm]
            ax.plot(
                [0, 1],
                [before, before - gains[locus, arm]],
                "o-",
                color=ARM_COLOR[arm],
                lw=1.8,
                ms=5,
                label=ARM_LABEL[arm],
            )
        ax.set(
            xlim=(-0.17, 1.17),
            ylim=(0, 0.43),
            xticks=[0, 1],
            xticklabels=["Before", "Final"],
            yticks=[0, 0.1, 0.2, 0.3, 0.4],
        )
        ax.text(
            0.5,
            -0.27,
            f"{n} clusters · {3 * n} sessions",
            transform=ax.transAxes,
            ha="center",
            fontsize=9,
            color=COLORS["muted"],
        )
    axes[0].set_ylabel("Mean prediction MAE")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.53, 1.02),
        ncol=3,
        columnspacing=1.5,
        handlelength=1.5,
        fontsize=10,
    )
    fig.text(
        0.55,
        0.015,
        "Selective-correction criterion unmet at every locus",
        ha="center",
        fontsize=9.5,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-3-prior-uptake-and-correction")


def render_figure_4_matched(cell_rows, cross_configuration_rows, b3_rows):
    del cross_configuration_rows  # descriptive contrasts remain in the text and source table
    fig = plt.figure(figsize=(6.6, 3.15))
    left = fig.add_axes((0.10, 0.23, 0.24, 0.61))
    right = fig.add_axes((0.67, 0.23, 0.30, 0.61))
    heading(left, "a", "B2: numerical fit")
    clean_axis(left, grid="y")
    for row in cell_rows:
        left.plot(
            [0, 1],
            [row["pre_error"], row["post_error"]],
            "o-",
            color=ARM_COLOR[row["arm"]],
            lw=0.9,
            alpha=0.7,
            ms=3,
        )
    left.set(
        yscale="log",
        ylim=(0.003, 0.6),
        xlim=(-0.17, 1.17),
        xticks=[0, 1],
        xticklabels=["Before", "After"],
        yticks=[0.005, 0.02, 0.1, 0.5],
    )
    left.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda value, _: f"{value:g}"))
    left.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    left.axhline(0.02, color="#AAB7C0", ls="--", lw=0.8)
    left.set_ylabel("Prediction MAE (log scale)")
    left.text(
        0.5, -0.30, "15 paired cells · 5 worlds", transform=left.transAxes, ha="center", fontsize=9
    )
    heading(right, "b", "B3: available and useful")
    clean_axis(right)
    measures = ["Completed", "Joint law recovery", "Top-1 action", "Useful action gain"]
    for row in b3_rows:
        y = 3 - measures.index(row["measure"]) + (0.13 if row["model"] == "deepseek" else -0.13)
        right.plot(row["rate"], y, "o", color=MODEL_COLORS[row["model"]], ms=5)
        right.text(
            max(row["rate"] + 0.06, 0.075),
            y,
            f"{row['count']}/{row['denominator']}",
            fontsize=9,
            va="center",
            color=MODEL_COLORS[row["model"]],
        )
    right.set(
        xlim=(-0.025, 1.36),
        ylim=(-0.48, 3.5),
        xticks=[0, 0.5, 1],
        xticklabels=["0%", "50%", "100%"],
        yticks=[3, 2, 1, 0],
        yticklabels=["Completed", "Joint recovery", "Top-1", "Useful gain"],
    )
    right.tick_params(axis="y", length=0, labelsize=9.5)
    right.set_xlabel("Share of scheduled opportunities", fontsize=9)
    model_legend(fig, y=1.02)
    fig.text(
        0.51,
        0.015,
        "B2 underidentifies family; B3 retains all 13 DeepSeek schema failures.",
        ha="center",
        fontsize=9,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-4-matched-evidence-localization")


def render_figure_5_cross_model_c2(model_rows, locus_rows, gate_rows):
    del gate_rows
    fig = plt.figure(figsize=(6.6, 3.25))
    left = fig.add_axes((0.15, 0.24, 0.35, 0.59))
    right = fig.add_axes((0.64, 0.24, 0.34, 0.59))
    heading(left, "a", "Prediction → executable law")
    clean_axis(left)
    for row in locus_rows:
        y = (2 - list(LOCUS_NAMES).index(row["locus"])) * 1.5
        y += 0.21 if row["model"] == "deepseek" else -0.21
        color = MODEL_COLORS[row["model"]]
        law = row["mean_law_mae"]
        matched_prediction = law - row["mean_law_compression_loss"]
        left.plot([matched_prediction, law], [y, y], color=color, lw=2)
        left.plot(matched_prediction, y, "o", mfc="white", mec=color, ms=5, mew=1.3)
        left.plot(law, y, "o", color=color, ms=5)
    left.set(
        xlim=(0.1, 0.31),
        ylim=(-0.6, 3.7),
        yticks=[3, 1.5, 0],
        yticklabels=list(LOCUS_NAMES.values()),
        xticks=[0.1, 0.2, 0.3],
        xlabel="Mean absolute error",
    )
    left.tick_params(axis="y", length=0)
    heading(right, "b", "Incumbent replay")
    outcome_colors = [COLORS["aligned"], "#CDD5DB", COLORS["misindexed"], "#FAFAFA"]
    for row, y in zip(model_rows, [1, 0], strict=True):
        counts = [
            row["blind_better_count"],
            row["blind_equivalent_count"],
            row["blind_worse_count"],
            row["scheduled_cell_count"] - row["blind_gain_evaluable_count"],
        ]
        start = 0
        for index, (count, color) in enumerate(zip(counts, outcome_colors, strict=True)):
            right.barh(
                y,
                count,
                left=start,
                height=0.25,
                color=color,
                edgecolor="#8998A2",
                linewidth=0.5,
                hatch="////" if index == 3 else None,
            )
            start += count
        right.text(
            0,
            y + 0.25,
            MODEL_SHORT[row["model"]],
            fontsize=10,
            fontweight="bold",
            color=MODEL_COLORS[row["model"]],
        )
        right.text(0, y - 0.34, " / ".join(map(str, counts)), fontsize=10, color=COLORS["ink"])
    right.set(
        xlim=(0, 135),
        ylim=(-0.55, 1.7),
        xticks=[0, 45, 90, 135],
        yticks=[],
        xlabel="Scheduled cells",
    )
    clean_axis(right)
    right.spines["left"].set_visible(False)
    model_legend(fig, y=1.02)
    fig.text(0.12, 0.095, "○ Prediction    ● Law", fontsize=9.5, color=COLORS["muted"])
    fig.text(
        0.63, 0.095, "Counts: better / equal / worse / missing", fontsize=8.5, color=COLORS["muted"]
    )
    fig.text(
        0.51,
        0.015,
        "Matched law evaluations: 135 DeepSeek, 129 GPT · 135 scheduled per model",
        ha="center",
        fontsize=9,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-5-capability-chain")


def render_figure_6_open_action(
    open_rows,
    open_summary,
    formal,
    construction,
    qualification,
    gate_alignment,
    reviewer_controls,
    action_extension,
):
    del formal, construction, qualification, gate_alignment, reviewer_controls
    eligible_ids = {row["cell_id"] for row in open_rows if row["eligible"]}
    fig = plt.figure(figsize=(6.6, 4.65))
    scatter = fig.add_axes((0.10, 0.58, 0.31, 0.29))
    outcome = fig.add_axes((0.67, 0.58, 0.29, 0.29))
    forest = fig.add_axes((0.31, 0.13, 0.64, 0.27))
    heading(scatter, "a", "DeepSeek: law vs. action")
    clean_axis(scatter, grid="both")
    scatter.plot([0, 1], [0, 1], color="#B6C1C9", ls="--", lw=0.8)
    missing = 0
    rows = open_summary["decision_aligned_law_action"]["cell_rows"]
    for row in rows:
        x = row["law_implied_normalized_regret"]
        y = row["participant_normalized_regret"]
        if row["cell_id"] not in eligible_ids:
            scatter.plot(x, 1.13, "x", color=COLORS["red"], ms=5)
            missing += 1
        else:
            scatter.plot(
                x,
                y,
                "o",
                color=MODEL_COLORS["deepseek"],
                ms=4,
                alpha=0.65,
                mec="white",
                mew=0.3,
            )
    scatter.set(
        xlim=(-0.04, 1.04),
        ylim=(-0.05, 1.38),
        xticks=[0, 0.5, 1],
        yticks=[0, 0.5, 1],
        xlabel="Law-implied regret",
        ylabel="Participant regret",
    )
    scatter.text(
        0.02, 1.30, f"{missing} missing rankings", fontsize=8, va="center", color=COLORS["red"]
    )
    condition_rows, contrasts = build_action_extension_rows(action_extension)
    heading(outcome, "b", "Information strategies")
    clean_axis(outcome)
    order = ["no_evidence", "learned_law_only", "autonomous_exploration", "yoked_evidence"]
    for row in condition_rows:
        y = 3 - order.index(row["condition"]) + (0.13 if row["model"] == "deepseek" else -0.13)
        value = row["mean_failure_aware_normalized_regret"]
        outcome.plot(value, y, "o", color=MODEL_COLORS[row["model"]], ms=4.5)
        outcome.text(
            1.01,
            y,
            f"{row['completed_count']}/45",
            fontsize=8.5,
            va="center",
            color=MODEL_COLORS[row["model"]],
        )
    outcome.set(
        xlim=(0, 1.3),
        ylim=(-0.55, 3.55),
        xticks=[0, 0.5, 1],
        yticks=[3, 2, 1, 0],
        yticklabels=["None", "Law only", "Autonomous", "Yoked"],
        xlabel="Failure-aware regret",
    )
    outcome.tick_params(axis="y", length=0, labelsize=9)
    outcome.text(1.05, 3.85, "Valid", fontsize=8.5, color=COLORS["muted"])
    heading(forest, "c", "Paired differences from no evidence")
    clean_axis(forest)
    forest.axvline(0, color=COLORS["ink"], lw=0.9)
    contrast_ids = [
        "autonomous_exploration_minus_no_evidence",
        "learned_law_only_minus_no_evidence",
        "yoked_evidence_minus_no_evidence",
    ]
    for row in contrasts:
        if row["contrast"] not in contrast_ids:
            continue
        y = (
            2
            - contrast_ids.index(row["contrast"])
            + (0.12 if row["model"] == "deepseek" else -0.12)
        )
        mean = row["mean_regret_difference"]
        forest.errorbar(
            mean,
            y,
            xerr=[[mean - row["interval_low"]], [row["interval_high"] - mean]],
            fmt="o",
            ms=4.5,
            color=MODEL_COLORS[row["model"]],
            lw=1.5,
            capsize=2,
        )
    forest.set(
        xlim=(-0.26, 0.58),
        ylim=(-0.48, 2.5),
        xticks=[-0.2, 0, 0.2, 0.4],
        yticks=[2, 1, 0],
        yticklabels=["Autonomous", "Law only", "Yoked"],
    )
    forest.tick_params(axis="y", length=0)
    forest.set_xlabel("Change in regret    ← better     worse →", fontsize=10)
    model_legend(fig, y=1.005)
    fig.text(
        0.52,
        0.015,
        "45 strata/model · 95% world-cluster bootstrap intervals · failures retained",
        ha="center",
        fontsize=9,
        color=COLORS["muted"],
    )
    return export_figure(fig, "figure-6-open-action-formal")


def main() -> int:
    configure_matplotlib()
    design_path = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
    preflight_path = (
        ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json"
    )
    current = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))
    publication_reanalysis_path = (
        ROOT / current["work_ii"]["w2_64_publication_reanalysis"]["report"]
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
    paired_error_rows = [
        {
            "model": row["model"],
            "locus": row["locus"],
            "matched_law_count": row["law_evaluated_count"],
            "matched_prediction_mae": row["mean_law_mae"] - row["mean_law_compression_loss"],
            "law_mae": row["mean_law_mae"],
        }
        for row in c2_locus_rows
    ]
    write_csv(
        SOURCE_DIR / "figure-5-matched-error-endpoints.csv",
        paired_error_rows,
        ["model", "locus", "matched_law_count", "matched_prediction_mae", "law_mae"],
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
    m1_binding = current["work_ii"].get("w2_72_m1_replication")
    m1_report = None
    if m1_binding and m1_binding.get("formal_result"):
        import render_m1_replication

        m1_report, m1_path = render_m1_replication.load_report()
        outputs["figure_7"] = render_m1_replication.render(m1_report)
        source_paths.extend([m1_path, OUTPUT_DIR / "render_m1_replication.py"])
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-prior-discovery-figure-manifest-0.1",
        "status": "formal_results_with_bounded_secondary_analyses",
        "backend": "python_matplotlib",
        "formal_hypothesis_tests_run": False,
        "provider_groups_mixed_in_scientific_contrasts": m1_report is not None,
        "provider_group_handling": "Historical cohorts remain separate by model. M1, when present, "
        "uses its preregistered average over two model configurations and two repeats within "
        "each independent world; it does not estimate provider superiority.",
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
            "m1_scheduled_slots": len(m1_report["slots"]) if m1_report else 0,
            "m1_world_clusters": m1_report["independent_world_clusters"] if m1_report else 0,
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
            "B2 cross-configuration contrasts remain in the source tables and text; "
            "the incomplete A-P low block is excluded.",
            "Figure 5 compares fully scheduled 135-cell DeepSeek-v4-flash and GPT-5.6-sol "
            "C2 surfaces; model differences are matched descriptive and not provider "
            "causal effects.",
            "Figure 6 combines the four-condition action successor, the DeepSeek longitudinal "
            "decision-aligned law-action analysis; gate diagnostics remain in the appendix.",
            "The four-condition block is development successor evidence; yoked recipient "
            "failures remain in the failure-aware denominator and prevent a pure "
            "experiment-selection interpretation.",
            "The 96- and 320-query controls contain zero participant sessions; exposed "
            "construction and fresh qualification remain separate evidence roles.",
            "The gate-alignment diagnostic reproduces 16 frozen unit versions without new "
            "truth, provider or physical execution and does not revise historical stop "
            "decisions.",
            "No cross-provider capability ranking or context-reset portability claim is supported.",
            "M1, when present, replaces a quadratic representation and/or decision rule with "
            "public evidence fixed. World-level intervals are read from its frozen analysis. "
            "Recipients also receive evidence; this does not establish artifact-only transfer.",
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
