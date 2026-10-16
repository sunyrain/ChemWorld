"""Recompute W2-263 descriptive quantitative synthesis from retained exports only.

The unit of analysis is a fresh participant session. This script neither calls
the simulator/provider nor assigns semantic labels or an abduction success rate.
"""

# Chinese report text intentionally uses Chinese punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean, median

METRICS = ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
SIGMA = dict(zip(METRICS, (0.002, 0.006, 0.006), strict=True))
QUERIES = tuple(f"Q{i:02}" for i in range(1, 13))
GROUPS = {
    "all": QUERIES,
    "loading": QUERIES[:6],
    "scale": ("Q07", "Q08", "Q11", "Q12"),
    "path": ("Q09", "Q10"),
}
CONTROL_SETS = {
    "scale": (("Q04", "Q07", "Q08"), ("Q06", "Q11", "Q12")),
    "path": (("Q05", "Q09", "Q10"),),
}
STAGES = ("K1", "Q", "K2")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def describe(values):
    values = [v for v in values if v is not None]
    return {
        "n": len(values),
        "mean": fmean(values) if values else None,
        "median": median(values) if values else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }


def prediction_summary(rows):
    result = {}
    for group, queries in GROUPS.items():
        result[group] = {}
        for metric in METRICS:
            selected = [r for r in rows if r["query"] in queries and r["metric"] == metric]
            result[group][metric] = {
                "queries": len(selected),
                "planned_queries": len(queries),
                "reference_observations": sum(int(r["reference_repeats"]) for r in selected),
                "mae": fmean(float(r["absolute_error"]) for r in selected),
                "signed_error": fmean(float(r["signed_error"]) for r in selected),
                "empirical_coverage80": fmean(float(r["empirical_coverage80"]) for r in selected),
                "mean_width80": fmean(float(r["upper80"]) - float(r["lower80"]) for r in selected),
            }
    return result


def control_summary(rows):
    predictions = {(r["query"], r["metric"]): float(r["estimate"]) for r in rows}
    return {
        kind: {
            metric: describe(
                [
                    max(predictions[q, metric] for q in group)
                    - min(predictions[q, metric] for q in group)
                    for group in sets
                ]
            )
            for metric in METRICS
        }
        for kind, sets in CONTROL_SETS.items()
    }


