from __future__ import annotations

import copy
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
    assert "first_paper_composition_qualification" in node_ids
    qualification = {node.node_id: node for node in nodes}["first_paper_composition_qualification"]
    assert qualification.path == (
        "workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1-design-v3.json"
    )
    assert qualification.role == "formal_result"
    assert qualification.dependencies == ("task_design_matrix",)
    assert qualification.command is None
    assert pipeline["_node_lifecycle"](qualification) == "immutable"
    deterministic = {node.node_id: node for node in nodes}[
        "first_paper_deterministic_use_case_qualification"
    ]
    assert deterministic.path == (
        "workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1-design-v3.json"
    )
    assert deterministic.role == "formal_result"
    assert deterministic.dependencies == (
        "task_design_matrix",
        "first_paper_composition_qualification",
        "work_i_world_fork_qualification",
    )
    assert deterministic.command is None
    assert pipeline["_node_lifecycle"](deterministic) == "immutable"
    agent_use = {node.node_id: node for node in nodes}["first_paper_agent_instrument_use"]
    assert agent_use.path == (
        "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v3.json"
    )
    assert agent_use.role == "formal_result"
    assert agent_use.dependencies == (
        "first_paper_composition_qualification",
        "first_paper_deterministic_use_case_qualification",
        "work_i_world_fork_qualification",
    )
    assert agent_use.command is None
    assert pipeline["_node_lifecycle"](agent_use) == "immutable"
    assert {
        "work_i_world_fork_qualification",
        "work_i_world_fork_certificate",
        "work_i_known_policy_formal_audit",
        "work_i_known_policy_validity_report",
        "work_i_known_policy_delivery_manifest",
        "work_i_latent_terminal_estimand_contract",
        "work_i_latent_terminal_reconstructability",
        "work_i_latent_terminal_replay_qualification",
        "work_i_latent_terminal_formal_shadow",
        "work_i_latent_terminal_analysis",
        "work_i_incremental_data_contract",
        "work_i_fvl_derived_data",
        "work_i_fvl_derived_manifest",
    } <= node_ids
    assert not any(node_id.startswith("ncs_") for node_id in node_ids)
    assert {node.role for node in nodes} <= pipeline["CURRENT_ARTIFACT_ROLES"]
    assert all(pipeline["_node_producer"](node) for node in nodes)
    assert all(pipeline["_node_source_binding"](node) for node in nodes)
    assert all(
        pipeline["_node_lifecycle"](node) == "immutable"
        if node.node_id in pipeline["FROZEN_MECHANISM_NODE_IDS"]
        else (node.command is not None) == (pipeline["_node_lifecycle"](node) == "generated")
        for node in nodes
    )


def test_work_i_fvl_nodes_have_current_fail_closed_source_bindings() -> None:
    pipeline = _pipeline()
    nodes = {node.node_id: node for node in pipeline["NODES"] if node.node_id.startswith("work_i_")}
    assert len(nodes) == 13
    assert nodes["work_i_world_fork_certificate"].dependencies == (
        "work_i_world_fork_qualification",
    )
    assert nodes["work_i_fvl_derived_manifest"].dependencies == ("work_i_fvl_derived_data",)
    for node in nodes.values():
        payload = json.loads((Path(node.path)).read_text(encoding="utf-8"))
        assert pipeline["_work_i_source_binding_current"](node, payload) is True

    derived = json.loads(Path(nodes["work_i_fvl_derived_data"].path).read_text(encoding="utf-8"))
    derived["work_i_incremental"]["record_counts"]["L"]["latent_discard_units"] = 35
    assert (
        pipeline["_work_i_source_binding_current"](nodes["work_i_fvl_derived_data"], derived)
        is False
    )


def test_first_paper_composition_qualification_binding_fails_closed() -> None:
    pipeline = _pipeline()
    node = {item.node_id: item for item in pipeline["NODES"]}[
        "first_paper_composition_qualification"
    ]
    payload = json.loads(Path(node.path).read_text(encoding="utf-8"))
    validate = pipeline["_first_paper_composition_qualification_binding_current"]

    assert validate(payload) is False
    assert pipeline["_first_paper_composition_qualification_binding_errors"](
        payload
    ) == ["composition qualification runtime changed after execution"]

    mutations = [
        {**payload, "schema_version": "stale"},
        {**payload, "status": "failed"},
        {
            **payload,
            "receipt_completeness": {
                **payload["receipt_completeness"],
                "passed": False,
            },
        },
        {
            **payload,
            "reference_qualification": {
                **payload["reference_qualification"],
                "recipe_denominator": 1785,
            },
        },
        {
            **payload,
            "summary": {
                **payload["summary"],
                "public_private_leakage_count": 1,
            },
        },
        {
            **payload,
            "source_binding": {
                **payload["source_binding"],
                "experiment_note_sha256": "0" * 64,
            },
        },
        {
            **payload,
            "source_binding": {
                **payload["source_binding"],
                "execution_commit": "0" * 40,
            },
        },
        {
            **payload,
            "generated_qualification": {
                **payload["generated_qualification"],
                "cases": payload["generated_qualification"]["cases"][:-1],
            },
        },
    ]

    assert all(validate(mutated) is False for mutated in mutations)


