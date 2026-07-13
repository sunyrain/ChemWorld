from __future__ import annotations

import json

import pytest
from scripts.run_safe_policy_confirmatory import (
    DEFAULT_PROTOCOL,
    build_confirmatory_jobs,
    build_confirmatory_statistics,
    load_confirmatory_protocol,
)


def _result(task: str, method: str, seed: int, metric: str) -> dict:
    objective = {
        "structured_safe_gp_bo": 0.70 + (seed % 3) * 0.001,
        "structured_gp_bo": 0.72 + (seed % 3) * 0.001,
        "random": 0.60 + (seed % 3) * 0.001,
    }[method]
    risk = {
        "structured_safe_gp_bo": 0.05,
        "structured_gp_bo": 0.40,
        "random": 0.15,
    }[method]
    return {
        "task_id": task,
        "baseline_agent": method,
        "seed": seed,
        metric: objective,
        "score_replay": {
            "layered_evaluation": {
                "constraints": {"risk_budget_exceedance_rate": risk},
                "resources": {
                    "campaign_total_cost": 100.0,
                    "complete_experiment_count": 40,
                },
            }
        },
    }


def test_superseded_confirmatory_freeze_rejects_changed_policy_source(tmp_path) -> None:
    protocol = json.loads(DEFAULT_PROTOCOL.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="frozen policy source changed"):
        load_confirmatory_protocol()

    jobs = build_confirmatory_jobs(
        protocol,
        output_dir=tmp_path,
        evaluated_source_commit="a" * 40,
    )
    used = {
        int(seed)
        for cohort in protocol["previously_used_seeds"].values()
        for seed in cohort
    }
    assert len(jobs) == 12
    assert all(job.seeds == tuple(range(500, 520)) for job in jobs)
    assert not set(jobs[0].seeds) & used
    assert protocol["policy_identity"]["recipe_space_version"] == (
        "chemworld-task-recipe-space-0.2"
    )
    assert protocol["selection_evidence"]["development_results_are_confirmatory"] is False


def test_confirmatory_statistics_require_objective_safety_and_cost_on_every_task() -> None:
    protocol = json.loads(DEFAULT_PROTOCOL.read_text(encoding="utf-8"))
    metric_by_task = {
        "partition-discovery": "mean_product_in_organic",
        "reaction-to-crystallization": "mean_crystal_yield",
        "reaction-to-distillation": "mean_distillate_purity",
        "flow-reaction-optimization": "mean_flow_conversion",
    }
    results = [
        _result(task, method, seed, metric_by_task[task])
        for task in protocol["tasks"]
        for method in protocol["methods"]
        for seed in protocol["paired_confirmatory_seeds"]
    ]
    statistics = build_confirmatory_statistics(results, protocol=protocol)
    assert statistics["all_task_objective_rule_passed"] is True
    assert statistics["all_task_constraint_rule_passed"] is True
    assert statistics["all_task_joint_rule_passed"] is True
    assert statistics["secondary_safe_vs_unconstrained_gp"]["confirmatory_claim"] is False
    assert statistics["benchmark_claim_allowed"] is False
    assert statistics["publication_ready"] is False
