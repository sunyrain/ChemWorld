"""Three fixed native-model cases, authored notes and workbench-native archives (R63)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import run_hypothesis_notebook_pilot as base
from scripts.run_notebook_access_pilot import usage_summary

from chemworld.agent_interface import action_schema
from chemworld.providers.codex_subscription import CodexSubscriptionClient
from chemworld.workbench.service import ResearchStore, integer

MODEL = "gpt-5.6-sol"
CALLS, SECONDS, OPERATIONS = 40, 420, 24
UNITS = (
    ("reaction-to-assay", "Investigate yield and selectivity in one virtual reaction batch."),
    (
        "reaction-to-crystallization",
        "Investigate crystal recovery and purity in one virtual batch.",
    ),
    (
        "flow-reaction-optimization",
        "Investigate flow conversion and selectivity in one virtual batch.",
    ),
)
TASK = """You are the sole autonomous researcher in a ChemWorld VIRTUAL laboratory.
Choose the conditions, measurements and physical operations for the supplied research question.
Use only the public chemworld tools; no shell, external information, files or other agents.
Start with lab_status and obtain unfamiliar action schemas together using lab_schema.
You have ONE physical batch, 24 operation attempts, 40 total tool requests and 7 minutes.
All tools, including errors and notebook calls, share the request allowance. Do not invent evidence.
Synthetic spectra are finite simulator proxies, not verified real chemical structures.

Maintain a concise MODEL-AUTHORED scientific notebook for human review: BEFORE physical actions
write your question, testable expectation or competing expectations, intended observations and
uncertainty. Revise when consequential evidence changes or supports your interpretation. Cite
the public event IDs. After the terminal final assay, update the notebook with actual findings,
missing evidence and limitations, then submit finish_batch(report=...). Use concise Chinese
prose for the human-facing notebook and report; preserve schema names and units as given.
Do not write a per-action diary or private chain-of-thought. Choose when to read your notes;
their contents are never automatically injected. Missing notes do not lock the lab.

