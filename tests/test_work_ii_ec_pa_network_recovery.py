"""Recovery cannot repeat intact physics or retry scientific outcomes."""

import json
from copy import deepcopy

import pytest
from scripts import recover_work_ii_ec_pa_network as recovery
from scripts import run_work_ii_ec_pa_matrix as matrix


def failed_event(path, message="Transport error: network error: error decoding response body"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"type": "error", "message": message}) + "\n", encoding="utf-8")


@pytest.mark.parametrize("system", ["EC", "PA"])
def test_only_zero_action_source_may_start_fresh(tmp_path, system):
    unit = {"system": system}
    source = {"operations": 0, "status": "failed"}
    result = (
        {"status": "failed", **source}
        if system == "EC"
        else {
            "status": "failed",
            "source": source,
        }
    )
    failed_event(recovery.source_folder(unit, tmp_path) / "source-stdout.jsonl")
    assert recovery.recovery_kind(unit, result, tmp_path) == "fresh_source"
    if system == "EC":
        result["operations"] = 1
    else:
        source["operations"] = 1
    assert recovery.recovery_kind(unit, result, tmp_path) is None


@pytest.mark.parametrize("message", ["quota exceeded", "network error HTTP 429", "unauthorized"])
def test_non_network_or_quota_error_is_not_retried(tmp_path, message):
    path = tmp_path / "events.jsonl"
    failed_event(path, message)
    assert not recovery.network_failure(path)


def test_scientific_text_is_not_a_network_failure(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(json.dumps({"type": "item.completed", "text": "network error"}))
    assert not recovery.network_failure(path)


@pytest.mark.parametrize("reply_thread", ["original-thread", "wrong-thread"])
def test_posttest_restore_uses_same_thread_and_skips_sealed_stages(
    tmp_path, monkeypatch, reply_thread
):
    unit = {"system": "EC", "unit_id": "test"}
    folder, output = tmp_path / "original", tmp_path / "recovery"
    (folder / "provider-rollouts").mkdir(parents=True)
    (folder / "provider-rollouts" / "saved.jsonl").write_text("preserved context")
    output.mkdir()
    recovery.write(folder / "source-receipts.json", [{"thread_id": "original-thread"}])
    failed_event(folder / "Q" / "stdout.jsonl")
    original = {
        "status": "failed",
        "source_status": "completed",
        "operations": 84,
        "exact_replay": {"verified": True},
        "elapsed_s": 20,
        "recommendation_retest": {"retained": True},
        "failure": {"stage": "Q", "message": "provider_failure"},
        "posttests": {
            "K1": {"payload": {"report": "sealed mechanism"}, "failure": None},
            "Q": {"payload": None, "failure": "provider_failure"},
        },
    }
    snapshot = deepcopy(original)
    assert recovery.recovery_kind(unit, original, folder) == "posttests"
    calls = []

    def prepare(home, provider):
        (home / "codex-home").mkdir()
        return {"testing": True}

    def posttest(agent, out, stage, thread, progress, *, design):
        assert (
            agent.home_root / "codex-home/sessions/saved.jsonl"
        ).read_text() == "preserved context"
        assert agent.followup_environment == {"testing": True}
        calls.append((stage, thread, design))
        return {"payload": {"report": stage}, "thread_id": reply_thread, "failure": None}

    monkeypatch.setattr(recovery, "_prepare_codex_home", prepare)
    monkeypatch.setattr(recovery.ec, "posttest", posttest)
    monkeypatch.setattr(recovery.ec, "evaluate_predictions", lambda *a, **k: {"valid": True})
    design = {"queries": [], "Q": "unchanged Q", "K2": "unchanged K2"}
    result = recovery.recover_posttests(unit, original, folder, output, design, {}, {})
    expected = [("Q", "original-thread")]
    if reply_thread == "original-thread":
        expected.append(("K2", "original-thread"))
    assert [(s, t) for s, t, _ in calls] == expected
    assert all(d is design for _, _, d in calls)
    assert result["status"] == ("completed" if reply_thread == "original-thread" else "failed")
    if reply_thread != "original-thread":
        assert result["failure"]["message"] == "posttest_thread_changed"
    assert result["recommendation_retest"] == original["recommendation_retest"]
    assert result["operations"] == 84
    assert original == snapshot
    assert (output / "provider-rollouts/saved.jsonl").is_file()


def test_usage_delta_and_first_attempt_are_not_counted_twice():
    before = {
        "valid": True,
        "total": {
            "input": 100,
            "cached_input": 50,
            "output": 10,
            "uncached_input": 50,
            "input_plus_output": 110,
        },
    }
    after = {
        "valid": True,
        "total": {
            "input": 200,
            "cached_input": 80,
            "output": 30,
            "uncached_input": 120,
            "input_plus_output": 230,
        },
    }
    assert recovery.usage_delta(before, after)["tokens"]["input_plus_output"] == 120
    assert recovery.usage_delta({}, after) == {"known": False, "tokens": None}
    original = {"status": "failed", "network_recovery": {"row": {"status": "completed"}}}
    assert recovery.effective_row(original)["status"] == "completed"
    assert original["status"] == "failed"
    assert len(matrix.units()) == 90
