"""Fail-closed synthesis of ChemWorld's benchmark architecture evidence."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.physchem.mechanism_library import configuration_root

ARCHITECTURE_PROTOCOL_VERSION = "chemworld-benchmark-architecture-protocol-0.1"
ARCHITECTURE_AUDIT_VERSION = "chemworld-benchmark-architecture-audit-0.1"
DEFAULT_ARCHITECTURE_PROTOCOL_PATH = configuration_root() / "benchmark" / "architecture_vnext.json"
ROOT = Path(__file__).resolve().parents[3]


def load_architecture_protocol(
    path: str | Path = DEFAULT_ARCHITECTURE_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("architecture protocol must be a JSON object")
    return payload


def audit_benchmark_architecture(protocol: Mapping[str, Any]) -> dict[str, Any]:
    """Build one evidence graph without upgrading any missing result to a claim."""

    cache: dict[str, dict[str, Any]] = {}
    control_components = _audit_components(protocol.get("control_components"), cache)
    formal_components = _audit_components(
        protocol.get("formal_evidence_components"),
        cache,
    )
    cross_contracts = _audit_cross_contracts(protocol, cache)
    issues = _audit_known_issues(protocol.get("known_issue_probes"), cache)

    checks = {
        "schema": protocol.get("schema_version") == ARCHITECTURE_PROTOCOL_VERSION,
        "candidate_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False,
        "control_components_declared": bool(control_components),
        "formal_components_declared": bool(formal_components),
        "all_component_reports_exist": all(
            card["report_exists"]
            for card in (*control_components.values(), *formal_components.values())
        ),
        "all_report_digests_retained": all(
            bool(card["sha256"])
            for card in (*control_components.values(), *formal_components.values())
        ),
        "cross_contracts_consistent": all(cross_contracts.values()),
        "declared_cross_contracts_match": set(cross_contracts)
        == set(_mapping(protocol.get("required_cross_contracts"))),
        "publication_gate_is_conjunctive": "every control" in str(protocol.get("release_rule", "")),
    }
    controls_ready = all(card["passed"] for card in control_components.values())
    formal_evidence_ready = all(card["passed"] for card in formal_components.values())
    architecture_consistent = all(checks.values())
    active_issues = [card for card in issues if card["active"]]
    critical_path = [
        {
            "component": name,
            "observed": card["observed"],
            "required": card["expected"],
            "report": card["report"],
        }
        for name, card in formal_components.items()
        if not card["passed"]
    ]
    publication_ready = bool(
        architecture_consistent
        and controls_ready
        and formal_evidence_ready
        and not active_issues
        and protocol.get("publication_ready") is True
    )
    return {
        "schema_version": ARCHITECTURE_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": (
            "publication_ready"
            if publication_ready
            else "controls_ready_formal_evidence_missing"
            if architecture_consistent and controls_ready
            else "architecture_controls_failed"
        ),
        "benchmark_claim_allowed": publication_ready,
        "publication_ready": publication_ready,
        "architecture_consistent": architecture_consistent,
        "controls_ready": controls_ready,
        "formal_evidence_ready": formal_evidence_ready,
        "checks": checks,
        "cross_contracts": cross_contracts,
        "control_components": control_components,
        "formal_evidence_components": formal_components,
        "active_issue_count": len(active_issues),
        "active_issues": active_issues,
        "critical_path": critical_path,
        "release_rule": protocol.get("release_rule"),
    }


def _audit_components(
    raw_components: object,
    cache: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_components, Mapping):
        return {}
    audited: dict[str, dict[str, Any]] = {}
    for name, raw_spec in raw_components.items():
        spec = raw_spec if isinstance(raw_spec, Mapping) else {}
        report_path = str(spec.get("report", ""))
        payload, digest = _load_report(report_path, cache)
        field = str(spec.get("field", ""))
        observed = _field_value(payload, field) if payload is not None else None
        expected = spec.get("expected")
        audited[str(name)] = {
            "report": report_path,
            "report_exists": payload is not None,
            "sha256": digest,
            "field": field,
            "observed": observed,
            "expected": expected,
            "passed": payload is not None and observed == expected,
        }
    return audited


def _audit_known_issues(
    raw_probes: object,
    cache: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(raw_probes, list):
        return []
    issues: list[dict[str, Any]] = []
    for raw_probe in raw_probes:
        probe = raw_probe if isinstance(raw_probe, Mapping) else {}
        report_path = str(probe.get("report", ""))
        payload, digest = _load_report(report_path, cache)
        field = str(probe.get("field", ""))
        observed = _field_value(payload, field) if payload is not None else None
        problem_value = probe.get("problem_value")
        issues.append(
            {
                "issue_id": probe.get("issue_id"),
                "severity": probe.get("severity"),
                "active": payload is None or observed == problem_value,
                "observed": observed,
                "problem_value": problem_value,
                "report": report_path,
                "report_sha256": digest,
                "impact": probe.get("impact"),
                "remediation": probe.get("remediation"),
            }
        )
    return issues


def _audit_cross_contracts(
    protocol: Mapping[str, Any],
    cache: dict[str, dict[str, Any]],
) -> dict[str, bool]:
    freeze = _config("confirmatory_freeze_vnext.json", cache)
    methods = _config("method_protocol_vnext.json", cache)
    rl = _config("rl_baselines_vnext.json", cache)
    live = _config("live_llm_vnext.json", cache)

    freeze_tasks = set(_sequence(_field_value(freeze, "task_roles.core")))
    method_tasks = set(_sequence(methods.get("provisional_core_tasks")))
    rl_tasks = set(_sequence(rl.get("core_tasks")))
    method_cards = methods.get("methods", {})
    method_ids = set(method_cards) if isinstance(method_cards, Mapping) else set()
    rl_algorithms = rl.get("algorithms", {})
    rl_ids = set(rl_algorithms) if isinstance(rl_algorithms, Mapping) else set()
    llm_roles = live.get("agent_roles", {})
    llm_ids = set(llm_roles) if isinstance(llm_roles, Mapping) else set()
    llm_limits = _field_value(
        methods,
        "resource_policy.llm_hard_limits_per_evaluation_run",
    )
    request_limit = (
        int(llm_limits.get("provider_request_limit_per_operation", 0))
        if isinstance(llm_limits, Mapping)
        else 0
    )
    retries_counted = (
        llm_limits.get("failed_requests_count_toward_limit") is True
        if isinstance(llm_limits, Mapping)
        else False
    )
    claim_flags: list[object] = []
    for section in ("control_components", "formal_evidence_components"):
        for raw_spec in _mapping(protocol.get(section)).values():
            spec = raw_spec if isinstance(raw_spec, Mapping) else {}
            payload, _ = _load_report(str(spec.get("report", "")), cache)
            if payload is not None and "benchmark_claim_allowed" in payload:
                claim_flags.append(payload["benchmark_claim_allowed"])
    return {
        "core_task_sets_match": bool(freeze_tasks) and freeze_tasks == method_tasks == rl_tasks,
        "rl_algorithm_roles_match": bool(rl_ids) and rl_ids <= method_ids,
        "llm_role_ids_match": bool(llm_ids) and llm_ids <= method_ids,
        "provider_retries_bounded": request_limit >= 1 and retries_counted,
        "all_referenced_claim_flags_false": bool(claim_flags)
        and all(flag is False for flag in claim_flags)
        and all(
            config.get("benchmark_claim_allowed") is False for config in (freeze, methods, rl, live)
        ),
    }


def _config(filename: str, cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    relative = f"configs/benchmark/{filename}"
    payload, _ = _load_report(relative, cache)
    return payload or {}


def _load_report(
    relative_path: str,
    cache: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, str | None]:
    if relative_path in cache:
        cached = cache[relative_path]
        return cached["payload"], cached["sha256"]
    path = ROOT / relative_path
    if not relative_path or not path.is_file():
        return None, None
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"architecture evidence must be an object: {relative_path}")
    digest = hashlib.sha256(raw).hexdigest()
    cache[relative_path] = {"payload": payload, "sha256": digest}
    return payload, digest


def _field_value(payload: Mapping[str, Any] | None, field: str) -> Any:
    current: Any = payload
    for segment in field.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            return None
        current = current[segment]
    return current


def _sequence(value: object) -> tuple[str, ...]:
    if not isinstance(value, list | tuple):
        return ()
    return tuple(str(item) for item in value)


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


__all__ = [
    "ARCHITECTURE_AUDIT_VERSION",
    "ARCHITECTURE_PROTOCOL_VERSION",
    "DEFAULT_ARCHITECTURE_PROTOCOL_PATH",
    "audit_benchmark_architecture",
    "load_architecture_protocol",
]
