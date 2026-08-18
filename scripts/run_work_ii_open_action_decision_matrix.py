#!/usr/bin/env python3
"""Prepare and run the W2-48 five-world, three-arm development matrix."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_open_action_decision_pilot import (
    RUNTIME_RELATIVE,
    _candidate_truth_plan,
    _load,
)
from work_ii_longitudinal_runtime import Progress, _execute_cells

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import (
    ARMS,
    _world_campaign_config,
    summarize_results,
)
from chemworld.eval.work_ii_open_action_decision import (
    build_open_terminal_contract,
    compile_public_candidate_packet,
    validate_public_truth_binding,
)
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/work_ii_as_open_action_decision_v0.1.json"
DEFAULT_GRID = ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json"
DEFAULT_OUTPUT = ROOT / "runs/development/work-ii-as-open-action-decision-full-matrix-v0.1"


def _matrix_campaign_config(
    runtime: Mapping[str, Any],
    *,
    study_id: str,
    world_seed: int,
    public_candidates: list[Mapping[str, Any]],
) -> dict[str, Any]:
    contract = build_open_terminal_contract(
        study_id=study_id,
        world_seed=world_seed,
        public_candidates=public_candidates,
    )
    config = _world_campaign_config(
        runtime,
        study_id=study_id,
        world_seed=world_seed,
        terminal_contract=contract,
    )
    checkpoint = dict(config.get("belief_checkpoint", {}))
    metric_ids = [
        "product_in_organic",
        "product_in_aqueous",
        "phase_ratio",
        "score",
    ]
    checkpoint["allowed_metric_ids"] = metric_ids
    checkpoint["held_out_queries"] = [
        {
            **dict(query),
            "metric_ids": list(metric_ids),
        }
        for query in checkpoint.get("held_out_queries", [])
    ]
    config["belief_checkpoint"] = checkpoint
    config["formal_result"] = False
    config["pilot_id"] = f"{study_id}--seed{world_seed}"
    return config


def _world_record(
    *,
    protocol: Mapping[str, Any],
    grid_protocol: Mapping[str, Any],
    runtime: Mapping[str, Any],
    output_root: Path,
    world_seed: int,
    packet_seed: int,
    world_index: int,
    progress: Progress,
) -> dict[str, Any]:
    cluster_id = f"A_S_OAD_MATRIX--partition-discovery--seed{world_seed}"
    public_candidates, compiled_by_id = compile_public_candidate_packet(
        runtime,
        candidate_grid_protocol=grid_protocol,
        packet_seed=packet_seed,
    )
    binding_errors = validate_public_truth_binding(public_candidates, compiled_by_id)
    if binding_errors:
        raise ValueError(
            f"{cluster_id}: public/truth binding failed: " + "; ".join(binding_errors)
        )
    config = _matrix_campaign_config(
        runtime,
        study_id=str(protocol["study_id"]),
        world_seed=world_seed,
        public_candidates=public_candidates,
    )
    config_path = output_root / "campaign-configs" / f"seed-{world_seed}.json"
    write_json_atomic(config_path, config)

    checkpoint_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": "partition-discovery",
            "world_seed": world_seed,
        },
        config,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    checkpoint_errors = validate_evaluator_truth_plan(checkpoint_plan)
    if checkpoint_errors:
        raise ValueError(f"{cluster_id}: invalid checkpoint plan: " + "; ".join(checkpoint_errors))
    checkpoint_root = output_root / "checkpoint-truth" / cluster_id
    checkpoint_report = _reuse_or_execute_truth(
        checkpoint_plan,
        config,
        checkpoint_root,
    )
    checkpoint_report_errors = validate_evaluator_truth_report(checkpoint_report, checkpoint_plan)
    if checkpoint_report_errors or checkpoint_report.get("status") != "completed":
        raise ValueError(
            f"{cluster_id}: checkpoint truth failed: "
            + ("; ".join(checkpoint_report_errors) or str(checkpoint_report.get("status")))
        )

    candidate_plan = _candidate_truth_plan(
        config,
        cluster_id=cluster_id,
        world_seed=world_seed,
        compiled_by_id=compiled_by_id,
        public_candidates=public_candidates,
    )
    candidate_errors = validate_evaluator_truth_plan(candidate_plan)
    if candidate_errors:
        raise ValueError(f"{cluster_id}: invalid candidate plan: " + "; ".join(candidate_errors))
    candidate_root = output_root / "candidate-truth" / cluster_id
    candidate_report = _reuse_or_execute_truth(candidate_plan, config, candidate_root)
    candidate_report_errors = validate_evaluator_truth_report(candidate_report, candidate_plan)
    if candidate_report_errors or candidate_report.get("status") != "completed":
        raise ValueError(
            f"{cluster_id}: candidate truth failed: "
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
    contract = config["terminal_action_readout"]
    cells = [
        {
            "cell_id": f"{cluster_id}--{arm}",
            "cluster_id": cluster_id,
            "world_seed": world_seed,
            "arm": arm,
            "campaign_config_path": config_path.relative_to(output_root).as_posix(),
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
    write_json_atomic(
        output_root / "public-candidate-packets" / f"seed-{world_seed}.json",
        {
            "schema_version": "chemworld-work-ii-open-action-decision-public-packet-0.1",
            "world_seed": world_seed,
            "candidate_packet_seed": packet_seed,
            "candidate_outcomes_included": False,
            "candidates": public_candidates,
        },
    )
    progress.emit(
        {
            "stage": "matrix_provider_free_world_complete",
            "world_index": world_index,
            "total_worlds": 5,
            "world_seed": world_seed,
            "candidate_packet_seed": packet_seed,
            "checkpoint_truth_queries": checkpoint_plan["truth_query_count"],
            "candidate_truth_queries": candidate_plan["truth_query_count"],
            "exact_replay_queries": checkpoint_plan["truth_query_count"]
            + candidate_plan["truth_query_count"],
            "public_truth_binding": "passed",
        }
    )
    return {
        "world_seed": world_seed,
        "candidate_packet_seed": packet_seed,
        "cluster_id": cluster_id,
        "campaign_config_path": config_path.relative_to(output_root).as_posix(),
        "terminal_action_readout": deepcopy(contract),
        "public_candidates": public_candidates,
        "candidate_truth": candidate_truth,
        "presented_candidate_ranks": ranks,
        "candidate_pool_ranks": ranks,
        "candidate_action_plan_sha256": plan_hashes,
        "checkpoint_truth_plan": checkpoint_plan,
        "checkpoint_truth": deepcopy(dict(checkpoint_report["truth"])),
        "candidate_truth_plan_sha256": candidate_plan["plan_sha256"],
        "candidate_truth_report_sha256": candidate_report["report_sha256"],
        "checkpoint_truth_plan_sha256": checkpoint_plan["plan_sha256"],
        "checkpoint_truth_report_sha256": checkpoint_report["report_sha256"],
        "cells": cells,
    }


def _reuse_or_execute_truth(
    plan: Mapping[str, Any],
    config: Mapping[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    """Resume only from a complete immutable truth report; reject partial outputs."""

    if output_root.exists():
        report_path = output_root / "report.json"
        if not report_path.is_file():
            raise RuntimeError(
                "truth output is partial and cannot be resumed safely: "
                f"{output_root}"
            )
        report = _load(report_path)
        errors = validate_evaluator_truth_report(report, plan)
        if errors or report.get("status") != "completed":
            raise RuntimeError(
                f"existing truth output is invalid: {output_root}: "
                + ("; ".join(errors) or str(report.get("status")))
            )
        return report
    return execute_evaluator_truth_plan(plan, config, output_root)


def prepare_matrix(
    protocol_path: Path,
    grid_path: Path,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    protocol = _load(protocol_path)
    grid_protocol = _load(grid_path)
    runtime = _load(ROOT / RUNTIME_RELATIVE)
    worlds = protocol.get("formal_world_seeds")
    packet_seeds = protocol.get("formal_candidate_packet_seeds")
    if not isinstance(worlds, list) or len(worlds) != 5:
        raise ValueError("W2-48 requires five formal world seeds")
    if not isinstance(packet_seeds, list) or len(packet_seeds) != 5:
        raise ValueError("W2-48 requires five candidate packet seeds")
    if protocol.get("arms") != list(ARMS):
        raise ValueError("W2-48 arm order drifted")
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "campaign-configs").mkdir(parents=True, exist_ok=True)
    (output_root / "public-candidate-packets").mkdir(parents=True, exist_ok=True)
    worlds_out: list[dict[str, Any]] = []
    for index, (world_seed, packet_seed) in enumerate(
        zip(worlds, packet_seeds, strict=True), start=1
    ):
        worlds_out.append(
            _world_record(
                protocol=protocol,
                grid_protocol=grid_protocol,
                runtime=runtime,
                output_root=output_root,
                world_seed=int(world_seed),
                packet_seed=int(packet_seed),
                world_index=index,
                progress=progress,
            )
        )
    cells = [cell for world in worlds_out for cell in world["cells"]]
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-as-open-action-decision-matrix-manifest-0.1",
        "study_id": protocol["study_id"],
        "status": "prepared_development_full_matrix_provider_execution_authorized_by_user",
        "protocol_sha256": canonical_json_sha256(protocol),
        "candidate_grid_protocol_sha256": canonical_json_sha256(grid_protocol),
        "runtime_config": RUNTIME_RELATIVE,
        "world_count": 5,
        "world_seeds": [int(value) for value in worlds],
        "candidate_packet_seeds": [int(value) for value in packet_seeds],
        "cluster_count": 5,
        "cell_count": 15,
        "campaign_experiment_count_per_cell": 12,
        "participant_physical_experiment_count": 180,
        "candidate_count_per_world": 8,
        "checkpoint_truth_execution_count": 80,
        "candidate_truth_execution_count": 40,
        "provider_free_truth_query_count": 120,
        "provider_free_exact_replay_count": 120,
        "public_truth_binding_validation_count": 40,
        "formal_denominator": False,
        "provider_execution_authorized": True,
        "worlds": worlds_out,
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    return manifest


def _write_matrix_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S open-action full matrix development run",
        "",
        "本矩阵用于验证五世界三臂协议和决策接口, 不直接升级为 formal claim。",
        "",
        f"完成资格 cell: {summary.get('eligible_cell_count')}/"
        f"{summary.get('scheduled_cell_count')}",
        "",
        "| world | arm | 状态 | 实验数 | 选中排名 | Top-1 | raw regret | "
        "normalized regret | law MAE |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    rows = sorted(
        summary.get("cell_rows", []),
        key=lambda item: (int(item.get("world_seed", -1)), str(item.get("arm"))),
    )
    for row in rows:
        lines.append(
            f"| {row.get('world_seed')} | {row.get('arm')} | {row.get('status')} | "
            f"{row.get('campaign_complete_experiment_count')} | {row.get('selected_rank')} | "
            f"{int(row.get('top1_selected') is True)} | {row.get('raw_regret')} | "
            f"{row.get('normalized_regret')} | {row.get('law_normalized_mae')} |"
        )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            f"- provider-free truth: {summary.get('provider_free_truth_query_count')}",
            f"- exact replay: {summary.get('provider_free_exact_replay_count')}",
            f"- public/truth binding: {summary.get('public_truth_binding_status')}",
            "- candidate outcomes and ranks remain hidden from participant sessions.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
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
        manifest = prepare_matrix(protocol_path, grid_path, output, progress)
        progress.emit(
            {
                "stage": "matrix_provider_free_preflight_complete",
                "worlds": manifest["world_count"],
                "cells": manifest["cell_count"],
                "truth_queries": manifest["provider_free_truth_query_count"],
                "exact_replay_queries": manifest["provider_free_exact_replay_count"],
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
        phase="matrix",
        workers=args.workers,
        progress=progress,
    )
    summary = summarize_results(results)
    summary.update(
        {
            "study_id": manifest["study_id"],
            "world_count": manifest["world_count"],
            "world_seeds": manifest["world_seeds"],
            "candidate_packet_seeds": manifest["candidate_packet_seeds"],
            "interpretation_status": "development_full_five_world_three_arm_open_action",
            "formal_denominator": False,
            "all_scheduled_records_retained": len(results) == 15,
            "provider_free_truth_query_count": manifest["provider_free_truth_query_count"],
            "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
            "public_truth_binding_status": "passed",
            "candidate_outcomes_hidden_from_agent": True,
            "candidate_action_plans_public": True,
            "worker_count": args.workers,
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    _write_matrix_report(summary, output / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
