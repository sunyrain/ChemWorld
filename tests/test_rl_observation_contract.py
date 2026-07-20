from __future__ import annotations

import hashlib
import json

import gymnasium as gym
import numpy as np
import pytest

from chemworld.rl.environment import (
    RLWorldAllocation,
    build_rl_environment,
    load_rl_protocol,
)
from chemworld.rl.observation_contract import (
    OBSERVATION_CONTRACT_SCHEMA_VERSION,
    rl_observation_contract,
)
from chemworld.rl.rewards import core_operation_requirements
from chemworld.tasks import get_task
from chemworld.world.operations import OPERATION_TYPES
from chemworld.wrappers import action_mask

FORMAL_RL_TASK_IDS = (
    "partition-discovery",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)


def _allocation(task_id: str) -> RLWorldAllocation:
    protocol = load_rl_protocol("configs/benchmark/confirmatory_freeze_vnext.json")
    return RLWorldAllocation.from_protocol(protocol, task_id=task_id, name="train")


def _canonical_hash(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_observation_contract_hash_is_canonical_and_task_specific() -> None:
    contracts = [rl_observation_contract(task_id) for task_id in FORMAL_RL_TASK_IDS]
    for contract in contracts:
        digest = contract["contract_hash"]
        unhashed = dict(contract)
        unhashed.pop("contract_hash")
        assert contract["schema_version"] == OBSERVATION_CONTRACT_SCHEMA_VERSION
        assert digest == _canonical_hash(unhashed)
        assert len(str(digest)) == 64
        assert contract == rl_observation_contract(str(contract["task_id"]))
        assert contract["compatibility_policy"]["shape_only_compatible"] is False
    assert len({contract["contract_hash"] for contract in contracts}) == len(contracts)


@pytest.mark.parametrize("task_id", FORMAL_RL_TASK_IDS)
def test_observation_contract_matches_real_training_space_and_reset_vector(
    task_id: str,
) -> None:
    contract = rl_observation_contract(task_id)
    env = build_rl_environment(
        task_id=task_id,
        allocation=_allocation(task_id),
        sampler_seed=29,
        operation_budget=7,
        training_reward=True,
    )
    try:
        observation, info = env.reset()
        assert isinstance(env.observation_space, gym.spaces.Box)
        assert list(env.observation_space.shape or ()) == contract["shape"]
        np.testing.assert_array_equal(
            env.observation_space.low,
            np.asarray(contract["vector_bounds"]["low"], dtype=np.float32),
        )
        np.testing.assert_array_equal(
            env.observation_space.high,
            np.asarray(contract["vector_bounds"]["high"], dtype=np.float32),
        )
        assert env.observation_space.contains(observation)

        segments = contract["segments"]
        assert [segment["name"] for segment in segments] == contract["concatenation_order"]
        assert [segment["start"] for segment in segments] == [
            0,
            *[segment["stop_exclusive"] for segment in segments[:-1]],
        ]
        assert segments[-1]["stop_exclusive"] == len(contract["vector_keys"])

        by_name = {segment["name"]: segment for segment in segments}

        def values(name: str) -> np.ndarray:
            segment = by_name[name]
            return observation[segment["start"] : segment["stop_exclusive"]]

        np.testing.assert_array_equal(
            values("public_values"),
            np.asarray(info["rl_view"]["vector"], dtype=np.float32),
        )
        np.testing.assert_array_equal(
            values("public_observed_mask"),
            np.asarray(info["rl_view"]["mask"], dtype=np.float32),
        )
        np.testing.assert_array_equal(
            values("core_operation_progress"),
            np.asarray(info["rl_core_progress"]["satisfied"], dtype=np.float32),
        )
        np.testing.assert_array_equal(
            values("operation_affordance_mask"),
            np.asarray(action_mask(env), dtype=np.float32),
        )
        np.testing.assert_array_equal(
            values("campaign_progress"),
            np.asarray([0.0, 1.0, 0.0], dtype=np.float32),
        )
    finally:
        env.close()


@pytest.mark.parametrize("task_id", FORMAL_RL_TASK_IDS)
def test_observation_contract_freezes_public_progress_and_affordance_order(
    task_id: str,
) -> None:
    contract = rl_observation_contract(task_id)
    progress = contract["core_operation_progress"]
    assert progress["requirements"] == [
        list(group)
        for group in core_operation_requirements(
            get_task(task_id).allowed_operations, task_id=task_id
        )
    ]
    assert progress["invalid_precondition_updates_progress"] is False
    assert progress["reset"] == ("after experiment_ended and at environment or agent reset")
    assert contract["operation_affordance_mask"]["operation_order"] == list(OPERATION_TYPES)
    assert contract["vector_keys"][-3:] == [
        "operation_budget_fraction_used",
        "operation_budget_fraction_remaining",
        "completed_experiment_summary_ratio",
    ]
