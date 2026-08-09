from __future__ import annotations

import pytest

from chemworld.eval.work_ii_analysis import (
    WorkIIAnalysisError,
    correction_contrast,
    score_prediction_error,
)


def _predictions() -> list[dict[str, object]]:
    return [
        {
            "query_id": "q1",
            "metrics": [
                {
                    "metric_id": "yield",
                    "mean": 0.7,
                    "interval_lower": 0.6,
                    "interval_upper": 0.8,
                    "confidence": 0.8,
                },
                {
                    "metric_id": "risk",
                    "mean": 0.2,
                    "interval_lower": 0.1,
                    "interval_upper": 0.3,
                    "confidence": 0.7,
                },
            ],
        }
    ]


def test_prediction_error_is_unclipped_normalized_mae() -> None:
    result = score_prediction_error(
        _predictions(),
        {"q1": {"yield": 0.9, "risk": 0.1}},
        metric_scales={"yield": 0.5, "risk": 1.0},
    )
    assert result.term_count == 2
    assert result.error == pytest.approx((0.4 + 0.1) / 2.0)


def test_prediction_error_fails_closed_on_missing_or_duplicate_terms() -> None:
    with pytest.raises(WorkIIAnalysisError, match="exactly match"):
        score_prediction_error(_predictions(), {"q2": {"yield": 0.9}})
    duplicated = _predictions() * 2
    with pytest.raises(WorkIIAnalysisError, match="unique"):
        score_prediction_error(duplicated, {"q1": {"yield": 0.9, "risk": 0.1}})


def test_primary_contrast_and_missing_final_rule_are_frozen() -> None:
    result = correction_contrast(
        misindexed_pre=0.8,
        misindexed_final=0.3,
        aligned_pre=0.2,
        aligned_final=0.1,
    )
    assert result.misindexed_improvement == pytest.approx(0.5)
    assert result.aligned_improvement == pytest.approx(0.1)
    assert result.primary_contrast == pytest.approx(0.4)

    missing = correction_contrast(
        misindexed_pre=0.8,
        misindexed_final=None,
        aligned_pre=0.2,
        aligned_final=0.1,
    )
    assert missing.misindexed_improvement == 0.0
    assert missing.primary_contrast == pytest.approx(-0.1)
