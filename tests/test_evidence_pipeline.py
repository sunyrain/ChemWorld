from __future__ import annotations

import json
import runpy
from pathlib import Path


def _pipeline() -> dict[str, object]:
    return runpy.run_path("scripts/evidence_pipeline.py", run_name="evidence_pipeline")


def test_current_evidence_dag_has_unique_acyclic_materializations() -> None:
    pipeline = _pipeline()
    nodes = pipeline["NODES"]
    ordered = pipeline["generation_order"]()

    assert len({node.node_id for node in nodes}) == len(nodes)
    assert len({node.path for node in nodes}) == len(nodes)
    assert {node.node_id for node in ordered} == {node.node_id for node in nodes}
    node_ids = {node.node_id for node in nodes}
    assert "mechanism_a2_structural_receipt" in node_ids
    assert "mechanism_a3_structural_receipt" in node_ids
    assert "mechanism_public_gate_a_decision" in node_ids
    assert "mechanism_diagnostic_relation_graph" in node_ids
    assert "mechanism_confirmatory_task_semantics_audit" in node_ids
    assert "static_s0_formal_campaign_summary" in node_ids
    assert "static_s0_nominal_information_freeze_manifest" in node_ids
    assert "static_s0_misindexed_information_freeze_manifest" in node_ids
    assert "static_s0_material_information_triarm_summary" in node_ids
    assert "static_s0_five_task_campaign_plan" in node_ids
    assert "static_s0_five_task_participant_method" in node_ids
    assert "static_s0_five_task_postqualification_summary" in node_ids
    assert "pre_arxiv_claim_evidence_ledger" in node_ids
    assert "task_design_matrix" in node_ids
    assert not any(node_id.startswith("ncs_") for node_id in node_ids)
    assert {node.role for node in nodes} <= pipeline["CURRENT_ARTIFACT_ROLES"]
    assert all(pipeline["_node_producer"](node) for node in nodes)
    assert all(pipeline["_node_source_binding"](node) for node in nodes)
    assert all(
        pipeline["_node_lifecycle"](node) == "immutable"
        if node.node_id in pipeline["FROZEN_MECHANISM_NODE_IDS"]
        else (node.command is not None)
        == (pipeline["_node_lifecycle"](node) == "generated")
        for node in nodes
    )


def test_frozen_rc28_evidence_is_not_regenerated_after_task_contract_drift() -> None:
    pipeline = _pipeline()
    node_by_id = {node.node_id: node for node in pipeline["NODES"]}

    for node_id in pipeline["FROZEN_MECHANISM_NODE_IDS"]:
        node = node_by_id[node_id]
        assert node.command is None
        assert pipeline["_node_lifecycle"](node) == "immutable"
        assert pipeline["_node_producer"](node) == "frozen_rc28_preregistration_evidence"


def test_current_evidence_pipeline_records_formal_gate_a_pass() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    mechanism = current["mechanism_adaptation"]
    assert mechanism["status"] == "historical_gate_a_pass_current_binding_stale"
    assert mechanism["gate_a_pass"] is True
    assert mechanism["gate_a_certificate_status"] == {
        "a1_physical_intervention_validity": "passed",
        "a2_controlled_matched_identifiability": "historical_pass_current_binding_stale",
        "a3_online_attainability": "historical_pass_current_binding_stale",
    }
    assert (
        mechanism["gate_a_evidence_current"]
        is (
            current["evidence_dag"]["nodes"]["mechanism_public_gate_a_decision"][
                "artifact_state"
            ]
            == "current"
        )
    )
    assert pipeline["check_current_evidence"]() == []


def test_current_state_model_separates_validation_freeze_and_publication() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    assert current["runtime"]["contract_validation"] == "passed"
    assert current["formal_evaluation"]["benchmark_claim_allowed"] is False
    triarm = current["static_material_information_three_arm"]
    assert triarm["formal_result"] is True
    assert triarm["confirmatory_analysis_complete"] is True
    assert triarm["all_sixty_cells_exact_replay_verified"] is True
    assert triarm["world_seeds"] == list(range(10))
    five_task = current["static_s0_five_task_postqualification"]
    assert five_task["status"] == "completed_audited_development_only"
    assert five_task["formal_result"] is False
    assert five_task["benchmark_claim_allowed"] is False
    assert five_task["all_replay_verified"] is True
    assert five_task["result_count"] == 150
    assert five_task["threshold_failure_task"] == "partition-discovery"
    assert triarm["task_results"]["electrochemical"]["nominal_minus_opaque"][
        "familywise_result"
    ] == "positive_information_value"
    assert triarm["task_results"]["crystallization"]["nominal_minus_opaque"][
        "familywise_result"
    ] == "inconclusive"
    assert all(
        triarm["task_results"][task_key]["overall_recovery_claim"]["passed"]
        is False
        for task_key in ("electrochemical", "crystallization")
    )
    assert current["publication"]["status"] == "working_manuscript_not_submission_ready"
    assert current["publication"]["publication_ready"] is False
    assert current["task_design"] == {
        "matrix": "workstreams/flagship_tasks/reports/task-design-matrix-v1.json",
        "status": "all_registered_task_designs_executable_and_metric_bound",
        "registered_task_count": 15,
        "executable_midpoint_task_count": 15,
        "executable_boundary_task_count": 15,
        "boundary_recipe_case_count": 415,
        "declared_success_metric_count": 62,
        "bound_success_metric_count": 62,
        "dead_recipe_coordinate_count": 0,
        "formalization_blocker_count": 0,
        "formal_experiment_task_ids": [
            "electrochemical-conversion",
            "reaction-to-crystallization",
        ],
        "formal_empirical_comparison_pending_task_ids": [
            "equilibrium-characterization",
            "flow-reaction-optimization",
            "low-budget-characterization",
            "partition-discovery",
            "public-private-generalization",
            "purity-yield-tradeoff",
            "reaction-mechanism-explanation",
            "reaction-optimization-standard",
            "reaction-safety-constrained",
            "reaction-to-assay",
            "reaction-to-distillation",
            "reaction-to-purification",
            "tool-agent-planning",
        ],
        "nonconfirmatory_formal_experiments_required_for_future_claims": True,
    }

    summary = pipeline["current_status_summary"](current)
    assert summary["backend_candidate"]["contract_validation"] == "passed"
    assert summary["release_attestation"]["status"] == "passed"
    assert (
        summary["mechanism_gate_a"]["status"]
        == current["mechanism_adaptation"]["status"]
    )
    assert (
        summary["mechanism_gate_a"]["evidence_current"]
        is current["mechanism_adaptation"]["gate_a_evidence_current"]
    )
    assert summary["mechanism_gate_a"]["passed"] is True
    assert (
        summary["formal_benchmark"]["status"]
        == "static_s0_v1_formal_descriptive_results_complete_claim_bounded"
    )
    assert summary["formal_benchmark"]["benchmark_claim_allowed"] is False
    assert summary["publication"]["publication_ready"] is False
    assert (
        current["publication"][
            "new_scientific_experiments_required_for_narrow_scope"
        ]
        is False
    )
    assert current["publication"]["stronger_claim_experiments_pending"] is True


