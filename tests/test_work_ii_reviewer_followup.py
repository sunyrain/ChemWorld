from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_reviewer_followup import (
    B3_ARMS,
    B3_METRIC_IDS,
    _apply_shared_truth_noise,
    b3_output_schema,
    build_b3_candidate_queries,
    select_b3_rosters,
    summarize_b3_results,
    validate_b3_payload,
)


def _protocol() -> dict:
    path = Path("configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_shared_truth_noise_pairs_all_queries_without_mutating_source_plan() -> None:
    plan = {
        "queries": [
            {
                "query_id": "a",
                "observation_seed": 1,
                "observation_coordinate_sha256": "a" * 64,
            },
            {
                "query_id": "b",
                "observation_seed": 2,
                "observation_coordinate_sha256": "b" * 64,
            },
        ],
        "plan_sha256": "c" * 64,
    }
    paired = _apply_shared_truth_noise(
        plan,
        shared_observation_seed=123,
        world_seed=9,
    )

    assert [query["observation_seed"] for query in paired["queries"]] == [123, 123]
    assert len(
        {query["observation_coordinate_sha256"] for query in paired["queries"]}
    ) == 1
    assert plan["queries"][0]["observation_seed"] == 1
    assert paired["truth_noise_pairing"]["world_seed"] == 9
    assert paired["plan_sha256"] == canonical_json_sha256(
        {key: value for key, value in paired.items() if key != "plan_sha256"}
    )


def _paired_fixture(candidates: list[dict]) -> dict:
    paired = {}
    for seed in range(5):
        linear = {}
        power = {}
        for query in candidates:
            features = query["feature_values"]
            solvent = int(features["solvent"])
            extractant = int(features["extractant"])
            volume_index = int(str(query["query_id"]).split("-v")[1].split("-")[0])
            mixing_index = int(str(query["query_id"]).rsplit("-m", maxsplit=1)[1])
            baseline = 0.20 + 0.01 * solvent + 0.008 * extractant + seed * 0.001
            linear[str(query["query_id"])] = {
                "product_in_organic": baseline,
                "product_in_aqueous": 0.45 - baseline / 2.0,
                "phase_ratio": 0.40 + volume_index * 0.02,
                "score": 0.10
                + 0.01 * (solvent + extractant)
                + 0.03 * volume_index
                + 0.04 * mixing_index
                + seed * 0.001,
            }
            power[str(query["query_id"])] = {
                "product_in_organic": baseline + 0.06,
                "product_in_aqueous": 0.45 - baseline / 2.0 - 0.04,
                "phase_ratio": 0.46 + volume_index * 0.02,
                "score": linear[str(query["query_id"])]["score"] + 0.02,
            }
        paired[seed] = {"linear": linear, "power": power}
    return paired


def _payload(queries: list[dict], stage: str) -> dict:
    payload = {
        "status": f"{stage}_submission_complete",
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
    }
    if stage == "post":
        payload["selected_action_query_id"] = queries[0]["query_id"]
        payload["evidence_assessment"] = "Evidence supports the power response."
    return payload


def test_b3_candidate_grid_and_roster_cover_identifiable_pairs_and_actions() -> None:
    candidates = build_b3_candidate_queries(_protocol())
    assert len(candidates) == 128
    assert len({query["pair_id"] for query in candidates}) == 16
    roster = select_b3_rosters(
        candidates,
        _paired_fixture(candidates),
        action_gain_threshold=0.02,
    )
    assert len(roster["evidence_queries"]) == 8
    assert len(roster["scoring_queries"]) == 8
    assert roster["evidence_pair_count"] >= 4
    assert roster["scoring_pair_count"] >= 4
    assert set(roster["evidence_query_ids"]).isdisjoint(roster["scoring_query_ids"])
    assert all(row["improving_query_ids"] for row in roster["development_action_checks"])
    assert all(
        len(row["nonimproving_query_ids"]) >= 2
        for row in roster["development_action_checks"]
    )


def test_b3_schema_keeps_family_exponent_typed_law_prediction_and_action_separate() -> None:
    queries = build_b3_candidate_queries(_protocol())[:8]
    schema = b3_output_schema(queries, stage="post")
    assert "selected_action_query_id" in schema["required"]
    assert set(schema["properties"]["mechanism_family"]["enum"]) == {
        "FAMILY_A_LINEAR",
        "FAMILY_B_POWER",
        "FAMILY_C_SATURATING",
        "FAMILY_D_CONSTANT",
    }
    payload = _payload(queries, "post")
    assert validate_b3_payload(payload, queries, stage="post") == []
    payload["typed_law"]["reference_exponent"] = 1.0
    assert "typed-law exponent differs" in "; ".join(
        validate_b3_payload(payload, queries, stage="post")
    )


def test_b3_summary_scores_structural_recovery_and_novel_action() -> None:
    queries = build_b3_candidate_queries(_protocol())[:8]
    cells = []
    results = []
    scoring_truth = {
        query["query_id"]: dict.fromkeys(B3_METRIC_IDS, 0.5) for query in queries
    }
    for world_seed in range(5):
        for arm in B3_ARMS:
            cell_id = f"world-{world_seed}--{arm}"
            cells.append({"cell_id": cell_id})
            pre = _payload(queries, "pre")
            post = _payload(queries, "post")
            results.append(
                {
                    "status": "completed",
                    "cell_id": cell_id,
                    "cluster_id": f"world-{world_seed}",
                    "world_seed": world_seed,
                    "arm": arm,
                    "pre_submission": deepcopy(pre),
                    "post_submission": deepcopy(post),
                    "scores": {
                        "pre": {"mean_normalized_absolute_error": 0.1},
                        "post": {"mean_normalized_absolute_error": 0.02},
                    },
                    "selected_action": {
                        "true_score": scoring_truth[queries[0]["query_id"]]["score"] + 0.03,
                        "evidence_incumbent_score": scoring_truth[queries[0]["query_id"]]["score"],
                    },
                }
            )
    summary = summarize_b3_results(
        {"study_id": "fixture", "cells": cells, "scoring_term_count": 32},
        results,
    )
    assert summary["status"] == "completed"
    assert summary["complete_cluster_count"] == 5
    assert summary["by_arm"]["misindexed_nominal"]["exact_family_recovery_count"] == 5
    assert summary["by_arm"]["opaque"]["action_gain_at_least_0_02_count"] == 5
