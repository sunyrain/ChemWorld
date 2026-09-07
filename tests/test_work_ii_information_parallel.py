from __future__ import annotations

import math
import threading
from types import SimpleNamespace

import pytest
from scripts.run_work_ii_final_diagnostic import collect, digest, read, write
from scripts.run_work_ii_information_parallel import run_parallel


def fixture_runner(tmp_path, execute):
    cells = [{"cell_id": f"cell-{i}", "model": "deepseek", "tool": "on"} for i in range(8)]
    budgets = {"turn_timeout_s": 600, "session_timeout_s": 1200, "provider_retries": 0}
    write(
        tmp_path / "inputs.json",
        {
            "phase": "formal",
            "model": "deepseek",
            "cells": cells,
            "protocol": {"providers": {"deepseek": {}}, "formal": budgets},
        },
    )
    write(
        tmp_path / "freeze.json",
        {"execution_surface": {}, "inputs_sha256": digest(tmp_path / "inputs.json")},
    )
    write(tmp_path / "parallel_schedule.json", {"requested_workers": 3})
    write(
        tmp_path / "sessions/001/result.json",
        {"cell_id": cells[0]["cell_id"], "status": "failed", "failure": "tool_budget_exceeded"},
    )
    write(tmp_path / "sessions/002/attempt.json", {"cell_id": cells[1]["cell_id"]})
    prompt = object()

    def session(cell, protocol, phase, directory, deadline, progress, *, prompt_factory):
        assert math.isinf(deadline)
        assert protocol[phase] == budgets
        assert prompt_factory is prompt
        assert not (directory / "attempt.json").exists()
        write(directory / "attempt.json", {"cell_id": cell["cell_id"]})
        result = execute(int(directory.name))
        result.update(cell_id=cell["cell_id"], elapsed_s=1)
        write(directory / "result.json", result)
        return result

    def safe_collect(root, cells):
        assert not any((root / "sessions" / f"{i:03d}/attempt.json").exists() for i in range(3, 9))
        return collect(root, cells)

    return SimpleNamespace(
        read=read,
        write=write,
        digest=digest,
        surface=lambda _: {},
        collect=safe_collect,
        run_session=session,
        prompt=prompt,
    )


def test_parallel_assigns_each_unattempted_session_once_and_drains(tmp_path):
    barrier = threading.Barrier(3)
    calls = []
    active = 0
    maximum = 0
    lock = threading.Lock()

    def execute(index):
        nonlocal active, maximum
        with lock:
            calls.append(index)
            active += 1
            maximum = max(maximum, active)
        if index <= 5:
            barrier.wait(timeout=3)
        with lock:
            active -= 1
        return {"status": "completed", "failure": None}

    runner = fixture_runner(tmp_path, execute)
    original = {
        p: p.read_bytes() for p in tmp_path.rglob("*.json") if p.name != "parallel_schedule.json"
    }
    run_parallel(tmp_path, runner, 3)
    assert sorted(calls) == list(range(3, 9))
    assert maximum == 3 and active == 0
    assert all(p.read_bytes() == content for p, content in original.items())
    assert not (tmp_path / "executor.lock").exists()
    assert not (tmp_path / "sessions/002/result.json").exists()
    state = read(tmp_path / "progress.json")
    assert state["terminal"] == 8 and state["counts"] == {"failed": 2, "completed": 6}
    assert state["active_sessions"] == [] and state["unstarted"] == 0


@pytest.mark.parametrize("failure", ["platform_thread_changed", "forbidden_tool_call", "http_429"])
def test_parallel_drains_on_platform_stop_or_rate_limit(tmp_path, failure):
    started = threading.Barrier(3)
    calls = []
    lock = threading.Lock()
    active = set()
    prior_finished = threading.Event()

    def execute(index):
        with lock:
            calls.append(index)
            active.add(index)
        if index <= 5:
            started.wait(timeout=3)
            if index == 3:
                result = {"status": "failed", "failure": failure}
                if failure == "http_429":
                    result["receipts"] = [{"provider_errors": [{"http_status_codes": [429]}]}]
                prior_finished.set()
            else:
                assert prior_finished.wait(timeout=3)
                # Hold successful siblings until the failed receipt is observed by the coordinator.
                import time

                time.sleep(0.05)
                result = {"status": "completed", "failure": None}
        else:
            with lock:
                assert active == {index}
            result = {"status": "completed", "failure": None}
        with lock:
            active.remove(index)
        return result

    runner = fixture_runner(tmp_path, execute)
    run_parallel(tmp_path, runner, 3)
    state = read(tmp_path / "progress.json")
    assert not active and state["active_sessions"] == []
    if failure == "http_429":
        assert sorted(calls) == list(range(3, 9))
        assert state["workers"] == 1 and state["terminal"] == 8
        assert (
            read(tmp_path / "parallel_schedule.json")["concurrency_changes"][0]["reason"]
            == "explicit_http_429"
        )
    else:
        assert sorted(calls) == [3, 4, 5]
        assert state["unstarted"] == 3 and state["terminal"] == 5
        assert state["stop_reason"] == failure
        assert not (tmp_path / "sessions/006").exists()
