"""One bounded development pilot; see development-notebook-pilot-20261009.md."""

from __future__ import annotations

import argparse
import json
import threading
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from chemworld.agent_interface import action_schema, observation_view
from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace
from chemworld.data.logging import TrajectoryLogger, load_jsonl, to_builtin
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import CodexSubscriptionClient
from chemworld.runtime.solvent_transport import total_solvents
from chemworld.world.spectral_contract import acquisition_cost, acquisition_seconds

SYSTEM = """You are the experimental researcher in a finite anonymous chemical simulator.
Select one tool invocation per response as JSON: tool, arguments (a JSON-encoded object),
and a brief public scientific rationale. Do not give private chain-of-thought.
Use only supplied public information. Do not call external tools or inspect files.
Study whether changing a controllable condition changes final yield across two batches.
Choose the recipes and interpretations yourself. This is also a usability exercise:
include mixed media, thermal processing, at least one configured NMR measurement and
close both batches by terminate then final_assay. These are requested task coverage,
not evidence of spontaneous feature selection. The finite media and spectral channels
are synthetic proxies, not real named solvents or structural identifications.
Each batch allows 24 physical attempts, including failures. Overall allowance is 60
decisions and 20 minutes. You control notebook usage; it is optional and never scored.
After batch one, explicit conversation context is reset. Past public results and your
notebook remain available on demand. Do not assume plans were already executed.
Tools:
lab.schema {operation}: exact public action schema. Query before unfamiliar operations.
lab.status {}: public current state. lab.step {action: {...}}: ONE physical operation.
lab.next_batch {}: after the first final assay and any voluntary notes, start batch two.
lab.history {offset:0,limit:5}: public records across both batches.
lab.artifact {event_id,offset:0,limit:8000}: page of a public raw measurement JSON.
notebook.read {revision?:int,offset?:int,limit?:int}: current or past text on demand.
notebook.write {text:str,message?:str,reviewed_through?:event_id}: commit whole text;
returns metadata only. notebook.log {offset?:int,limit?:int}: versions, no text.
notebook.diff {before?:int,after?:int,offset?:int,limit?:int}: unified textual diff.
notebook.restore {revision:int,message?:str}: restore as a NEW revision; lab unchanged.
finish {report:str}: stop and report findings, evidence and remaining limitations.
Notebook content is never automatically loaded. Storage is shared only within this
two-batch research run. Only the tool responses you requested may contain note text.
Available physical operations: add_solvent, add_reagent, add_catalyst, heat, wait,
quench, configure_instrument, measure, terminate. Use schema for parameters and units.
"""
SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string"},
        "arguments": {"type": "string"},
        "rationale": {"type": "string"},
    },
    "required": ["tool", "arguments", "rationale"],
    "additionalProperties": False,
}
OPERATIONS = {
    "add_solvent",
    "add_reagent",
    "add_catalyst",
    "heat",
    "wait",
    "quench",
    "configure_instrument",
    "measure",
    "terminate",
}


def write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_builtin(data), ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def append(path: Path, data: Any) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(to_builtin(data), ensure_ascii=False, allow_nan=False) + "\n")


def composition() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-world-composition-0.1",
        "composition_id": "notebook-environment-pilot",
        "components": [
            {"kind": "reaction"},
            {"kind": "thermal"},
            {"kind": "observation", "parameters": {"instruments": ["hplc", "nmr", "final_assay"]}},
        ],
        "task": {"budget": 24, "instruments": ["hplc", "nmr", "final_assay"]},
    }


def token_count(usage: dict[str, Any]) -> int:
    """Use the provider adapter's normalized names; never add aliases twice."""
    if usage.get("total_tokens") is not None:
        return int(usage["total_tokens"])
    return int(usage.get("prompt_tokens", usage.get("input_tokens", 0))) + int(
        usage.get("completion_tokens", usage.get("output_tokens", 0))
    )


def notebook_probe(output: Path) -> dict[str, Any]:
    w = ExperimentDocumentWorkspace(output, versioned_notebook=True)
    w.initialize()
    w.append_operation({"event_id": "probe-1", "synthetic": True, "observation": 1})
    first = w.notebook_tool(
        "write", text="# Working note\nExplanation A.\n", reviewed_through="probe-1"
    )
    w.append_operation({"event_id": "probe-2", "synthetic": True, "observation": 2})
    w.notebook_tool("write", text="# Working note\nExplanation B.\n", reviewed_through="probe-2")
    facts = w.authoritative_path.read_bytes()
    delta = w.notebook_tool("diff", before=1, after=2)
    restored = w.notebook_tool("restore", revision=1)
    checks = {
        "versions_retained": w.notebook_tool("log")["total"] == 3,
        "diff": "-Explanation A." in delta["text"] and "+Explanation B." in delta["text"],
        "restore_appends": restored["revision"] == 3 and restored["restored_from"] == 1,
        "old_review_boundary": restored["reviewed_through"] == "probe-1",
        "facts_unchanged": w.authoritative_path.read_bytes() == facts,
        "restored_text": w.read_notebook() == w.read_notebook(1),
        "metadata_without_body": "Explanation A" not in json.dumps(first),
    }
    result = {"synthetic_interface_probe": True, "checks": checks, "passed": all(checks.values())}
    write(output / "probe.json", result)
    return result


