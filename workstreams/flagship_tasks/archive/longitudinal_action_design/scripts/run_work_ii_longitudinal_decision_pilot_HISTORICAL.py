#!/usr/bin/env python3
"""Historical W2-47 launcher retained for diagnosis; not a current execution entry."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from work_ii_longitudinal_runtime import Progress, _execute_cells

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import (
    ARMS,
    _checkpoint_action_hashes,
    _world_campaign_config,
    build_terminal_contract,
    summarize_results,
)
from chemworld.eval.work_ii_longitudinal_decision import (
    build_candidate_pool,
    build_decision_design,
    candidate_packet_coverage,
    load_decision_protocol,
    select_outcome_blind_packet,
)
from chemworld.eval.work_ii_reviewer_followup import _report_truth, _truth_report
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/work_ii_as_longitudinal_decision_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-as-longitudinal-decision-single-world-seed153150025-v0.1"
)
PILOT_NOTE = (
    "workstreams/flagship_tasks/experiments/"
    "work-ii-as-longitudinal-decision-single-world-3arm-pilot.md"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _resolve(root: Path, value: object, *, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else root / path


def _load_or_execute_truth(
    plan: Mapping[str, Any],
    runtime: Mapping[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    if output_root.exists():
        report = _load(output_root / "report.json")
    else:
        report = execute_evaluator_truth_plan(plan, runtime, output_root)
    errors = validate_evaluator_truth_report(report, plan)
    if errors or report.get("status") != "completed":
        raise ValueError(
            "invalid evaluator truth report: "
            + ("; ".join(errors) or str(report.get("status")))
        )
    return report


def prepare_pilot(
    protocol_path: Path,
    *,
    output_root: Path,
    world_seed: int,
    packet_seed: int,
    progress: Progress,
) -> dict[str, Any]:
    protocol_file, protocol = load_decision_protocol(protocol_path, repository_root=ROOT)
    if world_seed not in protocol["world_seeds"]:
        raise ValueError("pilot world seed is not in the frozen W2-47 roster")
    expected_packet_seed = protocol["candidate_packet_seeds"][
        protocol["world_seeds"].index(world_seed)
    ]
    if packet_seed != expected_packet_seed:
        raise ValueError("pilot packet seed must match the frozen world/packet pairing")

    # Materialize the full design first so the pilot cannot silently diverge from W2-47.
    design = build_decision_design(protocol_path, repository_root=ROOT)
    cluster_id = next(
        cluster["cluster_id"]
        for cluster in design["clusters"]
        if int(cluster["world_seed"]) == world_seed
    )
    runtime = _load(_resolve(ROOT, protocol["runtime_config"], field="runtime_config"))
    pool = build_candidate_pool(protocol)
    packet = select_outcome_blind_packet(
        pool,
        packet_seed=packet_seed,
        namespace=str(protocol["candidate_packet_namespace"]),
    )
    if candidate_packet_coverage(packet) != {
        "candidate_count": 8,
        "distinct_pair_count": 8,
        "volume_index_counts": {0: 2, 1: 2, 2: 2, 3: 2},
        "mixing_index_counts": {0: 4, 1: 4},
    }:
        raise ValueError("pilot candidate packet coverage is invalid")
    checkpoint_hashes = _checkpoint_action_hashes(runtime)
    candidate_plans = {
        str(query["query_id"]): compile_evaluator_truth_query(runtime, query)
        for query in packet
    }
    if checkpoint_hashes.intersection(
        str(plan["action_plan_sha256"]) for plan in candidate_plans.values()
    ):
        raise ValueError("pilot candidate collides with a checkpoint truth action plan")

    contract = build_terminal_contract(
        study_id=str(protocol["study_id"]),
        world_seed=world_seed,
        candidates=packet,
        prediction_mode="ranking_only",
    )
    campaign_config = _world_campaign_config(
        runtime,
        study_id=str(protocol["study_id"]),
        world_seed=world_seed,
        terminal_contract=contract,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    config_path = output_root / "campaign-config.json"
    write_json_atomic(config_path, campaign_config)

    checkpoint_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": "partition-discovery",
            "world_seed": world_seed,
        },
        campaign_config,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    plan_errors = validate_evaluator_truth_plan(checkpoint_plan)
    if plan_errors:
        raise ValueError("invalid checkpoint truth plan: " + "; ".join(plan_errors))
    checkpoint_root = output_root / "checkpoint-truth" / cluster_id
    checkpoint_report = _load_or_execute_truth(
        checkpoint_plan, campaign_config, checkpoint_root
    )
    progress.emit(
        {
            "stage": "pilot_checkpoint_truth_complete",
            "world_seed": world_seed,
            "completed_queries": len(checkpoint_plan["queries"]),
            "total_queries": len(checkpoint_plan["queries"]),
            "exact_replay_queries": len(checkpoint_plan["queries"]),
        }
    )

    candidate_root = output_root / "candidate-truth" / cluster_id
    candidate_report = _truth_report(
        runtime=runtime,
        queries=packet,
        exponent=1.75,
        world_seed=world_seed,
        cluster_id=cluster_id,
        output_root=candidate_root,
        liveness=lambda elapsed_s: progress.emit(
            {
                "stage": "pilot_candidate_truth_liveness",
                "world_seed": world_seed,
                "query_count": len(packet),
                "elapsed_s": elapsed_s,
            }
        ),
    )
    candidate_truth = _report_truth(candidate_report)
    if len(candidate_truth) != 8:
        raise ValueError("pilot candidate truth denominator differs from eight")
    progress.emit(
        {
            "stage": "pilot_candidate_truth_complete",
            "world_seed": world_seed,
            "completed_queries": len(candidate_truth),
            "total_queries": len(packet),
            "exact_replay_queries": len(candidate_truth),
        }
    )

    presented_ranks = {
        query_id: rank
        for rank, query_id in enumerate(
            sorted(
                candidate_truth,
                key=lambda query_id: (-float(candidate_truth[query_id]["score"]), query_id),
            ),
            start=1,
        )
    }
    action_hashes = {
        query_id: str(plan["action_plan_sha256"])
        for query_id, plan in candidate_plans.items()
    }
    cells = [
        {
            "cell_id": f"{cluster_id}--{arm}",
            "cluster_id": cluster_id,
            "world_seed": world_seed,
            "arm": arm,
            "campaign_config_path": config_path.relative_to(output_root).as_posix(),
            "terminal_action_readout": deepcopy(contract),
            "candidate_truth": deepcopy(candidate_truth),
            "presented_candidate_ranks": deepcopy(presented_ranks),
            "candidate_action_plan_sha256": deepcopy(action_hashes),
            "checkpoint_truth_plan": deepcopy(checkpoint_plan),
            "checkpoint_truth": deepcopy(dict(checkpoint_report["truth"])),
        }
        for arm in ARMS
    ]
    manifest: dict[str, Any] = {
        "schema_version": (
            "chemworld-work-ii-as-longitudinal-decision-single-world-"
            "pilot-manifest-0.1"
        ),
        "study_id": protocol["study_id"],
        "pilot_note": PILOT_NOTE,
        "status": "prepared_development_provider_execution_not_authorized",
        "protocol_path": protocol_file.relative_to(ROOT).as_posix(),
        "protocol_sha256": canonical_json_sha256(protocol),
        "design_sha256": design["design_sha256"],
        "world_seed": world_seed,
        "candidate_packet_seed": packet_seed,
        "cluster_id": cluster_id,
        "arm_count": 3,
        "cell_count": 3,
        "campaign_experiment_count_per_cell": 12,
        "participant_physical_experiment_count": 36,
        "candidate_count": 8,
        "candidate_truth_execution_count": 8,
        "checkpoint_truth_execution_count": 16,
        "provider_free_truth_execution_count": 24,
        "provider_free_exact_replay_count": 24,
        "prediction_mode": "ranking_only",
        "candidate_packet": deepcopy(packet),
        "candidate_packet_coverage": candidate_packet_coverage(packet),
        "candidate_selection_uses_hidden_truth": False,
        "candidate_selection_uses_hidden_rank": False,
        "provider_execution_authorized": False,
        "pilot_provider_execution_scope": "one_world_three_arm_development_only",
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    return manifest


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S 单 world 三臂 12 轮 development pilot",
        "",
        f"完成资格: {summary['eligible_cell_count']}/{summary['scheduled_cell_count']} cells",
        "",
        "| arm | status | experiments | selected rank | Top-1 | normalized regret | "
        "law MAE | overlap |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(summary["cell_rows"], key=lambda item: str(item.get("arm"))):
        lines.append(
            f"| {row.get('arm')} | {row.get('status')} | "
            f"{row.get('campaign_complete_experiment_count')} | "
            f"{row.get('selected_rank')} | {int(row.get('top1_selected') is True)} | "
            f"{row.get('normalized_regret')} | {row.get('law_normalized_mae')} | "
            f"{row.get('candidate_overlap_count')} |"
        )
    lines.extend(
        [
            "",
            "解释边界: 这是单 world development pilot, 不进入 W2-47 正式分母, "
            "也不支持跨 world 推断。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _finalize_output(manifest: Mapping[str, Any], output: Path) -> dict[str, Any]:
    cells_root = output / "provider" / "cells"
    cells = []
    for cell in manifest["cells"]:
        cell_id = str(cell["cell_id"])
        path = cells_root / f"{cell_id}.json"
        if not path.is_file():
            raise FileNotFoundError(f"missing retained provider cell result: {path}")
        cells.append(_load(path))
    if len(cells) != int(manifest["cell_count"]):
        raise ValueError("retained provider cell denominator differs from pilot manifest")
    summary = summarize_results(cells)
    summary.update(
        {
            "study_id": manifest["study_id"],
            "pilot_scope": manifest["pilot_provider_execution_scope"],
            "world_seed": manifest["world_seed"],
            "candidate_packet_seed": manifest["candidate_packet_seed"],
            "candidate_truth_execution_count": manifest["candidate_truth_execution_count"],
            "checkpoint_truth_execution_count": manifest["checkpoint_truth_execution_count"],
            "provider_free_truth_execution_count": manifest["provider_free_truth_execution_count"],
            "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
            "all_scheduled_records_retained": len(cells) == int(manifest["cell_count"]),
            "interpretation_status": "development_one_world_only",
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output / "summary.json", summary)
    _write_report(summary, output / "REPORT_ZH.md")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--world-seed", type=int, default=153150025)
    parser.add_argument("--packet-seed", type=int, default=400)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not any((args.prepare, args.execute, args.finalize)):
        parser.error("select --prepare, --execute, or --finalize")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
    output = args.output_root.resolve()
    progress = Progress(output / "progress.jsonl")
    manifest_path = output / "input_manifest.json"
    if args.prepare or not manifest_path.is_file():
        manifest = prepare_pilot(
            args.protocol.resolve(),
            output_root=output,
            world_seed=args.world_seed,
            packet_seed=args.packet_seed,
            progress=progress,
        )
    else:
        manifest = _load(manifest_path)
    if args.prepare and not args.execute:
        return 0
    if args.finalize:
        _finalize_output(manifest, output)
        return 0
    if manifest.get("status") != "prepared_development_provider_execution_not_authorized":
        raise RuntimeError("pilot manifest is not a prepared development manifest")
    if not args.allow_provider_execution:
        raise RuntimeError(
            "provider execution requires the explicit --allow-provider-execution pilot switch"
        )
    if (output / "provider").exists():
        raise FileExistsError("refusing to overwrite an existing provider pilot phase")
    results = _execute_cells(
        manifest["cells"],
        output_root=output,
        phase="provider",
        workers=args.workers,
        progress=progress,
    )
    del results
    _finalize_output(manifest, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
