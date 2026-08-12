#!/usr/bin/env python3
"""Run the provider-free distillation additional-rollback A-S seed-0 Q0."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np

from chemworld.agents.task_recipes import task_recipe_dimension, task_recipe_from_unit_vector
from chemworld.data.logging import load_jsonl
from chemworld.envs.observation_noise import ObservationNoiseCoordinate
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_distillation_additional_rollback_q0 import (
    DIRECT_METRICS,
    LAW_IDS,
    QUALIFICATION_VERSION,
    TASK_ID,
    WORLD_SEED,
    analyze,
    registered_cells,
    topology_intervention,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import MechanismFamilyIntervention
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-distillation-additional-rollback-q0-summary-0.1"
TASK_REPORT_VERSION = "chemworld-work-ii-distillation-additional-rollback-q0-task-report-0.1"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-distillation-additional-rollback-q0-seed0-20260812"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-distillation-additional-rollback-q0-seed0-20260812.json"
)
TOTAL_EXECUTIONS = len(registered_cells()) * len(LAW_IDS)
SCOPED_RUNTIME_PREFIXES = ("src/", "scripts/", "configs/", "workstreams/flagship_tasks/")


def _scoped_dirty_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    dirty = []
    for line in completed.stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.startswith(SCOPED_RUNTIME_PREFIXES):
            dirty.append(path)
    return sorted(dirty)


def _unit(value: float, low: float, high: float) -> float:
    return (float(value) - low) / (high - low)


def compile_actions(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    task_info = get_task(TASK_ID).to_dict()
    vector = np.full(task_recipe_dimension(task_info), 0.5, dtype=float)
    vector[0] = _unit(float(cell["temperature_K"]), 333.15, 423.15)
    vector[1] = _unit(float(cell["time_s"]), 900.0, 7200.0)
    vector[2] = _unit(0.015, 0.003, 0.030)
    vector[3] = _unit(675.0, 300.0, 1050.0)
    vector[4] = 0.125
    vector[5] = _unit(0.000315, 0.00008, 0.00055)
    vector[6] = 0.125
    vector[7] = _unit(332.5, 315.0, 350.0)
    vector[8] = _unit(900.0, 300.0, 1500.0)
    vector[9] = _unit(370.0, 345.0, 395.0)
    vector[10] = _unit(2400.0, 900.0, 3600.0)
    vector[11] = _unit(2.75, 0.5, 5.0)
    vector[12] = _unit(0.77, 0.55, 0.99)
    recipe = task_recipe_from_unit_vector(task_info, vector)
    return [dict(action) for action in recipe["steps"]]


def _binding(cell_id: str) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"work-ii-distillation-additional-rollback-q0:{WORLD_SEED}:{cell_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-distillation-additional-rollback-w{WORLD_SEED}-{digest[:12]}",
        digest,
    )


def mechanism_audit() -> dict[str, Any]:
    intervention = MechanismFamilyIntervention.from_dict(topology_intervention())
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(TASK_ID)
    native = generator.generate(scenario, WORLD_SEED)
    shifted = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    repeated = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    native_reactions = native.compiled_mechanism.network.reactions
    shifted_reactions = shifted.compiled_mechanism.network.reactions
    target = next(
        reaction for reaction in native_reactions if reaction.reaction_id == "esterification"
    )
    preserved = next(
        reaction for reaction in shifted_reactions if reaction.reaction_id == "esterification"
    )
    added = [
        reaction
        for reaction in shifted_reactions
        if reaction.reaction_id not in {item.reaction_id for item in native_reactions}
    ]
    rollback = added[0] if len(added) == 1 else None
    metadata = shifted.compiled_mechanism.network.metadata
    return {
        "native_mechanism_hash": native.compiled_mechanism.mechanism_hash,
        "intervention_mechanism_hash": shifted.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": (
            native.compiled_mechanism.mechanism_hash
            != shifted.compiled_mechanism.mechanism_hash
        ),
        "intervention_hash_deterministic": (
            shifted.compiled_mechanism.mechanism_hash
            == repeated.compiled_mechanism.mechanism_hash
        ),
        "native_target_reaction_id": target.reaction_id,
        "native_target_equation": target.equation,
        "native_target_reaction_is_reversible": target.reversible,
        "native_target_reaction_preserved": preserved.to_dict() == target.to_dict(),
        "added_reaction_count": len(added),
        "added_reaction_id": rollback.reaction_id if rollback is not None else None,
        "added_reaction_equation": rollback.equation if rollback is not None else None,
        "added_reaction_reactants": rollback.reactants if rollback is not None else None,
        "added_reaction_products": rollback.products if rollback is not None else None,
        "effective_reverse_rate_constant_s_inv": metadata.get(
            "derived_family_reverse_rate_constant_s_inv"
        ),
        "execution_mechanism_binding_matches": False,
    }


def _direct_measurement(
    records: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, float], dict[str, bool]]:
    candidates = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "hplc"
    ]
    if len(candidates) != 1:
        raise ValueError("trajectory must contain exactly one pre-distillation HPLC measurement")
    hplc = candidates[0]
    processed = hplc.get("processed_estimate")
    observed = hplc.get("observed_mask")
    if not isinstance(processed, Mapping) or not isinstance(observed, Mapping):
        raise ValueError("pre-distillation HPLC lacks processed estimates or observed mask")
    values: dict[str, float] = {}
    mask: dict[str, bool] = {}
    for metric in DIRECT_METRICS:
        value = processed.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"pre-distillation HPLC lacks finite {metric}")
        number = float(value)
        if not np.isfinite(number):
            raise ValueError(f"pre-distillation HPLC {metric} is not finite")
        values[metric] = number
        mask[metric] = observed.get(metric) is True
    return values, mask


def _terminal_metrics(records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, float], bool]:
    finals = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(finals) != 1:
        raise ValueError("trajectory must contain exactly one committed final assay")
    final = finals[0]
    observation = final.get("observation")
    if not isinstance(observation, Mapping):
        raise ValueError("final assay lacks public observation")
    metrics = {
        "distillate_purity": float(observation["distillate_purity"]),
        "distillate_recovery": float(observation["distillate_recovery"]),
        "score": float(final["leaderboard_score"]),
    }
    risk = float(observation["safety_risk"])
    return metrics, risk < float(get_task(TASK_ID).safety_limit)


def _visible_leakage_matches(records: Sequence[Mapping[str, Any]]) -> list[str]:
    tokens = (
        "mechanism_family",
        "world_intervention",
        "private_seed",
        "hidden_state",
        "evaluator_truth",
    )
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
        rendered = json.dumps(public, ensure_ascii=False, sort_keys=True)
        matches.update(token for token in tokens if token in rendered)
    return sorted(matches)


def execute(
    *, cell: Mapping[str, Any], law_id: str, output_root: Path
) -> dict[str, Any]:
    actions = compile_actions(cell)
    action_hash = canonical_json_sha256(actions)
    observation_seed, namespace, coordinate_hash = _binding(str(cell["cell_id"]))
    interventions = [] if law_id == LAW_IDS[0] else [topology_intervention()]
    law_root = output_root / str(cell["cell_id"]) / law_id
    law_root.mkdir(parents=True, exist_ok=False)
    trajectory = law_root / "trajectory.jsonl"
    started = perf_counter()
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    direct_metrics: dict[str, float] | None = None
    direct_mask: dict[str, bool] | None = None
    terminal_metrics: dict[str, float] | None = None
    safe: bool | None = None
    leakage: list[str] = []
    try:
        run_agent(
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(TASK_ID).world_split),
            budget=len(actions),
            objective="balanced",
            seed=WORLD_SEED,
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
                    "query contains a non-constitution failure: "
                    f"operation={first.get('operation_type')}, "
                    f"status={first.get('transaction_status')}, "
                    f"reason={first.get('rollback_reason')}"
                )
        replay = verify_records(records, tolerance=0.0, world_interventions=interventions).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("trajectory failed exact replay")
        leakage = _visible_leakage_matches(records)
        if physical_failure is None:
            direct_metrics, direct_mask = _direct_measurement(records)
            terminal_metrics, safe = _terminal_metrics(records)
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            leakage = _visible_leakage_matches(records)
    status = (
        "platform_failure"
        if failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    recorded_hashes = {
        str(row["mechanism_hash"])
        for row in records
        if isinstance(row.get("mechanism_hash"), str)
    }
    mechanism_hash = next(iter(recorded_hashes)) if len(recorded_hashes) == 1 else None
    if records and len(recorded_hashes) != 1 and failure is None:
        status = "platform_failure"
        failure = {
            "type": "MechanismBindingError",
            "message": "mechanism hash changed within one execution",
        }
    direct_noise_key = ObservationNoiseCoordinate(
        namespace=namespace,
        base_observation_seed=observation_seed,
        experiment_index=0,
        operation_type="measure",
        instrument="hplc",
        replicate_index=0,
    ).key_sha256
    row = {
        **dict(cell),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "law_id": law_id,
        "status": status,
        "attribution": (
            "platform_defect_candidate"
            if status == "platform_failure"
            else "protocol_owned_physical_boundary"
            if status == "physical_failure"
            else "protocol_owned_completed_outcome"
        ),
        "safe": safe,
        "direct_instrument": "hplc",
        "direct_measurement_stage": "post_quench_pre_evaporation_pre_distillation",
        "direct_metrics": direct_metrics,
        "direct_observed_mask": direct_mask,
        "terminal_metrics": terminal_metrics,
        "action_plan_sha256": action_hash,
        "observation_coordinate_sha256": coordinate_hash,
        "direct_noise_key_sha256": direct_noise_key,
        "mechanism_hash": mechanism_hash,
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": failure,
        "participant_visible_leakage_matches": leakage,
        "participant_visible_payload": {
            "direct_metrics": direct_metrics,
            "direct_observed_mask": direct_mask,
            "terminal_metrics": terminal_metrics,
        },
        "trajectory": (
            {"path": trajectory.relative_to(ROOT).as_posix(), "sha256": file_sha256(trajectory)}
            if trajectory.is_file()
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 6),
    }
    write_json_atomic(law_root / "receipt.json", row)
    return row


def _write_outputs(
    *,
    rows: list[dict[str, Any]],
    audit: dict[str, Any],
    output_root: Path,
    summary_path: Path,
    started: float,
) -> dict[str, Any]:
    native_hashes = {row["mechanism_hash"] for row in rows if row["law_id"] == LAW_IDS[0]}
    shifted_hashes = {row["mechanism_hash"] for row in rows if row["law_id"] == LAW_IDS[1]}
    audit["execution_mechanism_binding_matches"] = (
        len(rows) == TOTAL_EXECUTIONS
        and native_hashes == {audit["native_mechanism_hash"]}
        and shifted_hashes == {audit["intervention_mechanism_hash"]}
    )
    analysis = analyze(rows, audit)
    platform_stopped = any(row["status"] == "platform_failure" for row in rows)
    decision = (
        "platform_defect_stop_and_rerun_whole_block_after_fix"
        if platform_stopped
        else "proceed_to_unchanged_five_world_provider_free_qualification"
        if analysis["passed"]
        else "retain_q0_scientific_rejection_and_do_not_expand"
    )
    task_report: dict[str, Any] = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "rows": rows,
        "analysis": analysis,
    }
    task_report["report_sha256"] = canonical_json_sha256(task_report)
    report_path = output_root / "task-report.json"
    write_json_atomic(report_path, task_report)
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "source_commit": git_source_commit(ROOT),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_cells": len(registered_cells()),
            "planned_execution_count": TOTAL_EXECUTIONS,
            "attempted_execution_count": len(rows),
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "platform_stop_triggered": platform_stopped,
        "five_world_provider_free_expansion_authorized": analysis["passed"],
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": decision,
        "raw_binding": {
            "path": report_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(report_path),
        },
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(summary_path, summary)
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError(
            "distillation additional-rollback Q0 requires clean scoped sources: "
            + ", ".join(dirty)
        )
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite distillation additional-rollback Q0 outputs")
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    audit = mechanism_audit()
    rows: list[dict[str, Any]] = []
    for cell in registered_cells():
        for law_id in LAW_IDS:
            row = execute(cell=cell, law_id=law_id, output_root=args.output_root)
            rows.append(row)
            elapsed = perf_counter() - started
            rate = len(rows) / elapsed if elapsed else 0.0
            print(
                json.dumps(
                    {
                        "stage": "paired_execution",
                        "completed": len(rows),
                        "total": TOTAL_EXECUTIONS,
                        "throughput_executions_per_minute": round(rate * 60.0, 2),
                        "eta_s": round((TOTAL_EXECUTIONS - len(rows)) / rate, 1) if rate else None,
                        "failure_count": sum(item["status"] != "completed" for item in rows),
                        "current_cell": cell["cell_id"],
                        "law_id": law_id,
                        "status": row["status"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if row["status"] == "platform_failure":
                return _write_outputs(
                    rows=rows,
                    audit=audit,
                    output_root=args.output_root,
                    summary_path=args.summary,
                    started=started,
                )
    return _write_outputs(
        rows=rows,
        audit=audit,
        output_root=args.output_root,
        summary_path=args.summary,
        started=started,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    args.output_root = args.output_root.resolve()
    args.summary = args.summary.resolve()
    summary = run(args)
    print(
        json.dumps(
            {
                "attempted": summary["denominators"]["attempted"],
                "planned": summary["denominators"]["planned"],
                "decision": summary["decision"],
                "elapsed_s": summary["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary["analysis"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
