"""Render Work I Figure 5 from the current frozen G2 v0.4 lifecycle data."""

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
from itertools import pairwise
from pathlib import Path
from typing import Any, cast

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
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
SCRIPT_PATH = Path("scripts/render_work_i_figure_5.py")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-5-complete-lifecycles"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"

EXPECTED_OPERATION_SIGNATURE = (
    "add_reagent",
    "add_solvent",
    "set_potential",
    "electrolyze",
    "measure",
    "terminate",
    "measure",
)
OPERATION_LABELS = (
    "add\nreagent",
    "add\nsolvent",
    "set\npotential",
    "electrolyze",
    "UV-vis\nmeasure",
    "terminate",
    "final\nassay",
)


class FigureFiveError(RuntimeError):
    """Raised when a current frozen input or rendered Figure 5 fails closed."""


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("system_sha256") != _canonical_sha256(payload, "system_sha256"):
        raise FigureFiveError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureFiveError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureFiveError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureFiveError(f"stale P01 source binding: {path_value}")
    matches = [row for row in _mapping_rows(payload, "figures") if row.get("figure_id") == "F5"]
    if len(matches) != 1:
        raise FigureFiveError("P01 must define exactly one F5")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P06"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
        or spec.get("pending_result_panels") != []
    ):
        raise FigureFiveError("P01 F5 assignment differs from W1-P06")
    if [row.get("panel") for row in _mapping_rows(spec, "panels")] != list("ABCD"):
        raise FigureFiveError("P01 F5 panel order must be A-D")
    return spec