def test_first_paper_deterministic_use_case_binding_fails_closed() -> None:
    pipeline = _pipeline()
    node = {item.node_id: item for item in pipeline["NODES"]}[
        "first_paper_deterministic_use_case_qualification"
    ]
    payload = json.loads(Path(node.path).read_text(encoding="utf-8"))
    validate = pipeline["_first_paper_deterministic_use_case_binding_current"]

    assert validate(payload) is False
    assert pipeline["_first_paper_deterministic_use_case_binding_errors"](
        payload
    ) == ["deterministic use-case runtime changed after execution"]

    mutations = []
    stale_status = copy.deepcopy(payload)
    stale_status["status"] = "failed"
    mutations.append(stale_status)

    stale_denominator = copy.deepcopy(payload)
    stale_denominator["denominators"]["submitted_action_count"] = 88
    mutations.append(stale_denominator)

    missing_receipt = copy.deepcopy(payload)
    missing_receipt["cases"][0]["step_receipts"].pop()
    mutations.append(missing_receipt)

    stale_transaction = copy.deepcopy(payload)
    stale_transaction["cases"][0]["step_receipts"][0]["transaction"]["status"] = "rolled_back"
    mutations.append(stale_transaction)

    stale_resource = copy.deepcopy(payload)
    stale_resource["cases"][0]["step_receipts"][0]["resource_reconciliation"][
        "resource_reconciled"
    ] = False
    mutations.append(stale_resource)

    stale_rollback = copy.deepcopy(payload)
    u03 = next(case for case in stale_rollback["cases"] if case["case_id"] == "U03/E01")
    u03["step_receipts"][0]["rollback_recovery_receipt"]["ghost_state_preserved"] = False
    mutations.append(stale_rollback)

    stale_existing = copy.deepcopy(payload)
    stale_existing["existing_evidence"]["U04"]["binding"]["expected_sha256"] = "0" * 64
    mutations.append(stale_existing)

    stale_source = copy.deepcopy(payload)
    stale_source["source_binding"]["experiment_note"]["sha256"] = "0" * 64
    mutations.append(stale_source)

    stale_action = copy.deepcopy(payload)
    stale_action["cases"][0]["actions"][0]["volume_L"] = 0.03
    mutations.append(stale_action)

    assert all(validate(mutated) is False for mutated in mutations)


def test_first_paper_agent_instrument_use_binding_fails_closed() -> None:
    pipeline = _pipeline()
    node = {item.node_id: item for item in pipeline["NODES"]}[
        "first_paper_agent_instrument_use"
    ]
    payload = json.loads(Path(node.path).read_text(encoding="utf-8"))
    validate = pipeline["_first_paper_agent_instrument_use_binding_current"]

    assert validate(payload) is False
    assert pipeline["_first_paper_agent_instrument_use_binding_errors"](
        payload
    ) == ["agent instrument-use runtime changed after execution"]

    mutations = []
    stale_status = copy.deepcopy(payload)
    stale_status["status"] = "failed"
    mutations.append(stale_status)

    stale_action = copy.deepcopy(payload)
    stale_action["actions"][0]["transaction"]["status"] = "rolled_back"
    mutations.append(stale_action)

    stale_lifecycle = copy.deepcopy(payload)
    stale_lifecycle["lifecycle"]["committed_final_assay_count"] = 0
    mutations.append(stale_lifecycle)

    stale_resource = copy.deepcopy(payload)
    stale_resource["declared_resource_budget"]["observed_usage"]["process_time_s"] = 10441.0
    mutations.append(stale_resource)

    stale_provider = copy.deepcopy(payload)
    stale_provider["provider_accounting"]["usage"]["prompt_tokens"] = 493091
    mutations.append(stale_provider)

    stale_boundary = copy.deepcopy(payload)
    stale_boundary["public_boundary"]["finding_count"] = 1
    mutations.append(stale_boundary)

    stale_replay = copy.deepcopy(payload)
    stale_replay["exact_replay"]["max_abs_error"] = 1.0e-9
    mutations.append(stale_replay)

    stale_existing = copy.deepcopy(payload)
    stale_existing["existing_evidence"]["U05"]["binding"]["expected_sha256"] = "0" * 64
    mutations.append(stale_existing)

    stale_source = copy.deepcopy(payload)
    stale_source["source_binding"]["evaluator"]["sha256"] = "0" * 64
    mutations.append(stale_source)

    assert all(validate(mutated) is False for mutated in mutations)


def test_current_registry_exposes_work_i_fvl_boundary_without_hiding_failure() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))
    work_i = current["work_i_fvl"]
    assert work_i["registered_node_count"] == 13
    assert work_i["all_source_bindings_current"] is True
    assert work_i["latent_resolved_shadow_receipts"] == 6
    assert work_i["latent_unresolved_shadow_receipts"] == 30
    assert work_i["latent_complete_case_substitution_used"] is False
    assert work_i["scientific_gate_status"] == "blocked_on_30_unresolved_latent_receipts"
    nodes = current["evidence_dag"]["nodes"]
    assert nodes["work_i_latent_terminal_formal_shadow"]["artifact_state"] == "current"
    assert nodes["work_i_latent_terminal_formal_shadow"]["gate_state"] == "blocked"
    assert nodes["work_i_latent_terminal_analysis"]["gate_state"] == "blocked"


