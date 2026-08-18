#!/usr/bin/env python3
"""Run the user-authorized W2-48 one-world, one-seed, three-arm development pilot."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_campaign_pilot import _checkpoint_contract
from work_ii_longitudinal_runtime import Progress, _execute_cells

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import (
    _world_campaign_config,
    summarize_results,
)
from chemworld.eval.work_ii_open_action_decision import (
    ARMS,
    build_open_terminal_contract,
    compile_public_candidate_packet,
    validate_public_truth_binding,
)
from chemworld.eval.work_ii_truth import (
    WORK_II_TRUTH_PLAN_VERSION,
    _noise_binding,
    build_evaluator_truth_plan,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/work_ii_as_open_action_decision_v0.1.json"
DEFAULT_GRID = ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT / "runs/development/work-ii-as-open-action-decision-single-world-seed153150025-v0.1"
)
RUNTIME_RELATIVE = (
    "workstreams/flagship_tasks/reports/"
    "work-ii-w2-26-deepseek-runtime-configs-v0.1/a_s--partition-discovery--r12.json"
)
WORLD_SEED = 153150025
PACKET_SEED = 400


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _candidate_truth_plan(
    runtime: Mapping[str, Any],
    *,
    cluster_id: str,
    world_seed: int,
    compiled_by_id: Mapping[str, Mapping[str, Any]],
    public_candidates: list[Mapping[str, Any]],
) -> dict[str, Any]:
    queries: list[dict[str, Any]] = []
    for index, public in enumerate(public_candidates, start=1):
        query_id = str(public["query_id"])
        compiled = deepcopy(dict(compiled_by_id[query_id]))
        query = {
            **compiled,
            "execution_index": index,
            "execution_id": f"{cluster_id}--candidate-truth-{index:02d}",
            **_noise_binding(
                formal_preflight_sha256=None,
                world_cluster_id=cluster_id,
                query_id=query_id,
            ),
        }
        if query["action_plan"] != public["action_plan"]:
            raise ValueError(f"candidate {query_id} public/truth action plan differs")
        queries.append(query)
    checkpoint = _checkpoint_contract(runtime, "opaque")
    plan: dict[str, Any] = {
        "schema_version": WORK_II_TRUTH_PLAN_VERSION,
        "formal_result": False,
        "formal_preflight_sha256": None,
        "world_cluster_id": cluster_id,
        "task_id": str(runtime["task_id"]),
        "world_seed": int(world_seed),
        "campaign_config_sha256": canonical_json_sha256(runtime),
        "truth_query_count": len(queries),
        "truth_query_metric_count": sum(len(item["metric_ids"]) for item in queries),
        "evaluator_provider_call_count": 0,
        "participant_operation_denominator_impact": 0,
        "participant_feedback_allowed": False,
        "shared_across_prior_arms": True,
        "law_summary_contract": {
            "allowed_feature_ids": list(checkpoint["allowed_feature_ids"]),
            "allowed_metric_ids": list(checkpoint["allowed_metric_ids"]),
            "required_metric_ids": list(checkpoint["allowed_metric_ids"]),
            "evidence_catalog": list(checkpoint["evidence_catalog"]),
        },
        "queries": queries,
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S 开放式综合决策 - 单世界三臂 development pilot",
        "",
        "本报告只用于接口与科学流程诊断, 不进入 W2-48 正式五世界分母。",
        "",
        f"完成资格 cell: {summary.get('eligible_cell_count')}/"
        f"{summary.get('scheduled_cell_count')}",
        "",
        "| arm | 状态 | 完成实验数 | 选中真实排名 | Top-1 | raw regret | "
        "normalized regret | law MAE |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(summary.get("cell_rows", []), key=lambda item: str(item.get("arm"))):
        lines.append(
            f"| {row.get('arm')} | {row.get('status')} | "
            f"{row.get('campaign_complete_experiment_count')} | {row.get('selected_rank')} | "
            f"{int(row.get('top1_selected') is True)} | {row.get('raw_regret')} | "
            f"{row.get('normalized_regret')} | {row.get('law_normalized_mae')} |"
        )
    lines.extend(
        [
            "",
            "## 绑定检查",
            "",
            f"- provider-free truth: {summary.get('provider_free_truth_query_count')}",
            f"- exact replay: {summary.get('provider_free_exact_replay_count')}",
            f"- public/truth plan binding: {summary.get('public_truth_binding_status')}",
            "- 候选 outcome、hidden rank、checkpoint truth、其他 arm 证据均未公开。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prepare_pilot(protocol_path: Path, grid_path: Path, output_root: Path) -> dict[str, Any]:
    protocol = _load(protocol_path)
    grid_protocol = _load(grid_path)
    if protocol.get("development_pilot", {}).get("world_seed") != WORLD_SEED:
        raise ValueError("development pilot world seed drifted")
    if protocol.get("development_pilot", {}).get("candidate_packet_seed") != PACKET_SEED:
        raise ValueError("development pilot packet seed drifted")
    if protocol.get("arms") != list(ARMS):
        raise ValueError("W2-48 arm order drifted")
    runtime = _load(ROOT / RUNTIME_RELATIVE)
    if runtime.get("campaign", {}).get("complete_experiments") != 12:
        raise ValueError("pilot requires twelve campaign experiments")
    output_root.mkdir(parents=True, exist_ok=True)
    public_candidates, compiled_by_id = compile_public_candidate_packet(
        runtime,
        candidate_grid_protocol=grid_protocol,
        packet_seed=PACKET_SEED,
    )
    binding_errors = validate_public_truth_binding(public_candidates, compiled_by_id)
    if binding_errors:
        raise ValueError("public/truth candidate binding failed: " + "; ".join(binding_errors))
    cluster_id = f"A_S_OAD_PILOT--partition-discovery--seed{WORLD_SEED}"
    campaign_config = _world_campaign_config(
        runtime,
        study_id=str(protocol["study_id"]),
        world_seed=WORLD_SEED,
        terminal_contract=build_open_terminal_contract(
            study_id=str(protocol["study_id"]),
            world_seed=WORLD_SEED,
            public_candidates=public_candidates,
        ),
    )
    campaign_config["pilot_id"] = f"{protocol['study_id']}--seed{WORLD_SEED}"
    campaign_config["formal_result"] = False
    checkpoint_contract = dict(campaign_config.get("belief_checkpoint", {}))
    checkpoint_contract["allowed_metric_ids"] = [
        "product_in_organic",
        "product_in_aqueous",
        "phase_ratio",
        "score",
    ]
    checkpoint_contract["held_out_queries"] = [
        {
            **dict(query),
            "metric_ids": list(checkpoint_contract["allowed_metric_ids"]),
        }
        for query in checkpoint_contract.get("held_out_queries", [])
    ]
    campaign_config["belief_checkpoint"] = checkpoint_contract
    campaign_config_path = output_root / "campaign-config.json"
    write_json_atomic(campaign_config_path, campaign_config)

    checkpoint_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": "partition-discovery",
            "world_seed": WORLD_SEED,
        },
        campaign_config,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    checkpoint_errors = validate_evaluator_truth_plan(checkpoint_plan)
    if checkpoint_errors:
        raise ValueError("invalid checkpoint truth plan: " + "; ".join(checkpoint_errors))
    checkpoint_root = output_root / "checkpoint-truth"
    checkpoint_report = execute_evaluator_truth_plan(
        checkpoint_plan, campaign_config, checkpoint_root
    )
    checkpoint_report_errors = validate_evaluator_truth_report(checkpoint_report, checkpoint_plan)
    if checkpoint_report_errors or checkpoint_report.get("status") != "completed":
        raise ValueError(
            "checkpoint truth gate failed: "
            + ("; ".join(checkpoint_report_errors) or str(checkpoint_report.get("status")))
        )

    candidate_plan = _candidate_truth_plan(
        campaign_config,
        cluster_id=cluster_id,
        world_seed=WORLD_SEED,
        compiled_by_id=compiled_by_id,
        public_candidates=public_candidates,
    )
    candidate_errors = validate_evaluator_truth_plan(candidate_plan)
    if candidate_errors:
        raise ValueError("invalid candidate truth plan: " + "; ".join(candidate_errors))
    candidate_root = output_root / "candidate-truth"
    candidate_report = execute_evaluator_truth_plan(
        candidate_plan, campaign_config, candidate_root
    )
    candidate_report_errors = validate_evaluator_truth_report(candidate_report, candidate_plan)
    if candidate_report_errors or candidate_report.get("status") != "completed":
        raise ValueError(
            "candidate truth gate failed: "
            + ("; ".join(candidate_report_errors) or str(candidate_report.get("status")))
        )
    candidate_truth = deepcopy(dict(candidate_report["truth"]))
    ranks = {
        query_id: rank
        for rank, query_id in enumerate(
            sorted(candidate_truth, key=lambda item: (-candidate_truth[item]["score"], item)),
            start=1,
        )
    }
    plan_hashes = {
        str(row["query_id"]): str(row["action_plan_sha256"])
        for row in public_candidates
    }
    contract = campaign_config["terminal_action_readout"]
    cells = [
        {
            "cell_id": f"{cluster_id}--{arm}",
            "cluster_id": cluster_id,
            "world_seed": WORLD_SEED,
            "arm": arm,
            "campaign_config_path": campaign_config_path.relative_to(output_root).as_posix(),
            "terminal_action_readout": deepcopy(contract),
            "candidate_truth": deepcopy(candidate_truth),
            "presented_candidate_ranks": deepcopy(ranks),
            "candidate_pool_ranks": deepcopy(ranks),
            "candidate_action_plan_sha256": deepcopy(plan_hashes),
            "checkpoint_truth_plan": deepcopy(checkpoint_plan),
            "checkpoint_truth": deepcopy(dict(checkpoint_report["truth"])),
        }
        for arm in ARMS
    ]
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-as-open-action-decision-pilot-manifest-0.1",
        "study_id": protocol["study_id"],
        "status": "prepared_development_provider_execution_authorized_by_user",
        "protocol_sha256": canonical_json_sha256(protocol),
        "candidate_grid_protocol_sha256": canonical_json_sha256(grid_protocol),
        "runtime_config": RUNTIME_RELATIVE,
        "world_seed": WORLD_SEED,
        "candidate_packet_seed": PACKET_SEED,
        "cluster_count": 1,
        "cell_count": 3,
        "campaign_experiment_count_per_cell": 12,
        "participant_physical_experiment_count": 36,
        "candidate_count": 8,
        "provider_free_truth_query_count": 24,
        "provider_free_exact_replay_count": 24,
        "public_truth_binding_validation_count": 8,
        "formal_denominator": False,
        "provider_execution_authorized": True,
        "public_candidates": public_candidates,
        "candidate_truth_plan_sha256": candidate_plan["plan_sha256"],
        "candidate_truth_report_sha256": candidate_report["report_sha256"],
        "checkpoint_truth_plan_sha256": checkpoint_plan["plan_sha256"],
        "checkpoint_truth_report_sha256": checkpoint_report["report_sha256"],
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    write_json_atomic(output_root / "public_candidate_packet.json", {
        "schema_version": "chemworld-work-ii-open-action-decision-public-packet-0.1",
        "world_seed": WORLD_SEED,
        "candidate_packet_seed": PACKET_SEED,
        "candidate_outcomes_included": False,
        "candidates": public_candidates,
    })
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--candidate-grid", type=Path, default=DEFAULT_GRID)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not args.prepare and not args.execute:
        parser.error("select --prepare or --execute")
    if args.workers != 1:
        parser.error("the ChemWorld coordinator contract requires one executor for this pilot")
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    grid_path = (
        args.candidate_grid
        if args.candidate_grid.is_absolute()
        else ROOT / args.candidate_grid
    )
    output = args.output_root.resolve()
    progress = Progress(output / "progress.jsonl")
    manifest_path = output / "input_manifest.json"
    if args.prepare or not manifest_path.is_file():
        manifest = prepare_pilot(protocol_path, grid_path, output)
        progress.emit(
            {
                "stage": "provider_free_preflight_complete",
                "world_seed": WORLD_SEED,
                "candidate_packet_seed": PACKET_SEED,
                "candidate_count": 8,
                "truth_queries": 24,
                "exact_replay_queries": 24,
                "public_truth_binding": "passed",
            }
        )
    else:
        manifest = _load(manifest_path)
    if args.prepare and not args.execute:
        return 0
    if not args.allow_provider_execution:
        raise RuntimeError("provider execution requires explicit --allow-provider-execution")
    results = _execute_cells(
        manifest["cells"],
        output_root=output,
        phase="pilot",
        workers=1,
        progress=progress,
    )
    summary = summarize_results(results)
    summary.update(
        {
            "study_id": manifest["study_id"],
            "world_seed": WORLD_SEED,
            "candidate_packet_seed": PACKET_SEED,
            "interpretation_status": "development_one_world_three_arm_open_action_only",
            "formal_denominator": False,
            "all_scheduled_records_retained": len(results) == 3,
            "provider_free_truth_query_count": manifest["provider_free_truth_query_count"],
            "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
            "public_truth_binding_status": "passed",
            "candidate_outcomes_hidden_from_agent": True,
            "candidate_action_plans_public": True,
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    _write_report(summary, output / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
