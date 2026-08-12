#!/usr/bin/env python3
"""Run the Work II provider-free observation-layer development screen."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any

import gymnasium as gym

from chemworld.data.logging import load_jsonl, observation_to_json, to_builtin
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.work_ii_observation_screen import (
    OBSERVATION_SCREEN_VERSION,
    analyze_observation_world,
    observation_queries,
    screen_specs,
    truth_queries,
)
from chemworld.eval.work_ii_truth import compile_evaluator_truth_query
from chemworld.tasks import get_task
from chemworld.world.scoring import task_score_observation

try:
    from scripts.run_work_ii_mechanism_oracle_qualification import _environment_kwargs
    from scripts.run_work_ii_structural_candidate_qualification import _execute_query
except ModuleNotFoundError:
    from run_work_ii_mechanism_oracle_qualification import (  # type: ignore[no-redef]
        _environment_kwargs,
    )
    from run_work_ii_structural_candidate_qualification import (  # type: ignore[no-redef]
        _execute_query,
    )

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-observation-screen-summary-0.1"
WORLD_REPORT_VERSION = "chemworld-work-ii-observation-screen-world-report-0.1"
DEFAULT_OUTPUT_ROOT = ROOT / "runs/development/work-ii-observation-screen-seed0-20260812"
DEFAULT_SUMMARY = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-observation-screen-seed0-20260812.json"
)
SCOPED_RUNTIME_PREFIXES = (
    "src/",
    "scripts/",
    "configs/benchmark/",
    "workstreams/flagship_tasks/",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
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


class Progress:
    def __init__(self, output_root: Path, total: int) -> None:
        self.log_path = output_root / "progress.jsonl"
        self.status_path = output_root / "progress-status.json"
        self.started = perf_counter()
        self.total = total
        self.completed = 0
        self.physical_failures = 0
        self.platform_failures = 0

    def update(
        self,
        *,
        screen_id: str,
        world_seed: int,
        stage: str,
        status: str,
    ) -> None:
        self.completed += 1
        self.physical_failures += status == "physical_failure"
        self.platform_failures += status == "platform_failure"
        now = perf_counter()
        elapsed = now - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        payload = {
            "event": "work_ii_observation_screen_progress",
            "stage": stage,
            "screen_id": screen_id,
            "world_seed": world_seed,
            "completed": self.completed,
            "total": self.total,
            "throughput_executions_per_minute": round(rate * 60.0, 2),
            "eta_s": round((self.total - self.completed) / rate, 1) if rate else None,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "elapsed_s": round(elapsed, 1),
            "status": status,
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)

    def complete(self, *, decision: str) -> None:
        payload = {
            "event": "work_ii_observation_screen_completed",
            "stage": "completed",
            "completed": self.completed,
            "total": self.total,
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "decision": decision,
            "elapsed_s": round(perf_counter() - self.started, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_path, payload)
        print(rendered, flush=True)


def _truth_binding(
    *, screen_id: str, world_seed: int, query_id: str
) -> tuple[int, str, str]:
    digest = hashlib.sha256(
        f"work-ii-observation-truth-v0.1:{screen_id}:{world_seed}:{query_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-observation-truth-{screen_id}-w{world_seed}-{digest[:12]}",
        digest,
    )


def _execute_truth_once(
    *,
    screen_id: str,
    config: Mapping[str, Any],
    query: Mapping[str, Any],
    world_seed: int,
) -> dict[str, Any]:
    compiled = compile_evaluator_truth_query(config, query)
    observation_seed, namespace, coordinate_hash = _truth_binding(
        screen_id=screen_id,
        world_seed=world_seed,
        query_id=str(compiled["query_id"]),
    )
    environment_kwargs = _environment_kwargs(
        str(config["task_id"]),
        config,
        world_seed=world_seed,
        budget=len(compiled["action_plan"]),
    )
    environment_kwargs.update(
        {
            "observation_seed_override": observation_seed,
            "observation_noise_namespace": namespace,
        }
    )
    env = gym.make(
        get_task(str(config["task_id"])).env_id,
        **environment_kwargs,
    )
    try:
        env.reset(seed=world_seed)
        last_info: Mapping[str, Any] | None = None
        public_trace = []
        for action in compiled["action_plan"]:
            observation, reward, terminated, truncated, info = env.step(action)
            last_info = info
            public_trace.append(
                {
                    "action": to_builtin(action),
                    "observation": observation_to_json(observation),
                    "reward": float(reward),
                    "terminated": bool(terminated),
                    "truncated": bool(truncated),
                    "transaction_status": info.get("transaction_status"),
                    "rollback_reason": info.get("rollback_reason"),
                    "operation_type": info.get("operation_type"),
                    "constraint_flags": to_builtin(info.get("constraint_flags", {})),
                    "constitution_checks": to_builtin(info.get("constitution_checks", [])),
                    "state_delta_summary": to_builtin(info.get("state_delta_summary", {})),
                    "world_events": to_builtin(info.get("world_events", [])),
                }
            )
            if info.get("transaction_status") == "rolled_back":
                if info.get("rollback_reason") == "constitution_failed":
                    return {
                        "query_id": compiled["query_id"],
                        "level_index": int(query["level_index"]),
                        "status": "physical_failure",
                        "attribution": "protocol_owned_physical_boundary",
                        "metrics": None,
                        "failure": {"rollback_reason": "constitution_failed"},
                        "public_trace": public_trace,
                        "action_plan_sha256": compiled["action_plan_sha256"],
                        "observation_coordinate_sha256": coordinate_hash,
                    }
                return {
                    "query_id": compiled["query_id"],
                    "level_index": int(query["level_index"]),
                    "status": "platform_failure",
                    "attribution": "platform_defect_candidate",
                    "metrics": None,
                    "failure": {"rollback_reason": str(info.get("rollback_reason"))},
                    "public_trace": public_trace,
                    "action_plan_sha256": compiled["action_plan_sha256"],
                    "observation_coordinate_sha256": coordinate_hash,
                }
            if truncated and not terminated:
                raise ValueError("truth query truncated")
        if last_info is None:
            raise ValueError("truth query produced no operation info")
        base_env = env.unwrapped
        state = base_env._state
        truth = base_env.observation_kernel._truth_values(state)
        ledger_cost = float(state.ledger.cost)
        risk = float(state.ledger.risk)
        score = float(
            task_score_observation(
                contract=base_env.scoring_contract,
                values={**truth, "cost": min(1.0, ledger_cost), "safety_risk": risk},
            )
        )
        metrics = {
            str(metric): float(truth[metric])
            for metric in query["metric_ids"]
            if metric in truth
        }
        metrics["safety_risk"] = risk
        metrics["cost"] = ledger_cost
        metrics["score"] = score
        missing = [metric for metric in query["metric_ids"] if metric not in metrics]
        if missing:
            raise ValueError(f"truth metrics missing: {missing}")
        return {
            "query_id": compiled["query_id"],
            "level_index": int(query["level_index"]),
            "status": "completed",
            "attribution": "evaluator_owned_truth_audit",
            "safe": risk < float(get_task(str(config["task_id"])).safety_limit),
            "metrics": metrics,
            "failure": None,
            "public_trace": public_trace,
            "action_plan_sha256": compiled["action_plan_sha256"],
            "observation_coordinate_sha256": coordinate_hash,
        }
    finally:
        env.close()


def _final_truth_metrics(
    *,
    screen_id: str,
    config: Mapping[str, Any],
    query: Mapping[str, Any],
    world_seed: int,
    output_root: Path,
) -> dict[str, Any]:
    query_root = output_root / str(query["query_id"])
    query_root.mkdir(parents=True, exist_ok=False)
    started = perf_counter()
    try:
        execution = _execute_truth_once(
            screen_id=screen_id,
            config=config,
            query=query,
            world_seed=world_seed,
        )
        replay = _execute_truth_once(
            screen_id=screen_id,
            config=config,
            query=query,
            world_seed=world_seed,
        )
        execution_hash = canonical_json_sha256(execution)
        replay_hash = canonical_json_sha256(replay)
        verified = execution_hash == replay_hash
        raw = {
            "execution": execution,
            "replay": replay,
            "exact_replay": {
                "verified": verified,
                "execution_sha256": execution_hash,
                "replay_sha256": replay_hash,
            },
        }
        write_json_atomic(query_root / "truth-audit.json", raw)
        row = {key: value for key, value in execution.items() if key != "public_trace"}
        row["exact_replay"] = verified
        row["replay"] = raw["exact_replay"]
        row["truth_audit_sha256"] = file_sha256(query_root / "truth-audit.json")
        if not verified:
            row.update(
                {
                    "status": "platform_failure",
                    "attribution": "platform_defect_candidate",
                    "metrics": None,
                    "failure": {"type": "ReplayMismatch", "message": "truth replay drifted"},
                }
            )
        row["elapsed_s"] = round(perf_counter() - started, 6)
        return row
    except Exception as error:
        return {
            "query_id": str(query["query_id"]),
            "level_index": int(query["level_index"]),
            "status": "platform_failure",
            "attribution": "platform_defect_candidate",
            "safe": None,
            "metrics": None,
            "failure": {"type": type(error).__name__, "message": str(error)[:1000]},
            "exact_replay": False,
            "replay": None,
            "elapsed_s": round(perf_counter() - started, 6),
        }


def _registered_metric_mask(
    trajectory: Path, metric_ids: list[str]
) -> dict[str, bool]:
    records = load_jsonl(trajectory)
    finals = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(finals) != 1:
        return dict.fromkeys(metric_ids, False)
    observed_mask = finals[0].get("observed_mask", {})
    return {
        metric: isinstance(observed_mask, Mapping) and observed_mask.get(metric) is True
        for metric in metric_ids
    }


def _run_world(
    *,
    screen_id: str,
    config: Mapping[str, Any],
    world_seed: int,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    world_root = output_root / screen_id / f"world-{world_seed}"
    world_root.mkdir(parents=True, exist_ok=False)
    noisy_rows = []
    for query in observation_queries(screen_id):
        row = _execute_query(
            candidate_id=screen_id,
            config=config,
            world_seed=world_seed,
            query_spec=query,
            output_root=world_root / "noisy",
        )
        row["level_index"] = query["level_index"]
        row["replicate"] = query["replicate"]
        metric_mask = _registered_metric_mask(
            world_root / "noisy" / str(query["query_id"]) / "trajectory.jsonl",
            list(query["metric_ids"]),
        )
        row["registered_metric_observed_mask"] = metric_mask
        row["all_registered_metrics_observed"] = all(metric_mask.values())
        noisy_rows.append(row)
        progress.update(
            screen_id=screen_id,
            world_seed=world_seed,
            stage="noisy_replicate",
            status=str(row["status"]),
        )
    truth_rows = []
    for query in truth_queries(screen_id):
        row = _final_truth_metrics(
            screen_id=screen_id,
            config=config,
            query=query,
            world_seed=world_seed,
            output_root=world_root / "truth",
        )
        truth_rows.append(row)
        progress.update(
            screen_id=screen_id,
            world_seed=world_seed,
            stage="evaluator_truth",
            status=str(row["status"]),
        )
    analysis = analyze_observation_world(screen_id, noisy_rows, truth_rows)
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": OBSERVATION_SCREEN_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "screen_id": screen_id,
        "task_id": config["task_id"],
        "world_seed": world_seed,
        "outcome_ownership": "provider_free_observation_probe",
        "noisy_rows": noisy_rows,
        "truth_rows": truth_rows,
        "analysis": analysis,
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(world_root / "world-report.json", report)
    return report


def run(args: argparse.Namespace) -> dict[str, Any]:
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError("observation screen requires clean scoped sources: " + ", ".join(dirty))
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite observation screen outputs")
    specs = screen_specs()
    configs = {screen_id: _load(ROOT / str(spec["config"])) for screen_id, spec in specs.items()}
    args.output_root.mkdir(parents=True)
    total = len(specs) * len(args.world_seeds) * 12
    progress = Progress(args.output_root, total)
    started = perf_counter()
    reports = []
    for screen_id in specs:
        for world_seed in args.world_seeds:
            reports.append(
                _run_world(
                    screen_id=screen_id,
                    config=configs[screen_id],
                    world_seed=world_seed,
                    output_root=args.output_root,
                    progress=progress,
                )
            )
    by_screen = {}
    raw_bindings = []
    for screen_id in specs:
        selected = [row for row in reports if row["screen_id"] == screen_id]
        passed = all(row["analysis"]["passed"] for row in selected)
        by_screen[screen_id] = {
            "task_id": specs[screen_id]["task_id"],
            "world_count": len(selected),
            "passed_world_count": sum(row["analysis"]["passed"] for row in selected),
            "screen_passed": passed,
            "denominators": {
                key: sum(int(row["analysis"]["denominators"][key]) for row in selected)
                for key in (
                    "noisy_attempted",
                    "truth_attempted",
                    "completed",
                    "physical_failures",
                    "platform_failures",
                    "unsafe_completed",
                    "exact_replay",
                )
            },
            "worlds": [
                {
                    "world_seed": row["world_seed"],
                    "passed": row["analysis"]["passed"],
                    "failures": row["analysis"]["failures"],
                    "best_effect_metric": row["analysis"]["best_effect_metric"],
                    "metric_reports": row["analysis"]["metric_reports"],
                }
                for row in selected
            ],
        }
        for row in selected:
            path = args.output_root / screen_id / f"world-{row['world_seed']}" / "world-report.json"
            raw_bindings.append(
                {
                    "screen_id": screen_id,
                    "world_seed": row["world_seed"],
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": file_sha256(path),
                    "passed": row["analysis"]["passed"],
                }
            )
    all_passed = all(screen["screen_passed"] for screen in by_screen.values())
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": OBSERVATION_SCREEN_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "source_commit": git_source_commit(ROOT),
        "world_seeds": list(args.world_seeds),
        "coverage": {
            "screen_count": len(specs),
            "world_count": len(reports),
            "noisy_replicates_per_world": 9,
            "truth_queries_per_world": 3,
            "planned_execution_count": progress.total,
        },
        "denominators": {
            key: sum(screen["denominators"][key] for screen in by_screen.values())
            for key in (
                "noisy_attempted",
                "truth_attempted",
                "completed",
                "physical_failures",
                "platform_failures",
                "unsafe_completed",
                "exact_replay",
            )
        },
        "screens": by_screen,
        "all_screens_passed": all_passed,
        "expand_to_five_worlds": all_passed and args.world_seeds == [0],
        "provider_execution_authorized": False,
        "participant_d1_authorized": False,
        "decision": (
            "expand_unchanged_observation_screen_to_worlds_0_to_4"
            if all_passed and args.world_seeds == [0]
            else "retain_probe_and_do_not_expand"
            if not all_passed
            else "observation_screen_completed_for_requested_worlds"
        ),
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
    parser.add_argument("--world-seeds", type=int, nargs="+", default=[0])
    args = parser.parse_args()
    summary = run(args)
    print(
        json.dumps(
            {
                "completed": summary["denominators"]["completed"],
                "planned": summary["coverage"]["planned_execution_count"],
                "all_screens_passed": summary["all_screens_passed"],
                "decision": summary["decision"],
                "elapsed_s": summary["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary["all_screens_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
