from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.work_ii_study_b import (
    build_study_b_manifest,
    prediction_output_schema,
    score_prediction_payload,
    summarize_study_b_results,
    validate_prediction_payload,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_study_b_matched_evidence_v0.1.json"
OPENAI_AP_PROTOCOL = (
    ROOT
    / "configs/benchmark/work_ii_study_b_ap_gpt56_sol_medium_replication_v0.1.json"
)


@pytest.fixture(scope="module")
def manifest() -> dict:
    return build_study_b_manifest(PROTOCOL, repository_root=ROOT)


def _perfect_payload(cell: dict, stage: str) -> dict:
    return {
        "status": f"{stage}_evidence_complete",
        "predictions": [
            {"query_id": query_id, "metrics": deepcopy(metrics)}
            for query_id, metrics in cell["scoring_truth"].items()
        ],
        "model_summary": "concise public summary",
        "confidence": 0.8,
        **({"evidence_assessment": "evidence was incorporated"} if stage == "post" else {}),
    }


def test_manifest_freezes_exact_matched_evidence_denominators(manifest: dict) -> None:
    assert manifest["cell_count"] == 30
    assert manifest["cluster_count"] == 10
    assert manifest["participant_physical_experiment_count"] == 0
    assert {cell["locus"] for cell in manifest["cells"]} == {"A_P", "A_S"}
    for cluster in manifest["cluster_packets"]:
        assert cluster["evidence_query_count"] == 8
        assert cluster["scoring_query_count"] == 8
        assert cluster["scoring_term_count"] in {24, 48}
    for cluster_id in {cell["cluster_id"] for cell in manifest["cells"]}:
        members = [cell for cell in manifest["cells"] if cell["cluster_id"] == cluster_id]
        assert len(members) == 3
        assert {cell["arm"] for cell in members} == {
            "opaque",
            "aligned_nominal",
            "misindexed_nominal",
        }
        assert len({cell["public_packet_sha256"] for cell in members}) == 1
        evidence_ids = {item["query_id"] for item in members[0]["public_packet"]["evidence"]}
        scoring_ids = {
            item["query_id"] for item in members[0]["public_packet"]["scoring_queries"]
        }
        assert evidence_ids.isdisjoint(scoring_ids)


def test_openai_ap_replication_freezes_single_locus_denominator() -> None:
    replication = build_study_b_manifest(OPENAI_AP_PROTOCOL, repository_root=ROOT)

    assert replication["cell_count"] == 15
    assert replication["cluster_count"] == 5
    assert {cell["locus"] for cell in replication["cells"]} == {"A_P"}
    assert replication["provider"]["id"] == "chemworld_openai_https"
    assert replication["provider"]["model"] == "gpt-5.6-sol"


def test_prediction_schema_and_validation_are_exact(manifest: dict) -> None:
    cell = manifest["cells"][0]
    queries = cell["public_packet"]["scoring_queries"]
    schema = prediction_output_schema(queries, stage="post")
    assert schema["properties"]["predictions"]["minItems"] == 8
    payload = _perfect_payload(cell, "post")
    assert validate_prediction_payload(payload, queries, stage="post") == []
    broken = deepcopy(payload)
    broken["predictions"].pop()
    assert validate_prediction_payload(broken, queries, stage="post")


def test_scoring_and_summary_use_pre_to_post_gain(manifest: dict) -> None:
    results = []
    for cell in manifest["cells"]:
        perfect = _perfect_payload(cell, "post")
        post = score_prediction_payload(perfect, cell["scoring_truth"])
        pre = deepcopy(post)
        pre["mean_normalized_absolute_error"] = 0.2
        results.append(
            {
                "cell_id": cell["cell_id"],
                "cluster_id": cell["cluster_id"],
                "locus": cell["locus"],
                "task_id": cell["task_id"],
                "world_seed": cell["world_seed"],
                "arm": cell["arm"],
                "status": "completed",
                "scores": {"pre": pre, "post": post},
            }
        )
    summary = summarize_study_b_results(manifest, results)
    assert summary["status"] == "completed"
    assert summary["completed_cell_count"] == 30
    assert summary["complete_cluster_count"] == 10
    assert all(row["mean_primary_contrast"] == pytest.approx(0.0) for row in summary["locus_rows"])
