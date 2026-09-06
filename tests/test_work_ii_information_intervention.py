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
