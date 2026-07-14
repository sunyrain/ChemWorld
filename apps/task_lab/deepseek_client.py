"""Compatibility imports for Task Lab; provider code lives in ``chemworld``."""

from chemworld.providers.deepseek import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DeepSeekAPIError,
    DeepSeekClient,
    DeepSeekPricing,
    JsonCompletion,
    JsonPlannerClient,
    ReasoningEffort,
)

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
