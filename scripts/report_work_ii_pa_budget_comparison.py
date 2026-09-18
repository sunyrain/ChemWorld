"""Compare saved PA budget trials without invoking the model or simulator."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_pa_single_trial import METRICS, token_accounting, token_table

from chemworld.data.logging import load_jsonl


def describe(root):
    result = read(root / "result.json")
    batches = defaultdict(list)
    for row in load_jsonl(root / "source/trajectory.jsonl"):
        if row.get("transaction_status") == "committed":
            batches[int(row.get("experiment_index", 0)) + 1].append(row["action"])
    pairs = set()
    recipes = []
    actions_by_batch = []
    for index, actions in sorted(batches.items()):
        solvent = next(
            (a["solvent"] for a in reversed(actions) if a["operation"] == "add_solvent"), None
        )
        extractant = next(
            (a["extractant"] for a in reversed(actions) if a["operation"] == "add_extractant"), None
        )
        if solvent is not None and extractant is not None:
            pairs.add((solvent, extractant))
        recipes.append(json.dumps(actions, sort_keys=True))
        actions_by_batch.append({"batch": index, "actions": actions})
    evaluation = result.get("prediction_evaluation", {})
    return {
        "run_root": root.as_posix(),
        "planned_batches": result["planned_source_batches"],
        "completed_batches": result.get("source", {}).get("completed_batches", 0),
        "operations": result.get("source", {}).get("operations", 0),
        "source_elapsed_s": result.get("source", {}).get("elapsed_s"),
        "elapsed_s": result.get("elapsed_s"),
        "status": result["status"],
        "unique_pairs": sorted(pairs),
        "identical_full_action_sequences_repeated": len(recipes) - len(set(recipes)),
        "actions_by_batch": actions_by_batch,
        "prediction_evaluation": evaluation,
        "token_accounting": token_accounting(result),
    }


def export(baseline, candidate, output):
    old_design, new_design = [read(p / "design.json") for p in (baseline, candidate)]
    if any(old_design[k] != new_design[k] for k in ("model", "world", "queries", "K1", "Q", "K2")):
        raise ValueError("model, world or sealed posttests differ")
    rows = [describe(p) for p in (baseline, candidate)]
    comparison = {
        "development_only": True,
        "formal_budget_effect_established": False,
        "scope": "one fresh source per budget; legacy identity exposure retained",
        "trials": rows,
    }
    output.mkdir(parents=True, exist_ok=True)
    write(output / "comparison.json", comparison)
    lines = [
        "# PA 12/24次预算比较与token账本",
        "",
        "同世界、同模型、同后测，一次新会话对一次旧会话。"
        "保留旧公开身份与脚本接口，属于描述性开发诊断，不估计平均预算效应。",
        "",
        "| 项目 | 12次预算 | 24次预算 |",
        "| --- | ---: | ---: |",
    ]
    for name, fn in (
        ("完成批数", lambda r: f"{r['completed_batches']}/{r['planned_batches']}"),
        ("操作数", lambda r: r["operations"]),
        ("不同材料搭配", lambda r: f"{len(r['unique_pairs'])}/16"),
        ("完整操作序列重复次数", lambda r: r["identical_full_action_sequences_repeated"]),
        ("来源分钟", lambda r: f"{r['source_elapsed_s'] / 60:.2f}"),
        ("整链分钟", lambda r: f"{r['elapsed_s'] / 60:.2f}"),
        (
            "有机相MAE",
            lambda r: f"{r['prediction_evaluation']['metrics'][METRICS[0]]['mae']:.5f}",
        ),
        (
            "90%区间覆盖",
            lambda r: f"{r['prediction_evaluation']['metrics'][METRICS[0]]['coverage90']:.1%}",
        ),
        (
            "平均区间宽度",
            lambda r: f"{r['prediction_evaluation']['metrics'][METRICS[0]]['mean_width90']:.5f}",
        ),
        (
            "正确决策",
            lambda r: (
                f"{sum(d['correct'] for d in r['prediction_evaluation']['decisions'].values())}/2"
            ),
        ),
    ):
        try:
            values = [str(fn(r)) for r in rows]
        except (KeyError, TypeError):
            values = ["未完成/见机器记录"] * 2
        lines.append(f"| {name} | " + " | ".join(values) + " |")
    lines += [
        "",
        "## 分阶段token",
        "",
        "缓存输入已经包含在输入中；后测取同线程累计值之差，不累加累计快照。"
        "输出包含provider计入的推理token，美元费用不可归属。参考与重放不调用模型。",
    ]
    for row in rows:
        lines += [
            "",
            f"### {row['planned_batches']}次预算",
            "",
            *token_table(row["token_accounting"]),
        ]
    lines += [
        "",
        "## 逐题误差（有机相）",
        "",
        "| 题目 | 12次绝对误差 | 24次绝对误差 |",
        "| --- | ---: | ---: |",
    ]
    lookup = [
        {
            d["query_id"]: d
            for d in r["prediction_evaluation"].get("details", [])
            if d["metric"] == METRICS[0]
        }
        for r in rows
    ]
    for query in old_design["queries"]:
        q = query["query_id"]
        values = [f"{d[q]['absolute_error']:.5f}" if q in d else "缺失" for d in lookup]
        lines.append(f"| {q} | " + " | ".join(values) + " |")
    lines += [
        "",
        "24次来源从头知道完整预算，策略可从首批起不同；"
        "材料覆盖扩大不自动等于辨识质量提高，轨迹及机理问答须结合阅读。"
        "旧参考12批只复用一次，不计入本轮新增24批；各来源精确重放另计。"
        "旧整链耗时含参考生成与参考重放，新整链复用参考；整链时间不作为纯预算耗时效应。",
        "",
        "组批是共同工具规则下允许的自主策略。它不使总体表现比较失效，但此单次对比"
        "不能分离数据量、实验策略、计算投入与模型随机性。输入token或脚本数不测量思考深度。"
        "主设计继续12批和自主调度；不因本轮24批较差追加重跑，也不强制逐批反思。",
        "",
    ]
    (output / "COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    export(args.baseline, args.candidate, args.output)


if __name__ == "__main__":
    main()
