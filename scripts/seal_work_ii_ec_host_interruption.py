"""Retain an EC source lost in a diagnosed host reboot, without inventing a terminal receipt."""

from __future__ import annotations

import json
import shutil
from datetime import datetime

from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts.run_work_ii_astra_single_trial import read, write

from chemworld.data.logging import load_jsonl


def inspect_interruption(folder, home):
    """Require matching session ownership and an unfinished, durable physical prefix."""
    records = load_jsonl(folder / "trajectory.jsonl")
    if not records:
        raise ValueError("host-interruption recovery requires a nonempty physical prefix")
    events = [
        json.loads(line)
        for line in (folder / "source-stdout.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    threads = {e["thread_id"] for e in events if e.get("type") == "thread.started"}
    if len(threads) != 1 or any(e.get("type") in ("turn.completed", "turn.failed") for e in events):
        raise ValueError("requires one abruptly interrupted, nonterminal source thread")
    thread = next(iter(threads))
    sessions = list((home / "codex-home/sessions").rglob(f"*{thread}*.jsonl"))
    if len(sessions) != 1:
        raise ValueError("retained home does not uniquely match the interrupted source thread")
    session = [json.loads(line) for line in sessions[0].read_text(encoding="utf-8").splitlines()]
    if not any(
        e.get("type") == "session_meta" and e.get("payload", {}).get("id") == thread
        for e in session
    ):
        raise ValueError("retained rollout session identity mismatch")
    usage = next(
        (
            e["payload"].get("info", {}).get("total_token_usage")
            for e in reversed(session)
            if e.get("type") == "event_msg"
            and e.get("payload", {}).get("type") == "token_count"
            and e["payload"].get("info")
        ),
        None,
    )
    return records, thread, usage


def seal(unit, folder, home, *, reboot_time, classification="host_reboot"):
    if classification not in ("host_reboot", "process_exit"):
        raise ValueError("unsupported infrastructure interruption")
    if unit["system"] != "EC":
        raise ValueError("this diagnosed interruption is an EC source")
    if (folder / "result.json").exists():
        existing = read(folder / "result.json")
        if existing.get("interruption", {}).get("classification") != classification:
            raise ValueError("cannot relabel an existing result as a host interruption")
        return existing
    records, thread, usage = inspect_interruption(folder, home)
    last_time = datetime.fromisoformat(records[-1]["timestamp"])
    if datetime.fromisoformat(reboot_time) <= last_time:
        raise ValueError("reported reboot must follow the retained trajectory")
    replay = ec.replay_with_progress(
        records,
        f"host-interruption/{unit['unit_id']}",
        world_interventions=unit["world"].get("world_interventions"),
    )
    if not replay.get("verified"):
        raise RuntimeError("retained interrupted trajectory did not replay exactly")
    batches = ec.summaries(records)
    if len(batches) >= unit["budget"]:
        raise ValueError("complete physical source needs a different recovery boundary")
    for source, destination in (
        (home / "laboratory", folder / "workspace"),
        (home / "codex-home/sessions", folder / "provider-rollouts"),
    ):
        if not destination.exists():
            shutil.copytree(source, destination)
    failure = {
        "type": classification,
        "message": (
            "Host restarted during source execution; "
            if classification == "host_reboot"
            else "Execution processes disappeared during source execution; "
        )
        + "in-flight simulator/tool processes and terminal provider receipt were lost.",
    }
    interruption = {
        "classification": classification,
        "boundary": "source",
        "reboot_time" if classification == "host_reboot" else "detected_time": reboot_time,
        "source_thread": thread,
        "retained_operations": len(records),
        "retained_final_assays": len(batches),
        "last_durable_operation_time": records[-1]["timestamp"],
        "last_reported_thread_usage": usage,
        "token_accounting_complete": False,
        "usage_caveat": "Last reported cumulative usage is a lower bound; "
        "unfinished usage unknown.",
        "additional_replay_operations": replay["checked_steps"],
        "disposition": "Retain interrupted attempt; one explicitly authorized "
        "fresh source attempt.",
    }
    source_usage = dict(records[-1].get("method_resources", {}).get("agent_usage") or {})
    source_usage["provider_token_accounting_complete"] = False
    result = {
        "cell_id": f"{unit['goal']}-{unit['locus']}-{unit['arm']}",
        "goal": unit["goal"],
        "locus": unit["locus"],
        "arm": unit["arm"],
        "world": unit["world"]["world_id"],
        "planned_source_batches": unit["budget"],
        "status": "failed",
        "source_status": "interrupted",
        "source_failure": failure,
        "failure": failure,
        "interruption": interruption,
        "posttests": {},
        "posttest_status": "unavailable",
        "batches": batches,
        "operations": len(records),
        "rollbacks": [
            {"step": r["step"], "reason": r.get("rollback_reason")}
            for r in records
            if r.get("transaction_status") != "committed"
        ],
        "source_usage": source_usage,
        "exact_replay": replay,
        "recommendation": None,
        "elapsed_s": last_time.timestamp() - read(folder / "attempt.json")["started_epoch"],
    }
    name = (
        "host-interruption.json" if classification == "host_reboot" else "process-interruption.json"
    )
    write(folder / name, interruption)
    write(folder / "result.json", result)
    return result
