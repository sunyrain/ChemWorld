from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, TextIO

from chemworld.agents.experiment_codex_ipc import ExperimentCodexWorkspace
from chemworld.agents.experiment_codex_mcp import (
    BELIEF_SNAPSHOT_SHAPE_GUIDE,
    MCP_SERVER_VERSION,
    STAGED_BELIEF_SNAPSHOT_GUIDE,
    SUPPORTED_TOOLS,
    ChemWorldMCPServer,
)
from chemworld.eval.work_ii_prior_discovery import (
    WORK_II_LAW_SUMMARY_SCHEMA_VERSION,
    WORK_II_SNAPSHOT_SCHEMA_VERSION,
)


def test_final_response_contract_matches_session_scope() -> None:
    assert ChemWorldMCPServer._final_response_contract(campaign=True) == {
        "format": "json_object_only",
        "required_keys": ["status", "summary"],
        "status": "campaign_complete",
        "summary_max_length": 3000,
        "final_recommendation_contract": {
            "selected_experiment_index": ("1-based_integer_identifying_a_completed_experiment"),
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
        assert "tools/list are the sole executable authority" in initialized["instructions"]
        assert "host filesystem paths" in initialized["instructions"]

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
        assert (
            list(
                (workspace.transport_session_root("experiment-0001-test") / "requests").glob(
                    "*.json"
                )
            )
            == []
        )
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
    assert payload["error_code"] == "invalid_expected_step"
    assert payload["field_path"] == "expected_step"
    assert payload["expected"] == {"type": "integer", "minimum": 1}
    assert payload["observed"] is None
    assert payload["schema_fragment"] == payload["expected"]
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
        snapshot = by_name["commit_belief_snapshot"]["inputSchema"]
        assert snapshot["properties"]["action"]["enum"] == [
            "begin",
            "append_prediction_page",
            "append_law_page",
            "finalize",
        ]
        assert "oneOf" not in json.dumps(snapshot)
        header = snapshot["properties"]["snapshot_header"]
        assert "prior_assessment" in header["required"]
        assert set(header["properties"]["prior_assessment"]["required"]) == {
            "nominal_information_available",
            "reliability_probability",
            "suspected_misindexed_fields",
            "rationale",
        }
        assert "metric_laws" not in header["properties"]["law_summary"]["properties"]
        assert snapshot["properties"]["predictions"]["maxItems"] == 4
        metric_laws = snapshot["properties"]["metric_laws"]
        assert metric_laws["maxItems"] == 2
        assert "link" in metric_laws["items"]["required"]
        assert "sole participant-facing authority" in by_name[
            "commit_belief_snapshot"
        ]["description"]
        assert STAGED_BELIEF_SNAPSHOT_GUIDE in by_name["commit_belief_snapshot"]["description"]
        assert BELIEF_SNAPSHOT_SHAPE_GUIDE not in by_name["commit_belief_snapshot"]["description"]
        assert snapshot["properties"]["predictions"]["items"]["properties"]["metrics"][
            "items"
        ]["required"] == [
            "metric_id",
            "mean",
            "interval_lower",
            "interval_upper",
            "confidence",
        ]
        assert "snapshot" not in snapshot["properties"]
        assert "checkpoint_due=true" in by_name["step"]["description"]
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
    assert (
        workspace.final_recommendation_audit("campaign-final-recommendation-test")["recommendation"]
        == recommendation
    )

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
    assert (
        "different final recommendation" in json.loads(conflicting["content"][0]["text"])["error"]
    )


def test_campaign_status_exposes_checkpoint_and_closeout_state(tmp_path: Path) -> None:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_belief_checkpoint_contract(
        {
            "snapshot_stages": ["pre_evidence", "final"],
            "checkpoint_complete_experiments": [0, 1],
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
        session_id="campaign-status-test",
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="campaign",
    )
    server = ChemWorldMCPServer(workspace.root)

    initial = server._status()
    assert initial["campaign_closeout"] | {"belief_snapshot_submission": None} == {
        "campaign_ended": False,
        "complete_experiment_count": 0,
        "committed_checkpoint_count": 0,
        "required_checkpoint_count": 2,
        "checkpoint_due": True,
        "next_checkpoint_stage": "pre_evidence",
        "next_checkpoint_complete_experiment_count": 0,
        "final_recommendation_committed": False,
        "belief_snapshot_submission": None,
    }
    submission = initial["campaign_closeout"]["belief_snapshot_submission"]
    assert submission["submission_order"] == ["predictions-001", "laws-001"]
    assert submission["next_page_id"] == "predictions-001"

    snapshot_root = workspace.session_root("campaign-status-test") / "belief_snapshots"
    snapshot_root.mkdir()
    (snapshot_root / "01-pre_evidence.json").write_text("{}", encoding="utf-8")
    workspace.append_public_history(
        {
            "experiment_ended": True,
            "campaign_ended": True,
            "evidence_id": "experiment-1-final-assay",
        }
    )
    terminal = server._status()
    assert terminal["campaign_closeout"]["campaign_ended"] is True
    assert terminal["campaign_closeout"]["checkpoint_due"] is True
    assert terminal["campaign_closeout"]["next_checkpoint_stage"] == "final"
    assert terminal["campaign_closeout"]["next_checkpoint_complete_experiment_count"] == 1

    server._terminal_outcome = {"campaign_ended": True, "experiment_ended": True}
    terminal_after_step_return = server._status()
    assert terminal_after_step_return["experiment_ended"] is True
    assert terminal_after_step_return["campaign_closeout"]["checkpoint_due"] is True
    assert terminal_after_step_return["campaign_closeout"]["next_checkpoint_stage"] == "final"


def _campaign_workspace(tmp_path: Path, session_id: str) -> ExperimentCodexWorkspace:
    workspace = ExperimentCodexWorkspace(tmp_path / "workspace")
    workspace.initialize_fresh()
    workspace.publish_material_information({"condition_id": "opaque_codes"})
    workspace.publish_task_contract({"task_id": "test"})
    workspace.publish_belief_checkpoint_contract(
        {
            "snapshot_stages": ["pre_evidence", "after_experiment_2", "final"],
            "checkpoint_complete_experiments": [0, 2, 4],
            "query_metric_contract": {"q0": ["score"]},
            "allowed_feature_ids": ["potential_V"],
            "allowed_metric_ids": ["score"],
            "allowed_prior_fields": ["solvent"],
            "evidence_catalog": [
                "experiment-1-final-assay",
                "experiment-2-final-assay",
                "experiment-3-final-assay",
                "experiment-4-final-assay",
            ],
            "nominal_information_available": False,
        }
    )
    workspace.publish_current({"expected_step": 1, "available_actions": []})
    workspace.start_session(
        session_id=session_id,
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="campaign",
    )
    return workspace


def _minimal_snapshot(*, stage: str = "pre_evidence") -> dict[str, Any]:
    return {
        "schema_version": WORK_II_SNAPSHOT_SCHEMA_VERSION,
        "snapshot_id": f"snapshot-{stage}",
        "stage": stage,
        "prior_assessment": {
            "nominal_information_available": False,
            "reliability_probability": None,
            "suspected_misindexed_fields": [],
            "rationale": "No nominal dossier is available.",
        },
        "predictions": [
            {
                "query_id": "q0",
                "metrics": [
                    {
                        "metric_id": "score",
                        "mean": 0.5,
                        "interval_lower": 0.0,
                        "interval_upper": 1.0,
                        "confidence": 0.25,
                    }
                ],
            }
        ],
        "law_summary": {
            "schema_version": WORK_II_LAW_SUMMARY_SCHEMA_VERSION,
            "summary_id": f"law-{stage}",
            "feature_ids": ["potential_V"],
            "metric_laws": [
                {
                    "metric_id": "score",
                    "intercept": 0.5,
                    "link": "identity",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "terms": [],
                }
            ],
            "evidence_ids": [],
            "applicability": "Public query domain only.",
            "limitations": ["No experimental evidence yet."],
            "confidence": 0.25,
        },
        "evidence_ids": [],
        "next_experiment_intent": "Run a bounded discriminating experiment.",
        "overall_confidence": 0.25,
    }


def _staged_header(snapshot: dict[str, Any]) -> dict[str, Any]:
    law_summary = dict(snapshot["law_summary"])
    law_summary.pop("metric_laws")
    return {
        "snapshot_id": snapshot["snapshot_id"],
        "stage": snapshot["stage"],
        "prior_assessment": snapshot["prior_assessment"],
        "law_summary": law_summary,
        "evidence_ids": snapshot["evidence_ids"],
        "next_experiment_intent": snapshot["next_experiment_intent"],
        "overall_confidence": snapshot["overall_confidence"],
    }


def test_staged_belief_snapshot_is_exact_immutable_and_canonical(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-staged-snapshot-test")
    server = ChemWorldMCPServer(workspace.root)
    snapshot = _minimal_snapshot()

    material = server._call_tool("material_information", {})
    material_payload = json.loads(material["content"][0]["text"])
    plan = material_payload["belief_snapshot_submission"]
    assert plan["prediction_pages"] == [
        {
            "page_id": "predictions-001",
            "query_metric_contract": {"q0": ["score"]},
        }
    ]
    assert plan["law_pages"] == [{"page_id": "laws-001", "metric_ids": ["score"]}]

    begun = server._call_tool(
        "commit_belief_snapshot",
        {"action": "begin", "snapshot_header": _staged_header(snapshot)},
    )
    assert begun["isError"] is False
    assert workspace.belief_snapshot_audit("campaign-staged-snapshot-test") == []

    blocked = server._call_tool(
        "step",
        {
            "expected_step": 1,
            "action": {"operation": "terminate"},
            "decision_audit": {},
        },
    )
    assert blocked["isError"] is True
    assert json.loads(blocked["content"][0]["text"])["error_code"] == (
        "missing_required_belief_checkpoint"
    )

    bad_page = server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_prediction_page",
            "page_id": "predictions-001",
            "predictions": [
                {
                    "query_id": "q0",
                    "metrics": [
                        {
                            "metric_id": "wrong",
                            "mean": 0.5,
                            "interval_lower": 0.0,
                            "interval_upper": 1.0,
                            "confidence": 0.25,
                        }
                    ],
                }
            ],
        },
    )
    assert bad_page["isError"] is True
    assert json.loads(bad_page["content"][0]["text"])["error_code"] == (
        "invalid_belief_snapshot"
    )

    prediction = server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_prediction_page",
            "page_id": "predictions-001",
            "predictions": snapshot["predictions"],
        },
    )
    assert prediction["isError"] is False
    fragment_path = (
        workspace.session_root("campaign-staged-snapshot-test")
        / "belief_snapshot_drafts"
        / "01-pre_evidence"
        / "fragments"
        / "001-predictions-001.json"
    )
    accepted_bytes = fragment_path.read_bytes()

    duplicate = server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_prediction_page",
            "page_id": "predictions-001",
            "predictions": snapshot["predictions"],
        },
    )
    assert duplicate["isError"] is True
    assert "cannot be replaced" in json.loads(duplicate["content"][0]["text"])["error"]
    assert fragment_path.read_bytes() == accepted_bytes

    law = server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_law_page",
            "page_id": "laws-001",
            "metric_laws": snapshot["law_summary"]["metric_laws"],
        },
    )
    assert law["isError"] is False
    assert json.loads(law["content"][0]["text"])["ready_to_finalize"] is True
    assert workspace.belief_snapshot_audit("campaign-staged-snapshot-test") == []

    finalized = server._call_tool("commit_belief_snapshot", {"action": "finalize"})
    assert finalized["isError"] is False
    assert workspace.belief_snapshot_audit("campaign-staged-snapshot-test") == [snapshot]
    draft_audit = workspace.belief_snapshot_draft_audit("campaign-staged-snapshot-test")
    assert draft_audit["draft_count"] == 1
    assert draft_audit["fragment_count"] == 2
    assert draft_audit["drafts"][0]["manifest"]["snapshot_header"] == _staged_header(snapshot)
    assert [item["page_id"] for item in draft_audit["drafts"][0]["fragments"]] == [
        "predictions-001",
        "laws-001",
    ]
    assert draft_audit["drafts"][0]["finalization"]["status"] == "finalized"


