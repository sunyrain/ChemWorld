"""Preflight report for the frozen mechanism-adaptation confirmation protocol."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.mechanism_adaptation import (
    evaluate_protocol_gates,
    validate_mechanism_adaptation_protocol,
)
from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL = configuration_root() / "benchmark/mechanism_adaptation_v0.2.1.json"
REQUIRED_IMPLEMENTATION_ARTIFACTS = (
    "configs/benchmark/mechanism_adaptation_gate_a_v0.2.4.json",
    "src/chemworld/agents/mechanism_adaptation_live_llm.py",
    "src/chemworld/eval/mechanism_adaptation.py",
    "src/chemworld/eval/mechanism_design_audit.py",
    "src/chemworld/eval/mechanism_adaptation_execution.py",
    "scripts/audit_mechanism_adaptation_design.py",
    "scripts/run_mechanism_adaptation_v0_2.py",
    "scripts/plan_mechanism_adaptation_matrix.py",
    "tests/test_mechanism_adaptation.py",
    "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-public-matrix.json",
    "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc6.json",
)


def build_mechanism_adaptation_preflight(
    protocol_path: Path = DEFAULT_PROTOCOL,
) -> dict[str, Any]:
    """Check protocol completeness without treating unrun empirical gates as failures."""

    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    validation_errors = validate_mechanism_adaptation_protocol(protocol)
    design_audit_path = (
        ROOT / "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-design-audit-freeze-rc6.json"
    )
    gate_a_plan_path = configuration_root() / "benchmark/mechanism_adaptation_gate_a_v0.2.4.json"
    gate_a_plan = json.loads(gate_a_plan_path.read_text(encoding="utf-8"))
    design_audit = (
        json.loads(design_audit_path.read_text(encoding="utf-8"))
        if design_audit_path.is_file()
        else {}
    )
    design_audit_pass = bool(
        design_audit.get("pass")
        and design_audit.get("protocol_sha256") == _canonical_sha256(protocol)
        and design_audit.get("gate_a_plan_sha256") == _canonical_sha256(gate_a_plan)
    )
    artifacts = []
    for relative in REQUIRED_IMPLEMENTATION_ARTIFACTS:
        path = ROOT / relative
        artifacts.append(
            {
                "path": relative,
                "exists": path.is_file(),
                "sha256": _sha256(path) if path.is_file() else None,
            }
        )
    gate_status = evaluate_protocol_gates(protocol, {}) if not validation_errors else None
    implementation_complete = (
        not validation_errors and design_audit_pass and all(item["exists"] for item in artifacts)
    )
    return {
        "schema_version": "chemworld-mechanism-adaptation-preflight-0.2",
        "protocol_id": protocol.get("protocol_id"),
        "protocol_path": _relative_path(protocol_path),
        "protocol_sha256": _sha256(protocol_path),
        "status": (
            "protocol_complete_empirical_execution_pending"
            if implementation_complete
            else "preflight_incomplete"
        ),
        "implementation_complete": implementation_complete,
        "method_freeze_decision_blocker_count": len(validation_errors),
        "method_freeze_decision_blockers": validation_errors,
        "design_validity_audit_pass": design_audit_pass,
        "design_validity_audit": design_audit,
        "external_empirical_run_completed": False,
        "empirical_gate_status": dict.fromkeys(
            ("gate_0", "gate_a", "gate_b", "gate_c", "gate_d", "gate_e"),
            "not_evaluated",
        ),
        "gate_evaluator_without_evidence": gate_status,
        "publication_ready": False,
        "artifacts": artifacts,
        "interpretation": (
            "There are no unresolved method-freeze choices when blocker_count is zero. "
            "The remaining work is execution of the frozen external multi-seed/provider "
            "matrix, not an unmade protocol decision."
        ),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


__all__ = [
    "DEFAULT_PROTOCOL",
    "REQUIRED_IMPLEMENTATION_ARTIFACTS",
    "build_mechanism_adaptation_preflight",
]
