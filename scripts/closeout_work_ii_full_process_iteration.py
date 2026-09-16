"""Author-facing closeout of the four retained development blocks."""

# ruff: noqa: RUF001
from __future__ import annotations

import hashlib

from scripts.analyze_work_ii_phase_resolved_process import LABELS, pct, plot
from scripts.run_work_ii_astra_full_process_trial import QUALITY, ROOT, TASKS
from scripts.run_work_ii_astra_single_trial import read, write

OUTPUT = ROOT / "workstreams/flagship_tasks/reports/work-ii-full-process-iteration-20260915.json"


def trajectory_note(model):
    task = model["task"]
    measurements = {x["step"]: x["metrics"] for x in model.get("measurements", [])}
    if task == TASKS[0]:
        before, after = measurements[19], measurements[23]
        return (
            "第19至23步之间，Agent执行干燥、浓缩和再次洗涤。公开纯度读数从"
            f"{pct(before['purity'])}降至{pct(after['purity'])}，原投料回收从"
            f"{pct(before['recovery'])}降至{pct(after['recovery'])}。"
            "这是后处理区间的交付质量损失；多个动作合在一起，尚不能分离各动作效应。"
            "模型在终答中如实指出两项目标均未达标，没有把高转化率当作最终成功。"
        )
    if task == TASKS[2]:
        gc = next(x for x in model["measurements"] if x["instrument"] == "gc")
        return (
            "Agent使用了独立切段比例0.15、回流比10和3600秒蒸馏，随后GC纯度读数为"
            f"{pct(gc['metrics']['distillate_purity'])}，收集后出现provider错误。"
            "没有终检，不能把过程读数算作联合达标，也不能判为科学能力失败。"
            "回执仅给出未分类provider错误摘要，没有HTTP状态或具体服务原因；"
            "token用量缺失，不计为零。保留13步前缀，不补跑。"
        )
    hours = model["resources"]["process_time_s"] / 3600
    return (
        "模型先在三段各4小时冷却中降至250 K，第一次粒径读数为100%细粉；"
        "随后复热至290 K、加入10 mg晶种，再用4小时降至250 K，第二次粒径读数仍为100%。"
        f"随后过滤并终检，共用{hours:.2f}/100小时物理时间。"
        "模型识别了细粉问题并尝试修复，也如实报告最终未达标。"
        "这一轨迹提出的是修复策略与不可逆关闭时机问题；剩余时间多不等于同前缀仍可挽救，"
        "更不能据此声称它没有看到反馈或丢失了知识。"
    )


