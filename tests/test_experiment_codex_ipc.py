from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from chemworld.agents.experiment_codex_ipc import (
    EXPERIMENT_CODEX_IPC_VERSION,
    ExperimentCodexIPCError,
    ExperimentCodexWorkspace,
)


def _run_tool(workspace: ExperimentCodexWorkspace, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(workspace.lab_tool_path), *args],
        cwd=workspace.agent_directory,
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )


def test_workspace_starts_with_empty_optional_agent_directory(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell")
    manifest = workspace.initialize_fresh()
    expected_host_files = ["lab_tool.py", "python.cmd"] if os.name == "nt" else ["lab_tool.py"]
    assert sorted(path.name for path in workspace.agent_directory.iterdir()) == sorted(
        expected_host_files
    )
    assert manifest["authoritative_trajectory_in_workspace"] is False
    assert manifest["agent_directory"]["required_files"] == ["lab_tool.py"]
    assert (manifest["python_command_shim"] is not None) is (os.name == "nt")
    assert manifest["lab_tool"]["relative_path"] == "agent/lab_tool.py"
    assert manifest["lab_tool"]["writable_by_topology"] is True
    assert manifest["lab_tool"]["authoritative"] is False
    assert manifest["lab_tool"]["sha256"] == manifest["lab_tool"]["expected_sha256"]

    material = workspace.publish_material_information(
        {"material_information": {"mode": "opaque_codes"}, "material_catalog": {}}
    )
    task = workspace.publish_task_contract(
        {"task_id": "task-a", "scoring_contract": {"yield": 0.5}}
    )
    assert material["relative_path"] == "reference/material_information.json"
    assert task["relative_path"] == "reference/task_contract.json"
    assert workspace.snapshot_agent_files() == {}


def test_workspace_refuses_stale_cell_instead_of_reusing_memory(tmp_path: Path) -> None:
    root = tmp_path / "cell"
    root.mkdir()
    (root / "stale.txt").write_text("old", encoding="utf-8")
    with pytest.raises(FileExistsError):
        ExperimentCodexWorkspace(root).initialize_fresh()


def test_agent_transport_cannot_contain_host_response_by_topology(
    tmp_path: Path,
) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell")
    workspace.initialize_fresh()
    workspace.start_session(session_id="session-a", response_timeout_s=5.0)

    request_root = workspace.transport_session_root("session-a") / "requests"
    response_root = workspace.response_path("session-a", "request-a").parent
    assert request_root.is_relative_to(workspace.agent_directory)
    assert not response_root.is_relative_to(workspace.agent_directory)
    assert response_root == (workspace.root / ".ipc" / "sessions" / "session-a" / "responses")
    manifest = workspace.manifest()
    assert manifest["transport"]["contains_host_responses"] is False
    assert workspace.snapshot_agent_files() == {}


def test_lab_tool_status_history_and_artifact_inspection_are_bounded(
    tmp_path: Path,
) -> None:
    workspace = ExperimentCodexWorkspace(
        tmp_path / "cell",
        max_tool_output_bytes=2048,
        history_event_limit=12,
        history_byte_limit=8192,
    )
    workspace.initialize_fresh()
    workspace.publish_current({"step": 3, "legal_actions": [{"operation": "measure"}]})
    for index in range(12):
        workspace.append_public_history(
            {"event_id": f"event-{index}", "action": {"operation": "heat"}}
        )
    workspace.publish_artifact(
        artifact_id="spectrum-1",
        payload={"raw_signal": {"intensity": list(range(300))}},
    )
    workspace.start_session(
        session_id="session-a",
        response_timeout_s=5.0,
    )

    status = _run_tool(workspace, "status")
    assert status.returncode == 0
    assert json.loads(status.stdout)["step"] == 3

    history = _run_tool(workspace, "history", "--limit", "100")
    assert history.returncode == 0
    history_payload = json.loads(history.stdout)
    assert history_payload["authoritative"] is False
    assert len(history_payload["events"]) == 10

    first = _run_tool(
        workspace,
        "inspect",
        "--artifact-id",
        "spectrum-1",
        "--offset",
        "0",
        "--limit",
        "300",
    )
    assert first.returncode == 0
    fragment = json.loads(first.stdout)
    assert fragment["artifact_id"] == "spectrum-1"
    assert fragment["next_offset"] == 300
    assert len(first.stdout.encode("utf-8")) <= 2048
    audit = workspace.artifact_access_audit("session-a")
    assert audit == [
        {
            "artifact_id": "spectrum-1",
            "limit": 300,
            "offset": 0,
            "returned_character_count": 300,
            "total_character_count": fragment["total_character_count"],
        }
    ]


def test_lab_tool_step_round_trip_is_idempotent(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell", poll_interval_s=0.01)
    workspace.initialize_fresh()
    workspace.publish_current({"step": 1})
    workspace.start_session(session_id="session-a", response_timeout_s=5.0)
    request_file = workspace.agent_directory / "request.json"
    request_file.write_text(
        json.dumps(
            {
                "expected_step": 1,
                "action": {"operation": "add_reagent", "amount_mol": 0.01},
            }
        ),
        encoding="utf-8",
    )
    process = subprocess.Popen(
        [
            sys.executable,
            str(workspace.lab_tool_path),
            "step",
            "--request-file",
            "request.json",
        ],
        cwd=workspace.agent_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    request = workspace.wait_for_request(
        session_id="session-a",
        expected_step=1,
        timeout_s=5.0,
        process_alive=lambda: process.poll() is None,
        handled_request_ids=set(),
    )
    assert request.action["operation"] == "add_reagent"
    workspace.write_response(
        session_id="session-a",
        request_id=request.request_id,
        response={"ok": True, "event_id": "event-1"},
    )
    stdout, _ = process.communicate(timeout=5)
    assert process.returncode == 0
    assert json.loads(stdout)["event_id"] == "event-1"

    repeated = _run_tool(
        workspace,
        "step",
        "--request-file",
        "request.json",
    )
    assert repeated.returncode == 0
    assert json.loads(repeated.stdout)["event_id"] == "event-1"
    assert (
        len(list((workspace.transport_session_root("session-a") / "requests").glob("*.json"))) == 1
    )


def test_lab_tool_inline_action_round_trip(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell", poll_interval_s=0.01)
    workspace.initialize_fresh()
    workspace.publish_current({"step": 1})
    workspace.start_session(session_id="session-a", response_timeout_s=5.0)
    process = subprocess.Popen(
        [
            sys.executable,
            str(workspace.lab_tool_path),
            "step",
            "--expected-step",
            "1",
            "--action-json",
            '{"operation":"set_temperature","temperature_C":55.0}',
        ],
        cwd=workspace.agent_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    request = workspace.wait_for_request(
        session_id="session-a",
        expected_step=1,
        timeout_s=5.0,
        process_alive=lambda: process.poll() is None,
        handled_request_ids=set(),
    )
    assert request.action == {"operation": "set_temperature", "temperature_C": 55.0}
    workspace.verify_lab_tool()
    workspace.write_response(
        session_id="session-a",
        request_id=request.request_id,
        response={"ok": True, "event_id": "event-inline"},
    )
    stdout, _ = process.communicate(timeout=5)
    assert process.returncode == 0
    assert json.loads(stdout)["event_id"] == "event-inline"


def test_expected_step_mismatch_never_reaches_environment(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell", poll_interval_s=0.01)
    workspace.initialize_fresh()
    workspace.start_session(session_id="session-a", response_timeout_s=5.0)
    requests = workspace.transport_session_root("session-a") / "requests"
    wrong = {
        "schema_version": EXPERIMENT_CODEX_IPC_VERSION,
        "session_id": "session-a",
        "request_id": "wrong",
        "expected_step": 7,
        "action": {"operation": "terminate"},
    }
    (requests / "wrong.json").write_text(json.dumps(wrong), encoding="utf-8")

    with pytest.raises(TimeoutError):
        workspace.wait_for_request(
            session_id="session-a",
            expected_step=1,
            timeout_s=0.05,
            process_alive=lambda: True,
            handled_request_ids=set(),
        )
    response = json.loads(workspace.response_path("session-a", "wrong").read_text(encoding="utf-8"))
    assert response["error"] == "expected_step_mismatch"


def test_public_cache_and_tool_script_integrity_fail_closed(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(
        tmp_path / "cell",
        max_tool_output_bytes=1024,
        history_byte_limit=2048,
    )
    workspace.initialize_fresh()
    with pytest.raises(ExperimentCodexIPCError, match="hard cap"):
        workspace.publish_current({"oversized": "x" * 4000})

    workspace.lab_tool_path.write_text("tampered", encoding="utf-8")
    with pytest.raises(ExperimentCodexIPCError, match="changed"):
        workspace.verify_lab_tool()


def test_history_cache_is_rebuilt_from_host_memory_not_workspace_contents(
    tmp_path: Path,
) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "cell")
    workspace.initialize_fresh()
    workspace.append_public_history({"event_id": "event-1"})
    workspace.history_path.write_text("not-jsonl", encoding="utf-8")
    workspace.append_public_history({"event_id": "event-2"})

    rows = [
        json.loads(line) for line in workspace.history_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [row["event_id"] for row in rows] == ["event-1", "event-2"]
