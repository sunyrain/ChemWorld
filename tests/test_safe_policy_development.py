from __future__ import annotations

from scripts.run_safe_policy_development import (
    build_development_jobs,
    build_development_summary,
    load_development_protocol,
)


def _result(task: str, method: str, seed: int, metric: str) -> dict:
    safe = method == "structured_safe_gp_bo"
    return {
        "task_id": task,
        "baseline_agent": method,
        "seed": seed,
        metric: 0.50 if safe else 0.49,
        "score_replay": {
            "layered_evaluation": {
                "constraints": {
                    "risk_budget_exceedance_rate": 0.10 if safe else 0.12
                },
                "resources": {
                    "campaign_total_cost": 100.0,
                    "complete_experiment_count": 40,
                },
            }
        },
    }


def test_development_jobs_use_dev_only_matrix(tmp_path) -> None:
    protocol = load_development_protocol()
    jobs = build_development_jobs(
        protocol,
        output_dir=tmp_path,
        evaluated_source_commit="a" * 40,
    )
    assert len(jobs) == 12
    assert all(job.seeds == tuple(range(1100, 1120)) for job in jobs)
    assert not set(jobs[0].seeds) & set(protocol["bench_seeds_forbidden"])
    assert {job.method_id for job in jobs} == {
        "structured_safe_gp_bo",
        "structured_gp_bo",
        "random",
    }


def test_development_summary_can_select_safe_policy_without_claiming() -> None:
    protocol = load_development_protocol()
    results = []
    metric_by_task = {
        "partition-discovery": "mean_product_in_organic",
        "reaction-to-crystallization": "mean_crystal_yield",
        "reaction-to-distillation": "mean_distillate_purity",
        "flow-reaction-optimization": "mean_flow_conversion",
    }
    for task in protocol["tasks"]:
        for method in protocol["methods"]:
            for seed in protocol["dev_seeds"]:
                results.append(_result(task, method, seed, metric_by_task[task]))
    summary = build_development_summary(results, protocol=protocol)
    assert summary["result_count"] == 240
    assert summary["objective_retention_all_tasks_passed"] is True
    assert summary["constraints_vs_random_all_tasks_passed"] is True
    assert summary["selected_for_future_freeze"] is True
    assert summary["benchmark_claim_allowed"] is False
    assert summary["publication_ready"] is False
