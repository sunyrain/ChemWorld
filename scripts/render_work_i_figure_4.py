"""Render Work I Figure 4 from the current frozen G0 compiled-control data."""

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
from matplotlib.patches import FancyBboxPatch
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
SCRIPT_PATH = Path("scripts/render_work_i_figure_4.py")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-4-compiled-controls"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"

TASK_ORDER = ("electrochemical-conversion", "reaction-to-crystallization")
TASK_LABELS = {
    "electrochemical-conversion": "electrochemical",
    "reaction-to-crystallization": "crystallization",
}
TASK_MARKERS = {
    "electrochemical-conversion": "o",
    "reaction-to-crystallization": "s",
}
TASK_LINESTYLES = {
    "electrochemical-conversion": "-",
    "reaction-to-crystallization": "--",
}
ARM_ORDER = ("opaque", "nominal", "misindexed")
ARM_LABELS = {"opaque": "opaque", "nominal": "nominal", "misindexed": "misindexed"}
PREDICTION_METRICS = ("heldout_directional_accuracy", "heldout_brier_score")
EPISTEMIC_METRICS = (
    "declared_directional_accuracy",
    "mechanism_tag_f1",
    "structural_edge_f1",
    "unsupported_claim_rate",
)
GATE_ORDER = (
    "manipulation_check_passed",
    "differential_action_correction_passed",
    "performance_recovery_to_opaque_passed",
    "overall_recovery_claim_passed",
)


class FigureFourError(RuntimeError):
    """Raised when a current frozen input or rendered Figure 4 fails closed."""


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("system_sha256") != _canonical_sha256(payload, "system_sha256"):
        raise FigureFourError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureFourError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureFourError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureFourError(f"stale P01 source binding: {path_value}")
    matches = [row for row in _mapping_rows(payload, "figures") if row.get("figure_id") == "F4"]
    if len(matches) != 1:
        raise FigureFourError("P01 must define exactly one F4")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P05"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
        or spec.get("pending_result_panels") != []
    ):
        raise FigureFourError("P01 F4 assignment differs from W1-P05")
    if [row.get("panel") for row in _mapping_rows(spec, "panels")] != list("ABCD"):
        raise FigureFourError("P01 F4 panel order must be A-D")
    return spec


