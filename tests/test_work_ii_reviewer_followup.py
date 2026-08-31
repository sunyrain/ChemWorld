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
    build_b3_manifest,
    evaluate_b3_selected_action,
    resolve_b3_selected_action_query_id,
    select_b3_rosters,
    summarize_b3_canary_closeout,
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


def test_b3_shared_index_schema_resolves_only_visible_zero_based_actions() -> None:
    queries = build_b3_candidate_queries(_protocol())[:8]
    schema = b3_output_schema(
        queries,
        stage="post",
        action_selection_encoding="zero_based_index",
    )
    assert "selected_action_index" in schema["required"]
    assert "selected_action_query_id" not in schema["properties"]
    assert schema["properties"]["selected_action_index"]["enum"] == list(range(8))

    payload = _payload(queries, "post")
    payload.pop("selected_action_query_id")
    payload["selected_action_index"] = 3
    assert (
        validate_b3_payload(
            payload,
            queries,
            stage="post",
            action_selection_encoding="zero_based_index",
        )
        == []
    )
    assert resolve_b3_selected_action_query_id(
        payload,
        queries,
        action_selection_encoding="zero_based_index",
    ) == str(queries[3]["query_id"])

    missing_assessment = deepcopy(payload)
    missing_assessment.pop("evidence_assessment")
    assert "post evidence assessment is invalid" in validate_b3_payload(
        missing_assessment,
        queries,
        stage="post",
        action_selection_encoding="zero_based_index",
    )

    invalid_summary = deepcopy(payload)
    invalid_summary["model_summary"] = 3
    assert "post model summary is invalid" in validate_b3_payload(
        invalid_summary,
        queries,
        stage="post",
        action_selection_encoding="zero_based_index",
    )

    payload["selected_action_index"] = True
    assert "post selected action index is invalid" in validate_b3_payload(
        payload,
        queries,
        stage="post",
        action_selection_encoding="zero_based_index",
    )


def test_b3_runner_derived_stage_ignores_redundant_participant_status() -> None:
    queries = build_b3_candidate_queries(_protocol())[:8]
    schema = b3_output_schema(
        queries,
        stage="post",
        stage_status_encoding="runner_derived",
    )
    assert "status" not in schema["properties"]
    assert "status" not in schema["required"]

    payload = _payload(queries, "post")
    payload["status"] = "pre_submission_complete"
    assert (
        validate_b3_payload(
            payload,
            queries,
            stage="post",
            stage_status_encoding="runner_derived",
        )
        == []
    )


def test_b3_summary_scores_structural_recovery_and_novel_action() -> None:
    queries = build_b3_candidate_queries(_protocol())[:8]
    cells = []
    results = []
    scoring_truth = {
        query["query_id"]: {
            **dict.fromkeys(B3_METRIC_IDS, 0.5),
            "score": 0.8 - 0.05 * query_index,
        }
        for query_index, query in enumerate(queries)
    }
    for world_seed in range(5):
        for arm in B3_ARMS:
            cell_id = f"world-{world_seed}--{arm}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "cluster_id": f"world-{world_seed}",
                    "scoring_truth": scoring_truth,
                    "evidence_incumbent_score": 0.7,
                    "action_opportunity_eligible": True,
                    "action_opportunity_threshold": 0.02,
                }
            )
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
                        "true_score": scoring_truth[queries[0]["query_id"]]["score"],
                        "evidence_incumbent_score": 0.7,
                    },
                }
            )
    summary = summarize_b3_results(
        {
            "study_id": "fixture",
            "cells": cells,
            "cluster_packets": [
                {
                    "cluster_id": f"world-{world_seed}",
                    "action_opportunity_eligible": True,
                }
                for world_seed in range(5)
            ],
            "scoring_term_count": 32,
        },
        results,
    )
    assert summary["status"] == "completed"
    assert summary["complete_cluster_count"] == 5
    assert summary["by_arm"]["misindexed_nominal"]["exact_family_recovery_count"] == 5
    assert summary["by_arm"]["opaque"]["action_gain_at_least_0_02_count"] == 5
    assert summary["by_arm"]["opaque"]["top1_selected_count"] == 5
    assert summary["by_arm"]["opaque"]["mean_normalized_regret"] == 0.0
    assert summary["all_world_rank_regret_cell_denominator"] == 15
    assert summary["action_opportunity_eligible_gain_cell_denominator"] == 15


def test_b3_action_scoring_reports_rank_regret_and_opportunity_separately() -> None:
    cell = {
        "scoring_truth": {
            "a": {"score": 0.9},
            "b": {"score": 0.7},
            "c": {"score": 0.5},
        },
        "evidence_incumbent_score": 0.89,
        "action_opportunity_eligible": False,
        "action_opportunity_threshold": 0.02,
    }
    scored = evaluate_b3_selected_action(cell, "b")
    assert scored["selected_true_rank"] == 2
    assert scored["top1_selected"] is False
    assert abs(scored["raw_regret"] - 0.2) < 1.0e-12
    assert abs(scored["normalized_regret"] - 0.5) < 1.0e-12
    assert abs(scored["maximum_available_action_gain"] - 0.01) < 1.0e-12
    assert scored["action_opportunity_eligible"] is False


