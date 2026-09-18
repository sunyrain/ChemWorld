#!/usr/bin/env python3
"""Calibrate the final Experiment 1 C-S impurity-occlusion-law candidate."""

from __future__ import annotations

import argparse
import itertools
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_c_qualification import load_contract
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
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
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_c_parametric_repair_v1.0.2.json"
NOTE = (
    ROOT / "workstreams/flagship_tasks/experiment_1/systems/C/"
    "STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_2_0.md"
)
NOTE_SHA256 = "4c9efcf6955c1b1c13094b38f8974b3dec24942dc61a346a7f80dbd13402c310"
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


def surface_saturation_intervention() -> dict[str, Any]:
    return {
        "axis_id": "crystallization.impurity-occlusion-law",
        "mode": "extrapolation",
        "severity": 1.0,
    }


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


def analyze_world(
    rows: Sequence[Mapping[str, Any]], private_audit: Mapping[str, Any]
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
    }


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    if file_sha256(NOTE) != NOTE_SHA256:
        raise ValueError("C-S authoring note digest changed")
    contract = load_contract(ROOT, contract_path)
    config = _campaign_config(contract)
    design = _design(contract)
    output.mkdir(parents=True)
    total = len(CALIBRATION_SEEDS) * len(design) * len(LAW_IDS)
    completed = 0
    exact_replays = 0
    worlds = []
    for index, world_seed in enumerate(CALIBRATION_SEEDS, start=1):
        world_id = f"C-S-CAL{index:02d}"
        world = {"world_id": world_id, "world_seed": world_seed, "world_interventions": []}
        world_root = output / world_id
        world_root.mkdir()
        receipts = []
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
        write_json_atomic(world_root / "receipts.json", receipts)
        analysis = analyze_world(receipts, _private_fork_audit(world_seed))
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
        "note_sha256": NOTE_SHA256,
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
