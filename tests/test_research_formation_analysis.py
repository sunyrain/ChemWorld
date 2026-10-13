import pytest
from scripts import analyze_research_formation as analysis
from scripts.run_research_formation import cases, schedule


def test_world_contrasts_do_not_zero_impute_or_weight_worlds_by_available_sessions():
    rows = [{**r, "measurements": {}} for r in schedule()]
    for row in rows:
        if row["system"] != "EQ":
            continue
        value = None
        if row["world"] == "W01":
            value = 1 if row["arm"] == "Opaque" else 2
        elif row["world"] == "W02" and row["repeat"] == "repeat-01":
            value = 9 if row["arm"] == "Opaque" else 6
        row["measurements"]["lowest_three_macro_mae"] = value
    result = analysis.contrasts(rows, {"cases": cases()})["EQ"]["lowest_three_macro_mae"]
    assert result["equal_world_means"]["Opaque"]["mean"] == 5  # not pooled 3
    assert result["equal_world_means"]["Aligned"]["mean"] == 4
    assert result["world_mean_differences"]["mean"] == -1
    assert result["world_mean_differences"]["missing"] == 3
    assert result["complete_worlds"] == 1
    assert result["worlds"][1]["Opaque"]["observed"] == 1
    assert result["worlds"][1]["Opaque"]["sample_sd"] is None


def test_final_analysis_rejects_unfinished_block_before_export(tmp_path):
    analysis.write(tmp_path / "design.json", {})
    analysis.write(tmp_path / "summary.json", {"terminal_sources": 47, "active_units": [{}]})
    with pytest.raises(ValueError, match="48 terminal"):
        analysis.analyze(tmp_path, tmp_path / "reports", tmp_path / "final")
    assert not (tmp_path / "final").exists()


def test_quality_without_yield_is_not_counted_as_target_achievement():
    row = {
        "measurements": {"recommendation_true_crystal_yield": 0.0},
        "crystallization_quality": {"recommended_retest_feasible": True},
        "prediction_evaluation": {"valid": False},
    }
    result = analysis.enrich(row, None, {"system": "C"})
    assert result["measurements"]["recommendation_quality_feasible"] == 1
    assert result["measurements"]["recommendation_quality_and_yield_target"] == 0


def test_missing_recommendation_stays_missing():
    row = {
        "measurements": {},
        "prediction_evaluation": {"valid": False},
        "crystallization_quality": {"recommended_retest_feasible": None},
    }
    result = analysis.enrich(row, None, {"system": "C"})
    assert result["measurements"]["recommendation_quality_feasible"] is None
    assert result["measurements"]["recommendation_quality_and_yield_target"] is None
