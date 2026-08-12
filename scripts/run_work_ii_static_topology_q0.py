#!/usr/bin/env python3
"""Run the provider-free Work II static reversible-path topology Q0 screen."""

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

from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
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
from chemworld.eval.work_ii_static_topology_q0 import (
    LAW_IDS,
    STATIC_TOPOLOGY_Q0_VERSION,
    WORLD_SEED,
    analyze_task,
    registered_cells,
    task_specs,
    topology_intervention,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    MechanismFamilyIntervention,
    TopologyFamilyChange,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-static-topology-q0-summary-0.1"
TASK_REPORT_VERSION = "chemworld-work-ii-static-topology-q0-task-report-0.1"
DEFAULT_OUTPUT_ROOT = ROOT / "runs/development/work-ii-static-topology-q0-seed0-20260812"
DEFAULT_SUMMARY = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-static-topology-q0-seed0-20260812.json"
)
TOTAL_EXECUTIONS = len(task_specs()) * len(LAW_IDS) * 9
SCOPED_RUNTIME_PREFIXES = (
    "src/",
    "scripts/",
    "configs/benchmark/",
    "workstreams/flagship_tasks/",
)


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


def _compile_actions(task_id: str, cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    task_info = get_task(task_id).to_dict()
    vector = np.full(task_recipe_dimension(task_info), 0.5, dtype=float)
    if task_id == "reaction-to-crystallization":
        vector[0] = _unit(float(cell["temperature_K"]), 333.15, 423.15)
        vector[1] = _unit(float(cell["time_s"]), 900.0, 7200.0)
        vector[2] = _unit(0.015, 0.003, 0.030)
        vector[3] = _unit(675.0, 300.0, 1050.0)
        vector[4] = 0.125
        vector[5] = _unit(0.000315, 0.00008, 0.00055)
        vector[6] = 0.125
        vector[7] = _unit(0.008, 0.001, 0.015)
        vector[8] = _unit(290.0, 270.0, 315.0)
        vector[9] = _unit(7200.0, 600.0, 14_400.0)
    elif task_id == "flow-reaction-optimization":
        vector[0] = 0.125
        vector[1] = _unit(0.015, 0.003, 0.030)
        vector[2] = 0.125
        vector[3] = _unit(0.000315, 0.00008, 0.00055)
        vector[4] = _unit(2.1, 0.2, 4.0)
        vector[5] = _unit(float(cell["time_s"]), 180.0, 2400.0)
        vector[6] = _unit(float(cell["temperature_K"]), 330.0, 430.0)
        vector[7] = 1.0
    else:
        raise KeyError(f"unsupported static-topology task: {task_id}")
    recipe = task_recipe_from_unit_vector(task_info, vector)
    return [dict(action) for action in recipe["steps"]]


def _binding(task_id: str, cell_id: str) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"work-ii-static-topology-q0-v0.1:{task_id}:{WORLD_SEED}:{cell_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-static-topology-{task_id}-w{WORLD_SEED}-{digest[:12]}",
        digest,
    )


def _direct_measurement(
    records: Sequence[Mapping[str, Any]],
    *,
    instrument: str,
    metrics: Sequence[str],
) -> tuple[dict[str, float], dict[str, bool]]:
    candidates = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == instrument
    ]
    if not candidates:
        raise ValueError(f"trajectory lacks its direct {instrument} measurement")
    row = candidates[0]
    processed = row.get("processed_estimate")
    observed_mask = row.get("observed_mask")
    if not isinstance(processed, Mapping) or not isinstance(observed_mask, Mapping):
        raise ValueError("direct measurement lacks processed estimates or observed mask")
    values = {}
    mask = {}
    for metric in metrics:
        value = processed.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"direct measurement lacks finite {metric}")
        number = float(value)
        if not np.isfinite(number):
            raise ValueError(f"direct measurement {metric} is not finite")
        values[metric] = number
        mask[metric] = observed_mask.get(metric) is True
    return values, mask


def _terminal_metrics(
    records: Sequence[Mapping[str, Any]], metrics: Sequence[str]
) -> dict[str, float]:
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
        raise ValueError("final assay lacks its public observation")
    payload = dict(observation)
    payload["score"] = final.get("leaderboard_score")
    output = {}
    for metric in metrics:
        value = payload.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"final assay lacks finite {metric}")
        number = float(value)
        if not np.isfinite(number):
            raise ValueError(f"final assay {metric} is not finite")
        output[metric] = number
    return output


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


