"""One coordinator for independent, frozen Work II information sessions."""

from __future__ import annotations

import json
import os
import time
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path


def rate_limited(result: dict) -> bool:
    return any(
        429 in error.get("http_status_codes", [])
        for receipt in result.get("receipts", [])
        for error in receipt.get("provider_errors", [])
    )


def run_parallel(root: Path, runner, workers: int) -> None:
    """Workers write disjoint sessions; only the drained coordinator may collect."""
    if workers not in (2, 3):
        raise ValueError("parallel execution requires two or three workers")
    inputs = runner.read(root / "inputs.json")
    frozen = runner.read(root / "freeze.json")
    provider = inputs["protocol"]["providers"][inputs["model"]]
    if frozen["execution_surface"] != runner.surface(provider) or frozen[
        "inputs_sha256"
    ] != runner.digest(root / "inputs.json"):
        raise ValueError("frozen session surface or inputs changed")
    path = root / "parallel_schedule.json"
    schedule = runner.read(path)
    if schedule["requested_workers"] != workers:
        raise ValueError("worker count differs from the recorded schedule amendment")
    with (root / "executor.lock").open("x", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    try:
        # This is the sole collection before workers start. Never collect active attempts.
        existing = runner.collect(root, inputs["cells"])
        if any((r.get("failure") or "").startswith(("platform_", "forbidden_")) for r in existing):
            raise ValueError("parallel scheduling cannot override a platform/boundary stop")
        terminal = {r["cell_id"]: r for r in existing}
        pending = deque(
            (i, cell)
            for i, cell in enumerate(inputs["cells"], 1)
            if cell["cell_id"] not in terminal
        )
        schedule.update(
            status="running",
            activated_epoch=time.time(),
            effective_workers=workers,
            first_unstarted_session=pending[0][0] if pending else None,
            concurrency_changes=[],
        )
        runner.write(path, schedule)
        active = {}
        started = time.monotonic()
        initial_terminal = len(terminal)
        limit = workers
        drain_for_rate_limit = False
        stop_reason = None
        next_heartbeat = 0.0

        def progress() -> None:
            now = time.monotonic()
            finished = len(terminal) - initial_terminal
            rate = finished / max(now - started, 1)
            state = {
                "stage": "parallel_queue",
                "terminal": len(terminal),
                "total": len(inputs["cells"]),
                "counts": dict(Counter(r["status"] for r in terminal.values())),
                "active_sessions": sorted(i for i, _ in active.values()),
                "unresolved_sessions": [r["session"] for r in schedule.get("worker_errors", [])],
                "unstarted": len(pending),
                "workers": limit,
                "sessions_per_min": round(rate * 60, 3),
                "eta_s": round((len(pending) + len(active)) / rate)
                if rate and not stop_reason
                else None,
                "stop_reason": stop_reason,
                "draining_for_rate_limit": drain_for_rate_limit,
                "updated_epoch": time.time(),
            }
            runner.write(root / "progress.json", state)
            print(json.dumps(state), flush=True)

        with ThreadPoolExecutor(
            max_workers=workers, thread_name_prefix="information-session"
        ) as pool:
            while pending or active:
                if drain_for_rate_limit and not active:
                    limit = 1
                    drain_for_rate_limit = False
                    schedule["effective_workers"] = 1
                    schedule["concurrency_changes"].append(
                        {
                            "epoch": time.time(),
                            "workers": 1,
                            "reason": "explicit_http_429",
                        }
                    )
                    runner.write(path, schedule)
                while pending and len(active) < limit and not (stop_reason or drain_for_rate_limit):
                    index, cell = pending.popleft()
                    directory = root / "sessions" / f"{index:03d}"
                    if (directory / "attempt.json").exists() or (
                        directory / "result.json"
                    ).exists():
                        raise ValueError("scheduled session was already attempted; preserve it")
                    future = pool.submit(
                        runner.run_session,
                        cell,
                        inputs["protocol"],
                        inputs["phase"],
                        directory,
                        float("inf"),
                        {"session_index": index, "model": cell["model"], "workers": limit},
                        prompt_factory=runner.prompt,
                    )
                    active[future] = (index, cell)
                if time.monotonic() >= next_heartbeat:
                    progress()
                    next_heartbeat = time.monotonic() + 30
                if not active:
                    break
                done, _ = wait(active, timeout=1, return_when=FIRST_COMPLETED)
                for future in sorted(done, key=lambda f: active[f][0]):
                    index, cell = active.pop(future)
                    try:
                        result = future.result()
                    except Exception as error:
                        stop_reason = f"scheduler_exception_{type(error).__name__}"
                        schedule.setdefault("worker_errors", []).append(
                            {
                                "session": index,
                                "error_type": type(error).__name__,
                            }
                        )
                        continue
                    terminal[cell["cell_id"]] = result
                    failure = result.get("failure") or ""
                    if failure.startswith(("platform_", "forbidden_")):
                        stop_reason = failure
                    if rate_limited(result) and limit > 1:
                        drain_for_rate_limit = True
                    print(
                        json.dumps(
                            {
                                "session_terminal": index,
                                "status": result["status"],
                                "failure": result.get("failure"),
                                "elapsed_s": result.get("elapsed_s"),
                            }
                        ),
                        flush=True,
                    )
                if done:
                    progress()
        schedule.update(
            status="stopped" if stop_reason else "finished",
            finished_epoch=time.time(),
            stop_reason=stop_reason,
        )
        runner.write(path, schedule)
        progress()
    finally:
        (root / "executor.lock").unlink()
    if stop_reason:
        print(f"queue stopped after draining: {stop_reason}", flush=True)
