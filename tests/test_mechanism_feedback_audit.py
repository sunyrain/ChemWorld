from __future__ import annotations

from typing import Any

import pytest

from chemworld.eval.mechanism_feedback_audit import build_local_feedback_case


def _record(
    *,
    step: int,
    action: dict[str, Any],
    score: float,
    complete_count: int,
    experiment_index: int,
    ended: bool = False,
) -> dict[str, Any]:
    instrument = action.get("instrument")
    decision = {
        "status": "model_decision",
        "action": action,
        "evidence": ["public evidence"],
        "spectrum_interpretation": "public packet",
        "hypothesis": "test",
        "uncertainty": 0.5,
        "rationale": "audit",
        "request_historical_spectrum_id": None,
        "adaptation_source": "measurement",
        "mechanism_distribution": {"no_change": 0.5, "rate_law_family": 0.5},
        "declared_information_value": 0.4,
    }
    context = {
        "step": step,
        "task_id": "reaction-to-crystallization",
        "decision_stage": "evidence_update" if step > 1 else "experiment_setup",
        "campaign_state": {
            "remaining_budget": 20 - step,
            "experiment_index": experiment_index,
            "final_assay_count": complete_count,
            "operation_count": step - 1,
        },
        "visible_metrics": {"marker": score - 0.1},
        "latest_spectra": {
            "has_spectral_packet": instrument == "hplc",
            "marker": score - 0.1,
        },
        "uncertainty": {"marker": 0.1},
        "constraint_flags": {},
        "available_operations": ["measure", "terminate"],
        "previous_event_type": "measurement_result" if step > 1 else None,
        "historical_spectrum_catalog": [],
        "requested_historical_spectrum": {},
    }
    return {
        "step": step,
        "action": action,
        "agent_trace": [decision],
        "explanation": {
            "decision_context": context,
            "outcome": {
                "event_type": "experiment_end" if ended else "measurement_result"
            },
        },
        "agent_view": {
            "tool_json": {
                "observation": {"marker": score},
                "lab_report": {
                    "visible_metrics": {"marker": score},
                    "spectra_summary": {
                        "has_spectral_packet": instrument == "hplc",
                        "marker": score,
                    },
                },
            }
        },
        "agent_visible_observation": {"marker": score},
        "observed_reward": score,
        "observed_keys": ["marker"],
        "observed_mask": {"marker": True},
        "constraint_flags": {},
        "leaderboard_score": score if ended else None,
        "measurement_cost": 0.01,
        "operation_type": "measure",
        "transaction_status": "committed",
        "method_resources": {
            "complete_experiment_count": complete_count,
            "limits": {
                "operation_limit": 20,
                "complete_experiment_limit": 3,
                "checkpoint_complete_experiments": [1, 2, 3],
            },
        },
        "agent_metadata": {"diagnostic_per_experiment_action_limit": 8},
        "experiment_index": experiment_index,
    }


def test_local_feedback_case_branches_only_the_last_feedback_packet() -> None:
    iid = [
        _record(
            step=1,
            action={"operation": "measure", "instrument": "hplc"},
            score=0.2,
            complete_count=0,
            experiment_index=0,
        ),
        _record(
            step=2,
            action={"operation": "measure", "instrument": "final_assay"},
            score=0.3,
            complete_count=1,
            experiment_index=0,
            ended=True,
        ),
    ]
    shifted = [
        _record(
            step=1,
            action={"operation": "measure", "instrument": "hplc"},
            score=0.6,
            complete_count=0,
            experiment_index=0,
        ),
        _record(
            step=2,
            action={"operation": "measure", "instrument": "final_assay"},
            score=0.7,
            complete_count=1,
            experiment_index=0,
            ended=True,
        ),
        _record(
            step=3,
            action={"operation": "measure", "instrument": "hplc"},
            score=0.9,
            complete_count=1,
            experiment_index=1,
        ),
        _record(
            step=4,
            action={"operation": "terminate"},
            score=0.8,
            complete_count=1,
            experiment_index=1,
        ),
    ]

    case = build_local_feedback_case(
        iid,
        shifted,
        critical_instrument="hplc",
        target_shifted_experiment=2,
    )

    assert case["target"]["shifted_record_index"] == 2
    assert len(case["pre_feedback_prefix_sha256"]) == 64
    branches = case["branches"]
    assert branches["true_feedback"]["decision_context"].visible_metrics["marker"] == (
        pytest.approx(0.7)
    )
    assert branches["permuted_feedback"]["decision_context"].visible_metrics[
        "marker"
    ] == pytest.approx(0.2)
    assert branches["delayed_feedback"]["decision_context"].visible_metrics[
        "marker"
    ] == pytest.approx(0.6)
    assert branches["critical_measurement_deleted"][
        "decision_context"
    ].visible_metrics == {}
    outcomes = {
        condition: branch["prompt_memory"]["recent_decisions"][-1]["outcome"][
            "observation"
        ]["marker"]
        if branch["prompt_memory"]["recent_decisions"][-1]["outcome"][
            "observation"
        ]
        else None
        for condition, branch in branches.items()
    }
    assert outcomes == {
        "true_feedback": 0.9,
        "permuted_feedback": 0.2,
        "delayed_feedback": 0.6,
        "critical_measurement_deleted": None,
    }
