from __future__ import annotations

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.action_codec import ActionCodec
from chemworld.tasks import get_task, get_task_card, list_tasks
from chemworld.wrappers import (
    ActionMaskWrapper,
    NaNObservationWrapper,
    SafetyCostWrapper,
    validate_event_action,
)


def test_builtin_tasks_are_instantiable() -> None:
    task_ids = {task.task_id for task in list_tasks()}
    assert {
        "reaction-to-assay",
        "reaction-optimization-standard",
        "reaction-safety-constrained",
        "public-private-generalization",
        "reaction-mechanism-explanation",
    } <= task_ids
    task = get_task("reaction-optimization-standard")
    assert task.env_id == "ChemWorld"
    assert task.world_law_id == "chemworld-physical-chemistry"
    assert task.env_kwargs(seed=7)["seed"] == 7
    assert "hplc" in task.allowed_instruments
    card = get_task_card("reaction-optimization-standard")
    assert card["task_id"] == "reaction-optimization-standard"
    assert card["world_law_id"] == "chemworld-physical-chemistry"
    assert "baseline_reference_scores" in card
    assert "failure_modes" in card


def test_all_tasks_share_one_world_law() -> None:
    tasks = list_tasks()
    assert {task.env_id for task in tasks} == {"ChemWorld"}
    assert {task.world_law_id for task in tasks} == {"chemworld-physical-chemistry"}
    assert "reaction-to-purification" in {task.task_id for task in tasks}
    assert "partition-discovery" in {task.task_id for task in tasks}
    assert "purity-yield-tradeoff" in {task.task_id for task in tasks}


def test_action_mask_wrapper_reports_valid_operations() -> None:
    env = ActionMaskWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        _, info = env.reset(seed=0)
        assert "action_mask" in info
        assert "add_solvent" in info["valid_operations"]
        assert "heat" not in info["valid_operations"]

        validation = validate_event_action({"operation": "heat"}, env)
        assert not validation["valid"]
        assert not validation["preconditions"]["has_volume"]

        _, _, _, _, step_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
        )
        assert "heat" not in step_info["valid_operations"]
        _, _, _, _, step_info = env.step({"operation": "add_reagent", "amount_mol": 0.01})
        assert "heat" in step_info["valid_operations"]
    finally:
        env.close()


def test_action_codec_roundtrip_vector() -> None:
    codec = ActionCodec()
    action = {
        "operation": "heat",
        "target_temperature_K": 386.0,
        "duration_s": 900.0,
        "instrument": "hplc",
    }
    vector = codec.encode_vector(action)
    decoded = codec.decode_vector(vector)
    assert decoded["operation"] == "heat"
    assert decoded["instrument"] == "hplc"
    assert decoded["target_temperature_K"] == 386.0
    assert decoded["duration_s"] == 900.0


def test_action_mask_is_task_aware() -> None:
    reaction_env = ActionMaskWrapper(
        gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    )
    purification_env = ActionMaskWrapper(
        gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    )
    try:
        _, reaction_info = reaction_env.reset(seed=0)
        _, purification_info = purification_env.reset(seed=0)
        assert "add_extractant" not in reaction_info["valid_operations"]
        assert "add_extractant" not in purification_info["valid_operations"]

        validation = validate_event_action({"operation": "add_extractant"}, reaction_env)
        assert not validation["valid"]
        assert not validation["preconditions"]["operation_allowed_by_task"]
        assert "operation_allowed_by_task" in validation["invalid_reasons"]

        purification_env.step({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1})
        purification_env.step({"operation": "add_reagent", "amount_mol": 0.01})
        _, _, _, _, info = purification_env.step(
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.010}
        )
        assert "add_extractant" in info["valid_operations"]
    finally:
        reaction_env.close()
        purification_env.close()


def test_safety_cost_wrapper_preserves_gym_return_shape() -> None:
    env = SafetyCostWrapper(gym.make("ChemWorld", budget=2, seed=0))
    try:
        observation, info = env.reset(seed=0)
        assert isinstance(observation, dict)
        assert info["cost_signal"] == 0.0
        result = env.step({"operation": "heat", "duration_s": 100.0})
        assert len(result) == 5
        _, reward, _, _, step_info = result
        assert isinstance(reward, float)
        assert step_info["cost_signal"] > 0.0
        assert "precondition_failure" in step_info["cost_components"]
        assert step_info["constraint_budget_remaining"] <= 1.0
    finally:
        env.close()


def test_nan_observation_wrapper_returns_vector_with_mask() -> None:
    env = NaNObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        observation, _ = env.reset(seed=0)
        width = len(env.observation_keys)
        assert observation.shape == (width * 2,)
        assert np.any(observation[:width] == -1.0)
        assert set(np.unique(observation[width:])).issubset({0.0, 1.0})
    finally:
        env.close()


def test_purification_task_reaches_downstream_assay() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=2)
    try:
        obs, info = env.reset(seed=2)
        del obs
        assert "separate_phase" in info["allowed_operations"]
        actions = [
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
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
            {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018},
            {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
            {"operation": "settle", "duration_s": 420.0},
            {"operation": "separate_phase", "target_phase": "organic"},
            {"operation": "wash", "wash_volume_L": 0.008},
            {"operation": "dry"},
            {"operation": "concentrate", "duration_s": 600.0},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        final_info = {}
        observation = {}
        for action in actions:
            observation, _, terminated, _, final_info = env.step(action)
        assert terminated
        assert final_info["leaderboard_score"] is not None
        assert float(observation["purity"][0]) >= 0.0
        assert float(observation["recovery"][0]) >= 0.0
        assert final_info["processed_estimate"]["process_mass_balance_error"] >= 0.0
    finally:
        env.close()

