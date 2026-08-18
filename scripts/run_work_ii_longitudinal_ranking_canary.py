#!/usr/bin/env python3
"""Prepare and run the true twelve-round ranking-only longitudinal canary."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_campaign_pilot import (
    _checkpoint_contract,
    _qualification,
    _required_operation_counts,
)
from work_ii_longitudinal_runtime import (
    LAW_EVALUATION_CONTRACT,
    Progress,
    _execute_cells,
    _law_evaluation,
)

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import (
    ARMS,
    _checkpoint_action_hashes,
    _world_campaign_config,
    build_terminal_contract,
    evaluate_terminal_readout,
    summarize_results,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    AGENT_INVALID_ENFORCEMENT_POLICY,
    PROVIDER_ERROR_ENFORCEMENT_POLICY,
)
from chemworld.eval.work_ii_reviewer_followup import build_b3_candidate_queries
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_as_longitudinal_ranking_canary_v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT / "runs/development/work-ii-as-longitudinal-ranking-canary-v0.1"
)
PROTOCOL_VERSION = "chemworld-work-ii-as-longitudinal-ranking-canary-protocol-0.1"
MANIFEST_VERSION = "chemworld-work-ii-as-longitudinal-ranking-canary-manifest-0.1"


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


def load_canary_protocol(path: Path) -> dict[str, Any]:
    protocol = _load(path)
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        raise ValueError("unsupported longitudinal ranking canary protocol")
    if protocol.get("arms") != list(ARMS):
        raise ValueError("longitudinal ranking canary arm order drifted")
    if protocol.get("campaign_complete_experiments") != 12:
        raise ValueError("longitudinal ranking canary requires twelve experiments")
    if protocol.get("checkpoint_complete_experiments") != [0, 3, 6, 9, 12]:
        raise ValueError("longitudinal ranking canary checkpoint schedule drifted")
    if protocol.get("prediction_mode") != "ranking_only":
        raise ValueError("longitudinal ranking canary must use ranking-only mode")
    if protocol.get("candidate_count") != 8:
        raise ValueError("longitudinal ranking canary requires eight candidates")
    return protocol


def prepare_canary(
    protocol_path: Path,
    *,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    protocol = load_canary_protocol(protocol_path)
    output_root.mkdir(parents=True, exist_ok=True)
    runtime = _load(_resolve(ROOT, protocol["runtime_config"], field="runtime_config"))
    if runtime.get("campaign", {}).get("complete_experiments") != 12:
        raise ValueError("runtime does not implement a twelve-experiment campaign")
    if runtime.get("campaign", {}).get("checkpoint_complete_experiments") != [0, 3, 6, 9, 12]:
        raise ValueError("runtime checkpoint schedule differs from the canary")
    source_manifest = _load(
        _resolve(ROOT, protocol["source_b4_manifest"], field="source_b4_manifest")
    )
    source_truth_manifest = _load(
        _resolve(
            ROOT,
            protocol["source_b4_truth_manifest"],
            field="source_b4_truth_manifest",
        )
    )
    seed = int(protocol["world_seed"])
    source_cells = [
        cell
        for cell in source_manifest.get("cells", [])
        if isinstance(cell, dict) and int(cell.get("world_seed", -1)) == seed
    ]
    if len(source_cells) != 3 or {str(cell.get("arm")) for cell in source_cells} != set(ARMS):
        raise ValueError("source B4 manifest lacks one complete three-arm world")
    source_cell = next(cell for cell in source_cells if cell["arm"] == "opaque")
    public_candidates = source_cell["public_packet"]["unseen_action_candidates"]
    candidate_ids = [str(item["query_id"]) for item in public_candidates]
    if len(candidate_ids) != 8 or len(set(candidate_ids)) != 8:
        raise ValueError("source B4 candidate packet is invalid")
    grid_protocol = _load(
        _resolve(ROOT, protocol["candidate_grid_source"], field="candidate_grid_source")
    )
    candidate_by_id = {
        str(item["query_id"]): item for item in build_b3_candidate_queries(grid_protocol)
    }
    if any(query_id not in candidate_by_id for query_id in candidate_ids):
        raise ValueError("source B4 candidate lies outside the current action grid")
    candidate_queries = [candidate_by_id[query_id] for query_id in candidate_ids]
    contract = build_terminal_contract(
        study_id=str(protocol["study_id"]),
        world_seed=seed,
        candidates=candidate_queries,
        prediction_mode="ranking_only",
    )
    config = _world_campaign_config(
        runtime,
        study_id=str(protocol["study_id"]),
        world_seed=seed,
        terminal_contract=contract,
    )
    config_path = output_root / "campaign-config.json"
    write_json_atomic(config_path, config)

    cluster_id = f"A_S_LRC--partition-discovery--seed{seed}"
    checkpoint_plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": cluster_id,
            "task_id": "partition-discovery",
            "world_seed": seed,
        },
        runtime,
        formal_result=False,
        formal_preflight_sha256=None,
    )
    plan_errors = validate_evaluator_truth_plan(checkpoint_plan)
    if plan_errors:
        raise ValueError("invalid checkpoint truth plan: " + "; ".join(plan_errors))
    checkpoint_root = output_root / "checkpoint-truth" / cluster_id
    if checkpoint_root.exists():
        checkpoint_report = _load(checkpoint_root / "report.json")
    else:
        checkpoint_report = execute_evaluator_truth_plan(
            checkpoint_plan,
            runtime,
            checkpoint_root,
        )
    report_errors = validate_evaluator_truth_report(checkpoint_report, checkpoint_plan)
    if report_errors or checkpoint_report.get("status") != "completed":
        raise ValueError(
            "invalid checkpoint truth report: "
            + ("; ".join(report_errors) or str(checkpoint_report.get("status")))
        )
    progress.emit(
        {
            "stage": "longitudinal_ranking_checkpoint_truth_complete",
            "completed_queries": len(checkpoint_plan["queries"]),
            "total_queries": len(checkpoint_plan["queries"]),
            "exact_replay_queries": len(checkpoint_plan["queries"]),
        }
    )
    checkpoint_hashes = _checkpoint_action_hashes(runtime)
    candidate_plans = {
        query_id: compile_evaluator_truth_query(runtime, candidate_by_id[query_id])
        for query_id in candidate_ids
    }
    if checkpoint_hashes.intersection(
        str(plan["action_plan_sha256"]) for plan in candidate_plans.values()
    ):
        raise ValueError("terminal candidate collides with a checkpoint truth query")

    source_world = next(
        world
        for world in source_truth_manifest.get("worlds", [])
        if isinstance(world, dict) and int(world.get("world_seed", -1)) == seed
    )
    pool_ranks = {
        str(item["query"]["query_id"]): int(item["pool_rank"])
        for item in source_world["selected_actions"]
    }
    candidate_truth = deepcopy(dict(source_cell["scoring_truth"]))
    presented_ranks = deepcopy(dict(source_cell["hidden_action_ranks"]))
    action_hashes = {
        query_id: str(candidate_plans[query_id]["action_plan_sha256"])
        for query_id in candidate_ids
    }
    cells = [
        {
            "cell_id": f"{cluster_id}--{arm}",
            "cluster_id": cluster_id,
            "world_seed": seed,
            "arm": arm,
            "campaign_config_path": config_path.relative_to(output_root).as_posix(),
            "terminal_action_readout": deepcopy(contract),
            "candidate_truth": deepcopy(candidate_truth),
            "presented_candidate_ranks": deepcopy(presented_ranks),
            "candidate_pool_ranks": deepcopy(pool_ranks),
            "candidate_action_plan_sha256": deepcopy(action_hashes),
            "checkpoint_truth_plan": deepcopy(checkpoint_plan),
            "checkpoint_truth": deepcopy(dict(checkpoint_report["truth"])),
        }
        for arm in ARMS
    ]
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_VERSION,
        "study_id": protocol["study_id"],
        "status": "prepared_development_provider_execution_authorized",
        "protocol_sha256": canonical_json_sha256(protocol),
        "source_b4_manifest_sha256": source_manifest.get("manifest_sha256"),
        "source_b4_truth_manifest_sha256": source_truth_manifest.get(
            "truth_manifest_sha256"
        ),
        "world_seed": seed,
        "cluster_count": 1,
        "cell_count": 3,
        "campaign_experiment_count_per_cell": 12,
        "participant_physical_experiment_count": 36,
        "prediction_mode": "ranking_only",
        "terminal_prediction_term_count_per_cell": 0,
        "checkpoint_truth_execution_count": len(checkpoint_plan["queries"]),
        "checkpoint_exact_replay_count": len(checkpoint_plan["queries"]),
        "provider_execution_authorized": True,
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    return manifest


def _write_report(summary: dict[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S 12-round longitudinal ranking-only canary",
        "",
        f"合格 {summary['eligible_cell_count']}/{summary['scheduled_cell_count']} cells。",
        "",
        "| arm | eligible | experiments | selected rank | Top-1 | regret | law MAE |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(summary["cell_rows"], key=lambda item: str(item.get("arm"))):
        lines.append(
            f"| {row.get('arm')} | "
            f"{int(row.get('status') == 'completed_uncontaminated')} | "
            f"{row.get('campaign_complete_experiment_count')} | "
            f"{row.get('selected_rank')} | {int(row.get('top1_selected') is True)} | "
            f"{row.get('normalized_regret')} | {row.get('law_normalized_mae')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _requalify_campaign_summary(
    cell: Mapping[str, Any],
    config: Mapping[str, Any],
    campaign_summary: Mapping[str, Any],
) -> dict[str, Any]:
    recovered = deepcopy(dict(campaign_summary))
    qualification = _qualification(
        analysis=recovered.get("analysis", {}),
        exact_replay=recovered.get("exact_replay", {}),
        method_resources=recovered.get("method_resources", {}),
        method_resource_limits=config["method_resources"],
        receipts=recovered.get("provider_receipts", []),
        process_time_limit_s=float(config["campaign"]["process_time_limit_s"]),
        required_operation_counts=_required_operation_counts(config),
        required_snapshot_stages=list(
            _checkpoint_contract(config, str(cell["arm"]))["snapshot_stages"]
        ),
        operational_limits=config["provider"],
        max_resource_rejections=int(
            config.get("qualification", {}).get("max_resource_rejections", 0)
        ),
        minimum_unique_recipes=int(
            config.get("qualification", {}).get("minimum_unique_recipes", 0)
        ),
        maximum_exact_repeats=(
            int(config["qualification"]["maximum_exact_repeats"])
            if config.get("qualification", {}).get("maximum_exact_repeats") is not None
            else None
        ),
        agent_invalid_enforcement=AGENT_INVALID_ENFORCEMENT_POLICY,
        provider_error_enforcement=PROVIDER_ERROR_ENFORCEMENT_POLICY,
        unlimited_provider_continuations=True,
        terminal_action_readout_required=True,
        terminal_action_prediction_mode=str(
            cell["terminal_action_readout"].get("prediction_mode", "full_metrics")
        ),
    )
    recovered["qualification"] = qualification
    recovered["completed"] = recovered.get("failure") is None and qualification["passed"]
    recovered["law_summary_evaluation"] = _law_evaluation(cell, recovered)
    return recovered


def recover_canary_analysis(
    manifest: Mapping[str, Any],
    *,
    output_root: Path,
) -> list[dict[str, Any]]:
    config = _load(output_root / "campaign-config.json")
    source_by_id = {
        str(row["cell_id"]): row
        for path in sorted((output_root / "canary" / "cells").glob("*.json"))
        for row in [_load(path)]
    }
    recovered_root = output_root / "recovered-analysis"
    results: list[dict[str, Any]] = []
    for cell in manifest["cells"]:
        cell_id = str(cell["cell_id"])
        source = source_by_id.get(cell_id)
        if source is None:
            raise ValueError(f"missing retained canary result for {cell_id}")
        campaign_summary = source.get("campaign_summary")
        if not isinstance(campaign_summary, Mapping):
            raise ValueError(f"retained canary result lacks campaign summary for {cell_id}")
        recovered_campaign = _requalify_campaign_summary(cell, config, campaign_summary)
        action = evaluate_terminal_readout(
            cell,
            recovered_campaign,
            maximum_adequate_law_normalized_mae=float(
                LAW_EVALUATION_CONTRACT["maximum_adequate_law_normalized_mae"]
            ),
        )
        result: dict[str, Any] = {
            "schema_version": source.get("schema_version"),
            "cell_id": cell_id,
            "cluster_id": cell["cluster_id"],
            "world_seed": cell["world_seed"],
            "arm": cell["arm"],
            "phase": "recovered-analysis",
            "terminal_action_contract_sha256": cell["terminal_action_readout"][
                "contract_sha256"
            ],
            "source_result_sha256": source.get("result_sha256"),
            "recovery_reason": (
                "ranking-only recommendation was previously evaluated by the "
                "full-metrics qualification branch"
            ),
            "campaign_summary": recovered_campaign,
            **action,
            "elapsed_s": source.get("elapsed_s"),
        }
        result["result_sha256"] = canonical_json_sha256(result)
        write_json_atomic(recovered_root / "cells" / f"{cell_id}.json", result)
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not any((args.prepare, args.execute, args.analyze)):
        parser.error("select --prepare, --execute, or --analyze")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    protocol = load_canary_protocol(protocol_path)
    output = args.output_root.resolve()
    progress = Progress(output / "progress.jsonl")
    manifest_path = output / "input_manifest.json"
    if args.prepare or not manifest_path.is_file():
        manifest = prepare_canary(protocol_path, output_root=output, progress=progress)
    else:
        manifest = _load(manifest_path)
    if args.prepare and not args.execute and not args.analyze:
        return 0
    if args.execute:
        if (
            protocol.get("provider_execution_authorized") is not True
            or not args.allow_provider_execution
        ):
            raise RuntimeError(
                "provider execution requires protocol authorization and "
                "--allow-provider-execution"
            )
        results = _execute_cells(
            manifest["cells"],
            output_root=output,
            phase="canary",
            workers=args.workers,
            progress=progress,
        )
        summary = summarize_results(results)
        summary["study_id"] = protocol["study_id"]
        summary["interpretation_status"] = "development_one_exposed_world_only"
        summary["all_scheduled_records_retained"] = len(results) == 3
        summary["summary_sha256"] = canonical_json_sha256(
            {key: value for key, value in summary.items() if key != "summary_sha256"}
        )
        write_json_atomic(output / "summary.json", summary)
        _write_report(summary, output / "REPORT_ZH.md")
    if args.analyze and not args.execute:
        results = recover_canary_analysis(manifest, output_root=output)
        summary = summarize_results(results)
        summary["study_id"] = protocol["study_id"]
        summary["interpretation_status"] = "development_one_exposed_world_only"
        summary["all_scheduled_records_retained"] = len(results) == 3
        summary["summary_sha256"] = canonical_json_sha256(
            {key: value for key, value in summary.items() if key != "summary_sha256"}
        )
        write_json_atomic(output / "recovered-analysis" / "summary.json", summary)
        _write_report(summary, output / "recovered-analysis" / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
