from scripts.report_paper_case_stability import describe, directional_comparison, measurements


def test_missing_repeat_is_not_imputed_or_counted_as_independent_query():
    result = describe([1.0, None, 3.0])
    assert result["planned"] == 3 and result["observed"] == 2 and result["missing"] == 1
    assert result["mean"] == 2.0
    assert abs(result["sample_sd"] - 2**0.5) < 1e-10
    assert describe([None, None, None])["mean"] is None
    assert describe([1, None, None])["sample_sd"] is None


def test_invalid_prediction_does_not_become_perfect_quality_or_zero_error():
    row = {
        "system": "C",
        "prediction_evaluation": {
            "valid": False,
            "quality": {"true_positive": 3, "true_negative": 4},
            "metrics": {"crystal_purity": {"mae": 0.0}},
        },
    }
    result = measurements(row)
    assert result["quality_correct_of_12"] is None
    assert "crystal_purity_mae" not in result
    assert result["recommendation_fines_margin"] is None


def test_directional_counts_keep_missing_repeats_and_strict_ties():
    rows = {}
    for repeat, a, b in (("repeat-01", 1, 2), ("repeat-02", 1, 1), ("repeat-03", 1, None)):
        rows[(repeat, "A")] = {"measurements": {"score": a}}
        rows[(repeat, "B")] = {"measurements": {"score": b}}
    result = directional_comparison(rows, "A", "B", "score", True)
    assert result["holds"] == 1 and result["observed"] == 2 and result["planned"] == 3
    assert result["by_repeat"]["repeat-03"] is None
