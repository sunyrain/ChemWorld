from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts import run_hypothesis_notebook_pilot as base
from scripts.run_long_horizon_notebook_review import summarize_batch
from scripts.run_notebook_access_pilot import definitions
from scripts.run_notebook_utility_study import UtilityHost, command, write_outputs


@pytest.mark.parametrize("arm", ["H", "N"])
def test_new_process_recovers_report_on_demand_without_private_summary_or_note(tmp_path, arm):
    root = tmp_path / arm
    host = UtilityHost(root, arm, 1, time.time() + 60)
    report = "报告 — planned, not performed."
    host.result["private_evaluator_sentinel"] = "DO_NOT_DISCLOSE"
    host.call("finish_batch", {"report": report})
    host.close()
    requests = [
        {
            "jsonrpc": "2.0",
            "id": i,
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
        }
        for i, (name, args) in enumerate(
            [
                ("lab_status", {}),
                ("lab_reports", {}),
                ("lab_reports", {"batch": 1}),
                ("lab_history", {}),
                ("lab_reports", {"batch": 2}),
            ],
            1,
        )
    ]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.run_notebook_utility_study",
            "--serve",
            "--output",
            str(root),
            "--arm",
            arm,
            "--batch",
            "2",
            "--deadline",
            str(time.time() + 60),
        ],
        input="\n".join(json.dumps(q) for q in requests) + "\n",
        capture_output=True,
        encoding="utf-8",
        timeout=60,
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    values = [
        json.loads(json.loads(s)["result"]["content"][0]["text"])
        for s in result.stdout.splitlines()
    ]
    assert values[0]["previous_reports"] == {"batches": [1]}
    assert ("notebook" in values[0]) == (arm == "N")
    assert report not in json.dumps(values[:2], ensure_ascii=False)
    assert values[2]["text"] == report and not values[2]["final_assay_completed"]
    assert "DO_NOT_DISCLOSE" not in result.stdout
    assert values[3]["events"] == []  # Model reports never become authoritative facts.
    assert "error" in values[4]


def test_report_paging_unsubmitted_exclusion_and_arm_isolation(tmp_path):
    first = UtilityHost(tmp_path, "H", 1, time.time() + 60)
    first.call("finish_batch", {"report": "A\nβ\nC"})
    first.close()
    incomplete = UtilityHost(tmp_path, "H", 2, time.time() + 60)
    incomplete.result["report"] = "NOT_SUBMITTED"
    incomplete.close()
    third = UtilityHost(tmp_path, "H", 3, time.time() + 60)
    try:
        facts = third.docs.authoritative_path.read_bytes()
        result = third.call("lab_reports", {"batch": 1, "offset": 2, "limit": 2})
        assert result["text"] == "β\n" and result["next_offset"] == 4
        for args in ({"batch": "../1"}, {"batch": True}, {"batch": 2}, {"batch": 1, "limit": 0}):
            assert "error" in third.call("lab_reports", args)
        assert "error" in third.call("notebook_write", {"text": "blocked"})
        assert "error" in third.call("finish_batch", {"report": "x", "notebook_text": "blocked"})
        assert third.docs.authoritative_path.read_bytes() == facts
        assert third.docs.notebook_tool("log")["total"] == 0
        assert not any(t["name"].startswith("notebook_") for t in definitions("H"))
    finally:
        third.close()


def test_action_lookup_error_points_to_authoritative_history_without_changing_artifact(tmp_path):
    host = UtilityHost(tmp_path, "H", 1, time.time() + 60)
    try:
        action = {"operation": "add_solvent", "solvent": 2, "volume_L": 0.04}
        event = host.call("lab_step", {"action": action, "reason": "scripted test"})
        key = event["event_id"]
        artifact = tmp_path / "public-artifacts" / f"{key}.json"
        original = artifact.read_bytes()
        failure = host.call("lab_artifact", {"event_id": key, "fields": ["action", "observation"]})
        assert failure["error"] == "ValueError"
        assert f'lab_history(event_ids=["{key}"])' in failure["message"]
        recovered = host.call("lab_history", {"event_ids": [key]})
        assert recovered["events"][0]["action"] == action
        assert artifact.read_bytes() == original and host.steps == 1
        assert "Action parameters are history fields" in next(
            t["description"] for t in base.tool_definitions() if t["name"] == "lab_artifact"
        )
    finally:
        host.close()


def test_matching_world_noise_and_private_single_actor_command(tmp_path):
    for arm in ("H", "N"):
        host = UtilityHost(tmp_path / arm, arm, 4, time.time() + 60)
        try:
            assert host.env.seed == 0 and host.env.observation_seed_override == 4004
            assert host.status()["later_batches_remaining"] == 0
            assert host.tool_budget == 36
        finally:
            host.close()
        args = command(
            SimpleNamespace(codex_executable="codex", model="gpt-5.6-sol"),
            tmp_path / arm,
            arm,
            4,
            time.time() + 60,
        )
        assert args[args.index("multi_agent") - 1] == "--disable"
        server = json.loads(
            next(a.split("=", 1)[1] for a in args if a.startswith("mcp_servers.chemworld.args="))
        )
        assert server[server.index("--batch") + 1] == "4"
        assert server[server.index("--arm") + 1] == arm
        prompt = (tmp_path / arm / "provider/session-4/instructions.md").read_text(encoding="utf-8")
        assert ("versioned hypothesis notebook" in prompt) == (arm == "N")
        assert "lab_reports" in prompt and "FOUR independent" in prompt


def test_aggregate_retains_missing_slots_and_failed_batch_without_provider_payloads(tmp_path):
    host = UtilityHost(tmp_path / "N", "N", 1, time.time() + 60)
    host.call("notebook_write", {"text": "Prospective; no experiment executed."})
    host.close()
    batch = summarize_batch(
        tmp_path / "N", 1, {"usage_complete": False, "transport_failures": [{}]}
    )
    batch["retrievals"] = []
    summary = {
        "arms": {
            "H": {"batches": [], "total_tokens": 0},
            "N": {"batches": [batch], "total_tokens": 0},
        },
        "failures": ["retained"],
    }
    write_outputs(tmp_path, summary)
    data = base.read_json(tmp_path / "aggregate.json")
    slots = [b for a in data["arms"].values() for b in a["batches"]]
    assert len(slots) == 8 and sum(b["executed"] for b in slots) == 1
    assert data["failures"] == ["retained"]
    assert not slots[4]["engineering_passed"] and slots[4]["transport_failure_count"] == 1
    assert "Prospective; no experiment executed." in (tmp_path / "review.md").read_text(
        encoding="utf-8"
    )
