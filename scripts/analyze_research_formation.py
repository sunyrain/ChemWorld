"""Descriptive, read-only analysis of the fixed 48-session research-formation block."""

# ruff: noqa: RUF001 -- Chinese report prose.
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from statistics import fmean

from scripts.report_paper_case_stability import describe
from scripts.run_paper_case_notebooks import case_folder, read, write

METRICS = {
    "EQ": (
        "all_twelve_macro_mae",
        "lowest_three_macro_mae",
        "remaining_nine_macro_mae",
        "lowest_three_coverage80",
        "sampled_below_1mM",
        "minimum_positive_concentration_M",
        "pH_normalized_mean_width80",
        "acid_dissociation_fraction_mean_width80",
        "precipitation_signal_mean_width80",
    ),
    "C": (
        "crystal_yield_mae",
        "crystal_purity_mae",
        "crystal_size_mae",
        "crystal_fines_fraction_mae",
        "purity_signed_error",
        "quality_correct_of_12",
        "recommendation_true_crystal_yield",
        "recommendation_quality_feasible",
        "recommendation_quality_and_yield_target",
        "thermal_fines_direction_correct",
        "thermal_fines_absolute_delta_error",
    ),
}
LABELS = {
    "all_twelve_macro_mae": "全部 12 题平均 MAE",
    "lowest_three_macro_mae": "最低浓度三题 MAE",
    "remaining_nine_macro_mae": "其余九题 MAE",
    "lowest_three_coverage80": "最低浓度三题区间覆盖",
    "sampled_below_1mM": "源研究进入 1 mM 以下（比例）",
    "minimum_positive_concentration_M": "最低正浓度（M）",
    "pH_normalized_mean_width80": "pH 区间平均宽度",
    "acid_dissociation_fraction_mean_width80": "解离率区间平均宽度",
    "precipitation_signal_mean_width80": "沉淀信号区间平均宽度",
    "crystal_yield_mae": "回收率 MAE",
    "crystal_purity_mae": "纯度 MAE",
    "crystal_size_mae": "粒径 MAE",
    "crystal_fines_fraction_mae": "细粉比例 MAE",
    "purity_signed_error": "纯度有符号误差（预测减参考）",
    "quality_correct_of_12": "质量分类正确数 /12",
    "recommendation_true_crystal_yield": "推荐复测真实回收率",
    "recommendation_quality_feasible": "推荐复测满足质量条件（比例）",
    "recommendation_quality_and_yield_target": "推荐同时满足质量及回收率 ≥0.10（比例）",
    "thermal_fines_direction_correct": "热历史细粉方向正确（比例）",
    "thermal_fines_absolute_delta_error": "热历史细粉差值绝对误差",
}


def contrasts(rows, design):
    """World means have equal weight; missing sessions are never filled with zero."""
    output = {}
    for system, metrics in METRICS.items():
        worlds = sorted({c["world"] for c in design["cases"] if c["system"] == system})
        output[system] = {}
        for metric in metrics:
            world_rows = []
            for world in worlds:
                arms = {}
                for arm in ("Opaque", "Aligned"):
                    group = [
                        r
                        for r in rows
                        if (r["system"], r["world"], r["arm"]) == (system, world, arm)
                    ]
                    values = [r["measurements"].get(metric) for r in group]
                    arms[arm] = {**describe(values), "values": values}
                a, o = arms["Aligned"]["mean"], arms["Opaque"]["mean"]
                world_rows.append(
                    {
                        "world": world,
                        **arms,
                        "delta_aligned_minus_opaque": a - o
                        if a is not None and o is not None
                        else None,
                        "all_six_observed": all(arms[arm]["observed"] == 3 for arm in arms),
                    }
                )
            deltas = [r["delta_aligned_minus_opaque"] for r in world_rows]
            output[system][metric] = {
                "worlds": world_rows,
                "equal_world_means": {
                    arm: describe([r[arm]["mean"] for r in world_rows])
                    for arm in ("Opaque", "Aligned")
                },
                "world_mean_differences": describe(deltas),
                "aligned_lower_worlds": sum(d is not None and d < 0 for d in deltas),
                "equal_worlds": sum(d == 0 for d in deltas),
                "aligned_higher_worlds": sum(d is not None and d > 0 for d in deltas),
                "complete_worlds": sum(r["all_six_observed"] for r in world_rows),
            }
    return output


