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
from chemworld.wrappers import ContinuousEventActionWrapper, RLTrainingRewardWrapper


def _allocation(task_id: str, name: str = "train") -> RLWorldAllocation:
    return RLWorldAllocation.from_protocol(
        load_rl_protocol(FREEZE_PROTOCOL),
        task_id=task_id,
        name=name,  # type: ignore[arg-type]
    )


def test_continuous_action_adapter_has_stationary_fixed_semantics() -> None:
    env = ContinuousEventActionWrapper(gym.make("ChemWorld", task_id="partition-discovery"))
    try:
        env.reset(seed=0)
        assert env.action_space.shape == (49,)
        assert env.action_contract()["action_keys"] == list(env.event_action_space.spaces)
        assert env.action_contract()["operation_types"] == list(env.operation_types)
        add_reagent = np.full(49, -1.0, dtype=np.float32)
        add_reagent[env.operation_types.index("add_reagent")] = 1.0
        decoded = env.action(add_reagent)
        assert decoded["operation"] == env.operation_types.index("add_reagent")
        impossible = np.full(49, -1.0, dtype=np.float32)
        impossible[env.operation_types.index("cool_crystallize")] = 1.0
        masked = env.action(impossible)
        assert masked["operation"] != env.operation_types.index("cool_crystallize")
        low = env.action(np.full(49, -1.0, dtype=np.float32))
        assert float(low["potential_V"][0]) == pytest.approx(-3.0)
        high_parameters = np.ones(49, dtype=np.float32)
        high = env.action(high_parameters)
        assert float(high["potential_V"][0]) == pytest.approx(3.0)
        with pytest.raises(ValueError, match="finite vector"):
            env.action(np.full(49, np.nan, dtype=np.float32))
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


def test_domain_invalid_exploration_is_retained_instead_of_crashing_training(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=3)
    try:
        env.reset(seed=0)
        base = env.unwrapped

        def reject_domain_action(state: object, action: object) -> None:
            raise ValueError("private domain detail must not escape")

        monkeypatch.setattr(base.runtime, "apply_transaction", reject_domain_action)
        observation, reward, terminated, truncated, info = env.step(
            {
                "operation": "add_reagent",
                "amount_mol": 0.01,
            }
        )
        assert env.observation_space.contains(observation)
        assert np.isfinite(reward)
        assert terminated is False
        assert truncated is False
        assert info["transaction_status"] == "validation_failed"
        assert info["constraint_flags"]["precondition_failed"] is True
        assert info["preconditions"]["runtime_domain_valid"] is False
        assert "private domain detail" not in str(info)
    finally:
        env.close()


def test_observation_domain_failure_rolls_back_and_remains_replayable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=2)
    try:
        env.reset(seed=0)
        base = env.unwrapped

        def reject_observation(state: object, action: object, rng: object) -> None:
            raise ValueError("private solver detail must not escape")

        monkeypatch.setattr(base.observation_kernel, "observe", reject_observation)
        observation, reward, terminated, truncated, info = env.step(
            {"operation": "add_reagent", "amount_mol": 0.01}
        )
        assert env.observation_space.contains(observation)
        assert np.isfinite(reward)
        assert terminated is False
        assert truncated is False
        assert info["transaction_status"] == "validation_failed"
        assert info["preconditions"]["observation_domain_valid"] is False
        assert info["constraint_flags"]["precondition_failed"] is True
        assert "private solver detail" not in str(info)
    finally:
        env.close()


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


def test_training_reward_uses_public_failures_without_changing_raw_environment() -> None:
    env = RLTrainingRewardWrapper(
        gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=2)
    )
    try:
        env.reset(seed=0)
        _, shaped, _, _, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 280.0,
                "duration_s": 100.0,
            }
        )
        assert shaped == pytest.approx(-0.25)
        assert info["rl_training_reward"]["raw_reward"] == 0.0
        assert info["rl_training_reward"]["invalid_action"] is True
        contract = env.reward_contract()
        assert contract["public_signals_only"] is True
        assert contract["benchmark_evaluation_uses_shaped_reward"] is False
        diagnostics = env.training_diagnostics()
        assert diagnostics["invalid_action_count"] == 1
        assert diagnostics["invalid_action_rate"] == 1.0
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
