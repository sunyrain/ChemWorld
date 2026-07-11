"""Operation-level live-LLM adapter for the official benchmark runner.

The adapter intentionally owns no provider SDK.  A small JSON client is injected so
the official runner, fake-client tests, and provider-specific launchers all share the
same interaction semantics.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal, Protocol

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.interaction import AgentDecisionContext, InteractionCapabilities
from chemworld.data.logging import to_builtin

SpectrumDisclosure = Literal["assigned", "masked"]

SYSTEM_PROMPT = """You are an operation-level agent in the ChemWorld virtual laboratory.
Use only the supplied public task contract, observations, spectra, memory, and action schemas.
Choose exactly one next operation and return exactly one JSON object. Never claim hidden
chemical identities or hidden simulator state. Do not provide private chain-of-thought.
Provide only a concise public audit: evidence, spectrum interpretation, hypothesis,
uncertainty, rationale, and the selected action using exact schema field names.
"""

PROMPT_CONTRACT_VERSION = "chemworld-live-llm-operation-json-0.1"


class JsonCompletionLike(Protocol):
    payload: dict[str, Any]
    model: str
    usage: dict[str, Any]
    attempts: int


class JsonPlannerClientLike(Protocol):
    model: str

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletionLike: ...


class LiveLLMAgent(BaseAgent):
    """Use one provider decision per operation in the official runner.

    Provider and output failures are retained as invalid ``model_failure`` actions.
    This makes completion rate and validity honest: the harness never repairs an action
    or performs a terminal assay on the model's behalf.
    """

    name = "live_llm"

    def __init__(
        self,
        client: JsonPlannerClientLike,
        *,
        role_id: str,
        spectrum_disclosure: SpectrumDisclosure = "assigned",
        recent_decision_limit: int = 6,
        experiment_memory_limit: int = 12,
    ) -> None:
        if spectrum_disclosure not in {"assigned", "masked"}:
            raise ValueError("spectrum_disclosure must be assigned or masked")
        if recent_decision_limit <= 0 or experiment_memory_limit <= 0:
            raise ValueError("memory limits must be positive")
        self.client = client
        self.role_id = role_id
        self.spectrum_disclosure = spectrum_disclosure
        self.recent_decision_limit = int(recent_decision_limit)
        self.experiment_memory_limit = int(experiment_memory_limit)

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._usage = _empty_usage()
        self._model_call_count = 0
        self._recent_decisions: list[dict[str, Any]] = []
        self._experiment_memory: list[dict[str, Any]] = []
        self._last_decision: dict[str, Any] | None = None
        self._last_context: dict[str, Any] = {}
        self._last_public_view: dict[str, Any] = {}
        self._logical_decision_count = 0

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        raise RuntimeError("LiveLLMAgent requires the official public-view runner")

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        self._logical_decision_count += 1
        self._last_context = context.to_dict()
        self._last_public_view = to_builtin(public_view)
        prompt = self._build_prompt(context, public_view)
        try:
            completion = self.client.complete_json(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                max_tokens=8000 if bool(getattr(self.client, "thinking", False)) else 2000,
            )
            self._record_provider_usage(completion.attempts, completion.usage)
            decision = self._normalize_decision(completion.payload, context=context)
            decision["provider_model"] = str(completion.model)
            decision["provider_attempts"] = int(completion.attempts)
            decision["status"] = "model_decision"
        except Exception as exc:
            attempts = max(int(getattr(exc, "attempts", 1)), 1)
            usage = getattr(exc, "usage", {})
            self._record_provider_usage(attempts, usage if isinstance(usage, dict) else {})
            decision = self._failure_decision(context, exc)
        self._last_decision = decision
        self._recent_decisions.append(_prompt_memory_decision(decision))
        self._recent_decisions = self._recent_decisions[-self.recent_decision_limit :]
        return dict(decision["action"])

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        if self._last_decision is None:
            return
        outcome = {
            "reward": float(reward),
            "observed_keys": list(info.get("observed_keys", [])),
            "constraint_flags": to_builtin(info.get("constraint_flags", {})),
            "error_message": info.get("error_message"),
            "leaderboard_score": info.get("leaderboard_score"),
            "experiment_ended": bool(info.get("experiment_ended", False)),
            "observation": to_builtin(observation),
        }
        self._last_decision["outcome"] = outcome
        if self._recent_decisions:
            self._recent_decisions[-1]["outcome"] = outcome
        final_assay = action.get("operation") == "measure" and action.get("instrument") == (
            "final_assay"
        )
        if outcome["experiment_ended"] or final_assay:
            self._experiment_memory.append(
                {
                    "experiment_index": len(self._experiment_memory) + 1,
                    "terminal_action": to_builtin(action),
                    "score": info.get("leaderboard_score"),
                    "visible_metrics": to_builtin(
                        self._last_context.get("visible_metrics", {})
                    ),
                    "constraint_flags": outcome["constraint_flags"],
                    "recent_decisions": to_builtin(
                        self._recent_decisions[-self.recent_decision_limit :]
                    ),
                }
            )
            self._experiment_memory = self._experiment_memory[
                -self.experiment_memory_limit :
            ]

    def decision_audit(self) -> dict[str, Any] | None:
        if self._last_decision is None:
            return None
        return {
            "action": dict(self._last_decision["action"]),
            "evidence": list(self._last_decision["evidence"]),
            "hypothesis": str(self._last_decision["hypothesis"]),
            "uncertainty": float(self._last_decision["uncertainty"]),
            "rationale": str(self._last_decision["rationale"]),
            "adaptation_source": str(self._last_decision["adaptation_source"]),
        }

    def agent_trace(self) -> list[dict[str, Any]]:
        """Return only the current decision so JSONL logging remains linear in steps."""

        if self._last_decision is None:
            return []
        return [to_builtin(self._last_decision)]

    def interaction_capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(
            decision_scope="operation",
            consumes_intermediate_observations=True,
            consumes_spectra=self.spectrum_disclosure == "assigned",
            adapts_within_experiment=True,
            adapts_across_experiments=True,
            emits_structured_decision_audit=True,
        )

    def manifest(self) -> dict[str, Any]:
        payload = super().manifest()
        payload.update(
            {
                "role_id": self.role_id,
                "requires_online_model": True,
                "provider_model": self.client.model,
                "prompt_contract_version": PROMPT_CONTRACT_VERSION,
                "prompt_hash": _prompt_hash(),
                "spectrum_disclosure": self.spectrum_disclosure,
                "failure_policy": "retain_as_invalid_operation_without_harness_closeout",
                "private_reasoning_retained": False,
            }
        )
        return payload

    def method_resource_usage(self) -> dict[str, Any]:
        pricing_factory = getattr(self.client, "pricing_snapshot", None)
        cost_factory = getattr(self.client, "estimate_cost_usd", None)
        pricing = pricing_factory() if callable(pricing_factory) else None
        accounting_complete = isinstance(pricing, dict) and callable(cost_factory)
        cost = (
            float(cost_factory(self._usage))
            if isinstance(pricing, dict) and callable(cost_factory)
            else 0.0
        )
        return {
            "schema_version": "chemworld-method-resource-usage-0.1",
            "accounting_complete": accounting_complete,
            "usage_source": "provider_usage_and_frozen_price_snapshot",
            "model_call_count": self._model_call_count,
            "input_token_count": int(self._usage["prompt_tokens"]),
            "output_token_count": int(self._usage["completion_tokens"]),
            "monetary_cost_usd": cost,
            "training_environment_step_count": 0,
            "cpu_time_s": 0.0,
            "gpu_time_s": 0.0,
            "model_provenance": {
                "provider": "DeepSeek",
                "model_id": self.client.model,
                "model_snapshot_or_access_date": (
                    pricing.get("access_date") if isinstance(pricing, dict) else None
                ),
                "prompt_hash": _prompt_hash(),
                "request_parameters": {
                    "response_format": "json_object",
                    "thinking": bool(getattr(self.client, "thinking", False)),
                    "reasoning_effort": getattr(self.client, "reasoning_effort", None),
                    "logical_decisions": self._logical_decision_count,
                    "spectrum_disclosure": self.spectrum_disclosure,
                },
                "tokenizer_or_provider_usage_source": "DeepSeek response.usage",
                "pricing": pricing,
                "private_reasoning_retained": False,
            },
        }

    def _build_prompt(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> str:
        tool_json = public_view.get("tool_json", {})
        if not isinstance(tool_json, dict):
            tool_json = {}
        supplied_context = context.to_dict()
        if self.spectrum_disclosure == "masked":
            supplied_context["latest_spectra"] = {
                "masked": True,
                "reason": "paired spectral-information ablation",
            }
            tool_json = dict(tool_json)
            tool_json.pop("raw_signal", None)
            processed = dict(tool_json.get("processed_estimate", {}))
            for key in list(processed):
                if "peak" in key or "spectrum" in key or "spectra" in key:
                    processed.pop(key, None)
            tool_json["processed_estimate"] = processed
            lab_report = dict(tool_json.get("lab_report", {}))
            lab_report.pop("spectra_summary", None)
            tool_json["lab_report"] = lab_report
        prompt_payload = {
            "instruction": (
                "Choose exactly one next operation. Use observations and experiment memory "
                "to distinguish exploration, exploitation, replication, and measurement. "
                "If a public spectrum is supplied, identify only visible axes/features and "
                "state how they affect the decision; never invent peaks or identities. The "
                "harness will not repair, terminate, or assay on your behalf."
            ),
            "task_contract": to_builtin(self.task_info),
            "decision_context": to_builtin(supplied_context),
            "public_tool_view": to_builtin(tool_json),
            "completed_experiment_memory": to_builtin(self._experiment_memory),
            "recent_decisions": to_builtin(self._recent_decisions),
            "required_json_shape": {
                "action": {"operation": "exact operation plus required fields"},
                "evidence": ["short public observation or supplied spectral feature"],
                "spectrum_interpretation": "supported concise reading or no spectrum available",
                "hypothesis": "short testable expectation",
                "uncertainty": "number from 0 to 1",
                "rationale": "concise evidence-to-action justification",
            },
        }
        return json.dumps(prompt_payload, ensure_ascii=False, sort_keys=True)

    def _normalize_decision(
        self,
        payload: dict[str, Any],
        *,
        context: AgentDecisionContext,
    ) -> dict[str, Any]:
        raw_action = payload.get("action")
        action = raw_action if isinstance(raw_action, dict) else None
        if not action or not action.get("operation"):
            raise ValueError("model decision is missing action.operation")
        evidence_raw = payload.get("evidence")
        evidence = (
            [str(item) for item in evidence_raw[:6] if str(item).strip()]
            if isinstance(evidence_raw, list)
            else []
        )
        if not evidence:
            raise ValueError("model decision is missing public evidence")
        hypothesis = str(payload.get("hypothesis") or "").strip()
        rationale = str(payload.get("rationale") or "").strip()
        if not hypothesis or not rationale:
            raise ValueError("model decision is missing hypothesis or rationale")
        raw_uncertainty = payload.get("uncertainty")
        if isinstance(raw_uncertainty, bool) or not isinstance(raw_uncertainty, int | float):
            raise ValueError("model decision uncertainty must be numeric")
        uncertainty = float(raw_uncertainty)
        if not 0.0 <= uncertainty <= 1.0:
            raise ValueError("model decision uncertainty must be in [0, 1]")
        return {
            "action": to_builtin(action),
            "evidence": evidence,
            "spectrum_interpretation": str(
                payload.get("spectrum_interpretation") or "No spectrum available."
            ),
            "hypothesis": hypothesis,
            "uncertainty": uncertainty,
            "rationale": rationale,
            "adaptation_source": self._adaptation_source(context),
        }

    def _failure_decision(
        self,
        context: AgentDecisionContext,
        error: Exception,
    ) -> dict[str, Any]:
        error_kind = type(error).__name__
        return {
            "action": {"operation": "model_failure"},
            "evidence": [f"Provider or structured-output failure: {error_kind}."],
            "spectrum_interpretation": "Unavailable because no valid model decision was returned.",
            "hypothesis": "No executable hypothesis was produced.",
            "uncertainty": 1.0,
            "rationale": "Retain the failed decision as an invalid operation for fair evaluation.",
            "adaptation_source": self._adaptation_source(context),
            "provider_attempts": max(int(getattr(error, "attempts", 1)), 1),
            "status": "model_failure",
            "error_type": error_kind,
        }

    def _adaptation_source(self, context: AgentDecisionContext) -> str:
        spectra = context.latest_spectra
        has_spectrum = bool(
            spectra.get("has_spectral_packet")
            or spectra.get("raw_signal")
            or spectra.get("processed_estimate")
        )
        if self.spectrum_disclosure == "assigned" and has_spectrum:
            return "spectrum"
        if self._experiment_memory:
            return "experiment_memory"
        if context.previous_event_type == "measurement_result":
            return "measurement"
        if context.constraint_flags:
            return "validator"
        return "none"

    def _record_provider_usage(self, attempts: int, usage: dict[str, Any]) -> None:
        self._model_call_count += max(int(attempts), 1)
        for key in self._usage:
            value = usage.get(key, 0)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                self._usage[key] += value


def _prompt_hash() -> str:
    return hashlib.sha256(
        (SYSTEM_PROMPT + "|" + PROMPT_CONTRACT_VERSION).encode("utf-8")
    ).hexdigest()


def _empty_usage() -> dict[str, int]:
    return {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 0,
    }


def _prompt_memory_decision(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        key: to_builtin(decision[key])
        for key in (
            "action",
            "evidence",
            "spectrum_interpretation",
            "hypothesis",
            "uncertainty",
            "rationale",
            "adaptation_source",
            "status",
        )
        if key in decision
    }


__all__ = [
    "PROMPT_CONTRACT_VERSION",
    "SYSTEM_PROMPT",
    "JsonPlannerClientLike",
    "LiveLLMAgent",
    "SpectrumDisclosure",
]
