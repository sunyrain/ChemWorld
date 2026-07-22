"""Audit the clean, evidence-bound ChemWorld candidate backend freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

if __package__:
    from scripts.audit_maturity_truth_vnext import (
        build_report as build_maturity_report,
    )
    from scripts.audit_maturity_truth_vnext import (
        load_protocol as load_maturity_protocol,
    )
    from scripts.audit_maturity_truth_vnext import (
        validate_report as validate_maturity_report,
    )
    from scripts.audit_public_boundary_security_vnext import (
        build_report as build_public_boundary_report,
    )
    from scripts.audit_public_boundary_security_vnext import (
        load_protocol as load_public_boundary_protocol,
    )
    from scripts.audit_runtime_reachability_vnext import (
        build_report as build_reachability_report,
    )
    from scripts.audit_runtime_reachability_vnext import (
        load_protocol as load_reachability_protocol,
    )
    from scripts.audit_runtime_reachability_vnext import (
        validate_report as validate_reachability_report,
    )
    from scripts.audit_state_transition_invariants import (
        build_report as build_state_report,
    )
    from scripts.audit_state_transition_invariants import (
        load_protocol as load_state_protocol,
    )
    from scripts.audit_state_transition_invariants import (
        validate_report as validate_state_report,
    )
    from scripts.audit_vnext_runtime_integration import build_audit as build_runtime_audit
    from scripts.evidence_pipeline import _is_materialized_output_path
else:
    from audit_maturity_truth_vnext import (
        build_report as build_maturity_report,
    )
    from audit_maturity_truth_vnext import (
        load_protocol as load_maturity_protocol,
    )
    from audit_maturity_truth_vnext import (
        validate_report as validate_maturity_report,
    )
    from audit_public_boundary_security_vnext import (
        build_report as build_public_boundary_report,
    )
    from audit_public_boundary_security_vnext import (
        load_protocol as load_public_boundary_protocol,
    )
    from audit_runtime_reachability_vnext import (
        build_report as build_reachability_report,
    )
    from audit_runtime_reachability_vnext import (
        load_protocol as load_reachability_protocol,
    )
    from audit_runtime_reachability_vnext import (
        validate_report as validate_reachability_report,
    )
    from audit_state_transition_invariants import (
        build_report as build_state_report,
    )
    from audit_state_transition_invariants import (
        load_protocol as load_state_protocol,
    )
    from audit_state_transition_invariants import (
        validate_report as validate_state_report,
    )
    from audit_vnext_runtime_integration import build_audit as build_runtime_audit
    from evidence_pipeline import _is_materialized_output_path

from chemworld.physchem.maturity import MaturityLevel
from chemworld.tasks import list_tasks
from chemworld.world.operations import OPERATION_TYPES

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs" / "foundation" / "backend_v0.5.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams" / "world_foundation" / "reports" / "backend-v0.5.json"
)
REPORT_SCHEMA_VERSION = "chemworld-foundation-backend-freeze-audit-0.1"


def _json_hash(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _tracked_source_changes() -> list[str]:
    """List tracked non-generated paths that differ from HEAD."""

    changed: list[str] = []
    for line in _git_output("status", "--porcelain", "--untracked-files=no").splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not _is_materialized_output_path(path):
            changed.append(path)
    return changed


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("backend freeze protocol must be an object")
    return payload


def build_report(
    protocol: Mapping[str, Any] | None = None,
    *,
    enforce_clean_tree: bool = True,
) -> dict[str, Any]:
    # Kept for API compatibility. Dirty-candidate mode changes the CLI exit
    # policy, never the truth value of the clean-tree evidence check.
    _ = enforce_clean_tree
    protocol = load_protocol() if protocol is None else dict(protocol)
    tasks = tuple(list_tasks())
    task_payloads = {task.task_id: task.to_dict() for task in tasks}
    expected_hashes = dict(protocol["expected_task_contract_hashes"])
    actual_hashes = {task.task_id: task.contract_hash for task in tasks}
    minimum_rank = MaturityLevel.normalize(
        str(protocol["minimum_task_maturity"])
    ).rank

    runtime_report = build_runtime_audit()
    reachability_protocol = load_reachability_protocol()
    reachability_report = build_reachability_report(reachability_protocol)
    maturity_protocol = load_maturity_protocol()
    maturity_report = build_maturity_report(maturity_protocol)
    state_protocol = load_state_protocol()
    state_report = build_state_report(state_protocol)
    public_boundary_report = build_public_boundary_report(
        load_public_boundary_protocol()
    )

    tracked_changes = _tracked_source_changes()
    source_tree_dirty = bool(tracked_changes)
    artifact_hashes = {
        relative: _file_hash(ROOT / relative)
        for relative in protocol["bound_artifacts"]
        if (ROOT / relative).is_file()
    }
    expected_counts = protocol["expected_counts"]
    checks = {
        "protocol_schema": protocol.get("schema_version")
        == "chemworld-foundation-backend-freeze-protocol-0.1",
        "candidate_claim_boundary": protocol.get("release_status")
        == "candidate_backend_only"
        and protocol.get("benchmark_claim_allowed") is False,
        # Tree cleanliness is evidence, not a command-line policy choice.  The
        # old implementation made this check true under --allow-dirty and could
        # therefore emit source_tree_dirty=true together with a "frozen"
        # status.  --allow-dirty now controls only whether a current development
        # snapshot may be written; it never upgrades that snapshot to a clean
        # release attestation.
        "clean_tracked_tree": not source_tree_dirty,
        "task_contracts_exact": actual_hashes == expected_hashes,
        "task_count_exact": len(tasks) == expected_counts["tasks"],
        "operation_count_exact": len(OPERATION_TYPES) == expected_counts["operations"],
        "task_maturity_floor": all(
            MaturityLevel.normalize(payload["physics_maturity"]).rank >= minimum_rank
            and payload["proxy_allowed"] is False
            for payload in task_payloads.values()
        ),
        "runtime_integration": runtime_report["passed"] is True,
        "runtime_reachability": not validate_reachability_report(
            reachability_report, reachability_protocol
        )
        and reachability_report["provider_count"] == expected_counts["providers"]
        and reachability_report["lite_upgrade_targets"] == {},
        "maturity_truth": not validate_maturity_report(
            maturity_report, maturity_protocol
        )
        and maturity_report["release_allowed"] is True
        and maturity_report["finding_count"] == 0
        and maturity_report["model_card_count"] == expected_counts["model_cards"]
        and maturity_report["adapter_manifest_count"]
        == expected_counts["adapter_manifests"],
        "state_transition_invariants": not validate_state_report(
            state_report, state_protocol
        )
        and state_report["controls_complete"] is True
        and state_report["defect_inventory"] == [],
        "public_boundary": public_boundary_report["controls_ready"] is True
        and public_boundary_report["backend_freeze_allowed"] is True,
        "bound_artifacts_complete": set(artifact_hashes)
        == set(protocol["bound_artifacts"]),
    }
    contract_checks = {
        key: value for key, value in checks.items() if key != "clean_tracked_tree"
    }
    backend_contract_validated = all(contract_checks.values())
    backend_freeze_allowed = backend_contract_validated and checks["clean_tracked_tree"]
    if backend_freeze_allowed:
        status = "candidate_backend_clean_attested"
        clean_release_attestation = "passed"
    elif backend_contract_validated:
        status = "candidate_backend_validated_dirty_tree"
        clean_release_attestation = "pending_clean_tree"
    else:
        status = "blocked"
        clean_release_attestation = "blocked"
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "backend_id": protocol["backend_id"],
        "world_law_id": protocol["world_law_id"],
        "release_status": protocol["release_status"],
        "benchmark_claim_allowed": False,
        "backend_contract_validated": backend_contract_validated,
        "backend_freeze_allowed": backend_freeze_allowed,
        "clean_release_attestation": clean_release_attestation,
        "status": status,
        "source_commit": _git_output("rev-parse", "HEAD"),
        "source_tree_dirty": source_tree_dirty,
        "protocol_sha256": _json_hash(protocol),
        "task_contract_hashes": actual_hashes,
        "artifact_sha256": artifact_hashes,
        "checks": checks,
        "required_external_gates": list(protocol["required_external_gates"]),
        "limitations": list(protocol["limitations"]),
        "report_hash": None,
    }
    report["report_hash"] = _json_hash(report)
    return report


def validate_report(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unsupported report schema")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks:
        errors.append("checks missing")
    else:
        expected = all(bool(value) for value in checks.values())
        if report.get("backend_freeze_allowed") is not expected:
            errors.append("freeze decision mismatch")
        contract_expected = all(
            bool(value) for key, value in checks.items() if key != "clean_tracked_tree"
        )
        if report.get("backend_contract_validated") is not contract_expected:
            errors.append("backend contract validation mismatch")
        expected_attestation = (
            "passed"
            if expected
            else "pending_clean_tree"
            if contract_expected
            else "blocked"
        )
        if report.get("clean_release_attestation") != expected_attestation:
            errors.append("clean release attestation mismatch")
        expected_status = (
            "candidate_backend_clean_attested"
            if expected
            else "candidate_backend_validated_dirty_tree"
            if contract_expected
            else "blocked"
        )
        if report.get("status") != expected_status:
            errors.append("backend status mismatch")
    expected_hash = _json_hash({**dict(report), "report_hash": None})
    if report.get("report_hash") != expected_hash:
        errors.append("report hash mismatch")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--allow-dirty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(
        load_protocol(args.protocol),
        enforce_clean_tree=not args.allow_dirty,
    )
    errors = validate_report(report)
    if errors:
        raise ValueError("invalid backend freeze report: " + "; ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["backend_freeze_allowed"]:
        return 0
    if args.allow_dirty and report["backend_contract_validated"]:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
