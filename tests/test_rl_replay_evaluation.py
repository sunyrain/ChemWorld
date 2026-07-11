from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
import pytest
from scripts.run_rl_replay_development import load_protocol

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.agents.interaction import build_decision_context
from chemworld.agents.rl import FrozenSB3Agent, build_frozen_rl_observation
from chemworld.data.logging import to_builtin
from chemworld.rl.environment import (
    RLWorldAllocation,
    build_rl_environment,
    load_rl_protocol,
)
from chemworld.rl.evaluation import evaluate_replay_verified_sb3_checkpoint
from chemworld.wrappers import ContinuousEventActionWrapper, decode_continuous_event_action


def _allocation(task_id: str) -> RLWorldAllocation:
    protocol = load_rl_protocol("configs/benchmark/confirmatory_freeze_vnext.json")
    return RLWorldAllocation.from_protocol(protocol, task_id=task_id, name="train")


def test_replay_development_protocol_is_standard_seed_only_and_nonclaiming() -> None:
    protocol = load_protocol()
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["evaluation"]["world_family_allocation"] is None
    assert protocol["evidence_policy"]["exact_replay_required"] is True
    assert protocol["evidence_policy"]["failed_runs_retained_with_fail_closed_zero_endpoint"]


def test_public_view_rebuilds_exact_training_observation() -> None:
    task_id = "flow-reaction-optimization"
    env = build_rl_environment(
        task_id=task_id,
        allocation=_allocation(task_id),
        sampler_seed=7,
        operation_budget=5,
    )
    try:
        wrapped_observation, _ = env.reset()
        base = env.unwrapped
        raw_observation = base._last_observation
        raw_info = base._last_info
        public_view = agent_view_bundle(base, raw_observation, raw_info)
        context = build_decision_context(
            step=1,
            task_info=base.task_info(),
            campaign_state=base.campaign_state(),
            public_view=public_view,
            previous_event_type=None,
        )
        rebuilt, operation_mask = build_frozen_rl_observation(public_view, context)
        assert rebuilt == pytest.approx(wrapped_observation)
        assert sum(operation_mask) == len(context.available_operations)
    finally:
        env.close()


def test_pure_decoder_matches_gym_action_wrapper() -> None:
    env = ContinuousEventActionWrapper(
        gym.make("ChemWorld", task_id="flow-reaction-optimization")
    )
    try:
        env.reset(seed=3)
        vector = np.linspace(-1.0, 1.0, 49, dtype=np.float32)
        mask = list(env.unwrapped.operation_validator.action_mask(env.unwrapped._state))
        decoded = decode_continuous_event_action(
            vector,
            event_action_space=env.event_action_space,
            operation_mask=mask,
        )
        assert to_builtin(decoded) == to_builtin(env.action(vector))
    finally:
        env.close()


def test_checkpoint_digest_mismatch_fails_before_policy_load(tmp_path: Path) -> None:
    checkpoint = tmp_path / "policy.zip"
    checkpoint.write_bytes(b"not-a-checkpoint")
    manifest = {
        "schema_version": "chemworld-rl-checkpoint-0.1",
        "algorithm": "ppo",
        "task_id": "flow-reaction-optimization",
        "checkpoint_sha256": "0" * 64,
    }
    with pytest.raises(ValueError, match="digest"):
        FrozenSB3Agent(
            algorithm="ppo",
            checkpoint=checkpoint,
            checkpoint_manifest=manifest,
            task_id="flow-reaction-optimization",
        )


def test_frozen_policy_produces_official_replay_verified_trajectory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sb3 = pytest.importorskip("stable_baselines3")
    task_id = "flow-reaction-optimization"
    shape_env = build_rl_environment(
        task_id=task_id,
        allocation=_allocation(task_id),
        sampler_seed=1,
        operation_budget=3,
    )
    observation_space = shape_env.observation_space
    shape_env.close()

    class FakeModel:
        def __init__(self) -> None:
            self.observation_space = observation_space

        def set_random_seed(self, seed: int) -> None:
            self.seed = seed

        def predict(
            self, observation: np.ndarray, *, deterministic: bool
        ) -> tuple[np.ndarray, None]:
            del observation, deterministic
            return np.zeros(49, dtype=np.float32), None

    monkeypatch.setattr(sb3.PPO, "load", lambda *args, **kwargs: FakeModel())
    checkpoint = tmp_path / "policy.zip"
    checkpoint.write_bytes(b"frozen-policy-fixture")
    digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-rl-checkpoint-0.1",
        "algorithm": "ppo",
        "task_id": task_id,
        "checkpoint_sha256": digest,
        "training_environment_step_count": 8,
        "cpu_time_s": 0.1,
        "gpu_time_s": 0.0,
        "allocation": {"name": "train"},
        "versions": {"stable_baselines3": sb3.__version__},
    }
    report = evaluate_replay_verified_sb3_checkpoint(
        algorithm="ppo",
        checkpoint=checkpoint,
        checkpoint_manifest=manifest,
        task_id=task_id,
        seeds=[1180],
        operation_budget=3,
        output_dir=tmp_path / "evaluation",
        policy_seed=50,
    )
    assert report["all_replay_verified"] is True
    assert report["formal_evidence"] is False
    result = report["results"][0]
    assert result["resource_usage"]["training_environment_step_count"] == 8
    assert result["rl_evaluation"]["world_family_allocation"] is None
    layered = result["score_replay"]["layered_evaluation"]
    assert layered["status"] == "failed_no_successful_final_assay"
    assert layered["objective"]["best"] == 0.0
    assert layered["resources"]["incomplete_experiment_count"] == 1
