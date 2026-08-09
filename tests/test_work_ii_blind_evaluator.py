from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_blind as blind
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    execute_blind_evaluation_plan,
    validate_blind_evaluation_plan,
)


def _cell() -> dict[str, object]:
    return {
        "cell_id": "work-ii-public-01-01-arm-01",
        "cell_key_sha256": "a" * 64,
        "task_id": "electrochemical-conversion",
        "world_seed": 672326802,
    }


def _contract() -> dict[str, object]:
    return {
        "participant_final_recommendations_per_cell": 1,
        "blind_targets_per_cell": [
            "observed_incumbent",
            "participant_final_recommendation",
        ],
        "blind_replicates_per_target": 3,
        "paired_noise_within_replicate": True,
        "participant_feedback_from_blind_evaluator": False,
        "evaluator_provider_calls": 0,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
    }


def _summary() -> dict[str, object]:
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "robust public evidence",
    }
    return {
        "completed": True,
        "analysis": {
            "experiments": [
                {
                    "experiment_index": index,
                    "leaderboard_score": score,
                    "operations": [
                        {"operation": "wait", "duration_s": index},
                        {"operation": "measure", "instrument": "final_assay"},
                    ],
                }
                for index, score in enumerate((0.2, 0.8, 0.8, 0.4), start=1)
            ],
            "final_recommendation": recommendation,
            "final_recommendation_sha256": canonical_json_sha256(recommendation),
            "observed_incumbent_experiment_index": 2,
        },
    }


def test_blind_plan_freezes_two_targets_three_paired_replicates() -> None:
    plan = build_blind_evaluation_plan(_cell(), _summary(), _contract())
    assert validate_blind_evaluation_plan(plan) == []
    assert plan["blind_target_count"] == 2
    assert plan["blind_execution_count"] == 6
    assert plan["evaluator_provider_call_count"] == 0
    assert [target["source_experiment_index"] for target in plan["targets"]] == [2, 2]
    for replicate_index in range(1, 4):
        rows = [
            row
            for row in plan["executions"]
            if row["replicate_index"] == replicate_index
        ]
        assert len({row["paired_noise_id_sha256"] for row in rows}) == 1
        assert len({row["observation_seed"] for row in rows}) == 1


def test_blind_plan_rejects_tampering_and_incumbent_drift() -> None:
    plan = build_blind_evaluation_plan(_cell(), _summary(), _contract())
    tampered = deepcopy(plan)
    tampered["executions"][0]["action_plan_sha256"] = "b" * 64
    errors = validate_blind_evaluation_plan(tampered)
    assert "blind evaluator plan self-hash mismatch" in errors
    assert "blind evaluator action plan binding mismatch" in errors

    summary = _summary()
    summary["analysis"]["observed_incumbent_experiment_index"] = 3
    try:
        build_blind_evaluation_plan(_cell(), summary, _contract())
    except ValueError as error:
        assert "incumbent" in str(error)
    else:
        raise AssertionError("incumbent drift should fail closed")


def test_blind_executor_runs_six_zero_provider_replays_once(
    monkeypatch,
    tmp_path: Path,
) -> None:
    plan = build_blind_evaluation_plan(_cell(), _summary(), _contract())

    def fake_run_agent(**kwargs):
        agent = kwargs["agent"]
        output_path = Path(kwargs["output_path"])
        agent.reset({}, 0)
        rows = []
        history = []
        for step in range(1, kwargs["budget"] + 1):
            action = agent.act(history)
            info = {
                "transaction_status": "committed",
                "operation_type": action["operation"],
                "instrument": action.get("instrument"),
            }
            agent.update(action, {}, 0.0, info)
            rows.append(
                {
                    "action": action,
                    **info,
                    "leaderboard_score": 0.75 if step == kwargs["budget"] else None,
                }
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "".join(json.dumps(row) + "\n" for row in rows),
            encoding="utf-8",
        )
        return []

    class _Replay:
        def to_dict(self):
            return {"verified": True, "checked_steps": 2, "mismatches": []}

    monkeypatch.setattr(blind, "run_agent", fake_run_agent)
    monkeypatch.setattr(blind, "verify_records", lambda records, tolerance: _Replay())
    config = {
        "task_id": "electrochemical-conversion",
        "world_split": "test",
        "objective": "test",
        "observation_noise_mode": "deterministic_keyed",
    }
    output = tmp_path / "blind-output"
    report = execute_blind_evaluation_plan(
        plan,
        config,
        output,
    )
    assert report["status"] == "completed"
    assert report["completed_execution_count"] == 6
    assert report["evaluator_provider_call_count"] == 0
    assert report["participant_operation_denominator_impact"] == 0
    assert report["participant_feedback_emitted"] is False
    assert report["recommendation_gain_over_incumbent"] == 0.0
    assert len(list((output / "executions").glob("*/receipt.json"))) == 6
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        execute_blind_evaluation_plan(plan, config, output)
