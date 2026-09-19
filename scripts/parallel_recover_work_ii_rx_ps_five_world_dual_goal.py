#!/usr/bin/env python3
"""Resume the frozen RX P/S block with four isolated worker processes."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.recover_work_ii_rx_ps_five_world_dual_goal as recovery  # noqa: E402
import scripts.run_work_ii_rx_ps_five_world_dual_goal as campaign  # noqa: E402

RECOVERY_VERSION = "recovery-v7-parallel4"
TASK_26 = "RX-W03--P--mechanism_discovery--Aligned"
TASK_26_STAGES = ("Q", "K2")
DEFAULT_WORKERS = 4
HISTORICAL_MEDIAN_CELL_S = 703.3


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def result_candidates(root: Path, cell_id: str) -> tuple[Path, ...]:
    folder = root / "sources" / cell_id
    return (
        folder / "posttest-repair-v7" / "effective-result.json",
        folder / "posttest-repair-v3" / "effective-result.json",
        folder / "source-repair-v3" / "effective-result.json",
        folder / "result.json",
    )


def resolve_result(root: Path, cell_id: str) -> tuple[Path, dict[str, Any]] | None:
    for path in result_candidates(root, cell_id):
        if path.exists():
            return path, read(path)
    return None


def classify_schedule(
    root: Path, schedule: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    complete: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    for cell in schedule:
        resolved = resolve_result(root, str(cell["cell_id"]))
        if resolved is None:
            pending.append(dict(cell))
            continue
        _, result = resolved
        if result.get("status") == "completed" and result.get("posttest_chain_sealed") is True:
            complete.append(result)
            continue
        if cell["cell_id"] == TASK_26 and result.get("source_status") == "completed":
            pending.append(dict(cell))
            continue
        raise RuntimeError(f"unplanned nonconforming cell: {cell['cell_id']}")
    return complete, pending


def repair_task_26(
    root: Path,
    cell: Mapping[str, Any],
    config: Mapping[str, Any],
    progress: dict[str, Any],
) -> dict[str, Any]:
    original_folder = root / "sources" / TASK_26
    original_path = original_folder / "result.json"
    original = read(original_path)
    repair = original_folder / "posttest-repair-v7"
    effective_path = repair / "effective-result.json"
    if effective_path.exists():
        return read(effective_path)
    if repair.exists():
        raise RuntimeError("incomplete write-once task-26 repair requires inspection")
    if original.get("source_status") != "completed" or len(original.get("batches", [])) != 12:
        raise RuntimeError("task 26 does not have the required sealed twelve-batch source")
    if not original.get("posttests", {}).get("K1", {}).get("payload"):
        raise RuntimeError("task 26 has no valid K1 to preserve")

    repair.mkdir(parents=True)
    receipts = read(original_folder / "source-receipts.json")
    thread_id = receipts[-1].get("thread_id") if receipts else None
    if not thread_id:
        raise RuntimeError("task 26 has no resumable source thread")
    manifest = {
        "schema_version": "work-ii-rx-ps-posttest-repair-1.0",
        "recovery_version": RECOVERY_VERSION,
        "cell_id": TASK_26,
        "started_epoch": time.time(),
        "original_result_sha256": recovery.file_sha256(original_path),
        "source_experiments_rerun": False,
        "truth_revealed_to_agent": False,
        "question_changed": False,
        "model_changed": False,
        "thread_reused": True,
        "repair_stages": list(TASK_26_STAGES),
        "public_numerics_limit_recovery": recovery.NUMERICS_LIMIT,
    }
    write(repair / "manifest.json", manifest)
    query_rows = campaign.queries(config, str(cell["locus"]))
    repaired: dict[str, dict[str, Any]] = {}
    agent = recovery._repair_agent(original_folder, original, repair)
    try:
        recovery.restore_session_index(agent, original_folder / "provider-rollouts", thread_id)
        for stage in TASK_26_STAGES:
            progress.update(stage=TASK_26, phase=f"{stage}-repair", repair=True)
            turn = campaign.run_posttest(agent, repair, stage, thread_id, progress, query_rows)
            repaired[stage] = turn
            validation = campaign.validate_posttest_payload(stage, turn.get("payload"), query_rows)
            write(repair / f"{stage}-validation.json", validation)
            if validation.get("valid") is not True:
                break
            thread_id = turn.get("thread_id") or thread_id
    finally:
        agent.close()
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, repair / "provider-rollouts")
        agent._recovery_temporary_directory.cleanup()
    effective = recovery.merge_posttest_repair(original, repaired, query_rows)
    effective["recovery"] = manifest
    write(repair / "turns.json", repaired)
    write(effective_path, effective)
    if effective.get("status") != "completed":
        raise RuntimeError("task-26 posttest repair did not seal")
    return effective


def run_one(root_text: str, cell: Mapping[str, Any]) -> dict[str, Any]:
    started = time.monotonic()
    root = Path(root_text)
    recovery.configure_recovery_helpers()
    config = read(campaign.CONFIG)
    validated = campaign.validate_design(config)
    progress: dict[str, Any] = {
        "completed": 0,
        "total": 60,
        "stage": str(cell["cell_id"]),
        "phase": "parallel-recovery",
        "worker_pid": os.getpid(),
    }
    if cell["cell_id"] == TASK_26:
        result = repair_task_26(root, cell, config, progress)
    else:
        if (root / "sources" / str(cell["cell_id"])).exists():
            raise RuntimeError(f"refusing to overwrite existing cell directory: {cell['cell_id']}")
        result = campaign.run_cell(
            root,
            cell,
            p_package=validated["p_package"],
            s_contract=validated["s_contract"],
            config=config,
            progress=progress,
        )
    if result.get("status") != "completed" or result.get("posttest_chain_sealed") is not True:
        raise RuntimeError(f"cell did not seal: {cell['cell_id']}")
    return {
        "cell_id": result["cell_id"],
        "status": result["status"],
        "source_batches": len(result.get("batches", [])),
        "posttest_chain_sealed": result.get("posttest_chain_sealed"),
        "worker_pid": os.getpid(),
        "worker_elapsed_s": time.monotonic() - started,
    }


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def compact_results(root: Path, schedule: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cell in schedule:
        resolved = resolve_result(root, str(cell["cell_id"]))
        if resolved is None:
            continue
        path, result = resolved
        rows.append(
            {
                "cell_id": result.get("cell_id", cell["cell_id"]),
                "status": result.get("status"),
                "source_status": result.get("source_status"),
                "source_batches": len(result.get("batches", [])),
                "posttest_chain_sealed": result.get("posttest_chain_sealed"),
                "failure": result.get("failure"),
                "effective_result": str(path.relative_to(root)),
            }
        )
    return rows


def write_summary(
    recovery_root: Path,
    root: Path,
    schedule: Sequence[Mapping[str, Any]],
    *,
    phase: str,
    completed_work_items: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
) -> None:
    rows = compact_results(root, schedule)
    write(
        recovery_root / "summary.json",
        {
            "schema_version": "work-ii-rx-ps-parallel-recovery-summary-1.0",
            "recovery_version": RECOVERY_VERSION,
            "phase": phase,
            "workers": DEFAULT_WORKERS,
            "planned_sources": 60,
            "planned_source_batches": 720,
            "planned_posttests": 180,
            "effective_sources": sum(row["status"] == "completed" for row in rows),
            "effective_source_batches": sum(
                row["source_batches"] for row in rows if row["status"] == "completed"
            ),
            "sealed_posttest_chains": sum(
                row["posttest_chain_sealed"] is True for row in rows
            ),
            "truth_embargo_active": phase != "complete",
            "completed_work_items": list(completed_work_items),
            "failures": list(failures),
            "results": rows,
        },
    )


def finalize(
    root: Path,
    recovery_root: Path,
    schedule: Sequence[Mapping[str, Any]],
    config: Mapping[str, Any],
    completed_work_items: Sequence[Mapping[str, Any]],
) -> None:
    results: list[dict[str, Any]] = []
    for cell in schedule:
        resolved = resolve_result(root, str(cell["cell_id"]))
        if resolved is None:
            raise RuntimeError(f"missing result before truth release: {cell['cell_id']}")
        _, result = resolved
        if result.get("status") != "completed" or result.get("posttest_chain_sealed") is not True:
            raise RuntimeError(f"unsealed result before truth release: {cell['cell_id']}")
        results.append(result)
    write_summary(
        recovery_root,
        root,
        schedule,
        phase="sources_and_posttests_complete_truth_embargoed",
        completed_work_items=completed_work_items,
        failures=[],
    )
    print(json.dumps({"stage": "reference_truth", "phase": "provider_free", "completed": 60, "total": 60}), flush=True)
    truth = campaign.generate_truth(root, config)
    retests = 0
    for index, result in enumerate(results, start=1):
        query_rows = campaign.queries(config, result["locus"])
        evaluation = campaign.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            query_rows,
            truth[result["world_id"]][result["locus"]],
        )
        write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
        retest = campaign.run_recommendation_retest(root, result)
        if retest is not None:
            if (
                retest["failure"]
                or len(retest["batches"]) != 1
                or retest["rollbacks"]
                or retest["exact_replay"].get("verified") is not True
            ):
                raise RuntimeError(f"recommendation retest failed: {result['cell_id']}")
            retests += 1
        print(json.dumps({"stage": "evaluation_and_retest", "completed": index, "total": 60, "cell": result["cell_id"]}), flush=True)
    write_summary(
        recovery_root,
        root,
        schedule,
        phase="complete",
        completed_work_items=completed_work_items,
        failures=[],
    )
    write(
        recovery_root / "completion.json",
        {
            "completed_epoch": time.time(),
            "source_sessions": 60,
            "source_batches": 720,
            "posttests": 180,
            "reference_executions": 600,
            "recommendation_retests": retests,
            "original_failures_preserved": True,
            "parallel_workers": DEFAULT_WORKERS,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    args = parser.parse_args()
    if args.workers != DEFAULT_WORKERS:
        raise RuntimeError("this frozen recovery authorizes exactly four workers")

    root = args.root.resolve()
    config = read(campaign.CONFIG)
    validated = campaign.validate_design(config)
    existing_design = read(root / "design.json")
    if existing_design.get("frozen_config_sha256") != campaign.digest(config):
        raise RuntimeError("existing run is not bound to the frozen recovery config")
    if (root / "reference-truth").exists():
        raise RuntimeError("reference truth already exists before parallel recovery")

    complete, pending = classify_schedule(root, validated["schedule"])
    pending_ids = [str(cell["cell_id"]) for cell in pending]
    if len(complete) != 25 or len(pending) != 35 or pending_ids[0] != TASK_26:
        raise RuntimeError(
            f"unexpected recovery frontier: complete={len(complete)} pending={len(pending)} first={pending_ids[:1]}"
        )

    recovery_root = root / RECOVERY_VERSION
    recovery_root.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema_version": "work-ii-rx-ps-parallel-recovery-1.0",
        "recovery_version": RECOVERY_VERSION,
        "started_epoch": time.time(),
        "execution_commit": git_head(),
        "parallel_workers": DEFAULT_WORKERS,
        "complete_before_start": len(complete),
        "work_items": pending_ids,
        "task_26_repair_stages": list(TASK_26_STAGES),
        "new_source_cells": len(pending) - 1,
        "truth_revealed_before_all_cells_sealed": False,
        "historical_median_cell_s": HISTORICAL_MEDIAN_CELL_S,
        "initial_source_eta_s": HISTORICAL_MEDIAN_CELL_S * 9,
    }
    write(recovery_root / "manifest.json", manifest)

    state: dict[str, Any] = {
        "completed": 0,
        "total": len(pending),
        "phase": "parallel_sources_and_posttests",
        "workers": DEFAULT_WORKERS,
    }
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            done = int(state["completed"])
            remaining = len(pending) - done
            elapsed = time.monotonic() - started
            if done:
                throughput_eta = elapsed / done * remaining
                eta = max(throughput_eta, 0.0)
            else:
                eta = HISTORICAL_MEDIAN_CELL_S * ((remaining + DEFAULT_WORKERS - 1) // DEFAULT_WORKERS)
            print(
                json.dumps(
                    {
                        **state,
                        "effective_tasks": 25 + done,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(eta),
                    }
                ),
                flush=True,
            )

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    completed_work_items: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    pool = ProcessPoolExecutor(
        max_workers=DEFAULT_WORKERS,
        mp_context=multiprocessing.get_context("spawn"),
    )
    futures = {pool.submit(run_one, str(root), cell): cell for cell in pending}
    try:
        for future in as_completed(futures):
            cell = futures[future]
            try:
                item = future.result()
                completed_work_items.append(item)
                state["completed"] = len(completed_work_items)
                state["last_cell"] = item["cell_id"]
                print(json.dumps({**item, "completed_work_items": len(completed_work_items), "total_work_items": len(pending)}), flush=True)
                write_summary(
                    recovery_root,
                    root,
                    validated["schedule"],
                    phase="parallel_sources_and_posttests",
                    completed_work_items=completed_work_items,
                    failures=failures,
                )
            except Exception as exc:
                failures.append(
                    {
                        "cell_id": cell["cell_id"],
                        "type": type(exc).__name__,
                        "message": str(exc)[:2000],
                    }
                )
                for queued in futures:
                    queued.cancel()
                break
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
        stop.set()
        heartbeat_thread.join(timeout=2)

    if failures:
        write_summary(
            recovery_root,
            root,
            validated["schedule"],
            phase="failed_closed_truth_embargoed",
            completed_work_items=completed_work_items,
            failures=failures,
        )
        raise RuntimeError(f"parallel recovery failed closed: {failures[0]}")
    if len(completed_work_items) != len(pending):
        raise RuntimeError("parallel recovery ended without all work items")
    finalize(root, recovery_root, validated["schedule"], config, completed_work_items)


if __name__ == "__main__":
    main()
