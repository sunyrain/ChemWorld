from __future__ import annotations

import json

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agent_interface import rl_observation_spec
from chemworld.agents.llm import LLMReplayAgent, ToolUsingLLMStubAgent
from chemworld.data.datasets import flatten_record
from chemworld.data.logging import load_jsonl
from chemworld.envs.spaces import OBSERVATION_KEYS
from chemworld.eval.runner import run_agent
from chemworld.foundation.public_leakage import audit_public_payload
from chemworld.wrappers import (
    ActionSuggestionWrapper,
    AgentInfoWrapper,
    LLMObservationWrapper,
    RLObservationWrapper,
)


def test_env_exposes_agent_facing_methods() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        env.reset(seed=0)
        prompt = env.unwrapped.task_prompt()
        assert prompt["task_id"] == "reaction-to-purification"
        assert "budget" in prompt["text"].lower()
        assert "final_assay" in prompt["text"]
        assert "hplc" in prompt["allowed_instruments"]
        assert "purity" in prompt["success_metrics"]

        actions = env.unwrapped.available_actions()
        operations = {entry["operation"] for entry in actions}
        assert "add_solvent" in operations
        assert "heat" not in operations

        heat_schema = env.unwrapped.action_schema("heat")
        assert heat_schema["fields"]
        assert "target_temperature_K" in heat_schema["required_fields"]
        temperature_field = {
            field["field"]: field for field in heat_schema["fields"]
        }["target_temperature_K"]
        assert temperature_field["unit"] == "K"
        assert temperature_field["bounds"]["low"] == 250.0

        before = env.unwrapped.campaign_state()
        validation = env.unwrapped.validate_action({"operation": "heat", "duration_s": 1.0})
        after = env.unwrapped.campaign_state()
        assert not validation["valid"]
        assert before == after
    finally:
        env.close()


def test_pre_release_task_prompts_are_structured_and_public() -> None:
    expectations = {
        "reaction-to-assay": {
            "must_include": [
                "single-experiment",
                "final_assay_score",
                "trajectory_validity",
                "Terminate",
            ],
            "metrics": {"final_assay_score", "trajectory_validity"},
        },
        "reaction-to-purification": {
            "must_include": [
                "purity",
                "recovery",
                "process_mass_balance_error",
                "phase separation",
                "final_assay",
            ],
            "metrics": {"score", "purity", "recovery", "process_mass_balance_error"},
        },
        "partition-discovery": {
            "must_include": [
                "Campaign task",
                "partition",
                "phase_ratio",
                "product_in_organic",
                "product_in_aqueous",
            ],
            "metrics": {"phase_ratio", "product_in_organic", "product_in_aqueous"},
        },
    }
    for task_id, expected in expectations.items():
        env = gym.make("ChemWorld", task_id=task_id, seed=0)
        try:
            env.reset(seed=0)
            prompt = env.unwrapped.task_prompt()
            text = prompt["text"]
            assert prompt["prompt_version"] == "chemworld-agent-task-prompt-0.2"
            assert prompt["task_id"] == task_id
            assert str(prompt["budget"]) in text
            assert "budget" in text
            assert "Hidden information policy" in text
            assert "Allowed tools" in text
            assert "Success criteria" in text
            assert "Submission requirements" in text
            assert prompt["task_goal"]
            assert prompt["constraints"]
            assert prompt["success_criteria"]
            assert prompt["measurement_policy"]
            assert prompt["recommended_strategy"]
            assert prompt["failure_modes"]
            assert prompt["hidden_information_policy"]
            assert prompt["allowed_tools"]["operations"] == prompt["allowed_operations"]
            assert prompt["allowed_tools"]["instruments"] == prompt["allowed_instruments"]
            assert set(prompt["success_metrics"]) == expected["metrics"]
            lower_text = text.lower()
            for phrase in expected["must_include"]:
                assert phrase.lower() in lower_text
            hidden_species = set(env.unwrapped.scenario_instance.compiled_mechanism.species_index)
            assert not audit_public_payload(prompt, hidden_species_ids=hidden_species)
        finally:
            env.close()


def test_observation_views_are_json_safe_and_public() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        for action in (
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 382.0,
                "duration_s": 1350.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
        ):
            env.step(action)

        rl_view = env.unwrapped.observation_view("rl")
        assert rl_view["schema_version"] == "chemworld-rl-view-0.2"
        assert rl_view["nan_safe"]
        assert rl_view["missing_value"] == -1.0
        assert len(rl_view["vector"]) == len(rl_view["mask"])
        assert len(rl_view["bounds"]["low"]) == len(rl_view["vector"])
        assert len(rl_view["bounds"]["high"]) == len(rl_view["vector"])
        assert all(np.isfinite(float(value)) for value in rl_view["vector"])
        for value, observed in zip(rl_view["vector"], rl_view["mask"], strict=True):
            if observed == 0.0:
                assert value == rl_view["missing_value"]
        assert rl_view["keys"] == [*OBSERVATION_KEYS, "cost_signal"]
        assert rl_view["cost"] >= 0.0

        tool_view = env.unwrapped.observation_view("tool_json")
        json.dumps(tool_view, sort_keys=True)
        hidden_species = set(env.unwrapped.scenario_instance.compiled_mechanism.species_index)
        species_ids = _nested_values_for_key(tool_view["raw_signal"], "species_id")
        assert species_ids.isdisjoint(hidden_species)

        lab_report = env.unwrapped.observation_view("lab_report")
        assert "Visible score" in lab_report["text"]
        assert "Key public metrics" in lab_report["text"]
        assert "Campaign progress" in lab_report["text"]
        assert "Spectra packet" in lab_report["text"]
        assert lab_report["report_version"] == "chemworld-lab-report-0.2"
        assert "spectra_summary" in lab_report
        assert lab_report["spectra_summary"]["has_spectral_packet"]
        assert lab_report["spectra_summary"]["peak_table_count"] >= 1
        assert lab_report["instrument_summary"]["instrument"] == "hplc"
        assert lab_report["instrument_summary"]["is_measurement"]
        assert "score" in lab_report["visible_metrics"]
        assert lab_report["campaign_progress"]["remaining_budget"] >= 0
    finally:
        env.close()


