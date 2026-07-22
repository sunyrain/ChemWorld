"""Refresh and verify ChemWorld's current evidence dependency graph.

This is the only supported entry point for regenerating *current* evidence.
Historical reports remain immutable; the paths below are materialized views of
the current source and protocol state.
"""

from __future__ import annotations

import argparse
import json
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
        "report_lifecycle_policy",
        "configs/foundation/report_lifecycle_v0.1.json",
        "protocol_input",
    ),
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
        "backend_external_gates",
        "workstreams/world_foundation/reports/backend-external-gates-v0.5.json",
        "formal_result",
        ("backend_protocol",),
    ),
    EvidenceNode(
        "contract_coherence_protocol",
        "configs/foundation/contract_coherence_v0.5.json",
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
        "risk_cost_contract",
        "configs/benchmark/risk_cost_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_families_contract",
        "configs/benchmark/mechanism_families_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "agent_interaction_contract",
        "configs/benchmark/agent_interaction_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "method_protocol_contract",
        "configs/benchmark/method_protocol_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "confirmatory_freeze_contract",
        "configs/benchmark/confirmatory_freeze_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "reference_regret_contract",
        "configs/benchmark/reference_regret_vnext.json",
        "protocol_input",
    ),
    EvidenceNode(
        "evidence_quarantine_protocol",
        "configs/benchmark/evidence_quarantine_v0.5.json",
        "protocol_input",
    ),
    EvidenceNode(
        "formal_protocol",
        "configs/benchmark/formal_protocol_v0.4.json",
        "protocol_input",
    ),
    EvidenceNode(
        "interaction_strata",
        "configs/benchmark/interaction_strata_v0.4.json",
        "protocol_input",
    ),
    EvidenceNode(
        "statistical_analysis",
        "configs/benchmark/statistical_analysis_plan_v0.4.json",
        "protocol_input",
    ),
    EvidenceNode(
        "method_freeze_plan",
        "configs/benchmark/method_freeze_v0.4.json",
        "protocol_input",
    ),
    EvidenceNode(
        "llm_development_plan",
        "configs/methods/llm_v0.4/llm_development_plan.json",
        "protocol_input",
        ("runtime_affordance",),
    ),
    EvidenceNode(
        "live_llm_methods",
        "configs/methods/llm_v0.4/llm_methods.json",
        "protocol_input",
    ),
    EvidenceNode(
        "classic_methods",
        "configs/methods/classic_v0.4.1/classic_methods.json",
        "protocol_input",
    ),
    EvidenceNode(
        "operation_methods",
        "configs/methods/operation_v0.4.1/operation_methods.json",
        "protocol_input",
    ),
    EvidenceNode(
        "classic_development",
        "workstreams/benchmark_v1/reports/classic-dev-v0.4.1.json",
        "development_diagnostic",
        ("classic_methods",),
    ),
    EvidenceNode(
        "operation_development",
        "workstreams/benchmark_v1/reports/operation-baselines-dev-v0.4.1.json",
        "development_diagnostic",
        ("operation_methods",),
    ),
    EvidenceNode(
        "ppo_preflight",
        "workstreams/benchmark_v1/reports/rl-ppo-v0412-preflight-v0.4.json",
        "development_diagnostic",
    ),
    EvidenceNode(
        "sac_preflight",
        "workstreams/benchmark_v1/reports/rl-sac-v0412-preflight-v0.4.json",
        "development_diagnostic",
    ),
    EvidenceNode(
        "live_llm_development",
        "workstreams/benchmark_v1/reports/live-llm-dev-v0.4.11.json",
        "development_diagnostic",
        ("live_llm_methods", "llm_development_plan", "runtime_affordance"),
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
        "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc2.json",
        "formal_result",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_protocol_report",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-final-protocol-v0.2.md",
        "development_diagnostic",
        ("mechanism_protocol",),
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
            "mechanism_protocol_report",
            "mechanism_public_matrix",
        ),
        ("scripts/check_mechanism_adaptation_protocol.py",),
    ),
    EvidenceNode(
        "mechanism_gate_a",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.2.4.json",
        "formal_result",
        (
            "backend_candidate",
            "backend_protocol",
            "evaluation_contract",
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
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
        ("public_boundary_protocol", "runtime_integration"),
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
            "backend_external_gates",
        ),
        ("scripts/audit_backend_v05.py", "--allow-dirty"),
    ),
    EvidenceNode(
        "contract_coherence",
        "workstreams/world_foundation/reports/contract-coherence-v0.5.json",
        "generated_current",
        (
            "agent_interaction_contract",
            "backend_candidate",
            "confirmatory_freeze_contract",
            "contract_coherence_protocol",
            "evaluation_contract",
            "evidence_quarantine_protocol",
            "mechanism_families_contract",
            "method_protocol_contract",
            "reference_regret_contract",
            "risk_cost_contract",
            "runtime_reachability",
            "score_replay_contract",
            "state_transition_invariants",
        ),
        ("scripts/audit_contract_coherence_v0.5.py",),
    ),
    EvidenceNode(
        "method_freeze",
        "workstreams/benchmark_v1/reports/method-freeze-v0.4.json",
        "generated_current",
        (
            "backend_candidate",
            "classic_development",
            "contract_coherence",
            "formal_protocol",
            "interaction_strata",
            "live_llm_development",
            "llm_development_plan",
            "method_freeze_plan",
            "operation_development",
            "statistical_analysis",
        ),
        ("scripts/audit_method_freeze_v0.4.py",),
    ),
    EvidenceNode(
        "backend_bundle",
        "benchmark/releases/chemworld-serious-vnext/manifest.json",
        "generated_current",
        (
            "backend_candidate",
            "backend_golden_fixture",
            "maturity_truth",
            "public_boundary",
            "runtime_integration",
        ),
        ("scripts/build_vnext_backend_candidate.py",),
    ),
    EvidenceNode(
        "report_lifecycle_index",
        "workstreams/report-lifecycle-index-v0.1.json",
        "generated_current",
        (
            "backend_candidate",
            "backend_external_gates",
            "classic_development",
            "contract_coherence",
            "live_llm_development",
            "mechanism_agent_pilot",
            "mechanism_design_audit",
            "mechanism_gate_a",
            "mechanism_preflight",
            "mechanism_public_matrix",
            "method_freeze",
            "operation_development",
            "ppo_preflight",
            "public_boundary",
            "report_lifecycle_policy",
            "runtime_affordance",
            "runtime_integration",
            "runtime_reachability",
            "sac_preflight",
            "state_transition_invariants",
        ),
        ("scripts/build_report_lifecycle_index.py",),
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
    CurrentPathRule(("formal_evaluation", "protocol"), "protocol_input"),
    CurrentPathRule(("formal_evaluation", "interaction_strata"), "protocol_input"),
    CurrentPathRule(("formal_evaluation", "statistical_analysis"), "protocol_input"),
    CurrentPathRule(
        ("formal_evaluation", "contract_coherence_report"),
        "generated_current",
    ),
    CurrentPathRule(("formal_evaluation", "method_freeze_report"), "generated_current"),
    CurrentPathRule(("mechanism_adaptation", "protocol"), "protocol_input"),
    CurrentPathRule(("mechanism_adaptation", "preflight_report"), "generated_current"),
    CurrentPathRule(("mechanism_adaptation", "protocol_report"), "development_diagnostic"),
    CurrentPathRule(("mechanism_adaptation", "gate_a_plan"), "protocol_input"),
    CurrentPathRule(("mechanism_adaptation", "gate_a_report"), "formal_result"),
    CurrentPathRule(
        ("mechanism_adaptation", "agent_pilot_report"),
        "development_diagnostic",
    ),
    CurrentPathRule(("mechanism_adaptation", "design_audit_report"), "formal_result"),
    CurrentPathRule(
        ("development_evidence", "classic", "methods"),
        "protocol_input",
        metadata_path=("development_evidence", "classic"),
    ),
    CurrentPathRule(
        ("development_evidence", "classic", "report"),
        "development_diagnostic",
        metadata_path=("development_evidence", "classic"),
    ),
    CurrentPathRule(
        ("development_evidence", "operation", "methods"),
        "protocol_input",
        metadata_path=("development_evidence", "operation"),
    ),
    CurrentPathRule(
        ("development_evidence", "operation", "report"),
        "development_diagnostic",
        metadata_path=("development_evidence", "operation"),
    ),
    CurrentPathRule(
        ("development_evidence", "live_llm", "report"),
        "development_diagnostic",
        metadata_path=("development_evidence", "live_llm"),
    ),
    CurrentPathRule(("publication", "archived_working_draft"), "archived_history"),
    CurrentPathRule(("history_policy", "report_lifecycle_index"), "generated_current"),
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


def _run(node: EvidenceNode) -> None:
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
    completed = subprocess.run(
        command,
        cwd=ROOT,
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
    allowed_codes = {0, 1} if node.node_id in {"backend_candidate", "method_freeze"} else {0}
    if completed.returncode not in allowed_codes:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"generator failed for {node.node_id}: {detail}")
    if not (ROOT / node.path).is_file():
        raise RuntimeError(f"generator did not create {node.path}")


MATERIALIZED_OUTPUT_PREFIXES = ("benchmark/releases/chemworld-serious-vnext/",)


def _is_materialized_output_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    materialized_paths = {
        node.path.replace("\\", "/") for node in NODES if node.command is not None
    }
    materialized_paths.add("configs/current.json")
    return normalized in materialized_paths or normalized.startswith(MATERIALIZED_OUTPUT_PREFIXES)


def _git_tree_dirty() -> bool:
    """Return whether tracked source/protocol inputs differ from HEAD.

    Current evidence reports and release-bundle views are generated outputs. They
    may change during a DAG refresh without making the source tree itself dirty.
    """

    return git_worktree_dirty(
        ROOT,
        excluded_paths={
            "configs/current.json",
            *(node.path for node in NODES if node.command is not None),
        },
        excluded_prefixes=MATERIALIZED_OUTPUT_PREFIXES,
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


def _artifact_source_binding_current(
    node: EvidenceNode,
    payload: Mapping[str, Any],
) -> bool:
    """Verify declared report provenance against current executable source."""

    if node.role in {"protocol_input", "fixture"}:
        return True
    if node.node_id == "report_lifecycle_index":
        policy = json.loads(
            (ROOT / "configs/foundation/report_lifecycle_v0.1.json").read_text(
                encoding="utf-8"
            )
        )
        inventory = [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
            }
            for path in sorted(ROOT.glob(str(policy["report_glob"])))
            if path.is_file()
        ]
        if payload.get("report_corpus_sha256") != _canonical_sha256(inventory):
            return False
    if node.node_id == "runtime_affordance":
        from chemworld.eval.runtime_domain_affordance_audit import (
            guarded_source_sha256,
        )

        if payload.get("guarded_source_sha256") != guarded_source_sha256(ROOT):
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
    return not (
        isinstance(recorded_dirty, bool) and recorded_dirty != _git_tree_dirty()
    )


def _node_gate_state(node: EvidenceNode, payload: dict[str, Any]) -> str:
    if node.node_id == "report_lifecycle_index":
        return (
            "passed"
            if payload.get("status") == "complete"
            and payload.get("all_reports_classified_exactly_once") is True
            else "blocked"
        )
    if node.node_id == "backend_external_gates":
        return "passed" if payload.get("status") == "passed" else "blocked"
    if node.node_id == "backend_candidate":
        return "passed" if payload.get("backend_contract_validated") else "blocked"
    if node.node_id == "method_freeze":
        return "passed" if payload.get("method_freeze_ready") else "blocked"
    if node.node_id == "mechanism_gate_a":
        return "passed" if payload.get("gate_a_pass") else "blocked"
    if node.node_id == "mechanism_design_audit":
        return "passed" if payload.get("pass") else "blocked"
    if payload.get("passed") is False or payload.get("controls_ready") is False:
        return "blocked"
    return "passed"


def _formal_method_readiness(method: Mapping[str, Any]) -> dict[str, Any]:
    families = method.get("method_families", {})
    if not isinstance(families, Mapping):
        return {"ready": 0, "required": 5}
    classic = families.get("classic", {})
    operation = families.get("operation_baselines", {})
    llm = families.get("llm", {})
    rl = families.get("rl", {})
    ppo = rl.get("ppo", {}) if isinstance(rl, Mapping) else {}
    sac = rl.get("sac", {}) if isinstance(rl, Mapping) else {}
    readiness = {
        "classic": bool(isinstance(classic, Mapping) and classic.get("development_ready")),
        "operation_baselines": bool(
            isinstance(operation, Mapping) and operation.get("development_ready")
        ),
        "llm": bool(isinstance(llm, Mapping) and llm.get("development_ready")),
        "rl_ppo": bool(isinstance(ppo, Mapping) and ppo.get("development_ready")),
        "rl_sac": bool(isinstance(sac, Mapping) and sac.get("development_ready")),
    }
    return {
        "ready": sum(readiness.values()),
        "required": len(readiness),
        "slots": readiness,
    }


def _formal_protocol_binding_current(
    formal_protocol: Mapping[str, Any],
    backend_protocol: Mapping[str, Any],
    backend_report: Mapping[str, Any],
) -> bool:
    """Return whether the preregistered formal protocol targets this backend contract."""

    binding = formal_protocol.get("backend_binding", {})
    task_roles = formal_protocol.get("task_roles", {})
    formal_core = task_roles.get("formal_core", {}) if isinstance(task_roles, Mapping) else {}
    current_hashes = backend_report.get("task_contract_hashes", {})
    if not isinstance(binding, Mapping):
        return False
    manifest_relative = binding.get("release_manifest_path")
    if not isinstance(manifest_relative, str):
        return False
    manifest_path = (ROOT / manifest_relative).resolve()
    if not manifest_path.is_relative_to(ROOT.resolve()) or not manifest_path.is_file():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    p0_bindings = formal_protocol.get("p0_evidence_bindings", ())
    p0_current = bool(
        isinstance(p0_bindings, list)
        and p0_bindings
        and all(
            isinstance(item, Mapping)
            and isinstance(item.get("path"), str)
            and (ROOT / str(item["path"])).is_file()
            and item.get("sha256") == file_sha256(ROOT / str(item["path"]))
            for item in p0_bindings
        )
    )
    return bool(
        isinstance(formal_core, Mapping)
        and isinstance(current_hashes, Mapping)
        and isinstance(manifest, Mapping)
        and binding.get("release_manifest_sha256") == file_sha256(manifest_path)
        and binding.get("release_manifest_id") == manifest.get("backend_id")
        and binding.get("backend_semantic_sha256")
        == manifest.get("backend_semantic_sha256")
        and binding.get("runtime_backend_id") == backend_protocol.get("backend_id")
        and binding.get("world_law_id") == backend_protocol.get("world_law_id")
        and binding.get("task_contract_version") == backend_protocol.get("task_contract_version")
        and p0_current
        and formal_core
        and all(
            isinstance(spec, Mapping)
            and spec.get("task_contract_hash") == current_hashes.get(task_id)
            for task_id, spec in formal_core.items()
        )
    )


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
    readiness = formal["method_family_readiness"]
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
            "protocol_binding_state": formal["protocol_binding_state"],
            "method_families_ready": (f"{readiness['ready']}/{readiness['required']}"),
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
    backend = json.loads((ROOT / node_map()["backend_candidate"].path).read_text())
    backend_protocol = json.loads((ROOT / node_map()["backend_protocol"].path).read_text())
    coherence = json.loads((ROOT / node_map()["contract_coherence"].path).read_text())
    formal_protocol = json.loads((ROOT / node_map()["formal_protocol"].path).read_text())
    method = json.loads((ROOT / node_map()["method_freeze"].path).read_text())
    mechanism = json.loads((ROOT / node_map()["mechanism_gate_a"].path).read_text())
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text()
    )
    mechanism_pilot = json.loads((ROOT / node_map()["mechanism_agent_pilot"].path).read_text())
    method_plan = json.loads((ROOT / node_map()["method_freeze_plan"].path).read_text())
    mechanism_protocol = json.loads((ROOT / node_map()["mechanism_protocol"].path).read_text())
    mechanism_plan = json.loads((ROOT / node_map()["mechanism_gate_a_plan"].path).read_text())
    mechanism_evidence_current = _gate_a_binding_current(
        mechanism,
        mechanism_protocol,
        mechanism_plan,
    )
    mechanism_gate_a_pass = bool(mechanism_evidence_current and mechanism.get("gate_a_pass"))
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
    formal_protocol_current = _formal_protocol_binding_current(
        formal_protocol,
        backend_protocol,
        backend,
    )
    live_llm = json.loads((ROOT / node_map()["live_llm_development"].path).read_text())
    from chemworld.data.schema import OUTCOME_LAYER_FIELDS, TRAJECTORY_SCHEMA_VERSION

    dirty = _git_tree_dirty()
    nodes: dict[str, Any] = {}
    for node in generation_order():
        path = ROOT / node.path
        payload = json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else {}
        dependency_fresh = node.node_id == "report_lifecycle_index" or all(
            nodes[dependency]["freshness"] == "fresh" for dependency in node.dependencies
        )
        source_fresh = _artifact_source_binding_current(node, payload)
        binding_fresh = source_fresh and not (
            node.node_id == "mechanism_gate_a" and not mechanism_evidence_current
        )
        fresh = dependency_fresh and binding_fresh
        gate_state = _node_gate_state(node, payload) if fresh else "invalidated"
        if node.node_id == "formal_protocol" and not formal_protocol_current:
            gate_state = "invalidated"
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
        "legacy_trajectory_aliases_retained": [
            "benchmark_task_id",
            "observation",
            "reward",
            "agent_view",
            "leaderboard_score",
        ],
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
            "role": "formal_confirmatory_comparison",
            "protocol": "configs/benchmark/method_freeze_v0.4.json",
            "task_ids": list(method_plan["formal_core_tasks"]),
            "status": ("ready" if method.get("method_freeze_ready") else "method_freeze_blocked"),
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
    current["runtime"].update(
        {
            "status": backend["status"],
            "world_law_id": backend_protocol["world_law_id"],
            "task_contract_version": backend_protocol["task_contract_version"],
            "contract_validation": (
                "passed" if backend["backend_contract_validated"] else "blocked"
            ),
            "clean_release_attestation": backend["clean_release_attestation"],
            "external_quality_gates": (
                "passed"
                if backend.get("external_gate_evidence", {}).get("passed") is True
                else "pending"
            ),
            "source_tree_dirty": backend["source_tree_dirty"],
        }
    )
    current["formal_evaluation"].update(
        {
            "contract_coherence_report": node_map()["contract_coherence"].path,
            "contract_coherence_ready": coherence["controls_ready"],
            "protocol_binding_state": (
                "current"
                if formal_protocol_current
                else "invalidated_dependency_binding_mismatch"
            ),
            "status": (
                "method_freeze_ready"
                if formal_protocol_current and method["method_freeze_ready"]
                else "method_freeze_preflight_blocked"
                if formal_protocol_current
                else "formal_protocol_recertification_required"
            ),
            "method_freeze_ready": method["method_freeze_ready"],
            "bench_unlock_allowed": method["bench_unlock_allowed"],
            "blocker_count": len(method["blockers"]),
            "method_family_readiness": _formal_method_readiness(method),
            "formal_results_present": False,
            "benchmark_claim_allowed": False,
        }
    )
    current["mechanism_adaptation"].update(
        {
            "protocol": node_map()["mechanism_protocol"].path,
            "preflight_report": node_map()["mechanism_preflight"].path,
            "design_audit_report": node_map()["mechanism_design_audit"].path,
            "design_audit_pass": bool(
                mechanism_design.get("pass")
                and nodes["mechanism_design_audit"]["artifact_state"] == "current"
            ),
            "gate_a_plan": node_map()["mechanism_gate_a_plan"].path,
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
    )
    current["development_evidence"] = {
        "classic": {
            "methods": "configs/methods/classic_v0.4.1/classic_methods.json",
            "report": "workstreams/benchmark_v1/reports/classic-dev-v0.4.1.json",
            "artifact_state": nodes["classic_development"]["artifact_state"],
            "artifact_roles": ["protocol_input", "development_diagnostic"],
        },
        "operation": {
            "methods": "configs/methods/operation_v0.4.1/operation_methods.json",
            "report": ("workstreams/benchmark_v1/reports/operation-baselines-dev-v0.4.1.json"),
            "artifact_state": nodes["operation_development"]["artifact_state"],
            "artifact_roles": ["protocol_input", "development_diagnostic"],
        },
        "live_llm": {
            "target_version": "v0.4.11",
            "report": node_map()["live_llm_development"].path,
            "artifact_state": nodes["live_llm_development"]["artifact_state"],
            "artifact_roles": ["development_diagnostic"],
            "stage": live_llm["stage"],
            "promotion_decision": live_llm["promotion_gate"]["decision"],
            "formal_live_llm_development_ready": live_llm["formal_live_llm_development_ready"],
            "resume_prior_caches": False,
        },
        "formal_benchmark_evidence": False,
    }
    current["publication"] = {
        "status": "no_active_manuscript",
        "archived_working_draft": ("paper/archive/ncs-working-draft-2026-07-21/README.md"),
        "publication_ready": False,
    }
    blockers: list[dict[str, Any]] = []
    if backend["clean_release_attestation"] != "passed":
        blockers.append({"id": "clean_release_attestation_pending", "scope": "backend_release"})
    if not method["method_freeze_ready"]:
        blockers.append(
            {
                "id": "method_freeze_blocked",
                "scope": "formal_benchmark",
                "count": len(method["blockers"]),
            }
        )
    if not formal_protocol_current:
        blockers.append(
            {
                "id": "formal_protocol_recertification_required",
                "scope": "formal_benchmark",
                "reason": "dependency_binding_mismatch",
            }
        )
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
        "stale_binding_count": sum(
            node["artifact_state"] == "stale" for node in nodes.values()
        ),
        "stale_binding_ids": sorted(
            node_id
            for node_id, node in nodes.items()
            if node["artifact_state"] == "stale"
        ),
        "blockers": blockers,
    }
    current["history_policy"] = {
        "report_lifecycle_policy": node_map()["report_lifecycle_policy"].path,
        "report_lifecycle_index": node_map()["report_lifecycle_index"].path,
        "current_materialized_views_are_regenerated_by_the_evidence_dag": True,
        "historical_artifacts_are_immutable": True,
        "version_suffix_does_not_imply_current": True,
        "archive_directories_contain_non_current_diagnostics": True,
        "raw_runs_require_a_manifested_retention_decision_before_deletion": True,
    }
    write_json_atomic(CURRENT_REGISTRY, current, sort_keys=False)


