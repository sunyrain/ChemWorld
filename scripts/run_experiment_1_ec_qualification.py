#!/usr/bin/env python3
"""Run the frozen Experiment 1 EC-W00 or EC entity qualification block."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_ec_qualification import (
    analyze_entity_world,
    entity_prior_audit,
    load_contract,
    private_world_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    build_blind_policy_schedule,
    execute_one,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_ec_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-ec-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-ec-entity-summary-1.0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _plan(contract: dict[str, Any]) -> dict[str, Any]:
    campaign_binding = contract["task"]["campaign_config"]
    campaign = _load(ROOT / campaign_binding["path"])
    plan: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-ec-entity-plan-1.0.1",
        "development_only": True,
        "task_bindings": [
            {
                "task_id": contract["task"]["task_id"],
                "campaign_config": campaign_binding["path"],
                "campaign_config_sha256": canonical_json_sha256(campaign),
            }
        ],
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _policy(contract: dict[str, Any]) -> dict[str, Any]:
    entity = contract["loci"]["entity"]
    return {
        "nuisance_design": entity["nuisance_design"],
        "category_order_by_anchor": entity["category_order_by_anchor"],
    }


def _row(
    contract: dict[str, Any],
    *,
    world_id: str,
    world_seed: int,
    schedule_row: dict[str, Any],
    replicate: int,
    execution_index: int,
) -> dict[str, Any]:
    entity = contract["loci"]["entity"]
    task_id = contract["task"]["task_id"]
    support = [entity["gate_endpoint_id"], *entity["support_endpoint_ids"]]
    execution_id = (
        f"{world_id}-a{schedule_row['nuisance_anchor']}-"
        f"c{schedule_row['target_category']}-r{replicate}"
    )
    return {
        "execution_id": execution_id,
        "execution_index": execution_index,
        "phase": "experiment_1_ec_entity_qualification",
        "task_id": task_id,
        "world_id": world_id,
        "world_seed": world_seed,
        "replicate": replicate,
        "policy_replicate": replicate,
        "nuisance_anchor": schedule_row["nuisance_anchor"],
        "target_category": schedule_row["target_category"],
        "recipe_id": schedule_row["recipe_id"],
        "recipe": schedule_row["recipe"],
        "observation_seed": _stable_seed(
            entity["observation_noise_namespace"],
            world_id,
            schedule_row["nuisance_anchor"],
            schedule_row["target_category"],
            replicate,
        ),
        "observation_noise_namespace": entity["observation_noise_namespace"],
        "allowed_metric_ids": support,
        "support_metric_ids": support,
        "negative_control_metric_ids": [],
    }


def _schedule(contract: dict[str, Any]) -> list[dict[str, Any]]:
    return build_blind_policy_schedule(
        task_id=contract["task"]["task_id"],
        target_field=contract["loci"]["entity"]["target_field"],
        policy=_policy(contract),
    )


def run_canary(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    plan = _plan(contract)
    canary = contract["worlds"]["canary"]
    row = _row(
        contract,
        world_id=canary["world_id"],
        world_seed=int(canary["world_seed"]),
        schedule_row=_schedule(contract)[0],
        replicate=0,
        execution_index=0,
    )
    receipt = execute_one(ROOT, plan, row, output)
    prior = entity_prior_audit(contract)
    private = private_world_audit(contract, world_seed=int(canary["world_seed"]))
    passed = (
        receipt.get("status") == "completed"
        and isinstance(receipt.get("exact_replay"), dict)
        and receipt["exact_replay"].get("verified") is True
        and prior["passed"] is True
        and private["aligned_mapping_not_reversed"] is True
    )
    summary: dict[str, Any] = {
        "schema_version": CANARY_SUMMARY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "world_id": canary["world_id"],
        "world_seed": canary["world_seed"],
        "formal_denominator": False,
        "contract_sha256": canonical_json_sha256(contract),
        "receipt": receipt,
        "prior_audit": {
            key: value
            for key, value in prior.items()
            if key not in {"aligned", "misspecified"}
        },
        "private_world_audit": private,
        "passed": passed,
        "decision": "proceed_to_ec_w01_w05" if passed else "stop_before_ec_w01_w05",
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_entity(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    plan = _plan(contract)
    schedule = _schedule(contract)
    replicates = int(contract["loci"]["entity"]["independent_replicates"])
    reports = []
    all_receipts = []
    execution_index = 0
    for world in contract["worlds"]["qualification"]:
        world_root = output / world["world_id"]
        world_root.mkdir()
        receipts = []
        for schedule_row in schedule:
            for replicate in range(replicates):
                row = _row(
                    contract,
                    world_id=world["world_id"],
                    world_seed=int(world["world_seed"]),
                    schedule_row=schedule_row,
                    replicate=replicate,
                    execution_index=execution_index,
                )
                receipt = execute_one(ROOT, plan, row, world_root)
                receipts.append(receipt)
                all_receipts.append(receipt)
                execution_index += 1
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_entity_world(
            contract,
            world_id=world["world_id"],
            world_seed=int(world["world_seed"]),
            receipts=receipts,
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        print(
            json.dumps(
                {
                    "event": "entity_world_complete",
                    "world_id": world["world_id"],
                    "completed_worlds": len(reports),
                    "total_worlds": 5,
                    "status": report["status"],
                    "failures": report["failures"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    summary: dict[str, Any] = {
        "schema_version": ENTITY_SUMMARY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "contract_sha256": canonical_json_sha256(contract),
        "denominators": {
            "worlds": 5,
            "planned_executions": 5 * len(schedule) * replicates,
            "attempted_executions": len(all_receipts),
            "completed_executions": sum(row.get("status") == "completed" for row in all_receipts),
            "exact_replays": sum(
                isinstance(row.get("exact_replay"), dict)
                and row["exact_replay"].get("verified") is True
                for row in all_receipts
            ),
        },
        "worlds": [
            {
                "world_id": report["world_id"],
                "world_seed": report["world_seed"],
                "status": report["status"],
                "failures": report["failures"],
                "truth_sha256": report["private_world_audit"]["truth_sha256"],
                "report_sha256": report["report_sha256"],
            }
            for report in reports
        ],
        "five_world_qualified": all(report["status"] == "qualified" for report in reports),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--phase", choices=("canary", "entity"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract_path = args.contract.resolve()
    contract = load_contract(ROOT, contract_path)
    summary = (
        run_canary(contract, args.output.resolve())
        if args.phase == "canary"
        else run_entity(contract, args.output.resolve())
    )
    print(
        json.dumps(
            {
                "phase": args.phase,
                "output": str(args.output),
                "passed": summary.get("passed", summary.get("five_world_qualified")),
                "summary_sha256": summary["summary_sha256"],
                "contract_path": contract_path.relative_to(ROOT).as_posix(),
                "contract_file_sha256": file_sha256(contract_path),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary.get("passed", summary.get("five_world_qualified")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
