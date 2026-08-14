#!/usr/bin/env python3
"""Validate or execute the lightweight DeepSeek Work II public C2 cohort."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_deepseek_c2_prospective_v0.1.json"
CELL_RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
EXPECTED_BLOCKS = {
    "A_E_public": {"tasks": 5, "rounds": 8, "sessions": 75, "experiments": 600},
    "A_P": {"tasks": 2, "rounds": 10, "sessions": 30, "experiments": 300},
    "A_S": {"tasks": 2, "rounds": 12, "sessions": 30, "experiments": 360},
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _cell_id(block: str, task_id: str, seed: int, arm: str) -> str:
    return f"{block}--{task_id}--seed{seed}--{arm}"


def validate_and_expand(plan_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Validate the fixed denominator and return one row per world triplet."""

    plan_path = plan_path.resolve()
    plan = _load(plan_path)
    errors: list[str] = []
    if plan.get("schema_version") != "chemworld-work-ii-deepseek-c2-prospective-0.1":
        errors.append("unexpected plan schema")
    if plan.get("status") != "public_execution_authorized":
        errors.append("public cohort is not execution-authorized")
    provider = plan.get("provider")
    provider = provider if isinstance(provider, Mapping) else {}
    if (
        provider.get("id") != "deepseek"
        or provider.get("model") != "deepseek-v4-flash"
        or provider.get("resource_limits") != "report_only"
    ):
        errors.append("plan does not select unlimited/report-only DeepSeek execution")
    if tuple(plan.get("prior_arms", ())) != ARMS:
        errors.append("plan does not contain the exact three prior arms")
    note = (ROOT / str(plan.get("experiment_note", ""))).resolve()
    if not note.is_file() or not note.is_relative_to(ROOT.resolve()):
        errors.append("prospective experiment note is missing")
    execution = plan.get("execution")
    execution = execution if isinstance(execution, Mapping) else {}
    if (
        execution.get("scientific_or_method_failure_retained") is not True
        or execution.get("outcome_based_replacement_forbidden") is not True
        or execution.get("missing_infrastructure_only_resume") is not True
    ):
        errors.append("failure and resume semantics are not fixed")

    triplets: list[dict[str, Any]] = []
    observed_blocks: set[str] = set()
    all_seeds: set[int] = set()
    block_summaries: dict[str, dict[str, int]] = {}
    blocks = plan.get("public_blocks")
    blocks = blocks if isinstance(blocks, list) else []
    for block in blocks:
        if not isinstance(block, Mapping):
            errors.append("public block must be an object")
            continue
        block_id = str(block.get("block", ""))
        locus = str(block.get("locus", ""))
        expected = EXPECTED_BLOCKS.get(block_id)
        if expected is None or block_id in observed_blocks:
            errors.append(f"unexpected or duplicate public block: {block_id}")
            continue
        observed_blocks.add(block_id)
        rounds = int(block.get("rounds_per_session", -1))
        tasks = block.get("tasks")
        tasks = tasks if isinstance(tasks, list) else []
        if rounds != expected["rounds"] or len(tasks) != expected["tasks"]:
            errors.append(f"{block_id}: task or round denominator differs")
        task_ids: set[str] = set()
        for task in tasks:
            if not isinstance(task, Mapping):
                errors.append(f"{block_id}: task must be an object")
                continue
            task_id = str(task.get("task_id", ""))
            if not task_id or task_id in task_ids:
                errors.append(f"{block_id}: duplicate or empty task id")
                continue
            task_ids.add(task_id)
            config_path = (ROOT / str(task.get("config", ""))).resolve()
            if not config_path.is_file() or not config_path.is_relative_to(ROOT.resolve()):
                errors.append(f"{block_id}/{task_id}: runtime config is missing")
                continue
            config = _load(config_path)
            config_provider = config.get("provider")
            config_provider = config_provider if isinstance(config_provider, Mapping) else {}
            campaign = config.get("campaign")
            campaign = campaign if isinstance(campaign, Mapping) else {}
            identity = config.get("w2_26_runtime_identity")
            identity = identity if isinstance(identity, Mapping) else {}
            if (
                config.get("task_id") != task_id
                or config_provider.get("id") != "deepseek"
                or config_provider.get("model") != "deepseek-v4-flash"
                or set(config.get("prior_arms", {})) != set(ARMS)
                or campaign.get("complete_experiments") != rounds
                or identity.get("locus") != locus
                or identity.get("task_id") != task_id
                or identity.get("rounds") != rounds
            ):
                errors.append(f"{block_id}/{task_id}: runtime config differs from the plan")
            seeds = task.get("world_seeds")
            seeds = seeds if isinstance(seeds, list) else []
            if (
                len(seeds) != 5
                or len(set(seeds)) != 5
                or any(not isinstance(seed, int) or isinstance(seed, bool) for seed in seeds)
            ):
                errors.append(f"{block_id}/{task_id}: requires five unique integer worlds")
                continue
            for seed in seeds:
                if seed in all_seeds or seed in {0, 1, 2, 3, 4}:
                    errors.append(f"{block_id}/{task_id}: world identity is not fresh")
                all_seeds.add(seed)
                triplets.append(
                    {
                        "block": block_id,
                        "locus": locus,
                        "task_id": task_id,
                        "config_path": config_path,
                        "world_seed": seed,
                        "rounds": rounds,
                    }
                )
        sessions = len(tasks) * 5 * len(ARMS)
        experiments = sessions * rounds
        block_summaries[block_id] = {
            "tasks": len(tasks),
            "triplets": len(tasks) * 5,
            "sessions": sessions,
            "complete_experiments": experiments,
        }
        if sessions != expected["sessions"] or experiments != expected["experiments"]:
            errors.append(f"{block_id}: scheduled denominator differs")
    if observed_blocks != set(EXPECTED_BLOCKS):
        errors.append("plan lacks the exact A-E public, A-P, and A-S blocks")
    expected_totals = plan.get("expected_public_totals")
    actual_totals = {
        "task_world_clusters": len(triplets),
        "sessions": len(triplets) * len(ARMS),
        "complete_experiments": sum(row["rounds"] * len(ARMS) for row in triplets),
    }
    if expected_totals != actual_totals or actual_totals != {
        "task_world_clusters": 45,
        "sessions": 135,
        "complete_experiments": 1260,
    }:
        errors.append("public C2 totals are not exactly 45/135/1260")
    private = plan.get("private_block")
    private = private if isinstance(private, Mapping) else {}
    seal = (ROOT / str(private.get("seal", ""))).resolve()
    if (
        private.get("sessions") != 75
        or private.get("complete_experiments") != 600
        or private.get("start_condition")
        != "all_public_cells_terminal_and_public_analysis_frozen"
        or not seal.is_file()
        or not seal.is_relative_to((ROOT / "runs/private").resolve())
    ):
        errors.append("sealed A-E private follow-up is not fixed at 75/600")
    if plan.get("expected_complete_totals") != {
        "sessions": 210,
        "complete_experiments": 1860,
    }:
        errors.append("complete C2 totals are not exactly 210/1860")
    if errors:
        raise ValueError("; ".join(errors))
    return plan, triplets


