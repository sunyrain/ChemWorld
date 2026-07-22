from __future__ import annotations

from pathlib import Path

import gymnasium as gym
import numpy as np
import pytest
from scripts.audit_rl_baselines import FREEZE_PROTOCOL, RL_PROTOCOL, build_report

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.rl.environment import (
    RLWorldAllocation,
    TrainWorldFamilyWrapper,
    build_rl_environment,
    load_rl_protocol,
)
from chemworld.tasks import get_task
from chemworld.wrappers import (
    ConditionalHybridActionWrapper,
    ContinuousEventActionWrapper,
    RLControlObservationWrapper,
    RLObservationWrapper,
    RLTrainingRewardWrapper,
)


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
        assert env.action_space.shape == (50,)
        assert env.action_contract()["action_keys"] == list(env.event_action_space.spaces)
        assert env.action_contract()["operation_types"] == list(env.operation_types)
        add_reagent = np.full(50, -1.0, dtype=np.float32)
        add_reagent[env.operation_types.index("add_reagent")] = 1.0
        decoded = env.action(add_reagent)
        assert decoded["operation"] == env.operation_types.index("add_reagent")
        assert set(decoded) == {"operation", "amount_mol"}
        impossible = np.full(50, -1.0, dtype=np.float32)
        impossible[env.operation_types.index("cool_crystallize")] = 1.0
        masked = env.action(impossible)
        assert masked["operation"] != env.operation_types.index("cool_crystallize")
        low_parameters = add_reagent.copy()
        high_parameters = add_reagent.copy()
        amount_index = env.operation_logit_count + env.parameter_keys.index("amount_mol")
        low_parameters[amount_index] = -1.0
        high_parameters[amount_index] = 1.0
        low = env.action(low_parameters)
        high = env.action(high_parameters)
        assert float(low["amount_mol"]) < float(high["amount_mol"])
        assert "potential_V" not in low
        assert "potential_V" not in high
        assert env.action_contract()["schema_version"] == ("chemworld-continuous-event-action-0.4")
        assert env.action_contract()["inactive_parameter_policy"] == (
            "excluded_from_execution_and_trajectory"
        )
        assert env.action_contract()["execution_numeric_policy"]
        with pytest.raises(ValueError, match="finite vector"):
            env.action(np.full(50, np.nan, dtype=np.float32))
    finally:
        env.close()


def test_conditional_hybrid_adapter_excludes_irrelevant_coordinates() -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id="flow-reaction-optimization")
    )
    try:
        env.reset(seed=0)
        contract = env.action_contract()
        assert contract["schema_version"] == "chemworld-conditional-hybrid-action-0.8"
        assert contract["execution_projection"]["affordance_state_machine_version"].endswith("0.7")
        assert contract["execution_projection"]["state_dependent_categorical_choices"] is True
        assert contract["semantic_action"]["operation"]["kind"] == "categorical"
        assert contract["training_adapter"]["native_hybrid_distribution"] is False
        assert len(contract["contract_hash"]) == 64

        first = np.zeros(50, dtype=np.float32)
        first[env.operation_types.index("add_reagent")] = 1.0
        second = first.copy()
        # Change every parameter coordinate except amount_mol. The executed
        # conditional action must remain identical.
        amount_index = env.parameter_keys.index("amount_mol")
        second[len(env.operation_types) :] = 1.0
        second[len(env.operation_types) + amount_index] = first[
            len(env.operation_types) + amount_index
        ]
        assert env.action(first) == env.action(second)
        assert set(env.action(first)) == {"operation", "amount_mol"}
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


def test_rl_control_observation_exposes_and_resets_public_core_progress() -> None:
    env = RLControlObservationWrapper(
        RLObservationWrapper(
            gym.make(
                "ChemWorld",
                task_id="flow-reaction-optimization",
                budget_override=12,
                episode_mode_override="campaign",
            ),
            include_mask=True,
            include_cost=True,
        )
    )
    try:
        initial, initial_info = env.reset()
        assert initial_info["rl_core_progress"]["requirements"] == [
            ["set_flow_rate"],
            ["run_flow"],
        ]
        assert initial_info["rl_core_progress"]["satisfied"] == [False, False]

        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        progressed, _, _, _, progressed_info = env.step(
            {
                "operation": "set_flow_rate",
                "flow_rate_mL_min": 1.0,
                "residence_time_s": 600.0,
            }
        )
        assert progressed_info["rl_core_progress"]["satisfied"] == [True, False]
        assert not np.array_equal(initial, progressed)

        env.step(
            {
                "operation": "run_flow",
                "target_temperature_K": 380.0,
                "duration_s": 600.0,
            }
        )
        env.step({"operation": "terminate"})
        reset_observation, _, _, _, reset_info = env.step(
            {"operation": "measure", "instrument": "final_assay"}
        )
        assert reset_info["rl_core_progress"]["satisfied"] == [False, False]
        assert env.observation_space.contains(reset_observation)
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


def test_nonmeasurement_action_cannot_redeem_cached_observation_score() -> None:
    env = gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=6)
    try:
        env.reset(seed=0)
        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        _, measured_reward, _, _, measured_info = env.step(
            {"operation": "measure", "instrument": "uvvis"}
        )
        _, terminal_reward, _, _, terminal_info = env.step({"operation": "terminate"})
        assert np.isfinite(measured_reward)
        assert measured_info["environment_reward"]["fresh_measurement"] is True
        assert terminal_reward == 0.0
        assert terminal_info["environment_reward"] == {
            "schema_version": "chemworld-environment-reward-0.2",
            "semantics": "fresh_measurement_score_delta",
            "fresh_measurement": False,
            "cached_observation_rewarded": False,
            "score_delta": 0.0,
        }
    finally:
        env.close()


