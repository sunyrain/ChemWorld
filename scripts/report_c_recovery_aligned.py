"""Read-only scientific export of the corrected-definition 45-session C cohort."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import time
from collections import Counter
from pathlib import Path

from scripts.analyze_inquiry_trajectories import extract, parse_notes, timeline
from scripts.analyze_research_formation import LABELS, METRICS, enrich, num, stat
from scripts.report_paper_case_stability import describe
from scripts.report_research_extension import counts
from scripts.report_research_formation import export_case
from scripts.run_c_recovery_aligned import MODE, schedule
from scripts.run_paper_case_notebooks import case_folder, emit, read, write

ARMS = ("Opaque", "Aligned", "MisIndexed")
COHORT = "corrected_recovery_45"
QUANTITIES = ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction")
REPORT_METRICS = (
    *METRICS["C"],
    "quality_balanced_accuracy",
    *(f"{name}_coverage80" for name in QUANTITIES),
    *(f"{name}_mean_width80" for name in QUANTITIES),
)


def reference_quality_profile(truth):
    positive = sum(
        r["particles_present"] and r["crystal_purity"] >= 0.8 and r["crystal_fines_fraction"] <= 0.5
        for r in truth
    )
    return {
        "queries": len(truth),
        "quality_feasible": positive,
        "quality_infeasible": len(truth) - positive,
        "always_feasible_correct": positive,
        "always_infeasible_correct": len(truth) - positive,
    }


def grouped_metrics(rows):
    """Retain missing sessions and average world means with equal weight."""
    output = {}
    for metric in REPORT_METRICS:
        worlds = []
        for world in (f"W{i:02d}" for i in range(1, 6)):
            groups = {}
            for arm in ARMS:
                values = [
                    r["measurements"].get(metric)
                    for r in rows
                    if r["world"] == world and r["arm"] == arm
                ]
                groups[arm] = {**describe(values), "values": values}
            worlds.append({"world": world, **groups})
        output[metric] = {
            "worlds": worlds,
            "equal_world_means": {a: describe([w[a]["mean"] for w in worlds]) for a in ARMS},
            "session_values": {
                a: describe([r["measurements"].get(metric) for r in rows if r["arm"] == a])
                for a in ARMS
            },
        }
    return output


def source_timeline(row, root, output):
    folder = case_folder(root / row["repeat"], row)
    if (folder / "trajectory.jsonl").exists():
        return extract(row, output, {COHORT: root})
    if row["operations"] or row["completed_batches"]:
        raise ValueError("Missing trajectory for a nonempty source")
    # A provider failure before any action is a retained unit, not a missing source.
    note = output / row["repeat"] / f"{row['id']}-notebook.md"
    return {
        "repeat": row["repeat"],
        "id": row["id"],
        "status": row["status"],
        "failure": row["failure"],
        "cohort": COHORT,
        "versions": timeline(row, [], parse_notes(note)),
        "events": [],
        "batches": [],
        "metrics": {
            "source_operations": 0,
            "completed_batches": 0,
            "structural_feedback_opportunities": 0,
            "rejected_attempts": 0,
        },
        "source_checks": {"empty_source_retained": True},
    }


def build(root, output, *, require_complete=False):
    design = read(root / "design.json")
    if design["mode"] != MODE or design["schedule"] != schedule():
        raise ValueError("Not the fixed corrected-recovery 45-session block")
    output.mkdir(parents=True, exist_ok=True)
    rows, trajectories = [], []
    for unit in design["schedule"]:
        result = root / unit["repeat"] / "results" / f"{unit['id']}.json"
        if not result.exists():
            rows.append(
                {
                    **unit,
                    "cohort": COHORT,
                    "status": "pending",
                    "measurements": {},
                    "completed_batches": 0,
                    "sealed_stages": [],
                }
            )
            continue
        row = export_case(root, unit, output)
        row["cohort"] = COHORT
        enrich(row, root, unit)
        evaluation = row["prediction_evaluation"] or {}
        row["measurements"]["quality_balanced_accuracy"] = (
            evaluation.get("quality", {}).get("balanced_accuracy")
            if evaluation.get("valid")
            else None
        )
        trajectory = source_timeline(row, root, output)
        row["trajectory_metrics"] = trajectory["metrics"]
        write(output / "sessions" / unit["repeat"] / f"{unit['id']}.json", trajectory)
        write(output / unit["repeat"] / f"{unit['id']}.json", row)
        rows.append(row)
        trajectories.append(trajectory)
    total = counts(rows)
    terminal = [r for r in rows if r["status"] != "pending"]
    total["sessions_with_feedback_windows"] = sum(
        t["metrics"]["structural_feedback_opportunities"] > 0 for t in trajectories
    )
    total["structural_feedback_windows"] = sum(
        t["metrics"]["structural_feedback_opportunities"] for t in trajectories
    )
    result = {
        "scope": MODE,
        "source_commit": design["source_commit"],
        "experiment_note": design["experiment_note"],
        "recovery_definition": design["recovery_definition"],
        "provisional": len(terminal) != 45,
        "counts": total,
        "reference": read(root / "references/complete.json"),
        "status_counts": dict(Counter(r["status"] for r in rows)),
        "by_arm": {a: counts([r for r in rows if r["arm"] == a]) for a in ARMS},
        "metrics": grouped_metrics(rows),
        "reference_quality_profiles": {
            f"W{w:02d}": reference_quality_profile(
                read(root / "references" / f"C-W{w:02d}" / "result.json")["truth"]
            )
            for w in range(1, 6)
        },
        "failures": [
            {
                k: r.get(k)
                for k in (
                    "repeat",
                    "id",
                    "status",
                    "failure",
                    "missing_stages",
                    "posttest_validation",
                    "token_accounting",
                )
            }
            for r in terminal
            if r["status"] != "completed"
        ],
        "cases": [
            {k: v for k, v in r.items() if k not in {"posttests", "batch_outcomes"}} for r in rows
        ],
        "limitations": [
            "Fresh model sessions; model sampling RNG cannot be fixed.",
            "Corrected protocol, not a randomized prompt-correction effect estimate.",
            "Source batches, queries and windows are nested within sessions/worlds.",
            "Old 90-session results and failures remain; no replacement or denominator pooling.",
            "Timelines establish public evidence and execution, not private cognition "
            "or causality.",
            "Independent researcher review remains unfinished.",
        ],
    }
    write(output / "analysis.json", result)
    render(result, output)
    if require_complete and result["provisional"]:
        raise ValueError(f"Only {len(terminal)}/45 sessions are terminal")
    return result


def render(result, output):
    n = result["counts"]
    lines = [
        "# 统一回收定义后的45场结晶研究",
        "",
        "中途导出，不能据此改变实验安排或作全队列结论。"
        if result["provisional"]
        else "固定45场全部到达终态；失败保留，未按结果替换或追加会话。",
        "",
        f"终态 {n['terminal_sources']}/45；完整链 {n['complete_chains']}/45；"
        f"源批次 {n['completed_batches']}/540；后测 {n['sealed_posttests']}/135；"
        f"有效预测 {n['valid_Q']}/45；推荐复测 {n['retest_batches']}/45。",
        "",
        "回收率统一为扣除晶种后的固体目标物摩尔数除以初始试剂投料摩尔数，截断到[0,1]。"
        "源指令、任务契约、操作说明和预测问题均已对齐；数值动力学、噪声、评分与阈值未改。",
        "60个参考批次全部精确重放，数值与原参考一致。旧45场结晶独立保留；"
        "前后不是同期随机提示对照，不能把差异直接归因于定义修正。",
        "",
        f"源重放核验 {n['source_replays']}/{n['terminal_sources']}；"
        f"复测重放 {n['retest_replays']}/{n['retest_batches']}；"
        f"笔记 {n['notebook_versions']} 版；源操作 {n['source_operations']} 次。",
        f"完整token账 {n['complete_token_accounts']}/{n['terminal_sources']}；"
        f"已观测输入+输出token下限 {n['observed_input_plus_output_tokens']:,}。"
        "中断且未返回usage的会话不按零消耗解释。",
        f"结构窗口 {n['structural_feedback_windows']} 个，来自"
        f"{n['sessions_with_feedback_windows']}/{n['terminal_sources']} 场。"
        "这不是认识修订数，不并入旧105窗口编码。",
        "",
        "## 各信息条件的完成度",
        "",
        "| 信息条件 | 终态 | 完整链 | 源批次 | 后测 | 有效Q |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm, c in result["by_arm"].items():
        lines.append(
            f"| {arm} | {c['terminal_sources']}/15 | {c['complete_chains']}/15 | "
            f"{c['completed_batches']}/180 | {c['sealed_posttests']}/45 | {c['valid_Q']}/15 |"
        )
    lines += [
        "",
        "## 描述性结果",
        "",
        "每个世界先平均该臂可用会话，再对五世界等权平均。表中±为世界均值的样本标准差；"
        "括号为有观测世界数/5。逐世界表另给三场会话的均值、样本标准差及实测分母。",
        "质量合格只要求存在颗粒、纯度≥0.80和细粉≤0.50；联合合格另要求回收≥0.10。"
        "缺失预测/复测不计零，不以未完成代替预测错误。",
        "",
        "| 指标 | Opaque | Aligned | MisIndexed |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, detail in result["metrics"].items():
        values = [stat(detail["equal_world_means"][a]) for a in ARMS]
        label = (
            "质量分类 balanced accuracy"
            if name == "quality_balanced_accuracy"
            else LABELS.get(name, name)
        )
        lines.append(f"| {label} | " + " | ".join(values) + " |")
    lines += [
        "",
        "### 查询质量类别构成",
        "",
        "这是对既有12题的描述，不改变评分或问题。高分类正确数可能来自多数类别；"
        "同时报告原评估器的balanced accuracy，不能仅凭正确数推定理解了条件差异。",
        "",
        "| 世界 | 合格题 /12 | 不合格题 /12 | 恒预测合格正确数 | 恒预测不合格正确数 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for world, profile in result["reference_quality_profiles"].items():
        lines.append(
            f"| {world} | {profile['quality_feasible']} | {profile['quality_infeasible']} | "
            f"{profile['always_feasible_correct']} | {profile['always_infeasible_correct']} |"
        )
    lines += ["", "## 逐世界的三次会话", ""]
    for name in METRICS["C"]:
        lines += [
            f"### {LABELS[name]}",
            "",
            "| 世界 | Opaque | Aligned | MisIndexed |",
            "| --- | ---: | ---: | ---: |",
        ]
        for world in result["metrics"][name]["worlds"]:
            lines.append(f"| {world['world']} | " + " | ".join(stat(world[a]) for a in ARMS) + " |")
        lines.append("")
    lines += [
        "## 全部会话与科学记录",
        "",
        "| 会话 | 状态 | 批次 | 后测 | 回收MAE | 纯度偏差 | 笔记/报告/执行 |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["cases"]:
        key = f"{row['repeat']}/{row['id']}"
        links = (
            (f"[笔记]({key}-notebook.md) / [报告]({key}-reports.md) / [时序](sessions/{key}.json)")
            if row["status"] != "pending"
            else "—"
        )
        lines.append(
            f"| {key} | {row['status']} | {row['completed_batches']}/12 | "
            f"{len(row['sealed_stages'])}/3 | "
            f"{num(row['measurements'].get('crystal_yield_mae'))} | "
            f"{num(row['measurements'].get('purity_signed_error'))} | {links} |"
        )
    lines += ["", "## 保留失败", ""]
    if not result["failures"]:
        lines.append(
            "当前已终态会话未见失败；中途导出不代表尚未完成会话的结果。"
            if result["provisional"]
            else "无；45条链均完整。"
        )
    for failure in result["failures"]:
        lines.append(
            f"- {failure['repeat']}/{failure['id']}: {failure['status']}; "
            f"缺失={failure['missing_stages']}; {failure['failure']}"
        )
    lines += ["", "## 解释边界", "", *[f"- {s}" for s in result["limitations"]], ""]
    (output / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    while True:
        result = build(args.root, args.output, require_complete=args.require_complete)
        live = read(args.root / "summary.json")
        emit(
            {
                "stage": "scientific_export",
                "exported_sessions": result["counts"]["terminal_sources"],
                "planned_sessions": 45,
                "complete_chains": result["counts"]["complete_chains"],
                "live_batches": live["completed_batches"],
                "planned_batches": 540,
                "sealed_posttests": live["sealed_posttests"],
                "batches_per_minute": live.get("batches_per_minute"),
                "batch_eta_s": live.get("batch_eta_s"),
            }
        )
        if not args.watch or not result["provisional"]:
            return
        time.sleep(30)


if __name__ == "__main__":
    main()
