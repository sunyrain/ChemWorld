#!/usr/bin/env python3
"""Run the frozen Experiment 1 PA qualification v1.0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_pa_qualification import (
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
    entity_prior_audit,
    load_contract,
    structural_prior_arms,
    world_truth_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_partition_constitutive_q0 import (
    constitutive_intervention,
    frozen_nominal_pair_action_plan,
    registered_nominal_pair_cells,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.scoring import PARTITION_S0_EXTRACTION_EFFICIENCY_V3

try:
    from scripts.run_experiment_1_ec_qualification import Progress, _five_world_summary
except ModuleNotFoundError:
    from run_experiment_1_ec_qualification import Progress, _five_world_summary

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_pa_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-pa-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-pa-entity-summary-1.0.1"
PARAMETRIC_SUMMARY_VERSION = "chemworld-experiment-1-pa-parametric-summary-1.0.1"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-pa-structural-summary-1.0.1"
PUBLIC_METRICS = ("product_in_organic", "product_in_aqueous", "phase_ratio")
FORBIDDEN_VISIBLE_TOKENS = (
    "mechanism_family",
    "world_intervention",
    "private_seed",
    "hidden_state",
    "evaluator_truth",
)


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _actions(
    *,
    solvent: int,
    extractant: int,
    solvent_volume_L: float,
    aqueous_volume_L: float,
    extractant_volume_L: float,
    mix_duration_s: float,
    stirring_speed_rpm: float,
    settle_duration_s: float,
) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": solvent_volume_L, "solvent": solvent},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": aqueous_volume_L},
        {
            "operation": "add_extractant",
            "extractant": extractant,
            "volume_L": extractant_volume_L,
        },
        {
            "operation": "mix",
            "duration_s": mix_duration_s,
            "stirring_speed_rpm": stirring_speed_rpm,
        },
        {"operation": "settle", "duration_s": settle_duration_s},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _preseparation_measurement(
    records: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, float], dict[str, bool]]:
    candidates = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "hplc"
    ]
    if len(candidates) != 2:
        raise ValueError("partition trajectory must contain two committed HPLC measurements")
    selected = candidates[0]
    estimate = selected.get("processed_estimate")
    observed = selected.get("observed_mask")
    if not isinstance(estimate, Mapping) or not isinstance(observed, Mapping):
        raise ValueError("pre-separation HPLC lacks processed estimate or observed mask")
    values = {}
    masks = {}
    for metric in PUBLIC_METRICS:
        value = estimate.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"pre-separation HPLC lacks finite {metric}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"pre-separation HPLC {metric} is not finite")
        values[metric] = number
        masks[metric] = observed.get(metric) is True
    return values, masks


def _visible_leakage_matches(records: Sequence[Mapping[str, Any]]) -> list[str]:
    matches = set()
    for row in records:
        public = {
            key: row.get(key)
            for key in (
                "observation",
                "observed_mask",
                "processed_estimate",
                "raw_signal",
                "agent_visible_observation",
                "agent_view",
            )
        }
        rendered = json.dumps(public, sort_keys=True)
        matches.update(token for token in FORBIDDEN_VISIBLE_TOKENS if token in rendered)
    return sorted(matches)


def _execute(
    *,
    world: Mapping[str, Any],
    execution_id: str,
    actions: list[dict[str, Any]],
    observation_seed: int,
    namespace: str,
    output_root: Path,
    extra: Mapping[str, Any],
    structural_law_id: str | None = None,
) -> dict[str, Any]:
    execution_root = output_root / execution_id
    execution_root.mkdir(parents=True, exist_ok=False)
    trajectory = execution_root / "trajectory.jsonl"
    base_interventions = [dict(item) for item in world["world_interventions"]]
    interventions = list(base_interventions)
    if structural_law_id == "power_response":
        interventions.append(constitutive_intervention())
    elif structural_law_id not in {None, "linear_response"}:
        raise ValueError(f"unknown PA structural law {structural_law_id}")
    started = perf_counter()
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    measurement: dict[str, float] | None = None
    observed_mask: dict[str, bool] | None = None
    platform_failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    leakage: list[str] = []
    try:
        run_agent(
            env_id=get_task("partition-discovery").env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task("partition-discovery").world_split),
            budget=len(actions),
            objective="balanced",
            seed=int(world["world_seed"]),
            agent_seed=0,
            observation_seed=observation_seed,
            task_id="partition-discovery",
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "attribution": "protocol_owned_physical_boundary",
                }
            else:
                first = noncommitted[0]
                raise ValueError(
                    "non-constitution execution failure: "
                    f"operation={first.get('operation_type')} reason={first.get('rollback_reason')}"
                )
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions
        ).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("trajectory failed exact replay")
        leakage = _visible_leakage_matches(records)
        if physical_failure is None:
            measurement, observed_mask = _preseparation_measurement(records)
    except Exception as error:
        platform_failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            leakage = _visible_leakage_matches(records)
    status = (
        "platform_failure"
        if platform_failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    task_hashes = {
        str(row["task_contract_hash"])
        for row in records
        if isinstance(row.get("task_contract_hash"), str)
    }
    mechanism_hashes = {
        str(row["mechanism_hash"])
        for row in records
        if isinstance(row.get("mechanism_hash"), str)
    }
    world_family_hashes = {
        str(row["world_family_intervention_hash"])
        for row in records
        if isinstance(row.get("world_family_intervention_hash"), str)
    }
    mechanism_family_hashes = {
        str(row["mechanism_family_intervention_hash"])
        for row in records
        if isinstance(row.get("mechanism_family_intervention_hash"), str)
    }
    scenario = DefaultScenarioGenerator().generate(
        get_scenario("partition-discovery"), int(world["world_seed"]), tuple(interventions)
    )
    expected_exponent = scenario.parameters.domain_parameter("partition_coefficient_exponent")
    law_binding_verified = bool(
        status == "completed"
        and len(mechanism_hashes) == 1
        and scenario.compiled_mechanism.mechanism_hash in mechanism_hashes
        and (
            (structural_law_id != "power_response" and not mechanism_family_hashes)
            or (
                structural_law_id == "power_response"
                and scenario.initial_state.metadata.get("mechanism_family_intervention_hash")
                in mechanism_family_hashes
            )
        )
        and (
            not base_interventions
            or scenario.initial_state.metadata.get("world_family_intervention_hash")
            in world_family_hashes
        )
    )
    receipt: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-pa-execution-receipt-1.0.1",
        "execution_id": execution_id,
        "system_id": "PA",
        "task_id": "partition-discovery",
        "world_id": world["world_id"],
        "world_seed": world["world_seed"],
        "world_interventions_sha256": canonical_json_sha256(base_interventions),
        "structural_law_id": structural_law_id,
        "expected_partition_exponent": expected_exponent,
        "law_binding_verified": law_binding_verified,
        "status": status,
        "measurement_stage": "post_settle_pre_separation_hplc",
        "measurement": measurement,
        "observed_mask": observed_mask,
        "action_plan_sha256": canonical_json_sha256(actions),
        "observation_seed": observation_seed,
        "observation_noise_namespace": namespace,
        "task_contract_hash": next(iter(task_hashes)) if len(task_hashes) == 1 else None,
        "mechanism_hash": next(iter(mechanism_hashes)) if len(mechanism_hashes) == 1 else None,
        "world_family_intervention_hash": (
            next(iter(world_family_hashes)) if len(world_family_hashes) == 1 else None
        ),
        "mechanism_family_intervention_hash": (
            next(iter(mechanism_family_hashes)) if len(mechanism_family_hashes) == 1 else None
        ),
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": platform_failure,
        "participant_visible_leakage_matches": leakage,
        "participant_visible_payload": {
            "measurement_stage": "post_settle_pre_separation_hplc",
            "measurement": measurement,
            "observed_mask": observed_mask,
        },
        "trajectory": (
            {
                "path": trajectory.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(trajectory),
            }
            if trajectory.is_file()
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 6),
        **dict(extra),
    }
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    write_json_atomic(execution_root / "receipt.json", receipt)
    return receipt


def _worlds(contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in contract["worlds"]["qualification"]]


def _emit_world(event: str, reports: list[Mapping[str, Any]], report: Mapping[str, Any]) -> None:
    print(
        json.dumps(
            {
                "event": event,
                "world_id": report["world_id"],
                "completed_worlds": len(reports),
                "total_worlds": 5,
                "status": report["status"],
                "failures": report["failures"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


def run_canary(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    canary = dict(contract["worlds"]["canary"])
    locus = contract["loci"]["parametric"]
    point = next(row for row in locus["phase_design"] if row["point_id"] == "reference")
    actions = _actions(
        solvent=int(locus["reference_pair"]["solvent"]),
        extractant=int(locus["reference_pair"]["extractant"]),
        solvent_volume_L=float(point["solvent_volume_L"]),
        aqueous_volume_L=float(point["aqueous_volume_L"]),
        extractant_volume_L=float(point["extractant_volume_L"]),
        mix_duration_s=float(locus["mix_duration_s"]),
        stirring_speed_rpm=float(locus["stirring_speed_rpm"]),
        settle_duration_s=float(locus["settle_duration_s"]),
    )
    seed = _stable_seed("experiment-1-pa-canary", canary["world_seed"])
    receipt = _execute(
        world=canary,
        execution_id="PA-W00-reference",
        actions=actions,
        observation_seed=seed,
        namespace="experiment-1-v1.0.1-pa-canary",
        output_root=output,
        extra={"point_id": "reference"},
    )
    prior = entity_prior_audit(contract)
    truth = world_truth_audit(contract, canary)
    passed = bool(
        receipt["status"] == "completed"
        and receipt["exact_replay"] is True
        and receipt["law_binding_verified"] is True
        and prior["passed"] is True
        and truth["deterministic"] is True
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
        "prior_audit": {k: v for k, v in prior.items() if k not in {"aligned", "misspecified"}},
        "private_world_audit": truth,
        "passed": passed,
        "decision": "proceed_to_pa_blocks" if passed else "stop_before_pa_blocks",
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_entity(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["entity"]
    total = (
        5
        * len(locus["solvent_anchors"])
        * len(locus["extractant_targets"])
        * int(locus["independent_replicates"])
    )
    progress = Progress(total, event="experiment_1_pa_entity_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for solvent in locus["solvent_anchors"]:
            for extractant in locus["extractant_targets"]:
                for replicate in range(int(locus["independent_replicates"])):
                    execution_id = f"s{solvent}-x{extractant}-r{replicate}"
                    actions = _actions(
                        solvent=int(solvent),
                        extractant=int(extractant),
                        solvent_volume_L=float(locus["solvent_volume_L"]),
                        aqueous_volume_L=float(locus["aqueous_volume_L"]),
                        extractant_volume_L=float(locus["extractant_volume_L"]),
                        mix_duration_s=float(locus["mix_duration_s"]),
                        stirring_speed_rpm=float(locus["stirring_speed_rpm"]),
                        settle_duration_s=float(locus["settle_duration_s"]),
                    )
                    seed = _stable_seed(
                        locus["observation_noise_namespace"],
                        world["world_id"],
                        solvent,
                        extractant,
                        replicate,
                    )
                    receipt = _execute(
                        world=world,
                        execution_id=execution_id,
                        actions=actions,
                        observation_seed=seed,
                        namespace=str(locus["observation_noise_namespace"]),
                        output_root=world_root,
                        extra={
                            "solvent": int(solvent),
                            "extractant": int(extractant),
                            "replicate": replicate,
                        },
                    )
                    receipts.append(receipt)
                    progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_entity_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("pa_entity_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=ENTITY_SUMMARY_VERSION,
        contract=contract,
        locus="entity",
        reports=reports,
        planned_executions=total,
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_parametric(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["parametric"]
    total = 5 * len(locus["phase_design"]) * int(locus["independent_replicates"])
    progress = Progress(total, event="experiment_1_pa_parametric_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for point in locus["phase_design"]:
            for replicate in range(int(locus["independent_replicates"])):
                execution_id = f"{point['point_id']}-r{replicate}"
                actions = _actions(
                    solvent=int(locus["reference_pair"]["solvent"]),
                    extractant=int(locus["reference_pair"]["extractant"]),
                    solvent_volume_L=float(point["solvent_volume_L"]),
                    aqueous_volume_L=float(point["aqueous_volume_L"]),
                    extractant_volume_L=float(point["extractant_volume_L"]),
                    mix_duration_s=float(locus["mix_duration_s"]),
                    stirring_speed_rpm=float(locus["stirring_speed_rpm"]),
                    settle_duration_s=float(locus["settle_duration_s"]),
                )
                seed = _stable_seed(
                    locus["observation_noise_namespace"],
                    world["world_id"],
                    point["point_id"],
                    replicate,
                )
                receipt = _execute(
                    world=world,
                    execution_id=execution_id,
                    actions=actions,
                    observation_seed=seed,
                    namespace=str(locus["observation_noise_namespace"]),
                    output_root=world_root,
                    extra={**dict(point), "replicate": replicate},
                )
                receipts.append(receipt)
                progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_parametric_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("pa_parametric_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=PARAMETRIC_SUMMARY_VERSION,
        contract=contract,
        locus="parametric",
        reports=reports,
        planned_executions=total,
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["structural"]
    design = registered_nominal_pair_cells()
    total = 5 * len(design) * 2
    progress = Progress(total, event="experiment_1_pa_structural_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for cell in design:
            pair_id = str(cell["cell_id"])
            base_actions = frozen_nominal_pair_action_plan(cell)
            # Re-freeze only process intensification; categorical/volume coordinates remain
            # identical to the audited full 4x4 nominal-pair design.
            actions = [dict(action) for action in base_actions]
            actions[3] = {
                "operation": "mix",
                "duration_s": float(locus["mix_duration_s"]),
                "stirring_speed_rpm": float(locus["stirring_speed_rpm"]),
            }
            actions[4] = {"operation": "settle", "duration_s": float(locus["settle_duration_s"])}
            seed = _stable_seed(
                locus["observation_noise_namespace"], world["world_id"], pair_id
            )
            for law_id in ("linear_response", "power_response"):
                receipt = _execute(
                    world=world,
                    execution_id=f"{pair_id}-{law_id}",
                    actions=actions,
                    observation_seed=seed,
                    namespace=str(locus["observation_noise_namespace"]),
                    output_root=world_root,
                    extra={
                        "pair_id": pair_id,
                        "solvent": int(cell["solvent"]),
                        "extractant": int(cell["extractant"]),
                        "law_id": law_id,
                    },
                    structural_law_id=law_id,
                )
                receipts.append(receipt)
                progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_structural_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("pa_structural_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=STRUCTURAL_SUMMARY_VERSION,
        contract=contract,
        locus="structural",
        reports=reports,
        planned_executions=total,
    )
    summary["prior_arms"] = structural_prior_arms()
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--phase", choices=("canary", "entity", "parametric", "structural"), required=True
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