def test_generated_evidence_paths_do_not_make_source_tree_dirty() -> None:
    pipeline = _pipeline()

    assert pipeline["_is_materialized_output_path"]("configs/current.json")
    assert pipeline["_is_materialized_output_path"](
        "workstreams/world_foundation/reports/backend-v0.5.json"
    )
    assert not pipeline["_is_materialized_output_path"](
        "benchmark/releases/deprecated-copy/manifest.json"
    )
    assert not pipeline["_is_materialized_output_path"]("src/chemworld/data/schema.py")


def test_generated_json_line_endings_are_normalized_before_hashing(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline()
    node_type = pipeline["EvidenceNode"]
    output = tmp_path / "report.json"
    output.write_bytes(b'{\r\n  "status": "passed"\r\n}\r\n')
    original_root = pipeline["ROOT"]
    original_nodes = pipeline["NODES"]
    try:
        pipeline["_normalize_materialized_json_line_endings"].__globals__["ROOT"] = (
            tmp_path
        )
        pipeline["_normalize_materialized_json_line_endings"].__globals__["NODES"] = (
            node_type(
                "report",
                "report.json",
                "generated_current",
                command=("generator.py",),
            ),
        )
        pipeline["_normalize_materialized_json_line_endings"]()
    finally:
        pipeline["_normalize_materialized_json_line_endings"].__globals__["ROOT"] = (
            original_root
        )
        pipeline["_normalize_materialized_json_line_endings"].__globals__["NODES"] = (
            original_nodes
        )
    assert output.read_bytes() == b'{\n  "status": "passed"\n}\n'


def test_current_evidence_manifest_explains_every_node() -> None:
    pipeline = _pipeline()
    manifest = pipeline["current_evidence_manifest"]()

    assert len(manifest["nodes"]) == len(pipeline["NODES"])
    assert manifest["generation_order"] == [node.node_id for node in pipeline["generation_order"]()]
    assert all(
        {
            "role",
            "lifecycle",
            "producer",
            "dependencies",
            "source_binding",
            "freshness",
        }
        <= row.keys()
        for row in manifest["nodes"]
    )


def test_gate_state_is_not_conflated_with_artifact_validity() -> None:
    pipeline = _pipeline()

    for node in pipeline["NODES"]:
        if node.role in {"protocol_input", "development_diagnostic", "fixture"}:
            assert pipeline["_node_gate_state"](node, {}) == "not_applicable"
    formal_nodes = {node.node_id: node for node in pipeline["NODES"]}
    assert (
        pipeline["_node_gate_state"](
            formal_nodes["mechanism_design_audit"], {"pass": True}
        )
        == "passed"
    )
    assert (
        pipeline["_node_gate_state"](
            formal_nodes["mechanism_public_gate_a_decision"],
            {"gate_a_pass": False},
        )
        == "blocked"
    )
    assert (
        pipeline["_node_gate_state"](
            formal_nodes["mechanism_a2_structural_receipt"],
            {"structurally_complete": False},
        )
        == "blocked"
    )
    assert (
        pipeline["_node_gate_state"](
            formal_nodes["mechanism_a3_structural_receipt"],
            {"structurally_complete": True},
        )
        == "passed"
    )


def test_evidence_node_contract_errors_are_unambiguous() -> None:
    pipeline = _pipeline()
    node_type = pipeline["EvidenceNode"]
    invalid = node_type("missing_producer", "missing.json", "generated_current")
    assert pipeline["_node_contract_errors"](invalid) == [
        "generated current artifact has no producer: missing_producer"
    ]

    node = pipeline["NODES"][0]
    recorded = {
        "role": "fixture",
        "lifecycle": pipeline["_node_lifecycle"](node),
        "producer": pipeline["_node_producer"](node),
        "source_binding": pipeline["_node_source_binding"](node),
    }
    assert pipeline["_recorded_node_contract_errors"](node, recorded) == [
        f"registry artifact role mismatch: {node.node_id}"
    ]
