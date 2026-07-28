from __future__ import annotations

import copy

import pytest

from chemworld.agents.task_recipes import (
    electrochemical_recipe_parameters_from_unit_vector,
    electrochemical_recipe_unit_vector_from_parameters,
)
from chemworld.eval.electrochemical_predictive import (
    ELECTROCHEMICAL_STANDARDIZED_PREDICTIVE_VERSION,
    PREDICTIVE_DIRECTION_THRESHOLD,
    PREDICTIVE_QUERY_COUNT,
    SINGLE_STAGE_PREDICTIVE_QUERY_METRICS,
    STANDARDIZED_PREDICTIVE_ANCHOR_ID,
    STANDARDIZED_PREDICTIVE_INTERVENTIONS,
    STANDARDIZED_PREDICTIVE_REFERENCE_PARAMETERS,
    build_electrochemical_prediction_queries,
    build_standardized_electrochemical_prediction_queries,
    classify_metric_direction,
    parse_counterfactual_predictions,
    score_predictive_validation,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)


def test_standardized_prediction_queries_are_history_independent_and_frozen() -> None:
    queries = build_standardized_electrochemical_prediction_queries()

    assert STANDARDIZED_PREDICTIVE_ANCHOR_ID == "balanced-standardized-anchor-v0.1"
    assert [query.query_id for query in queries] == [
        "standardized-potential",
        "standardized-current",
        "standardized-electrolyte-profile",
    ]
    for query in queries:
        assert query.schema_version == ELECTROCHEMICAL_STANDARDIZED_PREDICTIVE_VERSION
        assert query.reference_experiment_index == -1
        assert query.reference_recipe_parameters == (
            STANDARDIZED_PREDICTIVE_REFERENCE_PARAMETERS
        )
        assert query.intervention_recipe_parameters == (
            STANDARDIZED_PREDICTIVE_INTERVENTIONS[query.intervention_variable]
        )


def test_single_stage_predictive_metrics_match_final_assay_field_names() -> None:
    assert SINGLE_STAGE_PREDICTIVE_QUERY_METRICS["potential_V"][0] == (
        "selective_product_yield"
    )
    assert SINGLE_STAGE_PREDICTIVE_QUERY_METRICS["current_mA"][0] == (
        "electrochemical_conversion"
    )
    queries = build_electrochemical_prediction_queries(
        [
            {
                "experiment_index": 0,
                "plan": {
                    "recipe_parameters": {
                        "electrolyte_profile": 0,
                        "solvent": 0,
                        "reagent_amount_mol": 0.010,
                        "potential_V": 0.8,
                        "current_mA": 180.0,
                        "duration_s": 2100.0,
                    }
                },
                "terminal_summary": {"leaderboard_score": 0.5},
            }
        ],
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    )
    assert queries[0].metric_ids[0] == "selective_product_yield"
    assert queries[1].metric_ids[0] == "electrochemical_conversion"


def _recipe(**updates: int | float) -> dict[str, int | float]:
    payload: dict[str, int | float] = {
        "electrolyte_profile": 0,
        "solvent": 0,
        "reagent_amount_mol": 0.010,
        "probe_potential_V": 0.90,
        "probe_current_mA": 45.0,
        "probe_duration_s": 420.0,
        "controlled_potential_V": 1.10,
        "controlled_current_mA": 65.0,
        "controlled_duration_s": 1500.0,
    }
    payload.update(updates)
    vector = electrochemical_recipe_unit_vector_from_parameters(payload)
    return electrochemical_recipe_parameters_from_unit_vector(vector)


def _history_item(
    experiment_index: int,
    score: float,
    recipe: dict[str, int | float],
) -> dict[str, object]:
    vector = electrochemical_recipe_unit_vector_from_parameters(recipe)
    return {
        "experiment_index": experiment_index,
        "plan": {
            "search_vector": [float(value) for value in vector],
            "recipe_parameters": copy.deepcopy(recipe),
        },
        "terminal_summary": {"leaderboard_score": score},
    }


def _predictions(queries: object) -> list[dict[str, object]]:
    return [
        {
            "query_id": query.query_id,
            "metric_predictions": [
                {
                    "metric_id": metric_id,
                    "direction": "increase",
                    "confidence": 0.7,
                }
                for metric_id in query.metric_ids
            ],
        }
        for query in queries
    ]


