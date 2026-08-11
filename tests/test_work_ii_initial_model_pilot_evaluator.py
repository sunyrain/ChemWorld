from __future__ import annotations

import pytest
from scripts.evaluate_work_ii_initial_model_pilot import (
    _blind_skip_reason,
    _descriptive_interpretation,
    _parametric_controls,
    _rationale_score_match,
    _registered_temperature_direction,
    _render_markdown,
    _scientific_trajectory_complete,
    _supplied_model_distance,
    _temperature_direction_contract,
)


def _cell(
    arm: str,
    *,
    best: float,
    improvement: float,
    reliability: list[float | None],
    challenged: list[list[str]],
) -> dict[str, object]:
    return {
        "prior_arm": arm,
        "best_observed_score": best,
        "effective_pre_error": 0.4,
        "effective_final_error": 0.4 - improvement,
        "checkpoint_improvement": improvement,
        "final_prior_reliability": reliability[-1],
        "prior_reliability_trajectory": reliability,
        "suspected_misindexed_fields_trajectory": challenged,
        "law_summary_error": 0.2,
        "blind_recommendation_gain": 0.0,
        "selected_experiment_index": 2,
        "observed_incumbent_experiment_index": 2,
        "provider_usage": {
            "input_token_count": 100,
            "cached_input_token_count": 80,
            "uncached_input_token_count": 20,
            "output_token_count": 10,
            "session_elapsed_s": 30.0,
            "recovered_mcp_tool_failure_count": 1,
            "provider_error_event_count": 0,
        },
    }


def test_markdown_interpretation_tracks_endpoint_and_prediction_directions() -> None:
    report = {
        "denominators": {
            "participant_cell_count": 3,
            "participant_completed_cell_count": 3,
            "participant_complete_experiment_count": 12,
            "participant_scheduled_experiment_count": 12,
            "participant_checkpoint_count": 12,
            "participant_operation_attempt_count": 74,
            "participant_logical_codex_turn_count": 3,
            "truth_completed_query_count": 4,
            "truth_query_count": 4,
            "truth_exact_replay_count": 4,
            "blind_completed_execution_count": 18,
            "blind_scheduled_execution_count": 18,
        },
        "cluster_contrast": {"H3_primary_contrast": -0.01},
        "cells": [
            _cell(
                "opaque", best=0.58, improvement=0.24, reliability=[None] * 4, challenged=[[]] * 4
            ),
            _cell(
                "aligned_nominal",
                best=0.81,
                improvement=-0.01,
                reliability=[0.7, 0.8],
                challenged=[[]] * 2,
            ),
            _cell(
                "misindexed_nominal",
                best=0.83,
                improvement=-0.02,
                reliability=[0.7, 0.4],
                challenged=[["potential_V"], []],
            ),
        ],
        "report_sha256": "abc",
    }
    report["descriptive_interpretation"] = _descriptive_interpretation(report)

    rendered = _render_markdown(report)

    assert "exceeded the opaque endpoint by 0.2500" in rendered
    assert "Held-out prediction worsened by 0.0200" in rendered
    assert "changed from 0.70 to 0.40" in rendered
    assert "challenged potential_V" in rendered
    assert "remained below the opaque" not in rendered
    assert "300 input tokens (240 cached; 60 uncached)" in rendered


