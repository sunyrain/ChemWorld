from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.rl.rewards import PublicBehaviorTracker
from chemworld.tasks import FLAGSHIP_TASK_IDS, get_task

REPORT_SCHEMA_VERSION = "chemworld-flagship-task-closure-0.1"


def _latin_hypercube(samples: int, dimensions: int, rng: np.random.Generator) -> np.ndarray:
    points = np.empty((samples, dimensions), dtype=float)
    for column in range(dimensions):
        points[:, column] = (rng.permutation(samples) + rng.random(samples)) / samples
    return points


def _finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _run_recipe(task_id: str, vector: np.ndarray, seed: int) -> dict[str, Any]:
    task = get_task(task_id)
    recipe = task_recipe_from_unit_vector(task.to_dict(), vector)
    env = gym.make(
        "ChemWorld",
        task_id=task_id,
        budget_override=len(recipe["steps"]) + 1,
        episode_mode_override="campaign",
    )
    behavior = PublicBehaviorTracker(task.allowed_operations, task_id=task_id)
    failures = {
        "invalid_action_count": 0,
        "transaction_rollback_count": 0,
        "constitution_failure_count": 0,
        "runtime_domain_failure_count": 0,
        "observation_domain_failure_count": 0,
    }
    final_info: dict[str, Any] = {}
    try:
        env.reset(seed=seed)
        for action in recipe["steps"]:
            _, _, _, _, final_info = env.step(action)
            behavior.observe(final_info)
            flags = dict(final_info.get("constraint_flags", {}))
            preconditions = dict(final_info.get("preconditions", {}))
            failures["invalid_action_count"] += int(flags.get("precondition_failed", False))
            failures["transaction_rollback_count"] += int(
                final_info.get("transaction_status") == "rolled_back"
            )
            failures["constitution_failure_count"] += int(flags.get("constitution_failed", False))
            failures["runtime_domain_failure_count"] += int(
                preconditions.get("runtime_domain_valid") is False
            )
            failures["observation_domain_failure_count"] += int(
                preconditions.get("observation_domain_valid") is False
            )
    finally:
        env.close()
    estimates = dict(final_info.get("processed_estimate", {}))
    return {
        "seed": seed,
        "vector": [float(value) for value in vector],
        "operation_count": len(recipe["steps"]),
        "experiment_completed": bool(final_info.get("experiment_ended", False)),
        "behavior_complete": behavior.complete,
        "behavior_tokens": sorted(behavior.tokens),
        "leaderboard_score": _finite_number(final_info.get("leaderboard_score")),
        "metrics": {
            metric: _finite_number(estimates.get(metric))
            for metric in task.success_metrics
            if metric not in {"score", "safety_risk"}
        },
        **failures,
    }


def _range(values: list[float]) -> float:
    return max(values) - min(values) if values else 0.0


def _correlations(vectors: np.ndarray, values: np.ndarray) -> list[float | None]:
    correlations: list[float | None] = []
    for column in range(vectors.shape[1]):
        x = vectors[:, column]
        if np.std(x) <= 1.0e-12 or np.std(values) <= 1.0e-12:
            correlations.append(None)
            continue
        correlations.append(float(np.corrcoef(x, values)[0, 1]))
    return correlations


def _reference_vectors(task_id: str, dimension: int) -> np.ndarray:
    midpoint = np.full(dimension, 0.5, dtype=float)
    if task_id == "reaction-to-crystallization":
        # Public slow-cooling anchor: it is not claimed optimal, but exercises
        # the low-cooling-rate/high-growth region that a small LHS can miss.
        slow_cooling = np.asarray(
            [0.70, 0.20, 0.50, 0.50, 0.10, 0.50, 0.10, 0.64, 0.222, 0.97],
            dtype=float,
        )
        return np.vstack([midpoint, slow_cooling])
    return midpoint.reshape(1, -1)


