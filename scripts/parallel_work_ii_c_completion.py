"""Four isolated C workers with one coordinator and unchanged scientific sessions."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import threading
import time
from pathlib import Path

import psutil
from scripts import resume_work_ii_c_completion as recovery
from scripts import run_work_ii_c_formal as formal
from scripts.run_work_ii_final_diagnostic import read, write


def pending_jobs(root):
    repairs, sources = [], []
    for cell in read(root / "design.json")["schedule"]:
        folder = root / "sources" / cell["id"]
        path = folder / "result.json"
        if not path.exists():
            if folder.exists():
                raise ValueError(f"Unsealed source directory: {cell['id']}")
            sources.append({"cell": cell, "kind": "source", "failures": 0, "ready_at": 0})
            continue
        result = read(path)
        if result["status"] == "running":
            raise ValueError(f"Existing running source must finish before takeover: {cell['id']}")
        failure = result.get("failure") or {}
        stage = failure.get("stage")
        if result["status"] != "failed" or stage not in ("K1", "Q", "K2"):
            continue
        context = Path((result.get("posttest_repair") or {}).get("root", folder))
        receipt = context / stage / "receipt.json"
        log = context / stage / "stdout.jsonl"
        revoked = any(
            "refresh token was revoked" in e.lower() for e in recovery.provider_errors(log)
        )
        if (
            receipt.exists()
            and not read(receipt).get("payload")
            and (recovery.retryable_transport(log) or revoked)
            and result["source"]["exact_replay"].get("verified") is True
        ):
            repairs.append({"cell": cell, "kind": "repair", "failures": 0, "ready_at": 0})
    return repairs + sources


def ready_jobs(queue, capacity, now):
    selected = []
    for job in list(queue):
        if len(selected) >= capacity:
            break
        if job["ready_at"] <= now:
            queue.remove(job)
            selected.append(job)
    return selected


def source_retry(root, job, result):
    folder = root / "sources" / job["cell"]["id"]
    if (
        result["status"] != "failed"
        or (result.get("failure") or {}).get("stage") != "source"
        or not recovery.transport_failure(folder)
    ):
        return False
    recovery.archive_source_failure(root, job["cell"], result)
    job["failures"] += 1
    job["ready_at"] = time.time() + recovery.retry_delay(job["failures"])
    return True


def worker(root, job_path, proxy):
    job = read(job_path)
    output = job_path.parent
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        os.environ[key] = proxy
    os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
    formal.verify_frozen(root)
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "cell": job["cell"]["id"],
        "kind": job["kind"],
        "activity": "executing",
        "started_epoch": time.time(),
        "retry_events": 0,
    }
    progress = {"phase": job["kind"], "operations": 0, "batches": 0}
    stop, lock = threading.Event(), threading.Lock()

    def emit():
        with lock:
            status = {**state, **progress, "epoch": time.time()}
            recovery.atomic_write(output / "status.json", status)
            print(json.dumps(status), flush=True)

    def heartbeat():
        while not stop.wait(30):
            emit()

    def wait(failures, stage):
        delay = recovery.retry_delay(failures)
        state.update(activity="retry_wait", retry_at_epoch=time.time() + delay)
        state["retry_events"] += 1
        progress["phase"] = stage
        emit()
        deadline = time.monotonic() + delay
        while time.monotonic() < deadline:
            time.sleep(min(30, max(0, deadline - time.monotonic())))
        state.update(activity="executing", retry_at_epoch=None)
        emit()

    original = formal.pilot.posttest

    def posttest(agent, folder, stage, thread_id, live, design):
        return recovery.retry_posttest(
            original, agent, folder, stage, thread_id, live, design, wait
        )

    emit()
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        if job["kind"] == "repair":
            if not recovery.repair_posttests(root, job["cell"], progress, wait):
                raise ValueError("Repair no longer matches its declared transport boundary")
        else:
            formal.pilot.posttest = posttest
            formal.source(root, job["cell"], progress)
        state["activity"] = "finished"
    except BaseException as exc:
        state.update(
            activity="worker_error", failure={"type": type(exc).__name__, "message": str(exc)}
        )
        raise
    finally:
        formal.pilot.posttest = original
        stop.set()
        thread.join(5)
        emit()


def coordinate(root, report, proxy, workers, *, repairs_only=False):
    old = read(root / "controller-status.json")
    if formal.controller_alive(old):
        raise ValueError("Existing controller is alive")
    waiter = root / "posttest-repair-controller.json"
    if waiter.exists() and formal.controller_alive(read(waiter)):
        raise ValueError("Existing repair waiter is alive")
    formal.verify_frozen(root)
    if not read(root / "qualification/result.json")["passed"]:
        raise ValueError("Qualification has not passed")
    queue = pending_jobs(root)
    if repairs_only:
        queue = [job for job in queue if job["kind"] == "repair"]
    work = root / ("parallel-posttest-workers" if repairs_only else "parallel-workers")
    work.mkdir(exist_ok=False)
    write(
        work / "takeover.json",
        {"previous_controller": old, "initial_jobs": queue, "workers": workers},
    )
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "sources",
        "activity": "parallel",
        "concurrency": workers,
        "started_epoch": time.time(),
        "retry_events": old.get("retry_events", 0),
    }
    active, finished, errors = {}, [], []
    next_emit = 0.0
    attempt = 0
    last_summary = None

    def emit():
        nonlocal last_summary
        states = []
        for entry in active.values():
            path = entry["path"] / "status.json"
            s = (
                read(path)
                if path.exists()
                else {
                    "cell": entry["job"]["cell"]["id"],
                    "kind": entry["job"]["kind"],
                    "activity": "starting",
                }
            )
            states.append(s)
        snapshot = {
            **state,
            "epoch": time.time(),
            "active_workers": len(active),
            "queued_jobs": len(queue),
            "finished_jobs": len(finished),
            "worker_errors": errors,
            "workers": states,
        }
        recovery.atomic_write(root / "controller-status.json", snapshot)
        try:
            summary = formal.export(root, report)
        except json.JSONDecodeError:
            # Frozen workers write result.json during stage transitions. Retry the
            # read on the next heartbeat, never alter or discard their records.
            print(json.dumps({**snapshot, "report": "waiting_for_result_write"}), flush=True)
            return
        last_summary = summary
        progress = {
            **snapshot,
            "completed_chains": summary["completed_chains"],
            "planned_chains": 30,
            "sealed_batches": summary["sealed_batches"],
            "completed_posttests": summary["completed_posttests"],
            "planned_posttests": 90,
            "elapsed_s": round(time.time() - state["started_epoch"]),
            "finished_jobs_per_hour": len(finished)
            * 3600
            / max(1, time.time() - state["started_epoch"]),
            "eta_s": None,
        }
        recovery.atomic_write(root / "progress.json", progress)
        summary["parallel_execution"] = snapshot
        recovery.atomic_write(report / "summary.json", summary)
        path = report / "REPORT.md"
        body = path.read_text(encoding="utf-8")
        body = body.replace("reference final assays", "interrupted source batch assays")
        body = body.replace(
            "These do not count as sealed qualification units.",
            "These are extra attempts, excluded from effective matrix denominators.",
        )
        banner = (
            f"Parallel continuation: {len(active)}/{workers} worker slots occupied; "
            f"{len(queue)} queued jobs; {len(finished)} jobs settled since takeover. "
            "Independent processes; sequential decisions and K1/Q/K2 within each cell.\n\n"
        )
        if states:
            banner += (
                "| Worker cell | Work | Stage | Activity | Batches |\n"
                "| --- | --- | --- | --- | ---: |\n"
            )
            for s in states:
                banner += (
                    f"| {s['cell']} | {s['kind']} | {s.get('phase', '')} "
                    f"| {s['activity']} | {s.get('batches', 0)} |\n"
                )
            banner += "\n"
        path.write_text(body.replace("\n\n", "\n\n" + banner, 1), encoding="utf-8")
        print(json.dumps(progress), flush=True)

    emit()
    try:
        while queue or active:
            for key, entry in list(active.items()):
                process = entry["process"]
                if process.poll() is None:
                    continue
                entry["log"].close()
                del active[key]
                job = entry["job"]
                if process.returncode:
                    errors.append(
                        {
                            "cell": job["cell"]["id"],
                            "worker": str(entry["path"]),
                            "exit_code": process.returncode,
                        }
                    )
                    continue
                result = read(root / "sources" / job["cell"]["id"] / "result.json")
                if job["kind"] == "source" and source_retry(root, job, result):
                    queue.append(job)
                    state["retry_events"] += 1
                else:
                    finished.append(
                        {"cell": job["cell"]["id"], "kind": job["kind"], "status": result["status"]}
                    )
                next_emit = 0
            for job in ready_jobs(queue, workers - len(active), time.time()):
                attempt += 1
                path = work / f"{attempt:03d}-{job['cell']['id']}-{job['kind']}"
                path.mkdir()
                write(path / "job.json", job)
                command = [
                    "uv",
                    "run",
                    "--no-sync",
                    "python",
                    "-m",
                    "scripts.parallel_work_ii_c_completion",
                    "--root",
                    str(root),
                    "--report",
                    str(report),
                    "--proxy",
                    proxy,
                    "--phase",
                    "worker",
                    "--job",
                    str(path / "job.json"),
                ]
                log = (path / "worker.log").open("ab", buffering=0)
                process = subprocess.Popen(
                    command,
                    cwd=formal.ROOT,
                    stdin=subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
                active[attempt] = {"job": job, "path": path, "process": process, "log": log}
                next_emit = 0
            if time.monotonic() >= next_emit:
                emit()
                next_emit = time.monotonic() + 30
            time.sleep(1)
        state.update(
            stage="completed"
            if last_summary and last_summary["completed_chains"] == 30
            else "ended_with_incomplete_chains",
            activity="finished",
        )
    except BaseException as exc:
        state.update(stage="interrupted", activity="coordinator_error", failure=str(exc))
        # Do not kill intact source sessions on a reporting/controller exception.
        raise
    finally:
        emit()
        write(work / "outcome.json", {"finished": finished, "errors": errors, "pending": queue})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--proxy", required=True)
    parser.add_argument(
        "--phase",
        choices=("launch", "coordinate", "worker", "queue-repair-sweep", "repair-sweep"),
        required=True,
    )
    parser.add_argument("--workers", type=int, choices=(4,), default=4)
    parser.add_argument("--job", type=Path)
    args = parser.parse_args()
    root, report = args.root.resolve(), args.report.resolve()
    if args.phase == "repair-sweep":
        status = {
            "pid": os.getpid(),
            "process_created": psutil.Process().create_time(),
            "stage": "waiting_for_four_worker_queue",
        }
        while formal.controller_alive(read(root / "controller-status.json")):
            recovery.atomic_write(
                root / "parallel-repair-waiter.json", {**status, "epoch": time.time()}
            )
            print(json.dumps({**status, "epoch": time.time()}), flush=True)
            time.sleep(30)
        previous = read(root / "controller-status.json")
        if previous.get("stage") not in ("completed", "ended_with_incomplete_chains"):
            raise ValueError("Main queue exited unexpectedly; inspect before repair takeover")
        coordinate(root, report, args.proxy, args.workers, repairs_only=True)
        return
    if args.phase == "queue-repair-sweep":
        waiting = root / "parallel-repair-waiter.json"
        if waiting.exists() and formal.controller_alive(read(waiting)):
            raise ValueError("Repair sweep is already queued")
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            "-m",
            "scripts.parallel_work_ii_c_completion",
            "--root",
            str(root),
            "--report",
            str(report),
            "--proxy",
            args.proxy,
            "--phase",
            "repair-sweep",
            "--workers",
            str(args.workers),
        ]
        process = formal.detached_process(command, root / "parallel-repair-sweep.log")
        print(json.dumps({"queued_repair_sweep_pid": process.pid}), flush=True)
        return
    if args.phase == "worker":
        worker(root, args.job.resolve(), args.proxy)
    elif args.phase == "coordinate":
        coordinate(root, report, args.proxy, args.workers)
    else:
        if formal.controller_alive(read(root / "controller-status.json")):
            raise ValueError("Old controller is still alive")
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            "-m",
            "scripts.parallel_work_ii_c_completion",
            "--root",
            str(root),
            "--report",
            str(report),
            "--proxy",
            args.proxy,
            "--phase",
            "coordinate",
            "--workers",
            str(args.workers),
        ]
        process = formal.detached_process(command, root / "parallel-controller.log")
        receipt = {"pid": process.pid, "command": command, "started_epoch": time.time()}
        write(root / "parallel-launch.json", receipt)
        print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
