"""Render Work I Figure 6 from the frozen G2 v0.5 fresh trajectories."""

# Static publication contract inherited from the shared Python helper:
# width_mm=179.832, Arial/sans-serif, svg.fonttype='none', pdf.fonttype=42;
# exports .svg, .pdf and .png at dpi=300.

# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle
from scripts.render_work_i_figure_1 import (
    _canonical_sha256,
    _configure_matplotlib,
    _file_sha256,
    _json_text,
    _mapping,
    _mapping_rows,
    _panel,
    _png_dimensions,
    _read_json,
)

ROOT = REPOSITORY_ROOT
CURRENT_PATH = Path("configs/current.json")
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
SHARED_STYLE_HELPER_PATH = Path("scripts/render_work_i_figure_1.py")
SCRIPT_PATH = Path("scripts/render_work_i_figure_6.py")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-6-fresh-trajectories"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"

WORLD_ORDER = (1, 3)
REPLICATE_ORDER = ("r01", "r02", "r03", "r04", "r05")
CORE_METRICS = (
    "global_best_discovery_fraction",
    "online_incumbent_retention_rate",
    "maximum_absolute_incumbent_drawdown",
    "terminal_to_global_best_ratio",
)
PROCESS_METRICS = (
    *CORE_METRICS[:3],
    "recovered_loss_episode_count",
    CORE_METRICS[3],
)
PROCESS_LABELS = ("discovery", "retention", "drawdown", "recovery", "terminal / best")
DISCORDANT_PAIR_IDS = ((1, "r03"), (3, "r01"))


class FigureSixError(RuntimeError):
    """Raised when a current frozen input or rendered Figure 6 fails closed."""


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("system_sha256") != _canonical_sha256(payload, "system_sha256"):
        raise FigureSixError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureSixError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureSixError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureSixError(f"stale P01 source binding: {path_value}")
    matches = [row for row in _mapping_rows(payload, "figures") if row.get("figure_id") == "F6"]
    if len(matches) != 1:
        raise FigureSixError("P01 must define exactly one F6")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P07"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
        or spec.get("pending_result_panels") != []
    ):
        raise FigureSixError("P01 F6 assignment differs from W1-P07")
    if [row.get("panel") for row in _mapping_rows(spec, "panels")] != list("ABCD"):
        raise FigureSixError("P01 F6 panel order must be A-D")
    return spec


