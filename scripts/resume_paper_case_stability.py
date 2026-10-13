"""Resume unstarted stability units with user-authorized bounded concurrency.

An attached PID is monitored only; this scheduler never restarts a source.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil
from scripts.run_paper_case_notebooks import CASES, ROOT, emit, live, read, write
from scripts.run_paper_case_stability import REPEATS, snapshot


def receipt(root, repeat, unit):
    return root / repeat / (
        "references/complete.json" if unit == "references" else f"results/{unit}.json"
    )


def validate_receipt(root, repeat, unit):
    result = read(receipt(root, repeat, unit))
    if unit == "references":
        if result.get("completed_batches") != 144 or result.get("replay_verified") is not True:
            raise RuntimeError(f"reference defect: {repeat}")
    else:
        source = result.get("source", result)
        if source.get("operations", 0) and not source.get("exact_replay", {}).get("verified"):
            raise RuntimeError(f"source replay defect: {repeat}/{unit}")


def pending_units(root, attached):
    pending = []
    for repeat in REPEATS:
        for unit in ["references", *(c["id"] for c in CASES)]:
            key = (repeat, unit)
            if key in attached:
                continue
            if receipt(root, *key).exists():
                validate_receipt(root, *key)
                continue
            if (root / repeat / "logs" / f"{unit}.log").exists():
                raise RuntimeError(f"Previously launched unit requires explicit attachment: {key}")
            pending.append(key)
    return pending


def eligible(root, key):
    repeat, unit = key
    return unit == "references" or receipt(root, repeat, "references").exists()


def poll(record):
    if record["external"]:
        return None if record["process"].is_running() else 0
    return record["process"].poll()


def progress(root, active, started, baseline, concurrency):
    summary = snapshot(root)
    units = []
    for repeat, unit in active:
        counts = {}
        if unit != "references" and not receipt(root, repeat, unit).exists():
            case = next(c for c in CASES if c["id"] == unit)
            counts = live(root / repeat, case)
        units.append({"repeat": repeat, "stage": unit, **counts})
    completed = summary["completed_batches"] + sum(r.get("batches", 0) for r in units)
    elapsed = max(time.monotonic() - started, 1e-6)
    added = completed - baseline if baseline is not None else 0
    output = {
        "concurrency_limit": concurrency,
        "active_units": units,
        "terminal_sources": summary["terminal_sources"],
        "completed_sources": summary["completed_sources"],
        "completed_batches": completed,
        "total_batches": 252,
        "sealed_posttests": summary["sealed_posttests"],
        "total_posttests": 60,
        "segment_elapsed_s": round(elapsed),
        "segment_new_batches": added,
        "batches_per_minute": 60 * added / elapsed,
        "eta_s": elapsed / added * (252 - completed) if added > 0 else None,
    }
    write(root / "parallel-progress.json", output)
    emit(output)
    return output


def resume(root, concurrency, attachments):
    if (root / "block-stop.json").exists():
        raise RuntimeError("This block has a fatal stop; do not resume it")
    active = {}
    for repeat, unit, pid in attachments:
        if repeat not in REPEATS or unit not in {c["id"] for c in CASES}:
            raise ValueError("Unknown attached source")
        process = psutil.Process(pid)
        active[(repeat, unit)] = {"process": process, "external": True, "stream": None}
    pending = pending_units(root, active)
    started = time.monotonic()
    if len(active) > concurrency:
        raise ValueError("Attached sessions exceed concurrency limit")
    baseline = progress(root, active, started, None, concurrency)["completed_batches"]
    write(
        root / "concurrency-amendment.json",
        {
            "authorization": "User requested 4 or 8 concurrent sessions; use 4",
            "concurrency": concurrency,
            "attached": [{"repeat": r, "unit": u, "pid": p} for r, u, p in attachments],
            "unstarted_units": [{"repeat": r, "unit": u} for r, u in pending],
            "completed_batches_at_switch": baseline,
            "participant_runtime_changed": False,
            "source_retries": 0,
            "on_execution_defect": "stop new launches; drain and retain already active units",
        },
    )
    failed = False
    while pending or active:
        for key, record in list(active.items()):
            code = poll(record)
            if code is None:
                continue
            if record["stream"]:
                record["stream"].close()
            del active[key]
            try:
                if code:
                    raise RuntimeError(f"unit process exited {code}")
                validate_receipt(root, *key)
            except (RuntimeError, OSError, ValueError) as error:
                failed = True
                write(root / "block-stop.json", {"repeat": key[0], "unit": key[1],
                      "reason": str(error), "drain_in_flight": True, "source_retry": False})
        if not failed:
            for key in list(pending):
                if len(active) >= concurrency:
                    break
                if not eligible(root, key):
                    continue
                repeat, unit = key
                log = root / repeat / "logs" / f"{unit}.log"
                log.parent.mkdir(exist_ok=True)
                stream = log.open("x", encoding="utf-8")
                options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
                process = subprocess.Popen(
                    [sys.executable, "-m", "scripts.run_paper_case_notebooks", "--root",
                     str(root / repeat), "--unit", unit],
                    cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, **options,
                )
                active[key] = {"process": process, "external": False, "stream": stream}
                pending.remove(key)
                emit({"launched": f"{repeat}/{unit}", "pid": process.pid})
        progress(root, active, started, baseline, concurrency)
        if failed and not active:
            break
        if pending or active:
            time.sleep(30)
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--concurrency", type=int, choices=range(1, 9), default=4)
    parser.add_argument("--attach", action="append", default=[], metavar="REPEAT:CASE:PID")
    args = parser.parse_args()
    attachments = [(r, u, int(p)) for r, u, p in (s.split(":") for s in args.attach)]
    return resume(args.root.resolve(), args.concurrency, attachments)


if __name__ == "__main__":
    raise SystemExit(main())
