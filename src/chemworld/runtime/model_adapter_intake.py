"""Validate claim-bound model adapter proposals before runtime integration."""

from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.physchem.maturity import (
    ModelAdapterManifest,
    ModelExecutionRole,
)
from chemworld.runtime.model_reachability import (
    AUTHORIZED_SHARED_CLAIM_PREFIXES,
    SHARED_INTEGRATION_PATHS,
    default_model_provider_registry,
)
from chemworld.world.operations import OPERATION_TYPES

ADAPTER_INTAKE_SCHEMA_VERSION = "chemworld-model-adapter-intake-0.1"
INTEGRATION_TARGET_WORLD_LAW = "chemworld-physical-chemistry-vnext"
_IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


@dataclass(frozen=True)
class AdapterIntakeFinding:
    check_id: str
    severity: str
    message: str

    def __post_init__(self) -> None:
        if self.severity not in {"error", "warning"}:
            raise ValueError("adapter intake finding severity must be error or warning")

    def to_dict(self) -> dict[str, str]:
        return {
            "check_id": self.check_id,
            "severity": self.severity,
            "message": self.message,
        }


def _normalize_repo_path(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if (
        not normalized
        or normalized.startswith("/")
        or re.match(r"^[A-Za-z]:/", normalized)
    ):
        raise ValueError(f"path must be repository-relative: {value!r}")
    parts = [part for part in normalized.split("/") if part not in {"", "."}]
    if not parts or ".." in parts:
        raise ValueError(f"path escapes repository root: {value!r}")
    return "/".join(parts)


def _path_contains(parent: str, child: str) -> bool:
    parent_parts = _normalize_repo_path(parent).split("/")
    child_parts = _normalize_repo_path(child).split("/")
    return child_parts[: len(parent_parts)] == parent_parts


def _paths_overlap(left: str, right: str) -> bool:
    return _path_contains(left, right) or _path_contains(right, left)


def _provider_symbol_exists(provider_path: str) -> bool:
    parts = provider_path.split(".")
    for index in range(len(parts), 0, -1):
        try:
            target: Any = importlib.import_module(".".join(parts[:index]))
        except ModuleNotFoundError:
            continue
        for attribute in parts[index:]:
            if not hasattr(target, attribute):
                return False
            target = getattr(target, attribute)
        return True
    return False


def _read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    return payload


def _claim_for_workstream(
    repository_root: Path,
    workstream: str,
) -> tuple[Path, dict[str, Any]] | None:
    active = repository_root / "claims" / "active" / f"{workstream}.json"
    candidates: list[Path] = [active] if active.is_file() else []
    candidates.extend(
        sorted(
            (repository_root / "claims" / "completed").glob(
                f"{workstream}--*.json"
            ),
            reverse=True,
        )
    )
    for path in candidates:
        try:
            payload = _read_json_object(path)
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        if payload.get("task_id") == workstream and payload.get("status") in {
            "active",
            "completed",
        }:
            return path, payload
    return None


def _display_path(path: Path, repository_root: Path) -> str:
    try:
        return path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _append_duplicate_findings(
    records: list[dict[str, Any]],
    manifests: list[ModelAdapterManifest | None],
) -> None:
    checks = (
        ("adapter_id", lambda item: item.adapter_id),
        ("provider_model_id", lambda item: item.provider_contract.model_id),
    )
    for label, getter in checks:
        values: dict[str, list[int]] = {}
        for index, manifest in enumerate(manifests):
            if manifest is not None:
                values.setdefault(getter(manifest), []).append(index)
        for value, indices in values.items():
            if len(indices) > 1:
                for index in indices:
                    records[index]["findings"].append(
                        AdapterIntakeFinding(
                            f"duplicate_{label}",
                            "error",
                            f"{label} {value!r} appears in multiple proposals",
                        )
                    )

    owned_paths: dict[str, list[int]] = {}
    for index, manifest in enumerate(manifests):
        if manifest is None:
            continue
        for owned_path in manifest.owned_paths:
            try:
                normalized = _normalize_repo_path(owned_path)
            except ValueError:
                continue
            owned_paths.setdefault(normalized, []).append(index)
    normalized_paths = sorted(owned_paths)
    for owned_path, indices in owned_paths.items():
        affected = sorted(set(indices))
        if len(affected) < 2:
            continue
        for index in affected:
            records[index]["findings"].append(
                AdapterIntakeFinding(
                    "proposal_owned_path_overlap",
                    "error",
                    f"multiple proposals own the same path: {owned_path!r}",
                )
            )
    for position, left in enumerate(normalized_paths):
        for right in normalized_paths[position + 1 :]:
            if not _paths_overlap(left, right):
                continue
            affected = sorted(set(owned_paths[left] + owned_paths[right]))
            if len(affected) < 2:
                continue
            for index in affected:
                records[index]["findings"].append(
                    AdapterIntakeFinding(
                        "proposal_owned_path_overlap",
                        "error",
                        f"proposal owned paths overlap across manifests: {left!r}, {right!r}",
                    )
                )


def validate_adapter_manifests(
    manifest_paths: list[Path] | tuple[Path, ...],
    *,
    repository_root: Path,
    target_world_law: str = INTEGRATION_TARGET_WORLD_LAW,
) -> dict[str, Any]:
    """Return a deterministic, machine-readable intake report."""

    root = repository_root.resolve()
    paths = sorted({path.resolve() for path in manifest_paths}, key=str)
    registered_providers = {
        provider.model_id: provider
        for provider in default_model_provider_registry().providers
    }
    registered_model_ids = set(registered_providers)
    records: list[dict[str, Any]] = []
    manifests: list[ModelAdapterManifest | None] = []

    for path in paths:
        findings: list[AdapterIntakeFinding] = []
        manifest: ModelAdapterManifest | None = None
        payload: dict[str, Any] = {}
        try:
            payload = _read_json_object(path)
            if not str(payload.get("manifest_hash", "")).strip():
                findings.append(
                    AdapterIntakeFinding(
                        "manifest_hash_required",
                        "error",
                        "proposal must include manifest_hash generated by to_dict()",
                    )
                )
            manifest = ModelAdapterManifest.from_dict(payload)
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            findings.append(
                AdapterIntakeFinding(
                    "manifest_parse",
                    "error",
                    f"cannot parse adapter manifest: {error}",
                )
            )

        record: dict[str, Any] = {
            "path": _display_path(path, root),
            "adapter_id": None,
            "provider_model_id": None,
            "owner_workstream": None,
            "claim_path": None,
            "claim_status": None,
            "manifest_hash": payload.get("manifest_hash"),
            "integration_state": "unresolved",
            "_provider_integrated": False,
            "findings": findings,
        }
        records.append(record)
        manifests.append(manifest)
        if manifest is None:
            continue

        record.update(
            {
                "adapter_id": manifest.adapter_id,
                "provider_model_id": manifest.provider_contract.model_id,
                "owner_workstream": manifest.owner_workstream,
                "manifest_hash": manifest.manifest_hash,
            }
        )
        registered_provider = registered_providers.get(
            manifest.provider_contract.model_id
        )
        provider_integrated = registered_provider == manifest.provider_contract
        record["_provider_integrated"] = provider_integrated
        record["integration_state"] = (
            "integrated" if provider_integrated else "proposal"
        )
        if not _IDENTIFIER_PATTERN.fullmatch(manifest.adapter_id):
            findings.append(
                AdapterIntakeFinding(
                    "adapter_id_format",
                    "error",
                    "adapter_id must use lowercase letters, digits, dot, underscore, or dash",
                )
            )
        if not _IDENTIFIER_PATTERN.fullmatch(manifest.provider_contract.model_id):
            findings.append(
                AdapterIntakeFinding(
                    "provider_model_id_format",
                    "error",
                    "provider model_id must use lowercase letters, digits, dot, "
                    "underscore, or dash",
                )
            )
        if manifest.status != "proposal":
            findings.append(
                AdapterIntakeFinding(
                    "proposal_status",
                    "error",
                    "intake accepts status='proposal'; integration changes status after review",
                )
            )
        if manifest.target_world_law != target_world_law:
            findings.append(
                AdapterIntakeFinding(
                    "target_world_law",
                    "error",
                    f"proposal targets {manifest.target_world_law!r}; "
                    f"expected {target_world_law!r}",
                )
            )
        unknown_operations = sorted(
            set(manifest.integration_operations) - set(OPERATION_TYPES)
        )
        if unknown_operations:
            findings.append(
                AdapterIntakeFinding(
                    "unknown_integration_operation",
                    "error",
                    f"unknown integration operations: {unknown_operations}",
                )
            )
        if manifest.provider_contract.role is ModelExecutionRole.REFERENCE:
            findings.append(
                AdapterIntakeFinding(
                    "reference_provider_integration",
                    "error",
                    "reference-only providers cannot be proposed for runtime integration",
                )
            )
        if not _provider_symbol_exists(manifest.provider_contract.provider_path):
            findings.append(
                AdapterIntakeFinding(
                    "provider_path_resolution",
                    "error",
                    f"provider path does not resolve: {manifest.provider_contract.provider_path}",
                )
            )
        if registered_provider is not None and not provider_integrated:
            findings.append(
                AdapterIntakeFinding(
                    "provider_model_id_conflict",
                    "error",
                    "provider model_id already exists; replacement providers "
                    "require a new model_id",
                )
            )
        elif provider_integrated:
            findings.append(
                AdapterIntakeFinding(
                    "provider_already_integrated",
                    "warning",
                    "registered provider exactly matches this hash-bound proposal",
                )
            )
        if manifest.provider_contract.model_id in manifest.replaces_model_ids:
            findings.append(
                AdapterIntakeFinding(
                    "self_replacement",
                    "error",
                    "provider cannot replace its own model_id",
                )
            )
        if len(manifest.replaces_model_ids) != len(set(manifest.replaces_model_ids)):
            findings.append(
                AdapterIntakeFinding(
                    "duplicate_replacement_model",
                    "error",
                    "replaces_model_ids cannot contain duplicates",
                )
            )

        claim = _claim_for_workstream(root, manifest.owner_workstream)
        if claim is None:
            findings.append(
                AdapterIntakeFinding(
                    "claim_required",
                    "error",
                    f"no active or completed claim for {manifest.owner_workstream!r}",
                )
            )
            claim_paths: tuple[str, ...] = ()
        else:
            claim_path, claim_payload = claim
            record["claim_path"] = _display_path(claim_path, root)
            record["claim_status"] = claim_payload.get("status")
            claim_paths = tuple(str(item) for item in claim_payload.get("owned_paths", ()))

        authorized_shared = manifest.owner_workstream.startswith(
            AUTHORIZED_SHARED_CLAIM_PREFIXES
        )
        for owned_path in manifest.owned_paths:
            try:
                normalized = _normalize_repo_path(owned_path)
            except ValueError as error:
                findings.append(
                    AdapterIntakeFinding("owned_path_format", "error", str(error))
                )
                continue
            if claim_paths and not any(
                _path_contains(claim_path, normalized) for claim_path in claim_paths
            ):
                findings.append(
                    AdapterIntakeFinding(
                        "owned_path_outside_claim",
                        "error",
                        f"manifest path {normalized!r} is outside the recorded claim",
                    )
                )
            shared_matches = [
                shared
                for shared in SHARED_INTEGRATION_PATHS
                if _paths_overlap(normalized, shared)
            ]
            if shared_matches and not authorized_shared:
                findings.append(
                    AdapterIntakeFinding(
                        "shared_path_authority",
                        "error",
                        f"module proposal cannot own shared paths: {shared_matches}",
                    )
                )

    _append_duplicate_findings(records, manifests)
    proposed_model_ids = {
        manifest.provider_contract.model_id
        for manifest in manifests
        if manifest is not None
    }
    known_replacement_ids = registered_model_ids | proposed_model_ids
    for record, manifest in zip(records, manifests, strict=True):
        if manifest is None:
            continue
        unknown_replacements = sorted(
            set(manifest.replaces_model_ids) - known_replacement_ids
        )
        if unknown_replacements and not bool(record["_provider_integrated"]):
            record["findings"].append(
                AdapterIntakeFinding(
                    "unknown_replacement_model",
                    "error",
                    f"replacement model ids are unknown: {unknown_replacements}",
                )
            )

    for record in records:
        finding_objects: list[AdapterIntakeFinding] = record["findings"]
        record["passed"] = not any(
            finding.severity == "error" for finding in finding_objects
        )
        record["findings"] = [finding.to_dict() for finding in finding_objects]
        record.pop("_provider_integrated", None)

    accepted_count = sum(bool(record["passed"]) for record in records)
    return {
        "schema_version": ADAPTER_INTAKE_SCHEMA_VERSION,
        "target_world_law": target_world_law,
        "manifest_count": len(records),
        "accepted_count": accepted_count,
        "rejected_count": len(records) - accepted_count,
        "passed": accepted_count == len(records),
        "manifests": records,
    }


__all__ = [
    "ADAPTER_INTAKE_SCHEMA_VERSION",
    "INTEGRATION_TARGET_WORLD_LAW",
    "AdapterIntakeFinding",
    "validate_adapter_manifests",
]
