from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_ppo_v048_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
PARENT_PLAN_PATH = ROOT / "configs/methods/rl_v0.4/ppo_v0410_preflight_plan.json"
PLAN_PATH = ROOT / "configs/methods/rl_v0.4/ppo_v0411_preflight_plan.json"
NEGATIVE_REPORT_PATH = (
    ROOT / "workstreams/benchmark_v1/reports/rl-ppo-v0410-preflight-v0.4.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _evaluated(count: int, endpoint: float) -> dict[str, Any]:
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
            "complete_experiment_count": count,
            "episode_completion_rate": count / 20,
            "behavior_complete_experiment_count": count,
            "behavior_complete_experiment_rate": count / 20,
            "quick_close_rate": 0.0,
            "invalid_action_rate": 0.0,
            "unsafe_step_rate": 0.0,
            "high_cost_step_rate": 0.0,
            "runtime_domain_failure_count": 0,
            "observation_domain_failure_count": 0,
            "primary_metric_observation_count": count,
            "mean_episode_best_primary_metric": endpoint,
        },
    }


def test_public_precondition_retry_is_frozen_and_namespaced() -> None:
    parent = _load(PARENT_PLAN_PATH)
    plan = _load(PLAN_PATH)
    protocol = _load(ROOT / str(plan["formal_protocol_path"]))

    checks = preflight.validate_plan(plan, protocol)
    evidence = preflight.validate_adapter_reattestation(ROOT, plan)

    assert all(checks.values())
    assert plan["schema_version"] == preflight.PUBLIC_PRECONDITION_PLAN_VERSION
    assert preflight.scientific_contract_sha256(parent) == preflight.scientific_contract_sha256(
        plan
    )
    assert plan["comparison"] == parent["comparison"]
    assert plan["development_evaluation"] == parent["development_evaluation"]
    assert plan["gate"] == parent["gate"]
    assert plan["adapter_reattestation"]["conditional_hybrid_action_schema_version"].endswith(
        "0.3"
    )
    assert "public-preconditions-v0411" in plan["writer_gate_path"]
    assert evidence["ppo_v0410_negative_report"]["full_matrix_allowed"] is False

    full_plan = _load(ROOT / str(plan["execution"]["full_training_plan"]))
    assert full_plan["current_contract_preflight"]["plan"] == PLAN_PATH.relative_to(
        ROOT
    ).as_posix()
    assert full_plan["current_contract_preflight"]["required_status"] == (
        "ppo_v0411_preflight_passed_full_matrix_allowed"
    )


def test_public_precondition_retry_rejects_tampered_negative_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = _load(PLAN_PATH)
    real_load = preflight._load_object

    def tampered_load(path: Path, label: str) -> dict[str, Any]:
        payload = real_load(path, label)
        if path.resolve() == NEGATIVE_REPORT_PATH.resolve():
            payload = copy.deepcopy(payload)
            payload["status"] = "ppo_v0410_preflight_passed_full_matrix_allowed"
        return payload

    monkeypatch.setattr(preflight, "_load_object", tampered_load)
    with pytest.raises(preflight.PPOPreflightError, match="negative_report_status"):
        preflight.validate_adapter_reattestation(ROOT, plan)


def test_public_precondition_retry_uses_v0411_gate_status() -> None:
    plan = _load(PLAN_PATH)
    jobs = []
    for index, (task_id, spec) in enumerate(plan["formal_core_tasks"].items()):
        jobs.append(
            {
                "task_id": task_id,
                "step0_evaluation": _evaluated(1, 0.0),
                "trained_evaluation": _evaluated(
                    2 if index < 2 else 1,
                    float(spec["sesoi"]) if index < 2 else 0.0,
                ),
            }
        )

    assessment = preflight.assess_gate(plan, jobs)

    assert assessment["passed"] is True
    assert assessment["status"] == "ppo_v0411_preflight_passed_full_matrix_allowed"
