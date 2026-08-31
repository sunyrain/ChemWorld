#!/usr/bin/env python3
"""Prepare and execute the fresh five-world, three-task open-action matrix."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import run_work_ii_multi_task_open_action_pilot as task_runner
from work_ii_longitudinal_runtime import Progress, _execute_cells

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import summarize_results

ROOT = Path(__file__).resolve().parents[1]
STUDY_ID = "work-ii-deepseek-multi-task-open-action-five-world-v0.1"
WORLD_SEEDS = (0, 1, 2, 3, 4)
TASK_IDS = tuple(task_runner.TASKS)
CELL_COUNT = len(WORLD_SEEDS) * len(TASK_IDS) * 3
DEFAULT_OUTPUT = (
    ROOT
    / "runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817"
)
GPT_RUNTIME_ROOT = ROOT / "configs/benchmark/work_ii_c2_gpt56_sol_medium_runtime_v0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _configure_formal_runtime(
    preflight_sha256: str, tested_commit: str, *, participant: str
) -> None:
    if len(preflight_sha256) != 64:
        raise ValueError("formal preflight binding must contain 64 hexadecimal characters")
    int(preflight_sha256, 16)
    if participant not in {"deepseek", "openai"}:
        raise ValueError("unsupported open-action participant")
    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.RUNTIME_ROOT = (
        task_runner.ROOT
        / "workstreams/flagship_tasks/reports/work-ii-w2-26-deepseek-runtime-configs-v0.1"
        if participant == "deepseek"
        else GPT_RUNTIME_ROOT
    )
    task_runner.STUDY_ID = (
        STUDY_ID
        if participant == "deepseek"
        else "work-ii-gpt56-sol-medium-multi-task-open-action-five-world-v0.1"
    )
    task_runner.FORMAL_RESULT = True
    task_runner.FORMAL_PREFLIGHT_SHA256 = preflight_sha256
    task_runner.TESTED_COMMIT = tested_commit


def prepare_matrix(
    output_root: Path,
    *,
    preflight_sha256: str,
    tested_commit: str,
    participant: str,
    progress: Progress,
) -> dict[str, Any]:
    _configure_formal_runtime(
        preflight_sha256, tested_commit, participant=participant
    )
    cells: list[dict[str, Any]] = []
    clusters: list[dict[str, Any]] = []
    cluster_index = 0
    for task_id in TASK_IDS:
        source = task_runner.RUNTIME_ROOT / task_runner.TASKS[task_id]
        for world_seed in WORLD_SEEDS:
            cluster_index += 1
            task_runner.WORLD_SEED = world_seed
            cluster_root = output_root / "clusters" / task_id / f"seed-{world_seed}"
            manifest = task_runner._prepare_task(
                task_id,
                source,
                cluster_root,
                progress,
            )
            task_root = cluster_root / task_id
            prepared_cells: list[dict[str, Any]] = []
            for raw_cell in manifest["cells"]:
                cell = dict(raw_cell)
                cell["campaign_config_path"] = (
                    task_root / str(raw_cell["campaign_config_path"])
                ).relative_to(output_root).as_posix()
                prepared_cells.append(cell)
            cells.extend(prepared_cells)
            clusters.append(
                {
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "cell_ids": [str(cell["cell_id"]) for cell in prepared_cells],
                    "provider_free_truth_query_count": int(
                        manifest["checkpoint_query_count"]
                    )
                    + int(manifest["candidate_count"]),
                }
            )
            progress.emit(
                {
                    "stage": "formal_matrix_cluster_prepared",
                    "cluster": cluster_index,
                    "total_clusters": len(TASK_IDS) * len(WORLD_SEEDS),
                    "task_id": task_id,
                    "world_seed": world_seed,
                }
            )
    manifest = {
        "schema_version": "chemworld-work-ii-multi-task-open-action-formal-matrix-0.1",
        "study_id": task_runner.STUDY_ID,
        "participant": participant,
        "formal_result": True,
        "formal_denominator": True,
        "formal_preflight_sha256": preflight_sha256,
        "tested_commit": tested_commit,
        "tasks": list(TASK_IDS),
        "world_seeds": list(WORLD_SEEDS),
        "arms": list(task_runner.ARMS),
        "cluster_count": len(clusters),
        "cell_count": len(cells),
        "campaign_experiment_count_per_cell": 12,
        "participant_physical_experiment_count": len(cells) * 12,
        "provider_free_truth_query_count": sum(
            int(cluster["provider_free_truth_query_count"]) for cluster in clusters
        ),
        "provider_free_exact_replay_count": sum(
            int(cluster["provider_free_truth_query_count"]) for cluster in clusters
        ),
        "resource_profile": "resource_recovery_v2",
        "operational_canary_cell_ids": clusters[0]["cell_ids"],
        "clusters": clusters,
        "cells": cells,
    }
    if manifest["cell_count"] != CELL_COUNT:
        raise ValueError(f"formal matrix must contain {CELL_COUNT} cells")
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    return manifest


def _load_completed_results(
    output_root: Path,
    cells: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    completed: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    result_root = output_root / "formal" / "cells"
    for raw_cell in cells:
        cell = dict(raw_cell)
        result_path = result_root / f"{cell['cell_id']}.json"
        campaign_path = output_root / "formal" / "campaigns" / str(cell["cell_id"])
        if result_path.is_file():
            result = _load(result_path)
            expected = result.get("result_sha256")
            actual = canonical_json_sha256(
                {key: value for key, value in result.items() if key != "result_sha256"}
            )
            if result.get("cell_id") != cell["cell_id"] or expected != actual:
                raise RuntimeError(f"invalid retained cell result: {result_path}")
            completed.append(result)
        elif campaign_path.exists():
            raise RuntimeError(
                "partial cell has no terminal result; hold for causal inspection: "
                f"{campaign_path}"
            )
        else:
            pending.append(cell)
    return completed, pending


def _write_summary(
    output_root: Path,
    manifest: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    *,
    worker_count: int,
    execution_status: str,
) -> None:
    summary = summarize_results(results)
    summary.update(
        {
            "study_id": manifest["study_id"],
            "formal_result": True,
            "formal_denominator": True,
            "execution_status": execution_status,
            "scheduled_cell_count": manifest["cell_count"],
            "retained_cell_count": len(results),
            "participant_physical_experiment_denominator": manifest[
                "participant_physical_experiment_count"
            ],
            "provider_free_truth_query_count": manifest[
                "provider_free_truth_query_count"
            ],
            "provider_free_exact_replay_count": manifest[
                "provider_free_exact_replay_count"
            ],
            "public_truth_binding_status": "passed",
            "candidate_outcomes_hidden_from_agent": True,
            "candidate_action_plans_public": True,
            "worker_count": worker_count,
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output_root / "summary.json", summary)


def _canary_passed(results: Sequence[Mapping[str, Any]]) -> bool:
    return len(results) == 3 and all(
        result.get("status") == "completed_uncontaminated" for result in results
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute-canary", action="store_true")
    parser.add_argument("--execute-remaining", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--formal-preflight-sha256", required=True)
    parser.add_argument("--tested-commit", required=True)
    parser.add_argument("--participant", choices=("deepseek", "openai"), default="deepseek")
    args = parser.parse_args()
    if not (args.prepare or args.execute_canary or args.execute_remaining):
        parser.error("select --prepare, --execute-canary, or --execute-remaining")
    if not 1 <= args.workers <= 6:
        parser.error("--workers must be between 1 and 6")
    output = (
        args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    ).resolve()
    output.mkdir(parents=True, exist_ok=True)
    progress = Progress(output / "progress.jsonl")
    manifest_path = output / "input_manifest.json"
    if args.prepare:
        if manifest_path.exists():
            raise RuntimeError(f"formal output root already exists: {manifest_path}")
        manifest = prepare_matrix(
            output,
            preflight_sha256=args.formal_preflight_sha256,
            tested_commit=args.tested_commit,
            participant=args.participant,
            progress=progress,
        )
        progress.emit(
            {
                "stage": "formal_matrix_provider_free_preflight_complete",
                "clusters": manifest["cluster_count"],
                "cells": manifest["cell_count"],
                "truth_queries": manifest["provider_free_truth_query_count"],
                "exact_replay_queries": manifest["provider_free_exact_replay_count"],
            }
        )
        if not (args.execute_canary or args.execute_remaining):
            return 0
    else:
        manifest = _load(manifest_path)
    if (
        manifest.get("formal_preflight_sha256") != args.formal_preflight_sha256
        or manifest.get("tested_commit") != args.tested_commit
        or manifest.get("cell_count") != CELL_COUNT
        or manifest.get("participant", "deepseek") != args.participant
    ):
        raise RuntimeError("formal matrix binding or denominator differs from the launch request")
    if args.execute_canary or args.execute_remaining:
        if not args.allow_provider_execution:
            raise RuntimeError("provider execution requires explicit --allow-provider-execution")
        completed, pending = _load_completed_results(output, manifest["cells"])
        canary_ids = set(manifest["operational_canary_cell_ids"])
        if args.execute_canary:
            selected = [cell for cell in pending if cell["cell_id"] in canary_ids]
            if len(selected) != 3:
                raise RuntimeError("operational canary is not a fresh three-cell cluster")
            new_results = _execute_cells(
                selected,
                output_root=output,
                phase="formal",
                workers=min(3, args.workers),
                progress=progress,
            )
            results = completed + new_results
            status = (
                "canary_passed_hold_for_sampling"
                if _canary_passed(new_results)
                else "canary_failed_hold"
            )
            _write_summary(
                output,
                manifest,
                results,
                worker_count=min(3, args.workers),
                execution_status=status,
            )
            progress.emit(
                {
                    "stage": status,
                    "completed_cells": len(results),
                    "total_cells": CELL_COUNT,
                }
            )
            return 0 if status == "canary_passed_hold_for_sampling" else 2
        canary_results = [result for result in completed if result.get("cell_id") in canary_ids]
        if not _canary_passed(canary_results):
            raise RuntimeError("remaining matrix is held until the three-cell canary passes")
        selected = [cell for cell in pending if cell["cell_id"] not in canary_ids]
        new_results = _execute_cells(
            selected,
            output_root=output,
            phase="formal",
            workers=args.workers,
            progress=progress,
        )
        results = completed + new_results
        status = "completed" if len(results) == CELL_COUNT else "incomplete"
        _write_summary(
            output,
            manifest,
            results,
            worker_count=args.workers,
            execution_status=status,
        )
        progress.emit(
            {
                "stage": f"formal_matrix_{status}",
                "completed_cells": len(results),
                "total_cells": CELL_COUNT,
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
