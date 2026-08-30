#!/usr/bin/env python
# ruff: noqa: RUF001
"""Build the matched cross-model closeout for the completed W2-58 B3 blocks."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_reviewer_followup import B3_ARMS, summarize_b3_results

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEEPSEEK_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-runner-derived-status-deepseek-v0.1-20260831"
)
DEFAULT_GPT_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-runner-derived-status-gpt56-sol-medium-v0.1-20260831"
)
DEFAULT_JSON_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b3-runner-derived-status-cross-model-closeout-v0.1.json"
)
DEFAULT_REPORT_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_AS_STUDY_B3_RUNNER_DERIVED_STATUS_CROSS_MODEL_CLOSEOUT_ZH.md"
)
EXPECTED_FORMAL_CELLS = 30
EXPECTED_CANARY_CELLS = 3
EXPECTED_CLUSTERS = 5
EXPECTED_REPLICATE_BLOCKS = 10
EXPECTED_REPLICATES_PER_ARM = 2


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _load_results(directory: Path) -> list[dict[str, Any]]:
    return [_load(path) for path in sorted(directory.glob("*.json"))]


def _hash_valid(value: Mapping[str, Any], field: str) -> bool:
    expected = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    return isinstance(expected, str) and canonical_json_sha256(payload) == expected


def _cell_coordinate(value: Mapping[str, Any]) -> tuple[str, int, str, int]:
    return (
        str(value["cluster_id"]),
        int(value["world_seed"]),
        str(value["arm"]),
        int(value.get("replicate_index", 1)),
    )


def _manifest_cells(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    cells = manifest.get("cells")
    if not isinstance(cells, list):
        raise ValueError("B3 manifest cells are unavailable")
    by_id = {str(cell["cell_id"]): cell for cell in cells}
    if len(by_id) != len(cells):
        raise ValueError("B3 manifest contains duplicate cell IDs")
    return by_id


def _packet_hashes(manifest: Mapping[str, Any]) -> dict[str, str]:
    packets = manifest.get("cluster_packets")
    if not isinstance(packets, list):
        raise ValueError("B3 cluster packets are unavailable")
    result = {
        str(packet["cluster_id"]): str(packet["public_packet_sha256"])
        for packet in packets
    }
    if len(result) != len(packets):
        raise ValueError("B3 manifest contains duplicate cluster packets")
    return result


def _provider_identity(manifest: Mapping[str, Any]) -> dict[str, Any]:
    provider = manifest.get("provider")
    if not isinstance(provider, Mapping):
        raise ValueError("B3 provider identity is unavailable")
    return {
        "id": provider.get("id"),
        "model": provider.get("model"),
        "reasoning_effort": provider.get("reasoning_effort"),
        "wire_api": provider.get("wire_api"),
        "auth_mode": provider.get("auth_mode"),
    }


def _validate_canary(
    manifest: Mapping[str, Any],
    canary_summary: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    cells = list(_manifest_cells(manifest).values())
    first_cluster = str(cells[0]["cluster_id"])
    expected_ids = {
        str(cell["cell_id"])
        for cell in cells
        if str(cell["cluster_id"]) == first_cluster
        and int(cell.get("replicate_index", 1)) == 1
    }
    observed_ids = [str(result.get("cell_id")) for result in results]
    if (
        canary_summary.get("qualified") is not True
        or len(results) != EXPECTED_CANARY_CELLS
        or len(set(observed_ids)) != EXPECTED_CANARY_CELLS
        or set(observed_ids) != expected_ids
    ):
        raise ValueError("B3 cross-model closeout requires a qualified 3/3 canary")
    for result in results:
        if not _hash_valid(result, "result_sha256"):
            raise ValueError("B3 canary result hash verification failed")
        receipts = result.get("provider_receipts")
        if (
            result.get("status") != "completed"
            or result.get("same_thread") is not True
            or not isinstance(receipts, list)
            or len(receipts) != 2
            or not all(
                isinstance(receipt, Mapping) and receipt.get("status") == "completed"
                for receipt in receipts
            )
        ):
            raise ValueError("B3 cross-model closeout requires complete same-thread canaries")
    return {
        "qualified": True,
        "completed_session_count": EXPECTED_CANARY_CELLS,
        "completed_turn_count": EXPECTED_CANARY_CELLS * 2,
        "result_hashes_verified": EXPECTED_CANARY_CELLS,
    }


def _validate_formal(
    manifest: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    stored_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if not _hash_valid(manifest, "manifest_sha256"):
        raise ValueError("B3 input manifest hash verification failed")
    if manifest.get("action_selection_encoding") != "zero_based_index":
        raise ValueError("B3 cross-model closeout requires shared zero-based action indices")
    if manifest.get("stage_status_encoding") != "runner_derived":
        raise ValueError("B3 cross-model closeout requires runner-derived stage status")
    if int(manifest.get("cell_count", -1)) != EXPECTED_FORMAL_CELLS:
        raise ValueError("B3 cross-model closeout requires a 30-cell manifest")

    manifest_cells = _manifest_cells(manifest)
    result_ids = [str(result.get("cell_id")) for result in results]
    if (
        len(results) != EXPECTED_FORMAL_CELLS
        or len(set(result_ids)) != EXPECTED_FORMAL_CELLS
        or set(result_ids) != set(manifest_cells)
    ):
        raise ValueError("B3 cross-model closeout requires exactly 30 formal results")

    study_id = str(manifest["study_id"])
    for result in results:
        cell_id = str(result["cell_id"])
        if result.get("status") != "completed":
            raise ValueError("B3 cross-model closeout rejects any formal failure")
        if str(result.get("study_id")) != study_id:
            raise ValueError("B3 formal result study identity drifted")
        if _cell_coordinate(result) != _cell_coordinate(manifest_cells[cell_id]):
            raise ValueError("B3 formal result coordinate drifted from its manifest cell")
        if not _hash_valid(result, "result_sha256"):
            raise ValueError("B3 formal result hash verification failed")

    summary = summarize_b3_results(manifest, results)
    if stored_summary is not None and dict(stored_summary) != summary:
        raise ValueError("stored B3 summary differs from deterministic recomputation")
    if (
        summary.get("status") != "completed"
        or int(summary.get("completed_cell_count", -1)) != EXPECTED_FORMAL_CELLS
        or int(summary.get("failed_cell_count", -1)) != 0
        or int(summary.get("complete_cluster_count", -1)) != EXPECTED_CLUSTERS
        or int(summary.get("complete_replicate_block_count", -1))
        != EXPECTED_REPLICATE_BLOCKS
        or int(summary.get("replicates_per_arm", -1)) != EXPECTED_REPLICATES_PER_ARM
        or any(
            int(summary["by_arm"][arm]["completed_cell_count"])
            != EXPECTED_FORMAL_CELLS // len(B3_ARMS)
            for arm in B3_ARMS
        )
    ):
        raise ValueError("B3 cross-model formal denominator is incomplete")
    return summary


def _metric_block(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row["action_opportunity_eligible"]]
    joint = [
        row
        for row in rows
        if row["post_family"] == "FAMILY_B_POWER"
        and float(row["post_exponent_absolute_error"]) <= 0.10
    ]
    denominator = len(rows)
    eligible_denominator = len(eligible)
    return {
        "cell_denominator": denominator,
        "mean_post_mae": mean(float(row["post_error"]) for row in rows),
        "family_recovery_count": sum(
            row["post_family"] == "FAMILY_B_POWER" for row in rows
        ),
        "family_recovery_rate": mean(
            float(row["post_family"] == "FAMILY_B_POWER") for row in rows
        ),
        "joint_family_exponent_recovery_count": len(joint),
        "joint_family_exponent_recovery_rate": len(joint) / denominator,
        "top1_count": sum(bool(row["top1_selected"]) for row in rows),
        "top1_rate": mean(float(bool(row["top1_selected"])) for row in rows),
        "mean_selected_true_rank": mean(float(row["selected_true_rank"]) for row in rows),
        "mean_normalized_regret": mean(float(row["normalized_regret"]) for row in rows),
        "eligible_gain_denominator": eligible_denominator,
        "eligible_positive_gain_count": sum(
            float(row["selected_action_gain"]) > 0.0 for row in eligible
        ),
        "eligible_gain_at_least_threshold_count": sum(
            float(row["selected_action_gain"])
            >= float(row["action_opportunity_threshold"])
            for row in eligible
        ),
        "eligible_gain_at_least_threshold_rate": (
            sum(
                float(row["selected_action_gain"])
                >= float(row["action_opportunity_threshold"])
                for row in eligible
            )
            / eligible_denominator
            if eligible_denominator
            else None
        ),
        "mean_eligible_action_gain": (
            mean(float(row["selected_action_gain"]) for row in eligible)
            if eligible
            else None
        ),
    }


def _provider_metrics(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = list(summary["cell_rows"])
    return {
        "pooled": _metric_block(rows),
        "by_arm": {
            arm: _metric_block([row for row in rows if row["arm"] == arm])
            for arm in B3_ARMS
        },
    }


def _descriptive_difference(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    left = {_cell_coordinate(row): row for row in left_rows}
    right = {_cell_coordinate(row): row for row in right_rows}
    if set(left) != set(right) or len(left) != len(left_rows) or len(right) != len(right_rows):
        raise ValueError("B3 paired cell coordinates are incomplete or duplicated")
    coordinates = sorted(left)
    eligible = [
        coordinate
        for coordinate in coordinates
        if left[coordinate]["action_opportunity_eligible"]
    ]

    def average_delta(field: str, selected: Sequence[tuple[str, int, str, int]]) -> float | None:
        if not selected:
            return None
        return mean(float(right[key][field]) - float(left[key][field]) for key in selected)

    def rate_delta(predicate: str) -> float:
        if predicate == "family":
            outcome = lambda row: row["post_family"] == "FAMILY_B_POWER"  # noqa: E731
        elif predicate == "joint":
            outcome = lambda row: (  # noqa: E731
                row["post_family"] == "FAMILY_B_POWER"
                and float(row["post_exponent_absolute_error"]) <= 0.10
            )
        elif predicate == "top1":
            outcome = lambda row: bool(row["top1_selected"])  # noqa: E731
        elif predicate == "gain_threshold":
            outcome = lambda row: (  # noqa: E731
                float(row["selected_action_gain"])
                >= float(row["action_opportunity_threshold"])
            )
        else:  # pragma: no cover - internal programming error
            raise ValueError(predicate)
        selected = eligible if predicate == "gain_threshold" else coordinates
        return mean(float(outcome(right[key])) - float(outcome(left[key])) for key in selected)

    return {
        "paired_cell_denominator": len(coordinates),
        "eligible_paired_cell_denominator": len(eligible),
        "mean_post_mae_difference": average_delta("post_error", coordinates),
        "family_recovery_rate_difference": rate_delta("family"),
        "joint_family_exponent_recovery_rate_difference": rate_delta("joint"),
        "top1_rate_difference": rate_delta("top1"),
        "mean_selected_true_rank_difference": average_delta(
            "selected_true_rank", coordinates
        ),
        "mean_normalized_regret_difference": average_delta(
            "normalized_regret", coordinates
        ),
        "mean_eligible_action_gain_difference": average_delta(
            "selected_action_gain", eligible
        ),
        "eligible_gain_at_least_threshold_rate_difference": rate_delta(
            "gain_threshold"
        ),
    }


def build_cross_model_summary(
    deepseek_manifest: Mapping[str, Any],
    deepseek_results: Sequence[Mapping[str, Any]],
    gpt_manifest: Mapping[str, Any],
    gpt_results: Sequence[Mapping[str, Any]],
    *,
    deepseek_stored_summary: Mapping[str, Any] | None = None,
    gpt_stored_summary: Mapping[str, Any] | None = None,
    canary_integrity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate two complete matched blocks and return descriptive cross-model results."""

    deepseek_summary = _validate_formal(
        deepseek_manifest, deepseek_results, deepseek_stored_summary
    )
    gpt_summary = _validate_formal(gpt_manifest, gpt_results, gpt_stored_summary)
    shared_fields = ("qualification_sha256", "public_truth_sha256", "roster_sha256")
    mismatched = [
        field
        for field in shared_fields
        if deepseek_manifest.get(field) != gpt_manifest.get(field)
    ]
    if mismatched:
        raise ValueError(f"B3 shared science hashes differ: {', '.join(mismatched)}")
    deepseek_packets = _packet_hashes(deepseek_manifest)
    gpt_packets = _packet_hashes(gpt_manifest)
    if deepseek_packets != gpt_packets:
        raise ValueError("B3 shared public packet hashes differ")

    deepseek_cells = _manifest_cells(deepseek_manifest)
    gpt_cells = _manifest_cells(gpt_manifest)
    deepseek_coordinates = {
        _cell_coordinate(cell): (cell_id, str(cell["public_packet_sha256"]))
        for cell_id, cell in deepseek_cells.items()
    }
    gpt_coordinates = {
        _cell_coordinate(cell): (cell_id, str(cell["public_packet_sha256"]))
        for cell_id, cell in gpt_cells.items()
    }
    if deepseek_coordinates != gpt_coordinates:
        raise ValueError("B3 formal cells do not share the same paired coordinates")

    deepseek_identity = _provider_identity(deepseek_manifest)
    gpt_identity = _provider_identity(gpt_manifest)
    if (
        deepseek_identity["id"],
        deepseek_identity["model"],
        deepseek_identity["reasoning_effort"],
    ) == (
        gpt_identity["id"],
        gpt_identity["model"],
        gpt_identity["reasoning_effort"],
    ):
        raise ValueError("B3 cross-model closeout requires two distinct model configurations")

    deepseek_rows = list(deepseek_summary["cell_rows"])
    gpt_rows = list(gpt_summary["cell_rows"])
    paired_by_arm = {
        arm: _descriptive_difference(
            [row for row in deepseek_rows if row["arm"] == arm],
            [row for row in gpt_rows if row["arm"] == arm],
        )
        for arm in B3_ARMS
    }
    result: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-b3-cross-model-closeout-0.1",
        "status": "formal_completed_matched_cross_model",
        "formal_result": True,
        "providers": {
            "deepseek": deepseek_identity,
            "gpt": gpt_identity,
        },
        "integrity": {
            "formal_completed_by_provider": {"deepseek": 30, "gpt": 30},
            "formal_failures_by_provider": {"deepseek": 0, "gpt": 0},
            "formal_result_hashes_verified_by_provider": {
                "deepseek": 30,
                "gpt": 30,
            },
            "stored_summary_exact_recomputation_by_provider": {
                "deepseek": deepseek_stored_summary is not None,
                "gpt": gpt_stored_summary is not None,
            },
            "canary": dict(canary_integrity or {}),
            "paired_cell_count": len(deepseek_coordinates),
            "paired_world_count": EXPECTED_CLUSTERS,
            "shared_hashes": {
                field: deepseek_manifest[field] for field in shared_fields
            },
            "shared_public_packet_hashes": deepseek_packets,
        },
        "provider_results": {
            "deepseek": _provider_metrics(deepseek_summary),
            "gpt": _provider_metrics(gpt_summary),
        },
        "paired_descriptive_differences": {
            "orientation": "gpt_minus_deepseek",
            "pooled": _descriptive_difference(deepseek_rows, gpt_rows),
            "by_arm": paired_by_arm,
            "inferential_test_performed": False,
        },
        "claim_boundaries": {
            "matched_cross_model_formal_denominator_available": True,
            "provider_specific_three_arm_results_supported": True,
            "descriptive_paired_model_differences_supported": True,
            "model_superiority_ranking_supported": False,
            "causal_provider_effect_supported": False,
            "generalization_beyond_the_frozen_b3_surface_supported": False,
        },
    }
    result["summary_sha256"] = canonical_json_sha256(result)
    return result


