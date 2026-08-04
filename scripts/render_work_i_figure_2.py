"""Render Work I Figure 2 from frozen known-policy validity evidence."""

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
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scripts.render_work_i_figure_1 import (
    _box,
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

from chemworld.eval.work_i_data_contract import (  # type: ignore[import-untyped]
    data_contract_sha256,
    validate_work_i_data_contract,
)

ROOT = REPOSITORY_ROOT
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
DATA_CONTRACT_PATH = Path("configs/benchmark/work_i_incremental_data_contract_v0.1.json")
KNOWN_POLICY_CONTRACT_PATH = Path("configs/benchmark/work_i_known_policy_contract_v0.1.json")
SHARED_STYLE_HELPER_PATH = Path("scripts/render_work_i_figure_1.py")
SCRIPT_PATH = Path("scripts/render_work_i_figure_2.py")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-2-known-policy-validity"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"

POLICY_ORDER = (
    "assay_all",
    "measure_then_threshold",
    "start_then_discard",
)
POLICY_LABELS = {
    "assay_all": "assay all",
    "measure_then_threshold": "measure then threshold",
    "start_then_discard": "start then discard",
}
POLICY_MARKERS = {
    "assay_all": "o",
    "measure_then_threshold": "^",
    "start_then_discard": "s",
}
POLICY_LINESTYLES = {
    "assay_all": "-",
    "measure_then_threshold": "--",
    "start_then_discard": ":",
}
PROFILE_METRICS = (
    "assay_fraction",
    "discard_fraction",
    "measured_lifecycle_fraction",
    "continued_after_measurement_fraction",
    "nonfinal_instrument_uses_per_closed_lifecycle",
    "attempted_operations_per_closed_lifecycle",
)


class FigureTwoError(RuntimeError):
    """Raised when a frozen source or rendered Figure 2 fails closed."""


def _source_binding(contract: Mapping[str, Any], artifact_id: str) -> Mapping[str, Any]:
    matches = [
        row
        for row in _mapping_rows(contract, "source_bindings")
        if row.get("artifact_id") == artifact_id
    ]
    if len(matches) != 1:
        raise FigureTwoError(f"expected one D01 binding for {artifact_id}")
    return matches[0]


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("system_sha256") != _canonical_sha256(payload, "system_sha256"):
        raise FigureTwoError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureTwoError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureTwoError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureTwoError(f"stale P01 source binding: {path_value}")
    matches = [row for row in _mapping_rows(payload, "figures") if row.get("figure_id") == "F2"]
    if len(matches) != 1:
        raise FigureTwoError("P01 must define exactly one F2")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P03"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
    ):
        raise FigureTwoError("P01 F2 assignment differs from W1-P03")
    if [row.get("panel") for row in _mapping_rows(spec, "panels")] != list("ABCD"):
        raise FigureTwoError("P01 F2 panel order must be A-D")
    return spec