def test_b3_manifest_supports_nested_provider_replicates(tmp_path: Path) -> None:
    protocol = _protocol()
    protocol["study_id"] = "replicated-fixture"
    protocol["execution"] = {
        "replicates_per_arm": 2,
        "formal_sessions": 30,
        "canary_sessions": 3,
    }
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    output = tmp_path / "prepared"
    output.mkdir()
    source = (
        Path(__file__).resolve().parents[1]
        / "runs/formal/work-ii-as-study-b3-identifiable-law-action-v0.1-20260815"
    )
    for name in ("frozen_roster.json", "qualification_summary.json", "public_truth_manifest.json"):
        (output / name).write_bytes((source / name).read_bytes())
    public_truth_path = output / "public_truth_manifest.json"
    public_truth = json.loads(public_truth_path.read_text(encoding="utf-8"))
    public_truth["status"] = "preflight_passed"
    public_truth_path.write_text(json.dumps(public_truth), encoding="utf-8")
    manifest = build_b3_manifest(
        protocol_path,
        repository_root=tmp_path,
        output_root=output,
    )
    assert manifest["cell_count"] == 30
    assert manifest["replicate_block_count"] == 10
    assert {cell["replicate_index"] for cell in manifest["cells"]} == {1, 2}
    assert len({cell["cell_id"] for cell in manifest["cells"]}) == 30
    assert all(len(cell["hidden_action_ranks"]) == 8 for cell in manifest["cells"])
    assert all("action_opportunity_eligible" in cell for cell in manifest["cells"])


def test_b3_manifest_materializes_shared_action_indices_without_truth_drift(
    tmp_path: Path,
) -> None:
    protocol = _protocol()
    protocol["study_id"] = "shared-index-fixture"
    protocol["action_selection_encoding"] = "zero_based_index"
    protocol["execution"] = {
        "replicates_per_arm": 2,
        "formal_sessions": 30,
        "canary_sessions": 3,
    }
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    output = tmp_path / "prepared"
    output.mkdir()
    source = (
        Path(__file__).resolve().parents[1]
        / "runs/formal/work-ii-as-study-b3-identifiable-law-action-v0.1-20260815"
    )
    for name in ("frozen_roster.json", "qualification_summary.json", "public_truth_manifest.json"):
        (output / name).write_bytes((source / name).read_bytes())
    public_truth_path = output / "public_truth_manifest.json"
    public_truth = json.loads(public_truth_path.read_text(encoding="utf-8"))
    public_truth["status"] = "preflight_passed"
    public_truth_path.write_text(json.dumps(public_truth), encoding="utf-8")

    manifest = build_b3_manifest(
        protocol_path,
        repository_root=tmp_path,
        output_root=output,
    )
    first_queries = manifest["cells"][0]["public_packet"]["scoring_action_queries"]
    assert manifest["action_selection_encoding"] == "zero_based_index"
    assert [query["action_index"] for query in first_queries] == list(range(8))
    assert set(manifest["cells"][0]["scoring_truth"]) == {
        query["query_id"] for query in first_queries
    }
    assert all(
        cell["action_selection_encoding"] == "zero_based_index"
        for cell in manifest["cells"]
    )


def test_b3_canary_closeout_retains_terminal_schema_failures() -> None:
    manifest = {
        "study_id": "replicated-fixture",
        "cell_count": 30,
        "cells": [
            {
                "cell_id": f"world-0--replicate-01--{arm}",
                "cluster_id": "world-0",
                "replicate_index": 1,
            }
            for arm in B3_ARMS
        ],
    }
    results = []
    for arm in B3_ARMS:
        failed = arm != "opaque"
        results.append(
            {
                "cell_id": f"world-0--replicate-01--{arm}",
                "arm": arm,
                "status": "failed" if failed else "completed",
                "provider_attempt_count": 1,
                "provider_receipts": [
                    {"status": "completed", "tool_event_count": 0},
                    {"status": "completed", "tool_event_count": 0},
                ],
                "failure": {
                    "classification": "participant_schema",
                    "type": "ParticipantSchemaError",
                    "message": "post selected action query ID is invalid",
                }
                if failed
                else None,
                "same_thread": True,
                "post_submission": {
                    "mechanism_family": "FAMILY_B_POWER",
                    "estimated_reference_exponent": 1.75,
                }
                if not failed
                else None,
                "scores": {
                    "post": {"mean_normalized_absolute_error": 0.01}
                }
                if not failed
                else {},
                "selected_action": {
                    "selected_true_rank": 6,
                    "top1_selected": False,
                    "normalized_regret": 0.4,
                    "action_opportunity_eligible": True,
                }
                if not failed
                else None,
            }
        )

    summary = summarize_b3_canary_closeout(
        manifest,
        results,
        {"qualified": False, "errors": ["two canary cells failed"]},
    )

    assert summary["status"] == "terminal_canary_rejected_before_formal"
    assert summary["scheduled_canary_session_count"] == 3
    assert summary["completed_canary_session_count"] == 1
    assert summary["participant_schema_failure_count"] == 2
    assert summary["provider_session_attempt_count"] == 3
    assert summary["provider_turn_count"] == 6
    assert summary["completed_provider_turn_count"] == 6
    assert summary["launched_formal_session_count"] == 0
    assert summary["unstarted_formal_session_count"] == 30
    assert summary["outcome_replacement_count"] == 0
