from __future__ import annotations

from pathlib import Path

import gymnasium as gym
import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env, data_equivalence

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import task_recipe_dimension, task_recipe_from_unit_vector
from chemworld.data.logging import TrajectoryLogger, load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.runtime.full_process_contract import sample_domain
from chemworld.wrappers import ContinuousEventActionWrapper, RLObservationWrapper

TASKS = (
    "reaction-to-assay",
    "reaction-to-distillation",
    "reaction-to-crystallization",
    "partition-discovery",
)


def sampling_path(path: Path, mode: str | None, seed: int, operation: str) -> dict:
    env = gym.make(
        "ChemWorld",
        task_id="reaction-to-distillation",
        seed=seed,
        full_process_contract_id=mode,
        episode_mode_override="single_experiment",
    )
    try:
        env.reset(seed=seed)
        task = {**env.unwrapped.task_info(), **env.unwrapped.evaluator_provenance()}
        recipe = task_recipe_from_unit_vector(task, np.full(task_recipe_dimension(task), 0.5))
        actions = recipe["steps"][:9]
        volume = 0.00015 if operation == "measure" else 0.0001
        actions.append(
            {"operation": "measure", "instrument": "gc"}
            if operation == "measure"
            else {"operation": "sample", "sample_volume_L": volume}
        )
        actions.extend(
            [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
        )
        snapshot = None
        with TrajectoryLogger(path) as logger:
            for step, action in enumerate(actions, 1):
                before = env.unwrapped._state
                observation, reward, terminated, truncated, info = env.step(action)
                logger.log(
                    task_info=task,
                    step=step,
                    action=action,
                    observation=observation,
                    reward=reward,
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={},
                )
                assert info["transaction_status"] == "committed", info.get("preconditions")
                if step != 10:
                    continue
                after = env.unwrapped._state
                domain = sample_domain(before)
                assert len(domain) == 1
                selected = domain[0]
                assert selected == "collected_fraction"
                total_loss = sum(p.volume_L for p in before.phases.phases.values()) - sum(
                    p.volume_L for p in after.phases.phases.values()
                )
                assert total_loss == pytest.approx(volume, abs=1e-12)
                assert before.volume_L - after.volume_L == pytest.approx(volume, abs=1e-12)
                fraction = volume / before.phases.phases[selected].volume_L
                if mode is not None:
                    assert after.species == before.species
                else:
                    assert after.species.initial_amounts_mol == pytest.approx(
                        {
                            key: amount * (1 - fraction)
                            for key, amount in before.species.initial_amounts_mol.items()
                        },
                        abs=1e-12,
                    )
                for phase_id, phase in before.phases.phases.items():
                    changed = after.phases.phases[phase_id]
                    if phase_id not in domain:
                        assert changed == phase
                    else:
                        for species, amount in phase.species_amounts_mol.items():
                            assert changed.species_amounts_mol[species] == pytest.approx(
                                amount * (1 - fraction), abs=1e-12
                            )
                assert info["sample_consumed"] == pytest.approx(volume, abs=1e-12)
                assert after.ledger.sample_consumed_L - before.ledger.sample_consumed_L == (
                    pytest.approx(volume, abs=1e-12)
                )
                snapshot = {
                    "selected": selected,
                    "total_loss_L": total_loss,
                    "reported_L": info["sample_consumed"],
                    "expected_L": volume,
                }
        replay = verify_records(load_jsonl(path), tolerance=0.0)
        assert replay.verified, replay.to_dict()
        return {
            "seed": seed,
            "mode": mode,
            "operation": operation,
            "sample": snapshot,
            "exact_replay": True,
            "actions": len(actions),
        }
    finally:
        env.close()


@pytest.mark.parametrize("mode", [None, "phase-resolved-process-v5"])
@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("operation", ["measure", "sample"])
def test_selected_sampling_conserves_unselected_phases(tmp_path, mode, seed, operation):
    sampling_path(tmp_path / "trajectory.jsonl", mode, seed, operation)


@pytest.mark.parametrize("task", TASKS)
@pytest.mark.parametrize("continuous", [False, True])
def test_supported_rl_entry_passes_official_gym_checker(task, continuous):
    env = RLObservationWrapper(gym.make("ChemWorld", task_id=task))
    if continuous:
        env = ContinuousEventActionWrapper(env)
    try:
        check_env(env)
    finally:
        env.close()


def test_seed_determinism_preserves_unique_audit_identity():
    env = RLObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay"))
    try:
        env.reset(seed=123)
        first = env.step({"operation": "add_solvent", "volume_L": 0.025, "solvent": 0})
        first_audit = dict(env.last_audit_metadata)
        env.reset(seed=123)
        second = env.step({"operation": "add_solvent", "volume_L": 0.025, "solvent": 0})
        assert data_equivalence(first, second)
        assert first_audit["campaign_id"] != env.last_audit_metadata["campaign_id"]
        assert env.unwrapped._last_info["campaign_id"] == env.last_audit_metadata["campaign_id"]
        assert "campaign_id" not in second[4]
    finally:
        env.close()


def test_vector_environment_has_finite_values_and_explicit_masks():
    def make():
        return ContinuousEventActionWrapper(
            RLObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay"))
        )

    env = gym.vector.SyncVectorEnv([make, make])
    try:
        observation, info = env.reset(seed=42)
        env.action_space.seed(42)
        for _ in range(20):
            observation, _, _, _, info = env.step(env.action_space.sample())
            assert np.isfinite(observation).all()
            assert "observation_mask" in info
        assert observation.shape[0] == 2
    finally:
        env.close()
