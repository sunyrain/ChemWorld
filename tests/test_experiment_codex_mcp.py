from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, TextIO

from chemworld.agents.experiment_codex_ipc import ExperimentCodexWorkspace
from chemworld.agents.experiment_codex_mcp import (
    MCP_SERVER_VERSION,
    SUPPORTED_TOOLS,
    ChemWorldMCPServer,
)


def test_final_response_contract_matches_session_scope() -> None:
    assert ChemWorldMCPServer._final_response_contract(campaign=True) == {
        "format": "json_object_only",
        "required_keys": ["status", "summary"],
        "status": "campaign_complete",
        "summary_max_length": 3000,
        "final_recommendation_contract": {
            "selected_experiment_index": (
                "1-based_integer_identifying_a_completed_experiment"
            ),
            "selection_rationale_max_length": 2000,
            "committed_before_blind_evaluation": True,
        },
        "prose_or_markdown_allowed": False,
    }
    assert ChemWorldMCPServer._final_response_contract(campaign=False)["status"] == (
        "experiment_complete"
    )


def _write_request(stream: TextIO, request_id: int, method: str, params: Any) -> None:
    stream.write(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            },
            separators=(",", ":"),
        )
        + "\n"
    )
    stream.flush()


def _read_response(stream: TextIO) -> dict[str, Any]:
    response = json.loads(stream.readline())
    assert isinstance(response, dict)
    return response


def test_host_owned_stdio_mcp_round_trip(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information(
        {"condition_id": "opaque_codes", "materials": ["M1", "M2"]}
    )
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id="experiment-0001-test",
        expected_step=1,
        response_timeout_s=10.0,
    )

    project_root = Path(__file__).resolve().parents[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "chemworld.agents.experiment_codex_mcp",
            "--workspace",
            str(workspace.root),
        ],
        cwd=project_root,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    assert process.stdin is not None
    assert process.stdout is not None
    try:
        _write_request(
            process.stdin,
            1,
            "initialize",
            {"protocolVersion": "2025-06-18", "capabilities": {}},
        )
        initialized = _read_response(process.stdout)["result"]
        assert initialized["serverInfo"]["version"] == MCP_SERVER_VERSION

        _write_request(process.stdin, 2, "tools/list", {})
        tools = _read_response(process.stdout)["result"]["tools"]
        assert {item["name"] for item in tools} == set(SUPPORTED_TOOLS)

        _write_request(
            process.stdin,
            3,
            "tools/call",
            {"name": "material_information", "arguments": {}},
        )
        material_result = _read_response(process.stdout)["result"]
        material = json.loads(material_result["content"][0]["text"])
        assert material["condition_id"] == "opaque_codes"

        action = {"operation": "terminate"}
        _write_request(
            process.stdin,
            4,
            "tools/call",
            {
                "name": "step",
                "arguments": {"expected_step": 1, "action": action},
            },
        )
        request = workspace.wait_for_request(
            session_id="experiment-0001-test",
            expected_step=1,
            timeout_s=5.0,
            process_alive=lambda: process.poll() is None,
            handled_request_ids=set(),
        )
        assert request.action == action
        workspace.write_response(
            session_id=request.session_id,
            request_id=request.request_id,
            response={
                "ok": True,
                "experiment_ended": True,
                "leaderboard_score": 0.25,
            },
        )
        step_result = _read_response(process.stdout)["result"]
        outcome = json.loads(step_result["content"][0]["text"])
        assert outcome["experiment_ended"] is True

        _write_request(process.stdin, 5, "tools/call", {"name": "status", "arguments": {}})
        terminal_status = _read_response(process.stdout)["result"]
        terminal_payload = json.loads(terminal_status["content"][0]["text"])
        assert terminal_payload["experiment_ended"] is True
        assert "final response" in terminal_payload["instruction"]

        _write_request(
            process.stdin,
            6,
            "tools/call",
            {
                "name": "step",
                "arguments": {
                    "expected_step": 2,
                    "action": {"operation": "add_reagent", "amount_mol": 0.01},
                },
            },
        )
        rejected_step = _read_response(process.stdout)["result"]
        assert rejected_step["isError"] is True
        rejected_payload = json.loads(rejected_step["content"][0]["text"])
        assert rejected_payload["error"] == (
            "RuntimeError: campaign_already_ended_submit_final_response"
        )

        audit = workspace.mcp_tool_call_audit("experiment-0001-test")
        assert [row["tool"] for row in audit] == [
            "material_information",
            "step",
            "status",
            "step",
        ]
        assert all(row["started_at"] for row in audit)
        assert all(row["duration_ms"] >= 0.0 for row in audit)
        assert [row["status"] for row in audit] == [
            "completed",
            "completed",
            "completed",
            "failed",
        ]
        assert audit[-1]["error_type"] == "RuntimeError"
        requests = workspace.session_root("experiment-0001-test") / "mcp_requests"
        assert len(list(requests.glob("*.json"))) == 1
        assert list(
            (workspace.transport_session_root("experiment-0001-test") / "requests").glob(
                "*.json"
            )
        ) == []
    finally:
        process.stdin.close()
        process.wait(timeout=5.0)


