from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.work_ii_b4_decision import (
    RETAIN_INCUMBENT,
    _select_ranked_actions,
    b4_output_schema,
    evaluate_b4_decision,
    validate_b4_payload,
)
from chemworld.eval.work_ii_reviewer_followup import (
    B3_METRIC_IDS,
    build_b3_candidate_queries,
)


def _grid_protocol() -> dict:
    path = Path("configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _payload(queries: list[dict], *, decision: str = "execute_candidate") -> dict:
    selected = queries[0]["query_id"] if decision == "execute_candidate" else RETAIN_INCUMBENT
    return {
        "status": "post_submission_complete",
        "mechanism_family": "FAMILY_B_POWER",
        "estimated_reference_exponent": 1.75,
        "confidence": 0.8,
        "typed_law": {
            "law_type": "reference_coefficient_power",
            "mechanism_family": "FAMILY_B_POWER",
            "reference_exponent": 1.75,
        },
        "predictions": [
            {
                "query_id": query["query_id"],
                "metrics": dict.fromkeys(B3_METRIC_IDS, 0.5),
            }
            for query in queries
        ],
        "model_summary": "Power response.",
        "decision_type": decision,
        "selected_action_query_id": selected,
        "evidence_assessment": "Evidence supports the power response.",
    }


def test_b4_rank_generator_spans_pool_and_nominal_pairs() -> None:
    candidates = build_b3_candidate_queries(_grid_protocol())
    truth = {
        query["query_id"]: {
            "product_in_organic": 0.5,
            "product_in_aqueous": 0.2,
            "phase_ratio": 0.8,
            "score": 1.0 - index / 200.0,
        }
        for index, query in enumerate(candidates)
    }
    selected = _select_ranked_actions(
        candidates[:120],
        truth,
        [1, 18, 35, 52, 69, 86, 103, 120],
        minimum_pair_count=4,
    )
    assert len(selected) == 8
    assert len({row["query"]["pair_id"] for row in selected}) >= 4
    assert selected[0]["pool_rank"] == 1
    assert {row["target_rank_position"] for row in selected} == {
        1,
        18,
        35,
        52,
        69,
        86,
        103,
        120,
    }


def test_b4_schema_and_validation_bind_execute_or_retain_decision() -> None:
    queries = build_b3_candidate_queries(_grid_protocol())[:8]
    schema = b4_output_schema(queries, stage="post")
    assert RETAIN_INCUMBENT in schema["properties"]["selected_action_query_id"]["enum"]
    execute = _payload(queries)
    assert validate_b4_payload(execute, queries, stage="post") == []
    retain = _payload(queries, decision="retain_incumbent")
    assert validate_b4_payload(retain, queries, stage="post") == []
    retain["selected_action_query_id"] = queries[0]["query_id"]
    assert "must use RETAIN_INCUMBENT" in "; ".join(
        validate_b4_payload(retain, queries, stage="post")
    )


def test_b4_decision_evaluator_scores_regret_and_correct_abstention() -> None:
    queries = build_b3_candidate_queries(_grid_protocol())[:8]
    truth = {
        query["query_id"]: {
            "product_in_organic": 0.5,
            "product_in_aqueous": 0.2,
            "phase_ratio": 0.8,
            "score": 0.60 - index * 0.01,
        }
        for index, query in enumerate(queries)
    }
    cell = {
        "scoring_truth": truth,
        "hidden_action_ranks": {
            query["query_id"]: index for index, query in enumerate(queries, start=1)
        },
        "evidence_incumbent_score": 0.65,
        "oracle_policy": "retain_incumbent",
    }
    result = evaluate_b4_decision(cell, _payload(queries, decision="retain_incumbent"))
    assert result["correct_abstention"] is True
    assert result["normalized_policy_regret"] == 0.0
    execute = evaluate_b4_decision(cell, _payload(queries))
    assert execute["false_execution"] is True
    assert execute["normalized_policy_regret"] > 0.0
