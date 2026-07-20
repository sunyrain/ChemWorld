from __future__ import annotations

import math

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.rl.rewards import PublicBehaviorTracker, reward_contract
from chemworld.task_design import SERIOUS_TASK_DESIGNS, review_task_design
from chemworld.tasks import FLAGSHIP_TASK_IDS, get_task

EXPECTED_METRICS = {
    "reaction-to-crystallization": {
        "score",
        "crystal_yield",
        "crystal_purity",
        "crystal_size",
        "crystal_csd_quality",
        "crystal_fines_fraction",
    },
    "electrochemical-conversion": {
        "score",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "transport_efficiency",
        "ohmic_efficiency",
        "energy_efficiency",
        "pH_normalized",
        "precipitation_signal",
        "safety_risk",
    },
}


def _run_midpoint(task_id: str, *, seed: int = 0) -> tuple[dict, PublicBehaviorTracker]:
    task = get_task(task_id)
    recipe = task_recipe_from_unit_vector(
        task.to_dict(),
        np.full(task_recipe_dimension(task.to_dict()), 0.5),
    )
    env = gym.make(
        "ChemWorld",
        task_id=task_id,
        budget_override=len(recipe["steps"]) + 1,
        episode_mode_override="campaign",
    )
    tracker = PublicBehaviorTracker(task.allowed_operations, task_id=task_id)
    final_info: dict = {}
    try:
        env.reset(seed=seed)
        for action in recipe["steps"]:
            _, _, _, _, final_info = env.step(action)
            tracker.observe(final_info)
            assert final_info["transaction_status"] == "committed"
            assert final_info["constraint_flags"]["precondition_failed"] is False
            assert final_info["preconditions"].get("runtime_domain_valid") is not False
            assert final_info["preconditions"].get("observation_domain_valid") is not False
    finally:
        env.close()
    return final_info, tracker


def test_flagship_scope_is_exactly_the_two_integrated_tasks() -> None:
    assert FLAGSHIP_TASK_IDS == (
        "reaction-to-crystallization",
        "electrochemical-conversion",
    )
    for task_id in FLAGSHIP_TASK_IDS:
        task = get_task(task_id)
        assert "flagship" in task.tags
        assert "closed-loop" in task.tags
        assert set(task.success_metrics) == EXPECTED_METRICS[task_id]
        review = review_task_design(task, SERIOUS_TASK_DESIGNS[task_id])
        assert review.contract_ready is True
        contract = reward_contract(task.allowed_operations, task_id=task_id)
        assert contract["behavioral_completion"]["ordered_flagship_milestones"] is True


@pytest.mark.parametrize("task_id", FLAGSHIP_TASK_IDS)
def test_midpoint_flagship_recipe_completes_physics_and_behavior_contract(task_id: str) -> None:
    final_info, tracker = _run_midpoint(task_id)
    assert final_info["experiment_ended"] is True
    assert final_info["leaderboard_score"] is not None
    assert tracker.complete is True
    processed = final_info["processed_estimate"]
    for metric in EXPECTED_METRICS[task_id] - {"score", "safety_risk"}:
        assert metric in processed
        assert math.isfinite(float(processed[metric]))


def test_crystallization_contract_requires_assays_before_cooling_and_isolation() -> None:
    _, tracker = _run_midpoint("reaction-to-crystallization")
    sequence = tracker.operation_sequence
    reaction_assay = sequence.index("measure:hplc")
    cooling = sequence.index("cool_crystallize")
    slurry_assay = sequence.index("measure:hplc", reaction_assay + 1)
    isolation = sequence.index("filter_crystals")
    assert reaction_assay < cooling < slurry_assay < isolation
    assert "controlled_cooling" in tracker.tokens


def test_electrochemical_contract_requires_diagnosis_before_changed_setpoint() -> None:
    _, tracker = _run_midpoint("electrochemical-conversion")
    sequence = tracker.operation_sequence
    first_electrolysis = sequence.index("electrolyze")
    ph_diagnostic = sequence.index("measure:ph_meter")
    performance_diagnostic = sequence.index("measure:uvvis")
    second_setpoint = sequence.index("set_potential", sequence.index("set_potential") + 1)
    second_electrolysis = sequence.index("electrolyze", first_electrolysis + 1)
    assert (
        first_electrolysis
        < ph_diagnostic
        < performance_diagnostic
        < second_setpoint
        < second_electrolysis
    )
    assert "adapted_setpoint" in tracker.tokens


def test_crystallization_termination_is_gated_by_isolated_crystals() -> None:
    task = get_task("reaction-to-crystallization")
    recipe = task_recipe_from_unit_vector(
        task.to_dict(),
        np.full(task_recipe_dimension(task.to_dict()), 0.5),
    )
    env = gym.make(
        "ChemWorld",
        task_id=task.task_id,
        budget_override=len(recipe["steps"]) + 1,
        episode_mode_override="campaign",
    )
    try:
        env.reset(seed=0)
        for action in recipe["steps"]:
            if action["operation"] == "filter_crystals":
                blocked = env.unwrapped.validate_action({"operation": "terminate"})
                assert blocked["valid"] is False
                assert (
                    "flagship_crystallization_requires_isolated_crystals"
                    in blocked["invalid_reasons"]
                )
            if action["operation"] == "terminate":
                assert env.unwrapped.validate_action(action)["valid"] is True
            env.step(action)
    finally:
        env.close()


def test_electrochemical_affordances_enforce_probe_diagnose_adapt_control() -> None:
    task = get_task("electrochemical-conversion")
    recipe = task_recipe_from_unit_vector(
        task.to_dict(),
        np.full(task_recipe_dimension(task.to_dict()), 0.5),
    )
    steps = list(recipe["steps"])
    env = gym.make(
        "ChemWorld",
        task_id=task.task_id,
        budget_override=len(steps) + 1,
        episode_mode_override="campaign",
    )
    try:
        env.reset(seed=0)
        for action in steps[:4]:
            env.step(action)

        measurement = env.unwrapped.action_schema("measure")
        instrument = next(
            field for field in measurement["fields"] if field["field"] == "instrument"
        )
        assert instrument["choices"] == ["uvvis", "ph_meter"]
        assert env.unwrapped.validate_action({"operation": "terminate"})["valid"] is False

        env.step(steps[4])
        measurement = env.unwrapped.action_schema("measure")
        instrument = next(
            field for field in measurement["fields"] if field["field"] == "instrument"
        )
        assert instrument["choices"] == ["uvvis"]
        env.step(steps[5])

        assert env.unwrapped.validate_action(steps[6])["valid"] is True
        env.step(steps[6])
        assert env.unwrapped.validate_action({"operation": "terminate"})["valid"] is False
        env.step(steps[7])

        measurement = env.unwrapped.action_schema("measure")
        instrument = next(
            field for field in measurement["fields"] if field["field"] == "instrument"
        )
        assert instrument["choices"] == ["uvvis"]
        env.step(steps[8])
        assert env.unwrapped.validate_action({"operation": "terminate"})["valid"] is True
    finally:
        env.close()
