#!/usr/bin/env python3
"""Screen a larger candidate-disjoint oracle grid on exposed construction worlds."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import qualify_work_ii_evidence_to_action_oracle as oracle_runner
import run_work_ii_multi_task_open_action_pilot as task_runner
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    build_hybrid_disjoint_oracle_grid,
    evaluate_candidate_packet,
    evaluate_oracle_law_candidate_order,
    fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid,
    split_registered_query_pool_maximin,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/work_ii_evidence_to_action_large_grid_v1.0.json"
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-large-grid-v1.0"
    / "construction-screen-v0.1"
)


def _validate_screen(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    units = protocol.get("construction_screen_units")
    if not isinstance(units, list) or not units:
        raise ValueError("construction screen units are missing")
    tasks = protocol["task_runtime_sources"]
    scheduled: list[dict[str, Any]] = []
    identities: set[tuple[str, int]] = set()
    reserved = {
        int(seed)
        for key in ("qualification_world_seeds", "formal_world_seeds")
        for seed in protocol[key]
    }
    for unit in units:
        if not isinstance(unit, dict):
            raise ValueError("construction screen unit must be an object")
        task_id = str(unit.get("task_id"))
        world_seed = unit.get("world_seed")
        role = str(unit.get("role"))
        if task_id not in tasks:
            raise ValueError(f"unknown construction task: {task_id}")
        if not isinstance(world_seed, int) or isinstance(world_seed, bool):
            raise ValueError("construction world seed must be an integer")
        identity = (task_id, world_seed)
        if identity in identities:
            raise ValueError(f"duplicate construction unit: {task_id}/seed{world_seed}")
        if world_seed in reserved:
            raise ValueError(f"construction unit uses a prospective/reserved seed: {world_seed}")
        identities.add(identity)
        scheduled.append({"task_id": task_id, "world_seed": world_seed, "role": role})
    return scheduled


def _prepare_task(
    *,
    protocol: dict[str, Any],
    task_id: str,
    task_index: int,
    output_root: Path,
) -> dict[str, Any]:
    source = oracle_runner._load((ROOT / protocol["task_runtime_sources"][task_id]).resolve())
    checkpoint = source.get("belief_checkpoint")
    checkpoint = checkpoint if isinstance(checkpoint, dict) else {}
    registered = checkpoint.get("held_out_queries")
    if not isinstance(registered, list):
        raise ValueError(f"{task_id}: registered query pool is missing")
    feature_ids = [str(item) for item in checkpoint.get("allowed_feature_ids", [])]
    metric_ids = task_runner._task_metrics(source)
    candidates, _ = split_registered_query_pool_maximin(
        registered,
        allowed_feature_ids=feature_ids,
    )
    candidate_ids = [str(row["query_id"]) for row in candidates]
    contract = protocol["oracle_grid_contract"]
    global_count = int(contract["global_query_count_per_task"])
    neighborhood_count = int(contract["candidate_neighborhood_query_count_per_task"])
    oversampling = int(contract["compile_valid_oversampling_factor"])
    proposed = build_hybrid_disjoint_oracle_grid(
        registered,
        allowed_feature_ids=feature_ids,
        allowed_metric_ids=metric_ids,
        candidate_query_ids=candidate_ids,
        global_query_count=global_count * oversampling,
        neighborhood_query_count=neighborhood_count * oversampling,
        neighborhood_span_fraction=float(contract["candidate_neighborhood_span_fraction"]),
        grid_id=f"e2a-lg-t{task_index + 1}",
    )
    grid = oracle_runner._compile_valid_grid(
        source,
        proposed,
        required_component_counts={
            "global": global_count,
            "candidate_neighborhood": neighborhood_count,
        },
    )
    if len(grid) != int(contract["query_count_per_task"]):
        raise AssertionError("compiled large-grid denominator differs")
    write_json_atomic(
        output_root / task_id / "registered_oracle_grid.json",
        {
            "schema_version": "chemworld-work-ii-evidence-to-action-oracle-grid-0.1",
            "task_id": task_id,
            "construction_rule": contract["construction_rule"],
            "selection_reads_truth": False,
            "proposed_query_count": len(proposed),
            "compile_valid_query_count": len(grid),
            "candidate_query_ids": candidate_ids,
            "component_counts": {
                "global": global_count,
                "candidate_neighborhood": neighborhood_count,
            },
            "queries": grid,
        },
    )
    return {
        "source": source,
        "registered": registered,
        "feature_ids": feature_ids,
        "metric_ids": metric_ids,
        "candidates": candidates,
        "candidate_ids": candidate_ids,
        "grid": grid,
    }


def _build_summary(
    protocol: dict[str, Any],
    scheduled: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    completed = len(rows)
    passed = sum(row["status"] == "passed" and row["candidate_status"] == "passed" for row in rows)
    finished = completed == len(scheduled)
    status = "in_progress"
    if finished:
        status = "passed" if passed == len(scheduled) else "scientifically_rejected"
    return {
        "schema_version": "chemworld-work-ii-evidence-to-action-large-grid-screen-0.1",
        "study_id": protocol["study_id"],
        "status": status,
        "evidence_role": "exposed_construction_only",
        "prospective_qualification_authorized": finished and status == "passed",
        "provider_execution_authorized": False,
        "planned_unit_count": len(scheduled),
        "evaluated_unit_count": completed,
        "passed_unit_count": passed,
        "scientifically_rejected_unit_count": completed - passed,
        "not_started_unit_count": len(scheduled) - completed,
        "grid_query_count_per_unit": int(protocol["oracle_grid_contract"]["query_count_per_task"]),
        "grid_truth_query_count": sum(int(row["grid_truth_query_count"]) for row in rows),
        "grid_exact_replay_query_count": sum(
            int(row["grid_exact_replay_query_count"]) for row in rows
        ),
        "registered_truth_query_count": sum(
            int(row["registered_truth_query_count"]) for row in rows
        ),
        "registered_exact_replay_query_count": sum(
            int(row["registered_exact_replay_query_count"]) for row in rows
        ),
        "provider_call_count": 0,
        "candidate_outcome_read_by_fitter_count": 0,
        "fit_candidate_overlap_count": sum(int(row["fit_candidate_overlap_count"]) for row in rows),
        "qualification_seed_evaluation_count": 0,
        "formal_seed_evaluation_count": 0,
        "threshold_relaxation": False,
        "outcome_based_replacement_count": 0,
        "failed_unit_removed": False,
        "unit_rows": rows,
    }


def _write_report(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Work II evidence-to-action large-grid oracle construction screen",
        "",
        f"状态: **{summary['status']}**",
        "",
        (
            f"完成 {summary['evaluated_unit_count']}/"
            f"{summary['planned_unit_count']} exposed units; "
            f"通过 {summary['passed_unit_count']}; 科学失败 "
            f"{summary['scientifically_rejected_unit_count']}。"
        ),
        "",
        "| task | seed | role | candidate | rho | oracle | Top-1 | rank | distill error |",
        "|---|---:|---|---|---:|---|---|---:|---:|",
    ]
    lines.extend(
        "| {task_id} | {world_seed} | {role} | {candidate_status} | {rho:.6f} | "
        "{status} | {top1} | {rank} | {error:.3e} |".format(
            task_id=row["task_id"],
            world_seed=row["world_seed"],
            role=row["role"],
            candidate_status=row["candidate_status"],
            rho=float(row["spearman_rank_correlation"]),
            status=row["status"],
            top1=str(bool(row["top1_agreement"])).lower(),
            rank=row["candidate_design_rank"],
            error=float(row["typed_distillation_maximum_absolute_error"]),
        )
        for row in summary["unit_rows"]
    )
    lines.extend(
        [
            "",
            (
                "本结果只用于 exposed construction。只有 7/7 通过才授权冻结独立 prospective "
                "qualification; 任何结果都不恢复 W2-51 或授权 provider/formal execution。"
            ),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--shards", type=int, default=32)
    args = parser.parse_args()
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    protocol = oracle_runner._load(protocol_path.resolve())
    scheduled = _validate_screen(protocol)
    if args.workers < 1 or args.shards < 1:
        raise ValueError("workers and shards must be positive")

    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.STUDY_ID = f"{protocol['study_id']}--construction-screen"
    task_runner.FORMAL_RESULT = False
    task_runner.FORMAL_PREFLIGHT_SHA256 = None
    task_runner.TESTED_COMMIT = None
    progress = Progress(output_root / "progress.jsonl")
    task_order = list(protocol["task_runtime_sources"])
    prepared = {
        task_id: _prepare_task(
            protocol=protocol,
            task_id=task_id,
            task_index=task_order.index(task_id),
            output_root=output_root,
        )
        for task_id in {unit["task_id"] for unit in scheduled}
    }
    rows: list[dict[str, Any]] = []
    artifact_contract = protocol["artifact_contract"]
    for unit_index, unit in enumerate(scheduled, start=1):
        task_id = unit["task_id"]
        world_seed = int(unit["world_seed"])
        task = prepared[task_id]
        progress.emit(
            {
                "stage": "large_grid_construction_unit_started",
                "completed_units": unit_index - 1,
                "total_units": len(scheduled),
                "task_id": task_id,
                "world_seed": world_seed,
            }
        )
        grid_report = oracle_runner._grid_report(
            task_id=task_id,
            world_seed=world_seed,
            source=task["source"],
            grid=task["grid"],
            output_root=output_root,
            progress=progress,
            workers=int(args.workers),
            shard_count=int(args.shards),
        )
        registered_report = oracle_runner._grid_report(
            task_id=task_id,
            world_seed=world_seed,
            source=task["source"],
            grid=[deepcopy(dict(query)) for query in task["registered"]],
            output_root=output_root / "registered-truth",
            progress=progress,
            workers=int(args.workers),
            shard_count=min(int(args.shards), len(task["registered"])),
        )
        fit_truth = {str(key): dict(value) for key, value in grid_report["truth"].items()}
        registered_truth = {
            str(key): dict(value) for key, value in registered_report["truth"].items()
        }
        candidate_truth = {
            query_id: registered_truth[query_id] for query_id in task["candidate_ids"]
        }
        candidate_qualification = evaluate_candidate_packet(
            candidate_truth,
            protocol["candidate_contract"],
        )
        artifact = fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid(
            task["grid"],
            fit_truth,
            candidate_queries=task["candidates"],
            allowed_feature_ids=task["feature_ids"],
            allowed_metric_ids=task["metric_ids"],
            summary_id=f"oracle-large-grid-v1.0--{task_id}--seed{world_seed}",
            tree_count=int(artifact_contract["oracle_candidate_predictor_tree_count"]),
            min_samples_leaf=int(artifact_contract["oracle_candidate_predictor_min_samples_leaf"]),
            random_seed=int(artifact_contract["oracle_candidate_predictor_random_seed"]),
            distillation_tolerance=float(
                artifact_contract["oracle_candidate_distillation_tolerance"]
            ),
        )
        qualification = evaluate_oracle_law_candidate_order(
            artifact,
            candidate_queries=task["candidates"],
            candidate_truth=candidate_truth,
            allowed_feature_ids=task["feature_ids"],
            allowed_metric_ids=task["metric_ids"],
            minimum_rank_correlation=float(
                artifact_contract["minimum_oracle_candidate_rank_correlation"]
            ),
        )
        write_json_atomic(
            output_root / task_id / f"seed-{world_seed}" / "oracle_artifact.json",
            artifact,
        )
        calibration = artifact["calibration_contract"]
        row = {
            "task_id": task_id,
            "world_seed": world_seed,
            "role": unit["role"],
            "grid_truth_query_count": int(grid_report["truth_query_count"]),
            "grid_exact_replay_query_count": int(grid_report["exact_replay_query_count"]),
            "registered_truth_query_count": int(registered_report["truth_query_count"]),
            "registered_exact_replay_query_count": int(
                registered_report["exact_replay_query_count"]
            ),
            "candidate_status": candidate_qualification["status"],
            "candidate_qualification": candidate_qualification,
            "candidate_design_rank": int(calibration["candidate_design_rank"]),
            "typed_distillation_maximum_absolute_error": float(
                calibration["maximum_absolute_error"]
            ),
            **qualification,
        }
        rows.append(row)
        progress.emit(
            {
                "stage": "large_grid_construction_unit_terminal",
                "completed_units": unit_index,
                "total_units": len(scheduled),
                "task_id": task_id,
                "world_seed": world_seed,
                "status": row["status"],
                "spearman_rank_correlation": row["spearman_rank_correlation"],
            }
        )
        partial = _build_summary(protocol, scheduled, rows)
        write_json_atomic(output_root / "summary.json", partial)
        _write_report(output_root / "REPORT_ZH.md", partial)

    summary = _build_summary(protocol, scheduled, rows)
    write_json_atomic(output_root / "summary.json", summary)
    _write_report(output_root / "REPORT_ZH.md", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
