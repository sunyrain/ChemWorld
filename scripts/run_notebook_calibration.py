"""R53: two continuous eight-batch campaigns; no required operation explanations."""

# Chinese reader-facing text uses Chinese punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import copy
import html
import json
import os
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import run_hypothesis_notebook_pilot as base
from scripts import run_long_horizon_notebook_review as review
from scripts.run_notebook_access_pilot import usage_summary
from scripts.run_notebook_environment_pilot import append

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import CodexSubscriptionClient

BATCHES = 8
TOOL_BUDGET = 288
SECONDS = 1800
TASK = """You are conducting EIGHT physical batches as one continuing research programme
in a finite anonymous chemical simulator, in this SAME conversation. Each batch starts
from a fresh physical state with its own resources; the hidden world stays fixed and
observation noise varies. Investigate a controllable process-condition relationship
with final yield and selectivity, and test its scope. Choose recipes, measurements,
controls, repetitions and subsequent experiments yourself.

Use only public chemworld tools. No external tools, files or other agents. Public history
and original public measurement artifacts can be retrieved when useful. Media and spectra
are synthetic proxies, not verified real chemical structures. Do not invent observations
or treat a planned experiment as a performed one. Interpret results with their stated
uncertainties. No private chain-of-thought is requested.

You have 30 minutes and 288 tool requests across the whole programme; each batch allows
24 environment operation attempts including rejections. Every tool request, including
retrievals and invalid requests, uses this shared allowance. Use lab_schema for unfamiliar
operations; multiple schemas can be requested together. lab_history pages contain at most
10 events, or select exact event_ids. lab_artifact reads the original public observation
JSON. Action parameters are available in lab_history.

Complete ordinary measurements before terminate, then measure(instrument=final_assay).
After a final assay, call lab_next_batch to start a fresh batch. No interim report is
required. After all eight batches call finish_campaign with your scientific findings,
supporting observations, limitations and final recommendation. If unable to finish, use
finish_campaign to report what was completed and what remains missing. Do not claim
unperformed results. Once finish_campaign returns, stop all tools and end your response.
If transport closes, report it and stop; do not repeatedly call an unavailable server.
"""
NOTE_TASK = """
Additionally, maintain a concise versioned hypothesis notebook for HUMAN UNDERSTANDING
AND REVIEW. Before starting physical experiments, record your research question and
testable expectation or competing expectations; uncertainty is acceptable. As consequential
evidence arrives, maintain the hypotheses, interpretations, scope and next decisions you
judge important, including why an interpretation changes or is retained. Link to relevant
public observations. Keep the final notebook consistent with your final conclusions.
Use your own Markdown format. Do not copy the raw action history or write a diary for every
operation. Reading, comparing versions and restoring are your choices; note contents are
never automatically inserted into tool responses. Missing notes do not lock the laboratory.
A restore creates a new version and does not undo experiments. Length and revision count
are not rewarded. Notes are your fallible scientific statements, not authoritative facts.
"""


def laboratory_definitions(arm: str) -> list[dict]:
    definitions = copy.deepcopy(base.tool_definitions())
    definitions = [
        t
        for t in definitions
        if t["name"] not in {"finish_batch", "lab_reports"}
        and (arm == "N" or not t["name"].startswith("notebook_"))
    ]
    for t in definitions:
        if t["name"] == "lab_step":
            t["inputSchema"]["properties"].pop("reason")
            t["inputSchema"]["required"] = ["action"]
        if t["name"] == "lab_status":
            t["description"] = "Current public state, remaining resources and campaign progress."
    return definitions


def definitions(arm: str) -> list[dict]:
    result = laboratory_definitions(arm)
    for name, description, properties, required in (
        ("lab_next_batch", "After final assay, open the next fresh physical batch.", {}, []),
        (
            "finish_campaign",
            "Submit the final scientific report and end this campaign.",
            {"report": {"type": "string"}},
            ["report"],
        ),
    ):
        result.append(
            {
                "name": name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False,
                },
                "annotations": {
                    "readOnlyHint": False,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            }
        )
    return result


class CalibrationBatchHost(base.PilotHost):
    def __init__(self, root: Path, arm: str, batch: int, deadline: float):
        self.arm = arm
        super().__init__(
            root,
            batch,
            tool_budget=TOOL_BUDGET,
            deadline=deadline,
            seed=0,
            observation_seed=5000 + batch,
        )

    def definitions(self) -> list[dict]:
        return laboratory_definitions(self.arm)

    def status(self) -> dict:
        result = super().status()
        result.pop("previous_reports")
        if self.arm == "B":
            result.pop("notebook")
        return result


