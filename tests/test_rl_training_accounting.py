from __future__ import annotations

from pathlib import Path

import pytest
from scripts.run_rl_100k_development import _evidence_gate, load_100k_protocol

from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol
from chemworld.rl.training import train_sb3_baseline


def _allocation() -> RLWorldAllocation:
    freeze = load_rl_protocol("configs/benchmark/confirmatory_freeze_vnext.json")
    return RLWorldAllocation.from_protocol(
        freeze,
        task_id="flow-reaction-optimization",
        name="train",
    )


def test_manifest_records_actual_ppo_rollout_steps_and_periodic_checkpoint(
    tmp_path: Path,
) -> None:
    pytest.importorskip("stable_baselines3")
    manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id="flow-reaction-optimization",
        allocation=_allocation(),
        total_timesteps=9,
        model_seed=71,
        output_dir=tmp_path,
        algorithm_kwargs={"n_steps": 8, "batch_size": 4},
        operation_budget=4,
        checkpoint_interval_steps=8,
    )
    assert manifest["requested_training_environment_step_count"] == 9
    assert manifest["training_environment_step_count"] == 16
    assert manifest["step_budget_exact"] is False
    assert manifest["training_diagnostics"]["step_count"] == 16
    assert manifest["schema_version"] == "chemworld-rl-checkpoint-0.2"
    assert len(manifest["action_contract_hash"]) == 64
    assert len(manifest["training_reward_contract_hash"]) == 64
    assert len(manifest["policy_distribution_contract_hash"]) == 64
    assert manifest["policy_distribution_contract"][
        "irrelevant_parameter_log_prob"
    ] is False
    artifacts = manifest["periodic_checkpoint_artifacts"]
    assert len(artifacts) == 2
    assert all(item["artifact_type"] == "checkpoint" for item in artifacts)
    assert all(len(item["sha256"]) == 64 for item in artifacts)
    assert len(manifest["periodic_checkpoint_contract_manifests"]) == 2
    assert all(
        (tmp_path / item["path"]).is_file()
        for item in manifest["periodic_checkpoint_contract_manifests"]
    )
    infrastructure = manifest["training_infrastructure"]
    assert infrastructure["parallel_environments"] == 1
    assert infrastructure["vectorization_backend"] == "dummy"
    assert infrastructure["requested_device"] == "cpu"
    assert infrastructure["resolved_device"] == "cpu"
    assert infrastructure["environment_steps_per_wall_second"] > 0.0


def test_vectorized_ppo_counts_total_environment_steps_and_checkpoints(
    tmp_path: Path,
) -> None:
    pytest.importorskip("stable_baselines3")
    manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id="flow-reaction-optimization",
        allocation=_allocation(),
        total_timesteps=9,
        model_seed=73,
        output_dir=tmp_path,
        algorithm_kwargs={"n_steps": 4, "batch_size": 4},
        operation_budget=2,
        checkpoint_interval_steps=8,
        parallel_environments=2,
        vectorization_backend="dummy",
        device="cpu",
    )
    assert manifest["training_environment_step_count"] == 16
    assert manifest["training_diagnostics"]["step_count"] == 16
    assert manifest["training_diagnostics"]["environment_count"] == 2
    assert manifest["training_infrastructure"]["parallel_environments"] == 2
    assert len(manifest["periodic_checkpoint_artifacts"]) == 2


def test_training_device_and_vectorization_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    torch = pytest.importorskip("torch")
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(RuntimeError, match="CUDA training was requested"):
        train_sb3_baseline(
            algorithm="ppo",
            task_id="flow-reaction-optimization",
            allocation=_allocation(),
            total_timesteps=8,
            model_seed=74,
            output_dir=tmp_path / "cuda",
            algorithm_kwargs={"n_steps": 8, "batch_size": 4},
            device="cuda",
        )
    with pytest.raises(ValueError, match="requires at least two"):
        train_sb3_baseline(
            algorithm="ppo",
            task_id="flow-reaction-optimization",
            allocation=_allocation(),
            total_timesteps=8,
            model_seed=74,
            output_dir=tmp_path / "subprocess",
            algorithm_kwargs={"n_steps": 8, "batch_size": 4},
            vectorization_backend="subprocess",
        )


def test_sac_periodic_manifest_distinguishes_model_and_replay_buffer(
    tmp_path: Path,
) -> None:
    pytest.importorskip("stable_baselines3")
    manifest = train_sb3_baseline(
        algorithm="sac",
        task_id="flow-reaction-optimization",
        allocation=_allocation(),
        total_timesteps=2,
        model_seed=72,
        output_dir=tmp_path,
        algorithm_kwargs={
            "buffer_size": 10,
            "learning_starts": 1,
            "batch_size": 1,
            "train_freq": 1,
            "gradient_steps": 1,
        },
        operation_budget=2,
        checkpoint_interval_steps=2,
        save_replay_buffer=True,
    )
    artifact_types = {
        Path(item["path"]).suffix: item["artifact_type"]
        for item in manifest["periodic_checkpoint_artifacts"]
    }
    assert artifact_types == {".zip": "checkpoint", ".pkl": "replay_buffer"}


def test_100k_protocol_requires_exact_steps_checkpoints_and_no_bench() -> None:
    protocol = load_100k_protocol()
    assert protocol["algorithm"] == "sac"
    assert protocol["training"]["actual_environment_steps_must_equal_requested"] is True
    assert protocol["training"]["checkpoint_interval_steps"] == 20_000
    assert protocol["training"]["save_replay_buffer"] is True
    assert protocol["final_dev"]["allocation"] == "dev"
    assert protocol["standard_replay"]["world_family_allocation"] is None
    assert protocol["benchmark_claim_allowed"] is False


def test_100k_gate_requires_domain_stability_and_replay_quality() -> None:
    spec = load_100k_protocol()["evidence_gate"]
    dev = {
        "episode_completion_rate": 1.0,
        "invalid_action_rate": 0.01,
        "runtime_domain_failure_count": 0,
        "observation_domain_failure_count": 0,
    }
    replay = {
        "all_replay_verified": True,
        "episode_completion_rate": 0.9,
        "invalid_action_rate": 0.01,
        "mean_final_best_score_including_failures": 0.01,
    }
    assert all(_evidence_gate(dev, replay, spec).values())
    unstable = {**dev, "observation_domain_failure_count": 1}
    assert _evidence_gate(unstable, replay, spec)["final_dev_domain_stability"] is False
    weak = {**replay, "mean_final_best_score_including_failures": 0.0}
    assert _evidence_gate(dev, weak, spec)["standard_replay_score"] is False