class Progress:
    def __init__(self, path: Path) -> None:
        self.path = path.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def emit(self, payload: Mapping[str, Any]) -> None:
        row = {"time": time.time(), **dict(payload)}
        with self.lock, self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()


def _cell_summary(output_root: Path, cell_id: str) -> dict[str, Any] | None:
    path = output_root / "cells" / cell_id / "summary.json"
    if not path.is_file():
        return None
    try:
        value = _load(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    binding = value.get("prospective_cohort_cell")
    if (
        value.get("prospective_formal_result") is not True
        or not isinstance(binding, Mapping)
        or binding.get("cell_id") != cell_id
    ):
        return None
    return value


def _run_triplet(
    triplet: Mapping[str, Any],
    *,
    plan_path: Path,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    block = str(triplet["block"])
    task_id = str(triplet["task_id"])
    seed = int(triplet["world_seed"])
    states: list[dict[str, Any]] = []
    for arm in ARMS:
        cell_id = _cell_id(block, task_id, seed, arm)
        existing = _cell_summary(output_root, cell_id)
        if existing is not None:
            states.append({"arm": arm, "cell_id": cell_id, "existing": existing})
            continue
        cell_root = output_root / "cells" / cell_id
        log_path = output_root / "logs" / f"{cell_id}.log"
        child_progress = output_root / "cell_progress" / f"{cell_id}.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        child_progress.parent.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            str(CELL_RUNNER),
            "--config",
            str(triplet["config_path"]),
            "--output",
            str(cell_root),
            "--progress-file",
            str(child_progress),
            "--world-seed",
            str(seed),
            "--prior-arm",
            arm,
            "--prospective-cohort-execution",
            "--prospective-cohort-plan",
            str(plan_path),
            "--prospective-cell-id",
            cell_id,
        ]
        log_handle = log_path.open("w", encoding="utf-8")
        kwargs: dict[str, Any] = {}
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            **kwargs,
        )
        states.append(
            {
                "arm": arm,
                "cell_id": cell_id,
                "process": process,
                "log_handle": log_handle,
                "log_path": log_path,
            }
        )
    progress.emit(
        {
            "event": "triplet_started",
            "block": block,
            "task_id": task_id,
            "world_seed": seed,
            "launched_cells": sum("process" in state for state in states),
        }
    )
    started = time.monotonic()
    next_heartbeat = started + 30.0
    while True:
        active = [
            state
            for state in states
            if "process" in state and state["process"].poll() is None
        ]
        if not active:
            break
        now = time.monotonic()
        if now >= next_heartbeat:
            progress.emit(
                {
                    "event": "triplet_heartbeat",
                    "block": block,
                    "task_id": task_id,
                    "world_seed": seed,
                    "active_cells": len(active),
                    "elapsed_seconds": round(now - started, 1),
                }
            )
            next_heartbeat = now + 30.0
        time.sleep(1.0)
    rows: list[dict[str, Any]] = []
    for state in states:
        if "process" in state:
            return_code = state["process"].wait()
            state["log_handle"].close()
        else:
            return_code = 0
        summary = _cell_summary(output_root, state["cell_id"])
        rows.append(
            {
                "cell_id": state["cell_id"],
                "arm": state["arm"],
                "terminal": summary is not None,
                "completed": summary.get("completed") is True if summary else False,
                "return_code": return_code,
                "failure": summary.get("failure") if summary else "missing_summary",
            }
        )
    result = {
        "block": block,
        "task_id": task_id,
        "world_seed": seed,
        "terminal_cells": sum(row["terminal"] for row in rows),
        "completed_cells": sum(row["completed"] for row in rows),
        "infrastructure_missing_cells": sum(not row["terminal"] for row in rows),
        "cells": rows,
    }
    progress.emit({"event": "triplet_finished", **result})
    return result


