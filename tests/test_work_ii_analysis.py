from __future__ import annotations

import pytest

from chemworld.eval.work_ii_analysis import (
    WorkIIAnalysisError,
    build_cluster_correction_record,
    correction_contrast,
    score_cell_checkpoint_errors,
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


def _snapshot(stage: str, mean: float) -> dict[str, object]:
    predictions = _predictions()
    predictions[0]["metrics"][0]["mean"] = mean
    predictions[0]["metrics"][0]["interval_lower"] = min(mean, 0.6)
    predictions[0]["metrics"][0]["interval_upper"] = max(mean, 0.9)
    return {"stage": stage, "predictions": predictions}


def test_cell_checkpoint_error_applies_censoring_and_missing_pre_rules() -> None:
    truth = {"q1": {"yield": 0.9, "risk": 0.1}}
    censored = score_cell_checkpoint_errors(
        {
            "belief_snapshots": [
                _snapshot("pre_evidence", 0.5),
                _snapshot("after_experiment_1", 0.8),
            ]
        },
        truth,
        terminal_state="right_censored",
    )
    assert censored["effective_pre_error"] == pytest.approx(0.25)
    assert censored["effective_final_error"] == pytest.approx(0.1)
    assert censored["primary_improvement"] == pytest.approx(0.15)
    assert censored["effective_final_stage"] == "after_experiment_1"

    missing_pre = score_cell_checkpoint_errors(
        {"belief_snapshots": [_snapshot("after_experiment_1", 0.8)]},
        truth,
        terminal_state="failed",
    )
    assert missing_pre["effective_pre_error"] is None
    assert missing_pre["effective_final_error"] is None
    assert missing_pre["primary_improvement"] == 0.0


def test_checkpoint_scoring_accepts_pattern_owned_snapshot_stages() -> None:
    truth = {"q1": {"yield": 0.9, "risk": 0.1}}
    stages = (
        "pre_evidence",
        "after_experiment_2",
        "after_experiment_4",
        "after_experiment_7",
        "final",
    )
    analysis = {
        "belief_snapshots": [
            _snapshot(stage, mean)
            for stage, mean in zip(stages, (0.5, 0.6, 0.7, 0.8, 0.9), strict=True)
        ]
    }

    report = score_cell_checkpoint_errors(
        analysis,
        truth,
        terminal_state="completed",
        snapshot_stages=stages,
    )

    assert report["scheduled_snapshot_count"] == 5
    assert list(report["checkpoint_scores"]) == list(stages)
    assert report["primary_improvement"] == pytest.approx(0.2)


def test_cluster_record_uses_retained_zero_improvement_cells() -> None:
    records = {
        "opaque": {"effective_pre_error": 0.5, "primary_improvement": 0.1},
        "aligned_nominal": {
            "effective_pre_error": 0.3,
            "primary_improvement": 0.05,
        },
        "misindexed_nominal": {
            "effective_pre_error": None,
            "primary_improvement": 0.0,
        },
    }
    cluster = build_cluster_correction_record(records)
    assert cluster["H1_prior_utility"] == pytest.approx(0.2)
    assert cluster["H2_prior_vulnerability"] is None
    assert cluster["H3_primary_contrast"] == pytest.approx(-0.05)
