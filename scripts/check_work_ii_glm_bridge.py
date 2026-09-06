"""Qualify a GLM transport with actual Codex turns and a fixed development block."""
# ruff: noqa: RUF001 -- Chinese report text uses Chinese punctuation.

from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
import time
from copy import deepcopy
from pathlib import Path

from chemworld.providers.responses_chat_bridge import ResponsesChatBridge

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run_work_ii_final_diagnostic import build_command, launch, science_inputs  # noqa: E402

from chemworld.eval.work_ii_final_diagnostic import prompt, schema, score, validate  # noqa: E402

MODEL = "zai-org/GLM-5.3"


def write(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def prepare_home(root: Path, bridge: ResponsesChatBridge) -> tuple[dict, dict, Path]:
    workspace, home = root / "workspace", root / "codex-home"
    workspace.mkdir(parents=True)
    home.mkdir()
    catalog = json.loads(
        (ROOT / "configs/providers/openrouter_kimi_k2_5_models.json").read_text(encoding="utf-8")
    )
    catalog["models"][0].update(
        slug=MODEL,
        display_name="GLM 5.3 via local Chat Completions bridge",
        description="Development transport candidate; context limits are local settings.",
        default_reasoning_level="medium",
        supports_reasoning_summaries=False,
        support_verbosity=False,
        supports_parallel_tool_calls=False,
        context_window=65536,
        max_context_window=65536,
    )
    catalog_path = root / "model_catalog.json"
    write(catalog_path, catalog)
    provider = {
        "id": "siliconflow_glm_bridge",
        "model": MODEL,
        "reasoning_effort": "medium",
        "auth_mode": "env_key",
    }
    (home / "config.toml").write_text(
        "\n".join(
            [
                f"model_catalog_json = {json.dumps(catalog_path.as_posix())}",
                "[features]",
                "enable_request_compression = false",
                "shell_snapshot = false",
                "[agents]",
                "enabled = false",
                "[model_providers.siliconflow_glm_bridge]",
                'name = "SiliconFlow GLM bridge"',
                f'base_url = "{bridge.base_url}"',
                'wire_api = "responses"',
                'env_key = "CHEMWORLD_GLM_BRIDGE_TOKEN"',
                "supports_websockets = false",
                "request_max_retries = 0",
                "stream_max_retries = 0",
                "stream_idle_timeout_ms = 180000",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    environment = {
        **os.environ,
        "CODEX_HOME": str(home),
        "CHEMWORLD_GLM_BRIDGE_TOKEN": bridge.local_token,
    }
    environment.pop("SILICONFLOW_API_KEY", None)
    for key in ("NO_PROXY", "no_proxy"):
        environment[key] = ",".join(filter(None, [environment.get(key), "127.0.0.1", "localhost"]))
    return provider, environment, workspace


def smoke(root: Path, bridge: ResponsesChatBridge) -> dict:
    provider, environment, workspace = prepare_home(root, bridge)
    audit = root / "tool_audit.jsonl"
    output_schema = {
        "type": "object",
        "properties": {
            "ok": {"type": "boolean"},
            "sum": {"type": "number"},
            "marker": {"type": "string"},
        },
        "required": ["ok", "sum", "marker"],
        "additionalProperties": False,
    }
    schema_path = root / "schema.json"
    write(schema_path, output_schema)
    prompts = [
        "Remember the marker LANTERN-47. Use public_numerics.calculate to evaluate 19+23. "
        "Return only JSON with ok=true, sum equal to the tool result "
        "and marker equal to that marker.",
        "Recall the marker and the sum from our previous turn. Use public_numerics.calculate to "
        "add 1 to that previous sum. Return only JSON with ok=true, "
        "the new sum and the same marker.",
    ]
    results, thread_id = [], None
    for index, message in enumerate(prompts, 1):
        command = build_command(
            provider, schema_path, workspace, audit=audit, thread_id=thread_id, provider_retries=0
        )
        receipt = launch(
            command,
            message,
            workspace,
            environment,
            root / f"turn-{index}",
            240,
            True,
            audit,
            {"block": "glm-smoke", "turn": index, "total": 2},
        )
        correct = receipt["payload"] == {"ok": True, "sum": 41 + index, "marker": "LANTERN-47"}
        stable = receipt.get("thread_id") is not None and (
            thread_id is None or thread_id == receipt["thread_id"]
        )
        results.append(
            {
                "turn": index,
                "passed": correct and stable and not receipt["failure"],
                "receipt": receipt,
            }
        )
        write(root / "partial.json", results)
        print(
            json.dumps(
                {
                    "block": "glm-smoke",
                    "completed": index,
                    "total": 2,
                    "passed": results[-1]["passed"],
                    "upstream_requests": len(bridge.records),
                }
            ),
            flush=True,
        )
        if not results[-1]["passed"]:
            break
        thread_id = receipt["thread_id"]
    tools = (
        [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
        if audit.exists()
        else []
    )
    passed = (
        len(results) == 2
        and all(r["passed"] for r in results)
        and (len(tools) >= 2 and [t.get("value") for t in tools] == [42.0, 43.0])
    )
    return {
        "stage": "smoke",
        "scheduled_turns": 2,
        "attempted_turns": len(results),
        "passed": passed,
        "results": results,
        "tool_audit": tools,
    }


def calibrate(root: Path, bridge: ResponsesChatBridge) -> dict:
    protocol = json.loads(
        (ROOT / "configs/benchmark/work_ii_final_diagnostic_20260905.json").read_text(
            encoding="utf-8"
        )
    )
    candidates, source = science_inputs(protocol, development=True)
    cells = [deepcopy(c) for c in candidates if c["model"] == "gpt"]
    for cell in cells:
        cell["model"] = "glm"
        cell["cell_id"] = cell["cell_id"].replace("--gpt--", "--glm--")
    write(root / "inputs.json", {"cells": cells, "source": source})
    results = []
    block_start = time.monotonic()
    for index, cell in enumerate(cells, 1):
        if time.monotonic() - block_start >= 2700 or len(bridge.records) >= 48:
            break
        directory = root / f"session-{index}"
        provider, environment, workspace = prepare_home(directory, bridge)
        audit = directory / "tool_audit.jsonl"
        result = {
            "cell_id": cell["cell_id"],
            "model": "glm",
            "tool": cell["tool"],
            "arm": cell["arm"],
            "status": "failed",
            "receipts": [],
        }
        start, thread_id = time.monotonic(), None
        for stage in ("pre", "post"):
            schema_path = directory / (stage + "_schema.json")
            write(schema_path, schema(cell, stage))
            enabled = stage == "post" and cell["tool"] == "on"
            command = build_command(
                provider,
                schema_path,
                workspace,
                audit=audit if enabled else None,
                thread_id=thread_id,
                provider_retries=0,
            )
            timeout = min(
                240, 480 - (time.monotonic() - start), 2700 - (time.monotonic() - block_start)
            )
            if timeout <= 0:
                result["failure"] = "resource_budget_exhausted"
                break
            receipt = launch(
                command,
                prompt(cell, stage, cell["tool"]),
                workspace,
                environment,
                directory / stage,
                timeout,
                enabled,
                audit,
                {"block": "glm-calibration", "session": index, "total": 6, "stage": stage},
            )
            result["receipts"].append({"stage": stage, **receipt})
            write(directory / "partial.json", result)
            if receipt["failure"]:
                result["failure"] = receipt["failure"]
                break
            try:
                validate(receipt["payload"], cell, stage)
            except ValueError as error:
                result.update(failure="participant_schema_" + stage, error=str(error))
                break
            if not receipt["thread_id"] or (thread_id and thread_id != receipt["thread_id"]):
                result["failure"] = "thread_identity_failure"
                break
            thread_id = receipt["thread_id"]
            result[stage] = receipt["payload"]
        else:
            result["status"] = "completed"
        result["elapsed_s"] = time.monotonic() - start
        result["score"] = score(result, cell)
        result["tool_audit"] = (
            [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            if audit.exists()
            else []
        )
        write(directory / "result.json", result)
        results.append(result)
        write(root / "partial.json", results)
        elapsed = time.monotonic() - block_start
        print(
            json.dumps(
                {
                    "block": "glm-calibration",
                    "completed": index,
                    "total": 6,
                    "status": result["status"],
                    "sessions_per_hour": 3600 * index / elapsed,
                    "eta_seconds": elapsed / index * (6 - index),
                    "upstream_requests": len(bridge.records),
                }
            ),
            flush=True,
        )
        if any(r["status"] == "failed" for r in bridge.records):
            break
    return {
        "stage": "calibration",
        "scheduled_sessions": 6,
        "attempted_sessions": len(results),
        "completed_sessions": sum(r["status"] == "completed" for r in results),
        "unstarted_sessions": 6 - len(results),
        "results": results,
        "passed": len(results) == 6 and all(r["status"] == "completed" for r in results),
    }


def build_report(attempts: list[Path], calibration: Path | None) -> dict:
    """Summarize explicitly selected immutable attempts, including unstarted units."""
    summaries = [json.loads((p / "summary.json").read_text(encoding="utf-8")) for p in attempts]
    block = (
        json.loads((calibration / "summary.json").read_text(encoding="utf-8"))
        if calibration
        else None
    )
    attempt_rows, requests = [], []
    for path, result in zip(attempts, summaries, strict=True):
        requests.extend(result["bridge_requests"])
        rows = []
        for turn in range(1, 3):
            item = next((r for r in result["results"] if r["turn"] == turn), None)
            receipt = item["receipt"] if item else {}
            rows.append(
                {
                    "turn": turn,
                    "status": (
                        "unstarted"
                        if item is None
                        else "valid_answer_and_thread"
                        if item["passed"]
                        else "failed"
                    ),
                    "failure": receipt.get("failure"),
                    "payload_fields": sorted(receipt["payload"])
                    if isinstance(receipt.get("payload"), dict)
                    else None,
                    "tool_event_count": receipt.get("tool_event_count"),
                    "usage": receipt.get("usage"),
                    "wall_seconds": receipt.get("elapsed_s"),
                }
            )
        attempt_rows.append(
            {
                "attempt": path.name,
                "raw_root": path.as_posix(),
                "schema_mode": result["schema_mode"],
                "passed": result["passed"],
                "failure_reasons": sorted(
                    {r["error_code"] for r in result["bridge_requests"] if r.get("error_code")}
                    | ({"mcp_not_executed"} if not result["tool_audit"] else set())
                    | (
                        {"answer_or_thread_check_failed"}
                        if any(not r["passed"] for r in result["results"])
                        else set()
                    )
                ),
                "scheduled_turns": 2,
                "attempted_turns": result["attempted_turns"],
                "mcp_calls": len(result["tool_audit"]),
                "turns": rows,
                "wall_seconds": result["wall_seconds"],
                "bridge_requests": result["bridge_requests"],
            }
        )
    if block:
        requests.extend(block["bridge_requests"])
    usage = [r["usage"] for r in requests if r.get("usage") is not None]
    calibration_rows = []
    if block:
        calibration_rows = [
            {k: row[k] for k in ("cell_id", "arm", "tool", "status", "elapsed_s", "score")}
            | {"failure": row.get("failure")}
            for row in block["results"]
        ]
    completed = block["completed_sessions"] if block else 0
    attempted = block["attempted_sessions"] if block else 0
    return {
        "schema_version": "chemworld-glm-adapter-development-1",
        "formal_result": False,
        "model": MODEL,
        "experiment_note": "workstreams/flagship_tasks/WORK_II_GLM_ADAPTER_DEVELOPMENT_NOTE.md",
        "codex_versions": sorted({s["codex_version"] for s in summaries}),
        "third_model_adopted": any(s["passed"] for s in summaries) and completed == 6,
        "status": (
            "development_qualified"
            if any(s["passed"] for s in summaries) and completed == 6
            else "not_qualified"
        ),
        "transport": {
            "attempt_limit": 3,
            "attempted": len(summaries),
            "passed": sum(s["passed"] for s in summaries),
            "scheduled_turns_in_attempted_blocks": 2 * len(summaries),
            "attempted_turns": sum(s["attempted_turns"] for s in summaries),
            "attempts": attempt_rows,
        },
        "calibration": {
            "scheduled_sessions": 6,
            "attempted_sessions": attempted,
            "completed_sessions": completed,
            "failed_sessions": attempted - completed,
            "unstarted_sessions": 6 - attempted,
            "scheduled_turns": 12,
            "attempted_turns": sum(len(r["receipts"]) for r in block["results"]) if block else 0,
            "status": "unstarted_transport_not_qualified" if not block else block["stage"],
            "results": calibration_rows,
        },
        "resource_accounting": {
            "bridge_requests": len(requests),
            "requests_reaching_upstream_http": sum("http_status" in r for r in requests),
            "requests_without_usage": sum(r.get("usage") is None for r in requests),
            "reported_input_tokens": sum(u["prompt_tokens"] for u in usage),
            "reported_output_tokens": sum(u["completion_tokens"] for u in usage),
            "reported_reasoning_tokens": sum(
                u.get("completion_tokens_details", {}).get("reasoning_tokens", 0) for u in usage
            ),
            "attempt_wall_seconds": sum(s["wall_seconds"] for s in summaries),
            "formal_60_session_eta_seconds": None,
        },
        "limits": [
            "Development transport qualification only; historical two-model evidence is unchanged.",
            "Provider-default reasoning; Codex medium is not mapped to equivalent GLM effort.",
            "Upstream output is buffered before Responses output-item SSE events are emitted.",
            "Freeform tools use a JSON input string; grammar constraints are conveyed as text.",
            "Missing provider usage remains null in request records.",
            "Short smoke latency does not estimate the unstarted six-session calibration.",
        ],
    }


def render_report(report: dict) -> str:
    transport, block, resource = (
        report["transport"],
        report["calibration"],
        report["resource_accounting"],
    )
    lines = [
        "# GLM Codex适配开发资格结果",
        "",
        "2026-09-06；模型 `zai-org/GLM-5.3`；development evidence。",
        "",
        f"第三模型采用：**{'是' if report['third_model_adopted'] else '否'}**。"
        f"真实工具闭环通过 {transport['passed']}/{transport['attempted']} 次工程尝试；"
        f"六会话校准完成 {block['completed_sessions']}/6，"
        f"未启动 {block['unstarted_sessions']}/6。",
        "",
        "| 尝试 | schema传输 | 尝试轮数/计划 | 实际MCP调用 | 完整通过 | wall秒 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in transport["attempts"]:
        lines.append(
            f"| {row['attempt']} | {row['schema_mode']} | {row['attempted_turns']}/2 | "
            f"{row['mcp_calls']} | {row['passed']} | {row['wall_seconds']:.2f} |"
        )
    lines.extend(["", "## 每次失败", ""])
    labels = {
        "unsupported_tool": "本地适配器不支持当时的工具声明, 请求未到上游",
        "mcp_not_executed": "没有真实MCP调用",
        "answer_or_thread_check_failed": "终答或thread检查未通过",
    }
    for row in transport["attempts"]:
        if row["failure_reasons"]:
            reasons = "; ".join(labels.get(r, r) for r in row["failure_reasons"])
            lines.append(f"- {row['attempt']}: {reasons}。")
    lines.extend(
        [
            "",
            "## 资源与边界",
            "",
            f"本块记录 {resource['bridge_requests']} 次本地请求，"
            f"{resource['requests_reaching_upstream_http']} 次到达上游HTTP；"
            f"报告输入 {resource['reported_input_tokens']:,}、"
            f"输出 {resource['reported_output_tokens']:,} tokens，"
            f"其中reasoning {resource['reported_reasoning_tokens']:,}。"
            f"{resource['requests_without_usage']} 条请求无usage，原记录保留null。",
            "",
            "未取得六会话吞吐，60会话正式复核ETA保持未知；不能用短算术调用外推。",
            "",
            *[f"- {item}" for item in report["limits"]],
            "",
            "实验与停止规则见[实验说明](../WORK_II_GLM_ADAPTER_DEVELOPMENT_NOTE.md)。",
            "原始请求、输出和凭据不进入Git；同名JSON保留全部尝试与固定分母。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("smoke", "calibrate", "report"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--schema-mode", choices=("json_schema", "json_object"), default="json_schema"
    )
    parser.add_argument("--key-stdin", action="store_true")
    parser.add_argument("--smoke-summary", type=Path)
    parser.add_argument("--attempts", type=Path, nargs="+")
    parser.add_argument("--calibration", type=Path)
    args = parser.parse_args()
    root = args.output.resolve()
    if args.stage == "report":
        if not args.attempts:
            parser.error("report requires explicit --attempts directories")
        report = build_report(args.attempts, args.calibration)
        write(root.with_suffix(".json"), report)
        root.with_suffix(".md").write_text(render_report(report), encoding="utf-8", newline="\n")
        print(json.dumps({"status": report["status"], "report": str(root)}))
        return
    if args.stage == "calibrate":
        if not args.smoke_summary:
            parser.error("calibration requires a passed --smoke-summary from this transport")
        qualified = json.loads(args.smoke_summary.read_text(encoding="utf-8"))
        if not (
            qualified.get("passed")
            and qualified.get("stage") == "smoke"
            and qualified.get("model") == MODEL
            and qualified.get("schema_mode") == args.schema_mode
        ):
            parser.error("calibration is not eligible: matching transport smoke has not passed")
    root.mkdir(parents=True, exist_ok=False)
    key = (
        getpass.getpass("SiliconFlow API key: ")
        if args.key_stdin
        else os.environ.get("SILICONFLOW_API_KEY", "")
    )
    if not key:
        parser.error("Provide the API key through the environment or a non-echo terminal")
    start = time.monotonic()
    with ResponsesChatBridge(
        api_key=key, audit_dir=root / "bridge", schema_mode=args.schema_mode
    ) as bridge:
        result = smoke(root, bridge) if args.stage == "smoke" else calibrate(root, bridge)
        result.update(
            model=MODEL,
            formal_result=False,
            schema_mode=args.schema_mode,
            bridge_requests=bridge.records,
            wall_seconds=time.monotonic() - start,
            codex_version=subprocess.check_output(
                [shutil.which("codex") or "codex", "--version"], text=True
            ).strip(),
        )
        write(root / "summary.json", result)
        print(
            json.dumps(
                {
                    k: v
                    for k, v in result.items()
                    if k not in {"results", "bridge_requests", "tool_audit"}
                }
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
