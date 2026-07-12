"""Bind shared-lite elimination to current tasks, routes, and evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_maturity_truth_vnext import (  # noqa: E402
    build_report as build_maturity_report,
)
from scripts.audit_maturity_truth_vnext import (  # noqa: E402
    load_protocol as load_maturity_protocol,
)

from chemworld.physchem.maturity import MaturityLevel  # noqa: E402
from chemworld.runtime.model_reachability import (  # noqa: E402
    ModelReachabilityRegistry,
    default_model_reachability_registry,
)
from chemworld.runtime.profiles import TaskRuntimeProfile  # noqa: E402
from chemworld.tasks import TaskSpec, list_tasks  # noqa: E402
from chemworld.world.operations import INSTRUMENTS, OPERATION_TYPES  # noqa: E402

DEFAULT_PROTOCOL = ROOT / "configs/foundation/lite_elimination_integration_vnext.json"
DEFAULT_MANIFEST = (
    ROOT / "configs/foundation/lite_elimination_before_after_vnext.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/world_foundation/reports/lite-elimination-integration-vnext.json"
)
PROTOCOL_SCHEMA_VERSION = "chemworld-foundation-lite-elimination-protocol-0.1"
MANIFEST_SCHEMA_VERSION = (
    "chemworld-foundation-lite-elimination-before-after-0.1"
)
REPORT_SCHEMA_VERSION = "chemworld-foundation-lite-elimination-report-0.1"
HISTORICAL_REACHABILITY_REPORT = (
    "workstreams/world_foundation/reports/runtime-reachability-vnext.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = _load_json(path)
    if payload.get("schema_version") != PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported lite-elimination protocol schema")
    task_ids = payload.get("expected_task_ids")
    modules = payload.get("shared_modules")
    if not isinstance(task_ids, list) or len(task_ids) != len(set(task_ids)):
        raise ValueError("expected_task_ids must be a unique list")
    if not isinstance(modules, list) or len(modules) != len(set(modules)):
        raise ValueError("shared_modules must be a unique list")
    if payload.get("benchmark_claim_allowed") is not False:
        raise ValueError("integration audit cannot authorize benchmark claims")
    return payload


def load_before_after_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    payload = _load_json(path)
    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("unsupported before/after manifest schema")
    before = payload.get("before_snapshot")
    after = payload.get("after_acceptance")
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise ValueError("before_snapshot and after_acceptance are required")
    transitions = after.get("provider_transitions")
    if not isinstance(transitions, list) or not transitions:
        raise ValueError("provider_transitions must be a non-empty list")
    before_ids = [str(item.get("before_model_id", "")) for item in transitions]
    if len(before_ids) != len(set(before_ids)):
        raise ValueError("provider transitions must cover each old model exactly once")
    for transition in transitions:
        transition_type = transition.get("transition_type")
        before_id = transition.get("before_model_id")
        after_id = transition.get("after_model_id")
        if transition_type not in {"replaced", "promoted_in_place"}:
            raise ValueError("unsupported provider transition type")
        if transition_type == "promoted_in_place" and before_id != after_id:
            raise ValueError("promoted_in_place transitions must retain the model id")
        if transition_type == "replaced" and before_id == after_id:
            raise ValueError("replaced transitions must change the model id")
    return payload


def _canonical_hash(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(encoded.encode()).hexdigest()


def _git_state(repository_root: Path) -> tuple[str | None, bool | None]:
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
                ["git", "status", "--porcelain", "--untracked-files=all"],
                cwd=repository_root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def _report_hash(report: Mapping[str, Any]) -> str:
    payload = dict(report)
    payload["report_hash"] = None
    return _canonical_hash(payload)


def _historical_before_evidence(
    before: Mapping[str, Any], repository_root: Path
) -> dict[str, Any]:
    commit = str(before["snapshot_report_commit"])
    try:
        raw = subprocess.run(
            ["git", "show", f"{commit}:{HISTORICAL_REACHABILITY_REPORT}"],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        historical = json.loads(raw)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return {
            "available": False,
            "matches_manifest": False,
            "error": type(error).__name__,
        }

    task_paths = historical.get("task_paths", {})
    task_maturity_counts = dict(
        sorted(
            Counter(
                row["declared_maturity"]["lowest_level"]
                for row in task_paths.values()
            ).items()
        )
    )
    proxy_false_count = sum(
        row["declared_maturity"]["proxy_allowed"] is False
        for row in task_paths.values()
    )
    shared_modules = set(before["shared_module_task_counts"])
    module_counts = dict.fromkeys(shared_modules, 0)
    for row in task_paths.values():
        present = {
            module["module_id"]
            for module in row["declared_maturity"]["modules"]
            if module["module_id"] in shared_modules
        }
        for module_id in present:
            module_counts[module_id] += 1
    observed = {
        "runtime_source_commit": historical.get("source_commit"),
        "task_count": historical.get("task_count"),
        "operation_count": historical.get("operation_count"),
        "provider_count": historical.get("provider_count"),
        "task_maturity_counts": task_maturity_counts,
        "proxy_allowed_false_task_count": proxy_false_count,
        "shared_module_task_counts": dict(sorted(module_counts.items())),
        "shared_lite_runtime_providers": historical.get("lite_upgrade_targets"),
    }
    expected = {
        key: before[key]
        for key in (
            "runtime_source_commit",
            "task_count",
            "operation_count",
            "provider_count",
            "task_maturity_counts",
            "proxy_allowed_false_task_count",
            "shared_module_task_counts",
            "shared_lite_runtime_providers",
        )
    }
    return {
        "available": True,
        "matches_manifest": observed == expected,
        "snapshot_report_commit": commit,
        "historical_report_path": HISTORICAL_REACHABILITY_REPORT,
        "historical_report_hash": historical.get("report_hash"),
        "observed": observed,
    }


def _flatten_grouped_ids(groups: Mapping[str, Sequence[str]]) -> set[str]:
    return {str(model_id) for values in groups.values() for model_id in values}


def _task_maturity_counts(tasks: Sequence[TaskSpec]) -> dict[str, int]:
    return dict(
        sorted(Counter(task.kernel_maturity.lowest_level.value for task in tasks).items())
    )


def _shared_module_task_counts(
    tasks: Sequence[TaskSpec], shared_modules: set[str]
) -> dict[str, int]:
    counts = dict.fromkeys(shared_modules, 0)
    for task in tasks:
        present = {
            module.module_id
            for module in task.kernel_maturity.modules
            if module.module_id in shared_modules
        }
        for module_id in present:
            counts[module_id] += 1
    return dict(sorted(counts.items()))


def build_report(
    protocol: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    *,
    repository_root: Path = ROOT,
    tasks: Sequence[TaskSpec] | None = None,
    registry: ModelReachabilityRegistry | None = None,
    maturity_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    protocol = load_protocol() if protocol is None else protocol
    manifest = load_before_after_manifest() if manifest is None else manifest
    tasks = tuple(sorted(list_tasks() if tasks is None else tasks, key=lambda x: x.task_id))
    registry = default_model_reachability_registry() if registry is None else registry
    if maturity_report is None:
        maturity_report = build_maturity_report(
            load_maturity_protocol(), repository_root=repository_root
        )

    providers = registry.providers.to_dict()
    shared_modules = set(protocol["shared_modules"])
    before = manifest["before_snapshot"]
    acceptance = manifest["after_acceptance"]
    old_ids = _flatten_grouped_ids(before["shared_lite_runtime_providers"])
    transitions = acceptance["provider_transitions"]
    retired_ids = {
        item["before_model_id"]
        for item in transitions
        if item["transition_type"] == "replaced"
    }
    promoted_in_place_ids = {
        item["before_model_id"]
        for item in transitions
        if item["transition_type"] == "promoted_in_place"
    }
    required_after_ids = _flatten_grouped_ids(acceptance["required_runtime_models"])
    historical_before_evidence = _historical_before_evidence(
        before, repository_root
    )
    all_route_ids = {
        model_id
        for route in registry.routes
        for model_id in route.reachable_model_ids(frozenset(INSTRUMENTS))
    }

    operation_matrix: dict[str, Any] = {}
    for route in sorted(registry.routes, key=lambda item: item.operation_type):
        model_ids = sorted(route.reachable_model_ids(frozenset(INSTRUMENTS)))
        operation_matrix[route.operation_type] = {
            **route.to_dict(),
            "all_model_ids": model_ids,
            "shared_model_ids": [
                model_id
                for model_id in model_ids
                if providers[model_id]["module_id"] in shared_modules
            ],
        }

    task_matrix: dict[str, Any] = {}
    task_assessments = maturity_report["task_assessments"]
    for task in tasks:
        profile = TaskRuntimeProfile.from_task(task)
        declared_ids = sorted(
            model_id
            for module in task.kernel_maturity.modules
            for model_id in module.model_ids
        )
        reachable_ids = sorted(registry.reachable_model_ids(profile))
        shared_claims = [
            module.to_dict()
            for module in task.kernel_maturity.modules
            if module.module_id in shared_modules
        ]
        shared_operations = []
        for operation in sorted(profile.allowed_operations):
            route = registry.route_for_operation(operation)
            model_ids = sorted(route.reachable_model_ids(profile.allowed_instruments))
            shared_ids = [
                model_id
                for model_id in model_ids
                if providers[model_id]["module_id"] in shared_modules
            ]
            if shared_ids:
                shared_operations.append(
                    {"operation": operation, "model_ids": shared_ids}
                )
        assessment = task_assessments[task.task_id]
        task_matrix[task.task_id] = {
            "task_contract_hash": task.contract_hash,
            "declared_maturity": task.kernel_maturity.lowest_level.value,
            "effective_runtime_maturity": assessment[
                "effective_runtime_maturity"
            ],
            "proxy_allowed": task.kernel_maturity.proxy_allowed,
            "declared_model_ids": declared_ids,
            "reachable_model_ids": reachable_ids,
            "declared_but_unreachable": sorted(set(declared_ids) - set(reachable_ids)),
            "reachable_but_undeclared": sorted(set(reachable_ids) - set(declared_ids)),
            "shared_module_claims": shared_claims,
            "shared_operation_routes": shared_operations,
        }

    evidence_matrix: dict[str, Any] = {}
    provider_assessments = maturity_report["provider_assessments"]
    for model_id in sorted(required_after_ids):
        provider = providers.get(model_id)
        assessment = provider_assessments.get(model_id)
        evidence_matrix[model_id] = {
            "module_id": None if provider is None else provider["module_id"],
            "maturity": None if provider is None else provider["maturity"],
            "role": None if provider is None else provider["role"],
            "runtime_reachable": bool(provider and provider["runtime_reachable"]),
            "routed": model_id in all_route_ids,
            "card_present": bool(assessment and assessment["card_present"]),
            "claim_verified": bool(assessment and assessment["claim_verified"]),
            "executed_in_runtime_evidence": bool(
                assessment and assessment["executed_in_runtime_evidence"]
            ),
            "effective_maturity": (
                None if assessment is None else assessment["effective_maturity"]
            ),
            "provenance": [] if provider is None else provider["provenance"],
            "task_ids": sorted(
                task_id
                for task_id, row in task_matrix.items()
                if model_id in row["reachable_model_ids"]
            ),
        }

    current_task_counts = _task_maturity_counts(tasks)
    current_module_counts = _shared_module_task_counts(tasks, shared_modules)
    current_shared_runtime = {
        model_id: payload
        for model_id, payload in providers.items()
        if payload["runtime_reachable"] and payload["module_id"] in shared_modules
    }
    minimum = MaturityLevel(protocol["minimum_task_maturity"])
    forbidden_levels = set(protocol["forbidden_formal_maturities"])
    expected_task_ids = list(protocol["expected_task_ids"])
    evidence_complete = all(
        row["runtime_reachable"]
        and row["routed"]
        and row["card_present"]
        and row["claim_verified"]
        and row["executed_in_runtime_evidence"]
        and MaturityLevel(row["effective_maturity"]).rank >= minimum.rank
        for row in evidence_matrix.values()
    )
    checks = {
        "manifest_boundary_nonclaiming": manifest["claim_boundary"]
        == {
            "changes_maturity_labels": False,
            "overwrites_historical_reports": False,
            "authorizes_benchmark_claims": False,
        },
        "before_snapshot_records_six_shared_lite_providers": len(old_ids) == 6,
        "historical_before_snapshot_matches_manifest": historical_before_evidence[
            "available"
        ]
        and historical_before_evidence["matches_manifest"],
        "shared_module_sets_exact": set(before["shared_lite_runtime_providers"])
        == shared_modules
        == set(acceptance["required_runtime_models"]),
        "provider_transition_coverage_exact": {
            item["before_model_id"]
            for item in acceptance["provider_transitions"]
        }
        == old_ids,
        "provider_transition_targets_match_after_contract": {
            item["after_model_id"] for item in acceptance["provider_transitions"]
        }
        == required_after_ids,
        "task_set_exact": list(task_matrix) == expected_task_ids,
        "task_count_exact": len(task_matrix) == protocol["expected_task_count"],
        "operation_count_exact": len(operation_matrix)
        == protocol["expected_operation_count"]
        == len(OPERATION_TYPES),
        "task_maturity_counts_match_after_contract": current_task_counts
        == acceptance["task_maturity_counts"],
        "all_tasks_meet_minimum_maturity": all(
            MaturityLevel(row["effective_runtime_maturity"]).rank >= minimum.rank
            for row in task_matrix.values()
        ),
        "all_tasks_disallow_proxy": all(
            row["proxy_allowed"] is False for row in task_matrix.values()
        ),
        "proxy_count_matches_after_contract": sum(
            row["proxy_allowed"] is False for row in task_matrix.values()
        )
        == acceptance["proxy_allowed_false_task_count"],
        "task_declarations_match_runtime_routes": all(
            not row["declared_but_unreachable"]
            and not row["reachable_but_undeclared"]
            for row in task_matrix.values()
        ),
        "shared_module_task_counts_match_before_and_after": current_module_counts
        == before["shared_module_task_counts"]
        == acceptance["shared_module_task_counts"],
        "replaced_lite_models_absent_from_registry_and_routes": not (
            retired_ids & set(providers) | retired_ids & all_route_ids
        ),
        "in_place_models_are_promoted_and_evidence_bound": all(
            model_id in current_shared_runtime
            and current_shared_runtime[model_id]["maturity"] not in forbidden_levels
            and evidence_matrix[model_id]["claim_verified"]
            and evidence_matrix[model_id]["executed_in_runtime_evidence"]
            for model_id in promoted_in_place_ids
        ),
        "required_after_models_exact": set(current_shared_runtime)
        == required_after_ids,
        "no_shared_formal_provider_is_proxy_or_lite": not any(
            payload["maturity"] in forbidden_levels
            for payload in current_shared_runtime.values()
        ),
        "shared_runtime_evidence_complete": evidence_complete,
        "maturity_truth_gate_passed": maturity_report["release_allowed"] is True
        and maturity_report["finding_count"] == 0,
    }
    source_commit, source_tree_dirty = _git_state(repository_root)
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_hash(protocol),
        "before_after_manifest_id": manifest["manifest_id"],
        "before_after_manifest_sha256": _canonical_hash(manifest),
        "source_commit": source_commit,
        "source_tree_dirty": source_tree_dirty,
        "status": "lite_elimination_verified" if all(checks.values()) else "failed",
        "integration_verified": all(checks.values()),
        "benchmark_claim_allowed": False,
        "checks": checks,
        "before_snapshot": before,
        "historical_before_evidence": historical_before_evidence,
        "after_snapshot": {
            "task_count": len(task_matrix),
            "operation_count": len(operation_matrix),
            "provider_count": len(providers),
            "task_maturity_counts": current_task_counts,
            "proxy_allowed_false_task_count": sum(
                row["proxy_allowed"] is False for row in task_matrix.values()
            ),
            "shared_module_task_counts": current_module_counts,
            "shared_runtime_provider_ids": sorted(current_shared_runtime),
            "retired_lite_provider_ids_present": sorted(
                retired_ids & (set(providers) | all_route_ids)
            ),
            "promoted_in_place_provider_ids": sorted(promoted_in_place_ids),
        },
        "provider_transitions": acceptance["provider_transitions"],
        "task_evidence_matrix": task_matrix,
        "shared_provider_evidence_matrix": evidence_matrix,
        "operation_route_matrix": operation_matrix,
        "limitations": [
            (
                "This report verifies the current bounded formal runtime paths; "
                "it does not relabel models."
            ),
            "Reference-validated maturity is limited to each model card's declared domain.",
            (
                "The integration audit does not authorize algorithm, benchmark, "
                "publication, or real-world claims."
            ),
        ],
        "report_hash": None,
    }
    report["report_hash"] = _report_hash(report)
    return report


def validate_report(
    report: Mapping[str, Any],
    protocol: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unsupported report schema")
    if report.get("protocol_sha256") != _canonical_hash(protocol):
        errors.append("protocol hash mismatch")
    if report.get("before_after_manifest_sha256") != _canonical_hash(manifest):
        errors.append("before/after manifest hash mismatch")
    checks = report.get("checks")
    if not isinstance(checks, Mapping) or not checks or not all(checks.values()):
        errors.append("one or more lite-elimination controls failed")
    if report.get("integration_verified") is not True:
        errors.append("integration is not verified")
    if report.get("benchmark_claim_allowed") is not False:
        errors.append("report must remain nonclaiming")
    if set(report.get("task_evidence_matrix", {})) != set(
        protocol["expected_task_ids"]
    ):
        errors.append("task evidence coverage mismatch")
    if set(report.get("operation_route_matrix", {})) != set(OPERATION_TYPES):
        errors.append("operation route coverage mismatch")
    if report.get("report_hash") != _report_hash(report):
        errors.append("report hash mismatch")
    return errors


def write_report(
    output: Path = DEFAULT_OUTPUT,
    protocol_path: Path = DEFAULT_PROTOCOL,
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    protocol = load_protocol(protocol_path)
    manifest = load_before_after_manifest(manifest_path)
    report = build_report(
        protocol,
        manifest,
        repository_root=repository_root,
    )
    errors = validate_report(report, protocol, manifest)
    if errors:
        raise ValueError("lite-elimination integration failed: " + "; ".join(errors))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = write_report(args.output, args.protocol, args.manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
