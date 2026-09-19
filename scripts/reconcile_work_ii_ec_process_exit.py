"""Seal the observed 17:17 EC process loss; preserve physics and provider context."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path

import psutil
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_ec_pa_matrix as matrix
from scripts import run_work_ii_ec_pa_parallel as parallel
from scripts import seal_work_ii_ec_host_interruption as host
from scripts.recover_work_ii_ec_pa_network import STAGES
from scripts.run_work_ii_astra_single_trial import read, write


def events(path):
    return [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]


def retained_home(actual):
    thread = {
        e["thread_id"]
        for e in events(actual / "source-stdout.jsonl")
        if e.get("type") == "thread.started"
    }
    if len(thread) != 1:
        raise ValueError("source must have one attributable thread")
    thread = next(iter(thread))
    homes = [
        h
        for h in Path(tempfile.gettempdir()).glob("chemworld-ec-sol-*")
        if list((h / "codex-home/sessions").rglob(f"*{thread}*.jsonl"))
    ]
    if len(homes) != 1:
        raise ValueError("cannot identify exactly one retained home")
    session = next((homes[0] / "codex-home/sessions").rglob(f"*{thread}*.jsonl"))
    if not any(
        e.get("type") == "session_meta" and e.get("payload", {}).get("id") == thread
        for e in events(session)
    ):
        raise ValueError("rollout thread identity mismatch")
    for p in psutil.process_iter(["pid", "cmdline"]):
        if p.pid == psutil.Process().pid:
            continue
        if any(str(homes[0]).lower() in a.lower() for a in p.info["cmdline"] or []):
            raise RuntimeError("retained home still has a live process")
    return homes[0], thread


def seal_posttests(unit, actual, home, thread):
    result = read(actual / "result.json")
    if result.get("interruption", {}).get("classification") == "process_exit":
        return result
    if result.get("source_status") != "completed" or not result["exact_replay"]["verified"]:
        raise ValueError("posttest restoration requires intact source and replay")
    if read(actual / "source-receipts.json")[-1]["thread_id"] != thread:
        raise ValueError("source receipt and retained rollout differ")
    missing = [s for s in STAGES if not result["posttests"].get(s, {}).get("payload")]
    if not missing:
        raise ValueError("completed answers must not be relabelled")
    stage = missing[0]
    log = actual / stage / "stdout.jsonl"
    if not log.is_file() or any(
        e.get("type") in ("turn.completed", "turn.failed") for e in events(log)
    ):
        raise ValueError("expected an abruptly interrupted posttest")
    shutil.copyfile(actual / "result.json", actual / "result-before-process-interruption.json")
    shutil.copytree(home / "codex-home/sessions", actual / "provider-rollouts")
    result["posttests"][stage] = {
        "payload": None,
        "failure": "process_interrupted",
        "thread_id": thread,
        "host_diagnosis_only": True,
    }
    result["interruption"] = {
        "classification": "process_exit",
        "boundary": "posttests",
        "stage": stage,
        "source_thread": thread,
        "initiating_cause": "unknown",
        "detected_time": datetime.now().astimezone().isoformat(),
        "token_accounting_complete": False,
    }
    result["failure"] = {"type": "process_exit", "stage": stage, "message": "process_interrupted"}
    result["posttest_status"] = "interrupted"
    result["status"] = "failed"
    result["elapsed_s"] = log.stat().st_mtime - read(actual / "attempt.json")["started_epoch"]
    # The recommendation was already sealed, but the original runner had not reached its retest.
    if not result.get("recommendation_retest"):
        selected = (result.get("recommendation") or {}).get("selected_experiment_index")
        batch = next((b for b in result["batches"] if b["lifecycle_index"] == selected), None)
        if batch is not None:
            print(
                json.dumps({"unit": unit["unit_id"], "stage": "pending_recommendation_retest"}),
                flush=True,
            )
            result["recommendation_retest"] = ec.reference_run(
                actual / "recommendation-retest",
                batch["actions"],
                observation_seed=101,
                source_envelope=True,
                source_budget=unit["budget"],
                world=unit["world"],
            )
            if not result["recommendation_retest"]["exact_replay"]["verified"]:
                raise RuntimeError("pending recommendation retest failed replay")
    write(actual / "process-interruption.json", result["interruption"])
    write(actual / "result.json", result)
    return result


def reconcile(root, report):
    state = read(root / "summary.json")
    workers = state["progress"].get("workers", [])
    expected = {
        "EC-W05-B24-discovery-E-Opaque",
        "EC-W05-B24-optimization-E-Aligned",
        "EC-W05-B24-optimization-E-MisIndexed",
        "EC-W05-B24-optimization-E-Opaque",
    }
    if state["status"] != "running" or {w["unit"] for w in workers} != expected:
        raise ValueError("this reconciliation is scoped to the retained 17:17 incident")
    pids = [state["parallel_execution"]["coordinator_pid"], *[w["pid"] for w in workers]]
    if any(psutil.pid_exists(p) for p in pids):
        raise RuntimeError("coordinator/worker PID still exists; do not duplicate work")
    write(root / "summary-before-process-exit-reconciliation.json", state)
    units = {u["unit_id"]: u for u in read(root / "design.json")["units"]}
    for uid in sorted(expected):
        unit = units[uid]
        parent, original = parallel.unit_paths(root, unit)
        replacement = root / "recoveries" / uid / "attempt-1"
        actual = (
            replacement / "discovery-E-Opaque" if uid.endswith("discovery-E-Opaque") else original
        )
        home, thread = retained_home(actual)
        if (actual / "result.json").is_file():
            result = seal_posttests(unit, actual, home, thread)
        else:
            result = host.seal(
                unit,
                actual,
                home,
                reboot_time=datetime.now().astimezone().isoformat(),
                classification="process_exit",
            )
        design = read(parent / "design.json")
        if actual == original:
            matrix.export_source(unit, result, actual, report / uid, design)
        else:
            # This fresh-source recovery lost only its final record; retain its real cost once.
            public = report / uid / "network-recovery"
            row = matrix.export_source(unit, result, actual, public, design)
            rec = {
                "kind": read(replacement / "attempt.json")["kind"],
                "attempt": 1,
                "source_folder": str(actual),
                "row": row,
                "result_path": str(actual / "result.json"),
                "report_path": f"{uid}/network-recovery/REPORT.md",
                "new_source_attempts": 1,
                "new_source_batches": row["completed_batches"],
                "new_source_operations": row["operations"],
                "new_posttest_attempts": len(result["posttests"]),
                "additional_reported_usage": {
                    "known": row["token_accounting"].get("valid", False),
                    "tokens": row["token_accounting"].get("total"),
                },
                "failed_attempt_usage_complete": False,
                "elapsed_s": result["elapsed_s"],
                "original_status": "failed",
                "interruption": result["interruption"],
            }
            write(replacement / "recovery.json", rec)
            write(public / "recovery.json", rec)
        index = next(i for i, r in enumerate(state["results"]) if r["unit_id"] == uid)
        state["results"][index] = parallel.collect(root, unit)
        print(
            json.dumps(
                {
                    "sealed": uid,
                    "batches": len(result["batches"]),
                    "operations": result["operations"],
                    "boundary": result["interruption"]["boundary"],
                }
            ),
            flush=True,
        )
    incident = {
        "classification": "process_tree_disappeared",
        "initiating_cause": "unknown",
        "last_heartbeat": state["progress"]["elapsed_s"],
        "retained_workers": workers,
        "detected_epoch": time.time(),
        "authorization": "2026-09-19 user requested continuation and process-exit diagnosis",
    }
    state.setdefault("runtime_incidents", []).append(incident)
    state.update(
        status="stopped",
        failure={"unit": workers[0]["unit"], "message": "process_tree_disappeared"},
    )
    progress = {
        **state["progress"],
        "stage": "stopped",
        "workers": [],
        "active_sources": 0,
        "eta_s": None,
        **parallel.source_counts(state["results"], {}),
    }
    matrix.save_matrix_state(root, report, state, progress, elapsed_s=progress["elapsed_s"])
    parallel.write_json_atomic(root / "progress.json", {"heartbeat": progress})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    reconcile(args.output.resolve(), args.report.resolve())
