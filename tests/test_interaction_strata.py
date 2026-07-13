from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.interaction_strata import (
    InteractionStrataError,
    audit_interaction_strata,
    classify_comparison,
    load_interaction_strata_protocol,
    validate_method_declaration,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "interaction-strata-v0.4.json"


def test_frozen_tracks_have_complete_distinct_method_scopes() -> None:
    protocol = load_interaction_strata_protocol()
    report = audit_interaction_strata(protocol)
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["track_summary"]["recipe_level"]["method_count"] == 8
    assert report["track_summary"]["operation_level"]["method_count"] == 7
    assert set(report["track_summary"]["recipe_level"]["methods"]).isdisjoint(
        report["track_summary"]["operation_level"]["methods"]
    )
    assert not report["registration_failures"]
    assert all(report["controls"].values())


def test_each_method_requires_every_capability_and_assistance_field() -> None:
    protocol = load_interaction_strata_protocol()
    payload = copy.deepcopy(protocol["methods"]["live_llm_a"])
    del payload["harness_assistance"]
    with pytest.raises(InteractionStrataError, match="harness_assistance"):
        validate_method_declaration("live_llm_a", payload, protocol=protocol)


def test_recipe_method_cannot_claim_operation_or_spectrum_capabilities() -> None:
    protocol = load_interaction_strata_protocol()
    payload = copy.deepcopy(protocol["methods"]["random"])
    payload["adapts_within_experiment"] = True
    with pytest.raises(InteractionStrataError, match="cannot adapt"):
        validate_method_declaration("random", payload, protocol=protocol)
    payload = copy.deepcopy(protocol["methods"]["random"])
    payload["decision_scope"] = "operation"
    with pytest.raises(InteractionStrataError, match="decision scope"):
        validate_method_declaration("random", payload, protocol=protocol)


def test_spectrum_capability_requires_all_paired_conditions() -> None:
    protocol = load_interaction_strata_protocol()
    payload = copy.deepcopy(protocol["methods"]["live_llm_a"])
    payload["spectrum_conditions"] = ["assigned"]
    with pytest.raises(InteractionStrataError, match="assigned/unassigned/masked"):
        validate_method_declaration("live_llm_a", payload, protocol=protocol)


def test_hidden_or_private_observation_set_is_rejected() -> None:
    protocol = copy.deepcopy(load_interaction_strata_protocol())
    protocol["public_observation_sets"]["bad"] = ["hidden_world_state"]
    payload = copy.deepcopy(protocol["methods"]["rule_based"])
    payload["public_observation_set"] = "bad"
    with pytest.raises(InteractionStrataError, match="public boundary"):
        validate_method_declaration("rule_based", payload, protocol=protocol)


def test_comparison_classification_prevents_cross_track_algorithm_claims() -> None:
    protocol = load_interaction_strata_protocol()
    declarations = {
        method_id: validate_method_declaration(method_id, payload, protocol=protocol)
        for method_id, payload in protocol["methods"].items()
    }
    assert (
        classify_comparison(
            declarations["random"],
            declarations["structured_gp_ei"],
            protocol=protocol,
        )
        == "algorithm_level_with_adaptation_strategy_as_a_method_property"
    )
    assert (
        classify_comparison(
            declarations["live_llm_a"], declarations["live_llm_b"], protocol=protocol
        )
        == "algorithm_level_when_prompt_and_model_roles_are_frozen"
    )
    assert (
        classify_comparison(declarations["random"], declarations["live_llm_a"], protocol=protocol)
        == "cross_track_system_level_descriptive"
    )


@pytest.mark.parametrize(
    ("mutator", "control"),
    [
        (
            lambda payload: payload["comparison_policy"].update(
                {"single_combined_ranking": "allowed"}
            ),
            "cross_track_claims_are_restricted",
        ),
        (
            lambda payload: payload["shared_evaluation_budget"].update(
                {"complete_experiments_per_cell": 20}
            ),
            "experiment_budget_and_checkpoints_match_parent",
        ),
        (
            lambda payload: payload["parallel_resource_ledger"].update(
                {"resource_axes_are_not_scalarized": False}
            ),
            "parallel_resource_axes_are_complete_and_not_scalarized",
        ),
        (
            lambda payload: payload["parent_formal_protocol"].update(
                {"protocol_sha256": "a" * 64}
            ),
            "parent_formal_protocol_is_exact_and_ready",
        ),
    ],
)
def test_protocol_drift_fails_closed(mutator: Any, control: str) -> None:
    protocol = copy.deepcopy(load_interaction_strata_protocol())
    mutator(protocol)
    report = audit_interaction_strata(protocol)
    assert report["controls_ready"] is False
    assert report["controls"][control] is False


def test_declared_method_drift_fails_registration_and_audit() -> None:
    protocol = copy.deepcopy(load_interaction_strata_protocol())
    del protocol["methods"]["ppo"]["resource_profile"]
    report = audit_interaction_strata(protocol)
    assert report["controls_ready"] is False
    assert report["controls"]["every_method_has_a_valid_complete_declaration"] is False
    assert "resource_profile" in report["registration_failures"]["ppo"]


def test_checked_in_report_is_ready_nonclaiming_and_discloses_assistance() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["capability_matrix"]["random"]["harness_assistance"] == [
        "typed_recipe_to_operation_compiler"
    ]
    assert report["capability_matrix"]["live_llm_a"]["harness_assistance"] == [
        "public_action_schema",
        "json_validation_without_action_repair",
    ]
    assert len(report["resource_axes"]) == 15
