"""Coverage, truth separation, retained failures, and world-level replication inference."""

from copy import deepcopy

import pytest
from scripts import run_work_ii_factorial_replication as runner
from scripts.run_work_ii_factorial import read, seal

from chemworld.eval.work_ii_factorial import CONDITIONS, TASKS, compile_design, score_slots
from chemworld.eval.work_ii_factorial_replication import (
    replication_protocol,
    source_schedule,
    summarize_factorial,
)


def test_new_worlds_balanced_nested_schedule_and_exact_denominators():
    protocol = replication_protocol()
    assert read(runner.PROTOCOL) == protocol
    worlds, schedule = protocol["worlds"], source_schedule(protocol)
    assert len(worlds) == len({world["world_seed"] for world in worlds}) == 10
    assert not set(range(5)) & {world["world_seed"] for world in worlds}
    assert len(schedule) == len({state["state_id"] for state in schedule}) == 40
    assert len(schedule) * 3 == protocol["provider_call_opportunities"] == 120
    assert len(schedule) * 4 == protocol["condition_slots"] == 160
    assert len(worlds) * (len(protocol["evidence_xy"]) + len(protocol["candidate_xy"])) == 200
    for world in worlds:
        for model in ("deepseek", "gpt"):
            nested = [
                row
                for row in schedule
                if row["cluster_id"] == world["cluster_id"] and row["model"] == model
            ]
            assert sorted(row["decision_order"][0] for row in nested) == ["F", "L"]
    assert source_schedule(protocol) == schedule


def setup_packets(tmp_path, monkeypatch, *, physical_failure=False):
    protocol = replication_protocol()
    monkeypatch.setattr(runner, "check_frozen", lambda root: protocol)
    seal(tmp_path / "protocol.json", protocol)
    seal(
        tmp_path / "physical.json",
        {
            "status": "failed" if physical_failure else "completed",
            "stop_reason": "physical_or_replay_failure" if physical_failure else None,
            "completed": 0 if physical_failure else 200,
            "receipts": [],
        },
    )
    seal(tmp_path / "release.json", {"tested_commit": "fixture", "execution_surface": {}})
    if not physical_failure:
        for world in protocol["worlds"]:
            packet = compile_design(protocol, world["task"])
            for row in packet["evidence"]:
                row["score"] = 0.2 + 0.1 * row["xy"][0]
            seal(tmp_path / "public" / f"{world['cluster_id']}.json", packet)
    return protocol


def test_failed_sources_keep_fitted_conditions_and_never_read_truth(tmp_path, monkeypatch):
    protocol = setup_packets(tmp_path, monkeypatch)
    attempted = []

    def fake_provider(root, call_id, model, stage, packet, law, progress, completed, **kwargs):
        attempted.append(call_id)
        assert kwargs["provider_override"] == protocol["providers"][model]
        assert kwargs["total"] == 120
        return {
            "call_id": call_id,
            "thread_id": call_id,
            "usage": {},
            "status": "schema_failed" if stage == "source" else "completed",
            "final_payload": {} if stage == "source" else {"candidate_id": "c01"},
        }

    monkeypatch.setattr(runner, "provider_call", fake_provider)
    result = runner.run_provider_block(tmp_path)  # no private scores exist
    assert len(result["slots"]) == 160
    assert len(result["calls"]) == 120
    assert len(attempted) == 80
    assert sum(row["status"] == "completed" for row in result["slots"]) == 80
    assert all(
        row["status"] == "completed" for row in result["slots"] if row["condition"].startswith("F")
    )
    assert runner.run_provider_block(tmp_path) == result
    assert len(attempted) == 80


@pytest.mark.parametrize("violation", ["reused", "tool", "identity"])
def test_protocol_violation_stops_remaining_calls_preserving_slots(
    tmp_path, monkeypatch, violation
):
    setup_packets(tmp_path, monkeypatch)
    attempted = []

    def fake_provider(root, call_id, model, stage, packet, law, progress, completed, **kwargs):
        attempted.append(call_id)
        return {
            "call_id": call_id,
            "thread_id": None if violation == "identity" else "same",
            "tool_event_count": int(violation == "tool"),
            "usage": {},
            "status": "completed",
            "final_payload": {"coefficients": [0.2, 0.1, 0, 0, 0, 0]}
            if stage == "source"
            else {"candidate_id": "c01"},
        }

    monkeypatch.setattr(runner, "provider_call", fake_provider)
    result = runner.run_provider_block(tmp_path)
    assert result["stop_reason"]
    assert len(attempted) == (2 if violation == "reused" else 1)
    assert len(result["slots"]) == 160 and len(result["calls"]) == 120


