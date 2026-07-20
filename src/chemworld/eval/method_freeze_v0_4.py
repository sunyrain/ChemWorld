"""Fail-closed preflight audit for the benchmark-v0.5 method freeze.

This module deliberately cannot issue or open a private Bench manifest.  Its
only positive outcome is that the public, Dev-only method evidence is complete
enough for the separate formal preflight issuer to be invoked.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.formal_classic import audit_classic_method_freeze
from chemworld.eval.formal_llm import audit_live_llm_method_freeze
from chemworld.eval.formal_rl import (
    FormalRLContractError,
    audit_formal_rl_contract,
    load_checkpoint_index,
)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_METHOD_FREEZE_PLAN_PATH = ROOT / "configs/benchmark/method_freeze_v0.4.json"

METHOD_FREEZE_PLAN_VERSION = "chemworld-method-freeze-plan-0.4"
METHOD_FREEZE_REPORT_VERSION = "chemworld-method-freeze-audit-0.4"

_REQUIRED_BINDINGS = (
    "formal_protocol",
    "interaction_strata",
    "statistical_plan",
    "reference_plan",
    "classic_freeze",
    "classic_development",
    "operation_baseline_freeze",
    "operation_baseline_development",
    "rl_contract",
    "ppo_checkpoint_index",
    "ppo_development",
    "sac_checkpoint_index",
    "sac_development",
    "llm_freeze",
    "llm_development_plan",
    "llm_development",
    "family_selection",
    "reference_builder_freeze",
    "formal_execution_budget",
)


class MethodFreezeAuditError(ValueError):
    """Raised when a method-freeze plan cannot be parsed safely."""


def load_method_freeze_plan(
    path: str | Path = DEFAULT_METHOD_FREEZE_PLAN_PATH,
) -> dict[str, Any]:
    """Load an exact method-freeze plan, rejecting unsupported schemas."""

    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MethodFreezeAuditError(f"method-freeze plan is unreadable: {exc}") from exc
    if not isinstance(payload, dict):
        raise MethodFreezeAuditError("method-freeze plan must be a JSON object")
    if payload.get("schema_version") != METHOD_FREEZE_PLAN_VERSION:
        raise MethodFreezeAuditError("method-freeze plan schema is unsupported")
    return payload


def audit_method_freeze(
    plan: Mapping[str, Any],
    *,
    root: str | Path = ROOT,
    source_probe: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit public method evidence without touching private Bench material."""

    repository = Path(root).resolve()
    blockers: list[str] = []
    checks: dict[str, bool] = {}
    observed_bindings: dict[str, dict[str, Any]] = {}
    payloads: dict[str, dict[str, Any] | None] = {}

    checks["schema_version"] = plan.get("schema_version") == METHOD_FREEZE_PLAN_VERSION
    checks["plan_status_ready"] = plan.get("status") == "method_freeze_candidate_bench_sealed"
    checks["no_formal_results"] = plan.get("formal_results_present") is False
    checks["benchmark_claim_denied"] = plan.get("benchmark_claim_allowed") is False
    checks["bench_access_denied"] = plan.get("bench_access_allowed") is False
    checks["bench_manifest_issuance_denied"] = plan.get("bench_manifest_issuance_allowed") is False
    checks["issuance_contract_fail_closed"] = _issuance_contract_ready(
        plan.get("issuance_contract")
    )

    raw_bindings = plan.get("artifact_bindings")
    bindings = raw_bindings if isinstance(raw_bindings, Mapping) else {}
    checks["required_artifact_binding_labels"] = set(bindings) == set(_REQUIRED_BINDINGS)
    for label in _REQUIRED_BINDINGS:
        payloads[label] = _audit_json_binding(
            label,
            bindings.get(label),
            root=repository,
            blockers=blockers,
            observed=observed_bindings,
        )

    formal_tasks = _text_tuple(plan.get("formal_core_tasks"))
    protocol = payloads["formal_protocol"] or {}
    interaction = payloads["interaction_strata"] or {}
    statistics = payloads["statistical_plan"] or {}
    reference_plan = payloads["reference_plan"] or {}
    checks["formal_core_tasks_exact"] = bool(formal_tasks) and formal_tasks == tuple(
        (protocol.get("task_roles") or {}).get("formal_core", {})
    )
    access = protocol.get("access_state")
    checks["bench_protocol_still_sealed"] = bool(
        isinstance(access, Mapping)
        and access.get("bench_manifest_initialized") is True
        and access.get("bench_run_started") is False
        and access.get("bench_results_present") is False
        and access.get("bench_values_exposed_to_evaluated_methods") is False
        and access.get("bench_used_for_tuning") is False
        and protocol.get("benchmark_claim_allowed") is False
    )
    checks["protocols_remain_nonresult_controls"] = all(
        item.get("formal_results_present") is False and item.get("benchmark_claim_allowed") is False
        for item in (protocol, interaction, statistics, reference_plan)
    )
    checks["method_scope_matches_preregistration"] = _method_scope_ready(
        plan.get("method_scope"), interaction=interaction, statistics=statistics
    )
    checks["selection_contract_matches_preregistration"] = plan.get(
        "selection_contract"
    ) == statistics.get("family_champion_selection")

    classic_summary = _audit_classic(
        payloads["classic_freeze"],
        payloads["classic_development"],
        root=repository,
        formal_tasks=formal_tasks,
        protocol=protocol,
        observed=observed_bindings,
        blockers=blockers,
    )
    checks["classic_development_ready"] = classic_summary["development_ready"] is True

    baseline_summary = _audit_operation_baselines(
        interaction=interaction,
        freeze=payloads["operation_baseline_freeze"],
        development=payloads["operation_baseline_development"],
        required=_text_tuple(
            (plan.get("method_scope") or {}).get("required_operation_baselines")
            if isinstance(plan.get("method_scope"), Mapping)
            else None
        ),
        blockers=blockers,
    )
    checks["operation_baselines_ready"] = baseline_summary["development_ready"] is True

    rl_contract_summary = _audit_rl_contract(
        payloads["rl_contract"], root=repository, blockers=blockers
    )
    checks["rl_contract_ready"] = rl_contract_summary["controls_ready"] is True
    rl_methods: dict[str, dict[str, Any]] = {}
    raw_rl_contract = plan.get("rl_evidence_contract")
    rl_evidence = raw_rl_contract if isinstance(raw_rl_contract, Mapping) else {}
    raw_method_contracts = rl_evidence.get("methods")
    method_contracts = raw_method_contracts if isinstance(raw_method_contracts, Mapping) else {}
    for method_id in ("ppo", "sac"):
        contract = method_contracts.get(method_id)
        rl_methods[method_id] = _audit_rl_method(
            method_id,
            contract if isinstance(contract, Mapping) else {},
            payloads=payloads,
            observed=observed_bindings,
            root=repository,
            formal_tasks=formal_tasks,
            protocol=protocol,
            blockers=blockers,
        )
    checks["rl_development_ready"] = all(
        item["development_ready"] is True for item in rl_methods.values()
    )

    llm_summary = _audit_llm(
        freeze=payloads["llm_freeze"],
        development_plan=payloads["llm_development_plan"],
        development=payloads["llm_development"],
        contract=plan.get("llm_evidence_contract"),
        observed=observed_bindings,
        blockers=blockers,
    )
    checks["llm_controls_ready"] = llm_summary["controls_ready"] is True
    checks["llm_development_ready"] = llm_summary["development_ready"] is True

    selection_summary = _audit_selection(
        payloads["family_selection"],
        plan=plan,
        statistics=statistics,
        observed=observed_bindings,
        blockers=blockers,
    )
    checks["family_selection_ready"] = selection_summary["ready"] is True

    reference_summary = _audit_reference_independence(
        reference_plan=reference_plan,
        builder_freeze=payloads["reference_builder_freeze"],
        contract=plan.get("reference_independence_contract"),
        method_ids=_text_tuple(
            (plan.get("method_scope") or {}).get("all_declared_method_ids")
            if isinstance(plan.get("method_scope"), Mapping)
            else None
        ),
        root=repository,
        blockers=blockers,
    )
    checks["reference_independence_ready"] = reference_summary["ready"] is True

    budget_summary = _audit_execution_budget(
        payloads["formal_execution_budget"],
        selection=payloads["family_selection"],
        formal_tasks=formal_tasks,
        blockers=blockers,
    )
    checks["formal_execution_budget_ready"] = budget_summary["ready"] is True

    source = dict(source_probe) if source_probe is not None else _probe_repository(repository)
    checks["source_commit_identified"] = _is_git_commit(source.get("commit"))
    # A dirty tree is reported but is not folded into method readiness here: an
    # evidence report is commonly generated as the final uncommitted artifact.
    # The later formal preflight independently requires a clean, digest-bound wheel.
    blockers.extend(f"control:{name}" for name, ready in checks.items() if not ready)
    blockers = sorted(set(blockers))
    readiness_checks = {
        name: ready for name, ready in checks.items() if name not in {"source_commit_identified"}
    }
    method_freeze_ready = all(readiness_checks.values()) and not blockers
    if not method_freeze_ready:
        blockers.append("method_freeze:development_incomplete")
        blockers = sorted(set(blockers))

    return {
        "schema_version": METHOD_FREEZE_REPORT_VERSION,
        "status": (
            "method_freeze_preflight_ready"
            if method_freeze_ready
            else "method_freeze_preflight_blocked"
        ),
        "method_freeze_ready": method_freeze_ready,
        "preflight_issuance_allowed": method_freeze_ready,
        "bench_unlock_allowed": False,
        "bench_manifest_issued": False,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "force_override_available": False,
        "private_bench_manifest_opened": False,
        "plan_sha256": _canonical_sha256(plan),
        "source_commit": source.get("commit") if _is_git_commit(source.get("commit")) else None,
        "source_tree_clean": source.get("clean") is True,
        "checks": checks,
        "blockers": blockers,
        "artifact_bindings": observed_bindings,
        "method_families": {
            "classic": classic_summary,
            "operation_baselines": baseline_summary,
            "rl_contract": rl_contract_summary,
            "rl": rl_methods,
            "llm": llm_summary,
        },
        "selection": selection_summary,
        "reference_independence": reference_summary,
        "formal_execution_budget": budget_summary,
        "limitations": [
            "This report is a public Dev-only control audit, not a benchmark result.",
            "It never reads raw private Bench assignments and cannot issue a Bench manifest.",
            "A ready outcome only permits the separate clean-wheel formal preflight to run.",
        ],
    }