def test_predictive_queries_use_earliest_tied_incumbent_and_are_deterministic() -> None:
    history = [
        _history_item(0, 0.4, _recipe(electrolyte_profile=0)),
        _history_item(1, 0.8, _recipe(electrolyte_profile=1)),
        _history_item(2, 0.8, _recipe(electrolyte_profile=2)),
    ]

    first = build_electrochemical_prediction_queries(history)
    second = build_electrochemical_prediction_queries(copy.deepcopy(history))

    assert len(first) == PREDICTIVE_QUERY_COUNT
    assert first == second
    assert all(query.reference_experiment_index == 1 for query in first)
    explored = {
        tuple(sorted(item["plan"]["recipe_parameters"].items())) for item in history
    }
    for query in first:
        changed = {
            field
            for field in query.reference_recipe_parameters
            if query.reference_recipe_parameters[field]
            != query.intervention_recipe_parameters[field]
        }
        assert changed == {query.intervention_variable}
        assert tuple(sorted(query.intervention_recipe_parameters.items())) not in explored
        assert len(query.query_sha256) == 64


def test_predictive_query_generation_fails_when_one_factor_space_is_exhausted() -> None:
    history = [
        _history_item(
            profile,
            1.0 if profile == 0 else 0.1,
            _recipe(electrolyte_profile=profile),
        )
        for profile in range(4)
    ]

    with pytest.raises(ValueError, match="cannot construct an unseen valid intervention"):
        build_electrochemical_prediction_queries(history)


def test_counterfactual_prediction_parser_requires_exact_query_and_metric_coverage() -> None:
    queries = build_electrochemical_prediction_queries(
        [_history_item(0, 0.5, _recipe())]
    )
    payload = _predictions(queries)

    parsed = parse_counterfactual_predictions(payload, queries=queries)

    assert len(parsed) == PREDICTIVE_QUERY_COUNT
    missing_metric = copy.deepcopy(payload)
    missing_metric[0]["metric_predictions"].pop()
    with pytest.raises(ValueError, match="wrong metrics"):
        parse_counterfactual_predictions(missing_metric, queries=queries)
    duplicate_query = copy.deepcopy(payload)
    duplicate_query[1]["query_id"] = duplicate_query[0]["query_id"]
    with pytest.raises(ValueError, match="unique"):
        parse_counterfactual_predictions(duplicate_query, queries=queries)


@pytest.mark.parametrize(
    ("delta", "expected"),
    [
        (PREDICTIVE_DIRECTION_THRESHOLD, "increase"),
        (-PREDICTIVE_DIRECTION_THRESHOLD, "decrease"),
        (PREDICTIVE_DIRECTION_THRESHOLD - 1e-12, "no_material_change"),
        (-PREDICTIVE_DIRECTION_THRESHOLD + 1e-12, "no_material_change"),
    ],
)
def test_predictive_direction_threshold_boundaries(delta: float, expected: str) -> None:
    assert (
        classify_metric_direction(delta, PREDICTIVE_DIRECTION_THRESHOLD) == expected
    )


def test_predictive_scoring_rejects_metric_or_delta_tampering() -> None:
    queries = build_electrochemical_prediction_queries(
        [_history_item(0, 0.5, _recipe())]
    )
    predictions = parse_counterfactual_predictions(
        _predictions(queries),
        queries=queries,
    )
    results = [
        {
            "query_id": query.query_id,
            "query_sha256": query.query_sha256,
            "metric_results": [
                {
                    "metric_id": metric_id,
                    "reference_mean": 0.4,
                    "intervention_mean": 0.5,
                    "delta": 0.1,
                    "direction_threshold": query.direction_thresholds[metric_id],
                    "metric_source": query.metric_sources[metric_id],
                    "actual_direction": "increase",
                }
                for metric_id in query.metric_ids
            ],
        }
        for query in queries
    ]

    score = score_predictive_validation(predictions, results, queries=queries)

    assert score["prediction_count"] == 9
    assert score["directional_accuracy"] == pytest.approx(1.0)
    tampered = copy.deepcopy(results)
    tampered[0]["metric_results"][0]["delta"] = 0.2
    with pytest.raises(ValueError, match="delta does not match"):
        score_predictive_validation(predictions, tampered, queries=queries)
