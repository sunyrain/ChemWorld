"""Bounded native-tool pilot; see development-hypothesis-notebook-20261009.md.

Each batch has one persistent CLI/MCP session. Only public tools are exposed;
the host retains the simulator, replay state and quality checks outside the agent cwd.
This development adapter does not modify the frozen Work II experiment protocol.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.run_notebook_environment_pilot import OPERATIONS, append, composition, quality

from chemworld.agent_interface import action_schema, observation_view
from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace, _atomic_write_text
from chemworld.agents.hypothesis_notebook import HYPOTHESIS_NOTEBOOK_ROLE
from chemworld.data.logging import TrajectoryLogger, load_jsonl, to_builtin
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import (
    HTTPS_PROVIDER_ID,
    CodexSubscriptionClient,
)

TASK = """You are the researcher in a finite anonymous chemical simulator. Use only the
chemworld tools and their public observations. Study whether changing one controllable
condition changes final yield across TWO independent batches of the same world.
Choose conditions and interpretations yourself. Requested usability coverage across
the two batches: mixed media, thermal processing, a configured NMR acquisition and
its readout, and both final assays. Media and spectral channels are synthetic proxies,
not real named solvents or structural identifications. Do not assume hidden laws.
Each batch allows 24 physical attempts including rejections; the whole run allows
60 tool requests and 20 minutes (10 minutes per session). Use lab_schema for unfamiliar
operations; request the needed operations together in one lab_schema call to avoid
repeated setup queries. Supply a concise public scientific reason with lab_step.
Final-assay lifecycle: finish ordinary measurements BEFORE terminate. Then call
lab_step with action {"operation":"terminate"}, followed by action
{"operation":"measure","instrument":"final_assay"}. final_assay is an instrument,
NOT an operation. No ordinary HPLC/NMR measurements after terminate.
After this batch, call finish_batch with a concise evidence-grounded report; you may
update your hypotheses first at your discretion. You can finish early if necessary,
but explain the incomplete work. Do not simulate unexecuted results in text.
After batch one, the next batch uses a fresh conversation. Your hypothesis notebook
and public history remain available through tools; neither body is preloaded.
Once finish_batch returns, make no more tool calls and end your response.
"""


def save(path: Path, data: Any) -> None:
    _atomic_write_text(path, json.dumps(to_builtin(data), ensure_ascii=False, indent=2))


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def page(items: list, offset: int = 0, limit: int = 5) -> dict[str, Any]:
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("offset must be nonnegative; limit must be 1..10 events")
    end = min(len(items), offset + limit)
    return {
        "events": items[offset:end],
        "total": len(items),
        "offset": offset,
        "next_offset": end if end < len(items) else None,
    }


def compact_public(view: dict[str, Any]) -> dict[str, Any]:
    """Filter display only; full public view remains a readable event artifact."""
    report = view["lab_report"]
    obs = view["observation"]
    # Keep missingness explicit; never present a missing value as zero.
    compact = {k: v for k, v in obs.items() if v is not None} if isinstance(obs, dict) else obs
    missing = [k for k, v in obs.items() if v is None] if isinstance(obs, dict) else []
    return {
        "observation": compact,
        "unobserved_keys": missing,
        "observed_keys": view["observed_keys"],
        "report": report["text"],
        "failure": report["failure_summary"],
        "available_operations": [
            a["operation"] for a in view["available_actions"] if a["operation"] in OPERATIONS
        ],
        "spectral_configurations": view["spectral_configurations"],
        "processed_estimate": view["processed_estimate"],
    }


def tool_definitions() -> list[dict[str, Any]]:
    string = {"type": "string"}
    integer = {"type": "integer", "minimum": 0}
    positive = {"type": "integer", "minimum": 1}
    specs = [
        ("lab_status", "Current public state and notebook metadata; no notebook body.", {}, []),
        (
            "lab_schema",
            "Exact schemas for a list of operations, in one lookup. final_assay uses measure.",
            {
                "operations": {
                    "type": "array",
                    "items": {"type": "string", "enum": sorted(OPERATIONS)},
                    "minItems": 1,
                    "maxItems": len(OPERATIONS),
                }
            },
            ["operations"],
        ),
        (
            "lab_step",
            "Execute ONE physical action. Rejections consume an attempt and are retained.",
            {"action": {"type": "object"}, "reason": string},
            ["action", "reason"],
        ),
        (
            "lab_history",
            "Read public facts across batches. No model interpretations.",
            {"offset": integer, "limit": {**positive, "maximum": 10}},
            [],
        ),
        (
            "lab_artifact",
            "Read full public observation/raw signal JSON, paginated by characters.",
            {"event_id": string, "offset": integer, "limit": {**positive, "maximum": 12000}},
            ["event_id"],
        ),
        (
            "notebook_read",
            "Read your hypothesis notebook only when needed; optionally a past revision.",
            {"revision": positive, "offset": integer, "limit": {**positive, "maximum": 32000}},
            [],
        ),
        (
            "notebook_write",
            "Commit your revisable hypotheses, evidence references and decisions. "
            "Replace whole text; not a history copy. Returns metadata only.",
            {
                "text": string,
                "message": string,
                "reviewed_through": {
                    **string,
                    "description": "Optional existing history event ID. "
                    "Omit this field before any experiment; do not send an empty string.",
                },
            },
            ["text"],
        ),
        (
            "notebook_log",
            "List retained revision metadata without text.",
            {"offset": integer, "limit": {**positive, "maximum": 100}},
            [],
        ),
        (
            "notebook_diff",
            "Compare hypothesis revisions as a paginated textual diff.",
            {
                "before": positive,
                "after": positive,
                "offset": integer,
                "limit": {**positive, "maximum": 32000},
            },
            [],
        ),
        (
            "notebook_restore",
            "Copy old hypotheses into a NEW revision; no laboratory rollback.",
            {"revision": positive, "message": string},
            ["revision"],
        ),
        (
            "finish_batch",
            "End this session after final assay, or explain an early stop.",
            {"report": string},
            ["report"],
        ),
    ]
    writes = {"lab_step", "notebook_write", "notebook_restore", "finish_batch"}
    return [
        {
            "name": name,
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": props,
                "required": required,
                "additionalProperties": False,
            },
            "annotations": {
                "readOnlyHint": name not in writes,
                "destructiveHint": False,
                "openWorldHint": False,
            },
        }
        for name, description, props, required in specs
    ]


class PilotHost:
    """One serialized MCP host owns one batch; notebook/history persist across hosts."""

    def __init__(
        self, root: Path, batch: int, *, tool_budget: int = 60, deadline: float | None = None
    ):
        self.root, self.batch = root, batch
        self.folder = root / f"batch-{batch}"
        self.folder.mkdir(parents=True, exist_ok=False)
        self.docs = ExperimentDocumentWorkspace(root / "research", versioned_notebook=True)
        self.docs.initialize()
        self.env = ChemWorldEnv(composition=composition(), seed=0)
        self.obs, self.info = self.env.reset(seed=0)
        self.logger = TrajectoryLogger(self.folder / "trajectory.jsonl")
        self.task = {**self.env.task_info(), **self.env.evaluator_provenance()}
        self.tool_budget = tool_budget
        self.deadline = deadline if deadline is not None else time.time() + 600
        self.terminal = self.truncated = self.finished = False
        self.steps = self.calls = 0
        self.result: dict[str, Any] = {
            "batch": batch,
            "actions": [],
            "quality": [],
            "errors": [],
            "tool_counts": {},
            "note_autoinjection": False,
        }
        self.persist()

    def view(self) -> dict[str, Any]:
        return observation_view(self.env, "tool_json", self.obs, self.info)

    def status(self) -> dict[str, Any]:
        return {
            "batch": self.batch,
            "physical_attempts_remaining": 24 - self.steps,
            "tool_requests_remaining": self.tool_budget - self.calls,
            "terminal": self.terminal,
            "truncated": self.truncated,
            "notebook": self.docs.manifest()["model_notebook"]["latest"],
            **compact_public(self.view()),
        }

    def persist(self) -> None:
        self.result.update(
            steps=self.steps,
            tool_calls=self.calls,
            terminal=bool(self.terminal),
            truncated=bool(self.truncated),
            finished=self.finished,
        )
        save(self.folder / "host-summary.json", self.result)

    def call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        self.calls += 1
        self.result["tool_counts"][name] = self.result["tool_counts"].get(name, 0) + 1
        invocation = {
            "batch": self.batch,
            "call": self.calls,
            "tool": name,
            "arguments": args,
            "recorded_at_unix": time.time(),
        }
        append(self.root / "tool-requests.jsonl", invocation)
        self.persist()
        try:
            if self.calls > self.tool_budget or time.time() >= self.deadline:
                raise ValueError("pilot budget exhausted; stop the session")
            if self.finished:
                raise ValueError("batch session already finished")
            schema = next((t["inputSchema"] for t in tool_definitions() if t["name"] == name), None)
            if schema is None:
                raise ValueError("unknown tool")
            if args.keys() - schema["properties"].keys() or set(schema["required"]) - args.keys():
                raise ValueError("unknown or missing tool arguments")
            result = self._call(name, args)
        except (ValueError, TypeError, KeyError) as error:
            result = {"error": type(error).__name__, "message": str(error)}
            self.result["errors"].append({"call": self.calls, "tool": name, **result})
        append(self.root / "interactions.jsonl", {**invocation, "result": result})
        self.persist()
        return result

    def _call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if name.startswith("notebook_"):
            return self.docs.notebook_tool(name.removeprefix("notebook_"), **args)
        if name == "lab_status":
            return self.status()
        if name == "lab_schema":
            operations = args["operations"]
            if not isinstance(operations, list) or not 1 <= len(operations) <= len(OPERATIONS):
                raise ValueError("operations must be a nonempty list of at most nine names")
            if any(not isinstance(op, str) or op not in OPERATIONS for op in operations):
                raise ValueError("unknown operation; final_assay is measure's instrument")
            return {op: action_schema(self.env, op) for op in operations}
        if name == "lab_history":
            return page(records(self.docs.authoritative_path), **args)
        if name == "lab_artifact":
            event_id = args["event_id"]
            # Resolve only an actual public event, never an arbitrary agent-supplied path.
            if event_id not in {e["event_id"] for e in records(self.docs.authoritative_path)}:
                raise ValueError("unknown public event")
            body = (self.root / "public-artifacts" / f"{event_id}.json").read_text(encoding="utf-8")
            offset, limit = args.get("offset", 0), args.get("limit", 8000)
            if (
                type(offset) is not int
                or offset < 0
                or type(limit) is not int
                or not 1 <= limit <= 12000
            ):
                raise ValueError("invalid artifact page")
            end = min(len(body), offset + limit)
            return {
                "text": body[offset:end],
                "offset": offset,
                "total_characters": len(body),
                "next_offset": end if end < len(body) else None,
            }
        if name == "finish_batch":
            if not isinstance(args["report"], str):
                raise ValueError("report must be text")
            self.result["report"] = args["report"]
            self.finished = True
            return {
                "finished": True,
                "final_assay_completed": bool(self.terminal),
                "truncated": bool(self.truncated),
            }
        if name != "lab_step":
            raise ValueError("unknown tool")
        action, reason = args["action"], args["reason"]
        if not isinstance(action, dict) or not isinstance(reason, str):
            raise ValueError("action must be an object and reason must be text")
        if self.terminal or self.truncated or self.steps >= 24:
            raise ValueError("physical batch closed; finish the session")
        if action.get("operation") not in OPERATIONS:
            raise ValueError("operation outside pilot; final_assay is measure's instrument")
        before = self.env._state
        revision = self.docs.manifest()["model_notebook"]["latest"]["revision"]
        self.obs, reward, self.terminal, self.truncated, self.info = self.env.step(action)
        self.steps += 1
        event_id = f"batch-{self.batch}-operation-{self.steps:03d}"
        self.logger.log(
            task_info=self.task,
            step=self.steps,
            action=action,
            observation=self.obs,
            reward=reward,
            terminated=self.terminal,
            truncated=self.truncated,
            info=self.info,
            agent_metadata={"notebook_revision": revision, "public_reason": reason},
        )
        assessment = quality(before, self.env._state, action, self.info)
        self.result["quality"].append(assessment)
        self.result["actions"].append(
            {
                "action": action,
                "status": self.info["transaction_status"],
                "event_id": event_id,
                "notebook_revision": revision,
            }
        )
        full_view = self.view()
        save(self.root / "public-artifacts" / f"{event_id}.json", full_view)
        event = {
            "event_id": event_id,
            "batch": self.batch,
            "action": action,
            "transaction_status": self.info["transaction_status"],
            "terminal": bool(self.terminal),
            "truncated": bool(self.truncated),
            "artifact_ref": event_id,
            **compact_public(full_view),
        }
        self.docs.append_operation(event)
        # Facts contain neither the model's reason nor its hypothesis notebook.
        return event

    def close(self) -> None:
        self.persist()
        self.logger.close()
        self.env.close()


def dispatch(host: PilotHost, request: dict[str, Any]) -> dict[str, Any] | None:
    request_id, method = request.get("id"), request.get("method")
    if "id" not in request:
        return None
    if method == "initialize":
        result = {
            "protocolVersion": request.get("params", {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "chemworld_hypothesis_pilot", "version": "0.1"},
            "instructions": "Use public lab tools for facts and notebook tools for your "
            "revisable hypotheses. Choose when to read or update. Final assay requires "
            "terminate followed by measure(instrument=final_assay). End with finish_batch. "
            "No more tools after finish_batch. Serial operations only.",
        }
    elif method in {"ping", "logging/setLevel"}:
        result = {}
    elif method == "tools/list":
        result = {"tools": tool_definitions()}
    elif method == "tools/call":
        params = request.get("params", {})
        if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "invalid tool params"},
            }
        value = host.call(params.get("name", ""), params.get("arguments", {}))
        result = {
            "content": [{"type": "text", "text": json.dumps(to_builtin(value))}],
            "isError": "error" in value,
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "method not found"},
        }
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def serve(root: Path, batch: int, tool_budget: int, deadline: float) -> None:
    # MCP is UTF-8 even when Windows starts the child with a legacy locale and
    # does not forward the launcher's PYTHONIOENCODING environment variable.
    sys.stdin.reconfigure(encoding="utf-8", errors="strict")
    sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    host = PilotHost(root, batch, tool_budget=tool_budget, deadline=deadline)
    try:
        for line in sys.stdin:
            response = dispatch(host, json.loads(line))
            if response is not None:
                print(json.dumps(response, ensure_ascii=False), flush=True)
    except Exception as error:
        host.result["host_exception"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        host.close()


def cli_command(client, root: Path, batch: int, tool_budget: int, deadline: float) -> list[str]:
    folder = root / "provider" / f"session-{batch}"
    folder.mkdir(parents=True, exist_ok=False)
    workspace = folder / "empty-workspace"
    workspace.mkdir()
    instructions = folder / "instructions.md"
    instructions.write_text(TASK + "\n" + HYPOTHESIS_NOTEBOOK_ROLE, encoding="utf-8")
    prompt = (
        f"Run batch {batch} of 2. Start with lab_status for the public initial state. "
        "Choose your research actions and maintain your hypotheses as described. "
        "This is a new conversation; past facts and your notebook, if any, are on demand."
    )
    (folder / "prompt.txt").write_text(prompt, encoding="utf-8")
    project = Path(__file__).resolve().parents[1]
    command = [
        client.codex_executable,
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
    ]
    for feature in ("shell_tool", "apps", "multi_agent", "plugins"):
        command += ["--disable", feature]
    settings = {
        "approval_policy": "never",
        "web_search": "disabled",
        "model_provider": HTTPS_PROVIDER_ID,
        "model_reasoning_effort": "medium",
        "model_instructions_file": instructions.as_posix(),
        "mcp_servers.chemworld.command": sys.executable,
        "mcp_servers.chemworld.args": [
            "-m",
            "scripts.run_hypothesis_notebook_pilot",
            "--serve",
            "--output",
            root.as_posix(),
            "--batch",
            str(batch),
            "--tool-budget",
            str(tool_budget),
            "--deadline",
            str(deadline),
        ],
        "mcp_servers.chemworld.cwd": project.as_posix(),
        "mcp_servers.chemworld.required": True,
        "mcp_servers.chemworld.enabled": True,
        "mcp_servers.chemworld.supports_parallel_tool_calls": False,
        "mcp_servers.chemworld.default_tools_approval_mode": "approve",
        "mcp_servers.chemworld.startup_timeout_sec": 30,
    }
    for key, value in settings.items():
        command += ["-c", f"{key}={json.dumps(value)}"]
    command += [
        "-c",
        f"model_providers.{HTTPS_PROVIDER_ID}="
        '{name="OpenAI",wire_api="responses",requires_openai_auth=true,'
        "supports_websockets=false}",
        "-m",
        client.model,
        "-C",
        str(workspace),
        "-",
    ]
    save(folder / "command.json", command)
    return command


def stop_process(process: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            check=False,
        )
    else:
        import signal

        os.killpg(process.pid, signal.SIGTERM)
    process.wait(timeout=30)


def collect(root: Path) -> dict[str, Any]:
    batches = []
    for path in sorted(root.glob("batch-*/host-summary.json")):
        batch = read_json(path)
        trajectory = load_jsonl(path.parent / "trajectory.jsonl")
        batch["replay"] = verify_records(trajectory, tolerance=0).to_dict() if trajectory else None
        batches.append(batch)
    actions = [a for b in batches for a in b["actions"]]
    committed = [a["action"] for a in actions if a["status"] == "committed"]
    coverage = {
        "mixed_media": any(
            len(
                {
                    a["action"].get("solvent")
                    for a in b["actions"]
                    if a["status"] == "committed" and a["action"]["operation"] == "add_solvent"
                }
            )
            >= 2
            for b in batches
        ),
        "thermal": any(a["operation"] == "heat" for a in committed),
        "configured_nmr": any(
            a["operation"] == "configure_instrument" and a.get("instrument") == "nmr"
            for a in committed
        ),
        "nmr_readout": any(
            a["operation"] == "measure" and a.get("instrument") == "nmr" for a in committed
        ),
    }
    docs = ExperimentDocumentWorkspace(root / "research", versioned_notebook=True)
    docs.initialize()
    return {
        "formal_result": False,
        "batches": batches,
        "batches_total": 2,
        "completed_batches": sum(b["terminal"] and not b["truncated"] for b in batches),
        "physical_attempts": len(actions),
        "committed": sum(a["status"] == "committed" for a in actions),
        "rolled_back": sum(a["status"] != "committed" for a in actions),
        "tool_counts": dict(Counter(r["tool"] for r in records(root / "tool-requests.jsonl"))),
        "coverage": coverage,
        "quality_passed": bool(actions)
        and all(all(q["checks"].values()) for b in batches for q in b["quality"]),
        "notebook_versions": docs.notebook_tool("log", limit=100),
        "note_autoinjection": False,
    }


def run(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    start, deadline = time.time(), time.time() + 1200
    provider: dict[str, Any] = {"sessions": [], "failures": [], "observed_tokens": 0}
    save(root / "provider-summary.json", provider)
    try:
        client = CodexSubscriptionClient(max_attempts=1)
        provider["configuration"] = client.pricing_snapshot()
        for batch in (1, 2):
            calls = len(records(root / "tool-requests.jsonl"))
            if calls >= 60 or time.time() >= deadline or provider["observed_tokens"] >= 300000:
                provider["failures"].append({"type": "budget_stop", "before_batch": batch})
                break
            batch_deadline = min(deadline, time.time() + 600)
            command = cli_command(client, root, batch, 60 - calls, batch_deadline)
            folder = root / "provider" / f"session-{batch}"
            kwargs = (
                {"creationflags": subprocess.CREATE_NO_WINDOW}
                if os.name == "nt"
                else {"start_new_session": True}
            )
            stop_reason = None
            with (
                (folder / "stdout.jsonl").open("w", encoding="utf-8") as stdout,
                (folder / "stderr.txt").open("w", encoding="utf-8") as stderr,
            ):
                process = subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=stdout,
                    stderr=stderr,
                    text=True,
                    encoding="utf-8",
                    **kwargs,
                )
                try:
                    process.stdin.write((folder / "prompt.txt").read_text(encoding="utf-8"))
                    process.stdin.close()
                    last_progress = 0.0
                    while process.poll() is None:
                        status = read_json(root / f"batch-{batch}" / "host-summary.json", {})
                        elapsed = time.time() - start
                        if time.time() - last_progress >= 20:
                            complete = sum(
                                read_json(p, {}).get("terminal", False)
                                for p in root.glob("batch-*/host-summary.json")
                            )
                            rate = complete * 60 / elapsed if elapsed else 0
                            print(
                                json.dumps(
                                    {
                                        "stage": "native_tool_session",
                                        "batch": batch,
                                        "completed": complete,
                                        "total": 2,
                                        "tool_calls": calls + status.get("tool_calls", 0),
                                        "physical_steps": status.get("steps", 0),
                                        "elapsed_s": round(elapsed),
                                        "batches_per_min": round(rate, 3),
                                        "eta_min": (2 - complete) / rate if rate else None,
                                    }
                                ),
                                flush=True,
                            )
                            last_progress = time.time()
                        if time.time() >= batch_deadline or (
                            calls + status.get("tool_calls", 0) >= 60 and not status.get("finished")
                        ):
                            stop_reason = "time_or_tool_budget"
                            stop_process(process)
                            break
                        time.sleep(0.25)
                finally:
                    if process.poll() is None:
                        stop_process(process)
            events = records(folder / "stdout.jsonl")
            usage_events = [
                e["usage"]
                for e in events
                if e.get("type") == "turn.completed" and isinstance(e.get("usage"), dict)
            ]
            usage = dict(Counter())
            for u in usage_events:
                for key, value in u.items():
                    if isinstance(value, (int, float)):
                        usage[key] = usage.get(key, 0) + value
            known = bool(usage_events) and all(
                "input_tokens" in u and "output_tokens" in u for u in usage_events
            )
            tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
            provider["observed_tokens"] += tokens
            session = {
                "batch": batch,
                "exit_code": process.returncode,
                "stop_reason": stop_reason,
                "usage": usage,
                "usage_complete": known,
                "mcp_completed_calls": sum(
                    e.get("type") == "item.completed"
                    and e.get("item", {}).get("type") == "mcp_tool_call"
                    for e in events
                ),
                "transport_failures": [
                    e["item"]
                    for e in events
                    if e.get("type") == "item.completed"
                    and e.get("item", {}).get("type") == "mcp_tool_call"
                    and e["item"].get("result") is None
                    and e["item"].get("error")
                ],
                "thread_ids": [
                    e.get("thread_id") for e in events if e.get("type") == "thread.started"
                ],
            }
            provider["sessions"].append(session)
            status = read_json(root / f"batch-{batch}" / "host-summary.json", {})
            if process.returncode or stop_reason or not known or session["transport_failures"]:
                provider["failures"].append({"type": "session_failure", **session})
            if not status.get("finished") or not status.get("terminal") or status.get("truncated"):
                provider["failures"].append(
                    {
                        "type": "incomplete_session",
                        "batch": batch,
                        "final_assay_completed": status.get("terminal", False),
                    }
                )
            save(root / "provider-summary.json", provider)
            if provider["failures"]:
                break
    except Exception as error:
        provider["failures"].append({"type": type(error).__name__, "message": str(error)})
    finally:
        provider["elapsed_s"] = time.time() - start
        save(root / "provider-summary.json", provider)
    summary = {**collect(root), "provider": provider}
    summary["passed"] = (
        summary["completed_batches"] == 2
        and not provider["failures"]
        and summary["quality_passed"]
        and all(summary["coverage"].values())
        and all(
            (b.get("replay") or {}).get("verified", False) and not b.get("host_exception")
            for b in summary["batches"]
        )
    )
    save(root / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--replay-only", action="store_true")
    parser.add_argument("--batch", type=int, choices=(1, 2), default=1)
    parser.add_argument("--tool-budget", type=int, default=60)
    parser.add_argument("--deadline", type=float, default=0)
    args = parser.parse_args()
    if args.serve:
        serve(args.output, args.batch, args.tool_budget, args.deadline)
    elif args.replay_only:
        result = collect(args.output)
        save(args.output / "fresh-process-replay.json", result)
        print(json.dumps({"replays": [b["replay"] for b in result["batches"]]}))
    else:
        result = run(args.output.resolve())
        print(
            json.dumps(
                {
                    k: result[k]
                    for k in ("passed", "completed_batches", "physical_attempts", "tool_counts")
                }
            ),
            flush=True,
        )
        raise SystemExit(0 if result["passed"] else 1)
