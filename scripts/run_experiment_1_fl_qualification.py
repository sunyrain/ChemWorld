#!/usr/bin/env python3
"""Run the frozen Experiment 1 FL qualification v1.0.1."""

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
from chemworld.envs.observation_noise import ObservationNoiseCoordinate
from chemworld.eval.experiment_1_fl_qualification import (
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
    entity_prior_audit,
    load_contract,
    parametric_prior_arms,
    structural_prior_arms,
    world_truth_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_static_topology_q0 import topology_intervention
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

try:
    from scripts.run_experiment_1_ec_qualification import Progress, _five_world_summary
except ModuleNotFoundError:
    from run_experiment_1_ec_qualification import Progress, _five_world_summary

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_fl_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-fl-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-fl-entity-summary-1.0.1"
PARAMETRIC_SUMMARY_VERSION = "chemworld-experiment-1-fl-parametric-summary-1.0.1"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-fl-structural-summary-1.0.1"
TASK_ID = "flow-reaction-optimization"
DIRECT_METRICS = ("yield", "selectivity", "flow_conversion")
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
    catalyst: int,
    reagent_amount_mol: float,
    catalyst_amount_mol: float,
    flow_rate_mL_min: float,
    residence_time_s: float,
    temperature_K: float,
) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": solvent},
        {"operation": "add_reagent", "amount_mol": reagent_amount_mol},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": catalyst_amount_mol,
            "catalyst": catalyst,
        },
        {
            "operation": "set_flow_rate",
            "flow_rate_mL_min": flow_rate_mL_min,
            "residence_time_s": residence_time_s,
        },
        {
            "operation": "run_flow",
            "target_temperature_K": temperature_K,
            "duration_s": 2.0 * residence_time_s,
        },
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _direct_measurement(
    records: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, float], dict[str, bool]]:
    candidates = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "uvvis"
    ]
    if len(candidates) != 1:
        raise ValueError("flow trajectory must contain one committed UV measurement")
    processed = candidates[0].get("processed_estimate")
    observed = candidates[0].get("observed_mask")
    if not isinstance(processed, Mapping) or not isinstance(observed, Mapping):
        raise ValueError("flow UV measurement lacks processed estimate or observed mask")
    values: dict[str, float] = {}
    masks: dict[str, bool] = {}
    for metric in DIRECT_METRICS:
        value = processed.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"flow UV measurement lacks finite {metric}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"flow UV {metric} is not finite")
        values[metric] = number
        masks[metric] = observed.get(metric) is True
    return values, masks


def _final_safety(records: Sequence[Mapping[str, Any]]) -> bool:
    rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("instrument") == "final_assay"
    ]
    if len(rows) != 1 or not isinstance(rows[0].get("observation"), Mapping):
        raise ValueError("flow trajectory lacks one final assay")
    return float(rows[0]["observation"]["safety_risk"]) < float(
        get_task(TASK_ID).safety_limit
    )


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


def _mechanism_audit(world: Mapping[str, Any]) -> dict[str, Any]:
    generator = DefaultScenarioGenerator()
    base = tuple(dict(item) for item in world["world_interventions"])
    altered = (*base, topology_intervention())
    scenario = get_scenario(TASK_ID)
    baseline = generator.generate(scenario, int(world["world_seed"]), base)
    reversible = generator.generate(scenario, int(world["world_seed"]), altered)
    repeated = generator.generate(scenario, int(world["world_seed"]), altered)
    metadata = reversible.compiled_mechanism.network.metadata
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "reversible_mechanism_hash": reversible.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": baseline.compiled_mechanism.mechanism_hash
        != reversible.compiled_mechanism.mechanism_hash,
        "reversible_hash_deterministic": reversible.compiled_mechanism.mechanism_hash
        == repeated.compiled_mechanism.mechanism_hash,
        "added_reaction_count": len(reversible.compiled_mechanism.network.reactions)
        - len(baseline.compiled_mechanism.network.reactions),
        "target_reaction_id": metadata.get("derived_family_target_reaction_id"),
        "transform_id": metadata.get("derived_family_transform_id"),
        "effective_reverse_rate_constant_s_inv": metadata.get(
            "derived_family_reverse_rate_constant_s_inv"
        ),
    }