def _validate_frozen_source(root: Path, binding: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    path_value = binding.get("path")
    file_sha256 = binding.get("file_sha256")
    canonical_sha256 = binding.get("canonical_json_sha256")
    if not all(isinstance(value, str) for value in (path_value, file_sha256, canonical_sha256)):
        raise FigureFourError("invalid frozen derived-data source binding")
    path = root / str(path_value)
    actual_file_sha256 = _file_sha256(path)
    payload = _read_json(path)
    if _canonical_sha256(payload, "__no_embedded_hash__") != canonical_sha256:
        raise FigureFourError(f"canonical source hash mismatch: {path_value}")
    return payload, actual_file_sha256


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Resolve current.json and validate the frozen G0 release inputs."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)
    current = _read_json(resolved / CURRENT_PATH)
    publication = _mapping(current, "publication")
    release_path_value = publication.get("release_manifest")
    if not isinstance(release_path_value, str):
        raise FigureFourError("configs/current.json lacks publication.release_manifest")
    release_path = Path(release_path_value)
    release = _read_json(resolved / release_path)
    evidence = _mapping(release, "evidence")
    derived_binding = _mapping(evidence, "frozen_derived_data")
    derived_path_value = derived_binding.get("path")
    if not isinstance(derived_path_value, str):
        raise FigureFourError("current release lacks the frozen derived-data path")
    derived_path = Path(derived_path_value)
    derived = _read_json(resolved / derived_path)
    if (
        derived_binding.get("status") != "frozen_complete"
        or derived.get("status") != "frozen_complete"
        or derived.get("derived_data_sha256") != _canonical_sha256(derived, "derived_data_sha256")
        or derived.get("derived_data_sha256") != derived_binding.get("derived_data_sha256")
    ):
        raise FigureFourError("current frozen derived-data binding is stale")

    static = _mapping(current, "static_scientific_optimization")
    triarm = _mapping(current, "static_material_information_three_arm")
    if (
        static.get("formal_result") is not True
        or static.get("benchmark_claim_allowed") is not False
        or triarm.get("formal_result") is not True
        or triarm.get("confirmatory_analysis_complete") is not True
        or triarm.get("benchmark_claim_allowed") is not False
        or triarm.get("total_physical_experiments") != 2280
        or triarm.get("world_seeds") != list(range(10))
    ):
        raise FigureFourError("current G0 status or counting boundary changed")

    sources = _mapping(derived, "sources")
    g0_v1_0_binding = _mapping(sources, "g0_v1_0")
    g0_v1_2_binding = _mapping(sources, "g0_v1_2")
    g0_v1_0, g0_v1_0_actual_file_sha256 = _validate_frozen_source(resolved, g0_v1_0_binding)
    g0_v1_2, g0_v1_2_actual_file_sha256 = _validate_frozen_source(resolved, g0_v1_2_binding)
    if (
        static.get("summary") != g0_v1_0_binding.get("path")
        or triarm.get("summary") != g0_v1_2_binding.get("path")
        or g0_v1_0.get("formal_result") is not True
        or g0_v1_0.get("benchmark_claim_allowed") is not False
        or g0_v1_2.get("formal_result") is not True
        or g0_v1_2.get("confirmatory_analysis_complete") is not True
        or g0_v1_2.get("benchmark_claim_allowed") is not False
    ):
        raise FigureFourError("current G0 source authority changed")

    g0 = _mapping(derived, "g0")
    task_arm_rows = [dict(row) for row in _mapping_rows(g0, "task_arm_rows")]
    world_arm_rows = [dict(row) for row in _mapping_rows(g0, "world_arm_rows")]
    if len(task_arm_rows) != 8 or len(world_arm_rows) != 60:
        raise FigureFourError("frozen G0 row counts changed")
    arm_profiles: dict[tuple[str, str], dict[str, Any]] = {}
    contrasts: dict[str, dict[str, Any]] = {}
    for row in task_arm_rows:
        task_id = row.get("task_id")
        arm = row.get("arm")
        if task_id not in TASK_ORDER or not isinstance(arm, str):
            raise FigureFourError("unexpected task or arm in G0 task-arm rows")
        if arm == "derived_contrasts":
            if task_id in contrasts:
                raise FigureFourError(f"duplicate derived contrast for {task_id}")
            contrasts[str(task_id)] = row
            continue
        if arm not in ARM_ORDER:
            raise FigureFourError(f"unexpected G0 information arm: {arm}")
        key = (str(task_id), arm)
        if key in arm_profiles:
            raise FigureFourError(f"duplicate G0 task-arm profile: {key}")
        arm_profiles[key] = row
    expected_profiles = {(task_id, arm) for task_id in TASK_ORDER for arm in ARM_ORDER}
    if set(arm_profiles) != expected_profiles or set(contrasts) != set(TASK_ORDER):
        raise FigureFourError("G0 task-arm profile balance changed")

    world_keys: set[tuple[str, str, int]] = set()
    for row in world_arm_rows:
        task_id = row.get("task_id")
        arm = row.get("arm")
        seed = row.get("world_seed")
        if task_id not in TASK_ORDER or arm not in ARM_ORDER or not isinstance(seed, int):
            raise FigureFourError("invalid G0 world-arm identity")
        world_keys.add((str(task_id), str(arm), seed))
    expected_world_keys = {
        (task_id, arm, seed) for task_id in TASK_ORDER for arm in ARM_ORDER for seed in range(10)
    }
    if world_keys != expected_world_keys:
        raise FigureFourError("G0 2-by-3-by-10 world-arm balance changed")

    for task_id in TASK_ORDER:
        opaque = arm_profiles[(task_id, "opaque")]
        if any(opaque.get(metric) is None for metric in EPISTEMIC_METRICS):
            raise FigureFourError(f"opaque epistemic readouts incomplete for {task_id}")
        for arm in ARM_ORDER:
            row = arm_profiles[(task_id, arm)]
            if (
                row.get("world_count") != 10
                or row.get("primary_score_mean") is None
                or row.get("primary_score_sd") is None
                or any(row.get(metric) is None for metric in PREDICTION_METRICS)
            ):
                raise FigureFourError(f"incomplete outcome/prediction profile for {task_id}/{arm}")
        gate_row = contrasts[task_id]
        if any(not isinstance(gate_row.get(gate), bool) for gate in GATE_ORDER):
            raise FigureFourError(f"invalid component gate profile for {task_id}")
    if contrasts["electrochemical-conversion"]["overall_recovery_claim_passed"] is not False:
        raise FigureFourError("electrochemical overall recovery gate changed")
    if contrasts["reaction-to-crystallization"]["overall_recovery_claim_passed"] is not False:
        raise FigureFourError("crystallization overall recovery gate changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "current": current,
        "release": release,
        "release_path": release_path,
        "derived": derived,
        "derived_path": derived_path,
        "g0_v1_0_binding": g0_v1_0_binding,
        "g0_v1_2_binding": g0_v1_2_binding,
        "g0_v1_0_actual_file_sha256": g0_v1_0_actual_file_sha256,
        "g0_v1_2_actual_file_sha256": g0_v1_2_actual_file_sha256,
        "arm_profiles": arm_profiles,
        "contrasts": contrasts,
        "world_arm_rows": world_arm_rows,
    }


def _configure(figure_system: Mapping[str, Any]) -> dict[str, str]:
    colors = _configure_matplotlib(figure_system)
    mpl.rcParams["svg.hashsalt"] = "chemworld-work-i-figure-4-v0.1"
    return colors


def _arm_colors(colors: Mapping[str, str]) -> dict[str, str]:
    return {
        "opaque": colors["navy"],
        "nominal": colors["coral"],
        "misindexed": colors["purple"],
    }


def _draw_panel_a(
    ax: Any,
    profiles: Mapping[tuple[str, str], Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "A", "Outcomes change by task and information", colors)
    arm_colors = _arm_colors(colors)
    x = np.arange(len(ARM_ORDER), dtype=float)
    offsets = {
        "electrochemical-conversion": -0.07,
        "reaction-to-crystallization": 0.07,
    }
    for task_id in TASK_ORDER:
        means = np.array(
            [float(profiles[(task_id, arm)]["primary_score_mean"]) for arm in ARM_ORDER]
        )
        errors = np.array(
            [float(profiles[(task_id, arm)]["primary_score_sd"]) for arm in ARM_ORDER]
        )
        task_x = x + offsets[task_id]
        ax.plot(
            task_x,
            means,
            color=colors["ink"],
            linestyle=TASK_LINESTYLES[task_id],
            linewidth=0.75,
            zorder=1,
        )
        for index, arm in enumerate(ARM_ORDER):
            ax.errorbar(
                [task_x[index]],
                [means[index]],
                yerr=[errors[index]],
                fmt=TASK_MARKERS[task_id],
                markersize=5.0,
                color=arm_colors[arm],
                markerfacecolor=colors["white"] if task_id == TASK_ORDER[0] else arm_colors[arm],
                markeredgewidth=0.9,
                capsize=2.0,
                elinewidth=0.65,
                zorder=3,
            )
        ax.text(
            task_x[-1] + 0.10,
            means[-1] + (0.02 if task_id == TASK_ORDER[0] else -0.015),
            TASK_LABELS[task_id],
            ha="left",
            va="center",
            fontsize=6.5,
            color=colors["ink"],
        )
    ax.set_xlim(-0.35, 2.55)
    ax.set_ylim(0.38, 0.90)
    ax.set_xticks(x, [ARM_LABELS[arm] for arm in ARM_ORDER])
    ax.set_ylabel("validated final score (mean ± SD)")
    ax.grid(axis="y", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    ax.text(
        0.02,
        0.04,
        "10 worlds per task-arm",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def _draw_panel_b(
    ax: Any,
    profiles: Mapping[tuple[str, str], Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "B", "Prediction and calibration stay separate", colors)
    arm_colors = _arm_colors(colors)
    metric_x = np.array([0.0, 1.0])
    arm_offsets = {"opaque": -0.13, "nominal": 0.0, "misindexed": 0.13}
    for task_id in TASK_ORDER:
        for arm in ARM_ORDER:
            values = [float(profiles[(task_id, arm)][metric]) for metric in PREDICTION_METRICS]
            x = metric_x + arm_offsets[arm]
            ax.scatter(
                x,
                values,
                marker=TASK_MARKERS[task_id],
                s=33,
                facecolor=(
                    colors["white"] if task_id == "electrochemical-conversion" else arm_colors[arm]
                ),
                edgecolor=arm_colors[arm],
                linewidth=0.9,
                zorder=3,
            )
    ax.set_xlim(-0.34, 1.34)
    ax.set_ylim(0.08, 0.86)
    ax.set_xticks(metric_x, ["directional accuracy ↑", "Brier score ↓"])
    ax.set_ylabel("raw held-out metric")
    ax.grid(axis="y", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    ax.text(
        0.50,
        0.96,
        "within each metric: opaque  |  nominal  |  misindexed",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.5,
        color=colors["mid_gray"],
    )
    ax.legend(
        handles=[
            Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markerfacecolor=colors["white"],
                markeredgecolor=colors["ink"],
                label="electrochemical",
            ),
            Line2D(
                [],
                [],
                marker="s",
                linestyle="none",
                markerfacecolor=colors["ink"],
                markeredgecolor=colors["ink"],
                label="crystallization",
            ),
        ],
        loc="center right",
        ncol=1,
        frameon=False,
        fontsize=6.5,
        columnspacing=1.1,
    )


def _draw_panel_c(
    ax: Any,
    profiles: Mapping[tuple[str, str], Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "C", "Opaque controls separate epistemic readouts", colors)
    x = np.arange(len(EPISTEMIC_METRICS), dtype=float)
    labels = (
        "declared\ndirection ↑",
        "mechanism\ntag F1 ↑",
        "structural\nedge F1 ↑",
        "unsupported\nclaim rate ↓",
    )
    task_colors = {
        "electrochemical-conversion": colors["navy"],
        "reaction-to-crystallization": colors["mid_gray"],
    }
    for task_id in TASK_ORDER:
        row = profiles[(task_id, "opaque")]
        values = np.array([float(row[metric]) for metric in EPISTEMIC_METRICS])
        ax.plot(
            x,
            values,
            color=task_colors[task_id],
            linestyle=TASK_LINESTYLES[task_id],
            linewidth=0.9,
            marker=TASK_MARKERS[task_id],
            markersize=4.8,
            markerfacecolor=(
                colors["white"] if task_id == "electrochemical-conversion" else task_colors[task_id]
            ),
            markeredgewidth=0.85,
        )
        ax.text(
            x[-1] + 0.10,
            values[-1],
            TASK_LABELS[task_id],
            ha="left",
            va="center",
            fontsize=6.5,
            color=task_colors[task_id],
        )
    ax.set_xlim(-0.18, 3.52)
    ax.set_ylim(0.0, 0.92)
    ax.set_xticks(x, labels)
    ax.set_ylabel("raw metric (opaque arm)")
    ax.grid(axis="y", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)


def _draw_panel_d(
    ax: Any,
    contrasts: Mapping[str, Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "D", "Component gates do not collapse to a scalar score", colors)
    ax.set_axis_off()
    gate_labels = (
        "manipulation",
        "action\ncorrection",
        "performance\nrecovery",
        "overall\nrecovery",
    )
    x_positions = [0.30, 0.49, 0.68, 0.87]
    y_positions = {
        "electrochemical-conversion": 0.61,
        "reaction-to-crystallization": 0.39,
    }
    for x, label in zip(x_positions, gate_labels, strict=True):
        ax.text(
            x,
            0.79,
            label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.5,
            color=colors["ink"],
        )
    for task_id in TASK_ORDER:
        y = y_positions[task_id]
        ax.text(
            0.04,
            y,
            TASK_LABELS[task_id],
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.5,
            fontweight=600,
            color=colors["ink"],
        )
        for x, gate in zip(x_positions, GATE_ORDER, strict=True):
            passed = bool(contrasts[task_id][gate])
            if passed:
                ax.scatter(
                    [x],
                    [y],
                    transform=ax.transAxes,
                    marker="o",
                    s=64,
                    facecolor=colors["teal"],
                    edgecolor=colors["teal"],
                    linewidth=1.1,
                    clip_on=False,
                )
            else:
                ax.scatter(
                    [x],
                    [y],
                    transform=ax.transAxes,
                    marker="x",
                    s=54,
                    color=colors["mid_gray"],
                    linewidth=1.25,
                    clip_on=False,
                )
    boundary = FancyBboxPatch(
        (0.055, 0.09),
        0.89,
        0.17,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes,
        facecolor=colors["pale_navy"],
        edgecolor=colors["grid_gray"],
        linewidth=0.75,
    )
    ax.add_patch(boundary)
    ax.text(
        0.50,
        0.195,
        "Component-wise gates differ; neither overall gate passes",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight=600,
        color=colors["ink"],
    )
    ax.text(
        0.50,
        0.135,
        "No weighted sum, ranking, or capability scalar",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 4 object."""

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
        left=0.075,
        right=0.985,
        bottom=0.10,
        top=0.965,
        wspace=0.29,
        hspace=0.43,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    profiles = cast(
        Mapping[tuple[str, str], Mapping[str, Any]],
        inputs["arm_profiles"],
    )
    contrasts = cast(Mapping[str, Mapping[str, Any]], inputs["contrasts"])
    _draw_panel_a(axes[0], profiles, colors)
    _draw_panel_b(axes[1], profiles, colors)
    _draw_panel_c(axes[2], profiles, colors)
    _draw_panel_d(axes[3], contrasts, colors)
    return figure


def _output_paths(output_dir: Path) -> dict[str, Path]:
    return {suffix: output_dir / f"{OUTPUT_STEM}.{suffix}" for suffix in ("svg", "pdf", "png")}


def render_outputs(inputs: Mapping[str, Any], output_dir: Path) -> dict[str, Path]:
    """Render deterministic editable and review formats to ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = _output_paths(output_dir)
    figure = build_figure(inputs)
    figure.savefig(
        paths["svg"],
        format="svg",
        facecolor="white",
        metadata={"Date": None, "Creator": "ChemWorld W1-P05 deterministic renderer"},
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
            "Title": "Compiled controls separate outcome, prediction, calibration and claims",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 4",
            "Creator": "ChemWorld W1-P05 deterministic renderer",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": "ChemWorld W1-P05 deterministic renderer"},
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
    release_path = cast(Path, inputs["release_path"])
    derived_path = cast(Path, inputs["derived_path"])
    g0_v1_0_binding = _mapping(inputs, "g0_v1_0_binding")
    g0_v1_2_binding = _mapping(inputs, "g0_v1_2_binding")
    g0_v1_0_actual_file_sha256 = cast(str, inputs["g0_v1_0_actual_file_sha256"])
    g0_v1_2_actual_file_sha256 = cast(str, inputs["g0_v1_2_actual_file_sha256"])
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
    manifest: dict[str, Any] = {
        "schema_id": "chemworld.work_i_figure_manifest",
        "schema_version": "0.1.0",
        "manifest_id": "work-i-figure-4-compiled-controls-v0.1",
        "status": "frozen_render",
        "figure_id": "F4",
        "owner_task": "W1-P05",
        "title": "Compiled controls separate outcome, prediction, calibration and claims",
        "figure_system_sha256": figure_system["system_sha256"],
        "derived_data_sha256": derived["derived_data_sha256"],
        "source_integrity": {
            "g0_v1_0_canonical_json_matches": True,
            "g0_v1_0_declared_file_bytes_match": (
                g0_v1_0_actual_file_sha256 == g0_v1_0_binding["file_sha256"]
            ),
            "g0_v1_2_canonical_json_matches": True,
            "g0_v1_2_declared_file_bytes_match": (
                g0_v1_2_actual_file_sha256 == g0_v1_2_binding["file_sha256"]
            ),
            "byte_drift_policy": (
                "canonical JSON identity is required; actual checked-out file bytes are bound here"
            ),
        },
        "source_bindings": [
            {
                "path": CURRENT_PATH.as_posix(),
                "role": "current_surface_registry",
                "sha256": _file_sha256(root / CURRENT_PATH),
            },
            {
                "path": release_path.as_posix(),
                "role": "current_release_entrypoint",
                "sha256": _file_sha256(root / release_path),
            },
            {
                "path": derived_path.as_posix(),
                "role": "frozen_derived_data",
                "sha256": _file_sha256(root / derived_path),
            },
            {
                "path": str(g0_v1_0_binding["path"]),
                "role": "immutable_opaque_formal_summary",
                "sha256": g0_v1_0_actual_file_sha256,
                "declared_file_sha256": str(g0_v1_0_binding["file_sha256"]),
                "canonical_json_sha256": str(g0_v1_0_binding["canonical_json_sha256"]),
            },
            {
                "path": str(g0_v1_2_binding["path"]),
                "role": "immutable_three_arm_formal_summary",
                "sha256": g0_v1_2_actual_file_sha256,
                "declared_file_sha256": str(g0_v1_2_binding["file_sha256"]),
                "canonical_json_sha256": str(g0_v1_2_binding["canonical_json_sha256"]),
            },
            {
                "path": FIGURE_SYSTEM_PATH.as_posix(),
                "role": "visual_contract",
                "sha256": _file_sha256(root / FIGURE_SYSTEM_PATH),
            },
            {
                "path": SHARED_STYLE_HELPER_PATH.as_posix(),
                "role": "frozen_visual_style_helper",
                "sha256": _file_sha256(root / SHARED_STYLE_HELPER_PATH),
            },
            {
                "path": SCRIPT_PATH.as_posix(),
                "role": "deterministic_renderer",
                "sha256": _file_sha256(root / SCRIPT_PATH),
            },
        ],
        "evidence_census": {
            "compiled_tasks": 2,
            "worlds_per_task": 10,
            "information_arms": 3,
            "participant_world_arm_cells": 60,
            "participant_physical_experiments": 2280,
            "outcome_readouts": 6,
            "heldout_prediction_readouts": 6,
            "heldout_calibration_readouts": 6,
            "opaque_epistemic_profiles": 2,
            "component_gate_profiles": 2,
            "registered_scalar_composite": False,
        },
        "panel_roles": {
            "A": "task_by_information_arm_validated_outcome",
            "B": "heldout_prediction_and_calibration_as_separate_raw_metrics",
            "C": "opaque_arm_epistemic_readouts_without_imputation",
            "D": "component_gate_matrix_without_scalar_aggregation",
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
            "formal_descriptive_compiled_controls": True,
            "benchmark_claim_allowed": False,
            "llm_vs_optimizer_competition": False,
            "scalar_experimental_intelligence": False,
            "general_population_information_effect": False,
            "primitive_control_agent_result": False,
            "real_laboratory_generalization": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "Compiled controls separate outcome" in svg:
        raise FigureFourError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureFourError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureFourError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p05-") as temporary:
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
        (ROOT / MANIFEST_PATH).write_text(
            _json_text(manifest),
            encoding="utf-8",
            newline="\n",
        )
    manifest_payload = _read_json(ROOT / MANIFEST_PATH) if args.check else manifest
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "figure_id": manifest_payload["figure_id"],
                "manifest_sha256": manifest_payload["manifest_sha256"],
                "outputs": len(manifest_payload["outputs"]),
                "participant_cells": manifest_payload["evidence_census"][
                    "participant_world_arm_cells"
                ],
                "registered_scalar_composite": manifest_payload["evidence_census"][
                    "registered_scalar_composite"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