def test_reaction_safety_parametric_controls_and_model_distance() -> None:
    experiment = {
        "operations": [
            {
                "operation": "heat",
                "target_temperature_K": 390.0,
                "duration_s": 1800.0,
            },
            {
                "operation": "heat",
                "target_temperature_K": 420.0,
                "duration_s": 3600.0,
            },
        ]
    }
    model = {
        "model": {
            "claim": {
                "reaction_temperature_K": 420.0,
                "reaction_duration_s": 7200.0,
                "temperature_tolerance_K": 15.0,
                "duration_tolerance_s": 300.0,
            }
        }
    }

    controls = _parametric_controls(experiment, "reaction-safety-constrained")

    assert controls == {
        "heat_stages": [
            {"reaction_temperature_K": 390.0, "reaction_duration_s": 1800.0},
            {"reaction_temperature_K": 420.0, "reaction_duration_s": 3600.0},
        ],
        "reaction_duration_s": 5400.0,
        "reaction_temperature_K": 420.0,
    }
    assert _supplied_model_distance(controls, model) == {
        "reaction_temperature_K": 0.0,
        "reaction_duration_s": 1500.0,
    }

    matched_prior_model = {
        "model": {"claim": {"directional_axis": "reaction_temperature_K"}},
        "context_contract": {
            "approximate_reference_region": {
                "reaction_temperature_K": 420.0,
                "reaction_duration_s": 3300.0,
                "temperature_tolerance_K": 10.0,
                "duration_tolerance_s": 600.0,
            }
        },
    }
    assert _supplied_model_distance(controls, matched_prior_model) == {
        "reaction_temperature_K": 0.0,
        "reaction_duration_s": 1500.0,
    }

    electrochemical_matched_prior = {
        "model": {"claim": {"directional_axis": "controlled_potential_V"}},
        "context_contract": {
            "reference_context": {
                "probe_potential_V": 1.18,
                "probe_current_mA": 70.0,
                "controlled_duration_s": 3540.0,
            }
        },
    }
    assert _supplied_model_distance(
        {"potential_V": 1.05, "current_mA": 75.0, "duration_s": 3600.0},
        electrochemical_matched_prior,
    ) == pytest.approx(
        {
            "controlled_potential_V": 0.13,
            "controlled_current_mA": 5.0,
            "controlled_duration_s": 60.0,
        }
    )


def test_rationale_score_match_detects_one_based_incumbent_reference() -> None:
    experiments = [
        {"experiment_index": 9, "leaderboard_score": 0.4150832466018063},
        {"experiment_index": 10, "leaderboard_score": 0.41915356995221154},
    ]
    recommendation = {
        "selected_experiment_index": 9,
        "selection_rationale": (
            "Experiment index 9 delivered the highest participant-visible score (0.41915); "
            "the repeat scored 0.41508."
        ),
    }

    assert _rationale_score_match(recommendation, experiments) == 10


def test_operational_failure_can_retain_a_complete_scientific_trajectory() -> None:
    summary = {
        "completed": False,
        "analysis": {
            "complete_experiment_count": 4,
            "right_censored_open_experiment": False,
        },
        "exact_replay": {"verified": True},
        "qualification": {
            "passed": False,
            "failed_checks": ["provider_operational_limits_reconciled"],
        },
    }

    assert _scientific_trajectory_complete(summary) is True

    summary["analysis"]["complete_experiment_count"] = 10
    assert _scientific_trajectory_complete(summary, 10) is True


def test_blind_skip_reason_never_invents_missing_recommendation() -> None:
    summary = {
        "completed": False,
        "analysis": {
            "complete_experiment_count": 10,
            "right_censored_open_experiment": False,
            "final_recommendation": None,
        },
        "exact_replay": {"verified": True},
    }

    assert _blind_skip_reason(summary, 10) == "missing_committed_final_recommendation"
    summary["analysis"]["complete_experiment_count"] = 0
    assert _blind_skip_reason(summary, 10) == "participant_trajectory_incomplete"


def test_registered_temperature_direction_uses_frozen_aligned_claim() -> None:
    config = {
        "prior_arms": {
            "aligned_nominal": {
                "initial_world_model": {
                    "model": {
                        "claim": {
                            "expected_relation": (
                                "Relative to the stated reference region, the lower-temperature "
                                "side should retain safe balanced performance more reliably than "
                                "the higher-temperature side."
                            )
                        }
                    }
                }
            }
        }
    }

    registered = _registered_temperature_direction(config)

    assert registered["preferred_side"] == "lower_temperature"
    assert registered["source"].endswith("claim.expected_relation")


def test_query_subset_direction_conflict_disables_binary_recovery_scoring() -> None:
    contract = _temperature_direction_contract(
        {"preferred_side": "lower_temperature"},
        {"preferred_side": "higher_temperature"},
    )

    assert contract["status"] == "query_subset_conflict"
    assert contract["recovery_scoring_authorized"] is False