def test_lab_report_includes_failed_action_recovery() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        env.step({"operation": "heat", "duration_s": 100.0})
        report = env.unwrapped.observation_view("lab_report")
        assert report["status"] == "failed_precondition"
        assert report["recovery_suggestion"]
        assert report["failure_summary"]["precondition_failed"]
        assert report["failure_summary"]["failed_preconditions"]
        assert report["next_action_hints"]
        assert "Recovery suggestion" in report["text"]
    finally:
        env.close()


def test_agent_wrappers_preserve_gym_shape_and_add_views() -> None:
    info_env = AgentInfoWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        _, info = info_env.reset(seed=0)
        assert "task_prompt" in info
        assert "campaign_state" in info
        assert "available_actions" in info
        result = info_env.step({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1})
        assert len(result) == 5
    finally:
        info_env.close()

    llm_env = LLMObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        _, info = llm_env.reset(seed=0)
        assert "lab_report" in info
        _, _, _, _, info = llm_env.step({"operation": "heat", "duration_s": 10.0})
        assert "recovery suggestion" in info["lab_report"]["text"].lower()
    finally:
        llm_env.close()

    rl_env = RLObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        observation, info = rl_env.reset(seed=0)
        assert observation.shape == rl_env.observation_space.shape
        assert np.all(np.isfinite(observation))
        assert rl_env.observation_space.contains(observation)
        assert np.all(np.isfinite(rl_env.observation_space.low))
        assert np.all(np.isfinite(rl_env.observation_space.high))
        assert "rl_view" in info
        spec = rl_observation_spec()
        assert info["rl_view"]["keys"] == spec["keys"]
        assert info["rl_view"]["bounds"] == spec["value_bounds"]
        assert info["observation_mask"].shape == (len(spec["keys"]),)
        assert "cost_signal" in info
    finally:
        rl_env.close()

    suggestion_env = ActionSuggestionWrapper(
        gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    )
    try:
        _, info = suggestion_env.reset(seed=0)
        assert "action_suggestions" in info
        _, _, _, _, info = suggestion_env.step({"operation": "heat", "duration_s": 10.0})
        assert "recovery_suggestion" in info
    finally:
        suggestion_env.close()


def test_campaign_state_updates_after_campaign_final_assay() -> None:
    env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    try:
        env.reset(seed=0)
        sequence = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 1500.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "quench"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        info = {}
        for action in sequence:
            _, _, terminated, truncated, info = env.step(action)
        state = env.unwrapped.campaign_state()
        report = env.unwrapped.observation_view("lab_report")
        assert not terminated
        assert not truncated
        assert info["experiment_ended"]
        assert state["final_assay_count"] == 1
        assert state["experiment_index"] == 1
        assert state["best_score"] is not None
        assert report["final_assay_summary"]["is_final_assay"]
        assert report["final_assay_summary"]["leaderboard_eligible"]
        assert report["campaign_progress"]["final_assay_count"] == 1
        assert "Final assay" in report["text"]
        assert "Best score so far" in report["text"]
    finally:
        env.close()


def test_tool_using_llm_stub_runs_agent_facing_tasks(tmp_path) -> None:
    output = tmp_path / "tool_stub.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=ToolUsingLLMStubAgent(),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=output,
    )
    records = load_jsonl(output)
    assert history[-1].info["leaderboard_score"] is not None
    assert records[-1]["agent_view"]["lab_report"]["mode"] == "lab_report"
    assert records[-1]["agent_trace"]
    flattened = flatten_record(records[-1])
    assert "agent_view" in flattened
    assert "agent_trace" in flattened


def test_llm_replay_agent_replays_action_trace(tmp_path) -> None:
    replay = tmp_path / "trace.jsonl"
    actions = [
        {"action": {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}},
        {"action": {"operation": "add_reagent", "amount_mol": 0.010}},
        {"action": {"operation": "terminate"}},
        {"action": {"operation": "measure", "instrument": "final_assay"}},
    ]
    replay.write_text(
        "\n".join(json.dumps(action, sort_keys=True) for action in actions),
        encoding="utf-8",
    )
    history = run_agent(
        env_id="ChemWorld",
        agent=LLMReplayAgent(replay),
        world_split="public-dev",
        budget=8,
        objective="balanced",
        seed=3,
        task_id="reaction-to-assay",
    )
    assert [record.action["operation"] for record in history[:4]] == [
        "add_solvent",
        "add_reagent",
        "terminate",
        "measure",
    ]


def _nested_values_for_key(payload: object, key: str) -> set[str]:
    if isinstance(payload, dict):
        values = {str(payload[key])} if key in payload else set()
        for value in payload.values():
            values.update(_nested_values_for_key(value, key))
        return values
    if isinstance(payload, list | tuple):
        values: set[str] = set()
        for item in payload:
            values.update(_nested_values_for_key(item, key))
        return values
    return set()
