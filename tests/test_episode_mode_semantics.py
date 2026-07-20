from __future__ import annotations

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.tasks import list_tasks

FINAL_ASSAY_RECIPE = [
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


def test_task_termination_policy_matches_episode_mode() -> None:
    for task in list_tasks():
        if task.episode_mode == "campaign":
            assert task.termination_policy in {
                "budget",
                "budget-with-workflow-gated-final-assay",
            }, task.task_id
            if task.termination_policy == "budget-with-workflow-gated-final-assay":
                assert "final_assay" in task.allowed_instruments, task.task_id
                assert "measure" in task.allowed_operations, task.task_id
        else:
            assert task.episode_mode == "single_experiment", task.task_id
            assert task.termination_policy == "final-assay-or-budget", task.task_id


def test_single_experiment_final_assay_terminates_episode() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        info = {}
        terminated = False
        truncated = False
        for action in FINAL_ASSAY_RECIPE:
            _, _, terminated, truncated, info = env.step(action)

        campaign_state = env.unwrapped.campaign_state()
        assert terminated is True
        assert truncated is False
        assert info["episode_mode"] == "single_experiment"
        assert info["experiment_ended"] is False
        assert "next_experiment_ready" not in info
        assert "next_experiment_index" not in info
        assert info["leaderboard_score"] is not None
        assert campaign_state["done"] is True
        assert campaign_state["final_assay_count"] == 1

        with pytest.raises(RuntimeError, match="Episode is done"):
            env.step({"operation": "add_solvent", "volume_L": 0.01, "solvent": 1})
    finally:
        env.close()


def test_campaign_final_assay_ends_experiment_but_not_episode() -> None:
    env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    try:
        env.reset(seed=0)
        final_info = {}
        terminated = False
        truncated = False
        for action in FINAL_ASSAY_RECIPE:
            _, _, terminated, truncated, final_info = env.step(action)

        campaign_state = env.unwrapped.campaign_state()
        assert terminated is False
        assert truncated is False
        assert final_info["episode_mode"] == "campaign"
        assert final_info["experiment_ended"] is True
        assert final_info["next_experiment_ready"] is True
        assert final_info["experiment_index"] == 0
        assert final_info["next_experiment_index"] == 1
        assert final_info["leaderboard_score"] is not None
        assert len(final_info["experiment_summaries"]) == 1
        assert final_info["experiment_summaries"][-1] == final_info["last_terminal_summary"]
        assert final_info["last_terminal_summary"]["experiment_index"] == 0
        assert final_info["last_terminal_summary"]["leaderboard_score"] == pytest.approx(
            final_info["leaderboard_score"]
        )
        assert campaign_state["done"] is False
        assert campaign_state["experiment_index"] == 1
        assert campaign_state["final_assay_count"] == 1
        assert campaign_state["last_terminal_summary"] == final_info["last_terminal_summary"]

        _, _, terminated, truncated, next_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
        )
        assert terminated is False
        assert truncated is False
        assert next_info["experiment_index"] == 1
        assert next_info["experiment_ended"] is False
        assert not next_info["constraint_flags"]["precondition_failed"]
    finally:
        env.close()


def test_agent_return_mutation_cannot_corrupt_campaign_or_observation_cache() -> None:
    env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    try:
        observation, _ = env.reset(seed=0)
        observation["score"][0] = np.float32(0.99)
        assert float(env.unwrapped._last_observation["score"][0]) == pytest.approx(0.0)

        final_info = {}
        final_observation = observation
        for action in FINAL_ASSAY_RECIPE:
            final_observation, _, _, _, final_info = env.step(action)

        internal_score = env.unwrapped._experiment_summaries[0]["leaderboard_score"]
        cached_score = float(env.unwrapped._last_observation["score"][0])
        cached_preconditions = dict(env.unwrapped._last_info["preconditions"])

        final_info["experiment_summaries"][0]["leaderboard_score"] = -999.0
        final_info["last_terminal_summary"]["leaderboard_score"] = -999.0
        final_info["preconditions"].clear()
        final_observation["score"][0] = np.float32(0.0)

        state = env.unwrapped.campaign_state()
        assert state["experiment_summaries"][0]["leaderboard_score"] == pytest.approx(
            internal_score
        )
        assert env.unwrapped._last_info["preconditions"] == cached_preconditions
        assert float(env.unwrapped._last_observation["score"][0]) == pytest.approx(
            cached_score
        )

        state["experiment_summaries"][0]["leaderboard_score"] = -123.0
        assert env.unwrapped._experiment_summaries[0]["leaderboard_score"] == pytest.approx(
            internal_score
        )
    finally:
        env.close()


def test_reset_and_campaign_initial_states_are_isolated_from_mutated_live_state() -> None:
    env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    try:
        env.reset(seed=0)
        base = env.unwrapped
        species_id = next(iter(base._state.species_amounts))
        expected = base.scenario_instance.initial_state.species_amounts[species_id]

        # Frozen dataclasses still contain mutable mapping members.  Even if an
        # internal diagnostic accidentally mutates the live mapping, the
        # scenario template used by reset/campaign rollover must remain clean.
        base._state.species_amounts[species_id] = 999.0
        assert base.scenario_instance.initial_state.species_amounts[species_id] == pytest.approx(
            expected
        )

        base.reset(seed=0)
        assert base._state.species_amounts[species_id] == pytest.approx(expected)
        assert base._state is not base.scenario_instance.initial_state
    finally:
        env.close()


def test_extended_research_profile_overrides_budget_and_episode_mode() -> None:
    env = gym.make(
        "ChemWorld",
        task_id="reaction-to-assay",
        seed=0,
        budget_override=36,
        episode_mode_override="campaign",
    )
    try:
        _, task_info = env.reset(seed=0)
        assert task_info["budget"] == 36
        assert task_info["official_budget"] == 18
        assert task_info["episode_mode"] == "campaign"
        assert task_info["contract_profile"] == "extended-research"
        final_info = {}
        for action in FINAL_ASSAY_RECIPE:
            _, _, terminated, truncated, final_info = env.step(action)
        assert not terminated
        assert not truncated
        state = env.unwrapped.campaign_state()
        assert state["experiment_index"] == 1
        assert len(state["experiment_summaries"]) == 1
        assert final_info["next_experiment_ready"] is True
    finally:
        env.close()
