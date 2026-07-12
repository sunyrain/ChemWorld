from __future__ import annotations

import json
from pathlib import Path

import gymnasium as gym
import numpy as np
import torch as th
from scripts.benchmark_rl_infrastructure import candidate_matrix

import chemworld  # noqa: F401
from chemworld.rl.evaluation import _ExperimentBehaviorTracker
from chemworld.rl.hybrid_actions import (
    conditional_hybrid_action_contract,
    decode_conditional_hybrid_action,
)
from chemworld.rl.hybrid_policy import (
    ConditionalHybridDistribution,
    policy_distribution_contract,
)
from chemworld.rl.rewards import core_operation_requirements, reward_contract
from chemworld.tasks import get_task
from chemworld.world.operations import OPERATION_TYPES, operation_contracts
from chemworld.wrappers import RLTrainingRewardWrapper, action_mask

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs" / "foundation" / "rl_contract_vnext.json"
REPORT = (
    ROOT
    / "workstreams"
    / "world_foundation"
    / "reports"
    / "rl-contract-vnext.json"
)


def test_infrastructure_matrix_covers_cpu_cuda_and_vectorization_choices() -> None:
    cpu_only = candidate_matrix(cuda_available=False)
    assert len(cpu_only) == 5
    assert {item["device"] for item in cpu_only} == {"cpu"}
    full = candidate_matrix(cuda_available=True)
    assert len(full) == 10
    assert {item["device"] for item in full} == {"cpu", "cuda"}
    assert {
        (item["parallel_environments"], item["vectorization_backend"])
        for item in full
        if item["device"] == "cpu"
    } == {
        (1, "dummy"),
        (4, "dummy"),
        (8, "dummy"),
        (4, "subprocess"),
        (8, "subprocess"),
    }


def test_protocol_is_nonclaiming_and_keeps_native_distribution_gap_visible() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["action_contract"]["operation_semantics"] == "categorical"
    assert protocol["action_contract"]["stable_baselines_adapter"][
        "native_hybrid_distribution"
    ] is False
    assert protocol["action_contract"]["ppo_policy_distribution"][
        "native_hybrid_distribution"
    ] is True
    assert protocol["development_gate"]["training_seeds"] == [106, 107, 108, 109, 110]
    assert protocol["development_gate"]["dev_episodes_per_seed"] == 20
    assert protocol["development_gate"]["training_environment_step_checkpoints"] == [
        25600,
        51200,
        102400,
    ]
    assert protocol["development_gate"]["training_operation_budget"] == 60
    assert protocol["evidence_policy"][
        "post_result_reward_or_hyperparameter_tuning_allowed"
    ] is False
    assert protocol["world_foundation_preconditions"]["formal_training_allowed"] is False
    assert protocol["training_infrastructure"]["device_must_be_explicit"] is True


def test_dev_behavior_tracker_requires_core_flow_and_final_assay_per_experiment() -> None:
    tracker = _ExperimentBehaviorTracker()
    for operation in ("set_flow_rate", "run_flow", "terminate"):
        tracker.observe(
            {
                "operation_type": operation,
                "experiment_ended": False,
                "constraint_flags": {"precondition_failed": False},
            }
        )
    tracker.observe(
        {
            "operation_type": "measure",
            "experiment_ended": True,
            "constraint_flags": {"precondition_failed": False},
        }
    )
    assert tracker.completed[0]["behavior_complete"] is True
    assert tracker.completed[0]["operation_sequence"][-1] == "measure:final_assay"

    tracker.observe(
        {
            "operation_type": "run_flow",
            "experiment_ended": False,
            "constraint_flags": {"precondition_failed": True},
        }
    )
    tracker.observe(
        {
            "operation_type": "measure",
            "experiment_ended": True,
            "constraint_flags": {"precondition_failed": False},
        }
    )
    assert tracker.completed[1]["behavior_complete"] is False
    assert tracker.completed[1]["quick_close_incomplete"] is True
    assert tracker.completed[1]["missing_required_operations"] == [
        "run_flow",
        "set_flow_rate",
    ]


def test_control_report_retains_pre_foundation_learning_diagnostic() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "pre_foundation_learning_diagnostic_infrastructure_blocked"
    assert report["validation"]["targeted_rl_tests_passed"] == 36
    assert report["checks"]["native_hybrid_policy_distribution"] is True
    assert report["checks"]["five_seed_twenty_episode_gate"] is False
    assert report["checks"]["repeated_terminate_removed_from_affordances"] is True
    assert report["gate_summary"]["passed_training_seed_count"] == 1
    assert report["gate_summary"]["status"] == "blocked"
    curve = report["pre_foundation_learning_curve"]
    assert curve["checkpoints"][1]["gate_passed"] is True
    assert curve["five_seed_expansion"] == "stopped_before_seed_107_completion"
    assert report["checks"]["world_foundation_preconditions_passed"] is False
    assert report["benchmark_claim_allowed"] is False


