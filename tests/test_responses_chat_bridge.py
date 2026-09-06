import io
import json
import urllib.error
import urllib.request

import pytest

from chemworld.providers.responses_chat_bridge import (
    BridgeError,
    ResponsesChatBridge,
    response_usage,
)


def test_tool_return_preserves_reasoning_arguments_and_roles(tmp_path):
    with ResponsesChatBridge(api_key="secret", audit_dir=tmp_path / "audit") as bridge:
        bridge.reasoning["call1"] = "private provider reasoning"
        request = {
            "model": bridge.model,
            "input": [
                {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": "public contract"}],
                },
                {
                    "type": "function_call",
                    "call_id": "call1",
                    "name": "calculate",
                    "arguments": '{"x":19}',
                },
                {"type": "function_call_output", "call_id": "call1", "output": "42"},
            ],
            "tools": [{"type": "function", "name": "calculate", "parameters": {"type": "object"}}],
        }
        body, _, _ = bridge.translate(request)
        assert body["messages"][0] == {"role": "system", "content": "public contract"}
        assert body["messages"][1]["reasoning_content"] == "private provider reasoning"
        assert body["messages"][1]["tool_calls"][0]["function"]["arguments"] == '{"x":19}'
        assert body["messages"][2] == {"role": "tool", "tool_call_id": "call1", "content": "42"}
        assert response_usage(None) is None


def test_sse_roundtrip_previous_id_auth_and_usage(monkeypatch, tmp_path):
    seen = []

    def upstream(self, body, record):
        seen.append(body)
        return {
            "content": "answer",
            "reasoning_content": "private",
            "tool_calls": [],
            "usage": {
                "prompt_tokens": 12,
                "completion_tokens": 7,
                "total_tokens": 19,
                "prompt_tokens_details": {"cached_tokens": 4},
                "completion_tokens_details": {"reasoning_tokens": 3},
            },
        }

    monkeypatch.setattr(ResponsesChatBridge, "_upstream", upstream)
    with ResponsesChatBridge(api_key="upstream-secret", audit_dir=tmp_path / "audit") as bridge:

        def post(data, token):
            req = urllib.request.Request(
                bridge.base_url + "/responses",
                data=json.dumps(data).encode(),
                headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req) as response:
                return response.read().decode()

        with pytest.raises(urllib.error.HTTPError) as error:
            post({"model": bridge.model}, "incorrect-token")
        assert error.value.code == 401
        wire = post({"model": bridge.model, "input": "first", "stream": True}, bridge.local_token)
        events = [json.loads(line[6:]) for line in wire.splitlines() if line.startswith("data: ")]
        assert [e["sequence_number"] for e in events] == list(range(len(events)))
        assert events[-1]["type"] == "response.completed"
        completed = events[-1]["response"]
        assert completed["usage"]["output_tokens_details"]["reasoning_tokens"] == 3
        assert "private" not in wire
        post(
            {"model": bridge.model, "previous_response_id": completed["id"], "input": "second"},
            bridge.local_token,
        )
        assert [m["role"] for m in seen[-1]["messages"]] == ["user", "assistant", "user"]
        assert seen[-1]["messages"][1]["reasoning_content"] == "private"


def test_upstream_failure_stays_failed_no_retry_or_usage_fabrication(monkeypatch, tmp_path):
    calls = []

    def failure(self, body, record):
        calls.append(body)
        raise BridgeError("upstream_http_429", "rate limited")

    monkeypatch.setattr(ResponsesChatBridge, "_upstream", failure)
    with ResponsesChatBridge(api_key="secret", audit_dir=tmp_path / "audit") as bridge:
        with pytest.raises(BridgeError, match="rate limited"):
            bridge.complete({"model": bridge.model, "input": "test"}, "r1")
        assert len(calls) == 1
        assert bridge.records[0]["status"] == "failed"
        assert bridge.records[0]["usage"] is None
        assert "r1" not in bridge.responses


