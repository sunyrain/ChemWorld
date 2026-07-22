from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from chemworld.eval.contract_coherence import (
    ContractCoherenceError,
    _method_aliases_resolve_to_same_implementation,
    assert_artifact_compatible,
    audit_contract_coherence,
    load_contract_coherence_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "world_foundation" / "reports" / "contract-coherence-v0.5.json"
SHA_A = "a" * 64
SHA_B = "b" * 64


def _artifact() -> dict[str, str]:
    return {
        "backend_id": "chemworld-physical-chemistry-v0.5-candidate",
        "backend_semantic_hash": SHA_A,
        "world_law_id": "chemworld-physical-chemistry-v0.5",
        "task_contract_hash": SHA_A,
        "evaluation_contract_version": "chemworld-layered-evaluation-0.3",
        "result_schema_version": "chemworld-evaluation-result-0.3",
        "score_replay_binding_version": "chemworld-score-replay-binding-0.1",
        "method_id": "random",
        "method_config_hash": SHA_A,
    }


def test_contract_graph_covers_every_serious_task_and_formal_method() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert set(report["task_graph"]) == {
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
        "electrochemical-conversion",
        "equilibrium-characterization",
    }
    assert len(report["method_contract"]["formal_to_implementation"]) == 12
    assert report["method_contract"]["legacy_alias_to_formal"]["greedy"] == "greedy_local"
    assert "gp_bo" not in report["method_contract"]["legacy_alias_to_formal"]
    assert report["method_contract"]["legacy_distinct_implementations"]["gp_bo"][
        "implementation"
    ] == "gp_bo"
    assert all(report["controls"].values())


def test_method_aliases_must_construct_the_same_agent_class() -> None:
    formal = {"structured_gp_ei": "structured_gp_bo"}
    assert _method_aliases_resolve_to_same_implementation(
        {"structured_gp_bo": "structured_gp_ei"}, formal
    )
    assert not _method_aliases_resolve_to_same_implementation(
        {"gp_bo": "structured_gp_ei"}, formal
    )


def test_each_task_graph_binds_runtime_observation_score_risk_and_world() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for task in report["task_graph"].values():
        assert task["operations"]
        assert task["providers"]
        assert task["allowed_instruments"]
        assert task["primary_metric"]
        assert task["primary_direction"] == "maximize"
        assert task["risk_limit"] > 0.0
        assert task["process_cost_limit"] > 0.0
        assert task["world_axes"] == [
            "interpolation",
            "extrapolation",
            "composition",
            "observation_noise",
        ]
        assert task["task_contract_hash"]


def test_same_schema_different_semantics_is_rejected() -> None:
    protocol = load_contract_coherence_protocol()
    strict = protocol["artifact_compatibility"]["strict_identity_fields"]
    expected = _artifact()
    assert_artifact_compatible(expected, dict(expected), strict_fields=strict)
    changed = dict(expected)
    changed["backend_semantic_hash"] = SHA_B
    with pytest.raises(ContractCoherenceError, match="backend_semantic_hash"):
        assert_artifact_compatible(expected, changed, strict_fields=strict)
    missing = dict(expected)
    del missing["method_config_hash"]
    with pytest.raises(ContractCoherenceError, match="field missing"):
        assert_artifact_compatible(expected, missing, strict_fields=strict)


def test_audit_fails_if_a_primary_metric_drifts() -> None:
    protocol = copy.deepcopy(load_contract_coherence_protocol())
    evaluation_path = ROOT / protocol["sources"]["evaluation"]
    payload = json.loads(evaluation_path.read_text(encoding="utf-8"))
    payload["tasks"]["partition-discovery"] = "wrong_metric"
    changed_path = ROOT / ".pytest_cache" / "contract-coherence-bad-evaluation.json"
    changed_path.parent.mkdir(parents=True, exist_ok=True)
    changed_path.write_text(json.dumps(payload), encoding="utf-8")
    protocol["sources"]["evaluation"] = str(changed_path.relative_to(ROOT))
    report = audit_contract_coherence(protocol)
    assert report["controls_ready"] is False
    assert report["controls"]["primary_metrics_are_single_source"] is False