def test_physical_failure_produces_full_stopped_report_without_provider(tmp_path, monkeypatch):
    setup_packets(tmp_path, monkeypatch, physical_failure=True)
    monkeypatch.setattr(runner, "provider_call", lambda *a, **k: pytest.fail("provider launched"))
    runner.run_provider_block(tmp_path)
    report = runner.analyze(tmp_path)
    assert not report["execution_valid"] and not report["formal_result"]
    assert report["statistics"] is None
    assert report["provider_attempted"] == 0
    assert report["provider_opportunities"] == 120
    assert report["condition_scheduled"] == 160
    assert len(report["failures"]) == 280  # all provider and condition slots retained


def test_full_analysis_reads_truth_only_after_selections_and_retains_numeric_failures(
    tmp_path, monkeypatch
):
    protocol = setup_packets(tmp_path, monkeypatch)

    def fake_provider(root, call_id, model, stage, packet, law, progress, completed, **kwargs):
        return {
            "call_id": call_id,
            "thread_id": call_id,
            "usage": {"input_tokens": 10},
            "status": "completed",
            "final_payload": {"coefficients": [1e308] * 6}
            if stage == "source"
            else {"candidate_id": "c01"},
        }

    monkeypatch.setattr(runner, "provider_call", fake_provider)
    runner.run_provider_block(tmp_path)
    truth = {
        world["cluster_id"]: {f"c{index + 1:02d}": 0.2 + 0.01 * index for index in range(8)}
        for world in protocol["worlds"]
    }
    seal(tmp_path / "private_scores.json", truth)
    report = runner.analyze(tmp_path)
    assert report["execution_valid"]
    assert report["provider_completed"] == 120
    assert report["condition_completed"] == 120  # L-X overflows in all 40 states
    assert len(report["failures"]) == 40
    assert len(report["artifact_metrics"]) == 80
    assert all(
        row["candidate_mae"] is None for row in report["artifact_metrics"] if row["artifact"] == "L"
    )
    assert report["provider_usage"]["input_tokens"] == 1200
    assert runner.analyze(tmp_path) == report


def scored_fixture(protocol):
    rows = []
    for state in source_schedule(protocol):
        effect = 0.1 if state["task"] == TASKS[0] else 0.3
        slots = [
            {
                **{
                    key: state[key] for key in ("state_id", "cluster_id", "task", "model", "repeat")
                },
                "condition": condition,
                "status": "completed",
                "candidate_id": "fit" if condition.startswith("F") else "law",
            }
            for condition in CONDITIONS
        ]
        rows.extend(score_slots(slots, {"fit": 0.8, "law": 0.8 - effect}))
    return rows


def test_world_task_weighting_and_nested_repeat_duplication_do_not_change_inference():
    protocol = replication_protocol()
    result = summarize_factorial(scored_fixture(protocol), protocol)
    primary = result["contrasts"][0]
    assert primary["world_clusters"] == 10
    assert primary["mean_difference"] == pytest.approx(-0.2)
    assert primary["interval"] == pytest.approx([-0.2, -0.2])
    assert primary["task_means"][TASKS[0]] == pytest.approx(-0.1)
    assert result["primary_material_benefit_supported"]
    repeated = deepcopy(protocol)
    repeated["model_repeats"] = 4
    second = summarize_factorial(scored_fixture(repeated), repeated)
    assert result["contrasts"] == second["contrasts"]
    with pytest.raises(ValueError, match="denominator"):
        summarize_factorial(scored_fixture(protocol)[:-1], protocol)
    rows = scored_fixture(protocol)
    rows[0]["cluster_id"] = "incorrect-world"
    with pytest.raises(ValueError, match="metadata"):
        summarize_factorial(rows, protocol)


def test_missing_output_keeps_primary_and_completed_only_denominators_distinct():
    protocol = replication_protocol()
    rows = scored_fixture(protocol)
    failed = next(row for row in rows if row["condition"] == "L-X")
    failed.update(
        status="blocked", raw_regret=None, failure_aware_regret=1.0, near_optimal=False, top1=False
    )
    result = summarize_factorial(rows, protocol)
    world = next(
        row
        for row in result["world_contrasts"]
        if row["cluster_id"] == failed["cluster_id"] and row["contrast"] == "F-X_minus_L-X"
    )
    assert world["nested_state_count"] == 4
    assert world["completed_pair_count"] == 3
    assert world["completed_only_difference"] > world["mean_difference"]
