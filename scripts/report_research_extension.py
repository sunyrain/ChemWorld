"""Read-only 48+42 coverage analysis and matched-quench scientific export."""

# ruff: noqa: RUF001 -- Chinese report prose.
from __future__ import annotations

import argparse
import time
from collections import Counter
from pathlib import Path

from scripts.analyze_research_formation import LABELS, METRICS, enrich, note_timeline, num, stat
from scripts.report_paper_case_stability import describe
from scripts.report_research_formation import export_case
from scripts.run_paper_case_notebooks import emit, read, write
from scripts.run_research_extension import ARMS


def counts(rows):
    terminal = [r for r in rows if r["status"] != "pending"]
    return {
        "planned_sources": len(rows),
        "terminal_sources": len(terminal),
        "complete_chains": sum(r["status"] == "completed" for r in terminal),
        "planned_batches": sum(r["batches"] for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in terminal),
        "planned_posttests": sum(4 if r["system"] == "EQ" else 3 for r in rows),
        "sealed_posttests": sum(len(r["sealed_stages"]) for r in terminal),
        "valid_Q": sum(bool((r["prediction_evaluation"] or {}).get("valid")) for r in terminal),
        "source_replays": sum(bool((r["exact_replay"] or {}).get("verified")) for r in terminal),
        "source_operations": sum(r["operations"] for r in terminal),
        "source_rollbacks": sum(len(r["rollbacks"]) for r in terminal),
        "notebook_versions": sum(r["notebook"]["version_count"] for r in terminal),
        "notebook_reads": sum(r["notebook"]["read_calls"] for r in terminal),
        "notebook_tool_failures": sum(r["notebook"]["tool_failures"] for r in terminal),
        "initial_notes_before_actions": sum(
            r["notebook"]["initial_note_before_action"] is True for r in terminal
        ),
        "retest_batches": sum(len(r["retest_batch_metrics"]) for r in terminal),
        "retest_replays": sum(
            bool((r["retest"].get("exact_replay") or {}).get("verified")) for r in terminal
        ),
        "complete_token_accounts": sum(r["token_accounting"]["complete"] for r in terminal),
        "observed_input_plus_output_tokens": sum(
            (r["token_accounting"].get("total") or {}).get("input_plus_output", 0) for r in terminal
        ),
    }


def contrasts(rows):
    result = {}
    for system, metrics in METRICS.items():
        result[system] = {}
        for metric in metrics:
            worlds = []
            for world in (f"W{i:02d}" for i in range(1, 6)):
                arms = {
                    arm: describe(
                        [
                            r["measurements"].get(metric)
                            for r in rows
                            if (r["system"], r["world"], r["arm"]) == (system, world, arm)
                        ]
                    )
                    for arm in ARMS
                }
                deltas = {}
                for left, right in (
                    ("Aligned", "Opaque"),
                    ("MisIndexed", "Opaque"),
                    ("MisIndexed", "Aligned"),
                ):
                    a, b = arms[left]["mean"], arms[right]["mean"]
                    deltas[f"{left}_minus_{right}"] = (
                        a - b if a is not None and b is not None else None
                    )
                worlds.append({"world": world, **arms, "deltas": deltas})
            result[system][metric] = {
                "worlds": worlds,
                "equal_world_means": {a: describe([w[a]["mean"] for w in worlds]) for a in ARMS},
                "paired_world_differences": {
                    key: describe([w["deltas"][key] for w in worlds]) for key in worlds[0]["deltas"]
                },
            }
    return result


def compact_state(state):
    return {k: state[k] for k in ("temperature_K", "reaction_chemistry_stopped", "resources")} | {
        "total_particle_count": state["particle_state"].get("csd_total_particle_count"),
    }


def quench_details(pairs):
    """Separate missing-endpoint mechanisms from complete-pair numerical contrasts."""
    failures = []
    transitions = Counter()
    for pair in pairs:
        for arm in ("absent", "present"):
            result = pair[arm]
            if not result["failure"]:
                continue
            rejected = next(
                (s for s in reversed(result["states"]) if s["transaction_status"] != "committed"),
                None,
            )
            failures.append(
                {
                    "pair": pair["id"],
                    "recipe": pair["recipe"],
                    "world": pair["world"],
                    "original_world": pair["world"] == pair["recipe_source_world"],
                    "arm": arm,
                    "failure": result["failure"],
                    "rejected_action": rejected["action"] if rejected else None,
                    "before": compact_state(rejected["before"]) if rejected else None,
                    "rollback_reason": rejected.get("rollback_reason") if rejected else None,
                }
            )
        if pair["absent"]["truth"] is not None and pair["present"]["truth"] is not None:
            a, p = (bool(pair[arm]["quality_and_recovery"]) for arm in ("absent", "present"))
            transitions[f"absent_{'pass' if a else 'fail'}_present_{'pass' if p else 'fail'}"] += 1
    return {
        "failure_arm_counts": dict(Counter(f["arm"] for f in failures)),
        "failure_details": failures,
        "complete_pair_quality_transitions": dict(transitions),
        "verified_replays": sum(
            bool((p[a].get("exact_replay") or {}).get("verified"))
            for p in pairs
            for a in ("absent", "present")
        ),
    }


