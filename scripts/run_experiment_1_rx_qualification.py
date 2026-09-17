#!/usr/bin/env python3
"""Run the frozen Experiment 1 RX qualification v1.0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.envs.observation_noise import ObservationNoiseCoordinate
from chemworld.eval.experiment_1_rx_qualification import (
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
    entity_prior_audit,
    load_contract,
    world_truth_audit,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    build_blind_policy_schedule,
    execute_one,
)
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    LAW_IDS,
    registered_cells,
    stable_catalyst_intervention,
)
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    analyze as analyze_deactivation,
)
from chemworld.eval.work_ii_matched_prior_qualification import (
    analyze_matched_prior_world,
    rounded_reference_context,
    surface_design,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    MechanismFamilyIntervention,
    TopologyFamilyChange,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

try:
    from scripts.run_experiment_1_ec_qualification import Progress, _five_world_summary
    from scripts.run_work_ii_catalyst_deactivation_q0 import (
        _compile_actions,
        _direct_measurement,
        _terminal_metrics,
        _visible_leakage_matches,
    )
    from scripts.run_work_ii_mechanism_oracle_qualification import (
        InMemoryMechanismEvaluator,
    )
    from scripts.run_work_ii_q1_response_surface import TASK_SPECS
except ModuleNotFoundError:
    from run_experiment_1_ec_qualification import Progress, _five_world_summary
    from run_work_ii_catalyst_deactivation_q0 import (
        _compile_actions,
        _direct_measurement,
        _terminal_metrics,
        _visible_leakage_matches,
    )
    from run_work_ii_mechanism_oracle_qualification import InMemoryMechanismEvaluator
    from run_work_ii_q1_response_surface import TASK_SPECS

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_rx_qualification_v1.0.1.json"
CANARY_SUMMARY_VERSION = "chemworld-experiment-1-rx-canary-summary-1.0.1"
ENTITY_SUMMARY_VERSION = "chemworld-experiment-1-rx-entity-summary-1.0.1"
PARAMETRIC_SUMMARY_VERSION = "chemworld-experiment-1-rx-parametric-summary-1.0.1"
STRUCTURAL_SUMMARY_VERSION = "chemworld-experiment-1-rx-structural-summary-1.0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _plan(contract: Mapping[str, Any]) -> dict[str, Any]:
    binding = contract["task"]["campaign_config"]
    campaign = _load(ROOT / str(binding["path"]))
    plan: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-rx-entity-plan-1.0.1",
        "development_only": True,
        "task_bindings": [
            {
                "task_id": contract["task"]["task_id"],
                "campaign_config": binding["path"],
                "campaign_config_sha256": canonical_json_sha256(campaign),
            }
        ],
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _schedule(contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    entity = contract["loci"]["entity"]
    return build_blind_policy_schedule(
        task_id=contract["task"]["task_id"],
        target_field=entity["target_field"],
        policy={
            "nuisance_design": entity["nuisance_design"],
            "category_order_by_anchor": entity["category_order_by_anchor"],
        },
    )


def _entity_row(
    contract: Mapping[str, Any],
    *,
    world_id: str,
    world_seed: int,
    schedule_row: Mapping[str, Any],
    replicate: int,
    execution_index: int,
) -> dict[str, Any]:
    entity = contract["loci"]["entity"]
    support = [entity["gate_endpoint_id"], *entity["support_endpoint_ids"]]
    execution_id = (
        f"{world_id}-a{schedule_row['nuisance_anchor']}-"
        f"c{schedule_row['target_category']}-r{replicate}"
    )
    return {
        "execution_id": execution_id,
        "execution_index": execution_index,
        "phase": "experiment_1_rx_entity_qualification",
        "task_id": contract["task"]["task_id"],
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


def run_canary(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    canary = contract["worlds"]["canary"]
    row = _entity_row(
        contract,
        world_id=str(canary["world_id"]),
        world_seed=int(canary["world_seed"]),
        schedule_row=_schedule(contract)[0],
        replicate=0,
        execution_index=0,
    )
    receipt = execute_one(ROOT, _plan(contract), row, output)
    prior = entity_prior_audit(contract)
    truth = world_truth_audit(contract, world_seed=int(canary["world_seed"]))
    passed = bool(
        receipt.get("status") == "completed"
        and isinstance(receipt.get("exact_replay"), Mapping)
        and receipt["exact_replay"].get("verified") is True
        and prior["passed"] is True
        and isinstance(truth.get("truth_sha256"), str)
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
        "private_world_audit": truth,
        "passed": passed,
        "decision": "proceed_to_rx_blocks" if passed else "stop_before_rx_blocks",
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
    progress = Progress(5 * len(schedule) * replicates, event="experiment_1_rx_entity_progress")
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        world_root = output / world_id
        world_root.mkdir()
        receipts = []
        for schedule_row in schedule:
            for replicate in range(replicates):
                row = _entity_row(
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
        report = analyze_entity_world(
            contract,
            world_id=world_id,
            world_seed=world_seed,
            receipts=receipts,
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("rx_entity_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=ENTITY_SUMMARY_VERSION,
        contract=contract,
        locus="entity",
        reports=reports,
        planned_executions=5 * len(schedule) * replicates,
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def _source_worlds(
    contract: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources = contract["source_assets"]
    reference = _load(ROOT / str(sources["parametric_reference_summary"]["path"]))
    noise = _load(ROOT / str(sources["parametric_noise_summary"]["path"]))
    for label, value in (("reference", reference), ("noise", noise)):
        expected = canonical_json_sha256(
            {key: item for key, item in value.items() if key != "summary_sha256"}
        )
        if value.get("summary_sha256") != expected:
            raise ValueError(f"parametric {label} summary self-hash mismatch")
    references = sorted(reference["worlds"], key=lambda row: int(row["world_seed"]))
    noises = sorted(noise["worlds"], key=lambda row: int(row["world_seed"]))
    if [int(row["world_seed"]) for row in references] != list(range(5)):
        raise ValueError("parametric reference worlds changed")
    if [int(row["world_seed"]) for row in noises] != list(range(5)):
        raise ValueError("parametric noise worlds changed")
    return references, noises


def _replay_projection(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "elapsed_s"}


def run_parametric(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    references, noises = _source_worlds(contract)
    spec = TASK_SPECS[contract["task"]["task_id"]]
    config = _load(ROOT / str(spec["config"]))
    reports = []
    progress = Progress(5 * 121, event="experiment_1_rx_parametric_progress")
    for world, reference, noise in zip(
        contract["worlds"]["qualification"], references, noises, strict=True
    ):
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        world_root = output / world_id
        world_root.mkdir()
        context = rounded_reference_context(reference["reference_selection"]["vector"])
        if context != reference["reference_context"]:
            raise ValueError(f"frozen reference context drifted for {world_id}")
        primary = InMemoryMechanismEvaluator(
            task_id=contract["task"]["task_id"],
            config=config,
            spec=spec,
            world_seed=world_seed,
        )
        replay = InMemoryMechanismEvaluator(
            task_id=contract["task"]["task_id"],
            config=config,
            spec=spec,
            world_seed=world_seed,
        )
        rows = []
        try:
            for design_row in surface_design(context):
                extra = {key: value for key, value in design_row.items() if key != "vector"}
                observed = primary.evaluate(
                    design_row["vector"],
                    phase="experiment_1_rx_parametric_surface",
                    extra=extra,
                )
                repeated = replay.evaluate(
                    design_row["vector"],
                    phase="experiment_1_rx_parametric_surface",
                    extra=extra,
                )
                primary_hash = canonical_json_sha256(_replay_projection(observed))
                replay_hash = canonical_json_sha256(_replay_projection(repeated))
                observed["exact_replay"] = {
                    "verified": primary_hash == replay_hash,
                    "primary_sha256": primary_hash,
                    "replay_sha256": replay_hash,
                }
                rows.append(observed)
                progress.update(world_id=world_id, status=str(observed["status"]))
        finally:
            primary.close()
            replay.close()
        write_json_atomic(world_root / "surface-rows.json", rows)
        sigma = float(noise["analysis"]["validation_noise"]["sigma"] or 0.0)
        legacy = analyze_matched_prior_world(
            rows,
            validation_sigma=sigma,
            reference_context=context,
            world_token=f"{contract['task']['task_id']}:{world_seed}",
        )
        report = analyze_parametric_world(
            contract,
            world_id=world_id,
            world_seed=world_seed,
            rows=rows,
            analysis=legacy,
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("rx_parametric_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=PARAMETRIC_SUMMARY_VERSION,
        contract=contract,
        locus="parametric",
        reports=reports,
        planned_executions=5 * 121,
    )
    summary["source_summaries"] = list(contract["source_assets"].values())
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


def _structural_binding(world_seed: int, cell_id: str) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"experiment-1-rx-structural-v1.0.1:{world_seed}:{cell_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"experiment-1-rx-structural-w{world_seed}-{digest[:12]}",
        digest,
    )


def _structural_mechanism_audit(world_seed: int) -> dict[str, Any]:
    intervention = MechanismFamilyIntervention(
        "topology_family",
        1.0,
        topology_change=TopologyFamilyChange(
            reaction_role="catalyst_deactivation_pathway",
            transform_id="stable_catalyst_topology_v1",
            reverse_rate_constant_s_inv_at_full_severity=None,
        ),
    )
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-safety")
    baseline = generator.generate(scenario, world_seed)
    stable = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    repeated = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    baseline_ids = {
        reaction.reaction_id for reaction in baseline.compiled_mechanism.network.reactions
    }
    stable_ids = {reaction.reaction_id for reaction in stable.compiled_mechanism.network.reactions}
    removed = sorted(baseline_ids - stable_ids)
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "stable_mechanism_hash": stable.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": (
            baseline.compiled_mechanism.mechanism_hash != stable.compiled_mechanism.mechanism_hash
        ),
        "stable_hash_deterministic": (
            stable.compiled_mechanism.mechanism_hash == repeated.compiled_mechanism.mechanism_hash
        ),
        "removed_reaction_count": len(removed),
        "removed_reaction_id": removed[0] if len(removed) == 1 else None,
        "retained_reaction_ids": sorted(stable_ids),
    }


def _recorded_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def _execute_structural(
    *,
    world_seed: int,
    cell: Mapping[str, Any],
    law_id: str,
    output_root: Path,
) -> dict[str, Any]:
    actions = _compile_actions(cell)
    observation_seed, namespace, coordinate_hash = _structural_binding(
        world_seed, str(cell["cell_id"])
    )
    interventions = [] if law_id == "deactivating_baseline" else [stable_catalyst_intervention()]
    law_root = output_root / str(cell["cell_id"]) / law_id
    law_root.mkdir(parents=True, exist_ok=False)
    trajectory = law_root / "trajectory.jsonl"
    started = perf_counter()
    failure = None
    physical_failure = None
    records: list[dict[str, Any]] = []
    replay = None
    direct_metrics = None
    direct_mask = None
    terminal_metrics = None
    safe = None
    visible_matches: list[str] = []
    try:
        run_agent(
            env_id=get_task("reaction-safety-constrained").env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split="public-test",
            budget=len(actions),
            objective="safe",
            seed=world_seed,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id="reaction-safety-constrained",
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        recorded_hashes = {
            str(row["mechanism_hash"])
            for row in records
            if isinstance(row.get("mechanism_hash"), str)
        }
        if len(recorded_hashes) != 1:
            raise ValueError("mechanism binding changed within one execution")
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "operations": sorted({str(row.get("operation_type")) for row in noncommitted}),
                    "attribution": "protocol_owned_physical_boundary",
                }
            else:
                raise ValueError("structural query contains a non-constitution failure")
        replay = verify_records(records, tolerance=0.0, world_interventions=interventions).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("RX structural trajectory failed exact replay")
        visible_matches = _visible_leakage_matches(records)
        if physical_failure is None:
            direct_metrics, direct_mask = _direct_measurement(records)
            terminal_metrics = _terminal_metrics(records)
            safe = terminal_metrics["safety_risk"] < float(
                get_task("reaction-safety-constrained").safety_limit
            )
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            visible_matches = _visible_leakage_matches(records)
    status = (
        "platform_failure"
        if failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    mechanism_hash = records[0].get("mechanism_hash") if records else None
    noise_key = ObservationNoiseCoordinate(
        namespace=namespace,
        base_observation_seed=observation_seed,
        experiment_index=0,
        operation_type="measure",
        instrument="hplc",
        replicate_index=0,
    ).key_sha256
    row = {
        **dict(cell),
        "task_id": "reaction-safety-constrained",
        "world_seed": world_seed,
        "law_id": law_id,
        "status": status,
        "safe": safe,
        "direct_instrument": "hplc",
        "direct_metrics": direct_metrics,
        "direct_observed_mask": direct_mask,
        "terminal_metrics": terminal_metrics,
        "action_plan_sha256": canonical_json_sha256(actions),
        "observation_coordinate_sha256": coordinate_hash,
        "direct_noise_key_sha256": noise_key,
        "mechanism_hash": mechanism_hash,
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": failure,
        "participant_visible_leakage_matches": visible_matches,
        "participant_visible_payload": {
            "direct_metrics": direct_metrics,
            "direct_observed_mask": direct_mask,
            "terminal_metrics": terminal_metrics,
        },
        "trajectory": (
            {"path": _recorded_path(trajectory), "sha256": file_sha256(trajectory)}
            if trajectory.is_file()
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 6),
    }
    write_json_atomic(law_root / "receipt.json", row)
    return row


def run_structural(contract: dict[str, Any], output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    design = registered_cells()
    reports = []
    progress = Progress(5 * len(design) * len(LAW_IDS), event="experiment_1_rx_structural_progress")
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        world_root = output / world_id
        world_root.mkdir()
        mechanism = _structural_mechanism_audit(world_seed)
        rows = []
        for cell in design:
            for law_id in LAW_IDS:
                row = _execute_structural(
                    world_seed=world_seed,
                    cell=cell,
                    law_id=law_id,
                    output_root=world_root,
                )
                rows.append(row)
                progress.update(world_id=world_id, status=str(row["status"]))
        write_json_atomic(world_root / "rows.json", rows)
        baseline_hashes = {
            row["mechanism_hash"] for row in rows if row["law_id"] == "deactivating_baseline"
        }
        stable_hashes = {
            row["mechanism_hash"] for row in rows if row["law_id"] == "stable_catalyst"
        }
        mechanism["execution_mechanism_binding_matches"] = bool(
            baseline_hashes == {mechanism["baseline_mechanism_hash"]}
            and stable_hashes == {mechanism["stable_mechanism_hash"]}
        )
        analysis = analyze_deactivation(rows, mechanism)
        report = analyze_structural_world(
            contract,
            world_id=world_id,
            world_seed=world_seed,
            rows=rows,
            analysis=analysis,
        )
        write_json_atomic(world_root / "world-report.json", report)
        reports.append(report)
        _emit_world("rx_structural_world_complete", reports, report)
    summary = _five_world_summary(
        schema_version=STRUCTURAL_SUMMARY_VERSION,
        contract=contract,
        locus="structural",
        reports=reports,
        planned_executions=5 * len(design) * len(LAW_IDS),
    )
    write_json_atomic(output / "summary.json", summary)
    return summary


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
