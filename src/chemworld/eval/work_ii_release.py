"""Pre-run evidence graph and clean-release receipt contracts for Work II."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import validate_formal_bindings
from chemworld.eval.work_ii_preregistration import (
    validate_preregistration_readiness,
    validate_submission_route_decision,
)
from chemworld.eval.work_ii_qualification import validate_method_qualification_readiness

PRERUN_EVIDENCE_GRAPH_VERSION = "chemworld-work-ii-prerun-evidence-graph-0.1"
CLEAN_RELEASE_RECEIPT_VERSION = "chemworld-work-ii-clean-release-receipt-0.1"

_DEFAULT_PATHS = {
    "current_registry": "configs/current.json",
    "formal_design": "configs/benchmark/work_ii_formal_design_v0.1.json",
    "analysis_plan": "configs/benchmark/work_ii_analysis_plan_v0.1.json",
    "formal_design_audit": (
        "workstreams/flagship_tasks/reports/work-ii-formal-world-prior-design-audit.json"
    ),
    "power_resource_audit": (
        "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"
    ),
    "formal_preflight": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-formal-matrix-runner-preflight-v0.1.json"
    ),
    "method_qualification_readiness": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-method-qualification-readiness-v0.1.json"
    ),
    "submission_route_decision": (
        "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
    ),
    "preregistration_readiness": (
        "workstreams/flagship_tasks/reports/work-ii-preregistration-readiness-v0.1.json"
    ),
    "preregistration_draft": (
        "workstreams/flagship_tasks/reports/work-ii-preregistration-draft-v0.1.md"
    ),
    "blind_evaluator_shakedown": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-blind-evaluator-development-shakedown-v0.2.json"
    ),
    "held_out_evaluator_shakedown": (
        "workstreams/flagship_tasks/reports/"
        "work-ii-held-out-evaluator-development-shakedown-v0.2.json"
    ),
}

_EDGE_SPECS = (
    ("current_registry", "gate_a_public_decision", "resolves_current_gate_a"),
    ("gate_a_public_decision", "formal_design", "qualifies_environment_for"),
    ("formal_design", "formal_design_audit", "audited_by"),
    ("formal_design", "analysis_plan", "analyzed_by"),
    ("formal_design", "power_resource_audit", "resources_audited_by"),
    ("analysis_plan", "power_resource_audit", "power_audited_by"),
    ("formal_design", "formal_preflight", "materialized_by"),
    ("analysis_plan", "formal_preflight", "materialized_by"),
    ("blind_evaluator_shakedown", "formal_preflight", "qualifies_evaluator_contract"),
    ("held_out_evaluator_shakedown", "formal_preflight", "qualifies_evaluator_contract"),
    ("formal_preflight", "method_qualification_readiness", "bounds_qualification"),
    ("submission_route_decision", "preregistration_readiness", "selects_route_for"),
    ("formal_design_audit", "preregistration_readiness", "supports"),
    ("power_resource_audit", "preregistration_readiness", "supports"),
    ("formal_preflight", "preregistration_readiness", "supports"),
    ("method_qualification_readiness", "preregistration_readiness", "blocks_until_passed"),
    ("preregistration_readiness", "preregistration_draft", "renders"),
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


def build_prerun_evidence_graph(root: Path) -> dict[str, Any]:
    """Build the outcome-blind DAG used by the Work II preregistration release audit."""

    root = root.resolve()
    paths = {key: root / value for key, value in _DEFAULT_PATHS.items()}
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
    blind = _load_object(paths["blind_evaluator_shakedown"])
    held_out = _load_object(paths["held_out_evaluator_shakedown"])
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
    for label, report in (
        ("formal-design audit", design_audit),
        ("power/resource audit", power_audit),
        ("blind evaluator shakedown", blind),
        ("held-out evaluator shakedown", held_out),
    ):
        if report.get("status") != "passed" or report.get("formal_result") is not False:
            failures.append(f"{label} has not passed its non-formal boundary")
    if design_audit.get("failures") != [] or power_audit.get("failures") != []:
        failures.append("a prerequisite audit contains failures")
    if blind.get("failures") != [] or held_out.get("all_failures") != []:
        failures.append("an evaluator shakedown contains failures")
    if (
        blind.get("participant_provider_calls") != 0
        or blind.get("evaluator_provider_calls") != 0
        or held_out.get("evaluator_provider_call_count") != 0
    ):
        failures.append("an evaluator development shakedown consumed provider calls")
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
            "blind_evaluator_shakedown",
            paths["blind_evaluator_shakedown"],
            evidence_role="development_evaluator_qualification",
            status=str(blind.get("status")),
        ),
        _json_node(
            root,
            "held_out_evaluator_shakedown",
            paths["held_out_evaluator_shakedown"],
            evidence_role="development_evaluator_qualification",
            status=str(held_out.get("status")),
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
        for source, target, relation in _EDGE_SPECS
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
            "development_shakedowns_are_not_participant_results": True,
            "formal_primary_data_present": False,
            "private_identities_present": False,
        },
        "source_bindings": [
            {
                "path": "src/chemworld/eval/work_ii_release.py",
                "file_sha256": file_sha256(root / "src/chemworld/eval/work_ii_release.py"),
            },
            {
                "path": "scripts/build_work_ii_prerun_evidence_graph.py",
                "file_sha256": file_sha256(
                    root / "scripts/build_work_ii_prerun_evidence_graph.py"
                ),
            },
        ],
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
    outgoing = {node_id: [] for node_id in node_ids}
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
    """Validate graph integrity, DAG topology, and every committed artifact byte hash."""

    errors: list[str] = []
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
    if len(nodes) != 13 or len(node_ids) != 13:
        errors.append("Work II pre-run evidence graph must contain 13 unique nodes")
    for node in nodes:
        if not isinstance(node, Mapping):
            errors.append("Work II pre-run evidence graph contains an invalid node")
            continue
        path_value = node.get("path")
        if not isinstance(path_value, str):
            errors.append("Work II pre-run evidence graph node lacks a path")
            continue
        path = root / path_value
        if not path.is_file() or node.get("file_sha256") != file_sha256(path):
            errors.append(f"Work II pre-run evidence graph node is stale: {node.get('id')}")
        if node.get("formal_participant_result") is not False:
            errors.append(f"Work II evidence node crosses formal-result boundary: {node.get('id')}")
    edges_value = graph.get("edges")
    edges = edges_value if isinstance(edges_value, list) else []
    if len(edges) != len(_EDGE_SPECS):
        errors.append("Work II pre-run evidence graph has an unexpected edge count")
    errors.extend(_dag_errors(node_ids, edges))
    summary = graph.get("summary")
    summary = summary if isinstance(summary, Mapping) else {}
    if (
        summary.get("node_count") != 13
        or summary.get("edge_count") != len(_EDGE_SPECS)
        or summary.get("passed_node_count") != 13
        or summary.get("failed_node_count") != 0
    ):
        errors.append("Work II pre-run evidence graph summary is inconsistent")
    for binding in graph.get("source_bindings", []):
        if not isinstance(binding, Mapping):
            errors.append("Work II evidence graph contains an invalid source binding")
            continue
        source_path = root / str(binding.get("path"))
        if not source_path.is_file() or binding.get("file_sha256") != file_sha256(source_path):
            errors.append(f"Work II evidence graph source binding is stale: {source_path.name}")
    return errors


def validate_clean_release_receipt(receipt: Mapping[str, Any]) -> list[str]:
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
    if not isinstance(commit, str) or len(commit) != 40:
        errors.append("Work II clean-release receipt lacks a full tested commit")
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
        or tests.get("passed") != 63
        or tests.get("failed") != 0
    ):
        errors.append("Work II clean-release receipt lacks the exact release test result")
    checks = receipt.get("frozen_checks")
    checks = checks if isinstance(checks, Mapping) else {}
    if checks.get("status") != "passed" or checks.get("passed") != 4:
        errors.append("Work II clean-release receipt lacks all frozen checks")
    graph = receipt.get("evidence_graph")
    graph = graph if isinstance(graph, Mapping) else {}
    if (
        graph.get("status") != "passed"
        or not isinstance(graph.get("graph_sha256"), str)
        or graph.get("node_count") != 13
        or graph.get("edge_count") != len(_EDGE_SPECS)
    ):
        errors.append("Work II clean-release receipt lacks a valid evidence graph result")
    return errors


__all__ = [
    "CLEAN_RELEASE_RECEIPT_VERSION",
    "PRERUN_EVIDENCE_GRAPH_VERSION",
    "build_prerun_evidence_graph",
    "clean_release_receipt_sha256",
    "prerun_evidence_graph_sha256",
    "validate_clean_release_receipt",
    "validate_prerun_evidence_graph",
]
