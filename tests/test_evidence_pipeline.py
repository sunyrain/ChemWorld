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
