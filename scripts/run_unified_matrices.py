"""Execute the authorized 300-session addition with one isolated global queue."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import threading
import time
import traceback
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from scripts.unified_matrix_runtime import WORKER_ENV, apply_environment

apply_environment()

ROOT = Path(__file__).resolve().parents[1]
NOTE = "workstreams/flagship_tasks/WORK_II_UNIFIED_MATRICES_20261016.md"
REPEATS = ("repeat-01", "repeat-02", "repeat-03")
TERMINAL = {"completed", "incomplete", "failed", "execution_error"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def now():
    return datetime.now(UTC).isoformat()


def emit(value):
    print(json.dumps(value, ensure_ascii=True), flush=True)


def schedule(research_cases=None, opportunity_cases=None):
    if research_cases is None:
        from scripts.unified_matrix_research import build_cases

        research_cases = build_cases()
    if opportunity_cases is None:
        from scripts.unified_matrix_c_opportunity import build_cases

        opportunity_cases = build_cases()
    units = []
    for index, repeat in enumerate(REPEATS):
        worlds = [f"W{w:02d}" for w in range(1, 6)]
        worlds = worlds[index * 2 :] + worlds[: index * 2]
        arm_order = (
            ("Opaque", "Aligned", "MisIndexed"),
            ("MisIndexed", "Opaque", "Aligned"),
            ("Aligned", "MisIndexed", "Opaque"),
        )[index]
        goals = ("discovery", "optimization") if index % 2 == 0 else ("optimization", "discovery")
        for world_index, world in enumerate(worlds):
            # Each world starts with varied systems rather than a long same-system batch.
            systems = ["EC", "RX", "PA", "P", "C"]
            rotation = (world_index + index) % len(systems)
            systems = systems[rotation:] + systems[:rotation]
            groups = {}
            for system in systems:
                if system == "C":
                    group = [
                        dict(c)
                        for c in opportunity_cases
                        if c["repeat"] == repeat and c["world"].endswith(world)
                    ]
                else:
                    group = [
                        {**c, "repeat": repeat}
                        for c in research_cases
                        if c["system"] == system and c["world"].endswith(world)
                    ]
                    group.sort(
                        key=lambda c: (
                            arm_order.index(c["arm"]),
                            goals.index(c["goal"]) if c.get("goal") in goals else 0,
                        )
                    )
                groups[system] = group
            while any(groups.values()):
                for system in systems:
                    if groups[system]:
                        unit = groups[system].pop(0)
                        unit["matrix"] = (
                            "A" if system in {"EC", "RX"} else "C" if system == "C" else "B"
                        )
                        units.append(unit)
    counts = Counter(u["system"] for u in units)
    if counts != {"EC": 90, "RX": 90, "PA": 45, "P": 45, "C": 30}:
        raise ValueError(f"Incorrect fixed coverage: {counts}")
    if len({(u["repeat"], u["id"]) for u in units}) != 300:
        raise ValueError("Duplicate session identities")
    if sum(u["batches"] for u in units) != 3420:
        raise ValueError("Incorrect source-assay denominator")
    return units


def folder(root, unit):
    return root / unit["repeat"] / unit["id"]


def prepare(root, workers):
    from scripts import unified_matrix_c_opportunity as opportunity
    from scripts import unified_matrix_research as research

    if root.exists():
        raise FileExistsError(f"New study root required: {root}")
    root.mkdir(parents=True)
    progress = {"stage": "preparing fixed inputs and references", "updated_at": now()}
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            progress["updated_at"] = now()
            write(root / "preparation-progress.json", progress)
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        units = schedule()
        design = {
            "experiment_note": NOTE,
            "schedule": units,
            "workers": workers,
            "planned_sessions": 300,
            "planned_research_sessions": 285,
            "planned_source_batches": 3420,
            "planned_posttests": 900,
            "retained_sessions": 150,
            "combined_design_sessions": 450,
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "created_at": now(),
            "model": "gpt-5.6-sol",
            "reasoning_effort": "medium",
            "worker_environment": WORKER_ENV,
            "source_retries": 0,
        }
        write(root / "design.json", design)
        progress["stage"] = "preparing EC/RX/PA/P inputs and evaluator references"
        research.prepare_inputs(root, progress=progress)
        progress["stage"] = "preparing C matched public inputs and evaluator references"
        opportunity.prepare_inputs(root, progress=progress)
        write(root / "prepared.json", {"at": now(), "planned_sessions": len(units)})
        snapshot(root)
    finally:
        stop.set()


def live_counts(path):
    """Count executed source actions only; never include reference/retest trajectories."""
    operations = batches = 0
    for trajectory in path.rglob("trajectory.jsonl"):
        relative = trajectory.relative_to(path).as_posix().lower()
        if any(word in relative for word in ("reference", "retest", "capture", "qualification")):
            continue
        try:
            for line in trajectory.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                operations += 1
                batches += int(
                    row.get("instrument") == "final_assay"
                    and row.get("transaction_status") == "committed"
                )
        except OSError:
            continue
    return operations, batches


def status_row(root, unit, active_keys=()):
    path = folder(root, unit)
    state_path = path / "status.json"
    state = read(state_path) if state_path.exists() else {}
    result_path = path / "result.json"
    result = read(result_path) if result_path.exists() else {}
    source = result.get("source", result)
    stages = result.get("posttests", {})
    sealed = [
        s
        for s in ("K1", "Q", "K2")
        if stages.get(s, {}).get("payload")
        and not stages[s].get("failure")
        and result.get("posttest_validation", {}).get(s, {}).get("valid", True)
    ]
    key = (unit["repeat"], unit["id"])
    status = state.get("status", "not_started")
    if key in active_keys and status not in TERMINAL:
        status = "running"
    operations, batches = (
        live_counts(path)
        if status == "running"
        or (status in TERMINAL and not source.get("batches") and unit["batches"])
        else (0, 0)
    )
    source_batches = source.get("batches", [])
    completed_batches = (
        len(source_batches) if isinstance(source_batches, list) else int(source_batches or 0)
    )
    return {
        **unit,
        "status": status,
        "completed_batches": max(completed_batches, batches),
        "operations": max(
            int(source.get("operations", source.get("operation_attempts", 0)) or 0), operations
        ),
        "sealed_posttests": len(sealed),
        "missing_posttests": [s for s in ("K1", "Q", "K2") if s not in sealed],
        "failure": state.get("failure") or result.get("failure"),
        "elapsed_s": state.get("elapsed_s", result.get("elapsed_s")),
        "prediction_evaluation": result.get("prediction_evaluation"),
        "source_replay": source.get("exact_replay"),
        "posttest_validation": result.get("posttest_validation", {}),
        "source_usage": result.get("source_usage", source.get("usage")),
        "posttest_usage": {s: t.get("usage", t.get("method_resources")) for s, t in stages.items()},
        "posttest_failures": {s: t.get("failure") for s, t in stages.items() if t.get("failure")},
        "result_path": str(result_path),
    }


def eta_estimate(rows, workers):
    completed = [
        r
        for r in rows
        if r["status"] in TERMINAL and r.get("elapsed_s") and r["sealed_posttests"] == 3
    ]
    if not completed:
        return {"eta_s": None, "eta_basis": "awaiting completed scientific chains"}
    durations = defaultdict(list)
    for row in completed:
        durations[(row["system"], row.get("opportunity", "Research"))].append(row["elapsed_s"])
    fallback = statistics.median(r["elapsed_s"] for r in completed)
    estimates = []
    for row in rows:
        if row["status"] in TERMINAL:
            continue
        observed = durations[(row["system"], row.get("opportunity", "Research"))]
        estimates.append(statistics.median(observed) if observed else fallback)
    eta = max(sum(estimates) / max(workers, 1), max(estimates, default=0))
    return {
        "eta_s": round(eta),
        "eta_basis": "completed-chain durations by system; active sessions counted in full",
        "eta_completed_chains": len(completed),
        "median_session_s": round(fallback),
    }


def snapshot(root, active_keys=(), started=None, blocked=(), baseline=(0, 0)):
    design = read(root / "design.json")
    rows = [status_row(root, u, active_keys) for u in design["schedule"]]
    terminal = sum(r["status"] in TERMINAL for r in rows)
    summary = {
        "updated_at": now(),
        "planned_sessions": 300,
        "terminal_sessions": terminal,
        "complete_chains": sum(r["status"] == "completed" for r in rows),
        "valid_forecasts": sum(
            bool((r.get("prediction_evaluation") or {}).get("valid")) for r in rows
        ),
        "incomplete_or_failed": sum(r["status"] in TERMINAL - {"completed"} for r in rows),
        "active_sessions": sum(r["status"] == "running" for r in rows),
        "not_started": sum(r["status"] == "not_started" for r in rows),
        "completed_source_batches": sum(r["completed_batches"] for r in rows),
        "planned_source_batches": 3420,
        "sealed_posttests": sum(r["sealed_posttests"] for r in rows),
        "planned_posttests": 900,
        "operations": sum(r["operations"] for r in rows),
        "worker_cap": design["workers"],
        "blocked_systems": list(blocked),
        "retained_sessions_separate": 150,
        "stage": "terminal"
        if terminal == 300
        else "running"
        if active_keys
        else "prepared_or_inactive",
        **eta_estimate(rows, design["workers"]),
        "by_system": {},
        "cases": rows,
    }
    for system in ("EC", "RX", "PA", "P", "C"):
        selected = [r for r in rows if r["system"] == system]
        summary["by_system"][system] = {
            "planned": len(selected),
            "terminal": sum(r["status"] in TERMINAL for r in selected),
            "complete": sum(r["status"] == "completed" for r in selected),
            "active": sum(r["status"] == "running" for r in selected),
            "batches": sum(r["completed_batches"] for r in selected),
        }
    if started:
        elapsed = max(time.monotonic() - started, 1)
        summary.update(
            elapsed_s=round(elapsed),
            terminal_per_hour=round(3600 * (terminal - baseline[0]) / elapsed, 2),
            batches_per_minute=round(
                60 * (summary["completed_source_batches"] - baseline[1]) / elapsed, 2
            ),
        )
    if blocked:
        summary.update(eta_s=None, eta_basis="affected systems held; full-block ETA unavailable")
    write(root / "summary.json", summary)
    lines = [
        "# Unified six-system matrices: live execution",
        "",
        f"Updated: {summary['updated_at']}",
        "",
        f"Terminal {terminal}/300; complete {summary['complete_chains']}; "
        f"incomplete/failed {summary['incomplete_or_failed']}; "
        f"active {summary['active_sessions']}.",
        f"Source assays {summary['completed_source_batches']}/3420; "
        f"sealed assessments {summary['sealed_posttests']}/900.",
        f"ETA seconds: {summary['eta_s']}; {summary['eta_basis']}.",
        "",
        "Existing 150 sessions remain separate, including original missing outcomes.",
        "",
        "| System | Planned | Terminal | Complete | Active | Assays |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for system, counts in summary["by_system"].items():
        lines.append(
            f"| {system} | {counts['planned']} | {counts['terminal']} | {counts['complete']} "
            f"| {counts['active']} | {counts['batches']} |"
        )
    lines += ["", "## Incomplete and failed units", ""]
    for row in rows:
        if row["status"] in TERMINAL - {"completed"}:
            lines.append(
                f"- {row['repeat']}/{row['id']}: {row['status']}; {row['failure']}; "
                f"missing {row['missing_posttests']}"
            )
    lines += [
        "",
        "Completion counts are not scientific success rates. Full semantic reading remains "
        "separate from automated execution accounting.",
    ]
    (root / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def worker(root, unit):
    path = folder(root, unit)
    if path.exists():
        raise FileExistsError(f"Unit already started; no replacement: {path}")
    path.mkdir(parents=True)
    start = time.monotonic()
    progress = {"stage": "starting", "unit": unit["id"]}
    write(
        path / "status.json",
        {"status": "running", "pid": os.getpid(), "started_at": now(), "unit": unit},
    )
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            write(
                path / "live.json",
                {**progress, "updated_at": now(), "elapsed_s": round(time.monotonic() - start)},
            )
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        if unit["system"] == "C":
            from scripts.unified_matrix_c_opportunity import execute_unit
        else:
            from scripts.unified_matrix_research import execute_unit
        result = execute_unit(root, unit, progress=progress)
        write(path / "result.json", result)
        row = status_row(root, unit)
        source = result.get("source", result)
        replay = source.get("exact_replay")
        if result.get("fatal_execution_error") or result.get("status") == "execution_error":
            raise RuntimeError(f"Adapter execution defect: {result.get('failure')}")
        if row["operations"] and not (replay or {}).get("verified"):
            raise RuntimeError("source exact replay failed")
        retest = result.get("recommendation_retest")
        if (
            retest
            and retest.get("operations")
            and not (retest.get("exact_replay") or {}).get("verified")
        ):
            raise RuntimeError("recommendation exact replay failed")
        complete = (
            row["sealed_posttests"] == 3
            and row["completed_batches"] == unit["batches"]
            and not result.get("failure")
            and result.get("status") == "completed"
            and (result.get("prediction_evaluation") or {}).get("valid") is True
        )
        status = "completed" if complete else "incomplete"
        write(
            path / "status.json",
            {
                "status": status,
                "ended_at": now(),
                "elapsed_s": time.monotonic() - start,
                "failure": result.get("failure"),
                "unit": unit,
            },
        )
        return 0
    except Exception as exc:
        traceback.print_exc()
        write(
            path / "status.json",
            {
                "status": "execution_error",
                "ended_at": now(),
                "elapsed_s": time.monotonic() - start,
                "failure": f"{type(exc).__name__}: {exc}",
                "unit": unit,
            },
        )
        return 2
    finally:
        stop.set()


def run(root):
    import psutil

    if not (root / "prepared.json").exists():
        raise RuntimeError("Preparation has not completed")
    design = read(root / "design.json")
    coordinator = root / "coordinator.json"
    if coordinator.exists():
        previous = read(coordinator)
        if psutil.pid_exists(previous["pid"]):
            process = psutil.Process(previous["pid"])
            if process.create_time() == previous.get("process_created_epoch"):
                raise RuntimeError("This study already has a live coordinator")
    pending = []
    for unit in design["schedule"]:
        path = folder(root, unit)
        if not path.exists():
            pending.append(unit)
        elif (path / "status.json").exists() and read(path / "status.json").get(
            "status"
        ) in TERMINAL:
            continue
        else:
            raise RuntimeError(f"Ambiguous or active unit; will not relaunch: {path}")
    active, blocked = {}, set()
    stop_path = root / "block-stop.json"
    if stop_path.exists():
        blocked.update(read(stop_path)["systems"])
    started = time.monotonic()
    initial = snapshot(root)
    baseline = (initial["terminal_sessions"], initial["completed_source_batches"])
    write(
        root / "coordinator.json",
        {
            "pid": os.getpid(),
            "started_at": now(),
            "workers": design["workers"],
            "process_created_epoch": psutil.Process().create_time(),
        },
    )
    last_report = 0.0
    while pending or active:
        for key, record in list(active.items()):
            code = record["process"].poll()
            if code is None:
                continue
            record["stream"].close()
            del active[key]
            if code:
                blocked.add(record["unit"]["system"])
                write(
                    stop_path,
                    {
                        "systems": sorted(blocked),
                        "at": now(),
                        "reason": f"worker exit {code}: {key}",
                        "drain_in_flight": True,
                    },
                )
        launch_cap = (
            min(6, design["workers"]) if time.monotonic() - started < 60 else design["workers"]
        )
        while len(active) < launch_cap and psutil.virtual_memory().available > 8 * 1024**3:
            index = next((i for i, u in enumerate(pending) if u["system"] not in blocked), None)
            if index is None:
                break
            unit = pending.pop(index)
            key = (unit["repeat"], unit["id"])
            log = root / "logs" / f"{unit['repeat']}-{unit['id']}.log"
            log.parent.mkdir(exist_ok=True)
            stream = log.open("w", encoding="utf-8")
            command = [
                sys.executable,
                "-u",
                "-m",
                "scripts.run_unified_matrices",
                "--root",
                str(root),
                "--unit",
                unit["id"],
                "--repeat",
                unit["repeat"],
            ]
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                env={**os.environ, **WORKER_ENV},
                stdout=stream,
                stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            active[key] = {"process": process, "stream": stream, "unit": unit}
        if time.monotonic() - last_report >= 30 or not active:
            summary = snapshot(root, active, started, sorted(blocked), baseline)
            emit({k: v for k, v in summary.items() if k != "cases"})
            last_report = time.monotonic()
        if not active and (not pending or all(u["system"] in blocked for u in pending)):
            break
        time.sleep(2)
    summary = snapshot(root, (), started, sorted(blocked), baseline)
    write(root / "completion-status.json", {k: v for k, v in summary.items() if k != "cases"})
    return 2 if blocked else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--unit")
    parser.add_argument("--repeat")
    args = parser.parse_args()
    root = args.root.resolve()
    if not 1 <= args.workers <= 24:
        parser.error("workers must be between 1 and 24")
    if args.prepare:
        prepare(root, args.workers)
        return 0
    if args.summarize:
        emit({k: v for k, v in snapshot(root).items() if k != "cases"})
        return 0
    if args.unit:
        unit = next(
            u
            for u in read(root / "design.json")["schedule"]
            if u["id"] == args.unit and u["repeat"] == args.repeat
        )
        return worker(root, unit)
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main())
