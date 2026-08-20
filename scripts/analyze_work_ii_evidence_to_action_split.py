#!/usr/bin/env python3
"""Compare the development hash split with a fixed registered alternating split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    evaluate_candidate_packet,
    evaluate_oracle_law_candidate_order,
    fit_oracle_law_from_disjoint_grid,
    split_registered_query_pool_maximin,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
DEFAULT_INPUT = (
    ROOT / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1/qualification-v2"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1"
    / "balanced-split-analysis-v0.1/summary.json"
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    input_root = args.input_root if args.input_root.is_absolute() else ROOT / args.input_root
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    protocol = _load(protocol_path.resolve())
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))

    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for task_id, runtime_path in protocol["task_runtime_sources"].items():
        runtime = _load((ROOT / str(runtime_path)).resolve())
        checkpoint = runtime.get("belief_checkpoint")
        checkpoint = checkpoint if isinstance(checkpoint, dict) else {}
        registered = checkpoint.get("held_out_queries")
        if not isinstance(registered, list):
            raise ValueError(f"{task_id}: registered query pool is missing")
        feature_ids = [str(item) for item in checkpoint.get("allowed_feature_ids", [])]
        candidates, fit_queries = split_registered_query_pool_maximin(
            registered,
            allowed_feature_ids=feature_ids,
        )
        candidate_ids = [str(row["query_id"]) for row in candidates]
        fit_ids = [str(row["query_id"]) for row in fit_queries]
        metric_ids = [str(item) for item in checkpoint.get("allowed_metric_ids", [])]
        if "score" not in metric_ids:
            metric_ids.append("score")
        for world_seed in protocol["qualification_world_seeds"]:
            task_root = input_root / str(task_id) / f"seed-{world_seed}" / str(task_id)
            candidate_report = task_root / "candidate-truth/report.json"
            checkpoint_report = task_root / "checkpoint-truth/report.json"
            if not candidate_report.is_file() or not checkpoint_report.is_file():
                missing.append(f"{task_id}/seed-{world_seed}")
                continue
            all_truth = {**_truth(candidate_report), **_truth(checkpoint_report)}
            if set(all_truth) != {str(row["query_id"]) for row in registered}:
                raise ValueError(f"{task_id}/seed-{world_seed}: 16-query truth set differs")
            selected_truth = {query_id: all_truth[query_id] for query_id in candidate_ids}
            fit_truth = {query_id: all_truth[query_id] for query_id in fit_ids}
            qualification = evaluate_candidate_packet(
                selected_truth,
                protocol["candidate_contract"],
            )
            artifact = fit_oracle_law_from_disjoint_grid(
                fit_queries,
                fit_truth,
                candidate_query_ids=candidate_ids,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                summary_id=f"oracle--{task_id}--seed{world_seed}",
            )
            oracle = evaluate_oracle_law_candidate_order(
                artifact,
                candidate_queries=candidates,
                candidate_truth=selected_truth,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                minimum_rank_correlation=float(
                    protocol["artifact_contract"][
                        "minimum_oracle_candidate_rank_correlation"
                    ]
                ),
            )
            rows.append(
                {
                    "task_id": task_id,
                    "world_seed": int(world_seed),
                    "candidate_query_ids": candidate_ids,
                    **qualification,
                    "oracle_qualification": oracle,
                }
            )

    expected = len(protocol["task_runtime_sources"]) * len(
        protocol["qualification_world_seeds"]
    )
    passed = sum(row["status"] == "passed" for row in rows)
    oracle_passed = sum(
        row["oracle_qualification"]["status"] == "passed" for row in rows
    )
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-balanced-split-analysis-0.1",
        "study_id": protocol["study_id"],
        "selection_rule": (
            "registered_16_query_public_feature_gower_maximin_8_"
            "candidate_remainder_checkpoint"
        ),
        "selection_reads_truth": False,
        "same_candidate_packet_across_worlds_within_task": True,
        "expected_cluster_count": expected,
        "evaluated_cluster_count": len(rows),
        "passed_cluster_count": passed,
        "oracle_passed_cluster_count": oracle_passed,
        "missing_clusters": missing,
        "status": (
            "passed"
            if len(rows) == expected and passed == expected and oracle_passed == expected
            else "failed"
            if len(rows) == expected
            else "incomplete"
        ),
        "provider_execution_authorized": False,
        "cluster_rows": rows,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not args.check_only:
        write_json_atomic(output_path.resolve(), summary)
    return 0 if summary["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
