import pytest
from scripts.analyze_work_ii_completed_pool import paired_summary, summarize_pairs


def test_influence_diagnostic_removes_whole_world_not_one_correlated_cell():
    pairs = [
        {"world": "W1", "first": 2, "second": 1},
        {"world": "W1", "first": 4, "second": 1},
        {"world": "W2", "first": 1, "second": 6},
        {"world": "W3", "first": 2, "second": 1},
    ]
    result = summarize_pairs(pairs)
    assert result["world_clusters"] == 3
    assert result["mean_difference"] == 0
    assert result["leave_one_world_out_difference_range"] == pytest.approx([-2, 5 / 3])


def test_conforming_sensitivity_excludes_the_complete_pair():
    result = paired_summary(
        [
            {"world": "W1", "first": 100, "second": 99, "conforming": False},
            {"world": "W2", "first": 2, "second": 5, "conforming": True},
        ]
    )
    assert result["all_scheduled"]["n"] == 2
    assert result["both_conforming"]["n"] == 1
    assert result["both_conforming"]["first_mean"] == 2
    assert result["both_conforming"]["second_mean"] == 5
    assert result["both_conforming"]["mean_difference"] == -3
