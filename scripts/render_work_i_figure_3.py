"""Render Work I Figure 3 from frozen complete-system terminal evidence."""

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

from chemworld.eval.work_i_data_contract import (  # type: ignore[import-untyped]
    data_contract_sha256,
    validate_work_i_data_contract,
)

ROOT = REPOSITORY_ROOT
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
DATA_CONTRACT_PATH = Path("configs/benchmark/work_i_incremental_data_contract_v0.1.json")
LATENT_CONTRACT_PATH = Path("configs/benchmark/work_i_latent_terminal_contract_v0.1.json")
LATENT_ANALYSIS_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json"
)
COMPARISON_PATH = Path("workstreams/arxiv_v1/reports/g2-agent-system-comparison-v0.1.json")
LEDGER_PATH = Path(
    "workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
)
ARCHIVE_MANIFEST_PATH = Path(
    "benchmark/releases/chemworld-serious-v1/"
    "g2-deepseek-v0.6-public-trajectory-archive/manifest.json"
)
SHARED_STYLE_HELPER_PATH = Path("scripts/render_work_i_figure_1.py")
SCRIPT_PATH = Path("scripts/render_work_i_figure_3.py")
OUTPUT_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
OUTPUT_STEM = "figure-3-terminal-policy"
MANIFEST_PATH = OUTPUT_DIR / f"{OUTPUT_STEM}.manifest.json"

ARM_ORDER = ("opaque_codes", "anonymous_nominal_properties")
ARM_LABELS = {
    "opaque_codes": "opaque",
    "anonymous_nominal_properties": "nominal",
}
ARM_OFFSETS = {
    "opaque_codes": -0.105,
    "anonymous_nominal_properties": 0.105,
}


class FigureThreeError(RuntimeError):
    """Raised when a frozen input or rendered Figure 3 fails closed."""


def _source_binding(contract: Mapping[str, Any], artifact_id: str) -> Mapping[str, Any]:
    matches = [
        row
        for row in _mapping_rows(contract, "source_bindings")
        if row.get("artifact_id") == artifact_id
    ]
    if len(matches) != 1:
        raise FigureThreeError(f"expected one D01 binding for {artifact_id}")
    return matches[0]


def _validate_figure_system(root: Path, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("system_sha256") != _canonical_sha256(payload, "system_sha256"):
        raise FigureThreeError("P01 figure-system self-hash mismatch")
    if payload.get("status") != "frozen":
        raise FigureThreeError("P01 figure system is not frozen")
    for binding in _mapping_rows(payload, "source_bindings"):
        path_value = binding.get("path")
        expected_hash = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected_hash, str):
            raise FigureThreeError("invalid P01 source binding")
        if _file_sha256(root / path_value) != expected_hash:
            raise FigureThreeError(f"stale P01 source binding: {path_value}")
    matches = [row for row in _mapping_rows(payload, "figures") if row.get("figure_id") == "F3"]
    if len(matches) != 1:
        raise FigureThreeError("P01 must define exactly one F3")
    spec = matches[0]
    if (
        spec.get("owner_task") != "W1-P04"
        or spec.get("output_stem") != OUTPUT_STEM
        or spec.get("grid_template") != "two_by_two"
    ):
        raise FigureThreeError("P01 F3 assignment differs from W1-P04")
    if [row.get("panel") for row in _mapping_rows(spec, "panels")] != list("ABCD"):
        raise FigureThreeError("P01 F3 panel order must be A-D")
    if spec.get("pending_result_panels") != ["C", "D"]:
        raise FigureThreeError("P01 F3 must retain the preregistered C-D pending slots")
    return spec


def _validate_bound_file(
    root: Path,
    source_manifest: Mapping[str, Any],
    relative_path: Path,
) -> dict[str, Any]:
    expected = source_manifest.get(relative_path.as_posix())
    if not isinstance(expected, str):
        raise FigureThreeError(f"latent contract does not bind {relative_path.as_posix()}")
    path = root / relative_path
    if _file_sha256(path) != expected:
        raise FigureThreeError(f"stale latent source binding: {relative_path.as_posix()}")
    return _read_json(path)


