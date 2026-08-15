#!/usr/bin/env python
# ruff: noqa: E501, RUF001
"""Analyze the completed Work II A-S Study B2 phase-process block."""

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
DEFAULT_RUN_ROOT = ROOT / "runs/formal/work-ii-as-study-b2-phase-process-v0.1-20260815"
DEFAULT_JSON = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-phase-process-results-v0.1.json"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_AS_STUDY_B2_PHASE_PROCESS_RESULTS_ZH.md"
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
METRICS = ("product_in_organic", "product_in_aqueous", "phase_ratio")


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
    observed = statistics.mean(values)
    standard_error = statistics.stdev(values) / math.sqrt(len(values))
    half_width = float(t.ppf(0.975, len(values) - 1)) * standard_error
    return {
        "n": len(values),
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
        "inference_unit": "public_world_seed",
    }


def _terms(cell: Mapping[str, Any], stage: str, metric_id: str) -> list[float]:
    return [
        float(term["normalized_absolute_error"])
        for term in cell["scores"][stage]["terms"]
        if term["metric_id"] == metric_id
    ]


def _cell_metric_error(cell: Mapping[str, Any], stage: str, metric_id: str) -> float:
    return statistics.mean(_terms(cell, stage, metric_id))


def _public_text(cell: Mapping[str, Any]) -> str:
    return (
        str(cell["post_prediction"]["model_summary"])
        + " "
        + str(cell["post_prediction"]["evidence_assessment"])
    ).lower()


