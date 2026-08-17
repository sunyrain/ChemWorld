#!/usr/bin/env python3
"""Run three task-specific one-world/three-arm open-action development pilots.

This launcher deliberately keeps the participant workflow open while materializing a complete,
task-specific public ActionPlan packet.  It is development evidence only.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any

from run_work_ii_campaign_pilot import _checkpoint_contract
from work_ii_longitudinal_runtime import Progress, _execute_cells

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import (
    _world_campaign_config,
    summarize_results,
)
from chemworld.eval.work_ii_open_action_decision import ARMS
from chemworld.eval.work_ii_truth import (
    WORK_II_TRUTH_PLAN_VERSION,
    _noise_binding,
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = ROOT / "workstreams/flagship_tasks/reports/work-ii-w2-26-deepseek-runtime-configs-v0.1"
WORLD_SEED = 0
PACKET_SEED = 240817
RESOURCE_PROFILE = "pilot"
STUDY_ID = "work-ii-multi-task-open-action-pilot-v0.1"
FORMAL_RESULT = False
FORMAL_PREFLIGHT_SHA256: str | None = None
TESTED_COMMIT: str | None = None
TASKS: dict[str, str] = {
    "electrochemical-conversion": "a_p--electrochemical-conversion--r10.json",
    "reaction-to-crystallization": "a_s--reaction-to-crystallization--r12.json",
    "reaction-safety-constrained": "a_p--reaction-safety-constrained--r10.json",
}
DEFAULT_OUTPUT = ROOT / "runs/development/work-ii-multi-task-open-action-pilot-v0.1"


def _apply_resource_profile(task_id: str, stock_limits: Mapping[str, Any]) -> dict[str, Any]:
    """Apply a pre-declared stock-cushion contract without changing coverage."""
    result = deepcopy(dict(stock_limits))
    if RESOURCE_PROFILE not in {"resource_recovery_v1", "resource_recovery_v2"}:
        return result
    cushions = {
        "electrochemical-conversion": {"solvent_L": 0.100},
        "reaction-to-crystallization": {"catalyst_mol": 0.003},
    }.get(task_id, {})
    if RESOURCE_PROFILE == "resource_recovery_v2" and task_id == "reaction-to-crystallization":
        cushions["seed_g"] = 0.040
    for key, cushion in cushions.items():
        if key in result:
            result[key] = float(result[key]) + float(cushion)
    return result


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _scale_number(value: Any, factor: float) -> Any:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return value
    scaled = float(value) * factor
    return int(math.ceil(scaled)) if isinstance(value, int) else scaled


def _scale_nested_numbers(value: Any, factor: float) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _scale_nested_numbers(item, factor) for key, item in value.items()}
    if isinstance(value, list):
        return [_scale_nested_numbers(item, factor) for item in value]
    return _scale_number(value, factor)


def _task_metrics(runtime: Mapping[str, Any]) -> list[str]:
    checkpoint = runtime.get("belief_checkpoint", {})
    checkpoint = checkpoint if isinstance(checkpoint, Mapping) else {}
    metrics = checkpoint.get("allowed_metric_ids")
    if not isinstance(metrics, list) or not metrics:
        analysis = runtime.get("analysis", {})
        analysis = analysis if isinstance(analysis, Mapping) else {}
        metrics = analysis.get("final_metric_ids")
    if not isinstance(metrics, list) or not metrics:
        raise ValueError(f"{runtime.get('task_id')}: no task metric IDs")
    result = [str(item) for item in metrics]
    if "score" not in result:
        result.append("score")
    return result


def _prepare_runtime(source: Mapping[str, Any], *, task_id: str, checkpoint_queries: list[dict[str, Any]]) -> dict[str, Any]:
    runtime = deepcopy(dict(source))
    runtime["task_id"] = task_id
    runtime["world_seed"] = WORLD_SEED
    runtime["formal_result"] = FORMAL_RESULT
    runtime["pilot_id"] = f"work-ii-multi-task-open-action--{task_id}--seed{WORLD_SEED}"
    runtime["observation_noise_namespace"] = f"work-ii-multi-task-open-action--{task_id}"
    runtime["snapshot_stages"] = [
        "pre_evidence",
        "after_experiment_3",
        "after_experiment_6",
        "after_experiment_9",
        "final",
    ]
    factor = 1.2 if int(runtime.get("campaign", {}).get("complete_experiments", 12)) != 12 else 1.0
    campaign = deepcopy(dict(runtime.get("campaign", {})))
    for field in (
        "operation_attempt_limit",
        "nonfinal_instrument_use_limit",
        "process_time_limit_s",
        "vessel_start_limit",
        "final_assay_limit",
    ):
        if field in campaign:
            campaign[field] = _scale_number(campaign[field], factor)
    campaign["complete_experiments"] = 12
    campaign["vessel_start_limit"] = 12
    campaign["final_assay_limit"] = 12
    campaign["checkpoint_complete_experiments"] = [0, 3, 6, 9, 12]
    closeout = deepcopy(dict(campaign.get("closeout_policy", {})))
    source_batches = max(1, int(source.get("campaign", {}).get("complete_experiments", 12)))
    closeout["planned_batches"] = 12
    for per_batch, total in (
        ("discard_path_operations_per_batch", "discard_path_total_operation_reserve"),
        ("final_assay_path_operations_per_batch", "final_assay_path_total_operation_reserve"),
    ):
        if per_batch in closeout:
            closeout[total] = int(closeout[per_batch]) * 12
    campaign["closeout_policy"] = closeout
    campaign["stock_limits"] = _apply_resource_profile(
        task_id,
        _scale_nested_numbers(campaign.get("stock_limits", {}), factor),
    )
    if RESOURCE_PROFILE == "resource_recovery_v2" and task_id in {
        "electrochemical-conversion",
        "reaction-to-crystallization",
    }:
        # v1 retained a second, independent failure class: the agent's long-duration
        # operation could not leave the protected closeout reserve.  Add a fixed cushion
        # without changing operation count, candidate coverage, or qualification rules.
        campaign["process_time_limit_s"] = float(campaign["process_time_limit_s"]) + 30_000.0
    campaign["operation_repeat_limits"] = _scale_nested_numbers(campaign.get("operation_repeat_limits", {}), factor)
    campaign["process_time_policy"] = _scale_nested_numbers(campaign.get("process_time_policy", {}), factor)
    campaign["card_id"] = f"work-ii-multi-task-open-action-{task_id}-k12"
    runtime["campaign"] = campaign

    method = deepcopy(dict(runtime.get("method_resources", {})))
    method["complete_experiment_limit"] = 12
    method["checkpoint_complete_experiments"] = [3, 6, 9, 12]
    for field in ("operation_limit", "input_token_limit", "uncached_input_token_limit", "output_token_limit", "wall_time_limit_s"):
        if field in method:
            method[field] = _scale_number(method[field], factor)
    runtime["method_resources"] = method

    metrics = _task_metrics(runtime)
    checkpoint = deepcopy(dict(runtime.get("belief_checkpoint", {})))
    checkpoint["allowed_metric_ids"] = metrics
    checkpoint["held_out_queries"] = [
        {**dict(query), "metric_ids": list(metrics)} for query in checkpoint_queries
    ]
    runtime["belief_checkpoint"] = checkpoint
    analysis = deepcopy(dict(runtime.get("analysis", {})))
    analysis["final_metric_ids"] = metrics
    runtime["analysis"] = analysis
    runtime["resource_profile"] = RESOURCE_PROFILE
    runtime["execution_context"] = {
        "execution_mode": "formal" if FORMAL_RESULT else "development",
        "evidence_status": (
            "formal_fresh_multi_world_matrix" if FORMAL_RESULT else "development_only"
        ),
        "release_eligible": FORMAL_RESULT,
        "tested_commit": TESTED_COMMIT,
        "freeze_id": FORMAL_PREFLIGHT_SHA256,
    }
    return runtime


def _select_split_queries(source: Mapping[str, Any], task_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checkpoint = source.get("belief_checkpoint", {})
    checkpoint = checkpoint if isinstance(checkpoint, Mapping) else {}
    raw = checkpoint.get("held_out_queries")
    if not isinstance(raw, list) or len(raw) < 16:
        raise ValueError(f"{task_id}: expected at least 16 registered held-out queries")
    ordered = sorted(
        (deepcopy(dict(item)) for item in raw if isinstance(item, Mapping)),
        key=lambda item: (sha256(f"{PACKET_SEED}:{task_id}:{item['query_id']}".encode()).hexdigest(), str(item["query_id"])),
    )
    candidates = ordered[:8]
    checkpoints = ordered[8:16]
    if len({str(item["query_id"]) for item in candidates + checkpoints}) != 16:
        raise ValueError(f"{task_id}: split query IDs are not unique")
    return candidates, checkpoints


def _workflow_family(task_id: str, actions: Sequence[Mapping[str, Any]]) -> str:
    operations = tuple(str(item.get("operation")) for item in actions)
    if task_id == "electrochemical-conversion":
        return "electrochemical_probe_then_controlled_conversion"
    if task_id == "reaction-to-crystallization":
        return "reaction_then_seeded_crystallization"
    if "quench" in operations:
        return "reaction_heat_then_safety_quench"
    return "reaction_safety_constrained"


def _public_candidate(task_id: str, query: Mapping[str, Any], compiled: Mapping[str, Any], metrics: list[str]) -> dict[str, Any]:
    actions = [deepcopy(dict(item)) for item in compiled["action_plan"]]
    if not actions or actions[-1].get("operation") != "measure" or actions[-1].get("instrument") != "final_assay":
        raise ValueError(f"{task_id}/{query['query_id']}: missing final assay")
    pair_id = str(query.get("pair_id", query["query_id"]))
    row = {
        "query_id": str(query["query_id"]),
        "pair_id": pair_id,
        "initial_state_contract": "fresh_task_batch",
        "ordered_operations": [str(item.get("operation")) for item in actions],
        "all_operation_parameters": actions,
        "action_plan": actions,
        "action_plan_sha256": str(compiled["action_plan_sha256"]),
        "measurement_positions": [index + 1 for index, item in enumerate(actions) if item.get("operation") == "measure"],
        "terminal_assay": {"operation": "measure", "instrument": "final_assay"},
        "workflow_family": _workflow_family(task_id, actions),
        "omitted_optional_operations": [],
        "objective": str(query.get("objective", "maximize task score subject to task constraints")),
        "metric_ids": metrics,
    }
    if canonical_json_sha256(actions) != row["action_plan_sha256"]:
        raise ValueError(f"{task_id}/{query['query_id']}: action-plan hash mismatch")
    return row


def _candidate_packet(runtime: Mapping[str, Any], task_id: str, candidates: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    metrics = _task_metrics(runtime)
    public: list[dict[str, Any]] = []
    compiled: dict[str, dict[str, Any]] = {}
    for raw in candidates:
        query = deepcopy(dict(raw))
        query["metric_ids"] = list(metrics)
        plan = compile_evaluator_truth_query(runtime, query)
        row = _public_candidate(task_id, query, plan, metrics)
        public.append(row)
        compiled[str(query["query_id"])] = plan
    if len(public) != 8 or len({row["query_id"] for row in public}) != 8:
        raise ValueError(f"{task_id}: candidate packet denominator is not eight")
    return public, compiled


def _candidate_truth_plan(runtime: Mapping[str, Any], *, cluster_id: str, candidates: Sequence[Mapping[str, Any]], compiled: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    queries: list[dict[str, Any]] = []
    for index, public in enumerate(candidates, start=1):
        query_id = str(public["query_id"])
        item = deepcopy(dict(compiled[query_id]))
        item.update({
            "execution_index": index,
            "execution_id": f"{cluster_id}--candidate-truth-{index:02d}",
            **_noise_binding(
                formal_preflight_sha256=FORMAL_PREFLIGHT_SHA256,
                world_cluster_id=cluster_id,
                query_id=query_id,
            ),
        })
        if item["action_plan"] != public["action_plan"]:
            raise ValueError(f"{cluster_id}/{query_id}: public/truth action plan differs")
        queries.append(item)
    checkpoint = _checkpoint_contract(runtime, "opaque")
    metrics = [str(item) for item in checkpoint["allowed_metric_ids"]]
    plan: dict[str, Any] = {
        "schema_version": WORK_II_TRUTH_PLAN_VERSION,
        "formal_result": FORMAL_RESULT,
        "formal_preflight_sha256": FORMAL_PREFLIGHT_SHA256,
        "world_cluster_id": cluster_id,
        "task_id": str(runtime["task_id"]),
        "world_seed": WORLD_SEED,
        "campaign_config_sha256": canonical_json_sha256(runtime),
        "truth_query_count": len(queries),
        "truth_query_metric_count": sum(len(item["metric_ids"]) for item in queries),
        "evaluator_provider_call_count": 0,
        "participant_operation_denominator_impact": 0,
        "participant_feedback_allowed": False,
        "shared_across_prior_arms": True,
        "law_summary_contract": {
            "allowed_feature_ids": list(checkpoint["allowed_feature_ids"]),
            "allowed_metric_ids": metrics,
            "required_metric_ids": metrics,
            "evidence_catalog": [f"experiment-{index}-final-assay" for index in range(1, len(queries) + 1)],
        },
        "queries": queries,
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _build_terminal_contract(task_id: str, study_id: str, public: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    metrics = list(public[0]["metric_ids"])
    contract: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-terminal-action-readout-contract-0.1",
        "protocol_version": "chemworld-work-ii-multi-task-open-action-pilot-0.1",
        "readout_id": f"{study_id}--{task_id}--seed{WORLD_SEED}",
        "task_id": task_id,
        "selection_mode": "rank_all_select_one",
        "prediction_mode": "ranking_only",
        "reveal_gate": "campaign_terminal_and_all_belief_checkpoints_committed",
        "metric_ids": metrics,
        "candidate_queries": [deepcopy(dict(row)) for row in public],
        "candidate_outcomes_included": False,
        "hidden_ranks_included": False,
        "additional_evidence_included": False,
        "public_plan_contract": "complete_action_plan_outcome_blind_v0.1",
        "no_implicit_defaults": True,
        "public_plan_hash_equals_truth_plan_hash": True,
        "truth_plan_hash_equals_executed_plan_hash": True,
    }
    contract["contract_sha256"] = canonical_json_sha256(contract)
    return contract


def _prepare_task(task_id: str, source_path: Path, output_root: Path, progress: Progress) -> dict[str, Any]:
    source = _load(source_path)
    candidate_raw, checkpoint_raw = _select_split_queries(source, task_id)
    runtime = _prepare_runtime(source, task_id=task_id, checkpoint_queries=checkpoint_raw)
    metrics = _task_metrics(runtime)
    public, compiled = _candidate_packet(runtime, task_id, candidate_raw)
    cluster_id = f"A_S_MULTI_TASK_OAD--{task_id}--seed{WORLD_SEED}"
    contract = _build_terminal_contract(task_id, STUDY_ID, public)
    config = _world_campaign_config(runtime, study_id=STUDY_ID, world_seed=WORLD_SEED, terminal_contract=contract)
    config["formal_result"] = FORMAL_RESULT
    config["pilot_id"] = f"{STUDY_ID}--{task_id}--seed{WORLD_SEED}"
    config["resource_profile"] = RESOURCE_PROFILE
    task_root = output_root / task_id
    config_path = task_root / "campaign-config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(config_path, config)

    checkpoint_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": task_id,
            "world_seed": WORLD_SEED,
        },
        config,
        formal_result=FORMAL_RESULT,
        formal_preflight_sha256=FORMAL_PREFLIGHT_SHA256,
    )
    errors = validate_evaluator_truth_plan(checkpoint_plan)
    if errors:
        raise ValueError(f"{task_id}: checkpoint truth plan invalid: {'; '.join(errors)}")
    checkpoint_root = output_root / task_id / "checkpoint-truth"
    checkpoint_report = execute_evaluator_truth_plan(checkpoint_plan, config, checkpoint_root)
    report_errors = validate_evaluator_truth_report(checkpoint_report, checkpoint_plan)
    if report_errors or checkpoint_report.get("status") != "completed":
        raise ValueError(f"{task_id}: checkpoint truth failed: {'; '.join(report_errors) or checkpoint_report.get('status')}")

    candidate_plan = _candidate_truth_plan(runtime=config, cluster_id=cluster_id, candidates=public, compiled=compiled)
    errors = validate_evaluator_truth_plan(candidate_plan)
    if errors:
        raise ValueError(f"{task_id}: candidate truth plan invalid: {'; '.join(errors)}")
    candidate_root = output_root / task_id / "candidate-truth"
    candidate_report = execute_evaluator_truth_plan(candidate_plan, config, candidate_root)
    report_errors = validate_evaluator_truth_report(candidate_report, candidate_plan)
    if report_errors or candidate_report.get("status") != "completed":
        raise ValueError(f"{task_id}: candidate truth failed: {'; '.join(report_errors) or candidate_report.get('status')}")

    candidate_truth = deepcopy(dict(candidate_report["truth"]))
    ranks = {query_id: rank for rank, query_id in enumerate(sorted(candidate_truth, key=lambda item: (-candidate_truth[item]["score"], item)), start=1)}
    plan_hashes = {str(row["query_id"]): str(row["action_plan_sha256"]) for row in public}
    cells = [
        {
            "cell_id": f"{cluster_id}--{arm}",
            "cluster_id": cluster_id,
            "task_id": task_id,
            "world_seed": WORLD_SEED,
            "arm": arm,
            "campaign_config_path": config_path.relative_to(task_root).as_posix(),
            "terminal_action_readout": deepcopy(contract),
            "candidate_truth": candidate_truth,
            "presented_candidate_ranks": ranks,
            "candidate_pool_ranks": ranks,
            "candidate_action_plan_sha256": plan_hashes,
            "checkpoint_truth_plan": checkpoint_plan,
            "checkpoint_truth": deepcopy(dict(checkpoint_report["truth"])),
        }
        for arm in ARMS
    ]
    write_json_atomic(output_root / task_id / "public_candidate_packet.json", {
        "schema_version": "chemworld-work-ii-multi-task-open-action-public-packet-0.1",
        "task_id": task_id,
        "world_seed": WORLD_SEED,
        "candidate_packet_seed": PACKET_SEED,
        "candidate_outcomes_included": False,
        "candidates": public,
    })
    manifest = {
        "schema_version": "chemworld-work-ii-multi-task-open-action-pilot-manifest-0.1",
        "task_id": task_id,
        "world_seed": WORLD_SEED,
        "candidate_packet_seed": PACKET_SEED,
        "source_runtime": source_path.relative_to(ROOT).as_posix(),
        "candidate_count": 8,
        "checkpoint_query_count": len(checkpoint_plan["queries"]),
        "campaign_experiment_count_per_cell": 12,
        "arm_count": 3,
        "participant_experiment_count": 36,
        "formal_denominator": FORMAL_RESULT,
        "resource_profile": RESOURCE_PROFILE,
        "provider_execution_authorized": True,
        "metrics": metrics,
        "candidate_truth_plan_sha256": candidate_plan["plan_sha256"],
        "candidate_truth_report_sha256": candidate_report["report_sha256"],
        "checkpoint_truth_plan_sha256": checkpoint_plan["plan_sha256"],
        "checkpoint_truth_report_sha256": checkpoint_report["report_sha256"],
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / task_id / "input_manifest.json", manifest)
    progress.emit({"stage": "provider_free_task_complete", "task_id": task_id, "completed_tasks": 0, "total_tasks": 3, "checkpoint_truth_queries": len(checkpoint_plan["queries"]), "candidate_truth_queries": len(candidate_plan["queries"]), "public_truth_binding": "passed"})
    return manifest


def _write_report(task_id: str, summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        f"# Work II {task_id}：单世界三臂 open-action development pilot",
        "",
        "本报告仅用于开发阶段接口、任务契约和科学流程诊断，不进入正式分母。",
        "",
        f"完成资格 cell：{summary.get('eligible_cell_count')}/{summary.get('scheduled_cell_count')}",
        "",
        "| arm | status | 完成实验数 | 选中真实排名 | Top-1 | raw regret | normalized regret | law MAE |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(summary.get("cell_rows", []), key=lambda item: str(item.get("arm"))):
        lines.append(f"| {row.get('arm')} | {row.get('status')} | {row.get('campaign_complete_experiment_count')} | {row.get('selected_rank')} | {int(row.get('top1_selected') is True)} | {row.get('raw_regret')} | {row.get('normalized_regret')} | {row.get('law_normalized_mae')} |")
    lines.extend(["", "- terminal mode: ranking-only; complete ActionPlan public, outcomes/ranks hidden", "- provider-free truth/replay and public-plan binding: passed"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    global RESOURCE_PROFILE, STUDY_ID, WORLD_SEED
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--world-seed", type=int, default=WORLD_SEED)
    parser.add_argument(
        "--resource-profile",
        choices=("pilot", "resource_recovery_v1", "resource_recovery_v2"),
        default="pilot",
        help="Use the original pilot contract or the pre-declared stock-cushion recovery contract.",
    )
    parser.add_argument("--task", action="append", choices=tuple(TASKS), help="run only the selected task(s)")
    args = parser.parse_args()
    if not args.prepare and not args.execute:
        parser.error("select --prepare or --execute")
    WORLD_SEED = int(args.world_seed)
    RESOURCE_PROFILE = str(args.resource_profile)
    STUDY_ID = (
        "work-ii-multi-task-open-action-recovery-v0.3"
        if RESOURCE_PROFILE == "resource_recovery_v2"
        else "work-ii-multi-task-open-action-recovery-v0.2"
        if RESOURCE_PROFILE == "resource_recovery_v1"
        else "work-ii-multi-task-open-action-pilot-v0.1"
    )
    output = (args.output_root if args.output_root.is_absolute() else ROOT / args.output_root).resolve()
    output.mkdir(parents=True, exist_ok=True)
    progress = Progress(output / "progress.jsonl")
    selected_tasks = args.task or list(TASKS)
    manifests: list[dict[str, Any]] = []
    for index, task_id in enumerate(selected_tasks, start=1):
        filename = TASKS[task_id]
        task_root = output / task_id
        manifest_path = task_root / "input_manifest.json"
        if args.prepare or not manifest_path.is_file():
            manifest = _prepare_task(task_id, RUNTIME_ROOT / filename, output, progress)
        else:
            manifest = _load(manifest_path)
        manifests.append(manifest)
        progress.emit({"stage": "task_prepared", "task_id": task_id, "completed_tasks": index, "total_tasks": len(selected_tasks)})
    if args.prepare and not args.execute:
        return 0
    if not args.allow_provider_execution:
        raise RuntimeError("provider execution requires explicit --allow-provider-execution")
    for index, manifest in enumerate(manifests, start=1):
        task_id = str(manifest["task_id"])
        task_root = output / task_id
        results = _execute_cells(manifest["cells"], output_root=task_root, phase="pilot", workers=1, progress=progress)
        summary = summarize_results(results)
        summary.update({
            "task_id": task_id,
            "world_seed": WORLD_SEED,
            "candidate_packet_seed": PACKET_SEED,
            "interpretation_status": "development_one_world_three_arm_open_action_only",
            "resource_profile": RESOURCE_PROFILE,
            "formal_denominator": False,
            "all_scheduled_records_retained": len(results) == 3,
            "provider_free_truth_query_count": int(manifest["checkpoint_query_count"]) + int(manifest["candidate_count"]),
            "provider_free_exact_replay_count": int(manifest["checkpoint_query_count"]) + int(manifest["candidate_count"]),
            "public_truth_binding_status": "passed",
            "candidate_outcomes_hidden_from_agent": True,
            "candidate_action_plans_public": True,
        })
        summary["summary_sha256"] = canonical_json_sha256({key: value for key, value in summary.items() if key != "summary_sha256"})
        write_json_atomic(task_root / "summary.json", summary)
        _write_report(task_id, summary, task_root / "REPORT_ZH.md")
        progress.emit({"stage": "task_provider_complete", "task_id": task_id, "completed_tasks": index, "total_tasks": len(selected_tasks)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
