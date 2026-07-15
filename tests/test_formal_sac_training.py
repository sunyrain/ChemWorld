from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

import chemworld.rl.formal_training as formal_training_module
from chemworld.rl.formal_training import (
    FormalPPOJob,
    FormalPPOTrainingError,
    build_jobs,
    finalize_training,
    load_execution_inputs,
    run_one_job,
    scan_completed_jobs,
    validate_training_plan,
)

ROOT = Path(__file__).resolve().parents[1]
SAC_PLAN = Path("configs/methods/rl_v0.4/sac_training_plan.json")
POST_AFFORDANCE_SAC_PLAN = Path("configs/methods/rl_v0.4/sac_training_plan_v0.4.1.json")


def _inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return load_execution_inputs(root=ROOT, plan_path=SAC_PLAN)


def test_sac_plan_binds_frozen_matrix_replay_buffers_and_comparability() -> None:
    plan, formal, methods = _inputs()

    checks = validate_training_plan(plan, formal_protocol=formal, methods_config=methods)
    jobs = build_jobs(plan)

    assert all(checks.values())
    assert len(jobs) == 20
    assert all(job.algorithm == "sac" for job in jobs)
    assert jobs[0].job_id == "sac-partition-discovery-seed0"
    assert plan["training"]["checkpoint_steps"] == [20_000, 40_000, 60_000, 80_000, 100_000]
    assert plan["training"]["save_replay_buffer"] is True
    assert plan["execution"]["expected_candidate_checkpoint_count"] == 100
    assert plan["comparability_boundary"]["native_hybrid_distribution"] is False
    assert plan["comparability_boundary"]["same_public_affordance_decoder_as_ppo"] is True
    assert plan["evidence_boundary"]["ppo_training_in_scope"] is False


def test_post_affordance_sac_full_plan_is_valid_and_starts_locked() -> None:
    plan, formal, methods = load_execution_inputs(root=ROOT, plan_path=POST_AFFORDANCE_SAC_PLAN)

    checks = validate_training_plan(plan, formal_protocol=formal, methods_config=methods)

    assert all(checks.values())
    assert plan["status"] == "post_affordance_preflight_pending_full_matrix_forbidden"
    assert plan["execution"]["full_matrix_started"] is False
    assert plan["execution"]["executed_training_run_count"] == 0
    assert plan["current_contract_preflight"]["required_report_schema"] == (
        "chemworld-sac-v0410-preflight-report-0.1"
    )
    assert plan["comparability_boundary"]["action_adapter_schema_version"] == (
        "chemworld-sb3-box-latent-adapter-0.2"
    )


def test_sac_plan_fails_closed_on_replay_or_comparability_drift() -> None:
    plan, formal, methods = _inputs()
    drifted = json.loads(json.dumps(plan))
    drifted["training"]["save_replay_buffer"] = False
    drifted["comparability_boundary"]["same_public_affordance_decoder_as_ppo"] = False

    with pytest.raises(FormalPPOTrainingError, match=r"sac_latent|sac_replay"):
        validate_training_plan(drifted, formal_protocol=formal, methods_config=methods)


