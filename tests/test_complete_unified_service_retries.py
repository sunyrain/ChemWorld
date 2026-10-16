"""Service reruns use synthetic terminal records; no provider or simulator calls."""

import json
import os
from pathlib import Path

import psutil
import pytest
from scripts import complete_unified_service_retries as service
from scripts import run_unified_matrices as runner


def test_completion_counts_follow_effective_summary_after_service_reruns(tmp_path):
    runner.write(
        tmp_path / "summary.json",
        {"complete_chains": 288, "valid_forecasts": 298, "cases": [{"status": "completed"}]},
    )
    runner.write(
        tmp_path / "completion-status.json", {"complete_chains": 284, "valid_forecasts": 294}
    )
    service.publish_phase(
        tmp_path,
        {"status": "completed", "rounds": [{}], "final": {"completed_units": 288}},
    )
    completion = runner.read(tmp_path / "completion-status.json")
    assert completion["complete_chains"] == 288
    assert completion["valid_forecasts"] == 298
    assert completion["service_retries"]["completed_units"] == 288
    assert completion["stage"] == "terminal"
    assert "cases" not in completion


def unit():
    return {
        "id": "P-W01-B12-optimization-E-Opaque",
        "repeat": "repeat-01",
        "system": "P",
        "world": "P-W01",
        "arm": "Opaque",
        "batches": 12,
        "matrix": "B",
    }


def save_case(
    root,
    row,
    *,
    failure=None,
    stage="source",
    completed=False,
    message=None,
    status=None,
    recovered=False,
):
    path = root / row["repeat"] / row["id"]
    posttests = {s: {"payload": {"report": "sealed"}, "failure": None} for s in service.STAGES}
    source = {
        "batches": [{}] * row["batches"],
        "operations": 150 if row["batches"] else 0,
        "exact_replay": {"verified": True},
    }
    if failure and not completed:
        if stage == "source":
            source.update(batches=[], operations=0, failure={"stage": "source", "message": failure})
            posttests = {}
        else:
            posttests = {
                s: v
                for s, v in posttests.items()
                if service.STAGES.index(s) <= service.STAGES.index(stage)
            }
            posttests[stage] = {"failure": failure, "payload": None}
    result = {
        "status": "completed" if completed else "failed",
        "source": source,
        "failure": None if completed else {"stage": stage, "message": failure},
        "posttests": posttests,
        "prediction_evaluation": {"valid": completed},
    }
    runner.write(path / "result.json", result)
    runner.write(
        path / "status.json",
        {
            "status": status or ("completed" if completed else "incomplete"),
            "failure": result["failure"],
            "elapsed_s": 20,
        },
    )
    if message:
        log = (
            path
            / "participant"
            / ("source-stdout.jsonl" if stage == "source" else f"{stage}/stdout.jsonl")
        )
        log.parent.mkdir(parents=True, exist_ok=True)
        events = [
            {"type": "error", "message": message},
            {"type": "turn.failed", "error": {"message": message}},
        ]
        if recovered:
            events.append({"type": "turn.completed"})
        log.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    return path


def classify(root, row):
    return service.classify_unit(root, row, {"schedule": [row]})


@pytest.mark.parametrize(
    "message,category",
    [
        ("stream disconnected before completion: error sending request", "transport"),
        ("HTTP 503 Service unavailable", "provider_5xx"),
        ("HTTP 429 too many requests", "rate_limit"),
        ("ReadTimeout: request timed out", "provider_timeout"),
    ],
)
def test_terminal_source_service_error_requires_matching_logs(tmp_path, message, category):
    row = unit()
    save_case(tmp_path, row, failure="max_provider_error_events", message=message)
    decision = classify(tmp_path, row)
    assert decision["classification"] == "eligible"
    assert decision["category"] == category
    assert decision["stage"] == "source"
    assert len(decision["evidence_paths"]) == 1


def test_posttest_requires_same_stage_not_earlier_source_error(tmp_path):
    row = unit()
    path = save_case(tmp_path, row, failure="provider_failure", stage="Q")
    log = path / "participant/source-stdout.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text(
        '{"type":"turn.failed","error":{"message":"stream disconnected"}}\n', encoding="utf-8"
    )
    assert classify(tmp_path, row)["classification"] == "needs_review"
    q = path / "participant/Q/stdout.jsonl"
    q.parent.mkdir(parents=True)
    q.write_text(log.read_text(encoding="utf-8"), encoding="utf-8")
    assert classify(tmp_path, row)["classification"] == "eligible"