def session_row(unit, exported, status, rows):
    session = exported or {}
    batches = session.get("batches", [])
    gaps = [b["physical_counterfactual"] for b in batches if b.get("physical_counterfactual")]
    counts = [sum(g["gap_in_assay_standard_deviations"][m] >= 3 for m in METRICS) for g in gaps]
    posttests = session.get("posttests", {})
    validations = session.get("posttest_validation", {})
    valid = {stage: validations.get(stage, {}).get("valid") is True for stage in STAGES}
    cf = session.get("counterfactual") or {}
    result = {
        "repeat": unit["repeat"],
        "id": unit["id"],
        "world": unit["world"],
        "pair": unit["pair"],
        "mechanism": unit["mechanism"],
        "exported": exported is not None,
        "status": session.get("status", status),
        "source_status": session.get("source_status"),
        "source_assays": len(batches),
        "planned_source_assays": unit["batches"],
        "operation_outcomes": dict(
            Counter(e["transaction_status"] for e in session.get("events", []))
        ),
        "notebook_versions": len(session.get("versions", [])),
        "sealed_stages_present": {s: bool(posttests.get(s)) for s in STAGES},
        "sealed_stages_valid": valid,
        "complete_chain": session.get("source_status") == "completed"
        and len(batches) == unit["batches"]
        and all(valid.values()),
        "source_replay_verified": (session.get("exact_replay") or {}).get("verified") is True,
        "counterfactual_status": cf.get("status", "not_exported"),
        "own_observations_identical": cf.get("own_source_observations_identical"),
        "own_operations_identical": cf.get("own_operation_outcomes_identical"),
        "counterfactual_replays": {
            k: (v.get("exact_replay") or {}).get("verified") is True
            for k, v in session.get("counterfactual_execution", {}).items()
        },
        "failure": session.get("failure"),
        "stage_failures": {k: v.get("failure") for k, v in posttests.items() if v.get("failure")},
        "counterfactual_failures": {
            k: v.get("failure")
            for k, v in session.get("counterfactual_execution", {}).items()
            if v.get("failure")
        },
        "separation": {
            "matched_assays": len(gaps),
            "observed_source_assays": len(batches),
            "planned_source_assays": unit["batches"],
            "per_channel_gap_sigma": {
                m: describe([g["gap_in_assay_standard_deviations"][m] for g in gaps])
                for m in METRICS
            },
            "mean_max_channel_gap_sigma": fmean(
                max(g["gap_in_assay_standard_deviations"].values()) for g in gaps
            )
            if gaps
            else None,
            "at_least_one_channel_3sigma": sum(c >= 1 for c in counts),
            "at_least_two_channels_3sigma": sum(c >= 2 for c in counts),
            "fraction_one_channel_3sigma": fmean(c >= 1 for c in counts) if counts else None,
            "fraction_two_channels_3sigma": fmean(c >= 2 for c in counts) if counts else None,
            "first_ordinal_one_channel_3sigma": next(
                (g["source_ordinal"] for g, c in zip(gaps, counts, strict=True) if c >= 1), None
            ),
            "first_ordinal_two_channels_3sigma": next(
                (g["source_ordinal"] for g, c in zip(gaps, counts, strict=True) if c >= 2), None
            ),
        },
        "prediction_rows": len(rows),
        "planned_prediction_rows": 36,
        "prediction_analysis_ready": False,
        "prediction_groups": None,
        "control_prediction_spread": None,
        "reaggregation_max_abs_error": None,
    }
    expected = {(q, m) for q in QUERIES for m in METRICS}
    observed = [(r["query"], r["metric"]) for r in rows]
    if len(observed) != len(set(observed)):
        raise ValueError(f"Duplicate prediction entries for {unit['repeat']}/{unit['id']}")
    if valid["Q"] and set(observed) == expected:
        payload = posttests["Q"]["payload"]
        sealed = {
            (q["query_id"], m): v for q in payload["predictions"] for m, v in q["metrics"].items()
        }
        for row in rows:
            forecast = sealed[row["query"], row["metric"]]
            for k in ("estimate", "lower80", "upper80"):
                if abs(float(row[k]) - forecast[k]) > 1e-12:
                    raise ValueError(f"Export mismatch: {unit['id']}/{row['query']}/{k}")
            error = float(row["estimate"]) - float(row["reference_mean"])
            if (
                abs(error - float(row["signed_error"])) > 1e-12
                or abs(abs(error) - float(row["absolute_error"])) > 1e-12
            ):
                raise ValueError(f"Error arithmetic mismatch: {unit['id']}/{row['query']}")
        result["prediction_analysis_ready"] = True
        result["prediction_groups"] = prediction_summary(rows)
        result["control_prediction_spread"] = control_summary(rows)
        stored = (session.get("prediction_evaluation") or {}).get("metrics", {})
        metric_keys = {
            "mae": "mae_to_five_repeat_mean",
            "empirical_coverage80": "empirical_coverage80",
            "mean_width80": "mean_width80",
        }
        differences = [
            abs(result["prediction_groups"]["all"][m][ours] - stored[m][theirs])
            for m in METRICS
            if m in stored
            for ours, theirs in metric_keys.items()
        ]
        result["reaggregation_max_abs_error"] = max(differences) if differences else None
        if differences and max(differences) > 1e-12:
            raise ValueError(f"Stored session metrics differ: {unit['repeat']}/{unit['id']}")
    return result


