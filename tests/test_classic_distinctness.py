from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.classic_distinctness import (
    audit_classic_distinctness,
    load_classic_distinctness_protocol,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "classic-distinctness-controls.json"
)


def test_classic_roles_have_distinct_executable_policy_identities() -> None:
    report = audit_classic_distinctness(load_classic_distinctness_protocol())

    assert report["controls_ready"] is True
    assert report["parent_task_complete"] is False
    assert report["formal_results_present"] is False
    assert report["formal_classic_matrix_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert len(report["methods"]) == 8
    assert report["checks"]["classes_unique"] is True
    assert report["checks"]["act_implementations_unique"] is True
    assert report["checks"]["semantic_fingerprints_unique"] is True
    assert all(report["method_checks"].values())
    assert all(report["adversarial_probes"].values())


def test_surrogate_roles_are_typed_and_acquisitions_remain_distinct() -> None:
    report = audit_classic_distinctness(load_classic_distinctness_protocol())
    methods = report["methods"]

    surrogate_roles = {
        role: card for role, card in methods.items() if card["surrogate"] is not None
    }
    assert len(surrogate_roles) == 5
    assert all(
        card["recipe_encoding"] == "continuous_plus_material_one_hot"
        for card in surrogate_roles.values()
    )
    assert methods["structured_gp_ei"]["acquisition"] == "expected_improvement"
    assert methods["structured_gp_pi"]["acquisition"] == "probability_improvement"
    assert methods["structured_gp_ucb"]["acquisition"] == "upper_confidence_bound"
    assert methods["structured_rf_ei"]["surrogate"] == "random_forest"
    assert methods["structured_safe_gp_ei"]["constraint"].startswith(
        "upper_confidence_risk_mask"
    )
    assert methods["greedy_local"]["search_policy"] == "task_recipe_local_perturbation"


def test_protocol_tampering_fails_closed() -> None:
    protocol = load_classic_distinctness_protocol()
    tampered = copy.deepcopy(protocol)
    tampered["required_methods"]["structured_gp_pi"]["source_tokens"] = [
        "gp_expected_improvement"
    ]

    report = audit_classic_distinctness(tampered)

    assert report["controls_ready"] is False
    assert report["method_checks"]["structured_gp_pi"] is False


def test_frozen_report_keeps_performance_gate_closed() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))

    assert report["controls_ready"] is True
    assert report["status"] == "controls_ready_formal_matrix_pending"
    assert report["formal_results_present"] is False
    assert report["formal_classic_matrix_ready"] is False
    assert report["parent_task_complete"] is False
