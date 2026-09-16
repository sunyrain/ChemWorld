from copy import deepcopy

import gymnasium as gym
import pytest

from chemworld.agent_interface import tool_json_view
from chemworld.agents.interactive_codex_experiment import _public_task_contract
from chemworld.research_brief import TASKS, VERSION, normalize_research_brief
from chemworld.world.scoring import (
    PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
    TASK_DERIVED_SCORING_CONTRACT,
)


def test_pa_evaluator_captures_assay_before_campaign_reset():
    from scripts.run_work_ii_gate_repair import EvaluatorCapture, recipes

    records = []
    env = EvaluatorCapture(
        gym.make(
            "ChemWorld",
            task_id=TASKS["PA"],
            scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
            research_brief={"schema_version": VERSION, "card": "PA", "prior_record": None},
            episode_mode_override="campaign",
            budget_override=48,
        ),
        records,
    )
    try:
        env.reset(seed=0)
        for batch in recipes("PA")[:2]:
            for action in batch:
                _, _, _, _, info = env.step(action)
                assert info["transaction_status"] == "committed"
        assert len(records) == 2
        for record in records:
            assert record["initial_target_mol"] > 0
            assert record["expected_sample_target_mol"] > 0
            assert record["before_error_mol"] <= 1e-8
            assert record["after_plus_sample_error_mol"] <= 1e-8
        assert "initial_target_mol" not in env.unwrapped.task_info()
    finally:
        env.close()


@pytest.mark.parametrize("code", TASKS)
def test_research_commission_reaches_real_public_and_provider_contract(code):
    brief = {"schema_version": VERSION, "card": code, "prior_record": None}
    scoring = (
        PARTITION_S0_EXTRACTION_EFFICIENCY_V3 if code == "PA" else TASK_DERIVED_SCORING_CONTRACT
    )
    env = gym.make(
        "ChemWorld", task_id=TASKS[code], research_brief=brief, scoring_contract_id=scoring
    )
    try:
        observation, info = env.reset(seed=0)
        task = env.unwrapped.task_info()
        packet = task["research_brief"]
        view = tool_json_view(env, observation, info)
        assert packet == view["research_brief"]
        assert _public_task_contract(task)["research_brief"] == packet
        assert packet["prior_record"] is None
        assert task["description"] == packet["commission"]
        telemetry = view["operational_state"]
        assert 250 < telemetry["temperature_K"] < 400
        assert telemetry["measurement_scope"] == "no_new_measurement"
        assert set(telemetry) == {
            "schema_version",
            "temperature_K",
            "pressure_Pa",
            "active_volume_L",
            "process_time_s",
            "state_scope",
            "measurement_scope",
            "phases",
            "flow",
            "geometry",
        }
    finally:
        env.close()


def test_pa_research_rejects_moving_denominator_contract():
    with pytest.raises(ValueError, match="fixed-initial-target"):
        normalize_research_brief(
            {"schema_version": VERSION, "card": "PA", "prior_record": None},
            task_id=TASKS["PA"],
            scoring_contract_id=TASK_DERIVED_SCORING_CONTRACT,
        )


def test_prior_keeps_scoped_claim_without_condition_identity_or_shared_mutability():
    prior = {
        "scope_actions": [{"operation": "wait", "duration_s": 30}],
        "metric": "yield",
        "estimate": 0.4,
        "half_width": 0.03,
    }
    payload = {"schema_version": VERSION, "card": "RX", "prior_record": prior}
    result = normalize_research_brief(
        payload, task_id=TASKS["RX"], scoring_contract_id=TASK_DERIVED_SCORING_CONTRACT
    )
    prior["scope_actions"][0]["duration_s"] = 100
    assert result["prior_record"]["scope_actions"][0]["duration_s"] == 30
    bad = deepcopy(payload)
    bad["prior_record"]["arm"] = "M"
    with pytest.raises(ValueError, match="without arm labels"):
        normalize_research_brief(
            bad, task_id=TASKS["RX"], scoring_contract_id=TASK_DERIVED_SCORING_CONTRACT
        )


def test_legacy_default_does_not_gain_task_or_sensor_information():
    env = gym.make("ChemWorld", task_id=TASKS["RX"])
    try:
        obs, info = env.reset(seed=0)
        assert "research_brief" not in env.unwrapped.task_info()
        view = tool_json_view(env, obs, info)
        assert "research_brief" not in view and "operational_state" not in view
    finally:
        env.close()


def test_completed_batch_telemetry_does_not_relabel_old_assay_as_new_batch():
    env = gym.make(
        "ChemWorld",
        task_id=TASKS["EQ"],
        research_brief={"schema_version": VERSION, "card": "EQ", "prior_record": None},
    )
    try:
        obs, _ = env.reset(seed=0)
        view = tool_json_view(
            env,
            obs,
            {
                "operation_type": "measure",
                "instrument": "final_assay",
                "transaction_status": "committed",
                "experiment_ended": True,
                "next_experiment_ready": True,
            },
        )
        assert view["operational_state"]["state_scope"] == "next_batch_initial_state"
        assert view["operational_state"]["measurement_scope"] == "just_closed_batch"
    finally:
        env.close()
