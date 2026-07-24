"""Preflight report for the frozen mechanism-adaptation confirmation protocol."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.mechanism_adaptation import (
    evaluate_protocol_gates,
    load_mechanism_adaptation_protocol,
    validate_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_gate_decision import (
    gate_a_certificate_decision,
    gate_a_execution_contract_binding,
)
from chemworld.eval.mechanism_relation_graph import (
    validate_diagnostic_relation_graph,
)
from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL = configuration_root() / "benchmark/mechanism_adaptation_v0.3.0.json"
REQUIRED_IMPLEMENTATION_ARTIFACTS = (
    "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json",
    "src/chemworld/agents/mechanism_adaptation_live_llm.py",
    "src/chemworld/eval/mechanism_adaptation.py",
    "src/chemworld/eval/flagship_semantics_audit.py",
    "src/chemworld/eval/mechanism_gate_decision.py",
    "src/chemworld/eval/mechanism_design_audit.py",
    "src/chemworld/eval/mechanism_relation_graph.py",
    "src/chemworld/eval/mechanism_adaptation_execution.py",
    "scripts/audit_mechanism_adaptation_design.py",
    "scripts/audit_flagship_experiment_semantics.py",
    "scripts/build_mechanism_diagnostic_relation_graph.py",
    "scripts/run_mechanism_adaptation.py",
    "scripts/plan_mechanism_adaptation_matrix.py",
    "tests/test_mechanism_adaptation.py",
    "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-public-matrix.json",
    "workstreams/flagship_tasks/reports/flagship-experiment-semantics-audit-rc23.json",
)


def build_mechanism_adaptation_preflight(
    protocol_path: Path = DEFAULT_PROTOCOL,
) -> dict[str, Any]:
    """Check protocol completeness without treating unrun empirical gates as failures."""

    protocol = load_mechanism_adaptation_protocol(protocol_path)
    validation_errors = validate_mechanism_adaptation_protocol(protocol)
    design_audit_relative = str(
        protocol["intervention_action_alignment"]["design_audit_report"]
    )
    design_audit_path = ROOT / design_audit_relative
    gate_a_plan_path = configuration_root() / "benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
    gate_a_plan = json.loads(gate_a_plan_path.read_text(encoding="utf-8"))
    relation_graph_path = ROOT / gate_a_plan["diagnostic_relation_graph"]["report"]
    relation_graph = (
        json.loads(relation_graph_path.read_text(encoding="utf-8"))
        if relation_graph_path.is_file()
        else {}
    )
    relation_graph_errors = (
        validate_diagnostic_relation_graph(protocol, gate_a_plan, relation_graph)
        if relation_graph
        else ["diagnostic relation graph is missing"]
    )
    semantics_path = (
        ROOT
        / "workstreams/flagship_tasks/reports/"
        "flagship-experiment-semantics-audit-rc23.json"
    )
    semantics = (
        json.loads(semantics_path.read_text(encoding="utf-8"))
        if semantics_path.is_file()
        else {}
    )
    semantics_errors = []
    if (
        semantics.get("pass") is not True
        or semantics.get("protocol_sha256") != _canonical_sha256(protocol)
        or semantics.get("gate_a_plan_sha256")
        != _canonical_sha256(gate_a_plan)
    ):
        semantics_errors.append(
            "flagship experiment semantics audit is missing, failed, or stale"
        )
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
    required_artifacts = (
        *REQUIRED_IMPLEMENTATION_ARTIFACTS,
        design_audit_relative,
        str(gate_a_plan["diagnostic_relation_graph"]["report"]),
    )
    for relative in required_artifacts:
        path = ROOT / relative
        artifacts.append(
            {
                "path": relative,
                "exists": path.is_file(),
                "sha256": _sha256(path) if path.is_file() else None,
            }
        )
    gate_status = (
        evaluate_protocol_gates(
            protocol,
            {"gate_a": {"design_validity_audit": design_audit}},
            gate_a_plan=gate_a_plan,
        )
        if not validation_errors
        else None
    )
    implementation_complete = (
        not validation_errors
        and not relation_graph_errors
        and not semantics_errors
        and design_audit_pass
        and all(item["exists"] for item in artifacts)
    )
    return {
        "schema_version": "chemworld-mechanism-adaptation-preflight-0.2",
        "protocol_id": protocol.get("protocol_id"),
        "protocol_path": _relative_path(protocol_path),
        "protocol_source_sha256": _sha256(protocol_path),
        "protocol_sha256": _canonical_sha256(protocol),
        "status": (
            "protocol_complete_empirical_execution_pending"
            if implementation_complete
            else "preflight_incomplete"
        ),
        "implementation_complete": implementation_complete,
        "method_freeze_decision_blocker_count": (
            len(validation_errors) + len(relation_graph_errors)
            + len(semantics_errors)
        ),
        "method_freeze_decision_blockers": [
            *validation_errors,
            *relation_graph_errors,
            *semantics_errors,
        ],
        "diagnostic_relation_graph": relation_graph,
        "flagship_experiment_semantics_audit": semantics,
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
            "A1 design validity may be complete while A2 controlled and A3 calibrated "
            "online certificates remain explicitly pending. Agent/provider campaigns "
            "remain separate later gates."
        ),
    }


def build_mechanism_adaptation_pending_gate_state(
    protocol_path: Path = DEFAULT_PROTOCOL,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build explicit non-empirical A3 and Gate A pending-state artifacts."""

    protocol = load_mechanism_adaptation_protocol(protocol_path)
    gate_a_plan_path = (
        configuration_root()
        / "benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
    )
    plan = json.loads(gate_a_plan_path.read_text(encoding="utf-8"))
    design_path = ROOT / plan["design_validity_precondition"]["report"]
    design = (
        json.loads(design_path.read_text(encoding="utf-8"))
        if design_path.is_file()
        else {}
    )
    binding = gate_a_execution_contract_binding(protocol, plan)
    requirement = plan["online_policy_feasible_certificate"]
    online_state = {
        "schema_version": requirement["certificate_schema_version"],
        "certificate_scope": requirement["certificate_scope"],
        "status": "pending_execution",
        "gate_pass": False,
        "formal_benchmark_result": False,
        "certificate_present": False,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": _canonical_sha256(plan),
        "execution_contract_binding": binding,
        "execution_contract_binding_sha256": binding["binding_sha256"],
        "controlled_matched_primary_budget": plan["held_out_certificate"][
            "primary_gate_budget"
        ],
        "online_policy_gate_budget": requirement["online_policy_gate_budget"],
        "evaluation_track_id": requirement["evaluation_track_id"],
        "minimum_stable_prefix_experiments": requirement[
            "minimum_stable_prefix_experiments"
        ],
        "hidden_change_time": True,
        "truth_change_time_support": requirement["truth_change_time_support"],
        "changepoint_semantics": requirement["changepoint_semantics"],
        "policy_received_change_time_support": False,
        "policy_received_minimum_stable_prefix": False,
        "policy_received_reference_certificate": False,
        "policy_received_phase_or_reset_indicator": False,
        "uses_actual_available_pre_change_history": True,
        "uses_actual_action_measurement_and_budget_contract": True,
        "reference_acquisition_certificate": {
            "status": "pending_execution",
            "gate_pass": False,
        },
        "online_capability_chain_certificate": {
            "status": "pending_execution",
            "gate_pass": False,
        },
        "interpretation": (
            "This is a deterministic readiness state, not an empirical online "
            "certificate. A new untouched execution is required."
        ),
        "publication_ready": False,
    }
    decision = gate_a_certificate_decision(
        protocol,
        plan,
        physical_intervention_validity_pass=bool(design.get("pass")),
        controlled_gate_pass=False,
        controlled_certificate_present=False,
    )
    online_reference = {
        **decision["online_policy_feasible_certificate"],
        "report": (
            "workstreams/flagship_tasks/reports/"
            "mechanism-adaptation-online-policy-certificate-v0.7-rc23-pending.json"
        ),
        "certificate_sha256": _canonical_sha256(online_state),
        "certificate_hash_source": "standalone_pending_state_canonical_json",
    }
    decision["online_policy_feasible_certificate"] = online_reference
    gate_state = {
        "schema_version": "chemworld-mechanism-adaptation-gate-a-report-0.3.0",
        "status": decision["status"],
        "formal_benchmark_result": False,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": _canonical_sha256(plan),
        "execution_contract_binding": binding,
        "design_validity_audit": {
            "report": plan["design_validity_precondition"]["report"],
            "pass": bool(design.get("pass")),
        },
        "certificate_decision": decision,
        "controlled_matched_certificate": {
            "status": "pending_execution",
            "gate_pass": False,
            "certificate_present": False,
        },
        "online_policy_feasible_certificate": online_reference,
        "gate_a_pass": False,
        "publication_ready": False,
        "interpretation": (
            "A1 design validity is recorded separately. A2 controlled and A3 "
            "calibrated online certificates have not been executed for v0.3."
        ),
    }
    return online_state, gate_state


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
    "build_mechanism_adaptation_pending_gate_state",
    "build_mechanism_adaptation_preflight",
]
