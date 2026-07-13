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

SpectrumDisclosure = Literal["assigned", "unassigned", "masked"]

SYSTEM_PROMPT = """You are an operation-level agent in the ChemWorld virtual laboratory.
Use only the supplied public task contract, observations, spectra, memory, and action schemas.
Choose exactly one next operation and return exactly one JSON object. Never claim hidden
chemical identities or hidden simulator state. Do not provide private chain-of-thought.
Provide only a concise public audit: evidence, spectrum interpretation, hypothesis,
uncertainty, rationale, and the selected action using exact schema field names.
"""

PROMPT_CONTRACT_VERSION = "chemworld-live-llm-operation-json-0.4"

_PURE_SPECTRAL_PACKET_KINDS = {
    "gc_chromatogram",
    "hplc_chromatogram",
    "ir_spectrum",
    "nmr_1h_spectrum",
    "uvvis_spectrum",
}
_SPECTRAL_FIELD_MARKERS = (
    "assignment",
    "channel",
    "chemical_shift",
    "chromatogram",
    "peak",
    "retention",
    "spectra",
    "spectrum",
    "wavelength",
    "wavenumber",
)


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
        if spectrum_disclosure not in {"assigned", "unassigned", "masked"}:
            raise ValueError(
                "spectrum_disclosure must be assigned, unassigned, or masked"
            )
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
        self._pending_historical_spectrum_id: str | None = None
        self._provider_failure_count = 0
        self._retry_count = 0
        self._system_fingerprints: set[str] = set()
        self._provider_attempt_records: list[dict[str, Any]] = []

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
        completion: JsonCompletionLike | None = None
        try:
            completion = self.client.complete_json(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                max_tokens=8000 if bool(getattr(self.client, "thinking", False)) else 2000,
            )
        except Exception as exc:
            attempts = max(int(getattr(exc, "attempts", 1)), 1)
            usage = getattr(exc, "usage", {})
            self._record_provider_usage(attempts, usage if isinstance(usage, dict) else {})
            self._record_provider_attempts(
                getattr(exc, "attempt_records", ()),
                fallback_status="failed",
                fallback_attempts=attempts,
                fallback_usage=usage if isinstance(usage, dict) else {},
            )
            self._provider_failure_count += 1
            self._retry_count += max(attempts - 1, 0)
            decision = self._failure_decision(context, exc)
        else:
            self._record_provider_usage(completion.attempts, completion.usage)
            self._record_provider_attempts(
                getattr(completion, "attempt_records", ()),
                fallback_status="succeeded",
                fallback_attempts=completion.attempts,
                fallback_usage=completion.usage,
                fallback_request_id=getattr(completion, "request_id", None),
                fallback_model=completion.model,
            )
            try:
                decision = self._normalize_decision(completion.payload, context=context)
            except Exception as exc:
                self._provider_failure_count += 1
                decision = self._failure_decision(context, exc)
            else:
                decision["status"] = "model_decision"
            decision["provider_model"] = str(completion.model)
            decision["provider_attempts"] = int(completion.attempts)
            decision["provider_usage"] = to_builtin(completion.usage)
            decision["provider_request_id"] = getattr(completion, "request_id", None)
            decision["system_fingerprint"] = getattr(
                completion, "system_fingerprint", None
            )
            decision["finish_reason"] = getattr(completion, "finish_reason", None)
            decision["reasoning_content_present"] = bool(
                getattr(completion, "reasoning_content_present", False)
            )
            decision["reasoning_character_count"] = int(
                getattr(completion, "reasoning_character_count", 0)
            )
            fingerprint = decision["system_fingerprint"]
            if isinstance(fingerprint, str) and fingerprint:
                self._system_fingerprints.add(fingerprint)
            self._retry_count += max(int(completion.attempts) - 1, 0)
        self._last_decision = decision
        self._recent_decisions.append(_prompt_memory_decision(decision))
        self._recent_decisions = self._recent_decisions[-self.recent_decision_limit :]
        return dict(decision["action"])

    def consume_historical_spectrum_request(self) -> str | None:
        """Consume the previous decision's explicit request at the next operation."""

        spectrum_id = self._pending_historical_spectrum_id
        self._pending_historical_spectrum_id = None
        return spectrum_id

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
            "observation": _compact_observation(observation),
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
            consumes_spectra=self.spectrum_disclosure != "masked",
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
                "historical_spectrum_access": (
                    "explicit_request_by_public_spectrum_id_delivered_next_decision"
                ),
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
                "provider_failure_count": self._provider_failure_count,
                "retry_count": self._retry_count,
                "observed_system_fingerprints": sorted(self._system_fingerprints),
            },
        }

    def provider_receipts(self) -> list[dict[str, Any]]:
        """Return attempt-level provider evidence without prompts or private reasoning."""

        pricing_factory = getattr(self.client, "pricing_snapshot", None)
        cost_factory = getattr(self.client, "estimate_cost_usd", None)
        pricing = pricing_factory() if callable(pricing_factory) else {}
        pricing_digest = (
            pricing.get("pricing_version_sha256") if isinstance(pricing, dict) else None
        )
        receipts: list[dict[str, Any]] = []
        for raw in self._provider_attempt_records:
            usage = raw.get("usage")
            normalized = usage if isinstance(usage, dict) else {}
            usage_complete = bool(raw.get("usage_complete", False))
            billable = bool(raw.get("billable", False))
            billed_cost = (
                float(cost_factory(normalized))
                if callable(cost_factory) and usage_complete and billable
                else 0.0
            )
            receipts.append(
                {
                    "schema_version": "chemworld-provider-receipt-0.4",
                    "request_id": raw.get("request_id"),
                    "logical_decision_index": raw["logical_decision_index"],
                    "attempt_index": raw["attempt_index"],
                    "status": raw["status"],
                    "provider": "DeepSeek",
                    "model_id": raw.get("model_id", self.client.model),
                    "pricing_version_sha256": pricing_digest,
                    "usage_source": raw.get("usage_source", "unavailable"),
                    "usage_complete": usage_complete,
                    "billable": billable,
                    "input_token_count": int(normalized.get("prompt_tokens", 0) or 0),
                    "output_token_count": int(normalized.get("completion_tokens", 0) or 0),
                    "input_cache_hit_token_count": int(
                        normalized.get("prompt_cache_hit_tokens", 0) or 0
                    ),
                    "input_cache_miss_token_count": int(
                        normalized.get("prompt_cache_miss_tokens", 0) or 0
                    ),
                    "billed_cost_usd": billed_cost,
                    "failure_type": raw.get("failure_type"),
                }
            )
        return receipts

    def _build_prompt(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> str:
        tool_json = public_view.get("tool_json", {})
        if not isinstance(tool_json, dict):
            tool_json = {}
        supplied_context = context.to_dict()
        supplied_context, tool_json = _condition_spectrum_inputs(
            supplied_context,
            tool_json,
            condition=self.spectrum_disclosure,
        )
        prompt_payload = {
            "instruction": (
                "Choose exactly one next operation. Use observations and experiment memory "
                "to distinguish exploration, exploitation, replication, and measurement. "
                "If a public spectrum is supplied, identify only visible axes/features and "
                "state how they affect the decision; never invent peaks or identities. A "
                "historical packet is supplied only after requesting its public spectrum_id "
                "in the preceding decision. The harness will not repair, terminate, or assay "
                "on your behalf."
            ),
            "task_contract": _compact_task_contract(self.task_info),
            "decision_context": to_builtin(supplied_context),
            "public_tool_view": _compact_tool_view(tool_json),
            "completed_experiment_memory": to_builtin(self._experiment_memory),
            "recent_decisions": to_builtin(self._recent_decisions),
            "required_json_shape": {
                "action": {"operation": "exact operation plus required fields"},
                "evidence": ["short public observation or supplied spectral feature"],
                "spectrum_interpretation": "supported concise reading or no spectrum available",
                "hypothesis": "short testable expectation",
                "uncertainty": "number from 0 to 1",
                "rationale": "concise evidence-to-action justification",
                "request_historical_spectrum_id": (
                    "optional public spectrum_id to retrieve for the next decision, or null"
                ),
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
        raw_request = payload.get("request_historical_spectrum_id")
        if raw_request is None:
            spectrum_request = None
        elif isinstance(raw_request, str) and raw_request.strip():
            spectrum_request = raw_request.strip()
        else:
            raise ValueError(
                "request_historical_spectrum_id must be a non-empty string or null"
            )
        self._pending_historical_spectrum_id = spectrum_request
        return {
            "action": to_builtin(action),
            "evidence": evidence,
            "spectrum_interpretation": str(
                payload.get("spectrum_interpretation") or "No spectrum available."
            ),
            "hypothesis": hypothesis,
            "uncertainty": uncertainty,
            "rationale": rationale,
            "request_historical_spectrum_id": spectrum_request,
            "adaptation_source": self._adaptation_source(context),
        }

    def _failure_decision(
        self,
        context: AgentDecisionContext,
        error: Exception,
    ) -> dict[str, Any]:
        error_kind = type(error).__name__
        self._pending_historical_spectrum_id = None
        return {
            "action": {"operation": "model_failure"},
            "evidence": [f"Provider or structured-output failure: {error_kind}."],
            "spectrum_interpretation": "Unavailable because no valid model decision was returned.",
            "hypothesis": "No executable hypothesis was produced.",
            "uncertainty": 1.0,
            "rationale": "Retain the failed decision as an invalid operation for fair evaluation.",
            "request_historical_spectrum_id": None,
            "adaptation_source": self._adaptation_source(context),
            "provider_attempts": max(int(getattr(error, "attempts", 1)), 1),
            "status": "model_failure",
            "error_type": error_kind,
        }

    def _adaptation_source(self, context: AgentDecisionContext) -> str:
        spectra = context.latest_spectra
        requested = context.requested_historical_spectrum
        has_spectrum = bool(
            spectra.get("has_spectral_packet")
            or spectra.get("raw_signal")
            or spectra.get("processed_estimate")
            or requested.get("raw_signal")
        )
        if self.spectrum_disclosure != "masked" and has_spectrum:
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

    def _record_provider_attempts(
        self,
        records: Any,
        *,
        fallback_status: str,
        fallback_attempts: int,
        fallback_usage: dict[str, Any],
        fallback_request_id: str | None = None,
        fallback_model: str | None = None,
    ) -> None:
        supplied = (
            [dict(item) for item in records if isinstance(item, dict)]
            if isinstance(records, list | tuple)
            else []
        )
        if not supplied:
            supplied = [
                {
                    "attempt_index": 1,
                    "status": fallback_status,
                    "request_id": fallback_request_id,
                    "model_id": fallback_model or self.client.model,
                    "usage": to_builtin(fallback_usage),
                    "usage_complete": False,
                    "billable": False,
                    "usage_source": "unavailable",
                    "reported_attempt_count": int(fallback_attempts),
                }
            ]
        for raw in supplied:
            raw["logical_decision_index"] = self._logical_decision_count
            self._provider_attempt_records.append(to_builtin(raw))


def _prompt_hash() -> str:
    return hashlib.sha256(
        (SYSTEM_PROMPT + "|" + PROMPT_CONTRACT_VERSION).encode("utf-8")
    ).hexdigest()


def _condition_spectrum_inputs(
    context: dict[str, Any],
    tool_view: dict[str, Any],
    *,
    condition: SpectrumDisclosure,
) -> tuple[dict[str, Any], dict[str, Any]]:
    supplied = to_builtin(context)
    tool = to_builtin(tool_view)
    if condition == "masked":
        supplied["latest_spectra"] = {
            "spectrum_condition": "masked",
            "available": False,
        }
        if supplied.get("requested_historical_spectrum"):
            request = supplied["requested_historical_spectrum"]
            supplied["requested_historical_spectrum"] = {
                "spectrum_id": request.get("spectrum_id"),
                "status": request.get("status"),
                "spectrum_condition": "masked",
                "available": False,
            }
        return supplied, _mask_spectral_tool_view(tool)
    if condition == "unassigned":
        supplied["latest_spectra"] = _unassign_spectral_fields(
            supplied.get("latest_spectra", {})
        )
        supplied["requested_historical_spectrum"] = _unassign_spectral_fields(
            supplied.get("requested_historical_spectrum", {})
        )
        return supplied, _unassign_spectral_tool_view(tool)
    for key in ("latest_spectra", "requested_historical_spectrum"):
        packet = supplied.get(key)
        if isinstance(packet, dict) and packet:
            packet["spectrum_condition"] = "assigned"
    return supplied, tool


def _mask_spectral_tool_view(tool_json: dict[str, Any]) -> dict[str, Any]:
    """Remove spectral evidence while preserving every non-spectral public field."""

    masked = dict(tool_json)
    raw_signal = masked.get("raw_signal")
    if isinstance(raw_signal, dict):
        kind = str(raw_signal.get("kind", ""))
        if kind in _PURE_SPECTRAL_PACKET_KINDS:
            masked.pop("raw_signal", None)
        else:
            masked["raw_signal"] = _redact_spectral_fields(raw_signal)
    processed = masked.get("processed_estimate")
    if isinstance(processed, dict):
        masked["processed_estimate"] = _redact_spectral_fields(processed)
    lab_report = masked.get("lab_report")
    if isinstance(lab_report, dict):
        public_report = dict(lab_report)
        public_report.pop("spectra_summary", None)
        masked["lab_report"] = public_report
    requested = masked.get("requested_historical_spectrum")
    if isinstance(requested, dict) and requested:
        masked["requested_historical_spectrum"] = {
            "spectrum_id": requested.get("spectrum_id"),
            "status": requested.get("status"),
            "spectrum_condition": "masked",
            "available": False,
        }
    return masked


def _unassign_spectral_tool_view(tool_json: dict[str, Any]) -> dict[str, Any]:
    unassigned = to_builtin(tool_json)
    for key in ("raw_signal", "processed_estimate", "requested_historical_spectrum"):
        if key in unassigned:
            unassigned[key] = _unassign_spectral_fields(unassigned[key])
    lab_report = unassigned.get("lab_report")
    if isinstance(lab_report, dict) and "spectra_summary" in lab_report:
        lab_report["spectra_summary"] = _unassign_spectral_fields(
            lab_report["spectra_summary"]
        )
    return unassigned


def _unassign_spectral_fields(payload: Any) -> Any:
    if isinstance(payload, dict):
        result: dict[str, Any] = {}
        for raw_key, value in payload.items():
            key = str(raw_key)
            normalized = key.lower()
            if normalized in {
                "species_id",
                "analyte_id",
                "group",
                "metadata",
                "identity",
            }:
                continue
            if normalized == "assignments":
                result[key] = []
            elif normalized == "assignment":
                result[key] = "unassigned"
            else:
                result[key] = _unassign_spectral_fields(value)
        if result and (
            "raw_signal" in result
            or "peaks" in result
            or "bands" in result
            or "spectrum_id" in result
        ):
            result["spectrum_condition"] = "unassigned"
        return result
    if isinstance(payload, list):
        return [_unassign_spectral_fields(item) for item in payload]
    return to_builtin(payload)


def _redact_spectral_fields(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            str(key): _redact_spectral_fields(value)
            for key, value in payload.items()
            if not _is_spectral_field(str(key))
        }
    if isinstance(payload, list):
        return [_redact_spectral_fields(item) for item in payload]
    return to_builtin(payload)


def _is_spectral_field(key: str) -> bool:
    normalized = key.lower()
    return any(marker in normalized for marker in _SPECTRAL_FIELD_MARKERS)


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
            "request_historical_spectrum_id",
            "adaptation_source",
            "status",
        )
        if key in decision
    }


def _compact_task_contract(task_info: dict[str, Any]) -> dict[str, Any]:
    """Keep user-facing decision facts without resending backend internals."""

    keys = (
        "task_id",
        "objective",
        "budget",
        "episode_mode",
        "safety_limit",
        "allowed_operations",
        "allowed_instruments",
        "material_catalog",
        "method_budget_contract",
        "observation_keys",
        "scenario_id",
    )
    return {
        key: to_builtin(task_info[key])
        for key in keys
        if key in task_info and task_info[key] is not None
    }


def _compact_tool_view(tool_json: dict[str, Any]) -> dict[str, Any]:
    """Retain exact affordances and evidence once, without duplicate reports."""

    compact: dict[str, Any] = {
        key: to_builtin(tool_json[key])
        for key in (
            "task",
            "raw_signal",
            "processed_estimate",
            "uncertainty",
            "cost",
            "cost_components",
            "constraints",
            "historical_spectrum_catalog",
            "requested_historical_spectrum",
        )
        if key in tool_json
    }
    observation = tool_json.get("observation")
    if isinstance(observation, dict):
        compact["observation"] = _compact_observation(observation)
    actions = tool_json.get("available_actions")
    if isinstance(actions, list):
        compact["available_actions"] = [
            _compact_action_affordance(item) for item in actions if isinstance(item, dict)
        ]
    return compact


def _compact_action_affordance(action: dict[str, Any]) -> dict[str, Any]:
    schema = action.get("schema")
    public_schema = (
        {
            key: to_builtin(schema[key])
            for key in ("operation", "required_fields", "fields")
            if key in schema
        }
        if isinstance(schema, dict)
        else {}
    )
    return {
        "operation": action.get("operation"),
        "valid": bool(action.get("valid", False)),
        "invalid_reasons": to_builtin(action.get("invalid_reasons", [])),
        "schema": public_schema,
    }


def _compact_observation(observation: dict[str, Any]) -> dict[str, Any]:
    return {
        str(key): to_builtin(value)
        for key, value in observation.items()
        if value is not None
    }


__all__ = [
    "PROMPT_CONTRACT_VERSION",
    "SYSTEM_PROMPT",
    "JsonPlannerClientLike",
    "LiveLLMAgent",
    "SpectrumDisclosure",
]
