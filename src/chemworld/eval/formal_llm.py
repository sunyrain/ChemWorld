"""Frozen live-LLM bindings and execution adapter for formal benchmark cells."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol, cast

from chemworld.agents.live_llm import LiveLLMAgent, SpectrumDisclosure
from chemworld.data.logging import load_jsonl
from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
from chemworld.eval.formal_runner import (
    CellIdentityError,
    FormalAdapterRegistry,
    FormalCellSpec,
    FormalExecutionAdapter,
    FormalMethodBinding,
    PrivateCellRuntime,
    canonical_sha256,
    file_sha256,
)
from chemworld.eval.resource_accounting_v0_4 import MethodKind
from chemworld.providers.deepseek import DeepSeekClient
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LLM_FREEZE_PATH = ROOT / "configs/methods/llm_v0.4/llm_methods.json"
LIVE_LLM_SOURCE_PATH = ROOT / "src/chemworld/agents/live_llm.py"
LLM_FREEZE_VERSION = "chemworld-live-llm-method-freeze-0.4.2"
LLM_METHOD_IDS = ("live_llm_a", "live_llm_b")
FORMAL_CELL_PROGRESS_VERSION = "chemworld-formal-cell-progress-0.1"

LLMMethodId = Literal["live_llm_a", "live_llm_b"]


class FormalLLMContractError(ValueError):
    """Raised when a live-LLM freeze or execution does not match its issued cell."""


class RunAgent(Protocol):
    def __call__(self, **kwargs: Any) -> Any: ...


ClientFactory = Callable[[Mapping[str, Any]], Any]


def _append_progress_event(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                dict(payload),
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )
        handle.flush()


def _formal_progress_callback(
    spec: FormalCellSpec,
    *,
    checkpoints: tuple[int, ...],
) -> Callable[[Any, list[dict[str, Any]]], None] | None:
    raw_path = os.environ.get("CHEMWORLD_FORMAL_PROGRESS_PATH")
    if not raw_path:
        return None
    path = Path(raw_path)
    emitted_checkpoints: set[int] = set()

    def report(record: Any, agent_trace: list[dict[str, Any]]) -> None:
        # Progress is deliberately limited to coarse public execution metadata.
        # Agent reasoning, action parameters, spectra, and private runtime values
        # remain in their existing controlled artifacts and never enter the inbox.
        del agent_trace
        resources = getattr(record, "method_resources", {})
        action = getattr(record, "action", {})
        info = getattr(record, "info", {})
        operation_count = resources.get("operation_count")
        complete_count = resources.get("complete_experiment_count")
        operation_type = action.get("operation") if isinstance(action, Mapping) else None
        transaction_status = (
            info.get("transaction_status") if isinstance(info, Mapping) else None
        )
        trajectory_event_type = getattr(record, "event_type", None)
        payload: dict[str, Any] = {
            "schema_version": FORMAL_CELL_PROGRESS_VERSION,
            "event_type": "operation_progress",
            "cell_identity_sha256": spec.cell_identity_sha256,
            "operation_count": operation_count,
            "complete_experiment_count": complete_count,
            "operation_type": operation_type,
            "transaction_status": transaction_status,
            "trajectory_event_type": trajectory_event_type,
        }
        _append_progress_event(path, payload)
        if complete_count in checkpoints and complete_count not in emitted_checkpoints:
            emitted_checkpoints.add(complete_count)
            _append_progress_event(
                path,
                {
                    "schema_version": FORMAL_CELL_PROGRESS_VERSION,
                    "event_type": "checkpoint",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "operation_count": operation_count,
                    "complete_experiment_count": complete_count,
                },
            )

    return report


def load_live_llm_method_freeze(
    path: str | Path = DEFAULT_LLM_FREEZE_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormalLLMContractError("live-LLM method freeze must be a JSON object")
    return payload


def _method_card(freeze: Mapping[str, Any], method_id: str) -> Mapping[str, Any]:
    methods = freeze.get("methods")
    card = methods.get(method_id) if isinstance(methods, Mapping) else None
    if not isinstance(card, Mapping):
        raise FormalLLMContractError(f"live-LLM method is not frozen: {method_id}")
    return card


def _model_config_payload(
    freeze: Mapping[str, Any], method_id: str, card: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": LLM_FREEZE_VERSION,
        "method_id": method_id,
        "provider": freeze.get("provider"),
        "base_url": freeze.get("base_url"),
        "provider_access_date": freeze.get("provider_access_date"),
        "model_id": card.get("model_id"),
        "role": card.get("role"),
        "request_configuration": card.get("request_configuration"),
    }


def live_llm_method_artifact_sha256(
    method_id: str,
    *,
    freeze: Mapping[str, Any] | None = None,
    freeze_path: str | Path = DEFAULT_LLM_FREEZE_PATH,
) -> str:
    resolved = load_live_llm_method_freeze(freeze_path) if freeze is None else freeze
    return canonical_sha256(
        {
            "schema_version": LLM_FREEZE_VERSION,
            "freeze_file_sha256": file_sha256(freeze_path),
            "method_id": method_id,
            "method_card": dict(_method_card(resolved, method_id)),
        }
    )


def formal_live_llm_method_bindings(
    freeze: Mapping[str, Any] | None = None,
    *,
    freeze_path: str | Path = DEFAULT_LLM_FREEZE_PATH,
) -> dict[str, FormalMethodBinding]:
    resolved = load_live_llm_method_freeze(freeze_path) if freeze is None else freeze
    audit = audit_live_llm_method_freeze(resolved)
    if audit["controls_ready"] is not True:
        raise CellIdentityError("live-LLM method freeze is not ready")
    prompt_sha256 = file_sha256(LIVE_LLM_SOURCE_PATH)
    return {
        method_id: FormalMethodBinding(
            method_id=method_id,
            kind="live_llm",
            artifact_sha256=live_llm_method_artifact_sha256(
                method_id,
                freeze=resolved,
                freeze_path=freeze_path,
            ),
            resource_profile="live_llm_evaluation",
            prompt_sha256=prompt_sha256,
            model_config_sha256=canonical_sha256(
                _model_config_payload(resolved, method_id, _method_card(resolved, method_id))
            ),
        )
        for method_id in LLM_METHOD_IDS
    }


def audit_live_llm_method_freeze(
    freeze: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = load_live_llm_method_freeze() if freeze is None else freeze
    methods = resolved.get("methods")
    conditions = resolved.get("supported_spectrum_conditions")
    interaction = resolved.get("interaction_contract")
    resources = resolved.get("resource_contract")
    pricing = resolved.get("pricing_usd_per_million_tokens")
    cards = methods if isinstance(methods, Mapping) else {}
    model_ids = {
        str(card.get("model_id"))
        for card in cards.values()
        if isinstance(card, Mapping)
    }
    pricing_checks: list[bool] = []
    request_checks: list[bool] = []
    for method_id in LLM_METHOD_IDS:
        card = cards.get(method_id)
        if not isinstance(card, Mapping):
            pricing_checks.append(False)
            request_checks.append(False)
            continue
        model_id = str(card.get("model_id") or "")
        request = card.get("request_configuration")
        frozen_price = pricing.get(model_id) if isinstance(pricing, Mapping) else None
        try:
            actual = DeepSeekClient(api_key="audit-only", model=model_id).pricing_snapshot()
        except Exception:
            pricing_checks.append(False)
        else:
            pricing_checks.append(
                isinstance(frozen_price, Mapping)
                and frozen_price.get("input_cache_hit")
                == actual["input_cache_hit_per_million_usd"]
                and frozen_price.get("input_cache_miss")
                == actual["input_cache_miss_per_million_usd"]
                and frozen_price.get("output") == actual["output_per_million_usd"]
                and actual["access_date"] == resolved.get("provider_access_date")
            )
        request_checks.append(
            isinstance(request, Mapping)
            and request.get("response_format") == "json_object"
            and request.get("max_tokens") == (8000 if request.get("thinking") else 2000)
            and request.get("max_attempts") == 3
            and request.get("temperature") is None
        )
    checks = {
        "schema": resolved.get("schema_version") == LLM_FREEZE_VERSION,
        "development_only": resolved.get("benchmark_claim_allowed") is False,
        "provider_identity": resolved.get("provider") == "DeepSeek"
        and resolved.get("base_url") == "https://api.deepseek.com"
        and resolved.get("provider_access_date") == "2026-07-13",
        "two_frozen_roles": set(cards) == set(LLM_METHOD_IDS)
        and model_ids == {"deepseek-v4-pro", "deepseek-v4-flash"},
        "three_spectrum_conditions": conditions == ["assigned", "unassigned", "masked"],
        "request_contracts_exact": all(request_checks),
        "pricing_matches_provider_snapshot": all(pricing_checks),
        "interaction_fail_closed": isinstance(interaction, Mapping)
        and interaction.get("decision_scope") == "operation"
        and interaction.get("automatic_action_repair") is False
        and interaction.get("automatic_closeout") is False,
        "private_reasoning_excluded": isinstance(interaction, Mapping)
        and interaction.get("private_chain_of_thought_requested") is False
        and interaction.get("private_reasoning_retained") is False,
        "resource_contract_complete": isinstance(resources, Mapping)
        and resources.get("provider_attempt_limit_per_operation") == 3
        and resources.get("input_token_limit_per_cell") == 1_000_000
        and resources.get("output_token_limit_per_cell") == 200_000
        and resources.get("monetary_cost_usd_limit_per_cell") == 2.0
        and resources.get("wall_time_limit_s_per_cell") == 1800.0
        and resources.get("training_environment_step_limit") == 0
        and all(
            isinstance(card, Mapping)
            and isinstance(card.get("request_configuration"), Mapping)
            and card["request_configuration"].get("max_attempts")
            == resources.get("provider_attempt_limit_per_operation")
            for card in cards.values()
        ),
        "prompt_source_present": LIVE_LLM_SOURCE_PATH.is_file(),
    }
    return {
        "schema_version": "chemworld-live-llm-method-freeze-audit-0.4",
        "controls_ready": all(checks.values()),
        "checks": checks,
        "method_ids": list(LLM_METHOD_IDS),
    }


def _default_client_factory(card: Mapping[str, Any]) -> Any:
    request = card.get("request_configuration")
    if not isinstance(request, Mapping):
        raise FormalLLMContractError("live-LLM request configuration is missing")
    return DeepSeekClient(
        base_url=str(card["base_url"]),
        model=str(card["model_id"]),
        thinking=bool(request["thinking"]),
        reasoning_effort=cast(Any, request.get("reasoning_effort") or "max"),
        timeout_s=float(request["timeout_s"]),
        max_attempts=int(request["max_attempts"]),
        retry_backoff_s=float(request["retry_backoff_s"]),
    )


def _default_run_agent(**kwargs: Any) -> Any:
    from chemworld.eval.runner import run_agent

    return run_agent(**kwargs)


def _bound_formal_risk_limit(spec: FormalCellSpec) -> float:
    protocol = load_formal_protocol()
    if canonical_sha256(protocol) != spec.protocol_sha256:
        raise CellIdentityError("formal protocol does not match the issued live-LLM cell")
    core = protocol.get("task_roles", {}).get("formal_core", {})
    task = core.get(spec.task_id) if isinstance(core, Mapping) else None
    risk_limit = task.get("risk_limit") if isinstance(task, Mapping) else None
    if (
        isinstance(risk_limit, bool)
        or not isinstance(risk_limit, int | float)
        or not 0.0 < float(risk_limit) < 1.0
    ):
        raise CellIdentityError("formal live-LLM task has no valid bound risk limit")
    return float(risk_limit)


@dataclass
class FormalLiveLLMAdapter:
    """Execute one exact live-LLM role with no harness repair or closeout."""

    method_id: str
    binding: FormalMethodBinding
    freeze: Mapping[str, Any]
    client_factory: ClientFactory = _default_client_factory
    run_agent_fn: RunAgent = _default_run_agent
    risk_limit_factory: Callable[[FormalCellSpec], float] = _bound_formal_risk_limit
    kind: MethodKind = field(default="live_llm", init=False)

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        if spec.method != self.binding:
            raise FormalLLMContractError("issued cell does not bind the frozen live-LLM method")
        if spec.spectrum_condition not in {"assigned", "unassigned", "masked"}:
            raise FormalLLMContractError("unsupported live-LLM spectrum condition")
        card = _method_card(self.freeze, self.method_id)
        client = self.client_factory(
            {**card, "base_url": self.freeze.get("base_url")}
        )
        if client.model != card.get("model_id"):
            raise FormalLLMContractError("client model does not match the frozen live-LLM role")
        agent = LiveLLMAgent(
            client,
            role_id=self.method_id,
            spectrum_disclosure=cast(SpectrumDisclosure, spec.spectrum_condition),
        )
        task = get_task(spec.task_id)
        # Formal cells are bound to the prospective limits in the formal protocol,
        # not the older candidate limits loaded by the ``vnext_risk_cost`` runner
        # alias.  Use the same explicit, replay-bound policy path as the classic
        # formal adapters.  Passing both policies is rejected by ``run_agent`` and,
        # more importantly, would leave different method families on different
        # risk thresholds.
        risk_limit = self.risk_limit_factory(spec)
        resource_contract = self.freeze.get("resource_contract")
        if not isinstance(resource_contract, Mapping):
            raise FormalLLMContractError("live-LLM resource contract is missing")
        provider_attempt_limit = int(
            resource_contract["provider_attempt_limit_per_operation"]
        )
        checkpoints = tuple(
            point
            for point in (1, 2, 4, 8, 12, 20, 40)
            if point <= spec.complete_experiments
        )
        execution_error: Exception | None = None
        try:
            self.run_agent_fn(
                env_id=task.env_id,
                agent=agent,
                world_split=task.world_split,
                budget=task.budget,
                objective=task.objective,
                seed=runtime.world_seed,
                agent_seed=runtime.method_seed,
                task_id=task.task_id,
                output_path=trajectory_path,
                budget_override=spec.operation_limit,
                episode_mode_override="campaign",
                evaluation_policy="task_contract",
                step_callback=_formal_progress_callback(
                    spec,
                    checkpoints=checkpoints,
                ),
                method_resource_limits={
                    "operation_limit": spec.operation_limit,
                    "complete_experiment_limit": spec.complete_experiments,
                    "wall_time_limit_s": float(
                        resource_contract["wall_time_limit_s_per_cell"]
                    ),
                    "model_call_limit": spec.operation_limit * provider_attempt_limit,
                    "input_token_limit": int(
                        resource_contract["input_token_limit_per_cell"]
                    ),
                    "output_token_limit": int(
                        resource_contract["output_token_limit_per_cell"]
                    ),
                    "monetary_cost_limit_usd": float(
                        resource_contract["monetary_cost_usd_limit_per_cell"]
                    ),
                    "training_environment_step_limit": int(
                        resource_contract["training_environment_step_limit"]
                    ),
                    "checkpoint_complete_experiments": checkpoints,
                },
                world_interventions=runtime.world_interventions,
                safety_limit_override=risk_limit,
            )
        except Exception as exc:
            # ``run_agent`` flushes its JSONL logger in ``finally``.  Preserve and
            # bind that partial evidence before propagating the original failure,
            # otherwise provider usage incurred before a resource limit or backend
            # exception becomes unauditable.
            execution_error = exc
        records = load_jsonl(trajectory_path) if trajectory_path.is_file() else []
        for record in records:
            record.update(
                {
                    "benchmark_task_id": spec.task_id,
                    "formal_cell_identity_sha256": spec.cell_identity_sha256,
                    "formal_method_id": spec.method.method_id,
                    "formal_pair_id": spec.pair_id,
                    "formal_spectrum_condition": spec.spectrum_condition,
                    "seed": runtime.world_seed,
                }
            )
        pricing_factory = getattr(client, "pricing_snapshot", None)
        receipts_factory = getattr(agent, "provider_receipts", None)
        if records:
            records[-1]["formal_resource_evidence"] = {
                "provider_receipts": (
                    receipts_factory() if callable(receipts_factory) else []
                ),
                "pricing_snapshot": (
                    pricing_factory() if callable(pricing_factory) else None
                ),
                "classic_compute_events": [],
                "private_reasoning_retained": False,
            }
            trajectory_path.write_text(
                "".join(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    + "\n"
                    for record in records
                ),
                encoding="utf-8",
            )
        if execution_error is not None:
            raise execution_error
        if not records:
            raise FormalLLMContractError("live-LLM adapter produced an empty trajectory")


def register_formal_live_llm_adapters(
    registry: FormalAdapterRegistry,
    freeze: Mapping[str, Any] | None = None,
    *,
    freeze_path: str | Path = DEFAULT_LLM_FREEZE_PATH,
    client_factory: ClientFactory = _default_client_factory,
    run_agent_fn: RunAgent = _default_run_agent,
    risk_limit_factory: Callable[[FormalCellSpec], float] = _bound_formal_risk_limit,
) -> None:
    resolved = load_live_llm_method_freeze(freeze_path) if freeze is None else freeze
    bindings = formal_live_llm_method_bindings(resolved, freeze_path=freeze_path)
    for raw_method_id in LLM_METHOD_IDS:
        method_id = cast(LLMMethodId, raw_method_id)
        binding = bindings[method_id]

        def factory(
            _spec: FormalCellSpec,
            *,
            method_id: LLMMethodId = method_id,
            binding: FormalMethodBinding = binding,
        ) -> FormalExecutionAdapter:
            return FormalLiveLLMAdapter(
                method_id=method_id,
                binding=binding,
                freeze=resolved,
                client_factory=client_factory,
                run_agent_fn=run_agent_fn,
                risk_limit_factory=risk_limit_factory,
            )

        registry.register(method_id, "live_llm", factory)


def build_formal_live_llm_registry(
    freeze: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> FormalAdapterRegistry:
    registry = FormalAdapterRegistry()
    register_formal_live_llm_adapters(registry, freeze, **kwargs)
    return registry


def create_formal_live_llm_adapter(spec: FormalCellSpec) -> FormalExecutionAdapter:
    """Default importable factory used by the single-cell subprocess launcher."""

    return build_formal_live_llm_registry().create(spec)


__all__ = [
    "DEFAULT_LLM_FREEZE_PATH",
    "LLM_FREEZE_VERSION",
    "LLM_METHOD_IDS",
    "FormalLLMContractError",
    "FormalLiveLLMAdapter",
    "audit_live_llm_method_freeze",
    "build_formal_live_llm_registry",
    "create_formal_live_llm_adapter",
    "formal_live_llm_method_bindings",
    "live_llm_method_artifact_sha256",
    "load_live_llm_method_freeze",
    "register_formal_live_llm_adapters",
]
