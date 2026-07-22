from __future__ import annotations

import pytest
from scripts.run_rl_interaction_development import (
    development_gate_passed,
    load_development_protocol,
)

from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol
from chemworld.rl.evaluation import evaluate_sb3_checkpoint


def test_development_protocol_is_train_dev_only_and_nonclaiming() -> None:
    protocol = load_development_protocol()
    assert protocol["training"]["allocation"] == "train"
    assert protocol["evaluation"]["allocation"] == "dev"
    assert protocol["training"]["action_contract_schema"] == (
        "chemworld-conditional-hybrid-action-0.8"
    )
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["publication_ready"] is False


def test_development_gate_requires_completion_and_low_invalid_rate() -> None:
    gate = load_development_protocol()["development_gate"]
    assert development_gate_passed(
        {"invalid_action_rate": 0.05, "episode_completion_rate": 0.75}, gate=gate
    )
    assert not development_gate_passed(
        {"invalid_action_rate": 0.20, "episode_completion_rate": 0.75}, gate=gate
    )
    assert not development_gate_passed(
        {"invalid_action_rate": 0.05, "episode_completion_rate": 0.25}, gate=gate
    )


def test_checkpoint_selection_evaluator_rejects_train_and_bench() -> None:
    freeze = load_rl_protocol("configs/benchmark/confirmatory_freeze_vnext.json")
    for allocation_name in ("train", "bench"):
        allocation = RLWorldAllocation.from_protocol(
            freeze,
            task_id="flow-reaction-optimization",
            name=allocation_name,  # type: ignore[arg-type]
        )
        with pytest.raises(ValueError, match=r"Train|Bench"):
            evaluate_sb3_checkpoint(
                algorithm="ppo",
                checkpoint="missing.zip",
                task_id="flow-reaction-optimization",
                allocation=allocation,
                episodes=1,
                operation_budget=1,
                sampler_seed=0,
                policy_seed=0,
                deterministic=False,
            )
