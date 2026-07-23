"""Refresh and verify ChemWorld's current evidence dependency graph.

This is the only supported entry point for regenerating current evidence. Git
history, rather than duplicate files in the working tree, retains superseded
protocols and reports.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.data.schema import (  # noqa: E402
    TRAJECTORY_ALIAS_WRITE_REMOVAL_VERSION,
    TRAJECTORY_COMPATIBILITY_ALIASES,
)
from chemworld.eval.mechanism_adaptation_execution import (  # noqa: E402
    gate_a_execution_contract_binding,
)
from chemworld.eval.provenance import (  # noqa: E402
    canonical_json_sha256 as _canonical_sha256,
)
from chemworld.eval.provenance import (  # noqa: E402
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    repository_tree_sha256,
    write_json_atomic,
)

CURRENT_REGISTRY = ROOT / "configs/current.json"


@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    path: str
    role: str
    dependencies: tuple[str, ...] = ()
    command: tuple[str, ...] | None = None


@dataclass(frozen=True)
class CurrentPathRule:
    """Schema rule for a path exposed through the current registry."""

    json_path: tuple[str, ...]
    artifact_role: str
    must_exist: bool = True
    metadata_path: tuple[str, ...] | None = None
    expected_state: str | None = None


NODES = (
    EvidenceNode(
        "runtime_reachability_protocol",
        "configs/foundation/runtime_reachability_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "state_transition_protocol",
        "configs/foundation/state_transition_invariants_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "public_boundary_protocol",
        "configs/foundation/public_boundary_security_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "maturity_protocol",
        "configs/foundation/maturity_truth_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "backend_protocol",
        "configs/foundation/backend_v0.5.json",
        "protocol_input",
    ),
    EvidenceNode(
        "evaluation_contract",
        "configs/benchmark/evaluation_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "score_replay_contract",
        "configs/benchmark/score_replay_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "public_harness_contract",
        "configs/benchmark/public_harness_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "exploit_matrix_contract",
        "configs/benchmark/exploit_matrix_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "semantic_invariance_contract",
        "configs/benchmark/semantic_invariance_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "live_llm_methods",
        "configs/methods/llm_v0.4/llm_methods.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_protocol",
        "configs/benchmark/mechanism_adaptation_v0.2.1.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_gate_a_plan",
        "configs/benchmark/mechanism_adaptation_gate_a_v0.2.4.json",
        "protocol_input",
        ("mechanism_protocol",),
    ),
    EvidenceNode(
        "mechanism_design_audit",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc15.json",
        "formal_result",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_public_matrix",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-public-matrix.json",
        "generated_current",
        ("mechanism_protocol",),
        ("scripts/plan_mechanism_adaptation_matrix.py",),
    ),
    EvidenceNode(
        "mechanism_preflight",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-preflight.json",
        "generated_current",
        (
            "mechanism_gate_a_plan",
            "mechanism_design_audit",
            "mechanism_protocol",
            "mechanism_public_matrix",
        ),
        ("scripts/check_mechanism_adaptation_protocol.py",),
    ),
    EvidenceNode(
        "mechanism_online_policy_certificate",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-online-policy-certificate-v0.3-rc15.json",
        "formal_result",
        (
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
            "mechanism_protocol",
        ),
    ),
    EvidenceNode(
        "mechanism_gate_a",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.2.4-rc15.json",
        "formal_result",
        (
            "backend_candidate",
            "backend_protocol",
            "evaluation_contract",
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
            "mechanism_online_policy_certificate",
            "mechanism_preflight",
            "mechanism_protocol",
            "public_boundary",
            "score_replay_contract",
        ),
    ),
    EvidenceNode(
        "mechanism_agent_pilot",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-agent-pilot-v0.2.1.json",
        "development_diagnostic",
        ("live_llm_methods", "mechanism_gate_a", "mechanism_protocol"),
    ),
    EvidenceNode(
        "backend_golden_fixture",
        "tests/fixtures/golden/core_scripted_trajectories.json",
        "fixture",
    ),
    EvidenceNode(
        "runtime_integration",
        "workstreams/world_foundation/reports/wf-110-runtime-integration.json",
        "generated_current",
        command=("scripts/audit_vnext_runtime_integration.py",),
    ),
    EvidenceNode(
        "runtime_reachability",
        "workstreams/world_foundation/reports/runtime-reachability-vnext.json",
        "generated_current",
        ("runtime_integration", "runtime_reachability_protocol"),
        ("scripts/audit_runtime_reachability_vnext.py",),
    ),
    EvidenceNode(
        "state_transition_invariants",
        "workstreams/world_foundation/reports/state-transition-invariants.json",
        "generated_current",
        ("runtime_integration", "state_transition_protocol"),
        ("scripts/audit_state_transition_invariants.py",),
    ),
    EvidenceNode(
        "public_boundary",
        "workstreams/world_foundation/reports/public-boundary-security-vnext.json",
        "generated_current",
        (
            "exploit_matrix_contract",
            "public_boundary_protocol",
            "public_harness_contract",
            "runtime_integration",
            "score_replay_contract",
            "semantic_invariance_contract",
        ),
        ("scripts/audit_public_boundary_security_vnext.py",),
    ),
    EvidenceNode(
        "maturity_truth",
        "workstreams/world_foundation/reports/maturity-truth-vnext.json",
        "generated_current",
        ("maturity_protocol", "runtime_integration", "runtime_reachability"),
        ("scripts/audit_maturity_truth_vnext.py",),
    ),
    EvidenceNode(
        "runtime_affordance",
        "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json",
        "generated_current",
        command=("scripts/audit_runtime_domain_affordances.py",),
    ),
    EvidenceNode(
        "backend_candidate",
        "workstreams/world_foundation/reports/backend-v0.5.json",
        "generated_current",
        (
            "runtime_integration",
            "runtime_reachability",
            "state_transition_invariants",
            "public_boundary",
            "maturity_truth",
            "backend_protocol",
        ),
        ("scripts/audit_backend_v05.py", "--allow-dirty"),
    ),
)


ARTIFACT_ROLES = frozenset(
    {
        "protocol_input",
        "generated_current",
        "formal_result",
        "development_diagnostic",
        "fixture",
        "superseded",
        "archive",
    }
)
CURRENT_ARTIFACT_ROLES = ARTIFACT_ROLES - {"superseded", "archive"}


def _node_lifecycle(node: EvidenceNode) -> str:
    return "generated" if node.command is not None else "immutable"


def _node_producer(node: EvidenceNode) -> str:
    if node.command is not None:
        return "python " + " ".join(node.command)
    return {
        "protocol_input": "maintainer_versioned_input",
        "formal_result": "frozen_formal_execution",
        "development_diagnostic": "versioned_development_execution",
        "fixture": "maintainer_versioned_fixture",
    }[node.role]


def _node_source_binding(node: EvidenceNode) -> str:
    return {
        "protocol_input": "content_sha256",
        "generated_current": "dependencies_and_source_commit",
        "formal_result": "protocol_plan_and_result_sha256",
        "development_diagnostic": "content_and_versioned_source_sha256",
        "fixture": "content_sha256",
    }[node.role]


def _node_contract_errors(node: EvidenceNode) -> list[str]:
    errors: list[str] = []
    if node.role not in ARTIFACT_ROLES:
        errors.append(f"undeclared artifact role: {node.node_id} -> {node.role}")
    elif node.role not in CURRENT_ARTIFACT_ROLES:
        errors.append(f"non-current artifact appears in current DAG: {node.node_id}")
    if node.role == "generated_current" and node.command is None:
        errors.append(f"generated current artifact has no producer: {node.node_id}")
    if node.role != "generated_current" and node.command is not None:
        errors.append(f"immutable artifact declares a generator: {node.node_id}")
    return errors


CURRENT_PATH_RULES = (
    CurrentPathRule(("runtime", "backend"), "protocol_input"),
    CurrentPathRule(("runtime", "backend_report"), "generated_current"),
    CurrentPathRule(("mechanism_adaptation", "protocol"), "protocol_input"),
    CurrentPathRule(("mechanism_adaptation", "preflight_report"), "generated_current"),
    CurrentPathRule(("mechanism_adaptation", "gate_a_plan"), "protocol_input"),
    CurrentPathRule(
        ("mechanism_adaptation", "online_policy_certificate_report"),
        "formal_result",
    ),
    CurrentPathRule(("mechanism_adaptation", "gate_a_report"), "formal_result"),
    CurrentPathRule(
        ("mechanism_adaptation", "agent_pilot_report"),
        "development_diagnostic",
    ),
    CurrentPathRule(("mechanism_adaptation", "design_audit_report"), "formal_result"),
)


def node_map() -> dict[str, EvidenceNode]:
    nodes = {node.node_id: node for node in NODES}
    if len(nodes) != len(NODES):
        raise ValueError("evidence DAG contains duplicate node ids")
    paths = [node.path for node in NODES]
    if len(set(paths)) != len(paths):
        raise ValueError("evidence DAG contains duplicate materialized paths")
    contract_errors = [error for node in NODES for error in _node_contract_errors(node)]
    if contract_errors:
        raise ValueError("; ".join(contract_errors))
    return nodes


def generation_order() -> list[EvidenceNode]:
    nodes = node_map()
    ordered: list[EvidenceNode] = []
    remaining = dict(nodes)
    while remaining:
        ready = [
            node
            for node in remaining.values()
            if all(dependency not in remaining for dependency in node.dependencies)
        ]
        if not ready:
            raise ValueError("evidence DAG is cyclic or names an unknown dependency")
        for node in sorted(ready, key=lambda item: item.node_id):
            unknown = set(node.dependencies) - nodes.keys()
            if unknown:
                raise ValueError(f"{node.node_id} has unknown dependencies: {sorted(unknown)}")
            ordered.append(node)
            remaining.pop(node.node_id)
    return ordered


def graph_sha256() -> str:
    return _canonical_sha256(
        [
            {
                "id": node.node_id,
                "path": node.path,
                "role": node.role,
                "lifecycle": _node_lifecycle(node),
                "producer": _node_producer(node),
                "source_binding": _node_source_binding(node),
                "dependencies": list(node.dependencies),
                "command": list(node.command) if node.command else None,
            }
            for node in NODES
        ]
    )


def _registry_value(registry: dict[str, Any], json_path: tuple[str, ...]) -> Any:
    value: Any = registry
    for key in json_path:
        if not isinstance(value, dict) or key not in value:
            raise KeyError(".".join(json_path))
        value = value[key]
    return value


def validate_current_registry_paths(registry: dict[str, Any], *, root: Path = ROOT) -> list[str]:
    """Validate explicitly classified current, planned, and historical paths."""

    errors: list[str] = []
    resolved_root = root.resolve()
    checked_metadata: set[tuple[str, ...]] = set()
    for rule in CURRENT_PATH_RULES:
        label = ".".join(rule.json_path)
        try:
            value = _registry_value(registry, rule.json_path)
        except KeyError:
            errors.append(f"current registry path field is missing: {label}")
            continue
        if not isinstance(value, str) or not value.strip():
            errors.append(f"current registry path is not a non-empty string: {label}")
            continue

        relative_path = Path(value)
        if relative_path.is_absolute():
            errors.append(f"current registry path must be repository-relative: {label}")
            continue
        resolved_path = (resolved_root / relative_path).resolve()
        if not resolved_path.is_relative_to(resolved_root):
            errors.append(f"current registry path escapes repository root: {label}")
            continue
        if rule.must_exist and not resolved_path.is_file():
            errors.append(f"missing required current artifact: {label} -> {value}")
        if not rule.must_exist and resolved_path.exists():
            errors.append(
                f"planned current artifact exists but remains pending: {label} -> {value}"
            )

        if rule.metadata_path is None or rule.metadata_path in checked_metadata:
            continue
        checked_metadata.add(rule.metadata_path)
        metadata_label = ".".join(rule.metadata_path)
        try:
            metadata = _registry_value(registry, rule.metadata_path)
        except KeyError:
            errors.append(f"current registry artifact metadata is missing: {metadata_label}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"current registry artifact metadata is invalid: {metadata_label}")
            continue
        if (
            rule.expected_state is not None
            and metadata.get("artifact_state") != rule.expected_state
        ):
            errors.append(f"current registry artifact state mismatch: {metadata_label}")
        declared_roles = metadata.get("artifact_roles")
        if not isinstance(declared_roles, list) or rule.artifact_role not in declared_roles:
            errors.append(
                f"current registry artifact role mismatch: {metadata_label} "
                f"requires {rule.artifact_role}"
            )
    return errors


def _run(
    node: EvidenceNode,
    *,
    source_commit: str | None = None,
    source_tree_dirty: bool | None = None,
) -> None:
    if _node_lifecycle(node) == "immutable":
        return
    if node.command is None:  # pragma: no cover - node_map rejects this contract
        raise RuntimeError(f"generated node has no producer: {node.node_id}")
    command = [sys.executable, *node.command]
    started = time.perf_counter()
    print(
        json.dumps({"event": "evidence_node_started", "node_id": node.node_id}),
        flush=True,
    )
    environment = os.environ.copy()
    if source_commit is not None and source_tree_dirty is not None:
        environment["CHEMWORLD_EVIDENCE_SOURCE_COMMIT"] = source_commit
        environment["CHEMWORLD_EVIDENCE_SOURCE_TREE_DIRTY"] = (
            "true" if source_tree_dirty else "false"
        )
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    print(
        json.dumps(
            {
                "event": "evidence_node_completed",
                "node_id": node.node_id,
                "returncode": completed.returncode,
                "elapsed_s": round(time.perf_counter() - started, 3),
            }
        ),
        flush=True,
    )
    # Negative gates are valid generated states, not generator crashes.  The
    # backend candidate is expected to remain blocked while a freeze-candidate
    # patch is still uncommitted; method freeze is likewise a truthful negative
    # gate until all methods are ready.
    allowed_codes = {0, 1} if node.node_id == "backend_candidate" else {0}
    if completed.returncode not in allowed_codes:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"generator failed for {node.node_id}: {detail}")
    if completed.returncode and completed.stderr.strip():
        raise RuntimeError(f"generator failed for {node.node_id}: {completed.stderr.strip()}")
    if not (ROOT / node.path).is_file():
        raise RuntimeError(f"generator did not create {node.path}")


def _is_materialized_output_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    materialized_paths = {
        node.path.replace("\\", "/") for node in NODES if node.command is not None
    }
    materialized_paths.add("configs/current.json")
    return normalized in materialized_paths


def _git_tree_dirty() -> bool:
    """Return whether tracked source/protocol inputs differ from HEAD.

    Current evidence reports are generated outputs. They may change during a DAG
    refresh without making the source tree itself dirty.
    """

    return git_worktree_dirty(
        ROOT,
        excluded_paths={
            "configs/current.json",
            *(node.path for node in NODES if node.command is not None),
        },
    )


def _repository_source_sha256() -> str:
    """Fingerprint executable source independently from generated artifacts."""

    return repository_tree_sha256(
        ROOT,
        relative_roots=("scripts", "src/chemworld"),
    )


def _git_head() -> str:
    return git_source_commit(ROOT)


def _gate_a_binding_current(
    report: Mapping[str, Any],
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> bool:
    expected_execution = gate_a_execution_contract_binding(protocol, plan)
    return bool(
        report.get("protocol_sha256") == _canonical_sha256(protocol)
        and report.get("gate_a_plan_sha256") == _canonical_sha256(plan)
        and report.get("protocol_id") == protocol.get("protocol_id")
        and report.get("gate_a_plan_id") == plan.get("plan_id")
        and report.get("execution_contract_binding") == expected_execution
    )


def _online_policy_certificate_binding_current(
    certificate: Mapping[str, Any],
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> bool:
    expected_execution = gate_a_execution_contract_binding(protocol, plan)
    return bool(
        certificate.get("protocol_sha256") == _canonical_sha256(protocol)
        and certificate.get("gate_a_plan_sha256") == _canonical_sha256(plan)
        and certificate.get("protocol_id") == protocol.get("protocol_id")
        and certificate.get("gate_a_plan_id") == plan.get("plan_id")
        and certificate.get("execution_contract_binding") == expected_execution
        and certificate.get("certificate_scope")
        == "online_policy_feasible_diagnosis"
    )


def _composed_gate_a_binding_current(
    report: Mapping[str, Any],
    online_certificate: Mapping[str, Any],
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> bool:
    decision = report.get("certificate_decision", {})
    online_reference = (
        decision.get("online_policy_feasible_certificate", {})
        if isinstance(decision, Mapping)
        else {}
    )
    return bool(
        _gate_a_binding_current(report, protocol, plan)
        and _online_policy_certificate_binding_current(
            online_certificate,
            protocol,
            plan,
        )
        and isinstance(online_reference, Mapping)
        and online_reference.get("report")
        == node_map()["mechanism_online_policy_certificate"].path
        and online_reference.get("certificate_sha256")
        == _canonical_sha256(online_certificate)
        and "task_reports" not in online_reference
        and "identifiability_by_post_change_budget" not in online_reference
    )


def _artifact_source_binding_current(
    node: EvidenceNode,
    payload: Mapping[str, Any],
) -> bool:
    """Verify declared report provenance against current executable source."""

    if node.role in {"protocol_input", "fixture"}:
        return True
    if node.node_id == "runtime_affordance":
        from chemworld.eval.runtime_domain_affordance_audit import (
            guarded_source_sha256,
        )

        if payload.get("guarded_source_sha256") != guarded_source_sha256(ROOT):
            return False
    if node.node_id == "mechanism_online_policy_certificate":
        protocol = json.loads(
            (ROOT / node_map()["mechanism_protocol"].path).read_text(
                encoding="utf-8"
            )
        )
        plan = json.loads(
            (ROOT / node_map()["mechanism_gate_a_plan"].path).read_text(
                encoding="utf-8"
            )
        )
        if not _online_policy_certificate_binding_current(
            payload,
            protocol,
            plan,
        ):
            return False
    source_commit = payload.get("source_commit")
    if (
        node.role != "generated_current"
        and isinstance(source_commit, str)
        and source_commit != _git_head()
    ):
        return False
    if payload.get("source_commit_stable") is False:
        return False
    recorded_dirty = payload.get("source_tree_dirty")
    return not (isinstance(recorded_dirty, bool) and recorded_dirty != _git_tree_dirty())


def _node_gate_state(node: EvidenceNode, payload: dict[str, Any]) -> str:
    if node.role in {"protocol_input", "development_diagnostic", "fixture"}:
        return "not_applicable"
    if node.node_id == "backend_candidate":
        return "passed" if payload.get("backend_contract_validated") else "blocked"
    if node.node_id == "mechanism_gate_a":
        return "passed" if payload.get("gate_a_pass") else "blocked"
    if node.node_id == "mechanism_design_audit":
        return "passed" if payload.get("pass") else "blocked"
    if payload.get("passed") is False or payload.get("controls_ready") is False:
        return "blocked"
    return "passed"


def current_status_summary(
    registry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the canonical independent readiness dimensions for maintainers."""

    current = (
        dict(registry)
        if registry is not None
        else json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    )
    runtime = current["runtime"]
    formal = current["formal_evaluation"]
    mechanism = current["mechanism_adaptation"]
    publication = current["publication"]
    return {
        "schema_version": "chemworld-current-status-summary-0.1",
        "backend_candidate": {
            "status": runtime["status"],
            "contract_validation": runtime["contract_validation"],
        },
        "release_attestation": {"status": runtime["clean_release_attestation"]},
        "mechanism_gate_a": {
            "status": mechanism["status"],
            "evidence_current": bool(mechanism.get("gate_a_evidence_current", False)),
            "passed": bool(mechanism["gate_a_pass"]),
        },
        "formal_benchmark": {
            "status": formal["status"],
            "benchmark_claim_allowed": formal["benchmark_claim_allowed"],
        },
        "publication": {
            "status": publication["status"],
            "publication_ready": publication["publication_ready"],
        },
        "interpretation": (
            "Backend validation, release attestation, mechanism identifiability, "
            "formal benchmark readiness, and publication readiness are independent."
        ),
    }


