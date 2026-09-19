#!/usr/bin/env python3
"""Recover EQ cells at frozen, auditable source or posttest boundaries."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_bounded_equilibrium as eq
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records

STAGES = ("K1", "Q", "K2")


def interrupted_snapshot(
    root: Path, config: Mapping[str, Any], cell: Mapping[str, Any]
) -> tuple[dict[str, Any] | None, Path]:
    """Load a sealed result or conservatively snapshot an interrupted write-once cell."""
    folder = root / "sources" / cell["cell_id"]
    result_path = folder / "RESULT.json"
    if result_path.is_file():
        return eq.read(result_path), folder
    if not folder.is_dir():
        return None, folder
    trajectory = folder / "trajectory.jsonl"
    records = load_jsonl(trajectory) if trajectory.is_file() else []
    world = eq.world_by_id(config, cell["world_id"])
    batches = eq.shared.summaries(records)
    replay = (
        verify_records(
            records,
            tolerance=0,
            world_interventions=copy.deepcopy(world["world_interventions"]),
        ).to_dict()
        if records
        else {"verified": False}
    )
    posttests: dict[str, Any] = {}
    validation: dict[str, Any] = {}
    for stage in STAGES:
        sealed = folder / "sealed" / f"{stage}.json"
        if not sealed.is_file():
            continue
        turn = eq.read(sealed)
        posttests[stage] = turn
        validation[stage] = eq.validate_posttest(
            stage, turn.get("payload"), eq.queries(config)
        )
    receipts_path = folder / "private-provider" / "source-receipts.json"
    receipts = eq.read(receipts_path) if receipts_path.is_file() else []
    thread_id = receipts[-1].get("thread_id") if receipts else None
    source_complete = len(batches) == 12 and replay.get("verified") is True
    snapshot = {
        "schema_version": "work-ii-eq-interrupted-snapshot-1.0",
        "cell_id": cell["cell_id"],
        "world_id": cell["world_id"],
        "arm": cell["arm"],
        "goal": cell["goal"],
        "status": "interrupted",
        "failure": {"type": "process_interruption", "message": "RESULT.json was not sealed"},
        "batches": batches,
        "operations": len(records),
        "rollbacks": [],
        "exact_replay": replay,
        "source_status": "completed" if source_complete else "partial" if batches else "failed",
        "posttests": posttests,
        "posttest_validation": validation,
        "posttest_chain_sealed": all(
            validation.get(stage, {}).get("valid") is True for stage in STAGES
        ),
        "thread_id_sha256": (
            eq.hashlib.sha256(str(thread_id).encode()).hexdigest() if thread_id else None
        ),
    }
    return snapshot, folder


def recovery_kind(result: Mapping[str, Any] | None, folder: Path) -> str | None:
    if result is None:
        return None
    if result.get("status") == "completed" and result.get("posttest_chain_sealed") is True:
        return None
    if (
        result.get("source_status") == "completed"
        and result.get("exact_replay", {}).get("verified") is True
        and (folder / "private-provider" / "source-receipts.json").is_file()
    ):
        return "posttests"
    return "fresh_source"


def latest_recovery(
    root: Path, cell_id: str, *, completed_only: bool = True
) -> tuple[dict[str, Any], Path] | None:
    base = root / "recoveries" / cell_id
    if not base.is_dir():
        return None
    for manifest in sorted(base.glob("attempt-*/recovery.json"), reverse=True):
        record = eq.read(manifest)
        result_path = Path(record["result_path"])
        if not result_path.is_absolute():
            result_path = root / result_path
        if result_path.is_file():
            result = eq.read(result_path)
            if not completed_only or (
                result.get("status") == "completed"
                and result.get("posttest_chain_sealed") is True
            ):
                return result, result_path
    return None


def effective_result(
    root: Path, config: Mapping[str, Any], cell: Mapping[str, Any]
) -> tuple[dict[str, Any] | None, Path]:
    original, folder = interrupted_snapshot(root, config, cell)
    if original and original.get("status") == "completed" and original.get("posttest_chain_sealed"):
        return original, folder / "RESULT.json"
    recovered = latest_recovery(root, cell["cell_id"])
    return recovered if recovered is not None else (original, folder / "RESULT.json")


def _thread_id(folder: Path) -> str:
    receipts = eq.read(folder / "private-provider" / "source-receipts.json")
    thread_id = receipts[-1].get("thread_id") if receipts else None
    if not thread_id:
        raise RuntimeError("completed EQ source has no resumable provider thread")
    return str(thread_id)


def recover_posttests(
    config: Mapping[str, Any], original: Mapping[str, Any], folder: Path, output: Path
) -> dict[str, Any]:
    """Reuse a completed source thread; never rerun its laboratory trajectory."""
    result = copy.deepcopy(dict(original))
    result["status"] = "recovering"
    result["failure"] = None
    private = output / "private-provider"
    home = private / "home"
    home.mkdir(parents=True)
    environment = _prepare_codex_home(home, eq.PROVIDER)
    source_sessions = folder / "private-provider" / "home" / "codex-home" / "sessions"
    if not source_sessions.is_dir():
        raise RuntimeError("completed EQ source has no resumable session store")
    shutil.copytree(source_sessions, home / "codex-home" / "sessions")
    agent = SimpleNamespace(home_root=home, followup_environment=environment)
    thread_id = _thread_id(folder)
    query_rows = eq.queries(config)
    started = time.monotonic()
    for stage in STAGES:
        previous = result.get("posttests", {}).get(stage, {})
        previous_validation = eq.validate_posttest(stage, previous.get("payload"), query_rows)
        if previous_validation["valid"]:
            result.setdefault("posttest_validation", {})[stage] = previous_validation
            continue
        turn = eq.run_posttest(
            agent,
            output,
            private,
            stage,
            thread_id,
            {"stage": result["cell_id"], "phase": stage, "recovery": True},
            query_rows,
        )
        result.setdefault("posttests", {})[stage] = turn
        validation = eq.validate_posttest(stage, turn.get("payload"), query_rows)
        result.setdefault("posttest_validation", {})[stage] = validation
        if not validation["valid"]:
            result["failure"] = {"type": "posttest_recovery_failure", "stage": stage, "message": validation["failure"]}
            break
    result["posttest_chain_sealed"] = all(
        result.get("posttest_validation", {}).get(stage, {}).get("valid") is True
        for stage in STAGES
    )
    result["status"] = "completed" if result["posttest_chain_sealed"] else "retained_nonconforming"
    result["recovery"] = {
        "kind": "posttests",
        "source_experiments_rerun": False,
        "thread_reused": True,
        "truth_revealed_to_agent": False,
        "question_changed": False,
        "model_changed": False,
    }
    result["recovery_elapsed_s"] = time.monotonic() - started
    eq.write(output / "RESULT.json", result)
    return result


def recover_one(
    root: Path,
    config: Mapping[str, Any],
    cell: Mapping[str, Any],
    *,
    attempt: int,
) -> dict[str, Any] | None:
    original, folder = interrupted_snapshot(root, config, cell)
    previous = latest_recovery(root, cell["cell_id"], completed_only=False)
    if previous is not None:
        original, result_path = previous
        folder = result_path.parent
    kind = recovery_kind(original, folder)
    if kind is None:
        return None
    output = root / "recoveries" / cell["cell_id"] / f"attempt-{attempt:02d}"
    if output.exists():
        raise RuntimeError(f"write-once recovery attempt already exists: {output}")
    output.mkdir(parents=True)
    eq.write(
        output / "attempt.json",
        {
            "schema_version": "work-ii-eq-recovery-attempt-1.0",
            "cell_id": cell["cell_id"],
            "attempt": attempt,
            "kind": kind,
            "started_epoch": time.time(),
            "original_preserved": True,
            "truth_revealed_to_agent": False,
        },
    )
    if kind == "posttests":
        assert original is not None
        result = recover_posttests(config, original, folder, output)
        result_path = output / "RESULT.json"
    else:
        progress: dict[str, Any] = {}
        result = eq.run_cell(
            output / "execution", config, cell, progress, threading.Lock()
        )
        result_path = output / "execution" / "sources" / cell["cell_id"] / "RESULT.json"
    record = {
        "schema_version": "work-ii-eq-recovery-record-1.0",
        "cell_id": cell["cell_id"],
        "attempt": attempt,
        "kind": kind,
        "status": result.get("status"),
        "result_path": os.path.relpath(result_path, root),
        "original_preserved": True,
        "truth_revealed_to_agent": False,
        "completed_epoch": time.time(),
    }
    eq.write(output / "recovery.json", record)
    return record


def plan(
    root: Path, config: Mapping[str, Any], schedule: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    rows = []
    for cell in schedule:
        effective, effective_path = effective_result(root, config, cell)
        original, folder = interrupted_snapshot(root, config, cell)
        rows.append(
            {
                "cell_id": cell["cell_id"],
                "effective_status": effective.get("status") if effective else "not_started",
                "effective_result": os.path.relpath(effective_path, root),
                "next_recovery": recovery_kind(original, folder),
            }
        )
    return rows


def finalize(
    root: Path, config: Mapping[str, Any], schedule: Sequence[Mapping[str, Any]]
) -> dict[str, Any] | None:
    resolved = [effective_result(root, config, cell) for cell in schedule]
    if len(resolved) != 15 or not all(
        result
        and result.get("status") == "completed"
        and result.get("posttest_chain_sealed") is True
        for result, _ in resolved
    ):
        return None
    truth = eq.generate_truth(root, config)
    for result, _ in resolved:
        assert result is not None
        evaluation = eq.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            eq.queries(config),
            truth[result["world_id"]],
        )
        eq.write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = {
        "schema_version": "work-ii-eq-effective-summary-1.0",
        "phase": "complete",
        "planned_sources": 15,
        "effective_sources": 15,
        "effective_source_batches": sum(len(result.get("batches", [])) for result, _ in resolved if result),
        "sealed_posttests": sum(len(result.get("posttests", {})) for result, _ in resolved if result),
        "sealed_posttest_chains": sum(result.get("posttest_chain_sealed") is True for result, _ in resolved if result),
        "failures": [],
        "cells": [
            {
                "cell_id": result["cell_id"],
                "status": result["status"],
                "effective_result": os.path.relpath(path, root),
            }
            for result, path in resolved
            if result
        ],
    }
    eq.write(root / "effective-summary.json", summary)
    completion = {
        "schema_version": "work-ii-eq-completion-1.1",
        "completed_epoch": time.time(),
        "source_sessions": 15,
        "source_batches": 180,
        "posttests": 45,
        "reference_executions": 300,
        "equilibrium_confidence_used_as_agent_uncertainty_or_score": False,
        "effective_summary_sha256": eq.digest(summary),
    }
    eq.write(root / "completion.json", completion)
    return completion


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("plan", "execute"), default="plan")
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--cell", action="append", default=[])
    args = parser.parse_args()
    if args.attempt < 1:
        raise ValueError("attempt must be positive")
    root = args.output.resolve()
    config = eq.load_config()
    validated = eq.validate_design(config)
    eq.configure_provider_helpers(config)
    eq.validate_freeze(root, config)
    schedule = validated["schedule"]
    selected = set(args.cell)
    current_plan = plan(root, config, schedule)
    print(json.dumps({"stage": "recovery_plan", "cells": current_plan}), flush=True)
    if args.mode == "plan":
        return
    for cell in schedule:
        if selected and cell["cell_id"] not in selected:
            continue
        record = recover_one(root, config, cell, attempt=args.attempt)
        if record:
            print(json.dumps({"stage": "recovery_complete", **record}), flush=True)
    completion = finalize(root, config, schedule)
    print(json.dumps({"stage": "recovery_finalize", "completion": completion}), flush=True)


if __name__ == "__main__":
    main()
