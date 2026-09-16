"""Summarize every retained W2-105 condition; never execute an experiment."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from scripts.run_work_ii_astra_full_process_trial import QUALITY, ROOT, TASKS
from scripts.run_work_ii_astra_single_trial import read, write

LABELS = dict(zip(TASKS, ("反应—萃取—纯化", "反应—路径依赖结晶", "反应—分段蒸馏"), strict=True))
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-phase-resolved-process-20260914.json"


def collect(root):
    plans = read(root / "planned_candidates.json")
    contract = plans[0].get("contract", "phase-resolved-process-v1")
    tasks = {p["task"] for p in plans}
    cells = []
    for plan in plans + [
        {"cell": f"A{i + 1}", "task": task, "kind": "agent"}
        for i, task in enumerate(TASKS)
        if task in tasks
    ]:
        path = root / plan["cell"] / "result.json"
        if not path.exists():
            cells.append(
                {
                    **{k: v for k, v in plan.items() if k != "actions"},
                    "status": "not_started",
                    "witness": False,
                }
            )
            continue
        result = read(path)
        a = result["analysis"]
        semantic_failure = (
            "quenched_heat_bypassed_dissolution; not a valid annealing intervention"
            if contract.endswith("v2") and plan["cell"] in {"C17", "C18", "C19", "C20"}
            else None
        )
        if contract.endswith("v3") and plan["cell"] in {"C17", "C18", "C19", "C20"}:
            semantic_failure = (
                "dissolved_seed_origin_lost; recycled seed can inflate new-product yield"
            )
        cells.append(
            {
                "cell": plan["cell"],
                "task": plan["task"],
                "kind": plan["kind"],
                "status": result["status"],
                "witness": result["witness"],
                "assay_truth": {k: result["assay_truth"].get(k) for k in QUALITY[plan["task"]]},
                "truth_quality_checks": result["truth_quality_checks"],
                "semantic_failure": semantic_failure,
                **a,
                "provider_operational_diagnostics": {
                    k: result.get("provider_usage", {}).get(k)
                    for k in (
                        "recovered_mcp_tool_failure_count",
                        "mcp_tool_failure_taxonomy",
                        "pre_action_restart_count",
                        "accepted_turn_continuation_count",
                    )
                }
                if plan["kind"] == "agent"
                else {},
                "provider_configuration": [
                    {
                        k: receipt.get(k)
                        for k in ("model_id", "reasoning_effort", "status", "session_elapsed_s")
                    }
                    for receipt in read(root / plan["cell"] / "receipts.json")
                ]
                if plan["kind"] == "agent"
                else [],
            }
        )
    refs = [c for c in cells if c["kind"] == "reference"]
    agents = [c for c in cells if c["kind"] == "agent"]
    return {
        "schema_version": "work-ii-phase-resolved-process-report-0.1",
        "evidence_mode": "development",
        "full_process_contract_id": contract,
        "experiment_note": "workstreams/flagship_tasks/"
        + {
            "phase-resolved-process-v1": "WORK_II_PHASE_RESOLVED_PROCESS_NOTE.md",
            "phase-resolved-process-v2": "WORK_II_PROCESS_CONTINUITY_NOTE.md",
            "phase-resolved-process-v3": "WORK_II_CRYSTAL_THERMAL_CONTINUITY_NOTE.md",
            "phase-resolved-process-v4": "WORK_II_CRYSTAL_SEED_CONTINUITY_NOTE.md",
        }[contract],
        "run_root": root.relative_to(ROOT).as_posix(),
        "quality_targets": QUALITY,
        "denominator": "original reactant charge; crystals exclude retained seed",
        "counts": {
            "reference_planned": len(refs),
            "reference_attempted": sum(c["status"] != "not_started" for c in refs),
            "reference_final_assays": sum(c.get("final_assays", 0) for c in refs),
            "reference_witnesses": sum(c["witness"] for c in refs),
            "reference_failed_executions": sum(c["status"] == "failed" for c in refs),
            "reference_semantic_failures": sum(bool(c.get("semantic_failure")) for c in refs),
            "agent_planned": len(agents),
            "agent_attempted": sum(c["status"] != "not_started" for c in agents),
            "agent_final_assays": sum(c.get("final_assays", 0) for c in agents),
            "agent_quality_passes": sum(c.get("quality_passed", False) for c in agents),
            "agent_failed_executions": sum(c["status"] == "failed" for c in agents),
            "recorded_operations": sum(c.get("operations", 0) for c in cells),
            "verified_trajectories": sum(c.get("replay", {}).get("verified", False) for c in cells),
        },
        "task_witnesses": {
            t: [c["cell"] for c in refs if c["task"] == t and c["witness"]] for t in TASKS
        },
        "cells": cells,
    }


def pct(x):
    return "—" if x is None else f"{100 * x:.2f}%"


def plot(report, output):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    historical = None
    if report["full_process_contract_id"].endswith("v2"):
        binding = read(ROOT / "configs/current.json")["work_ii"]["w2_105_phase_resolved_process"]
        historical_path = ROOT / binding["report"]
        if hashlib.sha256(historical_path.read_bytes()).hexdigest() != binding["report_sha256"]:
            raise ValueError("previous report binding mismatch")
        historical = read(historical_path)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
    for task, ax, title in zip(
        TASKS,
        axes,
        ("Reaction + purification", "Reaction + crystallization", "Reaction + distillation"),
        strict=True,
    ):
        quality_keys = list(QUALITY[task])
        xkey = quality_keys[1]
        ykey = "crystal_fines_fraction" if task == TASKS[1] else quality_keys[0]
        ax.axvline(0.1, color="#555555", linestyle=":", linewidth=1)
        ax.axhline(0.5 if task == TASKS[1] else 0.8, color="#555555", linestyle=":", linewidth=1)
        ax.fill_between(
            [0.1, 1],
            0 if task == TASKS[1] else 0.8,
            0.5 if task == TASKS[1] else 1,
            color="#e5f4e8",
            zorder=0,
        )
        for data, color, marker, label in (
            (historical, "#a9afb8", "o", "Previous contract"),
            (report, "#236b9b", "o", "Current candidates"),
        ):
            if data is None:
                continue
            rows = [
                c
                for c in data["cells"]
                if c["task"] == task
                and c["kind"] == "reference"
                and c.get("assay_truth", {}).get(xkey) is not None
            ]
            ax.scatter(
                [c["assay_truth"][xkey] for c in rows],
                [c["assay_truth"][ykey] for c in rows],
                s=32,
                color=color,
                marker=marker,
                alpha=0.7,
                label=label,
            )
        rows = [
            c
            for c in report["cells"]
            if c["task"] == task
            and c["kind"] == "agent"
            and c.get("assay_truth", {}).get(xkey) is not None
        ]
        if rows:
            ax.scatter(
                [c["assay_truth"][xkey] for c in rows],
                [c["assay_truth"][ykey] for c in rows],
                marker="*",
                s=170,
                color="#b02b30",
                label="Astra / medium",
                zorder=5,
            )
        xmax = max(
            [0.5]
            + [
                c.get("assay_truth", {}).get(xkey, 0) or 0
                for data in (historical, report)
                if data
                for c in data["cells"]
                if c["task"] == task
            ]
        )
        ax.set(
            xlim=(0, min(1.04, xmax + 0.05)),
            ylim=(0, 1.04),
            title=title,
            xlabel="Yield from original charge"
            if task == TASKS[1]
            else "Recovery from original charge",
            ylabel="Fines number fraction" if task == TASKS[1] else "Product purity",
        )
        ax.xaxis.set_major_formatter(PercentFormatter(1))
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=7, loc="lower right" if task != TASKS[1] else "upper right")
    fig.savefig(output.with_suffix(".png"), dpi=180)
    plt.close(fig)


def markdown(report):
    n = report["counts"]
    lines = [
        "# 相分辨完整流程：开发资格与单轮Agent",
        "",
        "2026-09-14—15；开发结果，不是正式论文证据。",
        "",
        f"无模型候选{n['reference_attempted']}/{n['reference_planned']}启动，"
        f"{n['reference_final_assays']}次终检，{n['reference_witnesses']}个联合质量见证；"
        f"{n['reference_failed_executions']}次执行失败。",
        f"Astra / medium预定{n['agent_planned']}个任务位，启动{n['agent_attempted']}个、"
        f"终检{n['agent_final_assays']}个、带噪质量达标{n['agent_quality_passes']}个。",
        "",
        "门槛保持：纯度≥80%、原始投料回收/扣晶种产率≥10%，结晶另要求细粉≤50%。"
        "见证要求取样前真值和带噪终检均过门槛，且零事务失败、重放和资源校验通过。",
        "",
        "## 各任务资格",
        "",
        "| 任务 | 见证数/预定 | 见证 |",
        "| --- | --- | --- |",
    ]
    for task in TASKS:
        witnesses = report["task_witnesses"][task]
        denominator = sum(c["kind"] == "reference" and c["task"] == task for c in report["cells"])
        if not denominator:
            continue
        lines.append(
            f"| {LABELS[task]} | {len(witnesses)}/{denominator} | {', '.join(witnesses) or '无'} |"
        )
    lines += [
        "",
        "## 全部终检结果",
        "",
        "表中为取样前真值；带噪读数及逐步测量完整保存在JSON。未达标不等于物理不可能。",
        "",
        "| 条件 | 任务 | 记录动作 | 真值纯度 | 真值回收/产率 | 真值细粉 | 带噪达标 | 联合见证 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in report["cells"]:
        keys = list(QUALITY[c["task"]])
        m = c.get("assay_truth", {})
        lines.append(
            f"| {c['cell']} | {LABELS[c['task']]} | {c.get('operations', '—')} | "
            f"{pct(m.get(keys[0]))} | {pct(m.get(keys[1]))} | "
            f"{pct(m.get('crystal_fines_fraction'))} | "
            f"{c.get('quality_passed', '未启动')} | {c['witness']} |"
        )
    lines += ["", "## 失败与未启动", ""]
    for c in report["cells"]:
        if c["status"] == "not_started":
            lines.append(f"- {c['cell']}：本块未启动；最终合同下的实际模型槽位以统一收束报告为准。")
        elif c["status"] == "failed" or c.get("failures"):
            lines.append(f"- {c['cell']}：{c.get('failure')}；事务失败：{c.get('failures')}。")
        if c.get("semantic_failure"):
            detail = (
                "淬灭后的加热未调用溶解服务；事务虽提交，但不是有效退火干预。"
                "阴性结果不能解释为退火无效。"
                if c["semantic_failure"].startswith("quenched_heat")
                else "溶解的晶种来源未在母液保留，再析出可能抬高新产物产率；"
                "该产率不作为有效资格证据。修正块保留相同覆盖重新执行。"
            )
            lines.append(f"- {c['cell']}：{detail}")
    lines += [
        "",
        "## 资源与检查",
        "",
        f"共{n['recorded_operations']}条持久动作，{n['verified_trajectories']}条轨迹精确重放。",
        "所有物理费用、时间、采样、库存、模型会话/响应/token按条件保存在JSON；"
        "订阅费用无法逐次归因，缺失费用不记作零。",
        "",
        "## 解释边界",
        "",
        "此块首先验证环境合同与任务可达性；不证明Agent的系统性失效或信息损失机制。"
        "参考候选是有限开发覆盖，不是最优策略，不把未成功搜索解释为不可达。"
        "单次Agent只能生成后续干预假说，不能支撑跨世界因果结论。",
        "",
        "新旧合同的回收分母不同，不能把新旧数字当作模型性能提升。旧失败保留。",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--bind", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--binding-key", default="w2_105_phase_resolved_process")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    report = collect(args.root.resolve())
    output = args.report.resolve()
    write(output, report)
    output.with_suffix(".md").write_text(markdown(report), encoding="utf-8")
    if args.plot:
        plot(report, output)
    if args.bind:
        current = read(ROOT / "configs/current.json")
        current["work_ii"][args.binding_key] = {
            "report": output.relative_to(ROOT).as_posix(),
            "report_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "run_root": report["run_root"],
            "evidence_mode": "development",
            "counts": report["counts"],
        }
        write(ROOT / "configs/current.json", current)
    print(report["counts"])


if __name__ == "__main__":
    main()
