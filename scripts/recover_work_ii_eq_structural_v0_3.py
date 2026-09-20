#!/usr/bin/env python3
"""Resume failed EQ-S v0.3 posttests without repeating source experiments."""
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

import scripts.run_work_ii_eq_structural_v0_3 as eq
from scripts.run_work_ii_study_b import _prepare_codex_home


def _original_source(root: Path, cell_id: str) -> Path:
    return root / "sources" / cell_id


def _source_thread_id(source: Path) -> str:
    receipts = eq.read(source / "private-provider" / "source-receipts.json")
    thread_id = receipts[-1].get("thread_id") if receipts else None
    if not thread_id:
        raise RuntimeError("completed EQ-S v0.3 source has no resumable provider thread")
    return str(thread_id)


def _latest_result(root: Path, cell_id: str) -> tuple[dict[str, Any], Path]:
    original = _original_source(root, cell_id) / "RESULT.json"
    candidates = [original]
    recovery_root = root / "recoveries" / cell_id
    if recovery_root.is_dir():
        candidates.extend(sorted(recovery_root.glob("attempt-*/RESULT.json")))
    existing = [path for path in candidates if path.is_file()]
    if not existing:
        raise RuntimeError(f"missing retained EQ-S v0.3 result: {cell_id}")
    path = existing[-1]
    return eq.read(path), path


def recover_one(
    root: Path,
    config: Mapping[str, Any],
    cell: Mapping[str, Any],
    *,
    attempt: int,
) -> dict[str, Any]:
    source = _original_source(root, str(cell["cell_id"]))
    original = eq.read(source / "RESULT.json")
    if (
        original.get("source_status") != "completed"
        or original.get("exact_replay", {}).get("verified") is not True
        or len(original.get("batches", [])) != 12
    ):
        raise RuntimeError(f"posttest recovery refuses an incomplete source: {cell['cell_id']}")

    base, base_path = _latest_result(root, str(cell["cell_id"]))
    output = root / "recoveries" / str(cell["cell_id"]) / f"attempt-{attempt:02d}"
    if output.exists():
        raise RuntimeError(f"write-once EQ-S v0.3 recovery exists: {output}")
    private = output / "private-provider"
    home = private / "home"
    (output / "sealed").mkdir(parents=True)
    home.mkdir(parents=True)
    environment = _prepare_codex_home(home, eq.PROVIDER)

    session_store = base_path.parent / "private-provider" / "home" / "codex-home" / "sessions"
    if not session_store.is_dir():
        raise RuntimeError(f"latest session store is missing: {cell['cell_id']}")
    shutil.copytree(session_store, home / "codex-home" / "sessions")
    shutil.copyfile(
        source / "private-provider" / "source-receipts.json",
        private / "source-receipts.json",
    )
    eq.write(
        output / "attempt.json",
        {
            "schema_version": "work-ii-eq-s-recovery-attempt-0.3",
            "cell_id": cell["cell_id"],
            "attempt": attempt,
            "kind": "posttests",
            "base_result": str(base_path.relative_to(root)),
            "source_experiments_rerun": False,
            "original_preserved": True,
            "truth_revealed_to_agent": False,
            "scientific_contract_changed": False,
            "reason": "Retained provider or posttest-format failure; resume the same thread from the latest legal boundary.",
            "started_epoch": time.time(),
        },
    )

    agent = SimpleNamespace(home_root=home, followup_environment=environment)
    result = copy.deepcopy(base)
    result["status"] = "recovering"
    result["failure"] = None
    query_rows = eq.queries(config)
    thread_id = _source_thread_id(source)
    started = time.monotonic()
    resumed_stages: list[str] = []
    for stage in eq.POSTTEST_STAGES:
        previous = result.get("posttests", {}).get(stage, {})
        validation = eq.validate_posttest(stage, previous.get("payload"), query_rows)
        if validation["valid"]:
            result.setdefault("posttest_validation", {})[stage] = validation
            continue
        resumed_stages.append(stage)
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
    history = list(result.get("recoveries", []))
    history.append(
        {
            "attempt": attempt,
            "kind": "posttests",
            "base_result": str(base_path.relative_to(root)),
            "resumed_stages": resumed_stages,
            "source_experiments_rerun": False,
            "thread_reused": True,
            "truth_revealed_to_agent": False,
            "question_changed": False,
            "model_changed": False,
        }
    )
    result["recoveries"] = history
    result["recovery_elapsed_s"] = time.monotonic() - started
    eq.write(output / "RESULT.json", result)
    eq.write(
        output / "recovery.json",
        {
            "schema_version": "work-ii-eq-s-recovery-record-0.3",
            "cell_id": cell["cell_id"],
            "attempt": attempt,
            "status": result["status"],
            "result_path": str((output / "RESULT.json").relative_to(root)),
            "base_result_path": str(base_path.relative_to(root)),
            "original_result_path": str((source / "RESULT.json").relative_to(root)),
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
    eq.configure_runtime(config)
    eq.eq_v2.validate_freeze(root, config)
    selected_ids = set(args.cell)
    selected = []
    for cell in validated["schedule"]:
        try:
            latest, _ = _latest_result(root, str(cell["cell_id"]))
        except RuntimeError:
            continue
        if (not selected_ids or cell["cell_id"] in selected_ids) and latest.get("status") != "completed":
            selected.append(cell)
    print(
        json.dumps(
            {"stage": "eq_s_v03_recovery_plan", "cells": [cell["cell_id"] for cell in selected]},
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
                        "stage": "eq_s_v03_recovery_complete",
                        "cell_id": cell["cell_id"],
                        "status": result["status"],
                        "source_experiments_rerun": False,
                    }
                ),
                flush=True,
            )
    summary = eq.write_summary(root, validated["schedule"], "recovery")
    print(json.dumps(summary), flush=True)
    if summary["completed_sources"] == 15:
        eq.finalize_after_sources(root, config, validated["schedule"])


if __name__ == "__main__":
    main()
