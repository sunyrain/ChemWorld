"""Render Work I Figure 1 from the frozen apparatus and world-fork evidence."""

# Static publication contract: Python, width_mm=179.832, Arial/sans-serif,
# svg.fonttype='none', pdf.fonttype=42; exports .svg, .pdf and .png at dpi=300.

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import tempfile
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

from chemworld.eval.work_i_data_contract import (  # type: ignore[import-untyped]
    data_contract_sha256,
    validate_work_i_data_contract,
)

ROOT = Path(__file__).resolve().parents[1]
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
DATA_CONTRACT_PATH = Path("configs/benchmark/work_i_incremental_data_contract_v0.1.json")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-1-apparatus-world-forks"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"
SCRIPT_PATH = Path("scripts/render_work_i_figure_1.py")

CASE_ORDER = (
    "partition-constitutive-law-family",
    "electrochemical-material-law-counterfactual",
)
GATE_ORDER = (
    "single_target_lineage",
    "public_contract_invariance",
    "same_sequence_executability",
    "expected_response_divergence",
    "exact_replay",
    "zero_provider_calls",
)
GATE_LABELS = {
    "single_target_lineage": "single-target lineage",
    "public_contract_invariance": "public contract invariant",
    "same_sequence_executability": "same sequence executable",
    "expected_response_divergence": "expected response diverges",
    "exact_replay": "exact replay",
    "zero_provider_calls": "zero provider calls",
}


