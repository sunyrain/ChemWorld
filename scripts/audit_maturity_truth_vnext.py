"""Audit maturity claims against cards, manifests, runtime routes, and evidence.

This gate intentionally separates an audit that ran correctly from a repository
that is ready to publish a high maturity claim.  A truthful negative report is a
valid audit result; ``release_allowed`` is the stricter publication decision.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
import re
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelCard,
)
from chemworld.runtime.model_reachability import (
    ModelReachabilityRegistry,
    default_model_reachability_registry,
)
from chemworld.runtime.profiles import TaskRuntimeProfile
from chemworld.tasks import TaskSpec, list_tasks

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/foundation/maturity_truth_vnext.json"
DEFAULT_OUTPUT = ROOT / "workstreams/world_foundation/reports/maturity-truth-vnext.json"
PROTOCOL_SCHEMA_VERSION = "chemworld-foundation-maturity-truth-protocol-0.1"
REPORT_SCHEMA_VERSION = "chemworld-foundation-maturity-truth-report-0.1"
_PATH_PATTERN = re.compile(
    r"(?:(?:tests|src|configs|workstreams|docs)/[A-Za-z0-9_./-]+)"
)
_HIGH_LEVELS = {
    MaturityLevel.REFERENCE_VALIDATED,
    MaturityLevel.PROFESSIONAL_CANDIDATE,
    MaturityLevel.PROFESSIONAL,
}


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported maturity truth protocol schema")
    for key in ("card_factories", "adapter_manifest_factories"):
        values = payload.get(key)
        if not isinstance(values, list) or not values or len(values) != len(set(values)):
            raise ValueError(f"{key} must be a non-empty unique list")
    if payload.get("expected_task_count", 0) <= 0:
        raise ValueError("expected_task_count must be positive")
    return payload


def collect_model_cards(protocol: Mapping[str, Any]) -> dict[str, ModelCard]:
    cards: dict[str, ModelCard] = {}
    for factory_path in protocol["card_factories"]:
        produced = _resolve_symbol(str(factory_path))()
        items = produced if isinstance(produced, tuple) else (produced,)
        for card in items:
            if not isinstance(card, ModelCard):
                raise TypeError(f"{factory_path} returned a non-ModelCard value")
            if card.model_id in cards:
                raise ValueError(f"duplicate model card id {card.model_id!r}")
            cards[card.model_id] = card
    return dict(sorted(cards.items()))


def collect_adapter_manifests(
    protocol: Mapping[str, Any],
) -> dict[str, ModelAdapterManifest]:
    manifests: dict[str, ModelAdapterManifest] = {}
    for factory_path in protocol["adapter_manifest_factories"]:
        manifest = _resolve_symbol(str(factory_path))()
        if not isinstance(manifest, ModelAdapterManifest):
            raise TypeError(f"{factory_path} returned a non-ModelAdapterManifest value")
        model_id = manifest.provider_contract.model_id
        if model_id in manifests:
            raise ValueError(f"duplicate adapter provider id {model_id!r}")
        manifests[model_id] = manifest
    return dict(sorted(manifests.items()))


def assess_model_card(
    card: ModelCard,
    protocol: Mapping[str, Any],
    *,
    repository_root: Path,
    provider: Any | None = None,
) -> dict[str, Any]:
    accepted_statuses = set(protocol["accepted_evidence_statuses"])
    completed = [
        item for item in card.validation_evidence if item.status in accepted_statuses
    ]
    evidence_rows = []
    for evidence in card.validation_evidence:
        paths = _evidence_paths(evidence.command_or_path)
        existing_paths = [path for path in paths if (repository_root / path).is_file()]
        evidence_rows.append(
            {
                **evidence.to_dict(),
                "repository_paths": paths,
                "existing_repository_paths": existing_paths,
                "path_valid": bool(paths) and len(paths) == len(existing_paths),
            }
        )

    reference_policy = protocol["reference_validated_requirements"]
    card_dict = card.to_dict()
    structural = {
        field: bool(card_dict.get(field))
        for field in reference_policy["required_card_fields"]
    }
    completed_rows = [
        row for row in evidence_rows if row["status"] in accepted_statuses
    ]
    numerical = any(
        row["path_valid"] and bool(row["tolerance"]) for row in completed_rows
    )
    evidence_text = _joined_evidence_text(card, completed_rows)
    reference_tokens = protocol["evidence_tokens"]["analytical_or_reference"]
    analytical_or_reference = bool(card.reference_reading) and (
        any(row["reference_backend"] for row in completed_rows)
        or _contains_token(evidence_text, reference_tokens)
    )
    failure_tokens = protocol["evidence_tokens"]["failure_domain"]
    failure_evidence = bool(card.failure_modes) and _contains_token(
        evidence_text, failure_tokens
    )
    reference_checks = {
        "required_card_fields_present": all(structural.values()),
        "completed_evidence_present": bool(completed),
        "numerical_tolerance_and_repository_path": numerical,
        "analytical_literature_or_independent_reference": analytical_or_reference,
        "failure_domain_evidence": failure_evidence,
    }
    reference_verified = all(reference_checks.values())

    professional_policy = protocol["professional_candidate_requirements"]
    provider_text = "" if provider is None else " ".join(
        [
            *provider.diagnostic_fields,
            *provider.provenance,
            *provider.input_fields,
            *provider.output_fields,
            provider.failure_policy,
        ]
    )
    full_text = f"{evidence_text} {provider_text} {' '.join(card.intended_use)}"
    distinct_reference_cases = len(
        {
            row["evidence_id"]
            for row in completed_rows
            if row["path_valid"] and row["tolerance"]
        }
    )
    professional_checks = {
        "reference_validated_checks": reference_verified,
        "runtime_diagnostics": bool(provider and provider.diagnostic_fields),
        "coupling_evidence": _contains_token(
            full_text, protocol["evidence_tokens"]["coupling"]
        ),
        "conservation_evidence": _contains_token(
            full_text, protocol["evidence_tokens"]["conservation"]
        ),
        "runtime_provenance": bool(provider and provider.provenance),
        "failure_domain_evidence": failure_evidence,
        "cross_reference_cases": distinct_reference_cases
        >= professional_policy["minimum_distinct_reference_cases"],
    }
    professional_verified = all(professional_checks.values())

    declared = card.maturity
    if declared.rank < MaturityLevel.REFERENCE_VALIDATED.rank:
        effective = declared
    elif professional_verified and declared.rank >= MaturityLevel.PROFESSIONAL_CANDIDATE.rank:
        effective = MaturityLevel.PROFESSIONAL_CANDIDATE
    elif reference_verified:
        effective = MaturityLevel.REFERENCE_VALIDATED
    else:
        effective = MaturityLevel.LITE
    return {
        "model_id": card.model_id,
        "module_id": card.module_id,
        "declared_maturity": declared.value,
        "effective_evidence_maturity": effective.value,
        "claim_verified": effective.rank >= declared.rank,
        "reference_validated_checks": reference_checks,
        "professional_candidate_checks": professional_checks,
        "card_fields_present": structural,
        "evidence": evidence_rows,
    }


def build_report(
    protocol: dict[str, Any] | None = None,
    *,
    repository_root: Path = ROOT,
    registry: ModelReachabilityRegistry | None = None,
    tasks: Sequence[TaskSpec] | None = None,
    cards: Mapping[str, ModelCard] | None = None,
    manifests: Mapping[str, ModelAdapterManifest] | None = None,
) -> dict[str, Any]:
    protocol = load_protocol() if protocol is None else copy.deepcopy(protocol)
    registry = default_model_reachability_registry() if registry is None else registry
    tasks = tuple(list_tasks()) if tasks is None else tuple(tasks)
    cards = collect_model_cards(protocol) if cards is None else dict(cards)
    manifests = (
        collect_adapter_manifests(protocol) if manifests is None else dict(manifests)
    )
    providers = {item.model_id: item for item in registry.providers.providers}
    routed_model_ids = {
        model_id
        for route in registry.routes
        for model_id in route.reachable_model_ids(
            frozenset(route.instrument_model_ids)
        )
    }
    runtime_path = repository_root / protocol["runtime_execution_evidence"]
    runtime_evidence = _load_json_if_file(runtime_path)
    executed_model_ids = _executed_model_ids(runtime_evidence)
    findings: list[dict[str, Any]] = []

    card_assessments: dict[str, dict[str, Any]] = {}
    for model_id, card in sorted(cards.items()):
        assessment = assess_model_card(
            card,
            protocol,
            repository_root=repository_root,
            provider=providers.get(model_id),
        )
        card_assessments[model_id] = assessment
        if card.maturity in _HIGH_LEVELS and not assessment["claim_verified"]:
            _add_finding(
                findings,
                "unsupported_model_card_maturity",
                "error",
                "model card maturity exceeds its strict evidence result",
                model_id=model_id,
                declared=card.maturity.value,
                effective=assessment["effective_evidence_maturity"],
            )

    provider_assessments: dict[str, dict[str, Any]] = {}
    expected_manifest_status = protocol["policy"]["runtime_provider_manifest_status"]
    for model_id, provider in sorted(providers.items()):
        provider_card = cards.get(model_id)
        card_assessment = card_assessments.get(model_id)
        manifest = manifests.get(model_id)
        routed = model_id in routed_model_ids
        executed = model_id in executed_model_ids
        same_card_maturity = bool(
            provider_card and provider_card.maturity is provider.maturity
        )
        manifest_contract_matches = bool(
            manifest and manifest.provider_contract.to_dict() == provider.to_dict()
        )
        manifest_state_valid = bool(
            manifest
            and (
                not routed
                or not provider.runtime_reachable
                or manifest.status == expected_manifest_status
            )
        )
        evidence_effective = (
            card_assessment["effective_evidence_maturity"]
            if card_assessment
            else MaturityLevel.LITE.value
        )
        evidence_rank = MaturityLevel.normalize(evidence_effective).rank
        high_claim = provider.maturity in _HIGH_LEVELS
        runtime_use_valid = not high_claim or not provider.runtime_reachable or (
            routed and executed
        )
        claim_verified = (
            not high_claim
            or (
                provider_card is not None
                and same_card_maturity
                and evidence_rank >= provider.maturity.rank
                and runtime_use_valid
                and (manifest is None or (manifest_contract_matches and manifest_state_valid))
            )
        )
        effective = (
            provider.maturity
            if claim_verified or not high_claim
            else MaturityLevel.normalize(
                protocol["policy"]["unverified_high_claim_effective_level"]
            )
        )
        provider_assessments[model_id] = {
            "model_id": model_id,
            "module_id": provider.module_id,
            "role": provider.role.value,
            "declared_maturity": provider.maturity.value,
            "effective_maturity": effective.value,
            "card_present": provider_card is not None,
            "card_maturity_matches": same_card_maturity,
            "manifest_present": manifest is not None,
            "manifest_contract_matches": manifest_contract_matches,
            "manifest_status": None if manifest is None else manifest.status,
            "manifest_state_valid": manifest_state_valid,
            "routed": routed,
            "executed_in_runtime_evidence": executed,
            "claim_verified": claim_verified,
            "provenance": list(provider.provenance),
        }
        if high_claim and provider_card is None:
            _add_finding(
                findings,
                "high_provider_missing_model_card",
                "error",
                "high maturity provider has no same-id model card",
                model_id=model_id,
            )
        if provider_card is not None and not same_card_maturity:
            _add_finding(
                findings,
                "provider_card_maturity_mismatch",
                "error",
                "provider and model card disagree on maturity",
                model_id=model_id,
                provider_maturity=provider.maturity.value,
                card_maturity=provider_card.maturity.value,
            )
        if high_claim and provider.runtime_reachable and not routed:
            _add_finding(
                findings,
                "high_provider_not_routed",
                "error",
                "registered high maturity provider is not reachable from an operation",
                model_id=model_id,
            )
        if high_claim and provider.runtime_reachable and routed and not executed:
            _add_finding(
                findings,
                "high_provider_not_executed",
                "error",
                (
                    "high maturity provider is registered/routed but absent from "
                    "runtime execution evidence"
                ),
                model_id=model_id,
            )
        if manifest is not None and not manifest_contract_matches:
            _add_finding(
                findings,
                "manifest_provider_contract_mismatch",
                "error",
                "adapter manifest and runtime provider contract differ",
                model_id=model_id,
            )
        if manifest is not None and not manifest_state_valid:
            _add_finding(
                findings,
                "manifest_runtime_state_mismatch",
                "error",
                "runtime-reachable provider is backed by a non-integrated manifest",
                model_id=model_id,
                manifest_status=manifest.status,
            )

    task_assessments: dict[str, dict[str, Any]] = {}
    for task in sorted(tasks, key=lambda item: item.task_id):
        profile = TaskRuntimeProfile.from_task(task)
        reachable = sorted(registry.reachable_model_ids(profile))
        declared = sorted(
            model_id
            for module in task.kernel_maturity.modules
            for model_id in module.model_ids
        )
        declared_but_unreachable = sorted(set(declared) - set(reachable))
        reachable_but_undeclared = sorted(set(reachable) - set(declared))
        levels = [
            MaturityLevel.normalize(provider_assessments[model_id]["effective_maturity"])
            for model_id in reachable
        ]
        effective_task_level = (
            min(levels, key=lambda level: level.rank).value
            if levels
            else "not_applicable"
        )
        module_results = []
        for module in task.kernel_maturity.modules:
            model_levels = [
                MaturityLevel.normalize(provider_assessments[model_id]["effective_maturity"])
                for model_id in module.model_ids
                if model_id in provider_assessments and model_id in reachable
            ]
            verified_level = (
                min(model_levels, key=lambda level: level.rank).value
                if model_levels
                else "not_applicable"
            )
            valid = bool(model_levels) and all(
                level.rank >= module.level.rank for level in model_levels
            )
            module_results.append(
                {
                    "module_id": module.module_id,
                    "declared_level": module.level.value,
                    "verified_level": verified_level,
                    "model_ids": list(module.model_ids),
                    "claim_verified": valid,
                }
            )
            if module.model_ids and not valid:
                _add_finding(
                    findings,
                    "task_module_maturity_exceeds_runtime_evidence",
                    "error",
                    "task module maturity is above its reachable providers' verified level",
                    task_id=task.task_id,
                    module_id=module.module_id,
                )
        aligned = not declared_but_unreachable and not reachable_but_undeclared
        if not aligned:
            _add_finding(
                findings,
                "task_runtime_route_mismatch",
                "error",
                "task declarations and reachable runtime model ids differ",
                task_id=task.task_id,
                declared_but_unreachable=declared_but_unreachable,
                reachable_but_undeclared=reachable_but_undeclared,
            )
        task_assessments[task.task_id] = {
            "task_contract_hash": task.contract_hash,
            "runtime_profile_hash": profile.profile_hash,
            "declared_lowest_maturity": task.kernel_maturity.lowest_level.value,
            "effective_runtime_maturity": effective_task_level,
            "reachable_model_ids": reachable,
            "declared_model_ids": declared,
            "declared_but_unreachable": declared_but_unreachable,
            "reachable_but_undeclared": reachable_but_undeclared,
            "module_claims": module_results,
        }

    structural_findings = [item.to_dict() for item in registry.structural_findings()]
    for finding in structural_findings:
        if finding["severity"] == "error":
            _add_finding(
                findings,
                "runtime_registry_integrity",
                "error",
                finding["message"],
                source_check=finding["check_id"],
                model_id=finding.get("model_id"),
                operation_type=finding.get("operation_type"),
            )

    document_path = repository_root / protocol["public_maturity_document"]
    document_text = document_path.read_text(encoding="utf-8") if document_path.is_file() else ""
    compact_document_text = "".join(document_text.split())
    missing_statements = [
        statement
        for statement in protocol["documentation_contract"]["required_statements"]
        if "".join(str(statement).split()) not in compact_document_text
    ]
    if missing_statements:
        _add_finding(
            findings,
            "public_document_contract_mismatch",
            "error",
            "public maturity document is missing protocol-bound statements",
            missing_statements=missing_statements,
        )
    public_claim_assessments: dict[str, dict[str, Any]] = {}
    for binding in protocol["documentation_contract"]["claim_bindings"]:
        claim_id = str(binding["claim_id"])
        claimed_level = MaturityLevel.normalize(str(binding["maturity"]))
        model_ids = [str(value) for value in binding["model_ids"]]
        token_present = (
            "".join(str(binding["document_token"]).split()) in compact_document_text
        )
        unknown_model_ids = sorted(set(model_ids) - set(provider_assessments))
        declared_source_matches = not unknown_model_ids and all(
            MaturityLevel.normalize(
                provider_assessments[model_id]["declared_maturity"]
            ).rank
            >= claimed_level.rank
            for model_id in model_ids
        )
        verified_source_matches = not unknown_model_ids and all(
            MaturityLevel.normalize(
                provider_assessments[model_id]["effective_maturity"]
            ).rank
            >= claimed_level.rank
            for model_id in model_ids
        )
        public_claim_assessments[claim_id] = {
            "document_token": binding["document_token"],
            "document_token_present": token_present,
            "claimed_maturity": claimed_level.value,
            "model_ids": model_ids,
            "unknown_model_ids": unknown_model_ids,
            "declared_source_matches": declared_source_matches,
            "verified_source_matches": verified_source_matches,
        }
        if not token_present or not declared_source_matches:
            _add_finding(
                findings,
                "public_claim_source_mismatch",
                "error",
                "public maturity claim is not aligned with bound provider declarations",
                claim_id=claim_id,
                unknown_model_ids=unknown_model_ids,
            )
        if token_present and declared_source_matches and not verified_source_matches:
            _add_finding(
                findings,
                "public_claim_exceeds_verified_maturity",
                "error",
                "public maturity claim exceeds runtime-backed verified maturity",
                claim_id=claim_id,
                model_ids=model_ids,
            )

    source_commit, source_tree_dirty = _git_state(repository_root)
    error_count = sum(item["severity"] == "error" for item in findings)
    checks = {
        "task_count_exact": len(tasks) == protocol["expected_task_count"],
        "runtime_registry_structurally_valid": not any(
            item["severity"] == "error" for item in structural_findings
        ),
        "task_routes_exact": all(
            not row["declared_but_unreachable"] and not row["reachable_but_undeclared"]
            for row in task_assessments.values()
        ),
        "public_document_contract_present": not missing_statements,
        "public_claims_runtime_verified": all(
            row["document_token_present"]
            and row["declared_source_matches"]
            and row["verified_source_matches"]
            for row in public_claim_assessments.values()
        ),
        "runtime_execution_evidence_available": bool(runtime_evidence),
        "all_high_claims_verified": not error_count,
    }
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _json_hash(protocol),
        "source_commit": source_commit,
        "source_tree_dirty": source_tree_dirty,
        "status": "release_allowed" if all(checks.values()) else "maturity_claims_blocked",
        "audit_integrity_valid": True,
        "release_allowed": all(checks.values()),
        "task_count": len(tasks),
        "provider_count": len(providers),
        "model_card_count": len(cards),
        "adapter_manifest_count": len(manifests),
        "checks": checks,
        "findings": sorted(
            findings,
            key=lambda item: (
                item["check_id"],
                str(item.get("task_id", "")),
                str(item.get("model_id", "")),
            ),
        ),
        "finding_count": len(findings),
        "error_count": error_count,
        "card_assessments": card_assessments,
        "provider_assessments": provider_assessments,
        "task_assessments": task_assessments,
        "adapter_manifests": {
            model_id: manifest.to_dict() for model_id, manifest in sorted(manifests.items())
        },
        "runtime_execution_evidence": {
            "path": protocol["runtime_execution_evidence"],
            "sha256": _file_hash(runtime_path),
            "executed_model_ids": sorted(executed_model_ids),
        },
        "public_document": {
            "path": protocol["public_maturity_document"],
            "sha256": _file_hash(document_path),
            "missing_required_statements": missing_statements,
            "claim_assessments": public_claim_assessments,
        },
        "runtime_structural_findings": structural_findings,
        "limitations": [
            "A registered or statically routed provider is not treated as executed.",
            "A truthful blocked report does not silently rewrite model or task maturity labels.",
            "Professional is not awarded by this candidate-stage protocol.",
        ],
        "report_hash": None,
    }
    report["report_hash"] = _report_hash(report)
    return report


def validate_report(
    report: Mapping[str, Any],
    protocol: Mapping[str, Any] | None = None,
    *,
    repository_root: Path = ROOT,
) -> list[str]:
    protocol = load_protocol() if protocol is None else protocol
    errors: list[str] = []
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unsupported report schema")
    if report.get("protocol_sha256") != _json_hash(protocol):
        errors.append("protocol hash mismatch")
    if report.get("task_count") != protocol["expected_task_count"]:
        errors.append("task count mismatch")
    task_assessments = report.get("task_assessments")
    expected_task_ids = {task.task_id for task in list_tasks()}
    if not isinstance(task_assessments, dict) or set(task_assessments) != expected_task_ids:
        errors.append("task coverage mismatch")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks:
        errors.append("checks missing")
    else:
        expected_release = all(bool(value) for value in checks.values())
        if report.get("release_allowed") is not expected_release:
            errors.append("release decision mismatch")
    if report.get("finding_count") != len(report.get("findings", ())):
        errors.append("finding count mismatch")
    expected_errors = sum(
        item.get("severity") == "error"
        for item in report.get("findings", ())
        if isinstance(item, dict)
    )
    if report.get("error_count") != expected_errors:
        errors.append("error count mismatch")
    runtime_path = repository_root / protocol["runtime_execution_evidence"]
    if report.get("runtime_execution_evidence", {}).get("sha256") != _file_hash(
        runtime_path
    ):
        errors.append("runtime execution evidence hash mismatch")
    document_path = repository_root / protocol["public_maturity_document"]
    if report.get("public_document", {}).get("sha256") != _file_hash(document_path):
        errors.append("public document hash mismatch")
    expected_hash = _report_hash({**dict(report), "report_hash": None})
    if report.get("report_hash") != expected_hash:
        errors.append("report hash mismatch")
    return errors


def write_report(
    output: Path = DEFAULT_OUTPUT,
    *,
    protocol_path: Path = DEFAULT_PROTOCOL,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    protocol = load_protocol(protocol_path)
    report = build_report(protocol, repository_root=repository_root)
    errors = validate_report(report, protocol, repository_root=repository_root)
    if errors:
        raise ValueError("invalid maturity truth report: " + "; ".join(errors))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def _resolve_symbol(path: str) -> Any:
    parts = path.split(".")
    for index in range(len(parts) - 1, 0, -1):
        try:
            module = importlib.import_module(".".join(parts[:index]))
        except ModuleNotFoundError:
            continue
        value: Any = module
        for part in parts[index:]:
            value = getattr(value, part)
        return value
    raise ImportError(f"cannot resolve symbol {path!r}")


def _evidence_paths(command_or_path: str | None) -> list[str]:
    if not command_or_path:
        return []
    return sorted(set(_PATH_PATTERN.findall(command_or_path.replace("\\", "/"))))


def _joined_evidence_text(card: ModelCard, rows: Sequence[Mapping[str, Any]]) -> str:
    pieces = [
        *card.equations,
        *card.failure_modes,
        *card.reference_reading,
        *card.intended_use,
    ]
    for row in rows:
        pieces.extend(
            str(row.get(key) or "")
            for key in ("evidence_type", "description", "reference_backend", "tolerance")
        )
    return " ".join(pieces).lower()


def _contains_token(text: str, tokens: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(str(token).lower() in lowered for token in tokens)


def _load_json_if_file(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _executed_model_ids(payload: Mapping[str, Any]) -> set[str]:
    model_ids: set[str] = set()

    def visit(value: Any, key: str = "", *, model_context: bool = False) -> None:
        model_context = model_context or key == "model_ids" or key.endswith("_model_ids")
        if isinstance(value, Mapping):
            for child_key, child in value.items():
                visit(child, str(child_key), model_context=model_context)
        elif isinstance(value, list):
            for child in value:
                visit(child, key, model_context=model_context)
        elif isinstance(value, str) and (
            model_context or key == "model_id" or key.endswith("_model_id")
        ):
            model_ids.add(value)

    visit(payload)
    return model_ids


def _add_finding(
    findings: list[dict[str, Any]],
    check_id: str,
    severity: str,
    message: str,
    **context: Any,
) -> None:
    findings.append(
        {
            "check_id": check_id,
            "severity": severity,
            "message": message,
            **{key: value for key, value in context.items() if value is not None},
        }
    )


def _json_hash(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _report_hash(report: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in report.items() if key != "report_hash"}
    return _json_hash(payload)


def _file_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_state(repository_root: Path) -> tuple[str | None, bool | None]:
    snapshot_commit = os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_COMMIT")
    snapshot_dirty = os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_TREE_DIRTY")
    if snapshot_commit and snapshot_dirty in {"true", "false"}:
        return snapshot_commit, snapshot_dirty == "true"
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repository_root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--require-release", action="store_true")
    args = parser.parse_args()
    report = write_report(args.output, protocol_path=args.protocol)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": report["status"],
                "release_allowed": report["release_allowed"],
                "finding_count": report["finding_count"],
                "report_hash": report["report_hash"],
            },
            sort_keys=True,
        )
    )
    return 1 if args.require_release and not report["release_allowed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
