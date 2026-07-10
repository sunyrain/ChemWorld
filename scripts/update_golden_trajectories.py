"""Regenerate core-task golden trajectory fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from chemworld.data.logging import load_jsonl
from chemworld.eval.golden import (
    core_golden_targets,
    summarize_golden_records,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.tasks import TASK_REGISTRY


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    fixture_path = root / "tests" / "fixtures" / "golden" / (
        "core_scripted_trajectories.json"
    )
    scratch = root / "runs" / "golden"
    scratch.mkdir(parents=True, exist_ok=True)
    fixture_path.parent.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, object]] = []
    for target in core_golden_targets():
        task = TASK_REGISTRY[target.task_id]
        trajectory_path = scratch / f"{target.task_id}_seed{target.seed}.jsonl"
        run_agent(
            env_id="ChemWorld",
            agent=make_agent(target.agent_name),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=target.seed,
            task_id=target.task_id,
            output_path=trajectory_path,
        )
        summaries.append(summarize_golden_records(load_jsonl(trajectory_path)))

    payload = {
        "fixture_schema_version": "chemworld-golden-fixture-0.1",
        "description": (
            "Canonical scripted trajectories for the three compact core "
            "ChemWorld benchmark tasks."
        ),
        "summaries": summaries,
    }
    fixture_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {fixture_path}")


if __name__ == "__main__":
    main()