def test_frozen_current_evidence_is_not_regenerated_after_task_contract_drift() -> None:
    pipeline = _pipeline()
    node_by_id = {node.node_id: node for node in pipeline["NODES"]}

    for node_id in pipeline["FROZEN_MECHANISM_NODE_IDS"]:
        node = node_by_id[node_id]
        assert node.command is None
        assert pipeline["_node_lifecycle"](node) == "immutable"
        assert pipeline["_node_producer"](node) == "frozen_current_preregistration_evidence"


def test_current_evidence_pipeline_records_formal_gate_a_pass() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    mechanism = current["mechanism_adaptation"]
    assert mechanism["status"] == "gate_a_passed_remaining_gates_pending"
    assert mechanism["gate_a_pass"] is True
    assert mechanism["gate_a_certificate_status"] == {
        "a1_physical_intervention_validity": "passed",
        "a2_controlled_matched_identifiability": "passed",
        "a3_online_attainability": "passed",
    }
    assert mechanism["gate_a_evidence_current"] is (
        current["evidence_dag"]["nodes"]["mechanism_public_gate_a_decision"]["artifact_state"]
        == "current"
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
    assert (
        triarm["task_results"]["electrochemical"]["nominal_minus_opaque"]["familywise_result"]
        == "positive_information_value"
    )
    assert (
        triarm["task_results"]["crystallization"]["nominal_minus_opaque"]["familywise_result"]
        == "inconclusive"
    )
    assert all(
        triarm["task_results"][task_key]["overall_recovery_claim"]["passed"] is False
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
    assert summary["mechanism_gate_a"]["status"] == current["mechanism_adaptation"]["status"]
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
    publication = current["publication"]
    assert publication["manuscript"] == ("paper/experimental_intelligence_v1_manuscript.md")
    assert publication["display_items"] == ("paper/experimental_intelligence_v1_display_items.md")
    assert publication["bibliography"] == ("paper/experimental_intelligence_v1_references.bib")
    assert publication["claim_evidence_ledger"] == (
        "workstreams/flagship_tasks/reports/pre-arxiv-claim-evidence-ledger-v1.json"
    )
    assert publication["composition_qualification_report"] == (
        "workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1-design-v3.json"
    )
    assert publication["deterministic_use_case_qualification_report"] == (
        "workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1-design-v3.json"
    )
    assert publication["agent_instrument_use_report"] == (
        "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v3.json"
    )
    deterministic_report = Path(publication["deterministic_use_case_qualification_report"])
    deterministic_node = current["evidence_dag"]["nodes"][
        "first_paper_deterministic_use_case_qualification"
    ]
    assert deterministic_node["sha256"] == pipeline["file_sha256"](deterministic_report)
    assert deterministic_node["artifact_state"] == "stale"
    assert deterministic_node["freshness"] == "stale_dependency_binding"
    assert deterministic_node["gate_state"] == "invalidated"
    assert publication["qualification_bindings_current"] == {
        "composition": False,
        "deterministic_use_cases": False,
        "agent_instrument_use": False,
    }
    assert publication["qualification_binding_errors"] == {
        "composition": ["composition qualification runtime changed after execution"],
        "deterministic_use_cases": [
            "deterministic use-case runtime changed after execution"
        ],
        "agent_instrument_use": [
            "agent instrument-use runtime changed after execution"
        ],
    }
    report = json.loads(
        Path(publication["composition_qualification_report"]).read_text(encoding="utf-8")
    )
    assert (
        pipeline["file_sha256"](pipeline["CURRENT_REGISTRY"])
        != report["source_binding"]["current_registry_sha256"]
    )
    assert publication["remaining_experiment_audit"] == (
        "workstreams/arxiv_v1/reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json"
    )
    assert publication["scope"] == ("experimental_intelligence_in_executable_chemical_worlds")
    assert publication["new_scientific_experiments_required_for_first_arxiv"] is False
    assert publication["required_new_scientific_matrix"]["planned_cells"] == 20
    assert publication["required_new_scientific_matrix"]["planned_vessel_opportunities"] == 120
    matrix = publication["required_new_scientific_matrix"]
    assert matrix["completed_cells"] == 18
    assert matrix["right_censored_cells"] == 2
    assert matrix["completed_pairs"] == 8
    assert matrix["status"] == "completed_audited_with_right_censoring"
    assert current["publication"]["stronger_claim_experiments_pending"] is False


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
        pipeline["_normalize_materialized_json_line_endings"].__globals__["ROOT"] = tmp_path
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
        pipeline["_normalize_materialized_json_line_endings"].__globals__["ROOT"] = original_root
        pipeline["_normalize_materialized_json_line_endings"].__globals__["NODES"] = original_nodes
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
        pipeline["_node_gate_state"](formal_nodes["mechanism_design_audit"], {"pass": True})
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