@pytest.mark.parametrize("kind", ["function", "custom"])
def test_namespaced_tool_roundtrip_keeps_identity_input_and_reasoning(kind, monkeypatch, tmp_path):
    original = "*** Begin Patch\n*** End Patch\n" if kind == "custom" else '{"expression":"19+23"}'
    argument = json.dumps({"input": original}) if kind == "custom" else original

    def upstream(self, body, record):
        return {
            "content": "",
            "reasoning_content": "reasoning continuity",
            "usage": None,
            "tool_calls": [{"id": "c1", "name": "numerics__calculate", "arguments": argument}],
        }

    monkeypatch.setattr(ResponsesChatBridge, "_upstream", upstream)
    with ResponsesChatBridge(api_key="secret", audit_dir=tmp_path / "audit") as bridge:
        request = {
            "model": bridge.model,
            "input": "compute",
            "tools": [
                {
                    "type": "namespace",
                    "name": "numerics",
                    "tools": [
                        {"type": kind, "name": "calculate", "parameters": {"type": "object"}}
                    ],
                }
            ],
        }
        output = bridge.complete(request, "r1")["output"][0]
        assert output["namespace"] == "numerics"
        assert output["name"] == "calculate"
        assert output["call_id"] == "c1"
        assert output["input" if kind == "custom" else "arguments"] == original
        request.update(
            previous_response_id="r1",
            input=[
                {
                    "type": "custom_tool_call_output"
                    if kind == "custom"
                    else "function_call_output",
                    "call_id": "c1",
                    "output": "42",
                }
            ],
        )
        body, _, _ = bridge.translate(request)
        call = body["messages"][1]["tool_calls"][0]
        assert call["function"] == {"name": "numerics__calculate", "arguments": argument}
        assert body["messages"][1]["reasoning_content"] == "reasoning continuity"
        assert body["messages"][2] == {"role": "tool", "tool_call_id": "c1", "content": "42"}


def test_failed_smoke_cannot_launch_calibration_or_request_a_key(monkeypatch, tmp_path):
    from scripts.check_work_ii_glm_bridge import main

    summary = tmp_path / "summary.json"
    summary.write_text(json.dumps({"passed": False, "stage": "smoke"}))
    output = tmp_path / "calibration"
    monkeypatch.setattr(
        "sys.argv",
        [
            "check",
            "calibrate",
            "--output",
            str(output),
            "--smoke-summary",
            str(summary),
            "--key-stdin",
        ],
    )
    monkeypatch.setattr("getpass.getpass", lambda *_a: pytest.fail("must not request a key"))
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert not output.exists()


def test_report_retains_failed_and_unstarted_denominators_and_missing_usage(tmp_path):
    from scripts.check_work_ii_glm_bridge import build_report

    (tmp_path / "summary.json").write_text(
        json.dumps(
            {
                "schema_mode": "json_schema",
                "passed": False,
                "attempted_turns": 1,
                "tool_audit": [],
                "wall_seconds": 0.5,
                "codex_version": "offline-fixture",
                "bridge_requests": [
                    {
                        "request": 1,
                        "status": "failed",
                        "usage": None,
                        "error_code": "unsupported_tool",
                    }
                ],
                "results": [{"turn": 1, "passed": False, "receipt": {"payload": None}}],
            }
        )
    )
    report = build_report([tmp_path], None)
    assert not report["third_model_adopted"]
    assert report["calibration"]["scheduled_sessions"] == 6
    assert report["calibration"]["unstarted_sessions"] == 6
    attempt = report["transport"]["attempts"][0]
    assert [r["status"] for r in attempt["turns"]] == ["failed", "unstarted"]
    assert attempt["bridge_requests"][0]["usage"] is None
    assert report["resource_accounting"]["requests_reaching_upstream_http"] == 0
    assert report["resource_accounting"]["requests_without_usage"] == 1


@pytest.mark.parametrize("error_after_usage", [False, True])
def test_upstream_stream_retains_fragmented_calls_and_known_usage(
    monkeypatch, tmp_path, error_after_usage
):
    usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    chunks = [
        {
            "model": "zai-org/GLM-5.3",
            "choices": [
                {
                    "delta": {
                        "tool_calls": [
                            {
                                "index": 0,
                                "id": "c1",
                                "function": {"name": "calculate", "arguments": '{"x":'},
                            }
                        ]
                    }
                }
            ],
        },
        {
            "choices": [
                {
                    "delta": {"tool_calls": [{"index": 0, "function": {"arguments": "42}"}}]},
                    "finish_reason": "tool_calls",
                }
            ]
        },
        {"usage": usage, "choices": []},
    ]
    if error_after_usage:
        chunks.append({"error": {"message": "interrupted after usage"}})
    response = io.BytesIO(
        ("".join("data: " + json.dumps(c) + "\n\n" for c in chunks) + "data: [DONE]\n\n").encode()
    )
    response.status = 200
    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_kw: response)
    with ResponsesChatBridge(api_key="secret", audit_dir=tmp_path / "audit") as bridge:
        record = {"request": 1}
        if error_after_usage:
            with pytest.raises(BridgeError, match="interrupted"):
                bridge._upstream({}, record)
        else:
            result = bridge._upstream({}, record)
            assert result["tool_calls"] == [
                {"id": "c1", "name": "calculate", "arguments": '{"x":42}'}
            ]
        assert record["usage"] == usage
