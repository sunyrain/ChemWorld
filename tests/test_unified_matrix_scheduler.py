"""Fixed coverage, bounded launch commands and failure-aware accounting."""

from collections import Counter

import pytest
from scripts import run_unified_matrices as runner
from scripts.unified_matrix_runtime import WORKER_ENV, bounded_builder, with_thread_limits


def test_production_schedule_covers_300_distinct_units():
    rows = runner.schedule()
    assert len(rows) == 300
    assert len({(r["repeat"], r["id"]) for r in rows}) == 300
    assert Counter(r["system"] for r in rows) == {"EC": 90, "RX": 90, "PA": 45, "P": 45, "C": 30}
    assert Counter(r["matrix"] for r in rows) == {"A": 180, "B": 90, "C": 30}
    assert sum(r["batches"] for r in rows) == 3420
    assert sum(r["batches"] == 0 for r in rows) == 15
    assert {r["system"] for r in rows[:24]} == {"EC", "RX", "PA", "P", "C"}
    for repeat in runner.REPEATS:
        selected = [r for r in rows if r["repeat"] == repeat]
        assert len(selected) == 100
        for system in ("EC", "RX"):
            assert Counter(r["goal"] for r in selected if r["system"] == system) == {
                "discovery": 15,
                "optimization": 15,
            }


def test_thread_limits_reach_all_three_mcp_servers_idempotently():
    command = with_thread_limits(["codex", "exec"])
    assert with_thread_limits(command) == command
    for server in ("chemworld_lab", "research_notebook", "public_numerics"):
        for key, value in WORKER_ENV.items():
            assert f'mcp_servers.{server}.env.{key}="{value}"' in command


def test_failure_keeps_acquired_source_and_does_not_count_invalid_sealed_stage(tmp_path):
    unit = runner.schedule()[0]
    path = runner.folder(tmp_path, unit)
    runner.write(
        path / "status.json", {"status": "execution_error", "failure": "bookkeeping error"}
    )
    runner.write(
        path / "result.json",
        {
            "source": {},
            "posttests": {"K1": {"payload": {"report": "x"}}},
            "posttest_validation": {"K1": {"valid": False}},
        },
    )
    trajectory = path / "participant" / "trajectory.jsonl"
    trajectory.parent.mkdir()
    trajectory.write_text(
        '{"instrument":"final_assay","transaction_status":"committed"}\n', encoding="utf-8"
    )
    row = runner.status_row(tmp_path, unit)
    assert row["completed_batches"] == 1
    assert row["operations"] == 1
    assert row["sealed_posttests"] == 0
    assert row["status"] == "execution_error"


def test_sealed_builder_disables_research_tools_with_valid_transport():
    command = bounded_builder(lambda: ["codex", "exec"])()
    for server in ("chemworld_lab", "research_notebook"):
        assert f"mcp_servers.{server}.enabled=false" in command
        assert any(item.startswith(f"mcp_servers.{server}.command=") for item in command)


def test_eta_requires_completed_chains_not_fast_failures():
    rows = [{"status": "failed", "elapsed_s": 1, "sealed_posttests": 0}]
    assert runner.eta_estimate(rows, 24)["eta_s"] is None


def test_retained_unit_path_and_terminal_result_are_read_without_relaunch(tmp_path):
    unit = runner.schedule()[0]
    old = tmp_path / "original" / unit["repeat"] / unit["id"]
    current = tmp_path / "recovery"
    runner.write(old / "status.json", {"status": "incomplete"})
    runner.write(old / "result.json", {"source": {"batches": [{}] * 12, "operations": 50}})
    runner.write(current / "design.json", {"retained_units": {runner.unit_key(unit): str(old)}})
    before = (old / "result.json").read_bytes()
    assert runner.folder(current, unit) == old
    row = runner.status_row(current, unit)
    assert row["status"] == "incomplete"
    assert row["completed_batches"] == 12
    assert row["operations"] == 50
    with pytest.raises(RuntimeError, match="Retained unit"):
        runner.worker(current, unit)
    assert (old / "result.json").read_bytes() == before