def _validate_latent_analysis(
    root: Path,
    latent_contract: Mapping[str, Any],
) -> dict[str, Any]:
    analysis = _read_json(root / LATENT_ANALYSIS_PATH)
    if analysis.get("analysis_sha256") != _canonical_sha256(analysis, "analysis_sha256"):
        raise FigureThreeError("latent-terminal analysis self-hash mismatch")
    evidence_bindings = _mapping(analysis, "evidence_bindings")
    if evidence_bindings.get("latent_terminal_contract_sha256") != latent_contract.get(
        "contract_sha256"
    ):
        raise FigureThreeError("latent-terminal analysis contract binding changed")
    census = _mapping(analysis, "census")
    gate = _mapping(analysis, "entry_gate")
    supplied = _mapping(gate, "supplied")
    missingness = _mapping(analysis, "missingness_and_censoring")
    if (
        analysis.get("status") != "incomplete_full_report_required"
        or analysis.get("analysis_mode") != "formal_shadow_analysis"
        or census.get("campaign_cells") != 10
        or census.get("closed_lifecycles") != 60
        or census.get("observed_assays") != 24
        or census.get("observed_discards") != 36
        or census.get("resolved_shadow_receipts") != 6
        or census.get("unresolved_shadow_receipts") != 30
        or gate.get("formal_gate_evaluated") is not True
        or gate.get("main_text_eligible") is not False
        or supplied.get("exact_same_identity_replay_count") != 6
        or supplied.get("valid_shadow_score_count") != 6
        or supplied.get("original_resource_ledger_mutated") is not True
        or missingness.get("fixed_discard_denominator") != 36
        or missingness.get("unresolved_count") != 30
        or missingness.get("complete_case_primary_used") is not False
    ):
        raise FigureThreeError("latent-terminal gate or census changed")
    return analysis


def _latent_bounds(analysis: Mapping[str, Any]) -> list[dict[str, Any]]:
    estimands = _mapping(analysis, "estimands")
    latent = _mapping(estimands, "latent_terminal_score")
    latent_aggregation = _mapping(latent, "aggregation")
    latent_micro = _mapping(latent_aggregation, "finite_population_micro")
    latent_overall = _mapping(latent_micro, "overall")
    latent_bound_set = _mapping(latent_overall, "bounds")
    latent_stats = _mapping(latent_bound_set, "mean_and_order_statistic_bounds")
    latent_mean = _mapping(latent_stats, "mean")

    delta = _mapping(estimands, "discard_to_observed_best_delta")
    delta_aggregation = _mapping(delta, "aggregation")
    delta_micro = _mapping(delta_aggregation, "finite_population_micro")
    delta_overall = _mapping(delta_micro, "overall")
    delta_bound_set = _mapping(delta_overall, "bounds")
    delta_stats = _mapping(delta_bound_set, "mean_and_order_statistic_bounds")
    delta_mean = _mapping(delta_stats, "mean")

    false_discard = _mapping(estimands, "false_discard_fraction")
    false_bounds = _mapping(false_discard, "bounds")
    false_lower = _mapping(false_bounds, "lower")
    false_upper = _mapping(false_bounds, "upper")

    oracle = _mapping(estimands, "campaign_oracle_regret")
    oracle_bounds = _mapping(oracle, "bounds")
    oracle_stats = _mapping(oracle_bounds, "mean_and_order_statistic_bounds")
    oracle_mean = _mapping(oracle_stats, "mean")

    rows = [
        {
            "estimand": "latent score mean",
            "lower": latent_mean.get("lower"),
            "upper": latent_mean.get("upper"),
            "denominator": 36,
        },
        {
            "estimand": "discard - observed best",
            "lower": delta_mean.get("lower"),
            "upper": delta_mean.get("upper"),
            "denominator": 36,
        },
        {
            "estimand": "false-discard fraction",
            "lower": false_lower.get("value"),
            "upper": false_upper.get("value"),
            "denominator": 36,
        },
        {
            "estimand": "campaign-oracle regret",
            "lower": oracle_mean.get("lower"),
            "upper": oracle_mean.get("upper"),
            "denominator": 9,
        },
    ]
    for row in rows:
        if not isinstance(row["lower"], (int, float)) or not isinstance(
            row["upper"], (int, float)
        ):
            raise FigureThreeError(f"missing finite-population bound: {row['estimand']}")
    return rows