def aggregate(sessions):
    available = [s for s in sessions if s["exported"]]
    predictions = [s for s in sessions if s["prediction_analysis_ready"]]
    separation = [s for s in sessions if s["separation"]["matched_assays"]]
    total = len(sessions)
    result = {
        "planned_sessions": total,
        "exported_sessions": len(available),
        "complete_chains": sum(s["complete_chain"] for s in sessions),
        "statuses": dict(Counter(s["status"] for s in sessions)),
        "source_assays": sum(s["source_assays"] for s in sessions),
        "planned_source_assays": sum(s["planned_source_assays"] for s in sessions),
        "valid_prediction_sessions": len(predictions),
        "matched_counterfactual_assays": sum(s["separation"]["matched_assays"] for s in sessions),
        "separation_sessions": len(separation),
        "sessions_any_one_channel_3sigma": sum(
            s["separation"]["at_least_one_channel_3sigma"] > 0 for s in sessions
        ),
        "sessions_any_two_channels_3sigma": sum(
            s["separation"]["at_least_two_channels_3sigma"] > 0 for s in sessions
        ),
        "assays_one_channel_3sigma": sum(
            s["separation"]["at_least_one_channel_3sigma"] for s in sessions
        ),
        "assays_two_channels_3sigma": sum(
            s["separation"]["at_least_two_channels_3sigma"] for s in sessions
        ),
        "separation_session_statistics": {
            name: describe([s["separation"][name] for s in separation])
            for name in (
                "mean_max_channel_gap_sigma",
                "fraction_one_channel_3sigma",
                "fraction_two_channels_3sigma",
            )
        },
        "per_channel_mean_gap_sigma": {
            m: describe([s["separation"]["per_channel_gap_sigma"][m]["mean"] for s in separation])
            for m in METRICS
        },
        "prediction_groups": {
            group: {
                m: {
                    k: describe([s["prediction_groups"][group][m][k] for s in predictions])
                    for k in ("mae", "signed_error", "empirical_coverage80", "mean_width80")
                }
                for m in METRICS
            }
            for group in GROUPS
        },
        "aggregation_weighting": (
            "equal available sessions within this planned group; "
            "world-equal summaries are separately identified"
        ),
        "control_prediction_spread": {
            kind: {
                m: describe([s["control_prediction_spread"][kind][m]["mean"] for s in predictions])
                for m in METRICS
            }
            for kind in CONTROL_SETS
        },
    }
    # MAE is bounded by [0,1] because public outcomes and validated forecasts are bounded.
    result["missing_session_mae_bounds"] = {
        group: {
            m: [
                sum(s["prediction_groups"][group][m]["mae"] for s in predictions) / total,
                (
                    sum(s["prediction_groups"][group][m]["mae"] for s in predictions)
                    + total
                    - len(predictions)
                )
                / total,
            ]
            for m in METRICS
        }
        for group in GROUPS
    }
    return result


def f(value, digits=4):
    return "—" if value is None else f"{value:.{digits}f}"


def spread(stat, digits=4):
    if not stat["n"]:
        return "—"
    return f"{f(stat['mean'], digits)} [{f(stat['min'], digits)}, {f(stat['max'], digits)}]"


def world_equal_prediction_groups(worlds):
    return {
        g: {
            m: {
                k: describe([w["prediction_groups"][g][m][k]["mean"] for w in worlds.values()])
                for k in ("mae", "signed_error", "empirical_coverage80", "mean_width80")
            }
            for m in METRICS
        }
        for g in GROUPS
    }


