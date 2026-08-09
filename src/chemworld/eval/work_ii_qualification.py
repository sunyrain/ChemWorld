"""Fail-closed authorization receipt for Work II formal execution."""

from __future__ import annotations

import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256

METHOD_QUALIFICATION_RECEIPT_VERSION = (
    "chemworld-work-ii-method-qualification-receipt-0.1"
)


def qualification_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    )


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
        "blind_evaluator_contract_sha256": canonical_json_sha256(
            manifest.get("blind_evaluator_contract")
        ),
    }
    for field, expected in expected_bindings.items():
        if receipt.get(field) != expected:
            errors.append(f"method qualification receipt has a mismatched {field}")
    if receipt.get("qualification_split") != "development_seed_0":
        errors.append("method qualification receipt uses the wrong development split")
    if receipt.get("qualified_prior_arms") != [
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    ]:
        errors.append("method qualification receipt does not cover the exact three arms")
    if receipt.get("qualified_cell_count") != 3:
        errors.append("method qualification receipt does not cover three development cells")
    if receipt.get("formal_participant_outcome_count_before_authorization") != 0:
        errors.append("formal participant outcomes existed before method authorization")
    attempt_cap = manifest.get("expected_counts", {}).get("provider_attempts_hard_cap")
    if receipt.get("approved_provider_attempt_hard_cap") != attempt_cap:
        errors.append("method qualification receipt has a mismatched provider-attempt cap")
    approved = receipt.get("approved_currency_ceiling_usd")
    if (
        isinstance(approved, bool)
        or not isinstance(approved, int | float)
        or not math.isfinite(float(approved))
        or float(approved) <= 0.0
        or float(approved) != float(currency_ceiling_usd)
    ):
        errors.append("method qualification receipt has a mismatched currency ceiling")
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
    return errors


__all__ = [
    "METHOD_QUALIFICATION_RECEIPT_VERSION",
    "qualification_receipt_sha256",
    "validate_method_qualification_receipt",
]
