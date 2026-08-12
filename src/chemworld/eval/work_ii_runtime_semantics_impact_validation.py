"""Independent validation for Work II runtime-semantics impact audits."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256

EXPECTED_SCHEMA_VERSION = "chemworld-work-ii-runtime-semantics-impact-audit-0.1"
EXPECTED_ACTIONS = {
    "affected": "pending_requalification",
    "unknown": "recover_bound_actions_then_reclassify",
    "unaffected": "no_runtime_semantics_requalification_required",
}


def _nonnegative_integer(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= 0


def _count_mapping_total(value: Any) -> int | None:
    if not isinstance(value, Mapping) or not all(
        _nonnegative_integer(item) for item in value.values()
    ):
        return None
    return sum(value.values())


def validate_runtime_semantics_impact_audit(report: Any) -> dict[str, Any]:
    failures: list[str] = []
    if not isinstance(report, Mapping):
        return {"passed": False, "failure_count": 1, "failures": ["report_not_object"]}
    if report.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        failures.append("schema_version_mismatch")
    embedded_hash = report.get("audit_sha256")
    payload_without_hash = {
        key: value for key, value in report.items() if key != "audit_sha256"
    }
    if not isinstance(embedded_hash, str) or embedded_hash != canonical_json_sha256(
        payload_without_hash
    ):
        failures.append("self_hash_mismatch")

    fixed_fields = {
        "formal_result": False,
        "provider_call_count": 0,
        "participant_outcome_values_used_for_classification": False,
        "formal_execution_authorized": False,
        "requalification_complete": False,
    }
    for key, expected in fixed_fields.items():
        if report.get(key) != expected or (
            key == "provider_call_count" and isinstance(report.get(key), bool)
        ):
            failures.append(f"fixed_field_mismatch:{key}")

    rows = report.get("reports")
    if not isinstance(rows, list):
        failures.append("reports_not_list")
        rows = []
    paths: list[str] = []
    counts: Counter[str] = Counter()
    for index, row in enumerate(rows):
        prefix = f"report[{index}]"
        if not isinstance(row, Mapping):
            failures.append(f"{prefix}:not_object")
            continue
        path = row.get("report_path")
        if not isinstance(path, str):
            failures.append(f"{prefix}:missing_report_path")
        else:
            paths.append(path)
            prefix = path
        classification = row.get("classification")
        if classification not in EXPECTED_ACTIONS:
            failures.append(f"{prefix}:invalid_classification")
            continue
        counts[str(classification)] += 1
        if row.get("required_action") != EXPECTED_ACTIONS[classification]:
            failures.append(f"{prefix}:classification_action_mismatch")

        trigger_ids = row.get("trigger_ids")
        findings = row.get("findings")
        binding = row.get("binding_audit")
        if not isinstance(trigger_ids, list) or not isinstance(findings, Mapping):
            failures.append(f"{prefix}:invalid_findings")
            continue
        if not isinstance(binding, Mapping):
            failures.append(f"{prefix}:invalid_binding_audit")
            continue
        evidence_sources = row.get("execution_evidence_sources")
        if (
            not isinstance(evidence_sources, list)
            or not all(isinstance(source, str) for source in evidence_sources)
            or bool(evidence_sources)
            != (row.get("execution_evidence_detected") is True)
        ):
            failures.append(f"{prefix}:execution_evidence_sources_mismatch")
        action_count = findings.get("action_count")
        destructive_count = findings.get("destructive_measurement_count")
        uncharged_count = findings.get("uncharged_reaction_operation_count")
        if not all(
            _nonnegative_integer(value)
            for value in (action_count, destructive_count, uncharged_count)
        ):
            failures.append(f"{prefix}:invalid_finding_denominator")
            continue
        expected_triggers = []
        if destructive_count:
            expected_triggers.append(
                "destructive_measurement_pre_withdrawal_observation_fix"
            )
        if uncharged_count:
            expected_triggers.append("zero_dose_catalyst_modifier_fix")
        if trigger_ids != expected_triggers:
            failures.append(f"{prefix}:trigger_finding_mismatch")
        destructive_by_instrument = findings.get(
            "destructive_measurements_by_instrument"
        )
        uncharged_by_operation = findings.get(
            "uncharged_reaction_operations_by_operation"
        )
        if _count_mapping_total(destructive_by_instrument) != destructive_count:
            failures.append(f"{prefix}:destructive_denominator_mismatch")
        if _count_mapping_total(uncharged_by_operation) != uncharged_count:
            failures.append(f"{prefix}:uncharged_denominator_mismatch")

        missing = binding.get("missing_paths")
        drift = binding.get("hash_drift_paths")
        artifacts = binding.get("artifacts")
        if not isinstance(missing, list) or not isinstance(drift, list):
            failures.append(f"{prefix}:invalid_binding_failures")
            continue
        artifact_action_counts = (
            [
                item.get("action_count")
                for item in artifacts
                if isinstance(item, Mapping)
            ]
            if isinstance(artifacts, list)
            else []
        )
        valid_artifact_action_counts = [
            value
            for value in artifact_action_counts
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0
        ]
        if (
            not isinstance(artifacts, list)
            or len(artifact_action_counts) != len(artifacts)
            or len(valid_artifact_action_counts) != len(artifact_action_counts)
            or sum(valid_artifact_action_counts) != action_count
        ):
            failures.append(f"{prefix}:action_denominator_mismatch")
        has_trigger = bool(trigger_ids)
        unknown_condition = bool(missing or drift) or (
            row.get("execution_evidence_detected") is True and action_count == 0
        )
        expected_classification = (
            "affected" if has_trigger else "unknown" if unknown_condition else "unaffected"
        )
        if classification != expected_classification:
            failures.append(f"{prefix}:classification_basis_mismatch")

        basis = row.get("classification_basis")
        if not isinstance(basis, Mapping) or not artifacts:
            failures.append(f"{prefix}:missing_classification_basis")
            continue
        root_findings = artifacts[0].get("findings", {})
        direct_trigger = bool(
            root_findings.get("destructive_measurement_count", 0)
            or root_findings.get("uncharged_reaction_operation_count", 0)
        )
        expected_basis = {
            "direct_action_trigger": direct_trigger,
            "bound_action_trigger": has_trigger and not direct_trigger,
            "binding_failure": bool(missing or drift),
            "execution_summary_without_actions": (
                row.get("execution_evidence_detected") is True and action_count == 0
            ),
            "fail_closed_propagation": (
                classification in {"affected", "unknown"} and not direct_trigger
            ),
        }
        if dict(basis) != expected_basis:
            failures.append(f"{prefix}:classification_basis_fields_mismatch")

    if len(paths) != len(set(paths)):
        failures.append("duplicate_report_paths")
    denominators = report.get("denominators")
    expected_denominators = {
        "report_count": len(rows),
        "affected_report_count": counts["affected"],
        "unknown_report_count": counts["unknown"],
        "unaffected_report_count": counts["unaffected"],
    }
    if denominators != expected_denominators:
        failures.append("summary_denominator_mismatch")
    expected_status = (
        "pending_requalification"
        if counts["affected"] or counts["unknown"]
        else "passed"
    )
    if report.get("status") != expected_status:
        failures.append("summary_status_mismatch")
    return {
        "passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "validated_report_count": len(rows),
    }


__all__ = ["validate_runtime_semantics_impact_audit"]
