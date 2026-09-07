import json
import time

import pytest

from chemworld.eval.work_ii_information_intervention import cells_for_world, prompt, summarize
from chemworld.eval.work_ii_public_endpoint_reference import candidate_domains, public_contract


def world():
    query = {"query_id": "q", "reference_partition_coefficient": 2.0}
    return {
        "cluster_id": "test",
        "target_exponent": 2.05,
        "scoring_truth": {
            "q": {
                "product_in_organic": 0.8,
                "product_in_aqueous": 0,
                "phase_ratio": 1,
                "score": 0.58,
            }
        },
        "public_packet": {
            "task_id": "partition-discovery",
            "metric_range": [0, 1],
            "candidate_mechanism_families": [],
            "scoring_action_queries": [query],
            "candidate_parameter_domains": candidate_domains(),
            "complete_observation_contract": public_contract(298.15),
            "evidence": [],
        },
    }


def test_only_post_disclosure_differs_within_prior_pair():
    cells = cells_for_world(world(), "gpt", 0)
    assert len(cells) == len({c["cell_id"] for c in cells}) == 6
    for a, b in zip(cells[::2], cells[1::2], strict=True):
        assert prompt(a, "pre", "on") == prompt(b, "pre", "on")
        pa = json.loads(prompt(a, "post", "on").rsplit("\n", 1)[1])
        pb = json.loads(prompt(b, "post", "on").rsplit("\n", 1)[1])
        assert ("complete_observation_contract" in pa) != ("complete_observation_contract" in pb)
        pa.pop("complete_observation_contract", None)
        pb.pop("complete_observation_contract", None)
        assert pa == pb
        assert "scoring_truth" not in pa and "target_exponent" not in pa
        assert "initial_world_model" not in pa
    # Unknown-prior prompt contains no realized answer.
    assert "2.05" not in prompt(cells[0], "pre", "on")


def test_recovery_uses_each_world_answer_and_excludes_retention():
    cells = cells_for_world(world(), "gpt", 0)
    results = []
    for cell in cells:
        payload = {
            "family": "FAMILY_B_POWER",
            "exponent": 2.05,
            "predictions": world()["scoring_truth"],
            "selected_query_id": "q",
        }
        status = "completed" if cell["information"] == "complete" else "failed"
        results.append({"cell_id": cell["cell_id"], "status": status, "post": payload})
    report = summarize(results, cells, formal=False)
    assert report["primary"]["mean"] == 1
    assert report["counts"] == {"failed": 3, "completed": 3}
    complete_recovery = next(
        g for g in report["groups"] if (g["information"], g["analysis"]) == ("complete", "recovery")
    )
    assert complete_recovery["scheduled"] == complete_recovery["joint_recovery"] == 2
    assert report["primary"]["approximate_world_bootstrap_95"] is None


def test_usage_counts_cumulative_threads_once_and_retains_interrupted_lower_bound():
    cells = cells_for_world(world(), "gpt", 0)
    results = [
        {
            "cell_id": cells[0]["cell_id"],
            "status": "failed",
            "receipts": [
                {"thread_id": "a", "usage": {"output_tokens": 10, "reasoning_output_tokens": 0}},
                {"thread_id": "a", "usage": {"output_tokens": 30, "reasoning_output_tokens": 0}},
            ],
        },
        {
            "cell_id": cells[1]["cell_id"],
            "status": "failed",
            "receipts": [
                {"thread_id": "b", "usage": {"output_tokens": 5}},
                {"thread_id": "b", "usage": {}},
            ],
        },
        {
            "cell_id": cells[2]["cell_id"],
            "status": "failed",
            "failure": "platform_thread_changed",
            "receipts": [
                {"thread_id": "c", "usage": {"output_tokens": 7}},
                {"thread_id": "d", "usage": {"output_tokens": 9}},
            ],
        },
    ]
    report = summarize(results, cells, formal=True)
    assert report["resources"]["output_tokens"] == 51
    assert report["resources"]["reasoning_output_tokens"] == 0
    assert report["resources"]["usage_missing_turns"] == 1
    assert report["counts"] == {"failed": 3, "unstarted": 3}
    assert report["primary"]["mean"] is None
    assert report["primary"]["approximate_world_bootstrap_95"] is None


