#!/usr/bin/env python3
"""Qualify a dense, candidate-disjoint oracle law before provider execution."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import run_work_ii_multi_task_open_action_pilot as task_runner
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    build_hybrid_disjoint_oracle_grid,
    evaluate_oracle_law_candidate_order,
    fit_oracle_law_from_disjoint_grid,
    split_registered_query_pool_maximin,
    validate_protocol,
)
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
DEFAULT_CANDIDATE_ROOT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1"
    / "qualification-v2"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1"
    / "oracle-qualification-v0.5"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _truth(path: Path) -> dict[str, dict[str, Any]]:
    report = _load(path)
    truth = report.get("truth")
    if report.get("status") != "completed" or not isinstance(truth, dict):
        raise ValueError(f"{path}: evaluator truth is incomplete")
    return {str(query_id): dict(metrics) for query_id, metrics in truth.items()}


def _execute_truth_shard(
    task_id: str,
    world_seed: int,
    source: dict[str, Any],
    queries: list[dict[str, Any]],
    shard_index: int,
    shard_root: Path,
) -> dict[str, Any]:
    report_path = shard_root / "report.json"
    if report_path.is_file():
        return _load(report_path)
    task_runner.WORLD_SEED = world_seed
    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.FORMAL_RESULT = False
    task_runner.FORMAL_PREFLIGHT_SHA256 = None
    task_runner.TESTED_COMMIT = None
    runtime = task_runner._prepare_runtime(
        source,
        task_id=task_id,
        checkpoint_queries=queries,
    )
    cluster = {
        "world_cluster_id": (
            f"E2A_ORACLE--{task_id}--seed{world_seed}--shard{shard_index:02d}"
        ),
        "task_id": task_id,
        "world_seed": world_seed,
    }
    plan = build_evaluator_truth_plan(
        cluster,
        runtime,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    errors = validate_evaluator_truth_plan(plan)
    if errors:
        raise ValueError(
            f"{task_id}/seed-{world_seed}/shard-{shard_index}: invalid plan: "
            f"{'; '.join(errors)}"
        )
    report = execute_evaluator_truth_plan(plan, runtime, shard_root)
    errors = validate_evaluator_truth_report(report, plan)
    if errors or report.get("status") != "completed":
        raise ValueError(
            f"{task_id}/seed-{world_seed}/shard-{shard_index}: truth failed: "
            f"{'; '.join(errors) or report.get('status')}"
        )
    return report


def _grid_report(
    *,
    task_id: str,
    world_seed: int,
    source: dict[str, Any],
    grid: list[dict[str, Any]],
    output_root: Path,
    progress: Progress,
    workers: int,
    shard_count: int,
) -> dict[str, Any]:
    cluster_root = output_root / task_id / f"seed-{world_seed}"
    summary_path = cluster_root / "grid-truth-summary.json"
    if summary_path.is_file():
        return _load(summary_path)
    shards = [grid[index::shard_count] for index in range(shard_count)]
    shards = [shard for shard in shards if shard]

    reports: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _execute_truth_shard,
                task_id,
                world_seed,
                source,
                shard,
                index,
                cluster_root / "grid-truth-shards" / f"shard-{index:02d}",
            ): index
            for index, shard in enumerate(shards, start=1)
        }
        for future in as_completed(futures):
            reports.append(future.result())
            progress.emit(
                {
                    "stage": "oracle_truth_shard_terminal",
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "completed_shards": len(reports),
                    "total_shards": len(shards),
                    "completed_queries": sum(
                        int(report["completed_truth_query_count"]) for report in reports
                    ),
                    "total_queries": len(grid),
                }
            )
    truth = {
        str(query_id): dict(metrics)
        for report in reports
        for query_id, metrics in report["truth"].items()
    }
    if len(truth) != len(grid):
        raise ValueError(f"{task_id}/seed-{world_seed}: combined oracle truth differs")
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-oracle-grid-truth-0.1",
        "status": "completed",
        "task_id": task_id,
        "world_seed": world_seed,
        "truth_query_count": len(grid),
        "completed_truth_query_count": len(truth),
        "failed_truth_query_count": 0,
        "shard_count": len(shards),
        "truth": truth,
    }
    write_json_atomic(summary_path, summary)
    return summary


def _compile_valid_grid(
    source: dict[str, Any],
    proposed: list[dict[str, Any]],
    *,
    required_component_counts: dict[str, int],
) -> list[dict[str, Any]]:
    retained: list[dict[str, Any]] = []
    counts = dict.fromkeys(required_component_counts, 0)
    for query in proposed:
        component = str(query.get("grid_component"))
        if component not in counts or counts[component] >= required_component_counts[component]:
            continue
        try:
            compile_evaluator_truth_query(source, query)
        except (TypeError, ValueError):
            continue
        retained.append(query)
        counts[component] += 1
        if counts == required_component_counts:
            break
    if counts != required_component_counts:
        raise ValueError(
            "public compile-valid oracle grid did not reach its registered denominator"
        )
    return retained


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--candidate-root", type=Path, default=DEFAULT_CANDIDATE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--shards", type=int, default=16)
    args = parser.parse_args()
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    candidate_root = (
        args.candidate_root if args.candidate_root.is_absolute() else ROOT / args.candidate_root
    ).resolve()
    output_root = (
        args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    ).resolve()
    protocol = _load(protocol_path.resolve())
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    if args.workers < 1 or args.shards < 1:
        raise ValueError("workers and shards must be positive")

    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.STUDY_ID = f"{protocol['study_id']}--oracle-qualification"
    task_runner.FORMAL_RESULT = False
    task_runner.FORMAL_PREFLIGHT_SHA256 = None
    task_runner.TESTED_COMMIT = None
    progress = Progress(output_root / "progress.jsonl")
    rows: list[dict[str, Any]] = []
    tasks = list(protocol["task_runtime_sources"].items())
    worlds = [int(seed) for seed in protocol["qualification_world_seeds"]]
    total = len(tasks) * len(worlds)
    for task_index, (task_id, runtime_path) in enumerate(tasks):
        source = _load((ROOT / str(runtime_path)).resolve())
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
        grid_contract = protocol["oracle_grid_contract"]
        target_grid_count = int(grid_contract["query_count_per_task"])
        global_count = int(grid_contract["global_query_count_per_task"])
        neighborhood_count = int(
            grid_contract["candidate_neighborhood_query_count_per_task"]
        )
        oversampling = int(grid_contract["compile_valid_oversampling_factor"])
        proposed_grid = build_hybrid_disjoint_oracle_grid(
            registered,
            allowed_feature_ids=feature_ids,
            allowed_metric_ids=metric_ids,
            candidate_query_ids=candidate_ids,
            global_query_count=global_count * oversampling,
            neighborhood_query_count=neighborhood_count * oversampling,
            neighborhood_span_fraction=float(
                grid_contract["candidate_neighborhood_span_fraction"]
            ),
            grid_id=f"oracle-grid--{task_id}",
        )
        grid = _compile_valid_grid(
            source,
            proposed_grid,
            required_component_counts={
                "global": global_count,
                "candidate_neighborhood": neighborhood_count,
            },
        )
        if len(grid) != target_grid_count:
            raise AssertionError("compiled hybrid oracle grid denominator differs")
        write_json_atomic(
            output_root / task_id / "registered_oracle_grid.json",
            {
                "schema_version": "chemworld-work-ii-evidence-to-action-oracle-grid-0.1",
                "task_id": task_id,
                "construction_rule": grid_contract["construction_rule"],
                "selection_reads_truth": False,
                "proposed_query_count": len(proposed_grid),
                "compile_valid_query_count": len(grid),
                "candidate_query_ids": candidate_ids,
                "component_counts": {
                    "global": global_count,
                    "candidate_neighborhood": neighborhood_count,
                },
                "queries": grid,
            },
        )
        for world_index, world_seed in enumerate(worlds):
            unit = task_index * len(worlds) + world_index + 1
            progress.emit(
                {
                    "stage": "oracle_qualification_cluster_started",
                    "completed_clusters": unit - 1,
                    "total_clusters": total,
                    "task_id": task_id,
                    "world_seed": world_seed,
                }
            )
            report = _grid_report(
                task_id=task_id,
                world_seed=world_seed,
                source=source,
                grid=grid,
                output_root=output_root,
                progress=progress,
                workers=int(args.workers),
                shard_count=int(args.shards),
            )
            fit_truth = {str(key): dict(value) for key, value in report["truth"].items()}
            retained_task_root = (
                candidate_root
                / task_id
                / f"seed-{world_seed}"
                / task_id
            )
            all_registered_truth = {
                **_truth(retained_task_root / "candidate-truth/report.json"),
                **_truth(retained_task_root / "checkpoint-truth/report.json"),
            }
            if len(all_registered_truth) != 16 or not set(candidate_ids).issubset(
                all_registered_truth
            ):
                raise ValueError(
                    f"{task_id}/seed-{world_seed}: registered truth identity differs"
                )
            candidate_truth = {
                query_id: all_registered_truth[query_id] for query_id in candidate_ids
            }
            artifact = fit_oracle_law_from_disjoint_grid(
                grid,
                fit_truth,
                candidate_query_ids=candidate_ids,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                summary_id=f"oracle--{task_id}--seed{world_seed}",
            )
            qualification = evaluate_oracle_law_candidate_order(
                artifact,
                candidate_queries=candidates,
                candidate_truth=candidate_truth,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                minimum_rank_correlation=float(
                    protocol["artifact_contract"]["minimum_oracle_candidate_rank_correlation"]
                ),
            )
            write_json_atomic(
                output_root / task_id / f"seed-{world_seed}" / "oracle_artifact.json",
                artifact,
            )
            rows.append(
                {
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "grid_truth_query_count": len(fit_truth),
                    "candidate_truth_query_count": len(candidate_truth),
                    **qualification,
                }
            )
            progress.emit(
                {
                    "stage": "oracle_qualification_cluster_terminal",
                    "completed_clusters": unit,
                    "total_clusters": total,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "status": qualification["status"],
                    "spearman_rank_correlation": qualification[
                        "spearman_rank_correlation"
                    ],
                }
            )

    passed = sum(row["status"] == "passed" for row in rows)
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-oracle-qualification-0.1",
        "study_id": protocol["study_id"],
        "status": "passed" if passed == total else "rejected",
        "provider_execution_authorized": False,
        "expected_cluster_count": total,
        "evaluated_cluster_count": len(rows),
        "passed_cluster_count": passed,
        "oracle_grid_query_count_per_task_world": int(
            protocol["oracle_grid_contract"]["query_count_per_task"]
        ),
        "provider_call_count": 0,
        "cluster_rows": rows,
    }
    write_json_atomic(output_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
