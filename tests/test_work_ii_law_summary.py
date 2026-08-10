from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.eval.work_ii_formal import EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT
from chemworld.eval.work_ii_law_summary import evaluate_final_law_summary


def _truth_plan() -> dict[str, object]:
    return {
        "law_summary_contract": {
            "allowed_feature_ids": ["x"],
            "allowed_metric_ids": ["yield"],
            "required_metric_ids": ["yield"],
            "evidence_catalog": [
                "experiment-1-final-assay",
                "experiment-2-final-assay",
                "experiment-3-final-assay",
                "experiment-4-final-assay",
            ],
        },
        "queries": [
            {"query_id": "q-low", "feature_values": {"x": 0.2}, "metric_ids": ["yield"]},
            {"query_id": "q-high", "feature_values": {"x": 0.8}, "metric_ids": ["yield"]},
        ],
    }


def _summary() -> dict[str, object]:
    return {
        "schema_version": "chemworld-work-ii-law-summary-0.1",
        "summary_id": "linear-yield-law",
        "feature_ids": ["x"],
        "metric_laws": [
            {
                "metric_id": "yield",
                "intercept": 0.0,
                "link": "identity",
                "lower_bound": 0.0,
                "upper_bound": 1.0,
                "terms": [
                    {
                        "term_id": "yield-x",
                        "basis": "linear",
                        "input_ids": ["x"],
                        "coefficient": 1.0,
                    }
                ],
            }
        ],
        "evidence_ids": ["experiment-1-final-assay"],
        "applicability": "registered x domain",
        "limitations": [],
        "confidence": 0.8,
    }


def _final_predictions() -> list[dict[str, object]]:
    return [
        {"query_id": "q-low", "metrics": [{"metric_id": "yield", "mean": 0.25}]},
        {"query_id": "q-high", "metrics": [{"metric_id": "yield", "mean": 0.75}]},
    ]


def test_final_law_summary_executes_and_scores_registered_queries() -> None:
    report = evaluate_final_law_summary(
        _summary(),
        truth_plan=_truth_plan(),
        evaluator_truth={"q-low": {"yield": 0.2}, "q-high": {"yield": 0.8}},
        final_checkpoint_predictions=_final_predictions(),
        effective_pre_error=0.4,
        effective_final_error=0.05,
        evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    )

    assert report["status"] == "evaluated"
    assert report["evaluator_executability_status"] == "passed_registered_query_execution"
    assert report["normalized_mae"] == pytest.approx(0.0)
    assert report["pre_to_law_summary_improvement"] == pytest.approx(0.4)
    assert report["summary_minus_effective_final_error"] == pytest.approx(-0.05)
    assert report["prediction_consistency_normalized_mae"] == pytest.approx(0.05)
    assert report["registered_query_metric_count"] == 2


def test_missing_final_law_summary_is_retained_without_imputation() -> None:
    report = evaluate_final_law_summary(
        None,
        truth_plan=_truth_plan(),
        evaluator_truth={"q-low": {"yield": 0.2}, "q-high": {"yield": 0.8}},
        final_checkpoint_predictions=_final_predictions(),
        effective_pre_error=0.4,
        effective_final_error=0.05,
        evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    )

    assert report["status"] == "missing_final_law_summary"
    assert report["normalized_mae"] is None
    assert report["evaluator_executability_status"].startswith("not_evaluated")


def test_law_summary_with_unknown_feature_fails_closed() -> None:
    summary = deepcopy(_summary())
    summary["feature_ids"] = ["unknown"]
    summary["metric_laws"][0]["terms"][0]["input_ids"] = ["unknown"]
    report = evaluate_final_law_summary(
        summary,
        truth_plan=_truth_plan(),
        evaluator_truth={"q-low": {"yield": 0.2}, "q-high": {"yield": 0.8}},
        final_checkpoint_predictions=_final_predictions(),
        effective_pre_error=0.4,
        effective_final_error=0.05,
        evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    )

    assert report["status"] == "law_summary_evaluation_failed"
    assert report["evaluator_executability_status"] == "failed_registered_query_execution"
    assert "unknown feature" in report["evaluation_error"]


def test_law_summary_error_remains_evaluable_when_final_predictions_are_missing() -> None:
    report = evaluate_final_law_summary(
        _summary(),
        truth_plan=_truth_plan(),
        evaluator_truth={"q-low": {"yield": 0.3}, "q-high": {"yield": 0.7}},
        final_checkpoint_predictions=None,
        effective_pre_error=None,
        effective_final_error=None,
        evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    )

    assert report["status"] == "evaluated"
    assert report["normalized_mae"] == pytest.approx(0.1)
    assert report["prediction_consistency_normalized_mae"] is None
    assert report["pre_to_law_summary_improvement"] is None