def export_quench(root, destination):
    if not (root / "summary.json").exists():
        return None
    original = read(root / "summary.json")
    pairs = []
    for pair in original["pairs"]:
        row = {k: v for k, v in pair.items() if k not in {"present", "absent"}}
        for arm in ("absent", "present"):
            row[arm] = {k: v for k, v in pair[arm].items() if k != "states"}
            row[arm]["state_transitions"] = [
                {
                    "action": s["action"],
                    "before": compact_state(s["before"]),
                    "after": compact_state(s["after"]),
                    "transaction_status": s["transaction_status"],
                    "rollback_reason": s.get("rollback_reason"),
                }
                for s in pair[arm]["states"]
            ]
        pairs.append(row)
    summary = {k: v for k, v in original.items() if k != "pairs"}
    summary["endpoint_analysis"] = quench_details(original["pairs"])
    write(destination / "quench_summary.json", summary)
    write(destination / "quench_pairs.json", pairs)
    lines = [
        "# 匹配淬灭操作对照",
        "",
        f"轨迹 {summary['completed_trajectories']}/180；配对 {summary['completed_pairs']}/90；"
        f"完整有效配对 {summary['valid_pairs']}/90。",
        "",
        "固定 18 条旧推荐配方交叉五世界；每对只增加/删除一项淬灭。"
        "差值为有淬灭减无淬灭；主要结果为无噪真值。原失败配方与新增无效执行均保留。",
        "本干预包含淬灭的温度、反应停止及时间/资源后果，不能单独归因于降温速度。"
        "它检验虚拟世界中的操作效果，不证明 Agent 判断形成的原因。",
        "以下数值均以两臂均取得完整终点测量的配对为条件；操作被拒绝的配对单列，缺测不填零。",
        "",
    ]
    for key, label, planned in (
        ("original_world", "原配方所属世界", 18),
        ("all_worlds", "全部五世界交叉", 90),
    ):
        g = summary[key]
        lines += [
            f"## {label}",
            "",
            f"有效配对 {g['valid_pairs']}/{planned}；满足质量与回收的配方："
            f"无淬灭 {g['quality_and_recovery']['absent']}，"
            f"有淬灭 {g['quality_and_recovery']['present']}。",
            f"细粉随淬灭增加 {g['fines_higher_with_quench']} 对，"
            f"减少 {g['fines_lower_with_quench']} 对。",
            "",
            "| 响应 | 配对平均差（有−无） |",
            "| --- | ---: |",
        ]
        lines += [f"| {k} | {num(v)} |" for k, v in g["mean_present_minus_absent"].items()]
        lines.append("")
    endpoint = summary["endpoint_analysis"]
    lines += [
        "## 后续操作能否执行，也是干预结果",
        "",
        f"无淬灭臂失败 {endpoint['failure_arm_counts'].get('absent', 0)} 条，"
        f"有淬灭臂失败 {endpoint['failure_arm_counts'].get('present', 0)} 条；"
        f"全部轨迹精确回放通过 {endpoint['verified_replays']}/"
        f"{summary['completed_trajectories']}。",
        "",
        "| 配方 | 世界 | 失败臂 | 被拒操作 | 操作前温度 K | 目标温度 K | 颗粒数 |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for f in endpoint["failure_details"]:
        action, state = f["rejected_action"] or {}, f["before"] or {}
        lines.append(
            f"| {f['recipe']} | {f['world']} | {f['arm']} | "
            f"{action.get('operation', '未记录')} | {num(state.get('temperature_K'))} | "
            f"{num(action.get('target_temperature_K'))} | "
            f"{num(state.get('total_particle_count'))} |"
        )
    lines += [
        "",
        "这些执行结果不能压成一个‘淬灭使细粉变多’的结论。"
        "加入淬灭可能先降低温度，使原定冷却目标高于当前温度、违反冷却前置条件；"
        "去掉淬灭也可能使后续粒径测量面对零颗粒状态。固定后续配方的对照保留这些后果，"
        "不通过调整冷却目标或补加结晶步骤修复它们。",
        "",
        "对原先关注的第二次 W03/Aligned 配方，加入淬灭后第一段冷却被拒绝，"
        "因此不能据此给出其最终细粉差值，或断言该配方的粒径变化已经得到数值因果验证。",
        "",
        "## 完整配对的达标转变",
        "",
        "| 无淬灭→有淬灭 | 配对数 |",
        "| --- | ---: |",
    ]
    labels = {
        "absent_pass_present_pass": "达标→达标",
        "absent_pass_present_fail": "达标→未达标",
        "absent_fail_present_pass": "未达标→达标",
        "absent_fail_present_fail": "未达标→未达标",
    }
    lines += [
        f"| {label} | {endpoint['complete_pair_quality_transitions'].get(key, 0)} |"
        for key, label in labels.items()
    ]
    lines += [
        "",
        "反方向和仍然达标的配对也被保留。这些结果支持在所测配方中讨论淬灭的总操作效果，"
        "不支持‘淬灭必然破坏结晶’。五世界复用同一组配方，不能把 90 对当作独立总体样本。",
        "",
    ]
    lines += [
        "## 全部配对",
        "",
        "| 配方 | 世界 | 原世界 | 无淬灭回收/细粉 | 有淬灭回收/细粉 |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for p in pairs:
        values = []
        for arm in ("absent", "present"):
            t = p[arm]["truth"] or {}
            values.append(f"{num(t.get('crystal_yield'))} / {num(t.get('crystal_fines_fraction'))}")
        lines.append(
            f"| {p['recipe']} | {p['world']} | {p['recipe_source_world']} | "
            f"{values[0]} | {values[1]} |"
        )
    lines += [
        "",
        "失败逐条保存在 [机器汇总](quench_summary.json)；"
        "[逐对真值、操作与状态变化](quench_pairs.json)。"
        "重复使用配方和世界不产生独立总体样本，未进行伪重复显著性检验。",
        "",
    ]
    (destination / "QUENCH.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def build(root, quench_root, destination):
    destination.mkdir(parents=True, exist_ok=True)
    design = read(root / "design.json")
    parent = Path(design["parent_root"])
    rows, timelines = [], []
    started = last_progress = time.monotonic()
    for cohort, source_root, units in (
        ("retained_48", parent, design["parent_schedule"]),
        ("extension_42", root, design["schedule"]),
    ):
        for unit in units:
            if (source_root / unit["repeat"] / "results" / f"{unit['id']}.json").exists():
                row = enrich(export_case(source_root, unit, destination), source_root, unit)
                timelines.append({"cohort": cohort, **note_timeline(source_root, unit, row)})
                write(
                    destination / unit["repeat"] / f"{unit['id']}.json", {**row, "cohort": cohort}
                )
            else:
                row = {**unit, "status": "pending", "measurements": {}}
            rows.append({**row, "cohort": cohort})
            if time.monotonic() - last_progress >= 30:
                elapsed = max(time.monotonic() - started, 1e-6)
                emit(
                    {
                        "stage": "scientific_export",
                        "slots": len(rows),
                        "total": 90,
                        "slots_per_minute": 60 * len(rows) / elapsed,
                        "eta_s": elapsed / len(rows) * (90 - len(rows)),
                    }
                )
                last_progress = time.monotonic()
    if len(rows) != 90 or len({(r["repeat"], r["id"]) for r in rows}) != 90:
        raise ValueError("Combined report must retain exactly 90 distinct slots")
    cohorts = {
        name: counts([r for r in rows if r["cohort"] == name])
        for name in ("retained_48", "extension_42")
    }
    total = counts(rows)
    failures = [
        {
            k: r.get(k)
            for k in (
                "cohort",
                "repeat",
                "id",
                "status",
                "failure",
                "missing_stages",
                "posttest_validation",
            )
        }
        for r in rows
        if r["status"] not in {"pending", "completed"}
    ]
    quench = export_quench(quench_root, destination)
    result = {
        "scope": "90-slot two-cohort EQ/C O/A/M coverage; 48 retained plus 42 later sessions",
        "provisional": total["terminal_sources"] != 90,
        "source_commits": {
            "retained_48": design["parent_source_commit"],
            "extension_42": design["source_commit"],
        },
        "counts": total,
        "cohorts": cohorts,
        "failures": failures,
        "world_contrasts": contrasts(rows),
        "note_timelines": timelines,
        "reference": read(root / "references/complete.json"),
        "quench": quench,
        "status_counts": dict(Counter(r["status"] for r in rows)),
        "cases": [
            {k: v for k, v in r.items() if k not in {"batch_outcomes", "posttests"}} for r in rows
        ],
        "limitations": [
            "Provider RNG seeds unavailable; fixed-world fresh sessions only.",
            "Added arms are not concurrent with retained arms; cohort drift is not isolated.",
            "Failures are retained and no source is replaced.",
            "No causal notebook-benefit or agent-belief effect is established.",
        ],
    }
    write(destination / "analysis.json", result)
    render(result, destination)
    return result


def render(result, output):
    n = result["counts"]
    lines = [
        "# 五世界三信息臂：90 场研究覆盖",
        "",
        "**中途预览：新增实验尚未全部结束。**" if result["provisional"] else "新增固定队列已结束。",
        "",
        f"终态 {n['terminal_sources']}/90；完整链 {n['complete_chains']}/90；"
        f"源批次 {n['completed_batches']}/1080；有效 Q {n['valid_Q']}/90；"
        f"封存阶段 {n['sealed_posttests']}/315。",
        "",
        "保留旧 48 场，新增缺口 42 场。三次是固定环境映射下的新模型会话，不是受控模型 RNG seed。"
        "新增信息臂与原信息臂存在执行时期差异；合并表提供覆盖与描述性比较，不将其称为同期随机实验。",
        "",
        "| 阶段 | 终态/计划 | 完整链 | 源批次 | 后测 | 笔记版本 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, c in result["cohorts"].items():
        lines.append(
            f"| {name} | {c['terminal_sources']}/{c['planned_sources']} | "
            f"{c['complete_chains']} | {c['completed_batches']}/{c['planned_batches']} | "
            f"{c['sealed_posttests']}/{c['planned_posttests']} | {c['notebook_versions']} |"
        )
    lines += [
        "",
        "[分层数值分析](ANALYSIS.md)；[匹配淬灭对照](QUENCH.md)；"
        "[机器汇总及全部失败](analysis.json)。",
        "",
        "| 重复 | 条件 | 阶段 | 状态 | 记录 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in sorted(result["cases"], key=lambda r: (r["id"], r["repeat"])):
        p = f"{r['repeat']}/{r['id']}"
        links = (
            f"[笔记]({p}-notebook.md) / [后测]({p}-reports.md) / [数据]({p}.json)"
            if r["status"] != "pending"
            else "未启动/尚未终态"
        )
        lines.append(f"| {r['repeat']} | {r['id']} | {r['cohort']} | {r['status']} | {links} |")
    (output / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    lines = [
        "# 分层统计",
        "",
        "均值及样本 SD 按会话计算，汇总对世界等权。"
        "每条件固定三场；缺失不补零。M 为原固定错配先验，不是新增提示策略。",
        "",
    ]
    for system, metrics in result["world_contrasts"].items():
        lines += [
            f"## {system}",
            "",
            "| 指标 | Opaque 世界均值 | Aligned 世界均值 | MisIndexed 世界均值 |",
            "| --- | ---: | ---: | ---: |",
        ]
        for name, value in metrics.items():
            cells = [stat(value["equal_world_means"][a]) for a in ARMS]
            lines.append(f"| {LABELS[name]} | " + " | ".join(cells) + " |")
        lines += [
            "",
            "| 指标 | 世界 | Opaque（n/3） | Aligned（n/3） | MisIndexed（n/3） |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
        for name, value in metrics.items():
            for world in value["worlds"]:
                cells = [stat(world[a]) for a in ARMS]
                lines.append(f"| {LABELS[name]} | {world['world']} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## 失败与记录完整性", "", f"失败/不完整链共 {len(result['failures'])} 条：", ""]
    lines += [
        f"- {f['cohort']} / {f['repeat']} / {f['id']}：{f['status']}；"
        f"缺失 {', '.join(f.get('missing_stages') or [])}。"
        for f in result["failures"]
    ]
    lines += [
        "",
        f"源回放 {n['source_replays']}/{n['terminal_sources']}；操作 {n['source_operations']}，"
        f"回滚 {n['source_rollbacks']}；推荐复测 {n['retest_replays']}/{n['retest_batches']}；"
        f"笔记 {n['notebook_versions']} 版，主动读取 {n['notebook_reads']} 次。",
        f"可用输入+输出 token {n['observed_input_plus_output_tokens']}；"
        f"完整 token 账本 {n['complete_token_accounts']}/{n['terminal_sources']}。"
        "未报告的使用量保持缺失；订阅成本不可按调用精确归属。",
        "",
    ]
    (output / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--quench-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.root, args.quench_root, args.output)
    print(result["counts"], flush=True)


if __name__ == "__main__":
    main()