def test_staged_partial_draft_does_not_cross_session_or_count_checkpoint(
    tmp_path: Path,
) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-staged-partial-test")
    server = ChemWorldMCPServer(workspace.root)
    snapshot = _minimal_snapshot()
    begun = server._call_tool(
        "commit_belief_snapshot",
        {"action": "begin", "snapshot_header": _staged_header(snapshot)},
    )
    assert begun["isError"] is False
    prediction = server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_prediction_page",
            "page_id": "predictions-001",
            "predictions": snapshot["predictions"],
        },
    )
    assert prediction["isError"] is False
    assert workspace.belief_snapshot_audit("campaign-staged-partial-test") == []
    assert workspace.belief_snapshot_draft_audit("campaign-staged-partial-test")[
        "fragment_count"
    ] == 1

    workspace.start_session(
        session_id="campaign-staged-new-session-test",
        expected_step=1,
        response_timeout_s=10.0,
        session_scope="campaign",
    )
    new_server = ChemWorldMCPServer(workspace.root)
    new_state = new_server._status()["campaign_closeout"]["belief_snapshot_submission"]
    assert new_state["draft_started"] is False
    assert new_state["accepted_page_count"] == 0
    assert workspace.belief_snapshot_draft_audit("campaign-staged-new-session-test")[
        "draft_count"
    ] == 0


