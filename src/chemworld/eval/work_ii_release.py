"""Pre-run evidence graph and clean-release receipt contracts for Work II."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
)
from chemworld.eval.work_ii_ae_formal_cohort import (
    qualification_tested_commit,
    validate_formal_ae_qualification,
)
from chemworld.eval.work_ii_cost import (
    build_formal_cost_contract,
    validate_formal_cost_contract,
)
from chemworld.eval.work_ii_formal import validate_formal_bindings
from chemworld.eval.work_ii_preregistration import (
    validate_preregistration_readiness,
    validate_submission_route_decision,
)
from chemworld.eval.work_ii_qualification import (
    qualification_receipt_sha256,
    validate_method_qualification_readiness,
    validate_method_qualification_receipt,
)

PRERUN_EVIDENCE_GRAPH_VERSION = "chemworld-work-ii-prerun-evidence-graph-0.1"
CLEAN_RELEASE_RECEIPT_VERSION = "chemworld-work-ii-clean-release-receipt-0.1"
# Keep the clean-release receipt tied to one exact, reviewable Work II test roster.
WORK_II_RELEASE_TEST_FILES = (
    "tests/test_work_ii_ae_formal_cohort.py",
    "tests/test_work_ii_ae_prior_qualification_v02.py",
    "tests/test_work_ii_analysis.py",
    "tests/test_work_ii_analysis_plan_audit.py",
    "tests/test_work_ii_blind_evaluator.py",
    "tests/test_work_ii_campaign_runner.py",
    "tests/test_work_ii_catalyst_deactivation_q0.py",
    "tests/test_work_ii_c2_admission.py",
    "tests/test_work_ii_c2_task_admission.py",
    "tests/test_work_ii_confirmatory.py",
    "tests/test_work_ii_constitutive_structural_qualification.py",
    "tests/test_work_ii_cost.py",
    "tests/test_work_ii_development_confirmation.py",
    "tests/test_work_ii_distillation_additional_rollback_q0.py",
    "tests/test_work_ii_crystallization_reversible_q0.py",
    "tests/test_work_ii_formal_design.py",
    "tests/test_work_ii_formal_evaluators.py",
    "tests/test_work_ii_formal_runner.py",
    "tests/test_work_ii_law_summary.py",
    "tests/test_work_ii_partition_constitutive_q0.py",
    "tests/test_work_ii_preregistration.py",
    "tests/test_work_ii_private.py",
    "tests/test_work_ii_private_execution.py",
    "tests/test_work_ii_process_profile.py",
    "tests/test_work_ii_public_c2.py",
    "tests/test_work_ii_qualification.py",
    "tests/test_work_ii_resource_calibration.py",
    "tests/test_work_ii_release.py",
    "tests/test_work_ii_report.py",
    "tests/test_work_ii_static_topology_q0.py",
    "tests/test_work_ii_truth.py",
)
PREREGISTRATION_FREEZE_RECEIPT_VERSION = (
    "chemworld-work-ii-preregistration-freeze-receipt-0.1"
)

_DEFAULT_PATHS = {
    "current_registry": "configs/current.json",
    "formal_design": "configs/benchmark/work_ii_formal_design_v0.2.json",
    "analysis_plan": "configs/benchmark/work_ii_analysis_plan_v0.2.json",
    "formal_design_audit": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-formal-world-prior-design-audit-v0.2.json"
    ),
    "power_resource_audit": (
        "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"
    ),
    "formal_preflight": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-formal-matrix-runner-preflight-v0.2.json"
    ),
    "method_qualification_readiness": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-method-qualification-readiness-v0.1.json"
    ),
    "submission_route_decision": (
        "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
    ),
    "preregistration_readiness": (
        "workstreams/flagship_tasks/reports/work-ii-preregistration-readiness-v0.2.json"
    ),
    "preregistration_draft": (
        "workstreams/flagship_tasks/reports/work-ii-preregistration-draft-v0.2.md"
    ),
}
_READINESS_VERSION_BY_FORMAL_PATHS = {
    (
        "configs/benchmark/work_ii_formal_design_v0.1.json",
        "configs/benchmark/work_ii_analysis_plan_v0.1.json",
    ): "v0.1",
    (
        "configs/benchmark/work_ii_formal_design_v0.2.json",
        "configs/benchmark/work_ii_analysis_plan_v0.2.json",
    ): "v0.2",
}


def _readiness_version(manifest: Mapping[str, Any]) -> str:
    design_binding = manifest.get("design_binding")
    design_binding = design_binding if isinstance(design_binding, Mapping) else {}
    analysis_binding = manifest.get("analysis_binding")
    analysis_binding = (
        analysis_binding if isinstance(analysis_binding, Mapping) else {}
    )
    formal_paths = (
        str(design_binding.get("path")),
        str(analysis_binding.get("path")),
    )
    try:
        return _READINESS_VERSION_BY_FORMAL_PATHS[formal_paths]
    except KeyError as error:
        raise ValueError(
            "unsupported formal design/analysis path pairing for "
            "preregistration readiness"
        ) from error

_CURRENT_EDGE_SPECS = (
    ("current_registry", "gate_a_public_decision", "resolves_current_gate_a"),
    ("gate_a_public_decision", "formal_design", "qualifies_environment_for"),
    ("formal_design", "formal_design_audit", "audited_by"),
    ("formal_design", "analysis_plan", "analyzed_by"),
    ("formal_design", "power_resource_audit", "resources_audited_by"),
    ("analysis_plan", "power_resource_audit", "power_audited_by"),
    ("formal_design", "formal_preflight", "materialized_by"),
    ("analysis_plan", "formal_preflight", "materialized_by"),
    ("formal_preflight", "method_qualification_readiness", "bounds_qualification"),
    ("submission_route_decision", "preregistration_readiness", "selects_route_for"),
    ("formal_design_audit", "preregistration_readiness", "supports"),
    ("power_resource_audit", "preregistration_readiness", "supports"),
    ("formal_preflight", "preregistration_readiness", "supports"),
    ("method_qualification_readiness", "preregistration_readiness", "blocks_until_passed"),
    ("preregistration_readiness", "preregistration_draft", "renders"),
)
_LEGACY_EDGE_SPECS = (
    *_CURRENT_EDGE_SPECS[:8],
    ("blind_evaluator_shakedown", "formal_preflight", "qualifies_evaluator_contract"),
    ("held_out_evaluator_shakedown", "formal_preflight", "qualifies_evaluator_contract"),
    *_CURRENT_EDGE_SPECS[8:],
)
_CURRENT_NODE_IDS = frozenset(
    {
        "current_registry",
        "gate_a_public_decision",
        "formal_design",
        "analysis_plan",
        "formal_design_audit",
        "power_resource_audit",
        "formal_preflight",
        "method_qualification_readiness",
        "submission_route_decision",
        "preregistration_readiness",
        "preregistration_draft",
    }
)
_LEGACY_NODE_IDS = _CURRENT_NODE_IDS | {
    "blind_evaluator_shakedown",
    "held_out_evaluator_shakedown",
}
_LEGACY_GRAPH_PATH = Path(
    "workstreams/flagship_tasks/reports/work-ii-prerun-evidence-graph-v0.1.json"
)

_CLEAN_RELEASE_MATERIAL_PATHS = (
    "configs",
    "pyproject.toml",
    "scripts",
    "src/chemworld",
    "tests",
    "uv.lock",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _relative(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: value for key, value in payload.items() if key != field})


def prerun_evidence_graph_sha256(graph: Mapping[str, Any]) -> str:
    return _self_hash(graph, "graph_sha256")


def clean_release_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def preregistration_freeze_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def _json_node(
    root: Path,
    node_id: str,
    path: Path,
    *,
    evidence_role: str,
    status: str,
) -> dict[str, Any]:
    value = _load_object(path)
    return {
        "id": node_id,
        "path": _relative(root, path),
        "media_type": "application/json",
        "file_sha256": file_sha256(path),
        "schema_version": value.get("schema_version"),
        "status": status,
        "evidence_role": evidence_role,
        "formal_participant_result": False,
    }


def _text_node(
    root: Path,
    node_id: str,
    path: Path,
    *,
    evidence_role: str,
    status: str,
) -> dict[str, Any]:
    return {
        "id": node_id,
        "path": _relative(root, path),
        "media_type": "text/markdown",
        "file_sha256": file_sha256(path),
        "schema_version": None,
        "status": status,
        "evidence_role": evidence_role,
        "formal_participant_result": False,
    }


def build_prerun_evidence_graph(
    root: Path, *, artifact_version: str = "v0.2"
) -> dict[str, Any]:
    """Build the outcome-blind DAG used by the Work II preregistration release audit."""

    root = root.resolve()
    if artifact_version not in {"v0.1", "v0.2"}:
        raise ValueError("Work II pre-run artifact version must be v0.1 or v0.2")
    if artifact_version == "v0.1":
        # v0.1 is immutable historical release evidence. Rebuilding it from the
        # current source would turn every later cleanup into a hash-refresh gate.
        return _load_object(root / _LEGACY_GRAPH_PATH)
    relative_paths = dict(_DEFAULT_PATHS)
    paths = {key: root / value for key, value in relative_paths.items()}
    current = _load_object(paths["current_registry"])
    mechanism = current.get("mechanism_adaptation")
    mechanism = mechanism if isinstance(mechanism, Mapping) else {}
    gate_path_value = mechanism.get("public_decision_report")
    gate_path = root / str(gate_path_value)

    gate = _load_object(gate_path)
    design = _load_object(paths["formal_design"])
    analysis = _load_object(paths["analysis_plan"])
    design_audit = _load_object(paths["formal_design_audit"])
    power_audit = _load_object(paths["power_resource_audit"])
    preflight = _load_object(paths["formal_preflight"])
    qualification = _load_object(paths["method_qualification_readiness"])
    route = _load_object(paths["submission_route_decision"])
    preregistration = _load_object(paths["preregistration_readiness"])
    draft = paths["preregistration_draft"].read_text(encoding="utf-8")

    failures = [
        *validate_formal_bindings(root, preflight),
        *validate_method_qualification_readiness(qualification),
        *validate_submission_route_decision(route),
        *validate_preregistration_readiness(preregistration),
    ]
    if current.get("schema_version") != "chemworld-current-surface-registry-0.4":
        failures.append("current artifact registry schema is unexpected")
    if (
        mechanism.get("status") != "gate_a_passed_remaining_gates_pending"
        or mechanism.get("gate_a_pass") is not True
        or mechanism.get("gate_a_evidence_current") is not True
    ):
        failures.append("current registry does not bind a current passed Gate A")
    if gate_path_value != (
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-public-decision-v0.1-rc29.json"
    ):
        failures.append("current registry resolves an unexpected Gate A decision")
    formal_gate = mechanism.get("formal_gate_a_result")
    formal_gate = formal_gate if isinstance(formal_gate, Mapping) else {}
    go_no_go = gate.get("go_no_go")
    go_no_go = go_no_go if isinstance(go_no_go, Mapping) else {}
    if (
        gate.get("schema_version") != "chemworld-mechanism-public-decision-0.1"
        or gate.get("gate_a_pass") is not True
        or go_no_go.get("branch") != "a2_a3_passed"
        or gate.get("decision_sha256") != formal_gate.get("decision_sha256")
    ):
        failures.append("current Gate A decision is invalid or registry-stale")
    if (
        power_audit.get("status") != "passed"
        or power_audit.get("formal_result") is not False
    ):
        failures.append("power/resource audit has not passed its non-formal boundary")
    qualification_container = design_audit.get("prior_distinguishability_qualification")
    qualification_container = (
        qualification_container if isinstance(qualification_container, Mapping) else {}
    )
    design_audit_legal = (
        design_audit.get("failures") == []
        and (
            design_audit.get("status") == "passed"
            or (
                design_audit.get("status")
                == "pending_provider_free_prior_distinguishability_qualification"
                and qualification_container.get("status")
                == "pending_provider_free_qualification_execution"
                and qualification_container.get("formal_execution_gate_satisfied") is False
                and qualification_container.get("static_contract_ready") is True
            )
        )
    )
    if not design_audit_legal or design_audit.get("formal_result") is not False:
        failures.append("formal-design audit is not a legal passed-or-pending state")
    if design_audit.get("failures") != [] or power_audit.get("failures") != []:
        failures.append("a prerequisite audit contains failures")
    if design_audit.get("design_sha256") != canonical_json_sha256(design):
        failures.append("formal-design audit does not bind the current design")
    if design_audit.get("audit_sha256") != _self_hash(
        design_audit, "audit_sha256"
    ):
        failures.append("formal-design audit self-hash mismatch")
    qualification_binding = qualification_container.get("qualification_report")
    qualification_binding = (
        qualification_binding if isinstance(qualification_binding, Mapping) else {}
    )
    qualification_relative = qualification_binding.get("path")
    qualification_pending = (
        qualification_container.get("status")
        == "pending_provider_free_qualification_execution"
        and qualification_container.get("formal_execution_gate_satisfied") is False
    )
    if not isinstance(qualification_relative, str) or not qualification_relative:
        if not qualification_pending:
            failures.append(
                "formal-design audit lacks its required A-E qualification evidence binding"
            )
    else:
        qualification_path = (root / qualification_relative).resolve()
        try:
            qualification_path.relative_to(root)
        except ValueError:
            failures.append("A-E qualification evidence binding escapes repository")
        else:
            if not qualification_path.is_file():
                failures.append("bound A-E qualification evidence is missing")
            else:
                qualification_report = _load_object(qualification_path)
                qualification_errors = validate_formal_ae_qualification(
                    root, qualification_path, design
                )
                failures.extend(
                    "A-E qualification: " + error for error in qualification_errors
                )
                if (
                    qualification_binding.get("file_sha256")
                    != file_sha256(qualification_path)
                    or qualification_binding.get("report_sha256")
                    != qualification_report.get("report_sha256")
                    or qualification_binding.get("tested_commit")
                    != qualification_tested_commit(qualification_report)
                ):
                    failures.append("formal-design audit A-E qualification binding is stale")
    if design.get("formal_execution_allowed") is not False:
        failures.append("formal design unexpectedly allows execution")
    if analysis.get("formal_execution_allowed") is not False:
        failures.append("analysis plan unexpectedly allows execution")
    if preflight.get("formal_execution_allowed") is not False:
        failures.append("formal preflight unexpectedly allows execution")
    if preregistration.get("formal_execution_allowed") is not False:
        failures.append("preregistration readiness unexpectedly allows execution")
    if f"`{preregistration.get('readiness_sha256')}`" not in draft:
        failures.append("preregistration draft is not bound to its readiness manifest")
    if "private_world_seed" in draft or "api_key" in draft.lower():
        failures.append("preregistration draft crosses a private or credential boundary")

    nodes = [
        _json_node(
            root,
            "current_registry",
            paths["current_registry"],
            evidence_role="current_artifact_resolution",
            status="passed",
        ),
        _json_node(
            root,
            "gate_a_public_decision",
            gate_path,
            evidence_role="environment_qualification_only",
            status="passed",
        ),
        _json_node(
            root,
            "formal_design",
            paths["formal_design"],
            evidence_role="frozen_protocol",
            status="frozen_execution_blocked",
        ),
        _json_node(
            root,
            "analysis_plan",
            paths["analysis_plan"],
            evidence_role="frozen_analysis",
            status="frozen_execution_blocked",
        ),
        _json_node(
            root,
            "formal_design_audit",
            paths["formal_design_audit"],
            evidence_role="design_qualification",
            status=str(design_audit.get("status")),
        ),
        _json_node(
            root,
            "power_resource_audit",
            paths["power_resource_audit"],
            evidence_role="power_resource_qualification",
            status=str(power_audit.get("status")),
        ),
        _json_node(
            root,
            "formal_preflight",
            paths["formal_preflight"],
            evidence_role="execution_preflight",
            status=str(preflight.get("status")),
        ),
        _json_node(
            root,
            "method_qualification_readiness",
            paths["method_qualification_readiness"],
            evidence_role="method_qualification_readiness",
            status=str(qualification.get("status")),
        ),
        _json_node(
            root,
            "submission_route_decision",
            paths["submission_route_decision"],
            evidence_role="outcome_blind_route_decision",
            status=str(route.get("status")),
        ),
        _json_node(
            root,
            "preregistration_readiness",
            paths["preregistration_readiness"],
            evidence_role="preregistration_readiness",
            status=str(preregistration.get("status")),
        ),
        _text_node(
            root,
            "preregistration_draft",
            paths["preregistration_draft"],
            evidence_role="reader_facing_protocol_draft",
            status="final_freeze_blocked",
        ),
    ]
    edges = [
        {"from": source, "to": target, "relation": relation}
        for source, target, relation in _CURRENT_EDGE_SPECS
    ]
    graph: dict[str, Any] = {
        "schema_version": PRERUN_EVIDENCE_GRAPH_VERSION,
        "status": "failed" if failures else "passed_final_freeze_blocked",
        "formal_result": False,
        "formal_execution_allowed": False,
        "provider_calls_executed": 0,
        "formal_participant_outcome_count": 0,
        "claim_boundary": {
            "gate_a_is_environment_qualification_only": True,
            "evaluator_contracts_are_covered_by_production_tests": True,
            "formal_primary_data_present": False,
            "private_identities_present": False,
        },
        # The clean-release receipt binds the exact tested commit. Duplicating
        # source-file hashes here would make this graph a second source authority.
        "source_bindings": [],
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "passed_node_count": len(nodes) if not failures else 0,
            "failed_node_count": 0 if not failures else len(nodes),
            "preregistration_blocker_count": len(
                preregistration.get("unresolved_requirement_ids", [])
            ),
        },
        "failures": failures,
    }
    graph["graph_sha256"] = prerun_evidence_graph_sha256(graph)
    return graph


def _dag_errors(node_ids: set[str], edges: Sequence[Mapping[str, Any]]) -> list[str]:
    errors: list[str] = []
    incoming = dict.fromkeys(node_ids, 0)
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        if source not in node_ids or target not in node_ids:
            errors.append("evidence graph edge references a missing node")
            continue
        incoming[str(target)] += 1
        outgoing[str(source)].append(str(target))
    queue = [node_id for node_id, count in incoming.items() if count == 0]
    visited = 0
    while queue:
        node_id = queue.pop()
        visited += 1
        for target in outgoing[node_id]:
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    if visited != len(node_ids):
        errors.append("evidence graph contains a cycle")
    return errors


def validate_prerun_evidence_graph(root: Path, graph: Mapping[str, Any]) -> list[str]:
    """Validate an immutable legacy snapshot or the current graph and its nodes."""

    root = root.resolve()
    legacy_snapshot = _load_object(root / _LEGACY_GRAPH_PATH)
    legacy_graph = graph.get("graph_sha256") == legacy_snapshot.get("graph_sha256")
    errors: list[str] = []
    if legacy_graph and graph != legacy_snapshot:
        errors.append("legacy Work II evidence graph differs from its immutable snapshot")
    if graph.get("schema_version") != PRERUN_EVIDENCE_GRAPH_VERSION:
        errors.append("unexpected Work II pre-run evidence graph schema")
    if graph.get("graph_sha256") != prerun_evidence_graph_sha256(graph):
        errors.append("Work II pre-run evidence graph self-hash mismatch")
    if graph.get("status") != "passed_final_freeze_blocked" or graph.get("failures") != []:
        errors.append("Work II pre-run evidence graph has not passed")
    if (
        graph.get("formal_result") is not False
        or graph.get("formal_execution_allowed") is not False
        or graph.get("provider_calls_executed") != 0
        or graph.get("formal_participant_outcome_count") != 0
    ):
        errors.append("Work II pre-run evidence graph crossed the execution boundary")
    nodes_value = graph.get("nodes")
    nodes = nodes_value if isinstance(nodes_value, list) else []
    node_ids = {
        str(node.get("id")) for node in nodes if isinstance(node, Mapping) and node.get("id")
    }
    if legacy_graph:
        expected_node_ids = _LEGACY_NODE_IDS
        expected_edge_specs = _LEGACY_EDGE_SPECS
    else:
        expected_node_ids = _CURRENT_NODE_IDS
        expected_edge_specs = _CURRENT_EDGE_SPECS
    expected_node_count = len(expected_node_ids)
    if node_ids != expected_node_ids:
        errors.append("Work II pre-run evidence graph has an unexpected node set")
    if len(nodes) != expected_node_count:
        errors.append("Work II pre-run evidence graph contains duplicate nodes")
    for node in nodes:
        if not isinstance(node, Mapping):
            errors.append("Work II pre-run evidence graph contains an invalid node")
            continue
        path_value = node.get("path")
        if not isinstance(path_value, str):
            errors.append("Work II pre-run evidence graph node lacks a path")
            continue
        if not legacy_graph:
            path = root / path_value
            if not path.is_file() or node.get("file_sha256") != file_sha256(path):
                errors.append(f"Work II pre-run evidence graph node is stale: {node.get('id')}")
        if node.get("formal_participant_result") is not False:
            errors.append(f"Work II evidence node crosses formal-result boundary: {node.get('id')}")
    edges_value = graph.get("edges")
    edges = edges_value if isinstance(edges_value, list) else []
    expected_edges = [
        {"from": source, "to": target, "relation": relation}
        for source, target, relation in expected_edge_specs
    ]
    if edges != expected_edges:
        errors.append("Work II pre-run evidence graph has an unexpected edge count")
    errors.extend(_dag_errors(node_ids, edges))
    summary = graph.get("summary")
    summary = summary if isinstance(summary, Mapping) else {}
    if (
        summary.get("node_count") != expected_node_count
        or summary.get("edge_count") != len(expected_edge_specs)
        or summary.get("passed_node_count") != expected_node_count
        or summary.get("failed_node_count") != 0
    ):
        errors.append("Work II pre-run evidence graph summary is inconsistent")
    source_bindings = graph.get("source_bindings", [])
    if not legacy_graph and source_bindings != []:
        errors.append("current Work II evidence graph duplicates release source bindings")
    return errors


def _material_tree_changed_since(root: Path, tested_commit: str) -> tuple[bool, str | None]:
    """Return material-tree change state and any Git diagnostic."""

    completed = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            tested_commit,
            "HEAD",
            "--",
            *_CLEAN_RELEASE_MATERIAL_PATHS,
        ],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0:
        return False, None
    if completed.returncode == 1:
        return True, None
    diagnostic = str(completed.stderr or "").strip()
    return True, diagnostic or f"git diff exited with status {completed.returncode}"


def validate_clean_release_receipt(
    receipt: Mapping[str, Any],
    *,
    root: Path | None = None,
) -> list[str]:
    """Validate the durable outcome-free receipt emitted by an independent checkout audit."""

    errors: list[str] = []
    if receipt.get("schema_version") != CLEAN_RELEASE_RECEIPT_VERSION:
        errors.append("unexpected Work II clean-release receipt schema")
    if receipt.get("receipt_sha256") != clean_release_receipt_sha256(receipt):
        errors.append("Work II clean-release receipt self-hash mismatch")
    if receipt.get("status") != "passed" or receipt.get("failures") != []:
        errors.append("Work II clean-release receipt has not passed")
    if (
        receipt.get("formal_result") is not False
        or receipt.get("formal_execution_allowed") is not False
        or receipt.get("provider_calls_executed") != 0
        or receipt.get("formal_participant_outcome_count") != 0
    ):
        errors.append("Work II clean-release receipt crossed the execution boundary")
    commit = receipt.get("tested_commit")
    if (
        not isinstance(commit, str)
        or len(commit) != 40
        or any(character not in "0123456789abcdef" for character in commit)
    ):
        errors.append("Work II clean-release receipt lacks a full tested commit")
    elif root is not None:
        root = root.resolve()
        if git_worktree_dirty(root):
            errors.append("current Work II release worktree is dirty")
        current_commit = git_source_commit(root)
        material_changed, material_error = _material_tree_changed_since(root, commit)
        if material_changed:
            errors.append(
                "current Work II implementation differs from the clean-release tested commit"
            )
        if material_error is not None:
            errors.append(f"clean-release material-tree comparison failed: {material_error}")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, current_commit],
            cwd=root,
            capture_output=True,
            check=False,
        )
        if ancestor.returncode == 1:
            errors.append("clean-release tested commit is not an ancestor of current HEAD")
        elif ancestor.returncode != 0:
            diagnostic = str(ancestor.stderr or "").strip()
            errors.append(
                "clean-release commit ancestry check failed: "
                + (diagnostic or f"git merge-base exited with status {ancestor.returncode}")
            )
    checkout = receipt.get("independent_checkout")
    checkout = checkout if isinstance(checkout, Mapping) else {}
    if (
        checkout.get("mode") != "git_clone_no_local"
        or checkout.get("clean_before") is not True
        or checkout.get("clean_after") is not True
        or checkout.get("path_recorded") is not False
    ):
        errors.append("Work II clean-release receipt lacks a clean independent checkout")
    wheel = receipt.get("wheel")
    wheel = wheel if isinstance(wheel, Mapping) else {}
    if (
        wheel.get("status") != "passed"
        or not isinstance(wheel.get("sha256"), str)
        or len(str(wheel.get("sha256"))) != 64
        or not isinstance(wheel.get("bytes"), int)
        or wheel.get("bytes", 0) <= 0
        or wheel.get("installed_import_smoke") is not True
    ):
        errors.append("Work II clean-release receipt lacks a valid clean wheel result")
    tests = receipt.get("work_ii_tests")
    tests = tests if isinstance(tests, Mapping) else {}
    if (
        tests.get("status") != "passed"
        or tests.get("test_files") != list(WORK_II_RELEASE_TEST_FILES)
        or not isinstance(tests.get("passed"), int)
        or isinstance(tests.get("passed"), bool)
        or tests.get("passed", 0) <= 0
        or tests.get("skipped") != 0
        or tests.get("failed") != 0
        or not isinstance(tests.get("stdout_sha256"), str)
        or not isinstance(tests.get("stderr_sha256"), str)
    ):
        errors.append("Work II clean-release receipt lacks the exact release test result")
    checks = receipt.get("frozen_checks")
    checks = checks if isinstance(checks, Mapping) else {}
    if checks.get("status") != "passed" or checks.get("passed") != 4:
        errors.append("Work II clean-release receipt lacks all frozen checks")
    graph = receipt.get("evidence_graph")
    graph = graph if isinstance(graph, Mapping) else {}
    graph_shape = (graph.get("node_count"), graph.get("edge_count"))
    if (
        graph.get("status") != "passed"
        or not isinstance(graph.get("graph_sha256"), str)
        or graph_shape
        not in {
            (len(_LEGACY_NODE_IDS), len(_LEGACY_EDGE_SPECS)),
            (len(_CURRENT_NODE_IDS), len(_CURRENT_EDGE_SPECS)),
        }
    ):
        errors.append("Work II clean-release receipt lacks a valid evidence graph result")
    return errors


def validate_preregistration_freeze_receipt(
    root: Path,
    receipt: Mapping[str, Any],
    manifest: Mapping[str, Any],
    qualification_receipt: Mapping[str, Any],
    qualification_receipt_path: Path,
    *,
    currency_ceiling_usd: float,
) -> list[str]:
    """Validate the final user-authorized, outcome-blind Work II freeze receipt."""

    errors: list[str] = []
    if receipt.get("schema_version") != PREREGISTRATION_FREEZE_RECEIPT_VERSION:
        errors.append("unexpected Work II preregistration-freeze receipt schema")
    if receipt.get("receipt_sha256") != preregistration_freeze_receipt_sha256(receipt):
        errors.append("Work II preregistration-freeze receipt self-hash mismatch")
    if receipt.get("status") != "passed_final_freeze":
        errors.append("Work II preregistration final freeze has not passed")
    if (
        receipt.get("formal_result") is not False
        or receipt.get("formal_participant_outcome_count") != 0
        or receipt.get("formal_execution_authorized") is not True
    ):
        errors.append("Work II preregistration-freeze receipt crossed its outcome boundary")

    bindings = receipt.get("bindings")
    bindings = bindings if isinstance(bindings, Mapping) else {}
    if bindings.get("formal_preflight_sha256") != manifest.get("preflight_sha256"):
        errors.append("preregistration freeze does not bind the formal manifest")

    route_path = root / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
    if not route_path.is_file():
        errors.append("current submission-route decision is missing")
        route: dict[str, Any] = {}
    else:
        route = _load_object(route_path)
        errors.extend(validate_submission_route_decision(route))
    selected_route = route.get("selected_option")
    if route.get("status") != "selected" or selected_route not in {
        "nature_registered_report_stage_1",
        "regular_submission",
    }:
        errors.append("submission route lacks outcome-blind user selection")
    if (
        bindings.get("route_decision_sha256") != route.get("decision_sha256")
        or receipt.get("selected_submission_route") != selected_route
    ):
        errors.append("preregistration freeze does not bind the selected submission route")

    try:
        readiness_version = _readiness_version(manifest)
    except ValueError as error:
        errors.append(str(error))
        readiness_version = "unsupported"
    readiness_path = root / (
        "workstreams/flagship_tasks/reports/"
        f"work-ii-preregistration-readiness-{readiness_version}.json"
    )
    if not readiness_path.is_file():
        errors.append("preregistration readiness manifest is missing")
    else:
        readiness = _load_object(readiness_path)
        if (
            bindings.get("preregistration_readiness_sha256")
            != readiness.get("readiness_sha256")
            or bindings.get("preregistration_readiness_file_sha256")
            != file_sha256(readiness_path)
        ):
            errors.append("preregistration freeze does not bind its readiness manifest")

    clean_path = (
        root
        / "workstreams/flagship_tasks/reports/"
        "work-ii-clean-release-receipt-v0.1.json"
    )
    if not clean_path.is_file():
        errors.append("clean-release receipt is missing")
    else:
        clean = _load_object(clean_path)
        clean_errors = validate_clean_release_receipt(clean, root=root)
        errors.extend(f"clean release: {error}" for error in clean_errors)
        clean_binding = bindings.get("clean_release")
        clean_binding = clean_binding if isinstance(clean_binding, Mapping) else {}
        if (
            clean_binding.get("file_sha256") != file_sha256(clean_path)
            or clean_binding.get("receipt_sha256") != clean.get("receipt_sha256")
            or clean_binding.get("tested_commit") != clean.get("tested_commit")
            or clean_binding.get("graph_sha256")
            != clean.get("evidence_graph", {}).get("graph_sha256")
        ):
            errors.append("preregistration freeze does not bind the clean-release receipt")

    qualification_path = qualification_receipt_path.resolve()
    if not qualification_path.is_file():
        errors.append("method-qualification receipt file is missing")
    else:
        qualification_binding = bindings.get("method_qualification")
        qualification_binding = (
            qualification_binding if isinstance(qualification_binding, Mapping) else {}
        )
        if (
            qualification_binding.get("path")
            != _relative(root, qualification_path)
            or qualification_binding.get("file_sha256") != file_sha256(qualification_path)
            or qualification_binding.get("receipt_sha256")
            != qualification_receipt_sha256(qualification_receipt)
        ):
            errors.append("preregistration freeze does not bind method qualification")
    qualification_ceiling = qualification_receipt.get("approved_currency_ceiling_usd")
    if (
        isinstance(qualification_ceiling, bool)
        or not isinstance(qualification_ceiling, int | float)
        or float(qualification_ceiling) <= 0
    ):
        errors.append("method qualification lacks its distinct positive currency ceiling")
    else:
        qualification_errors = validate_method_qualification_receipt(
            root,
            qualification_receipt,
            manifest,
            currency_ceiling_usd=float(qualification_ceiling),
        )
        errors.extend(f"method qualification: {error}" for error in qualification_errors)

    authorization = receipt.get("user_authorization")
    authorization = authorization if isinstance(authorization, Mapping) else {}
    if (
        authorization.get("authorized_by") != "user"
        or not isinstance(authorization.get("authorized_at"), str)
        or not authorization.get("authorized_at")
        or authorization.get("credential_rotation_confirmed") is not True
        or authorization.get("execution_command_approved") is not True
        or authorization.get("budget_approved") is not True
        or authorization.get("failure_escalation_approved") is not True
        or authorization.get("formal_pricing_contract_approved") is not True
    ):
        errors.append("preregistration freeze lacks complete user authorization")
    if (
        authorization.get("formal_currency_ceiling_usd") != currency_ceiling_usd
        or isinstance(currency_ceiling_usd, bool)
        or not isinstance(currency_ceiling_usd, int | float)
        or float(currency_ceiling_usd) <= 0
    ):
        errors.append("preregistration freeze formal currency ceiling differs from the CLI ceiling")
    if authorization.get("qualification_currency_ceiling_usd") != qualification_ceiling:
        errors.append("preregistration freeze changed the qualification currency ceiling")
    expected_eta = authorization.get("qualified_expected_eta_seconds")
    if not isinstance(expected_eta, (int, float)) or expected_eta <= 0:
        errors.append("preregistration freeze lacks a qualified positive ETA")
    if authorization.get("provider_contract") != manifest.get("provider_contract"):
        errors.append("preregistration freeze provider contract differs from the manifest")

    formal_budget = receipt.get("formal_currency_budget")
    if not isinstance(formal_budget, Mapping):
        errors.append("preregistration freeze lacks a formal currency budget contract")
    else:
        errors.extend(validate_formal_cost_contract(root, manifest, formal_budget))
        if formal_budget.get("formal_currency_ceiling_usd") != float(
            currency_ceiling_usd
        ):
            errors.append("formal currency budget differs from the user-approved ceiling")

    escalation = receipt.get("failure_escalation_contract")
    escalation = escalation if isinstance(escalation, Mapping) else {}
    if any(
        escalation.get(field) is not True
        for field in (
            "missing_infrastructure_only_resume",
            "persisted_scientific_trajectory_never_replaced",
            "halt_on_provider_attempt_cap",
            "result_direction_early_stopping_forbidden",
        )
    ):
        errors.append("preregistration freeze lacks the failure-escalation contract")

    route_compliance = receipt.get("route_compliance")
    route_compliance = route_compliance if isinstance(route_compliance, Mapping) else {}
    if selected_route == "nature_registered_report_stage_1":
        if (
            route_compliance.get("stage_1_in_principle_acceptance") is not True
            or route_compliance.get("approved_protocol_registered") is not True
            or not isinstance(route_compliance.get("registration_reference"), str)
            or not route_compliance.get("registration_reference")
        ):
            errors.append("Nature Registered Report route lacks IPA/registration evidence")
    elif selected_route == "regular_submission" and (
        route_compliance.get("target_and_evidence_threshold_frozen") is not True
        or not isinstance(route_compliance.get("target"), str)
        or not route_compliance.get("target")
        or not isinstance(route_compliance.get("evidence_threshold"), str)
        or not route_compliance.get("evidence_threshold")
    ):
        errors.append("regular-submission route lacks its frozen target/threshold")
    return errors


def build_preregistration_freeze_receipt(
    root: Path,
    manifest: Mapping[str, Any],
    qualification_receipt_path: Path,
    *,
    currency_ceiling_usd: float,
    qualified_expected_eta_seconds: float,
    authorized_at: str,
    route_compliance: Mapping[str, Any],
    pricing_source: str,
    pricing_observed_at: str,
    cache_hit_input_usd_per_million: float,
    cache_miss_input_usd_per_million: float,
    output_usd_per_million: float,
) -> dict[str, Any]:
    """Build the final receipt after every external W2-08/W2-10/W2-11 condition exists."""

    root = root.resolve()
    qualification_path = qualification_receipt_path.resolve()
    route_path = root / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
    readiness_version = _readiness_version(manifest)
    readiness_path = root / (
        "workstreams/flagship_tasks/reports/"
        f"work-ii-preregistration-readiness-{readiness_version}.json"
    )
    clean_path = (
        root
        / "workstreams/flagship_tasks/reports/"
        "work-ii-clean-release-receipt-v0.1.json"
    )
    route = _load_object(route_path)
    readiness = _load_object(readiness_path)
    clean = _load_object(clean_path)
    qualification = _load_object(qualification_path)
    qualification_ceiling = qualification.get("approved_currency_ceiling_usd")
    if (
        isinstance(qualification_ceiling, bool)
        or not isinstance(qualification_ceiling, int | float)
        or float(qualification_ceiling) <= 0
    ):
        raise ValueError("method qualification lacks its distinct positive currency ceiling")
    formal_budget = build_formal_cost_contract(
        root,
        manifest,
        formal_currency_ceiling_usd=float(currency_ceiling_usd),
        pricing_source=pricing_source,
        pricing_observed_at=pricing_observed_at,
        cache_hit_input_usd_per_million=float(cache_hit_input_usd_per_million),
        cache_miss_input_usd_per_million=float(cache_miss_input_usd_per_million),
        output_usd_per_million=float(output_usd_per_million),
    )
    receipt: dict[str, Any] = {
        "schema_version": PREREGISTRATION_FREEZE_RECEIPT_VERSION,
        "status": "passed_final_freeze",
        "formal_result": False,
        "formal_participant_outcome_count": 0,
        "formal_execution_authorized": True,
        "selected_submission_route": route.get("selected_option"),
        "formal_currency_budget": formal_budget,
        "bindings": {
            "formal_preflight_sha256": manifest.get("preflight_sha256"),
            "route_decision_sha256": route.get("decision_sha256"),
            "preregistration_readiness_sha256": readiness.get("readiness_sha256"),
            "preregistration_readiness_file_sha256": file_sha256(readiness_path),
            "clean_release": {
                "file_sha256": file_sha256(clean_path),
                "receipt_sha256": clean.get("receipt_sha256"),
                "tested_commit": clean.get("tested_commit"),
                "graph_sha256": clean.get("evidence_graph", {}).get("graph_sha256"),
            },
            "method_qualification": {
                "path": _relative(root, qualification_path),
                "file_sha256": file_sha256(qualification_path),
                "receipt_sha256": qualification_receipt_sha256(qualification),
            },
        },
        "user_authorization": {
            "authorized_by": "user",
            "authorized_at": authorized_at,
            "credential_rotation_confirmed": True,
            "execution_command_approved": True,
            "budget_approved": True,
            "failure_escalation_approved": True,
            "formal_pricing_contract_approved": True,
            "qualification_currency_ceiling_usd": float(qualification_ceiling),
            "formal_currency_ceiling_usd": float(currency_ceiling_usd),
            "qualified_expected_eta_seconds": float(qualified_expected_eta_seconds),
            "provider_contract": manifest.get("provider_contract"),
        },
        "failure_escalation_contract": {
            "missing_infrastructure_only_resume": True,
            "persisted_scientific_trajectory_never_replaced": True,
            "halt_on_provider_attempt_cap": True,
            "result_direction_early_stopping_forbidden": True,
        },
        "route_compliance": dict(route_compliance),
    }
    receipt["receipt_sha256"] = preregistration_freeze_receipt_sha256(receipt)
    errors = validate_preregistration_freeze_receipt(
        root,
        receipt,
        manifest,
        qualification,
        qualification_path,
        currency_ceiling_usd=float(currency_ceiling_usd),
    )
    if errors:
        raise ValueError("built preregistration freeze receipt is invalid: " + "; ".join(errors))
    return receipt


__all__ = [
    "CLEAN_RELEASE_RECEIPT_VERSION",
    "PREREGISTRATION_FREEZE_RECEIPT_VERSION",
    "PRERUN_EVIDENCE_GRAPH_VERSION",
    "WORK_II_RELEASE_TEST_FILES",
    "build_preregistration_freeze_receipt",
    "build_prerun_evidence_graph",
    "clean_release_receipt_sha256",
    "preregistration_freeze_receipt_sha256",
    "prerun_evidence_graph_sha256",
    "validate_clean_release_receipt",
    "validate_preregistration_freeze_receipt",
    "validate_prerun_evidence_graph",
]
