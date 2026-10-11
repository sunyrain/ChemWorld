"""Two six-batch research campaigns for human review; see the R49 experiment note."""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

from scripts import run_hypothesis_notebook_pilot as base
from scripts.run_notebook_access_pilot import usage_summary

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import CodexSubscriptionClient

GOALS = {
    "A": "Investigate a controllable process-condition relationship with final yield and "
    "selectivity, and test its scope. Choose variables, controls, repetitions and challenging "
    "conditions yourself. A higher yield alone does not establish a general relationship.",
    "B": "Investigate comparability and disagreement among public measurement readouts. "
    "Choose tests that help distinguish process-condition effects from acquisition or sampling "
    "effects. Use only available public operations; do not assume instruments measure the same "
    "quantity or that disagreement proves one is wrong. No hidden formula recovery is required.",
}
TASK = """You are conducting SIX independent physical batches in one finite anonymous chemical
simulator. This is one continuing research programme, with a new conversation per batch.
The world's physical laws and starting state are fixed across batches; measurement noise
streams differ. Each batch has its own resource ledger. Your public history and versioned
notebook persist across batches. Their bodies are available only through tools when requested.

Maintain a concise research notebook FOR A HUMAN RESEARCHER TO UNDERSTAND AND REVIEW.
Before the first physical operation of each batch, record the current question, why you
choose this experiment, and a testable expectation or competing expectations (uncertainty
is acceptable). After consequential evidence, record what changed or why the judgment is
unchanged. Before finishing the batch, leave your interpretation, exact public evidence
references, unresolved issues, and the next decision, or final synthesis in batch six.
Use ordinary Markdown; stable hypothesis labels may help. Do not copy the entire raw history.
Provide brief public scientific commitments, not private chain-of-thought. Do not backdate
a prediction, invent an observation, or describe a planned experiment as performed.
Records are for human review, not rewarded by word count or number of writes. Missing notes
do not lock the lab. Reading, comparing and restoring notes is your choice; avoid redundant
reading while relevant content remains in your current context. Restoring a note never
undoes experiments. Cite history for facts; notebook interpretations can be mistaken.

Choose the recipes, controls, repeats and measurements yourself. Only public chemworld
tools may be used. Media and spectral channels are synthetic proxies; do not claim real
chemical structures or hidden mechanisms. Interpret differences with known uncertainty,
confounds and limitations; do not invent error bars or thresholds after observing outcomes.
Each batch allows 24 physical attempts including rejections, 36 total tool requests and
300 seconds. Budget is finite; reserve enough for termination, final assay and reporting.
Use lab_schema to look up needed operations together. lab_history limit is at most 10
events; use offset or exact event_ids for additional pages. lab_artifact can select fields
including observation, processed_estimate, uncertainty or raw_signal when present; the
response lists available_fields. Tool errors are retained; correct them if needed.
Finish ordinary measurements BEFORE terminate. Then measure(instrument=final_assay).
You may save your complete updated notebook with finish_batch(notebook_text=...),
so the terminal interpretation and report can be submitted in one request. This is optional.
When describing a repeat, distinguish matching recipe/target settings from matching the
complete operation sequence, including sampling, quench and measurement settings.
Call finish_batch(report=...) with your evidence-grounded findings and limitations, then
stop all tool calls. No result is required to be positive. If unable to finish, say what
is missing. Batch six is the last batch; do not rely on extra future experiments being run.
"""


class ResearchHost(base.PilotHost):
    def __init__(self, root: Path, campaign: str, batch: int, deadline: float):
        self.campaign = campaign
        super().__init__(
            root,
            batch,
            tool_budget=36,
            deadline=deadline,
            seed=0,
            observation_seed=(1000 if campaign == "A" else 2000) + batch,
        )

    def status(self) -> dict[str, Any]:
        return {
            **super().status(),
            "campaign": self.campaign,
            "planned_batches": 6,
            "later_batches_remaining": 6 - self.batch,
        }


def serve(root: Path, campaign: str, batch: int, deadline: float) -> None:
    base.serve_host(root, batch, lambda: ResearchHost(root, campaign, batch, deadline))


