#!/usr/bin/env python3
"""Run the frozen provider-free Work II structural-candidate qualification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_structural_candidate_qualification import (
    STRUCTURAL_QUALIFICATION_VERSION,
    WORLD_SEEDS,
    analyze_candidate_world,
    candidate_specs,
    finite_metrics,
    registered_queries,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent, compile_evaluator_truth_query
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-structural-candidate-five-world-summary-0.1"
WORLD_REPORT_VERSION = "chemworld-work-ii-structural-candidate-world-report-0.1"
PACKAGE_VERSION = "chemworld-work-ii-structural-candidate-package-0.1"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-structural-candidate-qualification-20260811"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-structural-candidate-qualification-20260811.json"
)
DEFAULT_PACKAGE = ROOT / "configs/benchmark/work_ii_structural_candidate_package.json"
D1_PATHS = {
    "electrochemical_transport": (
        ROOT / "configs/benchmark/work_ii_electrochemical_transport_structural_d1.json"
    ),
    "crystallization_nucleation_growth": (
        ROOT / "configs/benchmark/work_ii_crystallization_nucleation_growth_structural_d1.json"
    ),
}
TOTAL_EXECUTIONS = 2 * len(WORLD_SEEDS) * 18
SCOPED_RUNTIME_PREFIXES = (
    "src/",
    "scripts/",
    "configs/benchmark/",
    "workstreams/flagship_tasks/",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


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


def _observation_binding(
    candidate_id: str,
    world_seed: int,
    query_id: str,
) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"work-ii-structural-v0.1:{candidate_id}:{world_seed}:{query_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-structural-{candidate_id}-w{world_seed}-{digest[:12]}",
        digest,
    )


def _rollback_rows(records: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [
        row
        for row in records
        if row.get("transaction_status") == "rolled_back"
        or row.get("rollback_reason") is not None
    ]


def _failed_checks(records: Sequence[Mapping[str, Any]]) -> list[str]:
    checks: set[str] = set()
    for row in records:
        if row.get("transaction_status") != "rolled_back":
            continue
        for event in row.get("world_events", []):
            if not isinstance(event, Mapping) or event.get("event_type") != "transaction_rollback":
                continue
            payload = event.get("payload", {})
            if not isinstance(payload, Mapping):
                continue
            raw = payload.get("failed_checks", [])
            values = raw.split(",") if isinstance(raw, str) else raw
            if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
                checks.update(str(value) for value in values if str(value))
    return sorted(checks)


def _final_metrics(
    records: Sequence[Mapping[str, Any]], metric_ids: Sequence[str]
) -> dict[str, float]:
    final_rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(final_rows) != 1:
        raise ValueError("structural query must contain exactly one committed final assay")
    final = final_rows[0]
    observation = final.get("observation")
    if not isinstance(observation, Mapping):
        raise ValueError("structural final assay lacks an observation")
    payload = dict(observation)
    payload["score"] = final.get("leaderboard_score")
    return finite_metrics(payload, metric_ids)


class Progress:
    def __init__(self, path: Path, status_path: Path) -> None:
        self.path = path
        self.status_path = status_path
        self.started = perf_counter()
        self.last_emit = self.started
        self.completed = 0
        self.physical_failures = 0
        self.platform_failures = 0

    def update(
        self,
        *,
        candidate_id: str,
        world_seed: int,
        stage: str,
        status: str,
        force: bool = False,
    ) -> None:
        self.completed += 1
        self.physical_failures += status == "physical_failure"
        self.platform_failures += status == "platform_failure"
        now = perf_counter()
        if not force and self.completed % 5 != 0 and now - self.last_emit < 30.0:
            return
        elapsed = now - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        payload = {
            "event": "work_ii_structural_candidate_progress",
            "candidate_id": candidate_id,
            "world_seed": world_seed,
            "stage": stage,
            "completed": self.completed,
            "total": TOTAL_EXECUTIONS,
            "throughput_executions_per_minute": round(rate * 60.0, 2),
            "eta_s": round((TOTAL_EXECUTIONS - self.completed) / rate, 1) if rate else None,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "elapsed_s": round(elapsed, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)
        self.last_emit = now

    def complete(self, *, decision: str) -> None:
        elapsed = perf_counter() - self.started
        payload = {
            "event": "work_ii_structural_candidate_completed",
            "stage": "completed",
            "completed": self.completed,
            "total": TOTAL_EXECUTIONS,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "decision": decision,
            "elapsed_s": round(elapsed, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)


def _execute_query(
    *,
    candidate_id: str,
    config: Mapping[str, Any],
    world_seed: int,
    query_spec: Mapping[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    query = compile_evaluator_truth_query(config, query_spec)
    query_root = output_root / str(query["query_id"])
    query_root.mkdir(parents=True, exist_ok=False)
    trajectory = query_root / "trajectory.jsonl"
    observation_seed, namespace, coordinate_hash = _observation_binding(
        candidate_id,
        world_seed,
        str(query["query_id"]),
    )
    failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    metrics: dict[str, float] | None = None
    replay: dict[str, Any] | None = None
    safe: bool | None = None
    started = perf_counter()
    try:
        run_agent(
            env_id=get_task(str(config["task_id"])).env_id,
            agent=_FrozenTruthReplayAgent(query["action_plan"]),
            world_split=str(config["world_split"]),
            budget=len(query["action_plan"]),
            objective=str(config["objective"]),
            seed=world_seed,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=str(config["task_id"]),
            output_path=trajectory,
            budget_override=len(query["action_plan"]),
            episode_mode_override="single_experiment",
            electrochemical_material_family_id=config.get(
                "electrochemical_material_family_id"
            ),
            crystallization_material_family_id=config.get(
                "crystallization_material_family_id"
            ),
            electrochemical_workflow_mode=str(query["workflow_mode"]),
            scoring_contract_id=config.get("scoring_contract_id"),
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
        )
        records = load_jsonl(trajectory)
        replay = verify_records(records, tolerance=0.0).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("structural trajectory failed exact replay")
        rollbacks = _rollback_rows(records)
        if rollbacks:
            if not all(row.get("rollback_reason") == "constitution_failed" for row in rollbacks):
                raise ValueError("structural query encountered a non-constitution rollback")
            physical_failure = {
                "rollback_count": len(rollbacks),
                "failed_checks": _failed_checks(records),
                "attribution": "protocol_owned_physical_boundary",
            }
        else:
            metrics = _final_metrics(records, query["metric_ids"])
            risk = metrics.get("safety_risk")
            safety_limit = float(get_task(str(config["task_id"])).safety_limit)
            safe = True if risk is None else risk < safety_limit
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
    status = (
        "platform_failure"
        if failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    attribution = (
        "platform_defect_candidate"
        if status == "platform_failure"
        else "protocol_owned_physical_boundary"
        if status == "physical_failure"
        else "protocol_owned_unsafe_outcome"
        if safe is False
        else "protocol_owned_completed_outcome"
    )
    return {
        "query_id": query["query_id"],
        "phase": query_spec["phase"],
        "world_seed": world_seed,
        "axis_a_index": int(query_spec["axis_a_index"]),
        "axis_b_index": int(query_spec["axis_b_index"]),
        "validation_group": query_spec.get("validation_group"),
        "replicate": query_spec.get("replicate"),
        "feature_values": query["feature_values"],
        "status": status,
        "attribution": attribution,
        "safe": safe,
        "metrics": metrics,
        "physical_failure": physical_failure,
        "platform_failure": failure,
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "action_plan_sha256": query["action_plan_sha256"],
        "observation_coordinate_sha256": coordinate_hash,
        "trajectory_sha256": file_sha256(trajectory) if trajectory.is_file() else None,
        "elapsed_s": round(perf_counter() - started, 6),
    }


def _run_world(
    *,
    candidate_id: str,
    config: Mapping[str, Any],
    world_seed: int,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    world_root = output_root / candidate_id / f"world-{world_seed}"
    world_root.mkdir(parents=True, exist_ok=False)
    rows = []
    for index, query in enumerate(registered_queries(candidate_id), start=1):
        row = _execute_query(
            candidate_id=candidate_id,
            config=config,
            world_seed=world_seed,
            query_spec=query,
            output_root=world_root,
        )
        rows.append(row)
        progress.update(
            candidate_id=candidate_id,
            world_seed=world_seed,
            stage=str(query["phase"]),
            status=str(row["status"]),
            force=index == 18,
        )
    analysis = analyze_candidate_world(candidate_id, rows)
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": STRUCTURAL_QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "candidate_id": candidate_id,
        "task_id": config["task_id"],
        "world_seed": world_seed,
        "outcome_ownership": "protocol_owned_provider_free",
        "rows": rows,
        "analysis": analysis,
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(world_root / "world-report.json", report)
    return report


def _d1_config(
    *,
    candidate_id: str,
    base: Mapping[str, Any],
    package_hash: str,
    prior_arms: Mapping[str, Any],
) -> dict[str, Any]:
    config = copy.deepcopy(dict(base))
    spec = candidate_specs()[candidate_id]
    task_id = str(spec["task_id"])
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.5",
            "pilot_id": f"work-ii-{candidate_id}-structural-d1",
            "formal_result": False,
            "world_seed": 0,
            "episode_mode": "campaign",
            "observation_noise_namespace": f"work-ii-{candidate_id}-structural-d1",
            "snapshot_stages": [
                "pre_evidence",
                "after_experiment_3",
                "after_experiment_6",
                "after_experiment_9",
                "final",
            ],
            "prior_arms": {
                arm_id: {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": copy.deepcopy(dict(model)),
                }
                for arm_id, model in prior_arms.items()
            },
            "intervention": {
                "locus": "structural_mechanistic",
                "target": prior_arms["aligned_nominal"]["target"],
                "target_controls": list(spec["axis_names"]),
                "fixed_reference_context": copy.deepcopy(spec["fixed_context"]),
                "world_and_resource_contract_matched": True,
                "q2_binding_sha256": package_hash,
            },
        }
    )
    config["belief_checkpoint"] = {
        "allowed_feature_ids": list(spec["fixed_context"]) + list(spec["axis_names"]),
        "allowed_metric_ids": list(spec["metrics"]),
        "allowed_prior_fields": list(spec["axis_names"]),
        "held_out_queries": [
            {
                "query_id": query["query_id"],
                "feature_values": query["feature_values"],
                "metric_ids": query["metric_ids"],
            }
            for query in registered_queries(candidate_id)
            if query["phase"] == "main_grid"
        ],
    }
    if task_id == "electrochemical-conversion":
        process_time_limit = 54_000.0
        operation_limit = 132
        stock_limits = {"reagent_mol": 0.414, "solvent_L": 0.345}
        repeat_limits = {"electrolyze": 24}
        policy = {
            "pattern_id": "electrochemical-structural-k12-ten-unique-two-repeat-planning",
            "formula": "10 unique + 2 exact-repeat probe/controlled electrolysis maxima",
            "required_stage_max_s": 45_000.0,
            "repeat_allowance_s": 9_000.0,
            "quench_transfer_allowance_s": 0.0,
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        }
    else:
        process_time_limit = 307_800.0
        operation_limit = 168
        stock_limits = {
            "reagent_mol": 0.276,
            "solvent_L": 0.552,
            "catalyst_mol": 0.0276,
            "seed_g": 0.69,
        }
        repeat_limits = {
            "heat": 12,
            "cool_crystallize": 12,
            "seed_crystals": 12,
            "filter_crystals": 12,
            "quench": 12,
        }
        policy = {
            "pattern_id": "crystallization-structural-k12-ten-unique-two-repeat-planning",
            "formula": "10 unique + 2 exact-repeat full stages plus 15% protected reserve",
            "required_stage_max_s": 266_400.0,
            "repeat_allowance_s": 44_400.0,
            "quench_transfer_allowance_s": 1_440.0,
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        }
    config["campaign"] = {
        "card_id": policy["pattern_id"],
        "checkpoint_complete_experiments": [0, 3, 6, 9, 12],
        "complete_experiments": 12,
        "final_assay_limit": 12,
        "nonfinal_instrument_use_limit": 36,
        "operation_attempt_limit": operation_limit,
        "operation_repeat_limits": repeat_limits,
        "process_time_limit_s": process_time_limit,
        "process_time_policy": policy,
        "stock_limits": stock_limits,
        "vessel_start_limit": 12,
        "closeout_policy": {
            "policy": "participant_controlled_advisory_no_hidden_allocation",
            "automatic_action_repair": False,
            "automatic_closeout": False,
            "planned_batches": 12,
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        },
    }
    config["method_resources"] = {
        "checkpoint_complete_experiments": [3, 6, 9, 12],
        "complete_experiment_limit": 12,
        "operation_limit": operation_limit,
        "model_call_limit": 1,
        "input_token_limit": 5_760_000,
        "uncached_input_token_limit": 768_000,
        "output_token_limit": 57_600,
        "wall_time_limit_s": 9_000.0,
        "training_environment_step_limit": 0,
        "resource_status": "development_d1_envelope_pending_w2_26_calibration",
    }
    config["qualification"] = {
        "q0_q1_q2_passed": True,
        "minimum_unique_recipes": 10,
        "maximum_exact_repeats": 2,
        "execution_authorized": False,
        "formal_r5_authorized": False,
        "resource_calibration_status": "pending_w2_26",
    }
    return config


def run(args: argparse.Namespace) -> dict[str, Any]:
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError(
            "structural qualification requires clean scoped sources: " + ", ".join(dirty)
        )
    protected = [args.output_root, args.summary, args.package, *D1_PATHS.values()]
    if any(path.exists() for path in protected):
        raise FileExistsError("refusing to overwrite structural qualification outputs")
    specs = candidate_specs()
    configs = {
        candidate_id: _load((ROOT / str(spec["config"])).resolve())
        for candidate_id, spec in specs.items()
    }
    args.output_root.mkdir(parents=True)
    progress = Progress(args.progress_file, args.status_file)
    started = perf_counter()
    reports = []
    for candidate_id in specs:
        for world_seed in WORLD_SEEDS:
            reports.append(
                _run_world(
                    candidate_id=candidate_id,
                    config=configs[candidate_id],
                    world_seed=world_seed,
                    output_root=args.output_root,
                    progress=progress,
                )
            )

    candidate_summaries = {}
    raw_bindings = []
    for candidate_id in specs:
        selected = [report for report in reports if report["candidate_id"] == candidate_id]
        passed = all(report["analysis"]["passed"] for report in selected)
        candidate_summaries[candidate_id] = {
            "task_id": specs[candidate_id]["task_id"],
            "world_count": len(selected),
            "passed_world_count": sum(report["analysis"]["passed"] for report in selected),
            "qualification_passed": passed,
            "denominators": {
                key: sum(int(report["analysis"]["denominators"][key]) for report in selected)
                for key in (
                    "attempted",
                    "completed",
                    "physical_failures",
                    "platform_failures",
                    "unsafe_completed",
                    "exact_replay",
                )
            },
            "worlds": [
                {
                    "world_seed": report["world_seed"],
                    "passed": report["analysis"]["passed"],
                    "failures": report["analysis"]["failures"],
                    "effects": report["analysis"]["effects"],
                    "model_qualification": report["analysis"]["model_qualification"],
                }
                for report in selected
            ],
        }
        for report in selected:
            path = (
                args.output_root
                / candidate_id
                / f"world-{report['world_seed']}"
                / "world-report.json"
            )
            raw_bindings.append(
                {
                    "candidate_id": candidate_id,
                    "world_seed": report["world_seed"],
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": file_sha256(path),
                    "passed": report["analysis"]["passed"],
                }
            )

    package: dict[str, Any] = {
        "schema_version": PACKAGE_VERSION,
        "qualification_schema_version": STRUCTURAL_QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "candidates": {
            candidate_id: {
                "task_id": specs[candidate_id]["task_id"],
                "qualification_passed": result["qualification_passed"],
                "fixed_context": specs[candidate_id]["fixed_context"],
                "axis_names": list(specs[candidate_id]["axis_names"]),
                "axis_levels": [list(levels) for levels in specs[candidate_id]["axis_levels"]],
                "prior_arms": reports[
                    next(
                        index
                        for index, report in enumerate(reports)
                        if report["candidate_id"] == candidate_id
                    )
                ]["analysis"]["prior_arms"],
            }
            for candidate_id, result in candidate_summaries.items()
        },
    }
    package["package_sha256"] = canonical_json_sha256(package)
    write_json_atomic(args.package, package)

    generated_configs = {}
    for candidate_id, result in candidate_summaries.items():
        if not result["qualification_passed"]:
            generated_configs[candidate_id] = None
            continue
        prior_arms = package["candidates"][candidate_id]["prior_arms"]
        d1 = _d1_config(
            candidate_id=candidate_id,
            base=configs[candidate_id],
            package_hash=package["package_sha256"],
            prior_arms=prior_arms,
        )
        path = D1_PATHS[candidate_id]
        write_json_atomic(path, d1)
        generated_configs[candidate_id] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "execution_authorized": False,
        }

    all_candidates_passed = all(
        result["qualification_passed"] for result in candidate_summaries.values()
    )
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": STRUCTURAL_QUALIFICATION_VERSION,
        "formal_result": False,
        "source_commit": git_source_commit(ROOT),
        "provider_call_count": 0,
        "outcome_ownership": "protocol_owned_provider_free",
        "coverage": {
            "candidate_count": 2,
            "worlds_per_candidate": 5,
            "main_grid_per_world": 9,
            "noisy_validation_per_world": 9,
            "planned_execution_count": TOTAL_EXECUTIONS,
        },
        "denominators": {
            key: sum(result["denominators"][key] for result in candidate_summaries.values())
            for key in (
                "attempted",
                "completed",
                "physical_failures",
                "platform_failures",
                "unsafe_completed",
                "exact_replay",
            )
        },
        "candidates": candidate_summaries,
        "all_candidates_passed": all_candidates_passed,
        "q2_packages_generated": sum(
            result["qualification_passed"] for result in candidate_summaries.values()
        ),
        "provider_execution_authorized": False,
        "formal_r5_authorized": False,
        "decision": (
            "authorize_static_d1_readiness_for_passing_candidates"
            if any(result["qualification_passed"] for result in candidate_summaries.values())
            else "retain_scientific_rejections_and_do_not_generate_d1"
        ),
        "generated_package": {
            "path": args.package.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(args.package),
        },
        "generated_d1_configs": generated_configs,
        "raw_bindings": raw_bindings,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.summary, summary)
    progress.complete(decision=str(summary["decision"]))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument("--status-file", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args)
    return 0 if summary["all_candidates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