def load_figure_inputs(root: Path = ROOT) -> dict[str, Any]:
    """Load frozen design inputs and the failed-gate latent-terminal analysis."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_spec = _validate_figure_system(resolved, figure_system)

    data_contract = _read_json(resolved / DATA_CONTRACT_PATH)
    if data_contract.get("contract_sha256") != data_contract_sha256(data_contract):
        raise FigureThreeError("D01 data-contract self-hash mismatch")
    contract_errors = validate_work_i_data_contract(data_contract, root=resolved)
    expected_post_execution_failure = [
        "F/V/L source chain is not freeze-ready: latent_estimand_contract_passes"
    ]
    if contract_errors and contract_errors != expected_post_execution_failure:
        raise FigureThreeError("D01 contract validation failed: " + "; ".join(contract_errors))

    latent_binding = _source_binding(data_contract, "latent_terminal_estimand_contract")
    if latent_binding.get("path") != LATENT_CONTRACT_PATH.as_posix():
        raise FigureThreeError("D01 latent-contract path changed")
    if _file_sha256(resolved / LATENT_CONTRACT_PATH) != latent_binding.get("file_sha256"):
        raise FigureThreeError("D01 latent-contract file hash mismatch")
    latent_contract = _read_json(resolved / LATENT_CONTRACT_PATH)
    if latent_contract.get("contract_sha256") != _canonical_sha256(
        latent_contract, "contract_sha256"
    ):
        raise FigureThreeError("L01 latent contract self-hash mismatch")
    if latent_contract.get("contract_sha256") != latent_binding.get("embedded_sha256"):
        raise FigureThreeError("D01 and L01 embedded hashes differ")
    latent_analysis = _validate_latent_analysis(resolved, latent_contract)
    latent_bounds = _latent_bounds(latent_analysis)

    evidence_bindings = _mapping(latent_contract, "evidence_bindings")
    source_manifest = _mapping(evidence_bindings, "source_manifest")
    comparison = _validate_bound_file(resolved, source_manifest, COMPARISON_PATH)
    # The coordinator ledger legitimately accumulated later F/V/L handoffs after L01 froze
    # its source snapshot. Validate the exact current layer facts below and bind its live hash.
    ledger = _read_json(resolved / LEDGER_PATH)
    archive_manifest = _validate_bound_file(resolved, source_manifest, ARCHIVE_MANIFEST_PATH)

    if comparison.get("comparison_sha256") != _canonical_sha256(comparison, "comparison_sha256"):
        raise FigureThreeError("complete-system comparison self-hash mismatch")
    if comparison.get("comparison_sha256") != evidence_bindings.get(
        "complete_system_comparison_sha256"
    ):
        raise FigureThreeError("L01 complete-system comparison binding changed")
    if (
        archive_manifest.get("archive_sha256") != evidence_bindings.get("public_archive_sha256")
        or archive_manifest.get("cell_count") != 10
    ):
        raise FigureThreeError("public trajectory archive binding changed")

    population = _mapping(latent_contract, "population")
    population_counts = _mapping(population, "counts")
    cells = [dict(row) for row in _mapping_rows(population, "cells")]
    if (
        len(cells) != 10
        or population_counts.get("cells") != 10
        or population_counts.get("closed_lifecycles") != 60
        or population_counts.get("observed_assays") != 24
        or population_counts.get("observed_discards") != 36
        or population_counts.get("shadow_evaluations_planned") != 36
        or population.get("latent_outcomes_accessed") is not False
    ):
        raise FigureThreeError("frozen latent-terminal population census changed")

    cell_profiles: dict[tuple[int, str], dict[str, Any]] = {}
    for cell in cells:
        cell_id = cell.get("cell_id")
        seed = cell.get("world_seed")
        arm = cell.get("information_arm")
        assays = cell.get("observed_assay_count")
        discards = cell.get("observed_discard_count")
        compact_path = cell.get("compact_path")
        compact_sha256 = cell.get("compact_sha256")
        if (
            not isinstance(cell_id, str)
            or not isinstance(seed, int)
            or arm not in ARM_ORDER
            or not isinstance(assays, int)
            or not isinstance(discards, int)
            or assays + discards != 6
            or not isinstance(compact_path, str)
            or not isinstance(compact_sha256, str)
        ):
            raise FigureThreeError("invalid frozen campaign-cell terminal profile")
        if _file_sha256(resolved / compact_path) != compact_sha256:
            raise FigureThreeError(f"stale compact trajectory binding: {compact_path}")
        key = (seed, str(arm))
        if key in cell_profiles:
            raise FigureThreeError(f"duplicate frozen campaign cell: {key}")
        cell_profiles[key] = cell
    expected_keys = {(seed, arm) for seed in range(5) for arm in ARM_ORDER}
    if set(cell_profiles) != expected_keys:
        raise FigureThreeError("world-by-arm campaign-cell balance changed")
    if (
        sum(int(row["observed_assay_count"]) for row in cells) != 24
        or sum(int(row["observed_discard_count"]) for row in cells) != 36
    ):
        raise FigureThreeError("campaign-cell counts do not reproduce the terminal census")

    systems = _mapping(comparison, "systems")
    codex = _mapping(systems, "codex_sol_medium_mcp")
    deepseek = _mapping(systems, "deepseek_v4_flash_direct")
    physical_matching = _mapping(comparison, "physical_matching")
    if (
        comparison.get("status") != "completed_audited_two_agent-system_demonstration"
        or comparison.get("formal_result") is not False
        or physical_matching.get("all_cells_matched") is not True
        or physical_matching.get("matched_cell_count") != 10
        or codex.get("audit_gates_passed") is not True
        or codex.get("closed_batch_count") != 60
        or codex.get("final_assay_count") != 60
        or codex.get("discarded_batch_count") != 0
        or deepseek.get("audit_gates_passed") is not True
        or deepseek.get("closed_batch_count") != 60
        or deepseek.get("final_assay_count") != 24
        or deepseek.get("discarded_batch_count") != 36
    ):
        raise FigureThreeError("frozen complete-system comparison changed")
    for system in (codex, deepseek):
        arms = _mapping(system, "arms")
        for arm in ("opaque", "nominal"):
            row = _mapping(arms, arm)
            if row.get("cell_count") != 5 or row.get("closed_batch_count") != 30:
                raise FigureThreeError("complete-system arm balance changed")

    experiment_layers = _mapping(ledger, "experiment_layers")
    codex_layer = _mapping(experiment_layers, "g2_v0_4_autonomous_development")
    if (
        codex_layer.get("worlds") != 5
        or codex_layer.get("arms") != 2
        or codex_layer.get("cells") != 10
        or codex_layer.get("vessels_per_cell") != 6
        or codex_layer.get("completed_physical_experiments") != 60
        or codex_layer.get("final_assays") != 60
        or codex_layer.get("all_cells_complete") is not True
    ):
        raise FigureThreeError("Codex six-vessels-per-cell census changed")

    aggregation = _mapping(latent_contract, "aggregation")
    opportunity_rule = _mapping(aggregation, "campaign_oracle_opportunity_rule")
    missingness = _mapping(latent_contract, "missingness_and_failure")
    quality_reference = _mapping(latent_contract, "quality_reference")
    entry_rules = _mapping(latent_contract, "entry_rules")
    if (
        opportunity_rule.get("defined_cell_count") != 9
        or opportunity_rule.get("no_opportunity_cell_ids") != ["cell-02"]
        or opportunity_rule.get("no_opportunity_value") is not None
        or missingness.get("all_36_required_for_primary_point_estimates") is not True
        or missingness.get("complete_case_primary_allowed") is not False
        or quality_reference.get("primary_threshold_formula") != "q_c = 0.90 B_c"
        or entry_rules.get("main_text_requires")
        != [
            "36/36 exact pre-discard prefix reconstructions",
            "36/36 valid evaluator-only shadow scores",
            "36/36 exact same-identity shadow replays",
            "zero agent/provider calls",
            "no mutation of original trajectories or resource ledgers",
        ]
    ):
        raise FigureThreeError("frozen latent-panel rules changed")

    return {
        "figure_system": figure_system,
        "figure_spec": figure_spec,
        "data_contract": data_contract,
        "latent_contract": latent_contract,
        "latent_analysis": latent_analysis,
        "latent_bounds": latent_bounds,
        "latent_binding": latent_binding,
        "comparison": comparison,
        "ledger": ledger,
        "archive_manifest": archive_manifest,
        "source_manifest": source_manifest,
        "codex": codex,
        "deepseek": deepseek,
        "cell_profiles": cell_profiles,
        "quality_reference": quality_reference,
        "opportunity_rule": opportunity_rule,
        "missingness": missingness,
    }


def _configure(figure_system: Mapping[str, Any]) -> dict[str, str]:
    colors = _configure_matplotlib(figure_system)
    mpl.rcParams["svg.hashsalt"] = "chemworld-work-i-figure-3-v0.1"
    return colors


def _draw_panel_a(ax: Any, colors: Mapping[str, str]) -> None:
    _panel(ax, "A", "120 closed lifecycles: 84 assays and 36 discards", colors)
    labels = ("system A", "system B", "total")
    assays = np.array([60, 24, 84])
    discards = np.array([0, 36, 36])
    positions = np.array([2, 1, 0])
    ax.barh(positions, assays, height=0.56, color=colors["teal"], label="final assay")
    ax.barh(
        positions,
        discards,
        left=assays,
        height=0.56,
        facecolor=colors["white"],
        edgecolor=colors["mid_gray"],
        hatch="////",
        linewidth=0.75,
        label="explicit discard",
    )
    ax.set_xlim(0, 124)
    ax.set_ylim(-0.55, 2.55)
    ax.set_yticks(positions, labels)
    ax.set_xticks([0, 30, 60, 90, 120])
    ax.set_xlabel("closed lifecycles (count)")
    ax.grid(axis="x", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    for y, assay, discard in zip(positions, assays, discards, strict=True):
        total = int(assay + discard)
        ax.text(
            min(float(assay) / 2, 53),
            y,
            f"{assay}/{total} assay",
            ha="center",
            va="center",
            fontsize=6.5,
            fontweight=600,
            color=colors["white"],
        )
        if discard:
            ax.text(
                assay + discard / 2,
                y,
                f"{discard}/{total} discard",
                ha="center",
                va="center",
                fontsize=6.5,
                fontweight=600,
                color=colors["ink"],
            )
    ax.text(
        1.5,
        2.37,
        "A: native Codex/MCP scaffold   B: DeepSeek/direct-JSON scaffold",
        ha="left",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def _draw_panel_b(
    ax: Any,
    cell_profiles: Mapping[tuple[int, str], Mapping[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "B", "Terminal actions vary by matched world and arm", colors)
    seeds: Any = np.arange(5, dtype=float)
    arm_colors = {
        "opaque_codes": colors["navy"],
        "anonymous_nominal_properties": colors["coral"],
    }
    arm_styles = {
        "opaque_codes": "--",
        "anonymous_nominal_properties": "-",
    }
    for arm in ARM_ORDER:
        x = seeds + ARM_OFFSETS[arm]
        deepseek_assays = np.array(
            [int(cell_profiles[(seed, arm)]["observed_assay_count"]) for seed in range(5)]
        )
        ax.plot(
            x,
            np.full(5, 6),
            color=arm_colors[arm],
            linestyle=arm_styles[arm],
            linewidth=0.75,
            marker="o",
            markersize=5.2,
            markerfacecolor=colors["white"],
            markeredgewidth=0.9,
            zorder=2,
        )
        ax.plot(
            x,
            deepseek_assays,
            color=arm_colors[arm],
            linestyle=arm_styles[arm],
            linewidth=1.0,
            marker="s",
            markersize=4.8,
            markeredgecolor=colors["white"],
            markeredgewidth=0.45,
            zorder=3,
        )
        for x_value, assay_count in zip(x, deepseek_assays, strict=True):
            ax.text(
                x_value,
                assay_count + 0.27,
                f"{assay_count}/6",
                ha="center",
                va="bottom",
                fontsize=6.5,
                color=arm_colors[arm],
            )
    ax.set_xlim(-0.45, 4.45)
    ax.set_ylim(-0.25, 6.85)
    ax.set_xticks(seeds, [str(seed) for seed in range(5)])
    ax.set_yticks([0, 3, 6])
    ax.set_xlabel("matched world seed")
    ax.set_ylabel("assay commitments / 6")
    ax.grid(axis="y", color=colors["grid_gray"], lw=0.35)
    ax.set_axisbelow(True)
    ax.text(
        4.40,
        6.50,
        "system A: 6/6 in every cell",
        ha="right",
        va="center",
        fontsize=6.5,
        color=colors["ink"],
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
                label="system A",
            ),
            Line2D(
                [],
                [],
                marker="s",
                linestyle="none",
                markerfacecolor=colors["ink"],
                markeredgecolor=colors["ink"],
                label="system B",
            ),
            Line2D([], [], color=colors["navy"], linestyle="--", label="opaque"),
            Line2D([], [], color=colors["coral"], linestyle="-", label="nominal"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.52, 0.00),
        ncol=2,
        frameon=False,
        fontsize=6.5,
        handlelength=1.5,
        columnspacing=1.1,
    )


def _draw_panel_c(
    ax: Any,
    latent_analysis: Mapping[str, Any],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "C", "The formal latent-result gate fails closed", colors)
    ax.set_axis_off()
    census = _mapping(latent_analysis, "census")
    resolved = int(census["resolved_shadow_receipts"])
    unresolved = int(census["unresolved_shadow_receipts"])
    frame = FancyBboxPatch(
        (0.055, 0.08),
        0.89,
        0.76,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes,
        facecolor=colors["white"],
        edgecolor=colors["grid_gray"],
        linewidth=0.75,
    )
    ax.add_patch(frame)
    for index in range(36):
        row, column = divmod(index, 6)
        ax.scatter(
            [0.21 + column * 0.105],
            [0.67 - row * 0.075],
            transform=ax.transAxes,
            marker="D",
            s=21,
            facecolor=colors["teal"] if index < resolved else colors["white"],
            edgecolor=colors["teal"] if index < resolved else colors["mid_gray"],
            linewidth=0.75,
            clip_on=False,
        )
    ax.text(
        0.50,
        0.775,
        "36/36 frozen discard identities retained",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=7.0,
        fontweight=600,
        color=colors["ink"],
    )
    ax.text(
        0.50,
        0.155,
        f"{resolved} resolved  /  {unresolved} unresolved",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["ink"],
    )
    ax.text(
        0.50,
        0.105,
        "latent-dependent point estimates withheld; no complete-case substitution",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=colors["mid_gray"],
    )


def _draw_panel_d(
    ax: Any,
    latent_bounds: list[dict[str, Any]],
    colors: Mapping[str, str],
) -> None:
    _panel(ax, "D", "Missing outcomes widen finite-population bounds", colors)
    y = np.arange(len(latent_bounds))[::-1]
    lower = np.array([float(row["lower"]) for row in latent_bounds])
    upper = np.array([float(row["upper"]) for row in latent_bounds])
    ax.axvline(0, color=colors["grid_gray"], linewidth=0.65, zorder=0)
    for index, (lo, hi) in enumerate(zip(lower, upper, strict=True)):
        yi = y[index]
        ax.plot([lo, hi], [yi, yi], color=colors["navy"], linewidth=2.2)
        ax.scatter(
            [lo, hi],
            [yi, yi],
            s=19,
            facecolor=colors["white"],
            edgecolor=colors["navy"],
            linewidth=0.85,
            zorder=2,
        )
        ax.text(
            hi + 0.025,
            yi,
            f"[{lo:.3f}, {hi:.3f}]",
            ha="left",
            va="center",
            fontsize=6.1,
            color=colors["ink"],
        )
    ax.set_xlim(-0.33, 1.13)
    ax.set_ylim(-0.8, len(latent_bounds) - 0.2)
    ax.set_yticks(y, [str(row["estimand"]) for row in latent_bounds])
    ax.set_xticks([-0.25, 0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("registered bound")
    ax.grid(axis="x", color=colors["grid_gray"], linewidth=0.35)
    ax.set_axisbelow(True)
    ax.text(
        0.02,
        0.02,
        "support bounds, not confidence intervals; cell-02 is a structural null",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.1,
        color=colors["mid_gray"],
    )


def build_figure(inputs: Mapping[str, Any]) -> Any:
    """Build the final-size Matplotlib Figure 3 object."""

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
        left=0.075,
        right=0.985,
        bottom=0.09,
        top=0.965,
        wspace=0.29,
        hspace=0.42,
    )
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    typed_cells = cast(
        Mapping[tuple[int, str], Mapping[str, Any]],
        inputs["cell_profiles"],
    )
    _draw_panel_a(axes[0], colors)
    _draw_panel_b(axes[1], typed_cells, colors)
    _draw_panel_c(axes[2], _mapping(inputs, "latent_analysis"), colors)
    _draw_panel_d(axes[3], cast(list[dict[str, Any]], inputs["latent_bounds"]), colors)
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
        metadata={"Date": None, "Creator": "ChemWorld W1-P09 deterministic renderer"},
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
            "Title": "Lifecycle completion does not specify terminal policy",
            "Author": "ChemWorld",
            "Subject": "Work I Figure 3",
            "Creator": "ChemWorld W1-P09 deterministic renderer",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        paths["png"],
        format="png",
        dpi=300,
        facecolor="white",
        metadata={"Software": "ChemWorld W1-P09 deterministic renderer"},
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
    latent_contract = _mapping(inputs, "latent_contract")
    latent_analysis = _mapping(inputs, "latent_analysis")
    latent_bounds = cast(list[dict[str, Any]], inputs["latent_bounds"])
    source_manifest = _mapping(inputs, "source_manifest")
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
        "manifest_id": "work-i-figure-3-terminal-policy-v0.1",
        "status": "frozen_latent_gate_failure_display",
        "figure_id": "F3",
        "owner_task": "W1-P09",
        "original_owner_task": "W1-P04",
        "title": "Lifecycle completion does not specify terminal policy",
        "figure_system_sha256": figure_system["system_sha256"],
        "data_contract_sha256": data_contract["contract_sha256"],
        "latent_contract_sha256": latent_contract["contract_sha256"],
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
                "path": LATENT_CONTRACT_PATH.as_posix(),
                "role": "outcome_blind_latent_terminal_contract",
                "sha256": _file_sha256(root / LATENT_CONTRACT_PATH),
            },
            {
                "path": LATENT_ANALYSIS_PATH.as_posix(),
                "role": "formal_latent_terminal_gate_and_bounds",
                "sha256": _file_sha256(root / LATENT_ANALYSIS_PATH),
            },
            {
                "path": COMPARISON_PATH.as_posix(),
                "role": "immutable_complete_system_comparison",
                "sha256": source_manifest[COMPARISON_PATH.as_posix()],
            },
            {
                "path": LEDGER_PATH.as_posix(),
                "role": "current_coordinator_experiment_accounting",
                "sha256": _file_sha256(root / LEDGER_PATH),
            },
            {
                "path": ARCHIVE_MANIFEST_PATH.as_posix(),
                "role": "immutable_public_trajectory_index",
                "sha256": source_manifest[ARCHIVE_MANIFEST_PATH.as_posix()],
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
            "distinct_complete_systems": 2,
            "matched_worlds": 5,
            "information_arms": 2,
            "matched_world_by_arm_cells": 10,
            "closed_lifecycles": 120,
            "final_assays": 84,
            "explicit_discards": 36,
            "complete_system_a": {"closed": 60, "assays": 60, "discards": 0},
            "complete_system_b": {"closed": 60, "assays": 24, "discards": 36},
            "registered_latent_discard_units": 36,
            "resolved_shadow_receipts": 6,
            "unresolved_shadow_receipts": 30,
            "campaign_oracle_opportunity_cells": 9,
            "structural_null_cells": ["cell-02"],
        },
        "panel_roles": {
            "A": "120_closed_lifecycles_partitioned_into_84_assays_and_36_discards",
            "B": "terminal_action_profiles_by_complete_system_world_and_information_arm",
            "C": "all_36_registered_discards_with_6_resolved_and_30_unresolved_receipts",
            "D": "finite_population_bounds_after_the_formal_latent_result_gate_failed",
        },
        "pending_result_panels": [],
        "latent_result_summary": {
            "analysis_sha256": latent_analysis["analysis_sha256"],
            "analysis_status": latent_analysis["status"],
            "main_text_eligible": False,
            "point_estimates_withheld": True,
            "resolved_shadow_receipts": 6,
            "unresolved_shadow_receipts": 30,
            "complete_case_primary_used": False,
            "finite_population_bounds": latent_bounds,
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
            "descriptive_complete_system_profiles": True,
            "lifecycle_completion_distinct_from_terminal_action": True,
            "isolated_model_backend_effect": False,
            "leaderboard_comparison": False,
            "discard_quality_point_estimate_reported": False,
            "failed_latent_gate_reported": True,
            "latent_result_direction_selected_after_outcomes": False,
            "real_laboratory_generalization": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def _validate_rendered_outputs(outputs: Mapping[str, Path]) -> None:
    svg = outputs["svg"].read_text(encoding="utf-8")
    pdf = outputs["pdf"].read_bytes()
    png_width, png_height = _png_dimensions(outputs["png"])
    if "<text" not in svg or "Lifecycle completion does not specify terminal policy" in svg:
        raise FigureThreeError("SVG text is not editable or contains a forbidden suptitle")
    if not pdf.startswith(b"%PDF") or b"/FontFile2" not in pdf:
        raise FigureThreeError("PDF is invalid or lacks embedded TrueType fonts")
    if (png_width, png_height) != (2124, 1560):
        raise FigureThreeError(f"unexpected final-size PNG dimensions: {png_width}x{png_height}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_figure_inputs(ROOT)
    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-w1-p09-") as temporary:
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
                "pending_panels": manifest_payload["pending_result_panels"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