def _write_current_registry() -> None:
    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    backend = json.loads(
        (ROOT / node_map()["backend_candidate"].path).read_text(
            encoding="utf-8"
        )
    )
    backend_protocol = json.loads(
        (ROOT / node_map()["backend_protocol"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism = json.loads(
        (ROOT / node_map()["mechanism_gate_a"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_online = json.loads(
        (
            ROOT / node_map()["mechanism_online_policy_certificate"].path
        ).read_text(encoding="utf-8")
    )
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_pilot = json.loads(
        (ROOT / node_map()["mechanism_agent_pilot"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_protocol = json.loads(
        (ROOT / node_map()["mechanism_protocol"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_plan = json.loads(
        (ROOT / node_map()["mechanism_gate_a_plan"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_evidence_current = _composed_gate_a_binding_current(
        mechanism,
        mechanism_online,
        mechanism_protocol,
        mechanism_plan,
    )
    mechanism_gate_a_pass = bool(
        mechanism_evidence_current and mechanism.get("gate_a_pass")
    )
    mechanism_decision = mechanism.get("certificate_decision", {})
    controlled_gate_a_pass = bool(
        mechanism_evidence_current
        and isinstance(mechanism_decision, Mapping)
        and mechanism_decision.get("controlled_matched_gate_pass") is True
    )
    online_certificate = (
        mechanism_decision.get("online_policy_feasible_certificate", {})
        if isinstance(mechanism_decision, Mapping)
        else {}
    )
    online_gate_a_pass = bool(
        mechanism_evidence_current
        and isinstance(online_certificate, Mapping)
        and online_certificate.get("gate_pass") is True
    )
    mechanism_gate_a_status = (
        "gate_a_passed_remaining_gates_pending"
        if mechanism_gate_a_pass
        else "gate_a_invalidated_recertification_required"
        if not mechanism_evidence_current
        else "gate_a_online_policy_certificate_pending"
        if controlled_gate_a_pass and not online_gate_a_pass
        else "gate_a_controlled_certificate_failed"
    )
    from chemworld.data.schema import OUTCOME_LAYER_FIELDS, TRAJECTORY_SCHEMA_VERSION

    dirty = _git_tree_dirty()
    nodes: dict[str, Any] = {}
    for node in generation_order():
        path = ROOT / node.path
        payload = json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else {}
        dependency_fresh = all(
            nodes[dependency]["freshness"] == "fresh" for dependency in node.dependencies
        )
        source_fresh = _artifact_source_binding_current(node, payload)
        binding_fresh = source_fresh and not (
            node.node_id == "mechanism_gate_a" and not mechanism_evidence_current
        )
        fresh = dependency_fresh and binding_fresh
        gate_state = _node_gate_state(node, payload) if fresh else "invalidated"
        nodes[node.node_id] = {
            "path": node.path,
            "role": node.role,
            "lifecycle": _node_lifecycle(node),
            "producer": _node_producer(node),
            "source_binding": _node_source_binding(node),
            "dependencies": list(node.dependencies),
            "sha256": file_sha256(path),
            "artifact_state": "current" if fresh else "stale",
            "freshness": "fresh" if fresh else "stale_dependency_binding",
            "gate_state": gate_state,
        }

    current["schema_version"] = "chemworld-current-surface-registry-0.4"
    current["updated_at"] = date.today().isoformat()
    current["project"].update(
        {
            "role": "agent_capability_evaluation_and_training_environment",
            "scientific_scope": "selected_physical_chemistry_causal_worlds",
            "environment_updates_agent_weights": False,
        }
    )
    current["system_model"] = {
        "schema_version": "chemworld-system-model-0.1",
        "layers": [
            "physical_causal_world_substrate",
            "experimental_interaction_runtime",
            "task_and_evaluation_contract",
        ],
        "agent_and_training_outside_environment": True,
        "canonical_entities": [
            "task",
            "world",
            "scenario",
            "campaign",
            "experiment",
            "operation",
        ],
        "benchmark_cell": ["task", "scenario", "agent", "seed"],
        "trajectory_schema_version": TRAJECTORY_SCHEMA_VERSION,
        "outcome_layers": list(OUTCOME_LAYER_FIELDS),
        "trajectory_compatibility_aliases": list(TRAJECTORY_COMPATIBILITY_ALIASES),
        "trajectory_alias_write_removal_version": (
            TRAJECTORY_ALIAS_WRITE_REMOVAL_VERSION
        ),
    }
    current["completeness_model"] = {
        "structural": "implemented_by_design_and_subject_to_runtime_controls",
        "evaluation": "contracts_defined_empirical_closure_pending",
        "attribution": (
            "gate_a_identifiability_passed_remaining_agent_attribution_gates_pending"
            if mechanism_gate_a_pass
            else "controlled_identifiability_passed_online_policy_certificate_pending"
            if controlled_gate_a_pass and mechanism_evidence_current
            else "gate_a_recertification_required_after_public_contract_change"
        ),
        "chemical_coverage": "selected_bounded_archetypes_not_exhaustive",
        "physical_fidelity": "model_card_bounded_not_universal_digital_twin",
    }
    current["benchmark_suites"] = {
        "core": {
            "role": "agent_comparison_environment",
            "protocol": "configs/benchmark/evaluation_vnext.json",
            "status": "environment_ready_methods_unfrozen",
        },
        "diagnostic": {
            "role": "identifiability_feedback_adaptation_and_autonomy_attribution",
            "protocol": "configs/benchmark/mechanism_adaptation_v0.2.1.json",
            "task_ids": list(mechanism_protocol["design"]["tasks"]),
            "status": (
                "gate_a_passed"
                if mechanism_gate_a_pass
                else "online_policy_certificate_pending"
                if controlled_gate_a_pass and mechanism_evidence_current
                else "gate_a_recertification_required"
            ),
        },
        "extended": {
            "role": "environment_coverage_training_and_demonstration",
            "registered_task_count": len(backend.get("task_contract_hashes", {})),
            "formal_ranking_claim": False,
        },
    }
    current["state_model"] = {
        "schema_version": "chemworld-evidence-state-model-0.3",
        "dimensions": {
            "artifact_state": ["current", "stale", "historical", "pending"],
            "artifact_role": sorted(ARTIFACT_ROLES),
            "artifact_lifecycle": ["generated", "immutable"],
            "gate_state": [
                "passed",
                "blocked",
                "invalidated",
                "pending",
                "not_applicable",
            ],
            "claim_scope": [
                "backend_control",
                "development",
                "formal_benchmark",
                "mechanism_benchmark",
                "publication",
            ],
        },
        "rules": [
            "status is the canonical lifecycle enum and booleans are derived claims",
            "current means regenerated from the declared DAG, not scientifically ready",
            (
                "generated artifacts have declared commands; protocol inputs, formal results, "
                "development diagnostics, and fixtures are immutable to DAG refresh"
            ),
            (
                "frozen requires a clean source-attested candidate and is never "
                "inferred from validation alone"
            ),
            (
                "backend validation does not imply method freeze, formal results, "
                "or publication readiness"
            ),
            "development evidence is never promoted to formal benchmark evidence by aggregation",
        ],
    }
    current["evidence_dag"] = {
        "schema_version": "chemworld-current-evidence-dag-0.3",
        "generator": "python scripts/evidence_pipeline.py --refresh",
        "checker": "python scripts/evidence_pipeline.py --check",
        "graph_sha256": graph_sha256(),
        "repository_source_sha256": _repository_source_sha256(),
        "generation_order": [node.node_id for node in generation_order()],
        "nodes": nodes,
    }
    current["runtime"] = {
        "backend": node_map()["backend_protocol"].path,
        "backend_report": node_map()["backend_candidate"].path,
        "backend_id": backend_protocol["backend_id"],
        "status": backend["status"],
        "contract_validation": ("passed" if backend["backend_contract_validated"] else "blocked"),
        "clean_release_attestation": backend["clean_release_attestation"],
        "source_tree_dirty": backend["source_tree_dirty"],
        "world_law_id": backend_protocol["world_law_id"],
        "task_contract_version": backend_protocol["task_contract_version"],
    }
    current["formal_evaluation"] = {
        "status": "environment_ready_methods_unfrozen",
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "interpretation": (
            "ChemWorld supplies the evaluation runtime; method selection, training, "
            "and result freezes belong to each evaluation campaign."
        ),
    }
    current["mechanism_adaptation"] = {
        "protocol": node_map()["mechanism_protocol"].path,
        "preflight_report": node_map()["mechanism_preflight"].path,
        "design_audit_report": node_map()["mechanism_design_audit"].path,
        "design_audit_pass": bool(
            mechanism_design.get("pass")
            and nodes["mechanism_design_audit"]["artifact_state"] == "current"
        ),
        "gate_a_plan": node_map()["mechanism_gate_a_plan"].path,
        "online_policy_certificate_report": node_map()[
            "mechanism_online_policy_certificate"
        ].path,
        "gate_a_report": node_map()["mechanism_gate_a"].path,
        "agent_pilot_report": node_map()["mechanism_agent_pilot"].path,
        "status": mechanism_gate_a_status,
        "gate_a_pass": mechanism_gate_a_pass,
        "gate_a_evidence_current": mechanism_evidence_current,
        "gate_a_certificate_status": {
            "controlled_matched_identifiability": (
                "passed"
                if controlled_gate_a_pass
                else "invalidated"
                if not mechanism_evidence_current
                else "failed"
            ),
            "online_policy_feasible_diagnosis": (
                "passed"
                if online_gate_a_pass
                else str(online_certificate.get("status", "pending_execution"))
                if mechanism_evidence_current and isinstance(online_certificate, Mapping)
                else "invalidated"
            ),
        },
        "new_external_provider_runs_completed": bool(
            mechanism_gate_a_pass
            and mechanism_protocol.get("data_contract", {}).get(
                "new_external_provider_runs_completed", False
            )
        ),
        "agent_pilot_gate_status": {
            gate: mechanism_pilot[gate]["status"]
            for gate in ("gate_0", "gate_b", "gate_c", "gate_d", "gate_e")
        },
        "agent_pilot_evidence_current": bool(
            nodes["mechanism_agent_pilot"]["artifact_state"] == "current"
        ),
        "agent_weight_updates_performed": False,
        "publication_ready": False,
    }
    current.pop("development_evidence", None)
    current.pop("history_policy", None)
    current["publication"] = {
        "status": "no_active_manuscript",
        "publication_ready": False,
    }
    blockers: list[dict[str, Any]] = []
    if backend["clean_release_attestation"] != "passed":
        blockers.append({"id": "clean_release_attestation_pending", "scope": "backend_release"})
    remaining_mechanism_gates = ["gate_b", "gate_c", "gate_d", "gate_e"]
    if not mechanism_gate_a_pass:
        remaining_mechanism_gates.insert(0, "gate_a")
    blockers.append(
        {
            "id": "mechanism_gates_remaining",
            "scope": "mechanism_benchmark",
            "gates": remaining_mechanism_gates,
        }
    )
    current["repository_integrity"] = {
        "status": (
            "current_evidence_coherent_worktree_dirty"
            if dirty
            else "current_evidence_coherent_worktree_clean"
        ),
        "current_evidence_coherent": True,
        "tracked_source_tree_dirty": dirty,
        "stale_binding_count": sum(node["artifact_state"] == "stale" for node in nodes.values()),
        "stale_binding_ids": sorted(
            node_id for node_id, node in nodes.items() if node["artifact_state"] == "stale"
        ),
        "blockers": blockers,
    }
    write_json_atomic(CURRENT_REGISTRY, current, sort_keys=False)


def refresh() -> None:
    source_commit = _git_head()
    source_tree_dirty = _git_tree_dirty()
    for node in generation_order():
        _run(
            node,
            source_commit=source_commit,
            source_tree_dirty=source_tree_dirty,
        )
    if _git_head() != source_commit or _git_tree_dirty() != source_tree_dirty:
        raise RuntimeError("source inputs changed during evidence refresh")
    _write_current_registry()


def _recorded_node_contract_errors(node: EvidenceNode, recorded: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if recorded.get("role") != node.role:
        errors.append(f"registry artifact role mismatch: {node.node_id}")
    if recorded.get("lifecycle") != _node_lifecycle(node):
        errors.append(f"registry lifecycle mismatch: {node.node_id}")
    if recorded.get("producer") != _node_producer(node):
        errors.append(f"registry producer mismatch: {node.node_id}")
    if recorded.get("source_binding") != _node_source_binding(node):
        errors.append(f"registry source binding mismatch: {node.node_id}")
    return errors


def current_evidence_manifest() -> dict[str, Any]:
    """Explain role, producer, dependencies, binding, and freshness for every node."""

    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    recorded_nodes = current.get("evidence_dag", {}).get("nodes", {})
    rows: list[dict[str, Any]] = []
    for node in generation_order():
        path = ROOT / node.path
        recorded = recorded_nodes.get(node.node_id, {})
        exists = path.is_file()
        digest_matches = bool(exists and recorded.get("sha256") == file_sha256(path))
        contract_matches = bool(
            recorded.get("path") == node.path
            and recorded.get("dependencies") == list(node.dependencies)
            and not _recorded_node_contract_errors(node, recorded)
        )
        rows.append(
            {
                "node_id": node.node_id,
                "path": node.path,
                "role": node.role,
                "lifecycle": _node_lifecycle(node),
                "producer": _node_producer(node),
                "dependencies": list(node.dependencies),
                "source_binding": _node_source_binding(node),
                "freshness": (
                    "fresh" if digest_matches and contract_matches else "stale_or_missing"
                ),
            }
        )
    return {
        "schema_version": "chemworld-current-evidence-manifest-0.1",
        "graph_sha256": graph_sha256(),
        "generation_order": [node.node_id for node in generation_order()],
        "nodes": rows,
    }


def check_current_evidence() -> list[str]:
    errors: list[str] = []
    try:
        ordered = generation_order()
    except ValueError as error:
        return [str(error)]
    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    if current.get("schema_version") != "chemworld-current-surface-registry-0.4":
        errors.append("current registry schema version is stale")
    errors.extend(validate_current_registry_paths(current))
    dag = current.get("evidence_dag", {})
    if dag.get("schema_version") != "chemworld-current-evidence-dag-0.3":
        errors.append("current registry evidence DAG schema version is stale")
    if dag.get("graph_sha256") != graph_sha256():
        errors.append("current registry evidence graph hash is stale")
    if dag.get("repository_source_sha256") != _repository_source_sha256():
        errors.append("current registry executable source fingerprint is stale")
    expected_order = [node.node_id for node in ordered]
    if dag.get("generation_order") != expected_order:
        errors.append("current registry generation order is stale")
    recorded_nodes_value = dag.get("nodes", {})
    if not isinstance(recorded_nodes_value, Mapping):
        errors.append("current registry evidence nodes must be an object")
        recorded_nodes: Mapping[str, Any] = {}
    else:
        recorded_nodes = recorded_nodes_value
    unexpected_nodes = sorted(set(recorded_nodes) - set(expected_order))
    if unexpected_nodes:
        errors.append(f"registry has undeclared evidence nodes: {unexpected_nodes}")
    binding_protocol = json.loads(
        (ROOT / node_map()["mechanism_protocol"].path).read_text(
            encoding="utf-8"
        )
    )
    binding_plan = json.loads(
        (ROOT / node_map()["mechanism_gate_a_plan"].path).read_text(
            encoding="utf-8"
        )
    )
    binding_gate_a = json.loads(
        (ROOT / node_map()["mechanism_gate_a"].path).read_text(
            encoding="utf-8"
        )
    )
    binding_online = json.loads(
        (
            ROOT / node_map()["mechanism_online_policy_certificate"].path
        ).read_text(encoding="utf-8")
    )
    gate_a_binding_current = _composed_gate_a_binding_current(
        binding_gate_a,
        binding_online,
        binding_protocol,
        binding_plan,
    )
    expected_freshness: dict[str, bool] = {}
    for node in ordered:
        path = ROOT / node.path
        recorded = recorded_nodes.get(node.node_id, {})
        if not path.is_file():
            errors.append(f"missing current evidence: {node.path}")
            continue
        if recorded.get("path") != node.path:
            errors.append(f"registry path mismatch: {node.node_id}")
        errors.extend(_recorded_node_contract_errors(node, recorded))
        if recorded.get("dependencies") != list(node.dependencies):
            errors.append(f"registry dependencies stale: {node.node_id}")
        if recorded.get("sha256") != file_sha256(path):
            errors.append(f"registry digest stale: {node.node_id}")
        dependencies_fresh = all(expected_freshness[dependency] for dependency in node.dependencies)
        payload = json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else {}
        source_fresh = _artifact_source_binding_current(node, payload)
        binding_fresh = source_fresh and not (
            node.node_id == "mechanism_gate_a" and not gate_a_binding_current
        )
        expected_freshness[node.node_id] = dependencies_fresh and binding_fresh
        expected_label = "fresh" if expected_freshness[node.node_id] else "stale_dependency_binding"
        if recorded.get("freshness") != expected_label:
            errors.append(f"registry freshness state mismatch: {node.node_id}")
        expected_gate_state = (
            _node_gate_state(
                node,
                payload,
            )
            if expected_freshness[node.node_id]
            else "invalidated"
        )
        if recorded.get("gate_state") != expected_gate_state:
            errors.append(f"registry gate state mismatch: {node.node_id}")

    expected_stale_ids = sorted(
        node_id for node_id, fresh in expected_freshness.items() if not fresh
    )
    repository_integrity = current.get("repository_integrity", {})
    if repository_integrity.get("stale_binding_count") != len(expected_stale_ids):
        errors.append("repository stale binding count is inconsistent")
    if repository_integrity.get("stale_binding_ids") != expected_stale_ids:
        errors.append("repository stale binding identities are inconsistent")

    from scripts.audit_backend_v05 import validate_report as validate_backend

    backend = json.loads(
        (ROOT / node_map()["backend_candidate"].path).read_text(
            encoding="utf-8"
        )
    )
    errors.extend(f"backend report invalid: {item}" for item in validate_backend(backend))
    if backend.get("backend_contract_validated") is not True and (
        backend.get("status") != "blocked" or backend.get("backend_freeze_allowed")
    ):
        errors.append("blocked backend state is internally inconsistent")
    if backend.get("source_tree_dirty") and backend.get("backend_freeze_allowed"):
        errors.append("dirty source tree is incorrectly recorded as frozen")

    mechanism_protocol = json.loads(
        (ROOT / node_map()["mechanism_protocol"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_plan = json.loads(
        (ROOT / node_map()["mechanism_gate_a_plan"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_online = json.loads(
        (
            ROOT / node_map()["mechanism_online_policy_certificate"].path
        ).read_text(encoding="utf-8")
    )
    mechanism = json.loads(
        (ROOT / node_map()["mechanism_gate_a"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_pilot = json.loads(
        (ROOT / node_map()["mechanism_agent_pilot"].path).read_text(
            encoding="utf-8"
        )
    )
    if mechanism_design.get("protocol_sha256") != _canonical_sha256(mechanism_protocol):
        errors.append("mechanism design-audit protocol binding is stale")
    if mechanism_design.get("gate_a_plan_sha256") != _canonical_sha256(mechanism_plan):
        errors.append("mechanism design-audit Gate A plan binding is stale")
    if mechanism_design.get("pass") is not True:
        errors.append("mechanism action/intervention design audit is blocked")
    if not _online_policy_certificate_binding_current(
        mechanism_online,
        mechanism_protocol,
        mechanism_plan,
    ):
        errors.append("mechanism online-policy certificate binding is stale")
    online_reference = mechanism.get("certificate_decision", {}).get(
        "online_policy_feasible_certificate",
        {},
    )
    if (
        not isinstance(online_reference, Mapping)
        or online_reference.get("report")
        != node_map()["mechanism_online_policy_certificate"].path
        or online_reference.get("certificate_sha256")
        != _canonical_sha256(mechanism_online)
    ):
        errors.append("mechanism Gate A online-policy reference is stale")
    if not gate_a_binding_current:
        gate_node = recorded_nodes.get("mechanism_gate_a", {})
        if gate_node.get("gate_state") != "invalidated":
            errors.append("stale mechanism Gate A is not marked invalidated")
    if mechanism.get("publication_ready") is not False:
        errors.append("mechanism Gate A improperly claims publication readiness")
    if mechanism_pilot.get("gate_0", {}).get("status") != "passed":
        errors.append("mechanism Agent pilot Gate 0 integrity is blocked")
    if mechanism_pilot.get("agent_weight_updates_performed") is not False:
        errors.append("mechanism Agent pilot incorrectly records weight updates")
    if mechanism_pilot.get("benchmark_claim_allowed") is not False:
        errors.append("mechanism Agent pilot improperly enables benchmark claims")
    runtime = current.get("runtime", {})
    formal = current.get("formal_evaluation", {})
    publication = current.get("publication", {})
    expected_backend_validation = (
        "passed" if backend.get("backend_contract_validated") else "blocked"
    )
    if runtime.get("contract_validation") != expected_backend_validation:
        errors.append("current registry backend validation state is inconsistent")
    if formal.get("status") != "environment_ready_methods_unfrozen":
        errors.append("current registry formal evaluation boundary is inconsistent")
    if formal.get("formal_results_present") is not False:
        errors.append("current registry improperly records formal results")
    if formal.get("benchmark_claim_allowed") is not False:
        errors.append("current registry improperly enables benchmark claims")
    mechanism_registry = current.get("mechanism_adaptation", {})
    expected_gate_a_pass = bool(gate_a_binding_current and mechanism.get("gate_a_pass"))
    if mechanism_registry.get("gate_a_pass") != expected_gate_a_pass:
        errors.append("current registry mechanism Gate A state is inconsistent")
    if publication.get("publication_ready") is not False:
        errors.append("current registry publication state is inconsistent")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--refresh", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--explain-evidence", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.status:
        print(json.dumps(current_status_summary(), indent=2, sort_keys=True))
        return 0
    if args.explain_evidence:
        print(json.dumps(current_evidence_manifest(), indent=2, sort_keys=True))
        return 0
    if args.refresh:
        refresh()
    errors = check_current_evidence()
    print(
        json.dumps(
            {
                "status": "passed" if not errors else "failed",
                "graph_sha256": graph_sha256(),
                "node_count": len(NODES),
                "errors": errors,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
