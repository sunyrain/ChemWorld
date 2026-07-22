from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import gymnasium as gym
import numpy as np
import pytest

from chemworld.agents.rl import RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION
from chemworld.rl.environment import (
    RLWorldAllocation,
    build_rl_environment,
    load_rl_protocol,
)
from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.rl.hybrid_actions import (
    conditional_hybrid_action_contract,
    policy_distribution_contract,
)
from chemworld.rl.observation_contract import rl_observation_contract
from chemworld.rl.rewards import reward_contract
from chemworld.tasks import get_task


def _dev_allocation(task_id: str) -> RLWorldAllocation:
    protocol = load_rl_protocol("configs/benchmark/rl_world_allocations.json")
    return RLWorldAllocation.from_protocol(protocol, task_id=task_id, name="dev")


def _sidecar(checkpoint: Path, *, observation_contract_hash: str) -> dict[str, object]:
    task_id = "flow-reaction-optimization"
    allocation = _dev_allocation(task_id)
    env = build_rl_environment(
        task_id=task_id,
        allocation=allocation,
        sampler_seed=0,
        operation_budget=2,
    )
    try:
        event_action_space = cast(gym.spaces.Dict, env.unwrapped.action_space)
        action_contract = conditional_hybrid_action_contract(event_action_space)
    finally:
        env.close()
    parameter_keys = tuple(
        action_contract["training_adapter"]["parameter_coordinate_keys"]
    )
    return {
        "schema_version": RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
        "algorithm": "ppo",
        "task_id": task_id,
        "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "observation_contract_hash": observation_contract_hash,
        "action_contract_hash": action_contract["contract_hash"],
        "training_reward_contract_hash": reward_contract(
            get_task(task_id).allowed_operations
        )["contract_hash"],
        "policy_distribution_contract_hash": policy_distribution_contract(parameter_keys)[
            "contract_hash"
        ],
    }


def test_dev_evaluator_rejects_observation_drift_before_policy_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sb3 = pytest.importorskip("stable_baselines3")
    checkpoint = tmp_path / "policy.zip"
    checkpoint.write_bytes(b"checkpoint-fixture")
    sidecar = _sidecar(checkpoint, observation_contract_hash="0" * 64)
    checkpoint.with_suffix(".manifest.json").write_text(
        json.dumps(sidecar), encoding="utf-8"
    )

    def unexpected_load(*args: object, **kwargs: object) -> object:
        raise AssertionError("observation-incompatible checkpoint was deserialized")

    monkeypatch.setattr(sb3.PPO, "load", unexpected_load)
    with pytest.raises(ValueError, match="observation_contract"):
        evaluate_sb3_checkpoint(
            algorithm="ppo",
            checkpoint=checkpoint,
            task_id="flow-reaction-optimization",
            allocation=_dev_allocation("flow-reaction-optimization"),
            episodes=1,
            operation_budget=2,
            sampler_seed=0,
            policy_seed=0,
            deterministic=False,
        )


def test_dev_evaluator_rejects_legacy_sidecar_before_policy_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sb3 = pytest.importorskip("stable_baselines3")
    checkpoint = tmp_path / "policy.zip"
    checkpoint.write_bytes(b"checkpoint-fixture")
    sidecar = _sidecar(checkpoint, observation_contract_hash="0" * 64)
    sidecar["schema_version"] = "chemworld-rl-checkpoint-contract-sidecar-0.1"
    checkpoint.with_suffix(".manifest.json").write_text(
        json.dumps(sidecar), encoding="utf-8"
    )

    def unexpected_load(*args: object, **kwargs: object) -> object:
        raise AssertionError("legacy checkpoint was deserialized")

    monkeypatch.setattr(sb3.PPO, "load", unexpected_load)
    with pytest.raises(ValueError, match="unsupported RL checkpoint contract manifest"):
        evaluate_sb3_checkpoint(
            algorithm="ppo",
            checkpoint=checkpoint,
            task_id="flow-reaction-optimization",
            allocation=_dev_allocation("flow-reaction-optimization"),
            episodes=1,
            operation_budget=2,
            sampler_seed=0,
            policy_seed=0,
            deterministic=False,
        )


def test_dev_evaluator_rejects_model_observation_bounds_after_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sb3 = pytest.importorskip("stable_baselines3")
    task_id = "flow-reaction-optimization"
    checkpoint = tmp_path / "policy.zip"
    checkpoint.write_bytes(b"checkpoint-fixture")
    observation_contract = rl_observation_contract(task_id)
    sidecar = _sidecar(
        checkpoint,
        observation_contract_hash=observation_contract["contract_hash"],
    )
    checkpoint.with_suffix(".manifest.json").write_text(
        json.dumps(sidecar), encoding="utf-8"
    )

    class ModelWithDriftedBounds:
        observation_space = gym.spaces.Box(
            low=-2.0,
            high=1.0,
            shape=tuple(observation_contract["shape"]),
            dtype=np.float32,
        )

    monkeypatch.setattr(
        sb3.PPO,
        "load",
        lambda *args, **kwargs: ModelWithDriftedBounds(),
    )
    with pytest.raises(ValueError, match="observation bounds"):
        evaluate_sb3_checkpoint(
            algorithm="ppo",
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=_dev_allocation(task_id),
            episodes=1,
            operation_budget=2,
            sampler_seed=0,
            policy_seed=0,
            deterministic=False,
        )
