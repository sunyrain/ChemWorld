"""Operation-level live-LLM adapter for the official benchmark runner.

The adapter intentionally owns no provider SDK.  A small JSON client is injected so
the official runner, fake-client tests, and provider-specific launchers all share the
same interaction semantics.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal, Protocol, cast

from chemworld.agent_interface import experiment_lifecycle_contract
from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.interaction import AgentDecisionContext, InteractionCapabilities
from chemworld.data.logging import to_builtin

SpectrumDisclosure = Literal["assigned", "unassigned", "masked"]

SYSTEM_PROMPT = """You are an operation-level agent in the ChemWorld causal world-model environment.
Use only the supplied public task contract, observations, spectra, memory, and action schemas.
Choose exactly one next operation and return exactly one JSON object. Never claim hidden
chemical identities or hidden simulator state. Do not provide private chain-of-thought.
Provide only a concise public audit: evidence, spectrum interpretation, hypothesis,
uncertainty, rationale, and the selected action using exact schema field names.
"""

PROMPT_CONTRACT_VERSION = "chemworld-live-llm-operation-json-0.7"
PROMPT_STATE_VERSION = "chemworld-live-llm-public-prompt-state-0.1"

_MAX_SPECTRUM_SERIES_POINTS = 64

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


class LiveLLMProviderUnavailableError(OSError):
    """Fail a formal cell without publishing a method-performance terminal."""

    def __init__(self, cause: Exception) -> None:
        super().__init__("live-LLM provider was unavailable before a billable response")
        self.provider_error_type = type(cause).__name__
        self.status_code = getattr(cause, "status_code", None)
        self.retryable = bool(getattr(cause, "retryable", False))
        self.attempts = max(int(getattr(cause, "attempts", 1)), 1)


class LiveLLMAgent(BaseAgent):
    """Use one provider decision per operation in the official runner.

    Provider and output failures are normally retained as invalid ``model_failure``
    actions.  Formal runs may instead fail fast when every provider attempt was rejected
    before billing, so an external outage cannot masquerade as method performance.  The
    harness never repairs an action or performs a terminal assay on the model's behalf.
    """

    name = "live_llm"

    def __init__(
        self,
        client: JsonPlannerClientLike,
        *,
        role_id: str,
        spectrum_disclosure: SpectrumDisclosure = "assigned",
        recent_decision_limit: int = 4,
        experiment_memory_limit: int = 4,
        response_max_tokens: int | None = None,
        fail_fast_on_unbillable_provider_failure: bool = False,
    ) -> None:
        if spectrum_disclosure not in {"assigned", "unassigned", "masked"}:
            raise ValueError(
                "spectrum_disclosure must be assigned, unassigned, or masked"
            )
        if recent_decision_limit <= 0 or experiment_memory_limit <= 0:
            raise ValueError("memory limits must be positive")
        if response_max_tokens is not None and response_max_tokens <= 0:
            raise ValueError("response_max_tokens must be positive")
        self.client = client
        self.role_id = role_id
        self.spectrum_disclosure = spectrum_disclosure
        self.recent_decision_limit = int(recent_decision_limit)
        self.experiment_memory_limit = int(experiment_memory_limit)
        self.response_max_tokens = (
            int(response_max_tokens)
            if response_max_tokens is not None
            else (8000 if bool(getattr(client, "thinking", False)) else 2000)
        )
        self.fail_fast_on_unbillable_provider_failure = bool(
            fail_fast_on_unbillable_provider_failure
        )

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._usage = _empty_usage()
        self._model_call_count = 0
        self._recent_decisions: list[dict[str, Any]] = []
        self._experiment_memory: list[dict[str, Any]] = []
        self._current_experiment_operations: list[dict[str, Any]] = []
        self._completed_experiment_count = 0
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

    def export_prompt_state(self) -> dict[str, Any]:
        """Export only public prompt memory for controlled same-prefix branching.

        Provider receipts, usage counters, private reasoning, and hidden environment state
        are deliberately excluded. The snapshot is bound to the current compact public
        task contract and can only be restored after ``reset`` on that same contract.
        """

        return {
            "schema_version": PROMPT_STATE_VERSION,
            "task_contract_sha256": _compact_task_contract_sha256(self.task_info),
            "recent_decisions": copy.deepcopy(to_builtin(self._recent_decisions)),
            "completed_experiment_memory": copy.deepcopy(
                to_builtin(self._experiment_memory)
            ),
            "current_experiment_operations": copy.deepcopy(
                to_builtin(self._current_experiment_operations)
            ),
            "completed_experiment_count": self._completed_experiment_count,
            "pending_historical_spectrum_id": self._pending_historical_spectrum_id,
        }

    def restore_prompt_state(self, state: Mapping[str, Any]) -> None:
        """Restore a validated public-memory snapshot for a local causal audit branch."""

        if state.get("schema_version") != PROMPT_STATE_VERSION:
            raise ValueError("unsupported live-LLM prompt-state schema")
        expected = _compact_task_contract_sha256(self.task_info)
        if state.get("task_contract_sha256") != expected:
            raise ValueError("prompt state does not match the active public task contract")
        recent = state.get("recent_decisions")
        experiments = state.get("completed_experiment_memory")
        operations = state.get("current_experiment_operations")
        if (
            not isinstance(recent, list)
            or not isinstance(experiments, list)
            or not isinstance(operations, list)
        ):
            raise ValueError("prompt-state memory fields must be lists")
        if not all(
            isinstance(record, dict)
            for memory in (recent, experiments, operations)
            for record in memory
        ):
            raise ValueError("prompt-state memory entries must be objects")
        completed = state.get("completed_experiment_count")
        if isinstance(completed, bool) or not isinstance(completed, int) or completed < 0:
            raise ValueError("completed_experiment_count must be a non-negative integer")
        pending = state.get("pending_historical_spectrum_id")
        if pending is not None and not isinstance(pending, str):
            raise ValueError("pending historical spectrum ID must be a string or null")
        recent_records = cast(list[dict[str, Any]], recent)
        experiment_records = cast(list[dict[str, Any]], experiments)
        operation_records = cast(list[dict[str, Any]], operations)
        self._recent_decisions = copy.deepcopy(recent_records)[-self.recent_decision_limit :]
        self._experiment_memory = copy.deepcopy(experiment_records)[
            -self.experiment_memory_limit :
        ]
        self._current_experiment_operations = copy.deepcopy(operation_records)
        self._completed_experiment_count = completed
        self._pending_historical_spectrum_id = pending
        self._last_decision = None
        self._last_context = {}
        self._last_public_view = {}

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
                max_tokens=self.response_max_tokens,
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
            if (
                self.fail_fast_on_unbillable_provider_failure
                and _all_provider_attempts_failed_unbillable(exc)
            ):
                raise LiveLLMProviderUnavailableError(exc) from exc
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
        self._current_experiment_operations.append(
            {
                "action": to_builtin(action),
                "observation": outcome["observation"],
                "constraint_flags": {
                    str(key): bool(value)
                    for key, value in outcome["constraint_flags"].items()
                    if value
                },
                "error_message": outcome["error_message"],
            }
        )
        final_assay = action.get("operation") == "measure" and action.get("instrument") == (
            "final_assay"
        )
        if outcome["experiment_ended"] or final_assay:
            self._completed_experiment_count += 1
            measurement_results = [
                item
                for item in self._current_experiment_operations
                if item["action"].get("operation") == "measure"
            ]
            self._experiment_memory.append(
                {
                    "experiment_index": self._completed_experiment_count,
                    "operation_count": len(self._current_experiment_operations),
                    "operation_sequence": [
                        item["action"] for item in self._current_experiment_operations
                    ],
                    "terminal_action": to_builtin(action),
                    "score": info.get("leaderboard_score"),
                    "visible_metrics": to_builtin(
                        self._last_context.get("visible_metrics", {})
                    ),
                    "constraint_flags": {
                        str(key): bool(value)
                        for key, value in outcome["constraint_flags"].items()
                        if value
                    },
                    "terminal_observation": outcome["observation"],
                    "measurement_results": measurement_results,
                }
            )
            self._experiment_memory = self._experiment_memory[
                -self.experiment_memory_limit :
            ]
            self._recent_decisions = []
            self._current_experiment_operations = []

    def decision_audit(self) -> dict[str, Any] | None:
        if self._last_decision is None:
            return None
        return {
            "action": dict(self._last_decision["action"]),
            "evidence": list(self._last_decision["evidence"]),
            "spectrum_interpretation": str(
                self._last_decision["spectrum_interpretation"]
            ),
            "hypothesis": str(self._last_decision["hypothesis"]),
            "uncertainty": float(self._last_decision["uncertainty"]),
            "rationale": str(self._last_decision["rationale"]),
            "request_historical_spectrum_id": self._last_decision.get(
                "request_historical_spectrum_id"
            ),
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
                "formal_unbillable_provider_failure_policy": (
                    "raise_resumable_infrastructure_interruption"
                    if self.fail_fast_on_unbillable_provider_failure
                    else "retain_as_invalid_operation"
                ),
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
                    "reasoning_effort": (
                        getattr(self.client, "reasoning_effort", None)
                        if bool(getattr(self.client, "thinking", False))
                        else None
                    ),
                    "max_tokens": self.response_max_tokens,
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
        supplied_context = _compact_prompt_spectra(supplied_context)
        prompt_payload = {
            "instruction": (
                "Choose exactly one next operation. Use observations and experiment memory "
                "to distinguish exploration, exploitation, replication, and measurement. "
                "If a public spectrum is supplied, identify only visible axes/features and "
                "state how they affect the decision; never invent peaks or identities. A "
                "spectrum is newly measured only when observation_provenance."
                "current_spectral_packet is true; catalog entries and retained metrics are "
                "historical. A "
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
        masked_tool = _mask_spectral_tool_view(tool)
        provenance = supplied.get("observation_provenance")
        if isinstance(provenance, dict):
            provenance["current_spectral_packet"] = False
        masked_latest: dict[str, Any] = {
            "spectrum_condition": "masked",
            "available": False,
        }
        for key in ("raw_signal", "processed_estimate"):
            value = masked_tool.get(key)
            if isinstance(value, dict) and value:
                masked_latest[key] = value
        supplied["latest_spectra"] = masked_latest
        if supplied.get("requested_historical_spectrum"):
            request = supplied["requested_historical_spectrum"]
            supplied["requested_historical_spectrum"] = {
                "spectrum_id": request.get("spectrum_id"),
                "status": request.get("status"),
                "spectrum_condition": "masked",
                "available": False,
            }
        return supplied, masked_tool
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


def _all_provider_attempts_failed_unbillable(error: Exception) -> bool:
    raw_records = getattr(error, "attempt_records", ())
    if not isinstance(raw_records, Sequence) or isinstance(raw_records, str | bytes):
        return False
    records = tuple(raw_records)
    return bool(records) and all(
        isinstance(record, Mapping)
        and record.get("status") == "failed"
        and record.get("billable") is False
        for record in records
    )


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


def _compact_task_contract_sha256(task_info: dict[str, Any]) -> str:
    payload = json.dumps(
        _compact_task_contract(task_info),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _compact_task_contract(task_info: dict[str, Any]) -> dict[str, Any]:
    """Keep user-facing decision facts without resending backend internals."""

    keys = (
        "task_goal",
        "description",
        "task_id",
        "objective",
        "budget",
        "episode_mode",
        "safety_limit",
        "success_metrics",
        "constraints",
        "termination_policy",
        "measurement_policy",
        "experiment_lifecycle",
        "observation_policy",
        "allowed_operations",
        "allowed_instruments",
        "material_catalog",
        "method_budget_contract",
        "observation_keys",
        "scenario_id",
    )
    compact = {
        key: to_builtin(task_info[key])
        for key in keys
        if key in task_info and task_info[key] is not None
    }
    compact.setdefault(
        "experiment_lifecycle",
        experiment_lifecycle_contract(task_info.get("episode_mode")),
    )
    if "task_goal" not in compact and compact.get("description"):
        compact["task_goal"] = compact["description"]
    return compact


def _compact_tool_view(tool_json: dict[str, Any]) -> dict[str, Any]:
    """Retain exact affordances without duplicating decision-context evidence."""

    compact: dict[str, Any] = {
        key: to_builtin(tool_json[key])
        for key in (
            "task",
            "uncertainty",
            "cost",
            "cost_components",
            "constraints",
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


def _compact_prompt_spectra(context: dict[str, Any]) -> dict[str, Any]:
    """Bound dense spectral transport while keeping peaks, axes, and public features.

    The full public packet remains in the trajectory and UI artifacts.  Only the JSON
    sent to the provider is compacted: primary numeric curves are uniformly sampled,
    replicate curves become numeric summaries, and all peak/assignment tables remain
    available.  ``build_decision_context`` already copies current and requested spectra
    from the tool view, so the tool-view copy is deliberately omitted above.
    """

    compact = to_builtin(context)
    latest = compact.get("latest_spectra")
    if (
        isinstance(latest, dict)
        and "has_spectral_packet" in latest
        and not latest["has_spectral_packet"]
    ):
        latest["raw_signal"] = {}
        latest["processed_estimate"] = {}
        latest["uncertainty"] = {}
    for key in ("latest_spectra", "requested_historical_spectrum"):
        value = compact.get(key)
        if isinstance(value, dict) and value:
            compact[key] = _compact_spectral_payload(value)
    return compact


def _compact_spectral_payload(payload: Any, *, field: str = "") -> Any:
    if isinstance(payload, dict):
        return {
            str(key): _compact_spectral_payload(value, field=str(key))
            for key, value in payload.items()
        }
    if isinstance(payload, list):
        if field == "replicate_signals" and all(
            isinstance(item, list) and _is_numeric_series(item) for item in payload
        ):
            return {
                "representation": "summary_only",
                "replicate_count": len(payload),
                "summaries": [_numeric_series_summary(item) for item in payload],
            }
        if _is_numeric_series(payload):
            return _compact_numeric_series(payload)
        return [_compact_spectral_payload(item) for item in payload]
    if isinstance(payload, float):
        return _round_public_float(payload)
    return to_builtin(payload)


def _is_numeric_series(values: list[Any]) -> bool:
    return bool(values) and all(
        not isinstance(value, bool) and isinstance(value, int | float) for value in values
    )


def _compact_numeric_series(values: list[Any]) -> list[Any] | dict[str, Any]:
    rounded = [_round_public_float(float(value)) for value in values]
    if len(rounded) <= _MAX_SPECTRUM_SERIES_POINTS:
        return rounded
    last = len(rounded) - 1
    indices = sorted(
        {
            round(position * last / (_MAX_SPECTRUM_SERIES_POINTS - 1))
            for position in range(_MAX_SPECTRUM_SERIES_POINTS)
        }
    )
    return {
        "representation": "uniform_index_sample",
        "original_point_count": len(rounded),
        "sample_indices": indices,
        "values": [rounded[index] for index in indices],
    }


def _numeric_series_summary(values: list[Any]) -> dict[str, Any]:
    numeric = [float(value) for value in values]
    return {
        "point_count": len(numeric),
        "minimum": _round_public_float(min(numeric)),
        "maximum": _round_public_float(max(numeric)),
        "mean": _round_public_float(sum(numeric) / len(numeric)),
    }


def _round_public_float(value: float) -> float:
    return float(f"{value:.8g}")


def _compact_action_affordance(action: dict[str, Any]) -> dict[str, Any]:
    schema = action.get("schema")
    public_schema = (
        {
            key: to_builtin(schema[key])
            for key in (
                "schema_version",
                "operation",
                "required_fields",
                "fields",
                "constraints",
            )
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
    "PROMPT_STATE_VERSION",
    "SYSTEM_PROMPT",
    "JsonPlannerClientLike",
    "LiveLLMAgent",
    "LiveLLMProviderUnavailableError",
    "SpectrumDisclosure",
]
