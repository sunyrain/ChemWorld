"""Sequential, fixed Kimi/Qwen transport comparison and conditional development calibration."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
import time
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path

from chemworld.providers.responses_chat_bridge import ResponsesChatBridge

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_work_ii_glm_bridge import calibrate, smoke, write  # noqa: E402
from scripts.probe_work_ii_siliconflow_glm import request  # noqa: E402

CANDIDATES = (
    ("kimi", "Pro/moonshotai/Kimi-K2.6"),
    ("qwen", "Qwen/Qwen3.5-397B-A17B"),
)
MODES = ("json_schema", "prompt_schema")
NOTE = "workstreams/flagship_tasks/WORK_II_PROVIDER_SELECTION_NOTE.md"


def direct_probes(key: str, model: str, root: Path) -> list[dict]:
    root.mkdir(parents=True)
    rows = []

    def probe(name: str, endpoint: str, body: dict) -> tuple[dict, dict]:
        write(root / (name + "-request.json"), body)
        record, payload = request(key, endpoint, body, root / (name + "-response.json"))
        record.update(check=name, status="failed", passed=False)
        rows.append(record)
        return record, payload if isinstance(payload, dict) else {}

    record, payload = probe(
        "native_responses",
        "/responses",
        {
            "model": model,
            "input": "Reply exactly OK.",
            "max_output_tokens": 1024,
        },
    )
    content = "".join(
        p.get("text", "")
        for item in payload.get("output", [])
        for p in item.get("content", [])
        if p.get("type") == "output_text"
    )
    record["passed"] = (
        record.get("http_status") == 200
        and payload.get("object") == "response"
        and payload.get("status") == "completed"
        and content.strip() == "OK"
    )
    record["status"] = "passed" if record["passed"] else "failed"
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Calculate the public expression 19+23.",
                "parameters": {
                    "type": "object",
                    "properties": {"expression": {"type": "string"}},
                    "required": ["expression"],
                    "additionalProperties": False,
                },
            },
        }
    ]
    messages = [
        {
            "role": "user",
            "content": (
                "Use calculate to evaluate 19+23. After the tool returns, reply exactly 42."
            ),
        }
    ]
    body = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "max_tokens": 1024,
        "stream": False,
    }
    record, payload = probe(
        "chat_tool_call",
        "/chat/completions",
        {
            **body,
            "tool_choice": {"type": "function", "function": {"name": "calculate"}},
        },
    )
    message = (payload.get("choices") or [{}])[0].get("message", {})
    calls = message.get("tool_calls") or []
    arguments = None
    if len(calls) == 1:
        with suppress(ValueError, TypeError):
            arguments = json.loads(calls[0].get("function", {}).get("arguments", ""))
    record["passed"] = bool(
        record.get("http_status") == 200
        and len(calls) == 1
        and calls[0].get("id")
        and calls[0].get("function", {}).get("name") == "calculate"
        and arguments == {"expression": "19+23"}
    )
    record["status"] = "passed" if record["passed"] else "failed"
    if record["passed"]:
        messages.extend(
            [message, {"role": "tool", "tool_call_id": calls[0]["id"], "content": "42"}]
        )
        record, payload = probe(
            "chat_tool_return",
            "/chat/completions",
            {
                **body,
                "tool_choice": "none",
            },
        )
        answer = (payload.get("choices") or [{}])[0].get("message", {}).get("content")
        record["passed"] = record.get("http_status") == 200 and str(answer).strip() == "42"
        record["status"] = "passed" if record["passed"] else "failed"
    else:
        rows.append(
            {
                "check": "chat_tool_return",
                "status": "unstarted",
                "passed": False,
                "usage": None,
                "reason": "initial_tool_call_did_not_pass",
            }
        )
    write(root / "summary.json", rows)
    return rows


def select_candidate(rows: list[dict]) -> dict | None:
    for label, model in CANDIDATES:
        for mode in MODES:
            if any(
                r["model"] == model and r["schema_mode"] == mode and r["status"] == "passed"
                for r in rows
            ):
                return {"label": label, "model": model, "schema_mode": mode}
    return None


def project_smoke(result: dict) -> dict:
    """Allowlist metadata; model messages and reasoning remain in ignored raw artifacts."""
    receipts = [r["receipt"] for r in result["results"]]
    return {
        "status": "passed" if result["passed"] else "failed",
        "scheduled_turns": 2,
        "attempted_turns": len(receipts),
        "valid_answer_turns": sum(r["passed"] for r in result["results"]),
        "mcp_calls": len(result["tool_audit"]),
        "mcp_values": [r.get("value") for r in result["tool_audit"]],
        "thread_count": len({r["thread_id"] for r in receipts if r.get("thread_id")}),
        "failures": [r["failure"] for r in receipts if r.get("failure")],
        "bridge_requests": result["bridge_requests"],
        "wall_seconds": result["wall_seconds"],
    }


def run_block(key: str, root: Path) -> dict:
    started = time.monotonic()
    report = {
        "schema_version": "chemworld-provider-selection-development-1",
        "formal_result": False,
        "experiment_note": NOTE,
        "candidates": [m for _, m in CANDIDATES],
        "codex_version": subprocess.check_output(
            [shutil.which("codex") or "codex", "--version"], text=True
        ).strip(),
        "direct_scheduled": 6,
        "direct": [],
        "harness_scheduled_sessions": 4,
        "harness_scheduled_turns": 8,
        "harness": [],
        "selected": None,
        "third_model_adopted": False,
        "formal_scientific_sessions": 0,
        "calibration": {
            "scheduled_sessions": 6,
            "attempted_sessions": 0,
            "completed_sessions": 0,
            "unstarted_sessions": 6,
            "scheduled_turns": 12,
            "attempted_turns": 0,
            "results": [],
            "bridge_requests": [],
        },
    }

    def progress(stage: str) -> None:
        elapsed = time.monotonic() - started
        completed = len(report["harness"])
        write(root / "partial.json", report)
        print(
            json.dumps(
                {
                    "stage": stage,
                    "direct_completed": len(report["direct"]),
                    "direct_total": 6,
                    "harness_completed": completed,
                    "harness_total": 4,
                    "elapsed_seconds": round(elapsed, 2),
                    "harness_sessions_per_hour": completed * 3600 / elapsed if completed else None,
                    "harness_eta_seconds": elapsed / completed * (4 - completed)
                    if completed
                    else None,
                }
            ),
            flush=True,
        )

    for label, model in CANDIDATES:
        progress(label + ":direct")
        report["direct"].extend(
            {"model": model, **r} for r in direct_probes(key, model, root / label / "direct")
        )
        for mode in MODES:
            progress(label + ":" + mode)
            directory = root / label / mode
            directory.mkdir(parents=True)
            start = time.monotonic()
            with ResponsesChatBridge(
                api_key=key,
                audit_dir=directory / "bridge",
                model=model,
                schema_mode=mode,
                max_requests=12,
            ) as bridge:
                result = smoke(directory, bridge)
                result.update(
                    model=model,
                    schema_mode=mode,
                    bridge_requests=bridge.records,
                    wall_seconds=time.monotonic() - start,
                )
                write(directory / "summary.json", result)
            report["harness"].append({"model": model, "schema_mode": mode, **project_smoke(result)})
            progress(label + ":" + mode + ":finished")
            if any(
                r.get("error_code")
                in {
                    "unsupported_input",
                    "unsupported_tool",
                    "unsupported_content",
                    "tool_name_collision",
                    "unknown_item",
                    "model_mismatch",
                }
                for r in bridge.records
            ):
                report["stop_reason"] = "shared_platform_defect"
                report["wall_seconds"] = time.monotonic() - started
                return report
    selected = report["selected"] = select_candidate(report["harness"])
    if selected:
        directory = root / "calibration"
        directory.mkdir()
        progress("calibration:" + selected["label"])
        with ResponsesChatBridge(
            api_key=key,
            audit_dir=directory / "bridge",
            model=selected["model"],
            schema_mode=selected["schema_mode"],
            max_requests=48,
        ) as bridge:
            start = time.monotonic()
            calibration = calibrate(directory, bridge, model_label=selected["label"])
            calibration.update(
                model=selected["model"],
                schema_mode=selected["schema_mode"],
                bridge_requests=bridge.records,
                wall_seconds=time.monotonic() - start,
            )
            write(directory / "summary.json", calibration)
        report["third_model_adopted"] = calibration["passed"]
        report["calibration"] = {
            **{k: v for k, v in calibration.items() if k != "results"},
            "scheduled_turns": 12,
            "attempted_turns": sum(len(r["receipts"]) for r in calibration["results"]),
            "results": [
                {
                    k: row[k]
                    for k in ("cell_id", "model", "arm", "tool", "status", "elapsed_s", "score")
                }
                | {"failure": row.get("failure"), "mcp_calls": len(row["tool_audit"])}
                for row in calibration["results"]
            ],
        }
    report["wall_seconds"] = time.monotonic() - started
    return report


def summarize(report: dict) -> str:
    lines = [
        "# Kimi / Qwen transport and development qualification",
        "",
        f"Development evidence. Codex: {report['codex_version']}.",
        "",
        "| Model | Check | Status | Actual MCP calls | Seconds |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in report["direct"]:
        seconds = f"{row['wall_seconds']:.2f}" if row.get("wall_seconds") is not None else "--"
        lines.append(f"| {row['model']} | {row['check']} | {row['status']} | n/a | {seconds} |")
    for row in report["harness"]:
        lines.append(
            f"| {row['model']} | Codex {row['schema_mode']} | {row['status']} | "
            f"{row['mcp_calls']} | {row['wall_seconds']:.2f} |"
        )
    block = report["calibration"]
    lines.extend(
        [
            "",
            f"Selected candidate: `{report['selected']}`.",
            f"Third model adopted (development-qualified): **{report['third_model_adopted']}**.",
            f"Calibration: {block['completed_sessions']}/6 completed; "
            f"{sum(r['status'] == 'failed' for r in block['results'])} failed; "
            f"{sum(r['status'] == 'interrupted' for r in block['results'])} interrupted; "
            f"{block['unstarted_sessions']} unstarted. "
            f"Attempted turns: {block['attempted_turns']}/12.",
            "",
            "Selection follows the fixed Kimi then Qwen order, using protocol checks only.",
            "Native API probes use forced tool selection; real Codex sessions use auto selection.",
            "prompt_schema omits upstream response_format and validates answers on the host; "
            "it is not server-enforced strict decoding.",
            "Provider-default reasoning is not equated to Codex medium effort. "
            "Output-item SSE events are emitted after buffering upstream output.",
            "Failures and missing usage are retained in the paired JSON. "
            "No existing formal evidence or scientific denominators are replaced.",
            "",
            "[Design and stopping rules](../WORK_II_PROVIDER_SELECTION_NOTE.md)",
            "",
        ]
    )
    if report.get("platform_incident"):
        lines.extend(
            [
                "## Platform interruption",
                "",
                *[f"- {item}" for item in report["platform_incident"]["findings"]],
                "",
            ]
        )
    resource = resource_summary(report)
    lines.extend(
        [
            "## Reported resources",
            "",
            f"Direct API opportunities: {resource['direct_attempted']}/6 attempted, "
            f"{6 - resource['direct_attempted']} unstarted. "
            f"Codex smoke turns: {resource['smoke_turns_attempted']}/8 attempted.",
            f"Known input tokens: {resource['reported_input_tokens']:,}; "
            f"known output tokens: {resource['reported_output_tokens']:,}; "
            f"requests without usage: {resource['requests_without_usage']}.",
            "These token totals cover reported usage only; "
            "interrupted provider work has unknown cost.",
            "Six-session throughput and formal-session ETA remain unknown "
            "until calibration completes.",
            "",
        ]
    )
    return "\n".join(lines)


def resource_summary(report: dict) -> dict:
    direct = [r for r in report["direct"] if r["status"] != "unstarted"]
    records = direct + [r for h in report["harness"] for r in h["bridge_requests"]]
    records += report["calibration"].get("bridge_requests", [])
    usage = [r["usage"] for r in records if r.get("usage") is not None]
    return {
        "direct_attempted": len(direct),
        "direct_passed": sum(r["status"] == "passed" for r in direct),
        "direct_failed": sum(r["status"] == "failed" for r in direct),
        "smoke_turns_attempted": sum(r["attempted_turns"] for r in report["harness"]),
        "harness_sessions_passed": sum(r["status"] == "passed" for r in report["harness"]),
        "recorded_requests": len(records),
        "requests_without_usage": sum(r.get("usage") is None for r in records),
        "reported_input_tokens": sum(u["prompt_tokens"] for u in usage),
        "reported_output_tokens": sum(u["completion_tokens"] for u in usage),
        "reported_reasoning_tokens": sum(
            u.get("completion_tokens_details", {}).get("reasoning_tokens", 0) for u in usage
        ),
        "calibration_session_eta_seconds": None,
        "formal_60_session_eta_seconds": None,
    }


def recover_interrupted(root: Path) -> dict:
    """Read durable artifacts after a stopped process; never invent completed receipts."""
    if (root / "summary.json").exists():
        raise FileExistsError("A completed summary already exists; do not replace it")
    report = json.loads((root / "partial.json").read_text(encoding="utf-8"))
    cal_root = root / "calibration"
    cells = json.loads((cal_root / "inputs.json").read_text(encoding="utf-8"))["cells"]
    rows, attempted, attempted_turns = [], 0, 0
    for index, cell in enumerate(cells, 1):
        directory = cal_root / f"session-{index}"
        completed = directory / "result.json"
        stage_count = sum(
            (directory / stage / "stdout.jsonl").exists() for stage in ("pre", "post")
        )
        row = {k: cell[k] for k in ("cell_id", "model", "arm", "tool")}
        if completed.exists():
            original = json.loads(completed.read_text(encoding="utf-8"))
            row.update({k: original[k] for k in ("status", "elapsed_s", "score")})
            row["failure"] = original.get("failure")
        elif stage_count:
            row.update(
                status="interrupted",
                failure="platform_process_tree_stopped",
                elapsed_s=None,
                score=None,
            )
        else:
            row.update(status="unstarted", failure=None, elapsed_s=None, score=None)
        row["attempted_turns"] = stage_count
        attempted += bool(stage_count)
        attempted_turns += stage_count
        rows.append(row)
    ledger = cal_root / "bridge/ledger.json"
    records = json.loads(ledger.read_text(encoding="utf-8")) if ledger.exists() else []
    by_request = {r["request"]: r for r in records}
    for path in sorted((cal_root / "bridge").glob("*-responses-request.json")):
        index = int(path.name.split("-")[0])
        if index not in by_request or by_request[index]["status"] == "started":
            by_request[index] = {
                **by_request.get(index, {}),
                "request": index,
                "status": "interrupted_unfinalized",
                "usage": by_request.get(index, {}).get("usage"),
                "error_code": "upstream_outcome_unknown_after_platform_stop",
            }
    completed_count = sum(r["status"] == "completed" for r in rows)
    report["calibration"] = {
        "status": "stopped_platform_defect",
        "scheduled_sessions": 6,
        "attempted_sessions": attempted,
        "completed_sessions": completed_count,
        "unstarted_sessions": 6 - attempted,
        "scheduled_turns": 12,
        "attempted_turns": attempted_turns,
        "results": rows,
        "bridge_requests": [by_request[k] for k in sorted(by_request)],
        "wall_seconds": None,
    }
    report.update(
        third_model_adopted=False, stop_reason="shared_platform_defect", wall_seconds=None
    )
    report["platform_incident"] = {
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "reconstructed_from_existing_artifacts": True,
        **json.loads((root / "platform_stop.json").read_text(encoding="utf-8")),
    }
    report["resource_accounting"] = resource_summary(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("run", "report", "recover-interrupted"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--key-stdin", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.stage == "recover-interrupted":
        write(root / "summary.json", recover_interrupted(root))
        print("Recovered terminal metadata; no provider calls or result replacement")
    elif args.stage == "run":
        root.mkdir(parents=True, exist_ok=False)
        key = (
            getpass.getpass("SiliconFlow API key: ")
            if args.key_stdin
            else os.environ.get("SILICONFLOW_API_KEY", "")
        )
        if not key:
            parser.error("Provide a key via environment or a non-echo terminal")
        report = run_block(key, root)
        report["resource_accounting"] = resource_summary(report)
        write(root / "summary.json", report)
        print(
            json.dumps(
                {
                    "finished": True,
                    "selected": report["selected"],
                    "adopted": report["third_model_adopted"],
                }
            ),
            flush=True,
        )
    else:
        if not args.output:
            parser.error("report requires --output (path stem)")
        report = json.loads((root / "summary.json").read_text(encoding="utf-8"))
        write(args.output.with_suffix(".json"), report)
        args.output.with_suffix(".md").write_text(summarize(report), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
