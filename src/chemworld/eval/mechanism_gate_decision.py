"""Authoritative certificate composition for mechanism-adaptation gates."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256

ONLINE_POLICY_CERTIFICATE_VERSION = (
    "chemworld-mechanism-adaptation-online-policy-certificate-0.1"
)


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
    if not isinstance(requirement, Mapping) or requirement.get(
        "required_before_formal_mechanism_claim"
    ) is not True:
        raise ValueError("Gate A plan must require an online-policy-feasible certificate")

    expected_protocol_sha = canonical_json_sha256(protocol)
    expected_plan_sha = canonical_json_sha256(plan)
    primary_budget = int(plan["held_out_certificate"]["primary_gate_budget"])
    if online_policy_certificate is None:
        online_summary = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "status": "pending_execution",
            "gate_pass": False,
            "required": True,
            "certificate_present": False,
            "primary_gate_budget": primary_budget,
        }
    else:
        certificate = dict(online_policy_certificate)
        errors: list[str] = []
        expected_values = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "certificate_scope": "online_policy_feasible_diagnosis",
            "protocol_sha256": expected_protocol_sha,
            "gate_a_plan_sha256": expected_plan_sha,
            "primary_gate_budget": primary_budget,
            "hidden_change_time": True,
            "uses_actual_available_pre_change_history": True,
            "uses_actual_action_measurement_and_budget_contract": True,
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


__all__ = ["ONLINE_POLICY_CERTIFICATE_VERSION", "gate_a_certificate_decision"]
