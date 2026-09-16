"""Close the interrupted Astra pilot from retained records, without new model calls."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scripts.run_work_ii_astra_single_trial import (
    METRICS,
    ROOT,
    TRAIN,
    WORLDS,
    fit_reference,
    interventions,
    predict_reference,
    read,
    write,
)

from chemworld.eval.verify import verify_records


def trajectory_rows(path: Path):
    return (
        [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if path.exists()
        else []
    )


def public_row(folder: Path, root: Path, *, replay_missing: bool):
    attempt = read(folder / "attempt.json")
    original = (
        read(folder / "result.json")
        if (folder / "result.json").exists()
        else {
            "name": folder.relative_to(root / "physical").as_posix(),
            "world": attempt["world"],
            "plan": attempt["plan"],
            "status": "interrupted",
            "exact_replay": False,
            "failure": "stopped_after_public_contract_defect_confirmed",
        }
    )
    records = trajectory_rows(folder / "trajectory.jsonl")
    final = next(
        (
            r
            for r in reversed(records)
            if r.get("instrument") == "final_assay" and r.get("transaction_status") == "committed"
        ),
        None,
    )
    row = {k: original.get(k) for k in ("name", "world", "plan", "status", "failure")}
    row["recorded_operations"] = len(records)
    row["failed_operations"] = [
        {
            "operation": r.get("operation_type"),
            "status": r.get("transaction_status"),
            "failed_preconditions": [
                k for k, v in r.get("preconditions", {}).items() if v is False
            ],
        }
        for r in records
        if r.get("transaction_status") != "committed"
    ]
    row["resources"] = {
        "process_time_s": sum(
            r.get("state_delta_summary", {}).get("delta_time_s", 0) for r in records
        ),
        "cost_units": sum(r.get("state_delta_summary", {}).get("delta_cost", 0) for r in records),
        "sample_consumed_L": sum(r.get("sample_consumed", 0) for r in records),
        "measurement_cost_units": sum(r.get("measurement_cost", 0) for r in records),
        "operation_count": len(records),
    }
    row["terminal"] = (
        {
            k: final["observation"].get(k)
            for k in (
                "yield",
                "conversion",
                "selectivity",
                "crystal_yield",
                "crystal_purity",
                "crystal_size",
                "crystal_csd_quality",
                "crystal_fines_fraction",
                "cost",
                "score",
            )
        }
        if final
        else None
    )
    row["exact_replay"] = original.get("exact_replay", False)
    replay_path = root / "closeout_replay" / (row["name"].replace("/", "__") + ".json")
    if not row["exact_replay"] and replay_path.exists():
        row["exact_replay"] = read(replay_path).get("verified") is True
    elif not row["exact_replay"] and replay_missing and records:
        print(
            json.dumps(
                {"stage": "retained_failure_replay", "unit": row["name"], "records": len(records)}
            ),
            flush=True,
        )
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions(row["world"])
        ).to_dict()
        write(replay_path, replay)
        row["exact_replay"] = replay.get("verified") is True
    row["final_assay_committed"] = final is not None
    row["usable_for_deployment_comparison"] = False if row["name"].startswith("deploy/") else None
    return row


def prediction_diagnostics(root: Path):
    truth = read(root / "blind_truth.json")
    valid = {q: r for q, r in truth.items() if r["status"] == "completed"}
    reports = []
    for name in ("standard_raw", "standard_whole"):
        p = root / "model" / f"read_{name}" / "result.json"
        if not p.exists():
            continue
        call = read(p)
        errors = []
        for q, row in valid.items():
            public = row["public"]
            target = {
                "reaction_yield": public["upstream_hplc"]["yield"],
                **{k: public["terminal"][k] for k in METRICS[1:]},
            }
            predicted = call["payload"]["predictions"][q]
            errors.append(
                {
                    "query": q,
                    "world": row["world"],
                    "truth": target,
                    "prediction": predicted,
                    "absolute_error": {k: abs(predicted[k] - target[k]) for k in METRICS},
                }
            )
        splits = {}
        for split, worlds in (("learning", TRAIN), ("heldout", WORLDS[2:])):
            subset = [e for e in errors if e["world"] in worlds]
            splits[split] = {
                "valid_queries": len(subset),
                "planned_queries": 4,
                "mae": {
                    k: float(np.mean([e["absolute_error"][k] for e in subset])) for k in METRICS
                },
            }
        reports.append(
            {
                "condition": name,
                "status": "conditional_diagnostic_only",
                "valid_queries": len(valid),
                "planned_queries": len(truth),
                "splits": splits,
                "query_rows": errors,
            }
        )
    difference = {}
    if len(reports) == 2:
        difference = {
            k: reports[1]["splits"]["heldout"]["mae"][k] - reports[0]["splits"]["heldout"]["mae"][k]
            for k in METRICS
        }
    return {
        "rows": reports,
        "heldout_whole_minus_raw_mae": difference,
        "interpretation": "Two valid heldout queries only; not a test of systematic information "
        "loss. Four planned queries violated cooling bounds and are retained as failures.",
    }


def build_report(root: Path, *, replay_missing=False):
    attempts = sorted((root / "physical").rglob("attempt.json"))
    rows = []
    for i, attempt in enumerate(attempts):
        rows.append(public_row(attempt.parent, root, replay_missing=replay_missing))
        if i % 8 == 0:
            print(
                json.dumps({"stage": "closeout", "completed": i + 1, "total": len(attempts)}),
                flush=True,
            )
    calls = [read(p) for p in sorted((root / "model").glob("*/result.json"))]
    usage = Counter()
    for call in calls:
        usage.update(call.get("receipt", {}).get("usage", {}))
    counts = Counter(r["status"] for r in rows)
    by_stage = defaultdict(Counter)
    resources = defaultdict(Counter)
    for row in rows:
        stage = row["name"].split("/")[0]
        by_stage[stage][row["status"]] += 1
        resources[stage].update(row["resources"])
    source_summaries = {}
    coverage = []
    reference_predictions = []
    truth = read(root / "blind_truth.json")
    for source in ("standard", "diagnostic", "space_filling"):
        data = [read(p) for p in sorted((root / "physical/source" / source).rglob("result.json"))]
        completed = [r["public"] for r in data if r["status"] == "completed"]
        source_summaries[source] = {
            "planned_batches": 12,
            "completed_batches": len(completed),
            "per_world": {
                w: {
                    "batches": sum(p["world"] == w for p in completed),
                    "best_score": max(p["terminal"]["score"] for p in completed if p["world"] == w),
                    "maximum_recovery": max(
                        p["terminal"]["crystal_yield"] for p in completed if p["world"] == w
                    ),
                }
                for w in TRAIN
            },
        }
        reference = fit_reference(data)
        for kind in ("component", "whole"):
            errors = []
            for q, actual in truth.items():
                if actual["status"] != "completed":
                    continue
                predicted = predict_reference(reference, actual["world"], actual["plan"], kind)
                if predicted is not None:
                    target = {
                        "reaction_yield": actual["public"]["upstream_hplc"]["yield"],
                        **{k: actual["public"]["terminal"][k] for k in METRICS[1:]},
                    }
                    errors.append(
                        {
                            "query": q,
                            "world": actual["world"],
                            "error": {k: abs(predicted[k] - target[k]) for k in METRICS},
                        }
                    )
            reference_predictions.append(
                {
                    "source": source,
                    "kind": kind,
                    "errors": errors,
                    "qualified_strong_reference": False,
                }
            )
        for world in WORLDS[2:]:
            feed = [
                p["upstream_hplc"]["yield"]
                for p in completed
                if p["world"].endswith(world[2:]) and p["upstream_hplc"]
            ]
            targets = [
                r["public"]["upstream_hplc"]["yield"]
                for r in truth.values()
                if r["world"] == world and r["status"] == "completed"
            ]
            coverage.append(
                {
                    "source": source,
                    "heldout_pair": world,
                    "learning_downstream_feed_yield_range": [min(feed), max(feed)],
                    "valid_test_feed_yields": targets,
                    "outside_observed_range": [not min(feed) <= t <= max(feed) for t in targets],
                    "interpretation": "marginal coverage diagnostic, not full state support",
                }
            )
    score_examples = [
        {"unit": r["name"], "world": r["world"], "plan": r["plan"], "terminal": r["terminal"]}
        for r in rows
        if r["status"] == "completed"
        and r["name"].startswith("source/")
        and r["terminal"]["crystal_yield"] <= 0.001
        and r["terminal"]["score"] >= 0.4
    ]
    payload = {
        "schema_version": "work-ii-astra-single-trial-closeout-1",
        "status": "development_stopped_public_contract_defects",
        "formal_result": False,
        "model": "gpt-6-astra",
        "reasoning_effort": "medium",
        "independent_groups": 1,
        "model_calls": {
            "planned": 20,
            "attempted": len(calls),
            "completed": sum(c["status"] == "completed" for c in calls),
            "failed": sum(c["status"] != "completed" for c in calls),
            "not_started": 20 - len(calls),
            "retries": 0,
        },
        "physical_runs": {
            "planned": 132,
            "attempted": len(rows),
            **dict(counts),
            "not_started": 132 - len(rows),
            "exact_replay_verified": sum(r["exact_replay"] for r in rows),
        },
        "stages": dict(by_stage),
        "resource_totals_by_stage": dict(resources),
        "reported_model_usage": dict(usage),
        "model_wall_seconds": sum(c.get("receipt", {}).get("elapsed_s", 0) for c in calls),
        "subscription_usd_cost": None,
        "model_call_rows": [
            {
                "name": c["name"],
                "status": c["status"],
                "usage": c.get("receipt", {}).get("usage", {}),
                "wall_seconds": c.get("receipt", {}).get("elapsed_s", 0),
            }
            for c in calls
        ],
        "sources": source_summaries,
        "prediction_diagnostics": prediction_diagnostics(root),
        "public_reference_diagnostics": reference_predictions,
        "score_without_growth_examples": score_examples,
        "observed_support_diagnostics": coverage,
        "deployment_comparison_valid": False,
        "targeted_E3_executed": False,
        "defects": [
            "Initial compiler omitted required slurry assay; original 8 failures kept.",
            "Public trial contract incorrectly allowed omission of mandatory pre-seeding assay.",
            "Independent scalar bounds omitted state-dependent cooling-temperature ceiling; "
            "4/8 blind query plans invalid.",
            "Existing task score rewards morphology/purity despite zero seed-excluded recovery; "
            "score is not a sufficient measure of useful recovered product.",
        ],
        "limits": [
            "One constructed group, no repeat or population inference.",
            "Valid prediction comparisons use 4/8 queries, only 2/4 heldout queries.",
            "Warm/cold operating coverage and downstream feed support not qualified.",
            "Raw and whole summary both retained substantial mechanism-related evidence.",
            "Original attempt results remain unchanged, including the interrupted trace.",
            "Closeout only replays retained traces and recalculates summaries; no new model calls.",
        ],
        "physical_rows": rows,
    }
    write(
        root / "closed.json",
        {
            "status": payload["status"],
            "resume_planned": False,
            "reason": "The once-per-condition trial ended after contract defects.",
        },
    )
    write(root / "closeout.json", payload)
    path = ROOT / "workstreams/flagship_tasks/reports/work-ii-astra-single-trial-20260914.json"
    write(path, payload)
    content = [
        "# GPT-6 Astra medium 单次开发试跑",
        "",
        "结论：取证和知识表达可运行，尚不能据此评价系统性信息损失。部署合同存在错误，已停止受影响条件。",
        "",
        f"模型：{len(calls)}/20 次调用完成，无重试；其余 {20 - len(calls)} 次未启动。",
        f"物理：计划132、尝试{len(rows)}、完成{counts['completed']}、失败{counts['failed']}、"
        f"中断{counts['interrupted']}、未启动{132 - len(rows)}；"
        f"保留轨迹重放通过{sum(r['exact_replay'] for r in rows)}/{len(rows)}。",
        "",
        "## 实际完成范围",
        "",
        "- E1来源：标准、结构化来源各12批，空间填充12批；共36/36批完成。",
        "- 知识表达：两种来源各生成整流程和组件知识包，共4/4份有效。",
        "- 盲测：4/8条合法完成；另一条预定流程在四世界均违反冷却动态上界。",
        "- 读出：标准Raw、标准整流程摘要各一次；部署比较无效，后续组件与定向E3未执行。",
        "",
        "## 有效测试点的描述性结果",
        "",
        "下表每条件只有2个有效留出点，不能用作总体效果或信息损失检验。",
        "",
        "| 交付 | 留出反应产率MAE | 留出晶体回收率MAE | 留出纯度MAE |",
        "| --- | --- | --- | --- |",
    ]
    for r in payload["prediction_diagnostics"]["rows"]:
        e = r["splits"]["heldout"]["mae"]
        content.append(
            f"| {r['condition']} | {e['reaction_yield']:.5f} | "
            f"{e['crystal_yield']:.5f} | {e['crystal_purity']:.5f} |"
        )
    content += [
        "",
        "完整记录和摘要都保留了有用关系；当前数值不支持概括为摘要导致系统性信息损失。",
        "",
        "## 必须先修的实验问题",
        "",
        "1. 当前固定播种流程要求反应后、过滤前两次HPLC；试跑错误地允许省略前者。",
        "   模型依照公开合同省略后被平台拒绝，属于实验接入错误，不能归因于Agent。",
        "2. 冷却范围必须随实际状态变化；不能将四个标量区间的笛卡尔积都称为合法流程。",
        "3. 当前score可能偏好几乎只保留晶种的高纯度/好粒径结果，应重新制定有意义的终端效用。",
        "4. 新组合下游进料可能超出学习记录覆盖；先解决支持域与可辨识性，再解释组合失败。",
        "",
        "### 评分问题的保留实例",
        "",
        "| 批次 | 组件 | 晶体回收率 | score |",
        "| --- | --- | --- | --- |",
    ]
    for r in score_examples:
        content.append(
            f"| {r['unit']} | {r['world']} | {r['terminal']['crystal_yield']:.5f} | "
            f"{r['terminal']['score']:.5f} |"
        )
    content += [
        "",
        "## 资源与记录",
        "",
        f"模型报告用量：`{json.dumps(dict(usage))}`。订阅调用不估算虚构美元费用。",
        "物理成本、样品、时间、逐调用token及全部失败/中断在同名JSON中。",
        "原始provider输出、谱图、轨迹和私有世界初始化保存在ignored运行目录；未覆盖任何原结果。",
        "早停后仅从保留轨迹核对重放与汇总，没有新增科学调用或补齐好结果。",
        "",
    ]
    path.with_suffix(".md").write_text("\n".join(content), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "models": payload["model_calls"],
                "physical": payload["physical_runs"],
                "predictions": payload["prediction_diagnostics"],
                "usage": dict(usage),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-missing", action="store_true")
    args = parser.parse_args()
    build_report(args.output.resolve(), replay_missing=args.replay_missing)
