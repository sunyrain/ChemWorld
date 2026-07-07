"""Official baseline report generation for release artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld import __version__
from chemworld.data.submission import git_commit
from chemworld.eval.leaderboard import aggregate_leaderboard
from chemworld.eval.suite import run_suite
from chemworld.tasks import get_task

DEFAULT_BASELINE_AGENTS = (
    "random",
    "lhs",
    "scripted_chemistry",
    "gp_bo",
    "safe_gp_bo",
    "tool_using_llm_stub",
)


@dataclass(frozen=True)
class BaselineReport:
    schema_version: str
    generated_at: str
    chemworld_version: str
    commit_hash: str | None
    tasks: tuple[str, ...]
    agents: tuple[str, ...]
    seeds: tuple[int, ...]
    output_dir: str
    result_count: int
    leaderboard_rows: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "chemworld_version": self.chemworld_version,
            "commit_hash": self.commit_hash,
            "tasks": list(self.tasks),
            "agents": list(self.agents),
            "seeds": list(self.seeds),
            "output_dir": self.output_dir,
            "result_count": self.result_count,
            "leaderboard_rows": self.leaderboard_rows,
        }


def generate_baseline_report(
    *,
    task_ids: list[str],
    agents: list[str] | None = None,
    seeds: list[int] | None = None,
    output_dir: str | Path,
) -> BaselineReport:
    """Run selected official baselines and write a release-style report.

    The report is intentionally task-based: each task keeps its own budget,
    split, objective, threshold, and allowed operations. The caller can pass a
    small seed list for smoke tests or the full task seed list for a release.
    """

    resolved_agents = tuple(agents or DEFAULT_BASELINE_AGENTS)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    all_results: list[dict[str, Any]] = []
    resolved_seeds = tuple(seeds or ())

    for task_id in task_ids:
        task = get_task(task_id)
        task_seeds = list(resolved_seeds or task.seeds)
        for agent_name in resolved_agents:
            task_output = root / "runs" / task.task_id / agent_name
            results = run_suite(
                agent_name=agent_name,
                env_id=task.env_id,
                world_splits=[task.world_split],
                seeds=task_seeds,
                budget=task.budget,
                objective=task.objective,
                output_dir=task_output,
                threshold=task.threshold,
                task_id=task.task_id,
            )
            for result in results:
                result["task_id"] = task.task_id
                result["baseline_agent"] = agent_name
            all_results.extend(results)

    results_path = root / "baseline_results.json"
    with results_path.open("w", encoding="utf-8") as handle:
        json.dump(all_results, handle, indent=2, sort_keys=True)

    leaderboard_rows = _aggregate_task_leaderboards(all_results)
    leaderboard_path = root / "baseline_leaderboard.json"
    with leaderboard_path.open("w", encoding="utf-8") as handle:
        json.dump(leaderboard_rows, handle, indent=2, sort_keys=True)

    report = BaselineReport(
        schema_version="chemworld-baseline-report-0.1",
        generated_at=datetime.now(UTC).isoformat(),
        chemworld_version=__version__,
        commit_hash=git_commit(),
        tasks=tuple(task_ids),
        agents=resolved_agents,
        seeds=resolved_seeds,
        output_dir=str(root),
        result_count=len(all_results),
        leaderboard_rows=leaderboard_rows,
    )
    report_path = root / "baseline_report.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, sort_keys=True)
    return report


def _aggregate_task_leaderboards(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_task: dict[str, list[dict[str, Any]]] = {}
    for result in results:
        task_id = str(result.get("task_id") or result.get("benchmark_task_id") or "unknown")
        by_task.setdefault(task_id, []).append(result)

    rows: list[dict[str, Any]] = []
    for task_id, task_results in sorted(by_task.items()):
        for row in aggregate_leaderboard(task_results):
            rows.append({"task_id": task_id, **row})
    rows.sort(key=lambda row: (str(row["task_id"]), int(row["rank"])))
    return rows


__all__ = ["DEFAULT_BASELINE_AGENTS", "BaselineReport", "generate_baseline_report"]