def enrich(row, root, unit):
    row["measurements"] = dict(row["measurements"])
    if unit["system"] != "C":
        return row
    quality = row["crystallization_quality"]
    feasible = quality["recommended_retest_feasible"]
    recovery = row["measurements"].get("recommendation_true_crystal_yield")
    row["measurements"]["recommendation_quality_feasible"] = (
        int(feasible) if feasible is not None else None
    )
    row["measurements"]["recommendation_quality_and_yield_target"] = (
        int(feasible and recovery >= 0.1) if feasible is not None and recovery is not None else None
    )
    evaluation = row["prediction_evaluation"] or {}
    if evaluation.get("valid"):
        reference = read(root / "references" / f"C-{unit['world']}" / "result.json")
        queries = read(root / unit["repeat"] / "C/design.json")["queries"]
        truth = dict(zip((q["query_id"] for q in queries), reference["truth"], strict=True))
        predictions = row["posttests"]["Q"]["payload"]["predictions"]
        for metric in ("crystal_purity", "crystal_yield", "crystal_size", "crystal_fines_fraction"):
            name = "purity_signed_error" if metric == "crystal_purity" else f"{metric}_signed_error"
            row["measurements"][name] = fmean(
                q[metric]["estimate"] - truth[q["query_id"]][metric] for q in predictions
            )
            row["measurements"][f"{metric}_mean_width80"] = evaluation["metrics"][metric][
                "interval_width"
            ]
        row["purity_detail"] = {
            "source_public": describe(
                [b["metrics"].get("crystal_purity") for b in row["batch_outcomes"]]
            ),
            "query_truth": describe([r["crystal_purity"] for r in truth.values()]),
            "query_predictions": describe([q["crystal_purity"]["estimate"] for q in predictions]),
        }
    return row


def note_timeline(root, unit, row):
    """Structural timing only; do not grade scientific content using keywords."""
    folder = case_folder(root / unit["repeat"], unit)
    trace = folder / "trajectory.jsonl"
    records = []
    if trace.exists():
        import json

        records = [
            json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines() if line
        ]
    revisions = []
    for revision in row["notebook"]["versions"]:
        available = records[: revision["public_cursor"]["event_count"]]
        revisions.append(
            {
                "revision": revision["revision"],
                "recorded_at": revision["recorded_at"],
                "public_operations": revision["public_cursor"]["event_count"],
                "completed_batches_available": sum(
                    r.get("instrument") == "final_assay"
                    and r.get("transaction_status") == "committed"
                    for r in available
                ),
            }
        )
    return {
        "repeat": unit["repeat"],
        "id": unit["id"],
        "revisions": revisions,
        "has_mid_source_revision": any(
            0 < v["completed_batches_available"] < 12 for v in revisions
        ),
    }


