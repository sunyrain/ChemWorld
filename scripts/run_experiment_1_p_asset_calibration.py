#!/usr/bin/env python3
"""Run a frozen, provider-free Experiment 1 P asset calibration contract.

No calibration contract is shipped by the asset-build commit.  Execution is therefore
fail-closed until a later preregistered note and machine contract bind the design.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_p_assets import structural_intervention
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "reaction-to-purification"


def _self_hash(value: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: item for key, item in value.items() if key != field})


def load_calibration_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "chemworld-experiment-1-p-calibration-contract-1.0.0":
        raise ValueError("P calibration contract schema changed")
    if value.get("status") != "frozen_before_calibration":
        raise ValueError("P calibration contract is not frozen")
    if value.get("formal_qualification_authorized") is not False:
        raise ValueError("P calibration contract must not authorize formal qualification")
    if value.get("contract_sha256") != _self_hash(value, "contract_sha256"):
        raise ValueError("P calibration contract self-hash changed")
    for binding_name in ("calibration_note", "asset_manifest", "asset_contract"):
        binding = value.get(binding_name, {})
        target = ROOT / str(binding.get("path", ""))
        if not target.is_file() or file_sha256(target) != binding.get("sha256"):
            raise ValueError(f"P calibration {binding_name} binding changed")
    manifest_path = ROOT / str(value["asset_manifest"]["path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("manifest_sha256") != _self_hash(manifest, "manifest_sha256"):
        raise ValueError("P asset manifest self-hash changed")
    return value


def frozen_action_plan(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
        {"operation": "add_reagent", "amount_mol": float(cell["reagent_mol"])},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.00025,
            "catalyst": 1,
        },
        {
            "operation": "heat",
            "target_temperature_K": 385.0,
            "duration_s": 1500.0,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "quench"},
        {
            "operation": "add_phase",
            "phase": "aqueous",
            "volume_L": float(cell["aqueous_volume_L"]),
        },
        {
            "operation": "add_extractant",
            "extractant": int(cell["extractant"]),
            "volume_L": float(cell["extractant_volume_L"]),
        },
        {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
        {"operation": "settle", "duration_s": 420.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    contract = load_calibration_contract(contract_path)
    asset_contract_path = ROOT / str(contract["asset_contract"]["path"])
    asset_contract = json.loads(asset_contract_path.read_text(encoding="utf-8"))
    worlds_by_id = {str(row["world_id"]): row for row in asset_contract["worlds"]}
    output.mkdir(parents=True)
    receipts = []
    for cell in contract["cells"]:
        world = worlds_by_id[str(cell["world_id"])]
        actions = frozen_action_plan(cell)
        for law_id in ("constant_K", "composition_coupled"):
            interventions = [dict(item) for item in world["world_interventions"]]
            if law_id == "composition_coupled":
                interventions.append(structural_intervention(asset_contract))
            execution_root = output / str(cell["cell_id"]) / law_id
            execution_root.mkdir(parents=True)
            trajectory = execution_root / "trajectory.jsonl"
            run_agent(
                env_id=get_task(TASK_ID).env_id,
                agent=_FrozenTruthReplayAgent(actions),
                world_split=str(get_task(TASK_ID).world_split),
                budget=len(actions),
                objective="balanced",
                seed=int(world["world_seed"]),
                agent_seed=0,
                observation_seed=int(cell["observation_seed"]),
                task_id=TASK_ID,
                output_path=trajectory,
                budget_override=len(actions),
                episode_mode_override="single_experiment",
                observation_noise_mode="keyed",
                observation_noise_namespace=str(contract["observation_noise_namespace"]),
                world_interventions=interventions,
            )
            records = load_jsonl(trajectory)
            replay = verify_records(
                records, tolerance=0.0, world_interventions=interventions
            ).to_dict()
            receipt = {
                "cell_id": cell["cell_id"],
                "world_id": cell["world_id"],
                "law_id": law_id,
                "action_plan_sha256": canonical_json_sha256(actions),
                "exact_replay": replay.get("verified") is True,
                "trajectory": {
                    "path": trajectory.relative_to(ROOT).as_posix(),
                    "sha256": file_sha256(trajectory),
                },
            }
            receipt["receipt_sha256"] = canonical_json_sha256(receipt)
            receipts.append(receipt)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-p-calibration-summary-1.0.0",
        "formal_qualification_result": False,
        "provider_call_count": 0,
        "planned_executions": 2 * len(contract["cells"]),
        "completed_executions": len(receipts),
        "all_exact_replay": all(row["exact_replay"] for row in receipts),
        "contract_sha256": file_sha256(contract_path),
        "receipts": receipts,
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.contract.resolve(), args.output.resolve()), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