def test_staged_final_checkpoint_returns_final_response_contract(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-staged-final-test")
    session_root = workspace.session_root("campaign-staged-final-test")
    snapshots = session_root / "belief_snapshots"
    snapshots.mkdir()
    (snapshots / "01-pre_evidence.json").write_text("{}", encoding="utf-8")
    (snapshots / "02-after_experiment_2.json").write_text("{}", encoding="utf-8")
    for index in range(4):
        workspace.append_public_history(
            {
                "experiment_ended": True,
                "campaign_ended": index == 3,
                "evidence_id": f"experiment-{index + 1}-final-assay",
            }
        )
    server = ChemWorldMCPServer(workspace.root)
    snapshot = _minimal_snapshot(stage="final")
    snapshot["evidence_ids"] = [
        f"experiment-{index}-final-assay" for index in range(1, 5)
    ]
    snapshot["law_summary"]["evidence_ids"] = list(snapshot["evidence_ids"])
    assert server._call_tool(
        "commit_belief_snapshot",
        {"action": "begin", "snapshot_header": _staged_header(snapshot)},
    )["isError"] is False
    assert server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_prediction_page",
            "page_id": "predictions-001",
            "predictions": snapshot["predictions"],
        },
    )["isError"] is False
    assert server._call_tool(
        "commit_belief_snapshot",
        {
            "action": "append_law_page",
            "page_id": "laws-001",
            "metric_laws": snapshot["law_summary"]["metric_laws"],
        },
    )["isError"] is False
    finalized = server._call_tool("commit_belief_snapshot", {"action": "finalize"})
    payload = json.loads(finalized["content"][0]["text"])
    assert payload["remaining_checkpoint_count"] == 0
    assert payload["final_response_contract"] == ChemWorldMCPServer._final_response_contract(
        campaign=True
    )


