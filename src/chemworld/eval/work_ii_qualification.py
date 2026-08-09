"""Fail-closed readiness and authorization gates for Work II qualification."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import (
    EXPECTED_METHOD_QUALIFICATION_CONTRACT,
    FORMAL_ARMS,
    FORMAL_SNAPSHOT_STAGES,
    build_formal_preflight,
    validate_formal_preflight,
)

METHOD_QUALIFICATION_REPORT_VERSION = "chemworld-work-ii-campaign-pilot-report-0.3"
METHOD_QUALIFICATION_READINESS_VERSION = "chemworld-work-ii-method-qualification-readiness-0.1"
METHOD_QUALIFICATION_RECEIPT_VERSION = "chemworld-work-ii-method-qualification-receipt-0.3"
METHOD_QUALIFICATION_EXECUTION_AUTHORIZATION_VERSION = (
    "chemworld-work-ii-method-qualification-execution-authorization-0.1"
)
REQUIRED_CELL_QUALIFICATION_CHECKS = (
    "planned_complete_experiments",
    "four_typed_belief_checkpoints",
    "one_campaign_session",
    "provider_session_completed",
    "final_recommendation_committed",
    "tool_integrity",
    "no_resource_rejection",
    "campaign_terminal",
    "process_time_reconciled",
    "task_required_operations_reconciled",
    "exact_replay",
    "execution_audit",
    "provider_usage_reconciled",
)


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: value for key, value in payload.items() if key != field})


def _is_finite_number(value: object, *, minimum: float = 0.0) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int | float)
        and math.isfinite(float(value))
        and float(value) >= minimum
    )


def _finite_float(value: object, *, minimum: float = 0.0) -> float | None:
    if not _is_finite_number(value, minimum=minimum):
        return None
    assert not isinstance(value, bool) and isinstance(value, int | float)
    return float(value)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _task_binding(manifest: Mapping[str, Any], task_id: str) -> Mapping[str, Any] | None:
    rows = manifest.get("task_bindings")
    if not isinstance(rows, list):
        return None
    matches = [row for row in rows if isinstance(row, Mapping) and row.get("task_id") == task_id]
    return matches[0] if len(matches) == 1 else None


def method_qualification_report_sha256(report: Mapping[str, Any]) -> str:
    """Return the embedded content hash for a qualification report."""

    return _self_hash(report, "report_sha256")


def method_qualification_readiness_sha256(report: Mapping[str, Any]) -> str:
    """Return the embedded content hash for a readiness report."""

    return _self_hash(report, "readiness_sha256")


def qualification_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def qualification_execution_authorization_sha256(
    authorization: Mapping[str, Any],
) -> str:
    return _self_hash(authorization, "authorization_sha256")


def build_qualification_execution_authorization(
    manifest: Mapping[str, Any],
    *,
    currency_ceiling_usd: float,
    approved_at: str,
) -> dict[str, Any]:
    """Build the credential-free authorization that must exist before provider execution."""

    contract = manifest.get("method_qualification_contract")
    contract = contract if isinstance(contract, Mapping) else {}
    task_id = str(contract.get("qualification_task_id", ""))
    task_binding = _task_binding(manifest, task_id)
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    campaign_binding = campaign_binding if isinstance(campaign_binding, Mapping) else {}
    authorization: dict[str, Any] = {
        "schema_version": METHOD_QUALIFICATION_EXECUTION_AUTHORIZATION_VERSION,
        "status": "authorized",
        "formal_result": False,
        "provider_execution_allowed": True,
        "formal_execution_authorized": False,
        "formal_participant_outcome_count_before_authorization": 0,
        "formal_preflight_sha256": manifest.get("preflight_sha256"),
        "provider_contract_sha256": canonical_json_sha256(manifest.get("provider_contract")),
        "participant_execution_contract_sha256": manifest.get(
            "participant_execution_contract_sha256"
        ),
        "method_qualification_contract_sha256": manifest.get(
            "method_qualification_contract_sha256"
        ),
        "qualification_schedule": {
            "task_id": task_id,
            "world_split": "development_and_qualification",
            "world_seed": contract.get("qualification_world_seed"),
            "prior_arms": list(FORMAL_ARMS),
            "campaign_config_path": campaign_binding.get("path"),
            "campaign_config_sha256": campaign_binding.get("sha256"),
            "provider_process_attempts_initial": 3,
            "provider_process_attempts_hard_cap": 6,
        },
        "user_authorization": {
            "authorized_by": "user",
            "approved_at": approved_at,
            "provider_contract_confirmed": True,
            "credential_rotation_confirmed": True,
            "currency": "USD",
            "currency_ceiling_usd": currency_ceiling_usd,
            "scope_method_qualification_contract_sha256": manifest.get(
                "method_qualification_contract_sha256"
            ),
            "credentials_present": False,
        },
    }
    authorization["authorization_sha256"] = qualification_execution_authorization_sha256(
        authorization
    )
    return authorization


def validate_qualification_execution_authorization(
    authorization: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> list[str]:
    """Validate the explicit pre-call user authorization for the exact qualification triplet."""

    errors: list[str] = []
    if (
        authorization.get("schema_version")
        != METHOD_QUALIFICATION_EXECUTION_AUTHORIZATION_VERSION
    ):
        errors.append("unexpected method-qualification execution authorization schema")
    if authorization.get(
        "authorization_sha256"
    ) != qualification_execution_authorization_sha256(authorization):
        errors.append("method-qualification execution authorization self-hash mismatch")
    if (
        authorization.get("status") != "authorized"
        or authorization.get("provider_execution_allowed") is not True
        or authorization.get("formal_execution_authorized") is not False
        or authorization.get("formal_result") is not False
        or authorization.get("formal_participant_outcome_count_before_authorization") != 0
    ):
        errors.append("method-qualification execution is not outcome-blind authorized")
    if authorization.get("formal_preflight_sha256") != manifest.get("preflight_sha256"):
        errors.append("method-qualification execution binds a different formal preflight")
    expected_bindings = {
        "provider_contract_sha256": canonical_json_sha256(manifest.get("provider_contract")),
        "participant_execution_contract_sha256": manifest.get(
            "participant_execution_contract_sha256"
        ),
        "method_qualification_contract_sha256": manifest.get(
            "method_qualification_contract_sha256"
        ),
    }
    for field, expected in expected_bindings.items():
        if authorization.get(field) != expected:
            errors.append(f"method-qualification execution has a mismatched {field}")
    contract = manifest.get("method_qualification_contract")
    contract = contract if isinstance(contract, Mapping) else {}
    task_binding = _task_binding(manifest, str(contract.get("qualification_task_id", "")))
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    campaign_binding = campaign_binding if isinstance(campaign_binding, Mapping) else {}
    schedule = authorization.get("qualification_schedule")
    schedule = schedule if isinstance(schedule, Mapping) else {}
    if schedule != {
        "task_id": contract.get("qualification_task_id"),
        "world_split": "development_and_qualification",
        "world_seed": contract.get("qualification_world_seed"),
        "prior_arms": list(FORMAL_ARMS),
        "campaign_config_path": campaign_binding.get("path"),
        "campaign_config_sha256": campaign_binding.get("sha256"),
        "provider_process_attempts_initial": 3,
        "provider_process_attempts_hard_cap": 6,
    }:
        errors.append("method-qualification execution schedule is not the frozen triplet")
    user = authorization.get("user_authorization")
    user = user if isinstance(user, Mapping) else {}
    ceiling = user.get("currency_ceiling_usd")
    if (
        user.get("authorized_by") != "user"
        or not isinstance(user.get("approved_at"), str)
        or not user.get("approved_at")
        or user.get("provider_contract_confirmed") is not True
        or user.get("credential_rotation_confirmed") is not True
        or user.get("currency") != "USD"
        or not _is_finite_number(ceiling, minimum=0.000000001)
        or user.get("scope_method_qualification_contract_sha256")
        != manifest.get("method_qualification_contract_sha256")
        or user.get("credentials_present") is not False
    ):
        errors.append("method-qualification execution lacks valid user/provider/currency approval")
    return errors


def validate_method_qualification_report(
    root: Path,
    report: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> list[str]:
    """Validate the scientific-process contents of a three-arm qualification report."""

    errors: list[str] = []
    contract = manifest.get("method_qualification_contract")
    if contract != EXPECTED_METHOD_QUALIFICATION_CONTRACT:
        errors.append("qualification report was checked against an invalid gate contract")
        contract = EXPECTED_METHOD_QUALIFICATION_CONTRACT
    if report.get("schema_version") != METHOD_QUALIFICATION_REPORT_VERSION:
        errors.append("unexpected method qualification report schema")
    if report.get("report_sha256") != method_qualification_report_sha256(report):
        errors.append("method qualification report self-hash mismatch")
    if report.get("formal_result") is not False:
        errors.append("method qualification report is mislabeled as a formal result")
    if report.get("qualification_execution_authorized") is not True:
        errors.append("method qualification report lacks pre-execution user authorization")
    authorization_binding = report.get("qualification_execution_authorization_binding")
    if not isinstance(authorization_binding, Mapping):
        errors.append("method qualification report lacks its execution-authorization binding")
    else:
        relative = authorization_binding.get("path")
        digest = authorization_binding.get("sha256")
        embedded = authorization_binding.get("authorization_sha256")
        if not isinstance(relative, str) or not isinstance(digest, str):
            errors.append("method qualification execution-authorization binding is incomplete")
        else:
            root = root.resolve()
            authorization_path = (root / relative).resolve()
            try:
                authorization_path.relative_to(root)
            except ValueError:
                errors.append("method qualification execution authorization escapes the repository")
            else:
                if (
                    not authorization_path.is_file()
                    or file_sha256(authorization_path) != digest
                ):
                    errors.append(
                        "method qualification execution authorization is missing or stale"
                    )
                else:
                    loaded = json.loads(authorization_path.read_text(encoding="utf-8"))
                    if not isinstance(loaded, dict):
                        errors.append(
                            "method qualification execution authorization is not an object"
                        )
                    else:
                        if loaded.get("authorization_sha256") != embedded:
                            errors.append(
                                "method qualification embedded execution authorization is stale"
                            )
                        errors.extend(
                            validate_qualification_execution_authorization(loaded, manifest)
                        )
    if report.get("world_seed") != contract["qualification_world_seed"]:
        errors.append("method qualification report uses the wrong development world")
    if (
        report.get("cell_count") != contract["qualification_cell_count"]
        or report.get("completed_cell_count") != contract["qualification_cell_count"]
    ):
        errors.append("method qualification report does not complete three cells")

    task_id = str(contract["qualification_task_id"])
    task_binding = _task_binding(manifest, task_id)
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    if not isinstance(campaign_binding, Mapping):
        errors.append("method qualification report lacks a frozen task binding")
    elif report.get("config_file_sha256") != campaign_binding.get("sha256"):
        errors.append("method qualification report used a different campaign config")
    if not _is_sha256(report.get("config_sha256")):
        errors.append("method qualification report lacks its canonical config hash")

    rows = report.get("results")
    if not isinstance(rows, list):
        errors.append("method qualification report results are missing")
        return errors
    observed_arms = [row.get("arm") for row in rows if isinstance(row, Mapping)]
    if len(rows) != 3 or tuple(observed_arms) != FORMAL_ARMS:
        errors.append("method qualification report does not retain the exact arm triplet")

    provider = manifest.get("provider_contract")
    provider = provider if isinstance(provider, Mapping) else {}
    for index, raw_row in enumerate(rows):
        arm = FORMAL_ARMS[index] if index < len(FORMAL_ARMS) else f"cell_{index + 1}"
        if not isinstance(raw_row, Mapping):
            errors.append(f"{arm}: method qualification cell is malformed")
            continue
        if raw_row.get("completed") is not True or raw_row.get("failure") is not None:
            errors.append(f"{arm}: method qualification cell did not complete")
        qualification = raw_row.get("qualification")
        qualification = qualification if isinstance(qualification, Mapping) else {}
        checks = qualification.get("checks")
        checks = checks if isinstance(checks, Mapping) else {}
        if (
            qualification.get("passed") is not True
            or qualification.get("failed_checks") != []
            or tuple(checks) != REQUIRED_CELL_QUALIFICATION_CHECKS
            or any(checks.get(name) is not True for name in REQUIRED_CELL_QUALIFICATION_CHECKS)
        ):
            errors.append(f"{arm}: fail-closed cell qualification did not pass")

        replay = raw_row.get("exact_replay")
        replay = replay if isinstance(replay, Mapping) else {}
        if replay.get("verified") is not True or replay.get("mismatches") != []:
            errors.append(f"{arm}: exact replay did not pass")

        analysis = raw_row.get("analysis")
        analysis = analysis if isinstance(analysis, Mapping) else {}
        experiments = analysis.get("experiments")
        experiments = experiments if isinstance(experiments, list) else []
        experiment_indices = [
            item.get("experiment_index") for item in experiments if isinstance(item, Mapping)
        ]
        snapshots = analysis.get("belief_snapshots")
        snapshots = snapshots if isinstance(snapshots, list) else []
        snapshot_stages = [item.get("stage") for item in snapshots if isinstance(item, Mapping)]
        resources = analysis.get("final_campaign_resources")
        resources = resources if isinstance(resources, Mapping) else {}
        state = resources.get("state")
        state = state if isinstance(state, Mapping) else {}
        audit = analysis.get("execution_audit")
        audit = audit if isinstance(audit, Mapping) else {}
        recommendation = analysis.get("final_recommendation")
        recommendation = recommendation if isinstance(recommendation, Mapping) else {}
        recommendation_hash = canonical_json_sha256(recommendation) if recommendation else None
        if (
            analysis.get("complete_experiment_count") != 4
            or analysis.get("right_censored_open_experiment") is not False
            or experiment_indices != [1, 2, 3, 4]
            or snapshot_stages != list(FORMAL_SNAPSHOT_STAGES)
            or analysis.get("resource_rejection_count") != 0
            or resources.get("campaign_terminal") is not True
            or state.get("closed_batches") != 4
            or state.get("final_assays") != 4
            or audit.get("passed") is not True
            or recommendation_hash != analysis.get("final_recommendation_sha256")
        ):
            errors.append(f"{arm}: campaign lifecycle or execution audit is incomplete")

        usage = raw_row.get("method_resources")
        usage = usage if isinstance(usage, Mapping) else {}
        provenance = usage.get("model_provenance")
        provenance = provenance if isinstance(provenance, Mapping) else {}
        parameters = provenance.get("request_parameters")
        parameters = parameters if isinstance(parameters, Mapping) else {}
        token_fields = (
            "input_token_count",
            "uncached_input_token_count",
            "output_token_count",
        )
        if (
            usage.get("provider_session_count") != 1
            or usage.get("model_call_count") != 1
            or usage.get("provider_usage_pending") is not False
            or usage.get("provider_usage_accounting_complete") is not True
            or usage.get("in_flight_model_call_count") != 0
            or any(not _is_finite_number(usage.get(field)) for field in token_fields)
            or provenance.get("provider_id") != provider.get("id")
            or provenance.get("model_id") != provider.get("model")
            or parameters.get("reasoning_effort") != provider.get("reasoning_effort")
        ):
            errors.append(f"{arm}: provider/session/resource accounting is invalid")

        receipts = raw_row.get("provider_receipts")
        receipts = receipts if isinstance(receipts, list) else []
        receipt = receipts[0] if len(receipts) == 1 and isinstance(receipts[0], Mapping) else {}
        if (
            len(receipts) != 1
            or receipt.get("session_scope") != "campaign"
            or receipt.get("status") != "completed"
            or receipt.get("return_code") != 0
            or receipt.get("final_payload_valid") is not True
            or receipt.get("final_payload_status") != "campaign_complete"
            or receipt.get("final_recommendation_sha256") != recommendation_hash
            or receipt.get("experiment_tool_integrity_verified_after_session") is not True
            or receipt.get("lab_tool_integrity_verified_after_session") is not True
            or receipt.get("mcp_tool_integrity_verified_after_session") is not True
            or receipt.get("model_id") != provider.get("model")
            or receipt.get("reasoning_effort") != provider.get("reasoning_effort")
            or receipt.get("usage_complete") is not True
        ):
            errors.append(f"{arm}: provider receipt is invalid")
    return errors


def _historical_binding(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    return {
        "path": relative,
        "sha256": file_sha256(path) if path.is_file() else None,
        "present": path.is_file(),
    }


def build_method_qualification_readiness(
    root: Path,
    design_path: Path,
    analysis_path: Path,
) -> dict[str, Any]:
    """Build a deterministic, zero-provider-call readiness report for W2-10."""

    root = root.resolve()
    manifest = build_formal_preflight(root, design_path, analysis_path)
    internal_errors = [*manifest.get("errors", []), *validate_formal_preflight(manifest)]
    contract = manifest.get("method_qualification_contract")
    contract = contract if isinstance(contract, Mapping) else {}
    task_id = str(contract.get("qualification_task_id", ""))
    task_binding = _task_binding(manifest, task_id)
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    campaign_binding = campaign_binding if isinstance(campaign_binding, Mapping) else {}
    config_path = root / str(campaign_binding.get("path", ""))
    config: dict[str, Any] = {}
    if config_path.is_file():
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            config = loaded
    if not config:
        internal_errors.append("qualification campaign config is missing")
    if config.get("task_id") != task_id:
        internal_errors.append("qualification task differs from its campaign config")
    if tuple(config.get("prior_arms", {})) != FORMAL_ARMS:
        internal_errors.append("qualification campaign does not preserve the arm triplet")
    execution = config.get("execution")
    execution = execution if isinstance(execution, Mapping) else {}
    if execution.get("failure_semantics") != (
        "finish the in-flight seed triplet, then stop before the next world seed"
    ):
        internal_errors.append("qualification triplet failure semantics are not frozen")
    campaign = config.get("campaign")
    campaign = campaign if isinstance(campaign, Mapping) else {}
    limits = config.get("method_resources")
    limits = limits if isinstance(limits, Mapping) else {}
    provider = manifest.get("provider_contract")
    provider = provider if isinstance(provider, Mapping) else {}
    config_provider = config.get("provider")
    config_provider = config_provider if isinstance(config_provider, Mapping) else {}
    if any(
        config_provider.get(field) != provider.get(field)
        for field in (
            "id",
            "name",
            "base_url",
            "wire_api",
            "model",
            "reasoning_effort",
            "request_timeout_s",
            "finalization_timeout_s",
        )
    ):
        internal_errors.append("qualification provider differs from the formal method")

    old_wellau = _historical_binding(
        root,
        "workstreams/flagship_tasks/reports/work-ii-seed0-persistent-campaign-pilot.json",
    )
    deepseek = _historical_binding(
        root,
        "workstreams/flagship_tasks/reports/work-ii-deepseek-codex-harness-diagnosis.md",
    )
    if not old_wellau["present"] or not deepseek["present"]:
        internal_errors.append("historical qualification evidence binding is missing")

    cell_count = int(contract.get("qualification_cell_count", 0))
    attempts_per_cell = 1 + int(contract.get("maximum_infrastructure_resume_attempts_per_cell", 0))
    expected_counts = {
        "accepted_scientific_cells": cell_count,
        "accepted_scientific_codex_processes": cell_count,
        "accepted_provider_sessions": cell_count,
        "accepted_participant_model_calls": cell_count,
        "complete_experiments": cell_count * int(campaign.get("complete_experiments", 0)),
        "belief_checkpoints": cell_count * int(contract.get("belief_checkpoints_per_cell", 0)),
        "operation_attempts_hard_cap": cell_count * int(campaign.get("operation_attempt_limit", 0)),
        "provider_process_attempts_initial": cell_count,
        "provider_process_attempts_hard_cap": cell_count * attempts_per_cell,
        "input_tokens_accepted_cell_cap": cell_count * int(limits.get("input_token_limit", 0)),
        "uncached_input_tokens_accepted_cell_cap": cell_count
        * int(limits.get("uncached_input_token_limit", 0)),
        "output_tokens_accepted_cell_cap": cell_count * int(limits.get("output_token_limit", 0)),
        "accepted_cell_wall_time_cap_s": cell_count * float(limits.get("wall_time_limit_s", 0.0)),
    }
    blockers = [
        "user must confirm the current provider contract or approve an explicit amendment",
        "user must confirm that the provider credential was rotated after exposure",
        "user must approve a qualification currency ceiling bound to the frozen gate contract",
        "the real-provider three-arm qualification triplet has not been executed",
    ]
    report: dict[str, Any] = {
        "schema_version": METHOD_QUALIFICATION_READINESS_VERSION,
        "status": "failed" if internal_errors else "passed_provider_execution_blocked",
        "formal_result": False,
        "provider_execution_allowed": False,
        "formal_execution_authorized": False,
        "provider_calls_executed": 0,
        "formal_participant_outcomes_before_authorization": 0,
        "formal_preflight_sha256": manifest.get("preflight_sha256"),
        "method_qualification_contract": dict(contract),
        "method_qualification_contract_sha256": canonical_json_sha256(contract),
        "participant_execution_contract_sha256": manifest.get(
            "participant_execution_contract_sha256"
        ),
        "provider_contract": dict(provider),
        "provider_contract_sha256": canonical_json_sha256(provider),
        "held_out_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("held_out_evaluator_contract")
        ),
        "qualification_schedule": {
            "task_id": task_id,
            "world_cohort": contract.get("qualification_world_cohort"),
            "world_seed": contract.get("qualification_world_seed"),
            "prior_arms": list(FORMAL_ARMS),
            "campaign_config": dict(campaign_binding),
            "runner": "scripts/run_work_ii_campaign_pilot.py",
            "required_execution_flags": [
                "--qualification-execution",
                "--qualification-authorization",
            ],
            "authorization_builder": (
                "scripts/authorize_work_ii_method_qualification.py"
            ),
            "authorization_schema": METHOD_QUALIFICATION_EXECUTION_AUTHORIZATION_VERSION,
            "report_schema": METHOD_QUALIFICATION_REPORT_VERSION,
            "receipt_builder": "scripts/build_work_ii_method_qualification_receipt.py",
            "receipt_schema": METHOD_QUALIFICATION_RECEIPT_VERSION,
            "output_scope": "runs/development",
            "triplet_failure_semantics": contract.get("triplet_failure_semantics"),
        },
        "expected_counts": expected_counts,
        "historical_evidence_assessment": [
            {
                "evidence_id": "wellau_seed0_2026_08_08",
                "binding": old_wellau,
                "eligible_for_current_method_receipt": False,
                "reasons": [
                    "public resource card exposed prior-arm identity",
                    "source predates the current participant execution and qualification contracts",
                ],
            },
            {
                "evidence_id": "deepseek_qualification_v2_seed0_opaque",
                "binding": deepseek,
                "eligible_for_current_method_receipt": False,
                "reasons": [
                    "covered only the opaque arm rather than the frozen three-arm triplet",
                    (
                        "used a provider and sampling contract different from the current "
                        "formal method"
                    ),
                ],
            },
        ],
        "blocking_requirements": blockers,
        "internal_errors": internal_errors,
    }
    report["readiness_sha256"] = method_qualification_readiness_sha256(report)
    return report


def validate_method_qualification_readiness(report: Mapping[str, Any]) -> list[str]:
    """Validate that readiness is deterministic, zero-call, and still blocked."""

    errors: list[str] = []
    if report.get("schema_version") != METHOD_QUALIFICATION_READINESS_VERSION:
        errors.append("unexpected method qualification readiness schema")
    if report.get("readiness_sha256") != method_qualification_readiness_sha256(report):
        errors.append("method qualification readiness self-hash mismatch")
    if report.get("status") != "passed_provider_execution_blocked":
        errors.append("method qualification readiness did not pass internal checks")
    if report.get("internal_errors") != []:
        errors.append("method qualification readiness has internal errors")
    if (
        report.get("formal_result") is not False
        or report.get("provider_execution_allowed") is not False
        or report.get("formal_execution_authorized") is not False
        or report.get("provider_calls_executed") != 0
        or report.get("formal_participant_outcomes_before_authorization") != 0
    ):
        errors.append("method qualification readiness crossed the execution boundary")
    contract = report.get("method_qualification_contract")
    if contract != EXPECTED_METHOD_QUALIFICATION_CONTRACT or report.get(
        "method_qualification_contract_sha256"
    ) != canonical_json_sha256(EXPECTED_METHOD_QUALIFICATION_CONTRACT):
        errors.append("method qualification readiness has an invalid gate contract")
    counts = report.get("expected_counts")
    counts = counts if isinstance(counts, Mapping) else {}
    if (
        counts.get("accepted_scientific_cells") != 3
        or counts.get("complete_experiments") != 12
        or counts.get("belief_checkpoints") != 12
        or counts.get("provider_process_attempts_hard_cap") != 6
    ):
        errors.append("method qualification readiness denominators are invalid")
    blockers = report.get("blocking_requirements")
    if not isinstance(blockers, list) or len(blockers) != 4:
        errors.append("method qualification readiness lacks its external blockers")
    return errors


def build_method_qualification_receipt(
    root: Path,
    report_path: Path,
    manifest: Mapping[str, Any],
    *,
    observed_cost_usd: float,
    pricing_source: str,
    pricing_observed_at: str,
) -> dict[str, Any]:
    """Build the formal authorization receipt from one validated three-arm report."""

    root = root.resolve()
    report_path = report_path.resolve()
    try:
        relative_report = report_path.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError("qualification report must be inside the repository") from error
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("qualification report must contain an object")
    report_errors = validate_method_qualification_report(root, report, manifest)
    if report_errors:
        raise ValueError("invalid method qualification report: " + "; ".join(report_errors))
    authorization_binding = report["qualification_execution_authorization_binding"]
    authorization_path = root / str(authorization_binding["path"])
    authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
    if not isinstance(authorization, dict):
        raise ValueError("qualification execution authorization must contain an object")
    authorization_errors = validate_qualification_execution_authorization(
        authorization, manifest
    )
    if authorization_errors:
        raise ValueError(
            "invalid qualification execution authorization: "
            + "; ".join(authorization_errors)
        )
    user = authorization["user_authorization"]
    ceiling = float(user["currency_ceiling_usd"])
    if (
        not _is_finite_number(observed_cost_usd)
        or float(observed_cost_usd) > ceiling
        or not pricing_source
        or not pricing_observed_at
    ):
        raise ValueError("qualification cost accounting is incomplete or exceeds approval")
    contract = EXPECTED_METHOD_QUALIFICATION_CONTRACT
    task_binding = _task_binding(manifest, str(contract["qualification_task_id"]))
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    if not isinstance(campaign_binding, Mapping):
        raise ValueError("formal manifest lacks the qualification campaign binding")
    receipt: dict[str, Any] = {
        "schema_version": METHOD_QUALIFICATION_RECEIPT_VERSION,
        "status": "passed",
        "formal_execution_authorized": True,
        "formal_preflight_sha256": manifest.get("preflight_sha256"),
        "provider_contract_sha256": canonical_json_sha256(manifest.get("provider_contract")),
        "provider_attempt_contract_sha256": canonical_json_sha256(
            manifest.get("provider_attempt_contract")
        ),
        "participant_execution_contract_sha256": manifest.get(
            "participant_execution_contract_sha256"
        ),
        "method_qualification_contract_sha256": manifest.get(
            "method_qualification_contract_sha256"
        ),
        "blind_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("blind_evaluator_contract")
        ),
        "held_out_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("held_out_evaluator_contract")
        ),
        "qualification_execution_authorization_sha256": authorization.get(
            "authorization_sha256"
        ),
        "qualification_split": "development_seed_0",
        "qualification_task_id": contract["qualification_task_id"],
        "qualification_world_seed": contract["qualification_world_seed"],
        "qualification_campaign_config_sha256": campaign_binding.get("sha256"),
        "qualified_prior_arms": list(FORMAL_ARMS),
        "qualified_cell_count": 3,
        "formal_participant_outcome_count_before_authorization": 0,
        "approved_provider_attempt_hard_cap": manifest.get("expected_counts", {}).get(
            "provider_attempts_hard_cap"
        ),
        "qualification_cost_accounting": {
            "currency": "USD",
            "accounting_complete": True,
            "observed_cost_usd": float(observed_cost_usd),
            "approved_ceiling_usd": ceiling,
            "approved_by": "user",
            "approved_at": user["approved_at"],
            "pricing_source": pricing_source,
            "pricing_observed_at": pricing_observed_at,
            "scope_method_qualification_contract_sha256": manifest.get(
                "method_qualification_contract_sha256"
            ),
        },
        "approved_currency_ceiling_usd": ceiling,
        "currency_approval": {
            "approved_by": "user",
            "approved_at": user["approved_at"],
            "approved_currency_ceiling_usd": ceiling,
            "scope_preflight_sha256": manifest.get("preflight_sha256"),
        },
        "qualification_report_binding": {
            "path": relative_report,
            "sha256": file_sha256(report_path),
            "report_sha256": report.get("report_sha256"),
        },
    }
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    errors = validate_method_qualification_receipt(
        root,
        receipt,
        manifest,
        currency_ceiling_usd=ceiling,
    )
    if errors:
        raise ValueError("built method qualification receipt is invalid: " + "; ".join(errors))
    return receipt


def validate_method_qualification_receipt(
    root: Path,
    receipt: Mapping[str, Any],
    manifest: Mapping[str, Any],
    *,
    currency_ceiling_usd: float,
) -> list[str]:
    """Validate method qualification, user cost approval and artifact binding."""

    errors: list[str] = []
    if receipt.get("schema_version") != METHOD_QUALIFICATION_RECEIPT_VERSION:
        errors.append("unexpected method qualification receipt schema")
    if receipt.get("receipt_sha256") != qualification_receipt_sha256(receipt):
        errors.append("method qualification receipt self-hash mismatch")
    if receipt.get("status") != "passed" or receipt.get("formal_execution_authorized") is not True:
        errors.append("method qualification receipt does not authorize formal execution")
    if receipt.get("formal_preflight_sha256") != manifest.get("preflight_sha256"):
        errors.append("method qualification receipt binds a different formal preflight")
    expected_bindings = {
        "provider_contract_sha256": canonical_json_sha256(manifest.get("provider_contract")),
        "provider_attempt_contract_sha256": canonical_json_sha256(
            manifest.get("provider_attempt_contract")
        ),
        "participant_execution_contract_sha256": manifest.get(
            "participant_execution_contract_sha256"
        ),
        "method_qualification_contract_sha256": manifest.get(
            "method_qualification_contract_sha256"
        ),
        "blind_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("blind_evaluator_contract")
        ),
        "held_out_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("held_out_evaluator_contract")
        ),
    }
    for field, expected in expected_bindings.items():
        if receipt.get(field) != expected:
            errors.append(f"method qualification receipt has a mismatched {field}")
    contract = EXPECTED_METHOD_QUALIFICATION_CONTRACT
    if receipt.get("qualification_split") != "development_seed_0":
        errors.append("method qualification receipt uses the wrong development split")
    if receipt.get("qualification_task_id") != contract["qualification_task_id"]:
        errors.append("method qualification receipt uses the wrong qualification task")
    if receipt.get("qualification_world_seed") != contract["qualification_world_seed"]:
        errors.append("method qualification receipt uses the wrong qualification world")
    if receipt.get("qualified_prior_arms") != list(FORMAL_ARMS):
        errors.append("method qualification receipt does not cover the exact three arms")
    if receipt.get("qualified_cell_count") != 3:
        errors.append("method qualification receipt does not cover three development cells")
    if receipt.get("formal_participant_outcome_count_before_authorization") != 0:
        errors.append("formal participant outcomes existed before method authorization")
    task_binding = _task_binding(manifest, str(contract["qualification_task_id"]))
    campaign_binding = (
        task_binding.get("campaign_config") if isinstance(task_binding, Mapping) else None
    )
    if not isinstance(campaign_binding, Mapping) or receipt.get(
        "qualification_campaign_config_sha256"
    ) != campaign_binding.get("sha256"):
        errors.append("method qualification receipt binds a different campaign config")
    attempt_cap = manifest.get("expected_counts", {}).get("provider_attempts_hard_cap")
    if receipt.get("approved_provider_attempt_hard_cap") != attempt_cap:
        errors.append("method qualification receipt has a mismatched provider-attempt cap")

    qualification_cost = receipt.get("qualification_cost_accounting")
    qualification_cost = qualification_cost if isinstance(qualification_cost, Mapping) else {}
    observed_cost = qualification_cost.get("observed_cost_usd")
    qualification_ceiling = qualification_cost.get("approved_ceiling_usd")
    observed_cost_value = _finite_float(observed_cost)
    qualification_ceiling_value = _finite_float(
        qualification_ceiling, minimum=0.000000001
    )
    if (
        qualification_cost.get("currency") != "USD"
        or qualification_cost.get("accounting_complete") is not True
        or qualification_cost.get("approved_by") != "user"
        or not isinstance(qualification_cost.get("approved_at"), str)
        or not qualification_cost.get("approved_at")
        or not isinstance(qualification_cost.get("pricing_source"), str)
        or not qualification_cost.get("pricing_source")
        or not isinstance(qualification_cost.get("pricing_observed_at"), str)
        or not qualification_cost.get("pricing_observed_at")
        or observed_cost_value is None
        or qualification_ceiling_value is None
        or (
            observed_cost_value is not None
            and qualification_ceiling_value is not None
            and observed_cost_value > qualification_ceiling_value
        )
        or qualification_cost.get("scope_method_qualification_contract_sha256")
        != manifest.get("method_qualification_contract_sha256")
    ):
        errors.append("method qualification receipt has invalid qualification cost accounting")

    approved = receipt.get("approved_currency_ceiling_usd")
    approved_value = _finite_float(approved, minimum=0.000000001)
    if approved_value is None or approved_value != float(currency_ceiling_usd):
        errors.append("method qualification receipt has a mismatched currency ceiling")
    if approved_value is not None and (
        qualification_ceiling_value is None
        or qualification_ceiling_value != approved_value
    ):
        errors.append("qualification cost ceiling differs from the user-approved ceiling")
    approval = receipt.get("currency_approval")
    if not isinstance(approval, Mapping):
        errors.append("method qualification receipt lacks user currency approval")
    elif (
        approval.get("approved_by") != "user"
        or approval.get("scope_preflight_sha256") != manifest.get("preflight_sha256")
        or approval.get("approved_currency_ceiling_usd") != approved
        or not isinstance(approval.get("approved_at"), str)
        or not approval.get("approved_at")
    ):
        errors.append("method qualification receipt has invalid user currency approval")

    binding = receipt.get("qualification_report_binding")
    if not isinstance(binding, Mapping):
        errors.append("method qualification receipt lacks its report binding")
    else:
        relative = binding.get("path")
        digest = binding.get("sha256")
        embedded_digest = binding.get("report_sha256")
        if not isinstance(relative, str) or not isinstance(digest, str):
            errors.append("method qualification report binding is incomplete")
        else:
            root = root.resolve()
            path = (root / relative).resolve()
            try:
                path.relative_to(root)
            except ValueError:
                errors.append("method qualification report binding escapes the repository")
            else:
                if not path.is_file() or file_sha256(path) != digest:
                    errors.append("method qualification report binding is missing or stale")
                else:
                    loaded = json.loads(path.read_text(encoding="utf-8"))
                    if not isinstance(loaded, dict):
                        errors.append("method qualification report is not an object")
                    else:
                        if loaded.get("report_sha256") != embedded_digest:
                            errors.append("method qualification embedded report hash is stale")
                        authorization_binding = loaded.get(
                            "qualification_execution_authorization_binding"
                        )
                        authorization_binding = (
                            authorization_binding
                            if isinstance(authorization_binding, Mapping)
                            else {}
                        )
                        if receipt.get(
                            "qualification_execution_authorization_sha256"
                        ) != authorization_binding.get("authorization_sha256"):
                            errors.append(
                                "method qualification receipt does not bind pre-call authorization"
                            )
                        errors.extend(validate_method_qualification_report(root, loaded, manifest))
    return errors


__all__ = [
    "METHOD_QUALIFICATION_EXECUTION_AUTHORIZATION_VERSION",
    "METHOD_QUALIFICATION_READINESS_VERSION",
    "METHOD_QUALIFICATION_RECEIPT_VERSION",
    "METHOD_QUALIFICATION_REPORT_VERSION",
    "REQUIRED_CELL_QUALIFICATION_CHECKS",
    "build_method_qualification_readiness",
    "build_qualification_execution_authorization",
    "method_qualification_readiness_sha256",
    "method_qualification_report_sha256",
    "qualification_execution_authorization_sha256",
    "qualification_receipt_sha256",
    "validate_method_qualification_readiness",
    "validate_method_qualification_receipt",
    "validate_method_qualification_report",
    "validate_qualification_execution_authorization",
]
