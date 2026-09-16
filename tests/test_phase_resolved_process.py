from copy import deepcopy

import gymnasium as gym
import pytest
from scripts.run_work_ii_astra_full_process_trial import TASKS, reference_actions

import chemworld  # noqa: F401
from chemworld.agent_interface import action_schema, full_process_operational_state
from chemworld.foundation import equipment_settings
from chemworld.runtime.full_process_contract import FULL_PROCESS_CONTRACT, withdraw_sample


def make(task, resolved=True):
    env = gym.make(
        "ChemWorld",
        task_id=task,
        budget_override=90,
        full_process_contract_id=FULL_PROCESS_CONTRACT if resolved else None,
    )
    env.reset(seed=0)
    return env


def step(env, action):
    result = env.step(action)
    assert result[-1]["transaction_status"] == "committed", result[-1]
    return result


def test_receiver_sampling_and_reselection_preserve_saved_inventory_and_charge():
    env = make(TASKS[2])
    try:
        for a in reference_actions(TASKS[2])[:11]:
            step(env, a)
        step(
            env,
            {
                "operation": "distill",
                "target_temperature_K": 370,
                "duration_s": 1200,
                "reflux_ratio": 3,
            },
        )
        before = deepcopy(env.unwrapped._state)
        step(env, {"operation": "measure", "instrument": "gc"})
        after = env.unwrapped._state
        assert (
            after.phases.phases["collected_fraction"] == before.phases.phases["collected_fraction"]
        )
        assert after.phases.phases["bottoms"] == before.phases.phases["bottoms"]
        assert after.species == before.species
        assert after.phases.phases["distillate"].volume_L == pytest.approx(
            before.phases.phases["distillate"].volume_L - 0.00015
        )
        inventory = deepcopy(after.species_amounts)
        step(env, {"operation": "collect_fraction", "transfer_fraction": 0.0})
        assert env.unwrapped._state.species_amounts == inventory
        assert full_process_operational_state(env, {})["selected_phase"] == "collected_fraction"
        truth = env.unwrapped.observation_kernel._truth_values(env.unwrapped._state)
        assert truth["distillate_recovery"] == truth["recovery"]
        assert truth["distillate_purity"] == truth["purity"]
    finally:
        env.close()


@pytest.mark.parametrize("resolved", [False, True])
def test_zero_collection_requires_existing_receiver_in_new_contract(resolved):
    env = make(TASKS[2], resolved)
    try:
        for a in reference_actions(TASKS[2])[:10]:
            step(env, a)
        assert not env.unwrapped.operation_validator.validate(
            {"operation": "collect_fraction", "transfer_fraction": 0.0}, env.unwrapped._state
        ).is_valid
        step(env, {"operation": "collect_fraction", "transfer_fraction": 0.5})
        assert (
            env.unwrapped.operation_validator.validate(
                {"operation": "collect_fraction", "transfer_fraction": 0.0}, env.unwrapped._state
            ).is_valid
            is resolved
        )
    finally:
        env.close()


def test_paid_particle_sensor_preserves_material_and_scales_slurry_seed_provenance():
    env = make(TASKS[1])
    try:
        for a in reference_actions(TASKS[1])[:10]:
            step(env, a)
        before = deepcopy(env.unwrapped._state)
        _, _, terminated, _, info = step(
            env, {"operation": "measure", "instrument": "particle_size"}
        )
        after = env.unwrapped._state
        assert not terminated
        assert after.species_amounts == before.species_amounts
        assert after.phases == before.phases
        assert after.ledger.cost - before.ledger.cost == pytest.approx(0.04)
        assert after.ledger.time_s - before.ledger.time_s == 120
        assert info["raw_signal"]["kind"] == "particle_size_signal"
        assert "crystal_fines_fraction" in info["observed_keys"]
        truth_before = env.unwrapped.observation_kernel._truth_values(after)
        sampled = withdraw_sample(after, after.volume_L / 10)
        truth_after = env.unwrapped.observation_kernel._truth_values(sampled)
        assert truth_after["crystal_yield"] == pytest.approx(truth_before["crystal_yield"] * 0.9)
        assert equipment_settings(sampled.equipment, "crystallizer")[
            "seed_target_mol"
        ] == pytest.approx(
            equipment_settings(after.equipment, "crystallizer")["seed_target_mol"] * 0.9
        )
        assert sampled.species == after.species
        env.reset(seed=0)
        assert env.unwrapped._state.metadata["full_process_contract_id"] == FULL_PROCESS_CONTRACT
        assert "particle_size" in str(action_schema(env, "measure"))
    finally:
        env.close()


def test_legacy_task_contract_is_unchanged_and_sensor_excluded():
    from chemworld.tasks import get_task

    for task in TASKS:
        env = make(task, False)
        try:
            assert env.unwrapped.task_spec.contract_hash == get_task(task).contract_hash
            assert "particle_size" not in env.unwrapped.allowed_instruments
        finally:
            env.close()
