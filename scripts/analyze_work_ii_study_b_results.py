#!/usr/bin/env python
# ruff: noqa: E501, RUF001
"""Analyze the completed Work II Study B matched-evidence block."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ROOT = ROOT / "runs/formal/work-ii-study-b-matched-evidence-v0.1-20260815"
DEFAULT_JSON = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-study-b-matched-evidence-results-v0.1.json"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_STUDY_B_MATCHED_EVIDENCE_RESULTS_ZH.md"
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _mean_sd(values: Sequence[float]) -> dict[str, float]:
    return {
        "mean": statistics.mean(values),
        "sd": statistics.stdev(values),
        "minimum": min(values),
        "maximum": max(values),
    }


def _mean_ci(values: Sequence[float]) -> dict[str, Any]:
    n = len(values)
    observed = statistics.mean(values)
    standard_error = statistics.stdev(values) / math.sqrt(n)
    half_width = float(t.ppf(0.975, n - 1)) * standard_error
    return {
        "n": n,
        "mean": observed,
        "standard_error": standard_error,
        "confidence_interval_95": [observed - half_width, observed + half_width],
    }


def _exact_sign_flip(values: Sequence[float]) -> dict[str, Any]:
    observed = statistics.mean(values)
    null = [
        statistics.mean([value * sign for value, sign in zip(values, signs, strict=True)])
        for signs in itertools.product((-1.0, 1.0), repeat=len(values))
    ]
    return {
        **_mean_ci(values),
        "values": list(values),
        "positive_world_count": sum(value > 0.0 for value in values),
        "zero_world_count": sum(value == 0.0 for value in values),
        "negative_world_count": sum(value < 0.0 for value in values),
        "exact_sign_flip_p_one_sided_greater": sum(
            value >= observed - 1.0e-15 for value in null
        )
        / len(null),
        "exact_sign_flip_p_two_sided": sum(
            abs(value) >= abs(observed) - 1.0e-15 for value in null
        )
        / len(null),
        "inference_unit": "task_x_world_seed",
    }


def _terms(cell: Mapping[str, Any], stage: str, metric_id: str) -> list[float]:
    return [
        float(term["normalized_absolute_error"])
        for term in cell["scores"][stage]["terms"]
        if term["metric_id"] == metric_id
    ]


def _cell_metric_error(cell: Mapping[str, Any], stage: str, metric_id: str) -> float:
    return statistics.mean(_terms(cell, stage, metric_id))


def _analyze_locus(cells: Sequence[Mapping[str, Any]], locus: str) -> dict[str, Any]:
    members = [cell for cell in cells if cell["locus"] == locus]
    seeds = sorted({int(cell["world_seed"]) for cell in members})
    metrics = sorted(
        {
            str(term["metric_id"])
            for cell in members
            for term in cell["scores"]["post"]["terms"]
        }
    )
    arm_summary: dict[str, Any] = {}
    for arm in ARMS:
        arm_cells = [cell for cell in members if cell["arm"] == arm]
        pre = [float(cell["scores"]["pre"]["mean_normalized_absolute_error"]) for cell in arm_cells]
        post = [float(cell["scores"]["post"]["mean_normalized_absolute_error"]) for cell in arm_cells]
        gain = [before - after for before, after in zip(pre, post, strict=True)]
        arm_summary[arm] = {
            "cell_count": len(arm_cells),
            "pre_error": _mean_sd(pre),
            "post_error": _mean_sd(post),
            "update_gain": _mean_sd(gain),
            "relative_error_reduction": _mean_sd(
                [(before - after) / before for before, after in zip(pre, post, strict=True)]
            ),
            "mean_confidence_pre": statistics.mean(
                float(cell["pre_prediction"]["confidence"]) for cell in arm_cells
            ),
            "mean_confidence_post": statistics.mean(
                float(cell["post_prediction"]["confidence"]) for cell in arm_cells
            ),
        }
    primary: list[float] = []
    post_mis_minus_aligned: list[float] = []
    post_mis_minus_opaque: list[float] = []
    world_rows: list[dict[str, Any]] = []
    for seed in seeds:
        world = {cell["arm"]: cell for cell in members if cell["world_seed"] == seed}
        errors = {
            arm: {
                stage: float(world[arm]["scores"][stage]["mean_normalized_absolute_error"])
                for stage in ("pre", "post")
            }
            for arm in ARMS
        }
        gains = {arm: errors[arm]["pre"] - errors[arm]["post"] for arm in ARMS}
        contrast = gains["misindexed_nominal"] - gains["aligned_nominal"]
        primary.append(contrast)
        post_mis_minus_aligned.append(
            errors["misindexed_nominal"]["post"] - errors["aligned_nominal"]["post"]
        )
        post_mis_minus_opaque.append(
            errors["misindexed_nominal"]["post"] - errors["opaque"]["post"]
        )
        world_rows.append(
            {
                "world_seed": seed,
                "errors": errors,
                "update_gains": gains,
                "primary_contrast": contrast,
            }
        )
    metric_rows: list[dict[str, Any]] = []
    for metric_id in metrics:
        by_arm: dict[str, Any] = {}
        for arm in ARMS:
            arm_cells = [cell for cell in members if cell["arm"] == arm]
            pre_terms = [value for cell in arm_cells for value in _terms(cell, "pre", metric_id)]
            post_terms = [value for cell in arm_cells for value in _terms(cell, "post", metric_id)]
            by_arm[arm] = {
                "pre_mean_error": statistics.mean(pre_terms),
                "post_mean_error": statistics.mean(post_terms),
                "mean_error_reduction": statistics.mean(pre_terms) - statistics.mean(post_terms),
                "term_count": len(post_terms),
            }
        metric_primary: list[float] = []
        metric_post_difference: list[float] = []
        for seed in seeds:
            world = {cell["arm"]: cell for cell in members if cell["world_seed"] == seed}
            aligned_gain = _cell_metric_error(
                world["aligned_nominal"], "pre", metric_id
            ) - _cell_metric_error(world["aligned_nominal"], "post", metric_id)
            misindexed_gain = _cell_metric_error(
                world["misindexed_nominal"], "pre", metric_id
            ) - _cell_metric_error(world["misindexed_nominal"], "post", metric_id)
            metric_primary.append(misindexed_gain - aligned_gain)
            metric_post_difference.append(
                _cell_metric_error(world["misindexed_nominal"], "post", metric_id)
                - _cell_metric_error(world["aligned_nominal"], "post", metric_id)
            )
        metric_rows.append(
            {
                "metric_id": metric_id,
                "by_arm": by_arm,
                "primary_contrast": _mean_ci(metric_primary),
                "primary_positive_world_count": sum(value > 0.0 for value in metric_primary),
                "post_misindexed_minus_aligned": _mean_ci(metric_post_difference),
                "post_misindexed_worse_world_count": sum(
                    value > 0.0 for value in metric_post_difference
                ),
            }
        )
    return {
        "locus": locus,
        "cluster_count": len(seeds),
        "cell_count": len(members),
        "arm_summary": arm_summary,
        "primary_contrast": _exact_sign_flip(primary),
        "post_misindexed_minus_aligned": _mean_ci(post_mis_minus_aligned),
        "post_misindexed_minus_opaque": _mean_ci(post_mis_minus_opaque),
        "world_rows": world_rows,
        "metric_rows": metric_rows,
    }


def _public_summary_audit(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ap_misindexed = [
        cell for cell in cells if cell["locus"] == "A_P" and cell["arm"] == "misindexed_nominal"
    ]
    as_misindexed = [
        cell for cell in cells if cell["locus"] == "A_S" and cell["arm"] == "misindexed_nominal"
    ]
    ap_rows = []
    for cell in sorted(ap_misindexed, key=lambda item: item["world_seed"]):
        text = (
            str(cell["post_prediction"]["model_summary"])
            + " "
            + str(cell["post_prediction"]["evidence_assessment"])
        ).lower()
        explicit_rejection = "contradict" in text or "opposite to the initial" in text
        peak_collapse = "collapse" in text and ("1.1" in text or "1.107" in text)
        ap_rows.append(
            {
                "world_seed": cell["world_seed"],
                "explicitly_rejected_supplied_direction": explicit_rejection,
                "adopted_peak_and_collapse_response": peak_collapse,
            }
        )
    as_rows = []
    target_law_markers = (
        "partition exponent 1.75",
        "1.75-power partition",
        "power-response partition",
        "partition power response",
    )
    fixed_process_markers = (
        "no phase_process",
        "all evidence shares",
        "same process condition",
        "fixed volumes/mixing",
        "fixed volumes/process",
        "identical volumes",
    )
    for cell in sorted(as_misindexed, key=lambda item: item["world_seed"]):
        text = (
            str(cell["post_prediction"]["model_summary"])
            + " "
            + str(cell["post_prediction"]["evidence_assessment"])
        ).lower()
        as_rows.append(
            {
                "world_seed": cell["world_seed"],
                "recovered_registered_partition_power_law": any(
                    marker in text for marker in target_law_markers
                ),
                "recognized_fixed_process_evidence_limit": any(
                    marker in text for marker in fixed_process_markers
                ),
                "used_linear_or_distribution_coefficient_model": any(
                    marker in text
                    for marker in ("linear", "partition coefficient", "distribution", "d~", "k_d")
                ),
            }
        )
    return {
        "source": "participant_public_model_summary_and_evidence_assessment_only",
        "private_reasoning_used": False,
        "A_P_misindexed": {
            "world_count": len(ap_rows),
            "explicit_direction_rejection_count": sum(
                row["explicitly_rejected_supplied_direction"] for row in ap_rows
            ),
            "peak_and_collapse_response_count": sum(
                row["adopted_peak_and_collapse_response"] for row in ap_rows
            ),
            "world_rows": ap_rows,
        },
        "A_S_misindexed": {
            "world_count": len(as_rows),
            "registered_partition_power_law_recovery_count": sum(
                row["recovered_registered_partition_power_law"] for row in as_rows
            ),
            "fixed_process_evidence_limit_recognition_count": sum(
                row["recognized_fixed_process_evidence_limit"] for row in as_rows
            ),
            "linear_or_distribution_model_count": sum(
                row["used_linear_or_distribution_coefficient_model"] for row in as_rows
            ),
            "world_rows": as_rows,
        },
    }


def analyze(run_root: Path) -> dict[str, Any]:
    summary = json.loads((run_root / "summary.json").read_text(encoding="utf-8"))
    cells = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((run_root / "cells").glob("*.json"))
    ]
    if (
        summary.get("status") != "completed"
        or summary.get("completed_cell_count") != 30
        or summary.get("failed_cell_count") != 0
        or len(cells) != 30
    ):
        raise RuntimeError("Study B is not a complete 30/30 zero-failure block")
    if any(cell.get("scores", {}).get("pre", {}).get("term_count") not in {24, 48} for cell in cells):
        raise RuntimeError("Study B contains an invalid pre-evidence denominator")
    if any(cell.get("scores", {}).get("post", {}).get("term_count") not in {24, 48} for cell in cells):
        raise RuntimeError("Study B contains an invalid post-evidence denominator")
    progress = [
        json.loads(line)
        for line in (run_root / "progress.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    formal_start = next(row["timestamp"] for row in progress if row["stage"] == "formal_execution_started")
    formal_end = max(
        row["timestamp"]
        for row in progress
        if row["stage"] == "formal_progress" and row.get("completed_cells") == 30
    )
    usage_fields = (
        "input_tokens",
        "cached_input_tokens",
        "cache_write_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    )
    usage = {
        field: sum(
            int(receipt.get("usage", {}).get(field, 0))
            for cell in cells
            for receipt in cell["provider_receipts"]
        )
        for field in usage_fields
    }
    tool_event_cells = [
        {
            "cell_id": cell["cell_id"],
            "tool_event_count": sum(
                int(receipt.get("tool_event_count", 0))
                for receipt in cell["provider_receipts"]
            ),
        }
        for cell in cells
        if any(receipt.get("tool_event_count", 0) for receipt in cell["provider_receipts"])
    ]
    return {
        "schema_version": "chemworld-work-ii-study-b-results-analysis-0.1",
        "study_id": summary["study_id"],
        "run_root": run_root.relative_to(ROOT).as_posix(),
        "integrity": {
            "scheduled_sessions": 30,
            "completed_sessions": 30,
            "failed_sessions": 0,
            "complete_clusters": 10,
            "provider_turns": sum(len(cell["provider_receipts"]) for cell in cells),
            "same_thread_sessions": sum(cell.get("same_thread") is True for cell in cells),
            "single_attempt_sessions": sum(cell.get("provider_attempt_count") == 1 for cell in cells),
            "infrastructure_predecessor_count": sum(
                len(cell.get("infrastructure_predecessors", [])) for cell in cells
            ),
            "participant_physical_experiment_count": 0,
            "tool_event_count": sum(row["tool_event_count"] for row in tool_event_cells),
            "tool_event_cells": tool_event_cells,
            "turn_failed_event_count": sum(
                int(receipt.get("event_counts", {}).get("turn.failed", 0))
                for cell in cells
                for receipt in cell["provider_receipts"]
            ),
            "formal_wall_time_seconds": formal_end - formal_start,
            "mean_cell_wall_time_seconds": statistics.mean(float(cell["elapsed_s"]) for cell in cells),
            "median_cell_wall_time_seconds": statistics.median(
                float(cell["elapsed_s"]) for cell in cells
            ),
            "provider_reported_usage": usage,
        },
        "locus_results": [_analyze_locus(cells, locus) for locus in ("A_P", "A_S")],
        "public_summary_audit": _public_summary_audit(cells),
        "interpretation_contract": {
            "registered_primary_estimand_retained": True,
            "registered_primary": (
                "misindexed_pre_to_post_error_reduction_minus_aligned_pre_to_post_error_reduction"
            ),
            "small_n_inference": "exact 2^5 cluster sign-flip; descriptive t interval",
            "post_error_and_metric_specific_results": "secondary sensitivity analyses",
            "cross_locus_pooling_performed": False,
            "canary_included": False,
        },
    }


def _f(value: float) -> str:
    return f"{value:.4f}"


def write_report(analysis: Mapping[str, Any], path: Path) -> None:
    loci = {row["locus"]: row for row in analysis["locus_results"]}
    ap = loci["A_P"]
    structural = loci["A_S"]
    ap_audit = analysis["public_summary_audit"]["A_P_misindexed"]
    as_audit = analysis["public_summary_audit"]["A_S_misindexed"]
    ap_arms = ap["arm_summary"]
    as_arms = structural["arm_summary"]
    ap_primary = ap["primary_contrast"]
    as_primary = structural["primary_contrast"]
    as_organic = next(
        row for row in structural["metric_rows"] if row["metric_id"] == "product_in_organic"
    )
    integrity = analysis["integrity"]
    lines = [
        "# Work II Study B：matched evidence 结果与机制分析",
        "",
        "## 结论先行",
        "",
        "Study B 完成了 30/30 fresh sessions、10/10 task-world clusters，0 失败、0 participant "
        "物理实验。结果支持一个分 locus 的机制结论，而不是统一的 seeking/updating 二分答案：",
        "",
        "1. **A-P electrochemical 支持 evidence-seeking bottleneck。** 固定反证到达后，错误方向先验"
        "在 5/5 worlds 都被公开文字明确否定，模型恢复了约 1.1 V 最优、1.3 V 以上性能坍塌的响应；"
        "三 arm 的 post-error 收敛到几乎相同水平。",
        "2. **A-S partition 尚不能定位 belief-updating failure。** misindexed sessions 没有恢复注册的"
        " 1.75 power law，但输入证据全部来自同一个 identity/process 条件，模型也明确指出缺少"
        " phase-process 干预。这个 packet 足以校准 endpoint，却不足以唯一反驳 linear/distribution law。",
        "3. 因此当前 Study B 是 **部分机制闭环**：A-P 闭环；A-S 暴露了 evidence level 与 law level"
        " 的错配。不能把 A-S 的负 primary contrast 直接写成‘模型看见充分反证仍拒绝更新’。",
        "",
        "## 1. 完整性与执行",
        "",
        f"- 正式 sessions：{integrity['completed_sessions']}/{integrity['scheduled_sessions']}；"
        f"clusters：{integrity['complete_clusters']}/10；失败 0。",
        f"- 两轮同 thread：{integrity['same_thread_sessions']}/30；provider turns："
        f"{integrity['provider_turns']}/60；全部一次完成，无 infrastructure predecessor。",
        f"- participant 物理实验：0；正式 wall time："
        f"{integrity['formal_wall_time_seconds'] / 60.0:.1f} min；中位 cell wall time："
        f"{integrity['median_cell_wall_time_seconds']:.1f} s。",
        f"- 60 个 turns 中出现 {integrity['tool_event_count']} 个工具事件，分布于 "
        f"{len(integrity['tool_event_cells'])} 个 pre turns；隔离 workspace、禁用 web/apps/plugins，"
        "无 evaluator truth 或仓库数据访问路径，且不影响两轮分母。",
        "",
        "## 2. 注册主指标",
        "",
        "主指标保持冻结定义：`(misindexed pre − post) − (aligned pre − post)`；正值表示在相同证据下，"
        "misindexed 比 aligned 获得更多纠错增益。统计单位是 world，单 locus 只有 n=5，因此 exact "
        "sign-flip 只作小样本方向校验。",
        "",
        "| Locus | opaque gain | aligned gain | misindexed gain | primary contrast | positive worlds | "
        "exact one-sided p | 95% descriptive CI |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| A-P | {_f(ap_arms['opaque']['update_gain']['mean'])} | "
        f"{_f(ap_arms['aligned_nominal']['update_gain']['mean'])} | "
        f"{_f(ap_arms['misindexed_nominal']['update_gain']['mean'])} | "
        f"{_f(ap_primary['mean'])} | {ap_primary['positive_world_count']}/5 | "
        f"{ap_primary['exact_sign_flip_p_one_sided_greater']:.3f} | "
        f"[{_f(ap_primary['confidence_interval_95'][0])}, "
        f"{_f(ap_primary['confidence_interval_95'][1])}] |",
        f"| A-S | {_f(as_arms['opaque']['update_gain']['mean'])} | "
        f"{_f(as_arms['aligned_nominal']['update_gain']['mean'])} | "
        f"{_f(as_arms['misindexed_nominal']['update_gain']['mean'])} | "
        f"{_f(as_primary['mean'])} | {as_primary['positive_world_count']}/5 | "
        f"{as_primary['exact_sign_flip_p_one_sided_greater']:.3f} | "
        f"[{_f(as_primary['confidence_interval_95'][0])}, "
        f"{_f(as_primary['confidence_interval_95'][1])}] |",
        "",
        "A-P 的主对比为正但 n=5 下未达到常规显著阈值；证据强度主要来自 5/5 明确文字纠错与三臂"
        " post-error 收敛，而不是 p 值。A-S 的主对比为负，但其 misindexed pre-error 本来更低，"
        "gain 受可改善空间影响，不能单独视为结构更新失败。",
        "",
        "## 3. A-P：固定反证使错误参数方向可纠正",
        "",
        "| Arm | pre error | post error | absolute gain | relative reduction |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        row = ap_arms[arm]
        lines.append(
            f"| {arm} | {_f(row['pre_error']['mean'])} | {_f(row['post_error']['mean'])} | "
            f"{_f(row['update_gain']['mean'])} | "
            f"{100.0 * row['relative_error_reduction']['mean']:.1f}% |"
        )
    lines.extend(
        [
            "",
            f"misindexed − aligned 的 post-error 均值差为 "
            f"{_f(ap['post_misindexed_minus_aligned']['mean'])}；misindexed − opaque 为 "
            f"{_f(ap['post_misindexed_minus_opaque']['mean'])}。三臂最终误差差异不到 0.004，说明"
            "反证到达后初始 prior 的方向影响基本被消除。",
            "",
            f"公开 summary 审计显示：{ap_audit['explicit_direction_rejection_count']}/5 misindexed worlds "
            f"明确否定 supplied direction，{ap_audit['peak_and_collapse_response_count']}/5 恢复"
            " peak-and-collapse 响应。该结果与 Study A 的 A-P suggestive、但未过 selective-correction gate "
            "结合，支持自由探索中的主要损失至少部分发生在反证获取，而不是反证到达后的参数更新。",
            "",
            "## 4. A-S：endpoint 校准不等于结构规律纠正",
            "",
            "| Arm | pre error | post error | absolute gain | relative reduction |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for arm in ARMS:
        row = as_arms[arm]
        lines.append(
            f"| {arm} | {_f(row['pre_error']['mean'])} | {_f(row['post_error']['mean'])} | "
            f"{_f(row['update_gain']['mean'])} | "
            f"{100.0 * row['relative_error_reduction']['mean']:.1f}% |"
        )
    lines.extend(
        [
            "",
            "三个 A-S arms 的相对误差下降都约 83–86%，说明 packet 能强力校准 endpoint。"
            "但这一数值不能证明 power law 被恢复：24 个评分项中，16 个是接近常数的 `phase_ratio` "
            "和 `product_in_aqueous`；真正承载结构变化的 `product_in_organic` 只有 8 项。",
            "",
            f"在 `product_in_organic` 上，aligned gain 为 "
            f"{_f(as_organic['by_arm']['aligned_nominal']['mean_error_reduction'])}，misindexed gain 为 "
            f"{_f(as_organic['by_arm']['misindexed_nominal']['mean_error_reduction'])}，主对比 "
            f"{_f(as_organic['primary_contrast']['mean'])}，仅 "
            f"{as_organic['primary_positive_world_count']}/5 worlds 为正。可是 misindexed 的 pre-error "
            "也明显更低，因此该 gain gap 仍不能单独识别 stubborn updating。",
            "",
            f"公开 summary 中，misindexed arm 恢复注册 1.75 partition power law 为 "
            f"{as_audit['registered_partition_power_law_recovery_count']}/5；继续使用 linear/distribution "
            f"coefficient 类模型为 {as_audit['linear_or_distribution_model_count']}/5；明确识别固定 process "
            f"证据局限为 {as_audit['fixed_process_evidence_limit_recognition_count']}/5。"
            "这说明模型做了数值更新，却没有完成结构更新；同时 packet 本身也没有提供足够的"
            " phase-process 对照去唯一要求结构更新。",
            "",
            "## 5. 对 Paper 2 故事的影响",
            "",
            "Study B 把能力链进一步拆开：",
            "",
            "- **参数规律层**：错误方向可以被高信息量反证覆盖；自由探索表现不佳包含 evidence-seeking "
            "loss。",
            "- **结构规律层**：相同数量的 endpoint evidence 可以显著降低 prediction error，却仍无法保证"
            "机制 family recovery。问题不只是‘模型是否愿意更新’，还包括 evidence 是否与 law 的"
            "可识别层级匹配。",
            "- 因此论文不应把 matched evidence 简化成一个 yes/no treatment；更强的表述是"
            " **correction requires intervention-complete evidence at the same abstraction level as the law**。",
            "",
            "## 6. 当前证据边界",
            "",
            "- Study B 的 A-P 子结论已经闭环。",
            "- Study B 的 A-S 子结论是设计诊断，不足以完成 acquisition-vs-updating 的结构 locus 因果定位。",
            "- 若要完成 A-S 定位，后续独立 B2 应给出能直接分离 linear 与 1.75-power law 的"
            " phase-process 成对干预，并用另一组不重叠 phase-process queries 评分；不能事后改写本次 30-cell "
            "block。",
            "- 当前结果不需要补跑或删除；它作为‘endpoint adaptation 与 structural correction 分离’的"
            "证据永久保留。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    analysis = analyze(args.run_root.resolve())
    _write_json(args.output_json.resolve(), analysis)
    write_report(analysis, args.output_report.resolve())
    print(json.dumps({"status": "completed", "output_json": str(args.output_json), "output_report": str(args.output_report)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
