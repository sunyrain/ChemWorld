"""Build a read-only World Law vNext integration plan from adapter proposals."""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Any

from chemworld.physchem.maturity import (
    ModelAdapterManifest,
    ModelExecutionRole,
)
from chemworld.runtime.model_adapter_intake import (
    INTEGRATION_TARGET_WORLD_LAW,
    validate_adapter_manifests,
)

VNEXT_STAGING_SCHEMA_VERSION = "chemworld-vnext-staging-plan-0.1"


class AdapterIntegrationClass(StrEnum):
    DIAGNOSTIC_ADDITION = "diagnostic_addition"
    RUNTIME_ADDITION = "runtime_addition"
    RUNTIME_REPLACEMENT = "runtime_replacement"


def classify_adapter(manifest: ModelAdapterManifest) -> AdapterIntegrationClass:
    """Classify a structurally valid proposal without mutating runtime routes."""

    role = manifest.provider_contract.role
    if role is ModelExecutionRole.DIAGNOSTIC:
        return AdapterIntegrationClass.DIAGNOSTIC_ADDITION
    if manifest.replaces_model_ids:
        return AdapterIntegrationClass.RUNTIME_REPLACEMENT
    return AdapterIntegrationClass.RUNTIME_ADDITION


def _read_manifest(path: Path) -> ModelAdapterManifest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("adapter manifest JSON root must be an object")
    return ModelAdapterManifest.from_dict(payload)


def _resolved_manifest_paths(
    manifest_paths: list[Path] | tuple[Path, ...],
) -> list[Path]:
    return sorted({path.resolve() for path in manifest_paths}, key=str)


def _staging_record(
    *,
    manifest: ModelAdapterManifest,
    intake_record: dict[str, Any],
) -> dict[str, Any]:
    integration_class = classify_adapter(manifest)
    claim_status = str(intake_record.get("claim_status") or "missing")
    readiness_blockers: list[dict[str, str]] = []
    planning_errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if claim_status != "completed":
        readiness_blockers.append(
            {
                "check_id": "delivery_claim_incomplete",
                "message": (
                    "adapter proposal passed structural intake but its owner claim "
                    "is not completed"
                ),
            }
        )
    if (
        integration_class is AdapterIntegrationClass.DIAGNOSTIC_ADDITION
        and manifest.replaces_model_ids
    ):
        planning_errors.append(
            {
                "check_id": "diagnostic_replacement_forbidden",
                "message": (
                    "a diagnostic provider cannot replace a runtime model; submit a "
                    "runtime provider with independent evidence"
                ),
            }
        )
    if integration_class is AdapterIntegrationClass.DIAGNOSTIC_ADDITION:
        maturity_effect = "none_on_runtime"
        warnings.append(
            {
                "check_id": "diagnostic_maturity_isolation",
                "message": (
                    "provider maturity applies only to the diagnostic contract and "
                    "must not raise task or runtime-model maturity"
                ),
            }
        )
    elif integration_class is AdapterIntegrationClass.RUNTIME_REPLACEMENT:
        maturity_effect = "candidate_requires_runtime_and_reference_evidence_review"
    else:
        maturity_effect = "candidate_requires_world_law_and_route_review"

    blockers = [*readiness_blockers, *planning_errors]
    integration_ready = not blockers
    return {
        "adapter_id": manifest.adapter_id,
        "source_path": intake_record["path"],
        "manifest_hash": manifest.manifest_hash,
        "owner_workstream": manifest.owner_workstream,
        "claim_path": intake_record.get("claim_path"),
        "claim_status": claim_status,
        "provider_model_id": manifest.provider_contract.model_id,
        "provider_module_id": manifest.provider_contract.module_id,
        "provider_role": manifest.provider_contract.role.value,
        "provider_maturity": manifest.provider_contract.maturity.value,
        "integration_class": integration_class.value,
        "integration_operations": list(manifest.integration_operations),
        "replaces_model_ids": list(manifest.replaces_model_ids),
        "target_world_law": manifest.target_world_law,
        "delivery_complete": claim_status == "completed",
        "integration_ready": integration_ready,
        "runtime_maturity_effect": maturity_effect,
        "runtime_maturity_upgrade_allowed": False,
        "can_remove_replaced_models": False,
        "readiness_blockers": readiness_blockers,
        "planning_errors": planning_errors,
        "blockers": blockers,
        "warnings": warnings,
    }