def analyze(root, reports, output, *, allow_partial=False):
    design = read(root / "design.json")
    state = read(root / "summary.json")
    if not allow_partial and (state["terminal_sources"] != 48 or state["active_units"]):
        raise ValueError("Final analysis requires 48 terminal sources and no active units")
    rows, timelines = [], []
    for unit in design["schedule"]:
        path = reports / unit["repeat"] / f"{unit['id']}.json"
        if path.exists():
            row = enrich(read(path), root, unit)
            timelines.append(note_timeline(root, unit, row))
        else:
            row = {**unit, "status": "pending", "measurements": {}}
        rows.append(row)
    terminal = [r for r in rows if r["status"] != "pending"]
    if not allow_partial and len(terminal) != 48:
        raise ValueError("Wait for the final exporter: not all 48 records are available")
    failures = [
        {
            "repeat": r["repeat"],
            "id": r["id"],
            "status": r["status"],
            "failure": r["failure"],
            "missing_stages": r["missing_stages"],
            "posttest_failures": {
                s: t.get("failure") for s, t in r["posttests"].items() if t.get("failure")
            },
            "posttest_validation": r["posttest_validation"],
        }
        for r in terminal
        if r["status"] != "completed"
    ]
    counters = {
        "planned_sources": 48,
        "terminal_sources": len(terminal),
        "complete_chains": sum(r["status"] == "completed" for r in terminal),
        "completed_source_batches": sum(r["completed_batches"] for r in terminal),
        "valid_Q": sum(bool((r["prediction_evaluation"] or {}).get("valid")) for r in terminal),
        "sealed_stages": sum(len(r["sealed_stages"]) for r in terminal),
        "source_replays": sum(bool((r["exact_replay"] or {}).get("verified")) for r in terminal),
        "source_operations": sum(r["operations"] for r in terminal),
        "source_rollbacks": sum(len(r["rollbacks"]) for r in terminal),
        "retest_batches": sum(len(r["retest_batch_metrics"]) for r in terminal),
        "retest_replays": sum(
            bool(r["retest"]["exact_replay"] and r["retest"]["exact_replay"].get("verified"))
            for r in terminal
        ),
        "retest_operations": sum(r["retest_operations"] for r in terminal),
        "notebook_versions": sum(r["notebook"]["version_count"] for r in terminal),
        "notebook_reads": sum(r["notebook"]["read_calls"] for r in terminal),
        "notebook_tool_failures": sum(r["notebook"]["tool_failures"] for r in terminal),
        "initial_notes_before_actions": sum(
            r["notebook"]["initial_note_before_action"] is True for r in terminal
        ),
        "missing_notebooks": sum(r["notebook"]["version_count"] == 0 for r in terminal),
        "sessions_with_mid_source_revision": sum(t["has_mid_source_revision"] for t in timelines),
        "notebook_cursor_failures": sum(
            not v["cursor_valid"] for r in terminal for v in r["notebook"]["validation"]
        ),
        "reviewed_reference_failures": sum(
            not v["reviewed_reference_valid"] for r in terminal for v in r["notebook"]["validation"]
        ),
        "unavailable_event_citations": sum(
            len(v["unavailable_event_citations"])
            for r in terminal
            for v in r["notebook"]["validation"]
        ),
        "complete_token_accounts": sum(r["token_accounting"]["complete"] for r in terminal),
        "observed_input_plus_output_tokens": sum(
            (r["token_accounting"].get("total") or {}).get("input_plus_output", 0) for r in terminal
        ),
        "laboratory_tool_failures": sum(
            (r["source_usage"] or {}).get("recovered_mcp_tool_failure_count", 0) for r in terminal
        ),
        "source_provider_process_attempts": sum(
            (r["source_usage"] or {}).get("provider_process_attempt_count", 0) for r in terminal
        ),
    }
    analysis = {
        "scope": "48 fresh sessions, current core, O/A contrast within fixed worlds",
        "provisional": len(terminal) != 48,
        "source_commit": design["source_commit"],
        "counts": counters,
        "reference": read(root / "references/complete.json"),
        "failures": failures,
        "world_contrasts": contrasts(rows, design),
        "condition_variability": {
            cell["id"]: {
                name: describe([r["measurements"].get(name) for r in rows if r["id"] == cell["id"]])
                for name in METRICS[cell["system"]]
            }
            for cell in design["cases"]
        },
        "note_timelines": timelines,
        "cases": [
            {k: v for k, v in r.items() if k not in {"batch_outcomes", "posttests"}} for r in rows
        ],
        "status_counts": dict(Counter(r["status"] for r in rows)),
    }
    write(output / "analysis.json", analysis)
    render_report(analysis, output)
    return analysis


def num(value):
    return "—" if value is None else f"{value:.5g}"


def stat(value):
    return (
        f"{num(value['mean'])} ± {num(value['sample_sd'])} ({value['observed']}/{value['planned']})"
    )


