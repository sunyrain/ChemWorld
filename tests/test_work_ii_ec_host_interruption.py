"""Host recovery preserves interrupted data and refuses completed/wrong-session sources."""

import json

import pytest
from scripts import seal_work_ii_ec_host_interruption as host


def fixture(tmp_path):
    folder, home = tmp_path / "source", tmp_path / "retained-home"
    folder.mkdir()
    sessions = home / "codex-home/sessions"
    sessions.mkdir(parents=True)
    (home / "laboratory").mkdir()
    (home / "laboratory/marker").write_text("preserved public workspace")
    record = {
        "step": 1,
        "action": {"operation": "add_reagent", "amount_mol": 0.01},
        "timestamp": "2026-09-19T01:00:10+00:00",
        "transaction_status": "committed",
    }
    (folder / "trajectory.jsonl").write_text(json.dumps(record) + "\n")
    (folder / "source-stdout.jsonl").write_text(
        json.dumps({"type": "thread.started", "thread_id": "original"}) + "\n"
    )
    (sessions / "rollout-original.jsonl").write_text(
        json.dumps({"type": "session_meta", "payload": {"id": "original"}}) + "\n"
    )
    host.write(folder / "attempt.json", {"started_epoch": 1789779600})
    unit = {
        "system": "EC",
        "unit_id": "test",
        "goal": "discovery",
        "locus": "E",
        "arm": "Opaque",
        "budget": 24,
        "world": {"world_id": "EC-W01", "world_interventions": []},
    }
    return folder, home, unit


@pytest.mark.parametrize("classification", ["host_reboot", "process_exit"])
def test_seals_intact_partial_prefix_and_preserves_original_files(
    tmp_path, monkeypatch, classification
):
    folder, home, unit = fixture(tmp_path)
    before = (folder / "trajectory.jsonl").read_bytes()
    calls = []

    def replay(records, label, **kwargs):
        calls.append((len(records), kwargs))
        return {"verified": True, "checked_steps": len(records), "max_abs_error": 0}

    monkeypatch.setattr(host.ec, "replay_with_progress", replay)
    monkeypatch.setattr(host.ec, "summaries", lambda records: [])
    result = host.seal(
        unit,
        folder,
        home,
        reboot_time="2026-09-19T01:01:00+00:00",
        classification=classification,
    )
    assert result["source_status"] == "interrupted"
    assert result["operations"] == 1 and result["posttests"] == {}
    assert result["interruption"]["last_reported_thread_usage"] is None
    assert result["interruption"]["token_accounting_complete"] is False
    assert (folder / "trajectory.jsonl").read_bytes() == before
    assert (folder / "workspace/marker").read_text() == "preserved public workspace"
    assert not (folder / "source-receipts.json").exists()
    assert (
        host.seal(
            unit,
            folder,
            home,
            reboot_time="2026-09-19T01:01:00+00:00",
            classification=classification,
        )
        == result
    )
    assert calls == [(1, {"world_interventions": []})]
    if classification == "process_exit":
        from scripts.recover_work_ii_ec_pa_network import recovery_kind

        assert recovery_kind(unit, result, folder, allow_partial=True) == (
            "fresh_source_after_process_interruption"
        )


def test_wrong_retained_thread_cannot_be_used(tmp_path):
    folder, home, _ = fixture(tmp_path)
    (home / "codex-home/sessions/rollout-original.jsonl").write_text(
        json.dumps({"type": "session_meta", "payload": {"id": "different"}})
    )
    with pytest.raises(ValueError, match="identity mismatch"):
        host.inspect_interruption(folder, home)


def test_completed_provider_turn_is_not_relabelled_as_interrupted(tmp_path):
    folder, home, _ = fixture(tmp_path)
    with (folder / "source-stdout.jsonl").open("a") as handle:
        handle.write(json.dumps({"type": "turn.completed"}) + "\n")
    with pytest.raises(ValueError, match="nonterminal"):
        host.inspect_interruption(folder, home)


def test_failed_replay_cannot_authorize_replacement(tmp_path, monkeypatch):
    folder, home, unit = fixture(tmp_path)
    monkeypatch.setattr(host.ec, "replay_with_progress", lambda *a, **k: {"verified": False})
    with pytest.raises(RuntimeError, match="replay exactly"):
        host.seal(unit, folder, home, reboot_time="2026-09-19T01:01:00+00:00")
    assert not (folder / "result.json").exists()


def test_seal_process_lost_posttest_preserves_physics_and_answers(tmp_path, monkeypatch):
    from scripts import reconcile_work_ii_ec_process_exit as process
    from scripts.recover_work_ii_ec_pa_network import recovery_kind

    folder, home, unit = fixture(tmp_path)
    original = {
        "status": "failed",
        "source_status": "completed",
        "operations": 1,
        "exact_replay": {"verified": True},
        "posttests": {"K1": {"payload": {"report": "sealed K1"}}},
        "batches": [{"lifecycle_index": 1, "actions": [{"operation": "terminate"}]}],
        "recommendation": {"selected_experiment_index": 1},
    }
    host.write(folder / "result.json", original)
    host.write(folder / "source-receipts.json", [{"thread_id": "original"}])
    (folder / "Q").mkdir()
    (folder / "Q/stdout.jsonl").write_text(json.dumps({"type": "turn.started"}) + "\n")
    calls = []

    def retest(path, actions, **kwargs):
        calls.append((actions, kwargs))
        return {"exact_replay": {"verified": True}, "batches": [{}]}

    monkeypatch.setattr(process.ec, "reference_run", retest)
    result = process.seal_posttests(unit, folder, home, "original")
    assert result["source_status"] == "completed" and result["operations"] == 1
    assert result["posttests"]["K1"] == original["posttests"]["K1"]
    assert result["posttests"]["Q"]["failure"] == "process_interrupted"
    assert host.read(folder / "result-before-process-interruption.json") == original
    assert recovery_kind(unit, result, folder) == "posttests"
    assert process.seal_posttests(unit, folder, home, "original") == result
    assert len(calls) == 1 and calls[0][0] == original["batches"][0]["actions"]
    assert calls[0][1]["observation_seed"] == 101