def build_vnext_integration_plan(
    manifest_paths: list[Path] | tuple[Path, ...],
    *,
    repository_root: Path,
    target_world_law: str = INTEGRATION_TARGET_WORLD_LAW,
) -> dict[str, Any]:
    """Validate and classify proposals while preserving the frozen v0.3 runtime."""

    paths = _resolved_manifest_paths(manifest_paths)
    intake = validate_adapter_manifests(
        paths,
        repository_root=repository_root,
        target_world_law=target_world_law,
    )
    intake_by_path = {
        str(record["path"]): record for record in intake["manifests"]
    }
    staging_records: list[dict[str, Any]] = []
    rejected_records: list[dict[str, Any]] = []

    for path in paths:
        try:
            display_path = path.relative_to(repository_root.resolve()).as_posix()
        except ValueError:
            display_path = str(path)
        intake_record = intake_by_path[display_path]
        if not intake_record["passed"]:
            rejected_records.append(
                {
                    "source_path": display_path,
                    "adapter_id": intake_record.get("adapter_id"),
                    "provider_model_id": intake_record.get("provider_model_id"),
                    "findings": intake_record["findings"],
                }
            )
            continue
        manifest = _read_manifest(path)
        staging_records.append(
            _staging_record(manifest=manifest, intake_record=intake_record)
        )

    operation_plan: dict[str, list[dict[str, Any]]] = {}
    for record in staging_records:
        for operation in record["integration_operations"]:
            operation_plan.setdefault(operation, []).append(
                {
                    "adapter_id": record["adapter_id"],
                    "provider_model_id": record["provider_model_id"],
                    "provider_role": record["provider_role"],
                    "integration_class": record["integration_class"],
                    "replaces_model_ids": record["replaces_model_ids"],
                    "integration_ready": record["integration_ready"],
                }
            )
    for entries in operation_plan.values():
        entries.sort(key=lambda item: str(item["adapter_id"]))

    integration_ready_count = sum(
        bool(record["integration_ready"]) for record in staging_records
    )
    pending_delivery_count = sum(
        not bool(record["delivery_complete"]) for record in staging_records
    )
    diagnostic_only_count = sum(
        record["integration_class"]
        == AdapterIntegrationClass.DIAGNOSTIC_ADDITION.value
        for record in staging_records
    )
    runtime_addition_count = sum(
        record["integration_class"] == AdapterIntegrationClass.RUNTIME_ADDITION.value
        for record in staging_records
    )
    runtime_replacement_count = sum(
        record["integration_class"]
        == AdapterIntegrationClass.RUNTIME_REPLACEMENT.value
        for record in staging_records
    )
    planning_error_count = sum(
        len(record["planning_errors"]) for record in staging_records
    )
    plan_integrity_passed = bool(intake["passed"] and planning_error_count == 0)
    return {
        "schema_version": VNEXT_STAGING_SCHEMA_VERSION,
        "base_world_law": "chemworld-physical-chemistry-v0.3",
        "target_world_law": target_world_law,
        "v0_3_runtime_changed": False,
        "manifest_count": len(paths),
        "intake_accepted_count": int(intake["accepted_count"]),
        "intake_rejected_count": int(intake["rejected_count"]),
        "staged_count": len(staging_records),
        "integration_ready_count": integration_ready_count,
        "pending_delivery_count": pending_delivery_count,
        "diagnostic_only_count": diagnostic_only_count,
        "runtime_addition_count": runtime_addition_count,
        "runtime_replacement_count": runtime_replacement_count,
        "runtime_maturity_upgrade_count": 0,
        "planning_error_count": planning_error_count,
        "plan_integrity_passed": plan_integrity_passed,
        "passed": plan_integrity_passed,
        "requires_new_world_law": bool(staging_records),
        "proposals": staging_records,
        "rejected_proposals": rejected_records,
        "operation_plan": {
            operation: operation_plan[operation]
            for operation in sorted(operation_plan)
        },
        "integration_policy": {
            "completed_claim_required": True,
            "diagnostic_maturity_propagates_to_runtime": False,
            "staging_can_remove_existing_models": False,
            "runtime_replacement_requires_new_model_id": True,
            "runtime_maturity_changes_require_post_integration_evidence": True,
        },
    }


__all__ = [
    "VNEXT_STAGING_SCHEMA_VERSION",
    "AdapterIntegrationClass",
    "build_vnext_integration_plan",
    "classify_adapter",
]
