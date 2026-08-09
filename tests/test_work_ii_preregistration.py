from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_preregistration as preregistration
from chemworld.eval.work_ii_preregistration import (
    NATURE_REGISTERED_REPORT_EXPANSION_URL,
    NATURE_REGISTERED_REPORT_GUIDELINES_URL,
    build_preregistration_readiness,
    render_preregistration_draft,
    route_decision_sha256,
    validate_preregistration_readiness,
    validate_submission_route_decision,
)

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
PREFLIGHT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json"
)
QUALIFICATION = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-method-qualification-readiness-v0.1.json"
)
POWER_AUDIT = ROOT / "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"
DESIGN_AUDIT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-world-prior-design-audit.json"
)


def _build() -> dict[str, object]:
    return build_preregistration_readiness(
        ROOT,
        route_path=ROUTE,
        design_path=DESIGN,
        analysis_path=ANALYSIS,
        formal_preflight_path=PREFLIGHT,
        qualification_readiness_path=QUALIFICATION,
        power_audit_path=POWER_AUDIT,
        design_audit_path=DESIGN_AUDIT,
    )


def test_submission_route_record_is_current_outcome_blind_and_pending_user_choice() -> None:
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    assert validate_submission_route_decision(route) == []
    assert route["status"] == "awaiting_user_selection"
    assert route["formal_participant_outcome_count_at_decision"] == 0
    assert route["recommended_option"] == "nature_registered_report_stage_1"
    assert {item["url"] for item in route["policy_sources"]} == {
        NATURE_REGISTERED_REPORT_GUIDELINES_URL,
        NATURE_REGISTERED_REPORT_EXPANSION_URL,
    }


def test_preregistration_readiness_is_deterministic_zero_call_and_blocked() -> None:
    first = _build()
    second = _build()
    assert first == second
    assert validate_preregistration_readiness(first) == []
    assert first["status"] == "passed_final_freeze_blocked"
    assert first["provider_calls_executed"] == 0
    assert first["formal_participant_outcome_count"] == 0
    assert first["formal_population"] == {
        "tasks": 5,
        "independent_task_world_clusters": 25,
        "prior_arms": ["opaque", "aligned_nominal", "misindexed_nominal"],
        "participant_cells": 75,
        "complete_experiments": 300,
        "belief_checkpoints": 300,
        "provider_sessions": 75,
        "provider_attempts_hard_cap": 150,
    }
    assert first["private_confirmation"]["private_identities_present"] is False
    assert len(first["unresolved_requirement_ids"]) == 6


def test_preregistration_draft_is_bound_to_manifest_and_has_no_private_identity() -> None:
    report = _build()
    rendered = render_preregistration_draft(report)
    assert f"Manifest SHA-256: `{report['readiness_sha256']}`" in rendered
    assert report["route_decision"]["decision_sha256"] in rendered
    assert NATURE_REGISTERED_REPORT_GUIDELINES_URL in rendered
    assert NATURE_REGISTERED_REPORT_EXPANSION_URL in rendered
    assert "private_world_seed" not in rendered
    assert "api_key" not in rendered.lower()


def test_route_cannot_be_reclassified_after_formal_outcomes_even_with_fresh_hash() -> None:
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    tampered = deepcopy(route)
    tampered["formal_participant_outcome_count_at_decision"] = 1
    tampered["decision_sha256"] = route_decision_sha256(tampered)
    errors = validate_submission_route_decision(tampered)
    assert "submission route was not decided before formal outcomes" in errors


def test_selected_route_is_accepted_and_removes_only_the_route_blocker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    route["status"] = "selected"
    route["selected_option"] = "nature_registered_report_stage_1"
    route["selected_by"] = "user"
    route["selected_at"] = "2026-08-10"
    route["decision_sha256"] = route_decision_sha256(route)
    original_load_object = preregistration._load_object

    def load_selected_route(path: Path) -> dict[str, object]:
        if path.resolve() == ROUTE.resolve():
            return deepcopy(route)
        return original_load_object(path)

    monkeypatch.setattr(preregistration, "_load_object", load_selected_route)

    report = build_preregistration_readiness(
        ROOT,
        route_path=ROUTE,
        design_path=DESIGN,
        analysis_path=ANALYSIS,
        formal_preflight_path=PREFLIGHT,
        qualification_readiness_path=QUALIFICATION,
        power_audit_path=POWER_AUDIT,
        design_audit_path=DESIGN_AUDIT,
    )

    assert validate_submission_route_decision(route) == []
    assert validate_preregistration_readiness(report) == []
    assert report["route_decision"]["selected_option"] == "nature_registered_report_stage_1"
    assert report["unresolved_requirement_ids"] == [
        "current_method_real_provider_qualification_receipt",
        "formal_currency_ceiling_and_provider_contract_approval",
        "qualified_expected_eta_from_current_method",
        "clean_wheel_independent_checkout_and_evidence_graph_receipt",
        "execution_command_budget_and_escalation_user_signoff",
    ]
