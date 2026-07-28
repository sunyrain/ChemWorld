from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from chemworld.providers.codex_subscription import (
    HTTPS_PROVIDER_ID,
    CodexSubscriptionClient,
    CodexSubscriptionError,
    _output_schema_from_prompt,
)


class _FakeCodexRunner:
    def __init__(self, exec_results: list[subprocess.CompletedProcess[str]]) -> None:
        self.exec_results = list(exec_results)
        self.exec_commands: list[list[str]] = []
        self.exec_inputs: list[str] = []
        self.instructions: list[str] = []
        self.schemas: list[dict[str, object]] = []

    def __call__(
        self,
        command: Sequence[str],
        stdin: str | None,
        timeout_s: float,
    ) -> subprocess.CompletedProcess[str]:
        del timeout_s
        args = list(command)
        if args[1:] == ["--version"]:
            return subprocess.CompletedProcess(args, 0, "codex-cli 0.145.0\n", "")
        if args[1:] == ["login", "status"]:
            return subprocess.CompletedProcess(args, 0, "Logged in using ChatGPT\n", "")
        self.exec_commands.append(args)
        self.exec_inputs.append(stdin or "")
        schema_path = Path(args[args.index("--output-schema") + 1])
        instructions_arg = args[args.index("-c", args.index("-c") + 1) :]
        model_instruction = next(
            item for item in instructions_arg if item.startswith("model_instructions_file=")
        )
        instructions_path = Path(json.loads(model_instruction.split("=", 1)[1]))
        self.instructions.append(instructions_path.read_text(encoding="utf-8"))
        self.schemas.append(json.loads(schema_path.read_text(encoding="utf-8")))
        return self.exec_results.pop(0)


def _event_result(
    text: str,
    *,
    returncode: int = 0,
    input_tokens: int = 100,
    cached_input_tokens: int = 20,
    output_tokens: int = 30,
    error_message: str | None = None,
) -> subprocess.CompletedProcess[str]:
    events: list[dict[str, object]] = [
        {"type": "thread.started", "thread_id": "thread-test"},
        {"type": "turn.started"},
    ]
    if error_message is not None:
        events.append({"type": "error", "message": error_message})
    events.extend(
        [
            {
                "type": "item.completed",
                "item": {"id": "item-test", "type": "agent_message", "text": text},
            },
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": input_tokens,
                    "cached_input_tokens": cached_input_tokens,
                    "cache_write_input_tokens": 0,
                    "output_tokens": output_tokens,
                    "reasoning_output_tokens": 0,
                },
            },
        ]
    )
    stdout = "\n".join(json.dumps(item) for item in events)
    return subprocess.CompletedProcess(["codex"], returncode, stdout, "")


def _prompt() -> str:
    return json.dumps(
        {
            "public_experiment_context": {"history": []},
            "required_json_shape": {
                "experiment_intent": "string",
                "search_vector": ["number in [0,1]"],
                "uncertainty": "number in [0,1]",
            },
        }
    )


def test_codex_subscription_client_uses_isolated_structured_exec() -> None:
    runner = _FakeCodexRunner(
        [
            _event_result(
                json.dumps(
                    {
                        "experiment_intent": "probe",
                        "search_vector": [0.5],
                        "uncertainty": 0.4,
                    }
                )
            )
        ]
    )
    client = CodexSubscriptionClient(
        codex_executable="codex-test",
        command_runner=runner,
    )

    completion = client.complete_json(
        system_prompt="Act as the frozen scientific planner.",
        user_prompt=_prompt(),
        max_tokens=512,
    )

    assert completion.payload["experiment_intent"] == "probe"
    assert completion.model == "gpt-5.6-sol"
    assert completion.request_id == "thread-test"
    assert completion.usage == {
        "prompt_tokens": 100,
        "completion_tokens": 30,
        "total_tokens": 130,
        "prompt_cache_hit_tokens": 20,
        "prompt_cache_miss_tokens": 80,
    }
    command = runner.exec_commands[0]
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert command.count("--disable") == 4
    assert "shell_tool" in command
    assert "apps" in command
    assert "multi_agent" in command
    assert "plugins" in command
    assert f'model_provider="{HTTPS_PROVIDER_ID}"' in command
    provider_config = next(
        item
        for item in command
        if item.startswith(f"model_providers.{HTTPS_PROVIDER_ID}=")
    )
    assert 'name="OpenAI"' in provider_config
    assert "requires_openai_auth=true" in provider_config
    assert "supports_websockets=false" in provider_config
    assert runner.exec_inputs == [_prompt()]
    assert "Act as the frozen scientific planner." in runner.instructions[0]
    assert "Do not call tools" in runner.instructions[0]
    assert runner.schemas[0]["additionalProperties"] is False


