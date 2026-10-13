"""Fixed 48-session EQ/C notebook study, with isolated four-slot execution (W2-249)."""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from scripts.run_paper_case_notebooks import (
    ROOT,
    case_folder,
    emit,
    execute_case,
    live,
    read,
    write,
)

NOTE = "workstreams/flagship_tasks/WORK_II_RESEARCH_FORMATION_20261013.md"
REPEATS = ("repeat-01", "repeat-02", "repeat-03")
ARMS = ("Opaque", "Aligned")
C_WORLDS = (1, 3, 5)
MODE = "prospective-research-formation-current-core"


def cases():
    """Interleave systems; keep both information arms adjacent within each world."""
    rows = []
    for world in range(1, 6):
        for system in ("EQ", "C") if world in C_WORLDS else ("EQ",):
            for arm in ARMS:
                rows.append(
                    {
                        "id": f"{system}-W{world:02d}-{arm}",
                        "system": system,
                        "world": f"W{world:02d}",
                        "arm": arm,
                        "cell": (
                            f"EQ-W{world:02d}--{arm}"
                            if system == "EQ"
                            else f"C-W{world:02d}-B12-E-{arm}"
                        ),
                        "model": "gpt-5.6-sol",
                        "batches": 12,
                    }
                )
    return rows


def schedule():
    # Rotate by an even number of cells and reverse arm order in round two.
    # This is fixed before execution, not adapted to outcomes or completion speed.
    base = cases()
    rows = []
    for index, repeat in enumerate(REPEATS):
        offset = index * 6
        ordered = base[offset:] + base[:offset]
        if index % 2:
            ordered = [c for i in range(0, len(ordered), 2) for c in ordered[i : i + 2][::-1]]
        rows.extend({"repeat": repeat, **case} for case in ordered)
    return rows


def prepare(root):
    from scripts import run_work_ii_c_formal as c
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq
    from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import provider

    original = ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto/design.json"
    c_design = read(original)
    if c_design["protocol"] != "c-quality-recovery-formal-v3-en":
        raise ValueError("Unexpected C protocol")
    expected_provider = provider({"model": "gpt-5.6-sol", "reasoning_effort": "medium"})
    if expected_provider != c.pilot.ec.PROVIDER or c_design["model"] != expected_provider:
        raise ValueError("C model/effort differs from the fixed study")
    config = eq.load_config()
    valid = eq.validate_design(config)
    if not {r["cell"] for r in cases() if r["system"] == "EQ"} <= {
        r["cell_id"] for r in valid["schedule"]
    }:
        raise ValueError("Missing EQ cells")
    wanted = {r["cell"] for r in cases() if r["system"] == "C"}
    c_design["schedule"] = [r for r in c_design["schedule"] if r["id"] in wanted]
    if len(c_design["schedule"]) != 6:
        raise ValueError("Missing C cells")
    c_design.update(
        planned_sources=6,
        planned_batches=72,
        planned_posttests=18,
        planned_retests=6,
        mode=MODE,
        automatic_retries=0,
        experiment_note=NOTE,
    )
    root.mkdir(parents=True, exist_ok=False)
    design = {
        "mode": MODE,
        "experiment_note": NOTE,
        "schedule": schedule(),
        "cases": cases(),
        "repeats": REPEATS,
        "concurrency": 4,
        "planned_sources": 48,
        "planned_source_batches": 576,
        "planned_posttests": 174,
        "planned_reference_batches": 336,
        "planned_reference_trajectories": 28,
        "maximum_recommendation_retests": 18,
        "source_retries": 0,
        "provider_sampling_seed_control": "unavailable; fresh sessions",
        "provider": expected_provider,
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "runtime_surface": c.runtime_surface(),
        "C_original": {
            "path": str(original),
            "sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
        },
        "eq_config": config,
        "reference_policy": "shared current-core host-only references, before sources",
        "inherited_protocol_overrides": [
            "48-session O/A matrix and fixed schedule in this experiment note",
            "shared references generated before participants, never supplied to them",
            "no success-dependent canary, recovery, or replacement",
            "source-stage notebook role applied equally in both information arms",
        ],
    }
    write(root / "design.json", design)
    for repeat in REPEATS:
        write(
            root / repeat / "design.json",
            {
                "source_commit": design["source_commit"],
                "eq_config": config,
                "mode": MODE,
                "cases": cases(),
                "experiment_note": NOTE,
            },
        )
        write(root / repeat / "C/design.json", copy.deepcopy(c_design))


