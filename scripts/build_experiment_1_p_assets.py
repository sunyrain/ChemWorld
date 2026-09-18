#!/usr/bin/env python3
"""Materialize the authoring-only Experiment 1 P asset manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
from math import log
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_p_assets import (
    build_world_assets,
    load_asset_contract,
    partition_truth,
    structural_intervention,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json"
SOURCE_PATHS = (
    "scripts/build_experiment_1_p_assets.py",
    "scripts/run_experiment_1_p_asset_calibration.py",
    "src/chemworld/eval/experiment_1_p_assets.py",
    "src/chemworld/runtime/phase_separation_services.py",
    "src/chemworld/world/phase_kernel.py",
    "src/chemworld/world/world_family.py",
    "src/chemworld/world/mechanism_family.py",
    "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json",
    "workstreams/flagship_tasks/experiment_1/systems/P/ASSET_AUTHORING_NOTE_V1_1_0.md",
)


def build(contract_path: Path, *, source_commit: str) -> dict[str, Any]:
    contract = load_asset_contract(contract_path)
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    world_assets = build_world_assets(contract)
    worlds = [row["truth"] for row in world_assets]
    anchors = contract["entity"]["feed_anchors"]
    extractant = int(contract["parametric"]["reference_extractant"])
    coupling = float(
        contract["structural"]["composition_coupling_multiplier_at_full_severity"]
    )
    intervention = structural_intervention(contract)
    scenario = get_scenario("reaction-to-purification")
    generator = DefaultScenarioGenerator()
    structural_by_world = []
    for world, asset in zip(contract["worlds"], world_assets, strict=True):
        truth = asset["truth"]
        multipliers = {
            "coefficient_multiplier": float(truth["partition_coefficient_multiplier"]),
            "phase_volume_multiplier": float(truth["partition_phase_volume_multiplier"]),
        }
        rows = []
        for anchor in anchors:
            inputs = {
                "extractant": extractant,
                "product_mol": float(anchor["product_mol"]),
                "impurity_mol": float(anchor["impurity_mol"]),
                **multipliers,
            }
            rows.append(
                {
                    "anchor_id": str(anchor["anchor_id"]),
                    "parent": partition_truth(contract, **inputs),
                    "child": partition_truth(
                        contract,
                        composition_coupling_multiplier=coupling,
                        **inputs,
                    ),
                }
            )
        parent_log_span = abs(log(rows[0]["parent"]["S_star"]) - log(rows[1]["parent"]["S_star"]))
        child_log_span = abs(log(rows[0]["child"]["S_star"]) - log(rows[1]["child"]["S_star"]))
        parent_world = generator.generate(
            scenario,
            int(world["world_seed"]),
            tuple(dict(item) for item in world["world_interventions"]),
        )
        child_world = generator.generate(
            scenario,
            int(world["world_seed"]),
            (*tuple(dict(item) for item in world["world_interventions"]), intervention),
        )
        structural_by_world.append(
            {
                "world_id": truth["world_id"],
                "parent_private_world_id": parent_world.parameters.world_id,
                "child_private_world_id": child_world.parameters.world_id,
                "rows": rows,
                "parent_log_s_star_span": parent_log_span,
                "child_log_s_star_span": child_log_span,
                "private_world_hash_changed": parent_world.parameters.world_id
                != child_world.parameters.world_id,
            }
        )
    source_bindings = [
        {"path": relative, "sha256": file_sha256(ROOT / relative)}
        for relative in SOURCE_PATHS
    ]
    checks = {
        "five_world_rows": len(worlds) == 5,
        "five_distinct_truth_hashes": len({row["truth_sha256"] for row in worlds}) == 5,
        "entity_derangement_has_no_fixed_point": all(
            index != source
            for asset in world_assets
            for index, source in enumerate(asset["entity_dossier"]["permutation"])
        ),
        "entity_prior_schema_symmetric": all(
            set(aligned) == set(misspecified)
            for asset in world_assets
            for aligned, misspecified in zip(
                asset["entity_dossier"]["aligned"],
                asset["entity_dossier"]["misspecified"],
                strict=True,
            )
        ),
        "s_star_band_widths_matched": all(
            asset["parametric_bands"]["aligned"]["log_half_width"]
            == asset["parametric_bands"]["misspecified"]["log_half_width"]
            for asset in world_assets
        ),
        "world_specific_assets_bound": all(
            asset["world_id"] == asset["entity_dossier"]["world_id"]
            == asset["parametric_bands"]["world_id"]
            for asset in world_assets
        ),
        "structural_parent_is_composition_independent": all(
            row["parent_log_s_star_span"] < 1.0e-12 for row in structural_by_world
        ),
        "structural_child_has_composition_response": all(
            row["child_log_s_star_span"] >= 0.10 for row in structural_by_world
        ),
        "structural_private_world_hash_changed": all(
            row["private_world_hash_changed"] for row in structural_by_world
        ),
    }
    result: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-p-asset-build-result-1.1.0",
        "formal_qualification_result": False,
        "participant_execution_authorized": False,
        "provider_call_count": 0,
        "asset_status": (
            "authoring-assets-pass" if all(checks.values()) else "authoring-assets-fail"
        ),
        "checks": checks,
        "failures": sorted(key for key, passed in checks.items() if not passed),
        "denominators": {
            "worlds": len(worlds),
            "extractants_per_world": 4,
            "entity_feed_anchors": len(anchors),
            "structural_feed_anchors_per_world": len(anchors),
        },
        "world_assets": world_assets,
        "structural": {
            "intervention": intervention,
            "worlds": structural_by_world,
        },
        "source_binding": {
            "source_commit": source_commit,
            "files": source_bindings,
            "source_binding_sha256": canonical_json_sha256(
                {"source_commit": source_commit, "files": source_bindings}
            ),
        },
        "contract_sha256": file_sha256(contract_path),
    }
    result["manifest_sha256"] = canonical_json_sha256(result)
    return result


def render(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Experiment 1 P asset build result v1.1.0",
            "",
            f"Status: **{result['asset_status']}**; formal qualification remains unauthorized.",
            "",
            (
                f"- Worlds: `{result['denominators']['worlds']}/5` materialized "
                "with distinct truth hashes."
            ),
            (
                f"- Extractants: `{result['denominators']['extractants_per_world']}` "
                "per World with two feed anchors."
            ),
            "- S* aligned/misspecified bands use identical log half-width.",
            "- Constant-K parent and composition-coupled child share one public task.",
            f"- Failures: `{len(result['failures'])}`.",
            "- Participant/provider calls: `0`.",
            "",
            "This is an authoring asset result, not Q1--Q8 qualification evidence.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    result = build(args.contract.resolve(), source_commit=args.source_commit)
    output.mkdir(parents=True)
    write_json_atomic(output / "asset-build-result.json", result)
    (output / "asset-build-result.md").write_text(render(result), encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["asset_status"] == "authoring-assets-pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