def _validate_ledger_source(
    root: Path,
    binding: Mapping[str, Any],
    expected_path: Path,
) -> dict[str, Any]:
    if binding.get("path") != expected_path.as_posix():
        raise FigureFiveError("current ledger differs from the frozen derived-data source")
    # The coordinator ledger is append-only across later Work I handoffs, so its
    # whole-file hashes legitimately differ from the D03 snapshot. Validate the
    # current G2 v0.4 layer against the frozen derived-data audit below instead of
    # requiring unrelated later ledger sections to reproduce the older bytes.
    ledger = _read_json(root / expected_path)
    return ledger


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Resolve current.json and validate the frozen G2 v0.4 lifecycle inputs."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)
    current = _read_json(resolved / CURRENT_PATH)
    publication = _mapping(current, "publication")
    release_value = publication.get("release_manifest")
    ledger_value = publication.get("experiment_ledger")
    if not isinstance(release_value, str) or not isinstance(ledger_value, str):
        raise FigureFiveError("configs/current.json lacks publication release or ledger paths")
    release_path = Path(release_value)
    ledger_path = Path(ledger_value)
    release = _read_json(resolved / release_path)
    evidence = _mapping(release, "evidence")
    derived_binding = _mapping(evidence, "frozen_derived_data")
    derived_value = derived_binding.get("path")
    compact_report_value = evidence.get("g2_v0_4_compact_report")
    if not isinstance(derived_value, str) or not isinstance(compact_report_value, str):
        raise FigureFiveError("current release lacks G2 v0.4 evidence paths")
    derived_path = Path(derived_value)
    compact_report_path = Path(compact_report_value)
    if not (resolved / compact_report_path).is_file():
        raise FigureFiveError("current compact G2 v0.4 report is missing")
    derived = _read_json(resolved / derived_path)
    if (
        derived_binding.get("status") != "frozen_complete"
        or derived.get("status") != "frozen_complete"
        or derived.get("derived_data_sha256") != _canonical_sha256(derived, "derived_data_sha256")
        or derived.get("derived_data_sha256") != derived_binding.get("derived_data_sha256")
    ):
        raise FigureFiveError("current frozen derived-data binding is stale")

    sources = _mapping(derived, "sources")
    ledger_binding = _mapping(sources, "experiment_ledger")
    ledger = _validate_ledger_source(resolved, ledger_binding, ledger_path)
    experiment_layers = _mapping(ledger, "experiment_layers")
    ledger_g2 = _mapping(experiment_layers, "g2_v0_4_autonomous_development")

    g2 = _mapping(derived, "g2_v0_4")
    cell_rows = [dict(row) for row in _mapping_rows(g2, "cell_rows")]
    demonstration = _mapping(g2, "one_experiment_demonstration")
    receipt = _mapping(demonstration, "campaign_resource_endpoints")
    if (
        len(cell_rows) != 10
        or g2.get("audit_sha256") != evidence.get("g2_v0_4_audit_sha256")
        or g2.get("audit_sha256") != ledger_g2.get("audit_sha256")
        or tuple(demonstration.get("operation_signature", ())) != EXPECTED_OPERATION_SIGNATURE
        or demonstration.get("operation_count") != 7
        or demonstration.get("arm") != "opaque"
        or demonstration.get("cell_id") != "cell-01"
        or demonstration.get("world_seed") != 0
        or demonstration.get("label")
        != "development demonstration; excluded from prior-effect inference"
    ):
        raise FigureFiveError("frozen G2 v0.4 demonstration identity changed")

    if (
        receipt.get("verified") is not True
        or receipt.get("trajectory_event_alignment_verified") is not True
        or receipt.get("expected_batches") != 6
        or receipt.get("closed_batches") != 6
        or receipt.get("final_assays") != 6
        or receipt.get("discarded_batches") != 0
        or receipt.get("operation_attempts") != 69
        or receipt.get("nonfinal_instrument_uses") != 17
        or receipt.get("vessel_starts") != 6
        or receipt.get("right_censored") is not False
    ):
        raise FigureFiveError("frozen example campaign receipt changed")
    report_only = _mapping(receipt, "report_only")
    stocks_used = _mapping(receipt, "stocks_used")
    if (
        report_only.get("physical_cost") is None
        or report_only.get("process_time_s") is None
        or report_only.get("sample_consumed_L") is None
        or stocks_used.get("reagent_mol") is None
        or stocks_used.get("solvent_L") is None
    ):
        raise FigureFiveError("example campaign receipt units are incomplete")

    cell_keys: set[tuple[int, str]] = set()
    for row in cell_rows:
        seed = row.get("world_seed")
        arm = row.get("arm")
        if not isinstance(seed, int) or arm not in ("opaque", "nominal"):
            raise FigureFiveError("invalid G2 v0.4 cell identity")
        cell_keys.add((seed, str(arm)))
        if row.get("completed_vessels") != 6 or len(row.get("final_score_sequence", [])) != 6:
            raise FigureFiveError("G2 v0.4 cell does not contain six closed vessels")
    if cell_keys != {(seed, arm) for seed in range(5) for arm in ("opaque", "nominal")}:
        raise FigureFiveError("G2 v0.4 5-by-2 cell balance changed")

    totals = {
        "closed_lifecycles": sum(int(row["completed_vessels"]) for row in cell_rows),
        "operation_attempts": sum(int(row["operation_count"]) for row in cell_rows),
        "nonfinal_measurements": sum(int(row["nonfinal_measurement_count"]) for row in cell_rows),
        "invalid_operations": sum(int(row["invalid_operation_count"]) for row in cell_rows),
    }
    if totals != {
        "closed_lifecycles": 60,
        "operation_attempts": 815,
        "nonfinal_measurements": 164,
        "invalid_operations": 0,
    }:
        raise FigureFiveError("G2 v0.4 aggregate lifecycle accounting changed")
    if (
        ledger_g2.get("worlds") != 5
        or ledger_g2.get("arms") != 2
        or ledger_g2.get("cells") != 10
        or ledger_g2.get("vessels_per_cell") != 6
        or ledger_g2.get("completed_physical_experiments") != 60
        or ledger_g2.get("final_assays") != 60
        or ledger_g2.get("accepted_primitive_operations") != 815
        or ledger_g2.get("nonfinal_instrument_measurements") != 164
        or ledger_g2.get("invalid_or_resource_rejected_operations") != 0
        or ledger_g2.get("provider_sessions") != 60
        or ledger_g2.get("all_cells_complete") is not True
        or ledger_g2.get("all_exact_replays_verified") is not True
        or ledger_g2.get("all_pairs_physically_matched") is not True
    ):
        raise FigureFiveError("experiment-ledger G2 v0.4 gates changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "current": current,
        "release": release,
        "release_path": release_path,
        "derived": derived,
        "derived_path": derived_path,
        "compact_report_path": compact_report_path,
        "ledger": ledger,
        "ledger_path": ledger_path,
        "ledger_binding": ledger_binding,
        "ledger_g2": ledger_g2,
        "g2": g2,
        "cell_rows": cell_rows,
        "demonstration": demonstration,
        "receipt": receipt,
        "totals": totals,
    }