def render_report(analysis, output):
    n = analysis["counts"]
    lines = [
        "# 48 场自主研究：定量分析",
        "",
        "**中途预览，不能据此选择后续实验或提前作整体结论。**"
        if analysis["provisional"]
        else "固定实验块已结束；全部结果与失败保留，旧研究不进入本块均值。",
        "",
        f"完整链 {n['complete_chains']}/48；终态 {n['terminal_sources']}/48；源批次 "
        f"{n['completed_source_batches']}/576；有效 Q {n['valid_Q']}/48；"
        f"有效封存阶段 {n['sealed_stages']}/174。",
        "",
        "## 统计单位与读法",
        "",
        "每个世界 × 信息条件有三次新会话。下表为会话均值 ± 样本 SD，括号为实际/计划会话数；"
        "总览对世界等权。Δ 为 Aligned 减 Opaque，误差指标负值表示 Aligned 较低。"
        "三次会话描述波动，不构成稳定总体成功率；试题、批次和参考噪声重复不充当 Agent 重复。"
        "缺失不按零计；世界真值、当时证据支持和模型公开判断需要分别解释。",
        "",
    ]
    for system, metrics in analysis["world_contrasts"].items():
        lines += [
            f"## {system}：按世界比较",
            "",
            "| 指标 | 世界 | Opaque 均值 ± SD (n/3) | Aligned 均值 ± SD (n/3) | Δ A−O |",
            "| --- | --- | --- | --- | ---: |",
        ]
        for name, result in metrics.items():
            for world in result["worlds"]:
                lines.append(
                    f"| {LABELS[name]} | {world['world']} | {stat(world['Opaque'])} | "
                    f"{stat(world['Aligned'])} | {num(world['delta_aligned_minus_opaque'])} |"
                )
        lines += [
            "",
            "### 世界等权总览",
            "",
            "| 指标 | Opaque | Aligned | Δ A−O | A 较低/相同/较高世界 | 完整世界 |",
            "| --- | ---: | ---: | ---: | --- | ---: |",
        ]
        for name, result in metrics.items():
            means = result["equal_world_means"]
            lines.append(
                f"| {LABELS[name]} | {num(means['Opaque']['mean'])} | "
                f"{num(means['Aligned']['mean'])} | "
                f"{num(result['world_mean_differences']['mean'])} | "
                f"{result['aligned_lower_worlds']}/{result['equal_worlds']}/"
                f"{result['aligned_higher_worlds']} | "
                f"{result['complete_worlds']}/{len(result['worlds'])} |"
            )
        lines += [""]
    lines += [
        "## 记录覆盖与执行结果",
        "",
        f"笔记 {n['notebook_versions']} 版；"
        f"初始笔记早于物理操作 {n['initial_notes_before_actions']}/"
        f"{n['terminal_sources']}；源研究途中有更新的会话 {n['sessions_with_mid_source_revision']}/"
        f"{n['terminal_sources']}；主动回读 {n['notebook_reads']} 次；"
        f"无笔记 {n['missing_notebooks']} 场。",
        "",
        "中途更新仅指已完成 1–11 批时发生一次版本提交，是记录可用性而非学习质量评分。"
        "开始与结束各一版不能定位判断在源研究中途的具体变化；后測报告不倒填为同期理由。",
        "",
        f"源回放 {n['source_replays']}/{n['terminal_sources']}；操作 {n['source_operations']}，"
        f"其中回滚 {n['source_rollbacks']}；"
        f"参考 {analysis['reference']['completed_batches']}/336 批、"
        f"{analysis['reference']['trajectories']}/28 条回放；推荐复测 {n['retest_batches']} 批、"
        f"{n['retest_replays']} 条回放。",
        "",
        f"笔记工具失败 {n['notebook_tool_failures']}；"
        f"实验室工具失败 {n['laboratory_tool_failures']}；"
        f"笔记游标异常 {n['notebook_cursor_failures']}；reviewed-through 异常 "
        f"{n['reviewed_reference_failures']}；"
        f"当时不可用事件引用 {n['unavailable_event_citations']}。",
        "",
        f"完整 token 账目 {n['complete_token_accounts']}/{n['terminal_sources']}；已知输入+输出 "
        f"{n['observed_input_plus_output_tokens']:,} tokens"
        "（缓存输入包含在输入中，不重复加算）；费用未知。",
        "",
        "## 保留失败",
        "",
    ]
    if analysis["failures"]:
        for row in analysis["failures"]:
            lines += [
                f"- {row['repeat']} / {row['id']}：{row['status']}；"
                f"缺失或无效阶段 {', '.join(row['missing_stages']) or '无'}；"
                f"原因详见同名 JSON。"
            ]
    else:
        lines += ["当前已结束会话没有不完整链；操作回滚和工具错误仍按上文保留。"]
    lines += [
        "",
        "## 解释边界",
        "",
        "EQ 误差对五次观测参考的均值计算，覆盖按原参考观测计算；浓度统计只纳入成功提交的"
        "普通 reagent/solvent 加料，component 替换不当作零浓度。C 原指标对保留参考真值计算，"
        "源笔记看到的是带噪公共读数。新增纯度有符号误差和记录时点汇总属于事后描述性分析。",
        "",
        "推荐满足纯度/细粉条件与达到回收率 0.10 目标分开报告；近零回收的种晶不能被表述为"
        "成功发现有效回收工艺。源研究成功、关系得到支持和未见条件预测准确也分别解释。",
        "",
        "没有无笔记对照、模型更换、强制纠错条件或受控早期历史分支。因此不由这些结果宣称"
        "笔记带来能力提升、某段文字造成后续选择，或特定自我确认机制已得到因果证实。",
        "",
        "逐场模型原文见 [REPORT.md](REPORT.md)；机器数值见 [analysis.json](analysis.json)。",
        "",
    ]
    (output / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    result = analyze(args.root, args.reports, args.output, allow_partial=args.allow_partial)
    print(result["counts"], flush=True)


if __name__ == "__main__":
    main()
