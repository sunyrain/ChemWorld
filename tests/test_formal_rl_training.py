from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.rl.environment import RLWorldAllocation
from chemworld.rl.evaluation import _ExperimentBehaviorTracker
from chemworld.rl.formal_training import (
    FormalPPOTrainingError,
    build_formal_allocation,
    build_jobs,
    finalize_training,
    load_execution_inputs,
    scan_completed_jobs,
    select_task_candidate,
    validate_training_plan,
)
from chemworld.rl.training import train_sb3_baseline
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]


def _inputs() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
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
    assert infrastructure["worker_process_cpu_time_s"] > 0.0
    assert infrastructure["worker_process_cpu_accounting_method"].startswith(
        "windows_GetProcessTimes"
    )
    assert manifest["cpu_time_s"] == pytest.approx(
        infrastructure["parent_process_cpu_time_s"] + infrastructure["worker_process_cpu_time_s"]
    )
