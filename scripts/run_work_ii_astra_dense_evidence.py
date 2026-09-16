"""Seven single-session Astra medium comparisons using a closed development screen."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
import math
import threading
import time
from collections import Counter
from copy import deepcopy
from pathlib import Path

import numpy as np
from scripts import run_work_ii_astra_corrected_pilot as base
from scripts import run_work_ii_early_time_screen as screen

ROOT = base.ROOT
NOTE = "workstreams/flagship_tasks/WORK_II_ASTRA_DENSE_EVIDENCE_NOTE.md"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-astra-dense-evidence-20260914.json"
CONDITIONS = ("raw", "whole", "component", "raw_scaffold", "task_only")
TOTAL = 7


def query_indices():
    return [
        i
        for i, p in enumerate(screen.grid())
        if p["reaction_duration_s"] in (120, 600, 1200)
        and p["cooling_fraction"] == 0
        and p["cooling_duration_s"] == 1200
    ]


def queries():
    return {
        f"{w}_{i:02d}": {"world": w, "grid_index": i, "plan": screen.grid()[i]}
        for w in base.WORLDS[2:]
        for i in query_indices()
    }


def compact_table(rows):
    columns = [
        "world",
        "grid_index",
        "TR_K",
        "tR_s",
        "cooling_fraction",
        "tC_s",
        "upstream_yield",
        "upstream_conversion",
        "upstream_selectivity",
        "actual_quench_K",
        "actual_cooling_K",
        "crystal_yield",
        "crystal_purity",
        "utility_per_hour",
        "process_time_s",
        "cost_units",
        "sample_consumed_L",
        "measurement_cost_units",
    ]
    values = []
    for row in sorted(rows, key=lambda r: (r["world"], r["name"])):
        if row["world"] not in base.TRAIN:
            raise ValueError("heldout evidence cannot enter public source table")
        p, public = row["plan"], row["public"]
        h, terminal, resource = public["upstream_hplc"], public["terminal"], row["resources"]
        values.append(
            [
                row["world"],
                int(row["name"].rsplit("/", 1)[1]),
                *[p[k] for k in screen.BOUNDS],
                h["yield"],
                h["conversion"],
                h["selectivity"],
                public["actual_quench_temperature_K"],
                public["actual_cooling_temperature_K"],
                terminal["crystal_yield"],
                terminal["crystal_purity"],
                terminal["utility_per_hour"],
                *[resource[k] for k in columns[-4:]],
            ]
        )
    return {
        "columns": columns,
        "rows": values,
        "scope": "Lossless values of the declared scientific fields, not full observation logs.",
    }


def contract():
    result = deepcopy(base.public_contract())
    result["bounds"] = screen.BOUNDS
    result["resources"].update(
        batches_per_source=144,
        source_rounds=1,
        deployment="select one of 72 listed sealed recipes per world",
    )
    result["measurement_warning"] += (
        " The fixed source table contains all declared fields at full precision."
    )
    return result


def prompt(instruction, payload):
    return (
        "You are an experimental scientist. Use only supplied public records and contract. "
        "You may call public_numerics.calculate at most eight times; no other tools, files "
        "or external context. Return the required JSON and concise conclusions, not private "
        "chain-of-thought.\n"
        + instruction
        + "\nPUBLIC INPUT:\n"
        + json.dumps({"contract": contract(), **payload}, separators=(",", ":"))
    )


def encode(root, representation, table, deadline):
    props = (
        {"summary": {"type": "string", "maxLength": 4500}}
        if representation == "whole"
        else {
            k: {"type": "string", "maxLength": 900} for k in ("R1", "R2", "C1", "C2", "interface")
        }
    )
    instruction = (
        "Prepare reusable scientific knowledge from the complete learning table. The next "
        "scientist will see your package and this same contract but no source table. Preserve "
        "numeric intervention-response relations, uncertainty and limitations useful for "
        "predicting new component pairings and selecting high-utility recipes. You cannot see "
        "target queries or outcomes. "
        + (
            "Return one whole-process summary <=4500 characters; component reasoning is allowed."
            if representation == "whole"
            else "Return five named component/interface slots, each <=900 characters."
        )
    )
    call = base.invoke(
        root,
        "encode_" + representation,
        prompt(instruction, {"source": table}),
        base.object_schema(props),
        deadline=deadline,
        planned_calls=TOTAL,
    )
    value = call.get("payload")
    valid = (
        call["status"] == "completed"
        and isinstance(value, dict)
        and set(value) == set(props)
        and all(isinstance(value[k], str) and len(value[k]) <= props[k]["maxLength"] for k in props)
    )
    package = {
        "valid": valid,
        "payload": value if valid else None,
        "characters": sum(len(v) for v in value.values()) if valid else None,
        "failure": None if valid else "missing_or_invalid_package",
    }
    base.write(root / "packages" / (representation + ".json"), package)
    return package


def readout_schema():
    return base.object_schema(
        {
            "predictions": base.object_schema(
                {
                    q: base.object_schema(
                        {k: {"type": "number", "minimum": 0, "maximum": 1} for k in base.METRICS}
                    )
                    for q in queries()
                }
            ),
            "selections": base.object_schema(
                {w: {"type": "integer", "minimum": 0, "maximum": 71} for w in base.WORLDS}
            ),
        }
    )


def valid_readout(payload):
    if not isinstance(payload, dict) or set(payload) != {"predictions", "selections"}:
        return False
    predictions, selections = payload["predictions"], payload["selections"]
    return (
        isinstance(predictions, dict)
        and set(predictions) == set(queries())
        and all(
            isinstance(p, dict)
            and set(p) == set(base.METRICS)
            and all(
                type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in p.values()
            )
            for p in predictions.values()
        )
        and isinstance(selections, dict)
        and set(selections) == set(base.WORLDS)
        and all(type(v) is int and 0 <= v < 72 for v in selections.values())
    )


def readout(root, condition, packet, deadline):
    if packet is None:
        result = {"condition": condition, "status": "not_started", "failure": "missing_package"}
    else:
        instruction = (
            "Predict all 18 queries: reaction_yield means upstream HPLC yield; crystal_yield "
            "and crystal_purity mean final assay outcomes. For each of the four worlds select "
            "one listed candidate index to maximize utility_per_hour. All decisions are sealed "
            "together, no target feedback. Learning pairs and heldout pairs share their named "
            "component laws. Predictions must be in [0,1]."
        )
        if condition == "raw_scaffold":
            instruction += (
                " Explicit procedure: first use same-R learning records to infer reaction yield, "
                "conversion and actual interface temperatures under each control; then infer "
                "same-C downstream response conditional on this feed state and cooling controls. "
                "Compose these relations and use the public utility formula to choose recipes."
            )
        call = base.invoke(
            root,
            "read_" + condition,
            prompt(
                instruction,
                {
                    "knowledge_delivery": packet,
                    "blind_queries": queries(),
                    "candidate_recipes": {str(i): p for i, p in enumerate(screen.grid())},
                },
            ),
            readout_schema(),
            deadline=deadline,
            planned_calls=TOTAL,
        )
        valid = call["status"] == "completed" and valid_readout(call.get("payload"))
        result = {
            "condition": condition,
            "status": "completed" if valid else "failed",
            "failure": None if valid else call.get("failure") or "invalid_readout",
            "payload": call.get("payload") if valid else None,
        }
    base.write(root / "readouts" / (condition + ".json"), result)
    return result


def reference_predictions(source_rows):
    """Only source public values; target actual interface is never an input."""
    if any(r["world"] not in base.TRAIN for r in source_rows):
        raise ValueError("reference must use only learning pairs")
    source = {(r["world"], int(r["name"].rsplit("/", 1)[1])): r["public"] for r in source_rows}
    output = {"component_knn3": {}, "same_C_recipe": {}}
    for q, query in queries().items():
        w, i = query["world"], query["grid_index"]
        same_r = next(s for s in base.TRAIN if s[:2] == w[:2])
        same_c = next(s for s in base.TRAIN if s[2:] == w[2:])
        upstream = source[same_r, i]
        vector = np.array(base.support_vector(upstream))
        neighbors = sorted(
            (float(np.max(np.abs(np.array(base.support_vector(source[same_c, j])) - vector))), j)
            for j in range(72)
        )
        exact = [j for d, j in neighbors if d <= 1e-12]
        selected = exact if exact else [j for _, j in neighbors[:3]]
        weights = np.ones(len(exact)) if exact else np.array([1 / d**2 for d, _ in neighbors[:3]])
        weights /= weights.sum()
        prediction = {"reaction_yield": upstream["upstream_hplc"]["yield"]}
        prediction.update(
            {
                metric: float(
                    sum(
                        weight * source[same_c, j]["terminal"][metric]
                        for weight, j in zip(weights, selected, strict=True)
                    )
                )
                for metric in base.METRICS[1:]
            }
        )
        output["component_knn3"][q] = prediction
        output["same_C_recipe"][q] = {
            "reaction_yield": upstream["upstream_hplc"]["yield"],
            **{m: source[same_c, i]["terminal"][m] for m in base.METRICS[1:]},
        }
    return output


def prediction_scores(predictions, lookup, support):
    rows = []
    for q, query in queries().items():
        public = lookup[query["world"], query["grid_index"]]["public"]
        truth = {
            "reaction_yield": public["upstream_hplc"]["yield"],
            **{k: public["terminal"][k] for k in base.METRICS[1:]},
        }
        rows.append(
            {
                "query": q,
                "near_support": support[q],
                "truth": truth,
                "prediction": predictions[q],
                "absolute_errors": {k: abs(truth[k] - predictions[q][k]) for k in base.METRICS},
            }
        )
    groups = {
        "all": rows,
        "near_support": [r for r in rows if r["near_support"]],
        "outside_support": [r for r in rows if not r["near_support"]],
    }
    return {
        "rows": rows,
        "metrics": {
            name: {
                "denominator": len(items),
                "mae": {
                    metric: float(np.mean([r["absolute_errors"][metric] for r in items]))
                    if items
                    else None
                    for metric in base.METRICS
                },
            }
            for name, items in groups.items()
        },
    }


def summarize(root, source_report, failure):
    calls = [base.read(p) for p in sorted((root / "model").glob("*/result.json"))]
    attempts = list((root / "model").glob("*/attempt.json"))
    packages = {p.stem: base.read(p) for p in sorted((root / "packages").glob("*.json"))}
    readouts = {p.stem: base.read(p) for p in sorted((root / "readouts").glob("*.json"))}
    lookup = {(r["world"], int(r["name"].rsplit("/", 1)[1])): r for r in source_report["rows"]}
    source_rows = [r for r in source_report["rows"] if r["world"] in base.TRAIN]
    support_lookup = {
        f"{r['world']}_{int(r['query'].rsplit('/', 1)[1]):02d}": r["near_support"]
        for r in source_report["support"]
    }
    references = {
        name: prediction_scores(predictions, lookup, support_lookup)
        for name, predictions in reference_predictions(source_rows).items()
    }
    condition_rows = []
    for condition in CONDITIONS:
        row = readouts.get(
            condition, {"condition": condition, "status": "not_started", "failure": "block_stopped"}
        )
        selected = row.get("payload", {}).get("selections", {}) if row.get("payload") else {}
        utilities = {
            w: lookup[w, selected[w]]["public"]["terminal"]["utility_per_hour"]
            if w in selected
            else 0
            for w in base.WORLDS
        }
        row["selection_utility"] = utilities
        row["selection_relative_regret"] = {
            w: 1 - utilities[w] / source_report["action_value"]["best_by_world"][w]["utility"]
            for w in base.WORLDS
        }
        if row["status"] == "completed":
            row["prediction_scores"] = prediction_scores(
                row["payload"]["predictions"], lookup, support_lookup
            )
            values = {v for p in row["payload"]["predictions"].values() for v in p.values()}
            indices = set(selected.values())
            row["readout_behavior"] = {
                "constant_prediction_value": next(iter(values)) if len(values) == 1 else None,
                "constant_selected_index": next(iter(indices)) if len(indices) == 1 else None,
            }
        condition_rows.append(row)
    usage = Counter()
    for c in calls:
        usage.update(
            {
                k: v
                for k, v in c.get("receipt", {}).get("usage", {}).items()
                if isinstance(v, (int, float))
            }
        )
    near = sum(support_lookup[q] for q in queries())
    by_condition = {r["condition"]: r for r in condition_rows}

    def near_mae(c):
        return (
            by_condition[c]
            .get("prediction_scores", {})
            .get("metrics", {})
            .get("near_support", {})
            .get("mae", {})
            .get("crystal_yield")
        )

    ref_mae = references["component_knn3"]["metrics"]["near_support"]["mae"]["crystal_yield"]
    hint = {
        c: near >= 6
        and ref_mae is not None
        and ref_mae <= 0.1
        and near_mae("raw") is not None
        and near_mae("raw") <= 0.1
        and near_mae(c) is not None
        and near_mae(c) - near_mae("raw") >= 0.05
        for c in ("whole", "component")
    }
    report = {
        "status": "development_stopped" if failure else "development_completed",
        "formal_result": False,
        "note": NOTE,
        "run_root": root.relative_to(ROOT).as_posix(),
        "source_binding": "work_ii.w2_101_early_time_screen",
        "source_batches_reused": 144,
        "scoring_batches_reused": 288,
        "new_physical_executions": 0,
        "source_resources": dict(sum((Counter(r["resources"]) for r in source_rows), Counter())),
        "model": base.PROVIDER,
        "model_sessions": {
            "planned": TOTAL,
            "attempted": len(attempts),
            "completed": sum(c["status"] == "completed" for c in calls),
            "failed": sum(c["status"] == "failed" for c in calls),
            "interrupted": len(attempts) - len(calls),
            "not_started": TOTAL - len(attempts),
            "retries": 0,
        },
        "public_numerics_turns": sum(
            len(p.read_text(encoding="utf-8").splitlines())
            for p in (root / "model").glob("*/numerics.jsonl")
        ),
        "reported_usage": dict(usage),
        "subscription_usd": None,
        "model_call_rows": [
            {k: c.get(k) for k in ("name", "model", "reasoning_effort", "status", "failure")}
            | {
                "usage": c.get("receipt", {}).get("usage"),
                "elapsed_s": c.get("receipt", {}).get("elapsed_s"),
            }
            for c in calls
        ],
        "packages": packages,
        "conditions": condition_rows,
        "references": references,
        "query_near_support": {"count": near, "denominator": 18},
        "action_screen_passed": source_report["screen_passed"],
        "single_block_summary_loss_hint": hint,
        "systematic_failure_established": False,
        "failure": failure,
    }
    base.write(root / "summary.json", report)
    base.write(REPORT, report)
    write_markdown(report)
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "status",
                    "model_sessions",
                    "query_near_support",
                    "single_block_summary_loss_hint",
                )
            }
        ),
        flush=True,
    )
    return report


def write_markdown(report):
    counts = report["model_sessions"]
    evidence = [r for r in report["conditions"] if r["condition"] != "task_only"]
    optimum = sum(
        r["status"] == "completed"
        and all(abs(r["selection_relative_regret"][w]) < 1e-12 for w in base.WORLDS[2:])
        for r in evidence
    )
    hints = [k for k, v in report["single_block_summary_loss_hint"].items() if v]
    conclusion = (
        "未达到预定的摘要交付损失标准。"
        if not hints
        else f"以下摘要达到预定的单块损失提示：{', '.join(hints)}。"
    )
    lines = [
        "# Astra medium：充分取证后的同证据交付",
        "",
        conclusion + f"四种有证据读出中，{optimum}/4在两个留出世界均选中网格最优配方。",
        "单组单次结果不能证明普遍无损或系统性失效；应结合前块的弱行动区分度解释。",
        "",
        f"{counts['completed']}/7计划模型会话完成，失败{counts['failed']}，未启动{counts['not_started']}，重试0。",
        "复用144条学习轨迹与288条网格评分轨迹；新增物理实验0。每个编码/读出条件均只运行一次。",
        "",
        f"固定18个留出预测查询，公开近支持{report['query_near_support']['count']}/18。",
        "",
        "| 条件 | 反应MAE | 回收MAE | 纯度MAE | 近支持回收MAE | 留出选择平均效用 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["conditions"]:
        if row["status"] != "completed":
            lines.append(f"| {row['condition']} | {row['status']} | — | — | — | 0 |")
            continue
        m = row["prediction_scores"]["metrics"]
        v = m["all"]["mae"]
        n = m["near_support"]["mae"]["crystal_yield"]
        utility = np.mean([row["selection_utility"][w] for w in base.WORLDS[2:]])
        lines.append(
            f"| {row['condition']} | {v['reaction_yield']:.4f} | {v['crystal_yield']:.4f} | "
            f"{v['crystal_purity']:.4f} | {f'{n:.4f}' if n is not None else '—'} | {utility:.6f} |"
        )
    for name, reference in report["references"].items():
        v, n = (
            reference["metrics"]["all"]["mae"],
            reference["metrics"]["near_support"]["mae"]["crystal_yield"],
        )
        lines.append(
            f"| {name} | {v['reaction_yield']:.4f} | {v['crystal_yield']:.4f} | "
            f"{v['crystal_purity']:.4f} | {f'{n:.4f}' if n is not None else '—'} | — |"
        )
    lines += [
        "",
        f"前块完整行动资格通过：{report['action_screen_passed']}。选择结果受其限制，只对应72条已测候选的离散选择。",
        f"预定单块摘要损失提示：{report['single_block_summary_loss_hint']}。",
        "该提示需近支持至少6条、固定组合参照与raw近支持回收MAE≤0.10、摘要劣化≥0.05；不能据单次读出声称系统性失效。",
        "编码器看不到查询列表；5个读出使用同一合同与同一18项查询，均不访问留出答案。",
        "公开近支持不等于完整隐状态支持，原始表是指定公开字段的数值表，不是全部观测日志。",
        "明确组合步骤条件只增加程序提示；任何差异同时包含fresh会话波动。",
        "",
        f"实际数值工具轮次：{report['public_numerics_turns']}；token：{report['reported_usage']}。美元费用未估算。",
        "",
        "所有预测、真值、误差、选择、失败及资源见同名JSON。",
        "",
        "![开发实验对照图](work-ii-astra-dense-evidence-20260914.png)",
    ]
    task_only = next(r for r in report["conditions"] if r["condition"] == "task_only")
    behavior = task_only.get("readout_behavior", {})
    if behavior.get("constant_prediction_value") is not None:
        lines += [
            "",
            "无证据会话的54个预测统一为"
            f"{behavior['constant_prediction_value']}，四世界统一选择候选"
            f"{behavior.get('constant_selected_index')}；这是该次会话的实际输出，"
            "不代表最强无信息策略。provider最终消息与评分payload已保留，可核对。",
        ]
    if report["failure"]:
        lines += ["", f"停止原因：{report['failure']}"]
    REPORT.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binding = base.read(ROOT / "configs/current.json")["work_ii"]["w2_101_early_time_screen"]
    source_report = base.read(ROOT / binding["report"])
    if (
        source_report["physical_runs"]["completed"] != 288
        or not source_report["criteria"]["runtime_and_replay"]
    ):
        raise ValueError(
            "source block incomplete or runtime failed; no provider calls authorized by this note"
        )
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    for source in (Path(__file__), Path(base.__file__)):
        (root / source.name).write_bytes(source.read_bytes())
    (root / "experiment_note.md").write_bytes((ROOT / NOTE).read_bytes())
    base.write(
        root / "design.json",
        {
            "note": NOTE,
            "source_binding": binding,
            "queries": queries(),
            "conditions": CONDITIONS,
            "planned_sessions": TOTAL,
        },
    )
    table = compact_table([r for r in source_report["rows"] if r["world"] in base.TRAIN])
    base.write(root / "public_source_table.json", table)
    deadline = time.time() + 7200
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            n = len(list((root / "model").glob("*/result.json")))
            rate = n * 60 / (time.monotonic() - started)
            print(
                json.dumps(
                    {
                        "stage": "dense_evidence_readout",
                        "terminal_sessions": n,
                        "planned": TOTAL,
                        "sessions_per_minute": round(rate, 3),
                        "eta_minutes": round((TOTAL - n) / rate, 1) if rate else None,
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    failure = None
    try:
        packages = {r: encode(root, r, table, deadline) for r in ("whole", "component")}
        packets = {
            "raw": table,
            "whole": packages["whole"]["payload"],
            "component": packages["component"]["payload"],
            "raw_scaffold": table,
            "task_only": {"records": [], "knowledge": "No experimental evidence supplied."},
        }
        for condition in CONDITIONS:
            readout(root, condition, packets[condition], deadline)
    except (Exception, KeyboardInterrupt) as exc:
        failure = f"{type(exc).__name__}: {exc}"
    finally:
        stop.set()
        worker.join(timeout=2)
        base.write(root / "closed.json", {"failure": failure, "resume_planned": False})
        summarize(root, source_report, failure)
    if failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
