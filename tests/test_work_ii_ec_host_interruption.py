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


def test_seals_intact_partial_prefix_and_preserves_original_files(tmp_path, monkeypatch):
    folder, home, unit = fixture(tmp_path)
    before = (folder / "trajectory.jsonl").read_bytes()
    calls = []

    def replay(records, label, **kwargs):
        calls.append((len(records), kwargs))
        return {"verified": True, "checked_steps": len(records), "max_abs_error": 0}

    monkeypatch.setattr(host.ec, "replay_with_progress", replay)
    monkeypatch.setattr(host.ec, "summaries", lambda records: [])
    result = host.seal(unit, folder, home, reboot_time="2026-09-19T01:01:00+00:00")
    assert result["source_status"] == "interrupted"
    assert result["operations"] == 1 and result["posttests"] == {}
    assert result["interruption"]["last_reported_thread_usage"] is None
    assert result["interruption"]["token_accounting_complete"] is False
    assert (folder / "trajectory.jsonl").read_bytes() == before
    assert (folder / "workspace/marker").read_text() == "preserved public workspace"
    assert not (folder / "source-receipts.json").exists()
    assert host.seal(unit, folder, home, reboot_time="2026-09-19T01:01:00+00:00") == result
    assert calls == [(1, {"world_interventions": []})]


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
