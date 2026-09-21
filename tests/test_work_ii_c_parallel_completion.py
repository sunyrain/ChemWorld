"""Isolated-cell selection and single-owner retry scheduling for C continuation."""

import json
from copy import deepcopy

import pytest
from scripts import parallel_work_ii_c_completion as parallel


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_select_repairs_before_new_sources_preserving_terminal_outcomes(tmp_path):
    cells = [{"id": f"C-{i}"} for i in range(6)]
    save(tmp_path / "design.json", {"schedule": cells})
    for i, result in {
        0: {"status": "completed"},
        1: {"status": "failed", "failure": {"stage": "source", "message": "budget exhausted"}},
        3: {
            "status": "failed",
            "failure": {"stage": "Q", "message": "provider_failure"},
            "source": {"exact_replay": {"verified": True}},
        },
        4: {"status": "failed", "failure": {"stage": "K2", "message": "bad answer"}},
    }.items():
        save(tmp_path / "sources" / cells[i]["id"] / "result.json", result)
    folder = tmp_path / "sources/C-3/Q"
    save(folder / "receipt.json", {"payload": None})
    save(folder / "stdout.jsonl", {"type": "error", "message": "idle timeout waiting for SSE"})
    assert [(j["cell"]["id"], j["kind"]) for j in parallel.pending_jobs(tmp_path)] == [
        ("C-3", "repair"),
        ("C-2", "source"),
        ("C-5", "source"),
    ]


def test_no_takeover_of_running_or_unsealed_source(tmp_path):
    save(tmp_path / "design.json", {"schedule": [{"id": "C-0"}]})
    folder = tmp_path / "sources/C-0"
    folder.mkdir(parents=True)
    with pytest.raises(ValueError, match="Unsealed"):
        parallel.pending_jobs(tmp_path)
    save(folder / "result.json", {"status": "running"})
    with pytest.raises(ValueError, match="running"):
        parallel.pending_jobs(tmp_path)


def test_capacity_and_backoff_do_not_block_other_independent_cells():
    jobs = [{"cell": {"id": str(i)}, "ready_at": 100 if i == 0 else 0} for i in range(8)]
    queue = deepcopy(jobs)
    selected = parallel.ready_jobs(queue, 4, 10)
    assert [j["cell"]["id"] for j in selected] == ["1", "2", "3", "4"]
    assert [j["cell"]["id"] for j in queue] == ["0", "5", "6", "7"]
    assert parallel.ready_jobs(queue, 0, 200) == []
    selected += parallel.ready_jobs(queue, 4, 200)
    assert len({j["cell"]["id"] for j in selected}) == 8
    assert not queue


def test_coordinator_archives_and_charges_failed_source_once(tmp_path, monkeypatch):
    folder = tmp_path / "sources/C-0"
    result = {
        "status": "failed",
        "failure": {"stage": "source"},
        "posttests": {},
        "source": {"operations": 7, "batches": [], "exact_replay": {"verified": True}},
    }
    save(folder / "result.json", result)
    save(folder / "source-stdout.jsonl", {"type": "error", "message": "network error"})
    save(
        tmp_path / "prior-attempt.json",
        {"operations": 20, "final_assays": 2, "provider_sources": 1},
    )
    monkeypatch.setattr(parallel.time, "time", lambda: 1000)
    job = {"cell": {"id": "C-0"}, "kind": "source", "failures": 0, "ready_at": 0}
    assert parallel.source_retry(tmp_path, job, result)
    assert job["failures"] == 1 and job["ready_at"] == 1060
    prior = parallel.read(tmp_path / "prior-attempt.json")
    assert (prior["operations"], prior["provider_sources"]) == (27, 2)
    assert parallel.source_retry(tmp_path, job, result) is False
    assert parallel.read(tmp_path / "prior-attempt.json") == prior


def test_worker_uses_isolated_posttest_wrapper_and_restores_binding(tmp_path, monkeypatch):
    job_path = tmp_path / "worker/job.json"
    save(job_path, {"cell": {"id": "C-0"}, "kind": "source"})
    monkeypatch.setattr(parallel.formal, "verify_frozen", lambda root: None)
    original = parallel.formal.pilot.posttest
    seen = []

    def source(root, cell, progress):
        assert parallel.formal.pilot.posttest is not original
        seen.append(cell["id"])
        progress.update(operations=12, batches=1, phase="K2")
        return {}

    monkeypatch.setattr(parallel.formal, "source", source)
    parallel.worker(tmp_path, job_path, "http://127.0.0.1:7890")
    assert seen == ["C-0"]
    assert parallel.formal.pilot.posttest is original
    status = parallel.read(job_path.parent / "status.json")
    assert status["activity"] == "finished" and status["operations"] == 12
