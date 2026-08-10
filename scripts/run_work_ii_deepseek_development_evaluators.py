#!/usr/bin/env python3
"""Evaluate retained DeepSeek Work II development trajectories without provider calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_analysis import score_cell_checkpoint_errors
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    execute_blind_evaluation_plan,
    validate_blind_evaluation_report,
)
from chemworld.eval.work_ii_development_confirmation import (
    build_cluster_rows,
    build_confirmation_summary,
    build_development_confirmation_preflight,
    collect_development_cells,
)
from chemworld.eval.work_ii_formal import EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT
from chemworld.eval.work_ii_law_summary import evaluate_final_law_summary
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = ROOT / (
    "configs/benchmark/"
    "work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json"
)
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_RAW = ROOT / (
    "runs/development/"
    "work-ii-deepseek-five-task-development-evaluation-20260810"
)
DEFAULT_REPORT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-five-task-development-evaluation-20260810.json"
)
DEFAULT_MARKDOWN = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-five-task-development-evaluation-20260810.md"
)
DEEPSEEK_CONFIGS = {
    "electrochemical-conversion": (
        "configs/benchmark/work_ii_electrochemical_deepseek_v4_flash_campaign.json"
    ),
    "reaction-to-crystallization": (
        "configs/benchmark/work_ii_crystallization_deepseek_v4_flash_campaign.json"
    ),
    "reaction-to-distillation": (
        "configs/benchmark/work_ii_distillation_deepseek_v4_flash_campaign.json"
    ),
    "partition-discovery": (
        "configs/benchmark/work_ii_partition_deepseek_v4_flash_campaign.json"
    ),
    "reaction-safety-constrained": (
        "configs/benchmark/work_ii_safety_deepseek_v4_flash_campaign.json"
    ),
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _load_sources(
    manifest: Mapping[str, Any],
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], list[dict[str, Any]]]:
    loaded: list[tuple[dict[str, Any], dict[str, Any]]] = []
    bindings: list[dict[str, Any]] = []
    for raw_source in manifest.get("sources", []):
        if not isinstance(raw_source, Mapping):
            raise ValueError("source manifest contains a malformed source")
        source = dict(raw_source)
        path = Path(str(source["path"]))
        path = path if path.is_absolute() else ROOT / path
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != source.get("sha256"):
            raise ValueError(f"source hash mismatch: {source['source_id']}")
        matrix = _load(path)
        loaded.append((source, matrix))
        bindings.append(
            {
                "source_id": source["source_id"],
                "task_id": source["task_id"],
                "path": source["path"],
                "sha256": actual,
                "terminal_cell_count": matrix.get("terminal_cell_count"),
                "completed_cell_count": matrix.get("completed_cell_count"),
            }
        )
    return loaded, bindings


def _final_snapshot(analysis: Mapping[str, Any]) -> Mapping[str, Any] | None:
    snapshots = analysis.get("belief_snapshots")
    if not isinstance(snapshots, list):
        return None
    return next(
        (
            item
            for item in snapshots
            if isinstance(item, Mapping) and item.get("stage") == "final"
        ),
        None,
    )


def _truth_row(report: Mapping[str, Any], cluster_id: str) -> dict[str, Any]:
    receipts = report.get("receipts")
    receipts = receipts if isinstance(receipts, list) else []
    return {
        "world_cluster_id": cluster_id,
        "task_id": report.get("task_id"),
        "world_seed": report.get("world_seed"),
        "status": report.get("status"),
        "query_count": report.get("truth_query_count", 0),
        "completed_query_count": report.get("completed_truth_query_count", 0),
        "failed_query_count": report.get("failed_truth_query_count", 0),
        "query_metric_count": report.get("truth_query_metric_count", 0),
        "exact_replay_count": sum(
            isinstance(receipt, Mapping)
            and isinstance(receipt.get("exact_replay"), Mapping)
            and receipt["exact_replay"].get("verified") is True
            for receipt in receipts
        ),
        "report_sha256": report.get("report_sha256"),
    }


def _render_markdown(report: Mapping[str, Any]) -> str:
    d = report["denominators"]
    h3 = report["cluster_contrasts"]["H3_primary_contrast"]
    lines = [
        "# Work II DeepSeek development evaluator confirmation",
        "",
        "Date: 2026-08-10. Status: development evidence only; not formal or private evidence.",
        "",
        "## Exact denominators",
        "",
        f"- Participant cells retained: **{d['participant_cell_count']}/75**.",
        (
            "- Completed and runner-qualified participant cells: "
            f"**{d['participant_completed_and_qualified_cell_count']}/75**; "
            f"failed or unqualified: **{d['participant_failed_or_unqualified_cell_count']}/75**."
        ),
        (
            "- Evaluator truth queries: "
            f"**{d['truth_completed_query_count']}/{d['truth_query_count']}** completed and "
            f"**{d['truth_exact_replay_count']}/{d['truth_query_count']}** exact replay."
        ),
        (
            "- Blind replays: "
            f"**{d['blind_completed_execution_count']}/"
            f"{d['blind_scheduled_execution_count']}** completed."
        ),
        (
            "- Final checkpoint predictions scored: "
            f"**{d['checkpoint_final_scored_cell_count']}/75**; executable final law summaries: "
            f"**{d['law_summary_evaluated_cell_count']}/75**."
        ),
        "- Evaluator provider calls: **0**; participant resource-ledger impact: **0**.",
        "",
        "## Development observations",
        "",
        (
            "The retained task x seed H3 contrast has "
            f"n={h3['count']} clusters and descriptive mean "
            f"{h3['mean']:.4f}. Positive values mean that the misindexed arm reduced held-out "
            "prediction error more than the aligned arm; this is descriptive and is not a "
            "formal test."
            if h3["mean"] is not None
            else "The H3 contrast was not estimable."
        ),
        "",
        "| Task | Arm | n cells | pre error | final error | improvement | law error | blind gain |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["task_arm_summaries"]:
        means = {
            field: (
                "NA"
                if row[field]["mean"] is None
                else f"{row[field]['mean']:.4f}"
            )
            for field in (
                "pre_error",
                "final_error",
                "checkpoint_improvement",
                "law_summary_error",
                "blind_recommendation_gain",
            )
        }

        lines.append(
            f"| {row['task_id']} | {row['prior_arm']} | {row['cell_count']} | "
            f"{means['pre_error']} | {means['final_error']} | "
            f"{means['checkpoint_improvement']} | {means['law_summary_error']} | "
            f"{means['blind_recommendation_gain']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This analysis adds evaluator-held prediction scoring, executable-law checks and blind "
            "replay to the already frozen DeepSeek development trajectories. It does not rerun any "
            "participant cell, replace failures, perform a formal hypothesis test, evaluate "
            "private transfer or support a cross-provider capability ranking.",
            "",
            f"Machine report SHA-256: `{report['analysis_sha256']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--raw-output", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--preflight", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    source_manifest = _load(args.sources.resolve())
    design = _load(args.design.resolve())
    loaded_sources, source_bindings = _load_sources(source_manifest)
    cells = collect_development_cells(source_manifest, loaded_sources)
    task_configs = {
        str(task["task_id"]): _load(ROOT / str(task["campaign_config"]))
        for task in design["tasks"]
    }
    participant_configs = {
        task_id: _load(ROOT / relative_path)
        for task_id, relative_path in DEEPSEEK_CONFIGS.items()
    }
    preflight = build_development_confirmation_preflight(
        source_manifest=source_manifest,
        cells=cells,
        task_configs=task_configs,
        participant_configs=participant_configs,
        source_bindings=source_bindings,
        source_commit=_source_commit(),
    )
    print(json.dumps({"event": "preflight", **preflight}, sort_keys=True), flush=True)
    if args.preflight or preflight["status"] != "passed":
        return 0 if preflight["status"] == "passed" else 1

    raw_root = args.raw_output.resolve()
    report_path = args.report.resolve()
    markdown_path = args.markdown.resolve()
    for path in (raw_root, report_path, markdown_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite development evidence: {path}")
    raw_root.mkdir(parents=True)
    write_json_atomic(raw_root / "preflight.json", preflight)

    cells_by_cluster: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for cell in cells:
        cells_by_cluster.setdefault(
            (str(cell["task_id"]), int(cell["world_seed"])), []
        ).append(cell)

    truth_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    blind_contract = design["blind_evaluator_contract"]
    ordered_clusters = sorted(cells_by_cluster)
    for cluster_index, (task_id, world_seed) in enumerate(ordered_clusters, start=1):
        cluster_id = f"deepseek-development--{task_id}--seed-{world_seed}"
        print(
            json.dumps(
                {
                    "event": "truth_cluster_started",
                    "cluster_index": cluster_index,
                    "cluster_count": len(ordered_clusters),
                    "world_cluster_id": cluster_id,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        config = task_configs[task_id]
        truth_root = raw_root / "truth" / cluster_id
        truth_plan = build_evaluator_truth_plan(
            {
                "world_cluster_id": cluster_id,
                "task_id": task_id,
                "world_seed": world_seed,
            },
            config,
            formal_result=False,
            formal_preflight_sha256=None,
        )
        truth_report = execute_evaluator_truth_plan(truth_plan, config, truth_root)
        truth_errors = validate_evaluator_truth_report(truth_report, truth_plan)
        for error in truth_errors:
            failures.append(
                {
                    "scope": "truth",
                    "world_cluster_id": cluster_id,
                    "error": error,
                }
            )
        truth_rows.append(_truth_row(truth_report, cluster_id))
        evaluator_truth = truth_report.get("truth")
        evaluator_truth = evaluator_truth if isinstance(evaluator_truth, Mapping) else {}

        for cell in cells_by_cluster[(task_id, world_seed)]:
            result = cell["result"]
            analysis = result.get("analysis")
            analysis = analysis if isinstance(analysis, Mapping) else {}
            try:
                checkpoint = score_cell_checkpoint_errors(
                    analysis,
                    evaluator_truth,
                    terminal_state=str(cell["participant_state"]),
                )
            except Exception as error:
                checkpoint = {
                    "effective_pre_error": None,
                    "effective_final_error": None,
                    "primary_improvement": 0.0,
                    "missing_failure_rule": "evaluator_scoring_failed_sets_zero_improvement",
                    "unscorable_snapshots": [{"reason": str(error)}],
                }
                failures.append(
                    {
                        "scope": "checkpoint_scoring",
                        "cell_id": cell["cell_id"],
                        "error": str(error),
                    }
                )
            final_snapshot = _final_snapshot(analysis)
            law = evaluate_final_law_summary(
                (
                    final_snapshot.get("law_summary")
                    if isinstance(final_snapshot, Mapping)
                    else None
                ),
                truth_plan=truth_plan,
                evaluator_truth=evaluator_truth,
                final_checkpoint_predictions=(
                    final_snapshot.get("predictions")
                    if isinstance(final_snapshot, Mapping)
                    else None
                ),
                effective_pre_error=checkpoint.get("effective_pre_error"),
                effective_final_error=checkpoint.get("effective_final_error"),
                evaluation_contract=EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
            )

            blind_scheduled = 0
            blind_completed = 0
            blind_gain = None
            blind_status = "not_scheduled_participant_cell_failed_or_unqualified"
            blind_report_sha256 = None
            if cell["completed_and_qualified"] is True:
                blind_scheduled = 6
                try:
                    blind_plan = build_blind_evaluation_plan(
                        cell,
                        result,
                        blind_contract,
                    )
                    blind_root = raw_root / "blind" / str(cell["cell_key_sha256"])
                    blind_report = execute_blind_evaluation_plan(
                        blind_plan,
                        config,
                        blind_root,
                    )
                    receipt_paths = sorted(
                        (blind_root / "executions").glob("*/receipt.json")
                    )
                    receipts = [_load(path) for path in receipt_paths]
                    by_hash = {
                        str(receipt["receipt_sha256"]): receipt for receipt in receipts
                    }
                    ordered = [
                        by_hash[str(digest)]
                        for digest in blind_report["receipt_sha256"]
                    ]
                    blind_errors = validate_blind_evaluation_report(
                        blind_report,
                        blind_plan,
                        ordered,
                    )
                    for error in blind_errors:
                        failures.append(
                            {
                                "scope": "blind",
                                "cell_id": cell["cell_id"],
                                "error": error,
                            }
                        )
                    blind_completed = int(
                        blind_report.get("completed_execution_count", 0)
                    )
                    blind_gain = blind_report.get(
                        "recommendation_gain_over_incumbent"
                    )
                    blind_status = str(blind_report.get("status"))
                    blind_report_sha256 = blind_report.get("report_sha256")
                except Exception as error:
                    blind_status = "failed_retained_no_replacement"
                    failures.append(
                        {
                            "scope": "blind",
                            "cell_id": cell["cell_id"],
                            "error": f"{type(error).__name__}: {error}",
                        }
                    )

            row = {
                "cell_id": cell["cell_id"],
                "cell_key_sha256": cell["cell_key_sha256"],
                "source_id": cell["source_id"],
                "task_id": task_id,
                "world_seed": world_seed,
                "prior_arm": cell["prior_arm"],
                "participant_state": cell["participant_state"],
                "participant_failure": cell["participant_failure"],
                "effective_pre_error": checkpoint.get("effective_pre_error"),
                "effective_final_error": checkpoint.get("effective_final_error"),
                "checkpoint_improvement": checkpoint.get("primary_improvement", 0.0),
                "checkpoint_missing_rule": checkpoint.get("missing_failure_rule"),
                "checkpoint_scored_snapshot_count": checkpoint.get(
                    "scored_snapshot_count", 0
                ),
                "checkpoint_unscorable_snapshots": checkpoint.get(
                    "unscorable_snapshots", []
                ),
                "law_summary_status": law.get("status"),
                "law_summary_executability": law.get(
                    "evaluator_executability_status"
                ),
                "law_summary_error": law.get("normalized_mae"),
                "law_summary_improvement": law.get(
                    "pre_to_law_summary_improvement"
                ),
                "law_summary_minus_final_error": law.get(
                    "summary_minus_effective_final_error"
                ),
                "law_summary_prediction_consistency_error": law.get(
                    "prediction_consistency_normalized_mae"
                ),
                "law_summary_evaluation_error": law.get("evaluation_error"),
                "blind_status": blind_status,
                "blind_scheduled_execution_count": blind_scheduled,
                "blind_completed_execution_count": blind_completed,
                "blind_recommendation_gain": blind_gain,
                "blind_report_sha256": blind_report_sha256,
            }
            cell_rows.append(row)
            print(
                json.dumps(
                    {
                        "event": "cell_evaluated",
                        "cluster_index": cluster_index,
                        "cluster_count": len(ordered_clusters),
                        "cell_id": cell["cell_id"],
                        "participant_state": cell["participant_state"],
                        "law_summary_status": law.get("status"),
                        "blind_completed": blind_completed,
                        "blind_scheduled": blind_scheduled,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        print(
            json.dumps(
                {
                    "event": "truth_cluster_completed",
                    "cluster_index": cluster_index,
                    "cluster_count": len(ordered_clusters),
                    "world_cluster_id": cluster_id,
                    "truth_status": truth_report.get("status"),
                    "completed_queries": truth_report.get(
                        "completed_truth_query_count"
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    cluster_rows = build_cluster_rows(cell_rows)
    report = build_confirmation_summary(
        preflight=preflight,
        cell_rows=cell_rows,
        cluster_rows=cluster_rows,
        truth_rows=truth_rows,
        failures=failures,
    )
    raw_receipt = {
        "preflight_sha256": preflight["preflight_sha256"],
        "analysis_sha256": report["analysis_sha256"],
        "truth_report_sha256": [row["report_sha256"] for row in truth_rows],
        "blind_report_sha256": [
            row["blind_report_sha256"]
            for row in cell_rows
            if row["blind_report_sha256"] is not None
        ],
    }
    raw_receipt["receipt_sha256"] = canonical_json_sha256(raw_receipt)
    write_json_atomic(raw_root / "receipt.json", raw_receipt)
    write_json_atomic(report_path, report)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_render_markdown(report), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "event": "completed",
                "status": report["status"],
                "analysis_sha256": report["analysis_sha256"],
                "report": str(report_path),
                "markdown": str(markdown_path),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
