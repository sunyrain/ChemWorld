from __future__ import annotations

from copy import deepcopy

from chemworld.eval.work_ii_terminal_schema_canary import (
    evaluate_terminal_payload,
    law_output_schema,
    summarize_canary,
    summarize_fixed_context_replay,
    terminal_output_schema,
    validate_law_payload,
    validate_terminal_payload,
)


def _queries() -> list[dict[str, object]]:
    return [
        {"query_id": f"q{index}", "metric_ids": ["a"]} for index in range(1, 9)
    ]


def _law() -> dict[str, object]:
    return {
        "status": "final_law_committed",
        "mechanism_family": "FAMILY_B_POWER",
        "estimated_reference_exponent": 1.75,
        "confidence": 0.8,
        "typed_law": {
            "law_type": "reference_coefficient_power",
            "mechanism_family": "FAMILY_B_POWER",
            "reference_exponent": 1.75,
        },
        "law_summary": "Power response supported by the fixed evidence.",
    }


def _terminal(condition: str) -> dict[str, object]:
    payload: dict[str, object] = {
        "status": "terminal_ranking_complete",
        "ranking": [f"q{index}" for index in range(1, 9)],
        "selected_action_query_id": "q1",
        "selection_confidence": 0.7,
        "mechanism_application": "The committed law orders the candidates.",
    }
    if condition == "full_32":
        payload["predictions"] = [
            {
                "query_id": f"q{index}",
                "metrics": {
                    "product_in_organic": 1.0 - index / 100.0,
                    "product_in_aqueous": index / 100.0,
                    "phase_ratio": 0.99,
                    "score": 1.0 - index / 100.0,
                },
            }
            for index in range(1, 9)
        ]
    return payload


def _cell() -> dict[str, object]:
    truth = {
        f"q{index}": {
            "product_in_organic": 1.0 - index / 100.0,
            "product_in_aqueous": index / 100.0,
            "phase_ratio": 0.99,
            "score": 1.0 - index / 100.0,
        }
        for index in range(1, 9)
    }
    return {
        "scoring_truth": truth,
        "hidden_action_ranks": {f"q{index}": index for index in range(1, 9)},
        "evidence_incumbent_score": 0.0,
        "oracle_policy": "execute_candidate",
    }


def test_schema_conditions_differ_only_by_terminal_predictions() -> None:
    law_schema = law_output_schema()
    assert "predictions" not in law_schema["properties"]
    full = terminal_output_schema(_queries(), condition="full_32")
    lean = terminal_output_schema(_queries(), condition="lean_ranking")
    assert "predictions" in full["required"]
    assert "predictions" not in lean["properties"]
    assert validate_law_payload(_law()) == []


def test_terminal_validation_requires_complete_ranking_and_condition_shape() -> None:
    assert validate_terminal_payload(
        _terminal("full_32"), _queries(), condition="full_32"
    ) == []
    assert validate_terminal_payload(
        _terminal("lean_ranking"), _queries(), condition="lean_ranking"
    ) == []
    invalid = deepcopy(_terminal("lean_ranking"))
    invalid["selected_action_query_id"] = "q2"
    assert "terminal selected action is not ranking[0]" in validate_terminal_payload(
        invalid, _queries(), condition="lean_ranking"
    )


def test_evaluation_scores_ranking_selection_and_full_prediction_only() -> None:
    full = evaluate_terminal_payload(_cell(), _terminal("full_32"), condition="full_32")
    lean = evaluate_terminal_payload(
        _cell(), _terminal("lean_ranking"), condition="lean_ranking"
    )
    assert full["selected_rank"] == 1
    assert full["ranking_kendall_tau"] == 1.0
    assert full["prediction_evaluation"]["term_count"] == 32
    assert "prediction_evaluation" not in lean


def test_summary_preserves_condition_denominators_and_matched_arms() -> None:
    results = []
    for arm in ("opaque", "aligned_nominal", "misindexed_nominal"):
        for condition in ("full_32", "lean_ranking"):
            terminal = _terminal(condition)
            results.append(
                {
                    "cell_id": f"{arm}-{condition}",
                    "arm": arm,
                    "condition": condition,
                    "status": "completed",
                    "terminal_evaluation": evaluate_terminal_payload(
                        _cell(), terminal, condition=condition
                    ),
                    "provider_receipts": [
                        {},
                        {
                            "elapsed_s": 1.0,
                            "usage": {
                                "output_tokens": 10,
                                "reasoning_output_tokens": 5,
                            },
                        },
                    ],
                }
            )
    summary = summarize_canary(results)
    assert summary["status"] == "completed"
    assert summary["by_condition"]["full_32"]["completed_session_count"] == 3
    assert summary["by_condition"]["lean_ranking"]["mean_prediction_mae"] is None
    assert len(summary["matched_arm_rows"]) == 3


def test_fixed_context_summary_pairs_replicates_without_arm_semantics() -> None:
    results = []
    for replicate in range(1, 4):
        for condition in ("full_32", "lean_ranking"):
            terminal = _terminal(condition)
            results.append(
                {
                    "cell_id": f"r{replicate}-{condition}",
                    "replicate": replicate,
                    "condition": condition,
                    "status": "completed",
                    "terminal_evaluation": evaluate_terminal_payload(
                        _cell(), terminal, condition=condition
                    ),
                    "provider_receipts": [
                        {
                            "elapsed_s": 1.0,
                            "usage": {
                                "output_tokens": 10,
                                "reasoning_output_tokens": 5,
                            },
                        }
                    ],
                }
            )
    summary = summarize_fixed_context_replay(results)
    assert summary["status"] == "completed"
    assert summary["fixed_reference_exponent"] == 1.75
    assert len(summary["paired_replicate_rows"]) == 3