def _validate_embedded_contract(payload: Mapping[str, Any]) -> str:
    supplied = payload.get("contract_sha256")
    computed = _canonical_sha256(payload, "contract_sha256")
    if not isinstance(supplied, str) or supplied != computed:
        raise FigureTwoError("known-policy contract self-hash mismatch")
    return supplied


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Load and validate frozen P01, D01, V02, and V09 inputs."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)
    data_contract = _read_json(resolved / DATA_CONTRACT_PATH)
    if data_contract.get("contract_sha256") != data_contract_sha256(data_contract):
        raise FigureTwoError("D01 data-contract self-hash mismatch")
    # D01 is an immutable pre-outcome interface freeze. Validate that frozen object,
    # then verify the V-specific bound files below; do not rebuild it from a later
    # coordinator ledger that legitimately accumulated post-freeze handoffs.
    contract_errors = validate_work_i_data_contract(data_contract)
    if contract_errors:
        raise FigureTwoError("D01 contract validation failed: " + "; ".join(contract_errors))

    source_payloads: dict[str, dict[str, Any]] = {}
    source_bindings: dict[str, Mapping[str, Any]] = {}
    for artifact_id in (
        "known_policy_validity_report",
        "known_policy_delivery_manifest",
    ):
        binding = _source_binding(data_contract, artifact_id)
        path_value = binding.get("path")
        if not isinstance(path_value, str):
            raise FigureTwoError(f"invalid source path for {artifact_id}")
        path = resolved / path_value
        if _file_sha256(path) != binding.get("file_sha256"):
            raise FigureTwoError(f"file hash mismatch for {artifact_id}")
        payload = _read_json(path)
        embedded_field = binding.get("embedded_hash_field")
        if not isinstance(embedded_field, str) or payload.get(embedded_field) != binding.get(
            "embedded_sha256"
        ):
            raise FigureTwoError(f"embedded hash mismatch for {artifact_id}")
        source_payloads[artifact_id] = payload
        source_bindings[artifact_id] = binding

    report = source_payloads["known_policy_validity_report"]
    delivery_manifest = source_payloads["known_policy_delivery_manifest"]
    policy_contract = _read_json(resolved / KNOWN_POLICY_CONTRACT_PATH)
    policy_contract_sha256 = _validate_embedded_contract(policy_contract)
    dependency_bindings = _mapping(_mapping(report, "input_bindings"), "dependency_bindings")
    if dependency_bindings.get("known_policy_contract_sha256") != policy_contract_sha256:
        raise FigureTwoError("V09 report does not bind the known-policy contract")

    estimand = _mapping(report, "estimand")
    reliability = _mapping(report, "test_retest_reliability")
    scientific_status = _mapping(report, "scientific_status")
    policy_summaries = _mapping(report, "policy_summaries")
    profiles = _mapping_rows(report, "campaign_profiles")
    if (
        report.get("status") != "positive_control_established"
        or scientific_status.get("established") is not True
        or estimand.get("primary_campaigns") != 30
        or estimand.get("primary_closed_lifecycles") != 180
        or estimand.get("retest_campaigns") != 30
        or estimand.get("retest_closed_lifecycles") != 180
        or estimand.get("provider_calls") != 0
        or estimand.get("retest_in_primary_estimand") is not False
        or reliability.get("pair_count") != 30
        or reliability.get("same_identity_deterministic_pairs") is not True
        or reliability.get("all_component_hashes_match") is not True
        or reliability.get("excluded_from_primary_estimand") is not True
        or len(profiles) != 30
        or delivery_manifest.get("status") != "complete"
        or delivery_manifest.get("immutable") is not True
    ):
        raise FigureTwoError("frozen V validity census or gates changed")
    if set(policy_summaries) != set(POLICY_ORDER):
        raise FigureTwoError("unexpected policy summary set")

    summaries: dict[str, dict[str, float]] = {}
    for policy_id in POLICY_ORDER:
        summary = _mapping(policy_summaries, policy_id)
        metrics = _mapping(summary, "metrics")
        if summary.get("campaign_count") != 10:
            raise FigureTwoError(f"unexpected campaign count for {policy_id}")
        summaries[policy_id] = {metric: float(metrics[metric]) for metric in PROFILE_METRICS}

    policy_rows = {
        str(row.get("policy_id")): row for row in _mapping_rows(policy_contract, "policies")
    }
    if set(policy_rows) != set(POLICY_ORDER):
        raise FigureTwoError("unexpected policy contract set")
    formal_matrix = _mapping(policy_contract, "formal_matrix")
    if (
        formal_matrix.get("campaign_count") != 30
        or formal_matrix.get("closed_lifecycle_count") != 180
        or formal_matrix.get("provider_call_count") != 0
    ):
        raise FigureTwoError("known-policy formal matrix changed")

    profile_policy_counts = dict.fromkeys(POLICY_ORDER, 0)
    profile_arm_counts: dict[str, int] = {}
    for profile in profiles:
        identity = _mapping(profile, "identity")
        policy_id = str(identity.get("policy_id"))
        arm = str(identity.get("information_arm"))
        if policy_id not in profile_policy_counts:
            raise FigureTwoError(f"unexpected profile policy: {policy_id}")
        profile_policy_counts[policy_id] += 1
        profile_arm_counts[arm] = profile_arm_counts.get(arm, 0) + 1
    if set(profile_policy_counts.values()) != {10} or profile_arm_counts != {
        "opaque_codes": 15,
        "anonymous_nominal_properties": 15,
    }:
        raise FigureTwoError("primary campaign profile balance changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "data_contract": data_contract,
        "report": report,
        "delivery_manifest": delivery_manifest,
        "policy_contract": policy_contract,
        "policy_contract_sha256": policy_contract_sha256,
        "source_bindings": source_bindings,
        "summaries": summaries,
        "policy_rows": policy_rows,
        "profile_policy_counts": profile_policy_counts,
        "profile_arm_counts": profile_arm_counts,
    }


