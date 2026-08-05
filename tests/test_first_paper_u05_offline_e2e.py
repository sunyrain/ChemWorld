from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.first_paper_u05_complete_agent import (
    FROZEN_CODEX_CLI_VERSION,
    build_report,
    write_outputs,
)

ROOT = Path(__file__).resolve().parents[1]
SECRET_SENTINEL = "sk-test-provider-body-must-not-survive"

FROZEN_VALID_ACTIONS = (
    {"operation": "add_solvent", "solvent": 1, "volume_L": 0.025},
    {"amount_mol": 0.01, "operation": "add_reagent"},
    {
        "catalyst": 1,
        "catalyst_amount_mol": 0.0002,
        "operation": "add_catalyst",
    },
    {
        "duration_s": 1306.9591977665114,
        "operation": "heat",
        "stirring_speed_rpm": 650.0,
        "target_temperature_K": 374.8222114730154,
    },
    {"operation": "quench"},
    {"instrument": "hplc", "operation": "measure"},
    {
        "duration_s": 393.66154130180973,
        "operation": "evaporate",
        "target_temperature_K": 340.9774386096923,
    },
    {
        "duration_s": 2360.8151849022124,
        "operation": "distill",
        "reflux_ratio": 2.9915574378729524,
        "target_temperature_K": 356.8501202305547,
    },
    {
        "operation": "collect_fraction",
        "transfer_fraction": 0.8339945066845685,
    },
    {"instrument": "gc", "operation": "measure"},
    {"operation": "terminate"},
    {"instrument": "final_assay", "operation": "measure"},
)


_FAKE_CODEX_MCP_SESSION = r"""
import json
import subprocess
import sys
from pathlib import Path

agent = Path(sys.argv[1]).resolve()
repository = Path(sys.argv[2]).resolve()
actions = json.loads(sys.argv[3])
workspace = agent.parent
secret = "sk-test-provider-body-must-not-survive"


def emit(value):
    print(json.dumps(value, separators=(",", ":")), flush=True)


mcp = subprocess.Popen(
    [
        sys.executable,
        "-u",
        "-m",
        "chemworld.agents.experiment_codex_mcp",
        "--workspace",
        str(workspace),
    ],
    cwd=repository,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True,
    encoding="utf-8",
)
if mcp.stdin is None or mcp.stdout is None:
    raise RuntimeError("fake MCP stdio was not created")


def rpc(request_id, method, params):
    mcp.stdin.write(
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
    mcp.stdin.flush()
    line = mcp.stdout.readline()
    if not line:
        raise RuntimeError("fake MCP server exited without a response")
    response = json.loads(line)
    if "error" in response:
        raise RuntimeError(response["error"].get("message", "MCP error"))
    return response["result"]


def tool_call(request_id, name, arguments):
    result = rpc(
        request_id,
        "tools/call",
        {"name": name, "arguments": arguments},
    )
    if result.get("isError") is True:
        raise RuntimeError(json.loads(result["content"][0]["text"])["error"])
    public_result = json.loads(result["content"][0]["text"])
    emit(
        {
            "type": "item.completed",
            "item": {
                "id": f"mcp-{request_id}",
                "type": "dynamic_tool_call",
                "tool": f"mcp__chemworld_lab__{name}",
                "arguments": arguments,
                "result": {
                    "raw_provider_body": public_result,
                    "secret": secret,
                    "absolute_temporary_path": str(workspace),
                },
                "status": "completed",
            },
        }
    )
    return public_result


emit({"type": "thread.started", "thread_id": "offline-u05-thread"})
rpc(1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {}})
tool_call(2, "material_information", {})
for step, action in enumerate(actions, start=1):
    outcome = tool_call(
        step + 2,
        "step",
        {"expected_step": step, "action": action},
    )
    if outcome.get("experiment_ended") is True:
        break

emit(
    {
        "type": "item.completed",
        "item": {
            "id": "final",
            "type": "agent_message",
            "text": json.dumps(
                {
                    "status": "experiment_complete",
                    "summary": f"complete; hidden={secret}; scratch={workspace}",
                },
                separators=(",", ":"),
            ),
        },
    }
)
emit(
    {
        "type": "turn.completed",
        "usage": {
            "input_tokens": 4096,
            "cached_input_tokens": 1024,
            "cache_write_input_tokens": 256,
            "output_tokens": 1024,
            "reasoning_output_tokens": 512,
        },
    }
)
print(
    json.dumps({"secret": secret, "absolute_temporary_path": str(workspace)}),
    file=sys.stderr,
    flush=True,
)
mcp.stdin.close()
mcp.wait(timeout=10.0)
if mcp.returncode != 0:
    raise RuntimeError("fake MCP server failed")
"""


