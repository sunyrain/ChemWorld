"""Run the staged five-task Work II prior-contract pilot."""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Mapping
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)

try:
    from scripts.qualify_static_s0_five_tasks import _participant_protocol
    from scripts.run_static_optimization_s0 import run_s0
except ModuleNotFoundError:
    from qualify_static_s0_five_tasks import _participant_protocol
    from run_static_optimization_s0 import run_s0

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_prior_pilot.json"
DEFAULT_OUTPUT = ROOT / "runs/development/work-ii-prior-pilot"


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return payload


def _repo_path(value: object) -> Path:
    path = (ROOT / str(value)).resolve()
    path.relative_to(ROOT)
    return path


def _stage_values(plan: Mapping[str, Any], stage_id: str) -> dict[str, Any]:
    stages = plan.get("stages")
    if not isinstance(stages, Mapping) or stage_id not in stages:
        raise ValueError(f"unknown Work II pilot stage: {stage_id}")
    stage = stages[stage_id]
    if not isinstance(stage, Mapping):
        raise ValueError(f"pilot stage {stage_id} must be an object")
    return copy.deepcopy(dict(stage))


def _selected_values(value: object, available: list[str], *, label: str) -> list[str]:
    if value == "all":
        return list(available)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be 'all' or a string list")
    selected = [str(item) for item in value]
    unknown = sorted(set(selected) - set(available))
    if unknown or len(selected) != len(set(selected)):
        raise ValueError(f"{label} contains unknown or duplicate values: {unknown}")
    return selected


def _material_information(
    plan: Mapping[str, Any],
    *,
    task_id: str,
    arm_id: str,
) -> dict[str, Any]:
    arm = copy.deepcopy(dict(plan["prior_arms"][arm_id]))
    if arm_id == "misindexed_nominal":
        arm.update(copy.deepcopy(dict(plan["tasks"][task_id]["misindexing"])))
    return arm


def build_pilot_protocol(
    plan: Mapping[str, Any],
    *,
    stage_id: str,
    task_id: str,
    arm_id: str,
    world_seed: int,
) -> dict[str, Any]:
    """Build one non-formal pilot cell without reading a realized world."""

    stage = _stage_values(plan, stage_id)
    protocol = _participant_protocol(plan, task_id)
    horizon = int(stage["exploration_experiments"])
    protocol["schema_version"] = "chemworld-work-ii-prior-pilot-protocol-0.1"
    protocol["protocol_id"] = (
        f"{plan['pilot_id']}--{stage_id}--{task_id}--{arm_id}--seed{world_seed}"
    )
    protocol["freeze_id"] = protocol["protocol_id"]
    protocol["status"] = "development_pilot_only"
    protocol["formal_result"] = False
    protocol["benchmark_claim_allowed"] = False
    protocol["world_policy"]["world_seed"] = int(world_seed)
    protocol["horizon"] = horizon
    protocol["scientific_campaign_budget"] = {
        "exploration_experiments": horizon,
        "horizon_visible": True,
        "final_synthesis_after_exploration": False,
    }
    protocol["material_information"] = _material_information(
        plan,
        task_id=task_id,
        arm_id=arm_id,
    )
    protocol["reward_contract"]["final_selection"] = (
        "best_observed_completed_experiment"
    )
    protocol["final_synthesis"] = {
        "enabled": False,
        "calls": 0,
        "mode": "not_run_in_prior_contract_pilot",
        "executes_experiment": False,
        "validation_feedback_returned_to_agent": False,
    }
    protocol["world_understanding"] = {
        "enabled": False,
        "declared_scoring_enabled": False,
        "predictive_score_enabled": False,
        "reason": "pilot qualifies prior delivery and provider execution only",
    }
    protocol["validation_budget"] = {
        "incumbent_replicates": 0,
        "recommendation_replicates": 0,
        "independent_observation_seeds": True,
        "paired_observation_seeds_across_targets": True,
        "feedback_returned_to_agent": False,
    }
    protocol["observation_noise_namespace"] = (
        f"{plan['observation_noise_namespace_base']}--{stage_id}--{task_id}--"
        f"{arm_id}--seed{world_seed}"
    )
    validate_static_optimization_protocol(protocol)
    return protocol


def _progress(
    path: Path | None,
    *,
    event: str,
    **payload: Any,
) -> None:
    if path is None:
        return
    record = {
        "schema_version": "chemworld-work-ii-prior-pilot-progress-0.1",
        "event": event,
        **payload,
    }
    write_json_atomic(path, record)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True), flush=True)


