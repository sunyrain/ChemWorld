"""Scientific boundaries for the minimal development factorial protocol."""

import json

import numpy as np
import pytest
from scripts import run_work_ii_factorial as runner
from scripts.run_work_ii_factorial import provider_call, seal

from chemworld.eval.work_ii_factorial import (
    TASKS,
    compile_design,
    design_matrix,
    development_protocol,
    fit_public_law,
    maximize,
    participant_prompt,
    public_packet,
    score_slots,
    validate_payload,
)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"coefficients": [0] * 5},
        {"coefficients": [True] * 6},
        {"coefficients": [float("nan")] * 6},
        {"coefficients": [0] * 6, "status": "ok"},
    ],
)
def test_minimal_law_rejects_invalid_or_redundant_payload(payload):
    with pytest.raises(ValueError):
        validate_payload(payload, "source")


def test_only_known_candidate_is_accepted():
    validate_payload({"candidate_id": "c01"}, "decision", ["c01"])
    with pytest.raises(ValueError):
        validate_payload({"candidate_id": "hidden-best"}, "decision", ["c01"])


def test_both_task_designs_compile_and_share_disjoint_stratified_coordinates():
    protocol = development_protocol()
    packets = [compile_design(protocol, task) for task in TASKS]
    for key, size in (("evidence", 12), ("candidates", 8)):
        xy = [row["xy"] for row in packets[0][key]]
        assert xy == [row["xy"] for row in packets[1][key]]
        for axis in (0, 1):
            assert sorted(int(point[axis] * size) for point in xy) == list(range(size))
        assert all(
            row["action_plan"][-1]["instrument"] == "final_assay"
            for packet in packets
            for row in packet[key]
        )
    assert not {tuple(row["xy"]) for row in packets[0]["evidence"]} & {
        tuple(row["xy"]) for row in packets[0]["candidates"]
    }


def test_fit_and_prompt_cannot_depend_on_private_candidate_scores():
    packet = compile_design(development_protocol(), TASKS[0])
    coefficients = [0.2, 0.3, -0.1, 0.01, -0.02, 0.04]
    for row, score in zip(
        packet["evidence"], design_matrix(packet["evidence"]) @ coefficients, strict=True
    ):
        row["score"] = float(score)
    law = fit_public_law(packet["evidence"], ridge=0)
    assert law == pytest.approx(coefficients, abs=1e-10)
    source = participant_prompt(packet, coefficients=None)
    decision = participant_prompt(packet, coefficients=law)
    packet["hidden_world"] = "CANARY_SECRET"
    for row in packet["candidates"]:
        row["score"] = "CANARY_SECRET"
        row["truth"] = {"label": "CANARY_SECRET"}
    assert participant_prompt(packet, coefficients=None) == source
    assert participant_prompt(packet, coefficients=law) == decision
    assert "candidates" not in public_packet(packet, candidates=False)
    assert "CANARY_SECRET" not in json.dumps(public_packet(packet, candidates=True))
    assert fit_public_law(packet["evidence"], ridge=0) == pytest.approx(law)
    best_index = int(np.argmax(design_matrix(packet["candidates"]) @ coefficients))
    assert maximize(law, packet["candidates"]) == packet["candidates"][best_index]["id"]


def test_failed_slots_remain_in_fixed_denominator_with_secondary_missing_regret():
    rows = score_slots(
        [
            {"status": "blocked", "candidate_id": None},
            {"status": "completed", "candidate_id": "c01"},
        ],
        {"c01": 0.4, "c02": 0.5},
    )
    assert len(rows) == 2
    assert rows[0]["failure_aware_regret"] == 1
    assert rows[0]["raw_regret"] is None
    assert rows[1]["raw_regret"] == pytest.approx(0.1)


def test_resume_retains_interrupted_attempt_and_never_launches_provider(tmp_path):
    seal(tmp_path / "provider" / "call" / "started.json", {"call_id": "call"})
    receipt = provider_call(tmp_path, "call", "unavailable", "source", {}, None, None, 0)
    assert receipt["status"] == "interrupted"
    assert provider_call(tmp_path, "call", "unavailable", "source", {}, None, None, 0) == receipt
    with pytest.raises(FileExistsError):
        seal(tmp_path / "provider" / "call" / "receipt.json", {"status": "better"})


def test_missing_source_preserves_all_slots_and_independent_fitted_conditions(
    tmp_path, monkeypatch
):
    seal(tmp_path / "m0.json", {"status": "completed"})
    for task in TASKS:
        packet = compile_design(development_protocol(), task)
        for row in packet["evidence"]:
            row["score"] = 0.2 + 0.1 * row["xy"][0]
        seal(tmp_path / "public" / f"{task}.json", packet)
    attempted = []

    def fake_provider(root, call_id, model, stage, packet, law, progress, completed):
        del root, model, law, progress, completed
        attempted.append(call_id)
        return {
            "call_id": call_id,
            "thread_id": call_id,
            "usage": {},
            "status": "schema_failed" if stage == "source" else "completed",
            "final_payload": {}
            if stage == "source"
            else {"candidate_id": packet["candidates"][0]["id"]},
        }

    monkeypatch.setattr(runner, "provider_call", fake_provider)
    # No private score file exists: a hidden-data dependency would fail this path.
    result = runner.run_provider_block(tmp_path)
    assert len(result["slots"]) == 16
    assert len(result["calls"]) == 12
    assert len(attempted) == 8  # four failed sources and four independent F-A decisions
    assert sum(row["status"] == "completed" for row in result["slots"]) == 8
    assert all(
        row["status"] == "completed" for row in result["slots"] if row["condition"].startswith("F")
    )
    runner.run_provider_block(tmp_path)
    assert len(attempted) == 8  # sealed selections resume without replacements