def _mechanism_audit(task_id: str) -> dict[str, Any]:
    intervention = MechanismFamilyIntervention(
        "topology_family",
        0.8,
        topology_change=TopologyFamilyChange(
            reaction_role="primary_target_pathway",
            transform_id="reversible_target_pathway_stress_v1",
            reverse_rate_constant_s_inv_at_full_severity=0.000625,
        ),
    )
    if intervention.to_dict() != topology_intervention():
        raise ValueError("static-topology intervention contract drifted")
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    baseline = generator.generate(scenario, WORLD_SEED)
    reversible = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    repeated = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    metadata = reversible.compiled_mechanism.network.metadata
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "reversible_mechanism_hash": reversible.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": (
            baseline.compiled_mechanism.mechanism_hash
            != reversible.compiled_mechanism.mechanism_hash
        ),
        "reversible_hash_deterministic": (
            reversible.compiled_mechanism.mechanism_hash
            == repeated.compiled_mechanism.mechanism_hash
        ),
        "added_reaction_count": (
            len(reversible.compiled_mechanism.network.reactions)
            - len(baseline.compiled_mechanism.network.reactions)
        ),
        "target_reaction_id": metadata.get("derived_family_target_reaction_id"),
        "transform_id": metadata.get("derived_family_transform_id"),
        "effective_reverse_rate_constant_s_inv": metadata.get(
            "derived_family_reverse_rate_constant_s_inv"
        ),
    }


