from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from scripts.audit_work_i_historical_report_alignment import (
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    HistoricalReportAlignmentError,
    _read_json,
    _validate_public_boundary_report,
    _validate_runtime_report,
    build_alignment_receipt,
    build_markdown_report,
    receipt_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _receipt() -> dict[str, object]:
    return _read_json(ROOT / REPORT_JSON_PATH)


def test_committed_receipt_is_self_hashed_and_deterministic() -> None:
    receipt = _receipt()
    assert receipt["receipt_sha256"] == receipt_sha256(receipt)
    assert receipt == build_alignment_receipt(ROOT)
    assert (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") == build_markdown_report(receipt)


def test_receipt_preserves_exact_historical_acceptance_evidence() -> None:
    acceptance = _receipt()["acceptance_evidence"]
    assert isinstance(acceptance, dict)
    assert acceptance["runtime_domain_affordance"] == {
        "all_checks_passed": True,
        "candidate_count": 237,
        "finding_count": 0,
        "guarded_sources_match_source_commit": True,
        "historical_source_commit": "a5d515929816541f5e8cf1293e20820a9dbe0da4",
        "runtime_committed_count": 235,
        "task_count": 6,
        "validator_valid_count": 235,
    }
    public = acceptance["public_boundary_security"]
    assert isinstance(public, dict)
    assert public["probe_count"] == 35
    assert public["passed_probe_count"] == 35
    assert public["failed_probe_count"] == 0
    assert public["semantic_invariance_paired_run_count"] == 12
    assert public["dependency_binding_count"] == 4


def test_reports_match_git_index_and_current_evidence_nodes() -> None:
    receipt = _receipt()
    assert receipt["status"] == "target_reports_aligned_global_refresh_queued"
    reports = receipt["source_reports"]
    assert isinstance(reports, list)
    assert len(reports) == 2
    assert all(
        row["tracked"] is True
        and row["working_tree_matches_index"] is True
        and row["git_index_blob_oid"] == row["working_tree_blob_oid"]
        for row in reports
    )
    nodes = receipt["current_evidence_bindings"]
    assert isinstance(nodes, list)
    assert {row["node"] for row in nodes} == {"runtime_affordance", "public_boundary"}
    assert all(
        row["artifact_state"] == "current"
        and row["freshness"] == "fresh"
        and row["gate_state"] == "passed"
        for row in nodes
    )
    assert receipt["alignment_decision"]["unexplained_target_report_drift"] is False
    integration = receipt["repository_integration_state"]
    assert integration["baseline_evidence_pipeline_check_passed"] is False
    assert integration["baseline_issue_existed_before_w1_m03_implementation"] is True
    assert integration["target_report_path_or_content_mismatch"] is False


def test_report_or_receipt_tampering_fails_closed() -> None:
    runtime = _read_json(
        ROOT / "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json"
    )
    runtime["summary"]["finding_count"] = 1
    with pytest.raises(HistoricalReportAlignmentError, match="acceptance evidence changed"):
        _validate_runtime_report(runtime)

    public = _read_json(
        ROOT / "workstreams/world_foundation/reports/public-boundary-security-vnext.json"
    )
    public["probe_groups"]["replay"]["valid_trajectory_verified"] = False
    with pytest.raises(HistoricalReportAlignmentError, match="acceptance evidence changed"):
        _validate_public_boundary_report(ROOT, public)

    receipt = deepcopy(_receipt())
    receipt["alignment_decision"]["unexplained_target_report_drift"] = True
    assert receipt["receipt_sha256"] != receipt_sha256(receipt)
