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
from chemworld.eval.mechanism_adaptation_execution import load_json_object  # noqa: E402
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
        "configs/methods/llm_v0.4/llm_methods_rc25.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_protocol",
        "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_gate_a_plan",
        "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json",
        "protocol_input",
        ("mechanism_protocol",),
    ),
    EvidenceNode(
        "mechanism_participant_preregistration_candidate",
        "configs/benchmark/"
        "mechanism_adaptation_participant_preregistration_rc28.json",
        "protocol_input",
        ("live_llm_methods", "mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_diagnostic_relation_graph",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc28.json",
        "generated_current",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_sample_size_audit",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-sample-size-audit-v0.3.0-rc28.json",
        "generated_current",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_preregistration",
        "configs/benchmark/"
        "mechanism-adaptation-preregistration-v0.3.0-rc28.json",
        "generated_current",
        (
            "mechanism_diagnostic_relation_graph",
            "mechanism_gate_a_plan",
            "mechanism_protocol",
            "mechanism_sample_size_audit",
        ),
    ),
    EvidenceNode(
        "mechanism_confirmatory_task_semantics_audit",
        "workstreams/flagship_tasks/reports/"
        "confirmatory-task-semantics-audit-rc28.json",
        "generated_current",
        (
            "mechanism_diagnostic_relation_graph",
            "mechanism_gate_a_plan",
            "mechanism_preregistration",
            "mechanism_protocol",
        ),
    ),
    EvidenceNode(
        "mechanism_design_audit",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc28.json",
        "generated_current",
        (
            "mechanism_diagnostic_relation_graph",
            "mechanism_confirmatory_task_semantics_audit",
            "mechanism_gate_a_plan",
            "mechanism_protocol",
        ),
    ),
    EvidenceNode(
        "mechanism_release_qualification",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-release-qualification-v0.1-rc28.json",
        "release_attestation",
        (
            "mechanism_design_audit",
            "mechanism_confirmatory_task_semantics_audit",
            "mechanism_gate_a_plan",
            "mechanism_preregistration",
            "mechanism_protocol",
            "mechanism_sample_size_audit",
        ),
    ),
    EvidenceNode(
        "mechanism_public_matrix",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-public-matrix.json",
        "generated_current",
        ("mechanism_protocol",),
        ("scripts/plan_mechanism_adaptation_matrix.py",),
    ),
    EvidenceNode(
        "mechanism_preflight",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-preflight.json",
        "generated_current",
        (
            "mechanism_gate_a_plan",
            "mechanism_design_audit",
            "mechanism_confirmatory_task_semantics_audit",
            "mechanism_protocol",
            "mechanism_public_matrix",
            "mechanism_preregistration",
            "mechanism_release_qualification",
            "mechanism_sample_size_audit",
        ),
        ("scripts/check_mechanism_adaptation_protocol.py",),
    ),
    EvidenceNode(
        "mechanism_a2_structural_receipt",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-a2-structural-receipt-v0.1-rc28.json",
        "formal_result",
        (
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
            "mechanism_preregistration",
            "mechanism_protocol",
            "mechanism_release_qualification",
        ),
    ),
    EvidenceNode(
        "mechanism_a3_structural_receipt",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-a3-structural-receipt-v0.1-rc28.json",
        "formal_result",
        (
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
            "mechanism_preregistration",
            "mechanism_protocol",
            "mechanism_release_qualification",
        ),
    ),
    EvidenceNode(
        "mechanism_public_gate_a_decision",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-public-decision-v0.1-rc28.json",
        "formal_result",
        (
            "mechanism_a2_structural_receipt",
            "mechanism_a3_structural_receipt",
            "mechanism_design_audit",
            "mechanism_diagnostic_relation_graph",
            "mechanism_confirmatory_task_semantics_audit",
            "mechanism_gate_a_plan",
            "mechanism_preregistration",
            "mechanism_protocol",
            "mechanism_release_qualification",
            "mechanism_sample_size_audit",
        ),
    ),
    EvidenceNode(
        "static_s0_electrochemical_protocol",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.0_electrochemical_material_opaque_20x10_formal.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_electrochemical_method",
        "configs/methods/llm_v1.0/"
        "participant_methods_s0_codex_subscription_sol_"
        "electrochemical_material_opaque_20x10_v10.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_electrochemical_world_understanding",
        "configs/benchmark/world_understanding_s0_electrochemical_material_v1.0.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_electrochemical_baselines",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.0_"
        "electrochemical_classic_baselines_20x10_formal.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_electrochemical_qualification",
        "workstreams/flagship_tasks/reports/static-s0-material-family-v2-qualification-v0.3.json",
        "development_diagnostic",
        ("static_s0_electrochemical_protocol",),
    ),
    EvidenceNode(
        "static_s0_crystallization_protocol",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.0_"
        "crystallization_material_opaque_20x10_formal.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_crystallization_method",
        "configs/methods/llm_v1.0/"
        "participant_methods_s0_codex_subscription_sol_"
        "crystallization_material_opaque_20x10_v10.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_crystallization_world_understanding",
        "configs/benchmark/world_understanding_s0_crystallization_material_v1.0.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_crystallization_baselines",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.0_"
        "crystallization_classic_baselines_20x10_formal.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_crystallization_qualification",
        "workstreams/flagship_tasks/reports/static-s0-crystallization-material-family-v1-qualification-v0.1.json",
        "development_diagnostic",
        ("static_s0_crystallization_protocol",),
    ),
    EvidenceNode(
        "static_s0_freeze_manifest",
        "configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json",
        "protocol_input",
        (
            "static_s0_electrochemical_protocol",
            "static_s0_electrochemical_method",
            "static_s0_electrochemical_world_understanding",
            "static_s0_electrochemical_baselines",
            "static_s0_crystallization_protocol",
            "static_s0_crystallization_method",
            "static_s0_crystallization_world_understanding",
            "static_s0_crystallization_baselines",
        ),
    ),
    EvidenceNode(
        "static_s0_replacement_readiness",
        "workstreams/flagship_tasks/reports/static-s0-replacement-readiness-v0.1.json",
        "development_diagnostic",
        (
            "static_s0_electrochemical_protocol",
            "static_s0_electrochemical_method",
            "static_s0_electrochemical_world_understanding",
            "static_s0_electrochemical_baselines",
            "static_s0_electrochemical_qualification",
            "static_s0_crystallization_protocol",
            "static_s0_crystallization_method",
            "static_s0_crystallization_world_understanding",
            "static_s0_crystallization_baselines",
            "static_s0_crystallization_qualification",
            "static_s0_freeze_manifest",
        ),
    ),
    EvidenceNode(
        "static_s0_formal_campaign_summary",
        "workstreams/flagship_tasks/reports/"
        "static-s0-v1.0-formal-campaign-summary.json",
        "formal_result",
        ("static_s0_freeze_manifest",),
    ),
    EvidenceNode(
        "static_s0_nominal_information_freeze_manifest",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json",
        "protocol_input",
        ("static_s0_formal_campaign_summary",),
    ),
    EvidenceNode(
        "static_s0_misindexed_information_freeze_manifest",
        "configs/benchmark/"
        "scientific_optimization_s0_v1.2_misindexed_information_freeze_manifest.json",
        "protocol_input",
        (
            "static_s0_formal_campaign_summary",
            "static_s0_nominal_information_freeze_manifest",
        ),
    ),
    EvidenceNode(
        "static_s0_material_information_triarm_summary",
        "workstreams/flagship_tasks/reports/"
        "static-s0-v1.2-three-arm-information-campaign-summary.json",
        "formal_result",
        (
            "static_s0_formal_campaign_summary",
            "static_s0_nominal_information_freeze_manifest",
            "static_s0_misindexed_information_freeze_manifest",
        ),
    ),
    EvidenceNode(
        "static_s0_five_task_campaign_plan",
        "configs/benchmark/static_s0_five_task_campaign_20x5_v0.1_dev.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_five_task_participant_method",
        "configs/methods/llm_v1.5/"
        "participant_methods_s0_codex_subscription_sol_five_task_20x5_v15.json",
        "protocol_input",
    ),
    EvidenceNode(
        "static_s0_five_task_postqualification_summary",
        "workstreams/flagship_tasks/reports/"
        "static-s0-five-task-postqualification-campaign-summary.json",
        "development_diagnostic",
        (
            "backend_candidate",
            "static_s0_five_task_campaign_plan",
            "static_s0_five_task_participant_method",
        ),
    ),
    EvidenceNode(
        "task_design_matrix",
        "workstreams/flagship_tasks/reports/task-design-matrix-v1.json",
        "generated_current",
        ("static_s0_formal_campaign_summary",),
        command=(
            "scripts/build_task_design_matrix.py",
            "--output",
            "workstreams/flagship_tasks/reports/task-design-matrix-v1.json",
        ),
    ),
    EvidenceNode(
        "pre_arxiv_claim_evidence_ledger",
        "workstreams/flagship_tasks/reports/"
        "pre-arxiv-claim-evidence-ledger-v1.json",
        "development_diagnostic",
        (
            "mechanism_public_gate_a_decision",
            "static_s0_formal_campaign_summary",
            "static_s0_material_information_triarm_summary",
            "task_design_matrix",
        ),
    ),
    EvidenceNode(
        "mechanism_agent_pilot",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-agent-pilot-v0.2.1.json",
        "development_diagnostic",
        ("live_llm_methods",),
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
        "release_attestation",
        "development_diagnostic",
        "fixture",
        "superseded",
        "archive",
    }
)
CURRENT_ARTIFACT_ROLES = ARTIFACT_ROLES - {"superseded", "archive"}

