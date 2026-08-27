#!/usr/bin/env python
# ruff: noqa: RUF001
"""Audit and close out the completed GPT-5.6-sol medium B3 formal block."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_reviewer_followup import summarize_b3_results

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-gpt56-sol-medium-replication-v0.1-"
    "20260828-execution2"
)
DEFAULT_JSON_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b3-gpt56-sol-medium-formal-closeout-v0.1.json"
)
DEFAULT_REPORT_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_AS_STUDY_B3_GPT56_SOL_MEDIUM_FORMAL_CLOSEOUT_ZH.md"
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _load_results(directory: Path) -> list[dict[str, Any]]:
    return [_load(path) for path in sorted(directory.glob("*.json"))]


def _result_hash_valid(result: Mapping[str, Any]) -> bool:
    expected = result.get("result_sha256")
    payload = dict(result)
    payload.pop("result_sha256", None)
    return isinstance(expected, str) and canonical_json_sha256(payload) == expected


def _phase_resources(
    results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    receipts: list[tuple[str, int, Mapping[str, Any]]] = []
    usage: Counter[str] = Counter()
    event_counts: Counter[str] = Counter()
    provider_errors: list[dict[str, Any]] = []
    for result in results:
        cell_id = str(result["cell_id"])
        for turn_index, receipt_value in enumerate(result["provider_receipts"], start=1):
            if not isinstance(receipt_value, Mapping):
                raise ValueError(f"{cell_id}: provider receipt is not an object")
            receipt = receipt_value
            receipts.append((cell_id, turn_index, receipt))
            for name, count in receipt.get("event_counts", {}).items():
                event_counts[str(name)] += int(count)
            for name, count in receipt.get("usage", {}).items():
                usage[str(name)] += int(count or 0)
            for error in receipt.get("provider_errors", []):
                provider_errors.append(
                    {
                        "cell_id": cell_id,
                        "turn_index": turn_index,
                        "receipt_status": receipt.get("status"),
                        "error": error,
                    }
                )
    input_tokens = int(usage["input_tokens"])
    cached_input_tokens = int(usage["cached_input_tokens"])
    return {
        "session_record_count": len(results),
        "provider_session_attempt_count": sum(
            int(result.get("provider_attempt_count", 0)) for result in results
        ),
        "completed_session_record_count": sum(
            result.get("status") == "completed" for result in results
        ),
        "same_thread_session_count": sum(
            result.get("same_thread") is True for result in results
        ),
        "provider_receipt_count": len(receipts),
        "completed_provider_receipt_count": sum(
            receipt.get("status") == "completed" for _, _, receipt in receipts
        ),
        "tool_event_count": sum(
            int(receipt.get("tool_event_count", 0) or 0)
            for _, _, receipt in receipts
        ),
        "participant_physical_experiment_count": sum(
            int(result.get("participant_physical_experiment_count", 0))
            for result in results
        ),
        "infrastructure_predecessor_count": sum(
            len(result.get("infrastructure_predecessors", []))
            for result in results
        ),
        "event_counts": dict(sorted(event_counts.items())),
        "provider_error_event_count": len(provider_errors),
        "provider_error_events": provider_errors,
        "usage": {
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_input_tokens,
            "uncached_input_tokens": input_tokens - cached_input_tokens,
            "cache_write_input_tokens": int(usage["cache_write_input_tokens"]),
            "output_tokens": int(usage["output_tokens"]),
            "reasoning_output_tokens": int(usage["reasoning_output_tokens"]),
        },
        "summed_session_elapsed_s": sum(
            float(result.get("elapsed_s", 0.0)) for result in results
        ),
    }


def _phase_wall_time(progress_rows: Sequence[Mapping[str, Any]], phase: str) -> float:
    prefix = f"b3_{phase}"
    rows = [
        row
        for row in progress_rows
        if str(row.get("stage", "")).startswith(prefix)
    ]
    if not rows:
        raise ValueError(f"progress ledger has no {phase} rows")
    return float(max(row["timestamp"] for row in rows)) - float(
        min(row["timestamp"] for row in rows)
    )


def _scientific_closeout(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = list(summary["cell_rows"])
    clusters = list(summary["cluster_rows"])
    structural_recovery = [
        row
        for row in rows
        if row["post_family"] == "FAMILY_B_POWER"
        and float(row["post_exponent_absolute_error"]) <= 0.10
    ]
    eligible = [row for row in rows if row["action_opportunity_eligible"]]
    by_arm: dict[str, Any] = {}
    for arm in ARMS:
        arm_rows = [row for row in rows if row["arm"] == arm]
        arm_eligible = [row for row in arm_rows if row["action_opportunity_eligible"]]
        joint = [
            row
            for row in arm_rows
            if row["post_family"] == "FAMILY_B_POWER"
            and float(row["post_exponent_absolute_error"]) <= 0.10
        ]
        by_arm[arm] = {
            **dict(summary["by_arm"][arm]),
            "joint_family_and_exponent_recovery_count": len(joint),
            "post_error_at_most_0_05_count": sum(
                float(row["post_error"]) <= 0.05 for row in arm_rows
            ),
            "eligible_joint_structural_recovery_count": sum(
                row["action_opportunity_eligible"] for row in joint
            ),
            "eligible_top1_count": sum(
                row["top1_selected"] for row in arm_eligible
            ),
        }

    def cluster_contrast(metric: str, left: str, right: str) -> dict[str, Any]:
        differences = [
            float(cluster[metric][left]) - float(cluster[metric][right])
            for cluster in clusters
        ]
        return {
            "left_arm": left,
            "right_arm": right,
            "mean_left_minus_right": mean(differences),
            "left_lower_world_count": sum(value < 0.0 for value in differences),
            "tie_world_count": sum(abs(value) <= 1.0e-12 for value in differences),
            "world_denominator": len(differences),
        }

    recovered_eligible = [
        row for row in structural_recovery if row["action_opportunity_eligible"]
    ]
    return {
        "by_arm": by_arm,
        "pooled": {
            "cell_denominator": len(rows),
            "mean_pre_error": mean(float(row["pre_error"]) for row in rows),
            "mean_post_error": mean(float(row["post_error"]) for row in rows),
            "joint_family_and_exponent_recovery_count": len(structural_recovery),
            "top1_count": sum(row["top1_selected"] for row in rows),
            "top1_in_action_ineligible_world_count": sum(
                row["top1_selected"] and not row["action_opportunity_eligible"]
                for row in rows
            ),
        },
        "world_cluster_contrasts": {
            "aligned_vs_opaque_exponent_error": cluster_contrast(
                "mean_exponent_error_by_arm", "aligned_nominal", "opaque"
            ),
            "aligned_vs_misindexed_exponent_error": cluster_contrast(
                "mean_exponent_error_by_arm",
                "aligned_nominal",
                "misindexed_nominal",
            ),
            "aligned_vs_misindexed_post_error": cluster_contrast(
                "mean_post_error_by_arm", "aligned_nominal", "misindexed_nominal"
            ),
            "aligned_vs_misindexed_rank": cluster_contrast(
                "mean_selected_true_rank_by_arm",
                "aligned_nominal",
                "misindexed_nominal",
            ),
            "aligned_vs_misindexed_regret": cluster_contrast(
                "mean_normalized_regret_by_arm",
                "aligned_nominal",
                "misindexed_nominal",
            ),
        },
        "action_bridge": {
            "all_world_rank_regret_cell_denominator": len(rows),
            "action_opportunity_eligible_cell_denominator": len(eligible),
            "action_opportunity_eligible_world_denominator": sum(
                cluster["action_opportunity_eligible"] for cluster in clusters
            ),
            "positive_gain_count": sum(
                float(row["selected_action_gain"]) > 0.0 for row in eligible
            ),
            "gain_at_least_0_02_count": sum(
                float(row["selected_action_gain"])
                >= float(row["action_opportunity_threshold"])
                for row in eligible
            ),
            "structurally_recovered_eligible_cell_count": len(recovered_eligible),
            "structurally_recovered_eligible_gain_at_least_0_02_count": sum(
                float(row["selected_action_gain"])
                >= float(row["action_opportunity_threshold"])
                for row in recovered_eligible
            ),
        },
        "cluster_rows": clusters,
    }


def _show(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}"


def _write_report(closeout: Mapping[str, Any], path: Path) -> None:
    science = closeout["science"]
    resources = closeout["resources"]
    canary = resources["canary"]
    formal = resources["formal"]
    lines = [
        "# Work II A-S Study B3 GPT-5.6-sol medium 正式实验收束",
        "",
        "状态：`formal_completed`。三臂 canary `3/3` 通过后，冻结的 formal matrix "
        "`30/30` cells 全部完成，失败 `0`；5 worlds × 3 arms × 2 independent "
        "sessions 的科学分母完整，canary 不进入 formal 分母。",
        "",
        "## 科学结果",
        "",
        "| arm | n | pre MAE | post MAE | family B | family+exponent recovery | "
        "Top-1 | mean rank | mean regret | eligible gain≥0.02 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        row = science["by_arm"][arm]
        lines.append(
            f"| {arm} | {row['completed_cell_count']} | "
            f"{_show(row['mean_pre_error'])} | {_show(row['mean_post_error'])} | "
            f"{row['exact_family_recovery_count']}/10 | "
            f"{row['joint_family_and_exponent_recovery_count']}/10 | "
            f"{row['top1_selected_count']}/10 | "
            f"{_show(row['mean_selected_true_rank'], 2)} | "
            f"{_show(row['mean_normalized_regret'])} | "
            f"{row['action_gain_at_least_0_02_count']}/"
            f"{row['action_opportunity_eligible_gain_denominator']} |"
        )
    aligned_opaque = science["world_cluster_contrasts"][
        "aligned_vs_opaque_exponent_error"
    ]
    aligned_misindexed = science["world_cluster_contrasts"][
        "aligned_vs_misindexed_exponent_error"
    ]
    action = science["action_bridge"]
    lines.extend(
        [
            "",
            "所有 arm 的平均未见查询误差都明显下降；formal post MAE 分别为 "
            f"`{_show(science['by_arm']['opaque']['mean_post_error'])}`、"
            f"`{_show(science['by_arm']['aligned_nominal']['mean_post_error'])}`、"
            f"`{_show(science['by_arm']['misindexed_nominal']['mean_post_error'])}`。"
            "因此直接证据稳定支持数值插值。",
            "",
            "结构层面没有出现普遍恢复。aligned arm 在 `5/10` sessions 同时保留 "
            "FAMILY_B_POWER 与 1.75±0.10；opaque 和 misindexed 均为 `0/10`。"
            "aligned 的 world-mean exponent error 对 opaque 和 misindexed 都在 "
            f"`{aligned_opaque['left_lower_world_count']}/5`、"
            f"`{aligned_misindexed['left_lower_world_count']}/5` worlds 更低。"
            "值得注意的是 misindexed 有 `8/10` 选择了 power family，却有 `0/10` "
            "恢复正确指数：family 标签本身不能视为结构识别。该结果支持“正确先验的部分保留”，"
            "不支持证据诱导的选择性错误先验修正。",
            "",
            "证据到行动的桥接同样没有建立。全 30 cells 只有 `2/30` Top-1，"
            "且两次都来自 action-opportunity 不成立的同一 world；在预先冻结的 "
            f"`{action['action_opportunity_eligible_cell_denominator']}` 个 eligible cells 中，"
            f"达到 gain≥0.02 的为 `{action['gain_at_least_0_02_count']}/"
            f"{action['action_opportunity_eligible_cell_denominator']}`。"
            "即使在 eligible 且结构恢复的 "
            f"`{action['structurally_recovered_eligible_cell_count']}` "
            "个 cells 中，也没有一个达到 0.02 action gain。",
            "",
            "## 执行与资源审计",
            "",
            "| phase | sessions | attempts | completed turns | same-thread | tools | "
            "physical experiments | wall time |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
            f"| canary | {canary['session_record_count']} | "
            f"{canary['provider_session_attempt_count']} | "
            f"{canary['completed_provider_receipt_count']}/"
            f"{canary['provider_receipt_count']} | "
            f"{canary['same_thread_session_count']}/3 | {canary['tool_event_count']} | "
            f"{canary['participant_physical_experiment_count']} | "
            f"{_show(resources['canary_wall_time_s'], 1)} s |",
            f"| formal | {formal['session_record_count']} | "
            f"{formal['provider_session_attempt_count']} | "
            f"{formal['completed_provider_receipt_count']}/"
            f"{formal['provider_receipt_count']} | "
            f"{formal['same_thread_session_count']}/30 | {formal['tool_event_count']} | "
            f"{formal['participant_physical_experiment_count']} | "
            f"{_show(resources['formal_wall_time_s'], 1)} s |",
            "",
            "总计 33 provider session attempts、66/66 completed turn receipts、0 retries、"
            "0 tool events、0 physical experiments。formal 最后一个 opaque post turn 记录过 "
            "`1` 个 transient provider error event，但同一 turn 最终返回 completed receipt，"
            "cell 状态仍为 completed；该事件完整保留，既不误记为 formal failure，也不忽略。",
            "",
            f"总 usage：input `{resources['total_usage']['input_tokens']}`（其中 cached "
            f"`{resources['total_usage']['cached_input_tokens']}`，uncached "
            f"`{resources['total_usage']['uncached_input_tokens']}`），output "
            f"`{resources['total_usage']['output_tokens']}`，reasoning output "
            f"`{resources['total_usage']['reasoning_output_tokens']}`。",
            "",
            "## 结论边界",
            "",
            "这是与 DeepSeek B3 provider-free science surface 逐字段匹配的 OpenAI "
            "GPT-5.6-sol medium 结果，但 DeepSeek block 没有形成 formal 科学分母，因此不能做 "
            "cross-provider leaderboard。可进入论文的是 GPT block 内部的冻结三臂结果："
            "数值收敛、正确先验的部分结构保留、错误先验未被选择性修正，以及结构理解到新动作的"
            "非单调映射。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    args = parser.parse_args()

    run_root = args.run_root.resolve()
    manifest = _load(run_root / "input_manifest.json")
    stored_summary = _load(run_root / "summary.json")
    canary_summary = _load(run_root / "canary_summary.json")
    qualification = _load(run_root / "qualification_summary.json")
    public_truth = _load(run_root / "public_truth_manifest.json")
    formal_results = _load_results(run_root / "cells")
    canary_results = _load_results(run_root / "canary")
    progress_rows = [
        json.loads(line)
        for line in (run_root / "progress.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]

    recomputed_summary = summarize_b3_results(manifest, formal_results)
    if recomputed_summary != stored_summary:
        raise ValueError("stored formal summary differs from a fresh deterministic recomputation")
    if canary_summary.get("qualified") is not True or len(canary_results) != 3:
        raise ValueError("the frozen three-session canary is not qualified and complete")
    if len(formal_results) != 30 or stored_summary.get("status") != "completed":
        raise ValueError("the frozen 30-session formal denominator is incomplete")
    if not all(_result_hash_valid(result) for result in [*canary_results, *formal_results]):
        raise ValueError("one or more immutable result hashes do not verify")
    if qualification.get("status") != "qualified":
        raise ValueError("provider-free structural qualification is unavailable")
    if public_truth.get("status") != "preflight_passed":
        raise ValueError("provider-free public truth preflight is unavailable")

    canary_resources = _phase_resources(canary_results)
    formal_resources = _phase_resources(formal_results)
    total_usage = {
        key: int(canary_resources["usage"][key])
        + int(formal_resources["usage"][key])
        for key in canary_resources["usage"]
    }
    closeout: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-b3-gpt56-formal-closeout-0.1",
        "status": "formal_completed",
        "formal_result": True,
        "study_id": manifest["study_id"],
        "provider": {
            "id": manifest["provider"]["id"],
            "model": manifest["provider"]["model"],
            "reasoning_effort": manifest["provider"]["reasoning_effort"],
            "wire_api": manifest["provider"]["wire_api"],
            "auth_mode": manifest["provider"]["auth_mode"],
        },
        "integrity": {
            "canary_qualified": True,
            "canary_result_hashes_verified": len(canary_results),
            "formal_result_hashes_verified": len(formal_results),
            "formal_summary_exact_recomputation": True,
            "scheduled_formal_cell_count": int(manifest["cell_count"]),
            "observed_formal_cell_count": len(formal_results),
            "completed_formal_cell_count": int(stored_summary["completed_cell_count"]),
            "failed_formal_cell_count": int(stored_summary["failed_cell_count"]),
            "complete_world_cluster_count": int(stored_summary["complete_cluster_count"]),
            "complete_replicate_block_count": int(
                stored_summary["complete_replicate_block_count"]
            ),
            "replicates_per_arm": int(stored_summary["replicates_per_arm"]),
            "canary_in_formal_scientific_denominator": False,
            "outcome_replacement_count": 0,
        },
        "provider_free_preparation": {
            "qualification_status": qualification["status"],
            "public_truth_status": public_truth["status"],
            "development_world_count": int(qualification["development_world_count"]),
            "public_world_count": int(public_truth["public_world_count"]),
            "action_opportunity_eligible_world_count": int(
                public_truth["action_opportunity_eligible_world_count"]
            ),
        },
        "science": _scientific_closeout(stored_summary),
        "resources": {
            "canary": canary_resources,
            "formal": formal_resources,
            "canary_wall_time_s": _phase_wall_time(progress_rows, "canary"),
            "formal_wall_time_s": _phase_wall_time(progress_rows, "formal"),
            "total_usage": total_usage,
        },
        "claim_boundaries": {
            "cross_provider_leaderboard_supported": False,
            "deepseek_formal_scientific_comparator_available": False,
            "provider_specific_three_arm_formal_result_supported": True,
            "generalized_structural_recovery_supported": False,
            "evidence_to_action_bridge_supported": False,
        },
        "failures": list(stored_summary["failures"]),
    }
    closeout["summary_sha256"] = canonical_json_sha256(closeout)
    write_json_atomic(args.json_output.resolve(), closeout)
    _write_report(closeout, args.report_output.resolve())
    print(
        json.dumps(
            {
                "status": closeout["status"],
                "formal_cells": closeout["integrity"][
                    "completed_formal_cell_count"
                ],
                "formal_failures": closeout["integrity"][
                    "failed_formal_cell_count"
                ],
                "structural_recovery_by_arm": {
                    arm: closeout["science"]["by_arm"][arm][
                        "joint_family_and_exponent_recovery_count"
                    ]
                    for arm in ARMS
                },
                "eligible_gain_at_least_0_02": closeout["science"][
                    "action_bridge"
                ]["gain_at_least_0_02_count"],
                "provider_error_events": closeout["resources"]["formal"][
                    "provider_error_event_count"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
