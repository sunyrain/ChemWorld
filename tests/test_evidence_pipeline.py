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
    assert not any(node_id.startswith("ncs_") for node_id in node_ids)
    assert {node.role for node in nodes} <= pipeline["CURRENT_ARTIFACT_ROLES"]
    assert all(pipeline["_node_producer"](node) for node in nodes)
    assert all(pipeline["_node_source_binding"](node) for node in nodes)
    assert all(
        (node.command is not None) == (pipeline["_node_lifecycle"](node) == "generated")
        for node in nodes
    )


def test_current_evidence_pipeline_rejects_no_stale_bindings() -> None:
    pipeline = _pipeline()

    assert pipeline["check_current_evidence"]() == []


def test_current_state_model_separates_validation_freeze_and_publication() -> None:
    pipeline = _pipeline()
    current = json.loads(pipeline["CURRENT_REGISTRY"].read_text(encoding="utf-8"))

    assert current["runtime"]["contract_validation"] == "passed"
    assert current["formal_evaluation"]["benchmark_claim_allowed"] is False
    assert current["publication"]["status"] == "no_active_manuscript"
    assert current["publication"]["publication_ready"] is False

    summary = pipeline["current_status_summary"](current)
    assert summary["backend_candidate"]["contract_validation"] == "passed"
    assert summary["release_attestation"]["status"] == "pending_external_gates"
    assert summary["mechanism_gate_a"]["status"] == "gate_a_online_policy_certificate_pending"
    assert summary["mechanism_gate_a"]["evidence_current"] is True
    assert summary["mechanism_gate_a"]["passed"] is False
    assert (
        summary["formal_benchmark"]["protocol_binding_state"]
        == "invalidated_dependency_binding_mismatch"
    )
    assert summary["formal_benchmark"]["status"] == "formal_protocol_recertification_required"
    assert summary["formal_benchmark"]["method_families_ready"] == "0/5"
    assert summary["formal_benchmark"]["benchmark_claim_allowed"] is False
    assert summary["publication"]["publication_ready"] is False


def test_generated_evidence_paths_do_not_make_source_tree_dirty() -> None:
    pipeline = _pipeline()

    assert pipeline["_is_materialized_output_path"]("configs/current.json")
    assert pipeline["_is_materialized_output_path"](
        "workstreams/world_foundation/reports/backend-v0.5.json"
    )
    assert pipeline["_is_materialized_output_path"](
        "benchmark/releases/chemworld-serious-vnext/manifest.json"
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