def test_every_conditional_action_uses_the_operation_registry_fields_only() -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization")
    try:
        assert isinstance(env.action_space, gym.spaces.Dict)
        contract = conditional_hybrid_action_contract(env.action_space)
        by_operation = contract["semantic_action"]["parameters"]["by_operation"]
        registry = operation_contracts()
        for operation in OPERATION_TYPES:
            assert [item["field"] for item in by_operation[operation]] == list(
                registry[operation].required_fields
            )

        vector = np.zeros(49, dtype=np.float32)
        vector[OPERATION_TYPES.index("run_flow")] = 1.0
        decoded = decode_conditional_hybrid_action(
            vector,
            event_action_space=env.action_space,
            operation_mask=[True] * len(OPERATION_TYPES),
        )
        assert set(decoded) == {"operation", "target_temperature_K", "duration_s"}
    finally:
        env.close()


def test_action_and_reward_contract_hashes_are_stable_and_semantic() -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization")
    try:
        assert isinstance(env.action_space, gym.spaces.Dict)
        first = conditional_hybrid_action_contract(env.action_space)
        second = conditional_hybrid_action_contract(env.action_space)
        assert first["contract_hash"] == second["contract_hash"]
        assert len(first["contract_hash"]) == 64
    finally:
        env.close()
    task = get_task("flow-reaction-optimization")
    reward = reward_contract(task.allowed_operations)
    assert reward["behavioral_completion"]["requirements"] == [
        ["set_flow_rate"],
        ["run_flow"],
    ]
    assert len(reward["contract_hash"]) == 64
    assert core_operation_requirements(task.allowed_operations) == (
        ("set_flow_rate",),
        ("run_flow",),
    )


def test_native_distribution_masks_operations_and_ignores_inactive_log_prob() -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization")
    try:
        assert isinstance(env.action_space, gym.spaces.Dict)
        action_contract = conditional_hybrid_action_contract(env.action_space)
    finally:
        env.close()
    parameter_keys = tuple(
        action_contract["training_adapter"]["parameter_coordinate_keys"]
    )
    distribution = ConditionalHybridDistribution(parameter_keys)
    logits = th.zeros((1, len(OPERATION_TYPES)))
    means = th.zeros((1, len(parameter_keys)))
    log_std = th.zeros(len(parameter_keys))
    mask = th.zeros((1, len(OPERATION_TYPES)), dtype=th.bool)
    run_flow_index = OPERATION_TYPES.index("run_flow")
    mask[0, run_flow_index] = True
    distribution.proba_distribution(logits, means, log_std, mask)
    action = distribution.mode()
    assert int(action[0, : len(OPERATION_TYPES)].argmax()) == run_flow_index

    inactive = action.clone()
    potential_index = parameter_keys.index("potential_V")
    inactive[0, len(OPERATION_TYPES) + potential_index] = 0.75
    assert distribution.log_prob(inactive) == distribution.log_prob(action)

    active = action.clone()
    duration_index = parameter_keys.index("duration_s")
    active[0, len(OPERATION_TYPES) + duration_index] = 0.75
    assert distribution.log_prob(active) < distribution.log_prob(action)
    contract = policy_distribution_contract(parameter_keys)
    assert contract["irrelevant_parameter_log_prob"] is False
    assert len(contract["contract_hash"]) == 64


def test_campaign_behavior_ledger_resets_between_experiments() -> None:
    env = RLTrainingRewardWrapper(
        gym.make(
            "ChemWorld",
            task_id="flow-reaction-optimization",
            budget_override=12,
            episode_mode_override="campaign",
        )
    )
    try:
        env.reset(seed=0)
        for action in (
            {"operation": "add_reagent", "amount_mol": 0.02},
            {"operation": "add_solvent", "volume_L": 0.05, "solvent": 0},
            {
                "operation": "set_flow_rate",
                "flow_rate_mL_min": 1.0,
                "residence_time_s": 600.0,
            },
            {
                "operation": "run_flow",
                "target_temperature_K": 380.0,
                "duration_s": 600.0,
            },
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ):
            _, _, _, _, first_info = env.step(action)
        assert first_info["rl_training_reward"]["behavior_complete"] is True

        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        env.step({"operation": "terminate"})
        _, _, _, _, second_info = env.step(
            {"operation": "measure", "instrument": "final_assay"}
        )
        assert second_info["rl_training_reward"]["behavior_complete"] is False
        assert second_info["rl_training_reward"]["quick_close_incomplete"] is True
    finally:
        env.close()


def test_repeated_terminate_is_not_an_affordance_and_fails_closed() -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=5)
    try:
        env.reset(seed=0)
        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        _, _, _, _, first = env.step({"operation": "terminate"})
        assert first["transaction_status"] == "committed"
        valid = {
            operation
            for operation, is_valid in zip(OPERATION_TYPES, action_mask(env), strict=True)
            if is_valid
        }
        assert valid == {"measure"}
        _, reward, terminated, truncated, repeated = env.step({"operation": "terminate"})
        assert reward == 0.0
        assert terminated is False
        assert truncated is False
        assert repeated["transaction_status"] == "rolled_back"
        assert repeated["constraint_flags"]["precondition_failed"] is True
        assert repeated["preconditions"]["not_terminated"] is False
    finally:
        env.close()
