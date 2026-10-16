"""Fixed coverage, bounded launch commands and failure-aware accounting."""

from collections import Counter

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
