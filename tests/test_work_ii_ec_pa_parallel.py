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
    # The retained failed row remains immutable while its recovery is active.
    assert parallel.next_units(rows, {rows[89]["unit_id"]}, 4) == []


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
    assert progress["completed_sources"] == 1


def test_progress_separates_completion_failure_and_active_recovery():
    rows = [{"unit_id": "ok", "status": "completed"}, {"unit_id": "bad", "status": "failed"}]
    assert parallel.source_counts(rows, {}) == {
        "completed_sources": 1,
        "failed_sources": 1,
        "terminal_sources": 2,
    }
    assert parallel.source_counts(rows, {"bad": {}}) == {
        "completed_sources": 1,
        "failed_sources": 0,
        "terminal_sources": 1,
    }


def test_resume_refuses_unknown_stop_and_second_recovery(tmp_path):
    import json

    unit = matrix.units()[0]
    _, actual = parallel.unit_paths(tmp_path, unit)
    original = {
        "status": "failed",
        "source_status": "failed",
        "operations": 7,
        "batches": [{}],
        "exact_replay": {"verified": True},
    }
    parallel.write(actual / "result.json", original)
    (actual / "source-stdout.jsonl").write_text(
        json.dumps({"type": "error", "message": "network error"}), encoding="utf-8"
    )
    state = {
        "status": "stopped",
        "failure": {"unit": unit["unit_id"]},
        "results": [{**unit, **original}],
    }
    before = deepcopy(state)
    assert parallel.resume_recoveries(tmp_path, state, allow_partial=True) == state["results"]
    assert state == before
    with pytest.raises(ValueError, match="eligible"):
        parallel.resume_recoveries(tmp_path, state, allow_partial=False)
    (tmp_path / "recoveries" / unit["unit_id"] / "attempt-1").mkdir(parents=True)
    with pytest.raises(ValueError, match="already exists"):
        parallel.resume_recoveries(tmp_path, state, allow_partial=True)


def test_recovery_worker_preserves_original_and_uses_saved_design(tmp_path, monkeypatch):
    import json

    root, report = tmp_path / "raw", tmp_path / "report"
    unit = matrix.units()[0]
    folder, actual = parallel.unit_paths(root, unit)
    parallel.write(root / "design.json", {})
    ref = root / "references" / unit["world"]["world_id"]
    parallel.write(ref / "design.json", {})
    parallel.write(ref / "reference-result.json", {"truth": {}})
    design = {"saved": "original source questions"}
    parallel.write(folder / "design.json", design)
    original = {
        "status": "failed",
        "source_status": "failed",
        "operations": 7,
        "batches": [{}],
        "exact_replay": {"verified": True},
    }
    parallel.write(actual / "result.json", original)
    (actual / "source-stdout.jsonl").write_text(
        json.dumps({"type": "error", "message": "network error"}), encoding="utf-8"
    )
    calls = []

    def recover(*args, **kwargs):
        calls.append((args[5], kwargs))
        path = root / "recoveries/result.json"
        parallel.write(path, {"failure": None})
        return {
            "result_path": str(path),
            "row": {"status": "completed", "operations": 84, "exact_replay": {"verified": True}},
        }

    monkeypatch.setattr(parallel, "recover", recover)
    monkeypatch.setattr(parallel.ec, "run_cell", lambda *a, **k: pytest.fail("duplicate source"))
    parallel.run_unit(root, report, unit, recovery_only=True, allow_partial=True)
    assert calls == [(design, {"allow_partial": True})]
    assert parallel.read(actual / "result.json") == original
    assert parallel.read(folder / "worker-progress.json")["stop_reason"] is None


