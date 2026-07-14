from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from scripts.run_sac_v048_preflight import (
    PLAN_VERSION,
    SACPreflightError,
    assess_gate,
    validate_plan,
)

from chemworld.rl.formal_training import (
    FormalPPOTrainingError,
    verify_current_contract_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs" / "methods" / "rl_v0.4" / "sac_v048_preflight_plan.json"
PROTOCOL_PATH = ROOT / "configs" / "benchmark" / "formal_protocol_v0.4.json"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _condition(
    *,
    behavior_complete: int,
    metric: float | None,
    runtime_failures: int = 0,
) -> dict[str, Any]:
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
            "episode_completion_rate": 1.0,
            "behavior_complete_experiment_rate": behavior_complete / 20,
            "quick_close_rate": 0.0,
            "invalid_action_rate": 0.0,
            "unsafe_step_rate": 0.0,
            "high_cost_step_rate": 0.0,
            "operation_count": 1200,
            "operation_counts": {"measure": 20},
            "runtime_domain_failure_count": runtime_failures,
            "observation_domain_failure_count": 0,
            "behavior_complete_experiment_count": behavior_complete,
            "primary_metric_observation_count": int(metric is not None) * 20,
            "mean_episode_best_primary_metric": metric,
        },
    }


def _jobs(*, runtime_failure_task: str | None = None) -> list[dict[str, Any]]:
    plan = _load(PLAN_PATH)
    jobs: list[dict[str, Any]] = []
    for index, (task_id, spec) in enumerate(plan["formal_core_tasks"].items()):
        before_behavior = index
        after_behavior = index + (1 if index < 2 else 0)
        jobs.append(
            {
                "task_id": task_id,
                "step0_evaluation": _condition(
                    behavior_complete=before_behavior,
                    metric=0.1,
                ),
                "trained_evaluation": _condition(
                    behavior_complete=after_behavior,
                    metric=0.1 + float(spec["sesoi"]) + 0.001,
                    runtime_failures=int(task_id == runtime_failure_task),
                ),
            }
        )
    return jobs


def test_sac_preflight_plan_is_frozen_and_protocol_bound() -> None:
    plan = _load(PLAN_PATH)
    protocol = _load(PROTOCOL_PATH)

    checks = validate_plan(plan, protocol)

    assert plan["schema_version"] == PLAN_VERSION
    assert all(checks.values())
    assert plan["comparison"]["trained_environment_steps"] == 25_600
    assert (
        plan["comparison"]["training_hyperparameters"]
        == _load(ROOT / "configs" / "methods" / "rl_v0.4" / "sac_training_plan.json")["training"][
            "hyperparameters"
        ]
    )
    assert plan["evidence_boundary"]["bench_accessed"] is False
    assert plan["evidence_boundary"]["reference_search_used"] is False
    assert plan["comparability_boundary"]["native_hybrid_distribution"] is False


def test_sac_preflight_rejects_posthoc_threshold_drift() -> None:
    plan = _load(PLAN_PATH)
    protocol = _load(PROTOCOL_PATH)
    plan["gate"]["minimum_tasks_with_learning_signal"] = 1

    with pytest.raises(SACPreflightError, match="gate_frozen"):
        validate_plan(plan, protocol)


def test_sac_preflight_learning_gate_passes_only_with_operational_tasks() -> None:
    plan = _load(PLAN_PATH)

    passing = assess_gate(plan, _jobs())
    failing = assess_gate(plan, _jobs(runtime_failure_task="partition-discovery"))

    assert passing["passed"] is True
    assert passing["learning_signal_task_count"] == 4
    assert passing["status"] == "sac_v048_preflight_passed_full_matrix_allowed"
    assert failing["passed"] is False
    assert failing["failed_checks"] == ["all_tasks_operational"]
    assert failing["status"] == "sac_v048_preflight_failed_full_matrix_forbidden"


def test_sac_preflight_requires_exact_four_task_set() -> None:
    plan = _load(PLAN_PATH)
    jobs = _jobs()
    jobs.pop()

    with pytest.raises(SACPreflightError, match="all four"):
        assess_gate(plan, jobs)


def test_sac_claim_owns_every_new_preflight_path() -> None:
    active = ROOT / "claims" / "active" / "benchmark-v05-rl-adapters--slice-sac-train-dev.json"
    completed = sorted(
        (ROOT / "claims" / "completed").glob(
            "benchmark-v05-rl-adapters--slice-sac-train-dev--*.json"
        )
    )
    claim = _load(next(path for path in reversed([*completed, active]) if path.is_file()))
    owned = set(claim["owned_paths"])

    assert {
        "configs/methods/rl_v0.4/sac_v048_preflight_plan.json",
        "scripts/run_sac_v048_preflight.py",
        "tests/test_sac_v048_preflight.py",
        "workstreams/benchmark_v1/reports/rl-sac-v048-preflight-v0.4.json",
    } <= owned


def test_full_sac_matrix_requires_exact_passing_current_source_report(
    tmp_path: Path,
) -> None:
    source_commit = "a" * 40
    preflight_plan = {"schema_version": PLAN_VERSION, "frozen": True}
    plan_path = tmp_path / "preflight-plan.json"
    report_path = tmp_path / "preflight-report.json"
    plan_path.write_text(json.dumps(preflight_plan) + "\n", encoding="utf-8")
    canonical = hashlib.sha256(
        json.dumps(preflight_plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    plan = {
        "algorithm": "sac",
        "task_id": "benchmark-v05-rl-adapters--slice-sac-train-dev",
        "current_contract_preflight": {
            "required_before_full_matrix": True,
            "plan": "preflight-plan.json",
            "report": "preflight-report.json",
            "required_report_schema": "chemworld-sac-v048-preflight-report-0.1",
            "required_status": "sac_v048_preflight_passed_full_matrix_allowed",
        },
    }
    report = {
        "schema_version": "chemworld-sac-v048-preflight-report-0.1",
        "status": "sac_v048_preflight_passed_full_matrix_allowed",
        "algorithm": "sac",
        "task_id": plan["task_id"],
        "source": {
            "source_commit": source_commit,
            "origin_main_commit": source_commit,
            "source_tree_clean": True,
            "source_commit_on_origin_main": True,
        },
        "preflight_plan_path": "preflight-plan.json",
        "preflight_plan_file_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
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
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")

    checks = verify_current_contract_preflight(
        root=tmp_path,
        plan=plan,
        source_commit=source_commit,
    )
    assert all(checks.values())

    report["full_matrix_allowed"] = False
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
    with pytest.raises(FormalPPOTrainingError, match="does not unlock"):
        verify_current_contract_preflight(
            root=tmp_path,
            plan=plan,
            source_commit=source_commit,
        )
