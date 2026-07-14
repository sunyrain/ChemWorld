from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_ppo_v048_preflight as preflight

from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.rl.formal_training import build_formal_allocation

ROOT = Path(__file__).resolve().parents[1]


def _inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    plan = json.loads((ROOT / preflight.DEFAULT_PLAN_PATH).read_text(encoding="utf-8"))
    protocol = json.loads((ROOT / plan["formal_protocol_path"]).read_text(encoding="utf-8"))
    return plan, protocol


def _evaluation(*, behavior: int, endpoint: float | None) -> dict[str, Any]:
    return {
        "exact_replay": True,
        "policy_mode": "stochastic_frozen_seed",
        "checkpoint_contract_compatibility": {
            "checkpoint_digest": True,
            "algorithm": True,
            "task": True,
            "observation_contract": True,
            "action_contract": True,
            "reward_contract": True,
            "policy_distribution_contract": True,
        },
        "summary": {
            "operation_count": 1200,
            "operation_counts": {"measure": 20, "wait": 1180},
            "complete_experiment_count": behavior,
            "episode_completion_rate": min(behavior / 20, 1.0),
            "behavior_complete_experiment_count": behavior,
            "behavior_complete_experiment_rate": 1.0 if behavior else 0.0,
            "quick_close_rate": 0.0,
            "invalid_action_rate": 0.0,
            "unsafe_step_rate": 0.0,
            "high_cost_step_rate": 0.0,
            "runtime_domain_failure_count": 0,
            "observation_domain_failure_count": 0,
            "primary_metric_observation_count": behavior,
            "mean_episode_best_primary_metric": endpoint,
        },
    }


def _jobs(
    plan: dict[str, Any], *, signal_tasks: set[str], before_behavior: int = 0
) -> list[dict[str, Any]]:
    jobs = []
    for task_id, task in plan["formal_core_tasks"].items():
        signal = task_id in signal_tasks
        jobs.append(
            {
                "task_id": task_id,
                "step0_evaluation": _evaluation(
                    behavior=before_behavior,
                    endpoint=0.0 if before_behavior else None,
                ),
                "trained_evaluation": _evaluation(
                    behavior=before_behavior + int(signal),
                    endpoint=float(task["sesoi"]) if signal else 0.0,
                ),
            }
        )
    return jobs


def test_preflight_plan_is_preregistered_against_formal_task_metrics() -> None:
    plan, protocol = _inputs()

    checks = preflight.validate_plan(plan, protocol)

    assert all(checks.values())
    assert plan["development_evaluation"]["deterministic_policy"] is False
    assert plan["development_evaluation"]["evaluation_repetitions"] == 2
    assert plan["gate"]["threshold_changes_after_execution_allowed"] is False
    assert plan["evidence_boundary"]["benchmark_claim_allowed"] is False