def _show(value: float | None, digits: int = 4) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    providers = summary["providers"]
    results = summary["provider_results"]
    differences = summary["paired_descriptive_differences"]
    lines = [
        "# Work II A-S Study B3 双模型正式实验收束",
        "",
        "状态：`formal_completed_matched_cross_model`。DeepSeek 与 GPT 各完成冻结的 "
        "`30/30` formal cells，失败均为 `0`；60 个结果按相同 world、arm 与 replicate "
        "逐格匹配。两边 canary 不进入 formal 科学分母。",
        "",
        "## 模型内结果",
        "",
        "| 模型 | arm | n | post MAE | family+exponent | Top-1 | mean rank | "
        "mean regret | eligible gain≥阈值 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for provider_key in ("deepseek", "gpt"):
        identity = providers[provider_key]
        label = f"{identity['model']} / {identity['reasoning_effort']}"
        for arm in B3_ARMS:
            row = results[provider_key]["by_arm"][arm]
            lines.append(
                f"| {label} | {arm} | {row['cell_denominator']} | "
                f"{_show(row['mean_post_mae'])} | "
                f"{row['joint_family_exponent_recovery_count']}/"
                f"{row['cell_denominator']} | {row['top1_count']}/"
                f"{row['cell_denominator']} | "
                f"{_show(row['mean_selected_true_rank'], 2)} | "
                f"{_show(row['mean_normalized_regret'])} | "
                f"{row['eligible_gain_at_least_threshold_count']}/"
                f"{row['eligible_gain_denominator']} |"
            )
    lines.extend(
        [
            "",
            "## 配对描述差值",
            "",
            "以下差值固定为 `GPT − DeepSeek`，仅描述同一冻结 B3 surface 上的位置差异；"
            "未执行模型优劣检验，也不解释为 provider 因果效应。",
            "",
            "| 范围 | paired n | post MAE Δ | joint recovery-rate Δ | Top-1-rate Δ | "
            "mean rank Δ | regret Δ | eligible gain Δ |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for label, row in [("pooled", differences["pooled"]), *differences["by_arm"].items()]:
        lines.append(
            f"| {label} | {row['paired_cell_denominator']} | "
            f"{_show(row['mean_post_mae_difference'])} | "
            f"{_show(row['joint_family_exponent_recovery_rate_difference'])} | "
            f"{_show(row['top1_rate_difference'])} | "
            f"{_show(row['mean_selected_true_rank_difference'])} | "
            f"{_show(row['mean_normalized_regret_difference'])} | "
            f"{_show(row['mean_eligible_action_gain_difference'])} |"
        )
    lines.extend(
        [
            "",
            "## 证据边界",
            "",
            "该结果支持两个模型配置各自的三臂 formal 结论，以及严格匹配 cell 的描述性差值。"
            "它不支持模型排行榜、provider 因果效应或对冻结 B3 surface 之外任务的普遍化。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deepseek-root", type=Path, default=DEFAULT_DEEPSEEK_ROOT)
    parser.add_argument("--gpt-root", type=Path, default=DEFAULT_GPT_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    args = parser.parse_args()

    roots = {
        "deepseek": args.deepseek_root.resolve(),
        "gpt": args.gpt_root.resolve(),
    }
    loaded: dict[str, dict[str, Any]] = {}
    canary_integrity: dict[str, Any] = {}
    for provider_key, root in roots.items():
        manifest = _load(root / "input_manifest.json")
        canary_summary = _load(root / "canary_summary.json")
        canary_results = _load_results(root / "canary")
        canary_integrity[provider_key] = _validate_canary(
            manifest, canary_summary, canary_results
        )
        loaded[provider_key] = {
            "manifest": manifest,
            "summary": _load(root / "summary.json"),
            "results": _load_results(root / "cells"),
        }

    summary = build_cross_model_summary(
        loaded["deepseek"]["manifest"],
        loaded["deepseek"]["results"],
        loaded["gpt"]["manifest"],
        loaded["gpt"]["results"],
        deepseek_stored_summary=loaded["deepseek"]["summary"],
        gpt_stored_summary=loaded["gpt"]["summary"],
        canary_integrity=canary_integrity,
    )
    json_output = args.json_output.resolve()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(json_output, summary)
    _write_report(summary, args.report_output.resolve())
    print(
        json.dumps(
            {
                "status": summary["status"],
                "formal_completed_by_provider": summary["integrity"][
                    "formal_completed_by_provider"
                ],
                "paired_cell_count": summary["integrity"]["paired_cell_count"],
                "orientation": summary["paired_descriptive_differences"][
                    "orientation"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
