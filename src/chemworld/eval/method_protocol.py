"""Fail-closed method fairness and resource-accounting controls."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import to_builtin
from chemworld.physchem.mechanism_library import configuration_root

METHOD_PROTOCOL_VERSION = "chemworld-method-protocol-0.2"
METHOD_RESOURCE_USAGE_VERSION = "chemworld-method-resource-usage-0.1"
METHOD_RESOURCE_LEDGER_VERSION = "chemworld-method-resource-ledger-0.1"
DEFAULT_METHOD_PROTOCOL_PATH = configuration_root() / "benchmark" / "method_protocol_vnext.json"
ROOT = Path(__file__).resolve().parents[3]

_AGENT_COUNTER_FIELDS = (
    "model_call_count",
    "input_token_count",
    "output_token_count",
    "training_environment_step_count",
)
_AGENT_FLOAT_FIELDS = ("monetary_cost_usd", "cpu_time_s", "gpu_time_s")


class MethodResourceLimitError(RuntimeError):
    """Raised before a resource-over-budget run can be treated as valid."""


@dataclass(frozen=True)
class MethodResourceLimits:
    """Hard per-run limits; ``None`` means report-only for that resource."""

    operation_limit: int
    complete_experiment_limit: int | None = None
    wall_time_limit_s: float | None = None
    model_call_limit: int | None = None
    input_token_limit: int | None = None
    output_token_limit: int | None = None
    monetary_cost_limit_usd: float | None = None
    training_environment_step_limit: int | None = None
    cpu_time_limit_s: float | None = None
    gpu_time_limit_s: float | None = None
    checkpoint_complete_experiments: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.operation_limit <= 0:
            raise ValueError("operation_limit must be positive")
        for name in (
            "complete_experiment_limit",
            "model_call_limit",
            "input_token_limit",
            "output_token_limit",
            "training_environment_step_limit",
        ):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative")
        for name in (
            "wall_time_limit_s",
            "monetary_cost_limit_usd",
            "cpu_time_limit_s",
            "gpu_time_limit_s",
        ):
            value = getattr(self, name)
            if value is not None and (not math.isfinite(value) or value < 0.0):
                raise ValueError(f"{name} must be finite and non-negative")
        if tuple(sorted(set(self.checkpoint_complete_experiments))) != (
            self.checkpoint_complete_experiments
        ):
            raise ValueError("checkpoint_complete_experiments must be sorted and unique")
        if any(item <= 0 for item in self.checkpoint_complete_experiments):
            raise ValueError("checkpoint_complete_experiments must be positive")
        if (
            self.complete_experiment_limit is not None
            and self.checkpoint_complete_experiments
            and self.checkpoint_complete_experiments[-1] > self.complete_experiment_limit
        ):
            raise ValueError("checkpoints cannot exceed complete_experiment_limit")

    @classmethod
    def from_payload(
        cls,
        payload: Mapping[str, Any] | None,
        *,
        operation_limit: int,
    ) -> MethodResourceLimits:
        values = dict(payload or {})
        values.setdefault("operation_limit", operation_limit)
        checkpoints = values.get("checkpoint_complete_experiments", ())
        values["checkpoint_complete_experiments"] = tuple(int(item) for item in checkpoints)
        return cls(**values)


@dataclass
class MethodResourceLedger:
    """Cumulative resource ledger shared by every official runner adapter."""

    limits: MethodResourceLimits
    requires_online_model: bool = False
    started_at: float = field(default_factory=perf_counter)
    operation_count: int = 0
    complete_experiment_count: int = 0
    decision_wall_time_s: float = 0.0
    update_wall_time_s: float = 0.0
    agent_usage: dict[str, Any] = field(default_factory=dict)
    reached_checkpoints: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.requires_online_model and self.limits.model_call_limit is None:
            raise ValueError("online model ledgers require an explicit provider request limit")

    def record_decision(
        self,
        *,
        elapsed_s: float,
        agent_usage: Mapping[str, Any],
    ) -> None:
        if not math.isfinite(elapsed_s) or elapsed_s < 0.0:
            raise ValueError("decision elapsed time must be finite and non-negative")
        self.operation_count += 1
        self.decision_wall_time_s += elapsed_s
        self._accept_agent_usage(agent_usage)
        self._enforce()

    def record_outcome(self, *, experiment_ended: bool, update_elapsed_s: float) -> None:
        if not math.isfinite(update_elapsed_s) or update_elapsed_s < 0.0:
            raise ValueError("update elapsed time must be finite and non-negative")
        self.update_wall_time_s += update_elapsed_s
        if experiment_ended:
            self.complete_experiment_count += 1
            if self.complete_experiment_count in self.limits.checkpoint_complete_experiments:
                self.reached_checkpoints.append(self.complete_experiment_count)
        self._enforce()

    def snapshot(self) -> dict[str, Any]:
        usage = self._normalized_usage(self.agent_usage)
        return {
            "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
            "operation_count": self.operation_count,
            "complete_experiment_count": self.complete_experiment_count,
            "decision_wall_time_s": self.decision_wall_time_s,
            "update_wall_time_s": self.update_wall_time_s,
            "run_wall_time_s": perf_counter() - self.started_at,
            "reached_checkpoints": list(self.reached_checkpoints),
            "limits": to_builtin(asdict(self.limits)),
            "agent_usage": to_builtin(usage),
            "accounting_complete": bool(usage["accounting_complete"]),
        }

    def _accept_agent_usage(self, payload: Mapping[str, Any]) -> None:
        usage = self._normalized_usage(payload)
        previous = self._normalized_usage(self.agent_usage)
        for name in (*_AGENT_COUNTER_FIELDS, *_AGENT_FLOAT_FIELDS):
            if usage[name] < previous[name]:
                raise ValueError(f"cumulative resource field decreased: {name}")
        if self.requires_online_model:
            if not usage["accounting_complete"]:
                raise ValueError("online model resource accounting must be complete")
            provenance = usage["model_provenance"]
            required = {
                "provider",
                "model_id",
                "model_snapshot_or_access_date",
                "prompt_hash",
                "request_parameters",
                "tokenizer_or_provider_usage_source",
            }
            if not isinstance(provenance, dict) or not required.issubset(provenance):
                raise ValueError("online model usage requires provider/model/prompt provenance")
        self.agent_usage = usage

    def _normalized_usage(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if not payload:
            payload = {
                "schema_version": METHOD_RESOURCE_USAGE_VERSION,
                "accounting_complete": not self.requires_online_model,
            }
        if payload.get("schema_version") != METHOD_RESOURCE_USAGE_VERSION:
            raise ValueError("unsupported method resource usage schema")
        normalized: dict[str, Any] = {
            "schema_version": METHOD_RESOURCE_USAGE_VERSION,
            "accounting_complete": bool(payload.get("accounting_complete", False)),
            "usage_source": str(payload.get("usage_source", "unspecified")),
            "model_provenance": to_builtin(payload.get("model_provenance", {})),
        }
        for name in _AGENT_COUNTER_FIELDS:
            counter_value = int(payload.get(name, 0))
            if counter_value < 0:
                raise ValueError(f"resource field must be non-negative: {name}")
            normalized[name] = counter_value
        for name in _AGENT_FLOAT_FIELDS:
            float_value = float(payload.get(name, 0.0))
            if not math.isfinite(float_value) or float_value < 0.0:
                raise ValueError(f"resource field must be finite and non-negative: {name}")
            normalized[name] = float_value
        return normalized

    def _enforce(self) -> None:
        snapshot = self.snapshot()
        usage = snapshot["agent_usage"]
        checks = (
            ("operation_count", self.operation_count, self.limits.operation_limit),
            (
                "complete_experiment_count",
                self.complete_experiment_count,
                self.limits.complete_experiment_limit,
            ),
            ("run_wall_time_s", snapshot["run_wall_time_s"], self.limits.wall_time_limit_s),
            ("model_call_count", usage["model_call_count"], self.limits.model_call_limit),
            ("input_token_count", usage["input_token_count"], self.limits.input_token_limit),
            ("output_token_count", usage["output_token_count"], self.limits.output_token_limit),
            (
                "monetary_cost_usd",
                usage["monetary_cost_usd"],
                self.limits.monetary_cost_limit_usd,
            ),
            (
                "training_environment_step_count",
                usage["training_environment_step_count"],
                self.limits.training_environment_step_limit,
            ),
            ("cpu_time_s", usage["cpu_time_s"], self.limits.cpu_time_limit_s),
            ("gpu_time_s", usage["gpu_time_s"], self.limits.gpu_time_limit_s),
        )
        exceeded = [
            name for name, observed, limit in checks if limit is not None and observed > limit
        ]
        if exceeded:
            raise MethodResourceLimitError("method resource limit exceeded: " + ", ".join(exceeded))


def audit_method_protocol(
    protocol: Mapping[str, Any],
    *,
    agent_registry: Mapping[str, Callable[[], Any]],
) -> dict[str, Any]:
    """Audit protocol structure and current implementation eligibility."""

    checkpoints = tuple(int(item) for item in protocol.get("checkpoints", ()))
    evaluation = protocol.get("evaluation_budget", {})
    method_specs = protocol.get("methods", {})
    registry_names = set(agent_registry)
    methods: dict[str, Any] = {}
    for method_id, spec in method_specs.items():
        implementation = spec.get("implementation")
        implemented = isinstance(implementation, str) and implementation in registry_names
        manifest: dict[str, Any] = {}
        if implemented:
            manifest = agent_registry[implementation]().manifest()
        required_encoding = spec.get("required_recipe_encoding")
        encoding_ready = required_encoding is None or manifest.get("recipe_encoding") == (
            required_encoding
        )
        capabilities = manifest.get("interaction_capabilities", {})
        required_capabilities = spec.get("required_capabilities", {})
        capabilities_ready = all(
            capabilities.get(name) == expected for name, expected in required_capabilities.items()
        )
        implementation_contract_ready = implemented and encoding_ready and capabilities_ready
        methods[str(method_id)] = {
            "family": spec.get("family"),
            "implementation": implementation,
            "implemented": implemented,
            "formal_role": spec.get("formal_role"),
            "current_eligibility": spec.get("current_eligibility"),
            "interaction_capabilities": capabilities or None,
            "required_recipe_encoding": required_encoding,
            "observed_recipe_encoding": manifest.get("recipe_encoding"),
            "required_capabilities": required_capabilities,
            "implementation_contract_ready": implementation_contract_ready,
            "requires_online_model": manifest.get("requires_online_model", False),
            "blockers": list(spec.get("blockers", ())),
        }

    required_families = set(protocol.get("required_method_families", ()))
    represented_families = {str(spec.get("family")) for spec in method_specs.values()}
    formal_candidates = [
        method_id
        for method_id, card in methods.items()
        if card["formal_role"] == "required" and card["current_eligibility"] == "candidate"
    ]
    missing_required = [
        method_id
        for method_id, card in methods.items()
        if card["formal_role"] == "required" and not card["implemented"]
    ]
    diagnostic_only = [
        method_id
        for method_id, card in methods.items()
        if card["current_eligibility"] != "candidate"
    ]
    required_ineligible = [
        method_id
        for method_id, card in methods.items()
        if card["formal_role"] == "required" and card["current_eligibility"] != "candidate"
    ]
    checks = {
        "schema": protocol.get("schema_version") == METHOD_PROTOCOL_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "complete_experiment_budget_positive": int(evaluation.get("complete_experiments", 0)) > 0,
        "checkpoint_schedule_sorted_unique": checkpoints == tuple(sorted(set(checkpoints))),
        "checkpoint_schedule_within_budget": bool(checkpoints)
        and checkpoints[-1] == int(evaluation.get("complete_experiments", 0)),
        "paired_seed_count_positive": int(protocol.get("paired_seed_count", 0)) > 0,
        "paired_seed_count_matches_ids": int(protocol.get("paired_seed_count", 0))
        == len(protocol.get("confirmatory_seed_ids", ())),
        "confirmatory_seed_ids_unique": len(set(protocol.get("confirmatory_seed_ids", ())))
        == len(protocol.get("confirmatory_seed_ids", ())),
        "confirmatory_seed_ids_are_fresh": not (
            set(protocol.get("confirmatory_seed_ids", ())) & set(range(20, 40))
        ),
        "superseded_seed_policy_is_fail_closed": protocol.get("superseded_seed_policy")
        == "seeds_20_39_are_diagnostic_only_and_must_not_be_reused",
        "joint_constraint_decision_required": protocol.get(
            "confirmatory_decision_contract", {}
        ).get("objective_safety_and_cost_joint_rule_required")
        is True,
        "all_required_families_represented": required_families <= represented_families,
        "stub_methods_excluded": all(
            spec.get("formal_role") == "excluded"
            for spec in method_specs.values()
            if spec.get("family") == "stub"
        ),
        "private_chain_of_thought_not_required": (
            protocol.get("llm_evidence_policy", {}).get("private_chain_of_thought_required")
            is False
        ),
        "resource_overrun_fails_closed": (
            protocol.get("resource_policy", {}).get("overrun_policy") == "fail_closed"
        ),
        "provider_retries_are_bounded_and_counted": (
            int(
                protocol.get("resource_policy", {})
                .get("llm_hard_limits_per_evaluation_run", {})
                .get("provider_request_limit_per_operation", 0)
            )
            >= 1
            and protocol.get("resource_policy", {})
            .get("llm_hard_limits_per_evaluation_run", {})
            .get("failed_requests_count_toward_limit")
            is True
        ),
        "pre_freeze_runs_are_diagnostic": (
            protocol.get("pre_freeze_result_policy") == "diagnostic_only"
        ),
        "declared_eligibility_matches_manifests": all(
            (card["current_eligibility"] == "candidate" and card["implementation_contract_ready"])
            or (
                card["current_eligibility"] != "candidate"
                and not card["implementation_contract_ready"]
            )
            or card["formal_role"] == "excluded"
            for card in methods.values()
        ),
    }
    evidence: dict[str, Any] = {}
    for evidence_id, relative_path in protocol.get("evidence_sources", {}).items():
        path = ROOT / str(relative_path)
        evidence[str(evidence_id)] = {
            "path": str(relative_path),
            "exists": path.is_file(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        }
    checks["evidence_sources_exist"] = bool(evidence) and all(
        item["exists"] for item in evidence.values()
    )
    controls_ready = all(checks.values())
    formal_matrix_ready = controls_ready and not missing_required and not required_ineligible
    return {
        "schema_version": "chemworld-method-protocol-audit-0.2",
        "protocol_id": protocol.get("protocol_id"),
        "status": "controls_ready_methods_pending" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "formal_method_matrix_ready": formal_matrix_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "methods": methods,
        "formal_candidate_methods": formal_candidates,
        "missing_required_methods": missing_required,
        "required_but_ineligible_methods": required_ineligible,
        "diagnostic_or_excluded_methods": diagnostic_only,
        "interaction_failures": list(protocol.get("observed_interaction_failures", ())),
        "confirmatory_seed_ids": list(protocol.get("confirmatory_seed_ids", ())),
        "confirmatory_decision_contract": dict(
            protocol.get("confirmatory_decision_contract", {})
        ),
        "evidence": evidence,
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def evaluation_resource_limits(
    protocol: Mapping[str, Any],
    *,
    operation_limit: int,
    requires_online_model: bool,
) -> MethodResourceLimits:
    """Translate the frozen candidate protocol into enforceable run limits."""

    evaluation = protocol["evaluation_budget"]
    resource_policy = protocol["resource_policy"]
    rl_limits = resource_policy["rl_hard_limits_per_task_training"]
    payload: dict[str, Any] = {
        "operation_limit": operation_limit,
        "complete_experiment_limit": int(evaluation["complete_experiments"]),
        "wall_time_limit_s": float(evaluation["wall_time_limit_s_per_run"]),
        "training_environment_step_limit": int(rl_limits["training_environment_steps"]),
        "gpu_time_limit_s": float(rl_limits["gpu_time_s"]),
        "checkpoint_complete_experiments": list(protocol["checkpoints"]),
    }
    if requires_online_model:
        llm_limits = resource_policy["llm_hard_limits_per_evaluation_run"]
        request_multiplier = int(llm_limits["provider_request_limit_per_operation"])
        if request_multiplier < 1:
            raise ValueError("provider_request_limit_per_operation must be positive")
        payload.update(
            {
                "model_call_limit": operation_limit * request_multiplier,
                "input_token_limit": int(llm_limits["input_tokens"]),
                "output_token_limit": int(llm_limits["output_tokens"]),
                "monetary_cost_limit_usd": float(llm_limits["monetary_cost_usd"]),
            }
        )
    return MethodResourceLimits.from_payload(payload, operation_limit=operation_limit)


def load_method_protocol(path: str | Path = DEFAULT_METHOD_PROTOCOL_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("method protocol must be a JSON object")
    return payload


__all__ = [
    "DEFAULT_METHOD_PROTOCOL_PATH",
    "METHOD_PROTOCOL_VERSION",
    "METHOD_RESOURCE_LEDGER_VERSION",
    "METHOD_RESOURCE_USAGE_VERSION",
    "MethodResourceLedger",
    "MethodResourceLimitError",
    "MethodResourceLimits",
    "audit_method_protocol",
    "evaluation_resource_limits",
    "load_method_protocol",
]
