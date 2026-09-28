"""Report Astra and the joint model matrix without changing retained results."""

# ruff: noqa: RUF001

from __future__ import annotations

import csv
from statistics import fmean, median

import analyze_work_ii_eq_three_model_matrix as common
from run_work_ii_eq_astra_matrix import MODEL, REPORT, ROOT, folder, jobs, read, write

PREVIOUS = ROOT / "workstreams/flagship_tasks/reports/eq-three-model-matrix-20260927"
MODELS = (*common.MODELS, MODEL)


def no_reuse(job):
    return False


def fmt(value, digits=5):
    return "缺失" if value is None else f"{value:.{digits}f}"


def group_score(group):
    return fmean(r["interval_score80"] for r in group["responses"].values())


def trajectory_findings(astra):
    rows = []
    for directory in (PREVIOUS, REPORT):
        with (directory / "source_batches.csv").open(encoding="utf-8-sig", newline="") as stream:
            rows.extend(csv.DictReader(stream))
    lines = [
        "",
        "## 实验路径与一个正面案例",
        "",
        "以下为完成后的描述性轨迹分析，不是新增实验或预设主检验。"
        "比较各场包含正投料的已检测批次的最低名义浓度；零投料空白不计作稀溶液取证。",
        "",
        "| 模型 | 各场最低浓度的中位数（M） | 曾测到≤1 mM的研究/15 |",
        "|---|---:|---:|",
    ]
    for model in MODELS:
        selected = [r for r in rows if r["model"] == model and float(r["reagent_mol"]) > 0]
        ids = {r["cell_id"] for r in selected}
        minima = [
            min(float(r["nominal_input_concentration_M"]) for r in selected if r["cell_id"] == cell)
            for cell in ids
        ]
        lines.append(
            f"| {model} | {median(minima):.6g} | {sum(c <= 0.001 + 1e-12 for c in minima)} |"
        )
    case = next(c for c in astra["cells"] if c["world_id"] == "EQ-W03" and c["arm"] == "MisIndexed")
    forecast = case["Q08_dissociation"]
    selected = [r for r in rows if r["model"] == MODEL and r["cell_id"] == case["cell_id"]]
    lines += [
        "",
        "### Astra / W03 / MisIndexed",
        "",
        "该例从前几批的局部平台，进入低浓度响应区间，随后还执行分段稀释、"
        "追加投料和延长等待。下表来自实际操作与检测记录。",
        "",
        "| 批次 | 名义终点浓度（μM） | 电离分数 |",
        "|---|---:|---:|",
    ]
    for r in selected:
        if int(r["batch"]) in (1, 2, 3, 4, 5, 9, 10, 12):
            lines.append(
                f"| {r['batch']} | "
                f"{1e6 * float(r['nominal_input_concentration_M']):.2f} | "
                f"{float(r['acid_dissociation_fraction']):.2%} |"
            )
    lines += [
        "",
        "在实验结束、预测封存之前的K1报告中，研究者明确区分了低浓度响应与高浓度"
        "平台，并将所给档案pKa区间4.609–4.709修正为约5.02的有效关系。"
        "这段解释属于公开科学报告，不是每次实验选择时记录的同期思考。",
        f"随后，对13.3 μM条件下的电离分数给出 "
        f"{forecast['estimate']:.2%} "
        f"[{forecast['lower80']:.2%}, {forecast['upper80']:.2%}]，"
        f"共同参考均值为 {forecast['reference_mean']:.2%}。",
        "该例连接了自主获得的边界证据、报告中表达的关系与后续准确预测。"
        "它不证明该研究者识别了唯一物理机制，也不能从跨模型差异单独分离"
        "采样策略与证据解释各自的因果贡献。MisIndexed总体更优也不等于错误先验本身更好。",
    ]
    return lines


