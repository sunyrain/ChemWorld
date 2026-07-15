from __future__ import annotations

import hashlib
import json
import os
from functools import partial
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from stable_baselines3.common.vec_env import DummyVecEnv

import chemworld.rl.formal_training as formal_training_module
from chemworld.data.logging import to_builtin
from chemworld.rl.batched_vec_env import BatchedSubprocVecEnv
from chemworld.rl.environment import RLWorldAllocation, build_rl_environment
from chemworld.rl.evaluation import _ExperimentBehaviorTracker
from chemworld.rl.formal_training import (
    FormalPPOTrainingError,
    build_formal_allocation,
    build_jobs,
    finalize_training,
    load_execution_inputs,
    run_one_job,
    scan_completed_jobs,
    select_task_candidate,
    validate_training_plan,
    verify_current_contract_preflight,
)
from chemworld.rl.training import train_sb3_baseline
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]


def _inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return load_execution_inputs(root=ROOT)


def test_plan_is_exactly_bound_to_formal_tasks_splits_and_ppo_budget() -> None:
    plan, formal, methods = _inputs()
    checks = validate_training_plan(plan, formal_protocol=formal, methods_config=methods)
    assert all(checks.values())
    jobs = build_jobs(plan)
    assert len(jobs) == 20
    assert len({job.job_id for job in jobs}) == 20
    assert [job.model_seed for job in jobs[:5]] == [0, 1, 2, 3, 4]
    assert plan["evidence_boundary"]["benchmark_claim_allowed"] is False
    assert plan["evidence_boundary"]["sac_training_in_scope"] is False
    assert plan["infrastructure"]["torch_num_threads"] == 1
    assert plan["infrastructure"]["vectorization_backend"] == "subprocess"
    assert plan["infrastructure_selection"]["selected_backend"] == "subprocess"
    assert plan["infrastructure_selection"]["formal_training_evidence"] is False


def test_post_affordance_ppo_full_plan_is_valid_but_starts_locked() -> None:
    path = ROOT / "configs/methods/rl_v0.4/ppo_training_plan_v0.4.1.json"
    plan, formal, methods = load_execution_inputs(root=ROOT, plan_path=path)

    checks = validate_training_plan(plan, formal_protocol=formal, methods_config=methods)

    assert all(checks.values())
    assert plan["status"] == "post_affordance_preflight_pending_full_matrix_forbidden"
    assert plan["execution"]["full_matrix_started"] is False
    assert plan["execution"]["full_matrix_start_forbidden_by_preflight"] is True
    assert plan["current_contract_preflight"]["required_report_schema"] == (
        "chemworld-ppo-v0410-preflight-report-0.1"
    )
    with pytest.raises(FormalPPOTrainingError, match="cannot load PPO preflight report"):
        verify_current_contract_preflight(
            root=ROOT,
            plan=plan,
            source_commit="a" * 40,
        )


def test_post_affordance_job_cannot_start_without_source_binding(tmp_path: Path) -> None:
    path = ROOT / "configs/methods/rl_v0.4/ppo_training_plan_v0.4.1.json"
    plan, formal, _methods = load_execution_inputs(root=ROOT, plan_path=path)

    with pytest.raises(FormalPPOTrainingError, match="missing its source commit"):
        run_one_job(
            root=tmp_path,
            plan=plan,
            formal_protocol=formal,
            job=build_jobs(plan)[0],
        )


def test_formal_execution_source_rejects_dirty_tree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    outputs = {
        ("rev-parse", "HEAD"): "a" * 40,
        ("status", "--porcelain=v1", "--untracked-files=all"): " M source.py",
    }

    def fake_check_output(args: list[str], **_kwargs: object) -> str:
        return outputs[tuple(args[1:])]

    monkeypatch.setattr(formal_training_module.subprocess, "check_output", fake_check_output)
    with pytest.raises(FormalPPOTrainingError, match="clean source tree"):
        formal_training_module.require_clean_execution_source(tmp_path)

    outputs[("status", "--porcelain=v1", "--untracked-files=all")] = ""
    assert formal_training_module.require_clean_execution_source(tmp_path) == "a" * 40


def test_legacy_negative_ppo_plan_cannot_unlock_execution() -> None:
    plan, _formal, _methods = _inputs()

    with pytest.raises(FormalPPOTrainingError, match="declaration is not executable"):
        verify_current_contract_preflight(
            root=ROOT,
            plan=plan,
            source_commit=str(plan["current_contract_preflight"]["source_commit"]),
        )


