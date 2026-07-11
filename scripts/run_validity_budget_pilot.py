"""Run paired baselines with task-specific learning-opportunity budgets."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.data.submission import git_commit
from chemworld.eval.seed_suite import task_seed_plan
from chemworld.eval.suite import run_suite
from chemworld.eval.validity_power import (
    audit_validity_power,
    minimum_learning_capacity,
)
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.parameters import WORLD_FAMILY_VERSION

DEFAULT_AGENTS = ("random", "gp_bo", "safe_gp_bo")


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", nargs="+", default=list(SERIOUS_TASK_IDS))
    parser.add_argument("--agents", nargs="+", default=list(DEFAULT_AGENTS))
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(5)))
    parser.add_argument(
        "--complete-experiments",
        type=int,
        help=(
            "Use this many complete experiments for every task instead of the "
            "dimension-aware minimum. Intended for long-horizon diagnostics."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/validity_power/calibrated_budget_pilot"),
    )
    args = parser.parse_args()
    if args.complete_experiments is not None and args.complete_experiments < 2:
        parser.error("--complete-experiments must be at least two")

    root = args.output_dir
    root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    budgets: dict[str, dict[str, int]] = {}
    seed_plan = task_seed_plan(args.tasks, override_seeds=args.seeds)
    for task_id in args.tasks:
        task = get_task(task_id)
        task_info = task.to_dict()
        minimum_experiments = minimum_learning_capacity(task_info)
        complete_experiments = (
            args.complete_experiments
            if args.complete_experiments is not None
            else minimum_experiments
        )
        diagnostic_budget = task_recipe_event_count(task_info) * complete_experiments
        budgets[task_id] = {
            "official_budget_steps": task.budget,
            "diagnostic_budget_steps": diagnostic_budget,
            "minimum_complete_experiments": minimum_experiments,
            "evaluated_complete_experiments": complete_experiments,
        }
        for agent in args.agents:
            task_results = run_suite(
                agent_name=agent,
                env_id=task.env_id,
                world_splits=[task.world_split],
                seeds=seed_plan[task_id],
                budget=task.budget,
                budget_override=diagnostic_budget,
                objective=task.objective,
                output_dir=root / "runs" / task_id / agent,
                threshold=task.threshold,
                task_id=task_id,
            )
            for result in task_results:
                result.update(
                    {
                        "task_id": task_id,
                        "baseline_agent": agent,
                        "evaluation_budget_steps": diagnostic_budget,
                        **budgets[task_id],
                    }
                )
                results.append(result)

    result_path = root / "baseline_results.json"
    result_path.write_bytes(
        (json.dumps(results, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    adaptive_pairs = tuple((agent, "random") for agent in args.agents if agent != "random")
    audit = audit_validity_power(
        results,
        task_ids=tuple(args.tasks),
        method_pairs=adaptive_pairs,
        adaptive_method_pairs=adaptive_pairs,
        planned_seed_count=20,
    )
    audit_path = root / "validity_power.json"
    audit_path.write_bytes(
        (json.dumps(audit, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    manifest = {
        "schema_version": "chemworld-validity-budget-pilot-0.1",
        "status": "diagnostic_only",
        "paper_claim_allowed": False,
        "generated_at": datetime.now(UTC).isoformat(),
        "evaluated_source_commit": git_commit(),
        "evaluation_source_tree_dirty": _tracked_tree_dirty(),
        "world_law_id": WORLD_FAMILY_VERSION,
        "tasks": list(args.tasks),
        "agents": list(args.agents),
        "seeds": list(args.seeds),
        "requested_complete_experiments": args.complete_experiments,
        "budgets": budgets,
        "result_count": len(results),
        "baseline_results": str(result_path),
        "validity_power": str(audit_path),
    }
    (root / "manifest.json").write_bytes(
        (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
