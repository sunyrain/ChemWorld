from __future__ import annotations

import runpy
from pathlib import Path

import pytest

from chemworld.eval.mechanism_adaptation_execution import (
    _declared_relational_action_groups,
    _validate_paired_public_contrast_encoding,
    build_action_library,
    load_json_object,
    load_protocol_object,
)
from chemworld.eval.mechanism_design_audit import relational_coverage_witness
from chemworld.eval.mechanism_release import (
    build_metric_embargo_receipt,
    build_public_gate_a_decision,
    derive_readiness,
    gate_a_go_no_go,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, object]:
    return {
        "schema_version": "chemworld-confirmatory-trial-manifest-0.1",
        "expected_count": 2,
        "completed_count": 2,
        "missing_trial_key_sha256": [],
        "unexpected_trial_key_sha256": [],
        "duplicate_count": 0,
        "invalid_receipts": [],
        "complete": True,
    }


def test_metric_embargo_receipt_discloses_only_structure() -> None:
    report = {
        "schema_version": "science-report",
        "protocol_sha256": "p",
        "gate_a_plan_sha256": "g",
        "trial_manifests": {"task": _manifest()},
        "secret_scientific_metric": 0.91,
    }
    receipt = build_metric_embargo_receipt(
        report,
        stage="a3",
        expected_trial_count=2,
    )
    assert receipt["structurally_complete"] is True
    assert receipt["scientific_metrics_disclosed"] is False
    assert "secret_scientific_metric" not in receipt


def test_formal_receipt_counts_match_frozen_job_matrices() -> None:
    runner = runpy.run_path(
        ROOT / "scripts" / "run_mechanism_adaptation.py",
        run_name="mechanism_adaptation_runner",
    )
    protocol = load_protocol_object(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
    )
    plan = load_json_object(
        ROOT
        / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json"
    )

    assert runner["_expected_a3_receipt_count"](protocol, plan) == 2016
    assert runner["_expected_a2_receipt_count"](protocol, plan) == 4896


def test_release_qualification_source_binding_tracks_selected_candidate() -> None:
    runner = runpy.run_path(
        ROOT / "scripts" / "qualify_mechanism_adaptation_release.py",
        run_name="mechanism_release_qualification",
    )
    protocol_path = ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc29.json"
    plan_path = (
        ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc29.json"
    )
    semantics_path = (
        ROOT
        / "workstreams/flagship_tasks/reports/confirmatory-task-semantics-audit-rc29.json"
    )
    plan = load_json_object(plan_path)

    command = runner["_source_binding_command"](
        "source-commit",
        protocol_path=protocol_path,
        plan_path=plan_path,
        plan=plan,
        semantics_path=semantics_path,
    )

    assert runner["_release_candidate"](plan) == "rc29"
    assert "configs/benchmark/mechanism_adaptation_v0.3.0_rc29.json" in command
    assert "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc29.json" in command
    assert (
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc29.json"
    ) in command
    assert (
        "workstreams/flagship_tasks/reports/confirmatory-task-semantics-audit-rc29.json"
    ) in command


def test_formal_paired_contrast_encoding_is_accepted() -> None:
    plan = load_json_object(
        ROOT
        / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json"
    )

    _validate_paired_public_contrast_encoding(plan["paired_phase_design"])


def test_primary_budget_covers_every_declared_relation_before_scheduling() -> None:
    protocol = load_protocol_object(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
    )
    plan = load_json_object(
        ROOT
        / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json"
    )
    expected_minimum = {
        "reaction-to-crystallization": 4,
        "electrochemical-conversion": 5,
    }
    for task_id, minimum in expected_minimum.items():
        action_library = build_action_library(
            task_id,
            action_count=plan["action_library"]["action_count_per_task"],
            seed=plan["action_library"]["design_seed"],
            design_id=plan["action_library"]["design"],
        )
        declarations = _declared_relational_action_groups(
            task_id=task_id,
            contract=protocol["task_mechanism_contracts"][task_id],
            action_library=action_library,
        )
        witness = relational_coverage_witness(
            declaration_groups=declarations,
            action_ids=list(action_library),
            budget=plan["held_out_certificate"]["primary_gate_budget"],
        )
        assert witness["minimum_distinct_actions"] == minimum
        assert witness["feasible"] is True

    impossible_electrochemical_budget = relational_coverage_witness(
        declaration_groups=declarations,
        action_ids=list(action_library),
        budget=4,
    )
    assert impossible_electrochemical_budget["minimum_distinct_actions"] == 5
    assert impossible_electrochemical_budget["feasible"] is False


def test_public_decision_requires_both_complete_receipts() -> None:
    report = {
        "trial_manifests": {"task": _manifest()},
        "certificate_decision": {
            "a1_physical_intervention_validity_pass": True,
            "a2_controlled_matched_identifiability_pass": True,
            "a3_online_attainability_pass": False,
            "gate_a_pass": False,
        },
    }
    a3_report = {"trial_manifests": {"task": _manifest()}}
    a2 = build_metric_embargo_receipt(
        report,
        stage="a2",
        expected_trial_count=2,
    )
    a3 = build_metric_embargo_receipt(
        a3_report,
        stage="a3",
        expected_trial_count=2,
    )
    decision = build_public_gate_a_decision(
        report,
        a3_report=a3_report,
        a2_structural_receipt=a2,
        a3_structural_receipt=a3,
        release_qualification={"qualified": True},
    )
    assert decision["go_no_go"]["branch"] == "a2_pass_a3_failed"
    assert decision["readiness"]["benchmark_ready"] is False

    invalid = dict(a3)
    invalid["structurally_complete"] = False
    with pytest.raises(ValueError, match="A3 structural receipt"):
        build_public_gate_a_decision(
            report,
            a3_report=a3_report,
            a2_structural_receipt=a2,
            a3_structural_receipt=invalid,
            release_qualification={"qualified": True},
        )


def test_readiness_is_independent_of_participant_performance() -> None:
    readiness = derive_readiness(
        a1_pass=True,
        a2_pass=True,
        a3_pass=True,
        runner_validated=True,
        statistics_validated=True,
        replay_validated=True,
        gates_b_to_e_executed=True,
        public_results_frozen=True,
        private_e_reported=True,
        private_a_reported=True,
        claims_match_results=True,
        participant_performance_pass=False,
    )
    assert readiness["publication_ready"] is True
    assert readiness["participant_performance_pass"] is False
    assert gate_a_go_no_go(a2_pass=False, a3_pass=False)["gate_e"] == (
        "autonomy_only"
    )
