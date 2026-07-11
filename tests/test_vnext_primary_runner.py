from __future__ import annotations

from scripts.run_vnext_primary import build_primary_jobs, build_primary_statistics

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.confirmatory_freeze import load_confirmatory_freeze
from chemworld.eval.suite import run_suite
from chemworld.tasks import get_task


def test_primary_job_plan_matches_frozen_core_method_seed_matrix(tmp_path) -> None:
    protocol = load_confirmatory_freeze()
    jobs = build_primary_jobs(
        protocol=protocol,
        output_dir=tmp_path,
        evaluated_source_commit="a" * 40,
    )
    assert len(jobs) == 8
    assert {job.task_id for job in jobs} == set(protocol["task_roles"]["core"])
    assert {job.method_id for job in jobs} == {"structured_gp_bo", "random"}
    assert all(job.seeds == tuple(range(20, 40)) for job in jobs)
    assert all(job.complete_experiments == 40 for job in jobs)
    assert all(
        job.operation_budget == task_recipe_event_count(get_task(job.task_id).to_dict()) * 40
        for job in jobs
    )


def test_primary_statistics_apply_task_sesoi_and_holm_without_scalarization() -> None:
    protocol = load_confirmatory_freeze()
    results = []
    for task_id in protocol["task_roles"]["core"]:
        field = PRIMARY_METRIC_FIELDS[task_id]
        sesoi = float(protocol["sesoi"]["tasks"][task_id]["sesoi"])
        budget = task_recipe_event_count(get_task(task_id).to_dict()) * 40
        for seed in range(20, 40):
            common = {
                "task_id": task_id,
                "seed": seed,
                "evaluation_budget_steps": budget,
            }
            results.append(
                {
                    **common,
                    "baseline_agent": "random",
                    field: 0.4 + seed * 1.0e-4,
                }
            )
            results.append(
                {
                    **common,
                    "baseline_agent": "structured_gp_bo",
                    field: 0.4 + seed * 1.0e-4 + 1.2 * sesoi,
                }
            )
    statistics = build_primary_statistics(results, protocol=protocol)
    assert statistics["cross_task_performance_score"] is None
    assert statistics["all_task_joint_rule_passed"] is True
    assert all(
        card["direction_passed"] and card["multiplicity_passed"] and card["sesoi_passed"]
        for card in statistics["task_decisions"].values()
    )
    assert all(
        card["holm_adjusted_p_value"] <= 0.05 for card in statistics["task_decisions"].values()
    )
    assert statistics["benchmark_claim_allowed"] is False


def test_suite_can_bind_vnext_risk_policy(tmp_path) -> None:
    task_id = "partition-discovery"
    task = get_task(task_id)
    results = run_suite(
        agent_name="random",
        env_id=task.env_id,
        world_splits=[task.world_split],
        seeds=[20],
        budget=task.budget,
        budget_override=task_recipe_event_count(task.to_dict()),
        objective=task.objective,
        output_dir=tmp_path,
        threshold=task.threshold,
        task_id=task_id,
        evaluation_policy="vnext_risk_cost",
    )
    assert len(results) == 1
    assert results[0]["verified"] is True
    assert results[0]["resource_usage"]["complete_experiment_count"] == 1
    contract = results[0]["score_replay"]["task_evaluation_contract"]
    assert contract["risk_limit_semantics"] == "benchmark_operational_risk_budget"
