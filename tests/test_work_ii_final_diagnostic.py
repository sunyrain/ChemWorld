"""Public-tool isolation, exact science reuse, and failure-aware analysis."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
import pytest
from scripts.run_work_ii_final_diagnostic import build_command, launch, tool_allowed

from chemworld.agents.diagnostic_numerics import calculate
from chemworld.eval.work_ii_final_diagnostic import (
    ARMS,
    METRICS,
    prompt,
    schedule,
    summarize,
    validate,
)


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('os')",
        "open('api.md')",
        "(1).__class__",
        "[1][0]",
        "x+1",
        "[x for x in [1]]",
        "True",
        "1/0",
        "exp(10000)",
        "linspace(0,1,4097)",
        "linspace(0,1,4096)*array([[1],[2]])",
        "clip(linspace(0,1,4096),[[0],[1]],1)",
        "linspace([0,1],1,4096)",
    ],
)
def test_numerics_rejects_private_and_unbounded_paths(expression: str) -> None:
    with pytest.raises((ValueError, TypeError, ArithmeticError)):
        calculate(expression)


def test_public_numerical_reference() -> None:
    # A generic known public table, independent of hidden B3 simulator parameters.
    assert calculate("lstsq([[1,0],[1,1],[1,2]],[2,5,8])") == pytest.approx([2, 3])
    assert calculate("mean(abs(array([1,2,3])-array([2,2,5])))") == pytest.approx(1)
    assert calculate("log(exp(0.75))") == pytest.approx(0.75)


def test_stdio_mcp_and_reconnect_attempt_accounting(tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    command = [
        sys.executable,
        "-m",
        "chemworld.agents.diagnostic_numerics",
        "--audit",
        str(audit),
        "--limit",
        "1",
    ]
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "calculate", "arguments": {"expression": "1+2"}},
        },
    ]
    result = subprocess.run(
        command,
        input="\n".join(json.dumps(r) for r in requests) + "\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=20,
    )
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert rows[0]["result"]["serverInfo"]["name"] == "public_numerics"
    assert [t["name"] for t in rows[1]["result"]["tools"]] == ["calculate"]
    assert json.loads(rows[2]["result"]["content"][0]["text"])["value"] == 3
    again = subprocess.run(
        command,
        input=json.dumps(requests[2]) + "\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=20,
    )
    assert json.loads(again.stdout)["result"]["isError"]
    assert len(audit.read_text().splitlines()) == 2


def cells() -> list[dict]:
    public = {
        "task_id": "synthetic",
        "metric_range": [0, 1],
        "candidate_mechanism_families": [],
        "scoring_action_queries": [{"query_id": "q"}],
        "evidence": [{"query_id": "e", "target_observations": {"score": 0.1}}],
    }
    return [
        {
            "cluster_id": f"world-{i}",
            "arm": arm,
            "initial_world_model": {},
            "public_packet": deepcopy(public),
            "scoring_truth": {"q": dict.fromkeys(METRICS, 0.5)},
            "action_opportunity_eligible": True,
            "evidence_incumbent_score": 0.1,
            "secret_marker": "NEVER_PARTICIPANT_VISIBLE",
        }
        for i in range(5)
        for arm in ARMS
    ]


def payload() -> dict:
    return {
        "family": "FAMILY_B_POWER",
        "exponent": 1.75,
        "predictions": {"q": dict.fromkeys(METRICS, 0.5)},
        "selected_query_id": "q",
    }


def test_public_boundary_and_typed_mapping() -> None:
    cell = cells()[0]
    for stage in ("pre", "post"):
        text = prompt(cell, stage, "on")
        for private in ("NEVER_PARTICIPANT_VISIBLE", "scoring_truth", "world-0"):
            assert private not in text
        assert ('"evidence"' in text) == (stage == "post")
    law = validate(payload(), cell, "post")
    assert law["reference_exponent"] == 1.75
    for mutate in (
        lambda p: p.update(exponent=float("nan")),
        lambda p: p["predictions"]["q"].pop("score"),
        lambda p: p.update(selected_query_id="private"),
    ):
        p = payload()
        mutate(p)
        with pytest.raises(ValueError):
            validate(p, cell, "post")


def test_balanced_world_estimand_and_missing_denominators() -> None:
    units = schedule(cells(), development=False)
    assert len(units) == len({c["cell_id"] for c in units}) == 120
    results = []
    for c in units:
        if c["tool"] == "on":
            results.append({"cell_id": c["cell_id"], "status": "completed", "post": payload()})
    report = summarize(results, units, formal=True)
    assert report["counts"] == {"completed": 60, "unstarted": 60}
    assert report["primary"]["mean"] == 1
    assert np.allclose(report["primary"]["approximate_world_bootstrap_95"], [1, 1])
    assert len(report["failures"]) == 60
    results[0] = {"cell_id": results[0]["cell_id"], "status": "failed", "failure": "timeout"}
    report = summarize(results, units, formal=True)
    assert report["primary"]["mean"] == pytest.approx(59 / 60)
    assert sum(r["joint_recovery"] for r in report["rows"]) == 59


def test_only_declared_mcp_tool_allowed() -> None:
    item = {"type": "mcp_tool_call", "server": "public_numerics", "tool": "calculate"}
    assert tool_allowed(item, True)
    assert not tool_allowed(item, False)
    assert not tool_allowed({**item, "tool": "read_file"}, True)
    assert not tool_allowed({"type": "command_execution"}, True)


def test_formal_retries_disabled_on_both_turns(tmp_path: Path) -> None:
    provider = {"id": "fixture", "model": "fixture", "reasoning_effort": "medium"}
    for thread in (None, "same-thread"):
        command = build_command(
            provider, tmp_path / "schema.json", tmp_path, thread_id=thread, provider_retries=0
        )
        assert "model_providers.fixture.request_max_retries=0" in command
        assert "model_providers.fixture.stream_max_retries=0" in command
        if thread:
            assert command[-2:] == [thread, "-"]


@pytest.mark.parametrize("stream", [False, True])
def test_cli_zero_retries_with_local_error_service(tmp_path: Path, stream: bool) -> None:
    calls = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            self.rfile.read(int(self.headers.get("Content-Length", "0")))
            calls.append(self.path)
            if stream:
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                event = {
                    "type": "response.incomplete",
                    "response": {
                        "id": "fixture",
                        "status": "incomplete",
                        "incomplete_details": {"reason": "max_output_tokens"},
                    },
                }
                self.wfile.write(
                    ("event: response.incomplete\ndata: " + json.dumps(event) + "\n\n").encode()
                )
            else:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b'{"error":{"message":"fixture temporary failure"}}')

        def log_message(self, *_args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    task_codex_home = tmp_path / "codex-home"
    task_codex_home.mkdir()
    catalog = (
        Path(__file__).resolve().parents[1] / "configs/providers/deepseek_v4_flash_models.json"
    )
    config = f"model_catalog_json = {json.dumps(catalog.as_posix())}\n"
    config += '[model_providers.fixture]\nname="Local fixture"\nwire_api="responses"\n'
    config += f'base_url="http://127.0.0.1:{server.server_port}/v1/"\n'
    config += "supports_websockets=false\n"
    (task_codex_home / "config.toml").write_text(config)
    contract = tmp_path / "schema.json"
    contract.write_text(
        '{"type":"object","properties":{"ok":{"type":"boolean"}},'
        '"required":["ok"],"additionalProperties":false}'
    )
    provider = {"id": "fixture", "model": "deepseek-v4-flash", "reasoning_effort": "high"}
    command = build_command(provider, contract, tmp_path, provider_retries=0)
    try:
        receipt = launch(
            command,
            "Local transport fixture: return JSON.",
            tmp_path,
            {**os.environ, "CODEX_HOME": str(task_codex_home)},
            tmp_path / "output",
            20,
            False,
            tmp_path / "audit.jsonl",
            {},
        )
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    assert calls == ["/v1/responses"]
    assert receipt["failure"] == "provider_failure"


def test_real_launch_retains_receipt_and_stops_forbidden_tool(tmp_path: Path) -> None:
    child = tmp_path / "fixture.py"
    events = [
        {"type": "thread.started", "thread_id": "fixture-thread"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": '{"ok":true}'}},
        {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 4}},
    ]
    child.write_text(
        "import sys\nsys.stdin.read()\n"
        + "\n".join(f"print({json.dumps(json.dumps(e))}, flush=True)" for e in events)
    )
    receipt = launch(
        [sys.executable, str(child)],
        "public input",
        tmp_path,
        dict(os.environ),
        tmp_path / "completed",
        10,
        False,
        tmp_path / "audit.jsonl",
        {},
    )
    assert receipt["payload"] == {"ok": True}
    assert receipt["usage"]["input_tokens"] == 10
    assert receipt["failure"] is None
    child.write_text(
        "import sys,time\nsys.stdin.read()\n"
        'print(\'{"type":"item.started","item":{"type":"command_execution"}}\','
        "flush=True)\ntime.sleep(30)\n"
    )
    receipt = launch(
        [sys.executable, str(child)],
        "public input",
        tmp_path,
        dict(os.environ),
        tmp_path / "forbidden",
        10,
        False,
        tmp_path / "audit.jsonl",
        {},
    )
    assert receipt["failure"] == "forbidden_tool"
    assert receipt["elapsed_s"] < 10
