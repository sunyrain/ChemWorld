#!/usr/bin/env python3
"""Recover sealed EQ-S posttests without rerunning source experiments."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import time
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_structural_v0_2 as eq
from scripts.run_work_ii_study_b import _prepare_codex_home


def _source_thread_id(folder: Path) -> str:
    receipts = eq.read(folder / "private-provider" / "source-receipts.json")
    thread_id = receipts[-1].get("thread_id") if receipts else None
    if not thread_id:
        raise RuntimeError("completed EQ-S source has no resumable provider thread")
    return str(thread_id)


def recover_one(
    root: Path,
    config: Mapping[str, Any],
    cell: Mapping[str, Any],
    *,
    attempt: int,
) -> dict[str, Any]:
    source = root / "sources" / cell["cell_id"]
    original_path = source / "RESULT.json"
    if not original_path.is_file():
        raise RuntimeError(f"missing retained EQ-S result: {cell['cell_id']}")
    original = eq.read(original_path)
    if (
        original.get("source_status") != "completed"
        or original.get("exact_replay", {}).get("verified") is not True
        or len(original.get("batches", [])) != 12
    ):
        raise RuntimeError(f"EQ-S recovery refuses an incomplete source: {cell['cell_id']}")

    output = root / "recoveries" / cell["cell_id"] / f"attempt-{attempt:02d}"
    if output.exists():
        raise RuntimeError(f"write-once EQ-S recovery exists: {output}")
    private = output / "private-provider"
    home = private / "home"
    (output / "sealed").mkdir(parents=True)
    home.mkdir(parents=True)
    environment = _prepare_codex_home(home, eq.PROVIDER)
    sessions = source / "private-provider" / "home" / "codex-home" / "sessions"
    if not sessions.is_dir():
        raise RuntimeError(f"EQ-S source session store is missing: {cell['cell_id']}")
    shutil.copytree(sessions, home / "codex-home" / "sessions")
    shutil.copyfile(
        source / "private-provider" / "source-receipts.json",
        private / "source-receipts.json",
    )
    eq.write(
        output / "attempt.json",
        {
            "schema_version": "work-ii-eq-s-recovery-attempt-0.2.1",
            "cell_id": cell["cell_id"],
            "attempt": attempt,
            "kind": "posttests",
            "source_experiments_rerun": False,
            "original_preserved": True,
            "truth_revealed_to_agent": False,
            "scientific_contract_changed": False,
            "reason": "Responses API rejected unsupported uniqueItems in the EQS output schema.",
            "started_epoch": time.time(),
        },
    )
    agent = SimpleNamespace(home_root=home, followup_environment=environment)
    result = copy.deepcopy(original)
    result["status"] = "recovering"
    result["failure"] = None
    query_rows = eq.queries(config)
    thread_id = _source_thread_id(source)
    started = time.monotonic()
    for stage in eq.POSTTEST_STAGES:
        previous = result.get("posttests", {}).get(stage, {})
        validation = eq.validate_posttest(stage, previous.get("payload"), query_rows)
        if validation["valid"]:
            result.setdefault("posttest_validation", {})[stage] = validation
            continue
        turn = eq.eq_v2.run_posttest(
            agent,
            output,
            private,
            stage,
            thread_id,
            {"stage": cell["cell_id"], "phase": stage, "recovery": True},
            query_rows,
        )
        result.setdefault("posttests", {})[stage] = turn
        validation = eq.validate_posttest(stage, turn.get("payload"), query_rows)
        result.setdefault("posttest_validation", {})[stage] = validation
        if not validation["valid"]:
            result["failure"] = {
                "type": "posttest_recovery_failure",
                "stage": stage,
                "message": validation["failure"],
            }
            break
    result["posttest_chain_sealed"] = all(
        result.get("posttest_validation", {}).get(stage, {}).get("valid") is True
        for stage in eq.POSTTEST_STAGES
    )
    result["status"] = "completed" if result["posttest_chain_sealed"] else "retained_nonconforming"
    result["recovery"] = {
        "kind": "posttests",
        "source_experiments_rerun": False,
        "thread_reused": True,
        "truth_revealed_to_agent": False,
        "question_changed": False,
        "model_changed": False,
        "schema_compatibility_repair": "uniqueItems removed; local uniqueness validation retained",
    }
    result["recovery_elapsed_s"] = time.monotonic() - started
    eq.write(output / "RESULT.json", result)
    eq.write(
        output / "recovery.json",
        {
            "schema_version": "work-ii-eq-s-recovery-record-0.2.1",
            "cell_id": cell["cell_id"],
            "attempt": attempt,
            "status": result["status"],
            "result_path": str((output / "RESULT.json").relative_to(root)),
            "original_result_path": str(original_path.relative_to(root)),
            "original_preserved": True,
            "truth_revealed_to_agent": False,
            "completed_epoch": time.time(),
        },
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--cell", action="append", default=[])
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1 or not 1 <= args.workers <= 8:
        raise ValueError("attempt must be positive and workers must be in 1..8")
    root = args.output.resolve()
    config = eq.load_config()
    validated = eq.validate_design(config)
    eq.bind_v2_runtime(config)
    eq.eq_v2.validate_freeze(root, config)
    selected_ids = set(args.cell)
    selected = [
        cell
        for cell in validated["schedule"]
        if (not selected_ids or cell["cell_id"] in selected_ids)
        and eq.effective_result(root, cell)[0] is not None
        and eq.effective_result(root, cell)[0].get("status") != "completed"
    ]
    print(
        json.dumps(
            {"stage": "eq_s_recovery_plan", "cells": [cell["cell_id"] for cell in selected]},
            sort_keys=True,
        ),
        flush=True,
    )
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(recover_one, root, config, cell, attempt=args.attempt): cell
            for cell in selected
        }
        for future in as_completed(futures):
            cell = futures[future]
            result = future.result()
            print(
                json.dumps(
                    {
                        "stage": "eq_s_recovery_complete",
                        "cell_id": cell["cell_id"],
                        "status": result["status"],
                        "source_experiments_rerun": False,
                    }
                ),
                flush=True,
            )
    print(json.dumps(eq.write_effective_summary(root, validated["schedule"], "recovery")), flush=True)


if __name__ == "__main__":
    main()