def test_small_sac_job_uses_exact_checkpoints_and_retained_replay_buffers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pytest.importorskip("stable_baselines3")
    plan, formal, _methods = _inputs()
    plan = json.loads(json.dumps(plan))
    plan["training"].update(
        {
            "requested_environment_steps_per_run": 4,
            "checkpoint_steps": [2, 4],
            "operation_budget": 2,
            "hyperparameters": {
                "buffer_size": 10,
                "learning_starts": 1,
                "batch_size": 1,
                "train_freq": 1,
                "gradient_steps": 1,
            },
        }
    )
    plan["infrastructure"]["progress_interval_steps"] = 2
    plan["development_selection"]["episodes_per_candidate"] = 1
    plan["development_selection"]["operation_budget_per_episode"] = 2
    plan["execution"]["artifact_root"] = "runs/test-formal-sac"

    def fake_evaluation(**_kwargs: object) -> dict[str, object]:
        return {
            "checkpoint_contract_compatibility": {"all": True},
            "summary": {
                "mean_episode_best_primary_metric": 0.1,
                "episode_completion_rate": 1.0,
                "behavior_complete_experiment_rate": 1.0,
                "primary_metric_missing_count": 0,
                "runtime_domain_failure_count": 0,
                "observation_domain_failure_count": 0,
            },
        }

    monkeypatch.setattr(formal_training_module, "evaluate_sb3_checkpoint", fake_evaluation)
    job = FormalPPOJob("flow-reaction-optimization", 4, "sac")

    summary = run_one_job(root=tmp_path, plan=plan, formal_protocol=formal, job=job)

    assert summary["schema_version"] == "chemworld-formal-sac-job-summary-0.4"
    assert [item["training_environment_step_count"] for item in summary["candidates"]] == [2, 4]
    manifest = json.loads(
        (tmp_path / summary["training_manifest_path"]).read_text(encoding="utf-8")
    )
    artifacts = manifest["periodic_checkpoint_artifacts"]
    assert sum(item["artifact_type"] == "checkpoint" for item in artifacts) == 2
    assert sum(item["artifact_type"] == "replay_buffer" for item in artifacts) == 2
    assert scan_completed_jobs(root=tmp_path, plan=plan)[job]["job_id"] == job.job_id


def test_sac_finalize_retains_complete_negative_matrix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, formal, methods = _inputs()
    plan = json.loads(json.dumps(plan))
    plan["execution"]["artifact_root"] = "runs/test-formal-sac"
    plan["execution"]["checkpoint_index"] = "configs/test-sac-index.json"
    plan["execution"]["report"] = "reports/test-sac-report.json"
    completed: dict[FormalPPOJob, dict[str, object]] = {}
    for index, job in enumerate(build_jobs(plan)):
        manifest = tmp_path / "manifests" / f"{job.job_id}.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("{}\n", encoding="utf-8")
        os.utime(manifest, (2_000.0 + index, 2_000.0 + index))
        candidates = [
            {
                "eligible": False,
                "training_environment_step_count": step,
                "dev_evaluation_sha256": "b" * 64,
                "summary": {"mean_episode_best_primary_metric": None},
            }
            for step in (20_000, 40_000, 60_000, 80_000, 100_000)
        ]
        completed[job] = {
            "job_id": job.job_id,
            "task_id": job.task_id,
            "model_seed": job.model_seed,
            "status": "complete",
            "training_manifest_path": manifest.relative_to(tmp_path).as_posix(),
            "training_manifest_sha256": "a" * 64,
            "requested_training_environment_step_count": 100_000,
            "training_environment_step_count": 100_000,
            "step_budget_exact": True,
            "cpu_time_s": 2.0,
            "gpu_time_s": 0.0,
            "wall_time_s": 4.0,
            "bench_accessed": False,
            "reference_search_used": False,
            "candidates": candidates,
        }
    monkeypatch.setattr(
        formal_training_module,
        "scan_completed_jobs",
        lambda **_kwargs: completed,
    )

    report = finalize_training(
        root=tmp_path,
        plan=plan,
        formal_protocol=formal,
        methods_config=methods,
    )

    assert report["status"] == "sac_train_dev_complete_selection_failed"
    assert report["sac_method_ready"] is False
    assert report["training_run_count"] == 20
    assert report["candidate_checkpoint_count"] == 100
    assert report["selected_checkpoint_count"] == 0
    assert report["failed_task_ids"] == list(plan["formal_core_tasks"])
    assert report["failed_checks"] == ["four_dev_selected_checkpoints"]
    assert report["integrity_failed_checks"] == []
    index = json.loads((tmp_path / "configs/test-sac-index.json").read_text(encoding="utf-8"))
    assert index["status"] == "sac_dev_selection_failed"
    assert index["method_ids"] == ["sac"]
    assert index["sac_method_ready"] is False