@pytest.mark.parametrize(
    "failure",
    [
        "tool_budget_exceeded",
        "session_wall_time_limit",
        "invalid prediction schema",
        "missing final recommendation",
    ],
)
def test_scientific_or_budget_failure_is_never_retried(tmp_path, failure):
    row = unit()
    save_case(tmp_path, row, failure=failure, message="stream disconnected")
    assert classify(tmp_path, row)["classification"] == "not_eligible"


@pytest.mark.parametrize(
    "message",
    ["quota exhausted", "HTTP 401 unauthorized", "insufficient credit", "billing failure"],
)
def test_account_access_block_is_review_not_scientific_failure(tmp_path, message):
    row = unit()
    save_case(tmp_path, row, failure="provider_failure", message=message)
    result = classify(tmp_path, row)
    assert result["classification"] == "needs_review"
    assert result["reason"] == "technical_access_block"


def test_completed_and_scientifically_incomplete_recovered_stream_not_retried(tmp_path):
    row = unit()
    path = save_case(tmp_path, row, completed=True, message="stream disconnected", recovered=True)
    assert classify(tmp_path, row)["classification"] == "not_eligible"
    result = runner.read(path / "result.json")
    result["failure"] = {"type": "nonconforming", "failed_checks": ["recommendation_retest"]}
    runner.write(path / "result.json", result)
    runner.write(path / "status.json", {"status": "incomplete", "failure": result["failure"]})
    assert classify(tmp_path, row)["classification"] == "not_eligible"


def test_aggregated_old_network_receipt_does_not_override_recovered_stream(tmp_path):
    row = unit()
    path = save_case(
        tmp_path, row, failure="provider_failure", message="stream disconnected", recovered=True
    )
    runner.write(
        path / "participant/source-receipts.json",
        [
            {
                "status": "interrupted_before_next_action",
                "failure_type": "max_provider_error_events",
                "provider_errors": [{"category": "network"}],
            }
        ],
    )
    assert classify(tmp_path, row)["classification"] == "needs_review"


def test_posttest_disconnection_does_not_erase_earlier_incomplete_science(tmp_path):
    row = unit()
    path = save_case(
        tmp_path, row, failure="provider_failure", stage="Q", message="stream disconnected"
    )
    result = runner.read(path / "result.json")
    result["source"]["batches"] = [{}] * 10
    runner.write(path / "result.json", result)
    assert classify(tmp_path, row)["classification"] == "not_eligible"
    result["source"]["failure"] = {"message": "operation limit exhausted"}
    runner.write(path / "result.json", result)
    assert classify(tmp_path, row)["classification"] == "not_eligible"


def test_exact_p_secondary_usage_failure_requires_terminal_network_and_failed_receipt(tmp_path):
    row = unit()
    path = save_case(tmp_path, row, failure="provider_failure", message="stream disconnected")
    result = runner.read(path / "result.json")
    failure = {"type": "ValueError", "message": service.MISSING_RESOURCE_MESSAGE, "stage": "source"}
    result["failure"] = result["source"]["failure"] = failure
    result["source"].update(batches=[{}] * 11, operations=218)
    runner.write(path / "result.json", result)
    assert classify(tmp_path, row)["classification"] == "needs_review"
    runner.write(
        path / "participant/source-receipts.json",
        [
            {
                "status": "failed",
                "usage_complete": False,
                "usage_observed": False,
                "usage_unavailable_reason": "codex_cli_completed_without_usage_event",
            }
        ],
    )
    decision = classify(tmp_path, row)
    assert decision["classification"] == "eligible"
    assert decision["reason"] == "confirmed_p_transport_interruption_with_missing_usage"
    result["source"]["failure"]["message"] = "A different resource accounting error"
    result["failure"] = result["source"]["failure"]
    runner.write(path / "result.json", result)
    assert classify(tmp_path, row)["classification"] == "needs_review"


