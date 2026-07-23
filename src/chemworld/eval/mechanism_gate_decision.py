"""Authoritative certificate composition for mechanism-adaptation gates."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    repository_tree_sha256,
)
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task
from chemworld.world.operations import operation_contracts

ONLINE_POLICY_CERTIFICATE_VERSION = "chemworld-mechanism-adaptation-online-policy-certificate-0.4"
PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def gate_a_execution_contract_binding(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind every Gate A certificate to the runtime semantics it evaluated."""

    config_paths = {
        "backend_contract": configuration_root() / "foundation/backend_v0.5.json",
        "evaluation_contract": configuration_root() / "benchmark/evaluation_vnext.json",
        "public_boundary_contract": (
            configuration_root() / "foundation/public_boundary_security_vnext.json"
        ),
    }
    binding: dict[str, Any] = {
        "schema_version": "chemworld-gate-a-execution-binding-0.1",
        "runtime_source_tree_sha256": repository_tree_sha256(
            PACKAGE_ROOT,
            relative_roots=(".",),
        ),
        "task_contract_hashes": {
            str(task_id): get_task(str(task_id)).contract_hash
            for task_id in protocol["design"]["tasks"]
        },
        "operation_contract_sha256": canonical_json_sha256(
            {key: value.to_dict() for key, value in sorted(operation_contracts().items())}
        ),
        "bound_config_sha256": {
            key: file_sha256(path) for key, path in sorted(config_paths.items())
        },
        "protocol_sha256": canonical_json_sha256(protocol),
        "gate_a_plan_sha256": canonical_json_sha256(plan),
    }
    binding["binding_sha256"] = canonical_json_sha256(binding)
    return binding


def gate_a_certificate_decision(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    *,
    controlled_gate_pass: bool,
    online_policy_certificate: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose Gate A from its two independently bound certificates.

    The controlled matched oracle establishes that the public experiment contract
    contains diagnostic information. It is not a substitute for demonstrating that
    an online policy can select and use diagnostic experiments under the same budget.
    Missing, stale, or malformed online-policy evidence therefore fails closed.
    """

    requirement = plan.get("online_policy_feasible_certificate")
    if (
        not isinstance(requirement, Mapping)
        or requirement.get("required_before_formal_mechanism_claim") is not True
    ):
        raise ValueError("Gate A plan must require an online-policy-feasible certificate")

    expected_protocol_sha = canonical_json_sha256(protocol)
    expected_plan_sha = canonical_json_sha256(plan)
    expected_execution_binding = gate_a_execution_contract_binding(protocol, plan)
    controlled_primary_budget = int(plan["held_out_certificate"]["primary_gate_budget"])
    online_gate_budget = int(requirement["online_policy_gate_budget"])
    if online_gate_budget != controlled_primary_budget:
        raise ValueError("Gate A controlled and online certificates must use an aligned budget")
    if online_policy_certificate is None:
        online_summary = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "status": "pending_execution",
            "gate_pass": False,
            "required": True,
            "certificate_present": False,
            "controlled_matched_primary_budget": controlled_primary_budget,
            "online_policy_gate_budget": online_gate_budget,
        }
    else:
        certificate = dict(online_policy_certificate)
        errors: list[str] = []
        expected_values = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "certificate_scope": "online_policy_feasible_diagnosis",
            "protocol_sha256": expected_protocol_sha,
            "gate_a_plan_sha256": expected_plan_sha,
            "controlled_matched_primary_budget": controlled_primary_budget,
            "online_policy_gate_budget": online_gate_budget,
            "hidden_change_time": True,
            "policy_received_phase_or_reset_indicator": False,
            "uses_actual_available_pre_change_history": True,
            "uses_actual_action_measurement_and_budget_contract": True,
            "execution_contract_binding_sha256": expected_execution_binding["binding_sha256"],
        }
        for field, expected in expected_values.items():
            if certificate.get(field) != expected:
                errors.append(f"{field} must equal {expected!r}")
        gate_pass = certificate.get("gate_pass")
        if not isinstance(gate_pass, bool):
            errors.append("gate_pass must be boolean")
        expected_status = "passed" if gate_pass is True else "failed"
        if certificate.get("status") != expected_status:
            errors.append(f"status must equal {expected_status!r}")
        if errors:
            raise ValueError("invalid online-policy-feasible certificate: " + "; ".join(errors))
        online_summary = {
            **certificate,
            "required": True,
            "certificate_present": True,
            "certificate_sha256": canonical_json_sha256(certificate),
        }

    online_gate_pass = online_summary["gate_pass"] is True
    combined_pass = bool(controlled_gate_pass and online_gate_pass)
    if combined_pass:
        status = "gate_a_passed"
    elif not controlled_gate_pass:
        status = "gate_a_failed_controlled_matched_certificate"
    elif online_summary["certificate_present"] is not True:
        status = "gate_a_blocked_online_policy_certificate_pending"
    else:
        status = "gate_a_failed_online_policy_certificate"
    return {
        "schema_version": "chemworld-mechanism-adaptation-gate-a-decision-0.1",
        "status": status,
        "required_certificates": [
            "controlled_matched_identifiability",
            "online_policy_feasible_diagnosis",
        ],
        "controlled_matched_gate_pass": bool(controlled_gate_pass),
        "online_policy_feasible_gate_pass": online_gate_pass,
        "online_policy_feasible_certificate": online_summary,
        "gate_a_pass": combined_pass,
    }


__all__ = [
    "ONLINE_POLICY_CERTIFICATE_VERSION",
    "gate_a_certificate_decision",
    "gate_a_execution_contract_binding",
]