@pytest.mark.parametrize("recovery_fails", [False, True])
@pytest.mark.parametrize("recovery_attempt", [1, 2, 3])
def test_four_worker_resume_and_drain_use_single_coordinator(
    tmp_path, monkeypatch, recovery_fails, recovery_attempt
):
    import json

    root, report = tmp_path / "raw", tmp_path / "report"
    plan = matrix.units()[:6]
    failed = {
        **plan[0],
        "status": "failed",
        "source_status": "failed",
        "operations": 7,
        "batches": [{}],
        "exact_replay": {"verified": True},
    }
    _, actual = parallel.unit_paths(root, plan[0])
    parallel.write(actual / "result.json", failed)
    (actual / "source-stdout.jsonl").write_text(
        json.dumps({"type": "error", "message": "network error"}), encoding="utf-8"
    )
    for number in range(1, recovery_attempt):
        previous = root / "recoveries" / plan[0]["unit_id"] / f"attempt-{number}"
        parallel.write(previous / "result.json", failed)
        parallel.write(
            previous / "recovery.json",
            {
                "kind": "fresh_source",
                "result_path": str(previous / "result.json"),
            },
        )
        (previous / "source-stdout.jsonl").write_text(
            json.dumps({"type": "error", "message": "network error"}), encoding="utf-8"
        )
    parallel.write(root / "design.json", {"units": plan})
    parallel.write(
        root / "summary.json",
        {
            "status": "stopped",
            "failure": {"unit": plan[0]["unit_id"]},
            "results": [failed] + [{**u, "status": "not_started"} for u in plan[1:]],
        },
    )
    live, launched, snapshots = set(), [], []
    peak = 0

    class Process:
        def __init__(self, command, **kwargs):
            nonlocal peak
            self.uid = command[command.index("--unit") + 1]
            self.pid = 100 + len(launched)
            self.polls = 0
            launched.append((self.uid, command))
            live.add(self.uid)
            peak = max(peak, len(live))
            unit = next(u for u in plan if u["unit_id"] == self.uid)
            folder, actual = parallel.unit_paths(root, unit)
            if not (actual / "result.json").exists():
                parallel.write(actual / "result.json", {})
            parallel.write(
                folder / "worker-progress.json",
                {
                    "unit": self.uid,
                    "stage": "terminal",
                    "stop_reason": "infrastructure recovery failed"
                    if recovery_fails and self.uid == plan[0]["unit_id"]
                    else None,
                },
            )

        def poll(self):
            self.polls += 1
            if self.polls == 1:
                return None
            live.discard(self.uid)
            return 0

    def collect(root, unit):
        return {**unit, "status": "failed" if recovery_fails and unit == plan[0] else "completed"}

    def save(root, report, state, progress, **kwargs):
        snapshots.append(deepcopy(progress))
        parallel.write(root / "summary.json", state)

    monkeypatch.setattr(parallel.subprocess, "Popen", Process)
    monkeypatch.setattr(parallel, "collect", collect)
    monkeypatch.setattr(parallel.time, "sleep", lambda _: None)
    monkeypatch.setattr(parallel.matrix, "save_matrix_state", save)
    parallel.coordinate(
        root,
        report,
        workers=4,
        resume=True,
        allow_partial=True,
        recovery_attempt=recovery_attempt if recovery_attempt < 3 else 1,
        next_recovery=recovery_attempt == 3,
    )
    assert peak == 4
    assert "--recover-unit" in launched[0][1]
    command = launched[0][1]
    assert command[command.index("--recovery-attempt") + 1] == str(recovery_attempt)
    assert all("--recovery-attempt" not in command for _, command in launched[1:])
    assert all("--retry-partial-network" in command for _, command in launched)
    assert [uid for uid, _ in launched] == [u["unit_id"] for u in plan[: len(launched)]]
    assert len(launched) == (4 if recovery_fails else 6)
    assert not live
    assert snapshots[-1]["completed_sources"] == (3 if recovery_fails else 6)
    if recovery_fails:
        assert snapshots[-1]["stage"] == "stopped"
        assert snapshots[-1]["eta_s"] is None
        assert any(s["stage"] == "draining_after_failure" for s in snapshots)
    else:
        assert snapshots[-1]["stage"] == "completed"


