from __future__ import annotations

import json
import runpy


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
    assert "mechanism_gate_a" in node_ids
    assert "mechanism_online_policy_certificate" in node_ids
    assert not any(node_id.startswith("ncs_") for node_id in node_ids)
    assert {node.role for node in nodes} <= pipeline["CURRENT_ARTIFACT_ROLES"]
    assert all(pipeline["_node_producer"](node) for node in nodes)
    assert all(pipeline["_node_source_binding"](node) for node in nodes)
    assert all(
        (node.command is not None) == (pipeline["_node_lifecycle"](node) == "generated")
        for node in nodes
    )


def test_current_evidence_pipeline_reports_only_declared_recertification_blocker() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    assert (
        current["mechanism_adaptation"]["status"]
        == "gate_a_invalidated_recertification_required"
    )
    assert current["mechanism_adaptation"]["gate_a_evidence_current"] is False
    assert pipeline["check_current_evidence"]() == [
        "mechanism online-policy certificate binding is stale"
    ]


def test_current_state_model_separates_validation_freeze_and_publication() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    assert current["runtime"]["contract_validation"] == "passed"
    assert current["formal_evaluation"]["benchmark_claim_allowed"] is False
    assert current["publication"]["status"] == "no_active_manuscript"
    assert current["publication"]["publication_ready"] is False

    summary = pipeline["current_status_summary"](current)
    assert summary["backend_candidate"]["contract_validation"] == "passed"
    assert summary["release_attestation"]["status"] == "passed"
    assert (
        summary["mechanism_gate_a"]["status"]
        == current["mechanism_adaptation"]["status"]
    )
    assert summary["mechanism_gate_a"]["evidence_current"] is False
    assert summary["mechanism_gate_a"]["passed"] is False
    assert summary["formal_benchmark"]["status"] == "environment_ready_methods_unfrozen"
    assert summary["formal_benchmark"]["benchmark_claim_allowed"] is False
    assert summary["publication"]["publication_ready"] is False


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
            formal_nodes["mechanism_gate_a"], {"gate_a_pass": False}
        )
        == "blocked"
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
