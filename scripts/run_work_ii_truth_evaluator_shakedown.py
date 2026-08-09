#!/usr/bin/env python3
"""Run the zero-provider Work II held-out evaluator on five development tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_RAW = (
    ROOT / "runs/development/work-ii-held-out-evaluator-shakedown-v0.1"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-held-out-evaluator-development-shakedown-v0.1.json"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--raw-output", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def run(args: argparse.Namespace) -> dict[str, Any]:
    design = _load(args.design.resolve())
    raw_output = args.raw_output.resolve()
    if raw_output.exists():
        raise FileExistsError(f"refusing to overwrite development output: {raw_output}")
    raw_output.mkdir(parents=True)
    task_rows: list[dict[str, Any]] = []
    for task_index, task in enumerate(design["tasks"], start=1):
        task_id = str(task["task_id"])
        config_path = ROOT / str(task["campaign_config"])
        config = _load(config_path)
        cluster = {
            "world_cluster_id": f"work-ii-development-{task_index:02d}-seed0",
            "task_id": task_id,
            "world_seed": 0,
        }
        plan = build_evaluator_truth_plan(
            cluster,
            config,
            formal_result=False,
            formal_preflight_sha256=None,
        )
        print(
            json.dumps(
                {
                    "event": "task_started",
                    "task_index": task_index,
                    "task_count": len(design["tasks"]),
                    "task_id": task_id,
                    "query_count": plan["truth_query_count"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        task_output = raw_output / f"task-{task_index:02d}"
        report = execute_evaluator_truth_plan(plan, config, task_output)
        validation_errors = validate_evaluator_truth_report(report, plan)
        failures = [
            {
                "query_id": receipt["query_id"],
                "failure_type": receipt.get("failure_type"),
                "failure_message": receipt.get("failure_message"),
            }
            for receipt in report["receipts"]
            if receipt["status"] != "completed"
        ]
        exact_replay_count = sum(
            receipt.get("exact_replay", {}).get("verified") is True
            for receipt in report["receipts"]
        )
        row = {
            "task_id": task_id,
            "plan_sha256": plan["plan_sha256"],
            "report_sha256": report["report_sha256"],
            "query_count": report["truth_query_count"],
            "completed_query_count": report["completed_truth_query_count"],
            "failed_query_count": report["failed_truth_query_count"],
            "query_metric_count": report["truth_query_metric_count"],
            "completed_query_metric_count": report[
                "completed_truth_query_metric_count"
            ],
            "operation_attempt_count": sum(
                int(receipt.get("operation_attempt_count", 0))
                for receipt in report["receipts"]
            ),
            "exact_replay_count": exact_replay_count,
            "evaluator_provider_call_count": report[
                "evaluator_provider_call_count"
            ],
            "participant_operation_denominator_impact": report[
                "participant_operation_denominator_impact"
            ],
            "participant_feedback_emitted": report[
                "participant_feedback_emitted"
            ],
            "validation_errors": validation_errors,
            "failures": failures,
        }
        task_rows.append(row)
        print(
            json.dumps(
                {
                    "event": "task_completed",
                    "task_index": task_index,
                    "task_count": len(design["tasks"]),
                    **row,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    expected_queries = 20
    expected_metrics = 68
    completed_queries = sum(row["completed_query_count"] for row in task_rows)
    failed_queries = sum(row["failed_query_count"] for row in task_rows)
    completed_metrics = sum(
        row["completed_query_metric_count"] for row in task_rows
    )
    exact_replays = sum(row["exact_replay_count"] for row in task_rows)
    passed = (
        len(task_rows) == 5
        and sum(row["query_count"] for row in task_rows) == expected_queries
        and completed_queries == expected_queries
        and failed_queries == 0
        and sum(row["query_metric_count"] for row in task_rows) == expected_metrics
        and completed_metrics == expected_metrics
        and exact_replays == expected_queries
        and all(not row["validation_errors"] for row in task_rows)
        and all(row["evaluator_provider_call_count"] == 0 for row in task_rows)
        and all(
            row["participant_operation_denominator_impact"] == 0
            for row in task_rows
        )
        and all(row["participant_feedback_emitted"] is False for row in task_rows)
    )
    summary: dict[str, Any] = {
        "schema_version": (
            "chemworld-work-ii-held-out-evaluator-development-shakedown-0.1"
        ),
        "formal_result": False,
        "development_world_seed": 0,
        "formal_participant_denominator": False,
        "status": "passed" if passed else "failed",
        "expected_task_count": 5,
        "observed_task_count": len(task_rows),
        "expected_query_count": expected_queries,
        "completed_query_count": completed_queries,
        "failed_query_count": failed_queries,
        "expected_query_metric_count": expected_metrics,
        "completed_query_metric_count": completed_metrics,
        "exact_replay_count": exact_replays,
        "operation_attempt_count": sum(
            row["operation_attempt_count"] for row in task_rows
        ),
        "evaluator_provider_call_count": sum(
            row["evaluator_provider_call_count"] for row in task_rows
        ),
        "participant_operation_denominator_impact": sum(
            row["participant_operation_denominator_impact"] for row in task_rows
        ),
        "participant_feedback_emitted": any(
            row["participant_feedback_emitted"] for row in task_rows
        ),
        "tasks": task_rows,
        "all_failures": [failure for row in task_rows for failure in row["failures"]],
    }
    summary["report_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.report.resolve(), summary)
    return summary


def main() -> int:
    args = _parse_args()
    report = run(args)
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
