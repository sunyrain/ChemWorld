from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_sac_v048_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/methods/rl_v0.4/sac_v049_preflight_plan.json"
REPORT_PATH = ROOT / "workstreams/benchmark_v1/reports/rl-sac-v049-preflight-v0.4.json"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _condition(*, behavior: int, endpoint: float) -> dict[str, Any]:
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
            "behavior_complete_experiment_rate": min(behavior / 20, 1.0),
            "quick_close_rate": 0.0,
            "invalid_action_rate": 0.0,
            "unsafe_step_rate": 0.0,
            "high_cost_step_rate": 0.0,
            "runtime_domain_failure_count": 0,
            "observation_domain_failure_count": 0,
            "primary_metric_observation_count": 20,
            "mean_episode_best_primary_metric": endpoint,
        },
    }


def _jobs(plan: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = []
    for index, (task_id, spec) in enumerate(plan["formal_core_tasks"].items()):
        signal = index < 2
        jobs.append(
            {
                "task_id": task_id,
                "step0_evaluation": _condition(behavior=1, endpoint=0.0),
                "trained_evaluation": _condition(
                    behavior=2 if signal else 1,
                    endpoint=float(spec["sesoi"]) if signal else 0.0,
                ),
            }
        )
    return jobs


def test_post_affordance_sac_plan_is_preregistered_and_namespaced() -> None:
    plan = _load(PLAN_PATH)
    protocol = _load(ROOT / plan["formal_protocol_path"])

    checks = preflight.validate_plan(plan, protocol)

    assert all(checks.values())
    assert plan["schema_version"] == preflight.POST_AFFORDANCE_PLAN_VERSION
    assert "post-affordance-v049" in plan["writer_gate_path"]
    assert "post-affordance-v049" in plan["execution"]["artifact_root"]
    assert plan["execution"]["report"].endswith("rl-sac-v049-preflight-v0.4.json")
    assert plan["comparability_boundary"]["system_level_comparison_only"] is True
    assert plan["evidence_boundary"]["v048_negative_result_remains_immutable"] is True


def test_post_affordance_sac_gate_uses_v049_status_without_relaxation() -> None:
    plan = _load(PLAN_PATH)

    assessment = preflight.assess_gate(plan, _jobs(plan))

    assert assessment["passed"] is True
    assert assessment["status"] == "sac_v049_preflight_passed_full_matrix_allowed"
    assert plan["gate"]["minimum_tasks_with_learning_signal"] == 2
    assert plan["gate"]["runtime_domain_failure_count_required"] == 0


def test_post_affordance_sac_report_rejects_source_or_tree_drift(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    outputs = {
        ("rev-parse", "HEAD"): "a" * 40,
        ("status", "--porcelain=v1", "--untracked-files=all"): "",
    }
    monkeypatch.setattr(preflight, "_git_output", lambda _root, *args: outputs[args])
    start = {"source_commit": "a" * 40}
    assert preflight.source_state_before_report(tmp_path, start)["source_commit_stable"] is True

    outputs[("rev-parse", "HEAD")] = "b" * 40
    with pytest.raises(preflight.SACPreflightError, match="commit changed"):
        preflight.source_state_before_report(tmp_path, start)

    outputs[("rev-parse", "HEAD")] = "a" * 40
    outputs[("status", "--porcelain=v1", "--untracked-files=all")] = " M source.py"
    with pytest.raises(preflight.SACPreflightError, match="tree changed"):
        preflight.source_state_before_report(tmp_path, start)


def test_post_affordance_sac_report_is_stable_complete_negative_evidence() -> None:
    report = _load(REPORT_PATH)

    assert report["status"] == "sac_v049_preflight_failed_full_matrix_forbidden"
    assert report["full_matrix_allowed"] is False
    assert len(report["jobs"]) == 4
    assert report["resource_accounting"]["training_environment_step_count"] == 102_400
    assert report["source"]["source_commit"] == (
        "9e2339c437a09f6bde05c95aeadca1f980df6725"
    )
    assert report["source"]["source_commit_stable"] is True
    assert report["source"]["source_tree_clean_before_report"] is True
    assert report["gate_assessment"]["learning_signal_task_count"] == 0
    assert report["gate_assessment"]["step0_total_behavior_complete_experiment_count"] == 13
    assert report["gate_assessment"]["trained_total_behavior_complete_experiment_count"] == 0
    assert sum(
        int(job["step0_evaluation"]["summary"]["runtime_domain_failure_count"])
        for job in report["jobs"]
    ) == 47
    assert sum(
        int(job["trained_evaluation"]["summary"]["runtime_domain_failure_count"])
        for job in report["jobs"]
    ) == 428
    assert all(job["step0_evaluation"]["exact_replay"] is True for job in report["jobs"])
    assert all(job["trained_evaluation"]["exact_replay"] is True for job in report["jobs"])
    assert report["benchmark_claim_allowed"] is False
