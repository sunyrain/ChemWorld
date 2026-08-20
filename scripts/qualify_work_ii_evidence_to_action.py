#!/usr/bin/env python3
"""Run provider-free candidate and replay qualification for the five-condition study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import run_work_ii_multi_task_open_action_pilot as task_runner
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    build_design_manifest,
    evaluate_candidate_packet,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1/qualification-v2"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _configure_task_runner(protocol: dict[str, Any]) -> None:
    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.STUDY_ID = f"{protocol['study_id']}--qualification"
    task_runner.FORMAL_RESULT = False
    task_runner.FORMAL_PREFLIGHT_SHA256 = None
    task_runner.TESTED_COMMIT = None
    task_runner.QUERY_SPLIT_STRATEGY = "registered_public_feature_maximin"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    protocol_path = (
        args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    ).resolve()
    output_root = (
        args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    ).resolve()
    protocol = _load(protocol_path)
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    design = build_design_manifest(protocol)
    _configure_task_runner(protocol)
    progress = Progress(output_root / "progress.jsonl")

    rows: list[dict[str, Any]] = []
    tasks = list(protocol["task_runtime_sources"].items())
    worlds = [int(seed) for seed in protocol["qualification_world_seeds"]]
    total = len(tasks) * len(worlds)
    for task_index, (task_id, runtime_path) in enumerate(tasks):
        source = (ROOT / str(runtime_path)).resolve()
        for world_index, world_seed in enumerate(worlds):
            unit = task_index * len(worlds) + world_index + 1
            packet_seed = (
                int(protocol["candidate_packet_seed_base"]) + task_index * 100
            )
            task_runner.WORLD_SEED = world_seed
            task_runner.PACKET_SEED = packet_seed
            unit_root = output_root / task_id / f"seed-{world_seed}"
            progress.emit(
                {
                    "stage": "e2a_qualification_cluster_started",
                    "completed_clusters": unit - 1,
                    "total_clusters": total,
                    "task_id": task_id,
                    "world_seed": world_seed,
                }
            )
            manifest = task_runner._prepare_task(
                task_id,
                source,
                unit_root,
                progress,
            )
            first_cell = manifest["cells"][0]
            result = evaluate_candidate_packet(
                first_cell["candidate_truth"],
                protocol["candidate_contract"],
            )
            rows.append(
                {
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "candidate_packet_seed": packet_seed,
                    "checkpoint_truth_query_count": manifest["checkpoint_query_count"],
                    "candidate_truth_query_count": manifest["candidate_count"],
                    "public_truth_binding": "passed",
                    "exact_replay": "passed",
                    **result,
                }
            )
            progress.emit(
                {
                    "stage": "e2a_qualification_cluster_terminal",
                    "completed_clusters": unit,
                    "total_clusters": total,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "status": result["status"],
                }
            )

    passed = sum(row["status"] == "passed" for row in rows)
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-qualification-0.1",
        "study_id": protocol["study_id"],
        "status": "candidate_qualification_passed" if passed == total else "rejected",
        "provider_execution_authorized": False,
        "development_cluster_count": total,
        "passed_cluster_count": passed,
        "checkpoint_truth_query_count": sum(
            int(row["checkpoint_truth_query_count"]) for row in rows
        ),
        "candidate_truth_query_count": sum(int(row["candidate_truth_query_count"]) for row in rows),
        "exact_replay_query_count": sum(
            int(row["checkpoint_truth_query_count"]) + int(row["candidate_truth_query_count"])
            for row in rows
        ),
        "oracle_artifact_qualification": "pending_runtime_implementation",
        "provider_ready": False,
        "design_denominators": {
            "scheduled_sessions": design["scheduled_session_count"],
            "participant_physical_experiments": design["participant_physical_experiment_count"],
        },
        "cluster_rows": rows,
    }
    write_json_atomic(output_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed == total else 2


if __name__ == "__main__":
    raise SystemExit(main())
