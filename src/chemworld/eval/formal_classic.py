"""Frozen classic and active-learning adapters for formal benchmark cells."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.agents.base import Agent
from chemworld.agents.bo import (
    StructuredGaussianProcessBOAgent,
    StructuredGaussianProcessPIAgent,
    StructuredGaussianProcessUCBAgent,
    StructuredRandomForestEIAgent,
    StructuredSafetyConstrainedBOAgent,
)
from chemworld.agents.greedy import GreedyLocalAgent
from chemworld.agents.lhs import LatinHypercubeAgent
from chemworld.agents.random import RandomAgent
from chemworld.agents.task_recipes import TASK_RECIPE_SPACE_VERSION
from chemworld.data.logging import load_jsonl
from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
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
from chemworld.eval.resource_accounting_v0_4 import CLASSIC_COMPUTE_EVENT_VERSION
from chemworld.eval.runner import run_agent
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CLASSIC_FREEZE_PATH = (
    configuration_root() / "methods" / "classic_v0.4.1" / "classic_methods.json"
)
CLASSIC_FREEZE_VERSION = "chemworld-classic-method-freeze-0.4.1"

AgentFactory = Callable[..., Agent]

_IMPLEMENTATIONS: dict[str, AgentFactory] = {
    "random": RandomAgent,
    "lhs": LatinHypercubeAgent,
    "greedy_local": GreedyLocalAgent,
    "structured_gp_ei": StructuredGaussianProcessBOAgent,
    "structured_gp_pi": StructuredGaussianProcessPIAgent,
    "structured_gp_ucb": StructuredGaussianProcessUCBAgent,
    "structured_rf_ei": StructuredRandomForestEIAgent,
    "structured_safe_gp_ei": StructuredSafetyConstrainedBOAgent,
}


def _file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _artifact_payload(method_id: str, card: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(card)
    payload.pop("artifact_sha256", None)
    return {
        "schema_version": CLASSIC_FREEZE_VERSION,
        "method_id": method_id,
        "method": payload,
    }


def classic_method_artifact_sha256(method_id: str, card: Mapping[str, Any]) -> str:
    """Hash a method card without creating a circular self-hash."""

    return canonical_sha256(_artifact_payload(method_id, card))


def load_classic_method_freeze(
    path: str | Path = DEFAULT_CLASSIC_FREEZE_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != CLASSIC_FREEZE_VERSION:
        raise CellIdentityError("unsupported classic method freeze schema")
    return payload


def audit_classic_method_freeze(
    freeze: Mapping[str, Any],
    *,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Fail closed on aliases, stale source digests, or incomplete method cards."""

    reasons: list[str] = []
    methods = freeze.get("methods")
    if not isinstance(methods, Mapping) or set(methods) != set(_IMPLEMENTATIONS):
        reasons.append("method_set_mismatch")
        methods = {}
    artifact_hashes: set[str] = set()
    method_reports: dict[str, Any] = {}
    for method_id in sorted(_IMPLEMENTATIONS):
        card = methods.get(method_id)
        method_reasons: list[str] = []
        if not isinstance(card, Mapping):
            method_reasons.append("method_card_missing")
            method_reports[method_id] = {"ready": False, "reasons": method_reasons}
            reasons.append(f"{method_id}:method_card_missing")
            continue
        if card.get("implementation") != method_id:
            method_reasons.append("implementation_alias_or_mismatch")
        if card.get("resource_profile") != "classic_recipe":
            method_reasons.append("resource_profile_mismatch")
        if not isinstance(card.get("hyperparameters"), Mapping):
            method_reasons.append("hyperparameters_missing")
        if not isinstance(card.get("failure_domains"), list) or not card["failure_domains"]:
            method_reasons.append("failure_domains_missing")
        source_bindings = card.get("source_bindings")
        if not isinstance(source_bindings, Mapping) or not source_bindings:
            method_reasons.append("source_bindings_missing")
        else:
            for relative, expected in source_bindings.items():
                source = (root / str(relative)).resolve()
                try:
                    source.relative_to(root.resolve())
                except ValueError:
                    method_reasons.append("source_binding_outside_repository")
                    continue
                if (
                    not isinstance(expected, str)
                    or len(expected) != 64
                    or not source.is_file()
                    or _file_sha256(source) != expected
                ):
                    method_reasons.append(f"source_binding_mismatch:{relative}")
        expected_artifact = classic_method_artifact_sha256(method_id, card)
        supplied_artifact = card.get("artifact_sha256")
        if supplied_artifact != expected_artifact:
            method_reasons.append("artifact_sha256_mismatch")
        elif supplied_artifact in artifact_hashes:
            method_reasons.append("artifact_sha256_not_unique")
        else:
            artifact_hashes.add(supplied_artifact)
        recipe_encoding = card.get("recipe_encoding")
        if method_id.startswith("structured_") and recipe_encoding != (
            "continuous_plus_material_one_hot"
        ):
            method_reasons.append("typed_material_encoding_missing")
        if method_id == "structured_safe_gp_ei" and card.get("constraint") != (
            "upper_confidence_risk_mask_with_minimum_risk_fallback"
        ):
            method_reasons.append("safe_constraint_missing")
        if method_reasons:
            reasons.extend(f"{method_id}:{reason}" for reason in method_reasons)
        method_reports[method_id] = {
            "ready": not method_reasons,
            "reasons": sorted(set(method_reasons)),
            "artifact_sha256": supplied_artifact,
        }
    status_ready = freeze.get("status") == "dev_frozen_bench_unseen"
    if not status_ready:
        reasons.append("freeze_status_invalid")
    if freeze.get("search_space_version") != TASK_RECIPE_SPACE_VERSION:
        reasons.append("search_space_version_mismatch")
    return {
        "schema_version": CLASSIC_FREEZE_VERSION,
        "status": "ready" if not reasons else "failed",
        "controls_ready": not reasons,
        "bench_results_used": False,
        "method_count": len(method_reports),
        "unique_artifact_count": len(artifact_hashes),
        "methods": method_reports,
        "reasons": sorted(set(reasons)),
    }


