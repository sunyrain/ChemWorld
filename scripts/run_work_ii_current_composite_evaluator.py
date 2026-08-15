#!/usr/bin/env python3
# ruff: noqa: RUF001
"""Evaluate the terminal DeepSeek public C2 composite without provider calls."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_current_composite import (
    execute_current_composite_evaluator,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_RUN = ROOT / "runs/formal/work-ii-deepseek-c2-public-v0.2-20260814"
DEFAULT_REPLACEMENT_RUN = ROOT / (
    "runs/formal/"
    "work-ii-deepseek-c2-as-crystallization-resource-recovery-v0.2-20260815"
)
DEFAULT_ANALYSIS_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.2.json"
DEFAULT_FORMAL_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
DEFAULT_RAW_OUTPUT = ROOT / (
    "runs/formal/"
    "work-ii-deepseek-c2-current-composite-evaluator-v0.2-20260815"
)
DEFAULT_REPORT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
DEFAULT_MARKDOWN = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_EVALUATION_V0.2_ZH.md"
)


def _number(value: Any, digits: int = 4) -> str:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return "NA"
    return f"{float(value):.{digits}f}"


def _primary_inference(gate: Mapping[str, Any]) -> Mapping[str, Any]:
    components = gate.get("components")
    if isinstance(components, Mapping):
        primary = components.get("H3_primary_contrast")
        if isinstance(primary, Mapping):
            return primary
    inference = gate.get("inference")
    if isinstance(inference, Mapping):
        return inference
    raise ValueError("locus gate lacks a primary H3 inference")


def _render_markdown(report: Mapping[str, Any]) -> str:
    denominators = report["denominators"]
    prediction = report["prediction_correction"]
    laws = report["executable_law"]
    blind = report["blind_action"]
    lines = [
        "# Work II DeepSeek C2 current-composite 评估",
        "",
        (
            "本报告把修复后的 A-S crystallization 完整替换块与其余 public participant "
            "结果组合，完成 provider-free 的科学纠错、规律恢复和 blind action 评估。"
        ),
        "",
        "## 完整分母",
        "",
        f"- Participant cells：**{denominators['cell_count']}**；matched worlds："
        f"**{denominators['cluster_count']}**。",
        (
            "- Participant 终态："
            + "，".join(
                f"{key}={value}"
                for key, value in denominators["terminal_state_counts"].items()
            )
            + "。"
        ),
        (
            "- Held-out truth："
            f"**{denominators['truth_completed_execution_count']}/"
            f"{denominators['truth_scheduled_execution_count']}**；checkpoint："
            f"**{denominators['checkpoint_scored_count']}/"
            f"{denominators['checkpoint_scheduled_count']}**。"
        ),
        (
            "- Final typed law："
            f"**{denominators['law_summary_evaluated_count']}/"
            f"{denominators['law_summary_scheduled_count']}**；blind executions："
            f"**{denominators['blind_completed_execution_count']}/"
            f"{denominators['blind_scheduled_execution_count']}**，其中未启动 "
            f"**{denominators['blind_unstarted_execution_count']}** 次属于 participant "
            "失败/右删失的预定分母。"
        ),
        "- Evaluator provider calls：**0**。",
        "",
        "## 科学纠错",
        "",
        "| Locus | failure-aware contrast | lower bound | p value | "
        "observed-point contrast | gate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for locus, result in prediction["locus_results"].items():
        gate = result["gate"]
        p_value = gate.get(
            "intersection_union_p_value",
            gate.get("effective_intersection_union_p_value"),
        )
        primary = _primary_inference(gate)
        observed_primary = _primary_inference(result["observed_point_sensitivity_gate"])
        lines.append(
            f"| {locus} | {_number(primary['estimate'])} | "
            f"{_number(primary['one_sided_95pct_lower_bound'])} | "
            f"{_number(p_value, 6)} | {_number(observed_primary['estimate'])} | "
            f"{gate['passed']} |"
        )
    c2 = prediction["C2_intersection_union"]
    lines.extend(
        [
            "",
            (
                "Public C2 要求三个 locus 同时通过；当前 intersection-union 决策为 "
                f"**{c2['passed']}**，整体 p value 为 "
                f"**{_number(c2['intersection_union_p_value'], 6)}**。"
            ),
            "",
            (
                "三个 locus 均存在从 pre 到 final 的平均预测误差下降，但注册检验要求"
                "错误先验相对正确先验获得更强修复。A-E 的 aligned noninferiority 通过，"
                "而 misindexed selective-improvement component 不通过；A-P 两任务方向均为正，"
                "但证据只达到 suggestive；A-S 中 crystallization 的局部信号被 partition 的"
                "负方向抵消。观察点敏感性仍不通过。"
            ),
            "",
            "| Locus | Opaque pre→final | Aligned pre→final | Misindexed pre→final |",
            "|---|---:|---:|---:|",
        ]
    )
    for locus in ("A_E", "A_P", "A_S"):
        by_arm = prediction["locus_results"][locus]["by_arm"]
        lines.append(
            f"| {locus} | {_number(by_arm['opaque']['mean_primary_improvement'])} | "
            f"{_number(by_arm['aligned_nominal']['mean_primary_improvement'])} | "
            f"{_number(by_arm['misindexed_nominal']['mean_primary_improvement'])} |"
        )
    lines.extend(
        [
            "",
            "所以当前最重要的区分是：**general prediction learning 存在，但 targeted "
            "wrong-model repair 未被支持。**",
            "",
            "## 规律恢复",
            "",
            "| Locus | evaluated laws | law MAE | pre→law improvement | law−final error |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for locus in ("A_E", "A_P", "A_S", "overall"):
        row = laws[locus]["all"]
        lines.append(
            f"| {locus} | {row['evaluated_count']}/{row['cell_count']} | "
            f"{_number(row['mean_normalized_mae'])} | "
            f"{_number(row['mean_pre_to_law_improvement'])} | "
            f"{_number(row['mean_summary_minus_final_error'])} |"
        )
    law_overall = laws["overall"]["all"]
    law_equal = (
        law_overall["evaluated_count"]
        - law_overall["law_better_than_final_prediction_count"]
        - law_overall["law_worse_than_final_prediction_count"]
    )
    lines.extend(
        [
            "",
            (
                "135 条规律全部可以执行，但与 final explicit predictions 相比，law "
                f"更好/相等/更差为 **{law_overall['law_better_than_final_prediction_count']}"
                f"/{law_equal}/{law_overall['law_worse_than_final_prediction_count']}**。"
                "可执行性与高保真规律压缩因此必须分开。"
            ),
            "",
            "## Blind action",
            "",
            "| Locus | evaluable cells | blind executions | mean gain | better/equal/worse |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for locus in ("A_E", "A_P", "A_S", "overall"):
        row = blind[locus]
        lines.append(
            f"| {locus} | {row['completed_blind_cell_count']}/"
            f"{row['assigned_cell_count']} | {row['completed_execution_count']}/"
            f"{row['scheduled_execution_count']} | "
            f"{_number(row['mean_recommendation_gain_over_incumbent'])} | "
            f"{row['recommendation_better_count']}/"
            f"{row['recommendation_equivalent_count']}/"
            f"{row['recommendation_worse_count']} |"
        )
    lines.extend(
        [
            "",
            (
                "14 个 participant failed/right-censored cells 对应的 84 次 replay 按既定"
                "规则未启动，不被填成失败或零增益。当前 action 层证明的是重放稳定性，"
                "不是新方案发现。"
            ),
            "",
            "## Evaluator 实现与缺陷修复",
            "",
            (
                "- Evaluator 直接绑定 120 个未受平台缺陷影响的 public cells 与 15 个完整 "
                "A-S crystallization replacement cells，不混入 superseded block。"
            ),
            (
                "- v0.1 truth/blind 路径未把冻结的 `world_interventions` 传入 runtime 与 "
                "exact replay；v0.2 在新输出根从第一单元完整重跑，旧结果仅保留为历史缺陷证据。"
            ),
            (
                "- A-S partition 的合法 evaluator query 可将 `settle_duration_s` 外推到 "
                "participant 搜索框之外。Truth compiler 已按物理 runtime domain 直接编译，"
                "4 个外推 query 未 clip、未删除。"
            ),
            "- 该修复不改变 participant 数据、注册 query、统计分母或判定阈值。",
            "",
            "## 解释边界",
            "",
            (
                "这是当前 public DeepSeek cohort 的完整 evaluator 闭环，也是更大研究计划的"
                "第一阶段证据；它不等于整篇 Paper 2 已完成。Private transfer、跨 provider "
                "复现和新的开放式实验设计均未由本报告回答。所有 participant 失败、"
                "右删失和未启动 blind 分母均被保留。"
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _progress_writer(path: Path | None) -> Callable[[Mapping[str, Any]], None]:
    def emit(payload: Mapping[str, Any]) -> None:
        rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        print(rendered, flush=True)

    return emit


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-run", type=Path, default=DEFAULT_BASE_RUN)
    parser.add_argument("--replacement-run", type=Path, default=DEFAULT_REPLACEMENT_RUN)
    parser.add_argument("--analysis-plan", type=Path, default=DEFAULT_ANALYSIS_PLAN)
    parser.add_argument("--formal-design", type=Path, default=DEFAULT_FORMAL_DESIGN)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_RAW_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Validate existing truth/blind units and execute only missing units.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.preflight and args.resume:
        raise ValueError("--preflight and --resume are mutually exclusive")
    report_path = args.report.resolve()
    markdown_path = args.markdown.resolve()
    if not args.preflight:
        for path in (report_path, markdown_path):
            if path.exists():
                raise FileExistsError(f"refusing to overwrite tracked result: {path}")
    result = execute_current_composite_evaluator(
        ROOT,
        base_run=args.base_run.resolve(),
        replacement_run=args.replacement_run.resolve(),
        analysis_plan_path=args.analysis_plan.resolve(),
        formal_design_path=args.formal_design.resolve(),
        output_root=args.output_root.resolve(),
        resume=bool(args.resume),
        preflight_only=bool(args.preflight),
        progress=_progress_writer(
            args.progress_file.resolve() if args.progress_file is not None else None
        ),
    )
    if args.preflight:
        print(
            json.dumps(
                {
                    "event": "current_composite_preflight",
                    "status": result["status"],
                    "roster": result["roster"],
                    "provider_call_count": result["provider_call_count"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0 if result["status"] == "passed" else 1
    write_json_atomic(report_path, result)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_render_markdown(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "event": "current_composite_outputs_written",
                "status": result["status"],
                "report": str(report_path),
                "markdown": str(markdown_path),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