def has_final_assay(lab: CalibrationBatchHost) -> bool:
    return any(
        a["status"] == "committed"
        and a["action"].get("operation") == "measure"
        and a["action"].get("instrument") == "final_assay"
        for a in lab.result["actions"]
    )


class CampaignHost:
    def __init__(self, root: Path, arm: str, deadline: float):
        self.root, self.arm, self.deadline = root, arm, deadline
        self.calls, self.finished, self.completed = 0, False, 0
        self.result: dict[str, Any] = {"errors": [], "report": None, "arm": arm}
        self.lab = CalibrationBatchHost(root, arm, 1, deadline)
        self.persist()

    def status(self) -> dict:
        return {
            **self.lab.status(),
            "planned_batches": BATCHES,
            "completed_batches": self.completed + int(has_final_assay(self.lab)),
            "tool_requests_remaining": max(0, TOOL_BUDGET - self.calls),
            "seconds_remaining": max(0, round(self.deadline - time.time())),
            "later_batches_remaining": BATCHES - self.lab.batch,
        }

    def persist(self) -> None:
        self.result.update(
            batch=self.lab.batch,
            current_physical_steps=self.lab.steps,
            total_calls=self.calls,
            finished=self.finished,
            completed_batches=self.completed + int(has_final_assay(self.lab)),
            planned_batches=BATCHES,
        )
        base.save(self.root / "campaign-state.json", self.result)

    def call(self, name: str, args: dict) -> dict:
        self.calls += 1
        invocation = {
            "global_call": self.calls,
            "batch": self.lab.batch,
            "tool": name,
            "arguments": args,
            "recorded_at_unix": time.time(),
        }
        append(self.root / "campaign-requests.jsonl", invocation)
        self.persist()
        try:
            if self.finished or self.calls > TOOL_BUDGET or time.time() >= self.deadline:
                raise ValueError("campaign closed or budget exhausted")
            schema = next(
                (t["inputSchema"] for t in definitions(self.arm) if t["name"] == name), None
            )
            if schema is None:
                raise ValueError("tool unavailable in this condition")
            if args.keys() - schema["properties"].keys() or set(schema["required"]) - args.keys():
                raise ValueError("unknown or missing tool arguments")
            if name == "lab_next_batch":
                if not has_final_assay(self.lab):
                    raise ValueError(
                        "complete terminate and final_assay before starting another batch"
                    )
                if self.lab.batch >= BATCHES:
                    raise ValueError("all eight batches used; finish_campaign")
                number = self.lab.batch + 1
                self.lab.result["closed_by_next_batch"] = True
                self.lab.close()
                self.completed += 1
                self.lab = CalibrationBatchHost(self.root, self.arm, number, self.deadline)
                result = self.status()
            elif name == "finish_campaign":
                if not isinstance(args["report"], str) or not args["report"].strip():
                    raise ValueError("report must be nonempty text")
                self.result["report"] = args["report"]
                self.finished = True
                result = {
                    "finished": True,
                    "completed_batches": self.status()["completed_batches"],
                    "planned_batches": BATCHES,
                }
            else:
                result = self.lab.call(name, args)
                if name == "lab_status" and "error" not in result:
                    result = self.status()
            if "error" in result:
                self.result["errors"].append({**invocation, "result": result})
        except (ValueError, TypeError, KeyError) as error:
            result = {"error": type(error).__name__, "message": str(error)}
            self.result["errors"].append({**invocation, "result": result})
        append(self.root / "campaign-interactions.jsonl", {**invocation, "result": result})
        self.persist()
        return result

    def close(self) -> None:
        self.lab.close()
        self.persist()


def dispatch(host: CampaignHost, request: dict) -> dict | None:
    result = base.dispatch(host, request)
    if result and "result" in result:
        if request.get("method") == "tools/list":
            result["result"]["tools"] = definitions(host.arm)
        elif request.get("method") == "initialize":
            result["result"]["instructions"] = (
                "Use public laboratory tools serially. After terminate, measure final_assay. "
                "Then lab_next_batch, or finish_campaign after the last batch."
            )
    return result


def command(client, root: Path, arm: str, deadline: float) -> list[str]:
    args = base.cli_command(client, root, 1, TOOL_BUDGET, deadline)
    for i, arg in enumerate(args):
        if arg.startswith("mcp_servers.chemworld.args="):
            args[i] = "mcp_servers.chemworld.args=" + json.dumps(
                [
                    "-m",
                    "scripts.run_notebook_calibration",
                    "--serve",
                    "--output",
                    root.as_posix(),
                    "--arm",
                    arm,
                    "--deadline",
                    str(deadline),
                ]
            )
    folder = root / "provider/session-1"
    (folder / "instructions.md").write_text(
        TASK + (NOTE_TASK if arm == "N" else ""), encoding="utf-8"
    )
    (folder / "prompt.txt").write_text(
        "Conduct the eight-batch research programme. Start with lab_status.", encoding="utf-8"
    )
    base.save(folder / "command.json", args)
    return args