def test_step_validation_error_exposes_bounded_repair_detail(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id="experiment-validation-detail-test",
        expected_step=1,
        response_timeout_s=10.0,
    )
    server = ChemWorldMCPServer(workspace.root)

    result = server._call_tool(
        "step",
        {"action": {"operation": "terminate"}, "request_id": "missing-step"},
    )

    assert result["isError"] is True
    payload = json.loads(result["content"][0]["text"])
    assert payload["error"] == "ValueError: expected_step must be an integer"
    audit = workspace.mcp_tool_call_audit("experiment-validation-detail-test")
    assert len(audit) == 1
    assert audit[0]["error_type"] == "ValueError"
    assert audit[0]["error_code"] == "invalid_expected_step"
    assert audit[0]["error_field_path"] == "expected_step"
    assert audit[0]["error_detail"] == "expected_step must be an integer"
    assert audit[0]["error_detail_byte_count"] > 0
    assert len(audit[0]["error_detail_sha256"]) == 64
    assert "arguments" not in audit[0]


def test_campaign_tool_schema_exposes_snapshot_and_decision_audit(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_belief_checkpoint_contract(
        {
            "snapshot_stages": [
                "pre_evidence",
                "after_experiment_1",
                "after_experiment_2",
                "final",
            ],
            "checkpoint_complete_experiments": [0, 1, 2, 4],
            "query_metric_contract": {"q0": ["score"]},
            "allowed_feature_ids": ["potential_V"],
            "allowed_metric_ids": ["score"],
            "allowed_prior_fields": ["solvent"],
            "evidence_catalog": ["experiment-1-final-assay"],
            "nominal_information_available": False,
        }
    )
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id="campaign-0001-test",
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="campaign",
    )
    project_root = Path(__file__).resolve().parents[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "chemworld.agents.experiment_codex_mcp",
            "--workspace",
            str(workspace.root),
        ],
        cwd=project_root,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    assert process.stdin is not None
    assert process.stdout is not None
    try:
        _write_request(process.stdin, 1, "tools/list", {})
        tools = _read_response(process.stdout)["result"]["tools"]
        by_name = {item["name"]: item for item in tools}
        step_schema = by_name["step"]["inputSchema"]
        assert "decision_audit" in step_schema["required"]
        assert set(step_schema["properties"]["decision_audit"]["required"]) == {
            "expected_effect",
            "diagnostic_target",
            "expected_information_gain",
            "belief_update_rule",
            "uncertainty",
            "adaptation_source",
        }
        snapshot = by_name["commit_belief_snapshot"]["inputSchema"]["properties"][
            "snapshot"
        ]
        assert snapshot["properties"]["schema_version"]["const"].startswith(
            "chemworld-work-ii-belief-snapshot"
        )
        assert "law_summary" in snapshot["required"]
        recommendation = by_name["commit_final_recommendation"]["inputSchema"]
        assert recommendation["properties"]["selected_experiment_index"]["maximum"] == 4
    finally:
        process.stdin.close()
        process.wait(timeout=5.0)


def test_final_recommendation_is_campaign_terminal_checkpoint_bound_and_idempotent(
    tmp_path: Path,
) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_belief_checkpoint_contract(
        {
            "snapshot_stages": [
                "pre_evidence",
                "after_experiment_1",
                "after_experiment_2",
                "final",
            ],
            "checkpoint_complete_experiments": [0, 1, 2, 4],
            "query_metric_contract": {"q0": ["score"]},
            "allowed_feature_ids": ["potential_V"],
            "allowed_metric_ids": ["score"],
            "allowed_prior_fields": ["solvent"],
            "evidence_catalog": ["experiment-1-final-assay"],
            "nominal_information_available": False,
        }
    )
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id="campaign-final-recommendation-test",
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="campaign",
    )
    session_root = workspace.session_root("campaign-final-recommendation-test")
    snapshots = session_root / "belief_snapshots"
    snapshots.mkdir()
    for index in range(4):
        (snapshots / f"{index + 1:02d}-stage.json").write_text("{}", encoding="utf-8")
    for index in range(4):
        workspace.append_public_history(
            {
                "experiment_ended": True,
                "campaign_ended": index == 3,
                "evidence_id": f"experiment-{index + 1}-final-assay",
            }
        )
    server = ChemWorldMCPServer(workspace.root)
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "best public evidence",
    }

    committed = server._call_tool("commit_final_recommendation", recommendation)
    assert committed["isError"] is False
    committed_payload = json.loads(committed["content"][0]["text"])
    assert committed_payload["already_committed"] is False
    assert workspace.final_recommendation_audit("campaign-final-recommendation-test")[
        "recommendation"
    ] == recommendation

    repeated = server._call_tool("commit_final_recommendation", recommendation)
    assert repeated["isError"] is False
    assert json.loads(repeated["content"][0]["text"])["already_committed"] is True

    conflicting = server._call_tool(
        "commit_final_recommendation",
        {
            "selected_experiment_index": 3,
            "selection_rationale": "different choice",
        },
    )
    assert conflicting["isError"] is True
    assert "different final recommendation" in json.loads(
        conflicting["content"][0]["text"]
    )["error"]


def test_final_recommendation_is_rejected_outside_campaign(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id="experiment-final-recommendation-test",
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="experiment",
    )
    server = ChemWorldMCPServer(workspace.root)
    result = server._call_tool(
        "commit_final_recommendation",
        {"selected_experiment_index": 1, "selection_rationale": "not allowed"},
    )
    assert result["isError"] is True
    assert "campaign sessions" in json.loads(result["content"][0]["text"])["error"]
