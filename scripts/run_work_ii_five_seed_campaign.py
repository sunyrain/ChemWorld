#!/usr/bin/env python3
"""Run the Work II electrochemical campaign for five world seeds with heartbeats."""

from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from time import perf_counter
from typing import Any, TextIO

from chemworld.eval.provenance import git_source_commit, git_worktree_dirty, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"
RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"


def _emit(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    print(rendered, flush=True)


def _drain(stream: TextIO, events: queue.Queue[str | None]) -> None:
    for line in stream:
        events.put(line.rstrip("\r\n"))
    events.put(None)


def _heartbeat(
    *,
    started: float,
    completed_cells: int,
    total_cells: int,
    last_event: dict[str, Any],
) -> dict[str, Any]:
    elapsed = perf_counter() - started
    rate = completed_cells / elapsed if elapsed > 0.0 else 0.0
    return {
        "event": "heartbeat",
        "elapsed_s": round(elapsed, 1),
        "completed_cells": completed_cells,
        "total_cells": total_cells,
        "throughput_cells_per_hour": round(rate * 3600.0, 3),
        "eta_s": (
            round((total_cells - completed_cells) / rate, 1)
            if rate > 0.0 and completed_cells < total_cells
            else 0.0
            if completed_cells == total_cells
            else None
        ),
        "current_world_seed": last_event.get("world_seed"),
        "current_arm": last_event.get("arm"),
        "current_stage": last_event.get("stage"),
        "current_step": last_event.get("step"),
        "current_complete_experiments": last_event.get("complete_experiments"),
        "liveness_counter": int(last_event.get("liveness_counter", 0)) + 1,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if git_worktree_dirty(ROOT):
        raise RuntimeError("five-seed provider execution requires a clean committed worktree")
    if not os.environ.get("WELLAU_API_KEY"):
        raise RuntimeError("WELLAU_API_KEY is not available")
    output = args.output.resolve()
    progress = args.progress_file.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite five-seed output: {output}")
    output.mkdir(parents=True)
    seeds = [int(seed) for seed in args.world_seed]
    if len(seeds) != 5 or len(set(seeds)) != 5:
        raise ValueError("five-seed execution requires exactly five distinct world seeds")
    total_cells = len(seeds) * 3
    completed_cells = 0
    started = perf_counter()
    seed_reports: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    last_event: dict[str, Any] = {"stage": "matrix_start", "liveness_counter": 0}
    _emit(
        progress,
        {
            "event": "matrix_started",
            "world_seeds": seeds,
            "completed_cells": 0,
            "total_cells": total_cells,
            "source_commit": git_source_commit(ROOT),
        },
    )
    for seed in seeds:
        seed_output = output / f"seed-{seed}"
        child_progress = progress.with_name(f"{progress.stem}-seed-{seed}.jsonl")
        command = [
            sys.executable,
            str(RUNNER),
            "--config",
            str(args.config.resolve()),
            "--output",
            str(seed_output),
            "--progress-file",
            str(child_progress),
            "--world-seed",
            str(seed),
        ]
        kwargs: dict[str, Any] = {}
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            **kwargs,
        )
        if process.stdout is None:
            process.kill()
            raise RuntimeError("five-seed child stdout was not created")
        events: queue.Queue[str | None] = queue.Queue()
        reader = threading.Thread(target=_drain, args=(process.stdout, events), daemon=True)
        reader.start()
        child_done = False
        while not child_done:
            try:
                line = events.get(timeout=float(args.heartbeat_interval_s))
            except queue.Empty:
                last_event = _heartbeat(
                    started=started,
                    completed_cells=completed_cells,
                    total_cells=total_cells,
                    last_event=last_event,
                )
                _emit(progress, last_event)
                continue
            if line is None:
                child_done = True
                continue
            try:
                child_event = json.loads(line)
            except json.JSONDecodeError:
                _emit(
                    progress,
                    {
                        "event": "child_log",
                        "world_seed": seed,
                        "message": line[:1000],
                    },
                )
                continue
            if not isinstance(child_event, dict):
                continue
            child_event["event"] = child_event.get("event", "child_progress")
            child_event["matrix_completed_cells_before_event"] = completed_cells
            if child_event.get("stage") == "cell_completed" and child_event.get("completed"):
                completed_cells += 1
            child_event["completed_cells"] = completed_cells
            child_event["total_cells"] = total_cells
            child_event["liveness_counter"] = int(last_event.get("liveness_counter", 0)) + 1
            last_event = child_event
            _emit(progress, child_event)
        return_code = process.wait()
        reader.join(timeout=5.0)
        report_path = seed_output / "report.json"
        seed_report = (
            json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else None
        )
        if isinstance(seed_report, dict):
            seed_reports.append(seed_report)
        if return_code != 0 or not isinstance(seed_report, dict):
            failures.append(
                {
                    "world_seed": seed,
                    "return_code": return_code,
                    "report_available": isinstance(seed_report, dict),
                }
            )
            break
    report = {
        "schema_version": "chemworld-work-ii-five-seed-campaign-report-0.1",
        "source_commit": git_source_commit(ROOT),
        "world_seeds": seeds,
        "expected_cell_count": total_cells,
        "completed_cell_count": completed_cells,
        "completed_seed_count": len(seed_reports),
        "elapsed_s": round(perf_counter() - started, 1),
        "all_cells_completed": completed_cells == total_cells and not failures,
        "failures": failures,
        "seed_reports": seed_reports,
    }
    write_json_atomic(output / "matrix_report.json", report)
    _emit(
        progress,
        {
            "event": "matrix_completed" if report["all_cells_completed"] else "matrix_failed",
            "completed_cells": completed_cells,
            "total_cells": total_cells,
            "elapsed_s": report["elapsed_s"],
            "output": str(output),
            "failures": failures,
        },
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument(
        "--world-seed",
        type=int,
        nargs=5,
        default=[0, 1, 2, 3, 4],
    )
    parser.add_argument("--heartbeat-interval-s", type=float, default=30.0)
    args = parser.parse_args()
    report = run(args)
    return 0 if report["all_cells_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