def command(
    client: CodexSubscriptionClient, root: Path, campaign: str, batch: int, deadline: float
) -> list[str]:
    args = base.cli_command(client, root, batch, 36, deadline)
    for i, arg in enumerate(args):
        if arg.startswith("mcp_servers.chemworld.args="):
            args[i] = "mcp_servers.chemworld.args=" + json.dumps(
                [
                    "-m",
                    "scripts.run_long_horizon_notebook_review",
                    "--serve",
                    "--output",
                    root.as_posix(),
                    "--campaign",
                    campaign,
                    "--batch",
                    str(batch),
                    "--deadline",
                    str(deadline),
                ]
            )
    folder = root / "provider" / f"session-{batch}"
    (folder / "instructions.md").write_text(
        TASK + "\nResearch question: " + GOALS[campaign], encoding="utf-8"
    )
    (folder / "prompt.txt").write_text(
        f"Conduct batch {batch} of 6. Start with lab_status. "
        + (
            "Your research starts with empty history and notes."
            if batch == 1
            else "New conversation; earlier public facts and your notes are available on demand."
        ),
        encoding="utf-8",
    )
    base.save(folder / "command.json", args)
    return args


def notebook_timeline(root: Path) -> list[dict[str, Any]]:
    """Mechanical timing/existence only, not semantic verification or a thought transcript."""
    available: set[str] = set()
    timeline = []
    for event in base.records(root / "interactions.jsonl"):
        result = event.get("result", {})
        if "error" in result:
            continue
        if event["tool"] == "lab_step" and result.get("event_id"):
            available.add(result["event_id"])
        revision = (
            result.get("notebook", {}).get("revision")
            if event["tool"] == "finish_batch"
            else result.get("revision")
        )
        if event["tool"] in {"notebook_write", "notebook_restore", "finish_batch"} and revision:
            record = base.read_json(
                root
                / "research"
                / "experiment_documents"
                / "notebook_history"
                / f"{revision:08d}.json"
            )
            references = sorted(set(re.findall(r"batch-\d+-operation-\d{3}", record["text"])))
            timeline.append(
                {
                    "batch": event["batch"],
                    "call": event["call"],
                    "revision": revision,
                    "record": record,
                    "exact_event_references": references,
                    "unavailable_references_at_commit": sorted(set(references) - available),
                }
            )
    return timeline


def summarize_batch(root: Path, batch: int, provider: dict[str, Any]) -> dict[str, Any]:
    host = base.read_json(root / f"batch-{batch}" / "host-summary.json", {})
    path = root / f"batch-{batch}" / "trajectory.jsonl"
    trajectory = load_jsonl(path) if path.exists() else []
    replay = verify_records(trajectory, tolerance=0).to_dict() if trajectory else None
    events = [e for e in base.records(root / "interactions.jsonl") if e["batch"] == batch]
    steps = [e for e in events if e["tool"] == "lab_step" and e.get("result", {}).get("event_id")]
    notes = [n for n in notebook_timeline(root) if n["batch"] == batch]
    public_messages = [
        e["item"]["text"]
        for e in base.records(root / "provider" / f"session-{batch}" / "stdout.jsonl")
        if e.get("type") == "item.completed"
        and e.get("item", {}).get("type") == "agent_message"
        and isinstance(e["item"].get("text"), str)
    ]
    quality = bool(host.get("actions")) and all(
        all(q["checks"].values()) for q in host.get("quality", [])
    )
    result = {
        "batch": batch,
        "provider": provider,
        "host": host,
        "replay": replay,
        "quality_passed": quality,
        "pre_first_action_revisions": [
            n["revision"] for n in notes if steps and n["call"] < steps[0]["call"]
        ],
        "post_last_action_revisions": [
            n["revision"] for n in notes if steps and n["call"] > steps[-1]["call"]
        ],
        "reference_issues": [n for n in notes if n["unavailable_references_at_commit"]],
        "notes_without_physical_actions": [n["revision"] for n in notes] if not steps else [],
        "cli_last_public_message": public_messages[-1] if public_messages else None,
        "final_observation": next(
            (e["result"]["observation"] for e in reversed(steps) if e["result"].get("terminal")),
            None,
        ),
        "measurements": [
            {
                "event_id": e["result"]["event_id"],
                "action": e["arguments"]["action"],
                "observation": e["result"]["observation"],
            }
            for e in steps
            if e["arguments"]["action"].get("operation") == "measure"
        ],
        "actual_actions_and_reasons": [e["arguments"] for e in steps],
        "engineering_passed": bool(
            host.get("terminal")
            and host.get("finished")
            and not host.get("truncated")
            and quality
            and replay
            and replay.get("verified")
            and not host.get("host_exception")
            and provider.get("usage_complete")
            and provider.get("exit_code") == 0
            and not provider.get("stop_reason")
            and not provider.get("transport_failures")
        ),
    }
    base.save(root / f"batch-{batch}" / "review-summary.json", result)
    return result


