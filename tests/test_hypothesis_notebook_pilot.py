from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from scripts.run_hypothesis_notebook_pilot import PilotHost, collect, dispatch, tool_definitions


def batch_actions():
    return [
        {"operation": "add_solvent", "solvent": 0, "volume_L": 0.015},
        {"operation": "add_solvent", "solvent": 1, "volume_L": 0.015},
        {"operation": "add_reagent", "amount_mol": 0.012},
        {
            "operation": "heat",
            "target_temperature_K": 350,
            "duration_s": 600,
            "stirring_speed_rpm": 600,
        },
        {
            "operation": "configure_instrument",
            "instrument": "nmr",
            "scan_count": 8,
            "resolution_factor": 1,
            "dilution_factor": 1,
        },
        {"operation": "measure", "instrument": "nmr"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def test_two_native_hosts_preserve_notes_on_demand_and_facts_separately(tmp_path):
    h1 = PilotHost(tmp_path, 1)
    secret = "H1: UNIQUE_SCIENTIFIC_INTERPRETATION"
    note = h1.call("notebook_write", {"text": secret})
    assert "text" not in note
    for action in batch_actions():
        result = h1.call("lab_step", {"action": action, "reason": "PUBLIC_REASON_ONLY"})
        assert "error" not in result, result
    assert result["terminal"]
    facts = h1.docs.authoritative_path.read_bytes()
    assert secret.encode() not in facts and b"PUBLIC_REASON_ONLY" not in facts
    last = result["event_id"]
    h1.call(
        "notebook_write",
        {"text": secret + "\nRevised after evidence " + last, "reviewed_through": last},
    )
    assert h1.call("finish_batch", {"report": "scripted"})["final_assay_completed"]
    h1.close()

    h2 = PilotHost(tmp_path, 2)
    try:
        assert secret not in json.dumps(h2.status())
        assert secret not in json.dumps(tool_definitions())
        assert h2.call("notebook_read", {})["text"].startswith(secret)
        history = h2.call("lab_history", {"offset": 0, "limit": 3})
        assert history["total"] == 8 and history["next_offset"] == 3
        before = h2.docs.authoritative_path.read_bytes()
        restored = h2.call("notebook_restore", {"revision": 1})
        assert restored["revision"] == 3
        assert h2.docs.authoritative_path.read_bytes() == before == facts
        assert "Revised" in h2.call("notebook_diff", {"before": 1, "after": 2})["text"]
        for action in batch_actions():
            h2.call("lab_step", {"action": action, "reason": "scripted"})
        h2.call("finish_batch", {"report": "scripted, not an LLM result"})
    finally:
        h2.close()
    result = collect(tmp_path)
    assert result["completed_batches"] == 2
    assert result["physical_attempts"] == result["committed"] == 16
    assert all(result["coverage"].values()) and result["quality_passed"]
    assert all(b["replay"]["verified"] for b in result["batches"])


def test_rejected_operations_and_tool_errors_are_retained(tmp_path):
    host = PilotHost(tmp_path, 1)
    try:
        host.call("lab_step", {"action": batch_actions()[0], "reason": "scripted"})
        host.call("lab_step", {"action": batch_actions()[2], "reason": "scripted"})
        host.call("lab_step", {"action": {"operation": "terminate"}, "reason": "scripted"})
        invalid = host.call(
            "lab_step",
            {
                "action": {"operation": "measure", "instrument": "nmr"},
                "reason": "invalid after termination",
            },
        )
        assert invalid["transaction_status"] == "rolled_back"
        assert host.call("notebook_write", {"text": "x", "reviewed_through": "future"})["error"]
        assert host.call("lab_artifact", {"event_id": "../../credentials"})["error"]
        assert host.steps == 4
    finally:
        host.close()
    result = collect(tmp_path)
    assert result["rolled_back"] == 1 and result["completed_batches"] == 0
    assert result["batches"][0]["replay"]["verified"]
    assert len(result["batches"][0]["errors"]) == 2


@pytest.mark.parametrize("expired", [True, False])
def test_limits_prevent_mutations_without_losing_requests(tmp_path, expired):
    host = PilotHost(
        tmp_path,
        1,
        tool_budget=0 if not expired else 60,
        deadline=time.time() - 1 if expired else time.time() + 600,
    )
    try:
        result = host.call("notebook_write", {"text": "must not commit"})
        assert "budget" in result["message"]
        assert host.docs.notebook_tool("log")["total"] == 0
        assert host.result["tool_calls"] == 1
    finally:
        host.close()


def test_stdio_protocol_real_subprocess_and_metadata_only(tmp_path):
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "notebook_write",
                "arguments": {"text": "HIDDEN_UNTIL_REQUESTED — 假设在350\u2013420 K待检验"},
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "lab_status", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "notebook_read", "arguments": {}},
        },
    ]
    child_env = {**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.run_hypothesis_notebook_pilot",
            "--serve",
            "--output",
            str(tmp_path),
            "--deadline",
            str(time.time() + 60),
        ],
        input="\n".join(json.dumps(r, ensure_ascii=False) for r in requests) + "\n",
        capture_output=True,
        encoding="utf-8",
        timeout=60,
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        env=child_env,
    )
    lines = [json.loads(line) for line in result.stdout.splitlines()]
    assert [r["id"] for r in lines] == [1, 2, 3, 4, 5]
    assert "HIDDEN_UNTIL_REQUESTED" not in json.dumps(lines[:4])
    assert "HIDDEN_UNTIL_REQUESTED" in json.dumps(lines[4])
    body = json.loads(lines[4]["result"]["content"][0]["text"])["text"]
    assert body == "HIDDEN_UNTIL_REQUESTED — 假设在350\u2013420 K待检验"
    assert all("error" not in r for r in lines)


def test_bad_protocol_params_do_not_mutate_environment(tmp_path):
    host = PilotHost(tmp_path, 1)
    try:
        result = dispatch(
            host,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "lab_step", "arguments": []},
            },
        )
        assert result["error"]["code"] == -32602
        assert host.steps == host.calls == 0
    finally:
        host.close()


def test_bulk_schema_and_handled_errors_allow_continuing(tmp_path):
    host = PilotHost(tmp_path, 1)
    try:
        schemas = host.call("lab_schema", {"operations": ["add_solvent", "measure", "terminate"]})
        assert set(schemas) == {"add_solvent", "measure", "terminate"}
        assert host.call("lab_schema", {"operations": ["final_assay"]})["error"]
        assert not host.call("notebook_write", {"text": "H1 — 未检验"}).get("error")
        assert host.docs.notebook_tool("read")["text"] == "H1 — 未检验"
    finally:
        host.close()