def test_user_stopped_block_reports_original_denominator_and_cannot_resume(tmp_path):
    from scripts.run_work_ii_information_intervention import analyze, run, write

    write(
        tmp_path / "inputs.json",
        {
            "phase": "formal",
            "model": "gpt",
            "cells": cells_for_world(world(), "gpt", 0),
            "protocol": {"providers": {"gpt": {}}, "formal": {}},
            "reference_binding": {},
        },
    )
    write(tmp_path / "user_stop.json", {"reason": "user_requested_reasoning_none"})
    report = analyze(tmp_path)
    assert report["status"] == "stopped_by_user"
    assert report["counts"] == {"unstarted": 6}
    assert report["primary"]["mean"] is None
    with pytest.raises(ValueError, match="user-stopped"):
        run(tmp_path)


def test_explicit_resume_keeps_failed_attempts_and_original_deadline(tmp_path, monkeypatch):
    from scripts import run_work_ii_information_intervention as runner

    cells = cells_for_world(world(), "gpt", 0)
    runner.write(
        tmp_path / "inputs.json",
        {
            "phase": "development",
            "model": "gpt",
            "cells": cells,
            "protocol": {"providers": {"gpt": {}}, "development": {}},
            "reference_binding": {},
        },
    )
    runner.write(tmp_path / "block.json", {"started_epoch": 100, "deadline_epoch": 200})
    runner.write(tmp_path / "user_stop.json", {"reason": "configuration_change"})
    runner.write(
        tmp_path / "user_resume.json",
        {
            "user_stop_sha256": runner.digest(tmp_path / "user_stop.json"),
            "deadline_epoch": 200,
        },
    )
    failed = {"cell_id": cells[0]["cell_id"], "status": "failed", "failure": "tool_budget_exceeded"}
    runner.write(tmp_path / "sessions/001/result.json", failed)
    runner.write(tmp_path / "sessions/002/attempt.json", {"cell_id": cells[1]["cell_id"]})
    original_files = {p: p.read_bytes() for p in tmp_path.rglob("*.json")}
    monkeypatch.setattr(runner.time, "time", lambda: 150)
    called = []

    def finish(cell, protocol, phase, directory, deadline, progress, **kwargs):
        assert deadline == 200
        called.append(cell["cell_id"])
        result = {
            "cell_id": cell["cell_id"],
            "status": "failed",
            "failure": "schema_validation_failed",
            "elapsed_s": 1,
        }
        runner.write(directory / "result.json", result)
        return result

    monkeypatch.setattr(runner, "run_session", finish)
    runner.run(tmp_path)
    assert called == [c["cell_id"] for c in cells[2:]]
    assert all(p.read_bytes() == content for p, content in original_files.items())
    report = runner.read(tmp_path / "summary.json")
    assert report["counts"] == {"failed": 6}
    assert report["status"] != "stopped_by_user"
    assert report["failures"][1]["failure"] == "interrupted_attempt_not_reissued"
    assert "user_stop" in report and "user_resume" in report
    runner.write(tmp_path / "user_stop.json", {"reason": "later_user_stop"})
    assert runner.authorized_resume(tmp_path) is None
    with pytest.raises(ValueError, match="user-stopped"):
        runner.run(tmp_path)


def test_frozen_resume_never_extends_expired_budget(tmp_path, monkeypatch):
    from scripts import run_work_ii_information_intervention as runner

    runner.write(tmp_path / "inputs.json", {"phase": "formal"})
    runner.write(
        tmp_path / "freeze.json", {"inputs_sha256": runner.digest(tmp_path / "inputs.json")}
    )
    runner.write(tmp_path / "block.json", {"started_epoch": 100, "deadline_epoch": 200})
    runner.write(tmp_path / "user_stop.json", {"reason": "configuration_change"})
    original_ledger = (tmp_path / "block.json").read_bytes()
    monkeypatch.setattr(runner.time, "time", lambda: 201)
    with pytest.raises(ValueError, match="deadline elapsed"):
        runner.resume_frozen(tmp_path)
    assert (tmp_path / "block.json").read_bytes() == original_ledger
    assert not (tmp_path / "user_resume.json").exists()


def test_resumed_deadline_reports_unstarted_without_inventing_results(tmp_path, monkeypatch):
    from scripts import run_work_ii_information_intervention as runner

    runner.write(
        tmp_path / "inputs.json",
        {
            "phase": "formal",
            "model": "gpt",
            "cells": cells_for_world(world(), "gpt", 0),
            "protocol": {"providers": {"gpt": {}}, "formal": {}},
            "reference_binding": {},
        },
    )
    runner.write(tmp_path / "user_stop.json", {"reason": "configuration_change"})
    runner.write(
        tmp_path / "user_resume.json",
        {
            "user_stop_sha256": runner.digest(tmp_path / "user_stop.json"),
            "deadline_epoch": 200,
        },
    )
    monkeypatch.setattr(runner.time, "time", lambda: 201)
    report = runner.analyze(tmp_path)
    assert report["status"] == "deadline_reached_with_unstarted"
    assert report["counts"] == {"unstarted": 6}
    assert report["primary"]["mean"] is None
    assert report["primary"]["approximate_world_bootstrap_95"] is None
    assert not (tmp_path / "sessions").exists()


