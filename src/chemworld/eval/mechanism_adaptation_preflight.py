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

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/mechanism_adaptation_v0.2.json"
REQUIRED_IMPLEMENTATION_ARTIFACTS = (
    "src/chemworld/agents/mechanism_adaptation_live_llm.py",
    "src/chemworld/eval/mechanism_adaptation.py",
    "src/chemworld/eval/flagship_reanalysis.py",
    "scripts/reanalyze_flagship_mechanism_diagnostics.py",
    "scripts/plan_mechanism_adaptation_matrix.py",
    "tests/test_mechanism_adaptation.py",
    "tests/test_flagship_reanalysis.py",
    "workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.1.json",
    "workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.1.md",
    "workstreams/flagship_tasks/reports/mechanism-adaptation-final-protocol-v0.2.md",
    "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2-public-matrix.json",
)


def build_mechanism_adaptation_preflight(
    protocol_path: Path = DEFAULT_PROTOCOL,
) -> dict[str, Any]:
    """Check protocol completeness without treating unrun empirical gates as failures."""

    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    validation_errors = validate_mechanism_adaptation_protocol(protocol)
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
    implementation_complete = not validation_errors and all(item["exists"] for item in artifacts)
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
