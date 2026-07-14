"""Frozen operation-level baseline identities and formal execution adapters."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from chemworld.agents.operation_baselines import (
    OPERATION_BASELINE_IDS,
    OperationBaselineAgent,
    make_operation_baseline_agent,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.formal_runner import (
    CellIdentityError,
    FormalAdapterRegistry,
    FormalCellSpec,
    FormalExecutionAdapter,
    FormalMethodBinding,
    MethodKind,
    PrivateCellRuntime,
    canonical_sha256,
)
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OPERATION_FREEZE_PATH = ROOT / "configs/methods/operation_v0.4/operation_methods.json"
OPERATION_FREEZE_VERSION = "chemworld-operation-method-freeze-0.4"

_EXPECTED_FAMILIES = {
    "operation_random": "operation_random",
    "observation_blind": "operation_control",
    "rule_based": "operation_control",
}
_EXPECTED_OBSERVATIONS = {
    "operation_random": "operation_affordance_only",
    "observation_blind": "operation_affordance_only",
    "rule_based": "operation_public_state",
}


class FormalOperationContractError(ValueError):
    """Raised when a formal operation baseline is not exactly frozen."""


class RunAgent(Protocol):
    def __call__(self, **kwargs: Any) -> Any: ...


def load_operation_method_freeze(
    path: str | Path = DEFAULT_OPERATION_FREEZE_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormalOperationContractError("operation freeze must be a JSON object")
    if payload.get("schema_version") != OPERATION_FREEZE_VERSION:
        raise FormalOperationContractError("operation freeze schema is unsupported")
    return payload


def operation_method_artifact_sha256(
    method_id: str,
    card: Mapping[str, Any],
) -> str:
    payload = {
        "schema_version": OPERATION_FREEZE_VERSION,
        "method_id": method_id,
        "method_card": {key: value for key, value in card.items() if key != "artifact_sha256"},
    }
    return canonical_sha256(payload)


def audit_operation_method_freeze(
    freeze: Mapping[str, Any] | None = None,
    *,
    root: str | Path = ROOT,
) -> dict[str, Any]:
    """Fail closed on stale source bindings, aliases, or capability drift."""

    resolved = load_operation_method_freeze() if freeze is None else freeze
    repository = Path(root).resolve()
    reasons: list[str] = []
    methods = resolved.get("methods")
    cards = methods if isinstance(methods, Mapping) else {}
    if set(cards) != set(OPERATION_BASELINE_IDS):
        reasons.append("method_set_mismatch")
    artifacts: set[str] = set()
    reports: dict[str, Any] = {}
    for method_id in OPERATION_BASELINE_IDS:
        card = cards.get(method_id)
        method_reasons: list[str] = []
        if not isinstance(card, Mapping):
            method_reasons.append("method_card_missing")
            reports[method_id] = {"ready": False, "reasons": method_reasons}
            reasons.append(f"{method_id}:method_card_missing")
            continue
        if card.get("implementation") != method_id:
            method_reasons.append("implementation_alias_or_mismatch")
        if card.get("family") != _EXPECTED_FAMILIES[method_id]:
            method_reasons.append("family_mismatch")
        if card.get("interaction_track") != "operation_level":
            method_reasons.append("interaction_track_mismatch")
        if card.get("public_observation_set") != _EXPECTED_OBSERVATIONS[method_id]:
            method_reasons.append("public_observation_set_mismatch")
        if card.get("resource_profile") != "operation_baseline":
            method_reasons.append("resource_profile_mismatch")
        if card.get("spectrum_conditions") != ["masked"]:
            method_reasons.append("spectrum_contract_mismatch")
        if card.get("consumes_spectra") is not False:
            method_reasons.append("spectrum_consumption_mismatch")
        if card.get("adapts_within_experiment") is not (method_id == "rule_based"):
            method_reasons.append("within_experiment_adaptation_mismatch")
        if card.get("adapts_across_experiments") is not False:
            method_reasons.append("across_experiment_adaptation_mismatch")
        hyperparameters = card.get("hyperparameters")
        if not isinstance(hyperparameters, Mapping):
            method_reasons.append("hyperparameters_missing")
        else:
            try:
                make_operation_baseline_agent(method_id, hyperparameters=hyperparameters)
            except (TypeError, ValueError):
                method_reasons.append("hyperparameters_invalid")
        source_bindings = card.get("source_bindings")
        if not isinstance(source_bindings, Mapping) or not source_bindings:
            method_reasons.append("source_bindings_missing")
        else:
            for raw_relative, expected in source_bindings.items():
                path = _safe_repo_path(repository, raw_relative)
                if (
                    path is None
                    or path.is_symlink()
                    or not path.is_file()
                    or not _is_sha256(expected)
                    or _file_sha256(path) != expected
                ):
                    method_reasons.append(f"source_binding_mismatch:{raw_relative}")
        supplied_artifact = card.get("artifact_sha256")
        expected_artifact = operation_method_artifact_sha256(method_id, card)
        if supplied_artifact != expected_artifact:
            method_reasons.append("artifact_sha256_mismatch")
        elif supplied_artifact in artifacts:
            method_reasons.append("artifact_sha256_not_unique")
        else:
            artifacts.add(str(supplied_artifact))
        if method_reasons:
            reasons.extend(f"{method_id}:{reason}" for reason in method_reasons)
        reports[method_id] = {
            "ready": not method_reasons,
            "reasons": sorted(set(method_reasons)),
            "artifact_sha256": supplied_artifact,
        }
    if resolved.get("status") != "dev_frozen_bench_unseen":
        reasons.append("freeze_status_invalid")
    if resolved.get("bench_results_used") is not False:
        reasons.append("bench_results_guard_invalid")
    if resolved.get("reference_search_results_used") is not False:
        reasons.append("reference_results_guard_invalid")
    return {
        "schema_version": "chemworld-operation-method-freeze-audit-0.4",
        "status": "ready" if not reasons else "failed",
        "controls_ready": not reasons,
        "method_count": len(reports),
        "unique_artifact_count": len(artifacts),
        "bench_results_used": False,
        "reference_search_results_used": False,
        "methods": reports,
        "reasons": sorted(set(reasons)),
    }


def make_frozen_operation_agent(
    method_id: str,
    freeze: Mapping[str, Any] | None = None,
) -> OperationBaselineAgent:
    resolved = load_operation_method_freeze() if freeze is None else freeze
    audit = audit_operation_method_freeze(resolved)
    if audit["controls_ready"] is not True:
        raise FormalOperationContractError("operation method freeze failed its audit")
    methods = resolved.get("methods")
    card = methods.get(method_id) if isinstance(methods, Mapping) else None
    if not isinstance(card, Mapping):
        raise FormalOperationContractError(f"operation method is not frozen: {method_id}")
    return make_operation_baseline_agent(
        method_id,
        hyperparameters=card.get("hyperparameters")
        if isinstance(card.get("hyperparameters"), Mapping)
        else None,
    )


def formal_operation_method_bindings(
    freeze: Mapping[str, Any] | None = None,
) -> dict[str, FormalMethodBinding]:
    resolved = load_operation_method_freeze() if freeze is None else freeze
    audit = audit_operation_method_freeze(resolved)
    if audit["controls_ready"] is not True:
        raise CellIdentityError("operation method freeze is not ready")
    methods = resolved["methods"]
    assert isinstance(methods, Mapping)
    return {
        method_id: FormalMethodBinding(
            method_id=method_id,
            kind="classic",
            artifact_sha256=str(methods[method_id]["artifact_sha256"]),
            resource_profile="operation_baseline",
        )
        for method_id in OPERATION_BASELINE_IDS
    }


def _default_run_agent(**kwargs: Any) -> Any:
    return run_agent(**kwargs)


@dataclass
class FormalOperationAdapter:
    """Execute one frozen operation control without harness action repair."""

    method_id: str
    artifact_sha256: str
    freeze: Mapping[str, Any] = field(default_factory=load_operation_method_freeze)
    run_agent_fn: RunAgent = _default_run_agent
    kind: MethodKind = field(default="classic", init=False)

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        if spec.spectrum_condition != "masked":
            raise FormalOperationContractError("operation baselines only accept masked spectra")
        bindings = formal_operation_method_bindings(self.freeze)
        expected = bindings.get(self.method_id)
        if expected is None or expected.artifact_sha256 != self.artifact_sha256:
            raise FormalOperationContractError("operation adapter artifact is not frozen")
        if spec.method != expected:
            raise FormalOperationContractError(
                "issued operation method binding does not match the freeze"
            )
        task = get_task(spec.task_id)
        agent = make_frozen_operation_agent(self.method_id, self.freeze)
        checkpoints = tuple(
            point for point in (4, 8, 12, 20, 40) if point <= spec.complete_experiments
        )
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
            method_resource_limits={
                "operation_limit": spec.operation_limit,
                "complete_experiment_limit": spec.complete_experiments,
                "checkpoint_complete_experiments": checkpoints,
            },
            world_interventions=runtime.world_interventions,
            safety_limit_override=_bound_formal_risk_limit(spec),
        )
        records = load_jsonl(trajectory_path)
        if not records:
            raise FormalOperationContractError("operation adapter produced an empty trajectory")
        for record in records:
            record.update(
                {
                    "benchmark_task_id": spec.task_id,
                    "formal_cell_identity_sha256": spec.cell_identity_sha256,
                    "formal_method_id": spec.method.method_id,
                    "formal_pair_id": spec.pair_id,
                    "formal_spectrum_condition": spec.spectrum_condition,
                }
            )
        records[-1]["formal_resource_evidence"] = {
            "provider_receipts": [],
            "classic_compute_events": [],
        }
        trajectory_path.write_text(
            "".join(
                json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )


def register_formal_operation_adapters(
    registry: FormalAdapterRegistry,
    freeze: Mapping[str, Any] | None = None,
) -> None:
    resolved = load_operation_method_freeze() if freeze is None else freeze
    for method_id, binding in formal_operation_method_bindings(resolved).items():
        registry.register(
            method_id,
            "classic",
            _operation_adapter_factory(
                method_id,
                binding.artifact_sha256,
                resolved,
            ),
        )


def build_formal_operation_registry(
    freeze: Mapping[str, Any] | None = None,
) -> FormalAdapterRegistry:
    registry = FormalAdapterRegistry()
    register_formal_operation_adapters(registry, freeze)
    return registry


def create_formal_operation_adapter(spec: FormalCellSpec) -> FormalExecutionAdapter:
    return build_formal_operation_registry().create(spec)


def _operation_adapter_factory(
    method_id: str,
    artifact_sha256: str,
    freeze: Mapping[str, Any],
) -> Callable[[FormalCellSpec], FormalExecutionAdapter]:
    def factory(_spec: FormalCellSpec) -> FormalExecutionAdapter:
        return FormalOperationAdapter(
            method_id=method_id,
            artifact_sha256=artifact_sha256,
            freeze=freeze,
        )

    return factory


def _bound_formal_risk_limit(spec: FormalCellSpec) -> float:
    from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol

    protocol = load_formal_protocol()
    if canonical_sha256(protocol) != spec.protocol_sha256:
        raise FormalOperationContractError("formal protocol digest is not bound")
    tasks = protocol.get("task_roles", {}).get("formal_core", {})
    task = tasks.get(spec.task_id) if isinstance(tasks, Mapping) else None
    if not isinstance(task, Mapping):
        raise FormalOperationContractError("formal task risk contract is missing")
    value = task.get("risk_limit")
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise FormalOperationContractError("formal task risk limit is invalid")
    return float(value)


def _safe_repo_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return None
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_sha256(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


__all__ = [
    "DEFAULT_OPERATION_FREEZE_PATH",
    "OPERATION_FREEZE_VERSION",
    "FormalOperationAdapter",
    "FormalOperationContractError",
    "audit_operation_method_freeze",
    "build_formal_operation_registry",
    "create_formal_operation_adapter",
    "formal_operation_method_bindings",
    "load_operation_method_freeze",
    "make_frozen_operation_agent",
    "operation_method_artifact_sha256",
    "register_formal_operation_adapters",
]