def _flow_configuration(
    world: Mapping[str, Any],
    *,
    flow_rate_mL_min: float,
    residence_time_s: float,
) -> dict[str, float]:
    truth = world_truth_audit({}, world)
    effective = residence_time_s * float(truth["flow_residence_multiplier"])
    volume_l = flow_rate_mL_min / 1000.0 / 60.0 * effective
    area_m2 = math.pi * 0.004**2 / 4.0
    return {
        "configured_flow_rate_mL_min": flow_rate_mL_min,
        "configured_residence_time_s": residence_time_s,
        "effective_minimum_duration_s": effective,
        "reactor_volume_L": volume_l,
        "geometry_length_m": (volume_l / 1000.0) / area_m2,
    }


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
    if structural_law_id == "reversible_target_pathway":
        interventions.append(topology_intervention())
    elif structural_law_id not in {None, "baseline"}:
        raise ValueError(f"unknown FL structural law {structural_law_id}")
    started = perf_counter()
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    measurement: dict[str, float] | None = None
    observed_mask: dict[str, bool] | None = None
    platform_failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    leakage: list[str] = []
    safe: bool | None = None
    try:
        run_agent(
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(TASK_ID).world_split),
            budget=len(actions),
            objective="balanced",
            seed=int(world["world_seed"]),
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=TASK_ID,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "operations": sorted({str(row.get("operation_type")) for row in noncommitted}),
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
            raise ValueError("flow trajectory failed exact replay")
        leakage = _visible_leakage_matches(records)
        if physical_failure is None:
            measurement, observed_mask = _direct_measurement(records)
            safe = _final_safety(records)
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
    mechanism_hashes = {
        str(row["mechanism_hash"])
        for row in records
        if isinstance(row.get("mechanism_hash"), str)
    }
    world_hashes = {
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
        get_scenario(TASK_ID), int(world["world_seed"]), tuple(interventions)
    )
    law_binding_verified = bool(
        status == "completed"
        and mechanism_hashes == {scenario.compiled_mechanism.mechanism_hash}
        and (
            not base_interventions
            or scenario.initial_state.metadata.get("world_family_intervention_hash")
            in world_hashes
        )
        and (
            structural_law_id != "reversible_target_pathway"
            or scenario.initial_state.metadata.get("mechanism_family_intervention_hash")
            in mechanism_family_hashes
        )
    )
    flow_rate = float(next(action["flow_rate_mL_min"] for action in actions if action["operation"] == "set_flow_rate"))
    residence = float(next(action["residence_time_s"] for action in actions if action["operation"] == "set_flow_rate"))
    direct_noise_key = ObservationNoiseCoordinate(
        namespace=namespace,
        base_observation_seed=observation_seed,
        experiment_index=0,
        operation_type="measure",
        instrument="uvvis",
        replicate_index=0,
    ).key_sha256
    receipt: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-fl-execution-receipt-1.0.1",
        "execution_id": execution_id,
        "system_id": "FL",
        "task_id": TASK_ID,
        "world_id": world["world_id"],
        "world_seed": world["world_seed"],
        "world_interventions_sha256": canonical_json_sha256(base_interventions),
        "law_id": structural_law_id,
        "status": status,
        "attribution": (
            "platform_defect_candidate"
            if status == "platform_failure"
            else "protocol_owned_physical_boundary"
            if status == "physical_failure"
            else "protocol_owned_completed_outcome"
        ),
        "safe": safe,
        "measurement": measurement,
        "observed_mask": observed_mask,
        "direct_metrics": measurement,
        "direct_observed_mask": observed_mask,
        "action_plan_sha256": canonical_json_sha256(actions),
        "observation_seed": observation_seed,
        "observation_noise_namespace": namespace,
        "observation_coordinate_sha256": canonical_json_sha256(
            {"namespace": namespace, "seed": observation_seed}
        ),
        "direct_noise_key_sha256": direct_noise_key,
        "mechanism_hash": next(iter(mechanism_hashes)) if len(mechanism_hashes) == 1 else None,
        "world_family_intervention_hash": next(iter(world_hashes)) if len(world_hashes) == 1 else None,
        "mechanism_family_intervention_hash": (
            next(iter(mechanism_family_hashes)) if len(mechanism_family_hashes) == 1 else None
        ),
        "law_binding_verified": law_binding_verified,
        "flow_configuration": _flow_configuration(
            world, flow_rate_mL_min=flow_rate, residence_time_s=residence
        ),
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": platform_failure,
        "participant_visible_leakage_matches": leakage,
        "participant_visible_payload": {
            "direct_metrics": measurement,
            "direct_observed_mask": observed_mask,
        },
        "trajectory": (
            {"path": trajectory.relative_to(ROOT).as_posix(), "sha256": file_sha256(trajectory)}
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
    world = dict(contract["worlds"]["canary"])
    actions = _actions(
        solvent=0,
        catalyst=1,
        reagent_amount_mol=0.015,
        catalyst_amount_mol=0.0003,
        flow_rate_mL_min=1.2,
        residence_time_s=900.0,
        temperature_K=390.0,
    )
    receipt = _execute(
        world=world,
        execution_id="FL-W00-reference",
        actions=actions,
        observation_seed=_stable_seed("experiment-1-fl-canary", world["world_seed"]),
        namespace="experiment-1-v1.0.1-fl-canary",
        output_root=output,
        extra={"temperature_K": 390.0, "residence_time_s": 900.0},
    )
    prior = entity_prior_audit(contract)
    truth = world_truth_audit(contract, world)
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
        "world_id": world["world_id"],
        "world_seed": world["world_seed"],
        "formal_denominator": False,
        "contract_sha256": canonical_json_sha256(contract),
        "receipt": receipt,
        "prior_audit": {k: v for k, v in prior.items() if k not in {"aligned", "misspecified"}},
        "private_world_audit": truth,
        "passed": passed,
        "decision": "proceed_to_fl_blocks" if passed else "stop_before_fl_blocks",
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_entity(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["entity"]
    total = 5 * len(locus["residence_anchors_s"]) * len(locus["catalyst_targets"]) * int(locus["independent_replicates"])
    progress = Progress(total, event="experiment_1_fl_entity_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for residence in locus["residence_anchors_s"]:
            for catalyst in locus["catalyst_targets"]:
                for replicate in range(int(locus["independent_replicates"])):
                    actions = _actions(
                        solvent=int(locus["solvent"]),
                        catalyst=int(catalyst),
                        reagent_amount_mol=float(locus["reagent_amount_mol"]),
                        catalyst_amount_mol=float(locus["catalyst_amount_mol"]),
                        flow_rate_mL_min=float(locus["flow_rate_mL_min"]),
                        residence_time_s=float(residence),
                        temperature_K=float(locus["temperature_K"]),
                    )
                    seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], residence, catalyst, replicate)
                    receipt = _execute(
                        world=world,
                        execution_id=f"tau-{int(residence)}-c{catalyst}-r{replicate}",
                        actions=actions,
                        observation_seed=seed,
                        namespace=str(locus["observation_noise_namespace"]),
                        output_root=world_root,
                        extra={"residence_time_s": float(residence), "catalyst": int(catalyst), "replicate": replicate},
                    )
                    receipts.append(receipt)
                    progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_entity_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("fl_entity_world_complete", reports, report)
    summary = _five_world_summary(schema_version=ENTITY_SUMMARY_VERSION, contract=contract, locus="entity", reports=reports, planned_executions=total)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_parametric(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["parametric"]
    total = 5 * len(locus["temperature_levels_K"]) * len(locus["residence_levels_s"]) * int(locus["independent_replicates"])
    progress = Progress(total, event="experiment_1_fl_parametric_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for temperature_index, temperature in enumerate(locus["temperature_levels_K"]):
            for time_index, residence in enumerate(locus["residence_levels_s"]):
                for replicate in range(int(locus["independent_replicates"])):
                    actions = _actions(
                        solvent=int(locus["solvent"]),
                        catalyst=int(locus["catalyst"]),
                        reagent_amount_mol=float(locus["reagent_amount_mol"]),
                        catalyst_amount_mol=float(locus["catalyst_amount_mol"]),
                        flow_rate_mL_min=float(locus["flow_rate_mL_min"]),
                        residence_time_s=float(residence),
                        temperature_K=float(temperature),
                    )
                    seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], temperature, residence, replicate)
                    receipt = _execute(
                        world=world,
                        execution_id=f"t{temperature_index}-tau{time_index}-r{replicate}",
                        actions=actions,
                        observation_seed=seed,
                        namespace=str(locus["observation_noise_namespace"]),
                        output_root=world_root,
                        extra={"temperature_K": float(temperature), "residence_time_s": float(residence), "temperature_index": temperature_index, "time_index": time_index, "replicate": replicate},
                    )
                    receipts.append(receipt)
                    progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_parametric_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("fl_parametric_world_complete", reports, report)
    summary = _five_world_summary(schema_version=PARAMETRIC_SUMMARY_VERSION, contract=contract, locus="parametric", reports=reports, planned_executions=total)
    summary["prior_arms"] = parametric_prior_arms(contract)
    summary["summary_sha256"] = canonical_json_sha256({key: value for key, value in summary.items() if key != "summary_sha256"})
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    locus = contract["loci"]["structural"]
    total = 5 * int(locus["grid_cells"]) * int(locus["law_count"])
    progress = Progress(total, event="experiment_1_fl_structural_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        mechanism = _mechanism_audit(world)
        for temperature_index, temperature in enumerate(locus["temperature_levels_K"]):
            for time_index, residence in enumerate(locus["residence_levels_s"]):
                cell_id = f"temperature-{temperature_index}-time-{time_index}"
                actions = _actions(
                    solvent=0,
                    catalyst=0,
                    reagent_amount_mol=0.015,
                    catalyst_amount_mol=0.000315,
                    flow_rate_mL_min=float(locus["flow_rate_mL_min"]),
                    residence_time_s=float(residence),
                    temperature_K=float(temperature),
                )
                seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], cell_id)
                for law_id in ("baseline", "reversible_target_pathway"):
                    receipt = _execute(
                        world=world,
                        execution_id=f"{cell_id}-{law_id}",
                        actions=actions,
                        observation_seed=seed,
                        namespace=str(locus["observation_noise_namespace"]),
                        output_root=world_root,
                        extra={"cell_id": cell_id, "temperature_K": float(temperature), "time_s": float(residence), "residence_time_s": float(residence), "temperature_index": temperature_index, "time_index": time_index},
                        structural_law_id=law_id,
                    )
                    receipts.append(receipt)
                    progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        baseline_hashes = {row["mechanism_hash"] for row in receipts if row["law_id"] == "baseline"}
        reversible_hashes = {row["mechanism_hash"] for row in receipts if row["law_id"] == "reversible_target_pathway"}
        mechanism["execution_mechanism_binding_matches"] = bool(
            baseline_hashes == {mechanism["baseline_mechanism_hash"]}
            and reversible_hashes == {mechanism["reversible_mechanism_hash"]}
        )
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_structural_world(contract, world=world, receipts=receipts, mechanism_audit=mechanism)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("fl_structural_world_complete", reports, report)
    summary = _five_world_summary(schema_version=STRUCTURAL_SUMMARY_VERSION, contract=contract, locus="structural", reports=reports, planned_executions=total)
    summary["prior_arms"] = structural_prior_arms(contract)
    summary["summary_sha256"] = canonical_json_sha256({key: value for key, value in summary.items() if key != "summary_sha256"})
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--phase", choices=("canary", "entity", "parametric", "structural"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract_path = args.contract.resolve()
    contract = load_contract(ROOT, contract_path)
    summary = {
        "canary": run_canary,
        "entity": run_entity,
        "parametric": run_parametric,
        "structural": run_structural,
    }[args.phase](contract, args.output.resolve())
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
