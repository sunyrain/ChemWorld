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
PRICING_ACCESS_DATE = "2026-07-11"
PRICING_SOURCE = "https://api-docs.deepseek.com/quick_start/pricing"
ReasoningEffort = Literal["high", "max"]


@dataclass(frozen=True)
class DeepSeekPricing:
    model_id: str
    input_cache_hit_per_million_usd: float
    input_cache_miss_per_million_usd: float
    output_per_million_usd: float
    access_date: str = PRICING_ACCESS_DATE
    source: str = PRICING_SOURCE

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "input_cache_hit_per_million_usd": self.input_cache_hit_per_million_usd,
            "input_cache_miss_per_million_usd": self.input_cache_miss_per_million_usd,
            "output_per_million_usd": self.output_per_million_usd,
            "access_date": self.access_date,
            "source": self.source,
        }


_PRICING = {
    "deepseek-v4-flash": DeepSeekPricing("deepseek-v4-flash", 0.0028, 0.14, 0.28),
    "deepseek-v4-pro": DeepSeekPricing("deepseek-v4-pro", 0.003625, 0.435, 0.87),
}


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

    def pricing_snapshot(self) -> dict[str, Any]:
        model_id = {
            "deepseek-chat": "deepseek-v4-flash",
            "deepseek-reasoner": "deepseek-v4-flash",
        }.get(self.model, self.model)
        try:
            pricing = _PRICING[model_id]
        except KeyError as exc:
            raise DeepSeekAPIError(f"No frozen pricing snapshot for model {self.model!r}") from exc
        payload = pricing.to_dict()
        payload["requested_model_id"] = self.model
        payload["legacy_alias"] = self.model != model_id
        return payload

    def estimate_cost_usd(self, usage: dict[str, Any]) -> float:
        pricing = self.pricing_snapshot()
        prompt_tokens = _nonnegative_int(usage.get("prompt_tokens"))
        cache_hit = _nonnegative_int(usage.get("prompt_cache_hit_tokens"))
        cache_miss = _nonnegative_int(usage.get("prompt_cache_miss_tokens"))
        accounted_prompt = cache_hit + cache_miss
        if accounted_prompt < prompt_tokens:
            cache_miss += prompt_tokens - accounted_prompt
        completion = _nonnegative_int(usage.get("completion_tokens"))
        return (
            cache_hit * float(pricing["input_cache_hit_per_million_usd"])
            + cache_miss * float(pricing["input_cache_miss_per_million_usd"])
            + completion * float(pricing["output_per_million_usd"])
        ) / 1_000_000.0

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
            "prompt_cache_hit_tokens": 0,
            "prompt_cache_miss_tokens": 0,
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


def _nonnegative_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return 0


__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_MODEL",
    "DeepSeekAPIError",
    "DeepSeekClient",
    "DeepSeekPricing",
    "JsonCompletion",
    "JsonPlannerClient",
    "ReasoningEffort",
]
