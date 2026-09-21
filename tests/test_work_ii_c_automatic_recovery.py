"""Exercise automatic recovery without provider calls or scientific resampling."""

import json
import sys
from copy import deepcopy

import pytest
from scripts import resume_work_ii_c_completion as recovery


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def error(path, message="stream disconnected: error sending request for url"):
    save(path, {"type": "error", "message": message})


def source_result(cell="C-test", status="failed"):
    return {
        "id": cell,
        "status": status,
        "failure": {"stage": "source", "message": "provider error"} if status == "failed" else None,
        "posttests": {},
        "source": {
            "operations": 3,
            "batches": [{"ordinal": 1}],
            "exact_replay": {"verified": True},
        },
    }


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"type": "error", "message": "error decoding response body: network error"}, True),
        ({"type": "turn.failed", "error": {"message": "connection reset"}}, True),
        ({"type": "error", "message": "stream disconnected: idle timeout waiting for SSE"}, True),
        ({"type": "error", "message": "error sending request: 401 unauthorized"}, False),
        ({"type": "error", "message": "quota exceeded"}, False),
        ({"type": "error", "message": "turn_timeout"}, False),
        ({"type": "item.completed", "text": "network error"}, False),
    ],
)
def test_only_provider_network_errors_are_retryable(tmp_path, event, expected):
    save(tmp_path / "source-stdout.jsonl", event)
    assert recovery.transport_failure(tmp_path) is expected


def test_archive_preserves_raw_attempt_and_accounts_for_extra_work(tmp_path):
    folder = tmp_path / "sources/C-test"
    result = source_result()
    save(folder / "result.json", result)
    error(folder / "source-stdout.jsonl")
    save(folder / "trajectory.jsonl", {"step": 3})
    before = {p.name: p.read_bytes() for p in folder.iterdir()}
    save(
        tmp_path / "prior-attempt.json",
        {"operations": 590, "final_assays": 26, "provider_sources": 6},
    )
    destination = recovery.archive_source_failure(tmp_path, {"id": "C-test"}, result)
    assert {p.name: p.read_bytes() for p in destination.iterdir()} == before
    assert not folder.exists()
    prior = recovery.read(tmp_path / "prior-attempt.json")
    assert (prior["operations"], prior["final_assays"], prior["provider_sources"]) == (593, 27, 7)
    assert prior["automatic_failed_attempts"][0]["root"] == str(destination)


@pytest.mark.parametrize("kind", ["unverified", "posttest_exposed", "completed", "scientific"])
def test_archive_rejects_unsafe_or_outcome_selected_retry(tmp_path, kind):
    folder = tmp_path / "sources/C-test"
    result = source_result()
    if kind == "unverified":
        result["source"]["exact_replay"]["verified"] = False
    elif kind == "posttest_exposed":
        result["posttests"]["K1"] = {"payload": {"answer": "sealed"}}
    elif kind == "completed":
        result["status"] = "completed"
    save(folder / "result.json", result)
    error(
        folder / "source-stdout.jsonl",
        "quality goal not reached" if kind == "scientific" else "network error",
    )
    with pytest.raises(ValueError):
        recovery.archive_source_failure(tmp_path, {"id": "C-test"}, result)
    assert (folder / "result.json").exists()


def test_posttest_continues_same_thread_and_cumulative_calculator_audit(tmp_path):
    sealed = tmp_path / "K1/receipt.json"
    save(sealed, {"payload": "completed earlier"})
    before = sealed.read_bytes()
    waits, seen = [], []
    audit = tmp_path / "Q-numerics.jsonl"

    def call(agent, folder, stage, thread, progress, design):
        assert thread == "retained-thread"
        assert design == {"question": "unchanged"}
        used = len(audit.read_text().splitlines()) if audit.exists() else 0
        seen.append(used)
        with audit.open("a", encoding="utf-8") as handle:
            handle.write('{"attempt": 1}\n')
        interrupted = len(seen) < 3
        turn = {
            "thread_id": thread,
            "failure": "provider_failure" if interrupted else None,
            "payload": None if interrupted else {"predictions": []},
            "elapsed_s": 2,
            "numerics_attempts": used + 1,
        }
        save(folder / stage / "receipt.json", turn)
        error(folder / stage / "stdout.jsonl")
        return turn

    turn = recovery.retry_posttest(
        call,
        None,
        tmp_path,
        "Q",
        "retained-thread",
        {},
        {"question": "unchanged"},
        lambda failures, stage: waits.append((failures, stage)),
    )
    assert waits == [(1, "Q"), (2, "Q")]
    assert seen == [0, 1, 2]
    assert turn["numerics_attempts"] == 3
    assert turn["elapsed_s"] == 6
    assert len(turn["transport_recovery_attempts"]) == 2
    assert sealed.read_bytes() == before
    assert (tmp_path / "posttest-interruptions/Q/attempt-0001/receipt.json").is_file()