def test_applied_calendar_amendment_reports_actual_budget_and_preserves_original(
    tmp_path, monkeypatch
):
    from scripts import run_work_ii_information_intervention as runner

    budgets = {
        "turn_timeout_s": 600,
        "session_timeout_s": 1200,
        "block_timeout_s": 43200,
        "provider_retries": 0,
    }
    runner.write(
        tmp_path / "inputs.json",
        {
            "phase": "formal",
            "model": "gpt",
            "cells": cells_for_world(world(), "gpt", 0),
            "protocol": {"providers": {"gpt": {}}, "formal": budgets},
            "reference_binding": {},
        },
    )
    runner.write(tmp_path / "user_stop.json", {"reason": "configuration_change"})
    runner.write(
        tmp_path / "user_resume.json",
        {
            "user_stop_sha256": runner.digest(tmp_path / "user_stop.json"),
            "deadline_epoch": 200,
        },
    )
    runner.write(tmp_path / "block.json", {"started_epoch": 100, "deadline_epoch": 200})
    original = {p: p.read_bytes() for p in tmp_path.glob("*.json")}
    amendment = {"original_deadline_epoch": 200, "effective_deadline_epoch": None}
    runner.write(tmp_path / "block_deadline_override.json", amendment)
    monkeypatch.setattr(runner.time, "time", lambda: 201)
    assert runner.analyze(tmp_path)["status"] == "deadline_reached_with_unstarted"
    amendment["activated_epoch"] = 150
    runner.write(tmp_path / "block_deadline_override.json", amendment)
    report = runner.analyze(tmp_path)
    assert report["status"] == "incomplete"
    assert report["counts"] == {"unstarted": 6}
    assert report["primary"]["mean"] is None
    assert report["budgets"] == budgets
    assert report["effective_budgets"] == {**budgets, "block_timeout_s": None}
    assert report["schedule_amendment"] == amendment
    assert all(p.read_bytes() == content for p, content in original.items())


def test_calendar_amendment_cannot_override_platform_stop(tmp_path):
    from scripts import run_work_ii_information_intervention as runner

    cells = cells_for_world(world(), "gpt", 0)
    runner.write(tmp_path / "inputs.json", {"phase": "formal", "cells": cells})
    runner.write(
        tmp_path / "freeze.json", {"inputs_sha256": runner.digest(tmp_path / "inputs.json")}
    )
    runner.write(tmp_path / "block.json", {"deadline_epoch": 200})
    runner.write(tmp_path / "user_stop.json", {"reason": "configuration_change"})
    runner.write(
        tmp_path / "user_resume.json",
        {"user_stop_sha256": runner.digest(tmp_path / "user_stop.json")},
    )
    runner.write(
        tmp_path / "block_deadline_override.json",
        {"original_deadline_epoch": 200, "effective_deadline_epoch": None},
    )
    runner.write(
        tmp_path / "sessions/001/result.json",
        {"cell_id": cells[0]["cell_id"], "failure": "platform_thread_changed", "status": "failed"},
    )
    with pytest.raises(ValueError, match="does not override platform"):
        runner.resume_frozen(tmp_path, without_block_deadline=True)


@pytest.mark.parametrize("reasoning_tokens", [1, None])
def test_none_mode_mismatch_stops_before_post(tmp_path, monkeypatch, reasoning_tokens):
    from scripts import run_work_ii_final_diagnostic as runner

    stages = []

    def fake_launch(*args):
        stages.append(args[-1]["stage"])
        usage = {} if reasoning_tokens is None else {"reasoning_output_tokens": reasoning_tokens}
        return {"failure": None, "usage": usage}

    monkeypatch.setattr(runner, "launch", fake_launch)
    monkeypatch.setattr(runner, "_prepare_codex_home", lambda *_args: {})
    result = runner.run_session(
        cells_for_world(world(), "gpt", 0)[0],
        {
            "providers": {"gpt": {"id": "fixture", "model": "fixture", "reasoning_effort": "none"}},
            "development": {"turn_timeout_s": 600, "session_timeout_s": 1200},
        },
        "development",
        tmp_path / "session",
        time.time() + 1200,
        {},
    )
    assert stages == ["pre"]
    assert result["status"] == "failed"
    assert result["failure"] == "platform_reasoning_not_disabled"
    assert len(result["receipts"]) == 1