def _method_card(freeze: Mapping[str, Any], method_id: str) -> Mapping[str, Any]:
    audit = audit_classic_method_freeze(freeze)
    if audit["controls_ready"] is not True:
        raise CellIdentityError("classic method freeze failed its source/artifact audit")
    methods = freeze["methods"]
    if not isinstance(methods, Mapping) or not isinstance(methods.get(method_id), Mapping):
        raise CellIdentityError(f"classic method is not frozen: {method_id}")
    return methods[method_id]


def make_frozen_classic_agent(
    method_id: str,
    *,
    freeze: Mapping[str, Any] | None = None,
) -> Agent:
    resolved = load_classic_method_freeze() if freeze is None else freeze
    card = _method_card(resolved, method_id)
    factory = _IMPLEMENTATIONS[method_id]
    hyperparameters = dict(card["hyperparameters"])
    return factory(**hyperparameters)


def formal_classic_method_bindings(
    freeze: Mapping[str, Any] | None = None,
) -> dict[str, FormalMethodBinding]:
    resolved = load_classic_method_freeze() if freeze is None else freeze
    audit = audit_classic_method_freeze(resolved)
    if audit["controls_ready"] is not True:
        raise CellIdentityError("classic method freeze is not ready")
    methods = resolved["methods"]
    return {
        method_id: FormalMethodBinding(
            method_id=method_id,
            kind="classic",
            artifact_sha256=str(methods[method_id]["artifact_sha256"]),
            resource_profile="classic_recipe",
        )
        for method_id in sorted(_IMPLEMENTATIONS)
    }