def _write_summary(
    plan: Mapping[str, Any],
    triplets: list[Mapping[str, Any]],
    output_root: Path,
) -> dict[str, Any]:
    cells: list[dict[str, Any]] = []
    for triplet in triplets:
        for arm in ARMS:
            cell_id = _cell_id(
                str(triplet["block"]),
                str(triplet["task_id"]),
                int(triplet["world_seed"]),
                arm,
            )
            summary = _cell_summary(output_root, cell_id)
            cells.append(
                {
                    "cell_id": cell_id,
                    "block": triplet["block"],
                    "task_id": triplet["task_id"],
                    "world_seed": triplet["world_seed"],
                    "prior_arm": arm,
                    "scheduled_experiments": triplet["rounds"],
                    "terminal": summary is not None,
                    "completed": summary.get("completed") is True if summary else False,
                    "complete_experiments": (
                        summary.get("analysis", {}).get("complete_experiment_count", 0)
                        if summary
                        else 0
                    ),
                    "failure": summary.get("failure") if summary else "missing_summary",
                }
            )
    terminal = sum(row["terminal"] for row in cells)
    completed = sum(row["completed"] for row in cells)
    experiments = sum(int(row["complete_experiments"]) for row in cells)
    report = {
        "schema_version": "chemworld-work-ii-deepseek-c2-public-progress-0.1",
        "cohort_id": plan.get("cohort_id"),
        "prospective_formal_result": terminal == len(cells),
        "status": "all_public_cells_terminal" if terminal == len(cells) else "in_progress",
        "expected_sessions": len(cells),
        "terminal_sessions": terminal,
        "completed_sessions": completed,
        "retained_noncompleted_sessions": terminal - completed,
        "missing_sessions": len(cells) - terminal,
        "expected_complete_experiments": 1260,
        "observed_complete_experiments": experiments,
        "cells": cells,
    }
    write_json_atomic(output_root / "summary.json", report)
    return report


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-concurrent-triplets", type=int)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    plan_path = args.plan.resolve()
    plan, triplets = validate_and_expand(plan_path)
    if args.check:
        print(
            json.dumps(
                {
                    "status": "ready",
                    "task_world_clusters": len(triplets),
                    "sessions": len(triplets) * 3,
                    "complete_experiments": sum(row["rounds"] * 3 for row in triplets),
                    "private_sessions_after_public": 75,
                    "private_complete_experiments_after_public": 600,
                    "complete_sessions": 210,
                    "complete_experiments": 1860,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0
    if args.output is None or args.progress_file is None:
        raise RuntimeError("--execute requires --output and --progress-file")
    output_root = args.output.resolve()
    if output_root.exists() and not args.resume:
        raise FileExistsError(f"refusing to overwrite cohort output: {output_root}")
    if not output_root.exists() and args.resume:
        raise FileNotFoundError("--resume requires an existing cohort output")
    output_root.mkdir(parents=True, exist_ok=args.resume)
    plan_copy = output_root / "execution_plan.json"
    if plan_copy.exists():
        if _load(plan_copy) != plan:
            raise RuntimeError("existing cohort output uses a different execution plan")
    else:
        write_json_atomic(plan_copy, plan)
    progress = Progress(args.progress_file)
    pending = [
        triplet
        for triplet in triplets
        if any(
            _cell_summary(
                output_root,
                _cell_id(
                    str(triplet["block"]),
                    str(triplet["task_id"]),
                    int(triplet["world_seed"]),
                    arm,
                ),
            )
            is None
            for arm in ARMS
        )
    ]
    concurrency = args.max_concurrent_triplets or int(
        plan.get("execution", {}).get("max_concurrent_triplets", 3)
    )
    if concurrency < 1:
        raise ValueError("max concurrent triplets must be positive")
    progress.emit(
        {
            "event": "public_c2_started" if not args.resume else "public_c2_resumed",
            "expected_triplets": len(triplets),
            "pending_triplets": len(pending),
            "expected_sessions": len(triplets) * 3,
            "max_concurrent_triplets": concurrency,
        }
    )
    infrastructure_pause = False
    for offset in range(0, len(pending), concurrency):
        batch = pending[offset : offset + concurrency]
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [
                pool.submit(
                    _run_triplet,
                    triplet,
                    plan_path=plan_path,
                    output_root=output_root,
                    progress=progress,
                )
                for triplet in batch
            ]
            for future in as_completed(futures):
                result = future.result()
                if result["infrastructure_missing_cells"] == 3:
                    infrastructure_pause = True
        summary = _write_summary(plan, triplets, output_root)
        progress.emit(
            {
                "event": "public_c2_batch_finished",
                "terminal_sessions": summary["terminal_sessions"],
                "expected_sessions": summary["expected_sessions"],
                "observed_complete_experiments": summary["observed_complete_experiments"],
                "expected_complete_experiments": 1260,
            }
        )
        if infrastructure_pause:
            break
    summary = _write_summary(plan, triplets, output_root)
    if infrastructure_pause and summary["status"] != "all_public_cells_terminal":
        summary["status"] = "paused_after_triplet_wide_infrastructure_failure"
        write_json_atomic(output_root / "summary.json", summary)
    progress.emit({"event": "public_c2_attempt_finished", **summary})
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
    return 0 if summary["status"] == "all_public_cells_terminal" else 1


if __name__ == "__main__":
    raise SystemExit(main())