class FigureOneError(RuntimeError):
    """Raised when a frozen source or rendered output fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FigureOneError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise FigureOneError(f"JSON root must be an object: {path}")
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise FigureOneError(f"{key} must be an object")
    return value


def _mapping_rows(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(row, Mapping) for row in value):
        raise FigureOneError(f"{key} must be a list of objects")
    return value


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_sha256(payload: Mapping[str, Any], hash_field: str) -> str:
    unhashed = deepcopy(dict(payload))
    unhashed.pop(hash_field, None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _source_binding(contract: Mapping[str, Any], artifact_id: str) -> Mapping[str, Any]:
    rows = _mapping_rows(contract, "source_bindings")
    matches = [row for row in rows if row.get("artifact_id") == artifact_id]
    if len(matches) != 1:
        raise FigureOneError(f"expected one D01 binding for {artifact_id}")
    return matches[0]


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    supplied_hash = payload.get("system_sha256")
    if supplied_hash != _canonical_sha256(payload, "system_sha256"):
        raise FigureOneError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureOneError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureOneError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureOneError(f"stale P01 source binding: {path_value}")
    figures = _mapping_rows(payload, "figures")
    matches = [row for row in figures if row.get("figure_id") == "F1"]
    if len(matches) != 1:
        raise FigureOneError("P01 must define exactly one F1")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P02"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
    ):
        raise FigureOneError("P01 F1 assignment differs from W1-P02")
    panels = _mapping_rows(spec, "panels")
    if [row.get("panel") for row in panels] != list("ABCD"):
        raise FigureOneError("P01 F1 panel order must be A-D")
    return spec


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Load and validate frozen P01, D01, and F evidence for Figure 1."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)
    data_contract = _read_json(resolved / DATA_CONTRACT_PATH)
    if data_contract.get("contract_sha256") != data_contract_sha256(data_contract):
        raise FigureOneError("D01 data-contract self-hash mismatch")
    # D01 is an immutable pre-outcome interface freeze. Validate that frozen object,
    # then verify the F-specific bound files below; do not rebuild it from a later
    # coordinator ledger that legitimately accumulated post-freeze handoffs.
    contract_errors = validate_work_i_data_contract(data_contract)
    if contract_errors:
        raise FigureOneError("D01 contract validation failed: " + "; ".join(contract_errors))

    source_payloads: dict[str, dict[str, Any]] = {}
    source_bindings: dict[str, Mapping[str, Any]] = {}
    for artifact_id in ("world_fork_qualification", "world_fork_certificate"):
        binding = _source_binding(data_contract, artifact_id)
        path_value = binding.get("path")
        if not isinstance(path_value, str):
            raise FigureOneError(f"invalid source path for {artifact_id}")
        path = resolved / path_value
        if _file_sha256(path) != binding.get("file_sha256"):
            raise FigureOneError(f"file hash mismatch for {artifact_id}")
        payload = _read_json(path)
        embedded_field = binding.get("embedded_hash_field")
        if not isinstance(embedded_field, str) or payload.get(embedded_field) != binding.get(
            "embedded_sha256"
        ):
            raise FigureOneError(f"embedded hash mismatch for {artifact_id}")
        source_payloads[artifact_id] = payload
        source_bindings[artifact_id] = binding

    qualification = source_payloads["world_fork_qualification"]
    certificate = source_payloads["world_fork_certificate"]
    design = _mapping(certificate, "design")
    result = _mapping(certificate, "result")
    gate_counts = _mapping(result, "gate_pass_counts")
    if (
        qualification.get("passed") is not True
        or result.get("passed") is not True
        or design.get("parent_child_pair_count") != 6
        or design.get("trace_count") != 24
        or design.get("provider_call_count") != 0
        or qualification.get("pair_count") != 6
        or qualification.get("trace_count") != 24
        or qualification.get("provider_call_count") != 0
        or any(gate_counts.get(gate) != 6 for gate in GATE_ORDER)
    ):
        raise FigureOneError("frozen F qualification counts or gates changed")

    summaries = {str(row.get("case_id")): row for row in _mapping_rows(result, "case_summaries")}
    if set(summaries) != set(CASE_ORDER):
        raise FigureOneError("unexpected world-fork case set")
    cases: list[dict[str, Any]] = []
    for case_id in CASE_ORDER:
        row = summaries[case_id]
        expectations = _mapping_rows(row, "expectation_summaries")
        public_rows = [item for item in expectations if item.get("channel") == "public_observation"]
        physical_rows = [item for item in expectations if item.get("channel") == "physical_state"]
        if len(public_rows) != 1 or len(physical_rows) != 1:
            raise FigureOneError(f"unexpected expectation channels for {case_id}")
        public = public_rows[0]
        physical = physical_rows[0]
        cases.append(
            {
                "case_id": case_id,
                "intervention_class": row.get("intervention_class"),
                "target_component_id": row.get("target_component_id"),
                "pair_pass_count": row.get("pair_pass_count"),
                "seeds": row.get("seeds"),
                "public_expectation_id": public.get("expectation_id"),
                "public_relative_delta_min": public.get("minimum_relative_delta"),
                "public_relative_delta_max": public.get("maximum_relative_delta"),
                "physical_expectation_id": physical.get("expectation_id"),
                "physical_relative_delta_min": physical.get("minimum_relative_delta"),
                "physical_relative_delta_max": physical.get("maximum_relative_delta"),
            }
        )

    pair_rows = _mapping_rows(result, "pairs")
    public_counts = {row.get("public_component_count") for row in pair_rows}
    invariant_counts = {row.get("public_invariant_component_count") for row in pair_rows}
    if len(pair_rows) != 6 or public_counts != {9} or invariant_counts != {9}:
        raise FigureOneError("public-component invariance census changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "data_contract": data_contract,
        "qualification": qualification,
        "certificate": certificate,
        "source_bindings": source_bindings,
        "cases": cases,
        "gate_pass_counts": {gate: int(gate_counts[gate]) for gate in GATE_ORDER},
        "public_component_count": 9,
    }


def _configure_matplotlib(figure_system: Mapping[str, Any]) -> dict[str, str]:
    palette = _mapping(_mapping(figure_system, "palette"), "tokens")
    colors = {key: str(value) for key, value in palette.items()}
    # Keep reference lines subordinate to the evidence marks at final print size.
    colors["grid_gray"] = "#E3E7EC"
    typography = _mapping(figure_system, "typography")
    families = typography.get("font_family_fallback_order")
    if not isinstance(families, list) or len(families) < 2:
        raise FigureOneError("invalid P01 font family stack")
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [str(value) for value in families[:-1]],
            "font.size": 7.0,
            "axes.titlesize": 8.5,
            "axes.titleweight": 600,
            "axes.labelsize": 7.5,
            "axes.edgecolor": colors["mid_gray"],
            "axes.linewidth": 0.5,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": colors["grid_gray"],
            "grid.linewidth": 0.35,
            "grid.alpha": 0.72,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 7.0,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "chemworld-work-i-figure-1-v0.1",
        }
    )
    return colors


def _panel(ax: Any, label: str, title: str, colors: Mapping[str, str]) -> None:
    ax.text(
        -0.052,
        1.085,
        label.lower(),
        transform=ax.transAxes,
        fontsize=8.5,
        fontweight=700,
        color=colors["ink"],
        va="top",
        ha="left",
    )
    ax.set_title(
        title,
        loc="left",
        pad=6,
        color=colors["ink"],
        fontsize=8.2,
        fontweight=600,
    )


def _box(
    ax: Any,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    face: str,
    edge: str,
    text_color: str,
    fontsize: float = 7.0,
    linewidth: float = 0.75,
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        transform=ax.transAxes,
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
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
        linespacing=1.15,
    )
    return patch


def _arrow(
    ax: Any,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
    *,
    connectionstyle: str = "arc3",
    linewidth: float = 1.1,
) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "lw": linewidth,
            "shrinkA": 0,
            "shrinkB": 0,
            "connectionstyle": connectionstyle,
        },
    )


def _draw_panel_a(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "A", "The agent is the subject; the world is the apparatus", colors)
    ax.set_axis_off()
    _box(
        ax,
        (0.02, 0.56),
        0.24,
        0.18,
        "complete\nagent system",
        face=colors["pale_navy"],
        edge=colors["navy"],
        text_color=colors["ink"],
    )
    _box(
        ax,
        (0.37, 0.56),
        0.22,
        0.18,
        "typed\noperation",
        face="#ECF6F3",
        edge=colors["teal"],
        text_color=colors["ink"],
    )
    _box(
        ax,
        (0.70, 0.56),
        0.27,
        0.18,
        "executable\nchemical world",
        face=colors["navy"],
        edge=colors["navy"],
        text_color=colors["white"],
    )
    _arrow(ax, (0.26, 0.65), (0.37, 0.65), colors["ink"])
    _arrow(ax, (0.59, 0.65), (0.70, 0.65), colors["ink"])
    _box(
        ax,
        (0.38, 0.20),
        0.30,
        0.16,
        "public observation",
        face="#FFF7E8",
        edge=colors["amber"],
        text_color=colors["ink"],
    )
    _arrow(ax, (0.83, 0.56), (0.68, 0.32), colors["amber"], connectionstyle="arc3,rad=0.08")
    _arrow(ax, (0.38, 0.28), (0.16, 0.56), colors["navy"], connectionstyle="arc3,rad=0.08")
    ax.text(
        0.84,
        0.42,
        "state transition",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )
    ax.text(
        0.19,
        0.39,
        "next decision",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )
    _box(
        ax,
        (0.02, 0.04),
        0.27,
        0.10,
        "resource receipt",
        face=colors["pale_coral"],
        edge=colors["coral"],
        text_color=colors["ink"],
        fontsize=6.5,
        linewidth=0.5,
    )
    _box(
        ax,
        (0.36, 0.04),
        0.27,
        0.10,
        "immutable trace",
        face="#F4F0FA",
        edge=colors["purple"],
        text_color=colors["ink"],
        fontsize=6.5,
        linewidth=0.5,
    )
    _box(
        ax,
        (0.70, 0.04),
        0.27,
        0.10,
        "evaluator boundary",
        face="#F4F5F6",
        edge=colors["mid_gray"],
        text_color=colors["ink"],
        fontsize=6.5,
        linewidth=0.5,
    )


def _draw_panel_b(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "B", "Identity, authority and replay controls stay explicit", colors)
    ax.set_axis_off()
    controls = (
        ("physical identity", "world + material", colors["navy"]),
        ("public contract", "actions + instruments", colors["teal"]),
        ("agent authority", "allowed choices", colors["amber"]),
        ("evidence access", "public view only", colors["purple"]),
        ("resource budget", "campaign ledger", colors["coral"]),
    )
    for index, (label, detail, color) in enumerate(controls):
        y = 0.78 - index * 0.135
        ax.add_patch(
            Circle(
                (0.065, y),
                0.021,
                transform=ax.transAxes,
                facecolor=color,
                edgecolor=color,
            )
        )
        ax.text(
            0.105,
            y,
            label,
            transform=ax.transAxes,
            va="center",
            ha="left",
            fontsize=7.0,
            fontweight=600,
            color=colors["ink"],
        )
        ax.text(
            0.48,
            y,
            detail,
            transform=ax.transAxes,
            va="center",
            ha="left",
            fontsize=6.5,
            color=colors["mid_gray"],
        )
        ax.plot(
            [0.105, 0.93],
            [y - 0.055, y - 0.055],
            transform=ax.transAxes,
            color=colors["grid_gray"],
            lw=0.35,
        )
    ax.text(
        0.06,
        0.065,
        "typed state",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color=colors["ink"],
    )
    _arrow(ax, (0.25, 0.085), (0.39, 0.085), colors["mid_gray"], linewidth=0.75)
    ax.text(
        0.43,
        0.065,
        "transaction + receipt",
        transform=ax.transAxes,
        fontsize=6.0,
        ha="left",
        color=colors["ink"],
    )
    _arrow(ax, (0.71, 0.085), (0.80, 0.085), colors["mid_gray"], linewidth=0.75)
    ax.text(
        0.83,
        0.065,
        "replay",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color=colors["ink"],
    )


def _short_component(value: str) -> str:
    return value.removeprefix("private_physics.").replace("_", " ")


def _draw_panel_c(
    ax: Any,
    cases: list[Mapping[str, Any]],
    public_component_count: int,
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "C", "A fork changes one private component, not the interface", colors)
    ax.set_axis_off()
    labels = {
        "partition-constitutive-law-family": "partition world",
        "electrochemical-material-law-counterfactual": "electrochemical world",
    }
    for index, case in enumerate(cases):
        center_y = 0.70 - index * 0.43
        ax.text(
            0.02,
            center_y + 0.13,
            labels[str(case["case_id"])],
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=7.0,
            fontweight=600,
            color=colors["ink"],
        )
        _box(
            ax,
            (0.03, center_y - 0.06),
            0.21,
            0.15,
            "parent\nworld",
            face=colors["pale_navy"],
            edge=colors["navy"],
            text_color=colors["ink"],
            fontsize=6.7,
        )
        _box(
            ax,
            (0.48, center_y - 0.06),
            0.21,
            0.15,
            "child\nworld",
            face=colors["pale_coral"],
            edge=colors["coral"],
            text_color=colors["ink"],
            fontsize=6.7,
        )
        _arrow(ax, (0.24, center_y + 0.015), (0.48, center_y + 0.015), colors["purple"])
        ax.text(
            0.36,
            center_y + 0.055,
            "one private component",
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=6.2,
            color=colors["purple"],
        )
        component = _short_component(str(case["target_component_id"]))
        ax.text(
            0.36,
            center_y - 0.065,
            component,
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=6.2,
            color=colors["mid_gray"],
        )
        public_min = 100.0 * float(case["public_relative_delta_min"])
        public_max = 100.0 * float(case["public_relative_delta_max"])
        physical_min = 100.0 * float(case["physical_relative_delta_min"])
        physical_max = 100.0 * float(case["physical_relative_delta_max"])
        ax.text(
            0.72,
            center_y + 0.055,
            f"obs. Δ  {public_min:.1f}-{public_max:.1f}%",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=5.8,
            color=colors["ink"],
            clip_on=True,
        )
        ax.text(
            0.72,
            center_y - 0.025,
            f"state Δ  {physical_min:.1f}-{physical_max:.1f}%",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=5.8,
            color=colors["ink"],
            clip_on=True,
        )
        ax.text(
            0.72,
            center_y - 0.105,
            f"public  {public_component_count}/{public_component_count} fixed",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=5.8,
            color=colors["teal"],
            clip_on=True,
        )


def _draw_panel_d(
    ax: Any,
    gate_pass_counts: Mapping[str, int],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "D", "All six fork pairs pass every frozen gate", colors)
    labels = [GATE_LABELS[gate] for gate in GATE_ORDER]
    values = [gate_pass_counts[gate] for gate in GATE_ORDER]
    positions = list(range(len(labels)))
    ax.barh(
        positions,
        values,
        height=0.58,
        color=colors["teal"],
        edgecolor=colors["white"],
        linewidth=0.5,
    )
    ax.set_yticks([])
    ax.set_xlim(0, 6.85)
    ax.set_ylim(5.65, -0.65)
    ax.set_xticks([0, 3, 6])
    ax.set_xlabel("parent-child pairs passing")
    ax.grid(axis="x", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    for position, label, value in zip(positions, labels, values, strict=True):
        ax.text(
            0.12,
            position,
            label,
            va="center",
            ha="left",
            fontsize=6.0,
            fontweight=600,
            color=colors["white"],
        )
        ax.text(
            value + 0.10,
            position,
            f"{value}/6",
            va="center",
            ha="left",
            fontsize=6.7,
            fontweight=600,
            color=colors["ink"],
        )
    ax.text(
        6.80,
        -0.48,
        "2 classes  |  3 seeds/class  |  24 traces  |  0 provider calls",
        ha="right",
        va="center",
        fontsize=5.8,
        color=colors["mid_gray"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 1 object."""

    figure_system = _mapping(inputs, "figure_system")
    colors = _configure_matplotlib(figure_system)
    canvas = _mapping(figure_system, "canvas")
    width = float(canvas["two_column_width"])
    height = float(canvas["default_two_by_two_height"])
    figure = plt.figure(figsize=(width, height), facecolor=colors["white"])
    grid = figure.add_gridspec(
        2,
        2,
        left=0.055,
        right=0.985,
        bottom=0.075,
        top=0.965,
        wspace=0.24,
        hspace=0.34,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    _draw_panel_a(axes[0], colors)
    _draw_panel_b(axes[1], colors)
    cases_value = inputs.get("cases")
    if not isinstance(cases_value, list):
        raise FigureOneError("cases must be a list")
    _draw_panel_c(
        axes[2],
        cases_value,
        int(inputs["public_component_count"]),
        colors,
    )
    gate_counts = _mapping(inputs, "gate_pass_counts")
    _draw_panel_d(axes[3], {key: int(value) for key, value in gate_counts.items()}, colors)
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
        metadata={"Date": None, "Creator": "ChemWorld W1-P02 deterministic renderer"},
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
            "Title": "ChemWorld apparatus and controlled world forks",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 1",
            "Creator": "ChemWorld W1-P02 deterministic renderer",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": "ChemWorld W1-P02 deterministic renderer"},
    )
    plt.close(figure)
    return paths