def make_primary(tmp_path):
    root = tmp_path / "a2"
    rows = [
        {**unit(), "id": f"case-{n:03d}", "repeat": f"repeat-{n // 100 + 1:02d}"}
        for n in range(300)
    ]
    runner.write(
        root / "design.json",
        {"schedule": rows, "planned_sessions": 300, "workers": 24, "retained_units": {}},
    )
    for name in service.INPUT_DIRS:
        runner.write(root / name / "prepared-input.json", {"immutable": name})
    for row in rows:
        save_case(root, row, completed=True)
    return root, rows


def test_waits_for_all_300_and_for_dead_primary_coordinator(tmp_path, monkeypatch):
    root, rows = make_primary(tmp_path)
    monkeypatch.setattr(service, "coordinator_live", lambda root: True)
    with pytest.raises(service.RetryHoldError, match="still alive"):
        service.inspect_primary(root)
    monkeypatch.setattr(service, "coordinator_live", lambda root: False)
    runner.write(root / rows[0]["repeat"] / rows[0]["id"] / "status.json", {"status": "running"})
    with pytest.raises(service.RetryHoldError, match="not fully"):
        service.inspect_primary(root)
    assert not (root / "service-retries.json").exists()


def test_two_service_rounds_preserve_all_attempts_and_publish_effective_view(tmp_path):
    root, rows = make_primary(tmp_path)
    failed = rows[0]
    original = save_case(root, failed, failure="provider_failure", message="stream disconnected")
    original_bytes = (original / "result.json").read_bytes()
    calls = []

    def run(retry_root):
        design = runner.read(retry_root / "design.json")
        assert len(design["schedule"]) == 300
        assert len(design["retained_units"]) == 299
        assert runner.unit_key(failed) not in design["retained_units"]
        assert design["workers"] == 24
        calls.append(retry_root.name)
        if len(calls) == 1:
            save_case(
                retry_root, failed, failure="provider_failure", message="HTTP 502 Bad gateway"
            )
        else:
            save_case(retry_root, failed, completed=True)
        return 0

    ledger = service.complete(root, run_function=run, retry_delay_s=0)
    assert calls == ["s01", "s02"]
    assert ledger["status"] == "completed"
    assert ledger["final"]["service_retry_attempts"] == 2
    assert ledger["final"]["retried_units"] == 1
    assert ledger["final"]["service_interruptions_remaining"] == 0
    assert (original / "result.json").read_bytes() == original_bytes
    assert (
        Path(runner.read(root / "design.json")["retained_units"][runner.unit_key(failed)]).parts[-3]
        == "s02"
    )
    summary = runner.read(root / "summary.json")
    assert summary["service_retries"]["status"] == "completed"
    assert summary["stage"] == "terminal"
    assert ledger["rounds"][1]["attempts"][0]["original_path"].endswith(
        "s01\\repeat-01\\case-000"
    ) or ledger["rounds"][1]["attempts"][0]["original_path"].endswith("s01/repeat-01/case-000")
    # A second invocation cannot repeat completed attempts.
    service.complete(
        root, run_function=lambda _: pytest.fail("Unexpected provider launch"), retry_delay_s=0
    )


def test_explicit_service_retries_proceed_before_unrelated_access_review(tmp_path):
    root, rows = make_primary(tmp_path)
    save_case(root, rows[0], failure="provider_failure", message="stream disconnected")
    save_case(root, rows[1], failure="quota exhausted")
    calls = []

    def run(retry_root):
        calls.append(retry_root)
        save_case(retry_root, rows[0], completed=True)
        return 0

    with pytest.raises(service.RetryHoldError, match="Remaining"):
        service.complete(root, run_function=run, retry_delay_s=0)
    ledger = runner.read(root / "service-retries.json")
    assert len(calls) == 1
    assert ledger["status"] == "needs_review"
    assert ledger["final"]["service_interruptions_remaining"] == 0
    assert ledger["final"]["needs_review"] == 1
    assert ledger["final"]["scientific_failures_retained"] == 0


def test_resume_after_terminal_retry_does_not_launch_it_again(tmp_path):
    root, rows = make_primary(tmp_path)
    save_case(root, rows[0], failure="provider_failure", message="stream disconnected")
    design, decisions = service.inspect_primary(root)
    ledger = {
        "schema": service.SCHEMA,
        "primary_root": str(root),
        "status": "running",
        "rounds": [],
        "original_units": {runner.unit_key(u): str(runner.folder(root, u, design)) for u in rows},
    }
    record = service.prepare_round(root, ledger, design, decisions)
    save_case(Path(record["root"]), rows[0], completed=True)
    record["state"] = "running"
    service.save_ledger(root, ledger)
    complete = service.complete(
        root, run_function=lambda _: pytest.fail("Terminal attempt relaunched"), retry_delay_s=0
    )
    assert complete["status"] == "completed"
    assert complete["final"]["service_retry_attempts"] == 1


