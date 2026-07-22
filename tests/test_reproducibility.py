from __future__ import annotations

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.world.recipes import recipe_to_event_sequence


def _run_once(seed: int) -> list[float]:
    actions = recipe_to_event_sequence(
        {
            "temperature": 110.0,
            "time": 3.0,
            "initial_concentration": 1.0,
            "stirring_speed": 700.0,
            "catalyst": 1,
            "solvent": 2,
        }
    )
    env = gym.make("ChemWorld", world_split="public-test", budget=len(actions), seed=seed)
    env.reset(seed=seed)
    rewards: list[float] = []
    for action in actions:
        _, reward, _, _, _ = env.step(action)
        rewards.append(reward)
    env.close()
    return rewards


def test_fixed_seed_is_reproducible() -> None:
    assert _run_once(123) == _run_once(123)


def test_split_changes_world() -> None:
    env_a = gym.make("ChemWorld", world_split="public-test", seed=5)
    env_b = gym.make("ChemWorld", world_split="private-eval", seed=5)
    env_a.reset(seed=5)
    env_b.reset(seed=5)
    assert (
        env_a.unwrapped.evaluator_provenance()["world_id"]
        != env_b.unwrapped.evaluator_provenance()["world_id"]
    )
    env_a.close()
    env_b.close()


def test_private_eval_can_use_external_salt(monkeypatch) -> None:
    env_placeholder = gym.make("ChemWorld", world_split="private-eval", seed=6)
    env_placeholder.reset(seed=6)
    placeholder_info = env_placeholder.unwrapped.evaluator_provenance()
    env_placeholder.close()

    monkeypatch.setenv("CHEMWORLD_PRIVATE_EVAL_SALT", "secret-suite")
    env_private = gym.make("ChemWorld", world_split="private-eval", seed=6)
    env_private.reset(seed=6)
    private_info = env_private.unwrapped.evaluator_provenance()
    env_private.close()

    assert placeholder_info["world_provider"] == "public-placeholder-private"
    assert private_info["world_provider"] == "external-private-registry"
    assert placeholder_info["world_id"] != private_info["world_id"]
    assert "secret-suite" not in private_info["world_id"]