FROZEN_MECHANISM_NODE_IDS = frozenset(
    {
        "mechanism_diagnostic_relation_graph",
        "mechanism_sample_size_audit",
        "mechanism_preregistration",
        "mechanism_confirmatory_task_semantics_audit",
        "mechanism_design_audit",
    }
)


def _node_lifecycle(node: EvidenceNode) -> str:
    if node.node_id in FROZEN_MECHANISM_NODE_IDS:
        return "immutable"
    return "generated" if node.command is not None else "immutable"


def _node_producer(node: EvidenceNode) -> str:
    if node.node_id in FROZEN_MECHANISM_NODE_IDS:
        return "frozen_rc28_preregistration_evidence"
    if node.command is not None:
        return "python " + " ".join(node.command)
    return {
        "protocol_input": "maintainer_versioned_input",
        "formal_result": "frozen_formal_execution",
        "release_attestation": "frozen_release_qualification",
        "development_diagnostic": "versioned_development_execution",
        "fixture": "maintainer_versioned_fixture",
    }[node.role]


def _node_source_binding(node: EvidenceNode) -> str:
    return {
        "protocol_input": "content_sha256",
        "generated_current": "dependencies_and_source_commit",
        "formal_result": "protocol_plan_and_result_sha256",
        "release_attestation": (
            "preregistered_source_commit_and_protocol_plan_sha256"
        ),
        "development_diagnostic": "content_and_versioned_source_sha256",
        "fixture": "content_sha256",
    }[node.role]


def _node_contract_errors(node: EvidenceNode) -> list[str]:
    errors: list[str] = []
    if node.role not in ARTIFACT_ROLES:
        errors.append(f"undeclared artifact role: {node.node_id} -> {node.role}")
    elif node.role not in CURRENT_ARTIFACT_ROLES:
        errors.append(f"non-current artifact appears in current DAG: {node.node_id}")
    if (
        node.role == "generated_current"
        and node.command is None
        and node.node_id not in FROZEN_MECHANISM_NODE_IDS
    ):
        errors.append(f"generated current artifact has no producer: {node.node_id}")
    if node.role != "generated_current" and node.command is not None:
        errors.append(f"immutable artifact declares a generator: {node.node_id}")
    return errors


CURRENT_PATH_RULES = (
    CurrentPathRule(("runtime", "backend"), "protocol_input"),
    CurrentPathRule(("runtime", "backend_report"), "generated_current"),
    CurrentPathRule(("task_design", "matrix"), "generated_current"),
    CurrentPathRule(
        ("static_scientific_optimization", "summary"),
        "formal_result",
    ),
    CurrentPathRule(
        ("static_material_information_three_arm", "summary"),
        "formal_result",
    ),
    CurrentPathRule(
        ("static_material_information_three_arm", "nominal_freeze_manifest"),
        "protocol_input",
    ),
    CurrentPathRule(
        ("static_material_information_three_arm", "misindexed_freeze_manifest"),
        "protocol_input",
    ),
    CurrentPathRule(
        ("static_s0_five_task_postqualification", "summary"),
        "development_diagnostic",
    ),
    CurrentPathRule(
        ("publication", "claim_evidence_ledger"),
        "development_diagnostic",
    ),
    CurrentPathRule(("publication", "manuscript"), "development_diagnostic"),
    CurrentPathRule(("mechanism_adaptation", "protocol"), "protocol_input"),
    CurrentPathRule(("mechanism_adaptation", "preflight_report"), "generated_current"),
    CurrentPathRule(("mechanism_adaptation", "gate_a_plan"), "protocol_input"),
    CurrentPathRule(
        ("mechanism_adaptation", "a2_structural_receipt"),
        "formal_result",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "a3_structural_receipt"),
        "formal_result",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "public_decision_report"),
        "formal_result",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "agent_pilot_report"),
        "development_diagnostic",
    ),
    CurrentPathRule(("mechanism_adaptation", "design_audit_report"), "generated_current"),
    CurrentPathRule(
        ("mechanism_adaptation", "semantics_audit_report"),
        "generated_current",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "diagnostic_relation_graph_report"),
        "generated_current",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "sample_size_audit_report"),
        "generated_current",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "preregistration_manifest"),
        "generated_current",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "release_qualification_report"),
        "release_attestation",
    ),
    CurrentPathRule(
        ("mechanism_adaptation", "participant_preregistration_candidate"),
        "protocol_input",
    ),
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
    _normalize_materialized_json_path(ROOT / node.path)


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