def test_transaction_rollback_is_invalid_and_penalized_even_when_preconditions_pass() -> None:
    task = get_task("reaction-to-distillation")
    recipe = task_recipe_from_unit_vector(
        task.to_dict(),
        np.full(task_recipe_dimension(task.to_dict()), 0.5),
    )
    env = RLTrainingRewardWrapper(gym.make("ChemWorld", task_id=task.task_id, budget_override=20))
    try:
        env.reset(seed=0)
        for action in recipe["steps"][:-2]:
            env.step(action)
        _, reward, _, _, info = env.step(
            {"operation": "wait", "duration_s": 1.0, "stirring_speed_rpm": 100.0}
        )
        reward_info = info["rl_training_reward"]
        assert info["transaction_status"] == "rolled_back"
        assert info["rollback_reason"] == "constitution_failed"
        assert info["constraint_flags"]["precondition_failed"] is False
        assert info["constraint_flags"]["constitution_failed"] is True
        assert reward == pytest.approx(-0.25)
        assert reward_info["transaction_rolled_back"] is True
        assert reward_info["invalid_action"] is True
        diagnostics = env.training_diagnostics()
        assert diagnostics["transaction_rollback_count"] == 1
        assert diagnostics["constitution_failure_count"] == 1
        assert diagnostics["invalid_action_count"] == 1
    finally:
        env.close()


def test_training_reward_penalizes_quick_close_and_gates_terminal_bonus() -> None:
    env = RLTrainingRewardWrapper(
        gym.make(
            "ChemWorld",
            task_id="flow-reaction-optimization",
            budget_override=8,
            episode_mode_override="campaign",
        )
    )
    try:
        env.reset(seed=0)
        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        _, terminate_reward, _, _, _ = env.step({"operation": "terminate"})
        _, assay_reward, _, _, info = env.step(
            {"operation": "measure", "instrument": "final_assay"}
        )
        reward_info = info["rl_training_reward"]
        assert terminate_reward == 0.0
        assert assay_reward == pytest.approx(reward_info["raw_reward"] - 1.0)
        assert reward_info["newly_unlocked_operations"] == 0
        assert reward_info["behavior_complete"] is False
        assert reward_info["quick_close_incomplete"] is True
        diagnostics = env.training_diagnostics()
        assert diagnostics["quick_close_count"] == 1
        assert diagnostics["behavior_complete_experiment_count"] == 0
        contract = env.reward_contract()
        assert contract["components"]["experiment_ended"] == 1.0
        assert contract["components"]["measurement"] == 0.0
        assert contract["components"]["quick_close_incomplete"] == -1.0
        assert contract["leakage_controls"]["terminal_bonus"] is True
        assert (
            contract["leakage_controls"]["terminal_bonus_requires_public_behavioral_completion"]
            is True
        )
    finally:
        env.close()


def test_flow_core_operation_is_recorded_as_behavioral_completion() -> None:
    env = RLTrainingRewardWrapper(
        gym.make("ChemWorld", task_id="flow-reaction-optimization", budget_override=8)
    )
    try:
        env.reset(seed=0)
        env.step({"operation": "add_reagent", "amount_mol": 0.02})
        env.step({"operation": "add_solvent", "volume_L": 0.05, "solvent": 0})
        _, setup_reward, _, _, setup_info = env.step(
            {
                "operation": "set_flow_rate",
                "flow_rate_mL_min": 1.0,
                "residence_time_s": 600.0,
            }
        )
        _, completion_reward, _, _, info = env.step(
            {
                "operation": "run_flow",
                "target_temperature_K": 380.0,
                "duration_s": 600.0,
            }
        )
        assert setup_info["rl_training_reward"]["newly_satisfied_core_requirements"] == 1
        assert setup_reward >= 0.10
        assert info["rl_training_reward"]["newly_satisfied_core_requirements"] == 1
        assert completion_reward == pytest.approx(1.098)
        assert info["rl_training_reward"]["behavior_complete"] is True
        assert info["rl_training_reward"]["executed_core_operations"] == [
            "run_flow",
            "set_flow_rate",
        ]
        assert env.training_diagnostics()["core_operation_counts"] == {
            "run_flow": 1,
            "set_flow_rate": 1,
        }
    finally:
        env.close()


def test_rl_protocol_keeps_formal_claims_closed() -> None:
    protocol = load_rl_protocol(RL_PROTOCOL)
    assert protocol["publication_ready"] is False
    assert protocol["benchmark_claim_allowed"] is False
    report = build_report()
    # Contract controls can be coherent while formal training and publication
    # claims remain explicitly closed.
    assert report["controls_ready"] is True
    assert report["checks"]["action_key_order_frozen"] is True
    assert report["formal_training_complete"] is False
    assert report["publication_ready"] is False
    if report["development_evidence"] is not None:
        assert report["development_evidence"]["passed"] is True
        assert set(report["development_evidence"]["eligible_algorithms"]) == {"ppo", "sac"}


def test_rl_extra_is_declared_without_becoming_core_dependency() -> None:
    pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "rl = [" in pyproject
    assert '"stable-baselines3>=2.9,<3.0"' in pyproject