def _audit_json_binding(
    label: str,
    raw: Any,
    *,
    root: Path,
    blockers: list[str],
    observed: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    if not isinstance(raw, Mapping):
        blockers.append(f"artifact:{label}:binding_missing")
        return None
    relative = raw.get("path")
    expected = raw.get("sha256")
    path = _safe_repo_path(root, relative)
    if path is None:
        blockers.append(f"artifact:{label}:path_unsafe")
        return None
    if not _is_sha256(expected):
        blockers.append(f"artifact:{label}:expected_sha256_missing")
    if path.is_symlink():
        blockers.append(f"artifact:{label}:symlink_forbidden")
        return None
    if not path.is_file():
        blockers.append(f"artifact:{label}:file_missing")
        return None
    digest = artifact_file_sha256(path)
    observed[label] = {"path": str(relative), "sha256": digest}
    if expected != digest:
        blockers.append(f"artifact:{label}:sha256_mismatch")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        blockers.append(f"artifact:{label}:json_invalid")
        return None
    if not isinstance(payload, dict):
        blockers.append(f"artifact:{label}:json_not_object")
        return None
    return payload


def _audit_classic(
    freeze: Mapping[str, Any] | None,
    development: Mapping[str, Any] | None,
    *,
    root: Path,
    formal_tasks: tuple[str, ...],
    protocol: Mapping[str, Any],
    observed: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    if freeze is None or development is None:
        blockers.append("classic:development_evidence_missing")
        return {"controls_ready": False, "development_ready": False}
    audit = audit_classic_method_freeze(freeze, root=root)
    methods = tuple(sorted(freeze.get("methods", {})))
    acceptance = development.get("acceptance")
    ready = bool(
        audit.get("controls_ready") is True
        and development.get("schema_version")
        == "chemworld-classic-development-audit-0.4.1"
        and development.get("status") == "formal_classic_matrix_ready"
        and development.get("formal_classic_matrix_ready") is True
        and development.get("bench_results_present") is False
        and development.get("reference_search_results_used") is False
        and tuple(development.get("tasks", ())) == formal_tasks
        and tuple(sorted(development.get("methods", ()))) == methods
        and isinstance(acceptance, Mapping)
        and all(
            acceptance.get(field) is True
            for field in (
                "all_accounting_complete",
                "all_cells_complete",
                "all_checked_replays_deterministic",
                "all_method_controls_pass",
                "full_preregistered_development_scope",
            )
        )
        and acceptance.get("bench_feedback_used") is False
        and development.get("classic_freeze_sha256") == _canonical_sha256(freeze)
        and development.get("formal_protocol_sha256") == _canonical_sha256(protocol)
    )
    if not ready:
        blockers.append("classic:development_contract_failed")
    return {
        "controls_ready": audit.get("controls_ready") is True,
        "development_ready": ready,
        "method_count": len(methods),
        "cell_count": development.get("cell_count"),
        "complete_experiments_per_cell": development.get("complete_experiments_per_cell"),
        "internal_family_champions": development.get("family_champions"),
        "final_preregistered_recipe_selection_present": False,
        "freeze_file_sha256": (observed.get("classic_freeze") or {}).get("sha256"),
        "development_file_sha256": (observed.get("classic_development") or {}).get("sha256"),
    }


def _audit_operation_baselines(
    *,
    interaction: Mapping[str, Any],
    freeze: Mapping[str, Any] | None,
    development: Mapping[str, Any] | None,
    required: tuple[str, ...],
    blockers: list[str],
) -> dict[str, Any]:
    registrations = interaction.get("methods")
    registrations = registrations if isinstance(registrations, Mapping) else {}
    pending = [
        method_id
        for method_id in required
        if not isinstance(registrations.get(method_id), Mapping)
        or registrations[method_id].get("implementation_status") != "formal_ready"
    ]
    for method_id in pending:
        blockers.append(f"operation_baseline:{method_id}:adapter_not_formal_ready")
    acceptance = development.get("acceptance") if development is not None else None
    acceptance = acceptance if isinstance(acceptance, Mapping) else {}
    summaries = development.get("method_summaries") if development is not None else None
    summaries = summaries if isinstance(summaries, Mapping) else {}
    expected_tasks = (
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    )
    evidence_ready = bool(
        freeze is not None
        and development is not None
        and freeze.get("schema_version") == "chemworld-operation-method-freeze-0.4.1"
        and freeze.get("status") == "dev_frozen_bench_unseen"
        and freeze.get("bench_results_used") is False
        and freeze.get("reference_search_results_used") is False
        and set(freeze.get("methods", {})) == set(required)
        and development.get("schema_version")
        == "chemworld-operation-baseline-development-audit-0.4.1"
        and development.get("status") == "formal_operation_baselines_ready"
        and development.get("formal_operation_baselines_ready") is True
        and development.get("source_tree_clean_at_start") is True
        and development.get("bench_results_present") is False
        and development.get("reference_search_results_used") is False
        and development.get("tasks") == list(expected_tasks)
        and set(development.get("methods", ())) == set(required)
        and development.get("train_seeds") == list(range(10_000, 10_004))
        and development.get("dev_seeds") == list(range(11_000, 11_020))
        and development.get("complete_experiments_per_cell") == 40
        and development.get("cell_count") == 288
        and development.get("operation_freeze_sha256") == _canonical_sha256(freeze)
        and all(
            acceptance.get(key) is True
            for key in (
                "full_preregistered_development_scope",
                "source_tree_clean_at_start",
                "all_method_controls_pass",
                "all_cells_complete",
                "all_primary_values_complete",
                "all_accounting_complete",
                "all_decision_audits_complete",
                "all_checked_replays_deterministic",
                "nonrandom_invalid_controls_pass",
                "action_diversity_controls_pass",
                "rule_measurement_adaptation_controls_pass",
                "operation_random_invalid_actions_retained",
            )
        )
        and acceptance.get("bench_feedback_used") is False
        and acceptance.get("reference_search_feedback_used") is False
        and int(acceptance.get("operation_random_invalid_operation_count", 0)) > 0
        and set(summaries) == set(required)
        and all(
            isinstance(summaries.get(method_id), Mapping)
            and summaries[method_id].get("cell_count") == 96
            and summaries[method_id].get("all_cells_complete") is True
            and summaries[method_id].get("all_primary_values_complete") is True
            and summaries[method_id].get("all_decision_audits_complete") is True
            and summaries[method_id].get("accounting_complete") is True
            and summaries[method_id].get("deterministic_replay") is True
            for method_id in required
        )
        and summaries.get("observation_blind", {}).get("invalid_operation_count") == 0
        and summaries.get("rule_based", {}).get("invalid_operation_count") == 0
    )
    if freeze is None or development is None:
        blockers.append("operation_baseline:development_evidence_missing")
    elif not evidence_ready:
        blockers.append("operation_baseline:development_contract_failed")
    return {
        "required_method_ids": list(required),
        "pending_adapter_method_ids": pending,
        "development_ready": not pending and evidence_ready,
    }


def _audit_rl_contract(
    config: Mapping[str, Any] | None,
    *,
    root: Path,
    blockers: list[str],
) -> dict[str, Any]:
    if config is None:
        blockers.append("rl:contract_missing")
        return {"controls_ready": False}
    audit = audit_formal_rl_contract(config, root=root)
    if audit.get("controls_ready") is not True:
        blockers.extend(f"rl:contract:{item}" for item in audit.get("failed_checks", ()))
    return {
        "controls_ready": audit.get("controls_ready") is True,
        "status": audit.get("status"),
        "required_checkpoint_count": audit.get("required_checkpoint_count"),
        "formal_ready_checkpoint_count": audit.get("formal_ready_checkpoint_count"),
        "config_sha256": audit.get("config_sha256"),
    }


def _audit_rl_method(
    method_id: str,
    contract: Mapping[str, Any],
    *,
    payloads: Mapping[str, Mapping[str, Any] | None],
    observed: Mapping[str, Mapping[str, Any]],
    root: Path,
    formal_tasks: tuple[str, ...],
    protocol: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    index_label = contract.get("checkpoint_index_binding")
    report_label = contract.get("development_binding")
    index = payloads.get(str(index_label)) if isinstance(index_label, str) else None
    report = payloads.get(str(report_label)) if isinstance(report_label, str) else None
    if index is None or report is None:
        blockers.append(f"rl:{method_id}:development_evidence_missing")
        return {
            "development_ready": False,
            "selected_checkpoint_count": 0,
            "expected_selected_checkpoint_count": len(formal_tasks),
            "missing_task_ids": list(formal_tasks),
        }
    checkpoints = index.get("checkpoints")
    entries = checkpoints if isinstance(checkpoints, list) else []
    task_ids = sorted(
        str(item.get("task_id"))
        for item in entries
        if isinstance(item, Mapping) and item.get("method_id") == method_id
    )
    missing_tasks = sorted(set(formal_tasks) - set(task_ids))
    selected_count = len(entries)
    expected_count = len(formal_tasks)
    if selected_count != expected_count:
        blockers.append(
            f"rl:{method_id}:expected_{expected_count}_selected_checkpoints_found_{selected_count}"
        )
    blockers.extend(f"rl:{method_id}:missing_task:{task}" for task in missing_tasks)
    ready_flag = str(contract.get("ready_flag") or "")
    metadata_ready = bool(
        index.get("schema_version") == "chemworld-formal-rl-checkpoint-index-0.4"
        and index.get("status") == contract.get("ready_index_status")
        and index.get(ready_flag) is True
        and index.get("formal_results_present") is False
        and index.get("benchmark_claim_allowed") is False
        and tuple(index.get("formal_core_tasks", ())) == formal_tasks
        and index.get("expected_selected_checkpoint_count") == expected_count
        and index.get("selected_checkpoint_count") == expected_count
        and selected_count == expected_count
        and not missing_tasks
        and report.get("status") == contract.get("ready_report_status")
        and report.get(ready_flag) is True
        and report.get("formal_results_present") is False
        and report.get("benchmark_claim_allowed") is False
        and report.get("selected_checkpoint_count") == expected_count
        and report.get("checkpoint_index_sha256")
        == (observed.get(str(index_label)) or {}).get("sha256")
    )
    bindings_ready = False
    binding_error: str | None = None
    if metadata_ready:
        index_path = (observed.get(str(index_label)) or {}).get("path")
        try:
            bindings = load_checkpoint_index(
                root / str(index_path), root=root, formal_protocol=protocol
            )
        except (FormalRLContractError, OSError, TypeError, ValueError) as exc:
            binding_error = type(exc).__name__
            blockers.append(f"rl:{method_id}:checkpoint_binding_invalid:{binding_error}")
        else:
            bindings_ready = bool(
                len(bindings) == expected_count
                and {item.method_id for item in bindings} == {method_id}
                and {item.task_id for item in bindings} == set(formal_tasks)
            )
    if not metadata_ready:
        blockers.append(f"rl:{method_id}:method_not_ready")
    return {
        "development_ready": metadata_ready and bindings_ready,
        "metadata_ready": metadata_ready,
        "checkpoint_bindings_ready": bindings_ready,
        "checkpoint_binding_error": binding_error,
        "selected_checkpoint_count": selected_count,
        "expected_selected_checkpoint_count": expected_count,
        "missing_task_ids": missing_tasks,
        "index_status": index.get("status"),
        "development_status": report.get("status"),
    }


def _audit_llm(
    *,
    freeze: Mapping[str, Any] | None,
    development_plan: Mapping[str, Any] | None,
    development: Mapping[str, Any] | None,
    contract: Any,
    observed: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    if freeze is None:
        blockers.append("llm:freeze_missing")
        controls_ready = False
        method_ids: list[str] = []
    else:
        audit = audit_live_llm_method_freeze(freeze)
        controls_ready = audit.get("controls_ready") is True
        method_ids = list(audit.get("method_ids", ()))
        if not controls_ready:
            blockers.extend(
                f"llm:freeze:{name}" for name, ready in audit.get("checks", {}).items() if not ready
            )
    contract = contract if isinstance(contract, Mapping) else {}
    stages = development_plan.get("stages") if isinstance(development_plan, Mapping) else None
    candidate = stages.get("candidate_screen") if isinstance(stages, Mapping) else None
    expected_candidate = contract.get("candidate_screen")
    plan_ready = bool(
        development_plan is not None
        and development_plan.get("schema_version") == contract.get("required_plan_schema_version")
        and development_plan.get("bench_access_allowed") is False
        and development_plan.get("benchmark_claim_allowed") is False
        and set(development_plan.get("methods", ())) == set(method_ids)
        and development_plan.get("spectrum_conditions") == ["assigned", "unassigned", "masked"]
        and isinstance(candidate, Mapping)
        and isinstance(expected_candidate, Mapping)
        and dict(candidate) == dict(expected_candidate)
        and "development_matrix" in (stages or {})
        and "development_matrix" in (development_plan.get("promotion_gates") or {})
    )
    if not plan_ready:
        blockers.append("llm:development_plan_invalid")
    if development is None:
        blockers.append("llm:development_matrix:report_missing")
        return {
            "controls_ready": controls_ready,
            "development_plan_ready": plan_ready,
            "development_plan_schema_version": (
                development_plan.get("schema_version")
                if isinstance(development_plan, Mapping)
                else None
            ),
            "development_ready": False,
            "method_ids": method_ids,
            "status": None,
            "stage": None,
        }
    gate = development.get("promotion_gate")
    freeze_digest = (observed.get("llm_freeze") or {}).get("sha256")
    development_plan_digest = (observed.get("llm_development_plan") or {}).get("sha256")
    ready = bool(
        controls_ready
        and plan_ready
        and development.get("schema_version") == contract.get("required_schema_version")
        and development.get("stage") == contract.get("required_stage")
        and development.get("status") == contract.get("required_status")
        and development.get(str(contract.get("required_ready_flag"))) is True
        and development.get("benchmark_claim_allowed") is False
        and development.get("bench_results_present") is False
        and development.get("reference_search_results_used") is False
        and development.get("private_reasoning_retained") is False
        and isinstance(gate, Mapping)
        and gate.get("passed") is contract.get("promotion_gate_passed")
        and gate.get("llm_freeze_sha256") == freeze_digest
        and gate.get("development_plan_sha256") == development_plan_digest
        and development.get("development_plan_sha256") == development_plan_digest
    )
    if not ready:
        blockers.append("llm:development_matrix:not_ready")
    return {
        "controls_ready": controls_ready,
        "development_plan_ready": plan_ready,
        "development_plan_schema_version": (
            development_plan.get("schema_version")
            if isinstance(development_plan, Mapping)
            else None
        ),
        "development_ready": ready,
        "method_ids": method_ids,
        "status": development.get("status"),
        "stage": development.get("stage"),
        "promotion_passed": gate.get("passed") if isinstance(gate, Mapping) else False,
    }


def _audit_selection(
    selection: Mapping[str, Any] | None,
    *,
    plan: Mapping[str, Any],
    statistics: Mapping[str, Any],
    observed: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    scope = plan.get("method_scope")
    expected_families = scope.get("development_families") if isinstance(scope, Mapping) else None
    expected_families = expected_families if isinstance(expected_families, Mapping) else {}
    if selection is None:
        blockers.append("selection:dev_family_champions_missing")
        return {
            "ready": False,
            "selected_champions": {},
            "required_families": sorted(expected_families),
        }
    champions = selection.get("champions")
    champions = champions if isinstance(champions, Mapping) else {}
    selection_contract = statistics.get("family_champion_selection")
    evidence = selection.get("evidence_bindings")
    evidence = evidence if isinstance(evidence, Mapping) else {}
    ready = bool(
        selection.get("schema_version") == "chemworld-method-selection-0.4"
        and selection.get("status") == "dev_selected_bench_unseen"
        and selection.get("formal_results_present") is False
        and selection.get("benchmark_claim_allowed") is False
        and selection.get("bench_information_used") is False
        and selection.get("selection_contract") == selection_contract
        and set(champions) == set(expected_families)
        and all(
            isinstance(champions.get(family), str) and champions[family] in candidates
            for family, candidates in expected_families.items()
            if isinstance(candidates, Sequence) and not isinstance(candidates, str)
        )
        and all(
            _is_sha256(value) and value in {item.get("sha256") for item in observed.values()}
            for value in evidence.values()
        )
    )
    if not ready:
        blockers.append("selection:dev_family_champions_invalid")
    return {
        "ready": ready,
        "selected_champions": dict(champions),
        "required_families": sorted(expected_families),
    }


def _audit_reference_independence(
    *,
    reference_plan: Mapping[str, Any],
    builder_freeze: Mapping[str, Any] | None,
    contract: Any,
    method_ids: tuple[str, ...],
    root: Path,
    blockers: list[str],
) -> dict[str, Any]:
    contract = contract if isinstance(contract, Mapping) else {}
    builder = reference_plan.get("builder_contract")
    builder = builder if isinstance(builder, Mapping) else {}
    plan_ready = bool(
        builder.get("builder_id") == contract.get("builder_id")
        and builder.get("implementation_namespace") == contract.get("implementation_namespace")
        and set(builder.get("evaluated_method_ids", ())) == set(method_ids)
        and builder.get("builder_identity_must_not_equal_evaluated_method") is True
        and builder.get("builder_code_digest_must_not_equal_evaluated_adapter_digest") is True
        and builder.get("training_search_and_evaluation_rng_streams_disjoint") is True
        and builder.get("hidden_state_access") is False
        and contract.get("evaluated_method_identity_overlap_allowed") is False
        and contract.get("evaluated_adapter_code_digest_overlap_allowed") is False
        and contract.get("training_search_evaluation_rng_overlap_allowed") is False
        and contract.get("hidden_state_access_allowed") is False
    )
    if not plan_ready:
        blockers.append("reference:independence_plan_invalid")
    if builder_freeze is None:
        blockers.append("reference:builder_implementation_freeze_missing")
        return {
            "plan_contract_ready": plan_ready,
            "builder_implementation_ready": False,
            "ready": False,
        }
    source_bindings = builder_freeze.get("source_bindings")
    source_bindings = source_bindings if isinstance(source_bindings, Mapping) else {}
    adapter_bindings = builder_freeze.get("evaluated_adapter_bindings")
    adapter_bindings = adapter_bindings if isinstance(adapter_bindings, Mapping) else {}
    source_ready = bool(source_bindings)
    adapter_digests = set(builder_freeze.get("evaluated_adapter_digests", ()))
    builder_digest = builder_freeze.get("builder_code_sha256")
    for relative, expected in source_bindings.items():
        path = _safe_repo_path(root, relative)
        source_ready = bool(
            source_ready
            and path is not None
            and not path.is_symlink()
            and path.is_file()
            and _is_sha256(expected)
            and artifact_file_sha256(path) == expected
        )
    adapter_bindings_ready = set(adapter_bindings) == set(method_ids)
    for method_id, raw_binding in adapter_bindings.items():
        if not isinstance(raw_binding, Mapping):
            adapter_bindings_ready = False
            continue
        path = _safe_repo_path(root, raw_binding.get("path"))
        try:
            payload = (
                json.loads(path.read_text(encoding="utf-8"))
                if path is not None and path.is_file() and not path.is_symlink()
                else None
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            payload = None
        methods = payload.get("methods") if isinstance(payload, Mapping) else None
        method_payload = methods.get(method_id) if isinstance(methods, Mapping) else None
        adapter_bindings_ready = bool(
            adapter_bindings_ready
            and isinstance(method_payload, Mapping)
            and _is_sha256(raw_binding.get("sha256"))
            and _canonical_sha256(method_payload) == raw_binding.get("sha256")
        )
    implementation_ready = bool(
        builder_freeze.get("schema_version") == "chemworld-reference-builder-freeze-0.4"
        and builder_freeze.get("status") == "code_frozen_bench_unseen"
        and builder_freeze.get("builder_id") == builder.get("builder_id")
        and builder_freeze.get("implementation_namespace")
        == builder.get("implementation_namespace")
        and builder_freeze.get("bench_results_used") is False
        and builder_freeze.get("evaluated_method_code_imported") is False
        and builder_freeze.get("hidden_state_access") is False
        and builder_freeze.get("rng_streams_disjoint") is True
        and _is_sha256(builder_digest)
        and builder_digest not in adapter_digests
        and len(adapter_digests) == len(method_ids)
        and adapter_digests
        == {
            binding.get("sha256")
            for binding in adapter_bindings.values()
            if isinstance(binding, Mapping)
        }
        and adapter_bindings_ready
        and source_ready
    )
    if not implementation_ready:
        blockers.append("reference:builder_implementation_freeze_invalid")
    return {
        "plan_contract_ready": plan_ready,
        "builder_implementation_ready": implementation_ready,
        "ready": plan_ready and implementation_ready,
    }


def _audit_execution_budget(
    budget: Mapping[str, Any] | None,
    *,
    selection: Mapping[str, Any] | None,
    formal_tasks: tuple[str, ...],
    blockers: list[str],
) -> dict[str, Any]:
    if budget is None:
        blockers.append("formal_budget:freeze_missing")
        return {"ready": False}
    run_counts = budget.get("run_counts")
    resources = budget.get("resource_limits")
    run_counts = run_counts if isinstance(run_counts, Mapping) else {}
    resources = resources if isinstance(resources, Mapping) else {}
    ready = bool(
        selection is not None
        and budget.get("schema_version") == "chemworld-formal-execution-budget-0.4"
        and budget.get("status") == "frozen_before_bench"
        and budget.get("formal_results_present") is False
        and budget.get("benchmark_claim_allowed") is False
        and tuple(budget.get("formal_core_tasks", ())) == formal_tasks
        and isinstance(run_counts.get("base_matrix_cell_count"), int)
        and run_counts.get("base_matrix_cell_count", 0) > 0
        and isinstance(run_counts.get("complete_experiment_count"), int)
        and run_counts.get("complete_experiment_count", 0) > 0
        and all(
            _is_nonnegative_number(resources.get(field))
            for field in (
                "api_cost_hard_limit_usd",
                "cpu_hour_hard_limit",
                "gpu_hour_hard_limit",
                "disk_byte_hard_limit",
            )
        )
        and _is_sha256(budget.get("method_selection_sha256"))
        and budget.get("method_selection_sha256") == _canonical_sha256(selection)
    )
    if not ready:
        blockers.append("formal_budget:freeze_invalid")
    return {
        "ready": ready,
        "run_counts": dict(run_counts),
        "resource_limits": dict(resources),
    }


def _method_scope_ready(
    raw: Any,
    *,
    interaction: Mapping[str, Any],
    statistics: Mapping[str, Any],
) -> bool:
    if not isinstance(raw, Mapping):
        return False
    methods = interaction.get("methods")
    tracks = interaction.get("tracks")
    selection = statistics.get("family_champion_selection")
    if not all(isinstance(item, Mapping) for item in (methods, tracks, selection)):
        return False
    if not isinstance(methods, Mapping) or not isinstance(selection, Mapping):
        return False
    return bool(
        set(raw.get("all_declared_method_ids", ())) == set(methods)
        and raw.get("development_families") == selection.get("families")
        and set(raw.get("mandatory_comparators", ())) == {"random", "operation_random"}
        and set(raw.get("required_operation_baselines", ()))
        == {"operation_random", "observation_blind", "rule_based"}
    )


def _issuance_contract_ready(raw: Any) -> bool:
    return bool(
        isinstance(raw, Mapping)
        and raw.get("this_audit_may_issue_bench_manifest") is False
        and raw.get("preflight_required_after_method_freeze") is True
        and raw.get("force_override_available") is False
        and raw.get("bench_must_remain_sealed_while_incomplete") is True
    )


def _safe_repo_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    relative = Path(raw)
    if relative.is_absolute():
        return None
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        dict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def artifact_file_sha256(path: Path) -> str:
    """Hash artifacts after the only Git transport normalization we allow.

    Bound JSON evidence is committed as LF by ``.gitattributes``.  Windows
    generators can still leave CRLF in an existing worktree before Git writes
    the LF blob, so hashing raw worktree bytes made identical commits pass in
    one worktree and fail in a clean checkout.  JSON bindings normalize CRLF to
    LF; binary and source artifacts retain exact-byte hashing.
    """

    payload = path.read_bytes()
    if path.suffix.lower() == ".json":
        payload = payload.replace(b"\r\n", b"\n")
    return hashlib.sha256(payload).hexdigest()


def _is_sha256(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_nonnegative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _is_git_commit(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def _text_tuple(raw: Any) -> tuple[str, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        return ()
    if not all(isinstance(item, str) and item for item in raw):
        return ()
    return tuple(raw)


def _probe_repository(root: Path) -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "clean": False}
    return {"commit": commit, "clean": not status.strip()}


__all__ = [
    "DEFAULT_METHOD_FREEZE_PLAN_PATH",
    "METHOD_FREEZE_PLAN_VERSION",
    "METHOD_FREEZE_REPORT_VERSION",
    "MethodFreezeAuditError",
    "artifact_file_sha256",
    "audit_method_freeze",
    "load_method_freeze_plan",
]
