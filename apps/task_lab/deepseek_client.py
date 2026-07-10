"""Small dependency-free client for DeepSeek's OpenAI-compatible chat API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Literal, Protocol

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-pro"
ReasoningEffort = Literal["high", "max"]


class JsonPlannerClient(Protocol):
    model: str

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion: ...


@dataclass(frozen=True)
class JsonCompletion:
    payload: dict[str, Any]
    model: str
    usage: dict[str, Any]
    request_id: str | None = None
    attempts: int = 1


class DeepSeekAPIError(RuntimeError):
    """Raised for a redacted DeepSeek transport or response failure."""

    def __init__(
        self,
        message: str,
        *,
        attempts: int = 1,
        usage: dict[str, int] | None = None,
    ) -> None:
        super().__init__(message)
        self.attempts = attempts
        self.usage = dict(usage or {})


class DeepSeekClient:
    """Call DeepSeek without adding an SDK dependency to ChemWorld."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float = 120.0,
        thinking: bool = False,
        reasoning_effort: ReasoningEffort = "max",
    ) -> None:
        self._api_key = (api_key or os.environ.get("DEEPSEEK_API_KEY", "")).strip()
        if not self._api_key:
            raise DeepSeekAPIError(
                "DEEPSEEK_API_KEY is not set. Keep the key in an environment variable."
            )
        self.base_url = (
            base_url or os.environ.get("DEEPSEEK_BASE_URL") or DEFAULT_BASE_URL
        ).rstrip("/")
        self.model = model or os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL
        self.timeout_s = timeout_s
        self.thinking = thinking
        if reasoning_effort not in {"high", "max"}:
            raise ValueError("reasoning_effort must be high or max")
        self.reasoning_effort = reasoning_effort

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        aggregate_usage: dict[str, int] = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        last_error: Exception | None = None
        for attempt in range(1, 4):
            retry_note = (
                "\nThe previous response was empty or invalid. Return the required JSON now."
                if attempt > 1
                else ""
            )
            body = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + retry_note},
                ],
                "response_format": {"type": "json_object"},
                "thinking": {"type": "enabled" if self.thinking else "disabled"},
                "stream": False,
                "max_tokens": max_tokens,
            }
            if self.thinking:
                body["reasoning_effort"] = self.reasoning_effort
            raw, request_id = self._send(body)
            envelope: dict[str, Any] = {}
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise TypeError("response envelope is not an object")
                envelope = parsed
                _merge_usage(aggregate_usage, envelope.get("usage"))
                choice = envelope["choices"][0]
                content = choice["message"]["content"]
                payload = _parse_json_content(content)
                if not isinstance(payload, dict):
                    raise TypeError("JSON output is not an object")
                return JsonCompletion(
                    payload=payload,
                    model=str(envelope.get("model") or self.model),
                    usage=aggregate_usage,
                    request_id=request_id or envelope.get("id"),
                    attempts=attempt,
                )
            except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
                last_error = exc
        raise DeepSeekAPIError(
            "DeepSeek returned invalid JSON output after 3 attempts",
            attempts=3,
            usage=aggregate_usage,
        ) from last_error

    def _send(self, body: dict[str, Any]) -> tuple[str, str | None]:
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "ChemWorld-Task-Lab/0.2",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                return (
                    response.read().decode("utf-8"),
                    response.headers.get("x-request-id"),
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise DeepSeekAPIError(f"DeepSeek HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise DeepSeekAPIError(f"DeepSeek connection failed: {exc.reason}") from exc
        except TimeoutError as exc:
            raise DeepSeekAPIError("DeepSeek request timed out") from exc


def _parse_json_content(content: object) -> Any:
    if not isinstance(content, str) or not content.strip():
        raise json.JSONDecodeError("empty model content", "", 0)
    text = content.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())


def _merge_usage(total: dict[str, int], usage: object) -> None:
    if not isinstance(usage, dict):
        return
    for key in total:
        value = usage.get(key, 0)
        if isinstance(value, int) and not isinstance(value, bool):
            total[key] += value


__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_MODEL",
    "DeepSeekAPIError",
    "DeepSeekClient",
    "JsonCompletion",
    "JsonPlannerClient",
    "ReasoningEffort",
]
