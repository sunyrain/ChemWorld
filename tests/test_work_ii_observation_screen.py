from __future__ import annotations

from typing import Any

import pytest

from chemworld.eval.work_ii_observation_screen import (
    analyze_observation_world,
    observation_queries,
    screen_specs,
    truth_queries,
)


def _base_metrics(screen_id: str, level: int) -> dict[str, float]:
    if screen_id == "electrochemical_observation":
        return {
            "selective_product_yield": 0.15 + 0.25 * level,
            "faradaic_efficiency": 0.85 - 0.25 * level,
            "transport_efficiency": 0.90 - 0.25 * level,
            "ohmic_efficiency": 0.75,
            "energy_efficiency": 0.70 - 0.05 * level,
            "safety_risk": 0.10,
            "score": 0.50 + 0.05 * level,
        }
    return {
        "crystal_yield": 0.40 + 0.10 * level,
        "crystal_size": 0.45 + 0.10 * level,
        "crystal_csd_quality": 0.30 + 0.20 * level,
        "crystal_fines_fraction": 0.70 - 0.20 * level,
        "score": 0.45 + 0.05 * level,
    }


def _synthetic_rows(screen_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    noisy = []
    offsets = (-0.005, 0.0, 0.005)
    for query in observation_queries(screen_id):
        level = int(query["level_index"])
        offset = offsets[int(query["replicate"]) - 1]
        noisy.append(
            {
                **query,
                "status": "completed",
                "safe": True,
                "exact_replay": True,
                "metrics": {
                    key: value + offset for key, value in _base_metrics(screen_id, level).items()
                },
            }
        )
    truth = [
        {
            **query,
            "status": "completed",
            "safe": True,
            "exact_replay": True,
            "metrics": _base_metrics(screen_id, int(query["level_index"])),
        }
        for query in truth_queries(screen_id)
    ]
    return noisy, truth


@pytest.mark.parametrize("screen_id", list(screen_specs()))
def test_observation_screen_accepts_visible_effect_with_small_unbiased_noise(
    screen_id: str,
) -> None:
    noisy, truth = _synthetic_rows(screen_id)

    result = analyze_observation_world(screen_id, noisy, truth)

    assert result["passed"] is True
    assert result["denominators"] == {
        "noisy_attempted": 9,
        "truth_attempted": 3,
        "completed": 12,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
        "exact_replay": 12,
    }
    assert result["metric_reports"][result["best_effect_metric"]]["effect_passed"] is True


def test_observation_screen_rejects_platform_failure() -> None:
    noisy, truth = _synthetic_rows("electrochemical_observation")
    noisy[0]["status"] = "platform_failure"
    noisy[0]["exact_replay"] = False

    result = analyze_observation_world("electrochemical_observation", noisy, truth)

    assert result["passed"] is False
    assert "all_noisy_completed" in result["failures"]
    assert "zero_platform_failures" in result["failures"]