def test_codex_subscription_client_retries_invalid_json_and_aggregates_usage() -> None:
    runner = _FakeCodexRunner(
        [
            _event_result("not-json", input_tokens=10, cached_input_tokens=0, output_tokens=2),
            _event_result(
                json.dumps(
                    {
                        "experiment_intent": "retry",
                        "search_vector": [0.25],
                        "uncertainty": 0.7,
                    }
                ),
                input_tokens=12,
                cached_input_tokens=4,
                output_tokens=8,
            ),
        ]
    )
    client = CodexSubscriptionClient(
        codex_executable="codex-test",
        command_runner=runner,
        retry_backoff_s=0.0,
        sleep=lambda _: None,
    )

    completion = client.complete_json(
        system_prompt="Return JSON.",
        user_prompt=_prompt(),
    )

    assert completion.attempts == 2
    assert completion.usage == {
        "prompt_tokens": 22,
        "completion_tokens": 10,
        "total_tokens": 32,
        "prompt_cache_hit_tokens": 4,
        "prompt_cache_miss_tokens": 18,
    }
    assert [item["status"] for item in completion.attempt_records] == [
        "failed",
        "succeeded",
    ]


def test_codex_subscription_client_requires_chatgpt_login() -> None:
    def api_key_runner(
        command: Sequence[str],
        stdin: str | None,
        timeout_s: float,
    ) -> subprocess.CompletedProcess[str]:
        del stdin, timeout_s
        args = list(command)
        if args[1:] == ["--version"]:
            return subprocess.CompletedProcess(args, 0, "codex-cli 0.145.0\n", "")
        return subprocess.CompletedProcess(args, 0, "Logged in using an API key\n", "")

    with pytest.raises(CodexSubscriptionError, match="ChatGPT subscription"):
        CodexSubscriptionClient(
            codex_executable="codex-test",
            command_runner=api_key_runner,
        )


def test_codex_subscription_pricing_is_not_misreported_as_zero_cost() -> None:
    client = CodexSubscriptionClient(
        codex_executable="codex-test",
        command_runner=_FakeCodexRunner([]),
    )

    pricing = client.pricing_snapshot()

    assert pricing["provider"] == "OpenAI Codex"
    assert pricing["transport"] == "codex_exec_jsonl_https_sse"
    assert pricing["websocket_enabled"] is False
    assert pricing["authentication"] == "chatgpt_subscription_cached_login"
    assert pricing["accounting_complete"] is False
    assert "subscription" in pricing["pricing_unavailable_reason"].lower()


def test_output_schema_is_derived_from_frozen_required_shape() -> None:
    schema = _output_schema_from_prompt(
        json.dumps(
            {
                "required_json_shape": {
                    "recipe": {
                        "potential_V": {
                            "type": "number",
                            "minimum": 0.6,
                            "maximum": 1.8,
                            "unit": "V",
                        },
                        "profile": "integer code",
                    },
                    "risks": ["string"],
                }
            }
        )
    )

    assert schema == {
        "type": "object",
        "properties": {
            "recipe": {
                "type": "object",
                "properties": {
                    "potential_V": {
                        "type": "number",
                        "minimum": 0.6,
                        "maximum": 1.8,
                    },
                    "profile": {"type": "integer"},
                },
                "required": ["potential_V", "profile"],
                "additionalProperties": False,
            },
            "risks": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["recipe", "risks"],
        "additionalProperties": False,
    }
