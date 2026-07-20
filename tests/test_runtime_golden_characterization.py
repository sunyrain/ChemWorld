from __future__ import annotations

import math
from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.envs.chemworld_env import OBSERVATION_KEYS
from chemworld.tasks import TaskSpec, list_tasks

REACTION_STEPS: tuple[dict[str, Any], ...] = (
    {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
    {"operation": "add_reagent", "amount_mol": 0.010},
    {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
    {
        "operation": "heat",
        "target_temperature_K": 385.0,
        "duration_s": 1500.0,
        "stirring_speed_rpm": 720.0,
    },
    {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0},
)

REACTION_FINAL = (
    *REACTION_STEPS,
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

PURIFICATION_FINAL = (
    *REACTION_STEPS,
    {"operation": "quench"},
    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
    {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018},
    {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
    {"operation": "settle", "duration_s": 420.0},
    {"operation": "separate_phase", "target_phase": "organic"},
    {"operation": "wash", "wash_volume_L": 0.008},
    {"operation": "dry"},
    {"operation": "concentrate", "duration_s": 600.0},
    {"operation": "transfer", "transfer_fraction": 0.97},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

CRYSTALLIZATION_FINAL = (
    *REACTION_STEPS,
    {"operation": "measure", "instrument": "hplc"},
    {"operation": "seed_crystals", "seed_mass_g": 0.006},
    {
        "operation": "cool_crystallize",
        "target_temperature_K": 278.15,
        "duration_s": 1800.0,
    },
    {"operation": "measure", "instrument": "hplc"},
    {"operation": "filter_crystals"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

DISTILLATION_FINAL = (
    *REACTION_STEPS,
    {"operation": "evaporate", "target_temperature_K": 335.0, "duration_s": 600.0},
    {
        "operation": "distill",
        "target_temperature_K": 360.0,
        "duration_s": 1500.0,
        "reflux_ratio": 2.0,
    },
    {"operation": "collect_fraction", "transfer_fraction": 0.92},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

FLOW_FINAL = (
    {"operation": "add_solvent", "volume_L": 0.026, "solvent": 2},
    {"operation": "add_reagent", "amount_mol": 0.010},
    {"operation": "add_catalyst", "catalyst_amount_mol": 0.00022, "catalyst": 1},
    {"operation": "set_flow_rate", "flow_rate_mL_min": 1.2, "residence_time_s": 900.0},
    {"operation": "run_flow", "target_temperature_K": 382.0, "duration_s": 1800.0},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

ELECTROCHEMISTRY_FINAL = (
    {"operation": "add_solvent", "volume_L": 0.026, "solvent": 0},
    {"operation": "add_reagent", "amount_mol": 0.010},
    {
        "operation": "set_potential",
        "potential_V": 1.15,
        "current_mA": 75.0,
        "electrolyte_profile": 1,
    },
    {"operation": "electrolyze", "duration_s": 1800.0},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

EQUILIBRIUM_FINAL = (
    {"operation": "add_solvent", "volume_L": 0.030, "solvent": 0},
    {"operation": "add_reagent", "amount_mol": 0.006},
    {"operation": "measure", "instrument": "ph_meter"},
    {"operation": "add_reagent", "amount_mol": 0.004},
    {"operation": "measure", "instrument": "ph_meter"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

PARTITION_FINAL = (
    {"operation": "add_solvent", "volume_L": 0.025, "solvent": 1},
    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.018},
    {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018},
    {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 750.0},
    {"operation": "settle", "duration_s": 360.0},
    {"operation": "separate_phase", "target_phase": "organic"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)

GOLDEN: dict[str, dict[str, Any]] = {
    "electrochemical-conversion": {
        "mechanism_id": "electrochemical_conversion",
        "steps": 6,
        "score": 0.7634379681948985,
    },
    "equilibrium-characterization": {
        "mechanism_id": "simple_batch_reaction",
        "steps": 7,
        "score": 0.28981344839072215,
    },
    "flow-reaction-optimization": {
        "mechanism_id": "pfr_hotspot",
        "steps": 7,
        "score": 0.04025939108974932,
    },
    "low-budget-characterization": {
        "mechanism_id": "autocatalytic_reaction",
        "steps": 7,
        "score": 0.1918881438581116,
    },
    "partition-discovery": {
        "mechanism_id": "reaction_extraction",
        "steps": 8,
        "score": 0.4365037717211494,
    },
    "public-private-generalization": {
        "mechanism_id": "parallel_series_reaction",
        "steps": 7,
        "score": 0.11534868145970442,
    },
    "purity-yield-tradeoff": {
        "mechanism_id": "reaction_extraction",
        "steps": 17,
        "score": 0.25507638518935166,
    },
    "reaction-mechanism-explanation": {
        "mechanism_id": "autocatalytic_reaction",
        "steps": 7,
        "score": 0.22155533806413272,
    },
    "reaction-optimization-standard": {
        "mechanism_id": "simple_batch_reaction",
        "steps": 7,
        "score": 0.372689896248878,
    },
    "reaction-safety-constrained": {
        "mechanism_id": "catalyst_deactivation",
        "steps": 7,
        "score": 0.11042791355818407,
    },
    "reaction-to-assay": {
        "mechanism_id": "simple_batch_reaction",
        "steps": 7,
        "score": 0.2640746425356242,
    },
    "reaction-to-crystallization": {
        "mechanism_id": "simple_batch_reaction",
        "steps": 12,
        "score": 0.4597052333212239,
    },
    "reaction-to-distillation": {
        "mechanism_id": "reactive_distillation_lite",
        "steps": 10,
        "score": 0.2057057872506592,
    },
    "reaction-to-purification": {
        "mechanism_id": "reaction_extraction",
        "steps": 17,
        "score": 0.296613558321044,
    },
    "tool-agent-planning": {
        "mechanism_id": "reaction_extraction",
        "steps": 17,
        "score": 0.0,
    },
}


def _scripted_final_actions(task_id: str) -> tuple[dict[str, Any], ...]:
    if task_id in {
        "reaction-to-purification",
        "purity-yield-tradeoff",
        "tool-agent-planning",
    }:
        return PURIFICATION_FINAL
    if task_id == "reaction-to-crystallization":
        return CRYSTALLIZATION_FINAL
    if task_id == "reaction-to-distillation":
        return DISTILLATION_FINAL
    if task_id == "flow-reaction-optimization":
        return FLOW_FINAL
    if task_id == "electrochemical-conversion":
        return ELECTROCHEMISTRY_FINAL
    if task_id == "equilibrium-characterization":
        return EQUILIBRIUM_FINAL
    if task_id == "partition-discovery":
        return PARTITION_FINAL
    return REACTION_FINAL


def test_golden_registry_covers_current_formal_tasks() -> None:
    assert {task.task_id for task in list_tasks()} == set(GOLDEN)


@pytest.mark.parametrize("task", list_tasks(), ids=lambda task: task.task_id)
def test_runtime_v2_golden_scripted_final_assay(
    task: TaskSpec,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CHEMWORLD_PRIVATE_EVAL_SALT", raising=False)
    expected = GOLDEN[task.task_id]
    actions = _scripted_final_actions(task.task_id)
    assert len(actions) == expected["steps"]

    env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
    try:
        observation, reset_info = env.reset(seed=task.seeds[0])
        assert reset_info["mechanism_id"] == expected["mechanism_id"]
        assert reset_info["mechanism_hash"]

        final_info: dict[str, Any] = {}
        final_terminated = False
        final_truncated = False
        for action in actions:
            observation, _, final_terminated, final_truncated, final_info = env.step(action)
            assert not final_info["constraint_flags"]["precondition_failed"], action
            assert final_info["transaction_status"] == "committed"
            assert final_info["kernel_id"].startswith("chemworld.operation.")
            assert final_info["mechanism_hash"] == reset_info["mechanism_hash"]

        assert final_info["operation_type"] == "measure"
        assert final_info["instrument"] == "final_assay"
        assert final_info["kernel_id"] == "chemworld.operation.measure"
        assert final_info["leaderboard_score"] == pytest.approx(
            expected["score"],
            abs=1e-9,
        )
        assert final_info["remaining_budget"] == task.budget - expected["steps"]
        assert final_info["world_events"][0]["event_type"] == "operation_applied"
        assert final_info["state_patches_summary"][0]["patch_type"] == "replace_state"
        assert "process" in final_info["affected_ledgers"]
        assert "observation" in final_info["affected_ledgers"]
        assert "equipment" in final_info["affected_ledgers"]
        assert {
            "phase_system",
            "phase_settled",
            "selected_phase",
            "final_assay_done",
            "final_assay_time_s",
            "crystal_seeded",
            "crystal_seed_mass_g",
            "crystallization_active",
            "crystal_product_mol",
            "crystal_impurity_mol",
            "distillation_active",
            "distillate_product_mol",
            "distillate_impurity_mol",
            "solvent_loss",
            "initial_reactant_mol",
            "crystals_filtered",
            "distillation_model",
            "distillation_kernel",
            "fraction_collected",
        }.isdisjoint(env.unwrapped._state.metadata)
        assert not any(
            key.startswith("initial_") and key.endswith("_mol")
            for key in env.unwrapped._state.metadata
        )
        if env.unwrapped._state.phases is not None:
            assert all(
                {"product_mol", "impurity_mol", "solvent_loss"}.isdisjoint(
                    phase.metadata
                )
                for phase in env.unwrapped._state.phases.phases.values()
            )

        if task.episode_mode == "campaign":
            assert not final_terminated
            assert not final_truncated
            assert final_info["experiment_ended"] is True
            assert final_info["next_experiment_ready"] is True
        else:
            assert final_terminated
            assert not final_truncated
            assert final_info["experiment_ended"] is False
            assert "next_experiment_ready" not in final_info

        observable_success_metrics = set(OBSERVATION_KEYS).intersection(
            task.success_metrics
        )
        for key in observable_success_metrics:
            assert math.isfinite(float(observation[key][0])), key
    finally:
        env.close()
