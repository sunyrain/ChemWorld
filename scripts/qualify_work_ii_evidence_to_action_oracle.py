#!/usr/bin/env python3
"""Qualify a dense, candidate-disjoint oracle law before provider execution."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from typing import Any

import run_work_ii_multi_task_open_action_pilot as task_runner
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    build_hybrid_disjoint_oracle_grid,
    evaluate_candidate_packet,
    evaluate_oracle_law_candidate_order,
    fit_candidate_calibrated_oracle_law_from_disjoint_grid,
    fit_candidate_domain_distilled_oracle_law_from_disjoint_grid,
    fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid,
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
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.4.json"
)
DEFAULT_CANDIDATE_ROOT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1"
    / "qualification-v2"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.4"
    / "oracle-qualification-v0.1"
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
        "world_cluster_id": (f"E2A_ORACLE--{task_id}--seed{world_seed}--shard{shard_index:02d}"),
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
            f"{task_id}/seed-{world_seed}/shard-{shard_index}: invalid plan: {'; '.join(errors)}"
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
    receipts = [receipt for report in reports for receipt in report.get("receipts", [])]
    exact_replay_count = sum(
        isinstance(receipt, dict)
        and isinstance(receipt.get("exact_replay"), dict)
        and receipt["exact_replay"].get("verified") is True
        and receipt["exact_replay"].get("mismatches") == []
        for receipt in receipts
    )
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-oracle-grid-truth-0.1",
        "status": "completed",
        "task_id": task_id,
        "world_seed": world_seed,
        "truth_query_count": len(grid),
        "completed_truth_query_count": len(truth),
        "failed_truth_query_count": 0,
        "exact_replay_query_count": exact_replay_count,
        "evaluator_provider_call_count": sum(
            int(report.get("evaluator_provider_call_count", 0)) for report in reports
        ),
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


def _qualification_summary(
    *,
    protocol: dict[str, Any],
    fit_strategy: str,
    rows: list[dict[str, Any]],
    scheduled_clusters: list[dict[str, Any]],
) -> dict[str, Any]:
    total = len(scheduled_clusters)
    passed = sum(row["status"] == "passed" and row["candidate_status"] == "passed" for row in rows)
    rejected = next(
        (row for row in rows if row["status"] != "passed" or row["candidate_status"] != "passed"),
        None,
    )
    return {
        "schema_version": "chemworld-work-ii-evidence-to-action-oracle-qualification-0.2",
        "study_id": protocol["study_id"],
        "status": "passed" if passed == total else "scientifically_rejected",
        "provider_execution_authorized": False,
        "expected_cluster_count": total,
        "evaluated_cluster_count": len(rows),
        "passed_cluster_count": passed,
        "scientifically_rejected_cluster_count": int(rejected is not None),
        "not_started_cluster_count": total - len(rows),
        "not_started_clusters": scheduled_clusters[len(rows) :],
        "failure": rejected,
        "oracle_grid_query_count_per_task_world": int(
            protocol["oracle_grid_contract"]["query_count_per_task"]
        ),
        "provider_call_count": 0,
        "oracle_fit_strategy": fit_strategy,
        "registered_truth_query_count": sum(
            int(row["registered_truth_query_count"]) for row in rows
        ),
        "registered_exact_replay_query_count": sum(
            int(row["registered_exact_replay_query_count"] or 0) for row in rows
        ),
        "grid_truth_query_count": sum(int(row["grid_truth_query_count"]) for row in rows),
        "grid_exact_replay_query_count": sum(
            int(row["grid_exact_replay_query_count"]) for row in rows
        ),
        "candidate_outcome_read_by_fitter_count": 0,
        "outcome_based_replacement_count": 0,
        "threshold_relaxation": False,
        "cluster_rows": rows,
    }


def _write_readable_summary(path: Path, summary: dict[str, Any]) -> None:
    rows = summary["cluster_rows"]
    lines = [
        "# Work II evidence-to-action oracle qualification",
        "",
        f"状态: **{summary['status']}**",
        "",
        (
            f"完成 {summary['evaluated_cluster_count']}/{summary['expected_cluster_count']} "
            f"clusters; 通过 {summary['passed_cluster_count']}; 未启动 "
            f"{summary['not_started_cluster_count']}。provider calls=0, candidate outcome "
            "read by fitter=0。"
        ),
        "",
        "| task | seed | candidate | oracle rho | oracle | Top-1 |",
        "|---|---:|---|---:|---|---|",
    ]
    lines.extend(
        "| {task_id} | {world_seed} | {candidate_status} | {rho:.6f} | {status} | {top1} |".format(
            task_id=row["task_id"],
            world_seed=row["world_seed"],
            candidate_status=row["candidate_status"],
            rho=float(row["spearman_rank_correlation"]),
            status=row["status"],
            top1=str(bool(row["top1_agreement"])).lower(),
        )
        for row in rows
    )
    lines.extend(
        [
            "",
            (
                "通过仅表示 oracle 方法在本次全新 development qualification 上合格; "
                "不恢复历史 W2-51, 也不授权 participant/formal execution。"
            ),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    scheduled_clusters = [
        {"task_id": str(task_id), "world_seed": int(world_seed)}
        for task_id, _ in tasks
        for world_seed in worlds
    ]
    fit_strategy = str(
        protocol["artifact_contract"].get("oracle_fit_strategy", "disjoint_conditional_cubic_ridge")
    )
    oracle_version = str(protocol["artifact_contract"].get("oracle_version", "v0.4"))
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
        neighborhood_count = int(grid_contract["candidate_neighborhood_query_count_per_task"])
        oversampling = int(grid_contract["compile_valid_oversampling_factor"])
        proposed_grid = build_hybrid_disjoint_oracle_grid(
            registered,
            allowed_feature_ids=feature_ids,
            allowed_metric_ids=metric_ids,
            candidate_query_ids=candidate_ids,
            global_query_count=global_count * oversampling,
            neighborhood_query_count=neighborhood_count * oversampling,
            neighborhood_span_fraction=float(grid_contract["candidate_neighborhood_span_fraction"]),
            # Compact IDs keep Windows trajectory paths below MAX_PATH. The task-index prefix is
            # stable under the frozen protocol order and remains unique within this study.
            grid_id=f"e2a-o-t{task_index + 1}",
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
            if fit_strategy in {
                "disjoint_knn4_candidate_location_calibrated_conditional_cubic_ridge",
                "disjoint_knn4_candidate_domain_exact_typed_law_distillation",
                "disjoint_extra_trees_candidate_domain_exact_typed_law_distillation",
            }:
                registered_report = _grid_report(
                    task_id=task_id,
                    world_seed=world_seed,
                    source=source,
                    grid=[deepcopy(dict(query)) for query in registered],
                    output_root=output_root / "registered-truth",
                    progress=progress,
                    workers=int(args.workers),
                    shard_count=min(int(args.shards), len(registered)),
                )
                all_registered_truth = {
                    str(key): dict(value) for key, value in registered_report["truth"].items()
                }
            else:
                retained_task_root = candidate_root / task_id / f"seed-{world_seed}" / task_id
                all_registered_truth = {
                    **_truth(retained_task_root / "candidate-truth/report.json"),
                    **_truth(retained_task_root / "checkpoint-truth/report.json"),
                }
                registered_report = None
            if len(all_registered_truth) != 16 or not set(candidate_ids).issubset(
                all_registered_truth
            ):
                raise ValueError(f"{task_id}/seed-{world_seed}: registered truth identity differs")
            candidate_truth = {
                query_id: all_registered_truth[query_id] for query_id in candidate_ids
            }
            candidate_qualification = evaluate_candidate_packet(
                candidate_truth,
                protocol["candidate_contract"],
            )
            if fit_strategy == (
                "disjoint_knn4_candidate_location_calibrated_conditional_cubic_ridge"
            ):
                artifact = fit_candidate_calibrated_oracle_law_from_disjoint_grid(
                    grid,
                    fit_truth,
                    candidate_queries=candidates,
                    allowed_feature_ids=feature_ids,
                    allowed_metric_ids=metric_ids,
                    summary_id=f"oracle-v0.2--{task_id}--seed{world_seed}",
                    neighbor_count=int(
                        protocol["artifact_contract"]["oracle_candidate_calibration_neighbor_count"]
                    ),
                    candidate_calibration_weight=float(
                        protocol["artifact_contract"]["oracle_candidate_calibration_weight"]
                    ),
                )
            elif fit_strategy == ("disjoint_knn4_candidate_domain_exact_typed_law_distillation"):
                artifact = fit_candidate_domain_distilled_oracle_law_from_disjoint_grid(
                    grid,
                    fit_truth,
                    candidate_queries=candidates,
                    allowed_feature_ids=feature_ids,
                    allowed_metric_ids=metric_ids,
                    summary_id=f"oracle-v0.3--{task_id}--seed{world_seed}",
                    neighbor_count=int(
                        protocol["artifact_contract"]["oracle_candidate_calibration_neighbor_count"]
                    ),
                    distillation_tolerance=float(
                        protocol["artifact_contract"]["oracle_candidate_distillation_tolerance"]
                    ),
                )
            elif fit_strategy == (
                "disjoint_extra_trees_candidate_domain_exact_typed_law_distillation"
            ):
                artifact = fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid(
                    grid,
                    fit_truth,
                    candidate_queries=candidates,
                    allowed_feature_ids=feature_ids,
                    allowed_metric_ids=metric_ids,
                    summary_id=f"oracle-{oracle_version}--{task_id}--seed{world_seed}",
                    tree_count=int(
                        protocol["artifact_contract"]["oracle_candidate_predictor_tree_count"]
                    ),
                    min_samples_leaf=int(
                        protocol["artifact_contract"]["oracle_candidate_predictor_min_samples_leaf"]
                    ),
                    random_seed=int(
                        protocol["artifact_contract"]["oracle_candidate_predictor_random_seed"]
                    ),
                    distillation_tolerance=float(
                        protocol["artifact_contract"]["oracle_candidate_distillation_tolerance"]
                    ),
                )
            else:
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
                    "candidate_status": candidate_qualification["status"],
                    "candidate_qualification": candidate_qualification,
                    "registered_truth_query_count": (
                        int(registered_report["truth_query_count"])
                        if registered_report is not None
                        else len(all_registered_truth)
                    ),
                    "registered_exact_replay_query_count": (
                        int(registered_report["exact_replay_query_count"])
                        if registered_report is not None
                        else None
                    ),
                    "grid_exact_replay_query_count": int(
                        report.get("exact_replay_query_count", len(fit_truth))
                    ),
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
                    "spearman_rank_correlation": qualification["spearman_rank_correlation"],
                }
            )
            if qualification["status"] != "passed" or candidate_qualification["status"] != "passed":
                summary = _qualification_summary(
                    protocol=protocol,
                    fit_strategy=fit_strategy,
                    rows=rows,
                    scheduled_clusters=scheduled_clusters,
                )
                write_json_atomic(output_root / "summary.json", summary)
                _write_readable_summary(output_root / "REPORT_ZH.md", summary)
                print(json.dumps(summary, ensure_ascii=False, indent=2))
                return 2

    summary = _qualification_summary(
        protocol=protocol,
        fit_strategy=fit_strategy,
        rows=rows,
        scheduled_clusters=scheduled_clusters,
    )
    write_json_atomic(output_root / "summary.json", summary)
    _write_readable_summary(output_root / "REPORT_ZH.md", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
