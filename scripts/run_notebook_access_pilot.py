"""Three bounded continuation arms; design: development-notebook-access-20261011.md.

Reuses the development lab host. Never alters the source campaign or formal protocol.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from scripts import run_hypothesis_notebook_pilot as base

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import CodexSubscriptionClient

ARMS = ("H", "N", "C")
SOURCE = Path("D:/Projects/ChemWorld-local-research/20261009-hypothesis-notebook/attempt-02")
TASK = """You are continuing your research in a finite anonymous chemical simulator after
a conversation reset. The first independent batch has already been performed; this
is the second independent batch in the SAME world. Study whether changing one
controllable condition changes final yield. Choose your actions and interpretations.
Only public chemworld tools are available. History preserves past operations,
observations, failures and resources; retrieve information when useful. Tool use
and note length are not scored. You are not required to write or read notes.
Do not confuse plans with performed experiments. Media/spectral channels are
synthetic proxies, not named chemicals or identified structures. Give concise public
scientific reasons, not private chain-of-thought. Interpret numerical differences
with measurement uncertainty and possible confounds; do not invent error bars.
Budget: 24 physical attempts including rejections, 30 total tool requests, 300 seconds.
Use lab_schema to query unfamiliar operations together. Public artifact fields may
be selected when full raw spectra are unnecessary; original signals remain available.
Finish ordinary measurements BEFORE terminate; then measure(instrument=final_assay).
End with finish_batch(report=...) describing the comparison and limitations, then
make no further tool calls. Do not claim unexecuted results. The first batch already
covered mixed media, thermal processing and a configured NMR readout; do not repeat
coverage merely to satisfy a feature checklist.
"""
PROMPT = "Continue with batch 2. Start with lab_status for the public current state."
CUE = (
    " Before your first physical action, consider whether retrieving past evidence or "
    "existing interpretations would help; you may choose not to retrieve them."
)


def definitions(arm: str) -> list[dict[str, Any]]:
    result = [
        tool
        for tool in base.tool_definitions()
        if arm != "H" or not tool["name"].startswith("notebook_")
    ]
    if arm == "H":
        next(t for t in result if t["name"] == "finish_batch")["inputSchema"]["properties"].pop(
            "notebook_text", None
        )
    return result


class AccessHost(base.PilotHost):
    def __init__(self, root: Path, arm: str, deadline: float):
        self.arm = arm
        super().__init__(root, 2, tool_budget=30, deadline=deadline)

    def status(self) -> dict[str, Any]:
        result = super().status()
        if self.arm == "H":
            result.pop("notebook")
        return result

    def _call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if self.arm == "H" and name.startswith("notebook_"):
            raise ValueError("tool unavailable in this condition")
        if self.arm == "H" and name == "finish_batch" and "notebook_text" in args:
            raise ValueError("notebook unavailable in this condition")
        return super()._call(name, args)


def dispatch(host: AccessHost, request: dict[str, Any]) -> dict[str, Any] | None:
    response = base.dispatch(host, request)
    if response and "result" in response:
        if request.get("method") == "tools/list":
            response["result"]["tools"] = definitions(host.arm)
        elif request.get("method") == "initialize":
            response["result"]["instructions"] = (
                "Public lab access. Select tools when useful. Serial physical actions. "
                "After terminate, measure(instrument=final_assay), then finish_batch."
            )
    return response


def serve(root: Path, arm: str, deadline: float) -> None:
    base.serve_host(root, 2, lambda: AccessHost(root, arm, deadline), dispatcher=dispatch)


def prepare(source: Path, target: Path, arm: str) -> None:
    target.mkdir(parents=True, exist_ok=False)
    # Copy only public facts/artifacts and the author's notes, never provider payloads
    # or hidden evaluator state. No mutable filesystem links between branches.
    source_docs = source / "research" / "experiment_documents"
    target_docs = target / "research" / "experiment_documents"
    target_docs.mkdir(parents=True)
    shutil.copyfile(
        source_docs / "environment_authoritative_ledger.jsonl",
        target_docs / "environment_authoritative_ledger.jsonl",
    )
    if arm != "H":
        shutil.copyfile(
            source_docs / "model_owned_notebook.md", target_docs / "model_owned_notebook.md"
        )
        shutil.copytree(source_docs / "notebook_history", target_docs / "notebook_history")
    shutil.copytree(source / "public-artifacts", target / "public-artifacts")


def command(client: CodexSubscriptionClient, root: Path, arm: str, deadline: float) -> list[str]:
    args = base.cli_command(client, root, 2, 30, deadline)
    for i, arg in enumerate(args):
        if arg.startswith("mcp_servers.chemworld.args="):
            args[i] = "mcp_servers.chemworld.args=" + json.dumps(
                [
                    "-m",
                    "scripts.run_notebook_access_pilot",
                    "--serve",
                    "--output",
                    root.as_posix(),
                    "--arm",
                    arm,
                    "--deadline",
                    str(deadline),
                ]
            )
    folder = root / "provider" / "session-2"
    (folder / "instructions.md").write_text(TASK, encoding="utf-8")
    (folder / "prompt.txt").write_text(PROMPT + (CUE if arm == "C" else ""), encoding="utf-8")
    base.save(folder / "command.json", args)
    return args


def usage_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    usages = [
        e["usage"]
        for e in events
        if e.get("type") == "turn.completed" and isinstance(e.get("usage"), dict)
    ]
    totals: dict[str, int | float] = {}
    for usage in usages:
        for key, value in usage.items():
            if isinstance(value, (int, float)):
                totals[key] = totals.get(key, 0) + value
    return {
        "usage": totals,
        "usage_complete": bool(usages)
        and all("input_tokens" in u and "output_tokens" in u for u in usages),
        "total_tokens": totals.get("input_tokens", 0) + totals.get("output_tokens", 0),
        "transport_failures": [
            e["item"]
            for e in events
            if e.get("type") == "item.completed"
            and e.get("item", {}).get("type") == "mcp_tool_call"
            and e["item"].get("result") is None
            and e["item"].get("error")
        ],
        "thread_ids": [e.get("thread_id") for e in events if e.get("type") == "thread.started"],
        "item_types": sorted(
            {
                str(e.get("item", {}).get("type"))
                for e in events
                if e.get("type") == "item.completed"
            }
        ),
    }


def summarize_arm(root: Path, arm: str, provider: dict[str, Any]) -> dict[str, Any]:
    host = base.read_json(root / "batch-2" / "host-summary.json", {})
    interactions = base.records(root / "interactions.jsonl")
    trajectory = load_jsonl(root / "batch-2" / "trajectory.jsonl") if host else []
    replay = verify_records(trajectory, tolerance=0).to_dict() if trajectory else None
    first = {}
    for event in interactions:
        if "error" in event.get("result", {}):
            continue
        name = event["tool"]
        first.setdefault(name, event["call"])
        if name == "lab_step" and event["arguments"]["action"].get("operation") == "heat":
            first.setdefault("heat", event["call"])
    successful = [
        e
        for e in interactions
        if e["tool"] == "lab_step" and e.get("result", {}).get("transaction_status") == "committed"
    ]
    quality_passed = bool(host.get("actions")) and all(
        all(q["checks"].values()) for q in host.get("quality", [])
    )
    result = {
        "arm": arm,
        "provider": provider,
        "host": host,
        "replay": replay,
        "first_successful_tool_calls": first,
        "quality_passed": quality_passed,
        "committed_recipe": [e["arguments"]["action"] for e in successful],
        "final_observation": next(
            (
                e["result"]["observation"]
                for e in reversed(successful)
                if e["result"].get("terminal")
            ),
            None,
        ),
        "engineering_passed": bool(
            host.get("terminal")
            and host.get("finished")
            and not host.get("truncated")
            and quality_passed
            and replay
            and replay.get("verified")
            and not host.get("host_exception")
            and provider.get("usage_complete")
            and provider.get("exit_code") == 0
            and not provider.get("stop_reason")
            and not provider.get("transport_failures")
        ),
    }
    base.save(root / "summary.json", result)
    return result


def write_summary(root: Path, summary: dict[str, Any]) -> None:
    base.save(root / "summary.json", summary)
    rows = [
        "# Notebook access development pilot",
        "",
        "One source; three planned continuations.",
        "No population inference. Notebook call counts are not a success score.",
        "",
        "| Arm | Status | Assay | Replay | First history | First note | First action | Tokens |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    by_arm = {x["arm"]: x for x in summary["arms"]}
    for arm in ARMS:
        result = by_arm.get(arm)
        if result is None:
            rows.append(f"| {arm} | unstarted | NA | NA | NA | NA | NA | NA |")
            continue
        first, provider = result["first_successful_tool_calls"], result["provider"]
        rows.append(
            f"| {arm} | {'passed' if result['engineering_passed'] else 'failed'} | "
            f"{result['host'].get('terminal', False)} | "
            f"{(result['replay'] or {}).get('verified', False)} | "
            f"{first.get('lab_history')} | {first.get('notebook_read')} | "
            f"{first.get('lab_step')} | {provider.get('total_tokens')} |"
        )
    rows += [
        "",
        "All failures and full reports are retained in summary.json and arm directories.",
        "",
        "```json",
        json.dumps(summary["failures"], ensure_ascii=False, indent=2),
        "```",
    ]
    (root / "summary.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run(root: Path, source: Path = SOURCE) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    started = time.time()
    summary: dict[str, Any] = {
        "formal_result": False,
        "source": str(source),
        "independent_sources": 1,
        "planned_arms": list(ARMS),
        "arms": [],
        "failures": [],
        "total_tokens": 0,
    }
    write_summary(root, summary)
    try:
        source_replay = verify_records(
            load_jsonl(source / "batch-1" / "trajectory.jsonl"), tolerance=0
        ).to_dict()
        summary["source_replay"] = source_replay
        if not source_replay.get("verified"):
            raise ValueError("source trajectory does not replay on current execution surface")
        client = CodexSubscriptionClient(model="gpt-5.6-sol", max_attempts=1)
        summary["provider_configuration"] = client.pricing_snapshot()
        for arm in ARMS:
            if time.time() - started >= 900 or summary["total_tokens"] >= 900000:
                summary["failures"].append({"arm": arm, "type": "block_budget_stop"})
                break
            branch = root / arm
            prepare(source, branch, arm)
            deadline = min(started + 900, time.time() + 300)
            args = command(client, branch, arm, deadline)
            folder = branch / "provider" / "session-2"
            stop_reason = None
            begin = time.time()
            kwargs = (
                {"creationflags": subprocess.CREATE_NO_WINDOW}
                if os.name == "nt"
                else {"start_new_session": True}
            )
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
                        status = base.read_json(branch / "batch-2" / "host-summary.json", {})
                        if time.time() - last >= 20:
                            elapsed, count = time.time() - started, len(summary["arms"])
                            rate = count * 60 / elapsed if elapsed else 0
                            print(
                                json.dumps(
                                    {
                                        "stage": "continuation",
                                        "arm": arm,
                                        "completed": count,
                                        "total": 3,
                                        "calls": status.get("tool_calls", 0),
                                        "physical_steps": status.get("steps", 0),
                                        "arms_per_min": rate,
                                        "eta_min": (3 - count) / rate if rate else None,
                                    }
                                ),
                                flush=True,
                            )
                            last = time.time()
                        if time.time() >= deadline or (
                            status.get("tool_calls", 0) >= 30 and not status.get("finished")
                        ):
                            stop_reason = "time_or_tool_budget"
                            base.stop_process(process)
                            break
                        time.sleep(0.25)
                finally:
                    if process.poll() is None:
                        base.stop_process(process)
            provider = {
                **usage_summary(base.records(folder / "stdout.jsonl")),
                "exit_code": process.returncode,
                "stop_reason": stop_reason,
                "elapsed_s": time.time() - begin,
            }
            result = summarize_arm(branch, arm, provider)
            summary["arms"].append(result)
            summary["total_tokens"] += provider["total_tokens"]
            if not result["engineering_passed"]:
                summary["failures"].append({"arm": arm, "type": "incomplete_or_failed_arm"})
            write_summary(root, summary)
            if (
                not provider["usage_complete"]
                or provider["transport_failures"]
                or result["host"].get("host_exception")
                or (provider["exit_code"] and not stop_reason)
            ):
                summary["failures"].append({"arm": arm, "type": "provider_or_host_stop"})
                break
    except Exception as error:
        summary["failures"].append({"type": type(error).__name__, "message": str(error)})
    finally:
        summary["elapsed_s"] = time.time() - started
        summary["completed_arms"] = sum(a["engineering_passed"] for a in summary["arms"])
        summary["passed"] = summary["completed_arms"] == 3 and not summary["failures"]
        write_summary(root, summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--arm", choices=ARMS, default="N")
    parser.add_argument("--deadline", type=float, default=0)
    options = parser.parse_args()
    if options.serve:
        serve(options.output, options.arm, options.deadline)
    else:
        result = run(options.output.resolve(), options.source.resolve())
        print(json.dumps({k: result[k] for k in ("passed", "completed_arms", "total_tokens")}))
        raise SystemExit(0 if result["passed"] else 1)
