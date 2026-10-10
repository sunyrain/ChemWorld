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

    # A second, independent MCP process gets metadata only until it requests the
    # retained notebook. This verifies transport/persistence, not LLM behavior.
    restart_requests = [requests[0], requests[1], requests[4], requests[5]]
    restarted = subprocess.run(
        [*result.args, "--batch", "2"],
        input="\n".join(json.dumps(r, ensure_ascii=False) for r in restart_requests) + "\n",
        capture_output=True,
        encoding="utf-8",
        timeout=60,
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        env=child_env,
    )
    replies = [json.loads(line) for line in restarted.stdout.splitlines()]
    assert [r["id"] for r in replies] == [1, 4, 5]
    assert "HIDDEN_UNTIL_REQUESTED" not in json.dumps(replies[:2])
    recovered = json.loads(replies[2]["result"]["content"][0]["text"])
    assert recovered["revision"] == 1 and recovered["text"] == body


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


def test_cited_events_and_selected_artifact_fields_preserve_public_values(tmp_path):
    host = PilotHost(tmp_path, 1)
    try:
        for action in batch_actions():
            event = host.call("lab_step", {"action": action, "reason": "scripted"})
            assert "error" not in event
        ledger = host.docs.authoritative_path.read_bytes()
        nmr_id, final_id = "batch-1-operation-006", "batch-1-operation-008"
        matched = host.call("lab_history", {"event_ids": [final_id, nmr_id], "limit": 1})
        assert matched["total"] == 2 and matched["next_offset"] == 1
        assert matched["events"][0]["event_id"] == nmr_id
        second = host.call(
            "lab_history", {"event_ids": [final_id, nmr_id], "offset": 1, "limit": 1}
        )
        assert second["events"][0]["event_id"] == final_id
        assert second["next_offset"] is None

        original = (tmp_path / "public-artifacts" / f"{nmr_id}.json").read_bytes()
        artifact = json.loads(original)
        requested = ["observation", "processed_estimate"]
        response = host.call("lab_artifact", {"event_id": nmr_id, "fields": requested})
        assert response["next_offset"] is None
        assert response["selected_fields"] == requested
        assert json.loads(response["text"]) == {key: artifact[key] for key in requested}
        assert set(response["available_fields"]) == artifact.keys()
        assert len(response["text"]) < len(original.decode("utf-8"))
        # Raw values/arrays stay available and can be reassembled without loss.
        chunks = []
        offset = 0
        while offset is not None:
            response = host.call(
                "lab_artifact",
                {"event_id": nmr_id, "fields": ["raw_signal"], "offset": offset, "limit": 12000},
            )
            assert "error" not in response
            chunks.append(response["text"])
            offset = response["next_offset"]
        assert json.loads("".join(chunks)) == {"raw_signal": artifact["raw_signal"]}

        # Nulls/missing observations remain exactly as recorded, not inferred or zero-filled.
        initial_id = "batch-1-operation-001"
        initial = json.loads((tmp_path / "public-artifacts" / f"{initial_id}.json").read_bytes())
        response = host.call("lab_artifact", {"event_id": initial_id, "fields": ["observation"]})
        assert json.loads(response["text"])["observation"] == initial["observation"]
        assert any(value is None for value in initial["observation"].values())

        for tool, args in [
            ("lab_history", {"event_ids": [final_id, "future"]}),
            ("lab_history", {"event_ids": [final_id, final_id]}),
            ("lab_history", {"event_ids": []}),
            ("lab_history", {"event_ids": "not a list"}),
            ("lab_artifact", {"event_id": nmr_id, "fields": ["evaluator_truth"]}),
            ("lab_artifact", {"event_id": nmr_id, "fields": []}),
            ("lab_artifact", {"event_id": nmr_id, "fields": "raw_signal"}),
            ("lab_artifact", {"event_id": "../../credentials", "fields": ["observation"]}),
        ]:
            assert host.call(tool, args).get("error"), args
        assert host.steps == len(batch_actions())
        assert host.docs.authoritative_path.read_bytes() == ledger
        assert (tmp_path / "public-artifacts" / f"{nmr_id}.json").read_bytes() == original
        assert host.status()["public_history"] == {"event_count": 8, "last_event_id": final_id}
    finally:
        host.close()
