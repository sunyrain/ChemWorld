#!/usr/bin/env python3
"""Calibrate the final Experiment 1 C-S impurity-occlusion-law candidate."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_c_qualification import load_contract
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.physchem.crystallization_units import SURFACE_SATURATION_MAX_LOADING_RATIO
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    apply_crystallization_material_family,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

try:
    from scripts.run_experiment_1_c_qualification import (
        _campaign_config,
        _execute,
        _feature_values,
        _query_spec,
        _stable_seed,
    )
except ModuleNotFoundError:
    from run_experiment_1_c_qualification import (
        _campaign_config,
        _execute,
        _feature_values,
        _query_spec,
        _stable_seed,
    )

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/experiment_1_c_structural_authoring_v1.2.1.json"
)
CALIBRATION_SEEDS = (401, 402, 403)
SEED_LEVELS_G = (0.001, 0.015)
TEMPERATURE_LEVELS_K = (310.0, 270.0)
DURATION_LEVELS_S = (3600.0, 10800.0)
LAW_IDS = ("supersaturation_transfer_parent", "surface_saturation_occlusion")
METRICS = (
    "crystal_yield",
    "crystal_purity",
    "crystal_size",
    "crystal_csd_quality",
    "crystal_fines_fraction",
    "score",
)
EFFECT_GATE = 0.03
PURITY_EFFECT_GATE = 0.01
PURITY_CONSTRAINT = 0.98
SURFACE_HALF_SATURATION_MOL_L = 0.010
SCALAR_NULL_MULTIPLIERS = (1.0, 2.0, 4.0, 6.0)
SCALAR_NULL_FIT_CELLS = ("s0-t0-d0", "s0-t1-d1", "s1-t0-d1", "s1-t1-d0")
SCALAR_NULL_HELD_OUT_CELLS = ("s0-t0-d1", "s0-t1-d0", "s1-t0-d0", "s1-t1-d1")
SCALAR_NULL_METRICS = (
    "crystal_purity",
    "crystal_yield",
    "crystal_csd_quality",
    "crystal_fines_fraction",
)
DECLARED_FINAL_ASSAY_SIGMA = {
    "crystal_purity": 0.010,
    "crystal_yield": 0.010,
    "crystal_csd_quality": 0.018,
    "crystal_fines_fraction": 0.018,
}
SCALAR_NULL_MINIMUM_NORMALIZED_RESIDUAL = 2.0
SCALAR_NULL_MINIMUM_HELD_OUT_CELLS = 2


def _load_machine_contract(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    machine = json.loads(path.read_text(encoding="utf-8"))
    expected_schema = "chemworld-experiment-1-c-structural-authoring-contract-1.2.1"
    if machine.get("schema_version") != expected_schema:
        raise ValueError("C-S structural authoring machine-contract schema changed")
    if machine.get("status") != "frozen_before_calibration":
        raise ValueError("C-S structural authoring contract is not frozen")
    expected_self_hash = canonical_json_sha256(
        {key: value for key, value in machine.items() if key != "contract_sha256"}
    )
    if machine.get("contract_sha256") != expected_self_hash:
        raise ValueError("C-S structural authoring contract self-hash changed")
    note = machine.get("authoring_note", {})
    note_path = ROOT / str(note.get("path", ""))
    if not note_path.is_file() or file_sha256(note_path) != note.get("sha256"):
        raise ValueError("C-S authoring note binding changed")
    binding = machine.get("source_binding", {})
    source_commit = str(binding.get("source_commit", ""))
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for row in binding.get("files", []):
        source_path = ROOT / str(row.get("path", ""))
        if not source_path.is_file() or file_sha256(source_path) != row.get("sha256"):
            raise ValueError(f"C-S source binding changed: {row.get('path')}")
    constants = machine.get("scientific_constants", {})
    if float(constants.get("surface_saturation_max_loading_ratio")) != 4.0:
        raise ValueError("C-S surface-saturation coefficient must remain 4")
    if SURFACE_SATURATION_MAX_LOADING_RATIO != 4.0:
        raise ValueError("runtime surface-saturation coefficient changed")
    if float(constants.get("surface_half_saturation_mol_L")) != SURFACE_HALF_SATURATION_MOL_L:
        raise ValueError("C-S half-saturation constant changed")
    tournament = machine.get("tournament", {})
    if tuple(tournament.get("calibration_seeds", ())) != CALIBRATION_SEEDS:
        raise ValueError("C-S calibration seeds changed")
    if tuple(tournament.get("scalar_null_fit_cells", ())) != SCALAR_NULL_FIT_CELLS:
        raise ValueError("C-S scalar-null fit cells changed")
    if tuple(tournament.get("scalar_null_held_out_cells", ())) != SCALAR_NULL_HELD_OUT_CELLS:
        raise ValueError("C-S scalar-null held-out cells changed")
    frozen_multipliers = tuple(
        float(value) for value in tournament.get("scalar_null_multipliers", ())
    )
    if frozen_multipliers != SCALAR_NULL_MULTIPLIERS:
        raise ValueError("C-S scalar-null multiplier grid changed")
    gates = machine.get("gates", {})
    if float(gates.get("purity_effect_gate")) != PURITY_EFFECT_GATE:
        raise ValueError("C-S purity response gate changed")
    if float(gates.get("other_endpoint_effect_gate")) != EFFECT_GATE:
        raise ValueError("C-S endpoint response gate changed")
    frozen_residual_gate = float(gates.get("scalar_null_minimum_normalized_residual"))
    if frozen_residual_gate != SCALAR_NULL_MINIMUM_NORMALIZED_RESIDUAL:
        raise ValueError("C-S scalar-null residual gate changed")
    decision = machine.get("decision_rule", {})
    if float(decision.get("purity_constraint")) != PURITY_CONSTRAINT:
        raise ValueError("C-S purity-constrained decision changed")
    benchmark = machine.get("experiment_contract", {})
    benchmark_path = ROOT / str(benchmark.get("path", ""))
    if not benchmark_path.is_file() or file_sha256(benchmark_path) != benchmark.get("sha256"):
        raise ValueError("C-S base experiment contract binding changed")
    return machine, load_contract(ROOT, benchmark_path)


def surface_saturation_intervention() -> dict[str, Any]:
    return {
        "axis_id": "crystallization.impurity-occlusion-law",
        "mode": "extrapolation",
        "severity": 1.0,
    }


def scalar_null_intervention(multiplier: float) -> list[dict[str, Any]]:
    if multiplier == 1.0:
        return []
    if multiplier not in SCALAR_NULL_MULTIPLIERS:
        raise ValueError("scalar-null multiplier is outside the frozen candidate grid")
    return [
        {
            "axis_id": "crystallization.impurity-occlusion-capacity",
            "mode": "extrapolation",
            "severity": (multiplier - 1.0) / 5.0,
        }
    ]


def _design(contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for seed_index, seed_mass in enumerate(SEED_LEVELS_G):
        for temperature_index, temperature in enumerate(TEMPERATURE_LEVELS_K):
            for duration_index, duration in enumerate(DURATION_LEVELS_S):
                features = _feature_values(
                    contract,
                    catalyst=0,
                    solvent=0,
                    seed_mass_g=seed_mass,
                    temperature_K=temperature,
                )
                features["crystallization_duration_s"] = duration
                cell_id = f"s{seed_index}-t{temperature_index}-d{duration_index}"
                rows.append(
                    {
                        "cell_id": cell_id,
                        "seed_index": seed_index,
                        "temperature_index": temperature_index,
                        "duration_index": duration_index,
                        "query_spec": _query_spec(
                            query_id=cell_id,
                            feature_values=features,
                            phase="c_structural_authoring",
                            axis_a_index=seed_index,
                            axis_b_index=temperature_index,
                        ),
                    }
                )
    return rows


def _private_fork_audit(world_seed: int) -> dict[str, Any]:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-to-crystallization")
    parent = apply_crystallization_material_family(
        generator.generate(scenario, world_seed),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    child = apply_crystallization_material_family(
        generator.generate(scenario, world_seed, (surface_saturation_intervention(),)),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    repeated = apply_crystallization_material_family(
        generator.generate(scenario, world_seed, (surface_saturation_intervention(),)),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    parent_law = parent.initial_state.metadata.get(
        "crystallization_impurity_occlusion_law_id",
        "linear_supersaturation_transfer_v1",
    )
    child_law = child.initial_state.metadata.get("crystallization_impurity_occlusion_law_id")
    return {
        "parent_world_id": parent.parameters.world_id,
        "child_world_id": child.parameters.world_id,
        "child_hash_deterministic": child.parameters.world_id == repeated.parameters.world_id,
        "private_world_hash_changed": parent.parameters.world_id != child.parameters.world_id,
        "parent_occlusion_law_id": parent_law,
        "child_occlusion_law_id": child_law,
    }


def _scalar_null_analysis(
    paired_rows: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
    scalar_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    child_by_cell = {str(child["cell_id"]): child for _, child in paired_rows}
    scalar_by_key = {
        (str(row["cell_id"]), float(row["scalar_null_multiplier"])): row
        for row in scalar_rows
    }

    def normalized_sse(multiplier: float) -> float:
        residuals = []
        for cell_id in SCALAR_NULL_FIT_CELLS:
            child = child_by_cell[cell_id]
            null = scalar_by_key[(cell_id, multiplier)]
            for metric in SCALAR_NULL_METRICS:
                sigma = DECLARED_FINAL_ASSAY_SIGMA[metric]
                residuals.append(
                    (float(child["metrics"][metric]) - float(null["metrics"][metric])) / sigma
                )
        return sum(value**2 for value in residuals) / len(residuals)

    fit_scores = {
        str(multiplier): normalized_sse(multiplier)
        for multiplier in SCALAR_NULL_MULTIPLIERS
    }
    best_multiplier = min(
        SCALAR_NULL_MULTIPLIERS,
        key=lambda value: (fit_scores[str(value)], value),
    )
    held_out = []
    resolving_cells = set()
    for cell_id in SCALAR_NULL_HELD_OUT_CELLS:
        if (cell_id, best_multiplier) not in scalar_by_key:
            continue
        child = child_by_cell[cell_id]
        null = scalar_by_key[(cell_id, best_multiplier)]
        metric_residuals = {}
        for metric in SCALAR_NULL_METRICS:
            absolute = abs(float(child["metrics"][metric]) - float(null["metrics"][metric]))
            normalized = absolute / DECLARED_FINAL_ASSAY_SIGMA[metric]
            metric_residuals[metric] = {
                "absolute": absolute,
                "declared_sigma": DECLARED_FINAL_ASSAY_SIGMA[metric],
                "normalized": normalized,
            }
        maximum = max(row["normalized"] for row in metric_residuals.values())
        if maximum >= SCALAR_NULL_MINIMUM_NORMALIZED_RESIDUAL:
            resolving_cells.add(cell_id)
        held_out.append(
            {
                "cell_id": cell_id,
                "metric_residuals": metric_residuals,
                "maximum_normalized_residual": maximum,
            }
        )
    return {
        "fit_cells": list(SCALAR_NULL_FIT_CELLS),
        "held_out_cells": list(SCALAR_NULL_HELD_OUT_CELLS),
        "candidate_multipliers": list(SCALAR_NULL_MULTIPLIERS),
        "fit_normalized_mean_squared_error": fit_scores,
        "selected_multiplier": best_multiplier,
        "held_out_reports": held_out,
        "resolving_held_out_cells": sorted(resolving_cells),
        "minimum_normalized_residual": SCALAR_NULL_MINIMUM_NORMALIZED_RESIDUAL,
        "minimum_resolving_held_out_cells": SCALAR_NULL_MINIMUM_HELD_OUT_CELLS,
        "complete_held_out_denominator": len(held_out) == len(SCALAR_NULL_HELD_OUT_CELLS),
        "passed": (
            len(held_out) == len(SCALAR_NULL_HELD_OUT_CELLS)
            and len(resolving_cells) >= SCALAR_NULL_MINIMUM_HELD_OUT_CELLS
        ),
    }


def analyze_world(
    rows: Sequence[Mapping[str, Any]],
    scalar_rows: Sequence[Mapping[str, Any]],
    private_audit: Mapping[str, Any],
) -> dict[str, Any]:
    keyed = {(str(row["cell_id"]), str(row["law_id"])): row for row in rows}
    cells = sorted({str(row["cell_id"]) for row in rows})
    pairs = [
        (
            keyed[(cell, "supersaturation_transfer_parent")],
            keyed[(cell, "surface_saturation_occlusion")],
        )
        for cell in cells
    ]
    checks = {
        "fixed_execution_denominator": len(rows) == 16 and len(pairs) == 8,
        "all_completed": all(row.get("status") == "completed" for row in rows),
        "all_exact_replay": all(row.get("exact_replay") is True for row in rows),
        "truth_binding_verified": all(row.get("truth_binding_verified") is True for row in rows),
        "paired_action_plans": all(
            parent.get("action_plan_sha256") == child.get("action_plan_sha256")
            for parent, child in pairs
        ),
        "paired_observation_noise": all(
            parent.get("observation_coordinate_sha256")
            == child.get("observation_coordinate_sha256")
            for parent, child in pairs
        ),
        "participant_visible_leakage_free": all(
            not row.get("participant_visible_leakage_matches") for row in rows
        ),
        "private_world_hash_changed": (private_audit.get("private_world_hash_changed") is True),
        "child_hash_deterministic": private_audit.get("child_hash_deterministic") is True,
        "scalar_null_fixed_execution_denominator": (
            len(scalar_rows)
            == len(SCALAR_NULL_FIT_CELLS) * len(SCALAR_NULL_MULTIPLIERS)
            + len(SCALAR_NULL_HELD_OUT_CELLS)
        ),
        "scalar_null_all_completed": all(
            row.get("status") == "completed" for row in scalar_rows
        ),
        "scalar_null_all_exact_replay": all(
            row.get("exact_replay") is True for row in scalar_rows
        ),
        "scalar_null_truth_binding_verified": all(
            row.get("truth_binding_verified") is True for row in scalar_rows
        ),
        "scalar_null_participant_visible_leakage_free": all(
            not row.get("participant_visible_leakage_matches") for row in scalar_rows
        ),
        "executable_occlusion_law_switched": bool(
            private_audit["parent_occlusion_law_id"]
            == "linear_supersaturation_transfer_v1"
            and private_audit["child_occlusion_law_id"]
            == "surface_saturation_occlusion_v1"
        ),
    }
    metric_reports = {}
    supporting_cells: set[str] = set()
    for metric in METRICS:
        effect_gate = PURITY_EFFECT_GATE if metric == "crystal_purity" else EFFECT_GATE
        cell_gaps = []
        for parent, child in pairs:
            gap = float(child["metrics"][metric]) - float(parent["metrics"][metric])
            cell_gaps.append(
                {
                    "cell_id": parent["cell_id"],
                    "seed_index": int(parent["seed_index"]),
                    "temperature_index": int(parent["temperature_index"]),
                    "duration_index": int(parent["duration_index"]),
                    "signed_gap": gap,
                }
            )
            if abs(gap) >= effect_gate:
                supporting_cells.add(str(parent["cell_id"]))
        maximum = max(abs(row["signed_gap"]) for row in cell_gaps)
        metric_reports[metric] = {
            "effect_gate": effect_gate,
            "max_absolute_paired_gap": maximum,
            "effect_passed": maximum >= effect_gate,
            "cell_gaps": cell_gaps,
        }
    resolving_metrics = sum(row["effect_passed"] for row in metric_reports.values())
    coordinates = {
        str(row["cell_id"]): (
            int(row["seed_index"]),
            int(row["temperature_index"]),
            int(row["duration_index"]),
        )
        for row in rows
    }
    separated_support = any(
        sum(
            left_value != right_value
            for left_value, right_value in zip(coordinates[left], coordinates[right], strict=True)
        )
        >= 2
        for left, right in itertools.combinations(sorted(supporting_cells), 2)
    )
    interactions = []
    for metric in METRICS:
        gaps = {
            (
                int(row["seed_index"]),
                int(row["temperature_index"]),
                int(row["duration_index"]),
            ): float(row["signed_gap"])
            for row in metric_reports[metric]["cell_gaps"]
        }
        seed_interaction = max(
            abs(gaps[(1, temperature, duration)] - gaps[(0, temperature, duration)])
            for temperature in (0, 1)
            for duration in (0, 1)
        )
        cooling_interaction = max(
            abs(gaps[(seed, 1, duration)] - gaps[(seed, 0, duration)])
            for seed in (0, 1)
            for duration in (0, 1)
        )
        interactions.append(
            {
                "metric": metric,
                "seed_by_law": seed_interaction,
                "cooling_by_law": cooling_interaction,
                "maximum": max(seed_interaction, cooling_interaction),
            }
        )
    maximum_interaction = max(row["maximum"] for row in interactions)
    scalar_null = _scalar_null_analysis(pairs, scalar_rows)

    def purity_constrained_best(law_index: int) -> Mapping[str, Any]:
        candidates = [pair[law_index] for pair in pairs]
        feasible = [
            row
            for row in candidates
            if float(row["metrics"]["crystal_purity"]) >= PURITY_CONSTRAINT
        ]
        if feasible:
            return max(
                feasible,
                key=lambda row: (
                    float(row["metrics"]["crystal_yield"]),
                    float(row["metrics"]["crystal_csd_quality"]),
                    -float(row["metrics"]["crystal_fines_fraction"]),
                ),
            )
        return max(candidates, key=lambda row: float(row["metrics"]["crystal_purity"]))

    parent_best = purity_constrained_best(0)
    child_best = purity_constrained_best(1)
    decision_fields = ("seed_index", "temperature_index", "duration_index")
    decision_changes = [
        field for field in decision_fields if int(parent_best[field]) != int(child_best[field])
    ]
    checks.update(
        {
            "at_least_two_public_endpoints_resolve": resolving_metrics >= 2,
            "purity_endpoint_resolves": metric_reports["crystal_purity"]["effect_passed"],
            "two_separated_supporting_cells": separated_support,
            "non_scalar_interaction_signature": any(
                row["maximum"]
                >= (PURITY_EFFECT_GATE if row["metric"] == "crystal_purity" else EFFECT_GATE)
                for row in interactions
            ),
            "task_decision_changes": bool(decision_changes),
            "best_constant_multiplier_rejected_on_held_out_cells": scalar_null["passed"],
        }
    )
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "failures": sorted(key for key, value in checks.items() if not value),
        "resolving_metric_count": resolving_metrics,
        "metric_reports": metric_reports,
        "supporting_cells": sorted(supporting_cells),
        "interaction_reports": interactions,
        "maximum_interaction": maximum_interaction,
        "parent_best_cell": parent_best["cell_id"],
        "child_best_cell": child_best["cell_id"],
        "decision_changes": decision_changes,
        "decision_rule": {
            "purity_constraint": PURITY_CONSTRAINT,
            "primary_objective": "crystal_yield",
            "secondary_objective": "crystal_csd_quality",
            "fallback_if_infeasible": "maximize_crystal_purity",
        },
        "private_fork_audit": dict(private_audit),
        "scalar_null": scalar_null,
    }


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    machine_contract, contract = _load_machine_contract(contract_path)
    config = _campaign_config(contract)
    design = _design(contract)
    output.mkdir(parents=True)
    scalar_fit_executions = len(SCALAR_NULL_FIT_CELLS) * len(SCALAR_NULL_MULTIPLIERS)
    scalar_held_out_executions = len(SCALAR_NULL_HELD_OUT_CELLS)
    total = len(CALIBRATION_SEEDS) * (
        len(design) * len(LAW_IDS)
        + scalar_fit_executions
        + scalar_held_out_executions
    )
    completed = 0
    exact_replays = 0
    worlds = []
    for index, world_seed in enumerate(CALIBRATION_SEEDS, start=1):
        world_id = f"C-S-CAL{index:02d}"
        world = {"world_id": world_id, "world_seed": world_seed, "world_interventions": []}
        world_root = output / world_id
        world_root.mkdir()
        receipts = []
        design_by_cell = {str(row["cell_id"]): row for row in design}
        for cell in design:
            observation_seed = _stable_seed(
                "experiment-1-v1.2-c-structural-authoring",
                world_seed,
                cell["cell_id"],
            )
            for law_id in LAW_IDS:
                law_root = world_root / law_id
                law_root.mkdir(exist_ok=True)
                additional = (
                    []
                    if law_id == "supersaturation_transfer_parent"
                    else [surface_saturation_intervention()]
                )
                receipt = _execute(
                    contract=contract,
                    config=config,
                    world=world,
                    query_spec=cell["query_spec"],
                    observation_seed=observation_seed,
                    namespace="experiment-1-v1.2-c-structural-authoring",
                    output_root=law_root,
                    extra={
                        "cell_id": cell["cell_id"],
                        "law_id": law_id,
                        "seed_index": cell["seed_index"],
                        "temperature_index": cell["temperature_index"],
                        "duration_index": cell["duration_index"],
                    },
                    additional_world_interventions=additional,
                )
                receipts.append(receipt)
                completed += 1
                exact_replays += int(receipt.get("exact_replay") is True)
                if completed % 4 == 0:
                    print(
                        json.dumps(
                            {
                                "event": "c_structural_authoring_progress",
                                "completed": completed,
                                "total": total,
                                "world_id": world_id,
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
        child_by_cell = {
            str(row["cell_id"]): row
            for row in receipts
            if row["law_id"] == "surface_saturation_occlusion"
        }
        scalar_receipts = []
        for cell_id in SCALAR_NULL_FIT_CELLS:
            cell = design_by_cell[cell_id]
            observation_seed = int(child_by_cell[cell_id]["observation_seed"])
            for multiplier in SCALAR_NULL_MULTIPLIERS:
                scalar_root = world_root / f"scalar-null-{multiplier:g}"
                scalar_root.mkdir(exist_ok=True)
                receipt = _execute(
                    contract=contract,
                    config=config,
                    world=world,
                    query_spec=cell["query_spec"],
                    observation_seed=observation_seed,
                    namespace="experiment-1-v1.2-c-structural-authoring",
                    output_root=scalar_root,
                    extra={
                        "cell_id": cell_id,
                        "law_id": "constant_capacity_scalar_null",
                        "scalar_null_multiplier": multiplier,
                        "scalar_null_role": "fit",
                        "seed_index": cell["seed_index"],
                        "temperature_index": cell["temperature_index"],
                        "duration_index": cell["duration_index"],
                    },
                    additional_world_interventions=scalar_null_intervention(multiplier),
                )
                scalar_receipts.append(receipt)
                completed += 1
                exact_replays += int(receipt.get("exact_replay") is True)
        provisional = _scalar_null_analysis(
            [
                (
                    next(
                        row
                        for row in receipts
                        if row["cell_id"] == cell_id
                        and row["law_id"] == "supersaturation_transfer_parent"
                    ),
                    child_by_cell[cell_id],
                )
                for cell_id in sorted(child_by_cell)
            ],
            scalar_receipts,
        )
        best_multiplier = float(provisional["selected_multiplier"])
        for cell_id in SCALAR_NULL_HELD_OUT_CELLS:
            cell = design_by_cell[cell_id]
            scalar_root = world_root / f"scalar-null-{best_multiplier:g}"
            scalar_root.mkdir(exist_ok=True)
            receipt = _execute(
                contract=contract,
                config=config,
                world=world,
                query_spec=cell["query_spec"],
                observation_seed=int(child_by_cell[cell_id]["observation_seed"]),
                namespace="experiment-1-v1.2-c-structural-authoring",
                output_root=scalar_root,
                extra={
                    "cell_id": cell_id,
                    "law_id": "constant_capacity_scalar_null",
                    "scalar_null_multiplier": best_multiplier,
                    "scalar_null_role": "held_out",
                    "seed_index": cell["seed_index"],
                    "temperature_index": cell["temperature_index"],
                    "duration_index": cell["duration_index"],
                },
                additional_world_interventions=scalar_null_intervention(best_multiplier),
            )
            scalar_receipts.append(receipt)
            completed += 1
            exact_replays += int(receipt.get("exact_replay") is True)
        write_json_atomic(world_root / "receipts.json", receipts)
        write_json_atomic(world_root / "scalar-null-receipts.json", scalar_receipts)
        analysis = analyze_world(receipts, scalar_receipts, _private_fork_audit(world_seed))
        result = {"world_id": world_id, "world_seed": world_seed, **analysis}
        write_json_atomic(world_root / "analysis.json", result)
        worlds.append(result)
    passed_worlds = sum(world["passed"] for world in worlds)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-c-structural-authoring-1.2.0",
        "formal_result": False,
        "provider_call_count": 0,
        "benchmark_denominator": False,
        "calibration_world_seeds": list(CALIBRATION_SEEDS),
        "planned_executions": total,
        "completed_executions": completed,
        "exact_replays": exact_replays,
        "qualified_calibration_worlds": passed_worlds,
        "selected_candidate": (
            "surface_saturation_occlusion" if passed_worlds == len(worlds) else None
        ),
        "worlds": worlds,
        "machine_contract_sha256": file_sha256(contract_path),
        "machine_contract_self_sha256": machine_contract["contract_sha256"],
        "note_sha256": machine_contract["authoring_note"]["sha256"],
        "resolved_contract_sha256": canonical_json_sha256(contract),
        "contract_file_sha256": file_sha256(contract_path),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.contract.resolve(), args.output.resolve())
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["selected_candidate"] is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
