"""Reproducible development evaluation for frozen SB3 checkpoints."""

from __future__ import annotations

import hashlib
import json
import statistics
import time
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from chemworld.rl.environment import RLWorldAllocation, build_rl_environment
from chemworld.rl.hybrid_policy import policy_distribution_contract
from chemworld.rl.rewards import reward_contract
from chemworld.tasks import get_task

AlgorithmName = Literal["ppo", "sac"]


def _checkpoint_contract_manifest(checkpoint: Path) -> dict[str, Any]:
    path = checkpoint.with_suffix(".manifest.json")
    if not path.is_file():
        raise ValueError(
            "RL checkpoint is missing its contract manifest; legacy checkpoints are incompatible"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("RL checkpoint contract manifest must be a JSON object")
    return payload


def _environment_action_contract(env: Any) -> dict[str, Any]:
    current = env
    while current is not None:
        factory = getattr(current, "action_contract", None)
        if callable(factory):
            return dict(factory())
        current = getattr(current, "env", None)
    raise ValueError("RL evaluation environment is missing its action contract")


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

    checkpoint_path = Path(checkpoint)
    env = build_rl_environment(
        task_id=task_id,
        allocation=allocation,
        sampler_seed=sampler_seed,
        operation_budget=operation_budget,
        training_reward=False,
    )
    contract_manifest = _checkpoint_contract_manifest(checkpoint_path)
    if contract_manifest.get("schema_version") not in {
        "chemworld-rl-checkpoint-0.2",
        "chemworld-rl-checkpoint-contract-sidecar-0.1",
    }:
        env.close()
        raise ValueError("unsupported RL checkpoint contract manifest")
    expected_action = _environment_action_contract(env)
    expected_reward = reward_contract(get_task(task_id).allowed_operations)
    parameter_keys = tuple(
        str(item)
        for item in expected_action["training_adapter"]["parameter_coordinate_keys"]
    )
    expected_policy_distribution = policy_distribution_contract(parameter_keys)
    digest = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
    compatibility = {
        "checkpoint_digest": contract_manifest.get("checkpoint_sha256") == digest,
        "algorithm": contract_manifest.get("algorithm") == algorithm,
        "task": contract_manifest.get("task_id") == task_id,
        "action_contract": contract_manifest.get("action_contract_hash")
        == expected_action["contract_hash"],
        "reward_contract": contract_manifest.get("training_reward_contract_hash")
        == expected_reward["contract_hash"],
        "policy_distribution_contract": algorithm != "ppo"
        or contract_manifest.get("policy_distribution_contract_hash")
        == expected_policy_distribution["contract_hash"],
    }
    if not all(compatibility.values()):
        env.close()
        failed = sorted(key for key, passed in compatibility.items() if not passed)
        raise ValueError(f"RL checkpoint contract is incompatible: {', '.join(failed)}")
    model_class = sb3.PPO if algorithm == "ppo" else sb3.SAC
    set_random_seed(policy_seed)
    model = model_class.load(checkpoint_path)
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
        "checkpoint_contract_compatibility": compatibility,
        "action_contract_hash": expected_action["contract_hash"],
        "training_reward_contract_hash": expected_reward["contract_hash"],
        "policy_distribution_contract_hash": expected_policy_distribution[
            "contract_hash"
        ],
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


def evaluate_replay_verified_sb3_checkpoint(
    *,
    algorithm: AlgorithmName,
    checkpoint: str | Path,
    checkpoint_manifest: str | Path | dict[str, Any],
    task_id: str,
    seeds: list[int],
    operation_budget: int,
    output_dir: str | Path,
    policy_seed: int,
    deterministic: bool = False,
) -> dict[str, Any]:
    """Evaluate a frozen policy through official logging and exact action replay.

    This bridge intentionally uses ordinary registered task seeds.  World-family
    Dev/Bench cells require a separate intervention-bound replay contract and
    are not silently represented as standard trajectories here.
    """

    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("replay evaluation seeds must be non-empty and unique")
    if operation_budget <= 0:
        raise ValueError("operation_budget must be positive")
    from chemworld.agents.rl import FrozenSB3Agent
    from chemworld.data.logging import load_jsonl
    from chemworld.eval.result_artifacts import (
        build_verified_evaluation_result,
        validate_verified_evaluation_result,
    )
    from chemworld.eval.runner import run_agent

    root = Path(output_dir)
    trajectory_dir = root / "trajectories"
    result_dir = root / "results"
    trajectory_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for seed in seeds:
        trajectory_path = trajectory_dir / f"{algorithm}_{task_id}_seed{seed}.jsonl"
        agent = FrozenSB3Agent(
            algorithm=algorithm,
            checkpoint=checkpoint,
            checkpoint_manifest=checkpoint_manifest,
            task_id=task_id,
            deterministic=deterministic,
            policy_seed=policy_seed + seed,
        )
        wall_started = time.perf_counter()
        cpu_started = time.process_time()
        run_agent(
            env_id="ChemWorld",
            agent=agent,
            world_split="public-dev",
            budget=operation_budget,
            objective="balanced",
            seed=seed,
            task_id=task_id,
            output_path=trajectory_path,
            budget_override=operation_budget,
            episode_mode_override="campaign",
        )
        run_wall_time = time.perf_counter() - wall_started
        records = load_jsonl(trajectory_path)
        evaluation_started = time.perf_counter()
        result = build_verified_evaluation_result(
            records,
            trajectory_path=trajectory_path,
        )
        evaluation_wall_time = time.perf_counter() - evaluation_started
        result["resource_usage"] = _replay_resource_usage(
            records=records,
            result=result,
            run_wall_time_s=run_wall_time,
            evaluation_wall_time_s=evaluation_wall_time,
            process_cpu_time_s=time.process_time() - cpu_started,
        )
        result["rl_evaluation"] = {
            "schema_version": "chemworld-rl-replay-evaluation-0.1",
            "algorithm": algorithm,
            "policy_mode": (
                "deterministic" if deterministic else "stochastic_frozen_seed"
            ),
            "policy_seed": policy_seed + seed,
            "training_reward_used": False,
            "standard_registered_task_seed": True,
            "world_family_allocation": None,
            "formal_evidence": False,
        }
        result_path = result_dir / f"{algorithm}_{task_id}_seed{seed}.json"
        result["result_path"] = str(result_path.resolve())
        validate_verified_evaluation_result(result, replay=True)
        result_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        results.append(result)
    manifest = {
        "schema_version": "chemworld-rl-replay-evaluation-report-0.1",
        "algorithm": algorithm,
        "task_id": task_id,
        "seed_count": len(seeds),
        "seeds": list(seeds),
        "operation_budget": operation_budget,
        "policy_mode": "deterministic" if deterministic else "stochastic_frozen_seed",
        "all_replay_verified": all(result["verified"] is True for result in results),
        "result_count": len(results),
        "results": results,
        "formal_evidence": False,
        "claim_boundary": (
            "Replay-verified standard-seed development evidence only; this does not execute "
            "the frozen world-family Dev or Bench allocation and cannot support an RL ranking."
        ),
    }
    (root / "evaluation_report.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def _replay_resource_usage(
    *,
    records: list[dict[str, Any]],
    result: dict[str, Any],
    run_wall_time_s: float,
    evaluation_wall_time_s: float,
    process_cpu_time_s: float,
) -> dict[str, Any]:
    ledger = records[-1].get("method_resources", {})
    if ledger.get("schema_version") != "chemworld-method-resource-ledger-0.1":
        raise ValueError("RL trajectory is missing the method resource ledger")
    if ledger.get("accounting_complete") is not True:
        raise ValueError("RL trajectory resource accounting is incomplete")
    if int(ledger.get("operation_count", -1)) != int(result["steps"]):
        raise ValueError("RL resource ledger does not match verified operations")
    if int(ledger.get("complete_experiment_count", -1)) != int(result["final_assay_count"]):
        raise ValueError("RL resource ledger does not match verified experiments")
    usage = ledger.get("agent_usage", {})
    return {
        "schema_version": "chemworld-resource-usage-0.2",
        "run_wall_time_s": float(ledger["run_wall_time_s"]),
        "orchestration_wall_time_s": run_wall_time_s,
        "evaluation_wall_time_s": evaluation_wall_time_s,
        "total_wall_time_s": run_wall_time_s + evaluation_wall_time_s,
        "process_cpu_time_s": process_cpu_time_s,
        "step_count": int(ledger["operation_count"]),
        "complete_experiment_count": int(ledger["complete_experiment_count"]),
        "model_call_count": 0,
        "input_token_count": 0,
        "output_token_count": 0,
        "monetary_cost_usd": 0.0,
        "training_environment_step_count": int(
            usage.get("training_environment_step_count", 0)
        ),
        "cpu_time_s": float(usage.get("cpu_time_s", 0.0)),
        "gpu_time_s": float(usage.get("gpu_time_s", 0.0)),
        "method_ledger": ledger,
    }


__all__ = ["evaluate_replay_verified_sb3_checkpoint", "evaluate_sb3_checkpoint"]
