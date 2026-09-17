#!/usr/bin/env python3
"""Run the frozen Experiment 1 EC-W00 or EC entity qualification block."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.eval.experiment_1_ec_qualification import (
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
    entity_prior_audit,
    load_contract,
    private_world_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    build_blind_policy_schedule,
    execute_one,
)
from chemworld.eval.work_ii_electrochemical_matched_prior_qualification import (
    analyze_matched_prior_world,
    rounded_reference_context,
    surface_design,
)
from chemworld.eval.work_ii_structural_candidate_qualification import (
    analyze_candidate_world as analyze_legacy_structural_world,
)
from chemworld.eval.work_ii_structural_candidate_qualification import (
    candidate_specs as structural_candidate_specs,
)
from chemworld.eval.work_ii_structural_candidate_qualification import (
    registered_queries as structural_registered_queries,
)

try:
    from scripts.run_work_ii_mechanism_oracle_qualification import (
        InMemoryMechanismEvaluator,
    )
    from scripts.run_work_ii_q1_response_surface import TASK_SPECS
    from scripts.run_work_ii_structural_candidate_qualification import (
        _execute_query as execute_structural_query,
    )
except ModuleNotFoundError:
    from run_work_ii_mechanism_oracle_qualification import InMemoryMechanismEvaluator
    from run_work_ii_q1_response_surface import TASK_SPECS
    from run_work_ii_structural_candidate_qualification import (
        _execute_query as execute_structural_query,
    )

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_ec_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-ec-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-ec-entity-summary-1.0.1"
PARAMETRIC_SUMMARY_VERSION = "chemworld-experiment-1-ec-parametric-summary-1.0.1"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-ec-structural-summary-1.0.1"


class Progress:
    def __init__(self, total: int, *, event: str = "experiment_1_ec_entity_progress") -> None:
        self.total = total
        self.event = event
        self.completed = 0
        self.started = perf_counter()
        self.last_emit = self.started

    def update(self, *, world_id: str, status: str) -> None:
        self.completed += 1
        now = perf_counter()
        if self.completed % 4 != 0 and now - self.last_emit < 30.0:
            return
        elapsed = now - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        print(
            json.dumps(
                {
                    "event": self.event,
                    "world_id": world_id,
                    "last_execution_status": status,
                    "completed": self.completed,
                    "total": self.total,
                    "throughput_executions_per_minute": round(rate * 60.0, 2),
                    "eta_s": round((self.total - self.completed) / rate, 1) if rate else None,
                    "elapsed_s": round(elapsed, 1),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        self.last_emit = now


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
    progress = Progress(5 * len(schedule) * replicates)
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
                progress.update(world_id=world["world_id"], status=str(receipt["status"]))
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


def _replay_projection(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "elapsed_s"}


def _self_hashed_summary(path: Path) -> dict[str, Any]:
    value = _load(path)
    digest = value.get("summary_sha256")
    payload = {key: item for key, item in value.items() if key != "summary_sha256"}
    if digest != canonical_json_sha256(payload):
        raise ValueError(f"source summary self-hash mismatch: {path}")
    return value


def _parametric_frozen_sources(
    contract: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    bindings = contract["source_assets"]
    reference_binding = bindings["parametric_reference_summary"]
    noise_binding = bindings["parametric_noise_summary"]
    reference_path = ROOT / str(reference_binding["path"])
    noise_path = ROOT / str(noise_binding["path"])
    reference = _self_hashed_summary(reference_path)
    noise = _self_hashed_summary(noise_path)
    if reference.get("qualification_passed") is not True or noise.get("q2_authorized") is not True:
        raise ValueError("frozen parametric source summaries are not qualified for design reuse")
    reference_worlds = reference.get("worlds")
    noise_worlds = noise.get("worlds")
    if not isinstance(reference_worlds, list) or not isinstance(noise_worlds, list):
        raise ValueError("frozen parametric source summaries lack world rows")
    reference_worlds = sorted(reference_worlds, key=lambda row: int(row["world_seed"]))
    noise_worlds = sorted(noise_worlds, key=lambda row: int(row["world_seed"]))
    expected = list(range(5))
    if [int(row["world_seed"]) for row in reference_worlds] != expected:
        raise ValueError("frozen parametric reference worlds changed")
    if [int(row["world_seed"]) for row in noise_worlds] != expected:
        raise ValueError("frozen parametric noise worlds changed")
    return (
        reference_worlds,
        noise_worlds,
        [
            {
                "path": reference_binding["path"],
                "sha256": reference_binding["sha256"],
            },
            {"path": noise_binding["path"], "sha256": noise_binding["sha256"]},
        ],
    )


def _five_world_summary(
    *,
    schema_version: str,
    contract: Mapping[str, Any],
    locus: str,
    reports: list[Mapping[str, Any]],
    planned_executions: int,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "schema_version": schema_version,
        "formal_result": False,
        "provider_call_count": 0,
        "contract_sha256": canonical_json_sha256(contract),
        "prior_locus": locus,
        "denominators": {
            "worlds": 5,
            "planned_executions": planned_executions,
            "attempted_executions": sum(
                int(report["denominators"]["attempted"]) for report in reports
            ),
            "classified_executions": sum(
                int(
                    report["denominators"].get(
                        "classified", report["denominators"].get("completed", 0)
                    )
                )
                for report in reports
            ),
            "exact_replays": sum(
                int(report["denominators"]["exact_replay"]) for report in reports
            ),
            "platform_failures": sum(
                int(report["denominators"].get("platform_failures", 0))
                for report in reports
            ),
            "physical_failures": sum(
                int(report["denominators"].get("physical_failures", 0))
                for report in reports
            ),
        },
        "worlds": [
            {
                "world_id": report["world_id"],
                "world_seed": report["world_seed"],
                "status": report["status"],
                "failures": report["failures"],
                "report_sha256": report["report_sha256"],
            }
            for report in reports
        ],
        "five_world_qualified": all(report["status"] == "qualified" for report in reports),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    return summary


def run_parametric(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    references, noise_sources, source_bindings = _parametric_frozen_sources(contract)
    spec = TASK_SPECS[contract["task"]["task_id"]]
    config = _load(ROOT / str(spec["config"]))
    reports: list[dict[str, Any]] = []
    progress = Progress(5 * 121, event="experiment_1_ec_parametric_progress")
    for world, reference, noise_source in zip(
        contract["worlds"]["qualification"],
        references,
        noise_sources,
        strict=True,
    ):
        world_root = output / world["world_id"]
        world_root.mkdir()
        selected = reference["reference_selection"]
        reference_context = rounded_reference_context(selected["vector"])
        if reference_context != reference["reference_context"]:
            raise ValueError(f"frozen reference context drifted for {world['world_id']}")
        design = surface_design(reference_context)
        primary = InMemoryMechanismEvaluator(
            task_id=contract["task"]["task_id"],
            config=config,
            spec=spec,
            world_seed=int(world["world_seed"]),
        )
        replay = InMemoryMechanismEvaluator(
            task_id=contract["task"]["task_id"],
            config=config,
            spec=spec,
            world_seed=int(world["world_seed"]),
        )
        rows = []
        try:
            for design_row in design:
                extra = {key: value for key, value in design_row.items() if key != "vector"}
                observed = primary.evaluate(
                    design_row["vector"],
                    phase="experiment_1_ec_parametric_surface",
                    extra=extra,
                )
                repeated = replay.evaluate(
                    design_row["vector"],
                    phase="experiment_1_ec_parametric_surface",
                    extra=extra,
                )
                observed_hash = canonical_json_sha256(_replay_projection(observed))
                repeated_hash = canonical_json_sha256(_replay_projection(repeated))
                observed["exact_replay"] = {
                    "verified": observed_hash == repeated_hash,
                    "primary_sha256": observed_hash,
                    "replay_sha256": repeated_hash,
                }
                rows.append(observed)
                progress.update(world_id=world["world_id"], status=str(observed["status"]))
        finally:
            primary.close()
            replay.close()
        write_json_atomic(world_root / "surface-rows.json", rows)
        sigma = float(noise_source["analysis"]["validation_noise"]["sigma"] or 0.0)
        legacy = analyze_matched_prior_world(
            rows,
            validation_sigma=sigma,
            reference_context=reference_context,
            world_token=f"{contract['task']['task_id']}:{world['world_seed']}",
        )
        private = private_world_audit(contract, world_seed=int(world["world_seed"]))
        report = analyze_parametric_world(
            contract,
            world_id=str(world["world_id"]),
            world_seed=int(world["world_seed"]),
            rows=rows,
            analysis=legacy,
            source_truth_sha256=str(private["truth_sha256"]),
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        print(
            json.dumps(
                {
                    "event": "parametric_world_complete",
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
    summary = _five_world_summary(
        schema_version=PARAMETRIC_SUMMARY_VERSION,
        contract=contract,
        locus="parametric",
        reports=reports,
        planned_executions=5 * 121,
    )
    summary["source_summaries"] = source_bindings
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    candidate_id = str(contract["loci"]["structural"]["candidate_id"])
    candidate = structural_candidate_specs()[candidate_id]
    config = _load(ROOT / str(candidate["config"]))
    design = structural_registered_queries(candidate_id)
    reports: list[dict[str, Any]] = []
    progress = Progress(5 * len(design), event="experiment_1_ec_structural_progress")
    for world in contract["worlds"]["qualification"]:
        world_root = output / world["world_id"]
        world_root.mkdir()
        rows = []
        for query in design:
            row = execute_structural_query(
                candidate_id=candidate_id,
                config=config,
                world_seed=int(world["world_seed"]),
                query_spec=query,
                output_root=world_root,
            )
            rows.append(row)
            progress.update(world_id=world["world_id"], status=str(row["status"]))
        write_json_atomic(world_root / "rows.json", rows)
        legacy = analyze_legacy_structural_world(candidate_id, rows)
        private = private_world_audit(contract, world_seed=int(world["world_seed"]))
        report = analyze_structural_world(
            contract,
            world_id=str(world["world_id"]),
            world_seed=int(world["world_seed"]),
            rows=rows,
            analysis=legacy,
            truth_sha256=str(private["truth_sha256"]),
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        print(
            json.dumps(
                {
                    "event": "structural_world_complete",
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
    summary = _five_world_summary(
        schema_version=STRUCTURAL_SUMMARY_VERSION,
        contract=contract,
        locus="structural",
        reports=reports,
        planned_executions=5 * len(design),
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--phase",
        choices=("canary", "entity", "parametric", "structural"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract_path = args.contract.resolve()
    contract = load_contract(ROOT, contract_path)
    runners = {
        "canary": run_canary,
        "entity": run_entity,
        "parametric": run_parametric,
        "structural": run_structural,
    }
    summary = runners[args.phase](contract, args.output.resolve())
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