def references(root, progress):
    from scripts import run_work_ii_c_formal as c
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

    config = read(root / "design.json")["eq_config"]
    queries = eq.queries(config)
    actions = [a for q in queries for a in q["actions"]]
    truth, completed, operations, trajectories = {}, 0, 0, 0
    for world in config["worlds"]:
        world_id = world["world_id"]
        truth[world_id] = {q["query_id"]: [] for q in queries}
        for repeat in range(1, 6):
            progress.update(stage="references", unit=f"{world_id}/{repeat}")
            result = eq.reference_run(
                root / "references" / world_id / f"repeat-{repeat}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=eq.deterministic_seed("eq-reference-truth-v1", world_id, repeat),
                observation_namespace=f"work-ii-eq-truth-{world_id.lower()}-r{repeat:02d}",
            )
            if (
                result["failure"]
                or result["rollbacks"]
                or len(result["batches"]) != 12
                or not result["exact_replay"]["verified"]
            ):
                raise RuntimeError(f"EQ reference defect: {world_id}/{repeat}")
            for query, batch in zip(queries, result["batches"], strict=True):
                truth[world_id][query["query_id"]].append(
                    {m: batch["metrics"][m] for m in eq.METRICS}
                )
            completed += 12
            operations += result["operation_attempts"]
            trajectories += 1
            progress.update(reference_batches=completed, reference_operations=operations)
            write(root / "references/progress.json", progress)
            emit(progress)
    c_design = read(root / REPEATS[0] / "C/design.json")
    for world in C_WORLDS:
        progress.update(stage="references", unit=f"C-W{world:02d}")
        result = c.fixed(
            root / "references" / f"C-W{world:02d}",
            [a for q in c_design["queries"] for a in q["actions"]],
            world_seed=world - 1,
            batches=12,
        )
        if not result["passed"] or len(result["batches"]) != 12:
            raise RuntimeError(f"C reference defect: W{world:02d}")
        for repeat in REPEATS:
            write(root / repeat / "C/qualification" / f"W{world:02d}/queries/result.json", result)
        completed += 12
        operations += result["operations"]
        trajectories += 1
        progress.update(reference_batches=completed, reference_operations=operations)
        write(root / "references/progress.json", progress)
        emit(progress)
    write(root / "references/truth.json", {"EQ": truth})
    for repeat in REPEATS:
        write(root / repeat / "references/truth.json", {"EQ": truth})
    write(
        root / "references/complete.json",
        {
            "completed_batches": completed,
            "operations": operations,
            "trajectories": trajectories,
            "replay_verified": True,
            "shared_by_all_source_repetitions": True,
        },
    )


def validate_result(result):
    source = result.get("source", result)
    if source.get("operations", 0) and not (source.get("exact_replay") or {}).get("verified"):
        raise RuntimeError("source replay defect")
    retest = result.get("recommendation_retest") or {}
    if retest and not (retest.get("exact_replay") or {}).get("verified"):
        raise RuntimeError("recommendation replay defect")


def result_path(root, unit):
    return root / unit["repeat"] / "results" / f"{unit['id']}.json"


def snapshot(root, active=(), *, started=None):
    units = read(root / "design.json")["schedule"]
    rows = []
    for unit in units:
        path = result_path(root, unit)
        result = read(path) if path.exists() else {}
        source = result.get("source", result)
        key = (unit["repeat"], unit["id"])
        counts = live(root / unit["repeat"], unit) if key in active and not result else {}
        stages = ("K1", "Q", "K2", "EQS") if unit["system"] == "EQ" else ("K1", "Q", "K2")
        posttests = result.get("posttests", {})
        sealed = [
            stage
            for stage in stages
            if posttests.get(stage, {}).get("payload")
            and not posttests[stage].get("failure")
            and result.get("posttest_validation", {}).get(stage, {}).get("valid", True)
        ]
        rows.append(
            {
                **unit,
                "status": result.get("status", "running" if key in active else "not_started"),
                "completed_batches": len(source.get("batches", [])) + counts.get("batches", 0),
                "operations": source.get("operations", 0) + counts.get("operations", 0),
                "failure": result.get("failure"),
                "sealed_posttests": len(sealed),
                "missing_posttests": [s for s in stages if s not in sealed],
                "posttest_failures": {
                    s: t.get("failure") for s, t in posttests.items() if t.get("failure")
                },
                "posttest_validation": result.get("posttest_validation"),
                "exact_replay": source.get("exact_replay"),
                "rollbacks": source.get("rollbacks", []),
                "source_usage": result.get("source_usage", source.get("usage")),
                "posttest_usage": {
                    s: t.get("usage", t.get("method_resources")) for s, t in posttests.items()
                },
                "prediction_evaluation": result.get("prediction_evaluation"),
                "elapsed_s": result.get("elapsed_s"),
            }
        )
    output = {
        "mode": MODE,
        "planned_sources": 48,
        "planned_source_batches": 576,
        "planned_posttests": 174,
        "planned_reference_batches": 336,
        "terminal_sources": sum(r["status"] not in {"not_started", "running"} for r in rows),
        "completed_sources": sum(r["status"] == "completed" for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in rows),
        "sealed_posttests": sum(r["sealed_posttests"] for r in rows),
        "active_units": [
            {k: r[k] for k in ("repeat", "id", "operations", "completed_batches")}
            for r in rows
            if (r["repeat"], r["id"]) in active
        ],
        "reference": read(root / "references/complete.json")
        if (root / "references/complete.json").exists()
        else None,
        "block_stop": read(root / "block-stop.json")
        if (root / "block-stop.json").exists()
        else None,
        "cases": rows,
    }
    if started is not None:
        elapsed = max(time.monotonic() - started, 1e-6)
        completed = output["completed_batches"]
        output.update(
            elapsed_s=round(elapsed),
            batches_per_minute=60 * completed / elapsed,
            batch_eta_s=elapsed / completed * (576 - completed) if completed else None,
        )
    write(root / "summary.json", output)
    return output


