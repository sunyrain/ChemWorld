"""Bounded isolated source processes; one owner of the EC/PA matrix ledger."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import threading
import time
from pathlib import Path

import psutil
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_ec_pa_matrix as matrix
from scripts import run_work_ii_pa_single_trial as pa
from scripts.recover_work_ii_ec_pa_network import (
    effective_row,
    network_failure,
    recover,
    recovery_inputs,
    recovery_kind,
    source_folder,
)
from scripts.run_work_ii_astra_single_trial import read, write

from chemworld.eval.provenance import write_json_atomic


def unit_paths(root, unit):
    parent = root / "sources" / unit["unit_id"]
    actual = (
        parent / f"{unit['goal']}-{unit['locus']}-{unit['arm']}"
        if unit["system"] == "EC"
        else parent
    )
    return parent, actual


def collect(root, unit):
    _, actual = unit_paths(root, unit)
    row = matrix.source_row(unit, read(actual / "result.json"))
    row["exported"] = True
    records = [
        read(p)
        for p in sorted(
            (root / "recoveries" / unit["unit_id"]).glob("attempt-*/recovery.json"),
            key=lambda p: int(p.parent.name.split("-")[-1]),
        )
    ]
    if records:
        rec = records[-1]
        if len(records) > 1:
            row["recovery_history"] = records[:-1]
        key = (
            "infrastructure_recovery"
            if rec["kind"].endswith("host_interruption")
            else "network_recovery"
        )
        row[key] = rec
    return row


def next_units(rows, active, slots):
    # All E sources must be terminal before any P/S source is dispatched.
    e_pending = any(
        r["locus"] == "E" and (r["status"] not in ("completed", "failed") or r["unit_id"] in active)
        for r in rows
    )
    return [
        r
        for r in rows
        if r["status"] == "not_started"
        and r["unit_id"] not in active
        and (r["locus"] == "E" or not e_pending)
    ][:slots]


def prepare_owned_directory(folder, *, system="EC"):
    if system == "PA":
        if folder.exists():
            raise RuntimeError("PA source directory already exists; refusing duplicate execution")
        folder.parent.mkdir(parents=True, exist_ok=True)
        return  # PA execute creates its own root atomically.
    if folder.exists():
        if {p.name for p in folder.iterdir()} != {"parallel-handover.json"}:
            raise RuntimeError(
                "source directory already contains work; refusing duplicate execution"
            )
    else:
        folder.mkdir(parents=True, exist_ok=False)


def run_unit(
    root,
    report,
    unit,
    *,
    recovery_only=False,
    allow_partial=False,
    recovery_attempt=1,
    allow_usage_limit=False,
):
    if recovery_attempt != 1 and not recovery_only:
        raise ValueError("additional attempts apply only to an explicitly resumed source")
    if allow_usage_limit and not recovery_only:
        raise ValueError("quota restoration applies only to explicitly resumed posttests")
    folder, actual = unit_paths(root, unit)
    if not recovery_only:
        prepare_owned_directory(folder, system=unit["system"])
    design = read(root / "design.json")
    ref_folder = root / "references" / unit["world"]["world_id"]
    ref_design = read(ref_folder / "design.json")
    reference = read(ref_folder / ref_design.get("reference_result_file", "reference-result.json"))
    progress = {
        "unit": unit["unit_id"],
        "stage": "source",
        "phase": "source",
        "batches": 0,
        "operations": 0,
        "planned_batches": unit["budget"],
        "pid": os.getpid(),
    }
    started = time.monotonic()
    stop = threading.Event()
    if recovery_only or unit["system"] == "EC":
        write_json_atomic(
            folder / "worker-progress.json",
            {**progress, "elapsed_s": 0, "updated_epoch": time.time()},
        )

    def heartbeat():
        while not stop.wait(15):
            live = {
                **progress,
                "elapsed_s": time.monotonic() - started,
                "updated_epoch": time.time(),
            }
            write_json_atomic(folder / "worker-progress.json", live)
            print(json.dumps(live, default=str), flush=True)

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        if recovery_only:
            saved = read(folder / "design.json")
            result = read(actual / "result.json")
            latest, latest_folder, posttests = recovery_inputs(
                root, unit, result, actual, attempt=recovery_attempt
            )
            if (
                recovery_kind(
                    unit,
                    latest,
                    latest_folder,
                    allow_partial=allow_partial,
                    posttest_folder=posttests,
                    allow_usage_limit=allow_usage_limit,
                )
                is None
            ):
                raise ValueError("existing source has no eligible network recovery")
        elif unit["system"] == "EC":
            saved = {
                **design["questions"]["EC"],
                "queries": design["queries"]["EC"],
                "query_version": ec.QUERY_VERSION,
                "world_config": unit["world"],
                "batches_per_source": unit["budget"],
                "system": design["ec_system"][str(unit["budget"])],
                "goal": ec.GOALS[unit["goal"]],
            }
            write(folder / "design.json", saved)
            result = ec.run_cell(
                folder,
                unit["goal"],
                unit["locus"],
                unit["arm"],
                reference["truth"],
                progress,
            )
        else:
            # PA execute owns creation of its root; do not precreate files inside it.
            numerics = design["questions"]["PA"].get("posttest_numerics")
            pa.execute(
                folder,
                progress,
                arm=unit["arm"],
                batches=unit["budget"],
                world=unit["world"],
                reference_run=root / "references" / unit["world"]["world_id"],
                numerics_budget=pa.NumericsBudget.from_record(numerics)
                if numerics is not None
                else None,
            )
            result, saved = read(folder / "result.json"), read(folder / "design.json")
        if not recovery_only:
            matrix.export_source(unit, result, actual, report / unit["unit_id"], saved)
        recovered = recover(
            root,
            report,
            unit,
            result,
            actual,
            saved,
            reference["truth"],
            progress,
            allow_partial=allow_partial,
            **({"attempt": recovery_attempt} if recovery_attempt != 1 else {}),
            **({"allow_usage_limit": True} if allow_usage_limit else {}),
        )
        row = matrix.source_row(unit, result) if not recovered else recovered["row"]
        reason = None
        if recovered and read(Path(recovered["result_path"])).get("failure"):
            reason = "infrastructure recovery failed"
        elif not row["operations"] or not row["exact_replay"].get("verified"):
            reason = "source startup/replay failure"
        elif (
            not recovered
            and result.get("failure")
            and network_failure(source_folder(unit, actual) / "source-stdout.jsonl")
        ):
            reason = "partial source network failure"
        progress.update(stage="terminal", stop_reason=reason)
    except BaseException as exc:
        progress.update(stage="executor_failed", stop_reason=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        stop.set()
        thread.join(timeout=1)
        write_json_atomic(
            folder / "worker-progress.json",
            {**progress, "elapsed_s": time.monotonic() - started, "updated_epoch": time.time()},
        )


def accept_handover(state, reserved):
    expected = f"partial source retained; no automatic retry: {reserved}"
    failure = state.get("failure") or {}
    if state["status"] != "stopped" or failure.get("message") != expected:
        raise RuntimeError("old executor did not finish at the reserved handover boundary")
    state.setdefault("runtime_incidents", []).append(
        {
            "classification": "authorized_parallel_handover",
            "original_stop": failure,
            "unit_reserved": reserved,
            "scientific_failure": False,
        }
    )
    state["failure"] = None
    state["status"] = "running"


def next_recovery_attempt(root, unit):
    """One next attempt for an explicit resume; never an automatic retry loop."""
    folders = sorted(
        (root / "recoveries" / unit["unit_id"]).glob("attempt-*"),
        key=lambda p: int(p.name.split("-")[-1]),
    )
    for index, folder in enumerate(folders, 1):
        if folder.name != f"attempt-{index}" or not (folder / "recovery.json").is_file():
            raise ValueError(
                "unfinished or discontinuous recovery must be reconciled before resume"
            )
    return len(folders) + 1


def resume_recoveries(
    root,
    state,
    *,
    allow_partial,
    recovery_attempt=1,
    next_recovery=False,
    allow_usage_limit=False,
):
    """Validate the diagnosed stop without discarding a failed source or its costs."""
    if state["status"] != "stopped":
        raise ValueError("resume requires a stopped coordinator")
    if any(r["status"] == "running" for r in state["results"]):
        raise ValueError("unresolved running sources must be reconciled before resume")
    pending = []
    for row in state["results"]:
        if effective_row(row)["status"] != "failed":
            continue
        _, actual = unit_paths(root, row)
        original = read(actual / "result.json")
        number = next_recovery_attempt(root, row) if next_recovery else recovery_attempt
        attempt = root / "recoveries" / row["unit_id"] / f"attempt-{number}"
        if attempt.exists():
            raise ValueError("recovery attempt already exists; refusing another paid attempt")
        latest, latest_folder, posttests = recovery_inputs(
            root, row, original, actual, attempt=number
        )
        if (
            recovery_kind(
                row,
                latest,
                latest_folder,
                allow_partial=allow_partial,
                posttest_folder=posttests,
                allow_usage_limit=allow_usage_limit,
            )
            is None
        ):
            continue
        pending.append({**row, "recovery_attempt": number} if next_recovery else row)
    failure = state.get("failure") or {}
    if failure.get("unit") not in {r["unit_id"] for r in pending}:
        raise ValueError("stopped unit is not an eligible network recovery")
    return pending


def source_counts(rows, active):
    completed = sum(effective_row(r)["status"] == "completed" for r in rows)
    failed = sum(
        effective_row(r)["status"] == "failed" and r["unit_id"] not in active for r in rows
    )
    return {
        "completed_sources": completed,
        "failed_sources": failed,
        "terminal_sources": completed + failed,
    }


def coordinate(
    root,
    report,
    *,
    workers,
    old_executor_pid=None,
    reserved_unit=None,
    resume=False,
    allow_partial=False,
    recovery_attempt=1,
    next_recovery=False,
    allow_usage_limit=False,
):
    if not 1 <= workers <= 4:
        raise ValueError("authorized concurrency is between one and four sources")
    if resume and (old_executor_pid or reserved_unit):
        raise ValueError("resume and serial handover are different boundaries")
    if recovery_attempt != 1 and not resume:
        raise ValueError("additional recovery requires explicit resume")
    if next_recovery and (not resume or recovery_attempt != 1):
        raise ValueError("next recovery requires resume without a fixed attempt override")
    if allow_usage_limit and not resume:
        raise ValueError("quota restoration requires an explicit resume")
    if not resume and (not old_executor_pid or not reserved_unit):
        raise ValueError("serial handover requires its executor and reserved unit")
    plan = read(root / "design.json")["units"]
    by_id = {u["unit_id"]: u for u in plan}
    active = {}
    started = time.monotonic()
    initial = read(root / "summary.json")
    baseline = sum(
        effective_row(r)["status"] in ("completed", "failed") for r in initial["results"]
    )
    baseline_completed = source_counts(initial["results"], {})["completed_sources"]
    old = (
        psutil.Process(old_executor_pid)
        if old_executor_pid and psutil.pid_exists(old_executor_pid)
        else None
    )
    if old and "scripts.run_work_ii_ec_pa_matrix" not in " ".join(old.cmdline()):
        raise ValueError("old executor PID belongs to a different command")
    handover_pending = not resume
    state = None
    halt = None

    def launch(unit, *, recovery_only=False, attempt=1):
        folder, _ = unit_paths(root, unit)
        # External wrapper logs remain outside the repository.
        import tempfile

        log = Path(tempfile.gettempdir()) / f"chemworld-parallel-{unit['unit_id']}-{time.time_ns()}"
        stdout = log.with_suffix(".stdout.log").open("w", encoding="utf-8")
        stderr = log.with_suffix(".stderr.log").open("w", encoding="utf-8")
        command = [
            shutil.which("uv") or "uv",
            "run",
            "--no-sync",
            "python",
            "-u",
            "-m",
            "scripts.run_work_ii_ec_pa_parallel",
            "--output",
            str(root),
            "--report",
            str(report),
            "--unit",
            unit["unit_id"],
        ]
        if allow_partial:
            command.append("--retry-partial-network")
        if recovery_only:
            command.append("--recover-unit")
            command.extend(["--recovery-attempt", str(attempt)])
            if allow_usage_limit:
                command.append("--resume-after-quota")
        process = subprocess.Popen(
            command,
            cwd=matrix.ROOT,
            stdout=stdout,
            stderr=stderr,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        active[unit["unit_id"]] = {
            "process": process,
            "stdout": stdout,
            "stderr": stderr,
            "folder": folder,
            "started_epoch": time.time(),
        }
        print(json.dumps({"launched": unit["unit_id"], "pid": process.pid}), flush=True)

    if resume:
        state = initial
        pending = resume_recoveries(
            root,
            state,
            allow_partial=allow_partial,
            recovery_attempt=recovery_attempt,
            next_recovery=next_recovery,
            allow_usage_limit=allow_usage_limit,
        )
        if len(pending) > workers:
            raise ValueError("recovery queue exceeds available source slots")
        state.setdefault("runtime_incidents", []).append(
            {
                "classification": "authorized_network_resume",
                "original_stop": state.get("failure"),
                "previous_execution": state.get("parallel_execution"),
                "workers": workers,
                "authorization": "2026-09-19 user requested network recovery and continuation",
                "recovery_attempt": recovery_attempt,
                "recovery_attempts": {
                    r["unit_id"]: r.get("recovery_attempt", recovery_attempt) for r in pending
                },
                "recovery_units": [r["unit_id"] for r in pending],
                "usage_limit_restoration_authorized": allow_usage_limit,
            }
        )
        baseline -= len(pending)
        state.update(status="running", failure=None)
        state["parallel_execution"] = {
            "workers": workers,
            "coordinator_pid": os.getpid(),
            "started_epoch": time.time(),
            "baseline_terminal_sources": baseline,
            "baseline_completed_sources": baseline_completed,
            "source_process_isolation": True,
            "partial_network_recovery": allow_partial,
            "authorization": "2026-09-19 user requested further parallelism for 19:00",
        }
        for row in pending:
            launch(
                by_id[row["unit_id"]],
                recovery_only=True,
                attempt=row.get("recovery_attempt", recovery_attempt),
            )
    else:
        launch(by_id[reserved_unit])
    try:
        while True:
            if handover_pending:
                if old and old.is_running():
                    print(
                        json.dumps(
                            {
                                "stage": "handover",
                                "old_executor_pid": old_executor_pid,
                                "new_source": reserved_unit,
                                "max_active_sources": workers,
                            }
                        ),
                        flush=True,
                    )
                    time.sleep(15)
                    continue
                state = read(root / "summary.json")
                accept_handover(state, reserved_unit)
                handover_pending = False
                baseline = sum(
                    effective_row(r)["status"] in ("completed", "failed") for r in state["results"]
                )
                baseline_completed = source_counts(state["results"], {})["completed_sources"]
                state["parallel_execution"] = {
                    "workers": workers,
                    "coordinator_pid": os.getpid(),
                    "started_epoch": time.time(),
                    "authorization": "2026-09-19 user requested moderate parallel execution",
                    "source_process_isolation": True,
                    "baseline_terminal_sources": baseline,
                }
                for row in state["results"]:
                    if row["unit_id"] in active:
                        row["status"] = "running"
            for uid, job in list(active.items()):
                code = job["process"].poll()
                if code is None:
                    continue
                job["stdout"].close()
                job["stderr"].close()
                index = next(i for i, r in enumerate(state["results"]) if r["unit_id"] == uid)
                _, actual = unit_paths(root, by_id[uid])
                if (actual / "result.json").exists():
                    state["results"][index] = collect(root, by_id[uid])
                else:
                    state["results"][index].update(
                        status="failed", failure="executor result missing"
                    )
                progress_file = job["folder"] / "worker-progress.json"
                final = read(progress_file) if progress_file.exists() else {}
                if code != 0 or final.get("stop_reason"):
                    halt = {"unit": uid, "exit_code": code, "message": final.get("stop_reason")}
                del active[uid]
            if not halt:
                for row in next_units(state["results"], active, workers - len(active)):
                    row["status"] = "running"
                    launch(by_id[row["unit_id"]])
            live = []
            for uid, job in active.items():
                path = job["folder"] / "worker-progress.json"
                item = read(path) if path.exists() else {"unit": uid, "stage": "starting"}
                if item.get("updated_epoch", 0) < job["started_epoch"]:
                    item = {"unit": uid, "stage": "starting"}
                live.append({**item, "pid": job["process"].pid})
            counts = source_counts(state["results"], active)
            terminal = counts["terminal_sources"]
            elapsed = time.monotonic() - started
            delta = counts["completed_sources"] - baseline_completed
            throughput = delta / elapsed * 3600 if delta > 0 and elapsed > 0 else None
            progress = {
                "stage": "draining_after_failure" if halt else "parallel",
                "workers": live,
                "active_sources": len(active),
                "max_active_sources": workers,
                **counts,
                "planned_sources": len(plan),
                "elapsed_s": elapsed,
                "sources_per_hour": throughput,
                "throughput_basis": "successful completions in this concurrency segment",
                "eta_s": (len(plan) - terminal) / throughput * 3600
                if throughput and not halt
                else None,
            }
            if halt:
                state["failure"] = halt
                state["status"] = "draining_after_failure"
            if not active:
                state["status"] = "stopped" if halt else "completed"
                state["failure"] = halt
                progress["stage"] = state["status"]
            matrix.save_matrix_state(root, report, state, progress, elapsed_s=elapsed)
            write_json_atomic(root / "progress.json", {"heartbeat": progress, "elapsed_s": elapsed})
            print(json.dumps(progress, default=str), flush=True)
            if not active:
                break
            time.sleep(15)
    finally:
        # Do not kill live sources when only their coordinator encounters an error.
        for job in active.values():
            job["stdout"].close()
            job["stderr"].close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--unit")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--old-executor-pid", type=int)
    parser.add_argument("--reserved-unit")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--recover-unit", action="store_true")
    parser.add_argument("--retry-partial-network", action="store_true")
    parser.add_argument("--recovery-attempt", type=int, default=1)
    parser.add_argument("--resume-next-recovery", action="store_true")
    parser.add_argument("--resume-after-quota", action="store_true")
    args = parser.parse_args()
    if args.recovery_attempt < 1:
        parser.error("recovery attempt must be positive")
    if args.resume_next_recovery and (args.unit or not args.resume):
        parser.error("next recovery is a coordinator resume option")
    root, report = args.output.resolve(), args.report.resolve()
    if args.unit:
        unit = next(u for u in read(root / "design.json")["units"] if u["unit_id"] == args.unit)
        run_unit(
            root,
            report,
            unit,
            recovery_only=args.recover_unit,
            allow_partial=args.retry_partial_network,
            recovery_attempt=args.recovery_attempt,
            allow_usage_limit=args.resume_after_quota,
        )
    else:
        coordinate(
            root,
            report,
            workers=args.workers,
            old_executor_pid=args.old_executor_pid,
            reserved_unit=args.reserved_unit,
            resume=args.resume,
            allow_partial=args.retry_partial_network,
            recovery_attempt=args.recovery_attempt,
            next_recovery=args.resume_next_recovery,
            allow_usage_limit=args.resume_after_quota,
        )


if __name__ == "__main__":
    main()