def _configure(figure_system: Mapping[str, Any]) -> dict[str, str]:
    colors = _configure_matplotlib(figure_system)
    mpl.rcParams["svg.hashsalt"] = "chemworld-work-i-figure-2-v0.1"
    return colors


def _draw_panel_a(
    ax: Any,
    policy_rows: Mapping[str, Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "A", "Three policies were fixed before the formal worlds", colors)
    ax.set_axis_off()
    flows = {
        "assay_all": "process\n→ terminate → assay",
        "measure_then_threshold": "process → UV-vis\n→ threshold branch",
        "start_then_discard": "start → discard",
    }
    roles = {
        "assay_all": "terminal-commitment control",
        "measure_then_threshold": "evidence-conditioned control",
        "start_then_discard": "explicit-discard control",
    }
    for index, policy_id in enumerate(POLICY_ORDER):
        y = 0.73 - index * 0.29
        marker = POLICY_MARKERS[policy_id]
        ax.scatter(
            [0.065],
            [y + 0.055],
            transform=ax.transAxes,
            s=62,
            marker=marker,
            facecolor=colors["white"],
            edgecolor=colors["ink"],
            linewidth=1.1,
            clip_on=False,
        )
        ax.text(
            0.12,
            y + 0.08,
            POLICY_LABELS[policy_id],
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=7.2,
            fontweight=600,
            color=colors["ink"],
        )
        ax.text(
            0.12,
            y + 0.005,
            roles[policy_id],
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=5.8,
            color=colors["mid_gray"],
        )
        _box(
            ax,
            (0.51, y - 0.015),
            0.44,
            0.14,
            flows[policy_id],
            face=colors["pale_navy"] if index == 0 else colors["white"],
            edge=colors["grid_gray"],
            text_color=colors["ink"],
            fontsize=6.2,
            linewidth=0.5,
        )
        row = policy_rows[policy_id]
        operation_count = row.get("operation_count_per_lifecycle")
        operation_text = (
            "6 or 8 operations"
            if isinstance(operation_count, Mapping)
            else f"{operation_count} operations"
        )
        reads = "reads observation" if row.get("reads_observations_for_decisions") else "fixed"
        ax.text(
            0.95,
            y - 0.055,
            f"{operation_text}  •  {reads}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=5.6,
            color=colors["mid_gray"],
        )


def _draw_panel_b(
    ax: Any,
    summaries: Mapping[str, Mapping[str, float]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "B", "Terminal commitment recovers the three signatures", colors)
    y = np.arange(len(POLICY_ORDER))
    assay = np.array([summaries[policy]["assay_fraction"] for policy in POLICY_ORDER])
    discard = np.array([summaries[policy]["discard_fraction"] for policy in POLICY_ORDER])
    ax.barh(y, assay, color=colors["teal"], height=0.58, label="final assay")
    ax.barh(
        y,
        discard,
        left=assay,
        color=colors["mid_gray"],
        height=0.58,
        label="explicit discard",
    )
    ax.set_yticks([])
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(2.7, -0.7)
    ax.set_xticks([0.0, 0.5, 1.0], ["0", "50", "100"])
    ax.set_xlabel("closed lifecycles (%)")
    ax.grid(axis="x", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    for position, policy_id, assay_value, discard_value in zip(
        y, POLICY_ORDER, assay, discard, strict=True
    ):
        ax.text(
            0.018,
            position - 0.20,
            POLICY_LABELS[policy_id],
            ha="left",
            va="center",
            fontsize=5.8,
            fontweight=600,
            color=colors["white"],
        )
        if assay_value >= 0.16:
            ax.text(
                assay_value / 2,
                position,
                f"{100 * assay_value:.1f}% assay",
                ha="center",
                va="center",
                fontsize=6.0,
                fontweight=600,
                color=colors["white"],
            )
        if discard_value >= 0.16:
            ax.text(
                assay_value + discard_value / 2,
                position,
                f"{100 * discard_value:.1f}% discard",
                ha="center",
                va="center",
                fontsize=6.0,
                fontweight=600,
                color=colors["white"],
            )
    ax.text(
        0.99,
        -0.52,
        "10 campaigns/policy  •  6 lifecycles/campaign",
        ha="right",
        va="center",
        fontsize=5.8,
        color=colors["mid_gray"],
    )


def _normalized_profile(summary: Mapping[str, float]) -> list[float]:
    values = [summary[metric] for metric in PROFILE_METRICS]
    values[-1] /= 8.0
    return values


def _draw_panel_c(
    ax: Any,
    summaries: Mapping[str, Mapping[str, float]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "C", "A profile separates decisions, evidence and resources", colors)
    x = np.arange(len(PROFILE_METRICS))
    tick_labels = [
        "assay",
        "discard",
        "measure",
        "continue",
        "instrument",
        "ops / 8",
    ]
    offsets = {
        "assay_all": -0.045,
        "measure_then_threshold": 0.035,
        "start_then_discard": 0.0,
    }
    for policy_id in POLICY_ORDER:
        values = _normalized_profile(summaries[policy_id])
        ax.plot(
            x,
            values,
            color=colors["ink"],
            linestyle=POLICY_LINESTYLES[policy_id],
            linewidth=0.9,
            marker=POLICY_MARKERS[policy_id],
            markersize=4.2,
            markerfacecolor=colors["white"],
            markeredgecolor=colors["ink"],
            label=POLICY_LABELS[policy_id],
        )
        ax.text(
            x[-1] + 0.10,
            values[-1] + offsets[policy_id],
            {
                "assay_all": "assay all",
                "measure_then_threshold": "threshold",
                "start_then_discard": "discard",
            }[policy_id],
            ha="left",
            va="center",
            fontsize=5.7,
            color=colors["ink"],
        )
    ax.set_xlim(-0.18, len(x) - 0.15)
    ax.set_ylim(-0.08, 1.08)
    ax.set_xticks(x, tick_labels)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_ylabel("axis-specific value")
    ax.grid(axis="y", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)


def _draw_panel_d(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "D", "All 30 retests reproduce registered components", colors)
    checks = (
        "same identity",
        "trajectory",
        "resource ledger",
        "profile",
    )
    xs = np.arange(1, 31)
    for row_index, _ in enumerate(checks):
        ax.scatter(
            xs,
            np.full_like(xs, row_index),
            marker="s",
            s=18,
            facecolor=colors["teal"],
            edgecolor=colors["white"],
            linewidth=0.35,
        )
    ax.set_xlim(-7.0, 30.75)
    ax.set_ylim(3.55, -0.75)
    ax.set_yticks([])
    ax.set_xticks([1, 10, 20, 30])
    ax.set_xlabel("deterministic retest pair")
    ax.tick_params(axis="y", length=0)
    for row_index, label in enumerate(checks):
        ax.text(
            -6.5,
            row_index,
            label,
            ha="left",
            va="center",
            fontsize=6.0,
            color=colors["ink"],
        )
    for boundary in (10.5, 20.5):
        ax.axvline(boundary, color=colors["grid_gray"], lw=0.5)
    ax.text(
        5.5,
        -0.49,
        "assay all",
        ha="center",
        va="center",
        fontsize=5.8,
        color=colors["mid_gray"],
    )
    ax.text(
        15.5,
        -0.49,
        "measure / threshold",
        ha="center",
        va="center",
        fontsize=5.8,
        color=colors["mid_gray"],
    )
    ax.text(
        25.5,
        -0.49,
        "start / discard",
        ha="center",
        va="center",
        fontsize=5.8,
        color=colors["mid_gray"],
    )
    ax.text(
        30.5,
        3.38,
        "30/30 exact matches  •  reliability only  •  excluded from primary estimand",
        ha="right",
        va="center",
        fontsize=5.4,
        color=colors["mid_gray"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 2 object."""

    figure_system = _mapping(inputs, "figure_system")
    colors = _configure(figure_system)
    canvas = _mapping(figure_system, "canvas")
    figure = plt.figure(
        figsize=(
            float(canvas["two_column_width"]),
            float(canvas["default_two_by_two_height"]),
        ),
        facecolor=colors["white"],
    )
    grid = figure.add_gridspec(
        2,
        2,
        left=0.060,
        right=0.985,
        bottom=0.095,
        top=0.965,
        wspace=0.26,
        hspace=0.40,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    policy_rows = _mapping(inputs, "policy_rows")
    summaries = _mapping(inputs, "summaries")
    _draw_panel_a(
        axes[0],
        {policy: _mapping(policy_rows, policy) for policy in POLICY_ORDER},
        colors,
    )
    summary_rows = {policy: _mapping(summaries, policy) for policy in POLICY_ORDER}
    _draw_panel_b(axes[1], summary_rows, colors)
    _draw_panel_c(axes[2], summary_rows, colors)
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
        metadata={"Date": None, "Creator": "ChemWorld W1-P03 deterministic renderer"},
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
            "Title": "Known policies validate the experimental-agency profile",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 2",
            "Creator": "ChemWorld W1-P03 deterministic renderer",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": "ChemWorld W1-P03 deterministic renderer"},
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
    data_contract = _mapping(inputs, "data_contract")
    source_bindings = _mapping(inputs, "source_bindings")
    report_binding = _mapping(source_bindings, "known_policy_validity_report")
    delivery_binding = _mapping(source_bindings, "known_policy_delivery_manifest")
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
            row.update(
                {
                    "pixel_width": png_width,
                    "pixel_height": png_height,
                    "dpi": 300,
                }
            )
        output_rows.append(row)
    manifest: dict[str, Any] = {
        "schema_id": "chemworld.work_i_figure_manifest",
        "schema_version": "0.1.0",
        "manifest_id": "work-i-figure-2-known-policy-validity-v0.1",
        "status": "frozen_render",
        "figure_id": "F2",
        "owner_task": "W1-P03",
        "title": "Known policies validate the experimental-agency profile",
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
                "path": KNOWN_POLICY_CONTRACT_PATH.as_posix(),
                "role": "immutable_policy_protocol",
                "sha256": _file_sha256(root / KNOWN_POLICY_CONTRACT_PATH),
            },
            {
                "path": report_binding["path"],
                "role": "immutable_formal_report",
                "sha256": report_binding["file_sha256"],
            },
            {
                "path": delivery_binding["path"],
                "role": "immutable_delivery_manifest",
                "sha256": delivery_binding["file_sha256"],
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
            "known_policies": 3,
            "primary_campaigns": 30,
            "primary_closed_lifecycles": 180,
            "retest_campaigns": 30,
            "retest_closed_lifecycles": 180,
            "retest_in_primary_estimand": False,
            "provider_calls": 0,
            "all_30_retest_pairs_match": True,
        },
        "panel_roles": {
            "A": "frozen_policy_definitions_and_expected_signatures",
            "B": "terminal_commitment_profile_recovery",
            "C": "decision_evidence_resource_profile_without_composite",
            "D": "same_identity_deterministic_retest_reliability",
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
            "bounded_construct_and_discriminant_validity": True,
            "deterministic_reliability_positive_control": True,
            "model_or_provider_capability": False,
            "endpoint_performance_ranking": False,
            "causal_material_information_effect": False,
            "scalar_experimental_intelligence": False,
            "real_laboratory_generalization": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "Known policies validate" in svg:
        raise FigureTwoError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureTwoError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureTwoError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p03-") as temporary:
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
                "primary_campaigns": manifest_payload["evidence_census"]["primary_campaigns"],
                "retest_pairs": manifest_payload["evidence_census"]["retest_campaigns"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
