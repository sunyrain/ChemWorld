"""Run the fixed Astra-medium condition in the common five-world EQ matrix."""

from __future__ import annotations

import argparse
import os
import subprocess
import time
from pathlib import Path

from run_work_ii_eq_six_model_comparison import ROOT, emit, folder, read, write
from run_work_ii_eq_three_model_matrix import ARMS, WORLDS

MODEL = "gpt-6-astra"
REFERENCE = ROOT / "runs/development/eq-three-model-matrix-20260927/shared-reference/truth.json"
REPORT = ROOT / "workstreams/flagship_tasks/reports/eq-astra-medium-20260927"


def jobs():
    return [
        {"model": MODEL, "world_id": w, "arm": a, "cell_id": f"{w}--{a}"}
        for w in WORLDS
        for a in ARMS
    ]


def live(root, job):
    import json

    target = folder(root, job)
    row = {**job, "operations": 0, "batches": 0, "sealed": []}
    trajectory = target / "trajectory.jsonl"
    if trajectory.exists():
        for line in trajectory.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except ValueError:
                continue
            row["operations"] += 1
            row["batches"] += (
                record.get("instrument") == "final_assay"
                and record.get("transaction_status") == "committed"
            )
    row["sealed"] = [p.stem for p in (target / "sealed").glob("*.json")]
    if (target / "RESULT.json").exists():
        row["status"] = read(target / "RESULT.json")["status"]
    return row


def execute(root):
    pending, active, ended = jobs(), [], []
    started, last_progress = time.monotonic(), 0
    (root / "logs").mkdir()
    while pending or active:
        running = []
        for job, process, stream in active:
            code = process.poll()
            if code is None:
                running.append((job, process, stream))
            else:
                stream.close()
                ended.append({**job, "returncode": code})
        active = running
        while pending and len(active) < 6:
            job = pending.pop(0)
            stream = (root / "logs" / f"{job['cell_id']}.log").open("w", encoding="utf-8")
            command = [
                "uv",
                "run",
                "--no-sync",
                "python",
                str(Path(__file__).resolve()),
                "--mode",
                "cell",
                "--output",
                str(root),
                "--cell-id",
                job["cell_id"],
            ]
            options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                stdout=stream,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
                **options,
            )
            active.append((job, process, stream))
        now = time.monotonic()
        if now - last_progress >= 30 or not active:
            rows = [live(root, j) for j in jobs()]
            elapsed = now - started
            batches = sum(r["batches"] for r in rows)
            payload = {
                "phase": "research" if active else "research_terminal",
                "elapsed_s": round(elapsed),
                "terminal_sessions": len(ended),
                "planned_sessions": 15,
                "completed_sessions": sum(r.get("status") == "completed" for r in rows),
                "batches": batches,
                "planned_batches": 180,
                "sealed_stages": sum(len(r["sealed"]) for r in rows),
                "planned_stages": 60,
                "operations": sum(r["operations"] for r in rows),
                "batches_per_min": round(60 * batches / elapsed, 2) if elapsed else 0,
                "sessions_per_hour": round(3600 * len(ended) / elapsed, 2) if elapsed else 0,
                "eta_s": round(elapsed * (15 - len(ended)) / len(ended)) if ended else None,
                "active": [{**j, "pid": p.pid} for j, p, _ in active],
                "pending": len(pending),
                "cells": rows,
            }
            write(root / "progress.json", payload)
            emit({k: v for k, v in payload.items() if k != "cells"})
            last_progress = now
        if active:
            time.sleep(5)
    write(root / "worker_exits.json", ended)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("check", "coordinate", "cell", "summarize"), default="coordinate"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell-id")
    args = parser.parse_args()
    root = args.output.resolve()
    if args.mode == "cell":
        from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import run_eq_cell

        result = run_eq_cell(
            root / "conditions" / MODEL,
            {"model": MODEL, "reasoning_effort": "medium"},
            args.cell_id,
        )
        emit({"cell_id": args.cell_id, "status": result["status"]})
        return
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    assert {j["cell_id"] for j in jobs()} == {c["cell_id"] for c in schedule}
    assert config == read(REFERENCE.parents[1] / "design.json")["resolved_config"]
    assert REFERENCE.is_file()
    if args.mode == "check":
        emit({"model": MODEL, "effort": "medium", "sessions": 15, "batches": 180, "stages": 60})
        return
    if args.mode == "coordinate":
        root.mkdir(parents=True, exist_ok=False)
        write(
            root / "design.json",
            {
                "resolved_config": config,
                "sessions": jobs(),
                "model": MODEL,
                "reasoning_effort": "medium",
                "workers": 6,
                "reference_source": str(REFERENCE),
                "scope": "development; common EQ matrix",
            },
        )
        execute(root)
    assert len(read(root / "worker_exits.json")) == 15, "Participants not all terminal"
    from analyze_work_ii_eq_astra_matrix import analyze

    analyze(root, config, read(REFERENCE))


if __name__ == "__main__":
    main()
