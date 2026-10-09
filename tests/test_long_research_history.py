from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from scripts.run_research_documents_demo import run

from chemworld.agents.experiment_codex_ipc import ExperimentCodexWorkspace
from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.agents.public_history import public_history_page


def history_block(root: Path) -> dict:
    workspace = ExperimentCodexWorkspace(root, history_event_limit=64)
    workspace.initialize_fresh()
    workspace.start_session(session_id="history-test", response_timeout_s=5.0)
    for index in range(80):
        workspace.append_public_history(
            {
                "event_id": f"operation-{index:04d}",
                "synthetic_test": True,
                "action": {"operation": "wait", "duration_s": 1.0},
                "observation": {"crystal_size": None},
                "observed_mask": {"crystal_size": False},
            }
        )
    cached = [json.loads(line) for line in workspace.history_path.read_text().splitlines()]
    assert len(cached) == 64 and cached[0]["event_id"] == "operation-0016"
    # Instantiate the reader only after history is written; neither reader uses host memory.
    server = ChemWorldMCPServer(root)
    retrieved = []
    for offset in range(0, 80, 10):
        response = server._call_tool("history", {"offset": offset, "limit": 10})
        assert not response.get("isError", False)
        mcp = json.loads(response["content"][0]["text"])
        process = subprocess.run(
            [
                sys.executable,
                str(workspace.lab_tool_path),
                "history",
                "--offset",
                str(offset),
                "--limit",
                "10",
            ],
            cwd=workspace.agent_directory,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        cli = json.loads(process.stdout)
        assert {k: v for k, v in mcp.items() if k != "schema_version"} == {
            k: v for k, v in cli.items() if k != "schema_version"
        }
        assert mcp["total_event_count"] == 80
        assert mcp["cache_retained_event_count"] == 64
        assert mcp["cache_truncated"] and mcp["truncated"]
        assert mcp["next_offset"] == (offset + 10 if offset < 70 else None)
        retrieved.extend(mcp["events"])
    assert [r["event_id"] for r in retrieved] == [f"operation-{i:04d}" for i in range(80)]
    assert public_history_page(workspace.public_directory)["offset"] == 75
    assert public_history_page(workspace.public_directory, offset=80)["events"] == []
    return {
        "synthetic_events": 80,
        "retrieved": len(retrieved),
        "cache_retained": 64,
        "first_event": retrieved[0]["event_id"],
        "last_event": retrieved[-1]["event_id"],
        "tool_parity": True,
    }


def test_complete_history_survives_recent_cache_eviction_in_both_bridges(tmp_path):
    history_block(tmp_path / "workspace")


@pytest.mark.parametrize("arguments", [{"offset": -1}, {"offset": True}, {"limit": False}])
def test_history_rejects_invalid_page_coordinates(tmp_path, arguments):
    with pytest.raises(ValueError):
        public_history_page(tmp_path, **arguments)


def test_missing_archive_does_not_report_an_empty_complete_history(tmp_path):
    (tmp_path / "history.jsonl").write_text('{"event_id":"old"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="complete public history is unavailable"):
        public_history_page(tmp_path)


def test_history_byte_budget_preserves_events_and_provides_next_offset(tmp_path):
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace", max_tool_output_bytes=2048)
    workspace.initialize_fresh()
    workspace.start_session(session_id="byte-test", response_timeout_s=5.0)
    for index in range(4):
        workspace.append_public_history({"index": index, "text": "测量" * 100})
    server = ChemWorldMCPServer(workspace.root)
    forward = server._call_tool("history", {"offset": 0, "limit": 10})
    assert not forward["isError"]
    assert len(forward["content"][0]["text"].encode("utf-8")) <= 2048
    page = json.loads(forward["content"][0]["text"])
    assert [e["index"] for e in page["events"]] == [0, 1]
    assert page["next_offset"] == 2
    recent = public_history_page(workspace.public_directory, max_bytes=1920)
    assert recent["offset"] == 2
    assert [e["index"] for e in recent["events"]] == [2, 3]
    workspace.append_public_history({"index": 4, "text": "x" * 1950})
    oversized = public_history_page(workspace.public_directory, offset=4, max_bytes=1920)
    assert oversized["events"] == []
    assert oversized["oversized_event"]["offset"] == 4
    assert oversized["next_offset"] == 4  # No silent skip.
    rows = workspace.operation_history_path.read_text(encoding="utf-8").splitlines()
    assert json.loads(rows[4])["text"] == "x" * 1950


def test_offline_documents_adapter_retains_failure_and_restarts(tmp_path):
    output = tmp_path / "demo"
    summary = run(output)
    assert summary["operation_count"] == 6
    assert summary["failed_count"] == 1
    assert summary["committed_count"] == 5
    assert summary["final_assay"] and summary["replay"]["verified"]
    code = (
        "import json,sys; from pathlib import Path; "
        "from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace; "
        "from chemworld.data.logging import load_jsonl; "
        "from chemworld.eval.verify import verify_records; "
        "p=Path(sys.argv[1]); s=json.loads((p/'summary.json').read_text()); "
        "w=ExperimentDocumentWorkspace(p); "
        "w.initialize(expected_authoritative_sha256="
        "s['documents']['authoritative_ledger']['sha256']); "
        "assert 'Prediction before execution' in w.read_notebook(); "
        "assert verify_records(load_jsonl(p/'trajectory.jsonl'),tolerance=0.).verified; "
        "print(w.manifest()['authoritative_ledger']['line_count'])"
    )
    process = subprocess.run(
        [sys.executable, "-c", code, str(output)],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    assert process.stdout.strip() == "6"