def refresh() -> None:
    for node in generation_order():
        _run(node)
    _write_current_registry()


def _check_bundle(errors: list[str]) -> None:
    bundle_dir = ROOT / "benchmark/releases/chemworld-serious-vnext"
    manifest = json.loads((bundle_dir / "manifest.json").read_text())
    for filename, expected in manifest.get("artifact_sha256", {}).items():
        path = bundle_dir / filename
        if not path.is_file() or file_sha256(path) != expected:
            errors.append(f"backend bundle artifact is stale: {filename}")


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
    binding_protocol = json.loads((ROOT / node_map()["mechanism_protocol"].path).read_text())
    binding_plan = json.loads((ROOT / node_map()["mechanism_gate_a_plan"].path).read_text())
    binding_gate_a = json.loads((ROOT / node_map()["mechanism_gate_a"].path).read_text())
    gate_a_binding_current = _gate_a_binding_current(
        binding_gate_a,
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
        dependencies_fresh = node.node_id == "report_lifecycle_index" or all(
            expected_freshness[dependency] for dependency in node.dependencies
        )
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
        if (
            node.node_id == "formal_protocol"
            and current.get("formal_evaluation", {}).get("protocol_binding_state") != "current"
        ):
            expected_gate_state = "invalidated"
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

    from chemworld.eval.live_llm_development import (
        load_runtime_domain_affordance_binding,
    )

    try:
        load_runtime_domain_affordance_binding()
    except (RuntimeError, ValueError) as error:
        errors.append(f"runtime affordance binding invalid: {error}")

    from scripts.audit_backend_v05 import validate_report as validate_backend

    backend = json.loads((ROOT / node_map()["backend_candidate"].path).read_text())
    errors.extend(f"backend report invalid: {item}" for item in validate_backend(backend))
    if backend.get("backend_contract_validated") is not True and (
        backend.get("status") != "blocked" or backend.get("backend_freeze_allowed")
    ):
        errors.append("blocked backend state is internally inconsistent")
    if backend.get("source_tree_dirty") and backend.get("backend_freeze_allowed"):
        errors.append("dirty source tree is incorrectly recorded as frozen")

    method = json.loads((ROOT / node_map()["method_freeze"].path).read_text())
    coherence = json.loads((ROOT / node_map()["contract_coherence"].path).read_text())
    if coherence.get("controls_ready") is not True:
        errors.append("formal contract coherence is blocked")
    if method.get("benchmark_claim_allowed") is not False:
        errors.append("method-freeze report improperly enables benchmark claims")
    mechanism_protocol = json.loads((ROOT / node_map()["mechanism_protocol"].path).read_text())
    mechanism_plan = json.loads((ROOT / node_map()["mechanism_gate_a_plan"].path).read_text())
    mechanism_design = json.loads((ROOT / node_map()["mechanism_design_audit"].path).read_text())
    mechanism = json.loads((ROOT / node_map()["mechanism_gate_a"].path).read_text())
    mechanism_pilot = json.loads((ROOT / node_map()["mechanism_agent_pilot"].path).read_text())
    if mechanism_design.get("protocol_sha256") != _canonical_sha256(mechanism_protocol):
        errors.append("mechanism design-audit protocol binding is stale")
    if mechanism_design.get("gate_a_plan_sha256") != _canonical_sha256(mechanism_plan):
        errors.append("mechanism design-audit Gate A plan binding is stale")
    if mechanism_design.get("pass") is not True:
        errors.append("mechanism action/intervention design audit is blocked")
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
    _check_bundle(errors)

    runtime = current.get("runtime", {})
    formal = current.get("formal_evaluation", {})
    publication = current.get("publication", {})
    expected_backend_validation = (
        "passed" if backend.get("backend_contract_validated") else "blocked"
    )
    if runtime.get("contract_validation") != expected_backend_validation:
        errors.append("current registry backend validation state is inconsistent")
    if formal.get("method_freeze_ready") != method.get("method_freeze_ready"):
        errors.append("current registry method-freeze state is inconsistent")
    formal_protocol = json.loads((ROOT / node_map()["formal_protocol"].path).read_text())
    backend_protocol = json.loads((ROOT / node_map()["backend_protocol"].path).read_text())
    expected_formal_binding_state = (
        "current"
        if _formal_protocol_binding_current(formal_protocol, backend_protocol, backend)
        else "invalidated_dependency_binding_mismatch"
    )
    if formal.get("protocol_binding_state") != expected_formal_binding_state:
        errors.append("current registry formal protocol binding state is inconsistent")
    if expected_formal_binding_state != "current":
        formal_node = recorded_nodes.get("formal_protocol", {})
        if formal_node.get("gate_state") != "invalidated":
            errors.append("mismatched formal protocol is not marked invalidated")
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
