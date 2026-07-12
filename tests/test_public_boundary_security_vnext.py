from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_public_boundary_security_vnext import (
    PROTOCOL_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    _dependency_bindings,
    _identity_findings,
    build_report,
    load_protocol,
)

from chemworld.eval.public_harness import STEP_INFO_ALLOWLIST, TASK_INFO_ALLOWLIST
from chemworld.tasks import SERIOUS_TASK_IDS

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs" / "foundation" / "public_boundary_security_vnext.json"
REPORT = (
    ROOT
    / "workstreams"
    / "world_foundation"
    / "reports"
    / "public-boundary-security-vnext.json"
)


def test_protocol_declares_exact_public_surface_and_fail_closed_policy() -> None:
    protocol = load_protocol(PROTOCOL)

    assert protocol["schema_version"] == PROTOCOL_SCHEMA_VERSION
    assert protocol["status"] == "candidate_gate"
    assert protocol["freeze_policy"] == "all_declared_checks_must_pass"
    assert protocol["task_ids"] == list(SERIOUS_TASK_IDS)
    assert set(protocol["public_task_info_allowlist"]) == set(TASK_INFO_ALLOWLIST)
    assert set(protocol["public_step_info_allowlist"]) == set(STEP_INFO_ALLOWLIST)
    assert set(protocol["required_probe_groups"]) == {
        "allowlist_schema",
        "leakage",
        "adversarial",
        "replay",
        "invariance",
        "execution",
    }


def test_dependency_drift_and_identity_leaks_are_detected() -> None:
    protocol = load_protocol(PROTOCOL)
    bindings, ready = _dependency_bindings(protocol)

    assert ready is True
    assert all(item["passed"] for item in bindings.values())
    forbidden = frozenset(protocol["forbidden_identity_keys"])
    assert _identity_findings(
        {"provider_parameters": {"temperature": 0.1}, "nested": {"model_id": "x"}},
        forbidden,
    ) == ["$.provider_parameters", "$.nested.model_id"]
    assert _identity_findings({"mechanism_id": "public-mechanism"}, forbidden) == []


def test_committed_report_is_exact_executable_audit() -> None:
    committed = json.loads(REPORT.read_text(encoding="utf-8"))
    rebuilt = build_report(load_protocol(PROTOCOL))

    assert committed == rebuilt


def test_report_closes_every_declared_gate_without_sandbox_overclaim() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["schema_version"] == REPORT_SCHEMA_VERSION
    assert report["status"] == "controls_ready"
    assert report["controls_ready"] is True
    assert report["backend_freeze_allowed"] is True
    assert report["probe_count"] == 35
    assert all(report["checks"].values())
    assert all(
        all(probes.values()) for probes in report["probe_groups"].values()
    )
    assert report["probe_groups"]["replay"]["trajectory_truncation_rejected"] is True
    assert report["probe_groups"]["replay"]["trajectory_digest_tamper_rejected"] is True
    assert report["probe_groups"]["execution"]["windows_source_process"] is True
    assert report["probe_groups"]["execution"]["independent_process"] is True
    assert report["probe_groups"]["execution"]["clean_wheel_import"] is True
    assert report["details"]["execution"]["security_boundary"].endswith(
        "not-an-os-sandbox"
    )
