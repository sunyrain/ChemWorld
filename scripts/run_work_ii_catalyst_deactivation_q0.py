#!/usr/bin/env python3
"""Run the provider-free Work II catalyst-deactivation seed-0 Q0."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

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
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    CATALYST_DEACTIVATION_Q0_VERSION,
    DIRECT_METRICS,
    LAW_IDS,
    TASK_ID,
    WORLD_SEED,
    analyze,
    registered_cells,
    stable_catalyst_intervention,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    MechanismFamilyIntervention,
    TopologyFamilyChange,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-catalyst-deactivation-q0-summary-0.1"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-catalyst-deactivation-q0-seed0-20260812"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-catalyst-deactivation-q0-seed0-20260812.json"
)
TOTAL_EXECUTIONS = len(registered_cells()) * len(LAW_IDS)
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


def _compile_actions(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.015},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": float(cell["catalyst_amount_mol"]),
            "catalyst": 1,
        },
        {
            "operation": "heat",
            "target_temperature_K": float(cell["temperature_K"]),
            "duration_s": float(cell["duration_s"]),
            "stirring_speed_rpm": 675.0,
        },
        {"operation": "quench"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _binding(cell_id: str) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"work-ii-catalyst-deactivation-q0-v0.1:{TASK_ID}:{WORLD_SEED}:{cell_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-catalyst-deactivation-w{WORLD_SEED}-{digest[:12]}",
        digest,
    )


def _recorded_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


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
        raise ValueError("trajectory must contain exactly one committed HPLC measurement")
    row = candidates[0]
    processed = row.get("processed_estimate")
    observed_mask = row.get("observed_mask")
    if not isinstance(processed, Mapping) or not isinstance(observed_mask, Mapping):
        raise ValueError("HPLC measurement lacks processed estimates or observed mask")
    values = {}
    mask = {}
    for metric in DIRECT_METRICS:
        value = processed.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"HPLC measurement lacks finite {metric}")
        values[metric] = float(value)
        mask[metric] = observed_mask.get(metric) is True
    return values, mask


def _terminal_metrics(records: Sequence[Mapping[str, Any]]) -> dict[str, float]:
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
    return {
        "yield": float(observation["yield"]),
        "conversion": float(observation["conversion"]),
        "selectivity": float(observation["selectivity"]),
        "safety_risk": float(observation["safety_risk"]),
        "score": float(final["leaderboard_score"]),
    }


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


def _mechanism_audit() -> dict[str, Any]:
    intervention = MechanismFamilyIntervention(
        "topology_family",
        1.0,
        topology_change=TopologyFamilyChange(
            reaction_role="catalyst_deactivation_pathway",
            transform_id="stable_catalyst_topology_v1",
            reverse_rate_constant_s_inv_at_full_severity=None,
        ),
    )
    if intervention.to_dict() != stable_catalyst_intervention():
        raise ValueError("catalyst-deactivation Q0 intervention contract drifted")
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-safety")
    baseline = generator.generate(scenario, WORLD_SEED)
    stable = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    repeated = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    baseline_ids = {
        reaction.reaction_id for reaction in baseline.compiled_mechanism.network.reactions
    }
    stable_ids = {reaction.reaction_id for reaction in stable.compiled_mechanism.network.reactions}
    removed = sorted(baseline_ids - stable_ids)
    metadata = stable.compiled_mechanism.network.metadata
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "stable_mechanism_hash": stable.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": (
            baseline.compiled_mechanism.mechanism_hash
            != stable.compiled_mechanism.mechanism_hash
        ),
        "stable_hash_deterministic": (
            stable.compiled_mechanism.mechanism_hash
            == repeated.compiled_mechanism.mechanism_hash
        ),
        "removed_reaction_count": len(removed),
        "removed_reaction_id": removed[0] if len(removed) == 1 else None,
        "retained_reaction_ids": sorted(stable_ids),
        "target_reaction_id": metadata.get("derived_family_target_reaction_id"),
        "transform_id": metadata.get("derived_family_transform_id"),
    }


class Progress:
    def __init__(self, output_root: Path) -> None:
        self.path = output_root / "progress.jsonl"
        self.status_path = output_root / "progress-status.json"
        self.started = perf_counter()
        self.completed = 0
        self.physical_failures = 0
        self.platform_failures = 0

    def update(self, *, cell_id: str, law_id: str, status: str) -> None:
        self.completed += 1
        self.physical_failures += status == "physical_failure"
        self.platform_failures += status == "platform_failure"
        elapsed = perf_counter() - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        payload = {
            "event": "work_ii_catalyst_deactivation_q0_progress",
            "stage": "paired_execution",
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
            "event": "work_ii_catalyst_deactivation_q0_completed",
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
    cell: Mapping[str, Any],
    law_id: str,
    output_root: Path,
) -> dict[str, Any]:
    actions = _compile_actions(cell)
    action_hash = canonical_json_sha256(actions)
    observation_seed, namespace, coordinate_hash = _binding(str(cell["cell_id"]))
    interventions = [] if law_id == "deactivating_baseline" else [stable_catalyst_intervention()]
    law_root = output_root / str(cell["cell_id"]) / law_id
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
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(TASK_ID).world_split),
            budget=len(actions),
            objective="safe",
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
        recorded_hashes = {
            str(row["mechanism_hash"])
            for row in records
            if isinstance(row.get("mechanism_hash"), str)
        }
        if len(recorded_hashes) != 1:
            raise ValueError("mechanism binding changed within one fixed-world execution")
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
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
                    "Q0 query contains a non-constitution failure: "
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
            raise ValueError("catalyst-deactivation Q0 trajectory failed exact replay")
        visible_matches = _visible_leakage_matches(records)
        if physical_failure is None:
            direct_metrics, direct_mask = _direct_measurement(records)
            terminal_metrics = _terminal_metrics(records)
            safe = terminal_metrics["safety_risk"] < float(get_task(TASK_ID).safety_limit)
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
                "path": _recorded_path(trajectory),
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
            "catalyst-deactivation Q0 requires clean scoped sources: " + ", ".join(dirty)
        )
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite catalyst-deactivation Q0 outputs")
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    progress = Progress(args.output_root)
    mechanism = _mechanism_audit()
    rows = []
    for cell in registered_cells():
        for law_id in LAW_IDS:
            row = _execute(cell=cell, law_id=law_id, output_root=args.output_root)
            rows.append(row)
            progress.update(
                cell_id=str(cell["cell_id"]),
                law_id=law_id,
                status=str(row["status"]),
            )
    observed_baseline_hashes = {
        row["mechanism_hash"] for row in rows if row["law_id"] == "deactivating_baseline"
    }
    observed_stable_hashes = {
        row["mechanism_hash"] for row in rows if row["law_id"] == "stable_catalyst"
    }
    mechanism["execution_mechanism_binding_matches"] = (
        observed_baseline_hashes == {mechanism["baseline_mechanism_hash"]}
        and observed_stable_hashes == {mechanism["stable_mechanism_hash"]}
    )
    analysis = analyze(rows, mechanism)
    decision = (
        "retain_reaction_safety_as_second_static_structure_candidate"
        if analysis["passed"]
        else "retain_q0_scientific_rejection_and_do_not_expand"
    )
    raw_report: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-catalyst-deactivation-q0-report-0.1",
        "qualification_schema_version": CATALYST_DEACTIVATION_Q0_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "intervention_fixed_for_complete_execution": True,
        "rows": rows,
        "analysis": analysis,
    }
    raw_report["report_sha256"] = canonical_json_sha256(raw_report)
    report_path = args.output_root / "task-report.json"
    write_json_atomic(report_path, raw_report)
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": CATALYST_DEACTIVATION_Q0_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "source_commit": git_source_commit(ROOT),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "coverage": {
            "law_count": len(LAW_IDS),
            "grid_cell_count": len(registered_cells()),
            "planned_execution_count": TOTAL_EXECUTIONS,
        },
        "denominators": analysis["denominators"],
        "passed": analysis["passed"],
        "failures": analysis["failures"],
        "mechanism_audit": analysis["mechanism_audit"],
        "metric_reports": analysis["metric_reports"],
        "supporting_cells": analysis["supporting_cells"],
        "accumulation_reports": analysis["accumulation_reports"],
        "five_world_pair_qualification_authorized": analysis["passed"],
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": decision,
        "raw_bindings": [
            {
                "path": report_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(report_path),
                "passed": analysis["passed"],
            }
        ],
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
                "attempted": summary["denominators"]["attempted"],
                "planned": summary["coverage"]["planned_execution_count"],
                "passed": summary["passed"],
                "decision": summary["decision"],
                "elapsed_s": summary["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