@pytest.mark.parametrize("new_budget", [False, True])
def test_real_worker_entry_routes_pa_without_precreating_root(tmp_path, monkeypatch, new_budget):
    root, report = tmp_path / "raw", tmp_path / "report"
    unit = next(u for u in matrix.units() if u["system"] == "PA" and u["budget"] == 24)
    budget = parallel.pa.FOLLOWUP_NUMERICS if new_budget else None
    questions = {"posttest_numerics": budget.to_dict()} if budget is not None else {}
    parallel.write(root / "design.json", {"units": [unit], "questions": {"PA": questions}})
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
        {
            "arm": unit["arm"],
            "batches": 24,
            "world": unit["world"],
            "reference_run": ref,
            "numerics_budget": budget,
        }
    ]
    final = parallel.read(root / "sources" / unit["unit_id"] / "worker-progress.json")
    assert final["stage"] == "terminal" and final["stop_reason"] is None


def test_second_recovery_worker_preserves_history_and_aggregates_each_attempt_once(
    tmp_path, monkeypatch
):
    import json

    root, report = tmp_path / "raw", tmp_path / "report"
    report.mkdir()
    unit = matrix.units()[0]
    parent, actual = parallel.unit_paths(root, unit)
    design = {
        "system": "unchanged system",
        "goal": "unchanged goal",
        **{s: s for s in ("K1", "Q", "K2")},
    }
    parallel.write(root / "design.json", {})
    parallel.write(parent / "design.json", design)
    ref = root / "references" / unit["world"]["world_id"]
    parallel.write(ref / "design.json", {})
    parallel.write(ref / "reference-result.json", {"truth": {}})
    batches = [{"lifecycle_index": i, "metrics": {}} for i in range(12)]
    original = {
        "status": "failed",
        "source_status": "failed",
        "operations": 14,
        "batches": batches[:2],
        "exact_replay": {"verified": True},
        "posttests": {},
    }
    parallel.write(actual / "result.json", original)
    previous = root / "recoveries" / unit["unit_id"] / "attempt-1"
    failed = {**original, "operations": 0, "batches": []}
    parallel.write(previous / "result.json", failed)
    (previous / "source-stdout.jsonl").write_text(
        json.dumps({"type": "error", "message": "network error"}), encoding="utf-8"
    )
    record = {
        "kind": "fresh_source",
        "attempt": 1,
        "result_path": str(previous / "result.json"),
        "row": matrix.source_row(unit, failed),
        "new_source_attempts": 1,
        "new_source_batches": 0,
        "new_source_operations": 0,
        "new_posttest_attempts": 0,
        "report_path": "first/REPORT.md",
    }
    parallel.write(previous / "recovery.json", record)
    before = {
        p: p.read_bytes()
        for p in (actual / "result.json", previous / "result.json", previous / "recovery.json")
    }
    calls = []

    def run_cell(output, goal, locus, arm, truth, progress):
        assert parallel.read(output / "design.json") == design
        calls.append(output)
        result = {
            **original,
            "status": "completed",
            "source_status": "completed",
            "operations": 84,
            "batches": batches,
            "failure": None,
        }
        parallel.write(output / f"{goal}-{locus}-{arm}" / "result.json", result)
        return result

    monkeypatch.setattr(parallel.ec, "run_cell", run_cell)
    parallel.run_unit(
        root, report, unit, recovery_only=True, allow_partial=True, recovery_attempt=2
    )
    assert calls == [previous.parent / "attempt-2"]
    assert all(p.read_bytes() == content for p, content in before.items())
    row = parallel.collect(root, unit)
    assert row["status"] == "failed" and row["recovery_history"] == [record]
    assert parallel.effective_row(row)["completed_batches"] == 12
    assert row["network_recovery"]["attempt"] == 2
    state = {"status": "completed", "results": [row], "references": {}}
    matrix.save_matrix_state(root, report, state, {}, elapsed_s=1)
    assert state["retries"] == state["additional_source_attempts"] == 2
    assert state["source_batches"] == 14 and state["effective_source_batches"] == 12
    assert state["completed_sources"] == 1 and state["first_attempt_completed_sources"] == 0
    assert "network-recovery-2/REPORT.md" in (report / "REPORT.md").read_text(encoding="utf-8")