def run_session(client, root: Path, arm: str, completed: int, started: float) -> dict:
    deadline = time.time() + SECONDS
    args = command(client, root, arm, deadline)
    folder = root / "provider/session-1"
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
                state = base.read_json(root / "campaign-state.json", {})
                if time.time() - last >= 20:
                    elapsed = time.time() - started
                    done = completed + state.get("completed_batches", 0)
                    rate = done * 60 / elapsed
                    print(
                        json.dumps(
                            {
                                "stage": "continuous_research",
                                "arm": arm,
                                "completed": done,
                                "total": 2 * BATCHES,
                                "batch": state.get("batch", 1),
                                "calls": state.get("total_calls", 0),
                                "physical_steps": state.get("current_physical_steps", 0),
                                "elapsed_s": round(elapsed),
                                "batches_per_min": round(rate, 3),
                                "eta_min": round((2 * BATCHES - done) / rate, 1) if rate else None,
                            }
                        ),
                        flush=True,
                    )
                    last = time.time()
                if time.time() >= deadline or (
                    state.get("total_calls", 0) >= TOOL_BUDGET and not state.get("finished")
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


def summarize(root: Path, provider: dict) -> dict:
    events = base.records(root / "campaign-interactions.jsonl")
    state = base.read_json(root / "campaign-state.json", {})
    notes = review.notebook_timeline(root)
    batches = []
    for number in range(1, BATCHES + 1):
        folder = root / f"batch-{number}"
        host = base.read_json(folder / "host-summary.json", {})
        if not host:
            batches.append({"batch": number, "executed": False})
            continue
        steps = [e for e in events if e["batch"] == number and e["tool"] == "lab_step"]
        measurements = [
            e
            for e in steps
            if isinstance(e["arguments"].get("action"), dict)
            and e["arguments"]["action"].get("operation") == "measure"
            and e["result"].get("transaction_status") == "committed"
        ]
        final = next(
            (
                e["result"]
                for e in reversed(measurements)
                if e["arguments"]["action"].get("instrument") == "final_assay"
            ),
            None,
        )
        trajectory = load_jsonl(folder / "trajectory.jsonl")
        replay = verify_records(trajectory, tolerance=0).to_dict() if trajectory else None
        quality = bool(host.get("actions")) and all(
            all(q["checks"].values()) for q in host.get("quality", [])
        )
        batches.append(
            {
                "batch": number,
                "executed": True,
                "steps": host.get("steps", 0),
                "physical_requests": len(steps),
                "actions": host.get("actions", []),
                "environment_rejections": [
                    a for a in host.get("actions", []) if a["status"] != "committed"
                ],
                "quality": host.get("quality", []),
                "quality_passed": quality,
                "replay": replay,
                "host_exception": host.get("host_exception"),
                "truncated": host.get("truncated"),
                "final_observation": final.get("observation") if final else None,
                "final_assay_completed": bool(final),
                "engineering_passed": bool(
                    final
                    and quality
                    and replay
                    and replay["verified"]
                    and not host.get("truncated")
                    and not host.get("host_exception")
                ),
                "measurements": [
                    {
                        "global_call": e["global_call"],
                        "action": e["arguments"]["action"],
                        "result": e["result"],
                    }
                    for e in measurements
                ],
                "note_versions": [n["revision"] for n in notes if n["batch"] == number],
            }
        )
    stream = base.records(root / "provider/session-1/stdout.jsonl")
    public = [
        {"line": i, "item": e["item"]}
        for i, e in enumerate(stream, 1)
        if e.get("type") == "item.completed"
        and e.get("item", {}).get("type") in {"agent_message", "mcp_tool_call"}
    ]
    result = {
        "batches": batches,
        "provider": provider,
        "state": state,
        "notes": notes,
        "public_stream": public,
        "completed_batches": sum(b.get("final_assay_completed", False) for b in batches),
        "passed_batches": sum(b.get("engineering_passed", False) for b in batches),
        "tool_counts": dict(Counter(e["tool"] for e in events)),
        "errors": [e for e in events if "error" in e["result"]],
        "retrievals": [
            {k: e[k] for k in ("global_call", "batch", "tool", "arguments")}
            for e in events
            if e["tool"]
            in {"lab_history", "lab_artifact", "notebook_read", "notebook_log", "notebook_diff"}
        ],
    }
    result["shared_fault"] = bool(
        state.get("host_exception")
        or any(
            b.get("host_exception")
            or (b.get("replay") and not b["replay"]["verified"])
            or (b.get("actions") and not b.get("quality_passed"))
            for b in batches
        )
    )
    result["engineering_passed"] = bool(
        result["passed_batches"] == BATCHES
        and state.get("finished")
        and not result["shared_fault"]
        and provider.get("usage_complete")
        and provider.get("exit_code") == 0
        and not provider.get("stop_reason")
        and not provider.get("transport_failures")
    )
    base.save(root / "review-summary.json", result)
    write_arm_review(root, result, events)
    return result


def write_arm_review(root: Path, data: dict, events: list[dict]) -> None:
    lines = [
        f"# {root.name}：连续研究原始阅览",
        "",
        "以下为公开消息、工具记录和笔记原文，不补写模型未表达的假设。"
        "调用号为本研究线的全局请求序号；批末说明仅在原记录存在时展示。",
        "",
    ]
    notes = {n["revision"]: n for n in data["notes"]}
    for b in data["batches"]:
        lines += [f"## Batch {b['batch']}", ""]
        if not b["executed"]:
            lines += ["未执行。", ""]
            continue
        lines += [
            f"终检：{b['final_assay_completed']}；环境尝试：{b['steps']}；"
            f"笔记版本：{b['note_versions']}。",
            "",
        ]
        for e in (e for e in events if e["batch"] == b["batch"]):
            lines += [
                f"### call {e['global_call']} · {e['tool']}",
                "",
                "```json",
                json.dumps(e, ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        for version in b["note_versions"]:
            n = notes[version]
            lines += [f"### 笔记 v{version}（模型原文）", "", n["record"]["text"], ""]
    lines += [
        "## 最终提交报告（事后）",
        "",
        data["state"].get("report") or "未提交。",
        "",
        "## 同一 CLI 中的公开消息与调用顺序",
        "",
        "line 是 provider/session-1/stdout.jsonl 的原始行号。仅保留公开消息与工具项，"
        "不读取内部推理。公开说明出现在哪个工具结果之前/之后，可按以下顺序核查。",
        "",
    ]
    for e in data["public_stream"]:
        item = e["item"]
        if item["type"] == "agent_message":
            lines += [f"### line {e['line']} · 公开消息", "", item.get("text", ""), ""]
        else:
            lines += [
                f"- line {e['line']} · tool `{item.get('tool')}` · "
                f"id `{item.get('id')}` · arguments "
                f"`{json.dumps(item.get('arguments'), ensure_ascii=False)}`",
                "",
            ]
    (root / "review.md").write_text("\n".join(lines), encoding="utf-8")


def write_outputs(root: Path, summary: dict) -> None:
    base.save(root / "summary.json", summary)
    aggregate = {k: v for k, v in summary.items() if k != "arms"}
    aggregate["arms"] = {}
    lines = [
        "# R53：连续八批研究对照",
        "",
        "B：不额外要求同期科学说明；N：增加版本化假设笔记。两组均无强制操作理由字段、"
        "无逐批解释报告，各自同一会话连续研究。每组只有一条研究线，不能据此估计因果收益。",
        "",
        "[B 完整阅览](B/review.md) · [N 完整阅览](N/review.md)",
        "",
        "| 组 | 批 | 终检 | 环境尝试 | 产率 | 选择性 | 笔记版本 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for arm in ("B", "N"):
        data = summary["arms"].get(arm)
        if not data:
            aggregate["arms"][arm] = {"executed": False}
            lines += [f"| {arm} | {b} | 未执行 | — | — | — | — |" for b in range(1, BATCHES + 1)]
            continue
        aggregate["arms"][arm] = {
            k: data[k]
            for k in (
                "batches",
                "provider",
                "completed_batches",
                "passed_batches",
                "tool_counts",
                "retrievals",
                "engineering_passed",
                "shared_fault",
            )
        }
        aggregate["arms"][arm]["provider"] = {
            k: data["provider"].get(k)
            for k in (
                "usage",
                "usage_complete",
                "total_tokens",
                "exit_code",
                "stop_reason",
                "elapsed_s",
                "item_types",
            )
        }
        aggregate["arms"][arm]["provider"]["transport_failure_count"] = len(
            data["provider"].get("transport_failures", [])
        )
        # No source text, reports, prompts or raw provider bodies in the tracked aggregate.
        aggregate["arms"][arm]["errors"] = [
            {
                "global_call": e["global_call"],
                "batch": e["batch"],
                "tool": e["tool"],
                "error": e["result"].get("error"),
                "message": e["result"].get("message"),
            }
            for e in data["errors"]
        ]
        aggregate["arms"][arm]["notes"] = [
            {
                "revision": n["revision"],
                "batch": n["batch"],
                "call": n["call"],
                "characters": len(n["record"]["text"]),
                "unavailable_references_at_commit": n["unavailable_references_at_commit"],
            }
            for n in data["notes"]
        ]
        for b in data["batches"]:
            if not b["executed"]:
                lines.append(f"| {arm} | {b['batch']} | 未执行 | — | — | — | — |")
                continue
            obs = b.get("final_observation") or {}

            def value(key, obs=obs):
                return f"{obs[key]:.4f}" if isinstance(obs.get(key), (float, int)) else "—"

            lines.append(
                f"| {arm} | {b['batch']} | {b['final_assay_completed']} | {b['steps']} | "
                f"{value('yield')} | {value('selectivity')} | {b['note_versions']} |"
            )
    lines += [
        "",
        "## 完整资源与失败摘要",
        "",
        "```json",
        json.dumps(
            {k: v for k, v in aggregate.items() if k != "arms"}, ensure_ascii=False, indent=2
        ),
        "```",
        "",
    ]
    (root / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
    base.save(root / "aggregate.json", aggregate)
    rows = [line for line in lines if line.startswith("| ") and not line.startswith("| ---")]
    table = []
    for i, row in enumerate(rows):
        tag = "th" if i == 0 else "td"
        cells = row.strip("|").split("|")
        table.append(
            "<tr>" + "".join(f"<{tag}>{html.escape(c.strip())}</{tag}>" for c in cells) + "</tr>"
        )
    stats = html.escape(
        json.dumps(
            {k: v for k, v in aggregate.items() if k != "arms"}, ensure_ascii=False, indent=2
        )
    )
    (root / "comparison.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>R53 comparison</title>'
        "<style>body{max-width:1100px;margin:40px auto;padding:20px;font:16px/1.7 sans-serif}"
        "table{border-collapse:collapse;width:100%}th,td{padding:9px;border-bottom:1px solid #ddd;"
        "text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#205f59}</style>"
        "<h1>连续八批研究对照</h1><p>B：无额外说明要求；N：增加假设笔记职责。"
        "各组同一会话，自主选择实验；每组只有一条研究线，不作因果收益估计。</p>"
        '<a href="B/review.md">B 完整原文</a> · <a href="N/review.md">N 完整原文</a>'
        f"<table>{''.join(table)}</table><h2>资源与失败</h2><pre>{stats}</pre>",
        encoding="utf-8",
    )


def run(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=False)
    started = time.time()
    summary = {
        "formal_result": False,
        "planned_campaigns": 2,
        "planned_batches": 16,
        "completed_batches": 0,
        "total_tokens": 0,
        "failures": [],
        "arms": {},
    }
    write_outputs(root, summary)
    try:
        client = CodexSubscriptionClient(model="gpt-5.6-sol", max_attempts=1)
        for arm in ("B", "N"):
            provider = run_session(client, root / arm, arm, summary["completed_batches"], started)
            data = summarize(root / arm, provider)
            summary["arms"][arm] = data
            summary["completed_batches"] += data["completed_batches"]
            summary["total_tokens"] += provider["total_tokens"]
            if not data["engineering_passed"]:
                summary["failures"].append(
                    {
                        "arm": arm,
                        "type": "incomplete_or_failed_campaign",
                        "completed_batches": data["completed_batches"],
                    }
                )
            summary["elapsed_s"] = time.time() - started
            write_outputs(root, summary)
            print(
                json.dumps(
                    {
                        "stage": "campaign_recorded",
                        "arm": arm,
                        "completed": summary["completed_batches"],
                        "total": 16,
                        "total_tokens": summary["total_tokens"],
                        "shared_fault": data["shared_fault"],
                    }
                ),
                flush=True,
            )
            if data["shared_fault"]:
                break
    except Exception as error:
        summary["failures"].append({"type": type(error).__name__, "message": str(error)})
    finally:
        summary["elapsed_s"] = time.time() - started
        summary["engineering_passed"] = len(summary["arms"]) == 2 and all(
            a["engineering_passed"] for a in summary["arms"].values()
        )
        write_outputs(root, summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--arm", choices=("B", "N"), default="N")
    parser.add_argument("--deadline", type=float, default=0)
    options = parser.parse_args()
    if options.serve:
        base.serve_host(
            options.output,
            1,
            lambda: CampaignHost(options.output, options.arm, options.deadline),
            dispatcher=dispatch,
        )
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
