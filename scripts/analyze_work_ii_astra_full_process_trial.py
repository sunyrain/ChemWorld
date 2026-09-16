"""Recompute the one-round report from retained trajectories without new execution."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from scripts.run_work_ii_astra_full_process_trial import QUALITY, ROOT, TASKS, scalar

from chemworld.data.logging import load_jsonl

REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-astra-full-process-20260914.json"
LABELS = dict(zip(TASKS, ("反应—萃取—纯化", "反应—路径依赖结晶", "反应—分段蒸馏"), strict=True))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def close(a, b):
    return (
        isinstance(a, (int, float))
        and isinstance(b, (int, float))
        and math.isclose(a, b, abs_tol=1e-8)
    )


def analyze_cell(folder):
    retained = read(folder / "result.json")
    task, kind = retained["task"], retained["kind"]
    rows = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    receipts = read(folder / "receipts.json")
    committed = [r for r in rows if r.get("transaction_status") == "committed"]
    finals = [r for r in committed if r.get("instrument") == "final_assay"]
    final = finals[-1] if finals else {}
    metrics = {
        k: scalar(v)
        for k, v in final.get("observation", {}).items()
        if scalar(v) is not None and final.get("observed_mask", {}).get(k, True)
    }
    checks = {
        k: metrics.get(k) is not None and (metrics[k] >= v if op == ">=" else metrics[k] <= v)
        for k, (op, v) in QUALITY[task].items()
    }
    state = (
        rows[-1]
        .get("agent_view", {})
        .get("tool_json", {})
        .get("campaign_state", {})
        .get("campaign_resources", {})
        .get("state", {})
        if rows
        else {}
    )
    totals = state.get("report_only", {})
    sums = {
        "process_time_s": sum(
            float(r.get("state_delta_summary", {}).get("delta_time_s", 0)) for r in committed
        ),
        "physical_cost": sum(
            float(r.get("state_delta_summary", {}).get("delta_cost", 0)) for r in committed
        ),
        "sample_consumed_L": sum(float(r.get("sample_consumed") or 0) for r in committed),
    }
    source_card = rows[0].get("campaign_resource_card", {}).get("hard_limits", {}) if rows else {}
    stocks = Counter()
    stock_fields = {
        "add_reagent": ("reagent_mol", "amount_mol"),
        "add_solvent": ("solvent_L", "volume_L"),
        "add_catalyst": ("catalyst_mol", "catalyst_amount_mol"),
        "seed_crystals": ("seed_g", "seed_mass_g"),
        "add_extractant": ("extractant_L", "volume_L"),
        "add_phase": ("phase_liquid_L", "volume_L"),
        "wash": ("wash_solvent_L", "wash_volume_L"),
    }
    for row in committed:
        action = row["action"]
        if action["operation"] in stock_fields:
            key, field = stock_fields[action["operation"]]
            stocks[key] += float(action.get(field, 0))
    validation = {
        "final_count_matches_runner": len(finals) == retained["summary"]["final_assays"],
        "quality_matches_runner": (bool(finals) and all(checks.values()))
        == retained["summary"]["quality_passed"],
        "attempts_match_ledger": state.get("operation_attempts") == len(rows),
        "final_count_matches_ledger": state.get("final_assays") == len(finals),
        "nonfinal_instruments_match": state.get("nonfinal_instrument_uses")
        == sum(
            r.get("operation_type") == "measure" and r.get("instrument") != "final_assay"
            for r in committed
        ),
        "stock_deltas_match": all(
            close(v, state.get("stocks_used", {}).get(k)) for k, v in stocks.items()
        ),
        "stock_limits_respected": all(
            v <= source_card.get("stocks", {}).get(k, float("inf")) + 1e-8
            for k, v in stocks.items()
        ),
        **{k + "_reconciled": close(v, totals.get(k)) for k, v in sums.items()},
    }
    if not rows:
        validation = {"no_physical_rows": True}
    measurements = [
        {
            "step": i + 1,
            "instrument": r.get("instrument"),
            "metrics": {
                k: scalar(v)
                for k, v in r.get("observation", {}).items()
                if r.get("observed_mask", {}).get(k) and scalar(v) is not None
            },
        }
        for i, r in enumerate(rows)
        if r.get("operation_type") == "measure" and r.get("transaction_status") == "committed"
    ]
    failure = retained.get("failure")
    unlogged = []
    if kind == "reference" and task == TASKS[0] and "operation=dry" in str(failure):
        unlogged = [
            {
                "operation": "dry",
                "status": "resource_accounting_exception_after_runtime",
                "known_elapsed_s": 300,
                "durable_trajectory_row": False,
                "accounting": "15-step prefix totals only; "
                "failing operation not a committed record",
            }
        ]
    raw_usage = retained.get("provider_usage", {})
    usage = (
        {
            k: raw_usage.get(k)
            for k in (
                "provider_session_count",
                "provider_process_attempt_count",
                "logical_codex_turn_count",
                "accepted_turn_continuation_count",
                "provider_error_event_count",
                "provider_usage_observed",
                "provider_token_accounting_complete",
                "usage_source",
                "backend_model_response_count",
                "backend_model_response_accounting_complete",
            )
        }
        if kind == "agent"
        else {}
    )
    if kind == "agent":
        usage.update(
            {
                k: raw_usage.get(k) if raw_usage.get("token_counts_observed") else None
                for k in (
                    "input_token_count",
                    "cached_input_token_count",
                    "uncached_input_token_count",
                    "output_token_count",
                )
            }
        )
        usage["monetary_cost_usd"] = None
        usage["cost_note"] = "Subscription usage not attributable per run; unavailable is not zero."
        usage["mcp_tool_calls"] = sum(len(r.get("mcp_tool_calls", [])) for r in receipts)
        usage["mcp_step_calls"] = sum(
            t.get("tool") == "step" for r in receipts for t in r.get("mcp_tool_calls", [])
        )
    return {
        "task": task,
        "kind": kind,
        "status": retained["status"],
        "failure": failure,
        "operations": len(rows),
        "committed": len(committed),
        "final_assays": len(finals),
        "quality_targets": QUALITY[task],
        "quality_checks": checks,
        "quality_passed": bool(finals) and all(checks.values()),
        "final_metrics": metrics,
        "leaderboard_score": final.get("leaderboard_score"),
        "replay": read(folder / "replay.json"),
        "resources": totals,
        "stocks_used": dict(stocks),
        "nonfinal_instruments": state.get("nonfinal_instrument_uses"),
        "remaining_resources": state.get("remaining"),
        "validation": validation,
        "failures": retained["summary"]["failures"],
        "unlogged_failed_attempts": unlogged,
        "operation_counts": dict(Counter(r.get("operation_type") for r in committed)),
        "actions": retained["summary"]["actions"],
        "measurements": measurements,
        "provider_usage": usage,
        "elapsed_s": retained["elapsed_s"],
        "provider_terminal": [
            {
                k: r.get(k)
                for k in (
                    "final_payload_status",
                    "final_payload_summary",
                    "final_payload_valid",
                    "provider_error_event_count",
                    "provider_errors",
                    "return_code",
                )
            }
            for r in receipts
        ],
        "source_directory": folder.relative_to(ROOT).as_posix(),
    }


def percentage(value):
    return "—" if value is None else f"{value * 100:.2f}%"


def markdown(report):
    counts = report["counts"]
    lines = [
        "# Astra完整流程单轮开发结果",
        "",
        "2026-09-14；GPT-6 Astra / medium；开发证据，非正式实验。",
        "",
        "本轮每任务一个自主单批，Agent选择全部操作、材料和测量。尚未进行多批发现、机制组合迁移或信息损失因果实验。",
        "",
        f"预定Agent条件3个，实际启动{counts['agent_attempted']}个、合法终检{counts['agent_final_assays']}个、质量达标{counts['agent_quality_passed']}个；无Agent补跑。",
        f"参考尝试4个，包含1次干燥时间记账失败及其独立修正验证；{counts['reference_final_assays']}个完成终检。",
        "",
        "质量目标：纯化/蒸馏纯度≥80%、回收≥10%；结晶纯度≥80%、排除晶种回收≥10%、细粉≤50%。",
        "参考均未满足全部目标，因而未建立质量联合可达性的参考见证；阴性结果不能直接判为Agent能力缺陷。",
        "",
        "## 终检结果",
        "",
        "| 流程 | 条件 | 动作提交/记录 | 纯度 | 回收 | 细粉 | 原生分数 | 质量达标 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in report["cells"]:
        m = c["final_metrics"]
        purity_key, recovery_key = list(QUALITY[c["task"]])[:2]
        score = "—" if c["leaderboard_score"] is None else f"{c['leaderboard_score']:.4f}"
        label = {"reference": "原参考", "reference-corrected": "修正参考", "agent": "Astra自主"}[
            c["kind"]
        ]
        quality_label = ("是" if c["quality_passed"] else "否") if c["final_assays"] else "未评估"
        lines.append(
            f"| {LABELS[c['task']]} | {label} | "
            f"{c['operations'] + len(c['unlogged_failed_attempts'])}/{c['operations']} | "
            f"{percentage(m.get(purity_key))} | {percentage(m.get(recovery_key))} | "
            f"{percentage(m.get('crystal_fines_fraction'))} | {score} | {quality_label} |"
        )
    lines += [
        "",
        "回收使用各原生任务的分母；结晶是排除晶种的下游回收率，不等于原料到产品的总收率。原生分数为次指标。",
        "",
        "## 本轮观察与下一步假说",
        "",
        "纯化Agent进行了三段加热及六次HPLC；后段反应的转化读数继续上升，产率与选择性读数下降。"
        "后处理先加有机相、洗涤，后来才加萃取剂并混合，整条轨迹没有显式settle/separate_phase。"
        "这提示需要检验实验阶段组织和选相前信息使用，但没有同前缀对照，尚不能归因具体损失来源。",
        "",
        "蒸馏Agent完成三段加热、两段蒸馏与一次全部收集。高回收伴随低纯度；原生加权分数也未保证质量达标。"
        "应在后续独立块比较同一前缀的继续蒸馏、停止及收集策略，并核对采样对象；"
        "不能把不同阶段的GC读数变化直接归因于某个控制参数。",
        "",
        "结晶仅完成第一次加料便出现provider错误，原始回执只保留未分类错误摘要，具体服务原因未确证。"
        "本轮不补跑，不将此条件计作科学失败；完整自主结晶表现仍未知。",
        "",
        "下一块优先证明质量目标在公开操作和预算内可达，再做有信息对照的过程决策实验。"
        "本轮在3个预定Agent条件终态后停止，没有继续扩大样本或搜索失败案例。",
        "",
        "## 自主执行轨迹",
        "",
    ]
    for c in report["cells"]:
        if c["kind"] != "agent":
            continue
        lines += [
            f"### {LABELS[c['task']]}",
            "",
            f"状态：{c['status']}；已记录{c['operations']}次动作，{c['committed']}次提交成功。",
            "",
            "| 步 | 操作及参数 | 事务状态 |",
            "| --- | --- | --- |",
        ]
        for a in c["actions"]:
            lines.append(
                f"| {a['step']} | "
                f"`{json.dumps(a['action'], ensure_ascii=False, separators=(',', ':'))}` "
                f"| {a['status']} |"
            )
        lines += ["", "模型终答（保留其自述，解释须结合实际轨迹）：", ""]
        lines += [
            str(p.get("final_payload_summary") or "未取得有效终答") for p in c["provider_terminal"]
        ]
        if c["failure"]:
            lines += ["", f"失败：`{json.dumps(c['failure'], ensure_ascii=False)}`"]
        lines.append("")
    lines += [
        "## 资源与完整性",
        "",
        "| 流程/条件 | 过程秒 | 物理费用 | 采样升 | 非终检测量 | "
        "模型输入/缓存/输出tokens | 精确重放 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in report["cells"]:
        r, u = c["resources"], c["provider_usage"]
        tokens = "/".join(
            str(u.get(k, 0)) if u.get(k, 0) is not None else "未回传"
            for k in ("input_token_count", "cached_input_token_count", "output_token_count")
        )
        lines.append(
            f"| {LABELS[c['task']]}/{c['kind']} | {r.get('process_time_s', 0):.2f} | "
            f"{r.get('physical_cost', 0):.4f} | {r.get('sample_consumed_L', 0):.6f} | "
            f"{c['nonfinal_instruments']} | {tokens} | "
            f"{c['replay'].get('checked_steps', 0)}步/{c['replay'].get('verified')} |"
        )
    lines += [
        "",
        "原纯化失败只对15条持久化前缀做重放与记账；后续dry已触发运行但发生资源预留异常，不能声称全失败轨迹已精确重放。",
        "",
        "| 问题 | 类别/影响 | 处理与验证 |",
        "| --- | --- | --- |",
        "| dry固定耗时300秒未进入资源卡 | K1，执行记账缺陷；仅纯化受影响 | "
        "原失败保留，补上时间预留后从头验证同一参考一次；保留资源强制扣账，B/C不重跑 |",
        "",
        "逐动作时间、费用、采样与物料求和已与资源账交叉核对；具体检查及全部失败见JSON。",
        "结晶provider中断未回传token用量，记为缺失，不按零成本处理。后端模型响应次数未完整观测，"
        "会话/进程与MCP工具次数分别报告；订阅用量无法归属到每次运行的美元金额。",
        "",
        "## 解释边界",
        "",
        "测量后调整、重复控制和不可逆操作可用于提出后续假说；仅凭这一轮不能归因科学信息损失或系统性失效。",
        "新程序未改变模拟器物理定律；这是自由操作的单批试跑，完整实验矩阵仍待开发。",
        "",
        "[实验说明](../WORK_II_ASTRA_FULL_PROCESS_TRIAL_NOTE.md) · "
        "[机器结果](work-ii-astra-full-process-20260914.json)",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    cells = [
        analyze_cell(p)
        for kind in ("reference", "reference-corrected", "agent")
        for task in TASKS
        if (p := root / kind / task).joinpath("result.json").exists()
    ]
    agents = [c for c in cells if c["kind"] == "agent"]
    refs = [c for c in cells if c["kind"] != "agent"]
    report = {
        "schema_version": "work-ii-astra-full-process-report-1",
        "formal_result": False,
        "model": "gpt-6-astra",
        "reasoning_effort": "medium",
        "agent_retries": 0,
        "counts": {
            "agent_scheduled": 3,
            "agent_attempted": len(agents),
            "reference_scheduled": 4,
            "reference_attempted": len(refs),
            "agent_final_assays": sum(c["final_assays"] for c in agents),
            "agent_quality_passed": sum(c["quality_passed"] for c in agents),
            "reference_final_assays": sum(c["final_assays"] for c in refs),
            "recorded_operations": sum(c["operations"] for c in cells),
            "unlogged_failed_operations": sum(len(c["unlogged_failed_attempts"]) for c in cells),
            "replay_verified_trajectories_or_prefixes": sum(
                c["replay"].get("verified") is True for c in cells
            ),
        },
        "all_resource_checks_passed": all(all(c["validation"].values()) for c in cells),
        "known_usage_totals": {
            k: sum(c["provider_usage"].get(k) or 0 for c in agents)
            for k in (
                "input_token_count",
                "cached_input_token_count",
                "uncached_input_token_count",
                "output_token_count",
                "mcp_tool_calls",
                "mcp_step_calls",
                "provider_process_attempt_count",
                "provider_session_count",
            )
        },
        "token_usage_missing_conditions": [
            c["task"]
            for c in agents
            if not c["provider_usage"].get("provider_token_accounting_complete")
        ],
        "total_token_usage_complete": all(
            c["provider_usage"].get("provider_token_accounting_complete") is True for c in agents
        ),
        "systematic_failure_established": False,
        "cells": cells,
        "not_started": [read(p) for p in (root / "not_started").glob("*.json")],
    }
    write(REPORT, report)
    REPORT.with_suffix(".md").write_text(markdown(report), encoding="utf-8")
    current_path = ROOT / "configs/current.json"
    current = read(current_path)
    current["work_ii"]["w2_103_astra_full_process_trial"] = {
        "report": REPORT.relative_to(ROOT).as_posix(),
        "report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        "experiment_note": "workstreams/flagship_tasks/WORK_II_ASTRA_FULL_PROCESS_TRIAL_NOTE.md",
        "run_root": root.relative_to(ROOT).as_posix(),
        "status": "development_single_round_closed",
        "formal_result": False,
        "model": "gpt-6-astra",
        "reasoning_effort": "medium",
        **report["counts"],
    }
    write(current_path, current)
    print(
        json.dumps(
            {
                "counts": report["counts"],
                "resource_checks": report["all_resource_checks_passed"],
                "report": str(REPORT),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
