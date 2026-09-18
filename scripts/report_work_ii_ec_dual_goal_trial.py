"""Export public EC pilot outcomes and verbatim posttests, excluding raw provider payloads."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_ec_dual_goal_trial import K1, K2, METRICS, summaries

from chemworld.data.logging import load_jsonl

ROOT = Path(__file__).resolve().parents[1]


def number(value):
    return f"{value:.4f}" if isinstance(value, (int, float)) else "—"


def token_usage(value):
    value = value or {}
    aliases = {
        "input_tokens": "prompt_tokens",
        "cached_input_tokens": "prompt_cache_hit_tokens",
        "output_tokens": "completion_tokens",
        "reasoning_output_tokens": "reasoning_output_tokens",
    }
    return {key: int(value.get(key, value.get(alias, 0))) for key, alias in aliases.items()}


def recipe_description(actions):
    """Compact public actions without treating a current cap as delivered current."""
    steps = []
    for action in actions:
        operation = action.get("operation")
        if operation == "add_solvent":
            steps.append(f"S{action['solvent']} {action['volume_L']:g} L")
        elif operation == "add_reagent":
            steps.append(f"原料 {action['amount_mol']:g} mol")
        elif operation == "set_potential":
            steps.append(
                f"E{action['electrolyte_profile']} {action['potential_V']:g} V / "
                f"上限{action['current_mA']:g} mA"
            )
        elif operation == "electrolyze":
            steps.append(f"电解 {action['duration_s']:g} s")
        elif operation == "measure" and action.get("instrument") != "final_assay":
            steps.append(f"测量 {action['instrument']}")
        elif operation not in ("terminate", "measure"):
            steps.append(json.dumps(action, ensure_ascii=False))
    return " → ".join(steps)


def model_tool_transcript(folder):
    """Actual model tool inputs/outputs, after any agent-written script filtering."""
    rows = []
    for path in sorted((folder / "provider-rollouts").rglob("*.jsonl")):
        phase_index = -1
        for line in path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if event.get("type") == "turn_context":
                phase_index += 1
            payload = event.get("payload", {})
            if event.get("type") != "response_item" or payload.get("type") not in (
                "custom_tool_call",
                "custom_tool_call_output",
                "function_call",
                "function_call_output",
            ):
                continue
            rows.append(
                {
                    "phase": ("source", "K1", "Q", "K2")[phase_index]
                    if 0 <= phase_index < 4
                    else f"unmapped_turn_{phase_index}",
                    **{
                        key: payload[key]
                        for key in ("type", "call_id", "name", "input", "arguments", "output")
                        if key in payload
                    },
                }
            )
    return rows


def figures(rows, out):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    colors = {"Opaque": "#53636f", "Aligned": "#167da5", "MisIndexed": "#c05b47"}
    loci = [locus for locus in "EPS" if any(r["locus"] == locus for r in rows)] or ["E"]
    fig, axes = plt.subplots(
        2, len(loci), figsize=(5.5 if len(loci) == 1 else 11, 6.2),
        sharex=True, sharey=True, squeeze=False,
    )
    for row_index, goal in enumerate(("discovery", "optimization")):
        for col, locus in enumerate(loci):
            ax = axes[row_index, col]
            for row in rows:
                if row["goal"] != goal or row["locus"] != locus:
                    continue
                ys = [b["metrics"].get("score", float("nan")) for b in row["batches"]]
                if ys:
                    xs = np.arange(1, len(ys) + 1)
                    ax.plot(xs, ys, color=colors[row["arm"]], alpha=0.3, linewidth=0.8)
                    ax.plot(
                        xs,
                        np.maximum.accumulate(ys),
                        color=colors[row["arm"]],
                        label=row["arm"],
                        linewidth=1.8,
                    )
            ax.set_title(f"{goal.title()} / {locus}")
            ax.set(xlim=(1, 12), ylim=(0, 1), xticks=(1, 4, 8, 12))
            ax.grid(alpha=0.17)
            if col == 0:
                ax.set_ylabel("Observed balanced score")
            if row_index == 1:
                ax.set_xlabel("Completed batch")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.955), ncol=3, frameon=False
    )
    fig.suptitle("EC pilot: batch scores (faint) and best observed score", y=0.995, fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(out / "source-progress.png", dpi=160)
    fig.savefig(out / "source-progress.svg")
    plt.close(fig)
    valid = [r for r in rows if (r.get("prediction_evaluation") or {}).get("valid")]
    if valid:
        data = [[r["prediction_evaluation"]["metrics"][m]["mae"] for m in METRICS] for r in valid]
        fig, ax = plt.subplots(figsize=(10, max(3, len(valid) * 0.36)))
        im = ax.imshow(data, aspect="auto", cmap="YlOrRd", vmin=0)
        ax.set_yticks(range(len(valid)), [r["cell_id"] for r in valid])
        ax.set_xticks(
            range(6), ["Yield", "Selectivity", "Faradaic", "Transport", "Energy", "Score"]
        )
        for i, values in enumerate(data):
            for j, value in enumerate(values):
                ax.text(
                    j,
                    i,
                    f"{value:.3f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white" if value > 0.65 * np.max(data) else "black",
                )
        ax.set_title("Blind prediction MAE: 12 fixed conditions per source")
        fig.colorbar(im, ax=ax, label="Absolute error (all metrics in [0, 1])")
        fig.tight_layout()
        fig.savefig(out / "prediction-mae.png", dpi=160)
        fig.savefig(out / "prediction-mae.svg")
        plt.close(fig)


def public_cell(root, cell):
    folder = root / cell["cell_id"]
    completion_path = folder / "posttest-completion" / "result.json"
    completion = read(completion_path) if completion_path.exists() else None
    posttest_data = completion["posttests"] if completion else cell["posttests"]
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    final = [
        r
        for r in records
        if r.get("instrument") == "final_assay" and r.get("transaction_status") == "committed"
    ]
    mid = [
        r
        for r in records
        if r.get("action", {}).get("operation") == "measure"
        and r.get("instrument") != "final_assay"
        and r.get("transaction_status") == "committed"
    ]
    previous_retest = cell.get("recommendation_retest", {})
    repaired_path = folder / "recommendation-retest-source-budget" / "result.json"
    retest = read(repaired_path) if repaired_path.exists() else previous_retest
    retest_batches = retest.get("batches", [])
    posttests = {}
    for stage, receipt in posttest_data.items():
        posttests[stage] = {
            "answer": receipt.get("payload"),
            "failure": receipt.get("failure"),
            "elapsed_s": receipt.get("elapsed_s"),
            "cumulative_thread_usage": receipt.get("usage"),
        }
    source_receipts = read(folder / "source-receipts.json")
    previous_usage = token_usage(source_receipts[-1].get("usage") if source_receipts else {})
    phase_usage = {"source": previous_usage}
    for stage in ("K1", "Q", "K2"):
        receipt = posttest_data.get(stage)
        if not receipt or not receipt.get("thread_id"):
            continue
        current_usage = token_usage(receipt.get("usage"))
        if any(current_usage[k] < previous_usage[k] for k in current_usage):
            phase_usage[stage] = {"accounting_status": "nonmonotonic_report_requires_review"}
        else:
            phase_usage[stage] = {k: current_usage[k] - previous_usage[k] for k in current_usage}
            previous_usage = current_usage
    transcript = []
    stdout = folder / "source-stdout.jsonl"
    if stdout.exists():
        for line in stdout.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            item = event.get("item", {})
            if event.get("type") != "item.completed":
                continue
            if item.get("type") == "mcp_tool_call":
                response = item.get("result") or {}
                public_content = []
                for block in response.get("content", []) if isinstance(response, dict) else []:
                    if block.get("type") == "text":
                        try:
                            public_content.append(json.loads(block["text"]))
                        except (TypeError, ValueError):
                            public_content.append(block.get("text"))
                transcript.append(
                    {
                        "tool": item.get("tool"),
                        "server": item.get("server"),
                        "arguments": item.get("arguments"),
                        "public_response": public_content,
                        "status": item.get("status"),
                        "error": item.get("error"),
                    }
                )
            elif item.get("type") == "agent_message":
                transcript.append({"type": "agent_message", "text": item.get("text")})
    usage = cell.get("source_usage", {})
    return {
        **{
            k: cell.get(k)
            for k in (
                "cell_id",
                "goal",
                "locus",
                "arm",
                "status",
                "source_status",
                "failure",
                "operations",
                "elapsed_s",
                "rollbacks",
                "recommendation",
                "prediction_evaluation",
                "pre_repair_status",
                "pre_repair_failure",
            )
        },
        "final_assays": len(final),
        "public_tool_transcript": transcript,
        "model_tool_transcript": model_tool_transcript(
            folder / "posttest-completion" if completion else folder
        ),
        "posttest_procedure_amendment": bool(completion),
        "posttest_completion_status": completion.get("status") if completion else None,
        "posttest_completion_failure": completion.get("failure") if completion else None,
        "source_completion_issue": (
            f"{len(final)}/12 final assays; source not completed to planned count"
            if len(final) != 12 else None
        ),
        "prediction_evaluation": (
            completion["prediction_evaluation"] if completion else cell.get("prediction_evaluation")
        ),
        "source_handoff": [r.get("final_payload_summary") for r in source_receipts],
        "thread_cumulative_token_usage": previous_usage,
        "phase_incremental_token_usage": phase_usage,
        "usage_note": (
            "Codex resume reports cumulative thread totals; increments avoid double counting"
        ),
        "intermediate_measurements": len(mid),
        "discarded_batches": sum(
            r.get("action", {}).get("operation") == "discard_batch"
            and r.get("transaction_status") == "committed" for r in records
        ),
        "source_transport_outcomes": [
            {
                key: receipt.get(key) for key in (
                    "status", "terminal_reason", "provider_error_event_count",
                    "recovered_mcp_tool_failure_count", "mcp_tool_failure_taxonomy",
                )
            }
            for receipt in source_receipts
        ],
        "source_model": [
            {k: r.get(k) for k in ("model_id", "reasoning_effort", "usage", "failure_type")}
            for r in source_receipts
        ],
        "source_accounting": {
            k: usage.get(k)
            for k in (
                "input_token_count",
                "cached_input_token_count",
                "uncached_input_token_count",
                "output_token_count",
                "usage_complete",
                "provider_token_accounting_complete",
                "monetary_accounting_complete",
            )
        },
        "exact_replay": cell["exact_replay"],
        "batches": summaries(records),
        "posttests": posttests,
        "recommendation_retest": {
            "status": retest.get("status", "original_evaluation_only"),
            "unavailable_reason": retest.get("reason"),
            "failure": retest.get("failure"),
            "source_resource_envelope_matched": repaired_path.exists(),
            "previous_evaluator_failure": previous_retest.get("failure"),
            "exact_replay": retest.get("exact_replay"),
            "metrics": retest_batches[0]["metrics"] if retest_batches else None,
        },
        "public_trajectory": [
            {
                "step": i + 1,
                "action": r.get("action"),
                "status": r.get("transaction_status"),
                "observation": r.get("observation"),
                "rollback_reason": r.get("rollback_reason"),
            }
            for i, r in enumerate(records)
        ],
    }


def append_cell(row, root, out, posttest_root, truth):
    write(out / (row["cell_id"] + "-tools.json"), row["public_tool_transcript"])
    write(out / (row["cell_id"] + "-model-tools.json"), row["model_tool_transcript"])
    lines = [
        f"# {row['cell_id']}：完整公开结果",
        "",
        "开发试跑；同一世界的一场来源，不是独立机制重复。",
        "",
        f"状态：{row['status']}；终检 {row['final_assays']}/12；"
        f"中途测量 {row['intermediate_measurements']}/12。",
        f"失败：{json.dumps(row['failure'], ensure_ascii=False)}",
        f"来源完成情况：{row['source_completion_issue'] or '12/12'}。"
        + (
            "原来源失败状态保留；K1/Q/K2为来源队列结束后、沿原thread进行的一次程序补充。"
            if row["posttest_procedure_amendment"] else ""
        ),
        "",
        "快速阅读：先看十二批结果和操作摘要，再看 K1 机理、Q 盲预测、K2 复盘；"
        "完整逐步观测可展开核对。",
        "",
        "## 实际输入",
        "",
        "来源系统提示及初始公共任务如下（不含后台种子/真值/评估结果）。具体盲测题在 K1 后展示。",
        f"[工具执行层完整返回]({row['cell_id']}-tools.json)包括执行器取得的所有观测；"
        f"[模型实际工具输入输出]({row['cell_id']}-model-tools.json)保留 Agent 脚本及其输出。"
        "脚本可能只打印筛选后的摘要，故前者不自动等于进入模型上下文的内容。"
        "未读取的仪器附件不算已读取证据；不导出内部推理记录。",
        "",
    ]
    folder = root / row["cell_id"]
    for filename in ("source-instructions.txt", "source-prompt.txt"):
        if (folder / filename).exists():
            lines += [
                f"### {filename}",
                "",
                "```text",
                (folder / filename).read_text(encoding="utf-8"),
                "```",
                "",
            ]
    material_path = folder / "workspace" / "reference" / "material_information.json"
    if material_path.exists():
        lines += [
            "### Agent 实际取得的资料",
            "",
            "```json",
            json.dumps(read(material_path), ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    lines += [
        "## 十二批结果",
        "",
        "| 批次 | 产率 | 选择性 | 法拉第效率 | 传质效率 | 能量效率 | 得分 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for batch in row["batches"]:
        lines.append(
            "| "
            + str(batch["ordinal"])
            + " | "
            + " | ".join(number(batch["metrics"].get(k)) for k in METRICS)
            + " |"
        )
    lines += [
        "",
        "### 每批实际操作摘要",
        "",
        "电流值为设定上限；下表保持操作顺序，包括中途测量和分段电解。",
        "",
        "| 终检序号 / 生命周期编号 | 操作 |",
        "| --- | --- |",
    ]
    for batch in row["batches"]:
        lines.append(
            f"| {batch['ordinal']} / {batch['lifecycle_index']} | "
            f"{recipe_description(batch['actions'])} |"
        )
    lines += [
        "",
        "## 完整操作与公开观测",
        "",
        "观测按实际返回记录；未测或掩码字段不解释为已取得的证据。",
        "",
        "<details>",
        "<summary>展开完整逐步操作与观测</summary>",
        "",
    ]
    for record in row["public_trajectory"]:
        lines += [
            f"### 步骤 {record['step']} · {record['status']}",
            "",
            "```json",
            json.dumps(record, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    lines += [
        "</details>",
        "",
        "## 封存操作建议及独立复测",
        "",
        "```json",
        json.dumps(
            {"recommendation": row["recommendation"], "retest": row["recommendation_retest"]},
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
    ]
    lines += ["## 来源封存时的简短交付", "", *[x for x in row["source_handoff"] if x], ""]
    for stage in ("K1", "Q", "K2"):
        lines += [f"## {stage}：问题与完整回答", ""]
        posttest_folder = posttest_root / row["cell_id"]
        if row["posttest_procedure_amendment"]:
            posttest_folder = folder / "posttest-completion"
        prompt_path = posttest_folder / stage / "prompt.txt"
        lines += [
            (
                prompt_path.read_text(encoding="utf-8")
                if prompt_path.exists()
                else {"K1": K1, "K2": K2}.get(stage, "该阶段未执行；题目见固定设计。")
            ),
            "",
        ]
        receipt = row["posttests"].get(stage, {})
        payload = receipt.get("answer")
        if isinstance(payload, dict) and "report" in payload:
            lines += [payload["report"], ""]
        else:
            lines += ["```json", json.dumps(payload, ensure_ascii=False, indent=2), "```", ""]
        if receipt.get("failure"):
            lines += [f"后测失败：{receipt['failure']}", ""]
        if stage == "Q" and isinstance(payload, dict):
            lines += [
                "### 预测与独立参考逐项对照",
                "",
                "以下参考值只用于事后核验，未反馈给 Agent；区间为 Agent 提交的 80% 预测区间。",
                "",
                "| 条件 | 指标 | 预测 | 下限 | 上限 | 参考观测 | 绝对误差 |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
            for prediction in payload.get("predictions", []):
                query_id = prediction.get("query_id")
                for metric in METRICS:
                    item = prediction.get(metric, {})
                    target = truth.get(query_id, {}).get(metric)
                    estimate = item.get("estimate")
                    error = (
                        abs(estimate - target)
                        if isinstance(estimate, (int, float)) and isinstance(target, (int, float))
                        else None
                    )
                    lines.append(
                        f"| {query_id} | {metric} | {number(estimate)} | "
                        f"{number(item.get('lower80'))} | {number(item.get('upper80'))} | "
                        f"{number(target)} | {number(error)} |"
                    )
    lines += [
        "## 独立预测核验",
        "",
        "```json",
        json.dumps(row.get("prediction_evaluation"), ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    (out / (row["cell_id"] + ".md")).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, out = args.input.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    summary = read(root / "summary.json")
    source_root = Path(summary.get("source_root", root))
    scope_path = source_root / "scope-revision.json"
    scope = read(scope_path) if scope_path.exists() else {}
    planned_core = len(scope.get("core_sources", [])) if scope else 18
    planned_supplement = len(scope.get("retained_supplementary_sources", []))
    planned_total = planned_core + planned_supplement
    rows = [
        public_cell(source_root, c) for c in summary["results"]
        if c["status"] != "not_started_scope_reduced"
    ]
    for row in rows:
        row["analysis_role"] = (
            "supplementary"
            if row["cell_id"] in scope.get("retained_supplementary_sources", []) else "core"
        )
    core_rows = [row for row in rows if row["analysis_role"] == "core"]
    supplementary_rows = [row for row in rows if row["analysis_role"] == "supplementary"]
    startup_failures = []
    for version in (1, 2, 3):
        old_root = source_root.parent / f"ec-sol-dual-goal-20260918-v{version}"
        for attempt in sorted(old_root.glob("*/attempt.json")):
            result_path = attempt.parent / "result.json"
            old = read(result_path) if result_path.exists() else {}
            receipt_path = attempt.parent / "source-receipts.json"
            receipts = read(receipt_path) if receipt_path.exists() else []
            startup_failures.append(
                {
                    "block": f"v{version}",
                    "cell_id": attempt.parent.name,
                    "status": old.get("status", "interrupted_without_result"),
                    "operations": old.get("operations", 0),
                    "failure": old.get("failure"),
                    "model_thread_started": any(r.get("thread_id") for r in receipts)
                    if receipts
                    else None,
                    "reported_usage": [
                        r.get("usage") if r.get("usage_observed") else None for r in receipts
                    ],
                }
            )
    excluded_sources = []
    unblinded = source_root.parent / "ec-sol-dual-goal-20260918-v4"
    if source_root.name != unblinded.name:
        for attempt in sorted(unblinded.glob("*/attempt.json")):
            source = attempt.parent
            path = source / "trajectory.jsonl"
            records = load_jsonl(path) if path.exists() else []
            batches = summaries(records)
            old_retest_path = source / "recommendation-retest" / "result.json"
            old_retest = read(old_retest_path) if old_retest_path.exists() else {}
            receipt_path = source / "source-receipts.json"
            receipts = read(receipt_path) if receipt_path.exists() else []
            excluded_sources.append(
                {
                    "cell_id": source.name,
                    "operations": len(records),
                    "final_assays": len(batches),
                    "best_observed_score": max(
                        (b["metrics"].get("score", 0) for b in batches), default=None
                    ),
                    "status": "excluded_input_blinding_failure",
                    "reason": (
                        "arm label exposed through automatically injected cwd; whole block stopped"
                    ),
                    "result_present": (source / "result.json").exists(),
                    "independent_retest_batches": len(old_retest.get("batches", [])),
                    "reported_source_usage": (
                        receipts[-1].get("usage") if receipts else None
                    ),
                }
            )
    truth = read(root / "truth.json")
    output = {
        "status": "complete" if len(rows) == planned_total else "partial",
        "development_only": True,
        "independent_worlds": 1,
        "planned_sources": planned_core,
        "planned_source_batches": 12 * planned_core,
        "planned_supplementary_sources": planned_supplement,
        "planned_actual_sources": planned_total,
        "original_planned_sources": 18,
        "not_started_scope_reduced": len(scope.get("not_started_due_to_scope_change", [])),
        "original_full_plan_completed": not scope and len(rows) == 18,
        "scope_revision": scope or None,
        "attempted_sources": len(rows),
        "attempted_core_sources": len(core_rows),
        "core_complete_chains": sum(r["status"] == "completed" for r in core_rows),
        "core_final_assays": sum(r["final_assays"] for r in core_rows),
        "core_intermediate_measurements": sum(r["intermediate_measurements"] for r in core_rows),
        "supplementary_complete_chains": sum(
            r["status"] == "completed" for r in supplementary_rows
        ),
        "complete_chains": sum(r["status"] == "completed" for r in rows),
        "final_assays": sum(r["final_assays"] for r in rows),
        "intermediate_measurements": sum(r["intermediate_measurements"] for r in rows),
        "result_status_counts": dict(Counter(r["status"] for r in rows)),
        "posttest_completions": {
            stage: sum(
                bool(r["posttests"].get(stage, {}).get("answer"))
                and not r["posttests"].get(stage, {}).get("failure")
                for r in rows
            )
            for stage in ("K1", "Q", "K2")
        },
        "corrected_retests_completed": sum(
            r["recommendation_retest"]["status"] == "completed" for r in rows
        ),
        "posttest_procedure_amendments": [
            r["cell_id"] for r in rows if r["posttest_procedure_amendment"]
        ],
        "source_replays_verified": sum(r["exact_replay"].get("verified") is True for r in rows),
        "source_rollbacks": sum(len(r["rollbacks"]) for r in rows),
        "physical_batch_accounting": {
            "core_source_final_assays": sum(r["final_assays"] for r in core_rows),
            "supplementary_source_final_assays": sum(
                r["final_assays"] for r in supplementary_rows
            ),
            "reused_engineering_final_assays": 12,
            "reused_blind_reference_final_assays": 12,
            "original_valid_block_retest_final_assays": sum(
                len(read(path).get("batches", []))
                for r in rows
                if (path := source_root / r["cell_id"] / "recommendation-retest/result.json")
                .exists()
            ),
            "corrected_retest_final_assays": sum(
                r["recommendation_retest"]["status"] == "completed" for r in rows
            ),
            "excluded_unblinded_source_final_assays": sum(
                r["final_assays"] for r in excluded_sources
            ),
            "excluded_unblinded_retest_final_assays": sum(
                r["independent_retest_batches"] for r in excluded_sources
            ),
            "note": "Replays and software regression tests are not new study batches.",
        },
        "valid_block_token_usage": {
            key: sum(r["thread_cumulative_token_usage"][key] for r in rows)
            for key in token_usage({})
        },
        "truth": truth,
        "blind_reference_range": {
            metric: {
                "n": len(truth),
                "min": min(q[metric] for q in truth.values()),
                "max": max(q[metric] for q in truth.values()),
            }
            for metric in METRICS
        },
        "retained_startup_failures": startup_failures,
        "retained_unblinded_sources": excluded_sources,
        "source_reexecutions_reason": "whole affected block after input blinding failure",
        "outcome_selected_reruns": 0,
        "blind_reference_target": "independent keyed-noise final-assay observation",
        "results": [
            {
                **{
                    k: v for k, v in row.items()
                    if k not in ("public_tool_transcript", "model_tool_transcript")
                },
                "public_tool_transcript_file": row["cell_id"] + "-tools.json",
                "model_tool_transcript_file": row["cell_id"] + "-model-tools.json",
            }
            for row in rows
        ],
    }
    write(out / "summary.json", output)
    for row in rows:
        append_cell(row, source_root, out, root, truth)
    figures(core_rows, out)
    lines = [
        "# EC 单世界：十二批自由研究、三臂与机理/预测后测",
        "",
        f"模型 GPT-5.6 Sol / medium；开发数据。原协议核心完整链 "
        f"{output['core_complete_chains']}/{planned_core}，"
        f"核心终检 {output['core_final_assays']}/{12 * planned_core}，"
        f"核心中途测量 {output['core_intermediate_measurements']}/{12 * planned_core}。"
        f"另保留补充完整链 {output['supplementary_complete_chains']}/{planned_supplement}。",
        "",
        (
            "按用户明确指令收束为1世界 × 2目标 × E先验层 × 3臂，共6场核心来源。"
            "额外已启动的2场P层来源保留为补充，其余10场未启动，不计失败。"
            "原18场计划和范围调整记录保留。"
            if scope else "1世界 × 2目标 × 3先验层 × 3臂，共18场来源。"
        ),
        "每场12批；中途测量上限12，终检另计。",
        "优化组以 EC 公开综合得分为主要目标；探索组以形成并检验机理解释为主要目标，"
        "综合得分只是辅助读出。两组资源相同、会话独立。",
        "来源结束先封存操作建议，再回答 K1 自由机理报告、Q 固定条件盲预测、K2 复盘。"
        "无强制中途机制表或固定表达式。预测题预先固定、K1 后才展示；源实验可能偶然覆盖相同条件，"
        "不得把所有题自动视为远域外推。",
        "[逐证据分析](ANALYSIS.md) · "
        "[实验说明与程序修订](../../WORK_II_EC_SOL_DUAL_GOAL_TRIAL_NOTE.md)"
        " · [机器摘要](summary.json)",
        "",
        "![逐批观察得分及截至该批的最佳观察得分](source-progress.png)",
        "",
        "## 完成情况与资源",
        "",
        f"来源精确重放 {output['source_replays_verified']}/{len(rows)}；"
        f"来源回滚 {output['source_rollbacks']} 次。"
        f"K1/Q/K2 完整回答分别为 {output['posttest_completions']['K1']}/"
        f"{output['posttest_completions']['Q']}/{output['posttest_completions']['K2']}"
        f"（含补充，各计划{planned_total}）。"
        f"按来源资源修复后的建议复测完成 "
        f"{output['corrected_retests_completed']}/{planned_total}。",
        f"实际来源共 {len(rows)}/{planned_total} 场，"
        f"终检 {output['final_assays']}/{12 * planned_total} 批，"
        f"中途测量 {output['intermediate_measurements']}/{12 * planned_total} 次。",
        (
            "未完成来源及其原失败状态保留；"
            + "、".join(output['posttest_procedure_amendments'])
            + " 的后测沿原thread单独补齐，不算原协议全链成功。"
            if output['posttest_procedure_amendments'] else ""
        ),
        f"有效块累计输入 {output['valid_block_token_usage']['input_tokens']:,} tokens，"
        f"其中缓存输入 {output['valid_block_token_usage']['cached_input_tokens']:,}；"
        f"输出 {output['valid_block_token_usage']['output_tokens']:,}。"
        "同 thread 的续接回执是累计值，已按阶段差分避免重复计数。"
        "这些数值不含历史接入失败/排除块的消耗，也不代表已核对金额账单。",
        "",
        "## 核心结果",
        "",
        "| 目标/层/臂（完整记录） | 链状态 | 终检 | 中途测量 | 最佳观察得分 | "
        "建议复测得分 | 得分预测 MAE | 产率预测 MAE |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(core_rows + supplementary_rows):
        if supplementary_rows and index == len(core_rows):
            lines += [
                "",
                "## 保留的补充结果（不计核心三臂分母）",
                "",
                "| 目标/层/臂（完整记录） | 链状态 | 终检 | 中途测量 | 最佳观察得分 | "
                "建议复测得分 | 得分预测 MAE | 产率预测 MAE |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        best = max((b["metrics"].get("score", 0) for b in row["batches"]), default=None)
        metrics = (row.get("prediction_evaluation") or {}).get("metrics", {})
        retest = row["recommendation_retest"].get("metrics") or {}
        status_label = row["status"] + (
            "（后测补齐）" if row["posttest_procedure_amendment"] else ""
        )
        lines.append(
            f"| [{row['cell_id']}]({row['cell_id']}.md) | {status_label} | "
            f"{row['final_assays']}/12 | {row['intermediate_measurements']}/12 | "
            f"{number(best)} | {number(retest.get('score'))} | "
            f"{number(metrics.get('score', {}).get('mae'))} | "
            f"{number(metrics.get('selective_product_yield', {}).get('mae'))} |"
        )
    if (out / "prediction-mae.png").exists():
        lines += ["", "![盲预测逐指标绝对误差](prediction-mae.png)", ""]
    lines += [
        "",
        "## 解释边界",
        "",
        "这是一世界、每格一次的尝试性实验，不能估计普遍成功率或三臂总体因果效应。"
        "取证、机理、预测、优化分开报告；K2 的回忆不等于当时已公开的判断，"
        "后台真值不等于 Agent 已有证据。"
        "没有新增未经校准的 LLM 机理总分。80% 区间覆盖只是 12 题上的描述性核验。",
        "预测参考是独立噪声条件下的终检读数，误差包含仪器噪声；不是对无噪声潜在状态的直接评分。",
        "精确重放核验的是保留动作序列对应的物理轨迹，不表示再次调用模型会产生相同文本。",
        f"本轮固定预测题中 {sum(q['selective_product_yield'] < 0.02 for q in truth.values())}/12 "
        "个参考产率低于0.02。产率 MAE 很低可能部分来自响应范围较窄，"
        "须结合选择性、各效率、得分与区间宽度解释，不能单凭产率误差认定掌握了世界规律。",
        "",
        "启动接入故障及修复见实验说明；失败原始目录保留。原始 provider 数据不进入 Git，"
        "本目录仅导出公开实验记录、实际问题、回答和评价。",
        "",
    ]
    lines += [
        "## 保留的接入故障与排除记录",
        "",
        f"v1–v3 共 {len(startup_failures)} 次来源启动/中断记录；"
        f"v4 共 {len(excluded_sources)} 个来源因输入泄漏整块排除，"
        f"保留终检 {sum(r['final_assays'] for r in excluded_sources)} 批。",
        "这些记录未覆盖、未伪装成新的科学样本；逐项信息见 summary.json 与实验说明。",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                k: output[k]
                for k in ("status", "attempted_sources", "complete_chains", "final_assays")
            }
        )
    )


if __name__ == "__main__":
    main()
