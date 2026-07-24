from __future__ import annotations

import runpy
from pathlib import Path

import pytest

from chemworld.eval.mechanism_adaptation_execution import (
    load_json_object,
    load_protocol_object,
)
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
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc26.json"
    )
    plan = load_json_object(
        ROOT
        / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc26.json"
    )

    assert runner["_expected_a3_receipt_count"](protocol, plan) == 2016
    assert runner["_expected_a2_receipt_count"](protocol, plan) == 3456


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
