from __future__ import annotations

import copy
import json
from dataclasses import replace
from typing import Any

from scripts.audit_maturity_truth_vnext import (
    DEFAULT_OUTPUT,
    ROOT,
    build_report,
    collect_adapter_manifests,
    collect_model_cards,
    load_protocol,
    validate_report,
)

from chemworld.physchem.maturity import MaturityLevel
from chemworld.runtime.model_reachability import (
    ModelReachabilityRegistry,
    default_model_reachability_registry,
)


def _finding_ids(report: dict[str, Any]) -> set[str]:
    return {
        str(item["check_id"])
        for item in report["findings"]
    }


def test_protocol_collects_unique_cards_and_claim_bound_manifests() -> None:
    protocol = load_protocol()
    cards = collect_model_cards(protocol)
    manifests = collect_adapter_manifests(protocol)

    assert len(cards) == 57
    assert len(manifests) == 9
    assert set(manifests) <= set(cards)
    assert all(manifest.manifest_hash for manifest in manifests.values())


def test_truthful_report_is_valid_but_blocks_unsupported_publication() -> None:
    protocol = load_protocol()
    report = build_report(protocol)

    assert validate_report(report, protocol) == []
    assert report["audit_integrity_valid"] is True
    assert report["release_allowed"] is False
    assert report["status"] == "maturity_claims_blocked"
    assert report["checks"]["task_routes_exact"] is True
    assert report["provider_assessments"][
        "chemworld_stability_aware_lle_vnext"
    ]["executed_in_runtime_evidence"] is True
    assert "manifest_runtime_state_mismatch" not in _finding_ids(report)
    assert "high_provider_missing_model_card" in _finding_ids(report)
    assert "high_provider_not_executed" in _finding_ids(report)


def test_task_maturity_is_the_minimum_of_reachable_verified_providers() -> None:
    report = build_report(load_protocol())
    ranks = {level.value: level.rank for level in MaturityLevel}

    for task in report["task_assessments"].values():
        reachable = task["reachable_model_ids"]
        if not reachable:
            assert task["effective_runtime_maturity"] == "not_applicable"
            continue
        expected = min(
            (
                report["provider_assessments"][model_id]["effective_maturity"]
                for model_id in reachable
            ),
            key=ranks.__getitem__,
        )
        assert task["effective_runtime_maturity"] == expected


def test_forged_card_maturity_is_detected() -> None:
    protocol = load_protocol()
    cards = collect_model_cards(protocol)
    model_id = "nernst_butler_volmer_faradaic_v1"
    cards[model_id] = replace(
        cards[model_id], maturity=MaturityLevel.PROFESSIONAL_CANDIDATE
    )

    report = build_report(protocol, cards=cards)
    row = report["provider_assessments"][model_id]
    assert row["card_maturity_matches"] is False
    assert "provider_card_maturity_mismatch" in _finding_ids(report)


def test_forged_model_id_is_detected() -> None:
    protocol = load_protocol()
    cards = collect_model_cards(protocol)
    model_id = "nernst_butler_volmer_faradaic_v1"
    forged = replace(cards.pop(model_id), model_id="forged_professional_model")
    cards[forged.model_id] = forged

    report = build_report(protocol, cards=cards)
    assert report["provider_assessments"][model_id]["card_present"] is False
    missing = [
        item
        for item in report["findings"]
        if item["check_id"] == "high_provider_missing_model_card"
    ]
    assert any(item["model_id"] == model_id for item in missing)


def test_nonexistent_evidence_path_downgrades_the_claim() -> None:
    protocol = load_protocol()
    cards = collect_model_cards(protocol)
    model_id = "nernst_butler_volmer_faradaic_v1"
    card = cards[model_id]
    forged_evidence = replace(
        card.validation_evidence[0],
        command_or_path="tests/does_not_exist.py",
    )
    cards[model_id] = replace(card, validation_evidence=(forged_evidence,))

    report = build_report(protocol, cards=cards)
    assessment = report["card_assessments"][model_id]
    assert assessment["reference_validated_checks"][
        "numerical_tolerance_and_repository_path"
    ] is False
    assert assessment["effective_evidence_maturity"] == "lite"


def test_runtime_route_tampering_is_detected() -> None:
    protocol = load_protocol()
    registry = default_model_reachability_registry()
    routes = []
    for route in registry.routes:
        if route.operation_type == "electrolyze":
            route = replace(
                route,
                model_ids=(),
                model_free_reason="forged model-free route",
            )
        routes.append(route)
    forged_registry = ModelReachabilityRegistry(registry.providers, tuple(routes))

    report = build_report(protocol, registry=forged_registry)
    assert "high_provider_not_routed" in _finding_ids(report)
    assert "task_runtime_route_mismatch" in _finding_ids(report)
    assert "runtime_registry_integrity" in _finding_ids(report)


def test_registered_but_unexecuted_high_model_cannot_raise_task_maturity() -> None:
    report = build_report(load_protocol())
    row = report["provider_assessments"]["pfr"]

    assert row["declared_maturity"] == "professional_candidate"
    assert row["routed"] is True
    assert row["executed_in_runtime_evidence"] is False
    assert row["effective_maturity"] == "lite"
    flow_task = report["task_assessments"]["flow-reaction-optimization"]
    assert flow_task["effective_runtime_maturity"] == "lite"


def test_public_document_and_runtime_evidence_are_hash_bound() -> None:
    protocol = load_protocol()
    report = build_report(protocol)
    assert report["public_document"]["sha256"]
    assert report["runtime_execution_evidence"]["sha256"]

    tampered = copy.deepcopy(report)
    tampered["public_document"]["sha256"] = "0" * 64
    errors = validate_report(tampered, protocol)
    assert "public document hash mismatch" in errors
    assert "report hash mismatch" in errors


def test_committed_report_is_self_validating() -> None:
    report = json.loads(DEFAULT_OUTPUT.read_text(encoding="utf-8"))
    assert validate_report(report, load_protocol(), repository_root=ROOT) == []