@pytest.mark.parametrize(
    "failure,payload",
    [
        ("forbidden_tool", None),
        (None, {"answer": "poor"}),
        ("provider_failure", {"answer": "received"}),
    ],
)
def test_posttest_does_not_retry_accepted_answers_or_semantic_failures(tmp_path, failure, payload):
    def call(*args):
        error(tmp_path / "Q/stdout.jsonl")
        return {"failure": failure, "payload": payload, "thread_id": "t"}

    def forbidden_wait(*args):
        pytest.fail("Non-transport result was retried")

    result = recovery.retry_posttest(call, None, tmp_path, "Q", "t", {}, {}, forbidden_wait)
    assert result["payload"] == payload


def test_automatic_queue_retries_transport_then_advances_without_retrying_outcomes(
    tmp_path, monkeypatch
):
    root, report = tmp_path / "root", tmp_path / "report"
    cells = [{"id": "C-one"}, {"id": "C-two"}]
    save(root / "design.json", {"schedule": cells})
    save(root / "qualification/result.json", {"passed": True})
    save(
        root / "prior-attempt.json",
        {
            "retained_completed_cells": [],
            "transport_recovery": 4,
            "operations": 0,
            "final_assays": 0,
            "provider_sources": 0,
        },
    )
    monkeypatch.setattr(recovery.formal, "verify_frozen", lambda path: None)
    monkeypatch.setattr(recovery, "retry_delay", lambda failures: 0)
    calls = []

    def source(path, cell, progress):
        calls.append(cell["id"])
        folder = path / "sources" / cell["id"]
        folder.mkdir(parents=True, exist_ok=False)
        result = source_result(cell["id"], "completed" if len(calls) == 2 else "failed")
        if len(calls) == 1:
            error(folder / "source-stdout.jsonl")
        elif cell["id"] == "C-two":
            result["failure"] = {"stage": "source", "message": "missing recommendation"}
        save(folder / "result.json", result)
        return deepcopy(result)

    def export(path, target):
        rows = [recovery.read(p) for p in (path / "sources").glob("*/result.json")]
        target.mkdir(parents=True, exist_ok=True)
        (target / "REPORT.md").write_text("# Report\n\nPhase: sources.\n", encoding="utf-8")
        return {
            "completed_chains": sum(r["status"] == "completed" for r in rows),
            "sealed_batches": len(rows),
        }

    monkeypatch.setattr(recovery.formal, "source", source)
    monkeypatch.setattr(recovery.formal, "export", export)
    recovery.run(root, report, "http://127.0.0.1:7890", automatic=True)
    assert calls == ["C-one", "C-one", "C-two"]
    assert recovery.read(root / "sources/C-one/result.json")["status"] == "completed"
    assert recovery.read(root / "sources/C-two/result.json")["status"] == "failed"
    assert recovery.read(root / "prior-attempt.json")["provider_sources"] == 1
    assert recovery.read(root / "controller-status.json")["activity"] == "finished"


def test_backoff_is_capped_without_a_retry_count_cutoff():
    assert [recovery.retry_delay(i) for i in range(1, 8)] == [60, 120, 240, 480, 900, 900, 900]
    assert recovery.retry_delay(1000000) == 900


