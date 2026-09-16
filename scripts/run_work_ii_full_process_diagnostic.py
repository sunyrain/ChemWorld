"""Fixed 15-cell development diagnostic; no model calls or adaptive search."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import hashlib
import json
import threading
import time
from collections import Counter
from copy import deepcopy
from pathlib import Path

from scripts.analyze_work_ii_astra_full_process_trial import analyze_cell
from scripts.run_work_ii_astra_full_process_trial import (
    LIMITS,
    NAMESPACE,
    QUALITY,
    ROOT,
    TASKS,
    card,
    reference_actions,
    summarize,
)
from scripts.run_work_ii_astra_single_trial import read, write

from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task

NOTE = "workstreams/flagship_tasks/WORK_II_FULL_PROCESS_DIAGNOSTIC_NOTE.md"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-full-process-diagnostic-20260914.json"
CLOSE = [{"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]
GC = {"operation": "measure", "instrument": "gc"}


def source():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_103_astra_full_process_trial"]
    path = ROOT / binding["report"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding["report_sha256"]:
        raise ValueError("source report does not match current binding")
    return binding, ROOT / binding["run_root"]


def plans(old):
    def actions(kind, task):
        return [r["action"] for r in load_jsonl(old / kind / task / "trajectory.jsonl")]

    p = actions("agent", TASKS[0])
    d = actions("agent", TASKS[2])
    result = []

    def add(name, task, steps, prefix):
        result.append({"cell": name, "task": task, "actions": deepcopy(steps), "prefix": prefix})

    def workup(wash):
        return [
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
            {"operation": "add_extractant", "extractant": 3, "volume_L": 0.018},
            {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
            {"operation": "settle", "duration_s": 420.0},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "separate_phase", "target_phase": "organic"},
            *([{"operation": "wash", "wash_volume_L": wash}] if wash else []),
            {"operation": "dry"},
            {"operation": "concentrate", "duration_s": 600.0},
            {"operation": "transfer", "transfer_fraction": 0.97},
            {"operation": "measure", "instrument": "hplc"},
            *CLOSE,
        ]

    for index, wash in enumerate((0.0, 0.008, 0.020), 1):
        add(f"P{index}", TASKS[0], p[:10] + workup(wash), ["agent", 10])
    add("P4", TASKS[0], [*p[:7], {"operation": "quench"}, *workup(0.008)], ["agent", 7])
    add(
        "P5",
        TASKS[0],
        [a for a in reference_actions(TASKS[0]) if a["operation"] != "wash"],
        ["reference-corrected", 14],
    )

    collect = {"operation": "collect_fraction", "transfer_fraction": 1.0}
    add("D1", TASKS[2], [*d[:12], collect, GC, *CLOSE], ["agent", 12])
    for name, fraction in (("D2", 0.0), ("D3", 1.0)):
        add(
            name,
            TASKS[2],
            [
                *d[:12],
                collect,
                d[12],
                {"operation": "collect_fraction", "transfer_fraction": fraction},
                GC,
                *CLOSE,
            ],
            ["agent", 12],
        )
    add(
        "D4",
        TASKS[2],
        [
            *d[:10],
            {
                "operation": "distill",
                "target_temperature_K": 365.0,
                "duration_s": 1200.0,
                "reflux_ratio": 10.0,
            },
            collect,
            GC,
            *CLOSE,
        ],
        ["agent", 10],
    )

    def cool(target, duration):
        return {
            "operation": "cool_crystallize",
            "target_temperature_K": target,
            "duration_s": duration,
        }

    paths = [
        (0.006, [cool(278.15, 1800)]),
        (0.006, [cool(278.15, 14400)]),
        (0.050, [cool(278.15, 14400)]),
        (0.006, [cool(290.0, 14400)]),
        (0.006, [cool(305.0, 7200), cool(278.15, 7200)]),
        (
            0.006,
            [
                cool(278.15, 1800),
                {
                    "operation": "heat",
                    "target_temperature_K": 300.0,
                    "duration_s": 300.0,
                    "stirring_speed_rpm": 600.0,
                },
                cool(278.15, 14400),
            ],
        ),
    ]
    for index, (seed, path) in enumerate(paths, 1):
        add(
            f"C{index}",
            TASKS[1],
            [
                *reference_actions(TASKS[1])[:8],
                {"operation": "seed_crystals", "seed_mass_g": seed},
                *path,
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "filter_crystals"},
                *CLOSE,
            ],
            ["reference", 8],
        )
    return result


def snapshot(base):
    """Evaluator-only diagnostic, never passed to the policy."""
    state = base._state
    return {
        "temperature_K": state.temperature_K,
        "volume_L": state.volume_L,
        "process_metrics": {} if state.process is None else deepcopy(state.process.metrics),
        "species_amounts_mol": deepcopy(state.species_amounts),
        "phases": {}
        if state.phases is None
        else {
            key: {
                "selected": phase.selected,
                "volume_L": phase.volume_L,
                "species_amounts_mol": deepcopy(phase.species_amounts_mol),
            }
            for key, phase in state.phases.phases.items()
        },
        "removed_inventory": deepcopy(state.metadata.get("removed_phase_inventory_history", [])),
    }


def execute(root, plan, old, progress):
    folder = root / plan["cell"]
    folder.mkdir()  # Existing attempts are retained, never silently relaunched.
    write(folder / "plan.json", plan)
    task = plan["task"]
    progress.update(cell=plan["cell"], operations=0)
    holder, diagnostic = [], []
    started = time.monotonic()

    def wrap(env):
        holder.append(env.unwrapped)
        return env

    def on_step(record, trace):
        del trace
        diagnostic.append(
            {"step": len(diagnostic) + 1, "action": record.action, **snapshot(holder[0])}
        )
        progress["operations"] += 1
        if record.info.get("transaction_status") != "committed":
            raise RuntimeError(f"stop at failed transaction: {record.action}")

    failure = None
    try:
        run_agent(
            env_id=get_task(task).env_id,
            agent=_FrozenTruthReplayAgent(plan["actions"]),
            world_split="public-test",
            budget=LIMITS[task],
            budget_override=LIMITS[task],
            objective="balanced",
            seed=0,
            agent_seed=0,
            observation_seed=1,
            task_id=task,
            output_path=folder / "trajectory.jsonl",
            episode_mode_override="single_experiment",
            campaign_resource_card=card(task),
            observation_noise_mode="keyed",
            observation_noise_namespace=NAMESPACE,
            step_callback=on_step,
            env_wrapper=wrap,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    rows = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    summary = summarize(task, rows)
    replay = verify_records(rows, tolerance=0.0).to_dict() if rows else {"verified": False}
    write(folder / "evaluator_states.json", diagnostic)
    write(folder / "replay.json", replay)
    write(folder / "receipts.json", [])
    write(
        folder / "result.json",
        {
            "task": task,
            "kind": "deterministic_diagnostic",
            "failure": failure,
            "status": "completed" if summary["final_assays"] == 1 and failure is None else "failed",
            "summary": summary,
            "elapsed_s": time.monotonic() - started,
        },
    )
    analyzed = analyze_cell(folder)
    kind, count = plan["prefix"]
    prior = load_jsonl(old / kind / task / "trajectory.jsonl")
    prefix_fields = ("action", "observation", "state_delta_summary", "transaction_status")
    analyzed.update(
        cell=plan["cell"],
        prefix_steps=count,
        prefix_source=(old / kind / task).relative_to(ROOT).as_posix(),
        prefix_reproduced=len(rows) >= count
        and all(
            all(rows[i].get(k) == prior[i].get(k) for k in prefix_fields) for i in range(count)
        ),
        service_process_metrics=diagnostic[-1]["process_metrics"] if diagnostic else {},
    )
    # Qualification is computed only after assay-aligned truth extraction.
    analyzed["local_feasibility_witness"] = False
    write(folder / "analysis.json", analyzed)
    progress["completed"] += 1
    print(
        json.dumps(
            {
                "cell": plan["cell"],
                "completed": progress["completed"],
                "total": 15,
                "status": analyzed["status"],
                "quality": analyzed["quality_passed"],
                "failure": failure,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return analyzed


def build_report(root, binding, cells):
    by_id = {c["cell"]: c for c in cells}
    pairs = []
    for left, right in (
        ("P1", "P2"),
        ("P2", "P3"),
        ("P2", "P4"),
        ("D1", "D2"),
        ("D2", "D3"),
        ("D1", "D4"),
        ("C1", "C2"),
        ("C2", "C3"),
        ("C2", "C4"),
        ("C2", "C5"),
        ("C2", "C6"),
    ):
        a, b = by_id[left], by_id[right]
        keys = QUALITY[a["task"]]
        complete = a["status"] == b["status"] == "completed"
        av, bv = a.get("assay_truth_metrics", {}), b.get("assay_truth_metrics", {})
        deltas = {k: bv[k] - av[k] for k in keys if complete and k in av and k in bv}
        pairs.append(
            {
                "left": left,
                "right": right,
                "assay_truth_right_minus_left": deltas,
                "complete_pair": complete,
                "absolute_change_ge_0_05": {k: abs(v) >= 0.05 for k, v in deltas.items()},
            }
        )
    return {
        "status": "development_diagnostic_closed",
        "formal_result": False,
        "note": NOTE,
        "run_root": root.relative_to(ROOT).as_posix(),
        "source_binding": binding,
        "counts": {
            "planned": 15,
            "attempted": len(cells),
            "completed": sum(c["status"] == "completed" for c in cells),
            "final_assays": sum(c["final_assays"] for c in cells),
            "operations": sum(c["operations"] for c in cells),
            "replay_verified": sum(c["replay"].get("verified") is True for c in cells),
            "prefix_reproduced": sum(c["prefix_reproduced"] for c in cells),
            "transaction_failures": sum(len(c["failures"]) for c in cells),
            "execution_exceptions": sum(c["failure"] is not None for c in cells),
            "model_calls": 0,
        },
        "coverage_by_task": dict(Counter(c["task"] for c in cells)),
        "feasibility_witnesses": {
            t: [c["cell"] for c in cells if c["task"] == t and c["local_feasibility_witness"]]
            for t in TASKS
        },
        "all_resources_reconciled": all(all(c["validation"].values()) for c in cells),
        "cells": cells,
        "pairs": pairs,
        "interpretation": "One selected development world, fixed diagnostic paths. No global "
        "infeasibility, model capability or information-loss attribution follows from this block.",
    }


def markdown(report):
    lines = [
        "# 完整流程可达性与接口诊断",
        "",
        "2026-09-14；开发诊断；无新模型调用。",
        "",
        "固定15个完整批次，各一次；所有分支从首动作执行并支付前缀成本。",
        "不改W2-103质量阈值，不替换历史失败。",
        "",
        f"计数：`{json.dumps(report['counts'])}`。",
        "",
        "下表为实际终检读数；JSON另保留终检观察定律的无噪声真值及局部过程摘要，三者分列。",
        "局部过程摘要的组分/分母与终检不同，不能把它当成终检真值。",
        "局部见证要求合法完成、终检观察值与同口径真值均达标、重放和资源核对通过。",
        "",
        "| 条件 | 纯度 | 回收（结晶排除晶种） | 细粉 | 过程秒 | 费用 | 完成终检 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for c in report["cells"]:
        keys = list(QUALITY[c["task"]])
        metrics = c["final_metrics"]
        values = [f"{metrics[k]:.4f}" if k in metrics else "缺失" for k in keys]
        if len(values) == 2:
            values.append("—")
        resources = c["resources"]
        lines.append(
            f"| {c['cell']} | {' | '.join(values)} | "
            f"{resources.get('process_time_s', 0):.1f} | "
            f"{resources.get('physical_cost', 0):.4f} | {c['final_assays'] == 1} |"
        )
    lines += [
        "",
        "可达见证：`" + json.dumps(report["feasibility_witnesses"]) + "`。",
        "未出现见证只表示本块覆盖未证明可达，不表示全域无解。",
        "",
        "失败：",
    ]
    for c in report["cells"]:
        if c["failure"] or c["failures"]:
            lines.append(f"- {c['cell']}: {c['failure']}; {c['failures']}")
    if not any(c["failure"] or c["failures"] for c in report["cells"]):
        lines.append("无执行异常或事务失败；质量不达标仍保留。")
    lines += [
        "",
        "## 解释与实际调整",
        "",
        "1. 纯化P1→P2→P3增加洗涤，终检纯度约19.1%→15.2%→11.7%，回收同步下降。"
        "局部过程摘要却显示纯度提高：它只汇总可分配副产物家族，终检还计入残留的其他杂质；"
        "局部回收相对分离前产物，终检回收使用初始反应物。"
        "本报告初版误把局部摘要当作同口径真值，现由原轨迹重放提取真正终检真值；"
        "没有新条件、改动作或替换结果。这个分析错误不能归因于Agent。",
        "2. 蒸馏首段停止D1与追加并混合D3的终检纯度35.9%→24.4%，回收96.4%→97.1%；"
        "这是两个完整预定流程的描述性比较。预设的D2零收集隔离对照失败，"
        "不能把D1/D3比较冒充已完成的等过程成本隔离实验。缩短首段D4纯度51.1%、回收81.3%，仍未合格。",
        "3. 结晶延长冷却C1→C2，细粉终检100%→91.0%、净回收38.97%→45.94%；"
        "50 mg晶种未进一步改善细粉。当前HPLC只能测晶体纯度，粒径/细粉直到终检才可见，"
        "尚不支持声称已设计粒径反馈闭环。",
        "4. 两个失败属于本轮脚本设计：collect_fraction下限0.0001，零收集不是重选容器；"
        "C5试图从约301.78 K冷却到305 K，超过动态上界。保留失败，不补跑，不计为Agent错误。",
        "5. 已新增完整任务公开操作状态：实际温度/体积、相身份、选中对象、当前测量或旧读数标记；"
        "模型压缩状态包保留这些字段。组分真实含量、私有参数及免费粒径信息未公开。"
        "新增理想传感读数属于下一版合同，旧Agent并未看到；本轮未做新provider验证。",
        "6. 还确认采样按比例扣除全部库存，包括保存的相；不能将当前多容器解释为取样互相隔离。"
        "后续先处理测量对象/扣样范围及付费粒径仪器，再验证全组分终检质量的可达性。"
        "不降低80%纯度或50%细粉要求来制造成功。",
        "",
        "后续新Astra条件仍仅GPT-6 Astra / medium，各一次；先完成上述任务资格，"
        "再做同证据交付和同前缀决策对照。当前数据不能支持系统性信息损失或跨世界结论。",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binding, old = source()
    root = args.output.resolve()
    frozen = plans(old)
    root.mkdir(parents=True, exist_ok=False)
    write(root / "block.json", {"note": NOTE, "source_binding": binding, "plans": frozen})
    progress = {"stage": "deterministic", "completed": 0, "total": len(frozen), "operations": 0}
    started, stop = time.monotonic(), threading.Event()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            count = progress["completed"]
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed, 1),
                        "cells_per_min": count * 60 / elapsed,
                        "eta_s": (15 - count) * elapsed / count if count else None,
                    }
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        for plan in frozen:
            execute(root, plan, old, progress)
        from scripts.analyze_work_ii_full_process_diagnostic import analyze

        analyze(root)
    finally:
        stop.set()
        thread.join()


if __name__ == "__main__":
    main()
