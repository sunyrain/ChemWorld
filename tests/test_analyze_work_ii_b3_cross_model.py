from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_reviewer_followup import B3_ARMS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_work_ii_b3_cross_model as analysis  # noqa: E402


def _manifest(*, study_id: str, provider_id: str, model: str) -> dict:
    cells = []
    cluster_packets = []
    for world_index in range(5):
        world_seed = 100 + world_index
        cluster_id = f"cluster-{world_seed}"
        packet_hash = f"{world_index + 1:064x}"
        eligible = world_index < 3
        scoring_queries = [
            {"query_id": f"q-{query_index}", "action_index": query_index}
            for query_index in range(8)
        ]
        scoring_truth = {
            query["query_id"]: {"score": 1.0 - 0.1 * query["action_index"]}
            for query in scoring_queries
        }
        cluster_packets.append(
            {
                "cluster_id": cluster_id,
                "world_seed": world_seed,
                "public_packet_sha256": packet_hash,
                "action_opportunity_eligible": eligible,
            }
        )
        for replicate_index in (1, 2):
            replicate_block_id = f"{cluster_id}--replicate-{replicate_index:02d}"
            for arm in B3_ARMS:
                cell_id = f"{replicate_block_id}--{arm}"
                cells.append(
                    {
                        "study_id": study_id,
                        "cell_id": cell_id,
                        "cluster_id": cluster_id,
                        "replicate_block_id": replicate_block_id,
                        "replicate_index": replicate_index,
                        "world_seed": world_seed,
                        "arm": arm,
                        "action_selection_encoding": "zero_based_index",
                        "stage_status_encoding": "runner_derived",
                        "public_packet_sha256": packet_hash,
                        "public_packet": {
                            "scoring_action_queries": scoring_queries,
                        },
                        "scoring_truth": scoring_truth,
                        "evidence_incumbent_score": 0.5,
                        "action_opportunity_eligible": eligible,
                        "action_opportunity_threshold": 0.02,
                    }
                )
    manifest = {
        "schema_version": "fixture",
        "study_id": study_id,
        "provider": {
            "id": provider_id,
            "model": model,
            "reasoning_effort": "medium",
            "wire_api": "responses",
            "auth_mode": "fixture",
        },
        "action_selection_encoding": "zero_based_index",
        "stage_status_encoding": "runner_derived",
        "qualification_sha256": "a" * 64,
        "public_truth_sha256": "b" * 64,
        "roster_sha256": "c" * 64,
        "cell_count": 30,
        "cluster_count": 5,
        "replicate_block_count": 10,
        "replicates_per_arm": 2,
        "scoring_term_count": 32,
        "cluster_packets": cluster_packets,
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    return manifest


def _results(manifest: dict, *, selected_action_index: int) -> list[dict]:
    results = []
    for cell in manifest["cells"]:
        post_power = cell["arm"] == "aligned_nominal"
        result = {
            "schema_version": "fixture",
            "study_id": manifest["study_id"],
            "cell_id": cell["cell_id"],
            "cluster_id": cell["cluster_id"],
            "replicate_block_id": cell["replicate_block_id"],
            "replicate_index": cell["replicate_index"],
            "world_seed": cell["world_seed"],
            "arm": cell["arm"],
            "status": "completed",
            "pre_submission": {
                "mechanism_family": "FAMILY_A_LINEAR",
                "estimated_reference_exponent": 1.0,
            },
            "post_submission": {
                "mechanism_family": (
                    "FAMILY_B_POWER" if post_power else "FAMILY_A_LINEAR"
                ),
                "estimated_reference_exponent": 1.75 if post_power else 1.0,
                "selected_action_index": selected_action_index,
            },
            "scores": {
                "pre": {"mean_normalized_absolute_error": 0.20},
                "post": {
                    "mean_normalized_absolute_error": (
                        0.02 if post_power else 0.05
                    )
                },
            },
        }
        result["result_sha256"] = canonical_json_sha256(result)
        results.append(result)
    return results


def test_cross_model_summary_requires_and_reports_complete_matched_blocks() -> None:
    deepseek_manifest = _manifest(
        study_id="deepseek-study", provider_id="deepseek", model="deepseek-fixture"
    )
    gpt_manifest = _manifest(
        study_id="gpt-study", provider_id="openai", model="gpt-fixture"
    )
    summary = analysis.build_cross_model_summary(
        deepseek_manifest,
        _results(deepseek_manifest, selected_action_index=1),
        gpt_manifest,
        _results(gpt_manifest, selected_action_index=0),
    )

    assert summary["status"] == "formal_completed_matched_cross_model"
    assert summary["integrity"]["formal_completed_by_provider"] == {
        "deepseek": 30,
        "gpt": 30,
    }
    assert summary["integrity"]["paired_cell_count"] == 30
    assert summary["provider_results"]["deepseek"]["pooled"][
        "eligible_gain_denominator"
    ] == 18
    assert summary["paired_descriptive_differences"]["orientation"] == (
        "gpt_minus_deepseek"
    )
    assert summary["paired_descriptive_differences"]["pooled"][
        "top1_rate_difference"
    ] == 1.0
    assert summary["claim_boundaries"]["model_superiority_ranking_supported"] is False


def test_cross_model_summary_rejects_an_incomplete_formal_denominator() -> None:
    deepseek_manifest = _manifest(
        study_id="deepseek-study", provider_id="deepseek", model="deepseek-fixture"
    )
    gpt_manifest = _manifest(
        study_id="gpt-study", provider_id="openai", model="gpt-fixture"
    )
    deepseek_results = _results(deepseek_manifest, selected_action_index=1)

    with pytest.raises(ValueError, match="exactly 30 formal results"):
        analysis.build_cross_model_summary(
            deepseek_manifest,
            deepseek_results[:-1],
            gpt_manifest,
            _results(gpt_manifest, selected_action_index=0),
        )


def test_cross_model_summary_rejects_shared_truth_hash_drift() -> None:
    deepseek_manifest = _manifest(
        study_id="deepseek-study", provider_id="deepseek", model="deepseek-fixture"
    )
    gpt_manifest = _manifest(
        study_id="gpt-study", provider_id="openai", model="gpt-fixture"
    )
    gpt_manifest["public_truth_sha256"] = "d" * 64
    gpt_manifest.pop("manifest_sha256")
    gpt_manifest["manifest_sha256"] = canonical_json_sha256(gpt_manifest)

    with pytest.raises(ValueError, match="shared science hashes differ"):
        analysis.build_cross_model_summary(
            deepseek_manifest,
            _results(deepseek_manifest, selected_action_index=1),
            gpt_manifest,
            _results(gpt_manifest, selected_action_index=0),
        )


def test_cross_model_summary_rejects_shared_packet_hash_drift() -> None:
    deepseek_manifest = _manifest(
        study_id="deepseek-study", provider_id="deepseek", model="deepseek-fixture"
    )
    gpt_manifest = _manifest(
        study_id="gpt-study", provider_id="openai", model="gpt-fixture"
    )
    gpt_manifest["cluster_packets"][0]["public_packet_sha256"] = "e" * 64
    gpt_manifest.pop("manifest_sha256")
    gpt_manifest["manifest_sha256"] = canonical_json_sha256(gpt_manifest)

    with pytest.raises(ValueError, match="shared public packet hashes differ"):
        analysis.build_cross_model_summary(
            deepseek_manifest,
            _results(deepseek_manifest, selected_action_index=1),
            gpt_manifest,
            _results(gpt_manifest, selected_action_index=0),
        )


def _write_completed_run(root: Path, manifest: dict, results: list[dict]) -> None:
    (root / "cells").mkdir(parents=True)
    (root / "canary").mkdir()
    (root / "input_manifest.json").write_text(
        analysis.json.dumps(manifest), encoding="utf-8"
    )
    (root / "summary.json").write_text(
        analysis.json.dumps(analysis.summarize_b3_results(manifest, results)),
        encoding="utf-8",
    )
    for result in results:
        (root / "cells" / f"{result['cell_id']}.json").write_text(
            analysis.json.dumps(result), encoding="utf-8"
        )

    first_cluster = manifest["cells"][0]["cluster_id"]
    canary_results = [
        deepcopy(result)
        for result in results
        if result["cluster_id"] == first_cluster and result["replicate_index"] == 1
    ]
    for result in canary_results:
        result.pop("result_sha256")
        result["same_thread"] = True
        result["provider_receipts"] = [
            {"status": "completed"},
            {"status": "completed"},
        ]
        result["result_sha256"] = canonical_json_sha256(result)
        (root / "canary" / f"{result['cell_id']}.json").write_text(
            analysis.json.dumps(result), encoding="utf-8"
        )
    (root / "canary_summary.json").write_text(
        analysis.json.dumps({"qualified": True, "session_count": 3}),
        encoding="utf-8",
    )


def test_cross_model_analysis_cli_writes_only_after_two_complete_blocks(
    tmp_path: Path, monkeypatch
) -> None:
    deepseek_manifest = _manifest(
        study_id="deepseek-study", provider_id="deepseek", model="deepseek-fixture"
    )
    gpt_manifest = _manifest(
        study_id="gpt-study", provider_id="openai", model="gpt-fixture"
    )
    deepseek_root = tmp_path / "deepseek"
    gpt_root = tmp_path / "gpt"
    _write_completed_run(
        deepseek_root,
        deepseek_manifest,
        _results(deepseek_manifest, selected_action_index=1),
    )
    _write_completed_run(
        gpt_root,
        gpt_manifest,
        _results(gpt_manifest, selected_action_index=0),
    )
    json_output = tmp_path / "closeout.json"
    report_output = tmp_path / "closeout.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "analyze_work_ii_b3_cross_model.py",
            "--deepseek-root",
            str(deepseek_root),
            "--gpt-root",
            str(gpt_root),
            "--json-output",
            str(json_output),
            "--report-output",
            str(report_output),
        ],
    )

    assert analysis.main() == 0
    closeout = analysis.json.loads(json_output.read_text(encoding="utf-8"))
    assert closeout["status"] == "formal_completed_matched_cross_model"
    assert closeout["integrity"]["canary"]["deepseek"]["qualified"] is True
    assert closeout["integrity"]["canary"]["gpt"]["qualified"] is True
    assert "以下差值固定为" in report_output.read_text(encoding="utf-8")