def main():
    current = read(ROOT / "configs/current.json")
    keys = (
        "w2_105_phase_resolved_process",
        "w2_105b_process_continuity",
        "w2_105c_crystal_thermal_continuity",
        "w2_105d_crystal_seed_continuity",
    )
    reports = []
    for key in keys:
        binding = current["work_ii"][key]
        path = ROOT / binding["report"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != binding["report_sha256"]:
            raise ValueError(f"report binding mismatch: {key}")
        reports.append(read(path))
    _a, b, historical_c, d = reports
    cells = [x for x in b["cells"] if x["task"] != TASKS[1]] + d["cells"]
    refs = [x for x in cells if x["kind"] == "reference"]
    agents = sorted(
        [x for x in cells if x["kind"] == "agent"], key=lambda x: TASKS.index(x["task"])
    )
    quality_successes = sum(
        x.get("quality_passed", False)
        and bool(x.get("truth_quality_checks"))
        and all(x["truth_quality_checks"].values())
        for x in agents
    )
    seed_corrections = []
    for cell_id in ("C17", "C18", "C19", "C20"):
        old = next(x for x in historical_c["cells"] if x["cell"] == cell_id)
        new = next(x for x in d["cells"] if x["cell"] == cell_id)
        seed_corrections.append(
            {
                "cell": cell_id,
                "old_reported_yield": old["assay_truth"]["crystal_yield"],
                "corrected_yield": new["assay_truth"]["crystal_yield"],
                "purity_delta": new["assay_truth"]["crystal_purity"]
                - old["assay_truth"]["crystal_purity"],
                "fines_delta": new["assay_truth"]["crystal_fines_fraction"]
                - old["assay_truth"]["crystal_fines_fraction"],
                "physical_cost_delta": new["resources"]["physical_cost"]
                - old["resources"]["physical_cost"],
            }
        )
    result = {
        "schema_version": "work-ii-full-process-iteration-closeout-0.1",
        "evidence_mode": "development",
        "sources": {k: current["work_ii"][k] for k in keys},
        "counts": {
            "all_reference_attempts": sum(r["counts"]["reference_attempted"] for r in reports),
            "all_reference_final_assays": sum(
                r["counts"]["reference_final_assays"] for r in reports
            ),
            "all_reference_execution_failures": sum(
                r["counts"]["reference_failed_executions"] for r in reports
            ),
            "all_reference_semantic_failures": sum(
                r["counts"].get("reference_semantic_failures", 0) for r in reports
            ),
            "current_reference_candidates": len(refs),
            "current_reference_witnesses": sum(x["witness"] for x in refs),
            "agent_planned": len(agents),
            "agent_attempted": sum(x["status"] != "not_started" for x in agents),
            "agent_final_assays": sum(x.get("final_assays", 0) for x in agents),
            "agent_observed_quality_passes": sum(x.get("quality_passed", False) for x in agents),
            "agent_joint_quality_passes": quality_successes,
            "agent_valid_successes": sum(x.get("witness", False) for x in agents),
            "agent_execution_failures": sum(x["status"] == "failed" for x in agents),
            "agent_token_accounting_complete": sum(
                x.get("provider_usage", {}).get("provider_token_accounting_complete", False)
                for x in agents
            ),
            "agent_failed_transactions": sum(len(x.get("failures", [])) for x in agents),
            "agent_recovered_mcp_tool_failures": sum(
                x.get("provider_operational_diagnostics", {}).get(
                    "recovered_mcp_tool_failure_count"
                )
                or 0
                for x in agents
            ),
            "recorded_operations": sum(r["counts"]["recorded_operations"] for r in reports),
            "verified_trajectories": sum(r["counts"]["verified_trajectories"] for r in reports),
        },
        "task_witnesses": {
            t: [x["cell"] for x in refs if x["task"] == t and x["witness"]] for t in TASKS
        },
        "quality_targets": QUALITY,
        "seed_origin_corrections": seed_corrections,
        "trajectory_observations": {x["task"]: trajectory_note(x) for x in agents},
        "cells": cells,
        "validation": {
            "reference_coverage_complete": all(
                r["counts"]["reference_planned"] == r["counts"]["reference_attempted"]
                for r in reports
            ),
            "all_durable_trajectories_replayed": all(
                x.get("replay", {}).get("verified", False)
                for r in reports
                for x in r["cells"]
                if x.get("operations", 0)
            ),
            "all_recorded_resources_reconciled": all(
                all(x.get("validation", {}).values())
                for r in reports
                for x in r["cells"]
                if x.get("operations", 0)
            ),
            "three_unique_agent_task_slots": len(agents) == 3
            and {x["task"] for x in agents} == set(TASKS),
            "seed_fix_preserves_purity_and_fines": all(
                abs(x["purity_delta"]) < 1e-12 and abs(x["fines_delta"]) < 1e-12
                for x in seed_corrections
            ),
            "each_agent_one_astra_medium_session": all(
                len(x.get("provider_configuration", [])) == 1
                and x["provider_configuration"][0]["model_id"] == "gpt-6-astra"
                and x["provider_configuration"][0]["reasoning_effort"] == "medium"
                and x.get("provider_usage", {}).get("provider_process_attempt_count") == 1
                for x in agents
                if x["status"] != "not_started"
            ),
        },
        "full_process_contract_id": "phase-resolved-process-v2+v4",
        "limits": [
            "single hidden world per task; no across-world inference",
            "one Astra episode per task",
            "reference feasibility uses one observation-noise seed; not a robustness estimate",
            "purification/distillation: 12-hour process budget; crystallization: 100-hour budget",
            "bounded synthetic instruments and reduced physical models; "
            "not empirical chemistry validation",
        ],
    }
    write(OUTPUT, result)
    n = result["counts"]
    lines = [
        "# 完整流程开发迭代收束",
        "",
        "2026-09-14—15；GPT-6 Astra / medium。",
        "",
        f"本轮累计{n['all_reference_attempts']}个无模型候选，"
        f"{n['all_reference_final_assays']}次终检、{n['all_reference_execution_failures']}次执行失败；"
        "另外明确保留4个未真正触发溶解的无效退火干预，"
        "以及4个丢失母液晶种来源、可能高估产率的热循环。",
        f"当前合同下保留{n['current_reference_candidates']}个资格候选、"
        f"{n['current_reference_witnesses']}个联合质量见证。"
        f"Astra启动{n['agent_attempted']}/{n['agent_planned']}，完成终检{n['agent_final_assays']}，"
        f"带噪目标达标{n['agent_observed_quality_passes']}，真值与带噪共同达标"
        f"{n['agent_joint_quality_passes']}；每任务一次，未补跑模型。",
        "质量通过与执行完整性分别计数，provider中断不作为科学失败。",
        "",
        "## 完成的合同修复",
        "",
        "1. 液体读数与实际扣样对象一致，保存馏分不被其他相的测量消耗；"
        "回收率保留原始投料分母。结晶固液仍是明确声明的代表性浆料抽象。",
        "2. 保存馏分可用零转移量合法重选；蒸馏开放底层已有的独立切出比例，"
        "解除时长与累计混入量的绑定，保留实际热负荷限制。",
        "3. 粒径变为带噪、付费、非破坏性过程观测。结晶跨操作保留完整粒子群，"
        "取样/过滤同步扣减粒子数；复热实际触发溶解并同步粒径和热量。",
        "4. 晶种来源跨固相/母液、取样、过滤和再析出守恒；过滤后继续操作也读取当前来源。"
        "相内均匀示踪是明确的模型近似，不声称解析核壳。旧合同继续可重放，"
        "发现的平台状态损失与物理产品损失单独记录，不计作Agent科学能力失败。",
        "5. 溶解热同时进入热转移记录、累计能量和既有能耗费用公式，收费系数不变。",
        "",
        "## 当前资格与单次Agent",
        "",
        "资格要求原始投料回收/扣晶种产率≥10%、纯度≥80%；结晶另要求细粉≤50%。"
        "参考见证须同时通过取样前真值、带噪终检、事务、资源与重放检查。",
        "Astra表为带噪终检；下方见证表和图使用取样前真值。",
        "",
        "| 任务 | 当前资格见证/候选 | Astra状态 | 终检纯度 | 终检回收/产率 | 终检细粉 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for task in TASKS:
        taskrefs = [x for x in refs if x["task"] == task]
        model = next(x for x in agents if x["task"] == task)
        m = model.get("final_metrics", {})
        qkeys = list(QUALITY[task])
        if model["status"] == "not_started":
            outcome = "未启动"
        elif model["status"] == "failed":
            outcome = "终检后执行异常" if model.get("final_assays") else "执行中断"
        elif model.get("quality_passed") and all(model.get("truth_quality_checks", {}).values()):
            outcome = "联合质量达标"
        else:
            outcome = "完成，质量未达标"
        lines.append(
            f"| {LABELS[task]} | {sum(x['witness'] for x in taskrefs)}/{len(taskrefs)} | "
            f"{outcome} | {pct(m.get(qkeys[0]))} | {pct(m.get(qkeys[1]))} | "
            f"{pct(m.get('crystal_fines_fraction'))} |"
        )
    lines += [
        "",
        "下列参考配方只证明存在可行路径，未交给Astra；不是最优性主张。",
        "资格使用固定观测噪声种子；靠近门槛的见证还不能保证独立噪声下稳定通过。",
        "",
        "| 任务 | 保留的见证 | 真值纯度 | 真值原投料回收/产率 | 真值细粉 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for task in TASKS:
        for ref in (x for x in refs if x["task"] == task and x["witness"]):
            m = ref["assay_truth"]
            qkeys = list(QUALITY[task])
            lines.append(
                f"| {LABELS[task]} | {ref['cell']} | {pct(m.get(qkeys[0]))} | "
                f"{pct(m.get(qkeys[1]))} | {pct(m.get('crystal_fines_fraction'))} |"
            )
    lines += [
        "",
        "纯化/蒸馏物理时间预算12小时；结晶100小时，结晶参考投料及既定晶种库存不变。"
        "Agent自主选择合法投料，下表另报实际用量。"
        "不能将不同预算、不同合同的结果当作模型提升比较。",
        "",
        "![质量—回收图](work-ii-full-process-iteration-20260915.png)",
        "",
        "图中显示取样前真值。结晶绿色区域还要求化学纯度≥80%，须结合表格和JSON检查。",
        "",
        "## Astra轨迹与失败",
        "",
    ]
    for model in agents:
        lines += [f"### {LABELS[model['task']]}", ""]
        if model["status"] == "not_started":
            lines += ["未启动：尚无相应有效联合见证。", ""]
            continue
        lines += [
            f"记录{model.get('operations')}次操作，成功提交{model.get('committed')}次；"
            f"过程测量{model.get('nonfinal_instruments')}次，"
            f"失败事务{len(model.get('failures', []))}次。",
            "",
            result["trajectory_observations"][model["task"]],
            "",
            "逐步动作、公开读数、原生真值和模型终答见本报告JSON。模型终答是自述，"
            "不能代替实际终检。",
            "",
        ]
    lines += [
        "## 资源与执行完整性",
        "",
        "| 任务 | 投料mol/晶种g | 物理时长/小时 | 非终检测量 | 消耗样品/mL | "
        "输入/缓存/输出tokens | 精确重放 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for model in agents:
        r, u = model.get("resources", {}), model.get("provider_usage", {})
        stocks = model.get("stocks_used", {})
        tokens = "/".join(
            str(u.get(k)) if u.get(k) is not None else "缺失"
            for k in ("input_token_count", "cached_input_token_count", "output_token_count")
        )
        lines.append(
            f"| {LABELS[model['task']]} | {stocks.get('reagent_mol', 0):.4g}/"
            f"{stocks.get('seed_g', 0):.4g} | {r.get('process_time_s', 0) / 3600:.2f} | "
            f"{model.get('nonfinal_instruments', '—')} | "
            f"{r.get('sample_consumed_L', 0) * 1000:.3f} | {tokens} | "
            f"{'通过' if model.get('replay', {}).get('verified', False) else '未通过'} |"
        )
    lines += [
        "",
        "2/3会话token回传完整；蒸馏行只核算13步已记录前缀，模型用量缺失。"
        "后端模型响应次数未完整观测，三个会话不等于三次后端响应。"
        "订阅费用不能逐会话归因；缺失费用不记作零。",
        "",
    ]
    lines += [
        "## 论文主线如何收束",
        "",
        "本轮建立可执行、有代价且有质量门槛的过程任务。它仍不是系统性Agent失效的证据："
        "单世界、单次轨迹不能支撑跨世界因果归因。",
        "这里评估的是一个物理批次内的自主过程决策，尚未执行跨批发现、知识交付或接收者部署；"
        "即使出现质量失败，也不能直接称为科学发现中的摘要、记忆或知识损失。",
        "联合可达见证从初始状态出发，不保证Agent已经到达的每个决策前缀仍可挽救；"
        "后续分支诊断须先核对同一前缀和剩余预算内是否确有有效替代动作。",
        "",
        "下一阶段围绕同前缀、同证据、同预算的干预定位：先检验是否购买了必要的相/粒径信息，"
        "再比较完整过程记录与知识交付是否保留了决定下一步动作的状态，最后检验收到完整信息后是否仍选择失当。"
        "保存馏分与追加混合、单次冷却与复热后的再冷却是可操作的对照，"
        "先验证不同历史确实需要不同有效动作，再扩多机制组和留出组合。",
        "",
        "| 待定位环节 | 下一块需要的干预 | 可支持的解释 |",
        "| --- | --- | --- |",
        "| 取证 | 同预算比较自主与参考测量，保留所有购买和未购买的观测 | "
        "关键测量改变可恢复的行动信息；不把不可辨识性归责模型 |",
        "| 交付 | 同一份公开过程记录分别以Raw和自然知识包交给同一接收者 | "
        "来源已有的行动信息是否在交付中丢失 |",
        "| 使用 | 相同物理前缀、相同公开信息和剩余预算，比较闭环行动；"
        "对知识包只补回来源中确实存在的遗漏字段 | 补回信息能否修复行动；"
        "完整信息仍失败则单列使用问题 |",
        "",
        "正式核心仍应是多机制组的完整流程组合留出，配强配方复用和同信息闭环控制基线。"
        "上述单前缀干预服务于主结果解释，不另堆一组脱离实际流程的简单读表实验。"
        "所有模式都允许未出现，不能按Agent失败筛世界或持续加试直到出现显著结果。",
        "",
        "旧固定流程和旧负结果留作开发与边界证据；不把观测映射修复、模拟器压缩错误、"
        "单纯物料流失包装成科学Agent的信息损失发现。正式实验与稿件重写仍需独立稳定设计。",
        "",
        f"全部块共{n['recorded_operations']}条持久动作、{n['verified_trajectories']}条轨迹/已记录前缀的精确重放。"
        "逐候选参数、全部失败、分母与资源见四个独立JSON/报告及本报告JSON。",
        "",
    ]
    lines += ["## 证据入口", ""]
    for key, label in zip(
        keys,
        ("初始相分辨资格", "完整粒子群与独立切段", "热连续性资格（历史）", "晶种来源守恒复验"),
        strict=True,
    ):
        path = ROOT / current["work_ii"][key]["report"]
        lines.append(f"- [{label}]({path.with_suffix('.md').name})")
    lines.append("")
    OUTPUT.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    plot(result, OUTPUT)
    current["work_ii"]["w2_105_full_process_iteration"] = {
        "report": OUTPUT.relative_to(ROOT).as_posix(),
        "report_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "evidence_mode": "development",
        "counts": n,
    }
    write(ROOT / "configs/current.json", current)
    print(n)


if __name__ == "__main__":
    main()
