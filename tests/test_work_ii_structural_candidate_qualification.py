from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from chemworld.eval.work_ii_structural_candidate_qualification import (
    analyze_candidate_world,
    build_prior_arms,
    candidate_specs,
    registered_queries,
    validation_groups,
)


def _rows(
    candidate_id: str,
    metric_function: Callable[[int, int], dict[str, float]],
) -> list[dict[str, Any]]:
    rows = []
    for query in registered_queries(candidate_id):
        metrics = metric_function(
            int(query["axis_a_index"]), int(query["axis_b_index"])
        )
        rows.append(
            {
                **query,
                "status": "completed",
                "safe": True,
                "metrics": metrics,
                "exact_replay": True,
            }
        )
    return rows


def _electrochemical_metrics(axis_a: int, axis_b: int) -> dict[str, float]:
    potential = float(axis_a - 1)
    current = float(axis_b - 1)
    return {
        "selective_product_yield": 0.55 + 0.08 * potential + 0.12 * current - 0.09 * current**2,
        "faradaic_efficiency": 0.78 + 0.04 * potential - 0.05 * current - 0.11 * current**2,
        "transport_efficiency": 0.75 - 0.04 * current - 0.14 * current**2,
        "ohmic_efficiency": 0.72 - 0.05 * potential,
        "energy_efficiency": 0.68 - 0.03 * potential - 0.04 * current,
        "safety_risk": 0.10,
        "score": 0.62 + 0.03 * potential - 0.02 * current**2,
    }


def _crystallization_metrics(axis_a: int, axis_b: int) -> dict[str, float]:
    seed = float(axis_a - 1)
    cooling = float(axis_b - 1)
    return {
        "crystal_yield": 0.55 + 0.05 * seed + 0.12 * cooling,
        "crystal_size": 0.60 + 0.09 * seed + 0.04 * cooling,
        "crystal_csd_quality": 0.62 + 0.12 * seed + 0.08 * seed * cooling,
        "crystal_fines_fraction": 0.30 - 0.11 * seed - 0.07 * seed * cooling,
        "score": 0.58 + 0.05 * seed + 0.06 * cooling,
    }


@pytest.mark.parametrize(
    ("candidate_id", "metric_function"),
    [
        ("electrochemical_transport", _electrochemical_metrics),
        ("crystallization_nucleation_growth", _crystallization_metrics),
    ],
)
def test_frozen_design_and_analysis_pass_structurally_distinct_surfaces(
    candidate_id: str,
    metric_function: Callable[[int, int], dict[str, float]],
) -> None:
    queries = registered_queries(candidate_id)
    assert len(queries) == 18
    assert sum(query["phase"] == "main_grid" for query in queries) == 9
    assert sum(query["phase"] == "noisy_validation" for query in queries) == 9
    observed_groups = {
        (int(query["axis_a_index"]), int(query["axis_b_index"]))
        for query in queries
        if query["phase"] == "noisy_validation"
    }
    assert observed_groups == set(validation_groups(candidate_id))

    result = analyze_candidate_world(candidate_id, _rows(candidate_id, metric_function))

    assert result["passed"] is True
    assert result["denominators"] == {
        "attempted": 18,
        "completed": 18,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
        "exact_replay": 18,
    }
    assert result["model_qualification"]["disagreement_fraction"] >= 0.40
    assert result["model_qualification"]["blind_identified_aligned_model"] is True


def test_platform_failure_is_not_accepted_as_a_physical_outcome() -> None:
    rows = _rows("electrochemical_transport", _electrochemical_metrics)
    rows[0].update(
        {
            "status": "platform_failure",
            "attribution": "platform_defect_candidate",
            "exact_replay": False,
        }
    )

    result = analyze_candidate_world("electrochemical_transport", rows)

    assert result["passed"] is False
    assert "zero_platform_failures" in result["failures"]
    assert "all_exact_replay" in result["failures"]
    assert result["denominators"]["platform_failures"] == 1


def test_prior_arms_match_schema_and_confidence() -> None:
    for candidate_id in candidate_specs():
        priors = build_prior_arms(candidate_id)
        aligned = priors["aligned_nominal"]
        misspecified = priors["misindexed_nominal"]
        assert set(aligned) == set(misspecified)
        assert aligned["confidence"] == misspecified["confidence"] == 0.70
        assert aligned["claim"] != misspecified["claim"]