def test_retry_crosses_real_launcher_with_fresh_directory_and_existing_audit(tmp_path):
    from scripts.run_work_ii_final_diagnostic import launch

    from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    audit = tmp_path / "Q-numerics.jsonl"
    audit.write_text('{"attempt": 1}\n', encoding="utf-8")
    calls = []

    def call(agent, folder, stage, thread_id, progress, design):
        calls.append(stage)
        events = [{"type": "thread.started", "thread_id": thread_id}]
        if len(calls) == 1:
            events.append({"type": "error", "message": "idle timeout waiting for SSE"})
        else:
            events.append(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "agent_message",
                        "text": '{"answer":"ok"}',
                    },
                }
            )
        command = [sys.executable, "-c", f"import json; [print(json.dumps(e)) for e in {events!r}]"]
        return launch(
            command,
            "same question",
            workspace,
            dict(recovery.os.environ),
            folder / stage,
            10,
            True,
            audit,
            progress,
            numerics_budget=FOLLOWUP_NUMERICS,
        )

    turn = recovery.retry_posttest(
        call, None, tmp_path, "Q", "same-thread", {}, {}, lambda *args: None
    )
    assert calls == ["Q", "Q"]
    assert turn["payload"] == {"answer": "ok"}
    assert turn["failure"] is None
    assert turn["numerics_attempts"] == 1
    assert (tmp_path / "posttest-interruptions/Q/attempt-0001/stdout.jsonl").exists()
    assert (tmp_path / "Q/stdout.jsonl").exists()


@pytest.mark.parametrize("revoked", [False, True])
def test_repair_fills_questions_without_rerunning_underbudget_source(
    tmp_path, monkeypatch, revoked
):
    cell = {"id": "C-test", "batches": 12, "world_seed": 0, "arm": "Opaque"}
    folder = tmp_path / "sources/C-test"
    original = source_result()
    original["failure"] = {"stage": "Q", "message": "provider_failure"}
    original["posttests"] = {"K1": {"payload": {"sealed": True}, "failure": None}}
    original.update(elapsed_s=10, public_baselines={}, recommendation_retest={"passed": True})
    save(folder / "result.json", original)
    error(
        folder / "Q/stdout.jsonl",
        "refresh token was revoked" if revoked else "idle timeout waiting for SSE",
    )
    save(folder / "Q/receipt.json", {"payload": None, "failure": "provider_failure"})
    save(folder / "source-receipts.json", [{"thread_id": "t", "final_payload_valid": True}])
    home = tmp_path / "home"
    (home / "codex-home/sessions").mkdir(parents=True)
    if revoked:
        current = tmp_path / "current-login"
        current.mkdir()
        (current / "auth.json").write_text('"new-test-credential"')
        (home / "codex-home/auth.json").write_text('"old-test-credential"')
        monkeypatch.setenv("CODEX_HOME", str(current))
    save(folder / "runtime-location.json", {"home": str(home)})
    save(folder / "trajectory.jsonl", {"step": 1, "action": {"operation": "wait"}})
    before = (folder / "trajectory.jsonl").read_bytes()
    save(tmp_path / "design.json", {"queries": []})
    save(tmp_path / "qualification/W01/queries/result.json", {"truth": []})
    stages = []

    def posttest(agent, output, stage, thread, progress, design):
        stages.append(stage)
        assert thread == "t"
        return {"payload": {"answer": "kept"}, "failure": None}

    monkeypatch.setattr(recovery.formal.pilot, "posttest", posttest)
    monkeypatch.setattr(recovery.formal, "evaluate", lambda *args: {"valid": True})
    monkeypatch.setattr(recovery.formal.pilot, "token_accounting", lambda result: {})
    assert recovery.repair_posttests(tmp_path, cell, {}, lambda *args: None)
    result = recovery.read(folder / "result.json")
    assert stages == ["Q", "K2"]
    assert result["posttests"]["K1"] == original["posttests"]["K1"]
    assert result["status"] == "failed"
    assert result["retained_source_nonconformance"]["completed_batches"] == 1
    assert result["source"] == original["source"]
    assert (folder / "trajectory.jsonl").read_bytes() == before
    assert recovery.read(folder / "posttest-repair/original-result.json") == original
    if revoked:
        assert (home / "codex-home/auth.json").read_bytes() == (current / "auth.json").read_bytes()
        assert result["posttest_repair"]["credential_refreshed_from_current_local_login"] is True