def write_review(root: Path, summary: dict[str, Any]) -> None:
    base.save(root / "summary.json", summary)
    lines = [
        "# 长程研究阅览本",
        "",
        "以下表格来自实际工具记录；笔记差异和终报告为模型原文。",
        "未执行不补零，遗漏不代写，引用存在不等于主张成立。人工科学评价另见实验说明。",
        "",
    ]
    for name in GOALS:
        campaign = summary["campaigns"].get(name, {"batches": []})
        lines += [
            f"## 研究线 {name}",
            "",
            GOALS[name],
            "",
            "| 批次 | 终检 | 操作数 | 产率 | 选择性 | 事前新版本 | 事后新版本 | "
            "宿主输入错误 | 传输失败 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        found = {b["batch"]: b for b in campaign["batches"]}
        for number in range(1, 7):
            if number not in found:
                lines.append(f"| {number} | 未执行 | — | — | — | — | — | — | — |")
                continue
            b = found[number]
            obs = b["final_observation"] or {}
            lines.append(
                f"| {number} | {b['host'].get('terminal', False)} | "
                f"{b['host'].get('steps', 0)} | {obs.get('yield')} | "
                f"{obs.get('selectivity')} | {b['pre_first_action_revisions']} | "
                f"{b['post_last_action_revisions']} | {len(b['host'].get('errors', []))} | "
                f"{len(b['provider'].get('transport_failures', []))} |"
            )
        previous = ""
        notes = notebook_timeline(root / name) if (root / name).exists() else []
        for b in campaign["batches"]:
            lines += ["", f"### 批次 {b['batch']}", ""]
            if b.get("notes_without_physical_actions"):
                lines += [
                    f"本批没有物理操作；已保存笔记版本 {b['notes_without_physical_actions']}。"
                    "上表事前/事后位置没有可对应的物理动作，不表示没有写笔记。",
                    "",
                ]
            for note in [n for n in notes if n["batch"] == b["batch"]]:
                record = note["record"]
                delta = "\n".join(
                    difflib.unified_diff(
                        previous.splitlines(),
                        record["text"].splitlines(),
                        fromfile="previous",
                        tofile=f"revision-{note['revision']}",
                        lineterm="",
                    )
                )
                lines += [
                    f"笔记版本 {note['revision']}，本批第 {note['call']} 次工具调用；"
                    f"公开事件游标：{record.get('public_cursor')}。",
                    "",
                    "```diff",
                    delta,
                    "```",
                    "",
                ]
                if note["unavailable_references_at_commit"]:
                    lines += [f"提交时不存在的引用：{note['unavailable_references_at_commit']}", ""]
                previous = record["text"]
            lines += ["实际动作及当时公开理由：", ""]
            for i, action in enumerate(b["actual_actions_and_reasons"], 1):
                lines.append(
                    f"{i}. `{json.dumps(action['action'], ensure_ascii=False)}` — "
                    + action["reason"]
                )
            lines += [
                "",
                "模型终报告（原文）：",
                "",
                b["host"].get("report", "未提交"),
                "",
                "保留的工具错误：",
                "",
                "```json",
                json.dumps(b["host"].get("errors", []), ensure_ascii=False, indent=2),
                "```",
            ]
            if b.get("cli_last_public_message"):
                lines += [
                    "",
                    "CLI 最后一条公开消息（原文；不等于 finish_batch 提交成功）：",
                    "",
                    b["cli_last_public_message"],
                ]
            if b["provider"].get("transport_failures"):
                lines += ["", "传输失败（发生在宿主之外，不计入宿主输入错误）：", ""]
                for failure in b["provider"]["transport_failures"]:
                    lines.append(
                        f"- {failure.get('id')}: {failure.get('tool')} — "
                        f"{failure.get('error', {}).get('message')}"
                    )
    lines += [
        "",
        "## 资源与停止",
        "",
        "```json",
        json.dumps(
            {
                "completed": summary.get("completed_batches", 0),
                "planned": 12,
                "total_tokens": summary.get("total_tokens", 0),
                "failures": summary["failures"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
    ]
    (root / "review.md").write_text("\n".join(lines), encoding="utf-8")


def run_session(
    client: CodexSubscriptionClient,
    root: Path,
    campaign: str,
    batch: int,
    deadline: float,
    completed: int,
    block_start: float,
) -> dict[str, Any]:
    args = command(client, root, campaign, batch, deadline)
    folder = root / "provider" / f"session-{batch}"
    kwargs = (
        {"creationflags": subprocess.CREATE_NO_WINDOW}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    begin, stop_reason = time.time(), None
    with (
        (folder / "stdout.jsonl").open("w", encoding="utf-8") as stdout,
        (folder / "stderr.txt").open("w", encoding="utf-8") as stderr,
    ):
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            text=True,
            encoding="utf-8",
            **kwargs,
        )
        try:
            assert process.stdin is not None
            process.stdin.write((folder / "prompt.txt").read_text(encoding="utf-8"))
            process.stdin.close()
            last = 0.0
            while process.poll() is None:
                status = base.read_json(root / f"batch-{batch}" / "host-summary.json", {})
                if time.time() - last >= 20:
                    elapsed = time.time() - block_start
                    rate = completed * 60 / elapsed if elapsed else 0
                    print(
                        json.dumps(
                            {
                                "stage": "research",
                                "campaign": campaign,
                                "batch": batch,
                                "completed": completed,
                                "total": 12,
                                "calls": status.get("tool_calls", 0),
                                "physical_steps": status.get("steps", 0),
                                "elapsed_s": round(elapsed),
                                "batches_per_min": rate,
                                "eta_min": (12 - completed) / rate if rate else None,
                            }
                        ),
                        flush=True,
                    )
                    last = time.time()
                if time.time() >= deadline or (
                    status.get("tool_calls", 0) >= 36 and not status.get("finished")
                ):
                    stop_reason = "time_or_tool_budget"
                    base.stop_process(process)
                    break
                time.sleep(0.25)
        finally:
            if process.poll() is None:
                base.stop_process(process)
    return {
        **usage_summary(base.records(folder / "stdout.jsonl")),
        "exit_code": process.returncode,
        "stop_reason": stop_reason,
        "elapsed_s": time.time() - begin,
    }


def run(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    started = time.time()
    summary: dict[str, Any] = {
        "formal_result": False,
        "planned_campaigns": 2,
        "planned_batches": 12,
        "completed_batches": 0,
        "campaigns": {},
        "total_tokens": 0,
        "failures": [],
    }
    write_review(root, summary)
    fatal = False
    try:
        client = CodexSubscriptionClient(model="gpt-5.6-sol", max_attempts=1)
        summary["provider_configuration"] = client.pricing_snapshot()
        for name, goal in GOALS.items():
            line = summary["campaigns"][name] = {"goal": goal, "batches": [], "total_tokens": 0}
            campaign_start = time.time()
            for batch in range(1, 7):
                if time.time() - campaign_start >= 1800 or line["total_tokens"] >= 3000000:
                    summary["failures"].append(
                        {"campaign": name, "before_batch": batch, "type": "campaign_budget_stop"}
                    )
                    break
                deadline = min(campaign_start + 1800, time.time() + 300)
                provider = run_session(
                    client,
                    root / name,
                    name,
                    batch,
                    deadline,
                    summary["completed_batches"],
                    started,
                )
                result = summarize_batch(root / name, batch, provider)
                line["batches"].append(result)
                line["total_tokens"] += provider["total_tokens"]
                summary["total_tokens"] += provider["total_tokens"]
                summary["completed_batches"] += int(result["engineering_passed"])
                if not result["engineering_passed"]:
                    summary["failures"].append(
                        {"campaign": name, "batch": batch, "type": "incomplete_or_failed_batch"}
                    )
                fatal = bool(
                    not provider["usage_complete"]
                    or provider["transport_failures"]
                    or result["host"].get("host_exception")
                    or (provider["exit_code"] and not provider["stop_reason"])
                    or (result["replay"] and not result["replay"].get("verified"))
                )
                if fatal:
                    summary["failures"].append(
                        {"campaign": name, "batch": batch, "type": "provider_host_or_replay_stop"}
                    )
                write_review(root, summary)
                if fatal:
                    break
            line["elapsed_s"] = time.time() - campaign_start
            if fatal:
                break
    except Exception as error:
        summary["failures"].append({"type": type(error).__name__, "message": str(error)})
    finally:
        summary["elapsed_s"] = time.time() - started
        summary["engineering_passed"] = (
            summary["completed_batches"] == 12 and not summary["failures"]
        )
        write_review(root, summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--campaign", choices=tuple(GOALS), default="A")
    parser.add_argument("--batch", type=int, choices=range(1, 7), default=1)
    parser.add_argument("--deadline", type=float, default=0)
    options = parser.parse_args()
    if options.serve:
        serve(options.output, options.campaign, options.batch, options.deadline)
    else:
        result = run(options.output.resolve())
        print(
            json.dumps(
                {
                    k: result[k]
                    for k in (
                        "engineering_passed",
                        "completed_batches",
                        "total_tokens",
                        "elapsed_s",
                    )
                }
            ),
            flush=True,
        )
        raise SystemExit(0 if result["engineering_passed"] else 1)
