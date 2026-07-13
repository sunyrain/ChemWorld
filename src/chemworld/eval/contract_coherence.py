"""Build the v0.5 task-to-runtime-to-evaluator contract graph."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.evidence_quarantine import load_evidence_quarantine_policy
from chemworld.eval.method_protocol import METHOD_RESOURCE_LEDGER_VERSION
from chemworld.eval.runner import AGENT_REGISTRY
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import SERIOUS_TASK_IDS, list_tasks

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "foundation" / "contract_coherence_v0.5.json"
PROTOCOL_VERSION = "chemworld-contract-coherence-protocol-0.1"


class ContractCoherenceError(RuntimeError):
    """Raised when a formal artifact or contract graph is incoherent."""


def load_contract_coherence_protocol(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != PROTOCOL_VERSION:
        raise ContractCoherenceError("unsupported contract coherence protocol")
    return payload


def assert_artifact_compatible(
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    *,
    strict_fields: Sequence[str],
) -> None:
    """Reject a same-schema artifact whenever any semantic identity differs."""

    for field in strict_fields:
        if field not in expected or field not in observed:
            raise ContractCoherenceError(f"artifact identity field missing: {field}")
        if expected[field] != observed[field]:
            raise ContractCoherenceError(f"artifact semantic identity mismatch: {field}")
    for field in ("backend_semantic_hash", "task_contract_hash", "method_config_hash"):
        value = observed.get(field)
        if not isinstance(value, str) or not _is_sha256(value):
            raise ContractCoherenceError(f"artifact identity must be sha256: {field}")


def audit_contract_coherence(
    protocol: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    sources = {
        name: _read_object(_resolve_path(workspace, raw_path))
        for name, raw_path in protocol["sources"].items()
    }
    tasks = {task.task_id: task.to_dict() for task in list_tasks()}
    serious = tuple(SERIOUS_TASK_IDS)
    formal_core = tuple(protocol["task_roles"]["formal_core"])
    exploratory = tuple(protocol["task_roles"]["exploratory"])
    expected_serious = formal_core + exploratory

    runtime = sources["runtime_reachability"]
    evaluation = sources["evaluation"]
    replay = sources["score_replay"]
    risk = sources["risk_cost"]
    mechanism = sources["mechanism_families"]
    method = sources["method_protocol"]
    confirmatory = sources["confirmatory_freeze"]
    reference = sources["reference_regret"]
    backend = sources["backend"]
    state = sources["state_invariants"]
    quarantine = load_evidence_quarantine_policy(
        _resolve_path(workspace, protocol["sources"]["evidence_quarantine"])
    )

    graph: dict[str, dict[str, Any]] = {}
    for task_id in serious:
        task = tasks[task_id]
        runtime_task = runtime["task_paths"][task_id]
        primary = evaluation["tasks"][task_id]
        replay_task = replay["tasks"][task_id]
        risk_task = risk["tasks"][task_id]
        providers = {
            model_id: runtime["provider_catalog"][model_id]
            for model_id in runtime_task["reachable_model_ids"]
        }
        graph[task_id] = {
            "role": "formal_core" if task_id in formal_core else "exploratory",
            "task_contract_hash": task["contract_hash"],
            "budget": task["budget"],
            "termination_policy": task["termination_policy"],
            "observation_policy": task["observation_policy"],
            "allowed_instruments": task["allowed_instruments"],
            "operations": runtime_task["operation_paths"],
            "providers": providers,
            "primary_metric": primary,
            "primary_direction": replay_task["direction"],
            "risk_limit": risk_task["risk_limit"],
            "process_cost_limit": risk_task["process_cost_limit"],
            "mechanism_modes": mechanism["task_modes"][task_id],
            "world_axes": list(protocol["world_axes"]),
            "evaluation_contract_version": evaluation["evaluation_contract_version"],
            "result_schema_version": replay["result_schema_version"],
            "score_replay_binding_version": replay["binding_schema_version"],
        }

    method_mapping = {
        method_id: spec.get("implementation")
        for method_id, spec in method["methods"].items()
        if spec.get("formal_role") == "required"
    }
    expected_method_mapping = dict(protocol["method_contract"]["formal_to_implementation"])
    implementation_ready = all(
        implementation is None or implementation in AGENT_REGISTRY
        for implementation in expected_method_mapping.values()
    )
    aliases = dict(protocol["method_contract"]["legacy_alias_to_formal"])
    aliases_resolve = all(
        alias in AGENT_REGISTRY and formal_id in expected_method_mapping
        for alias, formal_id in aliases.items()
    )

    semantic = protocol["semantic_contract"]
    evaluation_policy = evaluation["policies"]
    replay_policy = replay["policies"]
    identity = protocol["contract_identity"]
    quarantine_ids = set(quarantine["quarantined_protocol_ids"])
    current_task_hashes = {task_id: tasks[task_id]["contract_hash"] for task_id in tasks}

    controls = {
        "protocol_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False
        and protocol.get("formal_results_present") is False,
        "serious_task_roles_are_exact": serious == expected_serious,
        "task_scopes_are_coherent": all(
            set(source) == set(serious)
            for source in (
                evaluation["tasks"],
                replay["tasks"],
                risk["tasks"],
                mechanism["reachable_tasks"],
            )
        ),
        "historical_confirmatory_roles_match": tuple(
            confirmatory["task_roles"]["core"]
        )
        == formal_core
        and tuple(confirmatory["task_roles"]["exploratory"]) == exploratory,
        "primary_metrics_are_single_source": all(
            evaluation["tasks"][task_id] == replay["tasks"][task_id]["primary_metric"]
            and evaluation["tasks"][task_id] in tasks[task_id]["success_metrics"]
            for task_id in serious
        ),
        "runtime_task_operations_are_exact": all(
            set(tasks[task_id]["allowed_operations"])
            == set(runtime["task_paths"][task_id]["runtime_profile"]["allowed_operations"])
            and not runtime["task_paths"][task_id]["declared_but_unreachable"]
            and not runtime["task_paths"][task_id]["reachable_but_undeclared"]
            for task_id in serious
        ),
        "runtime_instruments_are_exact": all(
            set(tasks[task_id]["allowed_instruments"])
            == set(runtime["task_paths"][task_id]["runtime_profile"]["allowed_instruments"])
            for task_id in serious
        ),
        "runtime_providers_are_exact": all(
            set(runtime["task_paths"][task_id]["declared_model_ids"])
            == set(runtime["task_paths"][task_id]["reachable_model_ids"])
            and all(
                runtime["provider_catalog"][model_id]["runtime_reachable"] is True
                for model_id in runtime["task_paths"][task_id]["reachable_model_ids"]
            )
            for task_id in serious
        ),
        "runtime_maturity_is_reference_or_better": all(
            _maturity_rank(tasks[task_id]["physics_maturity"])
            >= _maturity_rank("reference_validated")
            and tasks[task_id]["proxy_allowed"] is False
            for task_id in serious
        ),
        "risk_cost_limits_are_finite_positive": all(
            _finite_positive(risk["tasks"][task_id]["risk_limit"])
            and _finite_positive(risk["tasks"][task_id]["process_cost_limit"])
            for task_id in serious
        ),
        "terminal_primary_semantics_are_exact": evaluation_policy[
            "primary_and_objective_source"
        ]
        == semantic["primary_source"]
        == replay_policy["terminal_selector"]
        and evaluation_policy["missing_primary"]
        == semantic["missing_primary"]
        == replay_policy["missing_primary"]
        and evaluation_policy["online_reward_is_primary"]
        is semantic["online_reward_is_primary"]
        is replay_policy["online_reward_is_primary"],
        "risk_cost_semantics_are_exact": evaluation_policy["risk_aggregation"]
        == semantic["risk_aggregation"]
        == risk["risk_aggregation"]
        and evaluation_policy["campaign_total_cost"] == semantic["campaign_total_cost"]
        and risk["process_cost_aggregation"] == semantic["process_cost_aggregation"]
        and risk["measurement_cost_aggregation"]
        == semantic["measurement_cost_aggregation"],
        "automatic_repair_is_forbidden": evaluation_policy[
            "automatic_action_repair_or_closeout"
        ]
        == semantic["automatic_action_repair_or_closeout"],
        "resource_failure_semantics_are_exact": method["resource_policy"]["overrun_policy"]
        == semantic["resource_overrun"]
        and method["resource_policy"]["incomplete_accounting_policy"]
        == semantic["incomplete_resource_accounting"],
        "method_ids_and_implementations_are_coherent": method_mapping
        == expected_method_mapping
        and implementation_ready
        and aliases_resolve,
        "excluded_methods_are_exact": {
            method_id
            for method_id, spec in method["methods"].items()
            if spec.get("formal_role") == "excluded"
        }
        == set(protocol["method_contract"]["excluded_method_ids"]),
        "versions_are_coherent": all(
            task["task_contract_version"] == identity["task_contract_version"]
            and task["world_law_id"] == identity["world_law_id"]
            for task in tasks.values()
        )
        and backend["backend_id"] == identity["backend_id"]
        and backend["world_law_id"] == identity["world_law_id"]
        and backend["task_contract_hashes"] == current_task_hashes
        and evaluation["evaluation_contract_version"]
        == identity["evaluation_contract_version"]
        and replay["result_schema_version"] == identity["result_schema_version"]
        and replay["binding_schema_version"] == identity["score_replay_binding_version"]
        and reference["result_schema_version"] == identity["result_schema_version"]
        and reference["score_replay_binding_version"]
        == identity["score_replay_binding_version"]
        and identity["method_resource_ledger_version"] == METHOD_RESOURCE_LEDGER_VERSION,
        "state_and_runtime_controls_are_complete": state["controls_complete"] is True
        and runtime["controls_ready"] is True
        and not runtime["forbidden_runtime_models"]
        and not runtime["orphan_runtime_providers"]
        and not runtime["incomplete_provider_contracts"],
        "legacy_seed_protocols_are_quarantined": {
            confirmatory["protocol_id"],
            method["protocol_id"],
            reference["protocol_id"],
        }.issubset(quarantine_ids),
    }
    controls_ready = all(controls.values())
    source_commit, dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-contract-coherence-report-0.1",
        "protocol_id": protocol["protocol_id"],
        "status": "contract_graph_coherent_formal_protocol_pending"
        if controls_ready
        else "contract_graph_incoherent",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": source_commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "contract_graph_sha256": _canonical_sha256(graph),
        "controls": controls,
        "contract_identity": identity,
        "task_roles": protocol["task_roles"],
        "task_graph": graph,
        "method_contract": {
            "formal_to_implementation": expected_method_mapping,
            "legacy_alias_to_formal": aliases,
            "excluded_method_ids": protocol["method_contract"]["excluded_method_ids"],
        },
        "artifact_compatibility": protocol["artifact_compatibility"],
        "limitations": [
            "The backend semantic hash is introduced by the later portable-release gate.",
            "The coherent 0.4 protocol and private Bench commitment do not exist yet.",
            "PPO, SAC, and live LLM formal implementations remain intentionally unregistered.",
        ],
        "remaining_release_gates": [
            "freeze the portable backend semantic identity",
            "freeze formal protocol 0.4 from this graph",
            "register and freeze all evaluated method adapters",
        ],
    }


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ContractCoherenceError(f"JSON object required: {path}")
    return payload


def _resolve_path(workspace: Path, raw_path: Any) -> Path:
    path = (workspace / str(raw_path)).resolve()
    try:
        path.relative_to(workspace.resolve())
    except ValueError as exc:
        raise ContractCoherenceError("source path escapes workspace") from exc
    return path


def _maturity_rank(value: Any) -> int:
    return {"lite": 0, "reference_validated": 1, "professional_candidate": 2}.get(
        str(value), -1
    )


def _finite_positive(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(
        float(value)
    ) and float(value) > 0.0


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


__all__ = [
    "ContractCoherenceError",
    "assert_artifact_compatible",
    "audit_contract_coherence",
    "load_contract_coherence_protocol",
]
