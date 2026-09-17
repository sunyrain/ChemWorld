#!/usr/bin/env python3
"""Run the frozen Experiment 1 EC qualification repair v1.0.2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_ec_qualification_repair import (
    analyze_entity_repair_world,
    analyze_structural_candidate_repair,
    analyze_structural_repair_world,
    entity_prior_audit_repair,
    load_repair_contract,
    private_world_audit_repair,
    structural_repair_queries,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_structural_candidate_qualification import (
    candidate_specs as structural_candidate_specs,
)

try:
    from scripts.run_experiment_1_ec_qualification import (
        Progress,
        _five_world_summary,
        _plan,
        _row,
        _schedule,
    )
    from scripts.run_work_ii_structural_candidate_qualification import (
        _execute_query as execute_structural_query,
    )
except ModuleNotFoundError:
    from run_experiment_1_ec_qualification import (  # type: ignore[no-redef]
        Progress,
        _five_world_summary,
        _plan,
        _row,
        _schedule,
    )
    from run_work_ii_structural_candidate_qualification import (  # type: ignore[no-redef]
        _execute_query as execute_structural_query,
    )

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_ec_qualification_repair_v1.0.2.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-ec-repair-canary-summary-1.0.2"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-ec-repair-entity-summary-1.0.2"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-ec-repair-structural-summary-1.0.2"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def run_canary(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    plan = _plan(contract)
    canary = contract["worlds"]["canary"]
    row = _row(
        contract,
        world_id=str(canary["world_id"]),
        world_seed=int(canary["world_seed"]),
        schedule_row=_schedule(contract)[0],
        replicate=0,
        execution_index=0,
    )
    from chemworld.eval.work_ii_ae_prior_qualification_v02 import execute_one

    receipt = execute_one(ROOT, plan, row, output)
    prior = entity_prior_audit_repair(contract, world_id="EC-W00")
    private = private_world_audit_repair(
        contract, world_id="EC-W00", world_seed=int(canary["world_seed"])
    )
    passed = bool(
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
            key: value for key, value in prior.items() if key not in {"aligned", "misspecified"}
        },
        "private_world_audit": private,
        "passed": passed,
        "decision": "proceed_to_repair_blocks" if passed else "stop_before_repair_blocks",
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_entity(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    from chemworld.eval.work_ii_ae_prior_qualification_v02 import execute_one

    plan = _plan(contract)
    schedule = _schedule(contract)
    replicates = int(contract["loci"]["entity"]["independent_replicates"])
    reports: list[dict[str, Any]] = []
    all_receipts: list[dict[str, Any]] = []
    execution_index = 0
    progress = Progress(
        5 * len(schedule) * replicates,
        event="experiment_1_ec_repair_entity_progress",
    )
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        world_root = output / world_id
        world_root.mkdir()
        receipts: list[dict[str, Any]] = []
        for schedule_row in schedule:
            for replicate in range(replicates):
                row = _row(
                    contract,
                    world_id=world_id,
                    world_seed=world_seed,
                    schedule_row=schedule_row,
                    replicate=replicate,
                    execution_index=execution_index,
                )
                receipt = execute_one(ROOT, plan, row, world_root)
                receipts.append(receipt)
                all_receipts.append(receipt)
                execution_index += 1
                progress.update(world_id=world_id, status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_entity_repair_world(
            contract,
            world_id=world_id,
            world_seed=world_seed,
            receipts=receipts,
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        print(
            json.dumps(
                {
                    "event": "repair_entity_world_complete",
                    "world_id": world_id,
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
        "prior_locus": "entity",
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
                "descriptor_permutation": report["descriptor_permutation"],
                "report_sha256": report["report_sha256"],
            }
            for report in reports
        ],
        "five_world_qualified": all(report["status"] == "qualified" for report in reports),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    candidate_id = str(contract["loci"]["structural"]["candidate_id"])
    candidate = structural_candidate_specs()[candidate_id]
    config = _load(ROOT / str(candidate["config"]))
    design = structural_repair_queries(contract)
    reports: list[dict[str, Any]] = []
    progress = Progress(5 * len(design), event="experiment_1_ec_repair_structural_progress")
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        world_root = output / world_id
        world_root.mkdir()
        rows: list[dict[str, Any]] = []
        for query in design:
            row = execute_structural_query(
                candidate_id=candidate_id,
                config=config,
                world_seed=world_seed,
                query_spec=query,
                output_root=world_root,
            )
            rows.append(row)
            progress.update(world_id=world_id, status=str(row["status"]))
        write_json_atomic(world_root / "rows.json", rows)
        analysis = analyze_structural_candidate_repair(contract, rows)
        private = private_world_audit_repair(contract, world_id=world_id, world_seed=world_seed)
        report = analyze_structural_repair_world(
            contract,
            world_id=world_id,
            world_seed=world_seed,
            rows=rows,
            analysis=analysis,
            truth_sha256=str(private["truth_sha256"]),
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        print(
            json.dumps(
                {
                    "event": "repair_structural_world_complete",
                    "world_id": world_id,
                    "completed_worlds": len(reports),
                    "total_worlds": 5,
                    "status": report["status"],
                    "failures": report["failures"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    summary = _five_world_summary(
        schema_version=STRUCTURAL_SUMMARY_VERSION,
        contract=contract,
        locus="structural",
        reports=reports,
        planned_executions=5 * len(design),
    )
    summary["validation_groups"] = contract["loci"]["structural"]["validation_groups"]
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--phase", choices=("canary", "entity", "structural"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract_path = args.contract.resolve()
    contract = load_repair_contract(ROOT, contract_path)
    runners = {
        "canary": run_canary,
        "entity": run_entity,
        "structural": run_structural,
    }
    summary = runners[args.phase](contract, args.output.resolve())
    passed = summary.get("passed", summary.get("five_world_qualified"))
    print(
        json.dumps(
            {
                "phase": args.phase,
                "output": str(args.output),
                "passed": passed,
                "summary_sha256": summary["summary_sha256"],
                "contract_path": contract_path.relative_to(ROOT).as_posix(),
                "contract_file_sha256": file_sha256(contract_path),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
