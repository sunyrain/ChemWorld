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
    task_maturity: dict[str, dict[str, Any]]
    maturity_summary: dict[str, Any]
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
            "task_maturity": self.task_maturity,
            "maturity_summary": self.maturity_summary,
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

    task_maturity = {task_id: _task_maturity_payload(get_task(task_id)) for task_id in task_ids}
    validate_result_maturity_consistency(all_results, expected_by_task=task_maturity)
    maturity_summary = maturity_summary_for_results(all_results)

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
        task_maturity=task_maturity,
        maturity_summary=maturity_summary,
        leaderboard_rows=leaderboard_rows,
    )
    report_path = root / "baseline_report.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, sort_keys=True)
    return report


def _aggregate_task_leaderboards(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validate_result_maturity_consistency(results)
    by_task: dict[str, list[dict[str, Any]]] = {}
    for result in results:
        task_id = str(result.get("task_id") or result.get("benchmark_task_id") or "unknown")
        by_task.setdefault(task_id, []).append(result)

    rows: list[dict[str, Any]] = []
    for task_id, task_results in sorted(by_task.items()):
        maturity_payload = _result_maturity_payload(task_results[0])
        for row in aggregate_leaderboard(task_results):
            rows.append({"task_id": task_id, **maturity_payload, **row})
    rows.sort(key=lambda row: (str(row["task_id"]), int(row["rank"])))
    return rows


def _task_maturity_payload(task: Any) -> dict[str, Any]:
    payload = task.to_dict()
    return {
        "kernel_maturity": payload["kernel_maturity"],
        "physics_maturity": payload["physics_maturity"],
        "proxy_allowed": payload["proxy_allowed"],
    }


def _result_maturity_payload(result: dict[str, Any]) -> dict[str, Any]:
    missing = [
        key
        for key in ("kernel_maturity", "physics_maturity", "proxy_allowed")
        if key not in result
    ]
    if missing:
        raise ValueError(f"benchmark result missing maturity keys: {missing}")
    return {
        "kernel_maturity": result["kernel_maturity"],
        "physics_maturity": result["physics_maturity"],
        "proxy_allowed": bool(result["proxy_allowed"]),
    }


def validate_result_maturity_consistency(
    results: list[dict[str, Any]],
    *,
    expected_by_task: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Fail if benchmark results hide inconsistent physics-maturity metadata."""

    seen_by_task: dict[str, dict[str, Any]] = {}
    for result in results:
        task_id = str(result.get("task_id") or result.get("benchmark_task_id") or "unknown")
        maturity_payload = _result_maturity_payload(result)
        expected = None if expected_by_task is None else expected_by_task.get(task_id)
        if expected is not None and maturity_payload != expected:
            raise ValueError(
                f"benchmark result for {task_id!r} does not match task maturity metadata"
            )
        previous = seen_by_task.get(task_id)
        if previous is None:
            seen_by_task[task_id] = maturity_payload
        elif previous != maturity_payload:
            raise ValueError(f"mixed maturity metadata for benchmark task {task_id!r}")


def maturity_summary_for_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Return JSON-friendly run/task counts by physics maturity level."""

    validate_result_maturity_consistency(results)
    task_runs: dict[str, dict[str, Any]] = {}
    level_runs: dict[str, dict[str, Any]] = {}
    for result in results:
        task_id = str(result.get("task_id") or result.get("benchmark_task_id") or "unknown")
        maturity_payload = _result_maturity_payload(result)
        task_entry = task_runs.setdefault(
            task_id,
            {
                **maturity_payload,
                "runs": 0,
            },
        )
        task_entry["runs"] = int(task_entry["runs"]) + 1
        level = str(maturity_payload["physics_maturity"])
        level_entry = level_runs.setdefault(
            level,
            {
                "runs": 0,
                "tasks": set(),
                "proxy_allowed_runs": 0,
            },
        )
        level_entry["runs"] = int(level_entry["runs"]) + 1
        level_entry["tasks"].add(task_id)
        if maturity_payload["proxy_allowed"]:
            level_entry["proxy_allowed_runs"] = int(level_entry["proxy_allowed_runs"]) + 1

    return {
        "total_runs": len(results),
        "tasks": task_runs,
        "levels": {
            level: {
                "runs": entry["runs"],
                "tasks": sorted(entry["tasks"]),
                "proxy_allowed_runs": entry["proxy_allowed_runs"],
            }
            for level, entry in sorted(level_runs.items())
        },
    }


__all__ = [
    "DEFAULT_BASELINE_AGENTS",
    "BaselineReport",
    "generate_baseline_report",
    "maturity_summary_for_results",
    "validate_result_maturity_consistency",
]