def _validate_pairs(g2: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pairs = [dict(row) for row in _mapping_rows(g2, "paired_trajectories")]
    expected = {(world, replicate) for world in WORLD_ORDER for replicate in REPLICATE_ORDER}
    identities = {(row.get("world_seed"), row.get("trajectory_replicate_id")) for row in pairs}
    if len(pairs) != 10 or identities != expected:
        raise FigureSixError("fresh-trajectory pair identity matrix changed")

    complete: list[dict[str, Any]] = []
    censored: list[dict[str, Any]] = []
    for row in pairs:
        contrast = row.get("nominal_minus_opaque")
        if row.get("pair_complete") is True:
            if row.get("nominal_state") != "completed" or row.get("opaque_state") != "completed":
                raise FigureSixError("complete pair lacks two completed arms")
            if not isinstance(contrast, Mapping):
                raise FigureSixError("complete pair lacks its matched contrast")
            if any(
                not isinstance(contrast.get(metric), (int, float)) for metric in PROCESS_METRICS
            ):
                raise FigureSixError("complete pair lacks a process contrast")
            if any(
                not isinstance(contrast.get(metric), (int, float))
                for metric in ("best_final_score", "terminal_final_score")
            ):
                raise FigureSixError("complete pair lacks endpoint diagnostics")
            complete.append(row)
        else:
            states = {row.get("nominal_state"), row.get("opaque_state")}
            if states != {"completed", "right_censored"} or contrast is not None:
                raise FigureSixError("right-censored pair accounting changed")
            censored.append(row)
    if len(complete) != 8 or len(censored) != 2:
        raise FigureSixError("expected eight complete and two right-censored pairs")
    return pairs, complete


def _sign_discordant_pair_ids(complete_pairs: list[dict[str, Any]]) -> tuple[tuple[int, str], ...]:
    result: list[tuple[int, str]] = []
    for row in complete_pairs:
        contrast = cast(Mapping[str, Any], row["nominal_minus_opaque"])
        best = float(contrast["best_final_score"])
        terminal = float(contrast["terminal_final_score"])
        if (best > 0) != (terminal > 0):
            result.append((int(row["world_seed"]), str(row["trajectory_replicate_id"])))
    return tuple(result)


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Resolve current.json and validate the frozen G2 v0.5 evidence."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)
    current = _read_json(resolved / CURRENT_PATH)
    publication = _mapping(current, "publication")
    release_value = publication.get("release_manifest")
    audit_value = publication.get("remaining_experiment_audit")
    if not isinstance(release_value, str) or not isinstance(audit_value, str):
        raise FigureSixError("configs/current.json lacks release or remaining-audit paths")
    release_path = Path(release_value)
    audit_path = Path(audit_value)
    release = _read_json(resolved / release_path)
    evidence = _mapping(release, "evidence")
    derived_binding = _mapping(evidence, "frozen_derived_data")
    derived_value = derived_binding.get("path")
    if not isinstance(derived_value, str):
        raise FigureSixError("current release lacks frozen derived data")
    derived_path = Path(derived_value)
    derived = _read_json(resolved / derived_path)
    if (
        derived_binding.get("status") != "frozen_complete"
        or derived.get("status") != "frozen_complete"
        or derived.get("derived_data_sha256") != _canonical_sha256(derived, "derived_data_sha256")
        or derived.get("derived_data_sha256") != derived_binding.get("derived_data_sha256")
    ):
        raise FigureSixError("current frozen derived-data binding is stale")

    if evidence.get("g2_v0_5_remaining_audit") != audit_path.as_posix():
        raise FigureSixError("current and release remaining-audit paths differ")
    audit = _read_json(resolved / audit_path)
    if audit.get("audit_sha256") != _canonical_sha256(audit, "audit_sha256"):
        raise FigureSixError("remaining-experiment audit self-hash mismatch")

    g2 = _mapping(derived, "g2_v0_5")
    matrix = _mapping(g2, "matrix")
    interpretation = _mapping(g2, "interpretation")
    selected = _mapping(interpretation, "selected_branch")
    policy = _mapping(interpretation, "mapping_policy")
    policy_value = policy.get("path")
    if not isinstance(policy_value, str):
        raise FigureSixError("G2 v0.5 mapping policy path is missing")
    policy_path = Path(policy_value)
    if _file_sha256(resolved / policy_path) != policy.get("sha256"):
        raise FigureSixError("G2 v0.5 mapping policy hash mismatch")

    release_result = _mapping(evidence, "g2_v0_5_result")
    required_matrix = _mapping(publication, "required_new_scientific_matrix")
    if (
        g2.get("status") != "completed_audited_fresh_trajectory_replication_with_right_censoring"
        or g2.get("audit_sha256") != release_result.get("audit_sha256")
        or release_result.get("status") != g2.get("status")
        or release_result.get("completed_cells") != 18
        or release_result.get("right_censored_cells") != 2
        or release_result.get("completed_pairs") != 8
        or release_result.get("right_censored_pairs") != 2
        or release_result.get("executed_vessels") != 114
        or release_result.get("completed_final_assays") != 112
        or release_result.get("accepted_primitive_operations") != 1615
        or required_matrix.get("status") != "completed_audited_with_right_censoring"
        or required_matrix.get("planned_cells") != 20
        or required_matrix.get("planned_vessel_opportunities") != 120
    ):
        raise FigureSixError("current G2 v0.5 release accounting changed")
    if (
        matrix.get("all_attempt_selection_policies_verified") is not True
        or matrix.get("all_physical_pairs_verified") is not True
        or matrix.get("all_terminal_cells_resource_replay_verified") is not True
        or matrix.get("planned_cell_count") != 20
        or matrix.get("completed_cell_count") != 18
        or matrix.get("right_censored_cell_count") != 2
        or matrix.get("completed_pair_count") != 8
        or matrix.get("right_censored_cell_ids") != ["cell-001", "cell-019"]
        or matrix.get("world_seeds") != list(WORLD_ORDER)
        or matrix.get("trajectory_replicate_ids") != list(REPLICATE_ORDER)
    ):
        raise FigureSixError("G2 v0.5 matrix accounting changed")

    terminal = _mapping(audit, "formal_terminal_accounting")
    capacity = _mapping(audit, "paired_analysis_capacity")
    if (
        terminal.get("cells_still_to_terminalize") != 0
        or terminal.get("resolved_vessel_opportunity_slots") != 120
        or terminal.get("vessel_opportunity_slots_still_to_resolve") != 0
        or capacity.get("planned_pairs") != 10
        or capacity.get("completed_pairs") != 8
        or capacity.get("right_censored_pairs") != 2
        or capacity.get("unresolved_pairs") != 0
    ):
        raise FigureSixError("formal terminal or paired accounting changed")

    pairs, complete_pairs = _validate_pairs(g2)
    if _sign_discordant_pair_ids(complete_pairs) != DISCORDANT_PAIR_IDS:
        raise FigureSixError("2-of-8 best-versus-terminal diagnostic changed")

    classifications = _mapping(selected, "world_metric_classifications")
    core_classes = [
        str(_mapping(classifications, str(world))[metric])
        for world in WORLD_ORDER
        for metric in CORE_METRICS
    ]
    if (
        interpretation.get("analysis_unit") != "fixed physical world by fresh trajectory replicate"
        or interpretation.get("descriptive_only") is not True
        or interpretation.get("development_trajectory_included") is not False
        or interpretation.get("provider_sampling_seed_controlled") is not False
        or interpretation.get("selected_world_count") != 2
        or interpretation.get("fresh_replicates_per_selected_world") != 5
        or interpretation.get("general_world_effect_allowed") is not False
        or selected.get("branch_id") != "frequent_within_world_reversal"
        or tuple(selected.get("core_trajectory_metrics", ())) != CORE_METRICS
        or selected.get("directional_consistency_threshold") != 0.75
        or selected.get("mixed_world_by_core_metric_count") != 6
        or selected.get("world_by_core_metric_count") != 8
        or core_classes.count("mixed") != 6
        or core_classes.count("directionally_positive") != 1
        or core_classes.count("directionally_negative") != 1
    ):
        raise FigureSixError("G2 v0.5 descriptive interpretation boundary changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "current": current,
        "release": release,
        "release_path": release_path,
        "derived": derived,
        "derived_path": derived_path,
        "audit": audit,
        "audit_path": audit_path,
        "policy_path": policy_path,
        "g2": g2,
        "matrix": matrix,
        "interpretation": interpretation,
        "selected": selected,
        "pairs": pairs,
        "complete_pairs": complete_pairs,
        "core_classes": core_classes,
        "release_result": release_result,
    }


def _configure(figure_system: Mapping[str, Any]) -> dict[str, str]:
    colors = _configure_matplotlib(figure_system)
    mpl.rcParams["svg.hashsalt"] = "chemworld-work-i-figure-6-v0.1"
    return colors


def _draw_panel_a(ax: Any, pairs: list[dict[str, Any]], colors: Mapping[str, str]) -> None:
    _panel(ax, "A", "Fresh matched sessions retain planned coverage", colors)
    ax.set_axis_off()
    lookup = {(int(row["world_seed"]), str(row["trajectory_replicate_id"])): row for row in pairs}
    for column, _replicate in enumerate(REPLICATE_ORDER):
        x = 0.22 + column * 0.15
        ax.text(
            x,
            0.84,
            f"rep. {column + 1}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.5,
        )
    for row_index, world in enumerate(WORLD_ORDER):
        y = 0.64 - row_index * 0.31
        ax.text(
            0.03,
            y,
            f"world {world}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=7.0,
            fontweight=600,
            color=colors["ink"],
        )
        for column, replicate in enumerate(REPLICATE_ORDER):
            x = 0.22 + column * 0.15
            pair = lookup[(world, replicate)]
            complete = pair["pair_complete"] is True
            face = colors["pale_navy"] if complete else colors["pale_coral"]
            edge = colors["teal"] if complete else colors["coral"]
            box = FancyBboxPatch(
                (x - 0.055, y - 0.09),
                0.11,
                0.18,
                boxstyle="round,pad=0.006,rounding_size=0.012",
                transform=ax.transAxes,
                facecolor=face,
                edgecolor=edge,
                linewidth=0.8,
            )
            ax.add_patch(box)
            for dx, arm_color in ((-0.022, colors["navy"]), (0.022, colors["coral"])):
                state = pair["opaque_state"] if dx < 0 else pair["nominal_state"]
                ax.scatter(
                    [x + dx],
                    [y],
                    transform=ax.transAxes,
                    s=28,
                    marker="o",
                    facecolor=arm_color if state == "completed" else colors["white"],
                    edgecolor=arm_color,
                    linewidth=0.8,
                )
            ax.text(
                x,
                y - 0.125,
                "complete" if complete else "censored",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=6.5,
                color=edge,
            )
    ax.text(
        0.50,
        0.08,
        "10 planned matched pairs  |  8 complete  |  2 right-censored",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight=600,
        color=colors["ink"],
    )


def _draw_panel_b(ax: Any, complete_pairs: list[dict[str, Any]], colors: Mapping[str, str]) -> None:
    _panel(ax, "B", "Best and terminal contrasts can reverse sign", colors)
    ordered = sorted(
        complete_pairs,
        key=lambda row: (
            WORLD_ORDER.index(int(row["world_seed"])),
            REPLICATE_ORDER.index(str(row["trajectory_replicate_id"])),
        ),
    )
    y_positions = np.arange(len(ordered))[::-1]
    for y, row in zip(y_positions, ordered, strict=True):
        contrast = cast(Mapping[str, Any], row["nominal_minus_opaque"])
        best = float(contrast["best_final_score"])
        terminal = float(contrast["terminal_final_score"])
        identity = (int(row["world_seed"]), str(row["trajectory_replicate_id"]))
        color = colors["amber"] if identity in DISCORDANT_PAIR_IDS else colors["grid_gray"]
        ax.plot([best, terminal], [y, y], color=color, linewidth=1.2, zorder=1)
        ax.scatter([best], [y], color=colors["navy"], s=23, marker="o", zorder=2)
        ax.scatter([terminal], [y], color=colors["coral"], s=27, marker="D", zorder=2)
    ax.axvline(0, color=colors["mid_gray"], linewidth=0.7, linestyle="--")
    ax.set_xlim(-0.45, 0.55)
    ax.set_ylim(-1.5, 7.7)
    replicate_labels = {replicate: index + 1 for index, replicate in enumerate(REPLICATE_ORDER)}
    ax.set_yticks(
        y_positions,
        [
            f"world {row['world_seed']} / rep. "
            f"{replicate_labels[row['trajectory_replicate_id']]}"
            for row in ordered
        ],
    )
    ax.set_xlabel("nominal - opaque score contrast")
    ax.grid(axis="x", color=colors["grid_gray"], linewidth=0.45)
    ax.legend(
        handles=[
            Line2D(
                [], [], marker="o", linestyle="none", color=colors["navy"], label="historical best"
            ),
            Line2D(
                [], [], marker="D", linestyle="none", color=colors["coral"], label="raw terminal"
            ),
        ],
        loc="lower right",
        ncol=2,
        handletextpad=0.3,
        columnspacing=0.8,
    )
    ax.text(
        0.02,
        0.98,
        "2 / 8 sign-discordant\nendpoint diagnostic",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.5,
        fontweight=600,
        color=colors["amber"],
    )


def _draw_panel_c(ax: Any, complete_pairs: list[dict[str, Any]], colors: Mapping[str, str]) -> None:
    _panel(ax, "C", "Process contrasts vary within fixed worlds", colors)
    offsets = {1: -0.11, 3: 0.11}
    markers = {1: "o", 3: "s"}
    world_colors = {1: colors["ink"], 3: colors["mid_gray"]}
    for world in WORLD_ORDER:
        rows = [row for row in complete_pairs if row["world_seed"] == world]
        for metric_index, metric in enumerate(PROCESS_METRICS):
            values = [
                float(cast(Mapping[str, Any], row["nominal_minus_opaque"])[metric]) for row in rows
            ]
            jitter = np.linspace(-0.035, 0.035, len(values))
            ax.scatter(
                metric_index + offsets[world] + jitter,
                values,
                s=22,
                marker=markers[world],
                facecolor=world_colors[world] if world == 1 else colors["white"],
                edgecolor=world_colors[world],
                linewidth=0.75,
                label=f"world {world}" if metric_index == 0 else None,
                zorder=2,
            )
    ax.axhline(0, color=colors["mid_gray"], linewidth=0.7, linestyle="--")
    ax.set_xlim(-0.45, 4.45)
    ax.set_ylim(-1.08, 1.08)
    ax.set_xticks(range(len(PROCESS_LABELS)), PROCESS_LABELS, rotation=18, ha="right")
    ax.set_ylabel("nominal - opaque contrast")
    ax.grid(axis="y", color=colors["grid_gray"], linewidth=0.45)
    ax.legend(
        loc="upper left",
        ncol=2,
        handletextpad=0.3,
        columnspacing=0.8,
        borderaxespad=0.25,
    )


def _draw_panel_d(
    ax: Any,
    pairs: list[dict[str, Any]],
    selected: Mapping[str, Any],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "D", "Censoring is explicit; classes stay supporting", colors)
    ax.set_axis_off()
    ax.text(0.04, 0.86, "pair disposition", transform=ax.transAxes, fontsize=6.5, fontweight=600)
    for index, row in enumerate(pairs):
        x = 0.05 + index * 0.089
        complete = row["pair_complete"] is True
        ax.add_patch(
            Rectangle(
                (x, 0.72),
                0.065,
                0.085,
                transform=ax.transAxes,
                facecolor=colors["teal"] if complete else colors["white"],
                edgecolor=colors["teal"] if complete else colors["coral"],
                linewidth=0.8,
                hatch=None if complete else "///",
            )
        )
        ax.text(
            x + 0.0325,
            0.685,
            str(index + 1),
            transform=ax.transAxes,
            ha="center",
            fontsize=6.2,
        )
    ax.text(
        0.50,
        0.63,
        "8 complete  |  2 right-censored",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["ink"],
    )

    classifications = _mapping(selected, "world_metric_classifications")
    ax.text(
        0.04,
        0.53,
        "world x core-metric direction class at the frozen 0.75 threshold",
        transform=ax.transAxes,
        fontsize=6.5,
        fontweight=600,
    )
    cell_index = 0
    labels = ("disc.", "retain", "draw", "term/best")
    for row_index, world in enumerate(WORLD_ORDER):
        world_classes = _mapping(classifications, str(world))
        y = 0.35 - row_index * 0.17
        ax.text(
            0.04, y + 0.045, f"world {world}", transform=ax.transAxes, fontsize=6.5, va="center"
        )
        for metric_index, (metric, label) in enumerate(zip(CORE_METRICS, labels, strict=True)):
            classification = str(world_classes[metric])
            x = 0.20 + metric_index * 0.18
            face = colors["pale_navy"] if classification == "mixed" else colors["pale_coral"]
            edge = colors["mid_gray"] if classification == "mixed" else colors["amber"]
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    0.15,
                    0.09,
                    boxstyle="round,pad=0.004,rounding_size=0.010",
                    transform=ax.transAxes,
                    facecolor=face,
                    edgecolor=edge,
                    linewidth=0.75,
                )
            )
            symbol = (
                "mixed"
                if classification == "mixed"
                else ("positive" if classification.endswith("positive") else "negative")
            )
            ax.text(
                x + 0.075,
                y + 0.057,
                label,
                transform=ax.transAxes,
                ha="center",
                fontsize=6.0,
                fontweight=600,
            )
            ax.text(
                x + 0.075,
                y + 0.022,
                symbol,
                transform=ax.transAxes,
                ha="center",
                fontsize=6.0,
                color=edge,
            )
            cell_index += 1
    if cell_index != 8:
        raise FigureSixError("expected eight world-by-core-metric classification cells")
    boundary = FancyBboxPatch(
        (0.05, 0.020),
        0.88,
        0.115,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        transform=ax.transAxes,
        facecolor=colors["pale_coral"],
        edgecolor=colors["amber"],
        linewidth=0.75,
    )
    ax.add_patch(boundary)
    ax.text(
        0.49,
        0.078,
        "6 / 8 mixed — supporting & threshold-sensitive\nnot a primary endpoint",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=5.9,
        fontweight=600,
        color=colors["ink"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 6 object."""

    figure_system = _mapping(inputs, "figure_system")
    colors = _configure(figure_system)
    canvas = _mapping(figure_system, "canvas")
    figure = plt.figure(
        figsize=(float(canvas["two_column_width"]), float(canvas["default_two_by_two_height"])),
        facecolor=colors["white"],
    )
    grid = figure.add_gridspec(
        2,
        2,
        left=0.085,
        right=0.985,
        bottom=0.09,
        top=0.965,
        wspace=0.30,
        hspace=0.43,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    pairs = cast(list[dict[str, Any]], inputs["pairs"])
    complete_pairs = cast(list[dict[str, Any]], inputs["complete_pairs"])
    selected = cast(Mapping[str, Any], inputs["selected"])
    _draw_panel_a(axes[0], pairs, colors)
    _draw_panel_b(axes[1], complete_pairs, colors)
    _draw_panel_c(axes[2], complete_pairs, colors)
    _draw_panel_d(axes[3], pairs, selected, colors)
    return figure


def _output_paths(output_dir: Path) -> dict[str, Path]:
    return {suffix: output_dir / f"{OUTPUT_STEM}.{suffix}" for suffix in ("svg", "pdf", "png")}


def render_outputs(inputs: Mapping[str, Any], output_dir: Path) -> dict[str, Path]:
    """Render deterministic editable and review formats to ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = _output_paths(output_dir)
    figure = build_figure(inputs)
    creator = "ChemWorld W1-P07 deterministic renderer"
    figure.savefig(
        paths["svg"], format="svg", facecolor="white", metadata={"Date": None, "Creator": creator}
    )
    normalized_svg = "\n".join(
        line.rstrip() for line in paths["svg"].read_text(encoding="utf-8").splitlines()
    )
    paths["svg"].write_text(normalized_svg + "\n", encoding="utf-8", newline="\n")
    figure.savefig(
        paths["pdf"],
        format="pdf",
        facecolor="white",
        metadata={
            "Title": "Fresh trajectories reveal process structure omitted by endpoints",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 6",
            "Creator": creator,
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": creator},
    )
    plt.close(figure)
    return paths


def manifest_sha256(payload: Mapping[str, Any]) -> str:
    """Return the manifest digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "manifest_sha256")


def build_manifest(
    root: Path,
    inputs: Mapping[str, Any],
    outputs: Mapping[str, Path],
) -> dict[str, Any]:
    """Build the immutable per-figure source and output manifest."""

    figure_system = _mapping(inputs, "figure_system")
    derived = _mapping(inputs, "derived")
    g2 = _mapping(inputs, "g2")
    audit = _mapping(inputs, "audit")
    release_result = _mapping(inputs, "release_result")
    release_path = cast(Path, inputs["release_path"])
    derived_path = cast(Path, inputs["derived_path"])
    audit_path = cast(Path, inputs["audit_path"])
    policy_path = cast(Path, inputs["policy_path"])
    canonical_paths = _output_paths(root / OUTPUT_DIR)
    png_width, png_height = _png_dimensions(outputs["png"])
    output_rows: list[dict[str, Any]] = []
    for suffix in ("svg", "pdf", "png"):
        path = outputs[suffix]
        row: dict[str, Any] = {
            "format": suffix,
            "path": canonical_paths[suffix].relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        if suffix == "png":
            row.update({"pixel_width": png_width, "pixel_height": png_height, "dpi": 300})
        output_rows.append(row)
    source_paths = (
        (CURRENT_PATH, "current_surface_registry"),
        (release_path, "current_release_entrypoint"),
        (derived_path, "frozen_derived_data"),
        (audit_path, "formal_terminal_and_censoring_accounting"),
        (policy_path, "outcome_blind_interpretation_policy"),
        (FIGURE_SYSTEM_PATH, "visual_contract"),
        (SHARED_STYLE_HELPER_PATH, "frozen_visual_style_helper"),
        (SCRIPT_PATH, "deterministic_renderer"),
    )
    manifest: dict[str, Any] = {
        "schema_id": "chemworld.work_i_figure_manifest",
        "schema_version": "0.1.0",
        "manifest_id": "work-i-figure-6-fresh-trajectories-v0.1",
        "status": "frozen_render",
        "figure_id": "F6",
        "owner_task": "W1-P07",
        "title": "Fresh trajectories reveal process structure omitted by endpoints",
        "figure_system_sha256": figure_system["system_sha256"],
        "derived_data_sha256": derived["derived_data_sha256"],
        "g2_v0_5_audit_sha256": g2["audit_sha256"],
        "terminal_accounting_audit_sha256": audit["audit_sha256"],
        "release_result_manifest_sha256": release_result["manifest_sha256"],
        "source_bindings": [
            {"path": path.as_posix(), "role": role, "sha256": _file_sha256(root / path)}
            for path, role in source_paths
        ],
        "evidence_census": {
            "selected_worlds": 2,
            "fresh_replicates_per_world": 5,
            "planned_matched_pairs": 10,
            "complete_matched_pairs": 8,
            "right_censored_pairs": 2,
            "planned_cells": 20,
            "completed_cells": 18,
            "right_censored_cells": 2,
            "planned_vessel_opportunities": 120,
            "executed_vessels": 114,
            "completed_final_assays": 112,
            "accepted_primitive_operations": 1615,
            "best_vs_raw_terminal_sign_discordant_pairs": 2,
            "world_by_core_metric_classifications": 8,
            "mixed_world_by_core_metric_classifications": 6,
        },
        "panel_roles": {
            "A": "fresh_session_matched_design_and_coverage",
            "B": "best_versus_raw_terminal_contrasts_and_two_of_eight_endpoint_diagnostic",
            "C": "discovery_retention_drawdown_recovery_and_terminal_to_best_contrasts",
            "D": "right_censoring_and_threshold_sensitive_six_of_eight_supporting_classification",
        },
        "rendering": {
            "width_inches": 7.08,
            "height_inches": 5.2,
            "background": "opaque_white",
            "svg_text_editable": True,
            "pdf_fonttype": 42,
            "png_dpi": 300,
            "deterministic_metadata": True,
        },
        "outputs": output_rows,
        "claim_boundary": {
            "analysis_unit": "fixed physical world by fresh trajectory replicate",
            "selected_worlds_are_development_selected": True,
            "fresh_trajectories_are_descriptive": True,
            "development_trajectory_included": False,
            "provider_sampling_seed_controlled": False,
            "general_world_effect_allowed": False,
            "right_censored_pairs_retained": True,
            "two_of_eight_endpoint_result_is_diagnostic": True,
            "six_of_eight_mixed_result_is_supporting_threshold_sensitive": True,
            "population_level_material_information_claim": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "Fresh trajectories reveal process structure" in svg:
        raise FigureSixError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureSixError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureSixError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p07-") as temporary:
            temporary_dir = Path(temporary)
            outputs = render_outputs(inputs, temporary_dir)
            _validate_rendered_outputs(outputs)
            manifest = build_manifest(ROOT, inputs, outputs)
            for suffix, temporary_path in outputs.items():
                committed_path = ROOT / OUTPUT_DIR / f"{OUTPUT_STEM}.{suffix}"
                if temporary_path.read_bytes() != committed_path.read_bytes():
                    raise SystemExit(f"committed {suffix} differs from deterministic rebuild")
            if _json_text(manifest) != (ROOT / MANIFEST_PATH).read_text(encoding="utf-8"):
                raise SystemExit("committed manifest differs from deterministic rebuild")
    else:
        output_dir = ROOT / OUTPUT_DIR
        outputs = render_outputs(inputs, output_dir)
        _validate_rendered_outputs(outputs)
        manifest = build_manifest(ROOT, inputs, outputs)
        (ROOT / MANIFEST_PATH).write_text(_json_text(manifest), encoding="utf-8", newline="\n")
    payload = _read_json(ROOT / MANIFEST_PATH) if args.check else manifest
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "figure_id": payload["figure_id"],
                "manifest_sha256": payload["manifest_sha256"],
                "outputs": len(payload["outputs"]),
                "complete_pairs": payload["evidence_census"]["complete_matched_pairs"],
                "right_censored_pairs": payload["evidence_census"]["right_censored_pairs"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
