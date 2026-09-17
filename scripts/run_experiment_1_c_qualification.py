#!/usr/bin/env python3
"""Run the frozen Experiment 1 crystallization qualification v1.0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_c_qualification import (
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
    entity_prior_audit,
    load_contract,
    parametric_prior_arms,
    structural_prior_audit,
    world_truth_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_structural_candidate_qualification import registered_queries
from chemworld.eval.work_ii_truth import (
    _FrozenTruthReplayAgent,
    compile_evaluator_truth_query,
)
from chemworld.tasks import get_task
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    apply_crystallization_material_family,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

try:
    from scripts.run_experiment_1_ec_qualification import Progress, _five_world_summary
except ModuleNotFoundError:
    from run_experiment_1_ec_qualification import Progress, _five_world_summary

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_c_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-c-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-c-entity-summary-1.0.1"
PARAMETRIC_SUMMARY_VERSION = "chemworld-experiment-1-c-parametric-summary-1.0.1"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-c-structural-summary-1.0.1"
TASK_ID = "reaction-to-crystallization"
METRICS = (
    "crystal_yield",
    "crystal_purity",
    "crystal_size",
    "crystal_csd_quality",
    "crystal_fines_fraction",
    "score",
)
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


def _campaign_config(contract: Mapping[str, Any]) -> dict[str, Any]:
    path = ROOT / str(contract["task"]["campaign_config"]["path"])
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("crystallization campaign config must be an object")
    return value


def _feature_values(
    contract: Mapping[str, Any],
    *,
    catalyst: int,
    solvent: int,
    seed_mass_g: float,
    temperature_K: float,
) -> dict[str, Any]:
    return {
        "catalyst": catalyst,
        "solvent": solvent,
        **dict(contract["fixed_context"]),
        "seed_mass_g": seed_mass_g,
        "crystallization_temperature_K": temperature_K,
    }


def _query_spec(
    *,
    query_id: str,
    feature_values: Mapping[str, Any],
    phase: str,
    axis_a_index: int = 0,
    axis_b_index: int = 0,
    validation_group: int | None = None,
    replicate: int | None = None,
) -> dict[str, Any]:
    return {
        "query_id": query_id,
        "phase": phase,
        "axis_a_index": axis_a_index,
        "axis_b_index": axis_b_index,
        "validation_group": validation_group,
        "replicate": replicate,
        "feature_values": dict(feature_values),
        "metric_ids": list(METRICS),
    }


def _final_metrics(records: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    finals = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(finals) != 1 or not isinstance(finals[0].get("observation"), Mapping):
        raise ValueError("crystallization query must contain one committed final assay")
    payload = dict(finals[0]["observation"])
    payload["score"] = finals[0].get("leaderboard_score")
    output: dict[str, float] = {}
    for metric in METRICS:
        value = payload.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"crystallization final assay lacks finite {metric}")
        output[metric] = float(value)
    return output


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


def _rollback_rows(records: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [
        row
        for row in records
        if row.get("transaction_status") == "rolled_back"
        or row.get("rollback_reason") is not None
    ]


def _execute(
    *,
    contract: Mapping[str, Any],
    config: Mapping[str, Any],
    world: Mapping[str, Any],
    query_spec: Mapping[str, Any],
    observation_seed: int,
    namespace: str,
    output_root: Path,
    extra: Mapping[str, Any],
) -> dict[str, Any]:
    query = compile_evaluator_truth_query(config, query_spec)
    execution_root = output_root / str(query["query_id"])
    execution_root.mkdir(parents=True, exist_ok=False)
    trajectory = execution_root / "trajectory.jsonl"
    interventions = [dict(item) for item in world["world_interventions"]]
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    metrics: dict[str, float] | None = None
    physical_failure: dict[str, Any] | None = None
    platform_failure: dict[str, str] | None = None
    leakage: list[str] = []
    safe: bool | None = None
    started = perf_counter()
    try:
        run_agent(
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(query["action_plan"]),
            world_split=str(config["world_split"]),
            budget=len(query["action_plan"]),
            objective=str(config["objective"]),
            seed=int(world["world_seed"]),
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=TASK_ID,
            output_path=trajectory,
            budget_override=len(query["action_plan"]),
            episode_mode_override="single_experiment",
            crystallization_material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
            electrochemical_workflow_mode=str(query["workflow_mode"]),
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions
        ).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("crystallization trajectory failed exact replay")
        rollbacks = _rollback_rows(records)
        if rollbacks:
            if not all(row.get("rollback_reason") == "constitution_failed" for row in rollbacks):
                raise ValueError("crystallization query encountered non-constitution rollback")
            physical_failure = {
                "rollback_count": len(rollbacks),
                "attribution": "protocol_owned_physical_boundary",
            }
        else:
            metrics = _final_metrics(records)
            risk = float(metrics.get("safety_risk", 0.0))
            safe = risk < float(get_task(TASK_ID).safety_limit)
        leakage = _visible_leakage_matches(records)
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
    world_hashes = {
        str(row["world_family_intervention_hash"])
        for row in records
        if isinstance(row.get("world_family_intervention_hash"), str)
    }
    material_hashes = {
        str(row["crystallization_material_instance_sha256"])
        for row in records
        if isinstance(row.get("crystallization_material_instance_sha256"), str)
    }
    scenario = apply_crystallization_material_family(
        DefaultScenarioGenerator().generate(
            get_scenario(TASK_ID), int(world["world_seed"]), tuple(interventions)
        ),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    truth_binding_verified = bool(
        status == "completed"
        and material_hashes
        == {scenario.initial_state.metadata["crystallization_material_instance_sha256"]}
        and (
            not interventions
            or scenario.initial_state.metadata.get("world_family_intervention_hash")
            in world_hashes
        )
    )
    receipt: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-c-execution-receipt-1.0.1",
        "query_id": query["query_id"],
        "system_id": "C",
        "task_id": TASK_ID,
        "world_id": world["world_id"],
        "world_seed": world["world_seed"],
        "world_interventions_sha256": canonical_json_sha256(interventions),
        "phase": query_spec["phase"],
        "axis_a_index": int(query_spec.get("axis_a_index", 0)),
        "axis_b_index": int(query_spec.get("axis_b_index", 0)),
        "validation_group": query_spec.get("validation_group"),
        "replicate": query_spec.get("replicate"),
        "feature_values": dict(query["feature_values"]),
        "status": status,
        "safe": safe,
        "metrics": metrics,
        "physical_failure": physical_failure,
        "platform_failure": platform_failure,
        "truth_binding_verified": truth_binding_verified,
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "action_plan_sha256": query["action_plan_sha256"],
        "observation_seed": observation_seed,
        "observation_noise_namespace": namespace,
        "observation_coordinate_sha256": canonical_json_sha256(
            {"namespace": namespace, "seed": observation_seed}
        ),
        "fixed_context_sha256": canonical_json_sha256(
            {
                key: value
                for key, value in query["feature_values"].items()
                if key != "crystallization_temperature_K"
            }
        ),
        "participant_visible_leakage_matches": leakage,
        "participant_visible_payload": {"metrics": metrics},
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
    config = _campaign_config(contract)
    feature_values = _feature_values(
        contract, catalyst=0, solvent=0, seed_mass_g=0.008, temperature_K=290.0
    )
    receipt = _execute(
        contract=contract,
        config=config,
        world=world,
        query_spec=_query_spec(
            query_id="C-W00-reference", feature_values=feature_values, phase="canary"
        ),
        observation_seed=_stable_seed("experiment-1-c-canary", world["world_seed"]),
        namespace="experiment-1-v1.0.1-c-canary",
        output_root=output,
        extra={"temperature_K": 290.0},
    )
    prior = entity_prior_audit(contract)
    truth = world_truth_audit(contract, world)
    passed = bool(
        receipt["status"] == "completed"
        and receipt["exact_replay"] is True
        and receipt["truth_binding_verified"] is True
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
        "decision": "proceed_to_c_blocks" if passed else "stop_before_c_blocks",
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_entity(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    config = _campaign_config(contract)
    locus = contract["loci"]["entity"]
    total = 5 * len(locus["cooling_anchors_K"]) * len(locus["solvent_targets"]) * int(locus["independent_replicates"])
    progress = Progress(total, event="experiment_1_c_entity_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for temperature in locus["cooling_anchors_K"]:
            for solvent in locus["solvent_targets"]:
                for replicate in range(int(locus["independent_replicates"])):
                    feature_values = _feature_values(
                        contract,
                        catalyst=int(locus["catalyst"]),
                        solvent=int(solvent),
                        seed_mass_g=float(locus["seed_mass_g"]),
                        temperature_K=float(temperature),
                    )
                    seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], temperature, solvent, replicate)
                    receipt = _execute(
                        contract=contract,
                        config=config,
                        world=world,
                        query_spec=_query_spec(query_id=f"t{int(temperature)}-s{solvent}-r{replicate}", feature_values=feature_values, phase="entity"),
                        observation_seed=seed,
                        namespace=str(locus["observation_noise_namespace"]),
                        output_root=world_root,
                        extra={"temperature_K": float(temperature), "solvent": int(solvent)},
                    )
                    receipts.append(receipt)
                    progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_entity_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("c_entity_world_complete", reports, report)
    summary = _five_world_summary(schema_version=ENTITY_SUMMARY_VERSION, contract=contract, locus="entity", reports=reports, planned_executions=total)
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_parametric(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    config = _campaign_config(contract)
    locus = contract["loci"]["parametric"]
    total = 5 * len(locus["temperature_levels_K"]) * int(locus["independent_replicates"])
    progress = Progress(total, event="experiment_1_c_parametric_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for temperature_index, temperature in enumerate(locus["temperature_levels_K"]):
            for replicate in range(int(locus["independent_replicates"])):
                feature_values = _feature_values(
                    contract,
                    catalyst=int(locus["catalyst"]),
                    solvent=int(locus["solvent"]),
                    seed_mass_g=float(locus["seed_mass_g"]),
                    temperature_K=float(temperature),
                )
                seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], temperature, replicate)
                receipt = _execute(
                    contract=contract,
                    config=config,
                    world=world,
                    query_spec=_query_spec(query_id=f"t{temperature_index}-r{replicate}", feature_values=feature_values, phase="parametric", axis_b_index=temperature_index),
                    observation_seed=seed,
                    namespace=str(locus["observation_noise_namespace"]),
                    output_root=world_root,
                    extra={"temperature_K": float(temperature)},
                )
                receipts.append(receipt)
                progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_parametric_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("c_parametric_world_complete", reports, report)
    summary = _five_world_summary(schema_version=PARAMETRIC_SUMMARY_VERSION, contract=contract, locus="parametric", reports=reports, planned_executions=total)
    summary["prior_arms"] = {world["world_id"]: parametric_prior_arms(contract, world) for world in _worlds(contract)}
    summary["summary_sha256"] = canonical_json_sha256({key: value for key, value in summary.items() if key != "summary_sha256"})
    write_json_atomic(output / "summary.json", summary)
    return summary


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    config = _campaign_config(contract)
    locus = contract["loci"]["structural"]
    design = registered_queries(str(locus["candidate_id"]))
    total = 5 * len(design)
    progress = Progress(total, event="experiment_1_c_structural_progress")
    reports = []
    for world in _worlds(contract):
        world_root = output / str(world["world_id"])
        world_root.mkdir()
        receipts = []
        for query in design:
            seed = _stable_seed(locus["observation_noise_namespace"], world["world_id"], query["query_id"])
            receipt = _execute(
                contract=contract,
                config=config,
                world=world,
                query_spec=query,
                observation_seed=seed,
                namespace=str(locus["observation_noise_namespace"]),
                output_root=world_root,
                extra={},
            )
            receipts.append(receipt)
            progress.update(world_id=str(world["world_id"]), status=str(receipt["status"]))
        write_json_atomic(world_root / "receipts.json", receipts)
        report = analyze_structural_world(contract, world=world, receipts=receipts)
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("c_structural_world_complete", reports, report)
    summary = _five_world_summary(schema_version=STRUCTURAL_SUMMARY_VERSION, contract=contract, locus="structural", reports=reports, planned_executions=total)
    summary["prior_arms"] = structural_prior_audit()
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
