from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_ppo_v048_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
PARENT_PLAN_PATH = ROOT / "configs/methods/rl_v0.4/ppo_v049_preflight_plan.json"
PLAN_PATH = ROOT / "configs/methods/rl_v0.4/ppo_v0410_preflight_plan.json"
SAC_DIAGNOSTIC_PATH = ROOT / "workstreams/benchmark_v1/reports/rl-sac-v049-preflight-v0.4.json"


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


def test_public_schema_reattestation_keeps_scientific_settings_and_is_namespaced() -> None:
    parent = _load(PARENT_PLAN_PATH)
    plan = _load(PLAN_PATH)
    protocol = _load(ROOT / str(plan["formal_protocol_path"]))

    checks = preflight.validate_plan(plan, protocol)
    evidence = preflight.validate_adapter_reattestation(ROOT, plan)

    assert all(checks.values())
    assert plan["schema_version"] == preflight.PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION
    assert preflight.scientific_contract_sha256(parent) == preflight.scientific_contract_sha256(
        plan
    )
    assert plan["comparison"] == parent["comparison"]
    assert plan["development_evaluation"] == parent["development_evaluation"]
    assert plan["gate"] == parent["gate"]
    assert plan["adapter_reattestation"]["subprocess_worker_layout"] == (
        "spawn_single_batched_environment_worker"
    )
    assert plan["adapter_reattestation"]["parallel_environment_count_unchanged"] is True
    assert plan["adapter_reattestation"]["vector_slot_order_parity_required"] is True
    assert "post-affordance-v0410" in plan["writer_gate_path"]
    assert "post-affordance-v0410" in plan["execution"]["artifact_root"]
    failure = evidence["ppo_infrastructure_failure"]
    assert failure["observed_work"]["training_environment_step_count"] == 0
    assert failure["observed_work"]["outcome_metric_observed"] is False
    assert evidence["sac_adapter_diagnostic"]["full_matrix_allowed"] is False


def test_reattestation_rejects_tampered_adapter_diagnostic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = _load(PLAN_PATH)
    real_load = preflight._load_object

    def tampered_load(path: Path, label: str) -> dict[str, Any]:
        payload = real_load(path, label)
        if path.resolve() == SAC_DIAGNOSTIC_PATH.resolve():
            payload = copy.deepcopy(payload)
            payload["gate_assessment"]["learning_signal_task_count"] = 2
        return payload

    monkeypatch.setattr(preflight, "_load_object", tampered_load)
    with pytest.raises(preflight.PPOPreflightError, match="sac_diagnostic"):
        preflight.validate_adapter_reattestation(ROOT, plan)


def test_adapter_gate_keeps_v049_thresholds_and_uses_v0410_status() -> None:
    parent = _load(PARENT_PLAN_PATH)
    plan = _load(PLAN_PATH)
    jobs = []
    for index, (task_id, spec) in enumerate(plan["formal_core_tasks"].items()):
        before = 1
        after = 2 if index < 2 else 1
        jobs.append(
            {
                "task_id": task_id,
                "step0_evaluation": _evaluated(before, 0.0),
                "trained_evaluation": _evaluated(
                    after, float(spec["sesoi"]) if index < 2 else 0.0
                ),
            }
        )

    assessment = preflight.assess_gate(plan, jobs)

    assert plan["gate"] == parent["gate"]
    assert assessment["passed"] is True
    assert assessment["status"] == "ppo_v0410_preflight_passed_full_matrix_allowed"
