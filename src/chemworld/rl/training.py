"""Stable-Baselines3 training entry point with checkpoint provenance."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter, process_time
from typing import Any, Literal

from chemworld.rl.environment import RLWorldAllocation, build_rl_environment

AlgorithmName = Literal["ppo", "sac"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _action_contract(env: Any) -> dict[str, Any]:
    current = env
    while current is not None:
        factory = getattr(current, "action_contract", None)
        if callable(factory):
            return dict(factory())
        current = getattr(current, "env", None)
    raise RuntimeError("RL environment is missing its continuous action contract")


def _optional_wrapper_payload(env: Any, method: str) -> dict[str, Any] | None:
    current = env
    while current is not None:
        factory = getattr(current, method, None)
        if callable(factory):
            return dict(factory())
        current = getattr(current, "env", None)
    return None


def train_sb3_baseline(
    *,
    algorithm: AlgorithmName,
    task_id: str,
    allocation: RLWorldAllocation,
    total_timesteps: int,
    model_seed: int,
    output_dir: str | Path,
    algorithm_kwargs: dict[str, Any] | None = None,
    operation_budget: int | None = None,
    checkpoint_interval_steps: int | None = None,
    save_replay_buffer: bool = False,
) -> dict[str, Any]:
    """Train one baseline and retain the model plus a complete compute manifest."""

    if algorithm not in {"ppo", "sac"}:
        raise ValueError("algorithm must be ppo or sac")
    if total_timesteps <= 0:
        raise ValueError("total_timesteps must be positive")
    if checkpoint_interval_steps is not None and checkpoint_interval_steps <= 0:
        raise ValueError("checkpoint_interval_steps must be positive")
    if allocation.name != "train":
        raise ValueError("formal RL training accepts only the train allocation")
    try:
        import stable_baselines3 as sb3
        import torch
        from stable_baselines3.common.callbacks import CheckpointCallback
    except ImportError as exc:
        raise RuntimeError("install ChemWorld with the 'rl' extra to train PPO or SAC") from exc

    algorithm_class = sb3.PPO if algorithm == "ppo" else sb3.SAC
    env = build_rl_environment(
        task_id=task_id,
        allocation=allocation,
        sampler_seed=model_seed,
        operation_budget=operation_budget,
        training_reward=True,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    checkpoint_stem = output / f"{algorithm}-{task_id}-seed{model_seed}"
    periodic_dir = output / "checkpoints"
    action_contract = _action_contract(env)
    observation_shape = list(env.observation_space.shape or ())
    wall_started = perf_counter()
    cpu_started = process_time()
    try:
        callback = None
        if checkpoint_interval_steps is not None:
            periodic_dir.mkdir(parents=True, exist_ok=True)
            callback = CheckpointCallback(
                save_freq=checkpoint_interval_steps,
                save_path=str(periodic_dir),
                name_prefix=checkpoint_stem.name,
                save_replay_buffer=save_replay_buffer,
                save_vecnormalize=False,
            )
        model = algorithm_class(
            "MlpPolicy",
            env,
            seed=model_seed,
            verbose=0,
            device="auto",
            **dict(algorithm_kwargs or {}),
        )
        model.learn(
            total_timesteps=total_timesteps,
            progress_bar=False,
            callback=callback,
        )
        model.save(checkpoint_stem)
        actual_timesteps = int(model.num_timesteps)
        device = str(model.device)
        training_diagnostics = _optional_wrapper_payload(env, "training_diagnostics")
    finally:
        env.close()
    wall_time_s = perf_counter() - wall_started
    cpu_time_s = process_time() - cpu_started
    checkpoint = checkpoint_stem.with_suffix(".zip")
    if training_diagnostics is not None and int(
        training_diagnostics.get("step_count", -1)
    ) != actual_timesteps:
        raise RuntimeError("SB3 and environment training-step ledgers disagree")
    periodic_artifacts = [
        {
            "path": str(path.relative_to(output)),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256(path),
            "artifact_type": (
                "replay_buffer" if path.name.endswith("replay_buffer.pkl") else "checkpoint"
            ),
        }
        for path in sorted(periodic_dir.glob("*"))
        if path.is_file()
    ]
    manifest = {
        "schema_version": "chemworld-rl-checkpoint-0.1",
        "formal_evidence": False,
        "algorithm": algorithm,
        "task_id": task_id,
        "model_seed": model_seed,
        "allocation": allocation.public_manifest(),
        "action_contract": action_contract,
        "training_reward_contract": _optional_wrapper_payload(env, "reward_contract"),
        "training_diagnostics": training_diagnostics,
        "observation_shape": observation_shape,
        "requested_training_environment_step_count": total_timesteps,
        "training_environment_step_count": actual_timesteps,
        "step_budget_exact": actual_timesteps == total_timesteps,
        "checkpoint_interval_steps": checkpoint_interval_steps,
        "periodic_checkpoint_artifacts": periodic_artifacts,
        "replay_buffer_checkpointed": bool(save_replay_buffer),
        "operation_budget": operation_budget,
        "wall_time_s": wall_time_s,
        "cpu_time_s": cpu_time_s,
        "gpu_time_s": 0.0,
        "device": device,
        "checkpoint": checkpoint.name,
        "checkpoint_sha256": _sha256(checkpoint),
        "versions": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "stable_baselines3": sb3.__version__,
            "torch": torch.__version__,
        },
        "limitations": [
            "This checkpoint is diagnostic until the full frozen training budget is consumed.",
            (
                "Formal eligibility also requires replay-verified Bench evaluation "
                "and paired statistics."
            ),
        ],
    }
    manifest_path = checkpoint_stem.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


__all__ = ["train_sb3_baseline"]
