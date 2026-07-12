from __future__ import annotations

import copy
import json

from scripts.audit_lite_elimination_integration import (
    DEFAULT_OUTPUT,
    build_report,
    load_before_after_manifest,
    load_protocol,
    validate_report,
)


def test_before_snapshot_freezes_the_six_shared_lite_runtime_providers() -> None:
    manifest = load_before_after_manifest()
    before = manifest["before_snapshot"]
    groups = before["shared_lite_runtime_providers"]

    assert before["task_maturity_counts"] == {"lite": 15}
    assert {module_id: len(model_ids) for module_id, model_ids in groups.items()} == {
        "reaction_kinetics": 1,
        "reactors": 1,
        "spectroscopy_instruments": 4,
    }
    assert sum(map(len, groups.values())) == 6


def test_current_tasks_routes_and_evidence_close_the_shared_lite_gap() -> None:
    protocol = load_protocol()
    manifest = load_before_after_manifest()
    report = build_report(protocol, manifest)

    assert validate_report(report, protocol, manifest) == []
    assert report["status"] == "lite_elimination_verified"
    assert report["benchmark_claim_allowed"] is False
    assert report["after_snapshot"]["task_maturity_counts"] == {
        "reference_validated": 15
    }
    assert report["after_snapshot"]["proxy_allowed_false_task_count"] == 15
    assert report["after_snapshot"]["retired_lite_provider_ids_present"] == []
    assert report["after_snapshot"]["promoted_in_place_provider_ids"] == [
        "beer_lambert_uvvis",
        "chromatography_retention_plate",
    ]
    assert report["historical_before_evidence"]["available"] is True
    assert report["historical_before_evidence"]["matches_manifest"] is True
    assert all(report["checks"].values())


def test_all_fifteen_tasks_bind_maturity_proxy_routes_and_evidence() -> None:
    report = build_report(load_protocol(), load_before_after_manifest())

    assert len(report["task_evidence_matrix"]) == 15
    for row in report["task_evidence_matrix"].values():
        assert row["declared_maturity"] == "reference_validated"
        assert row["effective_runtime_maturity"] == "reference_validated"
        assert row["proxy_allowed"] is False
        assert row["declared_but_unreachable"] == []
        assert row["reachable_but_undeclared"] == []


def test_required_shared_runtime_providers_have_execution_evidence() -> None:
    report = build_report(load_protocol(), load_before_after_manifest())

    assert len(report["shared_provider_evidence_matrix"]) == 6
    for row in report["shared_provider_evidence_matrix"].values():
        assert row["maturity"] == "reference_validated"
        assert row["role"] == "runtime"
        assert row["runtime_reachable"] is True
        assert row["routed"] is True
        assert row["card_present"] is True
        assert row["claim_verified"] is True
        assert row["executed_in_runtime_evidence"] is True
        assert row["provenance"]
        assert row["task_ids"]


def test_report_is_tamper_evident_and_checked_in_report_is_valid() -> None:
    protocol = load_protocol()
    manifest = load_before_after_manifest()
    report = build_report(protocol, manifest)
    tampered = copy.deepcopy(report)
    tampered["task_evidence_matrix"].pop("partition-discovery")

    errors = validate_report(tampered, protocol, manifest)
    assert "task evidence coverage mismatch" in errors
    assert "report hash mismatch" in errors

    checked_in = json.loads(DEFAULT_OUTPUT.read_text(encoding="utf-8"))
    assert validate_report(checked_in, protocol, manifest) == []
