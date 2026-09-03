#!/usr/bin/env python3
# ruff: noqa: RUF001
"""Analyze matched W2-56/W2-63 B3 results with scheduled failure-aware denominators."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_reviewer_followup import B3_ARMS, summarize_b3_results

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEEPSEEK_ROOT = (
    ROOT
    / "runs/development/work-ii-w2-63-deepseek-b3-full-replication-v0.1-20260902"
)
DEFAULT_CODEX_ROOT = (
    ROOT
    / "runs/formal/"
    "work-ii-as-study-b3-gpt56-sol-medium-replication-v0.1-20260828-execution2"
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-63-b3-failure-aware-cross-model-v0.1.json"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_W2_63_B3_FAILURE_AWARE_CROSS_MODEL_ZH.md"
)
EXPECTED_CELLS = 30
EXPECTED_WORLDS = 5


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _load_results(root: Path) -> list[dict[str, Any]]:
    return [_load(path) for path in sorted((root / "cells").glob("*.json"))]


def _valid_self_hash(value: Mapping[str, Any], field: str) -> bool:
    expected = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    return isinstance(expected, str) and canonical_json_sha256(payload) == expected


def _coordinate(value: Mapping[str, Any]) -> tuple[str, str, int]:
    return (
        str(value["cluster_id"]),
        str(value["arm"]),
        int(value.get("replicate_index", 1)),
    )


def _receipts(result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    receipts: list[Mapping[str, Any]] = []
    for predecessor in result.get("infrastructure_predecessors", []):
        if isinstance(predecessor, Mapping):
            receipts.extend(
                item
                for item in predecessor.get("provider_receipts", [])
                if isinstance(item, Mapping)
            )
    receipts.extend(
        item
        for item in result.get("provider_receipts", [])
        if isinstance(item, Mapping)
    )
    return receipts


def _validate_root(root: Path) -> dict[str, Any]:
    manifest = _load(root / "input_manifest.json")
    results = _load_results(root)
    if not _valid_self_hash(manifest, "manifest_sha256"):
        raise ValueError(f"B3 manifest hash drifted: {root}")
    cells = manifest.get("cells")
    if not isinstance(cells, list) or len(cells) != EXPECTED_CELLS:
        raise ValueError(f"B3 manifest is not a 30-cell cohort: {root}")
    cells_by_id = {str(cell["cell_id"]): cell for cell in cells}
    results_by_id = {str(result["cell_id"]): result for result in results}
    if (
        len(cells_by_id) != EXPECTED_CELLS
        or len(results_by_id) != EXPECTED_CELLS
        or set(cells_by_id) != set(results_by_id)
    ):
        raise ValueError(f"B3 terminal results do not cover all scheduled cells: {root}")
    for cell_id, result in results_by_id.items():
        if result.get("status") not in {"completed", "failed"}:
            raise ValueError(f"B3 result is not terminal: {cell_id}")
        if str(result.get("study_id")) != str(manifest.get("study_id")):
            raise ValueError(f"B3 result study identity drifted: {cell_id}")
        if _coordinate(result) != _coordinate(cells_by_id[cell_id]):
            raise ValueError(f"B3 result coordinate drifted: {cell_id}")
        if not _valid_self_hash(result, "result_sha256"):
            raise ValueError(f"B3 result hash drifted: {cell_id}")
    summary = summarize_b3_results(manifest, results)
    stored = _load(root / "summary.json")
    if summary != stored:
        raise ValueError(f"B3 stored summary differs from recomputation: {root}")
    return {
        "root": root,
        "manifest": manifest,
        "cells": cells_by_id,
        "results": results_by_id,
        "summary": summary,
    }


def _validate_shared_science(
    deepseek: Mapping[str, Any], codex: Mapping[str, Any]
) -> dict[str, Any]:
    left = {_coordinate(cell): cell for cell in deepseek["cells"].values()}
    right = {_coordinate(cell): cell for cell in codex["cells"].values()}
    if set(left) != set(right) or len(left) != EXPECTED_CELLS:
        raise ValueError("B3 cross-model coordinates do not match")
    for coordinate in left:
        for field in ("public_packet", "scoring_truth"):
            if left[coordinate][field] != right[coordinate][field]:
                raise ValueError(f"B3 shared {field} differs at {coordinate}")
        if left[coordinate]["public_packet_sha256"] != right[coordinate][
            "public_packet_sha256"
        ]:
            raise ValueError(f"B3 packet hash differs at {coordinate}")
    return {
        "paired_cell_count": len(left),
        "paired_world_count": len({coordinate[0] for coordinate in left}),
        "public_packets_exact_match": True,
        "scoring_truth_exact_match": True,
    }


def _failure_aware_rows(block: Mapping[str, Any]) -> list[dict[str, Any]]:
    scientific_by_id = {
        str(row["cell_id"]): row for row in block["summary"].get("cell_rows", [])
    }
    rows: list[dict[str, Any]] = []
    for cell_id, cell in block["cells"].items():
        result = block["results"][cell_id]
        complete = result.get("status") == "completed"
        scientific = scientific_by_id.get(cell_id)
        if complete and scientific is None:
            raise ValueError(f"completed B3 cell lacks a scientific row: {cell_id}")
        failure = result.get("failure")
        failure = failure if isinstance(failure, Mapping) else {}
        post_family = scientific.get("post_family") if scientific else None
        exponent_error = (
            float(scientific["post_exponent_absolute_error"])
            if scientific is not None
            else None
        )
        joint_recovery = bool(
            post_family == "FAMILY_B_POWER"
            and exponent_error is not None
            and exponent_error <= 0.10
        )
        rows.append(
            {
                "cell_id": cell_id,
                "cluster_id": str(cell["cluster_id"]),
                "world_seed": int(cell["world_seed"]),
                "arm": str(cell["arm"]),
                "replicate_index": int(cell.get("replicate_index", 1)),
                "completed": complete,
                "failure_classification": failure.get("classification"),
                "post_error": float(scientific["post_error"]) if scientific else None,
                "family_recovery": post_family == "FAMILY_B_POWER",
                "joint_family_exponent_recovery": joint_recovery,
                "top1_selected": bool(scientific["top1_selected"]) if scientific else False,
                "selected_true_rank": (
                    float(scientific["selected_true_rank"]) if scientific else None
                ),
                "normalized_regret": (
                    float(scientific["normalized_regret"]) if scientific else 1.0
                ),
                "action_opportunity_eligible": (
                    bool(scientific["action_opportunity_eligible"])
                    if scientific
                    else None
                ),
                "selected_action_gain": (
                    float(scientific["selected_action_gain"]) if scientific else None
                ),
            }
        )
    return rows


def _mean_available(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = [float(row[field]) for row in rows if row.get(field) is not None]
    return mean(values) if values else None


def _metric_block(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in rows if row["completed"]]
    eligible = [row for row in completed if row["action_opportunity_eligible"]]
    failures = Counter(
        str(row["failure_classification"])
        for row in rows
        if not row["completed"]
    )
    return {
        "scheduled_cell_count": len(rows),
        "completed_cell_count": len(completed),
        "failed_cell_count": len(rows) - len(completed),
        "failure_classification_counts": dict(sorted(failures.items())),
        "failure_aware_mean_regret": mean(float(row["normalized_regret"]) for row in rows),
        "failure_aware_top1_count": sum(bool(row["top1_selected"]) for row in rows),
        "failure_aware_top1_rate": mean(float(bool(row["top1_selected"])) for row in rows),
        "failure_aware_joint_recovery_count": sum(
            bool(row["joint_family_exponent_recovery"]) for row in rows
        ),
        "failure_aware_joint_recovery_rate": mean(
            float(bool(row["joint_family_exponent_recovery"])) for row in rows
        ),
        "completed_mean_post_mae": _mean_available(completed, "post_error"),
        "completed_mean_selected_true_rank": _mean_available(
            completed, "selected_true_rank"
        ),
        "eligible_gain_denominator": len(eligible),
        "eligible_gain_at_least_0_02_count": sum(
            float(row["selected_action_gain"]) >= 0.02 for row in eligible
        ),
        "completed_mean_eligible_action_gain": _mean_available(
            eligible, "selected_action_gain"
        ),
    }


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _cluster_bootstrap(
    left: Mapping[tuple[str, str, int], Mapping[str, Any]],
    right: Mapping[tuple[str, str, int], Mapping[str, Any]],
    *,
    field: str,
    replicates: int = 10_000,
    seed: int = 263,
) -> dict[str, Any]:
    clusters = sorted({coordinate[0] for coordinate in left})
    cluster_deltas = {
        cluster: mean(
            float(right[coordinate][field]) - float(left[coordinate][field])
            for coordinate in left
            if coordinate[0] == cluster
        )
        for cluster in clusters
    }
    rng = random.Random(seed)
    draws = [
        mean(cluster_deltas[rng.choice(clusters)] for _ in clusters)
        for _ in range(replicates)
    ]
    return {
        "cluster_count": len(clusters),
        "replicate_count": replicates,
        "seed": seed,
        "estimate": mean(cluster_deltas.values()),
        "interval_95": [_percentile(draws, 0.025), _percentile(draws, 0.975)],
    }


def _paired_block(
    deepseek_rows: Sequence[Mapping[str, Any]],
    codex_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    left = {
        (str(row["cluster_id"]), str(row["arm"]), int(row["replicate_index"])): row
        for row in deepseek_rows
    }
    right = {
        (str(row["cluster_id"]), str(row["arm"]), int(row["replicate_index"])): row
        for row in codex_rows
    }
    if set(left) != set(right) or len(left) != len(deepseek_rows):
        raise ValueError("B3 paired result coordinates are incomplete")
    coordinates = sorted(left)
    common_complete = [
        coordinate
        for coordinate in coordinates
        if left[coordinate]["completed"] and right[coordinate]["completed"]
    ]
    regret = {
        coordinate: {
            "deepseek": float(left[coordinate]["normalized_regret"]),
            "codex": float(right[coordinate]["normalized_regret"]),
        }
        for coordinate in coordinates
    }
    bootstrap_left = {
        coordinate: {"regret": value["deepseek"]} for coordinate, value in regret.items()
    }
    bootstrap_right = {
        coordinate: {"regret": value["codex"]} for coordinate, value in regret.items()
    }
    return {
        "orientation": "codex_minus_deepseek",
        "paired_scheduled_cell_count": len(coordinates),
        "paired_common_completed_cell_count": len(common_complete),
        "failure_aware_mean_regret_difference": mean(
            float(right[key]["normalized_regret"])
            - float(left[key]["normalized_regret"])
            for key in coordinates
        ),
        "failure_aware_top1_rate_difference": mean(
            float(bool(right[key]["top1_selected"]))
            - float(bool(left[key]["top1_selected"]))
            for key in coordinates
        ),
        "failure_aware_joint_recovery_rate_difference": mean(
            float(bool(right[key]["joint_family_exponent_recovery"]))
            - float(bool(left[key]["joint_family_exponent_recovery"]))
            for key in coordinates
        ),
        "common_completed_post_mae_difference": (
            mean(
                float(right[key]["post_error"]) - float(left[key]["post_error"])
                for key in common_complete
            )
            if common_complete
            else None
        ),
        "common_completed_rank_difference": (
            mean(
                float(right[key]["selected_true_rank"])
                - float(left[key]["selected_true_rank"])
                for key in common_complete
            )
            if common_complete
            else None
        ),
        "regret_task_world_cluster_bootstrap": _cluster_bootstrap(
            bootstrap_left,
            bootstrap_right,
            field="regret",
        ),
        "inferential_model_superiority_test_performed": False,
    }


def _resource_summary(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    receipts = [receipt for result in results for receipt in _receipts(result)]
    usage = Counter()
    for receipt in receipts:
        for field, value in receipt.get("usage", {}).items():
            if isinstance(value, int | float) and not isinstance(value, bool):
                usage[str(field)] += value
    return {
        "provider_attempt_count": sum(
            int(result.get("provider_attempt_count", 1)) for result in results
        ),
        "provider_receipt_count": len(receipts),
        "completed_provider_receipt_count": sum(
            receipt.get("status") == "completed" for receipt in receipts
        ),
        "tool_event_count": sum(
            int(receipt.get("tool_event_count", 0)) for receipt in receipts
        ),
        "participant_physical_experiment_count": 0,
        "usage": dict(sorted(usage.items())),
    }


def build_summary(deepseek_root: Path, codex_root: Path) -> dict[str, Any]:
    deepseek = _validate_root(deepseek_root)
    codex = _validate_root(codex_root)
    shared = _validate_shared_science(deepseek, codex)
    deepseek_rows = _failure_aware_rows(deepseek)
    codex_rows = _failure_aware_rows(codex)
    result: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-w2-63-b3-failure-aware-cross-model-0.1",
        "status": "terminal_complete",
        "formal_result": False,
        "scheduled_cells_by_model": {"deepseek": 30, "codex": 30},
        "shared_science": shared,
        "cell_rows_by_model": {
            "deepseek": deepseek_rows,
            "codex": codex_rows,
        },
        "models": {
            "deepseek": {
                "provider": deepseek["manifest"]["provider"],
                "overall": _metric_block(deepseek_rows),
                "by_arm": {
                    arm: _metric_block([row for row in deepseek_rows if row["arm"] == arm])
                    for arm in B3_ARMS
                },
                "resources": _resource_summary(list(deepseek["results"].values())),
            },
            "codex": {
                "provider": codex["manifest"]["provider"],
                "overall": _metric_block(codex_rows),
                "by_arm": {
                    arm: _metric_block([row for row in codex_rows if row["arm"] == arm])
                    for arm in B3_ARMS
                },
                "resources": _resource_summary(list(codex["results"].values())),
            },
        },
        "paired_descriptive_differences": {
            "pooled": _paired_block(deepseek_rows, codex_rows),
            "by_arm": {
                arm: _paired_block(
                    [row for row in deepseek_rows if row["arm"] == arm],
                    [row for row in codex_rows if row["arm"] == arm],
                )
                for arm in B3_ARMS
            },
        },
        "claim_boundaries": {
            "scheduled_failure_aware_cross_model_denominator_available": True,
            "participant_failures_retained": True,
            "model_superiority_ranking_supported": False,
            "causal_provider_effect_supported": False,
            "generalization_beyond_frozen_b3_surface_supported": False,
        },
    }
    result["summary_sha256"] = canonical_json_sha256(result)
    return result


def _show(value: Any, digits: int = 4) -> str:
    return "—" if value is None else f"{float(value):.{digits}f}"


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II W2-63 B3 双模型 failure-aware 收束",
        "",
        "DeepSeek 与 Codex 均使用冻结的 30-cell B3 scientific surface。所有 participant "
        "失败保留；缺失动作固定计为 regret=1、Top-1=0。模型差值方向为 Codex − DeepSeek，"
        "仅作配对描述。",
        "",
        "| 模型 | scheduled | completed | failures | regret | Top-1 | joint law | post MAE |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for model in ("deepseek", "codex"):
        row = summary["models"][model]["overall"]
        lines.append(
            f"| {model} | {row['scheduled_cell_count']} | {row['completed_cell_count']} | "
            f"{row['failed_cell_count']} | {_show(row['failure_aware_mean_regret'])} | "
            f"{row['failure_aware_top1_count']}/{row['scheduled_cell_count']} | "
            f"{row['failure_aware_joint_recovery_count']}/{row['scheduled_cell_count']} | "
            f"{_show(row['completed_mean_post_mae'])} |"
        )
    paired = summary["paired_descriptive_differences"]["pooled"]
    interval = paired["regret_task_world_cluster_bootstrap"]["interval_95"]
    lines.extend(
        [
            "",
            "## 配对描述",
            "",
            "- failure-aware regret 差值: "
            f"`{_show(paired['failure_aware_mean_regret_difference'])}`; "
            f"task-world cluster bootstrap 95% interval "
            f"`[{_show(interval[0])}, {_show(interval[1])}]`。",
            f"- Top-1 rate 差值: `{_show(paired['failure_aware_top1_rate_difference'])}`。",
            f"- joint family+exponent recovery rate 差值: "
            f"`{_show(paired['failure_aware_joint_recovery_rate_difference'])}`。",
            "",
            "不执行模型优劣检验，也不将 provider 差异解释为因果效应。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deepseek-root", type=Path, default=DEFAULT_DEEPSEEK_ROOT)
    parser.add_argument("--codex-root", type=Path, default=DEFAULT_CODEX_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    summary = build_summary(args.deepseek_root.resolve(), args.codex_root.resolve())
    write_json_atomic(args.output.resolve(), summary)
    _write_report(summary, args.report.resolve())
    print(
        json.dumps(
            {
                "status": summary["status"],
                "scheduled_cells_by_model": summary["scheduled_cells_by_model"],
                "paired_cell_count": summary["shared_science"]["paired_cell_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