def public_status(env: ChemWorldEnv, obs, info) -> dict[str, Any]:
    view = observation_view(env, "tool_json", obs, info)
    report = view["lab_report"]
    return {
        "observation": view["observation"],
        "observed_keys": view["observed_keys"],
        "report": report["text"],
        "failure": report["failure_summary"],
        "available_operations": [
            a["operation"] for a in view["available_actions"] if a["operation"] in OPERATIONS
        ],
        "spectral_configurations": view["spectral_configurations"],
        "processed_estimate": view["processed_estimate"],
    }


def quality(before, after, action, info) -> dict[str, Any]:
    a = after.solvent_accounting
    errors = [
        abs(initial + added - removed - present)
        for initial, added, removed, present in zip(
            a.initial.volumes_L,
            a.added.volumes_L,
            a.removed.volumes_L,
            total_solvents(after).volumes_L,
            strict=True,
        )
    ]
    checks = {"carrier_balance": max(errors) <= 1e-10}
    details: dict[str, Any] = {"max_carrier_error_L": max(errors)}
    if action["operation"] == "measure" and info["transaction_status"] == "committed":
        checks["measurement_clock"] = after.ledger.time_s == before.ledger.time_s
        details["sample_consumed"] = info.get("sample_consumed")
        details["analysis_seconds"] = after.ledger.analysis_time_s - before.ledger.analysis_time_s
        if action.get("instrument") == "nmr":
            config = info["raw_signal"]["settings"]
            checks["analysis_seconds"] = (
                abs(details["analysis_seconds"] - acquisition_seconds("nmr", config)) <= 1e-10
            )
            checks["measurement_cost"] = (
                abs(after.ledger.cost - before.ledger.cost - acquisition_cost("nmr", config))
                <= 1e-10
            )
            checks["sample_volume"] = (
                abs(total_solvents(before).volume_L - total_solvents(after).volume_L - 0.0003)
                <= 1e-10
            )
    return {"checks": checks, **details}


def replay(output: Path) -> dict[str, Any]:
    reports = []
    for path in sorted(output.glob("batch-*/trajectory.jsonl")):
        records = load_jsonl(path)
        reports.append(
            {
                "path": str(path),
                "operation_count": len(records),
                **verify_records(records, tolerance=0).to_dict(),
            }
            if records
            else {"path": str(path), "operation_count": 0, "verified": None}
        )
    w = ExperimentDocumentWorkspace(output / "probe", versioned_notebook=True)
    w.initialize()
    result = {
        "replays": reports,
        "probe_new_process": w.read_notebook() == w.read_notebook(1)
        and w.notebook_tool("log")["total"] == 3,
    }
    write(output / "fresh-process-replay.json", result)
    return result