class Progress:
    def __init__(self, output_root: Path) -> None:
        self.path = output_root / "progress.jsonl"
        self.status_path = output_root / "progress-status.json"
        self.started = perf_counter()
        self.completed = 0
        self.physical_failures = 0
        self.platform_failures = 0

    def update(self, *, task_id: str, cell_id: str, law_id: str, status: str) -> None:
        self.completed += 1
        self.physical_failures += status == "physical_failure"
        self.platform_failures += status == "platform_failure"
        elapsed = perf_counter() - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        payload = {
            "event": "work_ii_static_topology_q0_progress",
            "stage": "paired_execution",
            "task_id": task_id,
            "cell_id": cell_id,
            "law_id": law_id,
            "status": status,
            "completed": self.completed,
            "total": TOTAL_EXECUTIONS,
            "throughput_executions_per_minute": round(rate * 60.0, 2),
            "eta_s": round((TOTAL_EXECUTIONS - self.completed) / rate, 1) if rate else None,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "elapsed_s": round(elapsed, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)

    def complete(self, decision: str) -> None:
        payload = {
            "event": "work_ii_static_topology_q0_completed",
            "stage": "completed",
            "completed": self.completed,
            "total": TOTAL_EXECUTIONS,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "decision": decision,
            "elapsed_s": round(perf_counter() - self.started, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)


def _execute(
    *,
    task_id: str,
    cell: Mapping[str, Any],
    law_id: str,
    output_root: Path,
) -> dict[str, Any]:
    spec = task_specs()[task_id]
    actions = _compile_actions(task_id, cell)
    action_hash = canonical_json_sha256(actions)
    observation_seed, namespace, coordinate_hash = _binding(task_id, str(cell["cell_id"]))
    interventions = [] if law_id == "baseline" else [topology_intervention()]
    law_root = output_root / task_id / str(cell["cell_id"]) / law_id
    law_root.mkdir(parents=True, exist_ok=False)
    trajectory = law_root / "trajectory.jsonl"
    started = perf_counter()
    failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    direct_metrics: dict[str, float] | None = None
    direct_mask: dict[str, bool] | None = None
    terminal_metrics: dict[str, float] | None = None
    safe: bool | None = None
    visible_matches: list[str] = []
    try:
        run_agent(
            env_id=get_task(task_id).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(task_id).world_split),
            budget=len(actions),
            objective=str(spec["objective"]),
            seed=WORLD_SEED,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=task_id,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            crystallization_material_family_id=spec["crystallization_material_family_id"],
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        recorded_mechanism_hashes = {
            str(row["mechanism_hash"])
            for row in records
            if isinstance(row.get("mechanism_hash"), str)
        }
        if len(recorded_mechanism_hashes) != 1:
            raise ValueError("static-topology mechanism binding changed within an execution")
        noncommitted = [
            row for row in records if row.get("transaction_status") != "committed"
        ]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "operations": sorted(
                        {str(row.get("operation_type")) for row in noncommitted}
                    ),
                    "attribution": "protocol_owned_physical_boundary",
                }
            else:
                first = noncommitted[0]
                raise ValueError(
                    "static-topology query contains a non-constitution failure: "
                    f"operation={first.get('operation_type')}, "
                    f"status={first.get('transaction_status')}, "
                    f"reason={first.get('rollback_reason')}"
                )
        replay = verify_records(
            records,
            tolerance=0.0,
            world_interventions=interventions,
        ).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("static-topology trajectory failed exact replay")
        visible_matches = _visible_leakage_matches(records)
        if physical_failure is None:
            direct_metrics, direct_mask = _direct_measurement(
                records,
                instrument=str(spec["direct_instrument"]),
                metrics=spec["direct_metrics"],
            )
            terminal_metrics = _terminal_metrics(records, spec["terminal_metrics"])
            final = next(
                row
                for row in records
                if row.get("transaction_status") == "committed"
                and row.get("instrument") == "final_assay"
            )
            risk = float(final["observation"]["safety_risk"])
            safe = risk < float(get_task(task_id).safety_limit)
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
    direct_noise_key = ObservationNoiseCoordinate(
        namespace=namespace,
        base_observation_seed=observation_seed,
        experiment_index=0,
        operation_type="measure",
        instrument=str(spec["direct_instrument"]),
        replicate_index=0,
    ).key_sha256
    row = {
        **dict(cell),
        "task_id": task_id,
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
        "direct_instrument": spec["direct_instrument"],
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
        "participant_visible_leakage_matches": visible_matches,
        "participant_visible_payload": {
            "direct_metrics": direct_metrics,
            "direct_observed_mask": direct_mask,
            "terminal_metrics": terminal_metrics,
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
    }
    write_json_atomic(law_root / "receipt.json", row)
    return row


def run(args: argparse.Namespace) -> dict[str, Any]:
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError(
            "static-topology Q0 requires clean scoped sources: " + ", ".join(dirty)
        )
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite static-topology Q0 outputs")
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    progress = Progress(args.output_root)
    task_reports = {}
    raw_bindings = []
    for task_id in task_specs():
        mechanism = _mechanism_audit(task_id)
        rows = []
        for cell in registered_cells(task_id):
            for law_id in LAW_IDS:
                row = _execute(
                    task_id=task_id,
                    cell=cell,
                    law_id=law_id,
                    output_root=args.output_root,
                )
                rows.append(row)
                progress.update(
                    task_id=task_id,
                    cell_id=str(cell["cell_id"]),
                    law_id=law_id,
                    status=str(row["status"]),
                )
        observed_baseline_hashes = {
            row["mechanism_hash"] for row in rows if row["law_id"] == "baseline"
        }
        observed_reversible_hashes = {
            row["mechanism_hash"]
            for row in rows
            if row["law_id"] == "reversible_target_pathway"
        }
        mechanism["execution_mechanism_binding_matches"] = (
            observed_baseline_hashes == {mechanism["baseline_mechanism_hash"]}
            and observed_reversible_hashes == {mechanism["reversible_mechanism_hash"]}
        )
        analysis = analyze_task(task_id, rows, mechanism)
        task_report: dict[str, Any] = {
            "schema_version": TASK_REPORT_VERSION,
            "qualification_schema_version": STATIC_TOPOLOGY_Q0_VERSION,
            "formal_result": False,
            "provider_call_count": 0,
            "participant_session_count": 0,
            "task_id": task_id,
            "world_seed": WORLD_SEED,
            "intervention_fixed_for_complete_execution": True,
            "rows": rows,
            "analysis": analysis,
        }
        task_report["report_sha256"] = canonical_json_sha256(task_report)
        report_path = args.output_root / task_id / "task-report.json"
        write_json_atomic(report_path, task_report)
        task_reports[task_id] = task_report
        raw_bindings.append(
            {
                "task_id": task_id,
                "path": report_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(report_path),
                "passed": analysis["passed"],
            }
        )

    all_passed = all(report["analysis"]["passed"] for report in task_reports.values())
    decision = (
        "proceed_to_static_topology_five_world_qualification"
        if all_passed
        else "retain_q0_scientific_rejection_and_do_not_expand"
    )
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": STATIC_TOPOLOGY_Q0_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "source_commit": git_source_commit(ROOT),
        "world_seed": WORLD_SEED,
        "coverage": {
            "task_count": len(task_reports),
            "law_count": len(LAW_IDS),
            "grid_cells_per_task": 9,
            "planned_execution_count": TOTAL_EXECUTIONS,
        },
        "denominators": {
            key: sum(
                int(report["analysis"]["denominators"][key])
                for report in task_reports.values()
            )
            for key in (
                "attempted",
                "completed",
                "exact_replay",
                "physical_failures",
                "platform_failures",
                "unsafe_completed",
            )
        },
        "tasks": {
            task_id: {
                "passed": report["analysis"]["passed"],
                "failures": report["analysis"]["failures"],
                "denominators": report["analysis"]["denominators"],
                "mechanism_audit": report["analysis"]["mechanism_audit"],
                "metric_reports": report["analysis"]["metric_reports"],
                "supporting_cells": report["analysis"]["supporting_cells"],
                "accumulation_reports": report["analysis"]["accumulation_reports"],
            }
            for task_id, report in task_reports.items()
        },
        "all_tasks_passed": all_passed,
        "five_world_expansion_authorized": all_passed,
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": decision,
        "raw_bindings": raw_bindings,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.summary, summary)
    progress.complete(decision)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    summary = run(args)
    print(
        json.dumps(
            {
                "completed": summary["denominators"]["completed"],
                "planned": summary["coverage"]["planned_execution_count"],
                "all_tasks_passed": summary["all_tasks_passed"],
                "decision": summary["decision"],
                "elapsed_s": summary["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary["all_tasks_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
