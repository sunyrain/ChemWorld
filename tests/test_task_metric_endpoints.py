from __future__ import annotations

import pytest

from chemworld.eval.task_metric_endpoints import (
    build_task_metric_contract,
    evaluate_task_metrics,
)
from chemworld.tasks import list_tasks


def _records() -> list[dict[str, object]]:
    return [
        {
            "step": 1,
            "run_id": "step-1",
            "transaction_status": "committed",
            "constraint_flags": {},
            "leaderboard_score": 0.4,
            "observation": {"score": 0.4, "yield": 0.5},
            "agent_trace": [{"validator_result": {"valid": True}}],
        },
        {
            "step": 2,
            "run_id": "step-2",
            "transaction_status": "committed",
            "constraint_flags": {},
            "leaderboard_score": 0.8,
            "observation": {"score": 0.8, "yield": 0.9},
            "agent_trace": [
                {"validator_result": {"valid": True}},
                {"validator_result": {}},
            ],
        },
    ]


def test_every_registered_success_metric_has_an_executable_endpoint() -> None:
    contracts = [
        build_task_metric_contract(task.success_metrics) for task in list_tasks()
    ]

    assert all(contract["all_metrics_bound"] for contract in contracts)
    assert {
        endpoint["source_layer"]
        for contract in contracts
        for endpoint in contract["endpoints"]
    } == {
        "paired_split_campaign",
        "predictive_holdout",
        "structured_artifact",
        "terminal_observation",
        "trajectory_aggregate",
    }


def test_trajectory_aliases_have_scientific_operation_definitions() -> None:
    result = evaluate_task_metrics(
        success_metrics=(
            "score",
            "final_assay_score",
            "sample_efficiency",
            "trajectory_validity",
            "constraint_violations",
            "validator_use",
        ),
        records=_records(),
        threshold=0.75,
    )

    values = {
        metric: row["value"] for metric, row in result["metrics"].items()
    }
    assert values == {
        "score": 0.8,
        "final_assay_score": 0.8,
        "sample_efficiency": 0.5,
        "trajectory_validity": 1.0,
        "constraint_violations": 0.0,
        "validator_use": 0.5,
    }
    assert result["all_required_inputs_present"] is True


def test_external_endpoint_inputs_fail_openly_then_evaluate() -> None:
    metrics = (
        "mechanism_explanation",
        "failure_analysis",
        "uncertainty",
        "local_model_quality",
        "public_private_gap",
        "rank_confidence",
    )
    missing = evaluate_task_metrics(
        success_metrics=metrics,
        records=_records(),
        threshold=0.75,
        bootstrap_samples=100,
    )
    assert missing["all_declared_metrics_implemented"] is True
    assert missing["all_required_inputs_present"] is False
    assert all(
        row["evaluation_status"] == "not_evaluated_missing_input"
        for row in missing["metrics"].values()
    )

    evaluated = evaluate_task_metrics(
        success_metrics=metrics,
        records=_records(),
        threshold=0.75,
        structured_artifact={
            "hypothesis": "temperature changes selectivity and degradation",
            "learned_mechanism": "catalyst and solvent interact",
            "failure_analysis": (
                "The cause is limited evidence; next experiment should mitigate uncertainty."
            ),
            "limitations": "uncertainty from limited measurements",
            "next_experiment": "validate with a new experiment",
            "evidence_ids": ["step-1", "step-2"],
        },
        predictive_holdout={
            "targets": [0.2, 0.8],
            "predictive_means": [0.25, 0.75],
            "predictive_standard_deviations": [0.1, 0.1],
        },
        paired_split={
            "public_scores_by_method": {
                "a": [0.8, 0.7, 0.9],
                "b": [0.5, 0.6, 0.4],
            },
            "private_scores_by_method": {
                "a": [0.75, 0.65, 0.85],
                "b": [0.45, 0.55, 0.35],
            },
        },
        bootstrap_samples=100,
        bootstrap_seed=7,
    )
    assert evaluated["all_required_inputs_present"] is True
    assert evaluated["metrics"]["rank_confidence"]["value"] == pytest.approx(1.0)
    assert evaluated["metrics"]["public_private_gap"]["value"] == pytest.approx(0.05)
    assert evaluated["metrics"]["local_model_quality"]["value"] > 0.9
    assert evaluated["metrics"]["mechanism_explanation"]["value"] > 0.5


def test_terminal_observation_endpoint_rejects_absent_declared_value() -> None:
    with pytest.raises(ValueError, match="does not expose declared metric"):
        evaluate_task_metrics(
            success_metrics=("purity",),
            records=_records(),
            threshold=0.75,
        )
