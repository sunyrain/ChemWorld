"""Agent-facing multi-round probe utilities."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean
from typing import Any

from chemworld.agents.llm import ToolUsingLLMStubAgent
from chemworld.data.logging import load_jsonl
from chemworld.data.submission import git_commit
from chemworld.data.validation import validate_records
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task

TOOL_AGENT_PROBE_SCHEMA_VERSION = "chemworld-tool-agent-probe-0.1"


@dataclass(frozen=True)
class ToolAgentProbeReport:
    schema_version: str
    generated_at: str
    commit_hash: str | None
    task_id: str
    agent_name: str
    seeds: list[int]
    budget: int
    min_rounds: int
    output_dir: str
    per_seed: list[dict[str, Any]]
    aggregate: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "commit_hash": self.commit_hash,
            "task_id": self.task_id,
            "agent_name": self.agent_name,
            "seeds": self.seeds,
            "budget": self.budget,
            "min_rounds": self.min_rounds,
            "output_dir": self.output_dir,
            "per_seed": self.per_seed,
            "aggregate": self.aggregate,
        }


def run_tool_agent_probe(
    *,
    task_id: str = "reaction-optimization-standard",
    seeds: list[int] | tuple[int, ...] = (0, 1, 2),
    budget: int | None = None,
    min_rounds: int = 12,
    output_dir: str | Path = Path("runs") / "tool_agent_probe",
) -> ToolAgentProbeReport:
    """Run ToolUsingLLMStubAgent over several seeds and summarize agent-facing metrics."""

    task = get_task(task_id)
    resolved_seeds = [int(seed) for seed in seeds]
    if not resolved_seeds:
        raise ValueError("seeds must be non-empty")
    resolved_budget = int(task.budget if budget is None else budget)
    if resolved_budget < min_rounds:
        raise ValueError("budget must be >= min_rounds")

    root = Path(output_dir)
    trajectory_dir = root / "trajectories"
    trajectory_dir.mkdir(parents=True, exist_ok=True)
    per_seed: list[dict[str, Any]] = []

    for seed in resolved_seeds:
        trajectory_path = trajectory_dir / f"tool_using_llm_stub_{task.task_id}_seed{seed}.jsonl"
        run_agent(
            env_id=task.env_id,
            agent=ToolUsingLLMStubAgent(),
            world_split=task.world_split,
            budget=resolved_budget,
            objective=task.objective,
            seed=seed,
            task_id=task.task_id,
            output_path=trajectory_path,
        )
        records = load_jsonl(trajectory_path)
        validate_records(records)
        if len(records) < min_rounds:
            raise RuntimeError(
                f"Probe for seed={seed} produced {len(records)} rounds; expected >= {min_rounds}"
            )
        metrics = evaluate_records(records, threshold=task.threshold)
        score_curve = _leaderboard_curve(records)
        trace = records[-1].get("agent_trace", [])
        first_score = _first_scored_value(records)
        observation_use = metrics.observation_use_summary
        per_seed.append(
            {
                "task_id": task.task_id,
                "seed": seed,
                "trajectory_path": str(trajectory_path),
                "decision_round_count": len(records),
                "agent_trace_step_count": len(trace) if isinstance(trace, list) else 0,
                "first_score": first_score,
                "best_score": metrics.final_best_score,
                "best_score_auc": metrics.area_under_best_score,
                "best_score_curve": score_curve,
                "invalid_action_count": metrics.invalid_action_count,
                "invalid_action_rate": metrics.invalid_action_rate,
                "precondition_failure_count": metrics.precondition_failure_count,
                "precondition_recovery_count": metrics.precondition_recovery_count,
                "final_assay_count": metrics.final_assay_count,
                "cost_aware_score": metrics.cost_aware_score,
                "safety_aware_score": metrics.safety_aware_score,
                "total_score": metrics.total_score,
                "instrument_counts": observation_use.get("instrument_counts", {}),
                "observed_key_counts": observation_use.get("observed_key_counts", {}),
                "final_lab_report_text": records[-1]
                .get("agent_view", {})
                .get("lab_report", {})
                .get("text", ""),
            }
        )

    aggregate = _aggregate_probe_rows(per_seed, min_rounds=min_rounds)
    report = ToolAgentProbeReport(
        schema_version=TOOL_AGENT_PROBE_SCHEMA_VERSION,
        generated_at=datetime.now(UTC).isoformat(),
        commit_hash=git_commit(),
        task_id=task.task_id,
        agent_name=ToolUsingLLMStubAgent.name,
        seeds=resolved_seeds,
        budget=resolved_budget,
        min_rounds=min_rounds,
        output_dir=str(root),
        per_seed=per_seed,
        aggregate=aggregate,
    )
    _write_probe_outputs(root, report)
    return report


def _leaderboard_curve(records: list[dict[str, Any]]) -> list[float]:
    best = 0.0
    curve: list[float] = []
    for record in records:
        value = record.get("leaderboard_score")
        if value is not None:
            best = max(best, float(value))
        curve.append(best)
    return curve


def _first_scored_value(records: list[dict[str, Any]]) -> float:
    for record in records:
        value = record.get("leaderboard_score")
        if value is not None:
            return float(value)
    return 0.0


def _aggregate_probe_rows(rows: list[dict[str, Any]], *, min_rounds: int) -> dict[str, Any]:
    metric_keys = [
        "decision_round_count",
        "agent_trace_step_count",
        "first_score",
        "best_score",
        "best_score_auc",
        "invalid_action_count",
        "invalid_action_rate",
        "precondition_failure_count",
        "precondition_recovery_count",
        "final_assay_count",
        "cost_aware_score",
        "safety_aware_score",
        "total_score",
    ]
    aggregate = {
        f"mean_{key}": float(fmean(float(row[key]) for row in rows)) for key in metric_keys
    }
    aggregate.update(
        {
            "seed_count": len(rows),
            "all_min_rounds_satisfied": all(
                int(row["decision_round_count"]) >= min_rounds for row in rows
            ),
            "all_trace_present": all(
                int(row["agent_trace_step_count"]) >= int(row["decision_round_count"])
                for row in rows
            ),
            "total_invalid_actions": int(sum(int(row["invalid_action_count"]) for row in rows)),
        }
    )
    return aggregate


def _write_probe_outputs(root: Path, report: ToolAgentProbeReport) -> None:
    root.mkdir(parents=True, exist_ok=True)
    payload = report.to_dict()
    with (root / "tool_agent_probe_report.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    with (root / "tool_agent_probe_summary.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        fieldnames = [
            "task_id",
            "seed",
            "decision_round_count",
            "agent_trace_step_count",
            "first_score",
            "best_score",
            "best_score_auc",
            "invalid_action_count",
            "invalid_action_rate",
            "precondition_failure_count",
            "precondition_recovery_count",
            "final_assay_count",
            "cost_aware_score",
            "safety_aware_score",
            "total_score",
            "trajectory_path",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in report.per_seed:
            writer.writerow({field: row.get(field) for field in fieldnames})


__all__ = [
    "TOOL_AGENT_PROBE_SCHEMA_VERSION",
    "ToolAgentProbeReport",
    "run_tool_agent_probe",
]
