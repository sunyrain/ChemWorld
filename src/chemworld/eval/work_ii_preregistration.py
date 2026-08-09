"""Outcome-blind submission-route and preregistration readiness for Work II."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    build_formal_preflight,
    validate_formal_bindings,
)
from chemworld.eval.work_ii_qualification import (
    validate_method_qualification_readiness,
)

SUBMISSION_ROUTE_DECISION_VERSION = "chemworld-work-ii-submission-route-decision-0.1"
PREREGISTRATION_READINESS_VERSION = "chemworld-work-ii-preregistration-readiness-0.1"
ROUTE_OPTIONS = (
    "nature_registered_report_stage_1",
    "regular_submission",
)
NATURE_REGISTERED_REPORT_GUIDELINES_URL = (
    "https://www.nature.com/nature/for-authors/registered-reports"
)
NATURE_REGISTERED_REPORT_EXPANSION_URL = "https://www.nature.com/articles/d41586-026-01629-y"


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: value for key, value in payload.items() if key != field})


def _relative(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _canonical_binding(root: Path, path: Path) -> dict[str, Any]:
    value = _load_object(path)
    return {
        "path": _relative(root, path),
        "hash_kind": "canonical_json_sha256",
        "sha256": canonical_json_sha256(value),
    }


def route_decision_sha256(decision: Mapping[str, Any]) -> str:
    return _self_hash(decision, "decision_sha256")


def preregistration_readiness_sha256(report: Mapping[str, Any]) -> str:
    return _self_hash(report, "readiness_sha256")


def validate_submission_route_decision(decision: Mapping[str, Any]) -> list[str]:
    """Validate the outcome-blind route choice or its explicit pending state."""

    errors: list[str] = []
    if decision.get("schema_version") != SUBMISSION_ROUTE_DECISION_VERSION:
        errors.append("unexpected Work II submission-route decision schema")
    if decision.get("decision_sha256") != route_decision_sha256(decision):
        errors.append("Work II submission-route decision self-hash mismatch")
    if decision.get("formal_result") is not False:
        errors.append("submission-route decision is mislabeled as a formal result")
    if decision.get("formal_participant_outcome_count_at_decision") != 0:
        errors.append("submission route was not decided before formal outcomes")
    sources = decision.get("policy_sources")
    sources = sources if isinstance(sources, list) else []
    urls = {row.get("url") for row in sources if isinstance(row, Mapping)}
    if urls != {
        NATURE_REGISTERED_REPORT_GUIDELINES_URL,
        NATURE_REGISTERED_REPORT_EXPANSION_URL,
    }:
        errors.append("submission-route decision lacks the frozen official policy sources")
    options = decision.get("options")
    if not isinstance(options, Mapping) or tuple(options) != ROUTE_OPTIONS:
        errors.append("submission-route decision does not contain the exact route options")
    if decision.get("recommended_option") != "nature_registered_report_stage_1":
        errors.append("submission-route recommendation differs from the outcome-blind review")
    outcome_blindness = decision.get("outcome_blindness_contract")
    if not isinstance(outcome_blindness, Mapping) or any(
        outcome_blindness.get(field) is not True
        for field in (
            "selection_must_precede_formal_primary_data",
            "route_change_based_on_formal_outcomes_forbidden",
            "primary_hypothesis_change_based_on_formal_outcomes_forbidden",
            "fallback_preserves_h3_design_analysis_and_failure_rules",
        )
    ):
        errors.append("submission-route outcome-blindness contract is incomplete")
    status = decision.get("status")
    selected = decision.get("selected_option")
    if status == "awaiting_user_selection":
        if any(
            decision.get(field) is not None
            for field in ("selected_option", "selected_by", "selected_at")
        ):
            errors.append("pending submission-route decision contains a selection")
    elif status == "selected":
        if (
            selected not in ROUTE_OPTIONS
            or decision.get("selected_by") != "user"
            or not isinstance(decision.get("selected_at"), str)
            or not decision.get("selected_at")
        ):
            errors.append("selected submission route lacks valid user authorization")
    else:
        errors.append("submission-route decision has an invalid status")
    return errors


def build_preregistration_readiness(
    root: Path,
    *,
    route_path: Path,
    design_path: Path,
    analysis_path: Path,
    formal_preflight_path: Path,
    qualification_readiness_path: Path,
    power_audit_path: Path,
    design_audit_path: Path,
) -> dict[str, Any]:
    """Build a zero-provider-call readiness manifest for the W2-11 freeze."""

    root = root.resolve()
    route = _load_object(route_path)
    design = _load_object(design_path)
    analysis = _load_object(analysis_path)
    committed_preflight = _load_object(formal_preflight_path)
    qualification = _load_object(qualification_readiness_path)
    power_audit = _load_object(power_audit_path)
    design_audit = _load_object(design_audit_path)
    rebuilt_preflight = build_formal_preflight(root, design_path, analysis_path)

    internal_errors = [
        *validate_submission_route_decision(route),
        *validate_formal_bindings(root, committed_preflight),
        *validate_method_qualification_readiness(qualification),
    ]
    if committed_preflight != rebuilt_preflight:
        internal_errors.append("committed formal preflight differs from deterministic rebuild")
    if power_audit.get("status") != "passed" or power_audit.get("failures") != []:
        internal_errors.append("Work II power/resource audit has not passed")
    if design_audit.get("status") != "passed" or design_audit.get("failures") != []:
        internal_errors.append("Work II formal-design audit has not passed")
    if design.get("formal_execution_allowed") is not False:
        internal_errors.append("formal design unexpectedly allows execution")
    if analysis.get("formal_execution_allowed") is not False:
        internal_errors.append("analysis plan unexpectedly allows execution")
    primary_design = design.get("primary_hypothesis")
    primary_analysis = analysis.get("primary_hypothesis")
    primary_design = primary_design if isinstance(primary_design, Mapping) else {}
    primary_analysis = primary_analysis if isinstance(primary_analysis, Mapping) else {}
    if (
        primary_design.get("id") != "H3_selective_evidence_driven_correction"
        or primary_analysis.get("id") != primary_design.get("id")
        or primary_analysis.get("primary_contrast") != "C_prior=Delta_misindexed-Delta_aligned"
    ):
        internal_errors.append("primary H3 differs across design and analysis")

    expected_counts = committed_preflight.get("expected_counts")
    expected_counts = expected_counts if isinstance(expected_counts, Mapping) else {}
    if (
        expected_counts.get("tasks") != 5
        or expected_counts.get("independent_task_world_clusters") != 25
        or expected_counts.get("participant_cells") != 75
        or expected_counts.get("complete_experiments") != 300
    ):
        internal_errors.append("formal schedule denominators differ from the preregistration")
    world_split = committed_preflight.get("world_split_contract")
    world_split = world_split if isinstance(world_split, Mapping) else {}
    private = world_split.get("private_confirmation")
    private = private if isinstance(private, Mapping) else {}
    private_commitment = private.get("sealed_identity_commitment_sha256")
    if private.get(
        "identities_present_in_manifest"
    ) is not False or private_commitment != design.get("world_cohort", {}).get(
        "private_confirmation", {}
    ).get("sealed_identity_commitment_sha256"):
        internal_errors.append("private confirmation boundary is not commitment-only")

    selected_route = route.get("selected_option")
    blockers = [
        {
            "id": "submission_route_user_selection",
            "owner": "user",
            "satisfied": selected_route in ROUTE_OPTIONS,
        },
        {
            "id": "current_method_real_provider_qualification_receipt",
            "owner": "w2_10",
            "satisfied": False,
        },
        {
            "id": "formal_currency_ceiling_and_provider_contract_approval",
            "owner": "user",
            "satisfied": False,
        },
        {
            "id": "qualified_expected_eta_from_current_method",
            "owner": "w2_07_w2_10",
            "satisfied": False,
        },
        {
            "id": "clean_wheel_independent_checkout_and_evidence_graph_receipt",
            "owner": "w2_11",
            "satisfied": False,
        },
        {
            "id": "execution_command_budget_and_escalation_user_signoff",
            "owner": "user",
            "satisfied": False,
        },
    ]
    unresolved = [row["id"] for row in blockers if not row["satisfied"]]
    report: dict[str, Any] = {
        "schema_version": PREREGISTRATION_READINESS_VERSION,
        "status": "failed" if internal_errors else "passed_final_freeze_blocked",
        "formal_result": False,
        "formal_execution_allowed": False,
        "final_preregistration_freeze_allowed": False,
        "provider_calls_executed": 0,
        "formal_participant_outcome_count": 0,
        "route_decision": {
            "binding": _canonical_binding(root, route_path),
            "decision_sha256": route.get("decision_sha256"),
            "status": route.get("status"),
            "recommended_option": route.get("recommended_option"),
            "selected_option": selected_route,
            "recommendation_action": route.get("recommendation_action"),
            "policy_as_of": route.get("policy_as_of"),
            "policy_sources": route.get("policy_sources"),
        },
        "protocol_bindings": {
            "formal_design": _canonical_binding(root, design_path),
            "analysis_plan": _canonical_binding(root, analysis_path),
            "formal_preflight": {
                "path": _relative(root, formal_preflight_path),
                "file_sha256": file_sha256(formal_preflight_path),
                "preflight_sha256": committed_preflight.get("preflight_sha256"),
            },
            "method_qualification_readiness": {
                "path": _relative(root, qualification_readiness_path),
                "file_sha256": file_sha256(qualification_readiness_path),
                "readiness_sha256": qualification.get("readiness_sha256"),
            },
            "power_resource_audit": {
                "path": _relative(root, power_audit_path),
                "file_sha256": file_sha256(power_audit_path),
            },
            "formal_design_audit": {
                "path": _relative(root, design_audit_path),
                "file_sha256": file_sha256(design_audit_path),
            },
        },
        "research_question": (
            "Can a persistent scientific agent use controlled experimental evidence to "
            "selectively revise a misindexed prior without degrading an aligned prior, and "
            "does that revision support executable law recovery and held-out transfer?"
        ),
        "primary_hypothesis": dict(primary_analysis),
        "claim_boundary": {
            "primary_h3_is_confirmatory": True,
            "all_other_unregistered_analyses_are_exploratory": True,
            "endpoint_success_alone_is_not_law_discovery": True,
            "environment_and_method_qualification_are_not_participant_outcomes": True,
            "historical_runs_are_pilot_or_qualification_only": True,
        },
        "formal_population": {
            "tasks": expected_counts.get("tasks"),
            "independent_task_world_clusters": expected_counts.get(
                "independent_task_world_clusters"
            ),
            "prior_arms": list(FORMAL_ARMS),
            "participant_cells": expected_counts.get("participant_cells"),
            "complete_experiments": expected_counts.get("complete_experiments"),
            "belief_checkpoints": expected_counts.get("belief_checkpoints"),
            "provider_sessions": expected_counts.get("provider_sessions"),
            "provider_attempts_hard_cap": expected_counts.get("provider_attempts_hard_cap"),
        },
        "method_and_evaluator_contracts": {
            "provider_contract": committed_preflight.get("provider_contract"),
            "participant_execution_contract_sha256": committed_preflight.get(
                "participant_execution_contract_sha256"
            ),
            "method_qualification_contract_sha256": committed_preflight.get(
                "method_qualification_contract_sha256"
            ),
            "blind_evaluator_contract_sha256": canonical_json_sha256(
                committed_preflight.get("blind_evaluator_contract")
            ),
            "held_out_evaluator_contract_sha256": canonical_json_sha256(
                committed_preflight.get("held_out_evaluator_contract")
            ),
        },
        "outcome_neutral_quality_gates": {
            "gate_a_current_and_passed": True,
            "formal_design_audit_passed": design_audit.get("status") == "passed",
            "power_resource_audit_passed": power_audit.get("status") == "passed",
            "method_qualification_required_before_formal": True,
            "exact_replay_required": True,
            "execution_audit_required": True,
            "private_identity_commitment_only": True,
        },
        "stopping_failure_and_deviation_contract": {
            "result_direction_early_stopping_forbidden": True,
            "failed_scientific_cells_retained_without_replacement": True,
            "infrastructure_missing_only_resume": True,
            "persisted_scientific_trajectory_forbids_replacement": True,
            "formal_route_or_h3_change_after_outcomes_forbidden": True,
            "registered_protocol_deviations_must_be_disclosed": True,
        },
        "private_confirmation": {
            "sealed_identity_commitment_sha256": private_commitment,
            "private_identities_present": False,
            "one_execution_after_public_analysis_freeze": True,
        },
        "execution_command_contract": {
            "runner": "scripts/run_work_ii_formal_matrix.py",
            "mode": "--execute",
            "required_flags": [
                "--manifest",
                "--output-root",
                "--progress-file",
                "--qualification-receipt",
                "--preregistration-freeze-receipt",
                "--currency-ceiling-usd",
                "--allow-formal-execution",
            ],
            "credentials_must_not_appear_in_command_or_git": True,
            "initial_execution_starts_from_a_clean_immutable_commit": True,
        },
        "frozen_component_readiness": {
            "protocol": True,
            "world_cohort": True,
            "participant_method_contract": True,
            "schedule_and_denominators": True,
            "metrics_and_estimands": True,
            "power_and_variance_contract": True,
            "stopping_failure_and_censoring": True,
            "analysis_plan": True,
            "private_commitment_boundary": True,
            "route_selection": selected_route in ROUTE_OPTIONS,
            "current_method_real_provider_qualification": False,
            "currency_budget_and_expected_eta": False,
            "clean_release_receipt": False,
            "user_execution_signoff": False,
        },
        "conditional_route_requirements": {
            "nature_registered_report_stage_1": [
                "submit_presubmission_enquiry",
                "receive_invitation_for_stage_1",
                "receive_in_principle_acceptance_before_formal_primary_data",
                "register_approved_protocol_publicly_or_under_embargo",
            ],
            "regular_submission": [
                "freeze_regular_target_and_evidence_threshold_before_formal_primary_data"
            ],
        },
        "blocking_requirements": blockers,
        "unresolved_requirement_ids": unresolved,
        "internal_errors": internal_errors,
    }
    report["readiness_sha256"] = preregistration_readiness_sha256(report)
    return report


def validate_preregistration_readiness(report: Mapping[str, Any]) -> list[str]:
    """Validate the preregistration readiness boundary and exact core denominators."""

    errors: list[str] = []
    if report.get("schema_version") != PREREGISTRATION_READINESS_VERSION:
        errors.append("unexpected Work II preregistration readiness schema")
    if report.get("readiness_sha256") != preregistration_readiness_sha256(report):
        errors.append("Work II preregistration readiness self-hash mismatch")
    if report.get("status") != "passed_final_freeze_blocked":
        errors.append("Work II preregistration readiness internal checks did not pass")
    if report.get("internal_errors") != []:
        errors.append("Work II preregistration readiness contains internal errors")
    if (
        report.get("formal_result") is not False
        or report.get("formal_execution_allowed") is not False
        or report.get("final_preregistration_freeze_allowed") is not False
        or report.get("provider_calls_executed") != 0
        or report.get("formal_participant_outcome_count") != 0
    ):
        errors.append("Work II preregistration readiness crossed the execution boundary")
    population = report.get("formal_population")
    population = population if isinstance(population, Mapping) else {}
    if (
        population.get("tasks") != 5
        or population.get("independent_task_world_clusters") != 25
        or population.get("prior_arms") != list(FORMAL_ARMS)
        or population.get("participant_cells") != 75
        or population.get("complete_experiments") != 300
    ):
        errors.append("Work II preregistration population differs from the frozen matrix")
    private = report.get("private_confirmation")
    private = private if isinstance(private, Mapping) else {}
    if (
        private.get("private_identities_present") is not False
        or not isinstance(private.get("sealed_identity_commitment_sha256"), str)
        or len(str(private.get("sealed_identity_commitment_sha256"))) != 64
    ):
        errors.append("Work II preregistration leaks or omits the private boundary")
    route = report.get("route_decision")
    route = route if isinstance(route, Mapping) else {}
    route_status = route.get("status")
    selected_route = route.get("selected_option")
    if route_status == "awaiting_user_selection":
        if selected_route is not None:
            errors.append("pending preregistration readiness contains a route selection")
    elif route_status == "selected":
        if selected_route not in ROUTE_OPTIONS:
            errors.append("selected preregistration readiness contains an invalid route")
    else:
        errors.append("preregistration readiness contains an invalid route status")
    unresolved = report.get("unresolved_requirement_ids")
    expected_blocker_count = 6 if selected_route is None else 5
    if not isinstance(unresolved, list) or len(unresolved) != expected_blocker_count:
        errors.append("Work II preregistration readiness has an invalid blocker set")
    return errors


def render_preregistration_draft(report: Mapping[str, Any]) -> str:
    """Render a concise narrative draft that remains bound to the readiness manifest."""

    route = report["route_decision"]
    population = report["formal_population"]
    hypothesis = report["primary_hypothesis"]
    blockers = report["unresolved_requirement_ids"]
    policy_sources = route["policy_sources"]
    lines = [
        "# Work II preregistration draft - final freeze blocked",
        "",
        f"Manifest SHA-256: `{report['readiness_sha256']}`",
        f"Route-decision SHA-256: `{route['decision_sha256']}`",
        "",
        "> This is an outcome-blind readiness draft, not a registered protocol and not an "
        "authorization to collect formal primary data.",
        "",
        "## Submission route",
        "",
        f"Current status: `{route['status']}`. Recommended option: "
        f"`{route['recommended_option']}`; action: `{route['recommendation_action']}`.",
        "The regular-submission fallback preserves H3, the formal design, analysis and "
        "failure rules; it cannot be selected in response to formal outcomes.",
        "",
        "## Confirmatory question and hypothesis",
        "",
        str(report["research_question"]),
        "",
        f"Primary hypothesis: `{hypothesis['id']}`. Registered contrast: "
        f"`{hypothesis['primary_contrast']}` with `{hypothesis['alternative']}`.",
        "Endpoint success alone is not law discovery; environment and method qualification "
        "are not participant outcomes.",
        "",
        "## Frozen formal population",
        "",
        f"The public matrix contains {population['tasks']} tasks, "
        f"{population['independent_task_world_clusters']} independent task x world clusters, "
        f"{population['participant_cells']} participant cells across "
        f"{', '.join(population['prior_arms'])}, and "
        f"{population['complete_experiments']} planned complete experiments.",
        f"It retains {population['belief_checkpoints']} typed belief checkpoints, "
        f"{population['provider_sessions']} accepted provider sessions and a hard cap of "
        f"{population['provider_attempts_hard_cap']} host provider-process attempts.",
        "",
        "## Outcome-neutral quality and failure rules",
        "",
        "Gate A, the formal-design audit and the power/resource audit must pass before "
        "execution. The current method must independently pass the real-provider three-arm "
        "qualification. Exact replay and the combined execution audit are mandatory.",
        "Scientific failures and right-censored cells are retained without replacement; only "
        "missing infrastructure may resume, and a persisted scientific trajectory forbids "
        "replacement. Result-direction early stopping is forbidden.",
        "",
        "## Private confirmation",
        "",
        f"Only commitment `{report['private_confirmation']['sealed_identity_commitment_sha256']}` "
        "is public. Private identities are absent from this draft and execute once after the "
        "public analysis is frozen.",
        "",
        "## Pilot boundary",
        "",
        "All existing Gate A, provider shakedown and development campaigns remain pilot, "
        "environment-qualification or method-qualification evidence. They are excluded from "
        "the 75-cell participant denominator and from H3.",
        "",
        "## Current blockers",
        "",
        *[f"- `{item}`" for item in blockers],
        "",
        "## Policy sources checked on 2026-08-10",
        "",
        *[f"- [{item['source_id']}]({item['url']})" for item in policy_sources],
        "",
    ]
    return "\n".join(lines)


__all__ = [
    "NATURE_REGISTERED_REPORT_EXPANSION_URL",
    "NATURE_REGISTERED_REPORT_GUIDELINES_URL",
    "PREREGISTRATION_READINESS_VERSION",
    "ROUTE_OPTIONS",
    "SUBMISSION_ROUTE_DECISION_VERSION",
    "build_preregistration_readiness",
    "preregistration_readiness_sha256",
    "render_preregistration_draft",
    "route_decision_sha256",
    "validate_preregistration_readiness",
    "validate_submission_route_decision",
]