def _configure(figure_system: Mapping[str, Any]) -> dict[str, str]:
    colors = _configure_matplotlib(figure_system)
    mpl.rcParams["svg.hashsalt"] = "chemworld-work-i-figure-5-v0.1"
    return colors


def _node(
    ax: Any,
    center: tuple[float, float],
    text: str,
    colors: Mapping[str, str],
    role: str,
) -> None:
    x, y = center
    face = {
        "operation": colors["pale_navy"],
        "measurement": colors["white"],
        "terminal": colors["white"],
    }[role]
    edge = {
        "operation": colors["navy"],
        "measurement": colors["amber"],
        "terminal": colors["teal"],
    }[role]
    patch = FancyBboxPatch(
        (x - 0.075, y - 0.075),
        0.15,
        0.15,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        transform=ax.transAxes,
        facecolor=face,
        edgecolor=edge,
        linewidth=0.9,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["ink"],
    )


def _arrow(
    ax: Any,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    half_extent = 0.085
    if abs(dx) >= abs(dy):
        direction = 1.0 if dx > 0 else -1.0
        start = (start[0] + direction * half_extent, start[1])
        end = (end[0] - direction * half_extent, end[1])
    else:
        direction = 1.0 if dy > 0 else -1.0
        start = (start[0], start[1] + direction * half_extent)
        end = (end[0], end[1] - direction * half_extent)
    arrow = FancyArrowPatch(
        start,
        end,
        transform=ax.transAxes,
        arrowstyle="-|>",
        mutation_scale=7,
        linewidth=0.75,
        color=color,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(arrow)


def _draw_panel_a(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "A", "One vessel exposes seven primitive operations", colors)
    ax.set_axis_off()
    centers = (
        (0.12, 0.67),
        (0.36, 0.67),
        (0.60, 0.67),
        (0.84, 0.67),
        (0.84, 0.30),
        (0.54, 0.30),
        (0.22, 0.30),
    )
    roles = (
        "operation",
        "operation",
        "operation",
        "operation",
        "measurement",
        "terminal",
        "measurement",
    )
    for index, (start, end) in enumerate(pairwise(centers)):
        _arrow(ax, start, end, colors["amber"] if index == 4 else colors["grid_gray"])
    for index, (center, label, role) in enumerate(
        zip(centers, OPERATION_LABELS, roles, strict=True), start=1
    ):
        _node(ax, center, label, colors, role)
        ax.text(
            center[0] - 0.07,
            center[1] + 0.10,
            str(index),
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.5,
            fontweight=600,
            color=colors["mid_gray"],
        )
    ax.text(
        0.69,
        0.48,
        "observation becomes public\nbefore the next decision",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.1,
        color=colors["amber"],
        bbox={
            "boxstyle": "round,pad=0.12",
            "facecolor": colors["white"],
            "edgecolor": "none",
        },
    )
    ax.text(
        0.03,
        0.08,
        "cell-01 · opaque · world seed 0 · descriptive example only",
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def _draw_panel_b(
    ax: Any,
    receipt: Mapping[str, Any],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "B", "Campaign receipts preserve units and denominators", colors)
    ax.set_axis_off()
    report_only = _mapping(receipt, "report_only")
    stocks = _mapping(receipt, "stocks_used")
    rows = (
        ("closure", "6 vessels · 6 closed · 6 final assays · 0 discards"),
        ("actions", "69 operation attempts · 17 non-final measurements"),
        (
            "stocks",
            f"{float(stocks['reagent_mol']):.2f} mol reagent · "
            f"{float(stocks['solvent_L']):.2f} L solvent",
        ),
        (
            "physical",
            f"{float(report_only['physical_cost']):.3f} cost · "
            f"{float(report_only['process_time_s']) / 3600:.1f} h · "
            f"{1000 * float(report_only['sample_consumed_L']):.2f} mL sample",
        ),
    )
    for index, (label, value) in enumerate(rows):
        y = 0.74 - index * 0.18
        patch = FancyBboxPatch(
            (0.04, y - 0.065),
            0.92,
            0.13,
            boxstyle="round,pad=0.008,rounding_size=0.014",
            transform=ax.transAxes,
            facecolor=colors["pale_navy"] if index % 2 == 0 else colors["white"],
            edgecolor=colors["grid_gray"],
            linewidth=0.65,
        )
        ax.add_patch(patch)
        ax.text(
            0.065,
            y,
            label,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.5,
            fontweight=600,
            color=colors["ink"],
        )
        ax.text(
            0.24,
            y,
            value,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.0,
            color=colors["ink"],
        )
    ax.text(
        0.50,
        0.065,
        "trajectory-event alignment verified · immutable receipt hashes bound",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def _draw_panel_c(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "C", "Identity, resources and replay stay external", colors)
    ax.set_axis_off()
    controls = (
        ("campaign identity", "cell · arm\nworld · vessel"),
        ("resource authority", "card SHA-256\nledger SHA-256"),
        ("event alignment", "trajectory ↔ receipt\nverified"),
        ("exact replay", "60/60 lifecycles\n10/10 paired cells"),
    )
    for index, (title, detail) in enumerate(controls):
        column = index % 2
        row = index // 2
        x = 0.08 + column * 0.46
        y = 0.70 - row * 0.34
        patch = FancyBboxPatch(
            (x, y - 0.11),
            0.38,
            0.22,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            transform=ax.transAxes,
            facecolor=colors["white"],
            edgecolor=colors["purple"],
            linewidth=0.85,
        )
        ax.add_patch(patch)
        ax.scatter(
            [x + 0.05],
            [y + 0.035],
            transform=ax.transAxes,
            marker="s",
            s=31,
            facecolor=colors["purple"],
            edgecolor=colors["white"],
            linewidth=0.45,
        )
        ax.text(
            x + 0.10,
            y + 0.045,
            title,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.5,
            fontweight=600,
            color=colors["ink"],
        )
        ax.text(
            x + 0.19,
            y - 0.045,
            detail,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.5,
            color=colors["mid_gray"],
        )
    ax.text(
        0.50,
        0.08,
        "The ledger is not prompt context; it is the auditable measurement spine",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["ink"],
    )


def _draw_panel_d(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "D", "Closure and failure accounting are explicit", colors)
    ax.set_axis_off()
    rows = (
        ("closed lifecycles", "60 / 60", colors["teal"]),
        ("final assays", "60", colors["teal"]),
        ("invalid or rejected", "0", colors["mid_gray"]),
        ("right-censored", "0", colors["mid_gray"]),
    )
    for index, (label, value, color) in enumerate(rows):
        y = 0.73 - index * 0.15
        ax.text(
            0.10,
            y,
            label,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.5,
            color=colors["ink"],
        )
        ax.text(
            0.88,
            y,
            value,
            transform=ax.transAxes,
            ha="right",
            va="center",
            fontsize=9.0,
            fontweight=700,
            color=color,
        )
        ax.plot(
            [0.10, 0.88],
            [y - 0.065, y - 0.065],
            transform=ax.transAxes,
            color=colors["grid_gray"],
            linewidth=0.35,
        )
    boundary = FancyBboxPatch(
        (0.07, 0.075),
        0.86,
        0.13,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes,
        facecolor=colors["pale_navy"],
        edgecolor=colors["grid_gray"],
        linewidth=0.65,
    )
    ax.add_patch(boundary)
    ax.text(
        0.50,
        0.155,
        "815 accepted operations · 164 non-final measurements",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight=600,
        color=colors["ink"],
    )
    ax.text(
        0.50,
        0.105,
        "repeated events, not independent sample units",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 5 object."""

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
        left=0.06,
        right=0.985,
        bottom=0.085,
        top=0.965,
        wspace=0.27,
        hspace=0.42,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    receipt = cast(Mapping[str, Any], inputs["receipt"])
    _draw_panel_a(axes[0], colors)
    _draw_panel_b(axes[1], receipt, colors)
    _draw_panel_c(axes[2], colors)
    _draw_panel_d(axes[3], colors)
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
        metadata={"Date": None, "Creator": "ChemWorld W1-P06 deterministic renderer"},
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
            "Title": "Primitive-control agents expose complete experimental lifecycles",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 5",
            "Creator": "ChemWorld W1-P06 deterministic renderer",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": "ChemWorld W1-P06 deterministic renderer"},
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
    receipt = _mapping(inputs, "receipt")
    release_path = cast(Path, inputs["release_path"])
    derived_path = cast(Path, inputs["derived_path"])
    compact_report_path = cast(Path, inputs["compact_report_path"])
    ledger_path = cast(Path, inputs["ledger_path"])
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
        "manifest_id": "work-i-figure-5-autonomous-lifecycle-v0.1",
        "status": "frozen_render",
        "figure_id": "F5",
        "owner_task": "W1-P06",
        "title": "Primitive-control agents expose complete experimental lifecycles",
        "figure_system_sha256": figure_system["system_sha256"],
        "derived_data_sha256": derived["derived_data_sha256"],
        "g2_v0_4_audit_sha256": g2["audit_sha256"],
        "example_resource_card_sha256": receipt["card_sha256"],
        "example_ledger_sha256": receipt["ledger_sha256"],
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
                "path": ledger_path.as_posix(),
                "role": "immutable_experiment_accounting",
                "sha256": _file_sha256(root / ledger_path),
            },
            {
                "path": compact_report_path.as_posix(),
                "role": "tracked_compact_lifecycle_report",
                "sha256": _file_sha256(root / compact_report_path),
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
            "worlds": 5,
            "information_arms": 2,
            "campaign_cells": 10,
            "closed_lifecycles": 60,
            "final_assays": 60,
            "explicit_discards": 0,
            "accepted_primitive_operations": 815,
            "nonfinal_measurements": 164,
            "invalid_or_rejected_operations": 0,
            "provider_sessions": 60,
            "right_censored_lifecycles": 0,
            "example_operation_count": 7,
        },
        "panel_roles": {
            "A": "one_seven_operation_lifecycle_with_observation_before_next_decision",
            "B": "campaign_resource_receipt_with_units_and_denominators",
            "C": "identity_resource_event_alignment_and_exact_replay_controls",
            "D": "failure_and_closure_accounting_without_event_level_pseudoreplication",
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
            "primitive_control_lifecycle_demonstration": True,
            "example_is_descriptive": True,
            "prior_effect_inference_from_example": False,
            "operations_as_independent_samples": False,
            "fixed_step_parameter_filling": False,
            "complete_system_model_only_attribution": False,
            "real_laboratory_generalization": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "Primitive-control agents expose" in svg:
        raise FigureFiveError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureFiveError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureFiveError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p06-") as temporary:
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
                "closed_lifecycles": manifest_payload["evidence_census"]["closed_lifecycles"],
                "accepted_operations": manifest_payload["evidence_census"][
                    "accepted_primitive_operations"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
