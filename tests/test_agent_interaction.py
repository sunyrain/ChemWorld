from __future__ import annotations

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.agents.interaction import build_decision_context


def _public_view(*operations: str) -> dict:
    return {
        "tool_json": {
            "available_actions": [
                {"operation": operation, "valid": True} for operation in operations
            ],
            "lab_report": {"visible_metrics": {}, "spectra_summary": {}},
        }
    }


@pytest.mark.parametrize("previous_event", ["operation_result", "measurement_result"])
def test_measure_only_affordance_is_persistently_labeled_closeout(
    previous_event: str,
) -> None:
    context = build_decision_context(
        step=8,
        task_info={"task_id": "reaction-to-crystallization"},
        campaign_state={"remaining_budget": 12},
        public_view=_public_view("measure"),
        previous_event_type=previous_event,
    )

    assert context.available_operations == ("measure",)
    assert context.decision_stage == "experiment_closeout"


def test_measurement_before_termination_remains_an_evidence_update() -> None:
    context = build_decision_context(
        step=5,
        task_info={"task_id": "reaction-to-crystallization"},
        campaign_state={"remaining_budget": 15},
        public_view=_public_view("measure", "terminate"),
        previous_event_type="measurement_result",
    )

    assert context.decision_stage == "evidence_update"


def test_new_experiment_setup_takes_priority_over_affordance_shape() -> None:
    context = build_decision_context(
        step=9,
        task_info={"task_id": "reaction-to-crystallization"},
        campaign_state={"remaining_budget": 11},
        public_view=_public_view("measure"),
        previous_event_type="experiment_end",
    )

    assert context.decision_stage == "experiment_setup"


def test_real_environment_reports_closeout_after_termination() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        observation, _ = env.reset(seed=0)
        observation, _, _, _, info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 0}
        )
        observation, _, _, _, info = env.step(
            {"operation": "add_reagent", "amount_mol": 0.01}
        )
        observation, _, _, _, info = env.step({"operation": "terminate"})
        public_view = agent_view_bundle(env, observation, info)

        context = build_decision_context(
            step=4,
            task_info={"task_id": "reaction-to-crystallization"},
            campaign_state=env.unwrapped.campaign_state(),
            public_view=public_view,
            previous_event_type="operation_result",
        )

        assert context.available_operations == ("measure",)
        assert context.decision_stage == "experiment_closeout"

        observation, _, _, _, info = env.step(
            {"operation": "measure", "instrument": "gc"}
        )
        public_view = agent_view_bundle(env, observation, info)
        after_intermediate_measurement = build_decision_context(
            step=5,
            task_info={"task_id": "reaction-to-crystallization"},
            campaign_state=env.unwrapped.campaign_state(),
            public_view=public_view,
            previous_event_type="measurement_result",
        )

        assert after_intermediate_measurement.available_operations == ("measure",)
        assert after_intermediate_measurement.decision_stage == "experiment_closeout"
    finally:
        env.close()
