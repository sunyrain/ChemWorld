"""Analyze retained pilot evidence; never call a provider or execute a new batch."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import numpy as np
from scripts.run_work_ii_astra_corrected_pilot import (
    METRICS,
    REPORT,
    SOURCES,
    TRAIN,
    WORLDS,
    predict_reference,
    read,
    write,
)


def mean_or_none(values):
    return float(np.mean(values)) if values else None


def error_summary(rows):
    return {
        "n": len(rows),
        **{k: mean_or_none([r["absolute_error"][k] for r in rows]) for k in METRICS},
    }


def draw_diagnostics(report):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lookup = {r["condition"]: r for r in report["conditions"]}
    names = [f"{source}_{kind}" for source in SOURCES for kind in ("raw", "whole", "component")]
    names.append("task_only")
    if any(name not in lookup or "mae" not in lookup[name] for name in names):
        return None
    labels = [
        "Std / raw",
        "Std / whole",
        "Std / component",
        "Structured / raw",
        "Structured / whole",
        "Structured / component",
        "No knowledge",
    ]
    colors = ["#356999"] * 3 + ["#D58A32"] * 3 + ["#929292"]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.3), gridspec_kw={"width_ratios": [1, 1, 1.05]})
    positions = np.arange(len(names))
    axes[0].barh(
        positions, [lookup[n]["mae"]["heldout"]["crystal_yield"] for n in names], color=colors
    )
    axes[0].set(
        yticks=positions,
        yticklabels=labels,
        xlabel="Held-out recovery MAE (lower is better)",
        title="Prediction | 6 fixed queries",
    )
    axes[0].invert_yaxis()
    axes[1].barh(
        positions, [lookup[n]["heldout_mean_utility"] for n in names], color=colors, alpha=0.7
    )
    for world, marker, color in (("R1C2", "o", "#172A3B"), ("R2C1", "x", "#90485D")):
        axes[1].scatter(
            [lookup[n]["deployment"][world]["utility_per_hour"] for n in names],
            positions,
            marker=marker,
            color=color,
            label=world,
            zorder=3,
        )
    axes[1].set(
        yticks=positions,
        yticklabels=labels,
        xlabel="Product estimate per process hour",
        title="Deployment | bar = two-pair mean",
    )
    axes[1].invert_yaxis()
    historical = [
        r["terminal"]["utility_per_hour"]
        for r in report["reference_deployments"]
        if r["name"].startswith("reference/standard/best_history/")
        and r["world"] in WORLDS[2:]
        and r["status"] == "completed"
    ]
    if len(historical) == 2:
        axes[1].axvline(
            float(np.mean(historical)),
            linestyle="--",
            color="#444444",
            linewidth=1,
            label="Best source recipe (mean)",
        )
    axes[1].legend(loc="best", fontsize=8)
    kinds = ["swap_R", "swap_C", "sham", "repair_R", "repair_C"]
    baseline = lookup["standard_component"]["heldout_mean_utility"]
    deltas = [lookup.get(f"standard_{kind}", {}).get("heldout_mean_utility") for kind in kinds]
    if all(d is not None for d in deltas):
        deltas = [d - baseline for d in deltas]
        axes[2].barh(
            np.arange(5), deltas, color=["#477A66" if d >= 0 else "#B26464" for d in deltas]
        )
        axes[2].set(
            yticks=np.arange(5),
            yticklabels=["Swap R", "Swap C", "Reorder only", "R data table", "C data table"],
            xlabel="Mean utility change vs standard component",
            title="Content interventions | 1 call each",
        )
        axes[2].invert_yaxis()
        axes[2].axvline(0, color="#333333", linewidth=0.8)
    for ax in axes:
        ax.spines[["right", "top"]].set_visible(False)
        ax.grid(axis="x", alpha=0.18)
        ax.set_axisbelow(True)
    fig.suptitle("Development pilot: one component group, one call per condition", fontsize=14)
    support = []
    for source in SOURCES:
        rows = [r for r in report["support"] if r["source"] == source and r["world"] in WORLDS[2:]]
        support.append(f"{source}: {sum(r['near_support'] for r in rows)}/{len(rows)}")
    fig.text(
        0.5,
        0.015,
        "Near-support held-out queries: "
        + "; ".join(support)
        + ". Descriptive results; no uncertainty estimates or systematic-failure claim.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.055, 1, 0.93))
    path = REPORT.with_suffix(".png")
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return path.name


def analyze(root: Path):
    if not (root / "closed.json").exists():
        raise ValueError("analyze only a closed experiment block")
    report = deepcopy(read(root / "summary.json"))
    report["model_call_unit"] = (
        "One scheduled fresh model session, including any public-numerics tool turns; "
        "not a count of HTTP requests."
    )
    for call in report["model_call_rows"]:
        audit = root / "model" / call["name"] / "numerics.jsonl"
        call["public_numerics_attempts"] = (
            sum(bool(line.strip()) for line in audit.read_text(encoding="utf-8").splitlines())
            if audit.exists()
            else 0
        )
    lookup = {r["condition"]: r for r in report["conditions"]}
    for condition in report["conditions"]:
        for split, worlds in (("learning", TRAIN), ("heldout", WORLDS[2:])):
            rows = [r for r in condition.get("errors", []) if r["world"] in worlds]
            condition.setdefault("support_strata", {})[split] = {
                label: error_summary([r for r in rows if r["near_support"] is flag])
                for label, flag in (("near_support", True), ("outside_support", False))
            }
        condition["heldout_mean_utility"] = mean_or_none(
            [
                condition.get("deployment", {}).get(w, {}).get("utility_per_hour")
                for w in WORLDS[2:]
                if condition.get("deployment", {}).get(w, {}).get("utility_per_hour") is not None
            ]
        )
    pairs = [(f"{s}_raw", f"{s}_{rep}") for s in SOURCES for rep in ("whole", "component")]
    pairs += [(f"standard_{rep}", f"diagnostic_{rep}") for rep in ("raw", "whole", "component")]
    pairs += [
        ("standard_component", f"standard_{name}")
        for name in ("swap_R", "swap_C", "sham", "repair_R", "repair_C")
    ]
    contrasts = []
    for base, treatment in pairs:
        a, b = lookup.get(base), lookup.get(treatment)
        if not a or not b or "mae" not in a or "mae" not in b:
            contrasts.append({"base": base, "treatment": treatment, "status": "missing_condition"})
            continue
        contrasts.append(
            {
                "base": base,
                "treatment": treatment,
                "status": "descriptive_single_call",
                "heldout_mae_treatment_minus_base": {
                    k: b["mae"]["heldout"][k] - a["mae"]["heldout"][k] for k in METRICS
                },
                "heldout_mean_utility_treatment_minus_base": b["heldout_mean_utility"]
                - a["heldout_mean_utility"],
            }
        )
    report["contrasts"] = contrasts
    references = (
        read(root / "reference_models.json") if (root / "reference_models.json").exists() else {}
    )
    truth = read(root / "blind_truth.json") if (root / "blind_truth.json").exists() else {}
    reference_errors = []
    for source, model in references.items():
        for kind in ("component", "whole"):
            rows = []
            for q, actual in truth.items():
                if actual["status"] != "completed":
                    continue
                prediction = predict_reference(model, actual["world"], actual["plan"], kind)
                if prediction is None:
                    continue
                target = {
                    "reaction_yield": actual["public"]["upstream_hplc"]["yield"],
                    **{k: actual["public"]["terminal"][k] for k in METRICS[1:]},
                }
                rows.append(
                    {
                        "query": q,
                        "world": actual["world"],
                        "truth": target,
                        "prediction": {k: prediction[k] for k in METRICS},
                        "absolute_error": {k: abs(prediction[k] - target[k]) for k in METRICS},
                    }
                )
            reference_errors.append(
                {
                    "source": source,
                    "kind": kind,
                    "query_rows": rows,
                    "learning": error_summary([r for r in rows if r["world"] in TRAIN]),
                    "heldout": error_summary([r for r in rows if r["world"] in WORLDS[2:]]),
                    "qualified_strong_reference": False,
                }
            )
    report["public_reference_prediction_diagnostics"] = reference_errors
    for row in report["physical_rows"]:
        original = read(root / "physical" / row["name"] / "result.json")
        public = original.get("public") or {}
        for field in ("actual_quench_temperature_K", "actual_cooling_temperature_K"):
            row[field] = public.get(field)
    report["reference_deployments"] = [
        r for r in report["physical_rows"] if r["name"].startswith("reference/")
    ]
    opportunity = []
    for world in WORLDS:
        rows = [
            r
            for r in report["physical_rows"]
            if r["world"] == world
            and r["name"].startswith("qualification/")
            and r["status"] == "completed"
        ]
        if not rows:
            continue
        best = max(rows, key=lambda r: r["terminal"]["utility_per_hour"])
        opportunity.append(
            {
                "world": world,
                "tested_plans": len(rows),
                "best_tested_plan": best["plan"],
                "best_tested_utility": best["terminal"]["utility_per_hour"],
                "worst_tested_utility": min(r["terminal"]["utility_per_hour"] for r in rows),
                "interpretation": "best of eight prespecified E0 plans; not a true optimum",
            }
        )
    report["qualification_decision_opportunity"] = opportunity
    report["knowledge_packages"] = []
    for path in sorted((root / "packages").glob("*.json")):
        package = read(path)
        report["knowledge_packages"].append(
            {
                "name": path.stem,
                "valid": package["valid"],
                "characters": sum(len(v) for v in (package.get("payload") or {}).values()),
            }
        )
    engineering = read(root.parent / "work-ii-astra-corrected-pilot-20260914" / "summary.json")
    report["preceding_engineering_block"] = {
        "report": "workstreams/flagship_tasks/reports/work-ii-astra-corrected-pilot-20260914.json",
        "status": engineering["status"],
        "physical_runs": engineering["physical_runs"],
        "model_calls": engineering["model_calls"],
        "stop_reason": engineering["stop_reason"],
        "same_world_initialization": True,
    }
    report["analysis_version"] = "retained-evidence-summary-1"
    report["diagnostic_figure"] = draw_diagnostics(report)
    write(REPORT, report)
    lines = [
        "# Astra medium：修正合同后的单次开发实验",
        "",
        "本轮采用两次必需HPLC、按公开实际温度解析的冷却配方，以及基于公开测量的产物效用。",
        "一组反应—结晶四格世界，每条件一次；属于开发诊断，不是正式论文证据。",
        "",
        f"状态：{report['status']}。模型完成 {report['model_calls']['completed']}/20，零重试。",
        "这里一次模型调用指一个预定fresh会话，允许预算内公共数值工具续轮；不等于一次HTTP请求。",
        f"当前块物理完成 {report['physical_runs']['completed']}/164，"
        f"失败 {report['physical_runs']['failed']}，"
        f"未执行 {report['physical_runs']['not_started']}；"
        "精确重放通过 "
        f"{report['physical_runs']['exact_replay_verified']}。",
        "另保留前一工程块1条温度检查失败：其12步操作均提交、重放通过、零模型调用。",
        "修正后沿用相同世界初始化，从首条检查重新验证。",
        "完成范围：32条E0、48条取证、12条盲测、48条Agent部署、24条参考部署；4份知识包有效。",
        "",
        "## 主要观察",
        "",
        "- 有实验知识的六种基本条件留出平均效用约0.312–0.316，无知识条件约0.051。",
        "- 整流程/组件表示没有带来明显的行动效用损失；反应与回收预测误差仍有差异。",
        "- 直接复用历史最优配方约0.310，距离组件包约2%；当前实例的行动区分度不足。",
        "- C身份置换平均效用约0.258，内容重排约0.316；这是人为内容干预的单次结果，不是自发遗忘。",
        "- 三来源的留出查询近支持均为0/6，不能据本轮解释纯组合泛化或系统性信息损失。",
        f"\n![开发试跑结果]({report['diagnostic_figure']})\n"
        if report["diagnostic_figure"]
        else "",
        "",
        "## 预测与首次部署",
        "",
        "学习和留出分别6条预定查询。MAE越低越好；效用为质量加权回收估计/过程小时，越高越好。",
        "效用使用HPLC反应产率、扣种回收率、固体纯度和实际过程时间；不是精确摩尔产率。",
        "",
        "| 条件 | 留出反应MAE | 留出回收MAE | 留出纯度MAE | R1C2效用/h | R2C1效用/h |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for condition in report["conditions"]:
        if "mae" not in condition:
            lines.append(f"| {condition['condition']} | 未完成 | — | — | — | — |")
            continue
        e, d = condition["mae"]["heldout"], condition["deployment"]
        lines.append(
            f"| {condition['condition']} | {e['reaction_yield']:.4f} | {e['crystal_yield']:.4f} | "
            f"{e['crystal_purity']:.4f} | {d['R1C2']['utility_per_hour']:.4f} | "
            f"{d['R2C1']['utility_per_hour']:.4f} |"
        )
    lines += [
        "",
        "## 同证据与内容干预",
        "",
        "以下均为处理条件减去基准；预测误差差为负表示误差减小，效用差为正表示改善。",
        "单次fresh调用存在采样波动；sham用于显示这一局限，不能凭单次置换差定位内部因果机制。",
        "",
        "| 基准 → 处理 | 反应MAE差 | 回收MAE差 | 留出平均效用差 |",
        "| --- | --- | --- | --- |",
    ]
    for contrast in contrasts:
        if contrast["status"] != "descriptive_single_call":
            continue
        e = contrast["heldout_mae_treatment_minus_base"]
        lines.append(
            f"| {contrast['base']} → {contrast['treatment']} | {e['reaction_yield']:+.4f} | "
            f"{e['crystal_yield']:+.4f} | "
            f"{contrast['heldout_mean_utility_treatment_minus_base']:+.4f} |"
        )
    lines += [
        "",
        "## 联合覆盖",
        "",
        "基于公开yield/conversion、实际淬灭温度、实际冷却温度和log时长的5维凸包距离。",
        "≤0.05为事前定义的近支持；这不是完整隐状态支持证明。所有事前查询均保留。",
        "",
        "| 来源 | 学习查询近支持 | 留出查询近支持 |",
        "| --- | --- | --- |",
    ]
    for source in (*SOURCES, "space_filling"):
        counts = []
        for worlds in (TRAIN, WORLDS[2:]):
            rows = [r for r in report["support"] if r["source"] == source and r["world"] in worlds]
            counts.append(f"{sum(r['near_support'] for r in rows)}/{len(rows)}")
        lines.append(f"| {source} | {counts[0]} | {counts[1]} |")
    lines += [
        "",
        "各条件在近支持/域外查询上的误差与确切分母见JSON的support_strata。",
        "支持不足时，本轮留出结果混合了组合迁移与外推，不能概括为纯组合失效。",
        "",
        "## 公开数据参考",
        "",
        "固定岭回归只是小样本经验参考，尚未获得强系统辨识资格。",
        "",
        "| 来源 | 参考 | 留出反应MAE | 留出回收MAE |",
        "| --- | --- | --- | --- |",
    ]
    for reference in reference_errors:
        e = reference["heldout"]
        if e["n"]:
            lines.append(
                f"| {reference['source']} | {reference['kind']} | "
                f"{e['reaction_yield']:.4f} | {e['crystal_yield']:.4f} |"
            )
    lines += ["", "| 来源 | 部署参考 | R1C2效用/h | R2C1效用/h |", "| --- | --- | --- | --- |"]
    for source in SOURCES:
        for kind in ("component", "whole", "best_history"):
            values = []
            for world in WORLDS[2:]:
                name = f"reference/{source}/{kind}/{world}"
                row = next((r for r in report["reference_deployments"] if r["name"] == name), None)
                values.append(
                    f"{row['terminal']['utility_per_hour']:.4f}"
                    if row and row["status"] == "completed"
                    else "未完成"
                )
            lines.append(f"| {source} | {kind} | {values[0]} | {values[1]} |")
    lines += [
        "",
        "## 资源、失败与解释边界",
        "",
        f"模型报告token用量：`{json.dumps(report['reported_model_usage'])}`。订阅费用未估算美元数。",
        f"物理资源合计：`{json.dumps(report['physical_resources'])}`。包含E0和参考；逐批资源在JSON中。",
        "知识包字符数、各次模型用量、全部物理参数/终态与失败均列于JSON；原始provider与私有初始化留在ignored目录。",
        "实际温度由公共操作schema读取；执行器不按HPLC结果改配方，不能称完整自主闭环科学家。",
    ]
    if report["stop_reason"]:
        lines.append(f"停止原因：{report['stop_reason']}")
    for row in report["physical_rows"] + report["model_call_rows"]:
        if row["status"] != "completed":
            lines.append(f"- {row['name']}：{row['failure']}")
    REPORT.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"status": report["status"], "conditions": len(lookup), "contrasts": len(contrasts)}
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    analyze(parser.parse_args().output.resolve())
