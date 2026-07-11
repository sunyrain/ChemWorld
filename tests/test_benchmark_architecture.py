from __future__ import annotations

from copy import deepcopy

from chemworld.eval.architecture_audit import (
    audit_benchmark_architecture,
    load_architecture_protocol,
)


def test_architecture_graph_separates_controls_from_formal_evidence() -> None:
    report = audit_benchmark_architecture(load_architecture_protocol())
    assert report["architecture_consistent"] is True
    assert report["controls_ready"] is True
    assert report["formal_evidence_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert report["status"] == "controls_ready_formal_evidence_missing"
    assert all(report["cross_contracts"].values())
    assert {item["issue_id"] for item in report["active_issues"]} == {
        "inactive_operational_risk_constraint",
        "live_llm_matrix_missing",
        "mechanism_adaptation_missing",
        "no_formal_spectral_policy",
        "no_formal_within_experiment_adaptation",
        "private_generalization_missing",
        "reference_regret_search_missing",
        "rl_training_matrix_missing",
    }
    assert {item["component"] for item in report["critical_path"]} == set(
        report["formal_evidence_components"]
    )


def test_architecture_graph_fails_closed_on_missing_component() -> None:
    protocol = deepcopy(load_architecture_protocol())
    protocol["control_components"]["task_validity"]["report"] = "missing.json"
    report = audit_benchmark_architecture(protocol)
    assert report["architecture_consistent"] is False
    assert report["controls_ready"] is False
    assert report["publication_ready"] is False
    assert report["control_components"]["task_validity"]["report_exists"] is False


def test_architecture_protocol_uses_conjunctive_release_rule() -> None:
    protocol = load_architecture_protocol()
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["publication_ready"] is False
    assert "every control" in protocol["release_rule"]
    assert "no weighted aggregate" in protocol["release_rule"]
