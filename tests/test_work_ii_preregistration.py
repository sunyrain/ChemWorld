from __future__ import annotations

import json
import os
import subprocess
import sys
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
from chemworld.eval.work_ii_route_selection import select_submission_route_decision

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


@pytest.mark.parametrize(
    "route_option",
    ["nature_registered_report_stage_1", "regular_submission"],
)
def test_submission_route_selector_records_one_irreversible_user_choice(
    route_option: str,
) -> None:
    pending = json.loads(ROUTE.read_text(encoding="utf-8"))
    selected = select_submission_route_decision(
        pending,
        selected_option=route_option,
        selected_at="2026-08-10T12:00:00+08:00",
    )

    assert validate_submission_route_decision(selected) == []
    assert selected["status"] == "selected"
    assert selected["selected_option"] == route_option
    assert selected["selected_by"] == "user"
    assert pending["status"] == "awaiting_user_selection"
    with pytest.raises(ValueError, match="already been selected"):
        select_submission_route_decision(
            selected,
            selected_option=route_option,
            selected_at="2026-08-10T12:01:00+08:00",
        )


def test_submission_route_selector_rejects_invalid_or_late_source() -> None:
    pending = json.loads(ROUTE.read_text(encoding="utf-8"))
    late = deepcopy(pending)
    late["formal_participant_outcome_count_at_decision"] = 1
    late["decision_sha256"] = route_decision_sha256(late)

    with pytest.raises(ValueError, match="before formal outcomes"):
        select_submission_route_decision(
            late,
            selected_option="regular_submission",
            selected_at="2026-08-10T12:00:00+08:00",
        )
    with pytest.raises(ValueError, match="unsupported submission route"):
        select_submission_route_decision(
            pending,
            selected_option="result_contingent_route",
            selected_at="2026-08-10T12:00:00+08:00",
        )


def test_submission_route_cli_is_fail_closed_and_write_once(tmp_path: Path) -> None:
    decision_path = tmp_path / "route.json"
    decision_path.write_bytes(ROUTE.read_bytes())
    original = decision_path.read_bytes()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "src"), str(ROOT)))
    base_command = [
        sys.executable,
        str(ROOT / "scripts/select_work_ii_submission_route.py"),
        "--decision",
        str(decision_path),
    ]

    missing = subprocess.run(
        base_command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert missing.returncode != 0
    assert decision_path.read_bytes() == original

    selected = subprocess.run(
        [
            *base_command,
            "--route",
            "regular_submission",
            "--selected-at",
            "2026-08-10T12:00:00+08:00",
            "--selected-by-user",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert selected.returncode == 0, selected.stderr
    checked = subprocess.run(
        [*base_command, "--check"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert checked.returncode == 0, checked.stderr
    reselected = subprocess.run(
        [
            *base_command,
            "--route",
            "nature_registered_report_stage_1",
            "--selected-at",
            "2026-08-10T12:01:00+08:00",
            "--selected-by-user",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert reselected.returncode != 0


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
    assert len(first["unresolved_requirement_ids"]) == 5
    assert first["frozen_component_readiness"]["clean_release_receipt"] is True


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
        "execution_command_budget_and_escalation_user_signoff",
    ]