def run_pilot(args: argparse.Namespace) -> dict[str, Any]:
    plan = _load_object(args.plan)
    stage = _stage_values(plan, args.stage)
    provider = str(stage["provider"])
    if provider not in {"mock", "wellau"}:
        raise ValueError("Work II prior pilot supports only mock or WellAU")
    if provider == "wellau" and not args.allow_external_provider:
        raise RuntimeError("real WellAU pilot requires --allow-external-provider")
    if provider == "wellau" and git_worktree_dirty(ROOT):
        raise RuntimeError("real WellAU pilot requires a clean committed worktree")

    task_ids = _selected_values(
        stage["task_ids"],
        [str(item) for item in plan["task_ids"]],
        label="stage.task_ids",
    )
    arm_ids = _selected_values(
        stage["prior_arms"],
        [str(item) for item in plan["prior_arms"]],
        label="stage.prior_arms",
    )
    world_seeds = [int(item) for item in stage["world_seeds"]]
    cells = [
        (task_id, arm_id, world_seed)
        for world_seed in world_seeds
        for task_id in task_ids
        for arm_id in arm_ids
    ]
    if len(cells) != int(stage["expected_cells"]):
        raise ValueError("pilot stage denominator differs from expected_cells")

    methods_path = _repo_path(plan["participant"]["method_config_path"])
    methods = _load_object(methods_path)
    method_id = str(plan["participant"]["method_id"])
    if list(methods["methods"]) != [method_id]:
        raise ValueError("Work II pilot method binding is ambiguous")
    method_sha256 = canonical_json_sha256(methods)
    output = args.output.resolve()
    progress_file = args.progress_file.resolve() if args.progress_file is not None else None
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for cell_index, (task_id, arm_id, world_seed) in enumerate(cells, start=1):
        _progress(
            progress_file,
            event="pilot_cell_started",
            stage=args.stage,
            completed_cells=cell_index - 1,
            total_cells=len(cells),
            current_cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            world_seed=world_seed,
            provider=provider,
        )
        protocol = build_pilot_protocol(
            plan,
            stage_id=args.stage,
            task_id=task_id,
            arm_id=arm_id,
            world_seed=world_seed,
        )
        cell_id = f"{cell_index:02d}--{task_id}--{arm_id}--seed{world_seed}"
        cell_root = output / "cells" / cell_id
        protocol_path = output / "protocols" / f"{cell_id}.json"
        write_json_atomic(protocol_path, protocol)
        report = run_s0(
            SimpleNamespace(
                protocol=protocol_path,
                llm_methods=methods_path,
                output=cell_root,
                provider=provider,
                allow_external_provider=provider == "wellau",
                confirm_protocol_sha256=canonical_json_sha256(protocol),
                confirm_method_sha256=method_sha256,
                world_seed=None,
                task=[task_id],
                method_id=[method_id],
                progress_file=progress_file,
            )
        )
        report_path = cell_root / "report.json"
        completed = (
            report["completed_cell_count"] == 1
            and report["method_failure_cell_count"] == 0
            and report["completed_experiment_count"]
            == int(stage["exploration_experiments"])
        )
        row = {
            "cell_index": cell_index,
            "task_id": task_id,
            "prior_arm": arm_id,
            "material_information_mode": protocol["material_information"]["mode"],
            "world_seed": world_seed,
            "completed": completed,
            "protocol_path": str(protocol_path.relative_to(output)),
            "protocol_sha256": canonical_json_sha256(protocol),
            "report_path": str(report_path.relative_to(output)),
            "report_sha256": canonical_json_sha256(report),
            "provider_calls": int(report["provider_call_count"]),
            "provider_attempts": int(report["provider_attempt_count"]),
            "provider_reported_total_tokens": int(
                report["provider_reported_total_tokens"]
            ),
            "failure_count": int(report["method_failure_cell_count"]),
        }
        results.append(row)
        if not completed:
            cell_failures = [
                item["failure"]
                for item in report["cells"]
                if item.get("failure") is not None
            ]
            failures.append({**row, "failures": cell_failures})
        _progress(
            progress_file,
            event="pilot_cell_completed" if completed else "pilot_cell_failed",
            stage=args.stage,
            completed_cells=sum(item["completed"] for item in results),
            failed_cells=len(failures),
            total_cells=len(cells),
            current_cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            world_seed=world_seed,
            provider=provider,
        )
        if failures:
            break

    summary = {
        "schema_version": "chemworld-work-ii-prior-pilot-index-0.1",
        "pilot_id": plan["pilot_id"],
        "stage": args.stage,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "scientific_result": False,
        "source_commit": git_source_commit(ROOT),
        "source_tree_dirty": git_worktree_dirty(ROOT),
        "provider": provider,
        "wire_api": "responses" if provider == "wellau" else "mock",
        "model_id": plan["participant"]["model_id"],
        "reasoning_effort": plan["participant"]["reasoning_effort"],
        "expected_cell_count": len(cells),
        "attempted_cell_count": len(results),
        "completed_cell_count": sum(item["completed"] for item in results),
        "failed_cell_count": len(failures),
        "all_requested_cells_completed": len(results) == len(cells) and not failures,
        "provider_call_count": sum(item["provider_calls"] for item in results),
        "provider_attempt_count": sum(item["provider_attempts"] for item in results),
        "provider_reported_total_tokens": sum(
            item["provider_reported_total_tokens"] for item in results
        ),
        "results": results,
        "failures": failures,
    }
    write_json_atomic(output / "pilot_execution_index.json", summary)
    _progress(
        progress_file,
        event="pilot_completed" if summary["all_requested_cells_completed"] else "pilot_failed",
        stage=args.stage,
        completed_cells=summary["completed_cell_count"],
        failed_cells=summary["failed_cell_count"],
        total_cells=summary["expected_cell_count"],
        provider=provider,
        output=str(output),
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--stage", choices=("contract-preflight", "real-probe"), required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--allow-external-provider", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    parsed = parse_args()
    result = run_pilot(parsed)
    print(
        json.dumps(
            {
                "output": str(parsed.output),
                "stage": result["stage"],
                "completed_cells": result["completed_cell_count"],
                "failed_cells": result["failed_cell_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result["all_requested_cells_completed"] else 1)
