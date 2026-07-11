"""Reproducible development evaluation for frozen SB3 checkpoints."""

from __future__ import annotations

import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from chemworld.rl.environment import RLWorldAllocation, build_rl_environment

AlgorithmName = Literal["ppo", "sac"]


def evaluate_sb3_checkpoint(
    *,
    algorithm: AlgorithmName,
    checkpoint: str | Path,
    task_id: str,
    allocation: RLWorldAllocation,
    episodes: int,
    operation_budget: int,
    sampler_seed: int,
    policy_seed: int,
    deterministic: bool,
) -> dict[str, Any]:
    """Evaluate one checkpoint without training reward or Bench access."""

    if episodes <= 0 or operation_budget <= 0:
        raise ValueError("episodes and operation_budget must be positive")
    if allocation.name == "train":
        raise ValueError("checkpoint selection evaluation must use Dev, not Train")
    if allocation.name == "bench":
        raise ValueError("development evaluation cannot inspect the Bench allocation")
    try:
        import stable_baselines3 as sb3
        from stable_baselines3.common.utils import set_random_seed
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("install ChemWorld with the 'rl' extra to evaluate PPO or SAC") from exc

    model_class = sb3.PPO if algorithm == "ppo" else sb3.SAC
    set_random_seed(policy_seed)
    model = model_class.load(Path(checkpoint))
    env = build_rl_environment(
        task_id=task_id,
        allocation=allocation,
        sampler_seed=sampler_seed,
        operation_budget=operation_budget,
        training_reward=False,
    )
    episode_cards: list[dict[str, Any]] = []
    operation_counts: Counter[str] = Counter()
    try:
        for episode_index in range(episodes):
            observation, _ = env.reset()
            invalid = 0
            unsafe = 0
            high_cost = 0
            measurements = 0
            runtime_domain_failures = 0
            observation_domain_failures = 0
            final_scores: list[float] = []
            raw_return = 0.0
            steps_taken = 0
            for _step_index in range(operation_budget):
                action, _ = model.predict(observation, deterministic=deterministic)
                observation, reward, terminated, truncated, info = env.step(action)
                steps_taken += 1
                flags = info.get("constraint_flags", {})
                preconditions = info.get("preconditions", {})
                invalid += int(bool(flags.get("precondition_failed", False)))
                unsafe += int(bool(flags.get("unsafe_by_task_limit", False)))
                high_cost += int(bool(flags.get("high_cost", False)))
                measurements += int(info.get("operation_type") == "measure")
                runtime_domain_failures += int(
                    preconditions.get("runtime_domain_valid") is False
                )
                observation_domain_failures += int(
                    preconditions.get("observation_domain_valid") is False
                )
                operation_counts[str(info.get("operation_type", "unknown"))] += 1
                raw_return += float(reward)
                terminal = info.get("last_terminal_summary")
                if info.get("experiment_ended") and isinstance(terminal, dict):
                    final_scores.append(float(terminal["leaderboard_score"]))
                if terminated or truncated:
                    break
            episode_cards.append(
                {
                    "episode_index": episode_index,
                    "operation_count": steps_taken,
                    "invalid_action_count": invalid,
                    "unsafe_step_count": unsafe,
                    "high_cost_step_count": high_cost,
                    "measurement_count": measurements,
                    "runtime_domain_failure_count": runtime_domain_failures,
                    "observation_domain_failure_count": observation_domain_failures,
                    "complete_experiment_count": len(final_scores),
                    "final_scores": final_scores,
                    "best_final_score": max(final_scores) if final_scores else 0.0,
                    "raw_environment_return": raw_return,
                }
            )
    finally:
        env.close()

    total_steps = sum(int(card["operation_count"]) for card in episode_cards)
    completed = sum(int(card["complete_experiment_count"]) for card in episode_cards)
    completed_episodes = sum(
        int(int(card["complete_experiment_count"]) > 0) for card in episode_cards
    )
    scores = [
        float(score)
        for card in episode_cards
        for score in card["final_scores"]
    ]
    return {
        "schema_version": "chemworld-rl-development-evaluation-0.1",
        "formal_evidence": False,
        "allocation": allocation.public_manifest(),
        "algorithm": algorithm,
        "task_id": task_id,
        "episodes": episodes,
        "operation_budget_per_episode": operation_budget,
        "sampler_seed": sampler_seed,
        "policy_seed": policy_seed,
        "policy_mode": "deterministic" if deterministic else "stochastic_frozen_seed",
        "training_reward_used": False,
        "episode_cards": episode_cards,
        "summary": {
            "operation_count": total_steps,
            "complete_experiment_count": completed,
            "episode_completion_rate": completed_episodes / episodes,
            "complete_experiments_per_episode": completed / episodes,
            "invalid_action_rate": sum(
                int(card["invalid_action_count"]) for card in episode_cards
            )
            / total_steps,
            "unsafe_step_rate": sum(
                int(card["unsafe_step_count"]) for card in episode_cards
            )
            / total_steps,
            "high_cost_step_rate": sum(
                int(card["high_cost_step_count"]) for card in episode_cards
            )
            / total_steps,
            "mean_final_score": statistics.fmean(scores) if scores else 0.0,
            "mean_episode_best_score": statistics.fmean(
                float(card["best_final_score"]) for card in episode_cards
            ),
            "runtime_domain_failure_count": sum(
                int(card["runtime_domain_failure_count"]) for card in episode_cards
            ),
            "observation_domain_failure_count": sum(
                int(card["observation_domain_failure_count"]) for card in episode_cards
            ),
            "operation_counts": dict(sorted(operation_counts.items())),
        },
        "claim_boundary": (
            "Dev-only checkpoint selection diagnostic; no replay trajectory or Bench result, "
            "therefore not benchmark evidence."
        ),
    }


__all__ = ["evaluate_sb3_checkpoint"]