@pytest.mark.parametrize("algorithm", ["ppo", "sac"])
def test_post_affordance_preflight_unlock_requires_stable_source_evidence(
    tmp_path: Path, algorithm: str
) -> None:
    source_commit = "a" * 40
    version = "v0410"
    task_id = (
        f"benchmark-v05-rl-adapters--slice-{algorithm}-v0410-public-schema-adapter-dev"
    )
    plan_relative = f"configs/methods/rl_v0.4/{algorithm}_{version}_preflight_plan.json"
    report_relative = (
        f"workstreams/benchmark_v1/reports/rl-{algorithm}-{version}-preflight-v0.4.json"
    )
    report_schema = f"chemworld-{algorithm}-{version}-preflight-report-0.1"
    required_status = f"{algorithm}_{version}_preflight_passed_full_matrix_allowed"
    preflight_plan = {
        "schema_version": f"chemworld-{algorithm}-{version}-preflight-plan-0.1",
        "task_id": task_id,
    }
    preflight_path = tmp_path / plan_relative
    preflight_path.parent.mkdir(parents=True, exist_ok=True)
    preflight_path.write_text(json.dumps(preflight_plan) + "\n", encoding="utf-8")
    declaration = {
        "required_before_full_matrix": True,
        "plan": plan_relative,
        "report": report_relative,
        "required_report_schema": report_schema,
        "required_status": required_status,
        "source_commit_must_equal_execution_head": True,
        "failure_forbids_full_matrix": True,
    }
    plan = {
        "algorithm": algorithm,
        "task_id": task_id,
        "current_contract_preflight": declaration,
    }
    canonical = hashlib.sha256(
        json.dumps(preflight_plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    report = {
        "schema_version": report_schema,
        "status": required_status,
        "algorithm": algorithm,
        "task_id": task_id,
        "source": {
            "source_commit": source_commit,
            "origin_main_commit": source_commit,
            "source_tree_clean": True,
            "source_commit_on_origin_main": True,
            "source_commit_before_report": source_commit,
            "source_commit_stable": True,
            "source_tree_clean_before_report": True,
        },
        "preflight_plan_path": plan_relative,
        "preflight_plan_file_sha256": hashlib.sha256(preflight_path.read_bytes()).hexdigest(),
        "preflight_plan_canonical_sha256": canonical,
        "gate_assessment": {"passed": True, "checks": {"learning": True}},
        "writer_gate": {
            "source_commit": source_commit,
            "writer_contract_ready": True,
            "formal_training_allowed": True,
        },
        "full_matrix_allowed": True,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "bench_accessed": False,
        "reference_search_used": False,
    }
    report_path = tmp_path / report_relative
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")

    checks = verify_current_contract_preflight(
        root=tmp_path,
        plan=plan,
        source_commit=source_commit,
    )
    assert all(checks.values())

    report["source"]["source_commit_stable"] = False
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
    with pytest.raises(FormalPPOTrainingError, match="source_stable_until_report"):
        verify_current_contract_preflight(
            root=tmp_path,
            plan=plan,
            source_commit=source_commit,
        )


@pytest.mark.parametrize(
    ("task_id", "metric"),
    [
        ("partition-discovery", "product_in_organic"),
        ("reaction-to-crystallization", "crystal_yield"),
        ("reaction-to-distillation", "distillate_purity"),
        ("flow-reaction-optimization", "flow_conversion"),
    ],
)
def test_formal_allocations_use_exact_public_namespaces_and_cells(
    task_id: str, metric: str
) -> None:
    plan, formal, _methods = _inputs()
    assert plan["formal_core_tasks"][task_id] == metric
    train = build_formal_allocation(formal, task_id=task_id, name="train")
    dev = build_formal_allocation(formal, task_id=task_id, name="dev")
    assert train.namespace_id == "chemworld-v0.5-train-0.4"
    assert dev.namespace_id == "chemworld-v0.5-dev-0.4"
    assert (min(train.base_seeds), max(train.base_seeds), len(train.base_seeds)) == (
        10_000,
        10_099,
        100,
    )
    assert (min(dev.base_seeds), max(dev.base_seeds), len(dev.base_seeds)) == (
        11_000,
        11_019,
        20,
    )
    assert len(train.cells) == 16
    assert len(dev.cells) == 12
    assert train.public_manifest()["namespace_id"] == train.namespace_id


def test_plan_fails_closed_on_bench_or_checkpoint_drift() -> None:
    plan, formal, methods = _inputs()
    drifted = json.loads(json.dumps(plan))
    drifted["split_bindings"]["bench_access"] = "allowed"
    drifted["training"]["checkpoint_steps"] = [25_600, 51_200, 76_800, 102_400]
    with pytest.raises(FormalPPOTrainingError, match="exact_checkpoint_steps"):
        validate_training_plan(drifted, formal_protocol=formal, methods_config=methods)


def test_exact_checkpoint_schedule_has_no_unregistered_intermediate(tmp_path: Path) -> None:
    pytest.importorskip("stable_baselines3")
    _plan, formal, _methods = _inputs()
    allocation = build_formal_allocation(formal, task_id="flow-reaction-optimization", name="train")
    manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id="flow-reaction-optimization",
        allocation=allocation,
        total_timesteps=16,
        model_seed=91,
        output_dir=tmp_path,
        algorithm_kwargs={"n_steps": 4, "batch_size": 4},
        operation_budget=4,
        checkpoint_steps=[8, 16],
        parallel_environments=2,
        torch_num_threads=1,
        progress_interval_steps=8,
    )
    checkpoint_names = sorted(
        Path(item["path"]).name
        for item in manifest["periodic_checkpoint_artifacts"]
        if item["artifact_type"] == "checkpoint"
    )
    assert checkpoint_names == [
        "ppo-flow-reaction-optimization-seed91_16_steps.zip",
        "ppo-flow-reaction-optimization-seed91_8_steps.zip",
    ]
    assert manifest["checkpoint_steps"] == [8, 16]
    assert manifest["checkpoint_interval_steps"] is None
    assert manifest["allocation"]["namespace_id"] == "chemworld-v0.5-train-0.4"
    assert manifest["bench_finetuning_used"] is False
    assert manifest["training_infrastructure"]["torch_num_threads"] == 1
    assert manifest["progress_interval_steps"] == 8
    assert (
        json.loads((tmp_path / "training-progress.json").read_text(encoding="utf-8"))[
            "progress_fraction"
        ]
        == 1.0
    )
    assert len(manifest["periodic_checkpoint_contract_manifests"]) == 2


def test_dev_behavior_tracker_uses_each_task_public_operation_contract() -> None:
    task = get_task("partition-discovery")
    tracker = _ExperimentBehaviorTracker(task.allowed_operations)
    for operation in ("mix", "settle", "separate_phase"):
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
    assert tracker.completed[0]["missing_required_operations"] == []
    assert "set_flow_rate" not in tracker.completed[0]["required_operations"]


def _summary(seed: int, candidates: list[dict[str, object]]) -> dict[str, object]:
    return {
        "job_id": f"ppo-partition-discovery-seed{seed}",
        "task_id": "partition-discovery",
        "model_seed": seed,
        "training_manifest_path": f"runs/seed-{seed}.manifest.json",
        "candidates": candidates,
    }


def _candidate(step: int, endpoint: float, *, eligible: bool = True) -> dict[str, object]:
    return {
        "eligible": eligible,
        "training_environment_step_count": step,
        "summary": {"mean_episode_best_primary_metric": endpoint},
    }


def test_selection_ranks_endpoint_then_fewer_steps_then_lower_seed() -> None:
    selected = select_task_candidate(
        "partition-discovery",
        [
            _summary(1, [_candidate(25_600, 0.8), _candidate(51_200, 0.9)]),
            _summary(0, [_candidate(25_600, 0.9), _candidate(51_200, 0.9)]),
            _summary(2, [_candidate(25_600, 2.0, eligible=False)]),
        ],
    )
    assert selected["summary"]["mean_episode_best_primary_metric"] == 0.9
    assert selected["training_environment_step_count"] == 25_600
    assert selected["model_seed"] == 0


def test_training_wall_time_uses_union_of_parallel_intervals(tmp_path: Path) -> None:
    manifests = [tmp_path / f"manifest-{index}.json" for index in range(3)]
    for manifest in manifests:
        manifest.write_text("{}\n", encoding="utf-8")
    for manifest, end in zip(manifests, (100.0, 104.0, 120.0), strict=True):
        os.utime(manifest, (end, end))
    summaries = [
        {"training_manifest_path": manifest.name, "wall_time_s": duration}
        for manifest, duration in zip(manifests, (8.0, 8.0, 5.0), strict=True)
    ]

    result = formal_training_module._training_wall_time_summary(root=tmp_path, summaries=summaries)

    assert result["observed_active_training_wall_time_s"] == pytest.approx(17.0)
    assert result["summed_job_wall_time_s_diagnostic_only"] == pytest.approx(21.0)
    assert result["parallel_wall_time_sum_used_as_elapsed"] is False
    assert result["parallel_overlap_observed"] is True
    assert result["merged_training_interval_count"] == 2


def test_json_writer_uses_portable_lf_bytes(tmp_path: Path) -> None:
    path = tmp_path / "evidence.json"

    formal_training_module._write_json(path, {"value": 1})

    payload = path.read_bytes()
    assert payload.endswith(b"\n")
    assert b"\r\n" not in payload


def test_finalize_records_scientific_selection_failure_without_hiding_matrix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, formal, methods = _inputs()
    plan = json.loads(json.dumps(plan))
    plan["execution"]["artifact_root"] = "runs/test-formal-ppo"
    plan["execution"]["checkpoint_index"] = "configs/test-index.json"
    plan["execution"]["report"] = "reports/test-report.json"
    selectable_tasks = {"reaction-to-distillation", "flow-reaction-optimization"}
    completed: dict[formal_training_module.FormalPPOJob, dict[str, object]] = {}
    for index, job in enumerate(build_jobs(plan)):
        manifest = tmp_path / "manifests" / f"{job.job_id}.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("{}\n", encoding="utf-8")
        os.utime(manifest, (1_000.0 + index, 1_000.0 + index))
        candidates: list[dict[str, object]] = []
        for step in (25_600, 51_200, 102_400):
            eligible = job.task_id in selectable_tasks and job.model_seed == 0 and step == 102_400
            candidates.append(
                {
                    "eligible": eligible,
                    "training_environment_step_count": step,
                    "checkpoint_path": f"runs/{job.job_id}-{step}.zip",
                    "checkpoint_contract_path": f"runs/{job.job_id}-{step}.manifest.json",
                    "dev_evaluation_sha256": "b" * 64,
                    "summary": {"mean_episode_best_primary_metric": 0.5 if eligible else None},
                }
            )
        completed[job] = {
            "job_id": job.job_id,
            "task_id": job.task_id,
            "model_seed": job.model_seed,
            "status": "complete",
            "training_manifest_path": manifest.relative_to(tmp_path).as_posix(),
            "training_manifest_sha256": "a" * 64,
            "requested_training_environment_step_count": 102_400,
            "training_environment_step_count": 102_400,
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
    monkeypatch.setattr(
        formal_training_module,
        "_materialize_selection",
        lambda **kwargs: {
            "method_id": "ppo",
            "task_id": kwargs["task_id"],
            "checkpoint_path": f"runs/selected/{kwargs['task_id']}.zip",
            "checkpoint_manifest_path": f"runs/selected/{kwargs['task_id']}.manifest.json",
            "training_resource_path": f"runs/selected/{kwargs['task_id']}.resources.json",
            "checkpoint_sha256": "c" * 64,
            "binding": {"task_id": kwargs["task_id"]},
        },
    )
    monkeypatch.setattr(
        formal_training_module,
        "_replay_selected",
        lambda **_kwargs: {
            "repetition_count": 2,
            "deterministic": True,
            "canonical_evaluation_sha256": "d" * 64,
            "summary": {},
        },
    )

    report = finalize_training(
        root=tmp_path,
        plan=plan,
        formal_protocol=formal,
        methods_config=methods,
    )

    assert report["status"] == "ppo_train_dev_complete_selection_failed"
    assert report["ppo_method_ready"] is False
    assert report["selected_checkpoint_count"] == 2
    assert report["failed_task_ids"] == ["partition-discovery", "reaction-to-crystallization"]
    assert report["failed_checks"] == ["four_dev_selected_checkpoints"]
    assert report["integrity_failed_checks"] == []
    assert report["training_run_count"] == 20
    assert report["candidate_checkpoint_count"] == 60
    assert report["training_resources"]["parallel_wall_time_sum_used_as_elapsed"] is False
    outcomes = {item["task_id"]: item for item in report["task_outcomes"]}
    assert outcomes["partition-discovery"]["status"] == "no_eligible_candidate"
    assert outcomes["reaction-to-distillation"]["status"] == "selected"
    checkpoint_index = json.loads(
        (tmp_path / "configs/test-index.json").read_text(encoding="utf-8")
    )
    assert checkpoint_index["status"] == "ppo_dev_selection_failed"
    assert checkpoint_index["missing_checkpoint_task_ids"] == report["failed_task_ids"]


def test_empty_run_tree_is_not_misreported_as_complete(tmp_path: Path) -> None:
    plan, formal, methods = _inputs()
    plan = json.loads(json.dumps(plan))
    plan["execution"]["artifact_root"] = "runs/test-formal-ppo"
    plan["execution"]["checkpoint_index"] = "configs/test-index.json"
    plan["execution"]["report"] = "reports/test-report.json"
    assert scan_completed_jobs(root=tmp_path, plan=plan) == {}
    with pytest.raises(FormalPPOTrainingError, match="0/20"):
        finalize_training(
            root=tmp_path,
            plan=plan,
            formal_protocol=formal,
            methods_config=methods,
        )


def test_world_allocation_rejects_blank_namespace() -> None:
    with pytest.raises(ValueError, match="namespace_id"):
        RLWorldAllocation(
            name="train",
            task_id="flow-reaction-optimization",
            base_seeds=(1,),
            cells=(("flow.reaction-kinetics", "interpolation", 0.1),),
            namespace_id=" ",
        )


@pytest.mark.skipif(__import__("os").name != "nt", reason="Windows handle accounting")
def test_windows_subprocess_worker_cpu_is_included(tmp_path: Path) -> None:
    pytest.importorskip("stable_baselines3")
    _plan, formal, _methods = _inputs()
    allocation = build_formal_allocation(formal, task_id="partition-discovery", name="train")
    manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id="partition-discovery",
        allocation=allocation,
        total_timesteps=8,
        model_seed=92,
        output_dir=tmp_path,
        algorithm_kwargs={"n_steps": 1, "batch_size": 8},
        operation_budget=4,
        parallel_environments=8,
        vectorization_backend="subprocess",
        torch_num_threads=1,
    )
    infrastructure = manifest["training_infrastructure"]
    assert infrastructure["subprocess_start_strategy"] == (
        "spawn_single_batched_environment_worker"
    )
    assert infrastructure["subprocess_worker_process_count"] == 1
    assert infrastructure["environments_per_worker_process"] == 8
    assert infrastructure["worker_process_cpu_time_s"] > 0.0
    assert infrastructure["worker_process_cpu_accounting_method"].startswith(
        "windows_GetProcessTimes"
    )
    assert manifest["cpu_time_s"] == pytest.approx(
        infrastructure["parent_process_cpu_time_s"] + infrastructure["worker_process_cpu_time_s"]
    )


def test_batched_subprocess_preserves_vector_slot_order_and_transitions() -> None:
    _plan, formal, _methods = _inputs()
    allocation = build_formal_allocation(formal, task_id="partition-discovery", name="train")
    factories = [
        partial(
            build_rl_environment,
            task_id="partition-discovery",
            allocation=allocation,
            sampler_seed=700 + rank,
            operation_budget=4,
            training_reward=True,
        )
        for rank in range(2)
    ]
    local = DummyVecEnv(factories)
    subprocess = BatchedSubprocVecEnv(factories, start_method="spawn")
    try:
        assert local.seed(900) == subprocess.seed(900)
        np.testing.assert_array_equal(local.reset(), subprocess.reset())
        assert to_builtin(local.reset_infos) == to_builtin(subprocess.reset_infos)

        actions = np.zeros((2, *local.action_space.shape), dtype=np.float32)
        for _ in range(4):
            local_observation, local_reward, local_done, local_info = local.step(actions)
            worker_observation, worker_reward, worker_done, worker_info = subprocess.step(actions)
            np.testing.assert_array_equal(local_observation, worker_observation)
            np.testing.assert_array_equal(local_reward, worker_reward)
            np.testing.assert_array_equal(local_done, worker_done)
            assert to_builtin(local_info) == to_builtin(worker_info)
    finally:
        local.close()
        subprocess.close()
