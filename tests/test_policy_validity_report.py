from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

import chemworld.eval.policy_validity_report as report_module
from chemworld.eval.policy_validity_audit import PolicyValidityAuditError
from chemworld.eval.policy_validity_matrix import semantic_sha256
from chemworld.eval.policy_validity_report import (
    FROZEN_GATES,
    PolicyValidityReportError,
    build_delivery_manifest,
    build_policy_validity_report,
    render_policy_validity_markdown,
    rendered_json_text,
)
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(
    "workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json"
)
AUDIT = Path("workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json")
V08_CLAIM = Path("workstreams/arxiv_v1/claims/W1-V08--codex-1.md")
V08_DONE_COMMIT = "4fb789ba76550bd0b30510123181bb5394a14d0b"
ANALYZERS = {
    "v09_reporter_source": Path("src/chemworld/eval/policy_validity_report.py"),
    "v09_reporter_cli": Path("scripts/report_work_i_policy_control_validity.py"),
    "v06_auditor_source": Path("src/chemworld/eval/policy_validity_audit.py"),
    "provenance_helper_source": Path("src/chemworld/eval/provenance.py"),
}


@pytest.fixture(scope="module")
def formal_audit() -> dict[str, Any]:
    return json.loads((ROOT / AUDIT).read_text(encoding="utf-8"))


def _rehash_audit(audit: dict[str, Any]) -> None:
    audit.pop("audit_sha256", None)
    audit["audit_sha256"] = canonical_json_sha256(audit)


def _build(
    monkeypatch: pytest.MonkeyPatch,
    receipt: dict[str, Any],
    *,
    manifest_path: Path = MANIFEST,
    audit_path: Path = AUDIT,
) -> dict[str, Any]:
    monkeypatch.setattr(
        report_module,
        "audit_policy_validity_manifest",
        lambda _: deepcopy(receipt),
    )
    return build_policy_validity_report(
        manifest_path,
        audit_path,
        v08_claim_path=V08_CLAIM,
        v08_done_commit=V08_DONE_COMMIT,
        analyzer_source_paths=ANALYZERS,
    )


def test_formal_report_is_campaign_equal_bounded_and_self_hashed(
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
) -> None:
    report = _build(monkeypatch, formal_audit)
    assert report["status"] == "positive_control_established"
    assert report["evidence_validity"]["status"] == "valid"
    assert report["estimand"] == {
        "unit": "one primary campaign profile",
        "weighting": "equal weight across ten world-arm campaigns per policy",
        "lifecycle_rows_pooled_before_profile_construction": False,
        "primary_campaigns": 30,
        "primary_closed_lifecycles": 180,
        "retest_campaigns": 30,
        "retest_closed_lifecycles": 180,
        "retest_in_primary_estimand": False,
        "provider_calls": 0,
    }
    assert len(report["campaign_profiles"]) == 30
    assert all(
        summary["campaign_count"] == 10 and summary["weighting"] == "one_campaign_one_equal_weight"
        for summary in report["policy_summaries"].values()
    )
    assert report["policy_summaries"]["measure_then_threshold"]["metrics"][
        "assay_fraction"
    ] == pytest.approx(28 / 60)
    assert report["scientific_status"]["threshold_assays"] == 28
    assert report["scientific_status"]["threshold_discards"] == 32
    assert report["test_retest_reliability"]["pair_count"] == 30
    assert report["test_retest_reliability"]["excluded_from_primary_estimand"] is True
    assert report["formal_world_controller_or_provider_execution"] is False
    assert report["claim_boundary"]["endpoint_performance_ranking"] is False
    unhashed = deepcopy(report)
    supplied = unhashed.pop("report_sha256")
    assert supplied == canonical_json_sha256(unhashed)


@pytest.mark.parametrize(
    ("gate", "section"),
    [
        ("threshold_non_degenerate", None),
        ("six_partial_orderings", "partial_ordering_checks"),
        ("exact_policy_signatures", "exact_signature_checks"),
        ("conditional_null_rules", "conditional_null_checks"),
    ],
)
def test_frozen_scientific_failures_are_reported_without_retuning(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
    gate: str,
    section: str | None,
) -> None:
    failed = deepcopy(formal_audit)
    failed["gates"][gate] = False
    failed["passed"] = False
    failed["status"] = "positive_control_unestablished"
    if gate == "threshold_non_degenerate":
        failed["counts"]["threshold_assays"] = 60
        failed["counts"]["threshold_discards"] = 0
    if section is not None:
        first_check = next(iter(failed[section]))
        failed[section][first_check] = False
    _rehash_audit(failed)
    audit_path = tmp_path / "failed-audit.json"
    write_json_atomic(audit_path, failed)

    report = _build(monkeypatch, failed, audit_path=audit_path)
    assert report["status"] == "positive_control_unestablished"
    assert gate in report["scientific_status"]["failed_gates"]
    assert "was not established" in report["conclusion"]
    assert report["claim_boundary"]["formal_retuning_or_result_replacement"] is False


