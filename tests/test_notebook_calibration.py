from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts import run_hypothesis_notebook_pilot as base
from scripts import run_notebook_calibration as study

RECIPE = [
    {"operation": "add_solvent", "solvent": 2, "volume_L": 0.04},
    {"operation": "add_reagent", "amount_mol": 0.02},
    {"operation": "add_catalyst", "catalyst": 0, "catalyst_amount_mol": 0.001},
    {
        "operation": "heat",
        "target_temperature_K": 340,
        "duration_s": 600,
        "stirring_speed_rpm": 600,
    },
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]


@pytest.mark.parametrize("arm", ["B", "N"])
def test_effective_prompt_and_tools_do_not_elicit_operation_explanations(tmp_path, arm):
    args = study.command(
        SimpleNamespace(codex_executable="codex", model="gpt-5.6-sol"),
        tmp_path / arm,
        arm,
        time.time() + 60,
    )
    text = (tmp_path / arm / "provider/session-1/instructions.md").read_text(encoding="utf-8")
    assert text == study.TASK + (study.NOTE_TASK if arm == "N" else "")
    assert "FIRST physical action" not in text and "public scientific reasons" not in text
    assert ("testable expectation" in text) == (arm == "N")
    assert "SAME conversation" in text and "No interim report is" in text
    assert args[args.index("multi_agent") - 1] == "--disable"
    host = study.CampaignHost(tmp_path / arm, arm, time.time() + 60)
    try:
        response = study.dispatch(host, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["lab_step"]["inputSchema"]["required"] == ["action"]
        assert "reason" not in tools["lab_step"]["inputSchema"]["properties"]
        assert "finish_batch" not in tools and "lab_reports" not in tools
        assert ("notebook_write" in tools) == (arm == "N")
        initialized = study.dispatch(host, {"id": 2, "method": "initialize"})
        assert "hypoth" not in initialized["result"]["instructions"]
        assert "notebook" not in initialized["result"]["instructions"]
    finally:
        host.close()


def test_original_host_still_requires_text_reason_and_new_host_preserves_physics(tmp_path):
    deadline = time.time() + 60
    old = base.PilotHost(tmp_path / "old", 1, seed=0, observation_seed=5001, deadline=deadline)
    new = study.CampaignHost(tmp_path / "new", "B", deadline)
    try:
        assert "error" in old.call("lab_step", {"action": RECIPE[0]})
        assert "error" in old.call("lab_step", {"action": RECIPE[0], "reason": None})
        assert old.steps == 0
        for action in RECIPE:
            expected = old.call("lab_step", {"action": action, "reason": "scripted test"})
            actual = new.call("lab_step", {"action": action})
            assert "error" not in actual and actual == expected
            assert actual["transaction_status"] == "committed"
        history = new.call("lab_history", {})
        assert "public_reason" not in json.dumps(history)
    finally:
        old.close()
        new.close()
    trajectory = load_records(tmp_path / "new/batch-1/trajectory.jsonl")
    assert all("public_reason" not in r.get("agent_metadata", {}) for r in trajectory)


def load_records(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_eight_batches_one_host_no_reports_required_and_notes_on_demand(tmp_path):
    host = study.CampaignHost(tmp_path, "N", time.time() + 60)
    try:
        failed = host.call("lab_next_batch", {})
        assert "error" in failed and host.lab.batch == 1 and host.lab.steps == 0
        note = "NOTE_SENTINEL: provisional claim, not a fact."
        host.call("notebook_write", {"text": note})
        for batch in range(1, 9):
            assert host.lab.batch == batch
            assert host.lab.env.observation_seed_override == 5000 + batch
            assert note not in json.dumps(host.call("lab_status", {}))
            assert host.lab.steps == 0
            for action in RECIPE:
                result = host.call("lab_step", {"action": action})
                assert result.get("transaction_status") == "committed", result
            if batch < 8:
                next_state = host.call("lab_next_batch", {})
                assert next_state["completed_batches"] == batch
                assert next_state["batch"] == batch + 1
                assert next_state["tool_requests_remaining"] == study.TOOL_BUDGET - host.calls
                assert note not in json.dumps(next_state)
        assert "error" in host.call("lab_next_batch", {})
        assert note in json.dumps(host.call("notebook_read", {}))
        assert "error" not in host.call("finish_campaign", {"report": "REPORT_SENTINEL"})
        assert "error" in host.call("lab_step", {"action": RECIPE[0]})
    finally:
        host.close()
    provider = {
        "usage_complete": True,
        "usage": {},
        "total_tokens": 0,
        "exit_code": 0,
        "transport_failures": [],
        "stop_reason": None,
    }
    data = study.summarize(tmp_path, provider)
    assert data["engineering_passed"] and data["completed_batches"] == 8
    assert len(data["errors"]) == 3 and len(data["notes"]) == 1
    assert all(b["replay"]["verified"] for b in data["batches"])
    assert all(
        "report" not in base.read_json(tmp_path / f"batch-{b}/host-summary.json")
        for b in range(1, 9)
    )
    summary = {"arms": {"N": data}, "failures": [], "planned_batches": 16}
    study.write_outputs(tmp_path, summary)
    aggregate = (tmp_path / "aggregate.json").read_text(encoding="utf-8")
    assert "NOTE_SENTINEL" not in aggregate and "REPORT_SENTINEL" not in aggregate
    assert base.read_json(tmp_path / "aggregate.json")["arms"]["B"] == {"executed": False}


def test_baseline_isolation_and_failed_requests_consume_shared_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "TOOL_BUDGET", 3)
    host = study.CampaignHost(tmp_path, "B", time.time() + 60)
    try:
        assert "error" in host.call("notebook_write", {"text": "not allowed"})
        assert "error" in host.call("lab_step", {"action": RECIPE[0], "reason": "not in schema"})
        assert host.call("lab_status", {})["tool_requests_remaining"] == 0
        assert "error" in host.call("lab_step", {"action": RECIPE[0]})
        assert host.lab.steps == 0 and host.calls == 4
        assert host.lab.docs.notebook_tool("log")["total"] == 0
    finally:
        host.close()
    assert len(load_records(tmp_path / "campaign-interactions.jsonl")) == 4
    data = study.summarize(tmp_path, {"usage_complete": False, "transport_failures": []})
    assert data["completed_batches"] == 0 and not data["engineering_passed"]
    assert len(data["errors"]) == 3


def test_stdio_continues_across_batch_without_new_session(tmp_path):
    requests = [("lab_step", {"action": a}) for a in RECIPE]
    requests += [
        ("lab_next_batch", {}),
        ("lab_step", {"action": RECIPE[0]}),
        ("finish_campaign", {"report": "Early close; second batch incomplete."}),
    ]
    wire = [
        {
            "jsonrpc": "2.0",
            "id": i,
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
        }
        for i, (name, args) in enumerate(requests, 1)
    ]
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.run_notebook_calibration",
            "--serve",
            "--output",
            str(tmp_path),
            "--arm",
            "B",
            "--deadline",
            str(time.time() + 60),
        ],
        input="\n".join(json.dumps(r) for r in wire) + "\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        cwd=Path(__file__).resolve().parents[1],
        check=True,
    )
    responses = [
        json.loads(json.loads(r)["result"]["content"][0]["text"])
        for r in process.stdout.splitlines()
    ]
    assert all("error" not in r for r in responses), responses
    assert responses[6]["batch"] == 2 and responses[-1]["completed_batches"] == 1
    assert base.read_json(tmp_path / "batch-2/host-summary.json")["steps"] == 1
    assert base.read_json(tmp_path / "campaign-state.json")["total_calls"] == len(wire)
