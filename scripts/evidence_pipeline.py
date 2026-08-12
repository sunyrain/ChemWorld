"""Refresh and verify ChemWorld's current evidence dependency graph.

This is the only supported entry point for regenerating current evidence. Git
history, rather than duplicate files in the working tree, retains superseded
protocols and reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.data.schema import (  # noqa: E402
    TRAJECTORY_ALIAS_WRITE_REMOVAL_VERSION,
    TRAJECTORY_COMPATIBILITY_ALIASES,
)
from chemworld.eval.composition_qualification_design import (  # noqa: E402
    QUALIFICATION_DESIGN_VERSION,
)
from chemworld.eval.mechanism_adaptation_execution import load_json_object  # noqa: E402
from chemworld.eval.mechanism_gate_decision import (  # noqa: E402
    gate_a_execution_contract_binding,
)
from chemworld.eval.mechanism_release import STRUCTURAL_RECEIPT_VERSION  # noqa: E402
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

FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID = "first_paper_composition_qualification"
FIRST_PAPER_COMPOSITION_QUALIFICATION_PATH = (
    "workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1-design-v3.json"
)
FIRST_PAPER_COMPOSITION_QUALIFICATION_GUARDED_PATHS = (
    "scripts/run_first_paper_composition_qualification.py",
    "src/chemworld/__init__.py",
    "src/chemworld/action_codec.py",
    "src/chemworld/agent_interface.py",
    "src/chemworld/agents/task_recipes.py",
    "src/chemworld/backends",
    "src/chemworld/campaign_resources.py",
    "src/chemworld/data",
    "src/chemworld/envs",
    "src/chemworld/eval/composition_qualification.py",
    "src/chemworld/eval/composition_qualification_design.py",
    "src/chemworld/eval/cross_world_infrastructure_qualification.py",
    "src/chemworld/eval/verify.py",
    "src/chemworld/foundation",
    "src/chemworld/materials.py",
    "src/chemworld/models",
    "src/chemworld/operation_validator.py",
    "src/chemworld/physchem",
    "src/chemworld/reference",
    "src/chemworld/registration.py",
    "src/chemworld/runtime",
    "src/chemworld/schemas",
    "src/chemworld/task_design.py",
    "src/chemworld/tasks.py",
    "src/chemworld/validation.py",
    "src/chemworld/world",
    "src/chemworld/wrappers.py",
)
FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID = "first_paper_deterministic_use_case_qualification"
FIRST_PAPER_DETERMINISTIC_USE_CASES_PATH = (
    "workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1-design-v3.json"
)
FIRST_PAPER_DETERMINISTIC_USE_CASES_GUARDED_PATHS = (
    "scripts/run_first_paper_deterministic_use_cases.py",
    "src/chemworld/eval/deterministic_use_cases.py",
    *FIRST_PAPER_COMPOSITION_QUALIFICATION_GUARDED_PATHS,
)
FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID = "first_paper_agent_instrument_use"
FIRST_PAPER_AGENT_INSTRUMENT_USE_PATH = (
    "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v3.json"
)
FIRST_PAPER_AGENT_INSTRUMENT_USE_GUARDED_PATHS = (
    "scripts/run_first_paper_u05_complete_agent.py",
    "src/chemworld/agents/interactive_codex_experiment.py",
    "src/chemworld/eval/first_paper_u05_complete_agent.py",
    "src/chemworld/eval/runner.py",
)


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
        "configs/benchmark/mechanism_adaptation_v0.3.0_rc29.json",
        "protocol_input",
    ),
    EvidenceNode(
        "mechanism_gate_a_plan",
        "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc29.json",
        "protocol_input",
        ("mechanism_protocol",),
    ),
    EvidenceNode(
        "mechanism_participant_preregistration_candidate",
        "configs/benchmark/mechanism_adaptation_participant_preregistration_rc28.json",
        "protocol_input",
        ("live_llm_methods", "mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_diagnostic_relation_graph",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc29.json",
        "generated_current",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_sample_size_audit",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-sample-size-audit-v0.3.0-rc29.json",
        "generated_current",
        ("mechanism_gate_a_plan", "mechanism_protocol"),
    ),
    EvidenceNode(
        "mechanism_preregistration",
        "configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc29.json",
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
        "workstreams/flagship_tasks/reports/confirmatory-task-semantics-audit-rc29.json",
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
        "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc29.json",
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
        "mechanism-adaptation-release-qualification-v0.1-rc29.json",
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
        (
            "scripts/plan_mechanism_adaptation_matrix.py",
            "--protocol",
            "configs/benchmark/mechanism_adaptation_v0.3.0_rc29.json",
            "--output",
            "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-public-matrix.json",
        ),
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
        (
            "scripts/check_mechanism_adaptation_protocol.py",
            "--protocol",
            "configs/benchmark/mechanism_adaptation_v0.3.0_rc29.json",
            "--gate-a-plan",
            "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc29.json",
            "--semantics-audit",
            "workstreams/flagship_tasks/reports/confirmatory-task-semantics-audit-rc29.json",
            "--output",
            "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-preflight.json",
            "--skip-pending-state-outputs",
        ),
    ),
    EvidenceNode(
        "mechanism_a2_structural_receipt",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-a2-structural-receipt-v0.1-rc29.json",
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
        "mechanism-adaptation-a3-structural-receipt-v0.1-rc29.json",
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
        "workstreams/flagship_tasks/reports/mechanism-adaptation-public-decision-v0.1-rc29.json",
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
        "workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json",
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
        FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
        FIRST_PAPER_COMPOSITION_QUALIFICATION_PATH,
        "formal_result",
        ("task_design_matrix",),
    ),
    EvidenceNode(
        FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID,
        FIRST_PAPER_DETERMINISTIC_USE_CASES_PATH,
        "formal_result",
        (
            "task_design_matrix",
            FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
            "work_i_world_fork_qualification",
        ),
    ),
    EvidenceNode(
        FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID,
        FIRST_PAPER_AGENT_INSTRUMENT_USE_PATH,
        "formal_result",
        (
            FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
            FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID,
            "work_i_world_fork_qualification",
        ),
    ),
    EvidenceNode(
        "work_i_world_fork_qualification",
        "workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json",
        "formal_result",
    ),
    EvidenceNode(
        "work_i_world_fork_certificate",
        "workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json",
        "release_attestation",
        ("work_i_world_fork_qualification",),
    ),
    EvidenceNode(
        "work_i_known_policy_formal_audit",
        "workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json",
        "formal_result",
    ),
    EvidenceNode(
        "work_i_known_policy_validity_report",
        "workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json",
        "formal_result",
        ("work_i_known_policy_formal_audit",),
    ),
    EvidenceNode(
        "work_i_known_policy_delivery_manifest",
        "workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.manifest.json",
        "release_attestation",
        (
            "work_i_known_policy_formal_audit",
            "work_i_known_policy_validity_report",
        ),
    ),
    EvidenceNode(
        "work_i_latent_terminal_estimand_contract",
        "configs/benchmark/work_i_latent_terminal_contract_v0.1.json",
        "protocol_input",
    ),
    EvidenceNode(
        "work_i_latent_terminal_reconstructability",
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json",
        "development_diagnostic",
        ("work_i_latent_terminal_estimand_contract",),
    ),
    EvidenceNode(
        "work_i_latent_terminal_replay_qualification",
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-replay-qualification-v0.1.json",
        "development_diagnostic",
        (
            "work_i_latent_terminal_estimand_contract",
            "work_i_latent_terminal_reconstructability",
        ),
    ),
    EvidenceNode(
        "work_i_latent_terminal_formal_shadow",
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json",
        "formal_result",
        (
            "work_i_latent_terminal_estimand_contract",
            "work_i_latent_terminal_reconstructability",
            "work_i_latent_terminal_replay_qualification",
        ),
    ),
    EvidenceNode(
        "work_i_latent_terminal_analysis",
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json",
        "formal_result",
        (
            "work_i_latent_terminal_estimand_contract",
            "work_i_latent_terminal_formal_shadow",
        ),
    ),
    EvidenceNode(
        "work_i_incremental_data_contract",
        "configs/benchmark/work_i_incremental_data_contract_v0.1.json",
        "protocol_input",
        (
            "work_i_world_fork_qualification",
            "work_i_world_fork_certificate",
            "work_i_known_policy_validity_report",
            "work_i_known_policy_delivery_manifest",
            "work_i_latent_terminal_estimand_contract",
            "work_i_latent_terminal_reconstructability",
            "work_i_latent_terminal_replay_qualification",
        ),
    ),
    EvidenceNode(
        "work_i_fvl_derived_data",
        "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json",
        "frozen_derived_data",
        (
            "work_i_incremental_data_contract",
            "work_i_world_fork_qualification",
            "work_i_world_fork_certificate",
            "work_i_known_policy_formal_audit",
            "work_i_known_policy_validity_report",
            "work_i_known_policy_delivery_manifest",
            "work_i_latent_terminal_estimand_contract",
            "work_i_latent_terminal_reconstructability",
            "work_i_latent_terminal_formal_shadow",
            "work_i_latent_terminal_analysis",
        ),
    ),
    EvidenceNode(
        "work_i_fvl_derived_manifest",
        "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.manifest.json",
        "release_attestation",
        ("work_i_fvl_derived_data",),
    ),
    EvidenceNode(
        "pre_arxiv_claim_evidence_ledger",
        "workstreams/flagship_tasks/reports/pre-arxiv-claim-evidence-ledger-v1.json",
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
        "frozen_derived_data",
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
        return "frozen_current_preregistration_evidence"
    if node.command is not None:
        return "python " + " ".join(node.command)
    return {
        "protocol_input": "maintainer_versioned_input",
        "formal_result": "frozen_formal_execution",
        "release_attestation": "frozen_release_qualification",
        "development_diagnostic": "versioned_development_execution",
        "fixture": "maintainer_versioned_fixture",
        "frozen_derived_data": "frozen_d03_source_bound_assembly",
    }[node.role]


def _node_source_binding(node: EvidenceNode) -> str:
    if node.node_id == FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID:
        return "execution_commit_and_source_blob_sha256"
    if node.node_id == FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID:
        return "execution_commit_source_blobs_and_current_evidence_sha256"
    if node.node_id == FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID:
        return "execution_commit_source_blobs_current_evidence_and_provider_receipts"
    return {
        "protocol_input": "content_sha256",
        "generated_current": "dependencies_and_source_commit",
        "formal_result": "protocol_plan_and_result_sha256",
        "release_attestation": ("preregistered_source_commit_and_protocol_plan_sha256"),
        "development_diagnostic": "content_and_versioned_source_sha256",
        "fixture": "content_sha256",
        "frozen_derived_data": "immutable_source_manifest_sha256",
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
    CurrentPathRule(
        ("publication", "composition_qualification_report"),
        "formal_result",
    ),
    CurrentPathRule(
        ("publication", "deterministic_use_case_qualification_report"),
        "formal_result",
    ),
    CurrentPathRule(
        ("publication", "agent_instrument_use_report"),
        "formal_result",
    ),
    CurrentPathRule(("work_i_fvl", "data_contract"), "protocol_input"),
    CurrentPathRule(("work_i_fvl", "world_fork_report"), "formal_result"),
    CurrentPathRule(("work_i_fvl", "world_fork_certificate"), "release_attestation"),
    CurrentPathRule(("work_i_fvl", "policy_audit"), "formal_result"),
    CurrentPathRule(("work_i_fvl", "policy_report"), "formal_result"),
    CurrentPathRule(("work_i_fvl", "policy_manifest"), "release_attestation"),
    CurrentPathRule(("work_i_fvl", "latent_contract"), "protocol_input"),
    CurrentPathRule(("work_i_fvl", "latent_formal_report"), "formal_result"),
    CurrentPathRule(("work_i_fvl", "latent_analysis"), "formal_result"),
    CurrentPathRule(("work_i_fvl", "derived_data"), "frozen_derived_data"),
    CurrentPathRule(("work_i_fvl", "derived_manifest"), "release_attestation"),
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
    allowed_codes = (
        {0, 1}
        if node.node_id in {"backend_candidate", "mechanism_preflight"}
        else {0}
    )
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
    expected_execution_binding = gate_a_execution_contract_binding(protocol, plan)
    return bool(
        receipt.get("schema_version") == STRUCTURAL_RECEIPT_VERSION
        and receipt.get("stage") == stage
        and receipt.get("protocol_sha256") == _canonical_sha256(protocol)
        and receipt.get("gate_a_plan_sha256") == _canonical_sha256(plan)
        and receipt.get("structurally_complete") is True
        and receipt.get("observed_completed_trial_count") == receipt.get("expected_trial_count")
        and isinstance(receipt.get("expected_trial_count"), int)
        and receipt.get("expected_trial_count", 0) > 0
        and isinstance(receipt.get("trial_manifest_count"), int)
        and receipt.get("trial_manifest_count", 0) > 0
        and isinstance(receipt.get("trial_manifests_sha256"), str)
        and isinstance(receipt.get("source_report_sha256"), str)
        and receipt.get("metric_embargo") == "active"
        and receipt.get("scientific_metrics_disclosed") is False
        and receipt.get("execution_contract_binding_sha256")
        == expected_execution_binding["binding_sha256"]
        and receipt.get("runtime_source_tree_sha256")
        == expected_execution_binding["runtime_source_tree_sha256"]
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
        and decision.get("schema_version") == "chemworld-mechanism-public-decision-0.1"
        and decision.get("a2_structural_receipt_sha256") == _canonical_sha256(a2_receipt)
        and decision.get("a3_structural_receipt_sha256") == _canonical_sha256(a3_receipt)
        and decision.get("gate_a_report_sha256") == a2_receipt.get("source_report_sha256")
        and decision.get("a3_report_sha256") == a3_receipt.get("source_report_sha256")
        and decision.get("release_qualification_sha256") == _canonical_sha256(release_qualification)
        and decision.get("metric_embargo") == "released_for_joint_a2_a3_decision"
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


def _embedded_json_hash_matches(
    payload: Mapping[str, Any],
    field: str,
    *,
    ensure_ascii: bool = False,
    additionally_excluded: tuple[str, ...] = (),
) -> bool:
    supplied = payload.get(field)
    if not isinstance(supplied, str) or len(supplied) != 64:
        return False
    candidate = dict(payload)
    candidate.pop(field, None)
    for excluded in additionally_excluded:
        candidate.pop(excluded, None)
    encoded = json.dumps(
        candidate,
        allow_nan=False,
        ensure_ascii=ensure_ascii,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest() == supplied


def _manifest_files_match(payload: Mapping[str, Any]) -> bool:
    files = payload.get("files")
    if not isinstance(files, list) or payload.get("file_count") != len(files):
        return False
    for row in files:
        if not isinstance(row, Mapping):
            return False
        relative = row.get("path")
        if not isinstance(relative, str):
            return False
        path = ROOT / relative
        if not path.is_file():
            return False
        if row.get("bytes") != path.stat().st_size or row.get("sha256") != file_sha256(path):
            return False
    return True


def _work_i_source_binding_current(
    node: EvidenceNode,
    payload: Mapping[str, Any],
) -> bool | None:
    """Validate frozen Work I identities without promoting scientific gate state."""

    if not node.node_id.startswith("work_i_"):
        return None
    if node.node_id == "work_i_incremental_data_contract":
        from chemworld.eval.work_i_data_contract import validate_work_i_data_contract

        return not validate_work_i_data_contract(payload, root=ROOT)
    if node.node_id == "work_i_world_fork_qualification":
        return bool(
            _embedded_json_hash_matches(payload, "report_sha256", ensure_ascii=True)
            and payload.get("passed") is True
            and payload.get("pair_count") == 6
            and payload.get("trace_count") == 24
            and payload.get("provider_call_count") == 0
        )
    if node.node_id == "work_i_world_fork_certificate":
        qualification_path = ROOT / node_map()["work_i_world_fork_qualification"].path
        qualification = load_json_object(qualification_path)
        source = payload.get("source", {})
        return bool(
            _embedded_json_hash_matches(
                payload,
                "certificate_sha256",
                ensure_ascii=True,
                additionally_excluded=("certificate_id",),
            )
            and isinstance(source, Mapping)
            and source.get("formal_report_content_sha256") == qualification.get("report_sha256")
            and source.get("formal_report_file_sha256") == file_sha256(qualification_path)
            and payload.get("result", {}).get("passed") is True
        )
    if node.node_id == "work_i_known_policy_formal_audit":
        counts = payload.get("counts", {})
        return bool(
            _embedded_json_hash_matches(payload, "audit_sha256")
            and payload.get("status") == "passed"
            and payload.get("passed") is True
            and isinstance(counts, Mapping)
            and counts.get("campaigns") == 30
            and counts.get("closed_lifecycles") == 180
            and counts.get("provider_calls") == 0
        )
    if node.node_id == "work_i_known_policy_validity_report":
        audit_path = ROOT / node_map()["work_i_known_policy_formal_audit"].path
        audit = load_json_object(audit_path)
        formal_binding = payload.get("input_bindings", {}).get("formal_audit", {})
        estimand = payload.get("estimand", {})
        return bool(
            _embedded_json_hash_matches(payload, "report_sha256")
            and payload.get("status") == "positive_control_established"
            and isinstance(formal_binding, Mapping)
            and formal_binding.get("audit_sha256") == audit.get("audit_sha256")
            and formal_binding.get("file_sha256") == file_sha256(audit_path)
            and isinstance(estimand, Mapping)
            and estimand.get("primary_campaigns") == 30
            and estimand.get("primary_closed_lifecycles") == 180
            and estimand.get("provider_calls") == 0
            and estimand.get("retest_in_primary_estimand") is False
        )
    if node.node_id == "work_i_known_policy_delivery_manifest":
        report = load_json_object(ROOT / node_map()["work_i_known_policy_validity_report"].path)
        audit = load_json_object(ROOT / node_map()["work_i_known_policy_formal_audit"].path)
        bindings = payload.get("bindings", {})
        entries = payload.get("entries", [])
        entries_current = isinstance(entries, list) and all(
            isinstance(row, Mapping)
            and isinstance(row.get("path"), str)
            and (ROOT / str(row["path"])).is_file()
            and row.get("byte_count") == (ROOT / str(row["path"])).stat().st_size
            and row.get("file_sha256") == file_sha256(ROOT / str(row["path"]))
            for row in entries
        )
        return bool(
            _embedded_json_hash_matches(payload, "delivery_manifest_sha256")
            and payload.get("status") == "complete"
            and payload.get("immutable") is True
            and payload.get("entry_count") == len(entries)
            and entries_current
            and isinstance(bindings, Mapping)
            and bindings.get("report_sha256") == report.get("report_sha256")
            and bindings.get("formal_audit_sha256") == audit.get("audit_sha256")
        )
    if node.node_id == "work_i_latent_terminal_estimand_contract":
        from chemworld.eval.latent_terminal_contract import validate_latent_terminal_contract

        return not validate_latent_terminal_contract(payload, root=ROOT)
    if node.node_id == "work_i_latent_terminal_reconstructability":
        from chemworld.eval.latent_terminal_reconstructability import (
            validate_reconstructability_report,
        )

        return not validate_reconstructability_report(payload, root=ROOT)
    if node.node_id == "work_i_latent_terminal_replay_qualification":
        census = payload.get("census", {})
        return bool(
            _embedded_json_hash_matches(payload, "report_sha256")
            and payload.get("status") == "PASS"
            and isinstance(census, Mapping)
            and census.get("agent_provider_calls") == 0
            and census.get("formal_checkpoint_payloads_loaded") == 0
            and census.get("formal_shadow_terminal_evaluations_executed") == 0
            and census.get("formal_latent_discard_scores_accessed") == 0
        )
    if node.node_id == "work_i_latent_terminal_formal_shadow":
        receipts = payload.get("receipts", [])
        return bool(
            _embedded_json_hash_matches(payload, "report_sha256")
            and payload.get("status") == "FAIL"
            and isinstance(receipts, list)
            and len(receipts) == 36
            and sum(row.get("outcome_status") == "resolved" for row in receipts) == 6
            and sum(row.get("outcome_status") == "unresolved" for row in receipts) == 30
            and payload.get("contract_sha256")
            == load_json_object(
                ROOT / node_map()["work_i_latent_terminal_estimand_contract"].path
            ).get("contract_sha256")
        )
    if node.node_id == "work_i_latent_terminal_analysis":
        from chemworld.eval.latent_terminal_analysis import validate_latent_terminal_analysis

        census = payload.get("census", {})
        missingness = payload.get("missingness_and_censoring", {})
        return bool(
            not validate_latent_terminal_analysis(payload)
            and payload.get("status") == "incomplete_full_report_required"
            and isinstance(census, Mapping)
            and census.get("resolved_shadow_receipts") == 6
            and census.get("unresolved_shadow_receipts") == 30
            and isinstance(missingness, Mapping)
            and missingness.get("complete_case_primary_used") is False
        )
    if node.node_id == "work_i_fvl_derived_data":
        incremental = payload.get("work_i_incremental", {})
        counts = incremental.get("record_counts", {}) if isinstance(incremental, Mapping) else {}
        contract = load_json_object(ROOT / node_map()["work_i_incremental_data_contract"].path)
        return bool(
            _embedded_json_hash_matches(payload, "derived_data_sha256")
            and payload.get("status") == "frozen_complete"
            and isinstance(incremental, Mapping)
            and incremental.get("data_contract_sha256") == contract.get("contract_sha256")
            and counts
            == {
                "F": {
                    "world_fork_expectations": 12,
                    "world_fork_pairs": 6,
                    "world_fork_traces": 24,
                },
                "L": {
                    "campaign_cells": 10,
                    "latent_discard_units": 36,
                    "terminal_lifecycles": 60,
                },
                "V": {
                    "policy_campaign_profiles": 30,
                    "policy_lifecycles": 180,
                    "policy_retest_campaigns": 30,
                },
            }
            and incremental.get("scientific_boundaries", {}).get(
                "latent_complete_case_substitution_used"
            )
            is False
            and incremental.get("scientific_boundaries", {}).get(
                "raw_hidden_state_or_provider_payloads_included"
            )
            is False
        )
    if node.node_id == "work_i_fvl_derived_manifest":
        derived_path = ROOT / node_map()["work_i_fvl_derived_data"].path
        derived = load_json_object(derived_path)
        return bool(
            _embedded_json_hash_matches(payload, "manifest_sha256")
            and payload.get("status") == "frozen"
            and payload.get("immutable") is True
            and payload.get("derived_data_sha256") == derived.get("derived_data_sha256")
            and _manifest_files_match(payload)
        )
    return False


def _git_blob(commit: str, path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout


def _git_blob_sha256(commit: str, path: str) -> str | None:
    blob = _git_blob(commit, path)
    return hashlib.sha256(blob).hexdigest() if blob is not None else None


def _task_design_matrix_semantics_match_execution(
    commit: str,
    path: str,
) -> bool:
    blob = _git_blob(commit, path)
    if blob is None:
        return False
    executed = json.loads(blob)
    current = load_json_object(ROOT / path)
    for payload in (executed, current):
        payload.pop("source_commit", None)
        payload.pop("source_tree_dirty", None)
    return _canonical_sha256(executed) == _canonical_sha256(current)


def _git_commit_is_ancestor(commit: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        ).returncode
        == 0
    )


def _git_paths_unchanged_since(commit: str, paths: tuple[str, ...]) -> bool:
    committed = subprocess.run(
        ["git", "diff", "--quiet", commit, "HEAD", "--", *paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    worktree = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "HEAD", "--", *paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", *paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    return bool(
        committed.returncode == worktree.returncode == staged.returncode == 0
        and status.returncode == 0
        and not status.stdout
    )


def _first_paper_composition_qualification_binding_errors(
    payload: Mapping[str, Any],
) -> list[str]:
    """Validate the immutable C/D qualification against its execution sources."""

    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    try:
        from chemworld.eval.composition_qualification import (
            _failure_counts,
            _receipt_completeness_errors,
        )

        require(
            payload.get("schema_version")
            == "chemworld-first-paper-composition-qualification-report-0.2",
            "composition qualification schema is stale",
        )
        require(
            payload.get("qualification_id") == "first-paper-composition-qualification-v1",
            "composition qualification identity is stale",
        )
        require(
            payload.get("status") == "passed",
            "composition qualification did not pass",
        )

        task_structure = payload.get("task_structure")
        reference = payload.get("reference_qualification")
        generated = payload.get("generated_qualification")
        mutants = payload.get("compile_mutants")
        modules = payload.get("module_qualification")
        interfaces = payload.get("interface_qualification")
        completeness = payload.get("receipt_completeness")
        summary = payload.get("summary")
        if not all(
            isinstance(part, dict)
            for part in (
                task_structure,
                reference,
                generated,
                mutants,
                modules,
                interfaces,
                completeness,
                summary,
            )
        ):
            return ["composition qualification sections are malformed"]

        units = reference.get("units")
        generated_cases = generated.get("cases")
        compile_mutants = mutants.get("mutants")
        module_probes = modules.get("probes")
        interface_paths = interfaces.get("paths")
        if not all(
            isinstance(rows, list)
            for rows in (
                units,
                generated_cases,
                compile_mutants,
                module_probes,
                interface_paths,
            )
        ):
            return ["composition qualification case lists are malformed"]
        reference_recipes = [case for unit in units for case in unit.get("valid_recipe_cases", [])]
        negative_probes = [probe for unit in units for probe in unit.get("negative_probes", [])]
        unseen = [
            case
            for case in generated_cases
            if case.get("pattern") == generated.get("unseen_pattern")
        ]

        detailed_counts = {
            "reference_units": len(units),
            "reference_recipes": len(reference_recipes),
            "negative_probes": len(negative_probes),
            "generated_compositions": len(generated_cases),
            "unseen_distillation_compositions": len(unseen),
            "compile_mutants": len(compile_mutants),
            "module_probes": len(module_probes),
            "interface_paths": len(interface_paths),
        }
        expected_counts = {
            "reference_units": 64,
            "reference_recipes": 1786,
            "negative_probes": 192,
            "generated_compositions": 52,
            "unseen_distillation_compositions": 8,
            "compile_mutants": 7,
            "module_probes": 32,
            "interface_paths": 7,
        }
        for key, expected in expected_counts.items():
            row = summary.get(key)
            require(
                isinstance(row, Mapping)
                and row.get("passed") == row.get("denominator") == expected,
                f"composition qualification summary count is stale: {key}",
            )
            require(
                detailed_counts[key] == expected,
                f"composition qualification detailed count is stale: {key}",
            )

        require(
            task_structure.get("registered_task_count") == 15
            and len(task_structure.get("tasks", [])) == 15
            and task_structure.get("world_unit_count") == 64,
            "composition qualification task-structure count is stale",
        )
        require(
            reference.get("unit_passed") == reference.get("unit_denominator") == 64
            and reference.get("recipe_passed") == reference.get("recipe_denominator") == 1786
            and reference.get("negative_probe_passed")
            == reference.get("negative_probe_denominator")
            == 192,
            "composition qualification reference counts are stale",
        )
        require(
            generated.get("passed") == generated.get("denominator") == 52
            and generated.get("unseen_passed") == generated.get("unseen_denominator") == 8,
            "composition qualification generated counts are stale",
        )
        require(
            mutants.get("passed") == mutants.get("denominator") == 7,
            "composition qualification mutant counts are stale",
        )
        require(
            modules.get("passed") == modules.get("denominator") == 32,
            "composition qualification module counts are stale",
        )
        require(
            interfaces.get("passed") == interfaces.get("denominator") == 7,
            "composition qualification interface counts are stale",
        )
        require(
            all(unit.get("passed") is True for unit in units)
            and all(case.get("passed") is True for case in reference_recipes)
            and all(probe.get("passed") is True for probe in negative_probes)
            and all(case.get("passed") is True for case in generated_cases)
            and all(mutant.get("passed") is True for mutant in compile_mutants)
            and all(probe.get("passed") is True for probe in module_probes)
            and all(path.get("passed") is True for path in interface_paths),
            "composition qualification contains a failed independent receipt",
        )

        require(
            completeness
            == {
                "passed": True,
                "error_count": 0,
                "errors": [],
                "failures": [],
            },
            "composition qualification receipt completeness failed",
        )
        require(
            isinstance(summary.get("failure_class_counts"), Mapping)
            and not summary.get("failure_class_counts"),
            "composition qualification reports failure classes",
        )
        require(
            summary.get("missing_receipt_count") == 0,
            "composition qualification reports missing receipts",
        )
        require(
            summary.get("public_private_leakage_count") == 0,
            "composition qualification reports public/private leakage",
        )
        require(
            generated.get("unseen_pattern") == "reaction-distillation-observation"
            and generated.get("unseen_reference_task_id_overlap") == [],
            "composition qualification unseen-world identity is stale",
        )

        completeness_errors = _receipt_completeness_errors(
            task_structure=task_structure,
            reference=reference,
            generated=generated,
            modules=modules,
            interfaces=interfaces,
        )
        require(
            not completeness_errors,
            "composition qualification completeness recomputation failed",
        )
        require(
            not _failure_counts([reference, generated, mutants, modules, interfaces, completeness]),
            "composition qualification failure recomputation failed",
        )

        require(
            len(unseen) == 8
            and [case.get("generation_index") for case in unseen] == list(range(8))
            and {case.get("generation_seed") for case in unseen} == {105}
            and unseen[0].get("composition_id")
            == "qualification-reaction-distillation-observation-coverage-0001"
            and unseen[0].get("composition_request_sha256")
            == "687007fb2fe9e7cb7bde1eff10219469fecc73903648d2fa34fec17c10694b4f",
            "composition qualification frozen unseen sequence is stale",
        )

        source = payload.get("source_binding")
        if not isinstance(source, Mapping):
            return ["composition qualification source binding is malformed"]
        expected_sources = {
            "experiment_note": (
                "workstreams/arxiv_v1/experiments/first-paper-composition-qualification.md"
            ),
            "current_registry": "configs/current.json",
            "task_design_matrix": ("workstreams/flagship_tasks/reports/task-design-matrix-v1.json"),
        }
        commit = source.get("execution_commit")
        require(
            isinstance(commit, str)
            and len(commit) == 40
            and all(character in "0123456789abcdef" for character in commit)
            and source.get("status") == "passed"
            and source.get("qualification_design_version")
            == QUALIFICATION_DESIGN_VERSION
            and _git_commit_is_ancestor(commit),
            "composition qualification execution commit is invalid",
        )
        if isinstance(commit, str):
            for field, expected_path in expected_sources.items():
                require(
                    source.get(field) == expected_path,
                    f"composition qualification source path is stale: {field}",
                )
                require(
                    _git_blob_sha256(commit, expected_path) == source.get(f"{field}_sha256"),
                    f"composition qualification source blob is stale: {field}",
                )
            require(
                file_sha256(ROOT / expected_sources["experiment_note"])
                == source.get("experiment_note_sha256"),
                "composition qualification experiment note changed after execution",
            )
            require(
                _task_design_matrix_semantics_match_execution(
                    commit,
                    expected_sources["task_design_matrix"],
                ),
                "composition qualification task-design semantics changed after execution",
            )
            require(
                _git_paths_unchanged_since(
                    commit,
                    FIRST_PAPER_COMPOSITION_QUALIFICATION_GUARDED_PATHS,
                ),
                "composition qualification runtime changed after execution",
            )
    except (KeyError, OSError, subprocess.SubprocessError, TypeError, ValueError) as error:
        errors.append(f"composition qualification validator error: {error}")
    return errors


def _first_paper_composition_qualification_binding_current(
    payload: Mapping[str, Any],
) -> bool:
    return not _first_paper_composition_qualification_binding_errors(payload)


def _first_paper_deterministic_use_case_binding_errors(
    payload: Mapping[str, Any],
) -> list[str]:
    """Validate the immutable deterministic use-case census and source bindings."""

    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    try:
        from chemworld.eval.deterministic_use_cases import (
            EXPECTED_ACTION_SHA256,
            EXPECTED_CASE_COUNT,
            EXPECTED_COMMITTED_ACTION_COUNT,
            EXPECTED_FINAL_ASSAY_COUNT,
            EXPECTED_ROLLBACK_COUNT,
            EXPECTED_SUBMITTED_ACTION_COUNT,
            QUALIFICATION_ID,
            REPORT_SCHEMA_VERSION,
            _failure_class_counts,
            _receipt_completeness_errors,
        )
        from chemworld.tasks import TASK_CONTRACT_VERSION

        expected_cases = {
            "U01": ("reaction-to-crystallization", 0, 12, 12, 0),
            "U02": ("composed-equilibrium-characterization-demo", 0, 5, 5, 0),
            "U03/E01": ("composed-reaction-purification-demo", 0, 19, 18, 1),
            "U06-flow": ("flow-reaction-optimization", 0, 8, 8, 0),
            "U06-electro": ("electrochemical-conversion", 0, 11, 11, 0),
            "U06-distillation": ("reaction-to-distillation", 0, 12, 12, 0),
            "U06-partition": ("partition-discovery", 0, 10, 10, 0),
            "U06-crystallization": ("reaction-to-crystallization", 1, 12, 12, 0),
        }
        expected_case_sources = {
            "U01": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
            "U02": {
                "examples/world-authoring/use-case-reference-paths-v0.1.json",
                "examples/world-authoring/composed-equilibrium-characterization-v0.1.json",
            },
            "U03/E01": {
                "examples/world-authoring/use-case-reference-paths-v0.1.json",
                "examples/world-authoring/composed-reaction-purification-v0.1.json",
            },
            "U06-flow": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
            "U06-electro": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
            "U06-distillation": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
            "U06-partition": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
            "U06-crystallization": {
                "src/chemworld/tasks.py",
                "src/chemworld/agents/task_recipes.py",
            },
        }

        require(
            payload.get("schema_version") == REPORT_SCHEMA_VERSION,
            "deterministic use-case qualification schema is stale",
        )
        require(
            payload.get("qualification_id") == QUALIFICATION_ID,
            "deterministic use-case qualification identity is stale",
        )
        require(
            payload.get("status") == "passed",
            "deterministic use-case qualification did not pass",
        )
        require(
            payload.get("provider_call_count") == 0,
            "deterministic use-case qualification reports provider calls",
        )
        require(
            payload.get("denominators")
            == {
                "case_count": EXPECTED_CASE_COUNT,
                "submitted_action_count": EXPECTED_SUBMITTED_ACTION_COUNT,
                "committed_action_count": EXPECTED_COMMITTED_ACTION_COUNT,
                "rolled_back_action_count": EXPECTED_ROLLBACK_COUNT,
                "final_assay_count": EXPECTED_FINAL_ASSAY_COUNT,
            },
            "deterministic use-case qualification denominators are stale",
        )

        cases = payload.get("cases")
        if not isinstance(cases, list):
            return ["deterministic use-case case list is malformed"]
        cases_by_id = {case.get("case_id"): case for case in cases if isinstance(case, Mapping)}
        require(
            len(cases) == len(cases_by_id) == EXPECTED_CASE_COUNT
            and set(cases_by_id) == set(expected_cases),
            "deterministic use-case identities or case denominator are stale",
        )

        submitted = checked = committed = rollbacks = final_assays = passed_cases = 0
        leakage_count = 0
        for case_id, expected in expected_cases.items():
            case = cases_by_id.get(case_id)
            if not isinstance(case, Mapping):
                continue
            identity, seed, expected_submitted, expected_committed, expected_rollbacks = expected
            actions = case.get("actions")
            receipts = case.get("step_receipts")
            expected_validation = case.get("expected_validation")
            expected_transactions = case.get("expected_transactions")
            if not all(
                isinstance(rows, list)
                for rows in (actions, receipts, expected_validation, expected_transactions)
            ):
                errors.append(f"deterministic use-case action receipts are malformed: {case_id}")
                continue

            require(
                case.get("public_identity") == identity
                and case.get("identity") == identity
                and case.get("seed") == seed,
                f"deterministic use-case identity binding is stale: {case_id}",
            )
            require(
                len(actions)
                == len(receipts)
                == len(expected_validation)
                == len(expected_transactions)
                == expected_submitted,
                f"deterministic use-case action denominator is stale: {case_id}",
            )
            expected_action_sha = EXPECTED_ACTION_SHA256[case_id]
            require(
                case.get("actions_sha256")
                == case.get("action_list_sha256")
                == expected_action_sha
                == _canonical_sha256(actions),
                f"deterministic use-case frozen action path is stale: {case_id}",
            )

            observed_commits = observed_rollbacks = observed_final_assays = 0
            for step_number, (action, receipt) in enumerate(
                zip(actions, receipts, strict=True), start=1
            ):
                if not isinstance(action, Mapping) or not isinstance(receipt, Mapping):
                    errors.append(
                        f"deterministic use-case step receipt is malformed: {case_id}.{step_number}"
                    )
                    continue
                expected_valid = expected_validation[step_number - 1]
                expected_status = expected_transactions[step_number - 1]
                validation = receipt.get("schema_validation")
                transaction = receipt.get("transaction")
                resource = receipt.get("resource_reconciliation")
                constitution = receipt.get("constitution_checks")
                require(
                    receipt.get("step") == step_number
                    and receipt.get("action") == action
                    and receipt.get("action_sha256") == _canonical_sha256(action)
                    and receipt.get("expected_validation") is expected_valid
                    and receipt.get("expected_transaction_status") == expected_status,
                    f"deterministic use-case step binding is stale: {case_id}.{step_number}",
                )
                require(
                    isinstance(validation, Mapping) and validation.get("valid") is expected_valid,
                    f"deterministic use-case validation receipt failed: {case_id}.{step_number}",
                )
                require(
                    isinstance(transaction, Mapping)
                    and transaction.get("status") == expected_status
                    and transaction.get("operation_committed") is (expected_status == "committed"),
                    f"deterministic use-case transaction receipt failed: {case_id}.{step_number}",
                )
                require(
                    isinstance(constitution, list)
                    and all(
                        isinstance(check, Mapping) and check.get("passed") is True
                        for check in constitution
                    ),
                    f"deterministic use-case constitution receipt failed: {case_id}.{step_number}",
                )
                require(
                    isinstance(receipt.get("world_events"), list)
                    and bool(receipt.get("world_events"))
                    and receipt.get("event_propagation_matches_operation") is True,
                    f"deterministic use-case event receipt failed: {case_id}.{step_number}",
                )
                require(
                    isinstance(receipt.get("resource_preflight"), Mapping)
                    and isinstance(receipt.get("resource_outcome_delta"), Mapping)
                    and isinstance(resource, Mapping)
                    and resource.get("resource_reconciled") is True
                    and resource.get("reconciliation_mismatches") == [],
                    f"deterministic use-case resource receipt failed: {case_id}.{step_number}",
                )
                require(
                    isinstance(receipt.get("public_observation"), Mapping)
                    and receipt.get("leakage_findings") == []
                    and receipt.get("failures") == []
                    and receipt.get("passed") is True,
                    f"deterministic use-case public step receipt failed: {case_id}.{step_number}",
                )
                if isinstance(transaction, Mapping):
                    observed_commits += transaction.get("status") == "committed"
                    observed_rollbacks += transaction.get("status") == "rolled_back"
                    observed_final_assays += bool(
                        action.get("operation") == "measure"
                        and action.get("instrument") == "final_assay"
                        and transaction.get("status") == "committed"
                    )

            require(
                case.get("submitted_action_count")
                == case.get("checked_action_count")
                == expected_submitted,
                f"deterministic use-case checked count is stale: {case_id}",
            )
            require(
                case.get("committed_action_count") == observed_commits == expected_committed,
                f"deterministic use-case commit count is stale: {case_id}",
            )
            require(
                case.get("rollback_count")
                == case.get("rolled_back_action_count")
                == observed_rollbacks
                == expected_rollbacks,
                f"deterministic use-case rollback count is stale: {case_id}",
            )
            require(
                case.get("committed_final_assay_count")
                == case.get("final_assay_count")
                == observed_final_assays
                == 1,
                f"deterministic use-case final-assay count is stale: {case_id}",
            )

            termination = case.get("termination_receipt")
            post_termination = (
                termination.get("post_termination_validation")
                if isinstance(termination, Mapping)
                else None
            )
            require(
                isinstance(termination, Mapping)
                and termination.get("closed") is True
                and termination.get("committed_terminate_count") == 1
                and termination.get("committed_final_assay_count") == 1
                and termination.get("final_terminated") is True
                and termination.get("final_truncated") is False
                and termination.get("right_censored_open_batch") is False
                and isinstance(post_termination, Mapping)
                and post_termination.get("passed") is True,
                f"deterministic use-case lifecycle receipt failed: {case_id}",
            )
            case_resource = case.get("resource_receipt")
            require(
                isinstance(case_resource, Mapping)
                and case_resource.get("resource_reconciled") is True
                and case_resource.get("reconciliation_mismatches") == []
                and case_resource.get("preflight", {}).get("receipt_count") == expected_submitted
                and case_resource.get("outcome_delta", {}).get("operations_committed")
                == expected_committed,
                f"deterministic use-case aggregate resource receipt failed: {case_id}",
            )
            replay = case.get("exact_replay")
            require(
                isinstance(replay, Mapping)
                and replay.get("verified") is True
                and replay.get("checked_steps") == expected_submitted
                and replay.get("max_abs_error") == 0.0
                and replay.get("mismatches") == [],
                f"deterministic use-case exact replay failed: {case_id}",
            )
            require(
                case.get("provider_call_count") == 0
                and case.get("public_private_leakage_count") == 0
                and case.get("leakage_findings") == []
                and int(case.get("trajectory_bytes", 0)) > 0
                and case.get("passed") is True
                and case.get("failures") == [],
                f"deterministic use-case completion receipt failed: {case_id}",
            )
            contract = case.get("contract_binding")
            require(
                isinstance(contract, Mapping)
                and contract.get("task_contract_hash_matches") is True
                and contract.get("task_contract_hash")
                == contract.get("expected_task_contract_hash")
                and all(
                    isinstance(contract.get(field), str) and len(contract[field]) == 64
                    for field in (
                        "task_contract_hash",
                        "runtime_profile_hash",
                        "scoring_contract_hash",
                        "observation_contract_hash",
                    )
                ),
                f"deterministic use-case contract binding failed: {case_id}",
            )

            case_sources = case.get("source_bindings")
            if not isinstance(case_sources, list):
                errors.append(f"deterministic use-case source bindings are malformed: {case_id}")
            else:
                source_paths = {
                    source.get("path") for source in case_sources if isinstance(source, Mapping)
                }
                require(
                    len(case_sources) == len(source_paths)
                    and source_paths == expected_case_sources[case_id],
                    f"deterministic use-case source paths are stale: {case_id}",
                )

            if case_id == "U03/E01":
                first = receipts[0] if receipts else None
                recovery = case.get("recovery_receipt")
                ghost = (
                    first.get("rollback_recovery_receipt") if isinstance(first, Mapping) else None
                )
                require(
                    isinstance(first, Mapping)
                    and first.get("action", {}).get("operation") == "separate_phase"
                    and first.get("schema_validation", {}).get("valid") is False
                    and first.get("transaction", {}).get("status") == "rolled_back"
                    and first.get("transaction", {}).get("rollback_reason") == "precondition_failed"
                    and isinstance(ghost, Mapping)
                    and ghost.get("ghost_state_preserved") is True
                    and ghost.get("physical", {}).get("preserved") is True
                    and ghost.get("observation_rng", {}).get("preserved") is True
                    and ghost.get("ledger", {}).get("ghost_state_preserved") is True
                    and ghost.get("process", {}).get("ghost_state_preserved") is True
                    and ghost.get("events", {}).get("reconciled") is True
                    and ghost.get("resource", {}).get("resource_reconciled") is True
                    and isinstance(recovery, Mapping)
                    and recovery.get("passed") is True
                    and recovery.get("observed_rollback_count") == 1
                    and recovery.get("subsequent_expected_commit_count") == 18
                    and recovery.get("subsequent_observed_commit_count") == 18,
                    "deterministic U03 rollback-recovery receipt failed",
                )

            submitted += expected_submitted
            checked += int(case.get("checked_action_count", 0))
            committed += observed_commits
            rollbacks += observed_rollbacks
            final_assays += observed_final_assays
            leakage_count += int(case.get("public_private_leakage_count", 0))
            passed_cases += case.get("passed") is True

        completeness_errors = _receipt_completeness_errors(cases)
        failure_counts = _failure_class_counts(cases, completeness_errors)
        require(
            not completeness_errors
            and payload.get("receipt_completeness")
            == {"passed": True, "error_count": 0, "errors": []},
            "deterministic use-case receipt completeness recomputation failed",
        )
        require(
            not failure_counts and payload.get("failures") == [],
            "deterministic use-case failure census is not empty",
        )
        require(
            payload.get("summary")
            == {
                "cases": {"passed": passed_cases, "denominator": len(cases)},
                "submitted_actions": {
                    "checked": checked,
                    "denominator": submitted,
                    "expected": EXPECTED_SUBMITTED_ACTION_COUNT,
                },
                "committed_actions": {
                    "observed": committed,
                    "expected": EXPECTED_COMMITTED_ACTION_COUNT,
                },
                "rolled_back_actions": {
                    "observed": rollbacks,
                    "expected": EXPECTED_ROLLBACK_COUNT,
                },
                "committed_final_assays": {
                    "observed": final_assays,
                    "expected": EXPECTED_FINAL_ASSAY_COUNT,
                },
                "public_private_leakage_count": leakage_count,
                "missing_receipt_count": len(completeness_errors),
                "failure_class_counts": failure_counts,
                "exact_denominators_passed": True,
            }
            and submitted == checked == EXPECTED_SUBMITTED_ACTION_COUNT
            and committed == EXPECTED_COMMITTED_ACTION_COUNT
            and rollbacks == EXPECTED_ROLLBACK_COUNT
            and final_assays == EXPECTED_FINAL_ASSAY_COUNT
            and passed_cases == EXPECTED_CASE_COUNT
            and leakage_count == 0,
            "deterministic use-case summary census is stale",
        )

        source = payload.get("source_binding")
        if not isinstance(source, Mapping):
            return ["deterministic use-case source binding is malformed"]
        commit = source.get("execution_commit")
        require(
            isinstance(commit, str)
            and len(commit) == 40
            and all(character in "0123456789abcdef" for character in commit)
            and _git_commit_is_ancestor(commit)
            and source.get("branch") == "main"
            and source.get("worktree_clean") is True
            and source.get("task_contract_version") == TASK_CONTRACT_VERSION,
            "deterministic use-case execution commit is invalid",
        )
        expected_launch_sources = {
            "experiment_note": (
                "workstreams/arxiv_v1/experiments/first-paper-deterministic-use-cases.md"
            ),
            "todo": "workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md",
        }
        if isinstance(commit, str):
            for field, expected_path in expected_launch_sources.items():
                binding = source.get(field)
                require(
                    isinstance(binding, Mapping)
                    and binding.get("path") == expected_path
                    and binding.get("sha256") == _git_blob_sha256(commit, expected_path)
                    and isinstance(binding.get("bytes"), int)
                    and binding.get("bytes") > 0,
                    f"deterministic use-case launch source is stale: {field}",
                )
            note_binding = source.get("experiment_note")
            require(
                isinstance(note_binding, Mapping)
                and file_sha256(ROOT / expected_launch_sources["experiment_note"])
                == note_binding.get("sha256"),
                "deterministic use-case experiment note changed after execution",
            )
            for case_id, case in cases_by_id.items():
                if not isinstance(case, Mapping):
                    continue
                for binding in case.get("source_bindings", []):
                    if not isinstance(binding, Mapping):
                        continue
                    relative_path = binding.get("path")
                    if not isinstance(relative_path, str):
                        errors.append(f"deterministic use-case source path is malformed: {case_id}")
                        continue
                    source_path = (ROOT / relative_path).resolve()
                    require(
                        source_path.is_relative_to(ROOT.resolve())
                        and source_path.is_file()
                        and file_sha256(source_path) == binding.get("sha256")
                        and source_path.stat().st_size == binding.get("bytes")
                        and _git_blob_sha256(commit, relative_path) == binding.get("sha256"),
                        f"deterministic use-case source blob is stale: {case_id}:{relative_path}",
                    )
            require(
                _git_paths_unchanged_since(
                    commit,
                    FIRST_PAPER_DETERMINISTIC_USE_CASES_GUARDED_PATHS,
                ),
                "deterministic use-case runtime changed after execution",
            )

        existing = payload.get("existing_evidence")
        if not isinstance(existing, Mapping):
            return ["deterministic use-case existing evidence binding is malformed"]
        require(
            existing.get("current_registry", {}).get("path") == "configs/current.json"
            and isinstance(existing.get("current_registry", {}).get("sha256"), str)
            and len(existing["current_registry"]["sha256"]) == 64,
            "deterministic use-case launch registry binding is malformed",
        )
        expected_existing_nodes = {
            "U04": (
                "work_i_world_fork_qualification",
                "workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json",
            ),
            "U05": (
                FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
                FIRST_PAPER_COMPOSITION_QUALIFICATION_PATH,
            ),
        }
        for use_case_id, (node_id, expected_path) in expected_existing_nodes.items():
            evidence = existing.get(use_case_id)
            binding = evidence.get("binding") if isinstance(evidence, Mapping) else None
            expected_sha = file_sha256(ROOT / expected_path)
            require(
                isinstance(evidence, Mapping)
                and evidence.get("passed") is True
                and isinstance(binding, Mapping)
                and binding.get("node_id") == node_id
                and binding.get("path") == expected_path
                and binding.get("expected_sha256") == binding.get("actual_sha256") == expected_sha
                and binding.get("artifact_state") == "current"
                and binding.get("freshness") == "fresh"
                and binding.get("gate_state") == "passed"
                and binding.get("binding_verified") is True,
                f"deterministic use-case existing evidence binding is stale: {use_case_id}",
            )
        require(
            isinstance(existing.get("U04"), Mapping)
            and existing["U04"].get("pair_count") == 6
            and existing["U04"].get("trace_count") == 24
            and existing["U04"].get("provider_call_count") == 0
            and existing["U04"].get("protocol_id")
            == "chemworld-work-i-world-fork-qualification-v0.1",
            "deterministic use-case U04 evidence summary is stale",
        )
        require(
            isinstance(existing.get("U05"), Mapping)
            and existing["U05"].get("composition_id")
            == "qualification-reaction-distillation-observation-coverage-0001"
            and existing["U05"].get("composition_request_sha256")
            == "687007fb2fe9e7cb7bde1eff10219469fecc73903648d2fa34fec17c10694b4f"
            and existing["U05"].get("generation_seed") == 105
            and existing["U05"].get("generation_index") == 0
            and existing["U05"].get("action_count") == 12
            and existing["U05"].get("exact_replay_verified") is True,
            "deterministic use-case U05 evidence summary is stale",
        )
    except (
        AttributeError,
        KeyError,
        OSError,
        subprocess.SubprocessError,
        TypeError,
        ValueError,
    ) as error:
        errors.append(f"deterministic use-case validator error: {error}")
    return errors


def _first_paper_deterministic_use_case_binding_current(
    payload: Mapping[str, Any],
) -> bool:
    return not _first_paper_deterministic_use_case_binding_errors(payload)


def _first_paper_agent_instrument_use_binding_errors(
    payload: Mapping[str, Any],
) -> list[str]:
    """Validate the immutable successful U05 complete-agent provider unit."""

    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    try:
        require(
            payload.get("schema_version")
            == "chemworld-first-paper-agent-instrument-use-report-0.1",
            "agent instrument-use schema is stale",
        )
        require(
            payload.get("qualification_id") == "first-paper-agent-instrument-use-v1",
            "agent instrument-use identity is stale",
        )
        require(payload.get("status") == "passed", "agent instrument-use did not pass")
        require(payload.get("failures") == [], "agent instrument-use reports failures")
        require(
            payload.get("failure_class_counts") == {},
            "agent instrument-use reports failure classes",
        )
        require(
            payload.get("denominators")
            == {
                "lifecycle_count": 1,
                "model_call_count": 1,
                "provider_session_count": 1,
                "submitted_action_count": 15,
                "trajectory_record_count": 15,
            },
            "agent instrument-use denominators are stale",
        )

        summary = payload.get("summary")
        require(
            isinstance(summary, Mapping)
            and summary.get("submitted_action_count") == 15
            and summary.get("committed_action_count") == 15
            and summary.get("committed_terminate_count") == 1
            and summary.get("committed_final_assay_count") == 1
            and summary.get("rollback_count") == 0
            and summary.get("provider_session_count") == 1
            and summary.get("mcp_step_count") == 15
            and summary.get("trajectory_record_count") == 15
            and summary.get("step_monitor_event_count") == 15
            and summary.get("public_private_leakage_count") == 0,
            "agent instrument-use summary is stale",
        )
        actions = payload.get("actions")
        require(
            isinstance(actions, list)
            and len(actions) == 15
            and [row.get("step") for row in actions] == list(range(1, 16))
            and all(row.get("passed") is True for row in actions)
            and all(row.get("transaction", {}).get("status") == "committed" for row in actions)
            and all(not row.get("failures") for row in actions),
            "agent instrument-use action census is stale",
        )

        lifecycle = payload.get("lifecycle")
        require(
            isinstance(lifecycle, Mapping)
            and lifecycle.get("passed") is True
            and lifecycle.get("right_censored") is False
            and lifecycle.get("submitted_action_count") == 15
            and lifecycle.get("committed_action_count") == 15
            and lifecycle.get("committed_terminate_count") == 1
            and lifecycle.get("committed_final_assay_count") == 1
            and lifecycle.get("rollback_count") == 0
            and all(lifecycle.get("checks", {}).values()),
            "agent instrument-use lifecycle is stale",
        )
        declared = payload.get("declared_resource_budget")
        require(
            isinstance(declared, Mapping)
            and declared.get("passed") is True
            and declared.get("checked_action_count") == 15
            and declared.get("exceeded_resources") == []
            and declared.get("first_exceeded_step") == {}
            and declared.get("declared_limits")
            == {
                "final_assays": 1,
                "instrument_uses": 4,
                "operation_attempts": 16,
                "process_time_s": 10440.0,
                "sample_consumed_L": 0.001,
            }
            and declared.get("observed_usage")
            == {
                "final_assays": 1,
                "instrument_uses": 4,
                "operation_attempts": 15,
                "process_time_s": 8158.454222464699,
                "sample_consumed_L": 0.0008500000000000001,
            }
            and all(declared.get("checks", {}).values()),
            "agent instrument-use declared resources are stale",
        )
        replay = payload.get("exact_replay")
        require(
            replay
            == {
                "checked_steps": 15,
                "max_abs_error": 0.0,
                "mismatches": [],
                "verified": True,
            },
            "agent instrument-use exact replay failed",
        )
        require(
            payload.get("receipt_completeness")
            == {"error_count": 0, "errors": [], "passed": True},
            "agent instrument-use receipts are incomplete",
        )
        require(
            payload.get("public_boundary")
            == {
                "final_payload_summary_retained": False,
                "finding_count": 0,
                "findings": [],
                "private_reasoning_retained": False,
                "raw_provider_payload_retained": False,
                "temporary_workspace_retained": False,
            }
            and payload.get("sanitization")
            == {"finding_count": 0, "findings": [], "passed": True},
            "agent instrument-use public boundary failed",
        )

        preflight = payload.get("provider_preflight")
        require(
            isinstance(preflight, Mapping)
            and preflight.get("verified") is True
            and preflight.get("cli_version_matches") is True
            and preflight.get("expected_cli_version") == "codex-cli 0.145.0"
            and preflight.get("observed_cli_version") == "codex-cli 0.145.0"
            and preflight.get("cached_chatgpt_login_status") == "passed",
            "agent instrument-use provider preflight failed",
        )
        provider = payload.get("provider_accounting")
        usage = provider.get("usage", {}) if isinstance(provider, Mapping) else {}
        breakdown = (
            provider.get("input_token_breakdown", {})
            if isinstance(provider, Mapping)
            else {}
        )
        require(
            isinstance(provider, Mapping)
            and provider.get("passed") is True
            and provider.get("provider_session_count") == 1
            and provider.get("logical_codex_turn_count") == 1
            and provider.get("model_call_count") == 1
            and provider.get("mcp_tool_call_count") == 17
            and provider.get("mcp_step_count") == 15
            and provider.get("accepted_action_count") == 15
            and all(provider.get("session_checks", {}).values())
            and all(provider.get("token_checks", {}).values())
            and all(provider.get("method_checks", {}).values())
            and usage.get("prompt_tokens") == 493092
            and usage.get("prompt_cache_hit_tokens") == 440832
            and usage.get("prompt_cache_miss_tokens") == 52260
            and usage.get("completion_tokens") == 2973
            and breakdown.get("cache_means_reused_input_context_not_repeated_output") is True,
            "agent instrument-use provider accounting is stale",
        )

        frozen = payload.get("frozen_experiment")
        require(
            isinstance(frozen, Mapping)
            and frozen.get("composition_request_sha256")
            == "687007fb2fe9e7cb7bde1eff10219469fecc73903648d2fa34fec17c10694b4f"
            and frozen.get("public_compiled_task_subobject_hash")
            == "2d89a69f68d910dc8593a6ccfad698b108114a5295d18a4c362aad59155c497d"
            and frozen.get("runtime_contract_binding", {}).get("task_contract_hash")
            == "9b775c56b1cfe07dc75afc355d4815077913b27cbeedf20d32fb21d9dadf9f14",
            "agent instrument-use frozen task binding is stale",
        )

        existing = payload.get("existing_evidence")
        expected_existing = {
            "U04": (
                "work_i_world_fork_qualification",
                "workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json",
            ),
            "U05": (
                FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
                FIRST_PAPER_COMPOSITION_QUALIFICATION_PATH,
            ),
        }
        require(isinstance(existing, Mapping), "agent instrument-use evidence is malformed")
        if isinstance(existing, Mapping):
            for key, (node_id, expected_path) in expected_existing.items():
                evidence = existing.get(key)
                binding = evidence.get("binding") if isinstance(evidence, Mapping) else None
                expected_sha = file_sha256(ROOT / expected_path)
                require(
                    isinstance(binding, Mapping)
                    and binding.get("node_id") == node_id
                    and binding.get("path") == expected_path
                    and binding.get("expected_sha256")
                    == binding.get("actual_sha256")
                    == expected_sha
                    and binding.get("binding_verified") is True,
                    f"agent instrument-use current evidence is stale: {key}",
                )

        source = payload.get("source_binding")
        if not isinstance(source, Mapping):
            return [*errors, "agent instrument-use source binding is malformed"]
        commit = source.get("execution_commit")
        require(
            isinstance(commit, str)
            and len(commit) == 40
            and _git_commit_is_ancestor(commit)
            and source.get("branch") == "main"
            and source.get("worktree_clean") is True,
            "agent instrument-use execution commit is invalid",
        )
        if isinstance(commit, str):
            for field in (
                "experiment_note",
                "evaluator",
                "runner",
                "interactive_agent",
                "execution_script",
            ):
                binding = source.get(field)
                relative_path = binding.get("path") if isinstance(binding, Mapping) else None
                require(
                    isinstance(relative_path, str)
                    and _git_blob_sha256(commit, relative_path) == binding.get("sha256"),
                    f"agent instrument-use source blob is stale: {field}",
                )
            require(
                _git_paths_unchanged_since(
                    commit,
                    FIRST_PAPER_AGENT_INSTRUMENT_USE_GUARDED_PATHS,
                ),
                "agent instrument-use runtime changed after execution",
            )
    except (
        AttributeError,
        KeyError,
        OSError,
        subprocess.SubprocessError,
        TypeError,
        ValueError,
    ) as error:
        errors.append(f"agent instrument-use validator error: {error}")
    return errors


def _first_paper_agent_instrument_use_binding_current(
    payload: Mapping[str, Any],
) -> bool:
    return not _first_paper_agent_instrument_use_binding_errors(payload)


def _artifact_source_binding_current(
    node: EvidenceNode,
    payload: Mapping[str, Any],
) -> bool:
    """Verify declared report provenance against current executable source."""

    work_i_binding = _work_i_source_binding_current(node, payload)
    if work_i_binding is not None:
        return work_i_binding
    if node.node_id == FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID:
        return _first_paper_composition_qualification_binding_current(payload)
    if node.node_id == FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID:
        return _first_paper_deterministic_use_case_binding_current(payload)
    if node.node_id == FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID:
        return _first_paper_agent_instrument_use_binding_current(payload)
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

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
        if validate_diagnostic_relation_graph(protocol, plan, payload):
            return False
    if node.node_id == "mechanism_sample_size_audit":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
        if (
            payload.get("pass") is not True
            or payload.get("protocol_sha256") != _canonical_sha256(protocol)
            or payload.get("gate_a_plan_sha256") != _canonical_sha256(plan)
        ):
            return False
    if node.node_id == "mechanism_preregistration":
        from chemworld.eval.mechanism_adaptation import (
            load_mechanism_adaptation_protocol,
        )
        from chemworld.eval.mechanism_preregistration import (
            validate_mechanism_preregistration,
        )

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
        relation_graph = json.loads(
            (ROOT / node_map()["mechanism_diagnostic_relation_graph"].path).read_text(
                encoding="utf-8"
            )
        )
        sample_size = json.loads(
            (ROOT / node_map()["mechanism_sample_size_audit"].path).read_text(encoding="utf-8")
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

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
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

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
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

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
        stage = "a2" if node.node_id == "mechanism_a2_structural_receipt" else "a3"
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

        protocol = load_mechanism_adaptation_protocol(ROOT / node_map()["mechanism_protocol"].path)
        plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
        a2_receipt = load_json_object(ROOT / node_map()["mechanism_a2_structural_receipt"].path)
        a3_receipt = load_json_object(ROOT / node_map()["mechanism_a3_structural_receipt"].path)
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
        freeze_manifest = load_json_object(ROOT / node_map()["static_s0_freeze_manifest"].path)
        execution = payload.get("execution", {})
        accounting = payload.get("accounting", {})
        if not (
            payload.get("schema_version") == "chemworld-static-s0-campaign-summary-1.0"
            and payload.get("status") == "completed_audited_formal_descriptive_result"
            and payload.get("formal_result") is True
            and payload.get("benchmark_claim_allowed") is False
            and payload.get("freeze", {}).get("manifest_sha256")
            == _canonical_sha256(freeze_manifest)
            and execution.get("participant", {}).get("all_exact_replay_verified") is True
            and execution.get("baselines", {}).get("all_exact_replay_verified") is True
            and accounting.get("campaign_total_physical_experiments") == 28060
            and set(payload.get("tasks", {})) == {"electrochemical", "crystallization"}
        ):
            return False
    if node.node_id == "static_s0_material_information_triarm_summary":
        nominal_manifest = load_json_object(
            ROOT / node_map()["static_s0_nominal_information_freeze_manifest"].path
        )
        misindexed_manifest = load_json_object(
            ROOT / node_map()["static_s0_misindexed_information_freeze_manifest"].path
        )
        execution = payload.get("execution", {})
        accounting = payload.get("accounting", {})
        tasks = payload.get("tasks", {})
        if not (
            payload.get("schema_version")
            == "chemworld-static-s0-material-information-triarm-result-1.0"
            and payload.get("status") == "completed_audited_formal_three_arm_result"
            and payload.get("formal_result") is True
            and payload.get("confirmatory_analysis_complete") is True
            and payload.get("benchmark_claim_allowed") is False
            and payload.get("freeze", {}).get("nominal_manifest_sha256")
            == _canonical_sha256(nominal_manifest)
            and payload.get("freeze", {}).get("misindexed_manifest_sha256")
            == _canonical_sha256(misindexed_manifest)
            and execution.get("world_seeds") == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            and execution.get("all_three_arms_completed") is True
            and execution.get("all_sixty_cells_exact_replay_verified") is True
            and accounting.get("three_arm_total", {}).get("participant_world_cells") == 60
            and accounting.get("three_arm_total", {}).get("total_physical_experiments") == 2280
            and accounting.get("three_arm_total", {}).get("provider_calls") == 1260
            and accounting.get("three_arm_total", {}).get("method_failures") == 0
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
                task.get("recovery", {}).get("overall_recovery_claim", {}).get("passed") is False
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
            and execution.get("campaign_plan_sha256") == _canonical_sha256(campaign_plan)
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
            and threshold_summary.get("all_tasks_reached_threshold_by_any_method_mean") is False
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
    if node.node_id in {
        FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID,
        FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID,
        FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID,
    }:
        return "passed" if payload.get("status") == "passed" else "blocked"
    if node.node_id == "backend_candidate":
        return "passed" if payload.get("backend_contract_validated") else "blocked"
    if node.node_id == "mechanism_preflight":
        return "passed" if payload.get("implementation_complete") else "blocked"
    if "gate_pass" in payload:
        return "passed" if payload.get("gate_pass") is True else "blocked"
    if node.node_id == "mechanism_public_gate_a_decision":
        return "passed" if payload.get("gate_a_pass") is True else "blocked"
    if node.node_id in {
        "mechanism_a2_structural_receipt",
        "mechanism_a3_structural_receipt",
    }:
        return "passed" if payload.get("structurally_complete") is True else "blocked"
    if node.node_id == "mechanism_design_audit":
        return "passed" if payload.get("pass") else "blocked"
    if node.node_id == "mechanism_release_qualification":
        return "passed" if payload.get("qualified") else "blocked"
    if node.node_id == "work_i_latent_terminal_formal_shadow":
        return "blocked" if payload.get("status") == "FAIL" else "passed"
    if node.node_id == "work_i_latent_terminal_analysis":
        return "blocked" if payload.get("status") == "incomplete_full_report_required" else "passed"
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
    backend = json.loads((ROOT / node_map()["backend_candidate"].path).read_text(encoding="utf-8"))
    backend_protocol = json.loads(
        (ROOT / node_map()["backend_protocol"].path).read_text(encoding="utf-8")
    )
    mechanism_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(encoding="utf-8")
    )
    mechanism_a2_receipt = json.loads(
        (ROOT / node_map()["mechanism_a2_structural_receipt"].path).read_text(encoding="utf-8")
    )
    mechanism_a3_receipt = json.loads(
        (ROOT / node_map()["mechanism_a3_structural_receipt"].path).read_text(encoding="utf-8")
    )
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text(encoding="utf-8")
    )
    mechanism_pilot = json.loads(
        (ROOT / node_map()["mechanism_agent_pilot"].path).read_text(encoding="utf-8")
    )
    mechanism_release_qualification = json.loads(
        (ROOT / node_map()["mechanism_release_qualification"].path).read_text(encoding="utf-8")
    )
    mechanism_protocol = load_mechanism_adaptation_protocol(
        ROOT / node_map()["mechanism_protocol"].path
    )
    mechanism_plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
    static_s0_summary_path = ROOT / node_map()["static_s0_formal_campaign_summary"].path
    static_s0_summary = load_json_object(static_s0_summary_path)
    static_s0_information_triarm = load_json_object(
        ROOT / node_map()["static_s0_material_information_triarm_summary"].path
    )
    static_s0_five_task = load_json_object(
        ROOT / node_map()["static_s0_five_task_postqualification_summary"].path
    )
    task_design_matrix = load_json_object(ROOT / node_map()["task_design_matrix"].path)
    composition_qualification = load_json_object(
        ROOT / node_map()[FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID].path
    )
    composition_qualification_errors = _first_paper_composition_qualification_binding_errors(
        composition_qualification
    )
    deterministic_use_cases = load_json_object(
        ROOT / node_map()[FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID].path
    )
    deterministic_use_case_errors = _first_paper_deterministic_use_case_binding_errors(
        deterministic_use_cases
    )
    agent_instrument_use = load_json_object(
        ROOT / node_map()[FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID].path
    )
    agent_instrument_use_errors = _first_paper_agent_instrument_use_binding_errors(
        agent_instrument_use
    )
    work_i_derived = load_json_object(ROOT / node_map()["work_i_fvl_derived_data"].path)
    work_i_derived_manifest = load_json_object(
        ROOT / node_map()["work_i_fvl_derived_manifest"].path
    )
    mechanism_evidence_current = _mechanism_public_decision_binding_current(
        mechanism_decision,
        mechanism_a2_receipt,
        mechanism_a3_receipt,
        mechanism_release_qualification,
        mechanism_protocol,
        mechanism_plan,
    )
    mechanism_gate_a_pass = bool(
        mechanism_evidence_current and mechanism_decision.get("gate_a_pass") is True
    )
    controlled_gate_a_pass = bool(
        mechanism_evidence_current and mechanism_decision.get("a2_pass") is True
    )
    online_gate_a_pass = bool(
        mechanism_evidence_current and mechanism_decision.get("a3_pass") is True
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
            node.node_id == "mechanism_public_gate_a_decision" and not mechanism_evidence_current
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
    current["updated_at"] = datetime.now(UTC).date().isoformat()
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
        "trajectory_alias_write_removal_version": (TRAJECTORY_ALIAS_WRITE_REMOVAL_VERSION),
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
                "gate_a_passed" if mechanism_gate_a_current else "gate_a_recertification_required"
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
        for row in static_s0_summary["tasks"]["electrochemical"]["participant"]["worlds"]
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
            static_s0_summary["execution"]["participant"]["all_exact_replay_verified"]
            and static_s0_summary["execution"]["baselines"]["all_exact_replay_verified"]
        ),
        "freeze_manifest": node_map()["static_s0_freeze_manifest"].path,
        "campaign_total_physical_experiments": int(
            static_s0_summary["accounting"]["campaign_total_physical_experiments"]
        ),
        "comparison_scope": static_s0_summary["reporting_boundaries"]["all_algorithm_comparisons"],
        "task_results": {
            task_key: {
                "participant_mean": static_s0_summary["tasks"][task_key]["participant"][
                    "primary_score"
                ]["mean"],
                "participant_world_bootstrap_95_interval": (
                    static_s0_summary["tasks"][task_key]["participant"]["primary_score"][
                        "world_bootstrap_95_interval"
                    ]
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
        "all_replay_verified": static_s0_five_task["execution"]["all_exact_replay_verified"],
        "all_tasks_reached_threshold_by_any_method_mean": (
            static_s0_five_task["threshold_summary"][
                "all_tasks_reached_threshold_by_any_method_mean"
            ]
        ),
        "threshold_failure_task": static_s0_five_task["threshold_summary"]["failure_task"],
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
        "summary": node_map()["static_s0_material_information_triarm_summary"].path,
        "nominal_freeze_manifest": node_map()["static_s0_nominal_information_freeze_manifest"].path,
        "misindexed_freeze_manifest": node_map()[
            "static_s0_misindexed_information_freeze_manifest"
        ].path,
        "status": static_s0_information_triarm["status"],
        "formal_result": True,
        "confirmatory_analysis_complete": True,
        "benchmark_claim_allowed": False,
        "world_seeds": static_s0_information_triarm["execution"]["world_seeds"],
        "all_sixty_cells_exact_replay_verified": (
            static_s0_information_triarm["execution"]["all_sixty_cells_exact_replay_verified"]
        ),
        "total_physical_experiments": static_s0_information_triarm["accounting"]["three_arm_total"][
            "total_physical_experiments"
        ],
        "provider_calls": static_s0_information_triarm["accounting"]["three_arm_total"][
            "provider_calls"
        ],
        "provider_retry_attempts": static_s0_information_triarm["accounting"]["three_arm_total"][
            "provider_retry_attempts"
        ],
        "task_results": {
            task_key: {
                "score_mean_by_arm": {
                    arm: static_s0_information_triarm["tasks"][task_key]["primary_score_by_arm"][
                        arm
                    ]["mean"]
                    for arm in ("opaque", "nominal", "misindexed")
                },
                "nominal_minus_opaque": (
                    static_s0_information_triarm["tasks"][task_key]["paired_contrasts"][
                        "nominal_minus_opaque"
                    ]
                ),
                "misindexed_minus_nominal": (
                    static_s0_information_triarm["tasks"][task_key]["paired_contrasts"][
                        "misindexed_minus_nominal"
                    ]
                ),
                "overall_recovery_claim": static_s0_information_triarm["tasks"][task_key][
                    "recovery"
                ]["overall_recovery_claim"],
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
        "boundary_recipe_case_count": int(task_design_validation["boundary_recipe_case_count"]),
        "declared_success_metric_count": int(
            task_design_validation["declared_success_metric_count"]
        ),
        "bound_success_metric_count": int(task_design_validation["bound_success_metric_count"]),
        "dead_recipe_coordinate_count": int(task_design_validation["dead_recipe_coordinate_count"]),
        "formalization_blocker_count": int(task_design_validation["formalization_blocker_count"]),
        "formal_experiment_task_ids": list(task_design_validation["formal_experiment_task_ids"]),
        "formal_empirical_comparison_pending_task_ids": list(
            task_design_validation["formal_empirical_comparison_pending_task_ids"]
        ),
        "nonconfirmatory_formal_experiments_required_for_future_claims": bool(
            task_design_validation["nonconfirmatory_formal_experiments_required_for_future_claims"]
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
    a2_active_primary = a2_public["active_oracle"]["by_budget"][primary_budget]
    a2_decoder_primary = a2_public["fixed_trajectory_decoder"]["by_budget"][primary_budget]
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
        "semantics_audit_report": node_map()["mechanism_confirmatory_task_semantics_audit"].path,
        "semantics_audit_pass": bool(
            nodes["mechanism_confirmatory_task_semantics_audit"]["gate_state"] == "passed"
        ),
        "diagnostic_relation_graph_report": node_map()["mechanism_diagnostic_relation_graph"].path,
        "sample_size_audit_report": node_map()["mechanism_sample_size_audit"].path,
        "preregistration_manifest": node_map()["mechanism_preregistration"].path,
        "release_qualification_report": node_map()["mechanism_release_qualification"].path,
        "release_qualification_pass": bool(
            mechanism_release_qualification.get("qualified") is True
            and nodes["mechanism_release_qualification"]["artifact_state"] == "current"
        ),
        "participant_preregistration_candidate": node_map()[
            "mechanism_participant_preregistration_candidate"
        ].path,
        "gate_a_plan": node_map()["mechanism_gate_a_plan"].path,
        "a2_structural_receipt": node_map()["mechanism_a2_structural_receipt"].path,
        "a3_structural_receipt": node_map()["mechanism_a3_structural_receipt"].path,
        "public_decision_report": node_map()["mechanism_public_gate_a_decision"].path,
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
            and nodes["mechanism_public_gate_a_decision"]["artifact_state"] == "current"
        ),
        "gate_a_certificate_status": {
            "a1_physical_intervention_validity": (
                "passed" if mechanism_design.get("pass") is True else "failed"
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
                "completed_trials": mechanism_a2_receipt["observed_completed_trial_count"],
                "primary_budget": int(primary_budget),
                "active_oracle_top1_accuracy": a2_active_primary["top1_accuracy"],
                "fixed_decoder_top1_accuracy": a2_decoder_primary["top1_accuracy"],
            },
            "a3": {
                "completed_trials": mechanism_a3_receipt["observed_completed_trial_count"],
                "reference_sufficient_rate": a3_primary["p_reference_sufficient"],
                "change_detection_sensitivity": a3_detection["sensitivity"],
                "change_detection_auroc": a3_detection["auroc"],
                "no_change_false_positive_rate": a3_detection["false_positive_rate"],
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
        "manuscript": "paper/experimental_intelligence_v1_manuscript.md",
        "display_items": "paper/experimental_intelligence_v1_display_items.md",
        "bibliography": "paper/experimental_intelligence_v1_references.bib",
        "master_plan": "workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md",
        "experiment_ledger": (
            "workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
        ),
        "claim_evidence_ledger": node_map()["pre_arxiv_claim_evidence_ledger"].path,
        "composition_qualification_report": node_map()[
            FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID
        ].path,
        "deterministic_use_case_qualification_report": node_map()[
            FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID
        ].path,
        "agent_instrument_use_report": node_map()[
            FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID
        ].path,
        "qualification_bindings_current": {
            "composition": not composition_qualification_errors,
            "deterministic_use_cases": not deterministic_use_case_errors,
            "agent_instrument_use": not agent_instrument_use_errors,
        },
        "qualification_binding_errors": {
            "composition": composition_qualification_errors,
            "deterministic_use_cases": deterministic_use_case_errors,
            "agent_instrument_use": agent_instrument_use_errors,
        },
        "derived_data": node_map()["work_i_fvl_derived_data"].path,
        "derived_data_manifest": node_map()["work_i_fvl_derived_manifest"].path,
        "release_manifest": "benchmark/releases/chemworld-serious-v1/manifest.json",
        "remaining_experiment_audit": (
            "workstreams/arxiv_v1/reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json"
        ),
        "scope": "experimental_intelligence_in_executable_chemical_worlds",
        "new_scientific_experiments_required_for_first_arxiv": False,
        "required_new_scientific_matrix": {
            "protocol_id": (
                "g2-electrochemical-autonomous-material-information-seed1-seed3-r5-v0.5"
            ),
            "planned_cells": 20,
            "planned_vessel_opportunities": 120,
            "completed_cells": 18,
            "right_censored_cells": 2,
            "completed_pairs": 8,
            "status": "completed_audited_with_right_censoring",
        },
        "stronger_claim_experiments_pending": False,
        "publication_ready": False,
    }
    work_i_node_ids = sorted(node_id for node_id in nodes if node_id.startswith("work_i_"))
    work_i_incremental = work_i_derived["work_i_incremental"]
    current["work_i_fvl"] = {
        "status": "frozen_derived_layer_with_explicit_latent_incompleteness",
        "all_source_bindings_current": all(
            nodes[node_id]["artifact_state"] == "current" for node_id in work_i_node_ids
        ),
        "registered_node_count": len(work_i_node_ids),
        "registered_node_ids": work_i_node_ids,
        "data_contract": node_map()["work_i_incremental_data_contract"].path,
        "world_fork_report": node_map()["work_i_world_fork_qualification"].path,
        "world_fork_certificate": node_map()["work_i_world_fork_certificate"].path,
        "policy_audit": node_map()["work_i_known_policy_formal_audit"].path,
        "policy_report": node_map()["work_i_known_policy_validity_report"].path,
        "policy_manifest": node_map()["work_i_known_policy_delivery_manifest"].path,
        "latent_contract": node_map()["work_i_latent_terminal_estimand_contract"].path,
        "latent_formal_report": node_map()["work_i_latent_terminal_formal_shadow"].path,
        "latent_analysis": node_map()["work_i_latent_terminal_analysis"].path,
        "derived_data": node_map()["work_i_fvl_derived_data"].path,
        "derived_manifest": node_map()["work_i_fvl_derived_manifest"].path,
        "data_contract_sha256": work_i_incremental["data_contract_sha256"],
        "derived_data_sha256": work_i_derived["derived_data_sha256"],
        "derived_manifest_sha256": work_i_derived_manifest["manifest_sha256"],
        "record_counts": work_i_incremental["record_counts"],
        "latent_resolved_shadow_receipts": 6,
        "latent_unresolved_shadow_receipts": 30,
        "latent_complete_case_substitution_used": False,
        "scientific_gate_status": "blocked_on_30_unresolved_latent_receipts",
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
        dependency_fresh = all(fresh_nodes[dependency] for dependency in node.dependencies)
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
            dependency_fresh and path.is_file() and _artifact_source_binding_current(node, payload)
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
    binding_plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
    binding_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(encoding="utf-8")
    )
    binding_a2_receipt = json.loads(
        (ROOT / node_map()["mechanism_a2_structural_receipt"].path).read_text(encoding="utf-8")
    )
    binding_a3_receipt = json.loads(
        (ROOT / node_map()["mechanism_a3_structural_receipt"].path).read_text(encoding="utf-8")
    )
    binding_release_qualification = json.loads(
        (ROOT / node_map()["mechanism_release_qualification"].path).read_text(encoding="utf-8")
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
            node.node_id == "mechanism_public_gate_a_decision" and not gate_a_binding_current
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

    backend = json.loads((ROOT / node_map()["backend_candidate"].path).read_text(encoding="utf-8"))
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
    mechanism_plan = load_json_object(ROOT / node_map()["mechanism_gate_a_plan"].path)
    mechanism_design = json.loads(
        (ROOT / node_map()["mechanism_design_audit"].path).read_text(encoding="utf-8")
    )
    mechanism_a2_receipt = json.loads(
        (ROOT / node_map()["mechanism_a2_structural_receipt"].path).read_text(encoding="utf-8")
    )
    mechanism_a3_receipt = json.loads(
        (ROOT / node_map()["mechanism_a3_structural_receipt"].path).read_text(encoding="utf-8")
    )
    mechanism_decision = json.loads(
        (ROOT / node_map()["mechanism_public_gate_a_decision"].path).read_text(encoding="utf-8")
    )
    mechanism_release_qualification = json.loads(
        (ROOT / node_map()["mechanism_release_qualification"].path).read_text(encoding="utf-8")
    )
    mechanism_pilot = json.loads(
        (ROOT / node_map()["mechanism_agent_pilot"].path).read_text(encoding="utf-8")
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
    composition_qualification_path = (
        ROOT / node_map()[FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID].path
    )
    composition_qualification = load_json_object(composition_qualification_path)
    composition_binding_errors = _first_paper_composition_qualification_binding_errors(
        composition_qualification
    )
    composition_node = recorded_nodes.get(FIRST_PAPER_COMPOSITION_QUALIFICATION_NODE_ID, {})
    expected_composition_state = "stale" if composition_binding_errors else "current"
    expected_composition_gate = "invalidated" if composition_binding_errors else "passed"
    if composition_node.get("artifact_state") != expected_composition_state:
        errors.append("composition qualification evidence state is inconsistent")
    if composition_node.get("gate_state") != expected_composition_gate:
        errors.append("composition qualification gate state is inconsistent")
    deterministic_use_case_path = (
        ROOT / node_map()[FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID].path
    )
    deterministic_use_cases = load_json_object(deterministic_use_case_path)
    deterministic_binding_errors = _first_paper_deterministic_use_case_binding_errors(
        deterministic_use_cases
    )
    deterministic_node = recorded_nodes.get(FIRST_PAPER_DETERMINISTIC_USE_CASES_NODE_ID, {})
    expected_deterministic_state = "stale" if deterministic_binding_errors else "current"
    expected_deterministic_freshness = (
        "stale_dependency_binding" if deterministic_binding_errors else "fresh"
    )
    expected_deterministic_gate = (
        "invalidated" if deterministic_binding_errors else "passed"
    )
    if deterministic_node.get("artifact_state") != expected_deterministic_state:
        errors.append("deterministic use-case evidence state is inconsistent")
    if deterministic_node.get("freshness") != expected_deterministic_freshness:
        errors.append("deterministic use-case freshness is inconsistent")
    if deterministic_node.get("gate_state") != expected_deterministic_gate:
        errors.append("deterministic use-case gate state is inconsistent")
    agent_instrument_use_path = (
        ROOT / node_map()[FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID].path
    )
    agent_instrument_use = load_json_object(agent_instrument_use_path)
    agent_instrument_binding_errors = _first_paper_agent_instrument_use_binding_errors(
        agent_instrument_use
    )
    agent_instrument_node = recorded_nodes.get(FIRST_PAPER_AGENT_INSTRUMENT_USE_NODE_ID, {})
    expected_agent_state = "stale" if agent_instrument_binding_errors else "current"
    expected_agent_gate = "invalidated" if agent_instrument_binding_errors else "passed"
    if agent_instrument_node.get("artifact_state") != expected_agent_state:
        errors.append("agent instrument-use evidence state is inconsistent")
    if agent_instrument_node.get("gate_state") != expected_agent_gate:
        errors.append("agent instrument-use gate state is inconsistent")
    expected_qualification_bindings = {
        "composition": not composition_binding_errors,
        "deterministic_use_cases": not deterministic_binding_errors,
        "agent_instrument_use": not agent_instrument_binding_errors,
    }
    if publication.get("qualification_bindings_current") != expected_qualification_bindings:
        errors.append("current registry qualification freshness summary is inconsistent")
    expected_qualification_errors = {
        "composition": composition_binding_errors,
        "deterministic_use_cases": deterministic_binding_errors,
        "agent_instrument_use": agent_instrument_binding_errors,
    }
    if publication.get("qualification_binding_errors") != expected_qualification_errors:
        errors.append("current registry qualification binding errors are inconsistent")
    expected_backend_validation = (
        "passed" if backend.get("backend_contract_validated") else "blocked"
    )
    expected_gate_a_pass = bool(
        gate_a_binding_current and mechanism_decision.get("gate_a_pass") is True
    )
    expected_gate_a_current = bool(
        expected_gate_a_pass
        and recorded_nodes.get("mechanism_public_gate_a_decision", {}).get("artifact_state")
        == "current"
    )
    if runtime.get("contract_validation") != expected_backend_validation:
        errors.append("current registry backend validation state is inconsistent")
    if formal.get("status") != "static_s0_v1_formal_descriptive_results_complete_claim_bounded":
        errors.append("current registry formal evaluation boundary is inconsistent")
    if formal.get("formal_results_present") is not True:
        errors.append("current registry omits completed static-S0 formal results")
    if formal.get("benchmark_claim_allowed") is not False:
        errors.append("current registry improperly enables participant benchmark claims")
    if formal.get("environment_certificate_results_present") is not True:
        errors.append("current registry omits formal environment certificate results")
    if formal.get("environment_benchmark_readiness_claim_allowed") is not expected_gate_a_current:
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
    if information_triarm.get("all_sixty_cells_exact_replay_verified") is not True:
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
        task_results.get(task_key, {}).get("overall_recovery_claim", {}).get("passed") is not False
        for task_key in ("electrochemical", "crystallization")
    ):
        errors.append("current registry overclaims wrong-prior recovery")
    task_design = current.get("task_design", {})
    if task_design.get("status") != "all_registered_task_designs_executable_and_metric_bound":
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
    if task_design.get("nonconfirmatory_formal_experiments_required_for_future_claims") is not True:
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
    expected_publication_paths = {
        "manuscript": "paper/experimental_intelligence_v1_manuscript.md",
        "display_items": "paper/experimental_intelligence_v1_display_items.md",
        "bibliography": "paper/experimental_intelligence_v1_references.bib",
        "master_plan": "workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md",
        "experiment_ledger": (
            "workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
        ),
        "composition_qualification_report": (
            "workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1-design-v3.json"
        ),
        "deterministic_use_case_qualification_report": (
            "workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1-design-v3.json"
        ),
        "agent_instrument_use_report": (
            "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v3.json"
        ),
        "release_manifest": "benchmark/releases/chemworld-serious-v1/manifest.json",
        "remaining_experiment_audit": (
            "workstreams/arxiv_v1/reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json"
        ),
    }
    for field, expected_path in expected_publication_paths.items():
        if publication.get(field) != expected_path:
            errors.append(f"current registry publication {field} is inconsistent")
        elif not (ROOT / expected_path).is_file():
            errors.append(f"current registry publication {field} is missing")
    if publication.get("scope") != ("experimental_intelligence_in_executable_chemical_worlds"):
        errors.append("current registry first-arXiv scope is inconsistent")
    if publication.get("new_scientific_experiments_required_for_first_arxiv") is not False:
        errors.append("current registry incorrectly marks first-arXiv experiments as pending")
    required_matrix = publication.get("required_new_scientific_matrix", {})
    if required_matrix.get("planned_cells") != 20:
        errors.append("current registry first-arXiv cell count is inconsistent")
    if required_matrix.get("planned_vessel_opportunities") != 120:
        errors.append("current registry first-arXiv opportunity count is inconsistent")
    if required_matrix.get("completed_cells") != 18:
        errors.append("current registry first-arXiv completed-cell count is inconsistent")
    if required_matrix.get("right_censored_cells") != 2:
        errors.append("current registry first-arXiv censoring count is inconsistent")
    if required_matrix.get("completed_pairs") != 8:
        errors.append("current registry first-arXiv completed-pair count is inconsistent")
    if required_matrix.get("status") != "completed_audited_with_right_censoring":
        errors.append("current registry first-arXiv matrix status is inconsistent")
    if publication.get("stronger_claim_experiments_pending") is not False:
        errors.append("current registry incorrectly requires stronger-claim experiments")
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
