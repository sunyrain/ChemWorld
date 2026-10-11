from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts.run_hypothesis_notebook_pilot import PilotHost
from scripts.run_notebook_access_pilot import ARMS, CUE, TASK, command, prepare, usage_summary


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "source"
    host = PilotHost(root, 1)
    try:
        host.call(
            "lab_step",
            {
                "action": {"operation": "add_solvent", "solvent": 0, "volume_L": 0.02},
                "reason": "MODEL_REASON_SENTINEL",
            },
        )
        host.call("notebook_write", {"text": "NOTE_SENTINEL — 假设", "message": "test"})
    finally:
        host.close()
    return root


@pytest.mark.parametrize("arm", ARMS)
def test_real_stdio_conditions_keep_facts_and_hide_notes_until_requested(source, tmp_path, arm):
    original = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
    branch = tmp_path / arm
    prepare(source, branch, arm)
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "lab_status", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "lab_history", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "notebook_read", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "finish_batch",
                "arguments": {
                    "report": "software test; no new physical batch",
                    "notebook_text": "FINAL_NOTE_SENTINEL",
                },
            },
        },
    ]
    response = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.run_notebook_access_pilot",
            "--serve",
            "--output",
            str(branch),
            "--arm",
            arm,
            "--deadline",
            str(time.time() + 60),
        ],
        input="\n".join(json.dumps(r) for r in requests) + "\n",
        capture_output=True,
        encoding="utf-8",
        check=True,
        timeout=60,
        cwd=Path(__file__).resolve().parents[1],
    )
    values = [json.loads(line)["result"] for line in response.stdout.splitlines()]
    assert "NOTE_SENTINEL" not in json.dumps(values[:4])
    assert "MODEL_REASON_SENTINEL" not in json.dumps(values)
    names = {t["name"] for t in values[1]["tools"]}
    assert ("notebook_read" in names) == (arm != "H")
    finish_schema = next(
        t["inputSchema"] for t in values[1]["tools"] if t["name"] == "finish_batch"
    )
    assert ("notebook_text" in finish_schema["properties"]) == (arm != "H")
    assert json.loads(values[3]["content"][0]["text"])["total"] == 1
    assert values[4]["isError"] == (arm == "H")
    assert ("NOTE_SENTINEL" in json.dumps(values[4])) == (arm != "H")
    assert values[5]["isError"] == (arm == "H")
    assert original == {
        p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()
    }


@pytest.mark.parametrize("arm", ARMS)
def test_commands_disable_delegation_and_do_not_require_note_maintenance(tmp_path, arm):
    client = SimpleNamespace(codex_executable="codex", model="gpt-5.6-sol")
    args = command(client, tmp_path, arm, time.time() + 60)
    index = args.index("multi_agent")
    assert args[index - 1] == "--disable"
    assert "--ignore-user-config" in args and "--ignore-rules" in args
    folder = tmp_path / "provider" / "session-2"
    assert (folder / "instructions.md").read_text(encoding="utf-8") == TASK
    assert (CUE in (folder / "prompt.txt").read_text(encoding="utf-8")) == (arm == "C")
    server_args = json.loads(
        next(a.split("=", 1)[1] for a in args if a.startswith("mcp_servers.chemworld.args="))
    )
    assert server_args[1] == "scripts.run_notebook_access_pilot"
    assert server_args[server_args.index("--arm") + 1] == arm


def test_usage_keeps_cached_input_and_missing_usage_distinct():
    assert not usage_summary([])["usage_complete"]
    result = usage_summary(
        [
            {
                "type": "turn.completed",
                "usage": {"input_tokens": 100, "cached_input_tokens": 80, "output_tokens": 5},
            }
        ]
    )
    assert result["usage_complete"] and result["total_tokens"] == 105
    assert result["usage"]["cached_input_tokens"] == 80