def _normalize_materialized_json_line_endings() -> None:
    """Make byte-level evidence hashes stable across Git's Windows checkout rules."""

    for node in NODES:
        if node.command is None:
            continue
        path = ROOT / node.path
        _normalize_materialized_json_path(path)


def _normalize_materialized_json_path(path: Path) -> None:
    if path.suffix.lower() != ".json" or not path.is_file():
        return
    payload = path.read_bytes()
    normalized = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if normalized != payload:
        path.write_bytes(normalized)


def _repository_source_sha256() -> str:
    """Fingerprint executable source independently from generated artifacts."""

    return repository_tree_sha256(
        ROOT,
        relative_roots=("scripts", "src/chemworld"),
    )


def _git_head() -> str:
    return git_source_commit(ROOT)


def _mechanism_structural_receipt_binding_current(
    receipt: Mapping[str, Any],
    *,
    stage: str,
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> bool:
    return bool(
        receipt.get("schema_version")
        == "chemworld-mechanism-metric-embargo-receipt-0.1"
        and receipt.get("stage") == stage
        and receipt.get("protocol_sha256") == _canonical_sha256(protocol)
        and receipt.get("gate_a_plan_sha256") == _canonical_sha256(plan)
        and receipt.get("structurally_complete") is True
        and receipt.get("observed_completed_trial_count")
        == receipt.get("expected_trial_count")
        and isinstance(receipt.get("expected_trial_count"), int)
        and receipt.get("expected_trial_count", 0) > 0
        and isinstance(receipt.get("trial_manifest_count"), int)
        and receipt.get("trial_manifest_count", 0) > 0
        and isinstance(receipt.get("trial_manifests_sha256"), str)
        and isinstance(receipt.get("source_report_sha256"), str)
        and receipt.get("metric_embargo") == "active"
        and receipt.get("scientific_metrics_disclosed") is False
    )


def _mechanism_public_decision_binding_current(
    decision: Mapping[str, Any],
    a2_receipt: Mapping[str, Any],
    a3_receipt: Mapping[str, Any],
    release_qualification: Mapping[str, Any],
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> bool:
    readiness = decision.get("readiness", {})
    go_no_go = decision.get("go_no_go", {})
    return bool(
        _mechanism_structural_receipt_binding_current(
            a2_receipt,
            stage="a2",
            protocol=protocol,
            plan=plan,
        )
        and _mechanism_structural_receipt_binding_current(
            a3_receipt,
            stage="a3",
            protocol=protocol,
            plan=plan,
        )
        and decision.get("schema_version")
        == "chemworld-mechanism-public-decision-0.1"
        and decision.get("a2_structural_receipt_sha256")
        == _canonical_sha256(a2_receipt)
        and decision.get("a3_structural_receipt_sha256")
        == _canonical_sha256(a3_receipt)
        and decision.get("gate_a_report_sha256")
        == a2_receipt.get("source_report_sha256")
        and decision.get("a3_report_sha256")
        == a3_receipt.get("source_report_sha256")
        and decision.get("release_qualification_sha256")
        == _canonical_sha256(release_qualification)
        and decision.get("metric_embargo")
        == "released_for_joint_a2_a3_decision"
        and decision.get("a1_pass") is True
        and decision.get("a2_pass") is True
        and decision.get("a3_pass") is True
        and decision.get("gate_a_pass") is True
        and isinstance(readiness, Mapping)
        and readiness.get("benchmark_ready") is True
        and readiness.get("evidence_complete") is False
        and readiness.get("publication_ready") is False
        and readiness.get("participant_performance_pass") is None
        and isinstance(go_no_go, Mapping)
        and go_no_go.get("branch") == "a2_a3_passed"
        and go_no_go.get("formal_gates_b_to_d") == "eligible"
        and go_no_go.get("gate_e") == "eligible"
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
    if node.node_id == "mechanism_diagnostic_relation_graph":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )
        from chemworld.eval.mechanism_relation_graph import (
            validate_diagnostic_relation_graph,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        if validate_diagnostic_relation_graph(protocol, plan, payload):
            return False
    if node.node_id == "mechanism_sample_size_audit":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        if (
            payload.get("pass") is not True
            or payload.get("protocol_sha256")
            != _canonical_sha256(protocol)
            or payload.get("gate_a_plan_sha256")
            != _canonical_sha256(plan)
        ):
            return False
    if node.node_id == "mechanism_preregistration":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )
        from chemworld.eval.mechanism_preregistration import (
            validate_mechanism_preregistration,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        relation_graph = json.loads(
            (
                ROOT
                / node_map()["mechanism_diagnostic_relation_graph"].path
            ).read_text(encoding="utf-8")
        )
        sample_size = json.loads(
            (
                ROOT / node_map()["mechanism_sample_size_audit"].path
            ).read_text(encoding="utf-8")
        )
        if validate_mechanism_preregistration(
            payload,
            repository_root=ROOT,
            protocol=protocol,
            plan=plan,
            relation_graph=relation_graph,
            sample_size_audit=sample_size,
        ):
            return False
    if node.node_id == "mechanism_confirmatory_task_semantics_audit":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        if (
            payload.get("pass") is not True
            or payload.get("protocol_sha256") != _canonical_sha256(protocol)
            or payload.get("gate_a_plan_sha256") != _canonical_sha256(plan)
        ):
            return False
    if node.node_id == "mechanism_release_qualification":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        if (
            payload.get("qualified") is not True
            or payload.get("formal_result") is not False
            or payload.get("formal_cohorts_consumed") is not False
            or payload.get("protocol_sha256") != _canonical_sha256(protocol)
            or payload.get("gate_a_plan_sha256") != _canonical_sha256(plan)
        ):
            return False
    if node.node_id in {
        "mechanism_a2_structural_receipt",
        "mechanism_a3_structural_receipt",
    }:
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        stage = (
            "a2"
            if node.node_id == "mechanism_a2_structural_receipt"
            else "a3"
        )
        if not _mechanism_structural_receipt_binding_current(
            payload,
            stage=stage,
            protocol=protocol,
            plan=plan,
        ):
            return False
    if node.node_id == "mechanism_public_gate_a_decision":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(
            ROOT / node_map()["mechanism_protocol"].path
        )
        plan = load_json_object(
            ROOT / node_map()["mechanism_gate_a_plan"].path
        )
        a2_receipt = load_json_object(
            ROOT / node_map()["mechanism_a2_structural_receipt"].path
        )
        a3_receipt = load_json_object(
            ROOT / node_map()["mechanism_a3_structural_receipt"].path
        )
        release_qualification = load_json_object(
            ROOT / node_map()["mechanism_release_qualification"].path
        )
        if not _mechanism_public_decision_binding_current(
            payload,
            a2_receipt,
            a3_receipt,
            release_qualification,
            protocol,
            plan,
        ):
            return False
    if node.node_id == "static_s0_formal_campaign_summary":
        freeze_manifest = load_json_object(
            ROOT / node_map()["static_s0_freeze_manifest"].path
        )
        execution = payload.get("execution", {})
        accounting = payload.get("accounting", {})
        if not (
            payload.get("schema_version")
            == "chemworld-static-s0-campaign-summary-1.0"
            and payload.get("status")
            == "completed_audited_formal_descriptive_result"
            and payload.get("formal_result") is True
            and payload.get("benchmark_claim_allowed") is False
            and payload.get("freeze", {}).get("manifest_sha256")
            == _canonical_sha256(freeze_manifest)
            and execution.get("participant", {}).get(
                "all_exact_replay_verified"
            )
            is True
            and execution.get("baselines", {}).get(
                "all_exact_replay_verified"
            )
            is True
            and accounting.get("campaign_total_physical_experiments") == 28060
            and set(payload.get("tasks", {}))
            == {"electrochemical", "crystallization"}
        ):
            return False
    if node.node_id == "static_s0_material_information_triarm_summary":
        nominal_manifest = load_json_object(
            ROOT / node_map()["static_s0_nominal_information_freeze_manifest"].path
        )
        misindexed_manifest = load_json_object(
            ROOT
            / node_map()["static_s0_misindexed_information_freeze_manifest"].path
        )
        execution = payload.get("execution", {})
        accounting = payload.get("accounting", {})
        tasks = payload.get("tasks", {})
        if not (
            payload.get("schema_version")
            == "chemworld-static-s0-material-information-triarm-result-1.0"
            and payload.get("status")
            == "completed_audited_formal_three_arm_result"
            and payload.get("formal_result") is True
            and payload.get("confirmatory_analysis_complete") is True
            and payload.get("benchmark_claim_allowed") is False
            and payload.get("freeze", {}).get("nominal_manifest_sha256")
            == _canonical_sha256(nominal_manifest)
            and payload.get("freeze", {}).get("misindexed_manifest_sha256")
            == _canonical_sha256(misindexed_manifest)
            and execution.get("world_seeds")
            == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            and execution.get("all_three_arms_completed") is True
            and execution.get("all_sixty_cells_exact_replay_verified") is True
            and accounting.get("three_arm_total", {}).get(
                "participant_world_cells"
            )
            == 60
            and accounting.get("three_arm_total", {}).get(
                "total_physical_experiments"
            )
            == 2280
            and accounting.get("three_arm_total", {}).get("provider_calls")
            == 1260
            and accounting.get("three_arm_total", {}).get("method_failures")
            == 0
            and set(tasks) == {"electrochemical", "crystallization"}
            and tasks.get("electrochemical", {})
            .get("paired_contrasts", {})
            .get("nominal_minus_opaque", {})
            .get("familywise_result")
            == "positive_information_value"
            and tasks.get("crystallization", {})
            .get("paired_contrasts", {})
            .get("nominal_minus_opaque", {})
            .get("familywise_result")
            == "inconclusive"
            and all(
                task.get("recovery", {})
                .get("overall_recovery_claim", {})
                .get("passed")
                is False
                for task in tasks.values()
            )
        ):
            return False
    if node.node_id == "static_s0_five_task_postqualification_summary":
        campaign_plan = load_json_object(
            ROOT / node_map()["static_s0_five_task_campaign_plan"].path
        )
        participant_method = load_json_object(
            ROOT / node_map()["static_s0_five_task_participant_method"].path
        )
        execution = payload.get("execution", {})
        accounting = payload.get("accounting", {})
        threshold_summary = payload.get("threshold_summary", {})
        if not (
            payload.get("schema_version")
            == "chemworld-static-s0-five-task-postqualification-summary-0.1"
            and payload.get("status") == "completed_audited_development_only"
            and payload.get("formal_result") is False
            and payload.get("benchmark_claim_allowed") is False
            and execution.get("campaign_plan_sha256")
            == _canonical_sha256(campaign_plan)
            and execution.get("all_cells_completed") is True
            and execution.get("all_exact_replay_verified") is True
            and execution.get("result_count") == 150
            and accounting.get("campaign_total_physical_experiments") == 3900
            and accounting.get("participant_provider_calls") == 526
            and payload.get("method", {}).get("participant_method_id")
            in participant_method.get("methods", {})
            and set(payload.get("tasks", {}))
            == {
                "electrochemical-conversion",
                "reaction-to-crystallization",
                "reaction-to-distillation",
                "partition-discovery",
                "flow-reaction-optimization",
            }
            and threshold_summary.get(
                "all_tasks_reached_threshold_by_any_method_mean"
            )
            is False
            and threshold_summary.get("failure_task") == "partition-discovery"
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
    if "gate_pass" in payload:
        return "passed" if payload.get("gate_pass") is True else "blocked"
    if node.node_id == "mechanism_public_gate_a_decision":
        return "passed" if payload.get("gate_a_pass") is True else "blocked"
    if node.node_id in {
        "mechanism_a2_structural_receipt",
        "mechanism_a3_structural_receipt",
    }:
        return (
            "passed"
            if payload.get("structurally_complete") is True
            else "blocked"
        )
    if node.node_id == "mechanism_design_audit":
        return "passed" if payload.get("pass") else "blocked"
    if node.node_id == "mechanism_release_qualification":
        return "passed" if payload.get("qualified") else "blocked"
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
    from chemworld.eval.mechanism_adaptation import (
        load_mechanism_adaptation_protocol,
    )

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
    mechanism_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_a2_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a2_structural_receipt"].path
        ).read_text(encoding="utf-8")
    )
    mechanism_a3_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a3_structural_receipt"].path
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
    mechanism_release_qualification = json.loads(
        (
            ROOT / node_map()["mechanism_release_qualification"].path
        ).read_text(encoding="utf-8")
    )
    mechanism_protocol = load_mechanism_adaptation_protocol(
        ROOT / node_map()["mechanism_protocol"].path
    )
    mechanism_plan = load_json_object(
        ROOT / node_map()["mechanism_gate_a_plan"].path
    )
    static_s0_summary_path = ROOT / node_map()["static_s0_formal_campaign_summary"].path
    static_s0_summary = load_json_object(static_s0_summary_path)
    static_s0_information_triarm = load_json_object(
        ROOT / node_map()["static_s0_material_information_triarm_summary"].path
    )
    static_s0_five_task = load_json_object(
        ROOT / node_map()["static_s0_five_task_postqualification_summary"].path
    )
    task_design_matrix = load_json_object(ROOT / node_map()["task_design_matrix"].path)
    mechanism_evidence_current = _mechanism_public_decision_binding_current(
        mechanism_decision,
        mechanism_a2_receipt,
        mechanism_a3_receipt,
        mechanism_release_qualification,
        mechanism_protocol,
        mechanism_plan,
    )
    mechanism_gate_a_pass = bool(
        mechanism_evidence_current
        and mechanism_decision.get("gate_a_pass") is True
    )
    controlled_gate_a_pass = bool(
        mechanism_evidence_current
        and mechanism_decision.get("a2_pass") is True
    )
    online_gate_a_pass = bool(
        mechanism_evidence_current
        and mechanism_decision.get("a3_pass") is True
    )
    mechanism_gate_a_status = (
        "gate_a_passed_remaining_gates_pending"
        if mechanism_gate_a_pass
        else "gate_a_invalidated_recertification_required"
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
            node.node_id == "mechanism_public_gate_a_decision"
            and not mechanism_evidence_current
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
    mechanism_gate_a_current = bool(
        mechanism_gate_a_pass
        and nodes["mechanism_public_gate_a_decision"]["artifact_state"] == "current"
    )

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
            if mechanism_gate_a_current
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
            "protocol": node_map()["mechanism_protocol"].path,
            "task_ids": list(mechanism_protocol["design"]["tasks"]),
            "status": (
                "gate_a_passed"
                if mechanism_gate_a_current
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
        "status": "static_s0_v1_formal_descriptive_results_complete_claim_bounded",
        "formal_results_present": True,
        "benchmark_claim_allowed": False,
        "environment_certificate_results_present": True,
        "environment_benchmark_readiness_claim_allowed": mechanism_gate_a_current,
        "interpretation": (
            "Legacy fixed-world static-S0 participant results were withdrawn. "
            "Replacement electrochemical and reaction-crystallization campaigns "
            "completed ten independent worlds, twenty exploration experiments per "
            "world, full classic baselines, and exact replay. Results are descriptive: "
            "electrochemical is positive against the best information-matched baseline "
            "but not stable against the best privileged calibration baseline; "
            "crystallization underperforms LHS. "
            "A separate five-task, five-world development comparison is complete "
            "and remains explicitly non-formal. "
            "RC28 Gate A remains a historical environment certificate with stale "
            "current-source binding; Participant Gates B-E remain unexecuted."
        ),
    }
    static_task_ids = [
        static_s0_summary["tasks"][task_key]["task_id"]
        for task_key in ("electrochemical", "crystallization")
    ]
    static_world_seeds = [
        int(row["world_seed"])
        for row in static_s0_summary["tasks"]["electrochemical"]["participant"][
            "worlds"
        ]
    ]
    current["static_scientific_optimization"] = {
        "summary": node_map()["static_s0_formal_campaign_summary"].path,
        "status": static_s0_summary["status"],
        "formal_result": True,
        "benchmark_claim_allowed": False,
        "task_ids": static_task_ids,
        "world_seeds": static_world_seeds,
        "exploration_experiments_per_seed": 20,
        "all_replay_verified": bool(
            static_s0_summary["execution"]["participant"][
                "all_exact_replay_verified"
            ]
            and static_s0_summary["execution"]["baselines"][
                "all_exact_replay_verified"
            ]
        ),
        "freeze_manifest": node_map()["static_s0_freeze_manifest"].path,
        "campaign_total_physical_experiments": int(
            static_s0_summary["accounting"][
                "campaign_total_physical_experiments"
            ]
        ),
        "comparison_scope": static_s0_summary["reporting_boundaries"][
            "all_algorithm_comparisons"
        ],
        "task_results": {
            task_key: {
                "participant_mean": static_s0_summary["tasks"][task_key][
                    "participant"
                ]["primary_score"]["mean"],
                "participant_world_bootstrap_95_interval": (
                    static_s0_summary["tasks"][task_key]["participant"][
                        "primary_score"
                    ]["world_bootstrap_95_interval"]
                ),
            }
            for task_key in ("electrochemical", "crystallization")
        },
        "hidden_world_change_evaluated": False,
    }
    current["static_s0_five_task_postqualification"] = {
        "summary": node_map()["static_s0_five_task_postqualification_summary"].path,
        "status": static_s0_five_task["status"],
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "task_ids": sorted(static_s0_five_task["tasks"]),
        "world_seeds": static_s0_five_task["execution"]["world_seeds"],
        "result_count": static_s0_five_task["execution"]["result_count"],
        "campaign_total_physical_experiments": static_s0_five_task["accounting"][
            "campaign_total_physical_experiments"
        ],
        "participant_provider_calls": static_s0_five_task["accounting"][
            "participant_provider_calls"
        ],
        "all_replay_verified": static_s0_five_task["execution"][
            "all_exact_replay_verified"
        ],
        "all_tasks_reached_threshold_by_any_method_mean": (
            static_s0_five_task["threshold_summary"][
                "all_tasks_reached_threshold_by_any_method_mean"
            ]
        ),
        "threshold_failure_task": static_s0_five_task["threshold_summary"][
            "failure_task"
        ],
        "participant_mean_by_task": {
            task_id: task["participant_mean"]
            for task_id, task in static_s0_five_task["tasks"].items()
        },
        "interpretation": (
            "Completed audited development comparison. It extends comparative "
            "coverage to five tasks but does not promote the results to formal "
            "benchmark evidence or a broad provider ranking."
        ),
    }
    current.pop("static_material_information_interim", None)
    current["static_material_information_three_arm"] = {
        "summary": node_map()[
            "static_s0_material_information_triarm_summary"
        ].path,
        "nominal_freeze_manifest": node_map()[
            "static_s0_nominal_information_freeze_manifest"
        ].path,
        "misindexed_freeze_manifest": node_map()[
            "static_s0_misindexed_information_freeze_manifest"
        ].path,
        "status": static_s0_information_triarm["status"],
        "formal_result": True,
        "confirmatory_analysis_complete": True,
        "benchmark_claim_allowed": False,
        "world_seeds": static_s0_information_triarm["execution"]["world_seeds"],
        "all_sixty_cells_exact_replay_verified": (
            static_s0_information_triarm["execution"][
                "all_sixty_cells_exact_replay_verified"
            ]
        ),
        "total_physical_experiments": static_s0_information_triarm["accounting"][
            "three_arm_total"
        ]["total_physical_experiments"],
        "provider_calls": static_s0_information_triarm["accounting"][
            "three_arm_total"
        ]["provider_calls"],
        "provider_retry_attempts": static_s0_information_triarm["accounting"][
            "three_arm_total"
        ]["provider_retry_attempts"],
        "task_results": {
            task_key: {
                "score_mean_by_arm": {
                    arm: static_s0_information_triarm["tasks"][task_key][
                        "primary_score_by_arm"
                    ][arm]["mean"]
                    for arm in ("opaque", "nominal", "misindexed")
                },
                "nominal_minus_opaque": (
                    static_s0_information_triarm["tasks"][task_key][
                        "paired_contrasts"
                    ]["nominal_minus_opaque"]
                ),
                "misindexed_minus_nominal": (
                    static_s0_information_triarm["tasks"][task_key][
                        "paired_contrasts"
                    ]["misindexed_minus_nominal"]
                ),
                "overall_recovery_claim": static_s0_information_triarm["tasks"][
                    task_key
                ]["recovery"]["overall_recovery_claim"],
            }
            for task_key in ("electrochemical", "crystallization")
        },
        "interpretation": (
            "Correct anonymous nominal properties have positive confirmatory "
            "information value for electrochemistry and an inconclusive effect for "
            "crystallization. The fixed targeted wrong prior changes behavior in "
            "both tasks, but neither task satisfies the preregistered overall "
            "recovery claim."
        ),
    }
    task_design_validation = task_design_matrix["design_validation"]
    current["task_design"] = {
        "matrix": node_map()["task_design_matrix"].path,
        "status": task_design_validation["status"],
        "registered_task_count": int(task_design_matrix["task_count"]),
        "executable_midpoint_task_count": int(
            task_design_validation["executable_midpoint_task_count"]
        ),
        "executable_boundary_task_count": int(
            task_design_validation["executable_boundary_task_count"]
        ),
        "boundary_recipe_case_count": int(
            task_design_validation["boundary_recipe_case_count"]
        ),
        "declared_success_metric_count": int(
            task_design_validation["declared_success_metric_count"]
        ),
        "bound_success_metric_count": int(
            task_design_validation["bound_success_metric_count"]
        ),
        "dead_recipe_coordinate_count": int(
            task_design_validation["dead_recipe_coordinate_count"]
        ),
        "formalization_blocker_count": int(
            task_design_validation["formalization_blocker_count"]
        ),
        "formal_experiment_task_ids": list(
            task_design_validation["formal_experiment_task_ids"]
        ),
        "formal_empirical_comparison_pending_task_ids": list(
            task_design_validation[
                "formal_empirical_comparison_pending_task_ids"
            ]
        ),
        "nonconfirmatory_formal_experiments_required_for_future_claims": bool(
            task_design_validation[
                "nonconfirmatory_formal_experiments_required_for_future_claims"
            ]
        ),
    }
    mechanism_state_machine = dict(mechanism_protocol["protocol_state_machine"])
    mechanism_state_machine.update(
        {
            "a2_controlled_identifiability": (
                "passed"
                if mechanism_gate_a_current and controlled_gate_a_pass
                else "historical_pass_current_binding_stale"
                if controlled_gate_a_pass
                else "invalidated"
            ),
            "a3_online_attainability": (
                "passed"
                if mechanism_gate_a_current and online_gate_a_pass
                else "historical_pass_current_binding_stale"
                if online_gate_a_pass
                else "invalidated"
            ),
            "participant_agent_gates_b_to_e": "pending_method_freeze",
            "publication_ready": False,
            "private_environment_confirmation": "eligible_not_executed",
            "private_agent_confirmation": "sealed_pending_participant_freeze",
            "benchmark_ready": mechanism_gate_a_current,
            "evidence_complete": False,
        }
    )
    public_tables = mechanism_decision["public_scientific_tables"]
    a2_public = public_tables["a2_controlled_identifiability"]
    a3_public = public_tables["a3_online_attainability"]
    primary_budget = str(a2_public["primary_gate_budget"])
    a2_active_primary = a2_public["active_oracle"]["by_budget"][
        primary_budget
    ]
    a2_decoder_primary = a2_public["fixed_trajectory_decoder"][
        "by_budget"
    ][primary_budget]
    a3_primary = a3_public["online_capability_chain_certificate"]
    a3_detection = a3_primary["change_detection_conditional_on_reference"]

    current["mechanism_adaptation"] = {
        "protocol": node_map()["mechanism_protocol"].path,
        "preflight_report": node_map()["mechanism_preflight"].path,
        "design_audit_report": node_map()["mechanism_design_audit"].path,
        "design_audit_pass": bool(
            mechanism_design.get("pass")
            and nodes["mechanism_design_audit"]["artifact_state"] == "current"
        ),
        "semantics_audit_report": node_map()[
            "mechanism_confirmatory_task_semantics_audit"
        ].path,
        "semantics_audit_pass": bool(
            nodes["mechanism_confirmatory_task_semantics_audit"]["gate_state"]
            == "passed"
        ),
        "diagnostic_relation_graph_report": node_map()[
            "mechanism_diagnostic_relation_graph"
        ].path,
        "sample_size_audit_report": node_map()[
            "mechanism_sample_size_audit"
        ].path,
        "preregistration_manifest": node_map()[
            "mechanism_preregistration"
        ].path,
        "release_qualification_report": node_map()[
            "mechanism_release_qualification"
        ].path,
        "release_qualification_pass": bool(
            mechanism_release_qualification.get("qualified") is True
            and nodes["mechanism_release_qualification"]["artifact_state"]
            == "current"
        ),
        "participant_preregistration_candidate": node_map()[
            "mechanism_participant_preregistration_candidate"
        ].path,
        "gate_a_plan": node_map()["mechanism_gate_a_plan"].path,
        "a2_structural_receipt": node_map()[
            "mechanism_a2_structural_receipt"
        ].path,
        "a3_structural_receipt": node_map()[
            "mechanism_a3_structural_receipt"
        ].path,
        "public_decision_report": node_map()[
            "mechanism_public_gate_a_decision"
        ].path,
        "agent_pilot_report": node_map()["mechanism_agent_pilot"].path,
        "protocol_state_machine": mechanism_state_machine,
        "status": (
            mechanism_gate_a_status
            if mechanism_gate_a_current
            else "historical_gate_a_pass_current_binding_stale"
        ),
        "gate_a_pass": mechanism_gate_a_pass,
        "gate_a_evidence_current": bool(
            mechanism_evidence_current
            and nodes["mechanism_public_gate_a_decision"]["artifact_state"]
            == "current"
        ),
        "gate_a_certificate_status": {
            "a1_physical_intervention_validity": (
                "passed"
                if mechanism_design.get("pass") is True
                else "failed"
            ),
            "a2_controlled_matched_identifiability": (
                "passed"
                if mechanism_gate_a_current and controlled_gate_a_pass
                else "historical_pass_current_binding_stale"
                if controlled_gate_a_pass
                else "invalidated"
            ),
            "a3_online_attainability": (
                "passed"
                if mechanism_gate_a_current and online_gate_a_pass
                else "historical_pass_current_binding_stale"
                if online_gate_a_pass
                else "invalidated"
            ),
        },
        "formal_gate_a_result": {
            "decision_sha256": mechanism_decision["decision_sha256"],
            "go_no_go_branch": mechanism_decision["go_no_go"]["branch"],
            "a2": {
                "completed_trials": mechanism_a2_receipt[
                    "observed_completed_trial_count"
                ],
                "primary_budget": int(primary_budget),
                "active_oracle_top1_accuracy": a2_active_primary[
                    "top1_accuracy"
                ],
                "fixed_decoder_top1_accuracy": a2_decoder_primary[
                    "top1_accuracy"
                ],
            },
            "a3": {
                "completed_trials": mechanism_a3_receipt[
                    "observed_completed_trial_count"
                ],
                "reference_sufficient_rate": a3_primary[
                    "p_reference_sufficient"
                ],
                "change_detection_sensitivity": a3_detection[
                    "sensitivity"
                ],
                "change_detection_auroc": a3_detection["auroc"],
                "no_change_false_positive_rate": a3_detection[
                    "false_positive_rate"
                ],
                "integrated_mean_brier": a3_primary[
                    "integrated_mean_change_probability_brier_score"
                ],
                "conditional_attribution": a3_primary[
                    "p_attribution_given_detection_and_reference"
                ],
                "end_to_end_success": a3_primary[
                    "p_end_to_end_reference_detection_attribution_success"
                ],
            },
        },
        "new_external_provider_runs_completed": False,
        "agent_pilot_gate_status": {
            gate: mechanism_pilot[gate]["status"]
            for gate in ("gate_0", "gate_b", "gate_c", "gate_d", "gate_e")
        },
        "agent_pilot_evidence_current": False,
        "agent_pilot_protocol_version": "historical_v0.2.1",
        "agent_weight_updates_performed": False,
        "benchmark_ready": mechanism_gate_a_current,
        "evidence_complete": False,
        "publication_ready": False,
    }
    current.pop("development_evidence", None)
    current.pop("history_policy", None)
    current["publication"] = {
        "status": "working_manuscript_not_submission_ready",
        "manuscript": "paper/chemworld_benchmark_manuscript.md",
        "claim_evidence_ledger": node_map()[
            "pre_arxiv_claim_evidence_ledger"
        ].path,
        "scope": "narrow_two_task_fixed_world_descriptive_benchmark",
        "new_scientific_experiments_required_for_narrow_scope": False,
        "stronger_claim_experiments_pending": True,
        "publication_ready": False,
    }
    blockers: list[dict[str, Any]] = []
    if backend["clean_release_attestation"] != "passed":
        blockers.append({"id": "clean_release_attestation_pending", "scope": "backend_release"})
    remaining_mechanism_gates = ["gate_b", "gate_c", "gate_d", "gate_e"]
    if not mechanism_gate_a_current:
        remaining_mechanism_gates.insert(0, "gate_a")
    blockers.append(
        {
            "id": "mechanism_gates_remaining",
            "scope": "mechanism_benchmark",
            "gates": remaining_mechanism_gates,
        }
    )
    stale_binding_ids = sorted(
        node_id for node_id, node in nodes.items() if node["artifact_state"] == "stale"
    )
    if stale_binding_ids:
        blockers.append(
            {
                "id": "stale_evidence_bindings",
                "scope": "evidence_registry",
                "artifact_ids": stale_binding_ids,
            }
        )
    current["repository_integrity"] = {
        "status": (
            "stale_evidence_bindings_worktree_dirty"
            if stale_binding_ids and dirty
            else "stale_evidence_bindings"
            if stale_binding_ids
            else "current_evidence_coherent_worktree_dirty"
            if dirty
            else "current_evidence_coherent_worktree_clean"
        ),
        "current_evidence_coherent": not stale_binding_ids,
        "tracked_source_tree_dirty": dirty,
        "stale_binding_count": len(stale_binding_ids),
        "stale_binding_ids": stale_binding_ids,
        "blockers": blockers,
    }
    write_json_atomic(CURRENT_REGISTRY, current, sort_keys=False)


def refresh() -> None:
    source_commit = _git_head()
    source_tree_dirty = _git_tree_dirty()
    fresh_nodes: dict[str, bool] = {}
    for node in generation_order():
        dependency_fresh = all(
            fresh_nodes[dependency] for dependency in node.dependencies
        )
        if dependency_fresh:
            _run(
                node,
                source_commit=source_commit,
                source_tree_dirty=source_tree_dirty,
            )
        path = ROOT / node.path
        payload = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.suffix == ".json" and path.is_file()
            else {}
        )
        fresh_nodes[node.node_id] = bool(
            dependency_fresh
            and path.is_file()
            and _artifact_source_binding_current(node, payload)
        )
    _normalize_materialized_json_line_endings()
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
    from chemworld.eval.mechanism_adaptation import (
        load_mechanism_adaptation_protocol,
    )

    binding_protocol = load_mechanism_adaptation_protocol(
        ROOT / node_map()["mechanism_protocol"].path
    )
    binding_plan = load_json_object(
        ROOT / node_map()["mechanism_gate_a_plan"].path
    )
    binding_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(
            encoding="utf-8"
        )
    )
    binding_a2_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a2_structural_receipt"].path
        ).read_text(encoding="utf-8")
    )
    binding_a3_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a3_structural_receipt"].path
        ).read_text(encoding="utf-8")
    )
    binding_release_qualification = json.loads(
        (
            ROOT / node_map()["mechanism_release_qualification"].path
        ).read_text(encoding="utf-8")
    )
    gate_a_binding_current = _mechanism_public_decision_binding_current(
        binding_decision,
        binding_a2_receipt,
        binding_a3_receipt,
        binding_release_qualification,
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
            node.node_id == "mechanism_public_gate_a_decision"
            and not gate_a_binding_current
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

    mechanism_protocol = load_mechanism_adaptation_protocol(
        ROOT / node_map()["mechanism_protocol"].path
    )
    mechanism_plan = load_json_object(
        ROOT / node_map()["mechanism_gate_a_plan"].path
    )
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_a2_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a2_structural_receipt"].path
        ).read_text(encoding="utf-8")
    )
    mechanism_a3_receipt = json.loads(
        (
            ROOT / node_map()["mechanism_a3_structural_receipt"].path
        ).read_text(encoding="utf-8")
    )
    mechanism_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(
            encoding="utf-8"
        )
    )
    mechanism_release_qualification = json.loads(
        (
            ROOT / node_map()["mechanism_release_qualification"].path
        ).read_text(encoding="utf-8")
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
    if not _mechanism_structural_receipt_binding_current(
        mechanism_a2_receipt,
        stage="a2",
        protocol=mechanism_protocol,
        plan=mechanism_plan,
    ):
        errors.append("mechanism A2 structural receipt binding is stale")
    if not _mechanism_structural_receipt_binding_current(
        mechanism_a3_receipt,
        stage="a3",
        protocol=mechanism_protocol,
        plan=mechanism_plan,
    ):
        errors.append("mechanism A3 structural receipt binding is stale")
    if not _mechanism_public_decision_binding_current(
        mechanism_decision,
        mechanism_a2_receipt,
        mechanism_a3_receipt,
        mechanism_release_qualification,
        mechanism_protocol,
        mechanism_plan,
    ):
        errors.append("mechanism public Gate A decision binding is stale")
    if not gate_a_binding_current:
        gate_node = recorded_nodes.get("mechanism_public_gate_a_decision", {})
        if gate_node.get("gate_state") != "invalidated":
            errors.append("stale mechanism Gate A is not marked invalidated")
    if mechanism_decision.get("readiness", {}).get("publication_ready") is not False:
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
    expected_gate_a_pass = bool(
        gate_a_binding_current
        and mechanism_decision.get("gate_a_pass") is True
    )
    expected_gate_a_current = bool(
        expected_gate_a_pass
        and recorded_nodes.get("mechanism_public_gate_a_decision", {}).get(
            "artifact_state"
        )
        == "current"
    )
    if runtime.get("contract_validation") != expected_backend_validation:
        errors.append("current registry backend validation state is inconsistent")
    if (
        formal.get("status")
        != "static_s0_v1_formal_descriptive_results_complete_claim_bounded"
    ):
        errors.append("current registry formal evaluation boundary is inconsistent")
    if formal.get("formal_results_present") is not True:
        errors.append("current registry omits completed static-S0 formal results")
    if formal.get("benchmark_claim_allowed") is not False:
        errors.append("current registry improperly enables participant benchmark claims")
    if formal.get("environment_certificate_results_present") is not True:
        errors.append("current registry omits formal environment certificate results")
    if (
        formal.get("environment_benchmark_readiness_claim_allowed")
        is not expected_gate_a_current
    ):
        errors.append("current registry environment readiness state is inconsistent")
    static_s0 = current.get("static_scientific_optimization", {})
    if static_s0.get("formal_result") is not True:
        errors.append("current registry omits replacement static-S0 evidence")
    if static_s0.get("benchmark_claim_allowed") is not False:
        errors.append("current registry improperly enables a broad static-S0 benchmark claim")
    if static_s0.get("all_replay_verified") is not True:
        errors.append("current registry omits replacement formal replay")
    if static_s0.get("hidden_world_change_evaluated") is not False:
        errors.append("current registry conflates static S0 with hidden world changes")
    five_task = current.get("static_s0_five_task_postqualification", {})
    if five_task.get("formal_result") is not False:
        errors.append("current registry promotes five-task development evidence")
    if five_task.get("benchmark_claim_allowed") is not False:
        errors.append("current registry enables a five-task benchmark claim")
    if five_task.get("all_replay_verified") is not True:
        errors.append("current registry omits five-task exact replay")
    if five_task.get("result_count") != 150:
        errors.append("current registry has inconsistent five-task result count")
    if five_task.get("threshold_failure_task") != "partition-discovery":
        errors.append("current registry hides the five-task threshold failure")
    information_triarm = current.get("static_material_information_three_arm", {})
    if information_triarm.get("formal_result") is not True:
        errors.append("current registry omits the formal three-arm information study")
    if information_triarm.get("confirmatory_analysis_complete") is not True:
        errors.append("current registry marks the three-arm information study incomplete")
    if (
        information_triarm.get("all_sixty_cells_exact_replay_verified")
        is not True
    ):
        errors.append("current registry omits three-arm information replay")
    if information_triarm.get("world_seeds") != list(range(10)):
        errors.append("current registry has inconsistent three-arm world seeds")
    task_results = information_triarm.get("task_results", {})
    if (
        task_results.get("electrochemical", {})
        .get("nominal_minus_opaque", {})
        .get("familywise_result")
        != "positive_information_value"
    ):
        errors.append("current registry hides electrochemical information value")
    if any(
        task_results.get(task_key, {})
        .get("overall_recovery_claim", {})
        .get("passed")
        is not False
        for task_key in ("electrochemical", "crystallization")
    ):
        errors.append("current registry overclaims wrong-prior recovery")
    task_design = current.get("task_design", {})
    if (
        task_design.get("status")
        != "all_registered_task_designs_executable_and_metric_bound"
    ):
        errors.append("current registry task-design status is inconsistent")
    if task_design.get("registered_task_count") != 15:
        errors.append("current registry task-design count is inconsistent")
    if task_design.get("executable_midpoint_task_count") != 15:
        errors.append("current registry omits executable task designs")
    if task_design.get("executable_boundary_task_count") != 15:
        errors.append("current registry omits task boundary execution")
    if task_design.get("boundary_recipe_case_count") != 415:
        errors.append("current registry task boundary case count is inconsistent")
    if task_design.get("declared_success_metric_count") != 62:
        errors.append("current registry declared metric count is inconsistent")
    if task_design.get("bound_success_metric_count") != 62:
        errors.append("current registry omits metric endpoint bindings")
    if task_design.get("dead_recipe_coordinate_count") != 0:
        errors.append("current registry records dead task-recipe coordinates")
    if task_design.get("formalization_blocker_count") != 0:
        errors.append("current registry records unresolved task-design blockers")
    if task_design.get("formal_experiment_task_ids") != [
        "electrochemical-conversion",
        "reaction-to-crystallization",
    ]:
        errors.append("current registry task-design empirical scope is inconsistent")
    if (
        task_design.get(
            "nonconfirmatory_formal_experiments_required_for_future_claims"
        )
        is not True
    ):
        errors.append("current registry hides pending nonconfirmatory experiments")
    if len(task_design.get("formal_empirical_comparison_pending_task_ids", [])) != 13:
        errors.append("current registry task-design empirical backlog is inconsistent")
    mechanism_registry = current.get("mechanism_adaptation", {})
    if mechanism_registry.get("gate_a_pass") != expected_gate_a_pass:
        errors.append("current registry mechanism Gate A state is inconsistent")
    if mechanism_registry.get("gate_a_evidence_current") != expected_gate_a_current:
        errors.append("current registry mechanism Gate A freshness is inconsistent")
    if mechanism_registry.get("benchmark_ready") != expected_gate_a_current:
        errors.append("current registry mechanism benchmark readiness is inconsistent")
    if publication.get("status") != "working_manuscript_not_submission_ready":
        errors.append("current registry manuscript state is inconsistent")
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