def test_belief_snapshot_error_returns_authoritative_repair_context(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-snapshot-repair-test")
    server = ChemWorldMCPServer(workspace.root)
    snapshot = _minimal_snapshot()
    snapshot.pop("schema_version")

    result = server._call_tool("commit_belief_snapshot", {"snapshot": snapshot})

    assert result["isError"] is True
    payload = json.loads(result["content"][0]["text"])
    assert payload["error_code"] == "invalid_belief_snapshot"
    assert payload["field_path"] == "snapshot"
    assert payload["schema_authority"] == (
        "tools/list -> commit_belief_snapshot.inputSchema.properties.snapshot"
    )
    assert "schema_version" in payload["expected"]["required_fields"]
    assert "schema_version" not in payload["observed"]["fields"]
    assert payload["schema_fragment"]["additionalProperties"] is False


def test_step_checkpoint_rejection_is_structured_and_actionable(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-step-checkpoint-test")
    server = ChemWorldMCPServer(workspace.root)

    result = server._call_tool(
        "step",
        {
            "expected_step": 1,
            "action": {"operation": "terminate"},
            "decision_audit": {},
        },
    )

    assert result["isError"] is True
    payload = json.loads(result["content"][0]["text"])
    assert payload["error_code"] == "missing_required_belief_checkpoint"
    assert payload["field_path"] == "checkpoint"
    assert payload["checkpoint_due"] is True
    assert payload["next_stage"] == "pre_evidence"
    assert payload["completed"] == 0
    assert payload["required"] == 0
    assert payload["expected"] == {
        "next_stage": "pre_evidence",
        "complete_experiment_count": 0,
    }
    assert "commit_belief_snapshot" in payload["recovery_action"]


def test_step_decision_audit_rejection_returns_schema_fragment(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-step-audit-repair-test")
    server = ChemWorldMCPServer(workspace.root)
    committed = server._call_tool("commit_belief_snapshot", {"snapshot": _minimal_snapshot()})
    assert committed["isError"] is False

    result = server._call_tool(
        "step",
        {
            "expected_step": 1,
            "action": {"operation": "terminate"},
            "decision_audit": {"expected_information_gain": "high"},
        },
    )

    payload = json.loads(result["content"][0]["text"])
    assert payload["error_code"] == "validation_error"
    assert payload["field_path"] == "decision_audit.expected_information_gain"
    assert payload["expected"] == {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
    }
    assert payload["observed"] == "high"
    assert payload["schema_fragment"] == payload["expected"]


def test_early_checkpoint_rejection_disambiguates_required_and_observed(tmp_path: Path) -> None:
    workspace = _campaign_workspace(tmp_path, "campaign-early-checkpoint-test")
    server = ChemWorldMCPServer(workspace.root)
    committed = server._call_tool("commit_belief_snapshot", {"snapshot": _minimal_snapshot()})
    assert committed["isError"] is False
    early = _minimal_snapshot(stage="after_experiment_2")

    result = server._call_tool("commit_belief_snapshot", {"snapshot": early})

    payload = json.loads(result["content"][0]["text"])
    assert payload["error_code"] == "invalid_checkpoint_timing"
    assert payload["checkpoint_due"] is False
    assert payload["next_stage"] == "after_experiment_2"
    assert payload["completed"] == 0
    assert payload["required"] == 2
    assert payload["observed"]["submitted_stage"] == "after_experiment_2"
    assert "Continue physical experiments" in payload["recovery_action"]


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
