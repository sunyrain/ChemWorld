from __future__ import annotations

import copy
import json
import runpy
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "configs" / "current.json"


def _registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _pipeline() -> dict[str, Any]:
    return runpy.run_path("scripts/evidence_pipeline.py", run_name="evidence_pipeline")


def test_current_registry_paths_exist() -> None:
    registry = _registry()
    pipeline = _pipeline()

    assert pipeline["validate_current_registry_paths"](registry, root=ROOT) == []


def test_current_registry_path_validation_fails_closed() -> None:
    registry = _registry()
    validate = _pipeline()["validate_current_registry_paths"]

    missing = copy.deepcopy(registry)
    missing["runtime"]["backend"] = "configs/foundation/does-not-exist.json"
    assert any(
        "missing required current artifact: runtime.backend" in error
        for error in validate(missing, root=ROOT)
    )

    outside = copy.deepcopy(registry)
    outside["runtime"]["backend"] = "../api.md"
    assert any(
        "current registry path escapes repository root: runtime.backend" in error
        for error in validate(outside, root=ROOT)
    )

def test_current_registry_matches_package_and_claim_boundaries() -> None:
    registry = _registry()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert registry["project"]["version"] == pyproject["project"]["version"]
    assert registry["project"]["role"] == "agent_capability_evaluation_and_training_environment"
    assert registry["project"]["environment_updates_agent_weights"] is False
    assert registry["formal_evaluation"]["formal_results_present"] is True
    assert registry["formal_evaluation"]["benchmark_claim_allowed"] is False
    assert (
        registry["formal_evaluation"]["environment_certificate_results_present"]
        is True
    )
    assert (
        registry["formal_evaluation"][
            "environment_benchmark_readiness_claim_allowed"
        ]
        is False
    )
    assert registry["mechanism_adaptation"]["publication_ready"] is False
    assert registry["static_scientific_optimization"]["formal_result"] is True
    assert registry["static_scientific_optimization"]["all_replay_verified"] is True
    assert (
        registry["static_scientific_optimization"]["hidden_world_change_evaluated"]
        is False
    )
    assert registry["task_design"]["registered_task_count"] == 15
    assert registry["task_design"]["executable_midpoint_task_count"] == 15
    assert registry["task_design"]["dead_recipe_coordinate_count"] == 0
    assert registry["task_design"]["formalization_blocker_count"] == 0
    assert registry["task_design"]["formal_experiment_task_ids"] == [
        "electrochemical-conversion",
        "reaction-to-crystallization",
    ]
    assert registry["mechanism_adaptation"]["new_external_provider_runs_completed"] is False
    assert registry["mechanism_adaptation"]["gate_a_pass"] is True
    assert registry["mechanism_adaptation"]["benchmark_ready"] is False
    assert registry["mechanism_adaptation"][
        "a2_structural_receipt"
    ].endswith(
        "mechanism-adaptation-a2-structural-receipt-v0.1-rc28.json"
    )
    assert registry["mechanism_adaptation"][
        "a3_structural_receipt"
    ].endswith(
        "mechanism-adaptation-a3-structural-receipt-v0.1-rc28.json"
    )
    assert registry["mechanism_adaptation"][
        "public_decision_report"
    ].endswith(
        "mechanism-adaptation-public-decision-v0.1-rc28.json"
    )
    assert registry["mechanism_adaptation"]["release_qualification_pass"] is False
    assert registry["mechanism_adaptation"][
        "participant_preregistration_candidate"
    ].endswith("mechanism_adaptation_participant_preregistration_rc28.json")
    assert registry["mechanism_adaptation"]["semantics_audit_pass"] is False
    assert registry["mechanism_adaptation"][
        "semantics_audit_report"
    ].endswith("confirmatory-task-semantics-audit-rc28.json")
    assert registry["mechanism_adaptation"]["gate_a_certificate_status"] == {
        "a1_physical_intervention_validity": "passed",
        "a2_controlled_matched_identifiability": "historical_pass_current_binding_stale",
        "a3_online_attainability": "historical_pass_current_binding_stale",
    }
    assert (
        registry["mechanism_adaptation"]["status"]
        == "historical_gate_a_pass_current_binding_stale"
    )
    assert (
        registry["mechanism_adaptation"]["gate_a_evidence_current"]
        is (
            registry["evidence_dag"]["nodes"][
                "mechanism_public_gate_a_decision"
            ]["artifact_state"]
            == "current"
        )
    )
    assert registry["mechanism_adaptation"]["agent_weight_updates_performed"] is False
    assert registry["mechanism_adaptation"]["agent_pilot_gate_status"] == {
        "gate_0": "passed",
        "gate_b": "descriptive_only_insufficient_pairs",
        "gate_c": "not_evaluated",
        "gate_d": "not_evaluated",
        "gate_e": "pilot_protocol_failure_observed",
    }


def test_current_mechanism_agent_and_legacy_agent_remain_replayable() -> None:
    from chemworld.agents import MechanismDiagnosticLiveLLMAgent
    from chemworld.agents.mechanism_adaptation_live_llm import (
        MechanismAdaptationLiveLLMAgent,
        MechanismCandidateSpec,
    )

    assert MechanismAdaptationLiveLLMAgent.__name__ == "MechanismAdaptationLiveLLMAgent"
    assert MechanismCandidateSpec.__name__ == "MechanismCandidateSpec"
    assert MechanismDiagnosticLiveLLMAgent.__name__ == "MechanismDiagnosticLiveLLMAgent"