def _bound_formal_risk_limit(spec: FormalCellSpec) -> float:
    protocol = load_formal_protocol()
    if canonical_sha256(protocol) != spec.protocol_sha256:
        raise CellIdentityError("formal protocol does not match the issued classic cell")
    core = protocol.get("task_roles", {}).get("formal_core", {})
    task = core.get(spec.task_id) if isinstance(core, Mapping) else None
    risk_limit = task.get("risk_limit") if isinstance(task, Mapping) else None
    if (
        isinstance(risk_limit, bool)
        or not isinstance(risk_limit, int | float)
        or not 0.0 < float(risk_limit) < 1.0
    ):
        raise CellIdentityError("formal classic task has no valid bound risk limit")
    return float(risk_limit)


@dataclass
class FormalClassicAdapter:
    """Execute exactly one frozen recipe-level method without harness repairs."""

    method_id: str
    artifact_sha256: str
    kind: MethodKind = "classic"

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        if spec.spectrum_condition != "masked":
            raise CellIdentityError("recipe-level classic methods require masked spectra")
        bindings = formal_classic_method_bindings()
        expected = bindings.get(self.method_id)
        if expected is None or expected.artifact_sha256 != self.artifact_sha256:
            raise CellIdentityError("classic adapter artifact is not the frozen method")
        if spec.method != expected:
            raise CellIdentityError("issued classic method binding does not match the freeze")
        task = get_task(spec.task_id)
        agent = make_frozen_classic_agent(self.method_id)
        run_agent(
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
                "checkpoint_complete_experiments": tuple(
                    point
                    for point in (4, 8, 12, 20, 40)
                    if point <= spec.complete_experiments
                ),
            },
            world_interventions=runtime.world_interventions,
            safety_limit_override=_bound_formal_risk_limit(spec),
        )
        records = load_jsonl(trajectory_path)
        if not records:
            raise RuntimeError("classic adapter produced an empty trajectory")
        raw_event_factory = getattr(agent, "formal_compute_events", None)
        raw_events = raw_event_factory() if callable(raw_event_factory) else []
        classic_events = [
            {
                "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
                "event_id": f"{self.method_id}-{int(event['event_index']):04d}",
                "cell_identity_sha256": spec.cell_identity_sha256,
                "event_kind": event["event_kind"],
                "cpu_time_s": float(event["cpu_time_s"]),
                "wall_time_s": float(event["wall_time_s"]),
            }
            for event in raw_events
        ]
        for record in records:
            record.update(
                {
                    "formal_cell_identity_sha256": spec.cell_identity_sha256,
                    "formal_method_id": spec.method.method_id,
                    "formal_pair_id": spec.pair_id,
                    "formal_spectrum_condition": spec.spectrum_condition,
                }
            )
        records[-1]["formal_resource_evidence"] = {
            "provider_receipts": [],
            "classic_compute_events": classic_events,
        }
        trajectory_path.write_text(
            "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
            encoding="utf-8",
        )


def register_formal_classic_adapters(
    registry: FormalAdapterRegistry,
    freeze: Mapping[str, Any] | None = None,
) -> None:
    bindings = formal_classic_method_bindings(freeze)
    for method_id, binding in bindings.items():
        registry.register(
            method_id,
            "classic",
            _classic_adapter_factory(method_id, binding.artifact_sha256),
        )


def _classic_adapter_factory(
    method_id: str,
    artifact_sha256: str,
) -> Callable[[FormalCellSpec], FormalExecutionAdapter]:
    def factory(_spec: FormalCellSpec) -> FormalExecutionAdapter:
        return FormalClassicAdapter(
            method_id=method_id,
            artifact_sha256=artifact_sha256,
        )

    return factory


def build_formal_classic_registry(
    freeze: Mapping[str, Any] | None = None,
) -> FormalAdapterRegistry:
    registry = FormalAdapterRegistry()
    register_formal_classic_adapters(registry, freeze)
    return registry


__all__ = [
    "CLASSIC_FREEZE_VERSION",
    "DEFAULT_CLASSIC_FREEZE_PATH",
    "FormalClassicAdapter",
    "audit_classic_method_freeze",
    "build_formal_classic_registry",
    "classic_method_artifact_sha256",
    "formal_classic_method_bindings",
    "load_classic_method_freeze",
    "make_frozen_classic_agent",
    "register_formal_classic_adapters",
]