def test_missing_retained_unit_is_never_treated_as_pending(tmp_path):
    unit = runner.schedule()[0]
    runner.write(tmp_path / "prepared.json", {})
    runner.write(
        tmp_path / "design.json",
        {
            "schedule": [unit],
            "workers": 1,
            "retained_units": {runner.unit_key(unit): str(tmp_path / "missing-original")},
        },
    )
    with pytest.raises(RuntimeError, match="Retained unit missing"):
        runner.run(tmp_path)


def test_narrow_mcp_startup_classification_requires_zero_scientific_activity(tmp_path):
    source = tmp_path / "participant"
    source.mkdir()
    stderr = source / "source-stderr.txt"
    stderr.write_text(
        "required MCP servers failed to initialize: research_notebook: "
        "handshaking with MCP server failed: connection closed: initialize response",
        encoding="utf-8",
    )
    result = {"source": {"operations": 0, "batches": []}}
    incident = runner.startup_infrastructure_failure(tmp_path, result)
    assert incident["type"] == "required_mcp_initialization_failed"
    assert incident["zero_scientific_operations"] is True
    assert "message" not in incident
    assert runner.startup_infrastructure_failure(tmp_path, {"source": {"operations": 1}}) is None
    trajectory = source / "trajectory.jsonl"
    trajectory.write_text('{"transaction_status":"committed"}\n', encoding="utf-8")
    assert runner.startup_infrastructure_failure(tmp_path, result) is None
    trajectory.write_text("", encoding="utf-8")
    notes = source / "notebook" / "notebook-calls.jsonl"
    notes.parent.mkdir()
    notes.write_text('{"tool":"notebook_write"}\n', encoding="utf-8")
    assert runner.startup_infrastructure_failure(tmp_path, result) is None


def test_provider_error_alone_is_not_system_startup_defect(tmp_path):
    (tmp_path / "source-stderr.txt").write_text(
        "HTTP 429 too many requests; Codex failed before the next executable operation",
        encoding="utf-8",
    )
    assert runner.startup_infrastructure_failure(tmp_path, {}) is None


def test_normal_startup_probe_never_reads_trajectories(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Normal startup probe read a scientific trajectory")

    monkeypatch.setattr(runner, "live_counts", forbidden)
    assert runner.startup_infrastructure_failure(tmp_path, {}) is None
    (tmp_path / "source-stderr.txt").write_text(
        "MCP servers initialized; ordinary diagnostic output", encoding="utf-8"
    )
    assert runner.startup_infrastructure_failure(tmp_path, {}) is None


def test_operational_hold_added_after_start_prevents_next_launch(tmp_path, monkeypatch):
    unit = runner.schedule()[0]
    runner.write(tmp_path / "prepared.json", {})
    runner.write(tmp_path / "design.json", {"schedule": [unit], "workers": 1})
    original = runner.snapshot
    snapshots = []

    def snapshot(*args, **kwargs):
        value = original(*args, **kwargs)
        if not snapshots:
            runner.write(tmp_path / "block-stop.json", {"systems": [unit["system"]]})
        snapshots.append(value)
        return value

    def no_launch(*args, **kwargs):
        raise AssertionError("Operational hold failed to stop launch")

    monkeypatch.setattr(runner, "snapshot", snapshot)
    monkeypatch.setattr(runner.subprocess, "Popen", no_launch)
    assert runner.run(tmp_path) == 2
    assert snapshots[-1]["blocked_systems"] == [unit["system"]]
    assert not runner.folder(tmp_path, unit).exists()


def test_persisted_worker_failure_keeps_existing_manual_hold(tmp_path):
    path = tmp_path / "block-stop.json"
    runner.write(path, {"systems": ["P"]})
    blocked = {"RX"}
    runner.persist_hold(path, blocked, "zero-operation MCP startup")
    assert runner.read(path)["systems"] == ["P", "RX"]
    assert blocked == {"P", "RX"}
