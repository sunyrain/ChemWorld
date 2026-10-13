"""Three fresh repetitions of the six fixed notebook cases (W2-247)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from scripts.run_paper_case_notebooks import CASES, ROOT, emit, live, prepare, summarize, write

REPEATS = ("repeat-01", "repeat-02", "repeat-03")


def snapshot(root: Path, active_repeat: str | None = None, active_case: str | None = None):
    rows = []
    active = {}
    for repeat in REPEATS:
        summary = summarize(root / repeat)
        rows.extend({"repeat": repeat, **case} for case in summary["cases"])
        if repeat == active_repeat and active_case:
            case = next(c for c in CASES if c["id"] == active_case)
            if not (root / repeat / "results" / f"{active_case}.json").exists():
                active = live(root / repeat, case)
    output = {
        "mode": "development-within-case-stability",
        "planned_sources": 18,
        "planned_source_batches": 252,
        "planned_posttests": 60,
        "terminal_sources": sum(r["status"] not in {"not_started", "running"} for r in rows),
        "completed_sources": sum(r["status"] == "completed" for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in rows),
        "sealed_posttests": sum(r["sealed_posttests"] for r in rows),
        "active": active,
        "cases": rows,
    }
    write(root / "summary.json", output)
    return output


def run(root: Path):
    root.mkdir(parents=True, exist_ok=False)
    for repeat in REPEATS:
        prepare(root / repeat)
    write(
        root / "design.json",
        {
            "experiment_note": (
                "workstreams/flagship_tasks/WORK_II_CASE_NOTEBOOK_STABILITY_20261013.md"
            ),
            "mode": "development-within-case-stability",
            "repeats": REPEATS,
            "cases": CASES,
            "planned_sources": 18,
            "planned_source_batches": 252,
            "planned_posttests": 60,
            "planned_reference_batches": 432,
            "maximum_recommendation_retests": 12,
            "source_retries": 0,
            "provider_sampling_seed_control": "unavailable; fresh independent sessions",
            "world_and_observation_mapping": "unchanged within each case",
        },
    )
    started = time.monotonic()
    for repeat in REPEATS:
        for unit in ["references", *(c["id"] for c in CASES)]:
            log = root / repeat / "logs" / f"{unit}.log"
            log.parent.mkdir(exist_ok=True)
            with log.open("w", encoding="utf-8") as stream:
                options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
                process = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "scripts.run_paper_case_notebooks",
                        "--root",
                        str(root / repeat),
                        "--unit",
                        unit,
                    ],
                    cwd=ROOT,
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    **options,
                )
                while process.poll() is None:
                    summary = snapshot(root, repeat, None if unit == "references" else unit)
                    completed = summary["completed_batches"] + summary["active"].get("batches", 0)
                    elapsed = time.monotonic() - started
                    emit(
                        {
                            "repeat": repeat,
                            "stage": unit,
                            "terminal_sources": summary["terminal_sources"],
                            "total_sources": 18,
                            "completed_batches": completed,
                            "total_batches": 252,
                            "sealed_posttests": summary["sealed_posttests"],
                            "total_posttests": 60,
                            "elapsed_s": round(elapsed),
                            "batches_per_minute": 60 * completed / elapsed,
                            "eta_s": elapsed / completed * (252 - completed) if completed else None,
                            "active": summary["active"],
                            "log_bytes": log.stat().st_size,
                        }
                    )
                    time.sleep(30)
            if process.returncode:
                write(
                    root / "block-stop.json",
                    {
                        "repeat": repeat,
                        "unit": unit,
                        "exit_code": process.returncode,
                        "reason": "execution or reference/replay defect; no retry",
                    },
                )
                snapshot(root)
                return process.returncode
    summary = snapshot(root)
    emit({k: v for k, v in summary.items() if k != "cases"})
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    if args.summarize:
        summary = snapshot(args.root.resolve())
        emit({k: v for k, v in summary.items() if k != "cases"})
        return 0
    return run(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
