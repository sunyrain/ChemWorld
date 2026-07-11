from __future__ import annotations

import copy

import pytest
from scripts.audit_vnext_primary import (
    _build_summary,
    _expected_result_keys,
    _validate_result_contract,
)

from chemworld.eval.confirmatory_freeze import load_confirmatory_freeze


def test_expected_primary_matrix_is_exactly_core_four_by_two_by_twenty() -> None:
    keys = _expected_result_keys(load_confirmatory_freeze())
    assert len(keys) == 160
    assert {task_id for task_id, _, _ in keys} == set(
        load_confirmatory_freeze()["task_roles"]["core"]
    )
    assert {method_id for _, method_id, _ in keys} == {"structured_gp_bo", "random"}
    assert {seed for _, _, seed in keys} == set(range(300, 320))


def test_result_contract_rejects_unbound_risk_policy() -> None:
    protocol = load_confirmatory_freeze()
    manifest = {
        "evaluated_source_commit": "a" * 40,
        "confirmatory_protocol_sha256": "b" * 64,
    }
    result = {
        "task_id": "partition-discovery",
        "baseline_agent": "random",
        "seed": 300,
        "result_schema_version": "chemworld-evaluation-result-0.3",
        "verified": True,
        "evaluation_policy": "vnext_risk_cost",
        "confirmatory_protocol_id": protocol["protocol_id"],
        "confirmatory_protocol_sha256": "b" * 64,
        "evaluated_source_commit": "a" * 40,
        "evaluation_source_tree_dirty": False,
        "resource_usage": {
            "complete_experiment_count": 40,
            "method_ledger": {"accounting_complete": True},
        },
        "score_replay": {
            "task_evaluation_contract": {
                "risk_limit_semantics": "benchmark_operational_risk_budget"
            }
        },
    }
    _validate_result_contract(result, manifest=manifest, protocol=protocol)
    unbound = copy.deepcopy(result)
    unbound["score_replay"]["task_evaluation_contract"]["risk_limit_semantics"] = "legacy"
    with pytest.raises(ValueError, match="operational-risk semantics"):
        _validate_result_contract(unbound, manifest=manifest, protocol=protocol)


def test_summary_preserves_nonclaiming_boundary() -> None:
    decision = {
        "objective_rule_passed": True,
        "complete_joint_rule_passed": False,
        "primary_metric": "product_in_organic",
        "sesoi": 0.02,
    }
    result = {
        "task_id": "partition-discovery",
        "baseline_agent": "random",
        "mean_product_in_organic": 0.4,
        "score_replay": {
            "layered_evaluation": {
                "constraints": {"risk_budget_exceedance_count": 1},
                "resources": {
                    "complete_experiment_count": 40,
                    "operation_count": 400,
                    "campaign_total_cost": 10.0,
                },
            }
        },
    }
    summary = _build_summary(
        manifest={
            "schema_version": "chemworld-vnext-primary-run-0.2",
            "generated_at": "2026-07-11T00:00:00+00:00",
            "evaluated_source_commit": "a" * 40,
            "confirmatory_protocol_id": "chemworld-vnext-confirmatory-freeze-0.3",
            "confirmatory_protocol_sha256": "b" * 64,
            "primary_results_sha256": "c" * 64,
            "primary_statistics_sha256": "d" * 64,
        },
        results=[result, {**result, "baseline_agent": "structured_gp_bo"}],
        recorded_statistics={
            "task_decisions": {"partition-discovery": decision},
            "all_task_objective_rule_passed": True,
            "all_task_constraint_rule_passed": False,
            "all_task_joint_rule_passed": False,
        },
        replay=True,
        distinct_trajectory_count=2,
    )
    assert summary["claim_boundary"]["objective_only_slice_supported"] is True
    assert summary["claim_boundary"]["constraint_complete_slice_supported"] is False
    assert summary["claim_boundary"]["primary_classical_slice_supported"] is False
    assert summary["comparison"]["complete_primary_rule_passed"] is False
    assert summary["claim_boundary"]["benchmark_claim_allowed"] is False
    assert summary["claim_boundary"]["publication_ready"] is False
    assert summary["comparison"]["cross_task_performance_score"] is None