def run(output: Path, client_factory=CodexSubscriptionClient) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=False)
    probe = notebook_probe(output / "probe")
    docs = ExperimentDocumentWorkspace(output / "research", versioned_notebook=True)
    docs.initialize()
    summary: dict[str, Any] = {
        "formal_result": False,
        "probe": probe,
        "batches": [],
        "failures": [],
        "provider_calls": 0,
        "tool_counts": {},
        "usage": {},
        "context_resets": 0,
        "note_autoinjection": False,
    }
    start = time.monotonic()
    done = threading.Event()
    progress = {"stage": "provider_start", "batch": 0, "lab_actions": 0, "decisions": 0}

    def heartbeat():
        while not done.wait(20):
            elapsed = time.monotonic() - start
            completed = len(summary["batches"])
            rate = completed * 60 / elapsed
            print(
                json.dumps(
                    {
                        **progress,
                        "batches_completed": completed,
                        "batches_total": 2,
                        "elapsed_s": round(elapsed),
                        "batches_per_min": rate,
                        "eta_min": (2 - completed) / rate if rate else None,
                    }
                ),
                flush=True,
            )

    threading.Thread(target=heartbeat, daemon=True).start()
    public_events: list[dict[str, Any]] = []
    artifacts: dict[str, Any] = {}
    transcript: list[dict[str, Any]] = []
    counts: Counter = Counter()
    stop = False
    try:
        client = client_factory(timeout_s=120, max_attempts=1, reasoning_effort="medium")
        summary["provider"] = client.pricing_snapshot()
        for batch in (1, 2):
            if stop:
                break
            env = ChemWorldEnv(composition=composition(), seed=0)
            obs, info = env.reset(seed=0)
            path = output / f"batch-{batch}" / "trajectory.jsonl"
            path.parent.mkdir()
            logger = TrajectoryLogger(path)
            task = {**env.task_info(), **env.evaluator_provenance()}
            steps, terminal, truncated, handoff = 0, False, False, False
            batch_result: dict[str, Any] = {
                "batch": batch,
                "quality": [],
                "actions": [],
                "terminal": False,
                "truncated": False,
            }
            if batch == 2:
                transcript = []
                summary["context_resets"] += 1
            initial = public_status(env, obs, info)
            transcript.append(
                {
                    "host": "batch_start",
                    "batch": batch,
                    "state": initial,
                    "context_reset": batch == 2,
                }
            )
            try:
                while not handoff and not truncated and not stop:
                    elapsed = time.monotonic() - start
                    usage = summary["usage"]
                    tokens = token_count(usage)
                    if summary["provider_calls"] >= 60 or elapsed >= 1200 or tokens >= 300000:
                        summary["failures"].append({"type": "budget_stop", "batch": batch})
                        stop = True
                        break
                    progress.update(
                        stage="model_decision",
                        batch=batch,
                        lab_actions=steps,
                        decisions=summary["provider_calls"],
                    )
                    call = summary["provider_calls"] + 1
                    prompt = json.dumps(
                        {
                            "batch": batch,
                            "physical_attempts_remaining": 24 - steps,
                            "decisions_remaining": 61 - call,
                            "interaction": transcript,
                        },
                        ensure_ascii=False,
                    )
                    write(
                        output / "provider" / f"{call:03d}-request.json",
                        {"system": SYSTEM, "user": json.loads(prompt), "schema": SCHEMA},
                    )
                    client.timeout_s = min(120, 1200 - elapsed)
                    summary["provider_calls"] = call
                    completion = client.complete_json(
                        system_prompt=SYSTEM,
                        user_prompt=prompt,
                        output_schema=SCHEMA,
                        max_tokens=2000,
                    )
                    write(output / "provider" / f"{call:03d}-response.json", asdict(completion))
                    for key, value in completion.usage.items():
                        if isinstance(value, (int, float)):
                            usage[key] = usage.get(key, 0) + value
                    payload = completion.payload
                    name = payload["tool"]
                    args = json.loads(payload["arguments"])
                    if not isinstance(args, dict):
                        raise ValueError("tool arguments must decode to an object")
                    counts[name] += 1
                    try:
                        if name.startswith("notebook."):
                            result = docs.notebook_tool(name.split(".", 1)[1], **args)
                        elif name == "lab.schema":
                            if args["operation"] not in OPERATIONS:
                                raise ValueError("operation is outside this pilot interface")
                            result = action_schema(env, args["operation"])
                        elif name == "lab.status":
                            result = public_status(env, obs, info)
                        elif name == "lab.history":
                            offset, limit = args.get("offset", 0), min(args.get("limit", 5), 10)
                            if offset < 0 or limit < 1:
                                raise ValueError("invalid history page")
                            result = {
                                "events": public_events[offset : offset + limit],
                                "total": len(public_events),
                                "offset": offset,
                                "next_offset": offset + limit
                                if offset + limit < len(public_events)
                                else None,
                            }
                        elif name == "lab.artifact":
                            body = json.dumps(artifacts[args["event_id"]], ensure_ascii=False)
                            offset, limit = (
                                args.get("offset", 0),
                                min(args.get("limit", 8000), 12000),
                            )
                            if offset < 0 or limit < 1:
                                raise ValueError("invalid artifact page")
                            result = {
                                "text": body[offset : offset + limit],
                                "offset": offset,
                                "total_characters": len(body),
                                "next_offset": offset + limit
                                if offset + limit < len(body)
                                else None,
                            }
                        elif name == "lab.step":
                            action = args["action"]
                            if terminal or action["operation"] not in OPERATIONS or steps >= 24:
                                raise ValueError("operation outside allowed actions/budget")
                            before = env._state
                            version = docs.manifest()["model_notebook"]["latest"]["revision"]
                            obs, reward, terminal, truncated, info = env.step(action)
                            steps += 1
                            event_id = f"batch-{batch}-operation-{steps:03d}"
                            logger.log(
                                task_info=task,
                                step=steps,
                                action=action,
                                observation=obs,
                                reward=reward,
                                terminated=terminal,
                                truncated=truncated,
                                info=info,
                                agent_metadata={
                                    "notebook_revision": version,
                                    "rationale": payload["rationale"],
                                },
                            )
                            assessment = quality(before, env._state, action, info)
                            batch_result["quality"].append(assessment)
                            batch_result["actions"].append(
                                {"action": action, "status": info["transaction_status"]}
                            )
                            result = {
                                "event_id": event_id,
                                "batch": batch,
                                "action": action,
                                "transaction_status": info["transaction_status"],
                                "terminal": terminal,
                                "truncated": truncated,
                                **public_status(env, obs, info),
                            }
                            if info.get("raw_signal"):
                                artifacts[event_id] = to_builtin(info["raw_signal"])
                                write(
                                    output / "public-artifacts" / f"{event_id}.json",
                                    artifacts[event_id],
                                )
                                result["artifact_ref"] = event_id
                            public_events.append(result)
                            docs.append_operation(result)
                            append(output / "public-events.jsonl", result)
                        elif name == "lab.next_batch":
                            if batch != 1 or not terminal:
                                raise ValueError("next_batch requires the first final assay")
                            handoff = True
                            result = {"next_batch": 2, "context_reset": True}
                        elif name == "finish":
                            summary["final_report"] = args["report"]
                            result = {"stopped": True}
                            stop = True
                        else:
                            raise ValueError("unknown tool")
                    except (ValueError, TypeError, KeyError) as error:
                        if name == "lab.step":
                            raise
                        result = {"error": type(error).__name__, "message": str(error)}
                        summary["failures"].append(
                            {
                                "type": "tool_error",
                                "call": call,
                                "tool": name,
                                "message": str(error),
                            }
                        )
                    interaction = {"request": payload, "result": result}
                    append(
                        output / "interactions.jsonl", {"call": call, "batch": batch, **interaction}
                    )
                    transcript.append(interaction)
                    print(
                        f"decision={call}/60 batch={batch}/2 actions={steps}/24 tool={name}",
                        flush=True,
                    )
                    write(output / "progress.json", {**progress, "provider_calls": call})
                batch_result.update(
                    terminal=bool(terminal),
                    truncated=bool(truncated),
                    steps=steps,
                    final_public=public_status(env, obs, info),
                )
            finally:
                logger.close()
                env.close()
                batch_result.update(steps=steps, terminal=bool(terminal), truncated=bool(truncated))
                summary["batches"].append(batch_result)
            records = load_jsonl(path)
            batch_result["replay"] = (
                verify_records(records, tolerance=0).to_dict() if records else None
            )
            if not terminal or truncated:
                stop = True
    except Exception as error:
        summary["failures"].append(
            {
                "type": type(error).__name__,
                "message": str(error),
                "attempt_records": getattr(error, "attempt_records", []),
                "usage": getattr(error, "usage", {}),
            }
        )
    finally:
        done.set()
        summary["tool_counts"] = dict(counts)
        summary["elapsed_s"] = time.monotonic() - start
        summary["notebook_versions"] = docs.notebook_tool("log", limit=100)
        summary["completed_batches"] = sum(
            b.get("terminal", False) and not b.get("truncated", False) for b in summary["batches"]
        )
        summary["operation_count"] = sum(b["steps"] for b in summary["batches"])
        summary["quality_passed"] = bool(summary["operation_count"]) and all(
            all(q["checks"].values()) for b in summary["batches"] for q in b["quality"]
        )
        actions = [
            a["action"]
            for b in summary["batches"]
            for a in b["actions"]
            if a["status"] == "committed"
        ]
        summary["coverage"] = {
            "mixed_media": any(
                len(
                    {
                        a["action"].get("solvent")
                        for a in b["actions"]
                        if a["status"] == "committed" and a["action"]["operation"] == "add_solvent"
                    }
                )
                >= 2
                for b in summary["batches"]
            ),
            "thermal": any(a["operation"] == "heat" for a in actions),
            "configured_nmr": any(
                a["operation"] == "configure_instrument" and a.get("instrument") == "nmr"
                for a in actions
            ),
            "nmr_readout": any(
                a["operation"] == "measure" and a.get("instrument") == "nmr" for a in actions
            ),
        }
        summary["rejected_operations"] = sum(
            a["status"] != "committed" for b in summary["batches"] for a in b["actions"]
        )
        summary["passed"] = (
            probe["passed"]
            and summary["completed_batches"] == 2
            and not summary["failures"]
            and summary["quality_passed"]
            and all(summary["coverage"].values())
            and all((b.get("replay") or {}).get("verified", False) for b in summary["batches"])
        )
        write(output / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-only", action="store_true")
    args = parser.parse_args()
    result = replay(args.output) if args.replay_only else run(args.output)
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "passed",
                    "completed_batches",
                    "provider_calls",
                    "operation_count",
                    "failures",
                    "probe_new_process",
                )
                if k in result
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
