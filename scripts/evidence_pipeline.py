"""Refresh and verify ChemWorld's current evidence dependency graph.

This is the only supported entry point for regenerating *current* evidence.
Historical reports remain immutable; the paths below are materialized views of
the current source and protocol state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CURRENT_REGISTRY = ROOT / "configs/current.json"


@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    path: str
    role: str
    dependencies: tuple[str, ...] = ()
    command: tuple[str, ...] | None = None


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
        "method_freeze_plan",
        "configs/benchmark/method_freeze_v0.4.json",
        "protocol_input",
    ),
    EvidenceNode(
        "llm_development_plan",
        "configs/methods/llm_v0.4/llm_development_plan.json",
        "development_input",
        ("runtime_affordance",),
    ),
    EvidenceNode(
        "classic_development",
        "workstreams/benchmark_v1/reports/classic-dev-v0.4.1.json",
        "development_input",
    ),
    EvidenceNode(
        "operation_development",
        "workstreams/benchmark_v1/reports/operation-baselines-dev-v0.4.1.json",
        "development_input",
    ),
    EvidenceNode(
        "ppo_preflight",
        "workstreams/benchmark_v1/reports/rl-ppo-v0412-preflight-v0.4.json",
        "development_input",
    ),
    EvidenceNode(
        "sac_preflight",
        "workstreams/benchmark_v1/reports/rl-sac-v0412-preflight-v0.4.json",
        "development_input",
    ),
    EvidenceNode(
        "mechanism_protocol",
        "configs/benchmark/mechanism_adaptation_v0.2.1.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_gate_a_plan",
        "configs/benchmark/mechanism_adaptation_gate_a_v0.2.1.json",
        "protocol_input",
        ("mechanism_protocol",),
    ),
    EvidenceNode(
        "mechanism_design_audit",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-v0.2.1.json",
        "development_control",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
        ("scripts/audit_mechanism_adaptation_design.py",),
    ),
    EvidenceNode(
        "mechanism_protocol_report",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-final-protocol-v0.2.md",
        "development_input",
        ("mechanism_protocol",),
    ),
    EvidenceNode(
        "mechanism_public_matrix",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-public-matrix.json",
        "development_control",
        ("mechanism_protocol",),
        ("scripts/plan_mechanism_adaptation_matrix.py",),
    ),
    EvidenceNode(
        "mechanism_preflight",
        "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-preflight.json",
        "development_control",
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
        "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.2.1.json",
        "mechanism_gate",
        (
            "mechanism_design_audit",
            "mechanism_gate_a_plan",
            "mechanism_preflight",
            "mechanism_protocol",
        ),
    ),
    EvidenceNode(
        "backend_golden_fixture",
        "tests/fixtures/golden/core_scripted_trajectories.json",
        "distribution_input",
    ),
    EvidenceNode(
        "runtime_integration",
        "workstreams/world_foundation/reports/wf-110-runtime-integration.json",
        "backend_control",
        command=("scripts/audit_vnext_runtime_integration.py",),
    ),
    EvidenceNode(
        "runtime_reachability",
        "workstreams/world_foundation/reports/runtime-reachability-vnext.json",
        "backend_control",
        ("runtime_integration", "runtime_reachability_protocol"),
        ("scripts/audit_runtime_reachability_vnext.py",),
    ),
    EvidenceNode(
        "state_transition_invariants",
        "workstreams/world_foundation/reports/state-transition-invariants.json",
        "backend_control",
        ("runtime_integration", "state_transition_protocol"),
        ("scripts/audit_state_transition_invariants.py",),
    ),
    EvidenceNode(
        "public_boundary",
        "workstreams/world_foundation/reports/public-boundary-security-vnext.json",
        "backend_control",
        ("public_boundary_protocol", "runtime_integration"),
        ("scripts/audit_public_boundary_security_vnext.py",),
    ),
    EvidenceNode(
        "maturity_truth",
        "workstreams/world_foundation/reports/maturity-truth-vnext.json",
        "backend_control",
        ("maturity_protocol", "runtime_integration", "runtime_reachability"),
        ("scripts/audit_maturity_truth_vnext.py",),
    ),
    EvidenceNode(
        "runtime_affordance",
        "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json",
        "development_control",
        command=("scripts/audit_runtime_domain_affordances.py",),
    ),
    EvidenceNode(
        "backend_candidate",
        "workstreams/world_foundation/reports/backend-v0.5.json",
        "backend_control",
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
    EvidenceNode(
        "method_freeze",
        "workstreams/benchmark_v1/reports/method-freeze-v0.4.json",
        "formal_gate",
        (
            "backend_candidate",
            "classic_development",
            "llm_development_plan",
            "method_freeze_plan",
            "operation_development",
        ),
        ("scripts/audit_method_freeze_v0.4.py",),
    ),
    EvidenceNode(
        "backend_bundle",
        "benchmark/releases/chemworld-serious-vnext/manifest.json",
        "distribution_bundle",
        (
            "backend_candidate",
            "backend_golden_fixture",
            "maturity_truth",
            "public_boundary",
            "runtime_integration",
        ),
        ("scripts/build_vnext_backend_candidate.py",),
    ),
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def node_map() -> dict[str, EvidenceNode]:
    nodes = {node.node_id: node for node in NODES}
    if len(nodes) != len(NODES):
        raise ValueError("evidence DAG contains duplicate node ids")
    paths = [node.path for node in NODES]
    if len(set(paths)) != len(paths):
        raise ValueError("evidence DAG contains duplicate materialized paths")
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
                raise ValueError(
                    f"{node.node_id} has unknown dependencies: {sorted(unknown)}"
                )
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
                "dependencies": list(node.dependencies),
                "command": list(node.command) if node.command else None,
            }
            for node in NODES
        ]
    )


def _run(node: EvidenceNode) -> None:
    if node.command is None:
        return
    command = [sys.executable, *node.command]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # Method freeze is a truthful negative gate until all methods are ready.
    allowed_codes = {0, 1} if node.node_id == "method_freeze" else {0}
    if completed.returncode not in allowed_codes:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"generator failed for {node.node_id}: {detail}")
    if not (ROOT / node.path).is_file():
        raise RuntimeError(f"generator did not create {node.path}")

MATERIALIZED_OUTPUT_PREFIXES = (
    "benchmark/releases/chemworld-serious-vnext/",
)


def _is_materialized_output_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    materialized_paths = {
        node.path.replace("\\", "/") for node in NODES if node.command is not None
    }
    materialized_paths.add("configs/current.json")
    return normalized in materialized_paths or normalized.startswith(
        MATERIALIZED_OUTPUT_PREFIXES
    )


def _git_tree_dirty() -> bool:
    """Return whether tracked source/protocol inputs differ from HEAD.

    Current evidence reports and release-bundle views are generated outputs. They
    may change during a DAG refresh without making the source tree itself dirty.
    """

    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    changed_source_paths: list[str] = []
    for line in completed.stdout.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not _is_materialized_output_path(path):
            changed_source_paths.append(path)
    return bool(changed_source_paths)


def _node_gate_state(node: EvidenceNode, payload: dict[str, Any]) -> str:
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


def _write_current_registry() -> None:
    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    backend = json.loads((ROOT / node_map()["backend_candidate"].path).read_text())
    method = json.loads((ROOT / node_map()["method_freeze"].path).read_text())
    mechanism = json.loads((ROOT / node_map()["mechanism_gate_a"].path).read_text())
    method_plan = json.loads((ROOT / node_map()["method_freeze_plan"].path).read_text())
    mechanism_protocol = json.loads(
        (ROOT / node_map()["mechanism_protocol"].path).read_text()
    )
    from chemworld.data.schema import OUTCOME_LAYER_FIELDS, TRAJECTORY_SCHEMA_VERSION

    dirty = _git_tree_dirty()
    nodes: dict[str, Any] = {}
    for node in generation_order():
        path = ROOT / node.path
        payload = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.suffix == ".json"
            else {}
        )
        nodes[node.node_id] = {
            "path": node.path,
            "role": node.role,
            "dependencies": list(node.dependencies),
            "sha256": file_sha256(path),
            "artifact_state": "current",
            "gate_state": _node_gate_state(node, payload),
        }

    current["schema_version"] = "chemworld-current-surface-registry-0.2"
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
        "attribution": "diagnostic_protocol_defined_gate_a_blocked",
        "chemical_coverage": "selected_bounded_archetypes_not_exhaustive",
        "physical_fidelity": "model_card_bounded_not_universal_digital_twin",
    }
    current["benchmark_suites"] = {
        "core": {
            "role": "formal_confirmatory_comparison",
            "protocol": "configs/benchmark/method_freeze_v0.4.json",
            "task_ids": list(method_plan["formal_core_tasks"]),
            "status": (
                "ready" if method.get("method_freeze_ready") else "method_freeze_blocked"
            ),
        },
        "diagnostic": {
            "role": "identifiability_feedback_adaptation_and_autonomy_attribution",
            "protocol": "configs/benchmark/mechanism_adaptation_v0.2.1.json",
            "task_ids": list(mechanism_protocol["design"]["tasks"]),
            "status": "gate_a_passed" if mechanism.get("gate_a_pass") else "gate_a_blocked",
        },
        "extended": {
            "role": "environment_coverage_training_and_demonstration",
            "registered_task_count": len(backend.get("task_contract_hashes", {})),
            "formal_ranking_claim": False,
        },
    }
    current["state_model"] = {
        "schema_version": "chemworld-evidence-state-model-0.1",
        "dimensions": {
            "artifact_state": ["current", "stale", "historical", "pending"],
            "gate_state": ["passed", "blocked", "pending", "not_applicable"],
            "claim_scope": [
                "backend_control",
                "development",
                "formal_benchmark",
                "mechanism_benchmark",
                "publication",
            ],
        },
        "rules": [
            "current means regenerated from the declared DAG, not scientifically ready",
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
        "schema_version": "chemworld-current-evidence-dag-0.1",
        "generator": "python scripts/evidence_pipeline.py --refresh",
        "checker": "python scripts/evidence_pipeline.py --check",
        "graph_sha256": graph_sha256(),
        "generation_order": [node.node_id for node in generation_order()],
        "nodes": nodes,
    }
    current["runtime"].update(
        {
            "status": backend["status"],
            "contract_validation": (
                "passed" if backend["backend_contract_validated"] else "blocked"
            ),
            "clean_release_attestation": backend["clean_release_attestation"],
            "source_tree_dirty": backend["source_tree_dirty"],
        }
    )
    current["formal_evaluation"].update(
        {
            "status": (
                "method_freeze_ready"
                if method["method_freeze_ready"]
                else "method_freeze_preflight_blocked"
            ),
            "method_freeze_ready": method["method_freeze_ready"],
            "bench_unlock_allowed": method["bench_unlock_allowed"],
            "blocker_count": len(method["blockers"]),
            "formal_results_present": False,
            "benchmark_claim_allowed": False,
        }
    )
    current["mechanism_adaptation"].update(
        {
            "protocol": node_map()["mechanism_protocol"].path,
            "preflight_report": node_map()["mechanism_preflight"].path,
            "design_audit_report": node_map()["mechanism_design_audit"].path,
            "design_audit_pass": True,
            "gate_a_plan": node_map()["mechanism_gate_a_plan"].path,
            "gate_a_report": node_map()["mechanism_gate_a"].path,
            "status": (
                "gate_a_passed_remaining_gates_pending"
                if mechanism.get("gate_a_pass")
                else "gate_a_failed_remaining_gates_pending"
            ),
            "gate_a_pass": bool(mechanism.get("gate_a_pass")),
            "new_external_provider_runs_completed": False,
            "publication_ready": False,
        }
    )
    current["publication"] = {
        "status": "no_active_manuscript",
        "archived_working_draft": (
            "paper/archive/ncs-working-draft-2026-07-21/README.md"
        ),
        "publication_ready": False,
    }
    blockers: list[dict[str, Any]] = []
    if backend["clean_release_attestation"] != "passed":
        blockers.append(
            {"id": "clean_release_attestation_pending", "scope": "backend_release"}
        )
    if not method["method_freeze_ready"]:
        blockers.append(
            {
                "id": "method_freeze_blocked",
                "scope": "formal_benchmark",
                "count": len(method["blockers"]),
            }
        )
    remaining_mechanism_gates = ["gate_0", "gate_b", "gate_c", "gate_d", "gate_e"]
    if not mechanism.get("gate_a_pass"):
        remaining_mechanism_gates.insert(1, "gate_a")
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
        "stale_binding_count": 0,
        "blockers": blockers,
    }
    current["history_policy"] = {
        "current_materialized_views_are_regenerated_by_the_evidence_dag": True,
        "historical_artifacts_are_immutable": True,
        "version_suffix_does_not_imply_current": True,
        "archive_directories_contain_non_current_diagnostics": True,
        "raw_runs_require_a_manifested_retention_decision_before_deletion": True,
    }
    CURRENT_REGISTRY.write_text(
        json.dumps(current, indent=2) + "\n", encoding="utf-8"
    )


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


def check_current_evidence() -> list[str]:
    errors: list[str] = []
    try:
        ordered = generation_order()
    except ValueError as error:
        return [str(error)]
    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    if current.get("schema_version") != "chemworld-current-surface-registry-0.2":
        errors.append("current registry schema version is stale")
    dag = current.get("evidence_dag", {})
    if dag.get("graph_sha256") != graph_sha256():
        errors.append("current registry evidence graph hash is stale")
    expected_order = [node.node_id for node in ordered]
    if dag.get("generation_order") != expected_order:
        errors.append("current registry generation order is stale")
    recorded_nodes = dag.get("nodes", {})
    for node in ordered:
        path = ROOT / node.path
        recorded = recorded_nodes.get(node.node_id, {})
        if not path.is_file():
            errors.append(f"missing current evidence: {node.path}")
            continue
        if recorded.get("path") != node.path:
            errors.append(f"registry path mismatch: {node.node_id}")
        if recorded.get("dependencies") != list(node.dependencies):
            errors.append(f"registry dependencies stale: {node.node_id}")
        if recorded.get("sha256") != file_sha256(path):
            errors.append(f"registry digest stale: {node.node_id}")

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
    if backend.get("backend_contract_validated") is not True:
        errors.append("backend contract validation is blocked")
    if backend.get("source_tree_dirty") and backend.get("backend_freeze_allowed"):
        errors.append("dirty source tree is incorrectly recorded as frozen")

    method = json.loads((ROOT / node_map()["method_freeze"].path).read_text())
    if method.get("benchmark_claim_allowed") is not False:
        errors.append("method-freeze report improperly enables benchmark claims")
    mechanism_protocol = json.loads(
        (ROOT / node_map()["mechanism_protocol"].path).read_text()
    )
    mechanism_plan = json.loads(
        (ROOT / node_map()["mechanism_gate_a_plan"].path).read_text()
    )
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text()
    )
    mechanism = json.loads((ROOT / node_map()["mechanism_gate_a"].path).read_text())
    if mechanism_design.get("protocol_sha256") != _canonical_sha256(mechanism_protocol):
        errors.append("mechanism design-audit protocol binding is stale")
    if mechanism_design.get("gate_a_plan_sha256") != _canonical_sha256(mechanism_plan):
        errors.append("mechanism design-audit Gate A plan binding is stale")
    if mechanism_design.get("pass") is not True:
        errors.append("mechanism action/intervention design audit is blocked")
    if mechanism.get("protocol_sha256") != _canonical_sha256(mechanism_protocol):
        errors.append("mechanism Gate A protocol binding is stale")
    if mechanism.get("gate_a_plan_sha256") != _canonical_sha256(mechanism_plan):
        errors.append("mechanism Gate A plan binding is stale")
    if mechanism.get("publication_ready") is not False:
        errors.append("mechanism Gate A improperly claims publication readiness")
    _check_bundle(errors)

    runtime = current.get("runtime", {})
    formal = current.get("formal_evaluation", {})
    publication = current.get("publication", {})
    if runtime.get("contract_validation") != "passed":
        errors.append("current registry backend validation state is inconsistent")
    if formal.get("method_freeze_ready") != method.get("method_freeze_ready"):
        errors.append("current registry method-freeze state is inconsistent")
    mechanism_registry = current.get("mechanism_adaptation", {})
    if mechanism_registry.get("gate_a_pass") != mechanism.get("gate_a_pass"):
        errors.append("current registry mechanism Gate A state is inconsistent")
    if publication.get("publication_ready") is not False:
        errors.append("current registry publication state is inconsistent")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--refresh", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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