def test_explicit_non_orderings_remain_non_gating(
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
) -> None:
    report = _build(monkeypatch, formal_audit)
    non_orderings = report["frozen_checks"]["explicit_non_orderings"]
    assert "mean_assayed_score" in non_orderings
    assert "best_assayed_score" in non_orderings
    assert not set(non_orderings).intersection(FROZEN_GATES)


def test_rejects_stale_formal_audit_self_hash(
    tmp_path: Path,
    formal_audit: dict[str, Any],
) -> None:
    stale = deepcopy(formal_audit)
    stale["counts"]["provider_calls"] = 1
    path = tmp_path / "stale-audit.json"
    write_json_atomic(path, stale)
    with pytest.raises(PolicyValidityReportError, match="formal audit self-hash mismatch"):
        build_policy_validity_report(
            MANIFEST,
            path,
            v08_claim_path=V08_CLAIM,
            v08_done_commit=V08_DONE_COMMIT,
            analyzer_source_paths=ANALYZERS,
        )


def test_rejects_receipt_that_differs_from_v06_reconstruction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
) -> None:
    stale = deepcopy(formal_audit)
    stale["claim_boundary"]["endpoint_performance_ranking"] = True
    _rehash_audit(stale)
    path = tmp_path / "different-audit.json"
    write_json_atomic(path, stale)
    monkeypatch.setattr(
        report_module,
        "audit_policy_validity_manifest",
        lambda _: deepcopy(formal_audit),
    )
    with pytest.raises(PolicyValidityReportError, match="differs from the V06 reconstruction"):
        build_policy_validity_report(
            MANIFEST,
            path,
            v08_claim_path=V08_CLAIM,
            v08_done_commit=V08_DONE_COMMIT,
            analyzer_source_paths=ANALYZERS,
        )


def test_rejects_stale_manifest_self_hash(
    tmp_path: Path,
    formal_audit: dict[str, Any],
) -> None:
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    manifest["materialized_counts"]["provider_calls"] = 1
    path = tmp_path / "stale-manifest.json"
    write_json_atomic(path, manifest)
    with pytest.raises(PolicyValidityReportError, match="manifest self-hash mismatch"):
        build_policy_validity_report(
            path,
            AUDIT,
            v08_claim_path=V08_CLAIM,
            v08_done_commit=V08_DONE_COMMIT,
            analyzer_source_paths=ANALYZERS,
        )


def test_rejects_stale_bundle_file_hash(
    tmp_path: Path,
    formal_audit: dict[str, Any],
) -> None:
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    reference = manifest["cells"][0]
    source_bundle = (ROOT / MANIFEST).parent / reference["bundle_path"]
    target_bundle = tmp_path / reference["bundle_path"]
    target_bundle.parent.mkdir(parents=True)
    shutil.copyfile(source_bundle, target_bundle)
    reference["file_sha256"] = "0" * 64
    manifest.pop("manifest_sha256")
    manifest["manifest_sha256"] = semantic_sha256(manifest)
    path = tmp_path / "matrix_manifest.json"
    write_json_atomic(path, manifest)
    with pytest.raises(PolicyValidityReportError, match="campaign bundle file hash mismatch"):
        build_policy_validity_report(
            path,
            AUDIT,
            v08_claim_path=V08_CLAIM,
            v08_done_commit=V08_DONE_COMMIT,
            analyzer_source_paths=ANALYZERS,
        )


def test_rejects_retest_mismatch_as_invalid_evidence(
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
) -> None:
    def fail_rebuild(_: Path) -> dict[str, Any]:
        raise PolicyValidityAuditError("same-identity retest mismatch")

    monkeypatch.setattr(report_module, "audit_policy_validity_manifest", fail_rebuild)
    with pytest.raises(PolicyValidityReportError, match="same-identity retest mismatch"):
        build_policy_validity_report(
            MANIFEST,
            AUDIT,
            v08_claim_path=V08_CLAIM,
            v08_done_commit=V08_DONE_COMMIT,
            analyzer_source_paths=ANALYZERS,
        )


def test_markdown_and_delivery_manifest_are_bounded_and_self_hashed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    formal_audit: dict[str, Any],
) -> None:
    report = _build(monkeypatch, formal_audit)
    markdown = render_policy_validity_markdown(report)
    assert "30 campaigns and 180 closed lifecycles" in markdown
    assert "not an endpoint ranking" in markdown
    assert "mean_assayed_score" in markdown
    delivery = build_delivery_manifest(
        report=report,
        markdown=markdown,
        report_path=tmp_path / "report.json",
        markdown_path=tmp_path / "report.md",
        matrix_manifest_path=MANIFEST,
        formal_audit_path=AUDIT,
        v08_claim_path=V08_CLAIM,
        analyzer_source_paths=ANALYZERS,
    )
    assert delivery["entry_count"] == 9
    assert delivery["delivery_manifest_sha256"] == canonical_json_sha256(
        {key: value for key, value in delivery.items() if key != "delivery_manifest_sha256"}
    )
    assert rendered_json_text(delivery).endswith("\n")
