from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

from scripts.run_hypothesis_notebook_pilot import PilotHost
from scripts.run_long_horizon_notebook_review import (
    ResearchHost,
    command,
    notebook_timeline,
    summarize_batch,
    write_review,
)
from scripts.run_notebook_environment_pilot import OPERATIONS

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records


def actions():
    return [
        {"operation": "add_solvent", "solvent": 0, "volume_L": 0.03},
        {"operation": "add_reagent", "amount_mol": 0.012},
        {
            "operation": "heat",
            "target_temperature_K": 350,
            "duration_s": 600,
            "stirring_speed_rpm": 600,
        },
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def test_noise_is_separate_and_every_batch_replays(tmp_path):
    observations = []
    for batch in (1, 2):
        host = ResearchHost(tmp_path, "A", batch, time.time() + 60)
        assert host.env.seed == 0 and host.env.observation_seed_override == 1000 + batch
        try:
            for action in actions():
                outcome = host.call("lab_step", {"action": action, "reason": "test only"})
                assert outcome.get("transaction_status") == "committed"
            observations.append(outcome["observation"])
            host.call("finish_batch", {"report": "scripted test"})
        finally:
            host.close()
        trajectory = load_jsonl(tmp_path / f"batch-{batch}" / "trajectory.jsonl")
        assert trajectory[0]["observation_seed"] == 1000 + batch
        assert verify_records(trajectory, tolerance=0).verified
    assert observations[0] != observations[1]


def test_review_retains_timing_invalid_references_and_missing_slots(tmp_path):
    root = tmp_path / "A"
    host = ResearchHost(root, "A", 1, time.time() + 60)
    try:
        host.call("notebook_write", {"text": "BEFORE_EXPECTATION_SENTINEL"})
        for action in actions():
            host.call("lab_step", {"action": action, "reason": "scripted reason"})
        host.call(
            "notebook_write",
            {"text": "AFTER_SENTINEL batch-1-operation-006; unsupported: batch-6-operation-006"},
        )
        host.call("finish_batch", {"report": "REPORT_SENTINEL"})
    finally:
        host.close()
    provider = {
        "usage_complete": True,
        "exit_code": 0,
        "stop_reason": None,
        "transport_failures": [],
    }
    result = summarize_batch(root, 1, provider)
    assert result["engineering_passed"]
    assert result["pre_first_action_revisions"] == [1]
    assert result["post_last_action_revisions"] == [2]
    assert notebook_timeline(root)[1]["unavailable_references_at_commit"] == [
        "batch-6-operation-006"
    ]
    summary = {"campaigns": {"A": {"batches": [result]}}, "failures": []}
    before = (root / "research/experiment_documents/model_owned_notebook.md").read_bytes()
    write_review(tmp_path, summary)
    text = (tmp_path / "review.md").read_text(encoding="utf-8")
    assert "BEFORE_EXPECTATION_SENTINEL" in text and "REPORT_SENTINEL" in text
    assert "batch-6-operation-006" in text and text.count("未执行 |") == 11
    assert before == (root / "research/experiment_documents/model_owned_notebook.md").read_bytes()


def test_new_stdio_session_exposes_metadata_not_note_body(tmp_path):
    initial = PilotHost(tmp_path, 1)
    initial.call("notebook_write", {"text": "PERSISTENT_RESEARCH_INTENT"})
    initial.close()
    queries = [
        {
            "jsonrpc": "2.0",
            "id": i,
            "method": "tools/call",
            "params": {"name": name, "arguments": {}},
        }
        for i, name in enumerate(("lab_status", "notebook_read"), 1)
    ]
    queries += [
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "lab_schema", "arguments": {"operations": sorted(OPERATIONS)}},
        },
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "lab_status"}},
    ]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.run_long_horizon_notebook_review",
            "--serve",
            "--output",
            str(tmp_path),
            "--campaign",
            "A",
            "--batch",
            "2",
            "--deadline",
            str(time.time() + 60),
        ],
        input="\n".join(json.dumps(q) for q in queries) + "\n",
        capture_output=True,
        encoding="utf-8",
        check=True,
        timeout=60,
        cwd=Path(__file__).resolve().parents[1],
    )
    responses = result.stdout.splitlines()
    assert len(responses) == 4
    schemas = json.loads(json.loads(responses[2])["result"]["content"][0]["text"])
    assert set(schemas) == OPERATIONS
    assert "PERSISTENT_RESEARCH_INTENT" not in responses[0]
    assert "PERSISTENT_RESEARCH_INTENT" in responses[1]
    assert (
        json.loads(json.loads(responses[0])["result"]["content"][0]["text"])[
            "later_batches_remaining"
        ]
        == 4
    )


def test_unexecuted_batch_retains_note_and_failed_finish_message(tmp_path):
    root = tmp_path / "A"
    host = ResearchHost(root, "A", 1, time.time() + 60)
    host.call("notebook_write", {"text": "PROSPECTIVE_PLAN_SENTINEL"})
    host.close()
    folder = root / "provider/session-1"
    folder.mkdir(parents=True)
    (folder / "stdout.jsonl").write_text(
        json.dumps(
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": "NO_EXPERIMENT_PERFORMED_SENTINEL"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    failure = {"id": "item_9", "tool": "finish_batch", "error": {"message": "Transport closed"}}
    provider = {"usage_complete": True, "exit_code": 0, "transport_failures": [failure]}
    result = summarize_batch(root, 1, provider)
    assert not result["engineering_passed"]
    assert result["notes_without_physical_actions"] == [1]
    assert result["cli_last_public_message"] == "NO_EXPERIMENT_PERFORMED_SENTINEL"
    assert not result["host"].get("report")
    write_review(tmp_path, {"campaigns": {"A": {"batches": [result]}}, "failures": [failure]})
    report = (tmp_path / "review.md").read_text(encoding="utf-8")
    assert "PROSPECTIVE_PLAN_SENTINEL" in report and "Transport closed" in report
    assert "NO_EXPERIMENT_PERFORMED_SENTINEL" in report


def test_runner_uses_correct_batch_and_keeps_single_actor(tmp_path):
    args = command(
        SimpleNamespace(codex_executable="codex", model="gpt-5.6-sol"),
        tmp_path,
        "B",
        6,
        time.time() + 60,
    )
    assert args[args.index("multi_agent") - 1] == "--disable"
    server = json.loads(
        next(a.split("=", 1)[1] for a in args if a.startswith("mcp_servers.chemworld.args="))
    )
    assert server[server.index("--batch") + 1] == "6"
    assert server[server.index("--campaign") + 1] == "B"
    instructions = (tmp_path / "provider/session-6/instructions.md").read_text(encoding="utf-8")
    assert "FOR A HUMAN RESEARCHER" in instructions and "comparability" in instructions
