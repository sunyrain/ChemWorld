"""Build the foundation runtime reachability and maturity-gap control report."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from chemworld.physchem.maturity import ModelExecutionRole
from chemworld.runtime.domain_service_registry import DomainServiceRegistry
from chemworld.runtime.kernel_registry import OperationKernelRegistry, affected_ledgers
from chemworld.runtime.maturity_audit import build_maturity_audit
from chemworld.runtime.model_reachability import default_model_reachability_registry
from chemworld.runtime.profiles import TaskRuntimeProfile
from chemworld.tasks import list_tasks
from chemworld.world.operations import OPERATION_TYPES

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/foundation/runtime_reachability_vnext.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams/world_foundation/reports/runtime-reachability-vnext.json"
)
REPORT_SCHEMA_VERSION = "chemworld-foundation-runtime-reachability-report-0.1"


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != (
        "chemworld-foundation-runtime-reachability-protocol-0.1"
    ):
        raise ValueError("unsupported runtime reachability protocol schema")
    expected_ids = payload.get("expected_task_ids")
    if not isinstance(expected_ids, list) or len(expected_ids) != len(set(expected_ids)):
        raise ValueError("expected_task_ids must be a unique list")
    return payload


def build_report(
    protocol: dict[str, Any] | None = None,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    protocol = load_protocol() if protocol is None else protocol
    registry = default_model_reachability_registry()
    services = DomainServiceRegistry.default()
    kernels = OperationKernelRegistry.default()
    tasks = tuple(sorted(list_tasks(), key=lambda item: item.task_id))
    task_ids = [task.task_id for task in tasks]
    providers = registry.providers.to_dict()
    maturity_report = build_maturity_audit(repository_root=repository_root)

    operation_paths: dict[str, dict[str, Any]] = {}
    routed_model_ids: set[str] = set()
    for operation in OPERATION_TYPES:
        route = registry.route_for_operation(operation)
        service = services.contract_for_operation(operation)
        kernel = kernels.get(operation)
        all_model_ids = sorted(
            route.reachable_model_ids(
                frozenset(
                    instrument
                    for instrument in route.instrument_model_ids
                )
            )
        )
        routed_model_ids.update(all_model_ids)
        operation_paths[operation] = {
            "operation": operation,
            "service": service.to_dict(),
            "kernel": {
                "kernel_id": kernel.kernel_id,
                "kernel_version": kernel.kernel_version,
                "required_capabilities": sorted(kernel.required_capabilities),
            },
            "base_model_ids": list(route.model_ids),
            "instrument_model_ids": {
                key: list(value)
                for key, value in sorted(route.instrument_model_ids.items())
            },
            "all_model_ids": all_model_ids,
            "model_free_reason": route.model_free_reason,
            "affected_ledgers": list(affected_ledgers(operation)),
        }

    task_paths: dict[str, dict[str, Any]] = {}
    for task in tasks:
        profile = TaskRuntimeProfile.from_task(task)
        declared_model_ids = sorted(
            model_id
            for module in task.kernel_maturity.modules
            for model_id in module.model_ids
        )
        reachable_model_ids = sorted(registry.reachable_model_ids(profile))
        task_operation_paths = []
        for operation in sorted(profile.allowed_operations):
            path = operation_paths[operation]
            task_model_ids = sorted(
                registry.route_for_operation(operation).reachable_model_ids(
                    profile.allowed_instruments
                )
            )
            task_operation_paths.append(
                {
                    "operation": operation,
                    "service_id": path["service"]["service_id"],
                    "kernel_id": path["kernel"]["kernel_id"],
                    "model_ids": task_model_ids,
                    "affected_ledgers": path["affected_ledgers"],
                }
            )
        task_paths[task.task_id] = {
            "task_contract_hash": task.contract_hash,
            "runtime_profile": profile.to_dict(),
            "declared_maturity": task.kernel_maturity.to_dict(),
            "declared_model_ids": declared_model_ids,
            "reachable_model_ids": reachable_model_ids,
            "declared_but_unreachable": sorted(
                set(declared_model_ids) - set(reachable_model_ids)
            ),
            "reachable_but_undeclared": sorted(
                set(reachable_model_ids) - set(declared_model_ids)
            ),
            "operation_paths": task_operation_paths,
        }

    required_fields = set(protocol["required_provider_contract_fields"])
    incomplete_provider_contracts = {
        model_id: sorted(required_fields - set(payload))
        for model_id, payload in providers.items()
        if required_fields - set(payload)
    }
    runtime_providers = {
        model_id: payload
        for model_id, payload in providers.items()
        if payload["runtime_reachable"]
    }
    forbidden_tokens = tuple(protocol["forbidden_runtime_model_id_tokens"])
    forbidden_runtime_models = sorted(
        model_id
        for model_id in runtime_providers
        if any(token in model_id.lower() for token in forbidden_tokens)
    )
    registered_runtime_ids = set(runtime_providers)
    orphan_runtime_providers = sorted(registered_runtime_ids - routed_model_ids)
    reference_routed = sorted(
        model_id
        for model_id in routed_model_ids
        if providers[model_id]["role"] == ModelExecutionRole.REFERENCE.value
    )
    actual_lite_groups: dict[str, list[str]] = {}
    for model_id, payload in runtime_providers.items():
        if payload["maturity"] == "lite":
            actual_lite_groups.setdefault(payload["module_id"], []).append(model_id)
    actual_lite_groups = {
        key: sorted(value) for key, value in sorted(actual_lite_groups.items())
    }
    expected_lite_groups = {
        key: sorted(value)
        for key, value in sorted(protocol["expected_lite_provider_groups"].items())
    }

    dynamic_evidence_path = repository_root / protocol["dynamic_integration_evidence"]
    dynamic_evidence = _dynamic_evidence_summary(dynamic_evidence_path)
    checks = {
        "task_set_exact": task_ids == protocol["expected_task_ids"],
        "task_count_exact": len(tasks) == protocol["expected_task_count"],
        "operation_count_exact": len(operation_paths)
        == protocol["expected_operation_count"],
        "all_operations_routed_once": set(operation_paths) == set(OPERATION_TYPES),
        "service_registry_complete": set(services.operation_map()) == set(OPERATION_TYPES),
        "kernel_registry_complete": all(kernels.has(item) for item in OPERATION_TYPES),
        "structural_contract_integrity": maturity_report["contract_integrity_passed"],
        "declarations_aligned": maturity_report["declaration_alignment_status"]
        == "aligned",
        "provider_contracts_complete": not incomplete_provider_contracts,
        "runtime_providers_routed": not orphan_runtime_providers,
        "reference_providers_not_routed": not reference_routed,
        "forbidden_runtime_models_absent": not forbidden_runtime_models,
        "lite_upgrade_targets_exact": actual_lite_groups == expected_lite_groups,
        "dynamic_integration_evidence_available": dynamic_evidence["available"],
        "dynamic_integration_evidence_passed": dynamic_evidence["passed"],
    }
    source_commit, source_tree_dirty = _git_state(repository_root)
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _json_hash(protocol),
        "source_commit": source_commit,
        "source_tree_dirty": source_tree_dirty,
        "status": (
            "controls_ready_upgrade_targets_found"
            if all(checks.values())
            else "controls_failed"
        ),
        "controls_ready": all(checks.values()),
        "benchmark_claim_allowed": False,
        "task_count": len(tasks),
        "operation_count": len(operation_paths),
        "provider_count": len(providers),
        "checks": checks,
        "operation_paths": operation_paths,
        "task_paths": task_paths,
        "provider_catalog": providers,
        "service_catalog": services.to_dict(),
        "kernel_catalog": kernels.to_dict(),
        "lite_upgrade_targets": actual_lite_groups,
        "incomplete_provider_contracts": incomplete_provider_contracts,
        "orphan_runtime_providers": orphan_runtime_providers,
        "reference_providers_routed": reference_routed,
        "forbidden_runtime_models": forbidden_runtime_models,
        "dynamic_integration_evidence": dynamic_evidence,
        "legacy_constraints": protocol["legacy_constraints"],
        "limitations": [
            "This is a control and reachability audit, not a maturity upgrade.",
            (
                "Static reachability does not replace domain-specific perturbation "
                "and reference validation."
            ),
            (
                "Legacy shared-claim prefix policy is intentionally superseded "
                "by the current claim checker."
            ),
        ],
        "remaining_gates": [
            "upgrade reaction_kinetics, reactors, and spectroscopy_instruments",
            "run state-transition and public-boundary audits",
            "complete domain coupling probes before changing task maturity labels",
        ],
        "report_hash": None,
    }
    report["report_hash"] = _report_hash(report)
    return report


def validate_report(
    report: dict[str, Any],
    protocol: dict[str, Any] | None = None,
) -> list[str]:
    protocol = load_protocol() if protocol is None else protocol
    errors: list[str] = []
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unsupported report schema")
    if report.get("protocol_sha256") != _json_hash(protocol):
        errors.append("protocol hash mismatch")
    if report.get("task_count") != protocol["expected_task_count"]:
        errors.append("task count mismatch")
    if report.get("operation_count") != protocol["expected_operation_count"]:
        errors.append("operation count mismatch")
    if set(report.get("task_paths", {})) != set(protocol["expected_task_ids"]):
        errors.append("task coverage mismatch")
    if set(report.get("operation_paths", {})) != set(OPERATION_TYPES):
        errors.append("operation coverage mismatch")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        errors.append("one or more reachability controls failed")
    if report.get("report_hash") != _report_hash({**report, "report_hash": None}):
        errors.append("report hash mismatch")
    return errors


def write_report(
    output: Path = DEFAULT_OUTPUT,
    protocol_path: Path = DEFAULT_PROTOCOL,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    protocol = load_protocol(protocol_path)
    report = build_report(protocol, repository_root=repository_root)
    errors = validate_report(report, protocol)
    if errors:
        raise ValueError("runtime reachability audit failed: " + "; ".join(errors))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _dynamic_evidence_summary(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"available": False, "passed": False, "path": str(path)}
    payload = json.loads(path.read_text(encoding="utf-8"))
    provider_check = next(
        (
            item
            for item in payload.get("checks", [])
            if item.get("check_id") == "providers_execute_in_transactions"
        ),
        None,
    )
    return {
        "available": True,
        "passed": bool(payload.get("passed") and provider_check and provider_check.get("passed")),
        "path": str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path),
        "schema_version": payload.get("schema_version"),
        "report_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "provider_model_ids": (
            dict(provider_check.get("evidence", {}).get("model_ids", {}))
            if provider_check
            else {}
        ),
    }


def _json_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _report_hash(report: dict[str, Any]) -> str:
    payload = {key: value for key, value in report.items() if key != "report_hash"}
    return _json_hash(payload)


def _git_state(root: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    except (OSError, subprocess.CalledProcessError):
        return None, None
    return commit, dirty


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        report = write_report(args.output, args.protocol)
    except ValueError as error:
        print(json.dumps({"status": "failed", "error": str(error)}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "status": report["status"],
                "output": str(args.output),
                "task_count": report["task_count"],
                "operation_count": report["operation_count"],
                "provider_count": report["provider_count"],
                "lite_upgrade_targets": report["lite_upgrade_targets"],
                "report_hash": report["report_hash"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
