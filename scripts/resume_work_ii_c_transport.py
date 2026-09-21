"""One declared zero-action C transport recovery; frozen runner remains unchanged."""

from __future__ import annotations

import argparse
import os
import shutil
import threading
import time
from pathlib import Path

import psutil
from scripts import run_work_ii_c_formal as formal
from scripts.run_work_ii_final_diagnostic import read, write


def prepare(original: Path, recovery: Path, report: Path) -> None:
    formal.verify_frozen(original)
    if formal.controller_alive(read(original / "controller-status.json")):
        raise ValueError("Original controller is still alive")
    design = read(original / "design.json")
    cell = design["schedule"][0]["id"]
    source = original / "sources" / cell
    result = read(source / "result.json")
    events = (source / "source-stdout.jsonl").read_text(encoding="utf-8")
    if (
        result["status"] != "failed"
        or result["source"]["operations"] != 0
        or result["source"]["batches"]
        or result["posttests"]
        or (source / "trajectory.jsonl").stat().st_size != 0
        or "error sending request for url" not in events
        or len(list((original / "sources").iterdir())) != 1
    ):
        raise ValueError("Recovery is limited to the observed first-cell zero-action failure")
    if not read(original / "qualification/result.json")["passed"]:
        raise ValueError("Original qualification did not pass")
    recovery.mkdir(parents=True, exist_ok=False)
    files = ["design.json", "release.json", "qualification/result.json"]
    files += [f"qualification/W{i:02d}/queries/result.json" for i in range(1, 6)]
    for relative in files:
        destination = recovery / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original / relative, destination)
        assert destination.read_bytes() == (original / relative).read_bytes()
    write(
        recovery / "prior-attempt.json",
        {
            "root": str(original),
            "cell": cell,
            "final_assays": 0,
            "operations": 0,
            "provider_sources": 1,
            "failure": result["failure"],
            "source_elapsed_s": result["source"]["elapsed_s"],
            "qualification_reused_from": str(original / "qualification"),
            "qualification_reexecuted": False,
            "recovery_reason": "zero-action provider transport failure; process-local proxy",
            "retry_limit": 1,
        },
    )
    formal.verify_frozen(recovery)
    formal.export(recovery, report)


def run(recovery: Path, report: Path, proxy: str) -> None:
    # Set inside the detached process: the Windows service does not inherit
    # the interactive launcher's environment. Never change user/global settings.
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        os.environ[name] = proxy
    os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
    formal.verify_frozen(recovery)
    if (recovery / "controller-status.json").exists():
        raise ValueError("This recovery has already started; no automatic second retry")
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "sources",
        "started_epoch": time.time(),
        "qualification_reused": True,
        "transport_recovery": 1,
    }
    stop = threading.Event()

    def emit() -> None:
        temporary = recovery / "controller-status.tmp"
        write(temporary, {**state, "epoch": time.time()})
        temporary.replace(recovery / "controller-status.json")
        formal.export(recovery, report)

    def heartbeat() -> None:
        while not stop.wait(30):
            emit()

    emit()
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        formal.run(recovery, report)
        summary = formal.export(recovery, report)
        state["stage"] = (
            "completed"
            if summary["completed_chains"] == summary["planned_sources"]
            else "ended_with_incomplete_chains"
        )
    except BaseException as exc:
        state.update(stage="interrupted", failure={"type": type(exc).__name__, "message": str(exc)})
        raise
    finally:
        stop.set()
        thread.join(timeout=5)
        emit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--proxy", required=True)
    parser.add_argument("--phase", choices=("launch", "run"), required=True)
    args = parser.parse_args()
    original, root, report = args.original.resolve(), args.root.resolve(), args.report.resolve()
    if args.phase == "run":
        run(root, report, args.proxy)
        return
    prepare(original, root, report)
    command = [
        "uv",
        "run",
        "--no-sync",
        "python",
        "-m",
        "scripts.resume_work_ii_c_transport",
        "--original",
        str(original),
        "--root",
        str(root),
        "--report",
        str(report),
        "--proxy",
        args.proxy,
        "--phase",
        "run",
    ]
    process = formal.detached_process(command, root / "controller.log")
    receipt = {"pid": process.pid, "command": command, "started_epoch": time.time()}
    write(root / "controller-launch.json", receipt)
    print(receipt, flush=True)


if __name__ == "__main__":
    main()
