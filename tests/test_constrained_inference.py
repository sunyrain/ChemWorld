from __future__ import annotations

import copy

from chemworld.eval.constrained_inference import paired_constraint_decisions


def _result(*, task: str, method: str, seed: int, risk: float, cost: float) -> dict:
    return {
        "task_id": task,
        "baseline_agent": method,
        "seed": seed,
        "score_replay": {
            "layered_evaluation": {
                "constraints": {"risk_budget_exceedance_rate": risk},
                "resources": {
                    "campaign_total_cost": cost,
                    "complete_experiment_count": 40,
                },
            }
        },
    }


def test_paired_constraint_decisions_pass_small_safety_and_cost_deltas() -> None:
    results = []
    for seed in range(20):
        results.extend(
            [
                _result(task="task", method="random", seed=seed, risk=0.20, cost=100.0),
                _result(task="task", method="candidate", seed=seed, risk=0.21, cost=102.0),
            ]
        )
    audit = paired_constraint_decisions(
        results,
        task_ids=["task"],
        candidate="candidate",
        comparator="random",
        paired_seeds=list(range(20)),
        bootstrap_samples=5_000,
        upper_quantile=0.99375,
        safety_margin=0.05,
        cost_margin=0.05,
    )
    decision = audit["task_decisions"]["task"]
    assert decision["safety"]["noninferiority_passed"] is True
    assert decision["cost"]["noninferiority_passed"] is True
    assert audit["all_task_constraints_passed"] is True


def test_paired_constraint_decisions_fail_observed_safety_regression() -> None:
    results = []
    for seed in range(20):
        results.extend(
            [
                _result(task="task", method="random", seed=seed, risk=0.20, cost=100.0),
                _result(task="task", method="candidate", seed=seed, risk=0.45, cost=101.0),
            ]
        )
    audit = paired_constraint_decisions(
        results,
        task_ids=["task"],
        candidate="candidate",
        comparator="random",
        paired_seeds=list(range(20)),
        bootstrap_samples=5_000,
        upper_quantile=0.99375,
        safety_margin=0.05,
        cost_margin=0.05,
    )
    assert audit["task_decisions"]["task"]["safety"]["noninferiority_passed"] is False
    assert audit["all_task_constraints_passed"] is False


def test_constraint_bootstrap_is_order_invariant_and_deterministic() -> None:
    results = []
    for seed in range(20):
        results.extend(
            [
                _result(task="task", method="random", seed=seed, risk=0.1, cost=100 + seed),
                _result(
                    task="task",
                    method="candidate",
                    seed=seed,
                    risk=0.1 + seed / 1000,
                    cost=(100 + seed) * 1.01,
                ),
            ]
        )
    kwargs = {
        "task_ids": ["task"],
        "candidate": "candidate",
        "comparator": "random",
        "paired_seeds": list(range(20)),
        "bootstrap_samples": 5_000,
        "upper_quantile": 0.99375,
        "safety_margin": 0.05,
        "cost_margin": 0.05,
    }
    first = paired_constraint_decisions(copy.deepcopy(results), **kwargs)
    second = paired_constraint_decisions(list(reversed(results)), **kwargs)
    assert first == second
