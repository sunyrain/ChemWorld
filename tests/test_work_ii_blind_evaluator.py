from __future__ import annotations

from copy import deepcopy

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
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
