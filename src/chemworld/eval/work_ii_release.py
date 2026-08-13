"""Clean-release and final formal-execution authorization contracts for Work II."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
)
from chemworld.eval.work_ii_cost import (
    build_formal_cost_contract,
    validate_formal_cost_contract,
)
from chemworld.eval.work_ii_qualification import (
    qualification_receipt_sha256,
    validate_method_qualification_receipt,
)

CLEAN_RELEASE_RECEIPT_VERSION = "chemworld-work-ii-clean-release-receipt-0.1"
# Keep the clean-release receipt tied to one exact, reviewable Work II test roster.
WORK_II_RELEASE_TEST_FILES = (
    "tests/test_work_ii_ae_formal_cohort.py",
    "tests/test_work_ii_ae_prior_qualification_v02.py",
    "tests/test_work_ii_analysis.py",
    "tests/test_work_ii_blind_evaluator.py",
    "tests/test_work_ii_campaign_runner.py",
    "tests/test_work_ii_catalyst_deactivation_q0.py",
    "tests/test_work_ii_c2_admission.py",
    "tests/test_work_ii_c2_task_admission.py",
    "tests/test_work_ii_confirmatory.py",
    "tests/test_work_ii_constitutive_structural_qualification.py",
    "tests/test_work_ii_cost.py",
    "tests/test_work_ii_development_confirmation.py",
    "tests/test_work_ii_distillation_additional_rollback_q0.py",
    "tests/test_work_ii_crystallization_reversible_q0.py",
    "tests/test_work_ii_formal_design.py",
    "tests/test_work_ii_formal_evaluators.py",
    "tests/test_work_ii_formal_runner.py",
    "tests/test_work_ii_law_summary.py",
    "tests/test_work_ii_partition_constitutive_q0.py",
    "tests/test_work_ii_private.py",
    "tests/test_work_ii_private_execution.py",
    "tests/test_work_ii_process_profile.py",
    "tests/test_work_ii_public_c2.py",
    "tests/test_work_ii_qualification.py",
    "tests/test_work_ii_resource_calibration.py",
    "tests/test_work_ii_release.py",
    "tests/test_work_ii_report.py",
    "tests/test_work_ii_static_topology_q0.py",
    "tests/test_work_ii_truth.py",
)
PREREGISTRATION_FREEZE_RECEIPT_VERSION = (
    "chemworld-work-ii-preregistration-freeze-receipt-0.1"
)

_CLEAN_RELEASE_MATERIAL_PATHS = (
    "configs",
    "pyproject.toml",
    "scripts",
    "src/chemworld",
    "uv.lock",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _relative(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: value for key, value in payload.items() if key != field})


def clean_release_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def preregistration_freeze_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def _material_tree_changed_since(root: Path, tested_commit: str) -> tuple[bool, str | None]:
    """Return material-tree change state and any Git diagnostic."""

    completed = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            tested_commit,
            "HEAD",
            "--",
            *_CLEAN_RELEASE_MATERIAL_PATHS,
        ],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0:
        return False, None
    if completed.returncode == 1:
        return True, None
    diagnostic = str(completed.stderr or "").strip()
    return True, diagnostic or f"git diff exited with status {completed.returncode}"


def validate_clean_release_receipt(
    receipt: Mapping[str, Any],
    *,
    root: Path | None = None,
) -> list[str]:
    """Validate the durable outcome-free receipt emitted by an independent checkout audit."""

    errors: list[str] = []
    if receipt.get("schema_version") != CLEAN_RELEASE_RECEIPT_VERSION:
        errors.append("unexpected Work II clean-release receipt schema")
    if receipt.get("receipt_sha256") != clean_release_receipt_sha256(receipt):
        errors.append("Work II clean-release receipt self-hash mismatch")
    if receipt.get("status") != "passed" or receipt.get("failures") != []:
        errors.append("Work II clean-release receipt has not passed")
    if (
        receipt.get("formal_result") is not False
        or receipt.get("formal_execution_allowed") is not False
        or receipt.get("provider_calls_executed") != 0
        or receipt.get("formal_participant_outcome_count") != 0
    ):
        errors.append("Work II clean-release receipt crossed the execution boundary")
    commit = receipt.get("tested_commit")
    if (
        not isinstance(commit, str)
        or len(commit) != 40
        or any(character not in "0123456789abcdef" for character in commit)
    ):
        errors.append("Work II clean-release receipt lacks a full tested commit")
    elif root is not None:
        root = root.resolve()
        if git_worktree_dirty(root):
            errors.append("current Work II release worktree is dirty")
        current_commit = git_source_commit(root)
        material_changed, material_error = _material_tree_changed_since(root, commit)
        if material_changed:
            errors.append(
                "current Work II implementation differs from the clean-release tested commit"
            )
        if material_error is not None:
            errors.append(f"clean-release material-tree comparison failed: {material_error}")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, current_commit],
            cwd=root,
            capture_output=True,
            check=False,
        )
        if ancestor.returncode == 1:
            errors.append("clean-release tested commit is not an ancestor of current HEAD")
        elif ancestor.returncode != 0:
            diagnostic = str(ancestor.stderr or "").strip()
            errors.append(
                "clean-release commit ancestry check failed: "
                + (diagnostic or f"git merge-base exited with status {ancestor.returncode}")
            )
    checkout = receipt.get("independent_checkout")
    checkout = checkout if isinstance(checkout, Mapping) else {}
    if (
        checkout.get("mode") != "git_clone_no_local"
        or checkout.get("clean_before") is not True
        or checkout.get("clean_after") is not True
        or checkout.get("path_recorded") is not False
    ):
        errors.append("Work II clean-release receipt lacks a clean independent checkout")
    wheel = receipt.get("wheel")
    wheel = wheel if isinstance(wheel, Mapping) else {}
    if (
        wheel.get("status") != "passed"
        or not isinstance(wheel.get("sha256"), str)
        or len(str(wheel.get("sha256"))) != 64
        or not isinstance(wheel.get("bytes"), int)
        or wheel.get("bytes", 0) <= 0
        or wheel.get("installed_import_smoke") is not True
    ):
        errors.append("Work II clean-release receipt lacks a valid clean wheel result")
    tests = receipt.get("work_ii_tests")
    tests = tests if isinstance(tests, Mapping) else {}
    if (
        tests.get("status") != "passed"
        or tests.get("test_files") != list(WORK_II_RELEASE_TEST_FILES)
        or not isinstance(tests.get("passed"), int)
        or isinstance(tests.get("passed"), bool)
        or tests.get("passed", 0) <= 0
        or tests.get("skipped") != 0
        or tests.get("failed") != 0
        or not isinstance(tests.get("stdout_sha256"), str)
        or not isinstance(tests.get("stderr_sha256"), str)
    ):
        errors.append("Work II clean-release receipt lacks the exact release test result")
    return errors


def validate_preregistration_freeze_receipt(
    root: Path,
    receipt: Mapping[str, Any],
    manifest: Mapping[str, Any],
    qualification_receipt: Mapping[str, Any],
    qualification_receipt_path: Path,
    *,
    currency_ceiling_usd: float,
) -> list[str]:
    """Validate the final user-authorized, outcome-blind Work II freeze receipt."""

    errors: list[str] = []
    if receipt.get("schema_version") != PREREGISTRATION_FREEZE_RECEIPT_VERSION:
        errors.append("unexpected Work II preregistration-freeze receipt schema")
    if receipt.get("receipt_sha256") != preregistration_freeze_receipt_sha256(receipt):
        errors.append("Work II preregistration-freeze receipt self-hash mismatch")
    if receipt.get("status") != "passed_final_freeze":
        errors.append("Work II preregistration final freeze has not passed")
    if (
        receipt.get("formal_result") is not False
        or receipt.get("formal_participant_outcome_count") != 0
        or receipt.get("formal_execution_authorized") is not True
    ):
        errors.append("Work II preregistration-freeze receipt crossed its outcome boundary")

    bindings = receipt.get("bindings")
    bindings = bindings if isinstance(bindings, Mapping) else {}
    if bindings.get("formal_preflight_sha256") != manifest.get("preflight_sha256"):
        errors.append("preregistration freeze does not bind the formal manifest")

    clean_path = (
        root
        / "workstreams/flagship_tasks/reports/"
        "work-ii-clean-release-receipt-v0.1.json"
    )
    if not clean_path.is_file():
        errors.append("clean-release receipt is missing")
    else:
        clean = _load_object(clean_path)
        clean_errors = validate_clean_release_receipt(clean, root=root)
        errors.extend(f"clean release: {error}" for error in clean_errors)
        clean_binding = bindings.get("clean_release")
        clean_binding = clean_binding if isinstance(clean_binding, Mapping) else {}
        if (
            clean_binding.get("file_sha256") != file_sha256(clean_path)
            or clean_binding.get("receipt_sha256") != clean.get("receipt_sha256")
            or clean_binding.get("tested_commit") != clean.get("tested_commit")
        ):
            errors.append("preregistration freeze does not bind the clean-release receipt")

    qualification_path = qualification_receipt_path.resolve()
    if not qualification_path.is_file():
        errors.append("method-qualification receipt file is missing")
    else:
        qualification_binding = bindings.get("method_qualification")
        qualification_binding = (
            qualification_binding if isinstance(qualification_binding, Mapping) else {}
        )
        if (
            qualification_binding.get("path")
            != _relative(root, qualification_path)
            or qualification_binding.get("file_sha256") != file_sha256(qualification_path)
            or qualification_binding.get("receipt_sha256")
            != qualification_receipt_sha256(qualification_receipt)
        ):
            errors.append("preregistration freeze does not bind method qualification")
    qualification_ceiling = qualification_receipt.get("approved_currency_ceiling_usd")
    if (
        isinstance(qualification_ceiling, bool)
        or not isinstance(qualification_ceiling, int | float)
        or float(qualification_ceiling) <= 0
    ):
        errors.append("method qualification lacks its distinct positive currency ceiling")
    else:
        qualification_errors = validate_method_qualification_receipt(
            root,
            qualification_receipt,
            manifest,
            currency_ceiling_usd=float(qualification_ceiling),
        )
        errors.extend(f"method qualification: {error}" for error in qualification_errors)

    authorization = receipt.get("user_authorization")
    authorization = authorization if isinstance(authorization, Mapping) else {}
    if (
        authorization.get("authorized_by") != "user"
        or not isinstance(authorization.get("authorized_at"), str)
        or not authorization.get("authorized_at")
        or authorization.get("credential_rotation_confirmed") is not True
        or authorization.get("execution_command_approved") is not True
        or authorization.get("budget_approved") is not True
        or authorization.get("failure_escalation_approved") is not True
        or authorization.get("formal_pricing_contract_approved") is not True
    ):
        errors.append("preregistration freeze lacks complete user authorization")
    if (
        authorization.get("formal_currency_ceiling_usd") != currency_ceiling_usd
        or isinstance(currency_ceiling_usd, bool)
        or not isinstance(currency_ceiling_usd, int | float)
        or float(currency_ceiling_usd) <= 0
    ):
        errors.append("preregistration freeze formal currency ceiling differs from the CLI ceiling")
    if authorization.get("qualification_currency_ceiling_usd") != qualification_ceiling:
        errors.append("preregistration freeze changed the qualification currency ceiling")
    expected_eta = authorization.get("qualified_expected_eta_seconds")
    if not isinstance(expected_eta, (int, float)) or expected_eta <= 0:
        errors.append("preregistration freeze lacks a qualified positive ETA")
    if authorization.get("provider_contract") != manifest.get("provider_contract"):
        errors.append("preregistration freeze provider contract differs from the manifest")

    formal_budget = receipt.get("formal_currency_budget")
    if not isinstance(formal_budget, Mapping):
        errors.append("preregistration freeze lacks a formal currency budget contract")
    else:
        errors.extend(validate_formal_cost_contract(root, manifest, formal_budget))
        if formal_budget.get("formal_currency_ceiling_usd") != float(
            currency_ceiling_usd
        ):
            errors.append("formal currency budget differs from the user-approved ceiling")

    escalation = receipt.get("failure_escalation_contract")
    escalation = escalation if isinstance(escalation, Mapping) else {}
    if any(
        escalation.get(field) is not True
        for field in (
            "missing_infrastructure_only_resume",
            "persisted_scientific_trajectory_never_replaced",
            "halt_on_provider_attempt_cap",
            "result_direction_early_stopping_forbidden",
        )
    ):
        errors.append("preregistration freeze lacks the failure-escalation contract")

    return errors


def build_preregistration_freeze_receipt(
    root: Path,
    manifest: Mapping[str, Any],
    qualification_receipt_path: Path,
    *,
    currency_ceiling_usd: float,
    qualified_expected_eta_seconds: float,
    authorized_at: str,
    pricing_source: str,
    pricing_observed_at: str,
    cache_hit_input_usd_per_million: float,
    cache_miss_input_usd_per_million: float,
    output_usd_per_million: float,
) -> dict[str, Any]:
    """Build the final receipt after every external W2-08/W2-10/W2-11 condition exists."""

    root = root.resolve()
    qualification_path = qualification_receipt_path.resolve()
    clean_path = (
        root
        / "workstreams/flagship_tasks/reports/"
        "work-ii-clean-release-receipt-v0.1.json"
    )
    clean = _load_object(clean_path)
    qualification = _load_object(qualification_path)
    qualification_ceiling = qualification.get("approved_currency_ceiling_usd")
    if (
        isinstance(qualification_ceiling, bool)
        or not isinstance(qualification_ceiling, int | float)
        or float(qualification_ceiling) <= 0
    ):
        raise ValueError("method qualification lacks its distinct positive currency ceiling")
    formal_budget = build_formal_cost_contract(
        root,
        manifest,
        formal_currency_ceiling_usd=float(currency_ceiling_usd),
        pricing_source=pricing_source,
        pricing_observed_at=pricing_observed_at,
        cache_hit_input_usd_per_million=float(cache_hit_input_usd_per_million),
        cache_miss_input_usd_per_million=float(cache_miss_input_usd_per_million),
        output_usd_per_million=float(output_usd_per_million),
    )
    receipt: dict[str, Any] = {
        "schema_version": PREREGISTRATION_FREEZE_RECEIPT_VERSION,
        "status": "passed_final_freeze",
        "formal_result": False,
        "formal_participant_outcome_count": 0,
        "formal_execution_authorized": True,
        "formal_currency_budget": formal_budget,
        "bindings": {
            "formal_preflight_sha256": manifest.get("preflight_sha256"),
            "clean_release": {
                "file_sha256": file_sha256(clean_path),
                "receipt_sha256": clean.get("receipt_sha256"),
                "tested_commit": clean.get("tested_commit"),
            },
            "method_qualification": {
                "path": _relative(root, qualification_path),
                "file_sha256": file_sha256(qualification_path),
                "receipt_sha256": qualification_receipt_sha256(qualification),
            },
        },
        "user_authorization": {
            "authorized_by": "user",
            "authorized_at": authorized_at,
            "credential_rotation_confirmed": True,
            "execution_command_approved": True,
            "budget_approved": True,
            "failure_escalation_approved": True,
            "formal_pricing_contract_approved": True,
            "qualification_currency_ceiling_usd": float(qualification_ceiling),
            "formal_currency_ceiling_usd": float(currency_ceiling_usd),
            "qualified_expected_eta_seconds": float(qualified_expected_eta_seconds),
            "provider_contract": manifest.get("provider_contract"),
        },
        "failure_escalation_contract": {
            "missing_infrastructure_only_resume": True,
            "persisted_scientific_trajectory_never_replaced": True,
            "halt_on_provider_attempt_cap": True,
            "result_direction_early_stopping_forbidden": True,
        },
    }
    receipt["receipt_sha256"] = preregistration_freeze_receipt_sha256(receipt)
    errors = validate_preregistration_freeze_receipt(
        root,
        receipt,
        manifest,
        qualification,
        qualification_path,
        currency_ceiling_usd=float(currency_ceiling_usd),
    )
    if errors:
        raise ValueError("built preregistration freeze receipt is invalid: " + "; ".join(errors))
    return receipt


__all__ = [
    "CLEAN_RELEASE_RECEIPT_VERSION",
    "PREREGISTRATION_FREEZE_RECEIPT_VERSION",
    "WORK_II_RELEASE_TEST_FILES",
    "build_preregistration_freeze_receipt",
    "clean_release_receipt_sha256",
    "preregistration_freeze_receipt_sha256",
    "validate_clean_release_receipt",
    "validate_preregistration_freeze_receipt",
]
