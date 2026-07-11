from __future__ import annotations

from pathlib import Path

import gymnasium as gym
import numpy as np
import pytest
from scripts.audit_rl_baselines import FREEZE_PROTOCOL, RL_PROTOCOL, build_report

import chemworld  # noqa: F401
from chemworld.rl.environment import (
    RLWorldAllocation,
    TrainWorldFamilyWrapper,
    build_rl_environment,
    load_rl_protocol,
)
from chemworld.wrappers import ContinuousEventActionWrapper


def _allocation(task_id: str, name: str = "train") -> RLWorldAllocation:
    return RLWorldAllocation.from_protocol(
        load_rl_protocol(FREEZE_PROTOCOL),
        task_id=task_id,
        name=name,  # type: ignore[arg-type]
    )


def test_continuous_action_adapter_has_stationary_fixed_semantics() -> None:
    env = ContinuousEventActionWrapper(gym.make("ChemWorld", task_id="partition-discovery"))
    try:
        assert env.action_space.shape == (22,)
        assert env.action_contract()["action_keys"] == list(env.event_action_space.spaces)
        low = env.action(np.full(22, -1.0, dtype=np.float32))
        high = env.action(np.full(22, 1.0, dtype=np.float32))
        assert low["operation"] == 0
        assert high["operation"] == env.event_action_space["operation"].n - 1
        assert float(low["potential_V"][0]) == pytest.approx(-3.0)
        assert float(high["potential_V"][0]) == pytest.approx(3.0)
        with pytest.raises(ValueError, match="finite vector"):
            env.action(np.full(22, np.nan, dtype=np.float32))
    finally:
        env.close()


def test_train_wrapper_never_accepts_bench_allocation() -> None:
    base = gym.make("ChemWorld", task_id="partition-discovery")
    try:
        with pytest.raises(ValueError, match="Bench allocation"):
            TrainWorldFamilyWrapper(
                base, allocation=_allocation("partition-discovery", "bench"), sampler_seed=0
            )
    finally:
        base.close()


def test_rl_environment_is_finite_and_resamples_only_train_cells() -> None:
    allocation = _allocation("flow-reaction-optimization")
    env = build_rl_environment(
        task_id=allocation.task_id,
        allocation=allocation,
        sampler_seed=4,
        operation_budget=3,
    )
    try:
        seen = []
        for _ in range(5):
            observation, info = env.reset()
            seen.append(info["rl_world_cell"])
            assert env.observation_space.contains(observation)
            assert np.all(np.isfinite(observation))
        assert all(item["allocation"] == "train" for item in seen)
        assert all(len(item["opaque_cell_id"]) == 16 for item in seen)
        assert all(item["axis_identity_visible"] is False for item in seen)
        assert all("world_seed" not in item and "axis_id" not in item for item in seen)
    finally:
        env.close()


def test_rl_protocol_keeps_formal_claims_closed() -> None:
    protocol = load_rl_protocol(RL_PROTOCOL)
    assert protocol["publication_ready"] is False
    assert protocol["benchmark_claim_allowed"] is False
    report = build_report()
    assert report["controls_ready"] is True
    assert report["formal_training_complete"] is False
    assert report["publication_ready"] is False


def test_rl_extra_is_declared_without_becoming_core_dependency() -> None:
    pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "rl = [" in pyproject
    assert '"stable-baselines3>=2.9,<3.0"' in pyproject
