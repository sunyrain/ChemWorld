from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

import gymnasium as gym
from scripts.audit_public_boundary_security_vnext import (
    PROTOCOL_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    _dependency_bindings,
    _identity_findings,
    build_report,
    load_protocol,
)

import chemworld  # noqa: F401
from chemworld.eval.public_harness import STEP_INFO_ALLOWLIST, TASK_INFO_ALLOWLIST
from chemworld.tasks import SERIOUS_TASK_IDS

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs" / "foundation" / "public_boundary_security_vnext.json"
REPORT = (
    ROOT / "workstreams" / "world_foundation" / "reports" / "public-boundary-security-vnext.json"
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


def test_paired_world_identity_is_private_but_evaluator_provenance_is_retained() -> None:
    baseline = gym.make("ChemWorld", task_id="electrochemical-conversion", seed=0)
    changed = gym.make(
        "ChemWorld",
        task_id="electrochemical-conversion",
        seed=0,
        world_interventions=(
            {
                "kind": "mechanism_family",
                "mode": "constitutive_law_family",
                "severity": 0.8,
            },
        ),
    )
    try:
        _, baseline_info = baseline.reset(seed=0)
        _, changed_info = changed.reset(seed=0)
        assert baseline_info == changed_info
        assert "seed" not in baseline_info
        assert baseline.unwrapped.evaluator_provenance()["world_seed"] == 0
        forbidden_public_keys = {
            "world_id",
            "world_provider",
            "mechanism_id",
            "mechanism_hash",
            "mechanism_version",
            "world_family_intervention_hash",
            "mechanism_family_intervention_hash",
            "material_law_counterfactual_hash",
        }

        def public_keys(value: object) -> set[str]:
            if isinstance(value, dict):
                return set(value) | {
                    nested for item in value.values() for nested in public_keys(item)
                }
            if isinstance(value, list):
                return {nested for item in value for nested in public_keys(item)}
            return set()

        assert public_keys(baseline_info).isdisjoint(forbidden_public_keys)
        baseline_provenance = baseline.unwrapped.evaluator_provenance()
        changed_provenance = changed.unwrapped.evaluator_provenance()
        assert baseline_provenance["world_id"] != changed_provenance["world_id"]
        assert changed_provenance["mechanism_family_intervention_hash"]

        _, _, _, _, step_info = baseline.step(
            {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0}
        )
        assert step_info["campaign_id"].startswith("episode-")
        UUID(step_info["campaign_id"].removeprefix("episode-"))
    finally:
        baseline.close()
        changed.close()


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
    assert report["checks"]["exploit_matrix_runtime"] is True
    assert all(all(probes.values()) for probes in report["probe_groups"].values())
    assert report["probe_groups"]["replay"]["trajectory_truncation_rejected"] is True
    assert report["probe_groups"]["replay"]["trajectory_digest_tamper_rejected"] is True
    assert report["details"]["adversarial"]["exploit_probes_revalidated_directly"] is True
    assert report["details"]["adversarial"]["exploit_controls_ready"] is True
    assert report["probe_groups"]["execution"]["windows_source_process"] is True
    assert report["probe_groups"]["execution"]["independent_process"] is True
    assert report["probe_groups"]["execution"]["clean_wheel_import"] is True
    assert report["details"]["execution"]["security_boundary"].endswith("not-an-os-sandbox")
