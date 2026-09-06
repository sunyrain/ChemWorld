"""Bounded provider compatibility probes; credentials stay out of artifacts and argv."""

# Chinese report prose intentionally uses fullwidth punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import contextlib
import getpass
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

BASE_URL = "https://api.siliconflow.cn/v1"
ROOT = Path(__file__).resolve().parents[1]


def summarize(run_root: Path, output: Path) -> None:
    """Publish allowlisted metadata, never the raw model messages or credentials."""
    records = {}
    for name, relative in (("discovery", "discovery-01"), ("api", "api-01"), ("codex", "codex-01")):
        records[name] = json.loads(
            (run_root / relative / "summary.json").read_text(encoding="utf-8")
        )
    api, codex = records["api"], records["codex"]
    checks = records["discovery"]["checks"] + api["checks"]
    for check in checks:
        check["passed"] = check.get("http_status") == 200
    by_name = {check["check"]: check for check in checks}
    by_name["chat_text"]["passed"] = api["text_passed"]
    by_name["chat_tool_call"]["passed"] = api["tool_calls"] == 1
    by_name["chat_tool_return"]["passed"] = api["tool_roundtrip_passed"]
    by_name["native_responses"]["passed"] = api["responses_object_received"]
    checks.append(
        {
            "check": "native_codex",
            "passed": codex["codex_turn_completed"],
            **{
                k: codex[k]
                for k in (
                    "exit_code",
                    "timed_out",
                    "wall_seconds",
                    "errors",
                    "tool_attempts",
                    "usage",
                    "continuation_tested",
                )
            },
        }
    )
    usages = [check["usage"] for check in checks if isinstance(check.get("usage"), dict)]
    report = {
        "schema_version": "chemworld-glm-harness-smoke-1",
        "formal_result": False,
        "experiment_note": "workstreams/flagship_tasks/WORK_II_GLM_HARNESS_SMOKE_NOTE.md",
        "model": api["model"],
        "base_url": BASE_URL,
        "models_discovered": [m["id"] for m in records["discovery"]["glm_models"]],
        "codex_version": subprocess.check_output(
            [shutil.which("codex") or "codex", "--version"], text=True
        ).strip(),
        "harness_command_builder": codex["command_builder"],
        "probe_units": "Five direct HTTP probes plus one actual Codex session",
        "scheduled_probes": 6,
        "attempted_probes": len(checks),
        "passed_probes": sum(check["passed"] for check in checks),
        "failed_probes": sum(not check["passed"] for check in checks),
        "checks": checks,
        "usage_coverage": "Usage received for three successful Chat Completions requests; "
        "failed Responses and Codex requests returned no usage.",
        "reported_usage": {
            k: sum(u.get(k, 0) for u in usages)
            for k in ("prompt_tokens", "completion_tokens", "total_tokens")
        },
        "unreached_harness_checks": [
            "MCP tool execution",
            "schema-valid terminal output",
            "same-thread continuation",
        ],
        "local_launcher_incidents": [
            {
                "stage": "discovery preflight",
                "provider_requests": 0,
                "reason": "Closed stdin in non-PTY invocation; corrected using getpass in a PTY.",
            }
        ],
        "result": "chat_and_tools_available_native_codex_not_connected",
        "scientific_sessions": 0,
        "core_executions": 0,
        "interpretation": "Compatibility smoke only. The configured /v1/responses route returned "
        "404 both directly and through the existing Codex harness. "
        "A Responses-to-Chat adapter was not implemented or tested. "
        "Hello/arithmetic latency is not a scientific-session ETA.",
    }
    lines = [
        "# GLM / SiliconFlow Codex harness 接入结果",
        "",
        f"模型：`{api['model']}`；Codex：`{report['codex_version']}`。开发接入测试，无科学会话。",
        "",
        "结论：聊天与工具闭环成功；原生Responses及实际Codex路径均返回404，未直接接通harness。",
        "",
        "| 探针 | 结果 | HTTP / CLI退出码 | 耗时（秒） |",
        "| --- | --- | ---: | ---: |",
    ]
    for check in checks:
        lines.append(
            f"| {check['check']} | {'通过' if check['passed'] else '失败'} | "
            f"{check.get('http_status', check.get('exit_code'))} | {check['wall_seconds']:.3f} |"
        )
    lines += [
        "",
        "6/6探针已执行，4通过、2失败；两条CLI错误事件属于同一次失败会话。",
        "工具API调用19+23后收到42，并正确使用工具结果完成回答。",
        "MCP执行、合法结构化终答、同thread续接因传输失败未到达，不能报告通过。",
        "",
        f"三次成功推理报告输入{report['reported_usage']['prompt_tokens']}、"
        f"输出{report['reported_usage']['completion_tokens']} tokens；"
        "失败请求未返回usage，不将其消费写成零。普通短调用耗时不能外推科学实验ETA。",
        "",
        "当前harness的wire_api=responses；该入口仅验证了Chat Completions能力。",
        "后续可开发Responses→Chat Completions适配器，再单独验证流式事件、工具返回、"
        "usage与会话续接。本块未实现适配器，也未启动第三模型科学实验。",
        "",
        "首次本地启动因stdin关闭在网络调用前终止；已改用PTY无回显输入。"
        "凭据未写入文件、参数或日志；原始响应仅保留在ignored runs。",
        "",
        "Codex协议依据：[官方配置文档](https://learn.chatgpt.com/docs/config-file/config-reference)。",
    ]
    for suffix, body in (
        (".json", json.dumps(report, indent=2, ensure_ascii=False) + "\n"),
        (".md", "\n".join(lines) + "\n"),
    ):
        path = output.with_suffix(suffix)
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(body)
    print(
        json.dumps(
            {
                k: report[k]
                for k in ("model", "attempted_probes", "passed_probes", "failed_probes", "result")
            }
        ),
        flush=True,
    )