def test_historical_archive_is_digest_bound_and_ineligible_for_current_use() -> None:
    archive_root = ROOT / "runs/benchmark-v0.5/rl-v0.4/ppo/shared/pre-v048-diagnostic"
    archive = json.loads((archive_root / "archive-manifest.json").read_text(encoding="utf-8"))

    assert archive["result_role"] == "historical_diagnostic"
    assert archive["formal_results_present"] is False
    assert archive["benchmark_claim_allowed"] is False
    assert archive["eligible_for_current_runtime_load"] is False
    assert archive["eligible_for_resume"] is False
    assert archive["eligible_for_formal_checkpoint_index"] is False
    assert archive["current_contract_rerun_required"] is True
    for artifact in archive["artifacts"]:
        path = archive_root / artifact["path"]
        assert path.stat().st_size == artifact["size_bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]


def test_current_negative_outcome_is_bound_and_forbids_full_matrix() -> None:
    preflight_path = ROOT / "workstreams/benchmark_v1/reports/rl-ppo-v048-preflight-v0.4.json"
    outcome_path = ROOT / "workstreams/benchmark_v1/reports/rl-ppo-dev-v0.4.8.json"
    index_path = ROOT / "configs/methods/rl_v0.4/ppo_checkpoint_index.json"
    plan_path = ROOT / "configs/methods/rl_v0.4/ppo_training_plan.json"
    preflight_report = json.loads(preflight_path.read_text(encoding="utf-8"))
    outcome = json.loads(outcome_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    assert preflight_report["status"] == "ppo_v048_preflight_failed_full_matrix_forbidden"
    assert preflight_report["full_matrix_allowed"] is False
    assert preflight_report["gate_assessment"]["learning_signal_task_count"] == 3
    assert preflight_report["gate_assessment"]["checks"]["all_tasks_operational"] is False
    assert len(preflight_report["jobs"]) == 4
    assert all(
        job[condition]["exact_replay"] is True
        and all(job[condition]["checkpoint_contract_compatibility"].values())
        for job in preflight_report["jobs"]
        for condition in ("step0_evaluation", "trained_evaluation")
    )
    assert (
        sum(
            job["trained_checkpoint"]["training_environment_step_count"]
            for job in preflight_report["jobs"]
        )
        == 102_400
    )
    assert (
        outcome["preflight"]["report_sha256"]
        == hashlib.sha256(preflight_path.read_bytes()).hexdigest()
    )
    assert outcome["full_matrix"]["executed_training_run_count"] == 0
    assert outcome["full_matrix"]["selected_checkpoint_count"] == 0
    assert outcome["ppo_method_ready"] is False
    assert (
        index["current_contract_outcome"]["report_sha256"]
        == hashlib.sha256(outcome_path.read_bytes()).hexdigest()
    )
    assert index["checkpoints"] == []
    assert index["ppo_method_ready"] is False
    assert plan["execution"]["full_matrix_started"] is False
    assert plan["execution"]["full_matrix_start_forbidden_by_preflight"] is True


def test_gate_requires_two_learning_signal_tasks_and_operational_replay() -> None:
    plan, _protocol = _inputs()
    tasks = list(plan["formal_core_tasks"])

    passed = preflight.assess_gate(plan, _jobs(plan, signal_tasks=set(tasks[:2])))
    failed = preflight.assess_gate(plan, _jobs(plan, signal_tasks={tasks[0]}))

    assert passed["passed"] is True
    assert passed["learning_signal_task_count"] == 2
    assert failed["passed"] is False
    assert failed["failed_checks"] == ["minimum_learning_signal_tasks"]


def test_gate_fails_closed_on_replay_or_domain_drift() -> None:
    plan, _protocol = _inputs()
    jobs = _jobs(plan, signal_tasks=set(plan["formal_core_tasks"]))
    jobs[0]["trained_evaluation"]["exact_replay"] = False
    jobs[1]["step0_evaluation"]["summary"]["runtime_domain_failure_count"] = 1

    result = preflight.assess_gate(plan, jobs)

    assert result["passed"] is False
    assert result["checks"]["all_tasks_operational"] is False
    assert "all_tasks_operational" in result["failed_checks"]


def test_source_state_requires_clean_exact_origin_main(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    outputs = {
        ("rev-parse", "HEAD"): "a" * 40,
        ("rev-parse", "origin/main"): "a" * 40,
        ("status", "--porcelain=v1", "--untracked-files=all"): "",
    }
    monkeypatch.setattr(preflight, "_git_output", lambda _root, *args: outputs[args])
    assert preflight.source_state(tmp_path)["source_tree_clean"] is True

    outputs[("rev-parse", "origin/main")] = "b" * 40
    with pytest.raises(preflight.PPOPreflightError, match="origin/main"):
        preflight.source_state(tmp_path)


def test_true_step0_checkpoint_loads_under_current_contract(tmp_path: Path) -> None:
    pytest.importorskip("stable_baselines3")
    _plan, protocol = _inputs()
    task_id = "flow-reaction-optimization"
    train = build_formal_allocation(protocol, task_id=task_id, name="train")
    dev = build_formal_allocation(protocol, task_id=task_id, name="dev")

    manifest = preflight.create_step0_checkpoint(
        task_id=task_id,
        allocation=train,
        model_seed=7,
        operation_budget=2,
        algorithm_kwargs={"n_steps": 2, "batch_size": 2, "n_epochs": 1},
        torch_num_threads=1,
        output_dir=tmp_path / "step0",
    )
    checkpoint = tmp_path / "step0" / manifest["checkpoint"]
    evaluation = evaluate_sb3_checkpoint(
        algorithm="ppo",
        checkpoint=checkpoint,
        task_id=task_id,
        allocation=dev,
        episodes=1,
        operation_budget=2,
        sampler_seed=123,
        policy_seed=456,
        deterministic=False,
        primary_metric="flow_conversion",
    )

    assert manifest["training_environment_step_count"] == 0
    assert all(evaluation["checkpoint_contract_compatibility"].values())
    assert evaluation["policy_mode"] == "stochastic_frozen_seed"
    sidecar = json.loads(checkpoint.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert sidecar["shape_only_compatible"] is False
    assert sidecar["legacy_checkpoint_compatible"] is False