def _fake_process_factory(
    commands: list[list[str]],
    prompts: list[str],
):
    encoded_actions = json.dumps(FROZEN_VALID_ACTIONS, separators=(",", ":"))

    def factory(command: Sequence[str], prompt: str, cwd: Path):
        commands.append(list(command))
        prompts.append(prompt)
        return subprocess.Popen(
            [
                sys.executable,
                "-u",
                "-c",
                _FAKE_CODEX_MCP_SESSION,
                str(cwd),
                str(ROOT),
                encoded_actions,
            ],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

    return factory


def _verified_provider_preflight() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-first-paper-codex-preflight-0.1",
        "expected_cli_version": FROZEN_CODEX_CLI_VERSION,
        "observed_cli_version": FROZEN_CODEX_CLI_VERSION,
        "cli_version_matches": True,
        "cached_chatgpt_login_status": "passed",
        "verified": True,
    }


def test_u05_fake_codex_full_lifecycle_is_a_complete_census_and_immutable(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    scratch = tmp_path / "scratch"
    report = build_report(
        repository_root=ROOT,
        require_clean=False,
        scratch_dir=scratch,
        process_factory=_fake_process_factory(commands, prompts),
        provider_preflight=_verified_provider_preflight(),
    )

    assert report["status"] == "passed", report["failures"]
    assert report["failures"] == []
    assert report["failure_class_counts"] == {}
    assert len(commands) == 1
    assert len(prompts) == 1
    assert "--ephemeral" in commands[0]
    assert "chemworld_lab" in prompts[0]
    assert SECRET_SENTINEL not in prompts[0]
    assert "deterministic_reference_actions" not in json.loads(prompts[0])
    runtime_binding = report["frozen_experiment"]["runtime_contract_binding"]
    assert runtime_binding["task_contract_hash_matches"] is True
    assert runtime_binding["task_contract_hash"] == (
        "9b775c56b1cfe07dc75afc355d4815077913b27cbeedf20d32fb21d9dadf9f14"
    )
    assert report["frozen_experiment"]["public_compiled_task_subobject_hash"] == (
        "0ada08676d4b4afd20383619b4a1392639b4641ad26a15fb3b3e0f38c0b2de1e"
    )

    actions = report["actions"]
    expected_count = len(FROZEN_VALID_ACTIONS)
    assert report["denominators"] == {
        "lifecycle_count": 1,
        "provider_session_count": 1,
        "model_call_count": 1,
        "submitted_action_count": expected_count,
        "trajectory_record_count": expected_count,
    }
    assert [row["step"] for row in actions] == list(range(1, expected_count + 1))
    assert [row["action"] for row in actions] == list(FROZEN_VALID_ACTIONS)
    assert [row["action"] for row in actions[-2:]] == [
        {"operation": "terminate"},
        {"instrument": "final_assay", "operation": "measure"},
    ]
    assert all(row["schema_validation"]["valid"] is True for row in actions)
    assert all(row["transaction"]["status"] == "committed" for row in actions)
    assert all(row["transaction"]["rollback_reason"] is None for row in actions)
    assert all(row["resource_preflight"]["allowed"] is True for row in actions)
    assert all(not row["resource_preflight"]["rejection_reasons"] for row in actions)
    assert all(
        row["resource_reconciliation"]["resource_reconciled"] is True
        for row in actions
    )
    assert all(row["provider_binding"]["accepted_action_verified"] is True for row in actions)
    assert all(row["provider_binding"]["mcp_step"]["verified"] is True for row in actions)
    assert all(row["method_resources"]["operation_count"] == row["step"] for row in actions)
    assert all(row["leakage_findings"] == [] for row in actions)
    assert all(row["passed"] is True and row["failures"] == [] for row in actions)

    monitor = report["step_monitor"]
    assert monitor["all_passed"] is True
    assert monitor["event_count"] == expected_count
    assert [event["step"] for event in monitor["events"]] == list(
        range(1, expected_count + 1)
    )
    assert all(event["status"] == "passed" for event in monitor["events"])
    assert monitor["events"][-1]["lifecycle"] == {
        "terminate_count": 1,
        "final_assay_count": 1,
        "complete": True,
    }

    lifecycle = report["lifecycle"]
    assert lifecycle["passed"] is True
    assert lifecycle["submitted_action_count"] == expected_count
    assert lifecycle["committed_action_count"] == expected_count
    assert lifecycle["rollback_count"] == 0
    assert lifecycle["committed_terminate_count"] == 1
    assert lifecycle["committed_final_assay_count"] == 1
    assert lifecycle["complete_experiment_count"] == 1
    assert lifecycle["right_censored"] is False
    assert all(lifecycle["checks"].values())

    provider = report["provider_accounting"]
    assert provider["passed"] is True
    assert provider["session_count"] == 1
    assert provider["model_call_count"] == 1
    assert provider["accepted_action_count"] == expected_count
    assert provider["mcp_tool_call_count"] == expected_count + 1
    assert provider["mcp_step_count"] == expected_count
    assert provider["usage"]["prompt_tokens"] == 4096
    assert provider["usage"]["completion_tokens"] == 1024
    assert all(provider["session_checks"].values())
    assert all(provider["token_checks"].values())
    assert all(provider["method_checks"].values())

    session = report["provider_session_receipts"][0]
    assert [row["tool"] for row in session["mcp_tool_calls"]] == [
        "material_information",
        *(["step"] * expected_count),
    ]
    assert session["provider_errors"] == []
    assert session["usage_complete"] is True
    assert session["private_reasoning_retained"] is False
    assert "final_payload_summary" not in session
    assert all(
        event.get("arguments_body_retained") is False
        and event.get("result_body_retained") is False
        for event in session["tool_events"]
    )

    assert report["environment_resource_receipt"]["resource_reconciled"] is True
    assert report["declared_resource_budget"]["passed"] is True
    assert all(report["declared_resource_budget"]["checks"].values())
    assert report["declared_resource_budget"]["exceeded_resources"] == []
    assert report["exact_replay"] == {
        "verified": True,
        "checked_steps": expected_count,
        "max_abs_error": 0.0,
        "mismatches": [],
    }
    assert report["receipt_completeness"] == {
        "passed": True,
        "error_count": 0,
        "errors": [],
    }
    assert report["public_boundary"]["finding_count"] == 0
    assert report["sanitization"] == {
        "passed": True,
        "finding_count": 0,
        "findings": [],
    }

    serialized = json.dumps(report, ensure_ascii=False, sort_keys=True)
    assert SECRET_SENTINEL not in serialized
    assert str(scratch.resolve()) not in serialized
    assert "raw_provider_body" not in serialized
    assert '"final_payload_summary":' not in serialized

    output_json = tmp_path / "first-paper-agent-instrument-use-v1.json"
    output_md = tmp_path / "first-paper-agent-instrument-use-v1.md"
    write_outputs(report, output_path=output_json, markdown_path=output_md)
    original_json = output_json.read_bytes()
    original_md = output_md.read_bytes()
    with pytest.raises(FileExistsError, match="refusing to replace or overwrite"):
        write_outputs(report, output_path=output_json, markdown_path=output_md)
    assert output_json.read_bytes() == original_json
    assert output_md.read_bytes() == original_md
