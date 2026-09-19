"""Source ownership, phase scheduling and accounting under two-process execution."""

from copy import deepcopy

import pytest
from scripts import run_work_ii_ec_pa_matrix as matrix
from scripts import run_work_ii_ec_pa_parallel as parallel


def test_dispatch_preserves_order_capacity_and_e_before_ps():
    rows = [{**r, "status": "not_started"} for r in matrix.units(include_ps=True)]
    assert [r["unit_id"] for r in parallel.next_units(rows, set(), 2)] == [
        r["unit_id"] for r in rows[:2]
    ]
    for r in rows[:89]:
        r["status"] = "completed"
    rows[89]["status"] = "running"
    assert parallel.next_units(rows, {rows[89]["unit_id"]}, 1) == []
    rows[89]["status"] = "failed"
    assert parallel.next_units(rows, set(), 2) == rows[90:92]
    assert parallel.next_units(rows, set(), 0) == []


def test_only_empty_handover_reservation_may_be_claimed(tmp_path):
    root = tmp_path / "EC"
    root.mkdir()
    (root / "parallel-handover.json").write_text("{}")
    parallel.prepare_owned_directory(root)
    (root / "design.json").write_text("{}")
    with pytest.raises(RuntimeError, match="duplicate"):
        parallel.prepare_owned_directory(root)


def test_pa_executor_keeps_ownership_of_root_creation(tmp_path):
    root = tmp_path / "sources/PA"
    parallel.prepare_owned_directory(root, system="PA")
    assert root.parent.is_dir() and not root.exists()
    root.mkdir()
    with pytest.raises(RuntimeError, match="duplicate"):
        parallel.prepare_owned_directory(root, system="PA")


def test_handover_cannot_hide_a_real_executor_failure():
    state = {"status": "stopped", "failure": {"message": "reference/replay failure"}}
    before = deepcopy(state)
    with pytest.raises(RuntimeError, match="handover boundary"):
        parallel.accept_handover(state, "reserved")
    assert state == before
    state["failure"] = {"message": "partial source retained; no automatic retry: reserved"}
    parallel.accept_handover(state, "reserved")
    assert state["status"] == "running" and state["failure"] is None
    assert state["runtime_incidents"][0]["scientific_failure"] is False


def test_parallel_report_uses_wall_throughput_and_counts_replacement_cost(tmp_path):
    raw, report = tmp_path / "raw", tmp_path / "report"
    raw.mkdir()
    report.mkdir()
    unit = matrix.units()[9]
    result = {
        **unit,
        "status": "failed",
        "completed_batches": 19,
        "infrastructure_recovery": {
            "kind": "fresh_source_after_host_interruption",
            "row": {
                "status": "completed",
                "completed_batches": 24,
                "posttests_completed": 3,
                "elapsed_s": 1000,
                "english_output": True,
            },
            "new_source_batches": 24,
            "new_source_attempts": 1,
            "new_posttest_attempts": 3,
            "report_path": "host-recovery/REPORT.md",
        },
    }
    state = {
        "status": "running",
        "results": [result],
        "references": {},
        "parallel_execution": {"workers": 2},
        "failure": None,
    }
    progress = {"sources_per_hour": 12, "eta_s": 1234}
    matrix.save_matrix_state(raw, report, state, progress, elapsed_s=300)
    assert progress["sources_per_hour"] == 12 and progress["eta_s"] == 1234
    assert state["source_batches"] == 43 and state["effective_source_batches"] == 24
    assert state["completed_sources"] == 1 and state["planned_sources"] == 1


def test_real_worker_entry_routes_pa_without_precreating_root(tmp_path, monkeypatch):
    root, report = tmp_path / "raw", tmp_path / "report"
    unit = next(u for u in matrix.units() if u["system"] == "PA" and u["budget"] == 24)
    parallel.write(root / "design.json", {"units": [unit]})
    ref = root / "references" / unit["world"]["world_id"]
    parallel.write(ref / "design.json", {})
    parallel.write(ref / "reference-result.json", {"truth": {}})
    calls = []

    def execute(folder, progress, **kwargs):
        assert not folder.exists()
        folder.mkdir()
        calls.append(kwargs)
        parallel.write(folder / "design.json", {})
        parallel.write(
            folder / "result.json",
            {
                "status": "completed",
                "posttests": {},
                "source": {
                    "status": "completed",
                    "operations": 1,
                    "exact_replay": {"verified": True},
                },
            },
        )

    monkeypatch.setattr(parallel.pa, "execute", execute)
    monkeypatch.setattr(parallel.matrix, "export_source", lambda *a, **k: None)
    monkeypatch.setattr(parallel, "recover", lambda *a, **k: None)
    parallel.run_unit(root, report, unit)
    assert calls == [
        {"arm": unit["arm"], "batches": 24, "world": unit["world"], "reference_run": ref}
    ]
    final = parallel.read(root / "sources" / unit["unit_id"] / "worker-progress.json")
    assert final["stage"] == "terminal" and final["stop_reason"] is None