def launch(root, unit):
    key = "references" if unit is None else f"{unit['repeat']}/{unit['id']}"
    log = root / "logs" / f"{key}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    stream = log.open("x", encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "scripts.run_research_formation",
        "--root",
        str(root),
        "--unit",
        "references" if unit is None else unit["id"],
    ]
    if unit is not None:
        command += ["--repeat", unit["repeat"]]
    try:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=stream,
            stderr=subprocess.STDOUT,
            **({"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}),
        )
    except Exception:
        stream.close()
        raise
    emit({"launched": key, "pid": process.pid})
    write(
        root / "launches" / f"{key}.json", {"pid": process.pid, "epoch": time.time(), "attempt": 1}
    )
    return {"process": process, "stream": stream, "unit": unit}


def coordinate(root):
    prepare(root)
    started = time.monotonic()
    ref = launch(root, None)
    while ref["process"].poll() is None:
        progress_path = root / "references/progress.json"
        emit(
            {
                "stage": "references",
                "total_batches": 336,
                "elapsed_s": round(time.monotonic() - started),
                "log_bytes": (root / "logs/references.log").stat().st_size,
                "progress": read(progress_path) if progress_path.exists() else {},
            }
        )
        time.sleep(30)
    ref["stream"].close()
    if ref["process"].returncode or not (root / "references/complete.json").exists():
        write(
            root / "block-stop.json", {"stage": "references", "reason": "reference process defect"}
        )
        snapshot(root)
        return 1
    return run_pool(root)


def run_pool(root):
    pending = list(read(root / "design.json")["schedule"])
    active, failed = {}, False
    started = time.monotonic()
    while pending or active:
        for key, record in list(active.items()):
            code = record["process"].poll()
            if code is None:
                continue
            record["stream"].close()
            del active[key]
            try:
                if code:
                    raise RuntimeError(f"execution process exited {code}")
                validate_result(read(result_path(root, record["unit"])))
            except (RuntimeError, OSError, ValueError) as exc:
                failed = True
                write(
                    root / "block-stop.json",
                    {
                        "unit": key,
                        "reason": str(exc),
                        "drain_in_flight": True,
                        "source_retry": False,
                    },
                )
        if not failed:
            while pending and len(active) < 4:
                unit = pending.pop(0)
                key = (unit["repeat"], unit["id"])
                try:
                    active[key] = launch(root, unit)
                except (OSError, ValueError) as exc:
                    failed = True
                    write(
                        root / "block-stop.json",
                        {
                            "unit": key,
                            "reason": str(exc),
                            "drain_in_flight": True,
                            "source_retry": False,
                        },
                    )
                    break
        summary = snapshot(root, active, started=started)
        emit({k: v for k, v in summary.items() if k != "cases"})
        if failed and not active:
            break
        if pending or active:
            time.sleep(30)
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--unit", choices=["references", *(c["id"] for c in cases())])
    parser.add_argument("--repeat", choices=REPEATS)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.summarize:
        summary = snapshot(root)
        emit({k: v for k, v in summary.items() if k != "cases"})
        return 0
    if not args.unit:
        return coordinate(root)
    progress = {"stage": args.unit, "reference_batches": 0}
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        if args.unit == "references":
            references(root, progress)
        else:
            if not args.repeat:
                parser.error("--repeat is required for a source")
            unit = next(
                c
                for c in read(root / "design.json")["schedule"]
                if c["id"] == args.unit and c["repeat"] == args.repeat
            )
            folder = case_folder(root / args.repeat, unit)
            if folder.exists() or result_path(root, unit).exists():
                raise RuntimeError("Source already started; no retry or overwrite")
            result = execute_case(root / args.repeat, unit, progress)
            write(result_path(root, unit), result)
            validate_result(result)
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