def render(astra, joint):
    lines = [
        "# 同一平衡研究矩阵中的 GPT-6 Astra medium",
        "",
        f"Astra 完成 {astra['completed_source_sessions']}/15 场自主实验与 "
        f"{astra['valid_Q_sessions']}/15 场有效预测，完整四阶段链条 "
        f"{astra['completed_sessions']}/{astra['planned_sessions']} 场；"
        f"{astra['completed_batches']}/{astra['planned_batches']} 批实验，"
        f"{astra['valid_stages']}/{astra['planned_stages']} 个原会话封存阶段，"
        f"{astra['valid_scalar_predictions']}/{astra['planned_scalar_predictions']} 个标量预测。",
        f"精确重放 {astra['replay_verified']}/15；操作尝试 {astra['operations']} 次，"
        f"其中拒绝/回滚 {astra['rollbacks']} 次。",
        "",
        "GPT-6 Astra、GPT-5.6 Luna、GPT-5.6 Terra 和 GPT-5.5 均使用 medium，"
        "相同五世界、Opaque/Aligned/MisIndexed 三臂、每场12批自主实验与原会话"
        "K1→Q→K2→EQS。medium 是共同请求设置，不代表实际计算量相等。",
        "",
        "这些条件属于同一科学问题的跨模型矩阵。Astra 的15场全部新运行；其余45场"
        "保持不变，其中六场W01先导结果在补全先前矩阵前已知。"
        "共同参考为既有300个参考批次，不新增真值运行，不向研究者反馈参考值。",
        f"联合矩阵完成 {joint['completed_sessions']}/60 场、"
        f"{joint['completed_batches']}/720 批、{joint['valid_stages']}/240 个封存阶段；"
        f"保留 {joint['rollbacks']} 次操作拒绝/回滚，以及 "
        f"{len(joint['retained_infrastructure_attempts'])} 次已记录的基础设施中断。"
        "这些中断单独记录，不计作科学失败；有效阶段以恢复后的记录汇总。",
        "Astra 的 W05/Opaque 最后一次 EQS 曾在提供商返回 HTTP 503 时中断。"
        + (
            "现已在原 Astra-medium 会话中用原提示续接成功；实验、K1、Q、K2、"
            "参考值及预测评分均保持不变，失败尝试原样保留。"
            if any(c.get("posttest_recoveries") for c in astra["cells"])
            else "该阶段仍待运行恢复；已完成的实验与有效Q保持纳入，不视为科学失败。"
        ),
        "",
        "## 五世界等权均值",
        "",
        "| 模型 | 条件 | 有效Q/5 | 其余九题MAE | 最稀三题MAE | 最稀覆盖率 | 最稀区间评分 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for a in joint["aggregates"]:
        if a["scope"] != "all_five":
            continue
        nine, dilute = a["groups"]["other_nine"], a["groups"]["dilute_three"]
        coverage = dilute["coverage80"]
        values = [
            a["model"],
            a["arm"],
            str(a["valid_Q"]),
            fmt(nine["macro_mae"]),
            fmt(dilute["macro_mae"]),
            "缺失" if coverage is None else f"{coverage:.1%}",
            fmt(group_score(dilute)) if dilute["responses"] else "缺失",
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines += [
        "",
        "MAE 对 pH/14、电离分数、沉淀信号等权汇总。最稀三题为预先固定的"
        "Q03/Q08/Q09，其余九题也包含边界及未探索条件。区间标称覆盖率80%；"
        "区间评分=宽度+10×区间外距离，越低越好；评分保留五次参考观测。",
        "",
        "![四模型共同矩阵](comparison.png)",
        "",
        "## Aligned相对Opaque的逐世界结果",
        "",
        "| 模型 | 有效配对/5 | 九题改善 | 三题改善 | 九题改善、三题恶化 |",
        "|---|---:|---:|---:|---:|",
    ]
    for model in MODELS:
        pairs = [
            p
            for p in joint["paired_comparisons"]
            if p["model"] == model and p["contrast"] == "Aligned-Opaque" and p["valid_pair"]
        ]
        counts = [
            len(pairs),
            sum(p["other_nine_delta"] < 0 for p in pairs),
            sum(p["dilute_three_delta"] < 0 for p in pairs),
            sum(p["reversal"] for p in pairs),
        ]
        lines.append("| " + model + " | " + " | ".join(map(str, counts)) + " |")
    lines += [
        "",
        "### Astra的全部逐世界对比",
        "",
        "| 世界 | 对比 | 九题ΔMAE | 三题ΔMAE | 收益反转 |",
        "|---|---|---:|---:|---|",
    ]
    for p in astra["paired_comparisons"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    p["world_id"],
                    p["contrast"],
                    fmt(p["other_nine_delta"]),
                    fmt(p["dilute_three_delta"]),
                    "是" if p["reversal"] else "否" if p["valid_pair"] else "缺失",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "### W02-W05敏感性分析",
        "",
        "保留去掉已知先导世界W01后的比较；Astra的五个世界均未复用先导会话。",
        "",
        "| 模型 | 九题平均ΔMAE | 三题平均ΔMAE |",
        "|---|---:|---:|",
    ]
    for model in MODELS:
        rows = {
            a["arm"]: a
            for a in joint["aggregates"]
            if a["scope"] == "new_worlds_only" and a["model"] == model
        }
        deltas = []
        for group in ("other_nine", "dilute_three"):
            a = rows["Aligned"]["groups"][group]["macro_mae"]
            o = rows["Opaque"]["groups"][group]["macro_mae"]
            deltas.append(None if a is None or o is None else a - o)
        lines.append("| " + model + " | " + " | ".join(fmt(d) for d in deltas) + " |")
    lines += trajectory_findings(astra)
    lines += ["", "## 完成情况与失败", ""]
    for c in astra["cells"]:
        lines.append(
            f"- {c['world_id']}/{c['arm']}: {c['status']}; "
            f"{c['source_batches']}/12批; {c['operations']}次操作尝试; "
            f"{c['rollbacks']}次拒绝/回滚; replay={c['replay_verified']}; "
            f"source failure={c['failure']}; posttest failures={c['posttest_failures']}."
        )
    lines += [
        "",
        "## 证据范围与文件",
        "",
        "这是固定矩阵的开发性结果，每个模型—世界—信息条件仅一次研究。"
        "全部失败保留；有效Q与完整研究链分别计数。世界、查询、响应与参考重复"
        "不能当作独立模型重复。点误差、覆盖率和区间评分需分别解读。"
        "MisIndexed的结果完整报告，不从其优劣推断错误知识本身的因果价值。",
        "",
        "[Astra机器汇总](summary.json) · [四模型共同汇总](joint_summary.json) · "
        "[全部60场](joint_cell_metrics.csv) · [逐世界对比](joint_paired_comparisons.csv)",
        "",
        "[Astra逐批记录](source_batches.csv) · [逐项预测](predictions.csv) · "
        "[原会话公开解释](PUBLIC_ACCOUNTS.md) · [共同参考](reference_observations.json) · "
        "[矢量图](comparison.pdf)",
        "",
    ]
    (REPORT / "REPORT_ZH.md").write_text("\n".join(lines), encoding="utf-8")


def analyze(root, config, truth):
    astra = common.analyze(
        root,
        config,
        truth,
        report=REPORT,
        selected_jobs=jobs(),
        source_resolver=folder,
        reused_predicate=no_reuse,
        models=(MODEL,),
        scope="development; Astra medium condition of the common five-world EQ matrix",
        render=False,
    )
    previous = read(PREVIOUS / "summary.json")
    assert read(PREVIOUS / "reference_observations.json") == truth
    cells = [*previous["cells"], *astra["cells"]]
    joint = {
        "scope": "common EQ matrix; four model configurations; sequentially authorized blocks",
        "models": list(MODELS),
        "planned_sessions": 60,
        "completed_sessions": previous["completed_sessions"] + astra["completed_sessions"],
        "valid_Q_sessions": previous["valid_Q_sessions"] + astra["valid_Q_sessions"],
        "planned_batches": 720,
        "completed_batches": previous["completed_batches"] + astra["completed_batches"],
        "planned_stages": 240,
        "valid_stages": previous["valid_stages"] + astra["valid_stages"],
        "planned_scalar_predictions": 2160,
        "valid_scalar_predictions": previous["valid_scalar_predictions"]
        + astra["valid_scalar_predictions"],
        "replay_verified": previous["replay_verified"] + astra["replay_verified"],
        "operations": previous["operations"] + astra["operations"],
        "rollbacks": previous["rollbacks"] + astra["rollbacks"],
        "retained_infrastructure_attempts": previous["retained_infrastructure_attempts"]
        + astra["retained_infrastructure_attempts"],
        "cells": cells,
        "aggregates": common.aggregate(cells, MODELS),
        "paired_comparisons": common.paired(cells, MODELS),
    }
    write(REPORT / "joint_summary.json", joint)
    for name in ("cell_metrics.csv", "paired_comparisons.csv"):
        rows = []
        for directory in (PREVIOUS, REPORT):
            with (directory / name).open(encoding="utf-8-sig", newline="") as stream:
                rows.extend(csv.DictReader(stream))
        common.csv_write(REPORT / f"joint_{name}", rows)
    common.plot(joint, models=MODELS, report=REPORT)
    render(astra, joint)
    return joint