Perform ordinary measurements before terminate; then measure(instrument=final_assay).
Final assay closes physical operations but NOT your notebook, history or final report tools.
Leave tool allowance for a final notebook and finish_batch. If unable to complete, report
the failure and missing results honestly. If a platform failure is reported, do not attempt
further physical actions: record it and finish. After finish_batch, stop all tools.
"""


def definitions() -> list[dict[str, Any]]:
    result = []
    for name, description, properties, required in (
        (
            "lab_status",
            "Public task/state, remaining budgets and notebook metadata (no body).",
            {},
            [],
        ),
        (
            "lab_schema",
            "Exact schemas for several operations in one lookup.",
            {"operations": {"type": "array", "items": {"type": "string"}}},
            ["operations"],
        ),
        (
            "lab_step",
            "Submit a physical action. Rejections remain in history.",
            {"action": {"type": "object"}},
            ["action"],
        ),
        (
            "lab_history",
            "Read retained public events, including failures.",
            {"offset": {"type": "integer"}, "limit": {"type": "integer"}},
            [],
        ),
        (
            "lab_measurement",
            "Read the original public instrument packet.",
            {"event_id": {"type": "string"}},
            ["event_id"],
        ),
        (
            "notebook_write",
            "Write a complete new Markdown revision; never changes physical facts.",
            {"text": {"type": "string"}, "message": {"type": "string"}},
            ["text"],
        ),
        (
            "notebook_read",
            "Read your notebook on demand (optionally an earlier revision).",
            {
                "revision": {"type": "integer"},
                "offset": {"type": "integer"},
                "limit": {"type": "integer"},
            },
            [],
        ),
        ("notebook_log", "List revision metadata, without bodies.", {}, []),
        (
            "finish_batch",
            "Submit a report and end; does not fabricate a final assay.",
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
            }
        )
    return result


class Host:
    def __init__(self, root: Path, unit: int, deadline: float):
        self.root, self.unit, self.deadline = root, unit, deadline
        self.store = ResearchStore(root / "store")
        task, question = UNITS[unit - 1]
        self.run = self.store.create(
            {
                "name": f"R63 / {unit} / {task}",
                "project": "R63 formal model experiments",
                "question": question,
                "design": {"task_id": task, "seed": 7, "budget": OPERATIONS},
            }
        )
        self.run.data.update(
            status="running",
            actor=MODEL,
            provider="codex_subscription_native",
            model_calls=None,  # Underlying inference request count is not exposed by this CLI.
            model_tool_calls=0,
            model_configuration={
                "requested_model": MODEL,
                "reasoning_effort": "medium",
                "transport": "native CLI / MCP",
            },
            limits={"tool_limit": CALLS, "wall_limit_s": SECONDS},
            usage={"input_tokens": 0, "output_tokens": 0, "complete": False},
            evidence_mode="formal_limited_acceptance",
        )
        self.schemas = {
            op: action_schema(self.run.env, op)
            for op in self.run.env.unwrapped.task_info()["allowed_operations"]
        }
        self.result: dict[str, Any] = {
            "unit": unit,
            "run_id": self.run.data["id"],
            "calls": 0,
            "finished": False,
            "errors": [],
            "platform_failure": None,
        }
        self.persist()

    def persist(self) -> None:
        self.result["physical_submissions"] = self.run.data["submitted_steps"]
        self.run.persist()
        base.save(self.root / f"unit-{self.unit}/host.json", self.result)

    def status(self) -> dict[str, Any]:
        return {
            "question": self.run.data["question"],
            "task": self.run.data["task_prompt"],
            "state": self.run.data["view"],
            "physical_status": self.run.data["status"],
            "tool_requests_remaining": max(0, CALLS - self.result["calls"]),
            "seconds_remaining": max(0, round(self.deadline - time.time())),
            "notebook": self.run.notebook("model", "log", {}),
            "platform_failure": self.result["platform_failure"],
        }

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.result["calls"] += 1
        self.run.data["model_tool_calls"] = self.result["calls"]
        before = len(self.run.data["events"])
        try:
            if (
                self.result["finished"]
                or time.time() >= self.deadline
                or self.result["calls"] > CALLS
            ):
                raise ValueError("Session finished or time/tool budget exhausted; stop tools.")
            schema = next((d["inputSchema"] for d in definitions() if d["name"] == name), None)
            if (
                schema is None
                or arguments.keys() - schema["properties"].keys()
                or set(schema["required"]) - arguments.keys()
            ):
                raise ValueError("Unknown tool or invalid arguments; consult tool schema.")
            value = self._call(name, arguments)
        except (ValueError, KeyError, TypeError) as error:
            value = {"error": str(error)}
            self.result["errors"].append({"call": self.result["calls"], "tool": name, **value})
        except Exception as error:
            self.result["host_exception"] = {"type": type(error).__name__, "message": str(error)}
            self.result["platform_failure"] = "host_exception"
            self.persist()
            raise
        record = {
            "call": self.result["calls"],
            "tool": name,
            "arguments": arguments,
            "before_event_count": before,
            "result": value,
        }
        path = self.root / f"unit-{self.unit}/interactions.jsonl"
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.persist()
        return value

    def _call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if name == "lab_status":
            return self.status()
        if name == "lab_schema":
            return {op: self.schemas[op] for op in args["operations"]}
        if name == "lab_step":
            if self.result["platform_failure"]:
                raise ValueError("Platform failure: physical operations stopped; write report.")
            event = self.run.step(args["action"])
            if event["transaction_status"] == "rolled_back":
                self.result["platform_failure"] = "constitution_rollback"
                self.run.stop("failed", "Platform rollback; physical execution stopped.")
            return {k: v for k, v in event.items() if k != "series"}
        if name == "lab_history":
            offset = integer(args.get("offset", 0), "offset", 0, 240)
            limit = integer(args.get("limit", 10), "limit", 1, 10)
            events = self.run.data["events"]
            return {
                "total": len(events),
                "events": [
                    {k: v for k, v in e.items() if k != "series"}
                    for e in events[offset : offset + limit]
                ],
            }
        if name == "lab_measurement":
            event = next(
                (e for e in self.run.data["events"] if e.get("measurement") == args["event_id"]),
                None,
            )
            if event is None:
                raise ValueError("No public measurement at this event.")
            return base.read_json(self.run.root / "measurements" / (event["measurement"] + ".json"))
        if name.startswith("notebook_"):
            if len(str(args.get("text", ""))) > 16000:
                raise ValueError("Notebook maximum is 16000 characters.")
            return self.run.notebook("model", name.removeprefix("notebook_"), args)
        if name == "finish_batch":
            if not isinstance(args["report"], str) or len(args["report"]) > 16000:
                raise ValueError("Report must be text of at most 16000 characters.")
            self.run.data["model_report"] = args["report"]
            self.result["finished"] = True
            self.run.stop("stopped", "Native model report saved.")
            return {"finished": True, "final_assay_count": self.run.data["final_assay_count"]}
        raise ValueError("Unknown tool")

    def close(self) -> None:
        self.store.close()
        self.persist()


def dispatch(host: Host, request: dict[str, Any]) -> dict[str, Any] | None:
    response = base.dispatch(host, request)
    if response and "result" in response:
        if request.get("method") == "tools/list":
            response["result"]["tools"] = definitions()
        elif request.get("method") == "initialize":
            response["result"]["instructions"] = (
                "One virtual batch. Public tools only. Final assay ends physical actions, "
                "not notebook/history tools. Then write findings and finish_batch. Serial tools."
            )
    return response


def command(client: CodexSubscriptionClient, root: Path, unit: int, deadline: float) -> list[str]:
    branch = root / f"unit-{unit}"
    args = base.cli_command(client, branch, 1, CALLS, deadline)
    for i, arg in enumerate(args):
        if arg.startswith("mcp_servers.chemworld.args="):
            args[i] = "mcp_servers.chemworld.args=" + json.dumps(
                [
                    "-m",
                    "scripts.run_formal_workbench_model_notes",
                    "--serve",
                    "--output",
                    root.as_posix(),
                    "--unit",
                    str(unit),
                    "--deadline",
                    str(deadline),
                ]
            )
    folder = branch / "provider/session-1"
    (folder / "instructions.md").write_text(TASK, encoding="utf-8")
    (folder / "prompt.txt").write_text(
        "Conduct this virtual experiment autonomously, with your own scientific notebook. "
        "Start with lab_status.",
        encoding="utf-8",
    )
    base.save(folder / "command.json", args)
    return args


def run_session(client: CodexSubscriptionClient, root: Path, unit: int, started: float) -> dict:
    deadline = min(time.time() + SECONDS, started + 3 * SECONDS)
    args = command(client, root, unit, deadline)
    folder = root / f"unit-{unit}/provider/session-1"
    kwargs = (
        {"creationflags": subprocess.CREATE_NO_WINDOW}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    begin, last, stop_reason = time.time(), 0.0, None
    with (
        (folder / "stdout.jsonl").open("w", encoding="utf-8") as out,
        (folder / "stderr.txt").open("w", encoding="utf-8") as err,
    ):
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=out,
            stderr=err,
            text=True,
            encoding="utf-8",
            **kwargs,
        )
        try:
            assert process.stdin is not None
            process.stdin.write((folder / "prompt.txt").read_text(encoding="utf-8"))
            process.stdin.close()
            while process.poll() is None:
                state = base.read_json(root / f"unit-{unit}/host.json", {})
                elapsed = time.time() - started
                if time.time() - last >= 20:
                    done = unit - 1
                    rate = done * 60 / elapsed
                    print(
                        json.dumps(
                            {
                                "stage": "formal_native_model",
                                "unit": unit,
                                "completed": done,
                                "total": 3,
                                "tools": state.get("calls", 0),
                                "tool_limit": CALLS,
                                "physical_submissions": state.get("physical_submissions", 0),
                                "operation_limit": OPERATIONS,
                                "elapsed_s": round(elapsed),
                                "units_per_min": round(rate, 3),
                                "eta_min": round((3 - done) / rate, 1) if rate else None,
                            }
                        ),
                        flush=True,
                    )
                    last = time.time()
                if time.time() >= deadline or (
                    state.get("calls", 0) >= CALLS and not state.get("finished")
                ):
                    stop_reason = "time_or_tool_budget"
                    base.stop_process(process)
                    break
                time.sleep(0.25)
        finally:
            if process.poll() is None:
                base.stop_process(process)
    result = {
        **usage_summary(base.records(folder / "stdout.jsonl")),
        "exit_code": process.returncode,
        "stop_reason": stop_reason,
        "elapsed_s": time.time() - begin,
    }
    base.save(root / f"unit-{unit}/provider-summary.json", result)
    return result


def summarize(root: Path, unit: int, provider: dict) -> dict:
    host = base.read_json(root / f"unit-{unit}/host.json", {})
    result: dict[str, Any] = {
        "unit": unit,
        "task_id": UNITS[unit - 1][0],
        "status": "failed",
        "host": host,
        "provider": provider,
        "engineering_passed": False,
        "notebook_passed": False,
    }
    if not host:
        result["failure"] = "host_not_started"
        return result
    store = ResearchStore(root / "store")
    run = store.get(host["run_id"])
    run.data.update(wall_time_s=round(provider["elapsed_s"], 3))
    run.data["usage"] = {**provider["usage"], "complete": provider["usage_complete"]}
    run.persist()
    interactions = base.records(root / f"unit-{unit}/interactions.jsonl")
    revisions = run.notebook("model", "log", {"limit": 100})["revisions"]
    successful = [i for i in interactions if "error" not in i["result"]]
    writes = [i for i in successful if i["tool"] == "notebook_write"]
    final_events = [
        i + 1
        for i, e in enumerate(run.data["events"])
        if e["transaction_status"] == "committed" and e["action"].get("instrument") == "final_assay"
    ]
    try:
        replay = run.replay() if run.data["executed_steps"] else None
    except Exception as error:
        replay = {"verified": False, "error_type": type(error).__name__}
    result.update(
        run_id=host["run_id"],
        status=run.data["status"],
        final_assays=run.data["final_assay_count"],
        submissions=run.data["submitted_steps"],
        rejected=run.data["rejected_steps"],
        transaction_counts=dict(Counter(e["transaction_status"] for e in run.data["events"])),
        tool_counts=dict(Counter(i["tool"] for i in interactions)),
        notebook_versions=len(revisions),
        pre_action_note=any(i["before_event_count"] == 0 for i in writes),
        post_assay_note=bool(
            final_events and any(i["before_event_count"] >= final_events[-1] for i in writes)
        ),
        final_report=bool(run.data.get("model_report")),
        replay=replay,
        observation=run.data["view"]["observation"],
        resources=run.data["view"].get("cost_components"),
        budget=run.data["view"]["campaign_state"],
        failures=host.get("errors", []),
    )
    result["engineering_passed"] = bool(
        result["final_assays"]
        and replay
        and replay["verified"]
        and provider["usage_complete"]
        and provider["exit_code"] == 0
        and not provider["stop_reason"]
        and not provider["transport_failures"]
        and not host.get("host_exception")
        and not host.get("platform_failure")
    )
    result["notebook_passed"] = bool(
        result["pre_action_note"] and result["post_assay_note"] and result["final_report"]
    )
    review = [
        f"# Unit {unit}: {result['task_id']}",
        "",
        "Model-authored notes; not hidden reasoning.",
        "",
    ]
    for revision in reversed(revisions):
        text = run.notebook("model", "read", {"revision": revision["revision"], "limit": 32000})[
            "text"
        ]
        review += [
            f"## Revision {revision['revision']}",
            "",
            json.dumps(revision, ensure_ascii=False),
            "",
            text,
            "",
        ]
    review += ["## Model final report", "", run.data.get("model_report", "(missing)"), ""]
    (root / f"unit-{unit}/review.md").write_text("\n".join(review), encoding="utf-8")
    store.close()
    base.save(root / f"unit-{unit}/summary.json", result)
    return result


def run_block(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=False)
    project = Path(__file__).resolve().parents[1]
    # Bind the committed execution surface once; unrelated generated output is not a gate.
    paths = [
        "scripts/run_formal_workbench_model_notes.py",
        "scripts/run_hypothesis_notebook_pilot.py",
        "scripts/run_notebook_access_pilot.py",
        "src/chemworld/workbench/service.py",
        "src/chemworld/providers/codex_subscription.py",
        "uv.lock",
        "pyproject.toml",
    ]
    if subprocess.check_output(
        ["git", "diff", "HEAD", "--", "src/chemworld", "configs", *paths], cwd=project
    ):
        raise ValueError("Commit the execution surface before this formal block.")
    base.save(
        root / "source-binding.json",
        {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=project, text=True
            ).strip(),
            "entrypoint_sha256": {
                p: hashlib.sha256((project / p).read_bytes()).hexdigest() for p in paths
            },
            "runtime_resolution": (
                "Full runtime and task resources resolved by the source commit; "
                "no historical evidence input."
            ),
            "model": MODEL,
            "reasoning_effort": "medium",
            "units": UNITS,
            "tools": CALLS,
            "seconds": SECONDS,
            "operations": OPERATIONS,
        },
    )
    summary: dict[str, Any] = {
        "formal_result": True,
        "planned_units": 3,
        "units": [],
        "total_tokens": 0,
        "scope": "three-case native-model acceptance, not BYOK or causal notebook comparison",
    }
    started = time.time()
    base.save(root / "summary.json", summary)
    try:
        client = CodexSubscriptionClient(model=MODEL, max_attempts=1)
    except Exception as error:
        summary.update(
            block_stop="provider_setup_failed",
            error_type=type(error).__name__,
            unstarted_units=[1, 2, 3],
            engineering_passed=False,
            notebook_passed=False,
        )
        base.save(root / "summary.json", summary)
        return summary
    summary["provider_configuration"] = client.pricing_snapshot()
    for unit in range(1, 4):
        if summary["total_tokens"] >= 1500000 or time.time() - started >= 3 * SECONDS:
            summary["block_stop"] = "resource_threshold"
            break
        provider = run_session(client, root, unit, started)
        data = summarize(root, unit, provider)
        summary["units"].append(data)
        summary["total_tokens"] += provider["total_tokens"]
        base.save(root / "summary.json", summary)
        print(
            json.dumps(
                {
                    "stage": "unit_finished",
                    "unit": unit,
                    "total": 3,
                    "engineering_passed": data["engineering_passed"],
                    "notebook_passed": data["notebook_passed"],
                    "tokens": provider["total_tokens"],
                }
            ),
            flush=True,
        )
        if (
            data["host"].get("platform_failure")
            or data["host"].get("host_exception")
            or (data.get("replay") and not data["replay"]["verified"])
        ):
            summary["block_stop"] = "platform_failure"
            break
    summary["unstarted_units"] = list(range(len(summary["units"]) + 1, 4))
    summary["engineering_passed"] = len(summary["units"]) == 3 and all(
        u["engineering_passed"] for u in summary["units"]
    )
    summary["notebook_passed"] = len(summary["units"]) == 3 and all(
        u["notebook_passed"] for u in summary["units"]
    )
    summary["elapsed_s"] = time.time() - started
    base.save(root / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--unit", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--deadline", type=float, default=0)
    args = parser.parse_args()
    if args.serve:
        base.serve_host(
            args.output,
            args.unit,
            lambda: Host(args.output, args.unit, args.deadline),
            dispatcher=dispatch,
        )
        return 0
    result = run_block(args.output)
    return 0 if result["engineering_passed"] and result["notebook_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