def _png_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    if payload[:8] != b"\x89PNG\r\n\x1a\n" or payload[12:16] != b"IHDR":
        raise FigureOneError("invalid PNG signature or IHDR")
    return struct.unpack(">II", payload[16:24])


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
    data_contract = _mapping(inputs, "data_contract")
    source_bindings = _mapping(inputs, "source_bindings")
    qualification_binding = _mapping(source_bindings, "world_fork_qualification")
    certificate_binding = _mapping(source_bindings, "world_fork_certificate")
    png_width, png_height = _png_dimensions(outputs["png"])
    canonical_paths = _output_paths(root / OUTPUT_DIR)
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
            row["pixel_width"] = png_width
            row["pixel_height"] = png_height
            row["dpi"] = 300
        output_rows.append(row)
    manifest: dict[str, Any] = {
        "schema_id": "chemworld.work_i_figure_manifest",
        "schema_version": "0.1.0",
        "manifest_id": "work-i-figure-1-apparatus-world-forks-v0.1",
        "status": "frozen_render",
        "figure_id": "F1",
        "owner_task": "W1-P02",
        "title": "ChemWorld apparatus and controlled world forks",
        "figure_system_sha256": figure_system["system_sha256"],
        "data_contract_sha256": data_contract["contract_sha256"],
        "source_bindings": [
            {
                "path": FIGURE_SYSTEM_PATH.as_posix(),
                "role": "visual_contract",
                "sha256": _file_sha256(root / FIGURE_SYSTEM_PATH),
            },
            {
                "path": DATA_CONTRACT_PATH.as_posix(),
                "role": "data_and_counting_contract",
                "sha256": _file_sha256(root / DATA_CONTRACT_PATH),
            },
            {
                "path": qualification_binding["path"],
                "role": "immutable_formal_report",
                "sha256": qualification_binding["file_sha256"],
            },
            {
                "path": certificate_binding["path"],
                "role": "immutable_summary_certificate",
                "sha256": certificate_binding["file_sha256"],
            },
            {
                "path": SCRIPT_PATH.as_posix(),
                "role": "deterministic_renderer",
                "sha256": _file_sha256(root / SCRIPT_PATH),
            },
        ],
        "evidence_census": {
            "intervention_classes": 2,
            "seeds_per_class": 3,
            "parent_child_pairs": 6,
            "traces": 24,
            "executions_per_variant": 2,
            "public_components_invariant_per_pair": 9,
            "provider_calls": 0,
            "all_six_pairs_pass_all_six_gates": True,
        },
        "panel_roles": {
            "A": "agent_world_interaction_loop",
            "B": "identity_authority_evidence_resource_and_replay_controls",
            "C": "single_private_component_forks_with_public_invariance",
            "D": "six_pair_twenty_four_trace_qualification_gates",
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
            "programmable_world_apparatus": True,
            "agent_performance_claim": False,
            "rule_adaptation_claim": False,
            "arbitrary_world_dsl_claim": False,
            "physical_laboratory_transfer_claim": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _json_text(payload: Mapping[str, Any]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "ChemWorld apparatus" in svg:
        raise FigureOneError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureOneError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureOneError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p02-") as temporary:
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
                "pairs": manifest_payload["evidence_census"]["parent_child_pairs"],
                "traces": manifest_payload["evidence_census"]["traces"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