def audit_task(task_id: str, *, samples: int, seeds: tuple[int, ...]) -> dict[str, Any]:
    task = get_task(task_id)
    dimension = task_recipe_dimension(task.to_dict())
    rng = np.random.default_rng(20260717 + sum(ord(char) for char in task_id))
    reference_vectors = _reference_vectors(task_id, dimension)
    design = np.vstack([_latin_hypercube(samples, dimension, rng), reference_vectors])
    records = [_run_recipe(task_id, vector, seed) for seed in seeds for vector in design]
    scores = [
        float(record["leaderboard_score"])
        for record in records
        if record["leaderboard_score"] is not None
    ]
    vectors = np.asarray([record["vector"] for record in records], dtype=float)
    score_array = np.asarray(scores, dtype=float)
    metric_ranges: dict[str, float] = {}
    metric_correlations: dict[str, list[float | None]] = {}
    for metric in task.success_metrics:
        if metric in {"score", "safety_risk"}:
            continue
        values = [
            float(record["metrics"][metric])
            for record in records
            if record["metrics"].get(metric) is not None
        ]
        metric_ranges[metric] = _range(values)
        if len(values) == len(records):
            metric_correlations[metric] = _correlations(
                vectors,
                np.asarray(values, dtype=float),
            )
    failure_totals = {
        key: sum(int(record[key]) for record in records)
        for key in (
            "invalid_action_count",
            "transaction_rollback_count",
            "constitution_failure_count",
            "runtime_domain_failure_count",
            "observation_domain_failure_count",
        )
    }
    best = max(records, key=lambda record: float(record["leaderboard_score"] or 0.0))
    responsive_metric_count = sum(value >= 0.01 for value in metric_ranges.values())
    gates = {
        "all_experiments_complete": all(record["experiment_completed"] for record in records),
        "all_behavior_complete": all(record["behavior_complete"] for record in records),
        "zero_execution_failures": not any(failure_totals.values()),
        "score_range_at_least_0_02": _range(scores) >= 0.02,
        "at_least_three_responsive_metrics": responsive_metric_count >= 3,
        "declared_threshold_observed": float(best["leaderboard_score"] or 0.0) >= task.threshold,
    }
    return {
        "task_id": task_id,
        "task_contract_hash": task.contract_hash,
        "samples_per_seed": samples,
        "reference_vector_count": int(reference_vectors.shape[0]),
        "seeds": list(seeds),
        "recipe_dimension": dimension,
        "record_count": len(records),
        "score_summary": {
            "minimum": min(scores),
            "mean": statistics.fmean(scores),
            "maximum": max(scores),
            "range": _range(scores),
        },
        "metric_ranges": metric_ranges,
        "score_coordinate_correlations": _correlations(vectors, score_array),
        "metric_coordinate_correlations": metric_correlations,
        "responsive_metric_count": responsive_metric_count,
        "failure_totals": failure_totals,
        "best_record": best,
        "gates": gates,
        "task_ready": all(gates.values()),
    }


def build_report(*, samples: int, seeds: tuple[int, ...]) -> dict[str, Any]:
    tasks = {
        task_id: audit_task(task_id, samples=samples, seeds=seeds) for task_id in FLAGSHIP_TASK_IDS
    }
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "scope": list(FLAGSHIP_TASK_IDS),
        "formal_evidence": False,
        "purpose": "development closure before frozen learning evaluation",
        "tasks": tasks,
        "all_tasks_ready": all(task["task_ready"] for task in tasks.values()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/flagship_tasks/reports/flagship-task-closure.json"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.samples < 4 or not args.seeds:
        raise ValueError("at least four samples and one seed are required")
    report = build_report(samples=args.samples, seeds=tuple(args.seeds))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "all_tasks_ready": report["all_tasks_ready"],
                "tasks": {
                    task_id: {
                        "task_ready": task["task_ready"],
                        "score_summary": task["score_summary"],
                        "gates": task["gates"],
                    }
                    for task_id, task in report["tasks"].items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
