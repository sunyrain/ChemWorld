import json

from scripts.report_paper_case_stability import (
    describe,
    directional_comparison,
    measurements,
    seed_execution,
)


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


def test_equilibrium_reference_mean_errors_and_coverage_are_not_lost():
    row = {
        "system": "EQ",
        "prediction_evaluation": {
            "valid": True,
            "metrics": {
                "pH_normalized": {
                    "mae_to_five_repeat_mean": 0.012,
                    "empirical_coverage80": 0.95,
                    "mean_width80": 0.04,
                },
            },
        },
    }
    result = measurements(row)
    assert result["pH_normalized_mae"] == 0.012
    assert result["pH_normalized_coverage80"] == 0.95
    assert result["pH_normalized_mean_width80"] == 0.04


def test_rejected_seeding_is_not_counted_as_material_actually_added(tmp_path):
    rows = [
        {"action": {"operation": "seed_crystals", "seed_mass_g": 0.05},
         "experiment_index": 0, "transaction_status": status,
         "preconditions": {"payload_bounds:seed_mass_g": status == "committed"}}
        for status in ("committed", "validation_failed", "validation_failed")
    ]
    (tmp_path / "trajectory.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows), encoding="utf-8"
    )
    result = seed_execution(tmp_path)
    assert result["by_batch"] == [{"lifecycle_index": 1, "committed_calls": 1,
                                  "rejected_calls": 2, "committed_seed_additions_g": 0.05}]
    assert result["rejection_preconditions"] == {"payload_bounds:seed_mass_g": 2}
