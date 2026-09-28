"""Score every retained cell and export the fixed three-model EQ matrix."""

# ruff: noqa: RUF001

from __future__ import annotations

import csv
import json
from collections import defaultdict
from statistics import fmean, stdev

from run_work_ii_eq_three_model_matrix import (
    ARMS,
    DILUTE,
    MODELS,
    REPORT,
    WORLDS,
    emit,
    folder,
    jobs,
    read,
    reused,
    source,
    write,
)


def csv_write(path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def score(payload, truth, metrics):
    predictions = {q["query_id"]: q for q in payload["predictions"]}
    result = {}
    for group, query_ids in (
        ("other_nine", [q for q in truth if q not in DILUTE]),
        ("dilute_three", list(DILUTE)),
        ("all_twelve", list(truth)),
    ):
        responses = {}
        for metric in metrics:
            errors, covered, widths, interval_scores = [], [], [], []
            for qid in query_ids:
                p = predictions[qid]["metrics"][metric]
                estimate, lower, upper = (float(p[k]) for k in ("estimate", "lower80", "upper80"))
                observed = [float(r[metric]) for r in truth[qid]]
                errors.append(abs(estimate - fmean(observed)))
                covered.extend(lower <= y <= upper for y in observed)
                widths.append(upper - lower)
                interval_scores.extend(
                    upper - lower + 10 * max(lower - y, y - upper, 0) for y in observed
                )
            responses[metric] = {
                "mae": fmean(errors),
                "coverage80": fmean(covered),
                "width80": fmean(widths),
                "interval_score80": fmean(interval_scores),
            }
        result[group] = {
            "query_count": len(query_ids),
            "reference_coverage_judgments": len(query_ids) * 3 * 5,
            "macro_mae": fmean(r["mae"] for r in responses.values()),
            "coverage80": fmean(r["coverage80"] for r in responses.values()),
            "responses": responses,
        }
    return result


def aggregate(cells, models=MODELS):
    rows = []
    for scope, worlds in (("all_five", WORLDS), ("new_worlds_only", WORLDS[1:])):
        for model in models:
            for arm in ARMS:
                chosen = [
                    c
                    for c in cells
                    if c["world_id"] in worlds and c["model"] == model and c["arm"] == arm
                ]
                valid = [c for c in chosen if c["prediction_metrics"] is not None]
                row = {
                    "scope": scope,
                    "model": model,
                    "arm": arm,
                    "planned_sessions": len(worlds),
                    "complete_chains": sum(c["status"] == "completed" for c in chosen),
                    "valid_Q": len(valid),
                    "groups": {},
                }
                for group in ("other_nine", "dilute_three", "all_twelve"):
                    values = [c["prediction_metrics"][group]["macro_mae"] for c in valid]
                    row["groups"][group] = {
                        "macro_mae": fmean(values) if values else None,
                        "world_sd": stdev(values) if len(values) > 1 else None,
                        "coverage80": fmean(
                            c["prediction_metrics"][group]["coverage80"] for c in valid
                        )
                        if valid
                        else None,
                        "responses": {
                            metric: {
                                measure: fmean(
                                    c["prediction_metrics"][group]["responses"][metric][measure]
                                    for c in valid
                                )
                                for measure in ("mae", "coverage80", "width80", "interval_score80")
                            }
                            for metric in valid[0]["prediction_metrics"][group]["responses"]
                        }
                        if valid
                        else {},
                    }
                rows.append(row)
    return rows


def paired(cells, models=MODELS):
    output = []
    for model in models:
        for world in WORLDS:
            arms = {c["arm"]: c for c in cells if c["model"] == model and c["world_id"] == world}
            for arm in ARMS[1:]:
                pair = [arms[a] for a in ("Opaque", arm)]
                valid = all(c["prediction_metrics"] is not None for c in pair)
                row = {
                    "model": model,
                    "world_id": world,
                    "contrast": f"{arm}-Opaque",
                    "valid_pair": valid,
                    "both_chains_complete": all(c["status"] == "completed" for c in pair),
                    "other_nine_delta": None,
                    "dilute_three_delta": None,
                    "reversal": None,
                }
                if valid:
                    for group in ("other_nine", "dilute_three"):
                        row[f"{group}_delta"] = (
                            arms[arm]["prediction_metrics"][group]["macro_mae"]
                            - arms["Opaque"]["prediction_metrics"][group]["macro_mae"]
                        )
                    row["reversal"] = row["other_nine_delta"] < 0 < row["dilute_three_delta"]
                output.append(row)
    return output


def analyze(
    root,
    config,
    truth,
    *,
    report=REPORT,
    selected_jobs=None,
    source_resolver=source,
    reused_predicate=reused,
    models=MODELS,
    scope="development extension with six previously inspected W01 pilot cells",
    render=True,
):
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    report.mkdir(parents=True, exist_ok=True)
    selected_jobs = jobs() if selected_jobs is None else selected_jobs
    cells, predictions, batches = [], [], []
    accounts = [
        "# Original public scientific accounts",
        "",
        "Original sealed K1/Q/K2/EQS outputs. No private reasoning or raw provider transport.",
    ]
    for job in selected_jobs:
        target = source_resolver(root, job)
        result = read(target / "RESULT.json") if (target / "RESULT.json").exists() else {}
        trajectory = target / "trajectory.jsonl"
        records = (
            [json.loads(s) for s in trajectory.read_text(encoding="utf-8").splitlines()]
            if trajectory.exists()
            else []
        )
        grouped = defaultdict(list)
        for r in records:
            grouped[r["experiment_index"]].append(r)
        start = len(batches)
        for index, steps in grouped.items():
            committed = [r for r in steps if r.get("transaction_status") == "committed"]
            finals = [r for r in committed if r.get("instrument") == "final_assay"]
            if not finals:
                continue
            acid = sum(
                r["action"].get("amount_mol", 0)
                for r in committed
                if r["action"].get("operation") == "add_reagent"
            )
            volume = sum(
                r["action"].get("volume_L", 0)
                for r in committed
                if r["action"].get("operation") == "add_solvent"
            )
            batches.append(
                {
                    **job,
                    "batch": index + 1,
                    "reused_pilot": reused_predicate(job),
                    "operation_attempts": len(steps),
                    "rollbacks": len(steps) - len(committed),
                    "reagent_mol": acid,
                    "solvent_L": volume,
                    "nominal_input_concentration_M": acid / volume if volume else None,
                    **{m: finals[-1]["observation"][m] for m in eq.METRICS},
                    "operations": " > ".join(r["action"]["operation"] for r in committed),
                }
            )
        provenance = result.get("source_usage", {}).get("model_provenance", {})
        row = {
            **job,
            "reused_pilot": reused_predicate(job),
            "infrastructure_recovered": (not reused_predicate(job) and target != folder(root, job))
            or bool(result.get("posttest_recoveries")),
            "status": result.get("status", "missing_result"),
            "source_status": result.get("source_status", "missing_result"),
            "source_batches": len(batches) - start,
            "operations": len(records),
            "rollbacks": sum(r.get("transaction_status") != "committed" for r in records),
            "replay_verified": result.get("exact_replay", {}).get("verified", False),
            "sealed_stages": {
                s: v.get("valid") for s, v in result.get("posttest_validation", {}).items()
            },
            "posttest_failures": {
                s: {
                    "validation_failure": v.get("failure"),
                    "provider_failure": result.get("posttests", {}).get(s, {}).get("failure"),
                }
                for s, v in result.get("posttest_validation", {}).items()
                if not v.get("valid")
            },
            "posttest_recoveries": result.get("posttest_recoveries", []),
            "elapsed_s": result.get("elapsed_s"),
            "failure": result.get("failure"),
            "recorded_model": provenance.get("model_id"),
            "reasoning_effort": provenance.get("request_parameters", {}).get("reasoning_effort"),
            "prediction_metrics": None,
            "Q08_dissociation": None,
            "source_usage": {
                k: result.get("source_usage", {}).get(k)
                for k in (
                    "input_token_count",
                    "cached_input_token_count",
                    "uncached_input_token_count",
                    "output_token_count",
                    "session_elapsed_s",
                    "provider_process_attempt_count",
                )
            },
        }
        if row["status"] == "completed":
            assert row["source_batches"] == 12 and row["replay_verified"]
            assert row["recorded_model"] == job["model"] and row["reasoning_effort"] == "medium"
            assert all(row["sealed_stages"].get(s) for s in eq.POSTTEST_STAGES)
        cells.append(row)
        accounts.extend(["", f"## {job['model']} / {job['world_id']} / {job['arm']}"])
        for stage in eq.POSTTEST_STAGES:
            path = target / "sealed" / f"{stage}.json"
            if not path.exists():
                continue
            payload = read(path).get("payload")
            accounts.extend(
                ["", f"### {stage}", "", "```json", json.dumps(payload, indent=2), "```"]
            )
            if (
                stage != "Q"
                or not eq.validate_posttest(stage, payload, eq.queries(config))["valid"]
            ):
                continue
            cell_truth = truth[job["world_id"]]
            row["prediction_metrics"] = score(payload, cell_truth, eq.METRICS)
            original = eq.evaluate_predictions(payload, eq.queries(config), cell_truth)
            for metric in eq.METRICS:
                current = row["prediction_metrics"]["all_twelve"]["responses"][metric]
                for new, old in (
                    ("mae", "mae_to_five_repeat_mean"),
                    ("coverage80", "empirical_coverage80"),
                ):
                    assert abs(current[new] - original["metrics"][metric][old]) < 1e-12
            for q in payload["predictions"]:
                qid = q["query_id"]
                for metric in eq.METRICS:
                    p = q["metrics"][metric]
                    observed = [r[metric] for r in cell_truth[qid]]
                    predictions.append(
                        {
                            **job,
                            "query_id": qid,
                            "response": metric,
                            "group": "dilute_three" if qid in DILUTE else "other_nine",
                            **p,
                            "reference_mean": fmean(observed),
                            "absolute_error": abs(p["estimate"] - fmean(observed)),
                            "covered_references": sum(
                                p["lower80"] <= v <= p["upper80"] for v in observed
                            ),
                            "reference_count": 5,
                        }
                    )
                    if qid == "Q08" and metric == "acid_dissociation_fraction":
                        row["Q08_dissociation"] = {**p, "reference_mean": fmean(observed)}
    summary = {
        "status": "complete"
        if all(c["status"] == "completed" for c in cells)
        else "terminal_with_failures",
        "scope": scope,
        "planned_sessions": len(selected_jobs),
        "reused_sessions": sum(reused_predicate(j) for j in selected_jobs),
        "new_sessions": sum(not reused_predicate(j) for j in selected_jobs),
        "completed_sessions": sum(c["status"] == "completed" for c in cells),
        "completed_source_sessions": sum(c["source_status"] == "completed" for c in cells),
        "planned_batches": 12 * len(selected_jobs),
        "completed_batches": len(batches),
        "planned_stages": 4 * len(selected_jobs),
        "valid_stages": sum(sum(bool(v) for v in c["sealed_stages"].values()) for c in cells),
        "valid_Q_sessions": sum(c["prediction_metrics"] is not None for c in cells),
        "planned_scalar_predictions": 36 * len(selected_jobs),
        "valid_scalar_predictions": len(predictions),
        "replay_verified": sum(c["replay_verified"] for c in cells),
        "operations": sum(c["operations"] for c in cells),
        "rollbacks": sum(c["rollbacks"] for c in cells),
        "cells": cells,
        "aggregates": aggregate(cells, models),
        "paired_comparisons": paired(cells, models),
    }
    recovery_path = root / "infrastructure-recovery.json"
    summary["retained_infrastructure_attempts"] = []
    if recovery_path.exists():
        plan = read(recovery_path)
        original = read(folder(root, plan) / "RESULT.json")
        summary["retained_infrastructure_attempts"].append(
            {
                "model": plan["model"],
                "cell_id": plan["cell_id"],
                "classification": plan["classification"],
                "operations": original["operations"],
                "source_batches": len(original["batches"]),
                "failure": original["failure"],
                "recovery_attempted": (root / "infrastructure-recovery-exit.json").exists(),
            }
        )
    summary["infrastructure_recovered_cells"] = sum(c["infrastructure_recovered"] for c in cells)
    for cell in cells:
        for recovery in cell["posttest_recoveries"]:
            summary["retained_infrastructure_attempts"].append(
                {
                    "model": cell["model"],
                    "cell_id": cell["cell_id"],
                    "stage": recovery["stage"],
                    "classification": recovery["classification"],
                    "failure": recovery["failure"],
                    "recovery_attempted": True,
                    "recovery_valid": recovery["recovery_valid"],
                    "same_thread_verified": recovery["same_thread_verified"],
                    "source_K1_Q_K2_unchanged": recovery["source_K1_Q_K2_unchanged"],
                }
            )
    write(root / "summary.json", summary)
    write(report / "summary.json", summary)
    write(report / "reference_observations.json", truth)
    cell_rows = []
    for cell in cells:
        flat = {
            k: cell[k]
            for k in (
                "world_id",
                "model",
                "arm",
                "reused_pilot",
                "status",
                "source_batches",
                "operations",
                "rollbacks",
                "replay_verified",
                "reasoning_effort",
                "elapsed_s",
            )
        }
        flat["valid_Q"] = cell["prediction_metrics"] is not None
        for group in ("other_nine", "dilute_three", "all_twelve"):
            for metric in ("macro_mae", "coverage80"):
                flat[f"{group}_{metric}"] = (
                    cell["prediction_metrics"][group][metric]
                    if cell["prediction_metrics"] is not None
                    else None
                )
        cell_rows.append(flat)
    csv_write(report / "cell_metrics.csv", cell_rows)
    csv_write(report / "source_batches.csv", batches)
    csv_write(report / "predictions.csv", predictions)
    csv_write(report / "paired_comparisons.csv", summary["paired_comparisons"])
    (report / "PUBLIC_ACCOUNTS.md").write_text("\n".join(accounts) + "\n", encoding="utf-8")
    if render:
        render_report(summary)
        plot(summary)
    emit(
        {
            "phase": "finished",
            "status": summary["status"],
            "completed": summary["completed_sessions"],
            "planned": len(selected_jobs),
        }
    )
    return summary


def render_report(summary):
    lines = [
        "# 五世界三臂跨模型平衡实验",
        "",
        f"完成 {summary['completed_sessions']}/45 会话、{summary['completed_batches']}/540 批实验、"
        f"{summary['valid_stages']}/180 个问答阶段。"
        f"有效预测 {summary['valid_scalar_predictions']}/1620。",
        "",
        "三个模型均为 medium。保留已知结果的六场 W01 先导研究，新增 39 场；"
        "全部原会话继续 K1/Q/K2/EQS。",
        "运行记录保留一次 Luna/W03/Aligned 的零操作网络中断，以及在原六路池内"
        "完成的隔离恢复；未替换任何已产生科学观测的结果。恢复记录见机器汇总。"
        if summary["retained_infrastructure_attempts"]
        else "无基础设施恢复。",
        "",
        "## 五世界等权平均",
        "",
        "| 模型 | 信息条件 | 完整会话 / 有效 Q | 其余九题 MAE | 最稀三题 MAE | 最稀组覆盖率 |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summary["aggregates"]:
        if row["scope"] != "all_five":
            continue
        groups = row["groups"]
        values = [groups["other_nine"]["macro_mae"], groups["dilute_three"]["macro_mae"]]
        text = [f"{v:.5f}" if v is not None else "缺失" for v in values]
        coverage = groups["dilute_three"]["coverage80"]
        lines.append(
            "| "
            + " | ".join(
                [
                    row["model"],
                    row["arm"],
                    f"{row['complete_chains']}/5；{row['valid_Q']}/5",
                    *text,
                    f"{coverage:.1%}" if coverage is not None else "缺失",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "MAE 为三个响应（pH/14、解离率、沉淀信号）的等权平均。最稀三题固定为 Q03/Q08/Q09；"
        "其余九题也包含边界及未探索条件。名义区间覆盖率为 80%。",
        "",
        "## 逐世界配对差值",
        "",
        "| 模型 | 世界 | 对比 | 九题 ΔMAE | 三题 ΔMAE | 收益反转 |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in summary["paired_comparisons"]:
        values = [
            f"{row[k]:+.5f}" if row[k] is not None else "缺失"
            for k in ("other_nine_delta", "dilute_three_delta")
        ]
        lines.append(
            "| "
            + " | ".join(
                [
                    row["model"],
                    row["world_id"],
                    row["contrast"],
                    *values,
                    "是" if row["reversal"] else "否" if row["valid_pair"] else "缺失",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "负差值表示相对 Opaque 改善；反转判据为九题差值 < 0 且三题差值 > 0。",
        "",
        "完整分母、失败、W02–W05 敏感性分析和逐世界读出见 [机器汇总](summary.json)。",
        "逐批数据：[source_batches.csv](source_batches.csv)；逐题预测：[predictions.csv](predictions.csv)；原会话公开解释：[PUBLIC_ACCOUNTS.md](PUBLIC_ACCOUNTS.md)。",
        "",
        "这是固定五世界的开发性扩展；每个模型/世界/信息条件只有一次会话。查询、响应和真值重复不作为独立模型重复。",
        "",
    ]
    (REPORT / "REPORT_ZH.md").write_text("\n".join(lines), encoding="utf-8")


def plot(summary, models=MODELS, report=REPORT):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    colors = {"Opaque": "#64727E", "Aligned": "#2D9A87", "MisIndexed": "#CC8549"}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), sharey=True, layout="constrained")
    valid = [c for c in summary["cells"] if c["prediction_metrics"] is not None]
    if not valid:
        plt.close(fig)
        return
    ymax = max(
        c["prediction_metrics"][g]["macro_mae"]
        for c in valid
        for g in ("other_nine", "dilute_three")
    )
    for ax, group, title in zip(
        axes,
        ("other_nine", "dilute_three"),
        ("Other nine queries", "Three most dilute queries"),
        strict=True,
    ):
        for mi, model in enumerate(models):
            for ai, arm in enumerate(ARMS):
                rows = [c for c in valid if c["model"] == model and c["arm"] == arm]
                if not rows:
                    continue
                x = mi + (ai - 1) * 0.26
                values = [c["prediction_metrics"][group]["macro_mae"] for c in rows]
                ax.bar(
                    x,
                    fmean(values),
                    width=0.23,
                    color=colors[arm],
                    alpha=0.85,
                    label=arm if mi == 0 else None,
                    zorder=2,
                )
                ax.scatter(
                    [x + (WORLDS.index(c["world_id"]) - 2) * 0.027 for c in rows],
                    values,
                    s=20,
                    color="#202020",
                    edgecolor="white",
                    linewidth=0.5,
                    zorder=4,
                )
        ax.set_xticks(
            range(len(models)), [m.removeprefix("gpt-").replace("-", " ").title() for m in models]
        )
        ax.set_title(title, fontsize=12)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color="#E5E5E5", linewidth=0.7)
        ax.set_ylim(0, ymax * 1.12)
    axes[0].set_ylabel("Macro MAE (lower is better)")
    axes[0].legend(frameon=False, fontsize=9)
    fig.supxlabel(
        "Bars: equal-world means. Dots: individual worlds. All models use medium.", fontsize=10
    )
    fig.savefig(report / "comparison.png", dpi=180)
    fig.savefig(report / "comparison.pdf")
    plt.close(fig)