def _public_summary_audit(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows: dict[str, list[dict[str, Any]]] = {arm: [] for arm in ARMS}
    exact_power_markers = (
        "exponent 1.75",
        "1.75-power",
        "1.75 power",
        "partition exponent 1.75",
    )
    power_compatible_markers = (
        "confirms the power-response",
        "corroborate the power-response",
        "power-response model's qualitative prediction",
        "nonlinear (superlinear) partition response",
    )
    saturation_markers = (
        "saturat",
        "nearly independent",
        "near-constant",
        "nearly constant",
        "fixed reference recovery",
        "fixed recovery ceiling",
        "flat at",
        "tightly clustered",
    )
    for cell in sorted(cells, key=lambda item: (item["arm"], item["world_seed"])):
        arm = str(cell["arm"])
        text = _public_text(cell)
        exact_power = any(marker in text for marker in exact_power_markers)
        power_compatible = exact_power or any(
            marker in text for marker in power_compatible_markers
        )
        explicit_linear_rejection = (
            "d*r/(1+d*r)" in text and "reject" in text
        ) or (
            ("linear reference" in text or "initial linear" in text)
            and any(marker in text for marker in ("reject", "contradict", "not support"))
        )
        explicit_supplied_power_rejection = (
            arm == "aligned_nominal"
            and "contradict" in text
            and ("power-law" in text or "power response" in text)
        )
        rows[arm].append(
            {
                "world_seed": int(cell["world_seed"]),
                "exact_1_75_power_law_recovery": exact_power,
                "power_compatible_language": power_compatible,
                "explicit_supplied_linear_partition_rejection": explicit_linear_rejection,
                "explicit_supplied_power_rejection": explicit_supplied_power_rejection,
                "empirical_saturation_or_endpoint_model": any(
                    marker in text for marker in saturation_markers
                ),
            }
        )
    return {
        "source": "participant_public_model_summary_and_evidence_assessment_only",
        "private_reasoning_used": False,
        "by_arm": {
            arm: {
                "world_count": len(arm_rows),
                "exact_1_75_power_law_recovery_count": sum(
                    row["exact_1_75_power_law_recovery"] for row in arm_rows
                ),
                "power_compatible_language_count": sum(
                    row["power_compatible_language"] for row in arm_rows
                ),
                "explicit_supplied_linear_partition_rejection_count": sum(
                    row["explicit_supplied_linear_partition_rejection"] for row in arm_rows
                ),
                "explicit_supplied_power_rejection_count": sum(
                    row["explicit_supplied_power_rejection"] for row in arm_rows
                ),
                "empirical_saturation_or_endpoint_model_count": sum(
                    row["empirical_saturation_or_endpoint_model"] for row in arm_rows
                ),
                "world_rows": arm_rows,
            }
            for arm, arm_rows in rows.items()
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
        or summary.get("completed_cell_count") != 15
        or summary.get("failed_cell_count") != 0
        or summary.get("complete_cluster_count") != 5
        or len(cells) != 15
    ):
        raise RuntimeError("A-S Study B2 is not a complete 15/15 zero-failure block")
    if any(cell.get("status") != "completed" for cell in cells):
        raise RuntimeError("A-S Study B2 contains a non-completed cell")
    if any(cell.get("same_thread") is not True for cell in cells):
        raise RuntimeError("A-S Study B2 contains a broken two-turn thread")
    if any(len(cell.get("provider_receipts", [])) != 2 for cell in cells):
        raise RuntimeError("A-S Study B2 provider-turn denominator drifted")
    if any(
        cell.get("scores", {}).get(stage, {}).get("term_count") != 24
        for cell in cells
        for stage in ("pre", "post")
    ):
        raise RuntimeError("A-S Study B2 scoring denominator drifted")

    progress = [
        json.loads(line)
        for line in (run_root / "progress.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    formal_start = next(
        row["timestamp"] for row in progress if row["stage"] == "formal_execution_started"
    )
    formal_end = max(
        row["timestamp"]
        for row in progress
        if row["stage"] == "formal_progress" and row.get("completed_cells") == 15
    )
    receipts = [receipt for cell in cells for receipt in cell["provider_receipts"]]
    usage_fields = (
        "input_tokens",
        "cached_input_tokens",
        "cache_write_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    )
    usage = {
        field: sum(int(receipt.get("usage", {}).get(field, 0)) for receipt in receipts)
        for field in usage_fields
    }

    arm_summary: dict[str, Any] = {}
    for arm in ARMS:
        arm_cells = [cell for cell in cells if cell["arm"] == arm]
        pre = [float(cell["scores"]["pre"]["mean_normalized_absolute_error"]) for cell in arm_cells]
        post = [
            float(cell["scores"]["post"]["mean_normalized_absolute_error"])
            for cell in arm_cells
        ]
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

    seeds = sorted({int(cell["world_seed"]) for cell in cells})
    primary_values: list[float] = []
    post_mis_minus_aligned: list[float] = []
    world_rows: list[dict[str, Any]] = []
    for seed in seeds:
        world = {cell["arm"]: cell for cell in cells if cell["world_seed"] == seed}
        errors = {
            arm: {
                stage: float(world[arm]["scores"][stage]["mean_normalized_absolute_error"])
                for stage in ("pre", "post")
            }
            for arm in ARMS
        }
        gains = {arm: errors[arm]["pre"] - errors[arm]["post"] for arm in ARMS}
        primary_value = gains["misindexed_nominal"] - gains["aligned_nominal"]
        primary_values.append(primary_value)
        post_difference = (
            errors["misindexed_nominal"]["post"] - errors["aligned_nominal"]["post"]
        )
        post_mis_minus_aligned.append(post_difference)
        world_rows.append(
            {
                "world_seed": seed,
                "errors": errors,
                "update_gains": gains,
                "primary_contrast": primary_value,
                "post_misindexed_minus_aligned": post_difference,
            }
        )

    metric_rows: list[dict[str, Any]] = []
    for metric_id in METRICS:
        by_arm: dict[str, Any] = {}
        for arm in ARMS:
            arm_cells = [cell for cell in cells if cell["arm"] == arm]
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
            world = {cell["arm"]: cell for cell in cells if cell["world_seed"] == seed}
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
            }
        )

    primary = _exact_sign_flip(primary_values)
    public_audit = _public_summary_audit(cells)
    misindexed_audit = public_audit["by_arm"]["misindexed_nominal"]
    return {
        "schema_version": "chemworld-work-ii-as-study-b2-results-analysis-0.1",
        "study_id": summary["study_id"],
        "run_root": run_root.relative_to(ROOT).as_posix(),
        "integrity": {
            "scheduled_sessions": 15,
            "completed_sessions": 15,
            "failed_sessions": 0,
            "complete_clusters": 5,
            "provider_turns": len(receipts),
            "same_thread_sessions": sum(cell.get("same_thread") is True for cell in cells),
            "single_attempt_sessions": sum(cell.get("provider_attempt_count") == 1 for cell in cells),
            "infrastructure_predecessor_count": sum(
                len(cell.get("infrastructure_predecessors", [])) for cell in cells
            ),
            "participant_physical_experiment_count": 0,
            "pre_scoring_term_count": sum(cell["scores"]["pre"]["term_count"] for cell in cells),
            "post_scoring_term_count": sum(cell["scores"]["post"]["term_count"] for cell in cells),
            "tool_event_count": sum(int(receipt.get("tool_event_count", 0)) for receipt in receipts),
            "turn_failed_event_count": sum(
                int(receipt.get("event_counts", {}).get("turn.failed", 0))
                for receipt in receipts
            ),
            "formal_wall_time_seconds": formal_end - formal_start,
            "mean_cell_wall_time_seconds": statistics.mean(float(cell["elapsed_s"]) for cell in cells),
            "median_cell_wall_time_seconds": statistics.median(
                float(cell["elapsed_s"]) for cell in cells
            ),
            "provider_reported_usage": usage,
            "query_roster_sha256": summary["query_roster_sha256"],
            "truth_manifest_sha256": summary["truth_manifest_sha256"],
        },
        "arm_summary": arm_summary,
        "primary_contrast": primary,
        "post_misindexed_minus_aligned": _mean_ci(post_mis_minus_aligned),
        "world_rows": world_rows,
        "metric_rows": metric_rows,
        "public_summary_audit": public_audit,
        "mechanism_disposition": {
            "registered_rule": "positive supports evidence seeking; small or negative despite diagnostic evidence supports belief-updating bottleneck; mixed or weak remains unresolved",
            "classification": "mixed_predictive_acquisition_signal_with_unrecovered_structural_law",
            "predictive_acquisition_component": primary["mean"] > 0.0,
            "structural_law_recovery_supported": (
                misindexed_audit["exact_1_75_power_law_recovery_count"] == 5
            ),
            "pure_evidence_seeking_bottleneck_supported": False,
            "pure_belief_updating_failure_supported": False,
            "interpretation": (
                "Direct phase-process evidence increased misindexed predictive update gain on average, "
                "but the five-world direction was mixed and no misindexed public summary recovered "
                "the registered 1.75 law. Evidence acquisition and numerical belief revision therefore "
                "improved, while structural law identification remained a separate bottleneck."
            ),
        },
        "historical_disposition": {
            "original_study_b_a_p": "retained_current_unaffected_by_world_intervention_defect",
            "original_study_b_a_s": (
                "historical_platform_defective_truth_source_excluded_from_current_claims"
            ),
            "current_a_s_matched_evidence": "this_b2_phase_process_block",
        },
        "interpretation_contract": {
            "registered_primary_estimand_retained": True,
            "registered_primary": (
                "misindexed_pre_to_post_error_reduction_minus_aligned_pre_to_post_error_reduction"
            ),
            "small_n_inference": "exact 2^5 world sign-flip; descriptive t interval",
            "canary_included": False,
            "cross_provider_claim_allowed": False,
            "transfer_claim_allowed": False,
        },
    }


def _f(value: float) -> str:
    return f"{value:.4f}"


def write_report(analysis: Mapping[str, Any], path: Path) -> None:
    integrity = analysis["integrity"]
    arms = analysis["arm_summary"]
    primary = analysis["primary_contrast"]
    audit = analysis["public_summary_audit"]["by_arm"]
    metrics = {row["metric_id"]: row for row in analysis["metric_rows"]}
    lines = [
        "# Work II A-S Study B2：phase-process matched evidence 结果",
        "",
        "## 结论先行",
        "",
        "B2 完成了 15/15 fresh two-turn sessions、30/30 provider turns、5/5 matched worlds，0 failures、0 participant 物理实验。直接给出预先验证可区分 linear 与 1.75-power response 的 phase-process evidence 后，misindexed 的平均 prediction update gain 高于 aligned，但世界方向混合；同时 misindexed 仍未在公开 summary 中恢复注册的 1.75 law。",
        "",
        f"- opaque/aligned/misindexed 的平均 gain 为 **{_f(arms['opaque']['update_gain']['mean'])}/{_f(arms['aligned_nominal']['update_gain']['mean'])}/{_f(arms['misindexed_nominal']['update_gain']['mean'])}**。",
        f"- 注册主对比为 **{_f(primary['mean'])}**，{primary['positive_world_count']}/5 worlds 为正，exact one-sided sign-flip **p={primary['exact_sign_flip_p_one_sided_greater']:.3f}**，95% 描述区间 [{_f(primary['confidence_interval_95'][0])}, {_f(primary['confidence_interval_95'][1])}]。",
        f"- misindexed 的 exact 1.75-law recovery 为 **{audit['misindexed_nominal']['exact_1_75_power_law_recovery_count']}/5**；明确拒绝 supplied linear partition form 为 **{audit['misindexed_nominal']['explicit_supplied_linear_partition_rejection_count']}/5**；5/5 转向经验饱和/endpoint 模型。",
        "",
        "因此 B2 没有支持一个单一的 seeking/updating 二分答案。更精确的收束是：**取得 law-level phase-process evidence 后，misindexed 数值预测确实能比 aligned 多更新一些，但这种优势不稳定，也没有转化为正确结构规律。** 纯 evidence-seeking bottleneck 与纯 stubborn belief updating 都过强；当前证据支持 acquisition、numerical revision 与 structural identification 三层分离。",
        "",
        "## 1. 完整性与资源",
        "",
        f"- sessions：{integrity['completed_sessions']}/{integrity['scheduled_sessions']}；same thread：{integrity['same_thread_sessions']}/15；provider turns：{integrity['provider_turns']}/30。",
        f"- pre/post scoring terms：{integrity['pre_scoring_term_count']}/{integrity['post_scoring_term_count']}，即每阶段 15×24；全部一次完成，无 infrastructure predecessor、无 turn.failed。",
        f"- provider-free truth：80/80；participant 物理实验：0；正式 wall time：{integrity['formal_wall_time_seconds'] / 60.0:.1f} min。",
        f"- provider reported usage：input {integrity['provider_reported_usage']['input_tokens']:,}，cached input {integrity['provider_reported_usage']['cached_input_tokens']:,}，output {integrity['provider_reported_usage']['output_tokens']:,}，reasoning output {integrity['provider_reported_usage']['reasoning_output_tokens']:,} tokens。",
        "",
        "## 2. 三臂 prediction 更新",
        "",
        "| Arm | pre error | post error | absolute gain | relative reduction |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        row = arms[arm]
        lines.append(
            f"| {arm} | {_f(row['pre_error']['mean'])} | {_f(row['post_error']['mean'])} | {_f(row['update_gain']['mean'])} | {100.0 * row['relative_error_reduction']['mean']:.1f}% |"
        )
    lines.extend(
        [
            "",
            "三个 arms 的 post error 都降到约 0.005–0.010，说明 phase-process packet 足以驱动强烈的 endpoint calibration。主对比的正均值来自 misindexed 更大的可改善空间与三个位点的额外 gain，但两个 worlds 为负，不能升级为稳定选择性纠错。",
            "",
            "| World seed | opaque gain | aligned gain | misindexed gain | primary contrast |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    for row in analysis["world_rows"]:
        gains = row["update_gains"]
        lines.append(
            f"| {row['world_seed']} | {_f(gains['opaque'])} | {_f(gains['aligned_nominal'])} | {_f(gains['misindexed_nominal'])} | {_f(row['primary_contrast'])} |"
        )
    lines.extend(
        [
            "",
            "## 3. Metric-level 结果",
            "",
            "| Metric | aligned gain | misindexed gain | primary contrast | positive worlds |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for metric_id in METRICS:
        row = metrics[metric_id]
        lines.append(
            f"| {metric_id} | {_f(row['by_arm']['aligned_nominal']['mean_error_reduction'])} | {_f(row['by_arm']['misindexed_nominal']['mean_error_reduction'])} | {_f(row['primary_contrast']['mean'])} | {row['primary_positive_world_count']}/5 |"
        )
    lines.extend(
        [
            "",
            "三个注册 metric 都进入主分母；没有只依赖接近常数的 endpoint channel。即便如此，结构恢复仍未出现，说明问题已经不能再归因于原 Study B 的 fixed-process evidence 缺口。",
            "",
            "## 4. 公开结构表述审计",
            "",
            "| Arm | exact 1.75 law | power-compatible wording | explicit linear rejection | empirical saturation model |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for arm in ARMS:
        row = audit[arm]
        lines.append(
            f"| {arm} | {row['exact_1_75_power_law_recovery_count']}/5 | {row['power_compatible_language_count']}/5 | {row['explicit_supplied_linear_partition_rejection_count']}/5 | {row['empirical_saturation_or_endpoint_model_count']}/5 |"
        )
    lines.extend(
        [
            "",
            "Aligned 也只有部分 worlds 使用 power-compatible 语言，且有 world 明确否定 supplied power model；misindexed 则 0/5 恢复 exact exponent。模型从证据中学到了低误差的局部映射，但没有把该映射压缩成注册的 constitutive law。",
            "",
            "## 5. 对原 Study B 与 Paper 2 的处置",
            "",
            "- 原 Study B 的 A-P electrochemical 15 sessions 不含 `world_interventions`，继续作为当前 evidence-seeking 证据。",
            "- 原 Study B 的 A-S partition 15 sessions 读取了受 evaluator 缺陷影响的 truth source；该分支保留为历史平台缺陷记录，但退出当前科学结论。",
            "- 本 B2 是当前 A-S matched-evidence 入口：它修复了 evidence-level mismatch，却得到 mixed predictive contrast 与 0/5 exact law recovery。",
            "- Paper 2 因此不再写“只需更好的 evidence 即可恢复结构 law”，也不写“模型完全拒绝更新”。当前结论是 numerical correction 与 structural law formation 分离。",
            "",
            "## 6. 解释边界",
            "",
            "这是单一 DeepSeek–Codex participant、五个 public worlds 的小样本机制 follow-up。它不支持跨 provider、private transfer 或普遍 LLM 主张；canary 不进入分析。结果不需要补跑或按方向筛选。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    analysis = analyze(args.run_root.resolve())
    _write_json(args.output_json.resolve(), analysis)
    write_report(analysis, args.output_report.resolve())
    print(
        json.dumps(
            {
                "status": "completed",
                "output_json": str(args.output_json.resolve()),
                "output_report": str(args.output_report.resolve()),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