def render(summary):
    totals, worlds, pairs = summary["totals"], summary["worlds"], summary["pairs"]
    all_done = summary["status"] == "all_planned_sessions_exported"
    state_text = (
        "全部计划会话已封存。" if all_done else "阶段性快照，未完成会话继续保留在计划分母中。"
    )
    lines = [
        "# 匹配机制世界：定量综合",
        "",
        f"更新：{summary['generated_at_utc']}。{state_text}",
        f"已封存 **{totals['exported_sessions']}/30** 场，"
        f"完整源研究—K1—Q—K2 链 **{totals['complete_chains']}/30**；"
        f"源终检 **{totals['source_assays']}/360**，"
        f"有效定量预测 **{totals['valid_prediction_sessions']}/30**。",
        "",
        "## 分析单位和口径",
        "",
        "覆盖固定为 5 对机制世界 × A/B 两机制 × 3 次新会话，共 30 场。"
        "A 为直接自由离子沉淀网络，B 增加中性水相离子对中间体。"
        "每世界三次会话共享既定观测随机键，模型采样 seed 不可控；这是新会话变异，"
        "不能解释为模型与测量噪声共同独立重采样。"
        "十个世界是受控覆盖，不能当作从全部化学世界随机抽样。"
        "研究任务已经明确给定加载、尺度与路径等研究维度，"
        "记录提示要求有可检验预期时在首个物理实验前记录，并在最后建议前完成笔记。"
        "不能把研究活动描述为从零提出全部研究问题，也不估计无提示的自然反绎频率。",
        "",
        "先在每场内计算 12 次源终检的物理区分量和 12 个留出题的误差，"
        "再汇总各世界三场；A/B 及总体比较按世界等权。"
        "本文表内 [最小, 最大] 表示会话间实际范围，不是置信区间。"
        "批次、问题、三个响应和五次参考测定均不是额外的独立研究会话。",
        "",
        "源动作序列在自身和匹配另一机制中原样回放。区分量为两世界噪声前均值的绝对差除以单次终检声明的标准差"
        "（归一化 pH 0.002，自由去质子化比例和沉淀比例均 0.006）。3σ 只用于描述可观测物理差异；"
        "它不是显著性检验、反绎成功率或 Agent 已识别机制的判据，"
        "也不表示 Agent 在另一世界会选择同样动作。",
        "",
        "预测 MAE 对照每世界、每题的五次实际参考测定均值；因非负裁剪，该均值不是噪声前物理真值。"
        "80% 区间覆盖率逐题对五次参考观测计算后在会话内平均；相同参考集合被该世界三场共享。"
        "归一化 pH 误差乘 14 为常规 pH 单位；两种比例误差乘 100 为百分点。",
        "",
        "## 完整性和失败",
        "",
        "| 项目 | 已观测/计划 |",
        "| --- | ---: |",
        f"| 源研究完成 | {summary['source_completed']}/30 |",
        f"| 源终检 | {totals['source_assays']}/360 |",
        *[f"| 有效 {stage} | {summary['valid_stages'][stage]}/30 |" for stage in STAGES],
        f"| 源轨迹精确回放 | {summary['source_replays_verified']}/30 |",
        f"| 自身/配对世界回放 | {summary['counterfactual_replays_verified']}/60 |",
        f"| 可匹配的源终检反事实 | {totals['matched_counterfactual_assays']}/360 |",
        f"| 预测条目（题 × 响应） | {summary['prediction_entries']}/1080 |",
        "",
        f"源操作状态：`{json.dumps(summary['operation_outcomes'], ensure_ascii=False)}`。"
        "操作拒绝保留在轨迹内，不按化学阴性结果计。尚未封存、无效预测与失败不以零误差填补；"
        "机器摘要逐场列出状态，并提供缺失会话 MAE 的 [0,1] 保守边界。",
        "",
        "首轮技术启动失败另列：4/30 启动损失、26/30 未启动、0 次科学操作；"
        "完整重启轮是本报告的 30 场，首轮不是另外 30 场有科学观测的研究，"
        "也没有选择性替换较差科学结果。资源使用见 resource-summary.json。",
        "",
        "## 实际所选实验的物理区分力",
        "",
        f"至少一次取得 ≥1 通道 3σ 物理差异的会话为 "
        f"{totals['sessions_any_one_channel_3sigma']}/30；"
        f"至少一次取得 ≥2 通道 3σ 差异的为 "
        f"{totals['sessions_any_two_channels_3sigma']}/30。"
        f"对应终检计数为 {totals['assays_one_channel_3sigma']}/360 和 "
        f"{totals['assays_two_channels_3sigma']}/360，"
        f"当前可匹配终检为 {totals['matched_counterfactual_assays']}/360。"
        "这些计数只描述所选实验含有的物理信息，不是机制识别成功数。",
        "",
        "先算每场中相应终检所占比例，再汇总当前可用会话，其平均比例分别为 "
        f"{f(totals['separation_session_statistics']['fraction_one_channel_3sigma']['mean'], 4)}、"
        f"{f(totals['separation_session_statistics']['fraction_two_channels_3sigma']['mean'], 4)}。"
        "全部会话各 12 次终检时，该均值与相应终检总数除以 360 一致。",
        "",
        "| 世界 | 封存/3 | 匹配终检/36 | 每场平均最大通道差/σ | "
        "≥1 通道3σ的场内比例 | ≥2 通道3σ的场内比例 |",
        "| --- | ---: | ---: | --- | --- | --- |",
    ]
    for name, w in worlds.items():
        d = w["separation_session_statistics"]
        lines.append(
            f"| {name} | {w['exported_sessions']}/3 | {w['matched_counterfactual_assays']}/36 | "
            f"{spread(d['mean_max_channel_gap_sigma'], 2)} | "
            f"{spread(d['fraction_one_channel_3sigma'], 3)} | "
            f"{spread(d['fraction_two_channels_3sigma'], 3)} |"
        )
    lines.extend(
        [
            "",
            "这些差异只表明所获证据在固定两世界之间含有区分信息。即使一次轨迹具有很多大差异批次，"
            "也仍可能只形成经验关系、保持多个解释并存，或错误重建某项操作。"
            "解释是否提出、如何检验和使用，需结合另列的逐场语义记录。",
            "",
            "## 留出预测：按世界汇总",
            "",
            "| 世界 | 有效Q/3 | 归一化pH MAE | 自由比例 MAE | 沉淀比例 MAE |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    for name, w in worlds.items():
        values = [spread(w["prediction_groups"]["all"][m]["mae"]) for m in METRICS]
        lines.append(
            f"| {name} | {w['valid_prediction_sessions']}/3 | " + " | ".join(values) + " |"
        )
    lines.extend(
        [
            "",
            "## 五对机制及其会话变异",
            "",
            "A/B 差异是世界条件下结果的描述；三场重复没有受控模型采样配对，"
            "不据此估计‘机制识别提升’。",
            "",
            "| 配对 | A有效/3 | B有效/3 | A 三响应MAE | B 三响应MAE | A/B平均最大通道差/σ |",
            "| --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for pair in pairs:
        a, b = worlds[f"EQ-{pair}-A"], worlds[f"EQ-{pair}-B"]
        av = "/".join(f(a["prediction_groups"]["all"][m]["mae"]["mean"]) for m in METRICS)
        bv = "/".join(f(b["prediction_groups"]["all"][m]["mae"]["mean"]) for m in METRICS)
        ad = f(a["separation_session_statistics"]["mean_max_channel_gap_sigma"]["mean"], 2)
        bd = f(b["separation_session_statistics"]["mean_max_channel_gap_sigma"]["mean"], 2)
        lines.append(
            f"| {pair} | {a['valid_prediction_sessions']}/3 | "
            f"{b['valid_prediction_sessions']}/3 | {av} | {bv} | {ad}/{bd} |"
        )
    lines.extend(
        [
            "",
            "## 加载、尺度和路径题",
            "",
            "加载题 Q01–Q06 为 0.02 L、浓度 0.002–0.6 M；"
            "尺度题为 Q07/Q08/Q11/Q12；路径题为 Q09/Q10。"
            "三组不重叠，但难度和浓度组成不同，组间 MAE 差异不能单独归因为尺度或路径。",
            "",
            "| 题组 | 有数据世界/10 | 归一化pH MAE | 自由比例 MAE | 沉淀比例 MAE |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    labels = {"all": "全部12题", "loading": "加载6题", "scale": "尺度4题", "path": "路径2题"}
    for group, label in labels.items():
        data = summary["world_equal_prediction_groups"][group]
        lines.append(
            f"| {label} | {data[METRICS[0]]['mae']['n']}/10 | "
            + " | ".join(f(data[m]["mae"]["mean"]) for m in METRICS)
            + " |"
        )
    lines.extend(["", "| 响应 | 全部题80%区间覆盖率 | 平均80%区间宽度 |", "| --- | ---: | ---: |"])
    for m in METRICS:
        d = summary["world_equal_prediction_groups"]["all"][m]
        lines.append(
            f"| {m} | {f(d['empirical_coverage80']['mean'], 3)} | {f(d['mean_width80']['mean'])} |"
        )
    lines.extend(
        [
            "",
            "另检验预测中心是否保持已知物理不变性：尺度组比较 Q04/Q07/Q08 与 Q06/Q11/Q12，"
            "路径组比较 Q05/Q09/Q10。先计算每组最大中心减最小中心，场内平均，再按世界等权；"
            "该量评价预测中心的一致性，不是原始噪声观测应当完全相同的要求。",
            "",
            "| 控制 | 归一化pH中心极差 | 自由比例中心极差 | 沉淀比例中心极差 |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for kind, label in (("scale", "尺度"), ("path", "路径")):
        lines.append(
            f"| {label} | "
            + " | ".join(
                f(summary["world_equal_control_spread"][kind][m]["mean"], 6) for m in METRICS
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 复算与解释边界",
            "",
            "运行 `uv run --no-sync python scripts/summarize_abductive_quantitative.py`。"
            "脚本通过 configs/current.json 的当前实验绑定找到设计，"
            "只读取封存会话和 predictions.csv；逐条核对预测中心/区间与封存Q一致，"
            "重新计算误差，并与逐场保存的 MAE、覆盖率和区间宽度对照。",
            f"当前最大重汇总差为 {summary['reaggregation_max_abs_error']}。"
            "机器结果见 quantitative-summary.json；"
            "其 world_equal 字段先按世界内有效会话平均，再等权汇总世界。",
            "",
            "未执行模型或模拟器调用；未把物理阈值提升为认知成功标准；未把预测改善当作反绎的定义。"
            "预测误差、证据可区分性和解释形成是彼此相关但需要分别报告的层次。",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("configs/current.json"))
    args = parser.parse_args()
    binding = read(args.registry)["work_ii"]["w2_263_abductive_completion"]
    root, report = Path(binding["run_root"]), Path(binding["report_root"]) / "experiment"
    design = read(root / "design.json")
    schedule = design["schedule"]
    snapshots = {
        (r["repeat"], r["id"]): r["status"] for r in read_csv(report / "session-summary.csv")
    }
    predictions = defaultdict(list)
    for row in read_csv(report / "predictions.csv"):
        predictions[row["repeat"], row["id"]].append(row)
    sessions = []
    for unit in schedule:
        path = report / "sessions" / unit["repeat"] / f"{unit['id']}.json"
        key = unit["repeat"], unit["id"]
        sessions.append(
            session_row(
                unit,
                read(path) if path.exists() else None,
                snapshots.get(key, "not_exported"),
                predictions[key],
            )
        )
    worlds = {
        name: aggregate([s for s in sessions if s["world"] == name])
        for name in sorted({s["world"] for s in sessions})
    }
    pairs = {
        name: aggregate([s for s in sessions if s["pair"] == name])
        for name in sorted({s["pair"] for s in sessions})
    }
    for name, pair in pairs.items():
        pair_worlds = {key: worlds[key] for key in (f"EQ-{name}-A", f"EQ-{name}-B")}
        pair["world_equal_prediction_groups"] = world_equal_prediction_groups(pair_worlds)
        pair["world_equal_separation"] = {
            key: describe(
                [w["separation_session_statistics"][key]["mean"] for w in pair_worlds.values()]
            )
            for key in (
                "mean_max_channel_gap_sigma",
                "fraction_one_channel_3sigma",
                "fraction_two_channels_3sigma",
            )
        }
    outcomes = Counter()
    for session in sessions:
        outcomes.update(session["operation_outcomes"])
    summary = {
        "schema_version": "chemworld-abductive-quantitative-1.0",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "status": "all_planned_sessions_exported"
        if all(s["exported"] for s in sessions)
        else "interim_sealed_sessions_only",
        "source_attempt": "participant-02",
        "source_commit": design["source_commit"],
        "analysis_unit": (
            "fresh_session; batches, notes, queries and reference assays are nested measurements"
        ),
        "design": {
            "pairs": 5,
            "mechanisms": 2,
            "sessions_per_world": 3,
            "planned_sessions": 30,
            "source_assays_per_session": 12,
            "heldout_queries": 12,
            "reference_repeats": 5,
            "sigma": SIGMA,
            "query_groups": GROUPS,
            "physical_control_sets": CONTROL_SETS,
        },
        "interpretation": (
            "3-sigma physical discrimination is descriptive, not an abduction success criterion; "
            "no model-seed control; fixed keyed observation noise reused across fresh sessions"
        ),
        "retained_startup_attempt": read(Path(binding["retained_attempt_analysis"])),
        "totals": aggregate(sessions),
        "source_completed": sum(s["source_status"] == "completed" for s in sessions),
        "valid_stages": {
            stage: sum(s["sealed_stages_valid"][stage] for s in sessions) for stage in STAGES
        },
        "source_replays_verified": sum(s["source_replay_verified"] for s in sessions),
        "counterfactual_replays_verified": sum(
            sum(s["counterfactual_replays"].values()) for s in sessions
        ),
        "own_world_observations_identical": sum(
            s["own_observations_identical"] is True for s in sessions
        ),
        "own_world_operations_identical": sum(
            s["own_operations_identical"] is True for s in sessions
        ),
        "operation_outcomes": dict(outcomes),
        "prediction_entries": sum(s["prediction_rows"] for s in sessions),
        "reaggregation_max_abs_error": max(
            (
                s["reaggregation_max_abs_error"]
                for s in sessions
                if s["reaggregation_max_abs_error"] is not None
            ),
            default=None,
        ),
        "worlds": worlds,
        "pairs": pairs,
        "world_equal_prediction_groups": world_equal_prediction_groups(worlds),
        "world_equal_control_spread": {
            k: {
                m: describe([w["control_prediction_spread"][k][m]["mean"] for w in worlds.values()])
                for m in METRICS
            }
            for k in CONTROL_SETS
        },
        "sessions": sessions,
    }
    (report / "quantitative-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (report / "QUANTITATIVE.md").write_text(render(summary), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": summary["status"],
                "exported": summary["totals"]["exported_sessions"],
                "planned": 30,
                "valid_Q": summary["totals"]["valid_prediction_sessions"],
                "source_assays": summary["totals"]["source_assays"],
                "reaggregation_max_abs_error": summary["reaggregation_max_abs_error"],
            }
        )
    )


if __name__ == "__main__":
    main()