def test_ambiguous_partial_retry_is_held_without_relaunch(tmp_path):
    root, rows = make_primary(tmp_path)
    save_case(root, rows[0], failure="provider_failure", message="stream disconnected")
    design, decisions = service.inspect_primary(root)
    ledger = {
        "schema": service.SCHEMA,
        "primary_root": str(root),
        "status": "running",
        "rounds": [],
    }
    record = service.prepare_round(root, ledger, design, decisions)
    runner.write(
        Path(record["root"]) / rows[0]["repeat"] / rows[0]["id"] / "status.json",
        {"status": "running"},
    )
    with pytest.raises(service.RetryHoldError, match="Ambiguous partial"):
        service.complete(
            root, run_function=lambda _: pytest.fail("Partial attempt relaunched"), retry_delay_s=0
        )


def test_live_retry_controller_and_pid_reuse_are_checked(tmp_path):
    with (
        service.controller_lock(tmp_path),
        pytest.raises(service.RetryHoldError, match="controller is alive"),
        service.controller_lock(tmp_path),
    ):
        pytest.fail("Concurrent controller")
    runner.write(
        tmp_path / "service-retries.lock.json",
        {
            "pid": os.getpid(),
            "process_created_epoch": psutil.Process().create_time() - 1,
        },
    )
    with service.controller_lock(tmp_path):
        assert runner.read(tmp_path / "service-retries.lock.json")["pid"] == os.getpid()


@pytest.mark.parametrize("mapping_already_written", [False, True])
def test_publication_crash_recovery_is_idempotent(tmp_path, mapping_already_written):
    root, rows = make_primary(tmp_path)
    original = save_case(root, rows[0], failure="provider_failure", message="stream disconnected")
    before = (original / "result.json").read_bytes()
    design, decisions = service.inspect_primary(root)
    ledger = {
        "schema": service.SCHEMA,
        "primary_root": str(root),
        "status": "running",
        "rounds": [],
    }
    record = service.prepare_round(root, ledger, design, decisions)
    replacement = save_case(Path(record["root"]), rows[0], completed=True)
    key = runner.unit_key(rows[0])
    record.update(
        state="publishing",
        attempts=[
            {
                "key": key,
                "original_path": str(original),
                "retry_path": str(replacement),
                "status": "completed",
                "failure": None,
            }
        ],
    )
    service.save_ledger(root, ledger)
    if mapping_already_written:
        design.setdefault("retained_units", {})[key] = str(replacement)
        runner.write(root / "design.json", design)
    result = service.complete(
        root, run_function=lambda _: pytest.fail("Published unit relaunched"), retry_delay_s=0
    )
    assert result["status"] == "completed"
    assert len(result["rounds"][0]["attempts"]) == 1
    assert (original / "result.json").read_bytes() == before
    assert runner.read(root / "design.json")["retained_units"][key] == str(replacement)


def test_resume_skips_terminal_attempt_and_only_runs_unstarted_selected_unit(tmp_path):
    root, rows = make_primary(tmp_path)
    for row in rows[:2]:
        save_case(root, row, failure="provider_failure", message="stream disconnected")
    design, decisions = service.inspect_primary(root)
    ledger = {
        "schema": service.SCHEMA,
        "primary_root": str(root),
        "status": "running",
        "rounds": [],
    }
    record = service.prepare_round(root, ledger, design, decisions)
    first = save_case(Path(record["root"]), rows[0], completed=True)
    first_bytes = (first / "result.json").read_bytes()
    calls = []

    def run(retry_root):
        for row in rows[:2]:
            if not (retry_root / row["repeat"] / row["id"]).exists():
                calls.append(runner.unit_key(row))
                save_case(retry_root, row, completed=True)
        return 0

    result = service.complete(root, run_function=run, retry_delay_s=0)
    assert calls == [runner.unit_key(rows[1])]
    assert result["final"]["service_retry_attempts"] == 2
    assert (first / "result.json").read_bytes() == first_bytes
