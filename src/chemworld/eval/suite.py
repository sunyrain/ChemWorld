"""Batch evaluation suites across splits and seeds."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.result_artifacts import build_verified_evaluation_result
from chemworld.eval.runner import make_agent, run_agent


def run_suite(
    *,
    agent_name: str,
    env_id: str,
    world_splits: list[str],
    seeds: list[int],
    budget: int,
    objective: str,
    output_dir: str | Path,
    threshold: float = 0.75,
    task_id: str | None = None,
    budget_override: int | None = None,
) -> list[dict[str, Any]]:
    """Run an agent across a matrix of splits and seeds, then evaluate runs."""

    root = Path(output_dir)
    trajectory_dir = root / "trajectories"
    result_dir = root / "results"
    trajectory_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for split in world_splits:
        for seed in seeds:
            trajectory_path = trajectory_dir / (
                f"{agent_name}_{env_id}_{split}_{objective}_seed{seed}.jsonl"
            )
            agent = make_agent(agent_name)
            run_wall_start = time.perf_counter()
            process_start = time.process_time()
            run_agent(
                env_id=env_id,
                agent=agent,
                world_split=split,
                budget=budget,
                objective=objective,
                seed=seed,
                task_id=task_id,
                output_path=trajectory_path,
                budget_override=budget_override,
            )
            run_wall_time = time.perf_counter() - run_wall_start
            evaluation_wall_start = time.perf_counter()
            records = load_jsonl(trajectory_path)
            result = build_verified_evaluation_result(
                records,
                trajectory_path=trajectory_path,
                threshold=threshold,
            )
            evaluation_wall_time = time.perf_counter() - evaluation_wall_start
            process_cpu_time = time.process_time() - process_start
            result.update(_maturity_payload(records[0]))
            result["resource_usage"] = {
                "schema_version": "chemworld-resource-usage-0.1",
                "run_wall_time_s": run_wall_time,
                "evaluation_wall_time_s": evaluation_wall_time,
                "total_wall_time_s": run_wall_time + evaluation_wall_time,
                "process_cpu_time_s": process_cpu_time,
                "step_count": int(result["steps"]),
                "complete_experiment_count": int(result["final_assay_count"]),
            }
            result_path = result_dir / (trajectory_path.stem + ".json")
            result["result_path"] = str(result_path.resolve())
            with result_path.open("w", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2, sort_keys=True)
            results.append(result)

    manifest_path = root / "suite_results.json"
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, sort_keys=True)
    return results


def _maturity_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "kernel_maturity": record.get("kernel_maturity", {}),
        "physics_maturity": record.get("physics_maturity"),
        "proxy_allowed": bool(record.get("proxy_allowed", False)),
    }
