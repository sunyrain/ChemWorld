#!/usr/bin/env python3
"""Run the zero-provider Work II blind-evaluator development shakedown."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    execute_blind_evaluation_plan,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT
    / "runs/development/work-ii-deepseek-qualification-v2-seed0-opaque/summary.json"
)
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot_deepseek_v4_flash.json"
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT / "runs/development/work-ii-blind-evaluator-shakedown-v0.2"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-blind-evaluator-development-shakedown-v0.2.json"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _synthetic_fixture(source: Mapping[str, Any]) -> dict[str, Any]:
    summary = deepcopy(dict(source))
    analysis = summary.get("analysis")
    if not isinstance(analysis, dict):
        raise ValueError("development source summary lacks analysis")
    experiments = analysis.get("experiments")
    if not isinstance(experiments, list) or len(experiments) != 4:
        raise ValueError("development source does not contain four experiments")
    scored = [
        (int(row["experiment_index"]), float(row["leaderboard_score"]))
        for row in experiments
        if isinstance(row, Mapping)
        and isinstance(row.get("experiment_index"), int)
        and not isinstance(row.get("experiment_index"), bool)
        and isinstance(row.get("leaderboard_score"), int | float)
        and not isinstance(row.get("leaderboard_score"), bool)
    ]
    if len(scored) != 4:
        raise ValueError("development source experiments are not all scored")
    incumbent = min(scored, key=lambda item: (-item[1], item[0]))[0]
    recommendation = {
        "selected_experiment_index": incumbent,
        "selection_rationale": (
            "development-only synthetic incumbent fixture; not a participant recommendation"
        ),
    }
    analysis["final_recommendation"] = recommendation
    analysis["final_recommendation_sha256"] = canonical_json_sha256(recommendation)
    analysis["observed_incumbent_experiment_index"] = incumbent
    summary["analysis"] = analysis
    summary["completed"] = True
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    source = _load(args.source.resolve())
    config = _load(args.config.resolve())
    design = _load(args.design.resolve())
    fixture = _synthetic_fixture(source)
    source_digest = file_sha256(args.source.resolve())
    cell = {
        "cell_id": "work-ii-development-blind-evaluator-shakedown-seed0-opaque",
        "cell_key_sha256": canonical_json_sha256(
            {
                "source_summary_sha256": source_digest,
                "purpose": "development_blind_evaluator_shakedown",
            }
        ),
        "task_id": config["task_id"],
        "world_seed": 0,
    }
    plan = build_blind_evaluation_plan(
        cell,
        fixture,
        design["blind_evaluator_contract"],
    )
    blind_report = execute_blind_evaluation_plan(
        plan,
        config,
        args.output.resolve(),
    )
    failures: list[dict[str, Any]] = []
    for receipt_path in sorted((args.output.resolve() / "executions").glob("*/receipt.json")):
        receipt = _load(receipt_path)
        if receipt.get("status") != "completed":
            failures.append(
                {
                    "execution_id": receipt.get("execution_id"),
                    "failure_type": receipt.get("failure_type"),
                }
            )
        elif receipt.get("exact_replay", {}).get("verified") is not True:
            failures.append(
                {
                    "execution_id": receipt.get("execution_id"),
                    "failure_type": "exact_replay_failed",
                }
            )
    passed = (
        blind_report["completed_execution_count"] == 6
        and blind_report["failed_execution_count"] == 0
        and blind_report["evaluator_provider_call_count"] == 0
        and blind_report["participant_operation_denominator_impact"] == 0
        and blind_report["participant_feedback_emitted"] is False
        and not failures
    )
    report: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-blind-evaluator-shakedown-0.1",
        "status": "passed" if passed else "failed",
        "formal_result": False,
        "participant_recommendation_used": False,
        "synthetic_recommendation_policy": "copy_observed_incumbent_for_apparatus_only",
        "participant_provider_calls": 0,
        "evaluator_provider_calls": blind_report["evaluator_provider_call_count"],
        "source_summary": {
            "path": args.source.resolve().relative_to(ROOT).as_posix(),
            "sha256": source_digest,
        },
        "denominators": {
            "cells": 1,
            "targets": 2,
            "paired_replicates_per_target": 3,
            "scheduled_executions": 6,
            "completed_executions": blind_report["completed_execution_count"],
            "failed_executions": blind_report["failed_execution_count"],
        },
        "isolation": {
            "participant_operation_denominator_impact": blind_report[
                "participant_operation_denominator_impact"
            ],
            "participant_feedback_emitted": blind_report[
                "participant_feedback_emitted"
            ],
        },
        "plan_sha256": plan["plan_sha256"],
        "blind_report_sha256": blind_report["report_sha256"],
        "failures": failures,
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(args.report.resolve(), report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    report = run(args)
    print(
        json.dumps(
            {
                "status": report["status"],
                **report["denominators"],
                "evaluator_provider_calls": report["evaluator_provider_calls"],
                "failure_count": len(report["failures"]),
                "report": str(args.report),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
