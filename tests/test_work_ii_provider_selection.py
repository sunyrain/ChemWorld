import json

import pytest
from scripts.check_work_ii_glm_bridge import prepare_home
from scripts.check_work_ii_provider_selection import (
    CANDIDATES,
    direct_probes,
    recover_interrupted,
    select_candidate,
)

from chemworld.providers.responses_chat_bridge import ResponsesChatBridge


def test_prompt_schema_keeps_tools_and_original_schema_without_upstream_json_constraint(tmp_path):
    schema = {"type": "object", "properties": {"sum": {"type": "number"}}, "required": ["sum"]}
    with ResponsesChatBridge(
        api_key="secret", audit_dir=tmp_path / "audit", schema_mode="prompt_schema"
    ) as bridge:
        request = {
            "model": bridge.model,
            "input": "Use calculate and then submit the answer.",
            "text": {"format": {"type": "json_schema", "name": "final", "schema": schema}},
            "tools": [{"type": "function", "name": "calculate", "parameters": schema}],
        }
        body, _, _ = bridge.translate(request)
        assert "response_format" not in body
        assert body["tool_choice"] == "auto"
        assert body["tools"][0]["function"]["parameters"] == schema
        content = body["messages"][0]["content"]
        assert json.loads(content[content.index("{") :]) == schema
        assert request["input"] == "Use calculate and then submit the answer."


def test_prompt_schema_merges_only_leading_system_messages_without_losing_the_contract(tmp_path):
    with ResponsesChatBridge(
        api_key="secret", audit_dir=tmp_path / "audit", schema_mode="prompt_schema"
    ) as bridge:
        request = {
            "model": bridge.model,
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
            "input": [
                {"role": "developer", "content": "Preserve this tool contract."},
                {"role": "user", "content": "Question"},
            ],
        }
        body, _, _ = bridge.translate(request)
        assert [m["role"] for m in body["messages"]] == ["system", "user"]
        assert body["messages"][0]["content"].endswith("\n\nPreserve this tool contract.")
        assert '{"type":"object"}' in body["messages"][0]["content"]
        assert body["messages"][1]["content"] == "Question"


def test_alternate_model_catalog_and_child_auth_are_isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("SILICONFLOW_API_KEY", "upstream-secret")
    model = CANDIDATES[1][1]
    with ResponsesChatBridge(
        api_key="upstream-secret", audit_dir=tmp_path / "audit", model=model
    ) as bridge:
        provider, environment, _ = prepare_home(tmp_path / "home", bridge)
        catalog = json.loads((tmp_path / "home/model_catalog.json").read_text())
        assert provider["model"] == catalog["models"][0]["slug"] == model
        assert "SILICONFLOW_API_KEY" not in environment
        assert environment["CHEMWORLD_GLM_BRIDGE_TOKEN"] == bridge.local_token
        config = (tmp_path / "home/codex-home/config.toml").read_text()
        assert bridge.local_token not in config and "upstream-secret" not in config


def test_fixed_selection_order_is_not_completion_order_or_science_score():
    kimi, qwen = [m for _, m in CANDIDATES]
    rows = [
        {"model": qwen, "schema_mode": "json_schema", "status": "passed", "score": 1},
        {"model": kimi, "schema_mode": "prompt_schema", "status": "passed", "score": 0},
    ]
    assert select_candidate(rows) == {
        "label": "kimi",
        "model": kimi,
        "schema_mode": "prompt_schema",
    }
    rows.append({"model": kimi, "schema_mode": "json_schema", "status": "passed"})
    assert select_candidate(rows)["schema_mode"] == "json_schema"
    assert select_candidate([]) is None


@pytest.mark.parametrize("valid_tool", [True, False])
def test_direct_control_keeps_reasoning_and_unstarted_followup(monkeypatch, tmp_path, valid_tool):
    seen = []
    model = CANDIDATES[0][1]

    def fake_request(key, endpoint, body, output):
        seen.append(body)
        assert key == "secret" and body["model"] == model
        if endpoint == "/responses":
            return {"http_status": 404, "usage": None}, {}
        if len(seen) == 2:
            return {"http_status": 200, "usage": None}, {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "reasoning_content": "continuity",
                            "tool_calls": [
                                {
                                    "id": "c1",
                                    "type": "function",
                                    "function": {
                                        "name": "calculate",
                                        "arguments": '{"expression":"19+23"}'
                                        if valid_tool
                                        else '{"expression":"not allowed"}',
                                    },
                                }
                            ],
                        }
                    }
                ]
            }
        assert body["messages"][1]["reasoning_content"] == "continuity"
        assert body["messages"][2]["content"] == "42"
        return {"http_status": 200, "usage": None}, {"choices": [{"message": {"content": "42"}}]}

    monkeypatch.setattr("scripts.check_work_ii_provider_selection.request", fake_request)
    result = direct_probes("secret", model, tmp_path / "direct")
    assert len(result) == 3
    assert len(seen) == (3 if valid_tool else 2)
    assert result[-1]["status"] == ("passed" if valid_tool else "unstarted")


def test_interruption_recovery_counts_started_sessions_and_preserves_known_usage(tmp_path):
    cal = tmp_path / "calibration"
    (cal / "bridge").mkdir(parents=True)
    (cal / "session-1/pre").mkdir(parents=True)
    (cal / "session-1/pre/stdout.jsonl").write_text('{"type":"turn.started"}\n')
    cells = [{"cell_id": str(i), "model": "kimi", "arm": "opaque", "tool": "off"} for i in range(6)]
    (cal / "inputs.json").write_text(json.dumps({"cells": cells}))
    (tmp_path / "partial.json").write_text(json.dumps({"direct": [], "harness": []}))
    (tmp_path / "platform_stop.json").write_text(json.dumps({"findings": ["Fixture stop"]}))
    usage = {"prompt_tokens": 7, "completion_tokens": 3, "total_tokens": 10}
    (cal / "bridge/001-responses-request.json").write_text("{}")
    (cal / "bridge/ledger.json").write_text(
        json.dumps([{"request": 1, "status": "started", "usage": usage}])
    )
    result = recover_interrupted(tmp_path)
    assert result["calibration"]["attempted_sessions"] == 1
    assert result["calibration"]["unstarted_sessions"] == 5
    assert result["calibration"]["attempted_turns"] == 1
    assert result["calibration"]["bridge_requests"][0]["usage"] == usage
    assert result["calibration"]["results"][0]["elapsed_s"] is None
    (tmp_path / "summary.json").write_text("{}")
    with pytest.raises(FileExistsError):
        recover_interrupted(tmp_path)
