"""Complete the 45-cell EQ matrix, preserving the six completed pilot cells."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from run_work_ii_eq_six_model_comparison import DILUTE, MODELS, ROOT, emit, folder, read, write

ARMS = ("Opaque", "Aligned", "MisIndexed")
WORLDS = tuple(f"EQ-W{i:02d}" for i in range(1, 6))
PILOT = ROOT / "runs/development/eq-six-model-comparison-20260927"
REPORT = ROOT / "workstreams/flagship_tasks/reports/eq-three-model-matrix-20260927"


def jobs():
    return [
        {"world_id": w, "arm": a, "model": m, "cell_id": f"{w}--{a}"}
        for w in WORLDS
        for a in ARMS
        for m in MODELS
    ]


def reused(job):
    return job["world_id"] == "EQ-W01" and job["arm"] != "MisIndexed"


def source(root, job):
    if root is not None:
        recovery = root / "infrastructure-recovery.json"
        if recovery.exists():
            plan = read(recovery)
            if job["model"] == plan["model"] and job["cell_id"] == plan["cell_id"]:
                target = folder(root / "infrastructure-recovery", job)
                if (target / "RESULT.json").exists():
                    return target
    return folder(PILOT if reused(job) else root, job)


def validate(config):
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    schedule = eq.validate_design(config)["schedule"]
    assert read(PILOT / "design.json")["resolved_config"] == config
    assert len(jobs()) == 45 and len([j for j in jobs() if not reused(j)]) == 39
    assert set(WORLDS) == {w["world_id"] for w in config["worlds"]}
    assert list(ARMS) == config["arms"]
    for job in jobs():
        assert any(s["cell_id"] == job["cell_id"] for s in schedule)
        if reused(job):
            result = read(source(None, job) / "RESULT.json")
            provenance = result["source_usage"]["model_provenance"]
            assert result["status"] == "completed" and len(result["batches"]) == 12
            assert provenance["model_id"] == job["model"]
            assert provenance["request_parameters"]["reasoning_effort"] == "medium"
            assert result["exact_replay"]["verified"]
            assert all(result["posttest_validation"][s]["valid"] for s in eq.POSTTEST_STAGES)


def cell(root, model, cell_id):
    from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import run_eq_cell

    result = run_eq_cell(
        root / "conditions" / model,
        {"model": model, "reasoning_effort": "medium"},
        cell_id,
    )
    emit({"model": model, "cell_id": cell_id, "status": result["status"]})
    recovery = root / "infrastructure-recovery.json"
    if recovery.exists():
        plan = read(recovery)
        if model == plan["trigger_model"] and cell_id == plan["trigger_cell_id"]:
            original = read(folder(root, plan) / "RESULT.json")
            assert original["operations"] == 0 and not original["batches"]
            recovered_root = root / "infrastructure-recovery"
            log = root / "logs" / "infrastructure-recovery.log"
            command = [
                "uv",
                "run",
                "--no-sync",
                "python",
                str(Path(__file__).resolve()),
                "--mode",
                "cell",
                "--output",
                str(recovered_root),
                "--model",
                plan["model"],
                "--cell-id",
                plan["cell_id"],
            ]
            options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
            with log.open("w", encoding="utf-8") as stream:
                process = subprocess.Popen(
                    command,
                    cwd=ROOT,
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    env=os.environ.copy(),
                    **options,
                )
                while process.poll() is None:
                    emit({"phase": "zero_action_transport_recovery", "cell_id": plan["cell_id"]})
                    time.sleep(30)
            write(root / "infrastructure-recovery-exit.json", {"returncode": process.returncode})


def live_cell(root, job):
    target = source(root, job)
    row = {**job, "reused_pilot": reused(job), "operations": 0, "batches": 0, "sealed": []}
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
    pending = [j for j in jobs() if not reused(j)]
    active, ended = [], []
    started, last_progress = time.monotonic(), 0
    (root / "logs").mkdir()
    while pending or active:
        still_active = []
        for job, process, stream in active:
            code = process.poll()
            if code is None:
                still_active.append((job, process, stream))
            else:
                stream.close()
                ended.append({**job, "returncode": code})
        active = still_active
        while pending and len(active) < 6:
            job = pending.pop(0)
            stream = (root / "logs" / f"{job['model']}--{job['cell_id']}.log").open("w")
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
                "--model",
                job["model"],
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
            rows = [live_cell(root, j) for j in jobs()]
            elapsed = now - started
            payload = {
                "phase": "research" if active else "research_terminal",
                "elapsed_s": round(elapsed),
                "terminal_new_sessions": len(ended),
                "planned_new_sessions": 39,
                "reused_sessions": 6,
                "terminal_total_sessions": 6 + len(ended),
                "planned_total_sessions": 45,
                "batches": sum(r["batches"] for r in rows),
                "planned_batches": 540,
                "sealed_stages": sum(len(r["sealed"]) for r in rows),
                "planned_stages": 180,
                "operations": sum(r["operations"] for r in rows),
                "sessions_per_hour": round(3600 * len(ended) / elapsed, 2) if elapsed else 0,
                "eta_s": round(elapsed * (39 - len(ended)) / len(ended)) if ended else None,
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


def reference_truth(root, config):
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    target = root / "shared-reference/truth.json"
    if target.exists():
        return read(target)
    queries = eq.queries(config)
    actions = [a for q in queries for a in q["actions"]]
    truth = {"EQ-W01": read(PILOT / "shared-reference/truth.json")}
    for world_id in WORLDS[1:]:
        truth[world_id] = {q["query_id"]: [] for q in queries}
        for repeat in range(1, 6):
            result = eq.reference_run(
                root / "shared-reference" / world_id / f"repeat-{repeat:02d}",
                actions,
                config=config,
                world=eq.world_by_id(config, world_id),
                batches=12,
                observation_seed=eq.deterministic_seed("eq-reference-truth-v1", world_id, repeat),
                observation_namespace=f"work-ii-eq-truth-{world_id.lower()}-r{repeat:02d}",
            )
            assert not result["failure"] and not result["rollbacks"]
            assert len(result["batches"]) == 12 and result["exact_replay"]["verified"]
            for q, batch in zip(queries, result["batches"], strict=True):
                truth[world_id][q["query_id"]].append(
                    {metric: float(batch["metrics"][metric]) for metric in eq.METRICS}
                )
            emit({"phase": "reference", "world": world_id, "repeat": repeat, "of": 5})
    write(target, truth)
    return truth


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("coordinate", "cell", "check", "summarize"), default="coordinate"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--cell-id")
    args = parser.parse_args()
    root = args.output.resolve()
    if args.mode == "cell":
        cell(root, args.model, args.cell_id)
        return
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    config = eq.load_config()
    validate(config)
    if args.mode == "check":
        emit({"planned": 45, "reuse": 6, "new": 39, "workers": 6, "batches": 540})
        return
    if args.mode == "coordinate":
        root.mkdir(parents=True, exist_ok=False)
        write(
            root / "design.json",
            {
                "resolved_config": config,
                "sessions": jobs(),
                "reasoning_effort": "medium",
                "workers": 6,
                "pilot_root": str(PILOT),
                "dilute_queries": DILUTE,
                "evidence_scope": "development extension after inspecting six pilot sessions",
            },
        )
        execute(root)
    else:
        assert len(read(root / "worker_exits.json")) == 39, "Participants are not terminal"
    truth = reference_truth(root, config)
    from analyze_work_ii_eq_three_model_matrix import analyze

    analyze(root, config, truth)


if __name__ == "__main__":
    main()
