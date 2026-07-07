"""Batch evaluation suites across splits and seeds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.data.validation import validate_records
from chemworld.eval.metrics import evaluate_records
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
            run_agent(
                env_id=env_id,
                agent=agent,
                world_split=split,
                budget=budget,
                objective=objective,
                seed=seed,
                output_path=trajectory_path,
            )
            records = load_jsonl(trajectory_path)
            validate_records(records)
            result = evaluate_records(records).to_dict()
            result["trajectory_path"] = str(trajectory_path)
            result_path = result_dir / (trajectory_path.stem + ".json")
            with result_path.open("w", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2, sort_keys=True)
            result["result_path"] = str(result_path)
            results.append(result)

    manifest_path = root / "suite_results.json"
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, sort_keys=True)
    return results