def codex_probe(key: str, model: str, output: Path) -> dict[str, Any]:
    """Exercise the existing Work II command builder with isolated env-key auth."""
    sys.path.insert(0, str(ROOT))
    from scripts.run_work_ii_final_diagnostic import build_command, stop_process

    workspace = output / "workspace"
    workspace.mkdir()
    codex_home = output / "codex-home"
    codex_home.mkdir()
    catalog = json.loads(
        (ROOT / "configs/providers/openrouter_kimi_k2_5_models.json").read_text(encoding="utf-8")
    )
    entry = catalog["models"][0]
    entry.update(
        slug=model,
        display_name="GLM SiliconFlow compatibility probe",
        description="Unqualified local catalog entry for a bounded API smoke test.",
        default_reasoning_level="medium",
    )
    catalog_path = output / "models.json"
    catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    provider = {
        "id": "siliconflow_glm",
        "name": "SiliconFlow GLM",
        "model": model,
        "reasoning_effort": "medium",
        "auth_mode": "env_key",
    }
    (codex_home / "config.toml").write_text(
        "\n".join(
            [
                f"model_catalog_json = {json.dumps(catalog_path.as_posix())}",
                "[model_providers.siliconflow_glm]",
                'name = "SiliconFlow GLM"',
                f'base_url = "{BASE_URL}"',
                'wire_api = "responses"',
                'env_key = "SILICONFLOW_API_KEY"',
                "supports_websockets = false",
                "request_max_retries = 0",
                "stream_max_retries = 0",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    schema_path = output / "schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"ok": {"type": "boolean"}, "sum": {"type": "integer"}},
                "required": ["ok", "sum"],
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )
    audit = output / "tool_audit.jsonl"
    command = build_command(provider, schema_path, workspace, audit=audit, provider_retries=0)
    environment = {**os.environ, "CODEX_HOME": str(codex_home), "SILICONFLOW_API_KEY": key}
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=workspace,
        env=environment,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **(
            {"creationflags": subprocess.CREATE_NO_WINDOW}
            if os.name == "nt"
            else {"start_new_session": True}
        ),
    )
    prompt = (
        "Use the public_numerics calculate tool to evaluate 19+23 once. "
        "Return only the required JSON with ok=true and sum equal to the tool result."
    )
    timed_out = False
    first = True
    while True:
        try:
            stdout, stderr = process.communicate(prompt if first else None, timeout=20)
            break
        except subprocess.TimeoutExpired:
            first = False
            elapsed = time.monotonic() - started
            print(f"stage=codex_native pending=1 elapsed_s={elapsed:.0f}", flush=True)
            if elapsed >= 180:
                timed_out = True
                stop_process(process)
                stdout, stderr = process.communicate()
                break
    stdout, stderr = stdout.replace(key, "[REDACTED]"), stderr.replace(key, "[REDACTED]")
    (output / "stdout.jsonl").write_text(stdout, encoding="utf-8", newline="\n")
    (output / "stderr.txt").write_text(stderr, encoding="utf-8", newline="\n")
    events = []
    for line in stdout.splitlines():
        with contextlib.suppress(json.JSONDecodeError):
            events.append(json.loads(line))
    errors = [
        event.get("message") or event.get("error", {}).get("message")
        for event in events
        if event.get("type") in {"error", "turn.failed"}
    ]
    return {
        "formal_result": False,
        "model": model,
        "base_url": BASE_URL,
        "command_builder": "scripts.run_work_ii_final_diagnostic.build_command",
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "wall_seconds": round(time.monotonic() - started, 3),
        "event_types": [event.get("type") for event in events],
        "errors": errors,
        "stderr_tail": stderr[-1200:],
        "tool_attempts": len(audit.read_text(encoding="utf-8").splitlines())
        if audit.exists()
        else 0,
        "usage": [event.get("usage") for event in events if event.get("type") == "turn.completed"],
        "codex_turn_completed": any(event.get("type") == "turn.completed" for event in events),
        "continuation_tested": False,
    }


def request(
    key: str, endpoint: str, body: dict[str, Any] | None, output: Path
) -> tuple[dict[str, Any], Any]:
    started = time.monotonic()
    stop = threading.Event()

    def heartbeat() -> None:
        while not stop.wait(20):
            print(
                f"stage={output.stem} pending=1 elapsed_s={time.monotonic() - started:.0f}",
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    req = urllib.request.Request(
        BASE_URL + endpoint,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    record: dict[str, Any] = {"endpoint": endpoint, "attempts": 1}
    payload = None
    try:
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                raw = response.read().decode("utf-8", errors="replace")
                record["http_status"] = response.status
        except urllib.error.HTTPError as error:
            raw = error.read().decode("utf-8", errors="replace")
            record["http_status"] = error.code
        raw = raw.replace(key, "[REDACTED]")
        output.write_text(raw, encoding="utf-8", newline="\n")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            record["response_format"] = "non_json"
        if isinstance(payload, dict):
            record["model_returned"] = payload.get("model")
            record["usage"] = payload.get("usage")
            error = payload.get("error")
            if error is not None or record["http_status"] >= 400:
                record["error"] = error if error is not None else payload
        elif record["http_status"] >= 400:
            record["error"] = raw[:300]
    except (OSError, urllib.error.URLError) as error:
        record["transport_error"] = str(error).replace(key, "[REDACTED]")[:300]
    finally:
        stop.set()
        worker.join()
        record["wall_seconds"] = round(time.monotonic() - started, 3)
    return record, payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("discover", "probe", "codex", "summarize"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--key-stdin", action="store_true")
    args = parser.parse_args()
    if args.stage == "summarize":
        if args.run_root is None:
            parser.error("summarize requires --run-root")
        summarize(args.run_root, args.output)
        return 0
    if args.output.exists():
        parser.error("Use a new output directory; prior attempts are retained")
    args.output.mkdir(parents=True)
    if args.key_stdin:
        key = (
            getpass.getpass("SiliconFlow API key: ")
            if sys.stdin.isatty()
            else sys.stdin.readline().strip()
        )
    else:
        key = os.environ.get("SILICONFLOW_API_KEY", "")
    if not key:
        parser.error("Provide SILICONFLOW_API_KEY or --key-stdin")
    report: dict[str, Any] = {"formal_result": False, "base_url": BASE_URL, "checks": []}

    def run(name: str, endpoint: str, body: dict[str, Any] | None) -> Any:
        print(f"stage={name} started completed={len(report['checks'])}", flush=True)
        result, payload = request(key, endpoint, body, args.output / f"{name}.json")
        result["check"] = name
        report["checks"].append(result)
        (args.output / "summary.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n"
        )
        print(json.dumps(result, ensure_ascii=True), flush=True)
        return payload

    if args.stage == "codex":
        if not args.model or "glm" not in args.model.lower():
            parser.error("Choose a GLM identifier from the discovery result")
        report = codex_probe(key, args.model, args.output.resolve())
    elif args.stage == "discover":
        data = run("models", "/models", None)
        report["glm_models"] = [
            {k: model[k] for k in ("id", "object", "owned_by") if k in model}
            for model in (data or {}).get("data", [])
            if "glm" in model.get("id", "").lower()
        ]
        print(json.dumps({"glm_models": report["glm_models"]}, ensure_ascii=True), flush=True)
    else:
        if not args.model or "glm" not in args.model.lower():
            parser.error("Choose a GLM identifier from the discovery result")
        report["model"] = args.model
        base = {"model": args.model, "max_tokens": 2048, "stream": False}
        messages = [
            {"role": "system", "content": "Follow the request concisely."},
            {"role": "user", "content": "Reply with exactly GLM_CONNECTION_OK."},
        ]
        result = run("chat_text", "/chat/completions", {**base, "messages": messages})
        choices = (result or {}).get("choices", [])
        report["text_passed"] = bool(
            choices and choices[0]["message"].get("content", "").strip() == "GLM_CONNECTION_OK"
        )
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_integers",
                    "description": "Return the exact sum of two integers.",
                    "parameters": {
                        "type": "object",
                        "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                        "required": ["a", "b"],
                        "additionalProperties": False,
                    },
                },
            }
        ]
        tool_messages = [
            {
                "role": "user",
                "content": (
                    "Call add_integers with a=19 and b=23. After receiving its result, reply with "
                    "exactly GLM_TOOL_OK=42. Do not calculate without the tool."
                ),
            }
        ]
        result = run(
            "chat_tool_call",
            "/chat/completions",
            {**base, "messages": tool_messages, "tools": tools},
        )
        choices = (result or {}).get("choices", [])
        message = choices[0]["message"] if choices else {}
        calls = message.get("tool_calls", [])
        report["tool_calls"] = len(calls)
        report["tool_roundtrip_passed"] = False
        if len(calls) == 1 and calls[0].get("function", {}).get("name") == "add_integers":
            arguments = json.loads(calls[0]["function"]["arguments"])
            if arguments == {"a": 19, "b": 23}:
                tool_messages.extend(
                    [
                        message,
                        {"role": "tool", "tool_call_id": calls[0]["id"], "content": '{"sum":42}'},
                    ]
                )
                result = run(
                    "chat_tool_return",
                    "/chat/completions",
                    {**base, "messages": tool_messages, "tools": tools},
                )
                choices = (result or {}).get("choices", [])
                report["tool_roundtrip_passed"] = bool(
                    choices and choices[0]["message"].get("content", "").strip() == "GLM_TOOL_OK=42"
                )
        result = run(
            "native_responses",
            "/responses",
            {
                "model": args.model,
                "input": "Reply with exactly GLM_RESPONSES_OK.",
                "max_output_tokens": 2048,
                "stream": False,
            },
        )
        report["responses_object_received"] = bool(
            isinstance(result, dict) and result.get("object") == "response"
        )
    (args.output / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps({k: v for k, v in report.items() if k != "checks"}, ensure_ascii=True),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
