from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.semantic_invariance import (
    REQUIRED_PROBES,
    MaterialCodeRemap,
    audit_semantic_invariance,
    nested_equivalent_action,
    reordered_observation,
)
from chemworld.materials import public_material_catalog

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "benchmark" / "semantic_invariance_vnext.json"
REPORT_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "semantic-invariance-controls.json"
)


def _protocol() -> dict[str, object]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def _remap() -> MaterialCodeRemap:
    return MaterialCodeRemap((2, 0, 3, 1), (1, 3, 0, 2))


def test_material_remap_round_trips_and_hides_canonical_ids() -> None:
    remap = _remap()
    canonical = {
        "operation": "add_catalyst",
        "solvent": 2,
        "catalyst": 0,
    }

    public = remap.encode_action(canonical)

    assert public == {"operation": "add_catalyst", "solvent": 0, "catalyst": 2}
    assert remap.decode_action(public) == canonical
    opaque = remap.opaque_catalog(public_material_catalog())
    opaque_text = json.dumps(opaque, sort_keys=True)
    assert "water" not in opaque_text
    assert "cat_a" not in opaque_text
    assert opaque["mapping_visibility_policy"].startswith("public codes only")


def test_material_remap_rejects_invalid_permutations_and_codes() -> None:
    with pytest.raises(ValueError, match="permutation"):
        MaterialCodeRemap((0, 0, 1, 2), (0, 1, 2, 3))
    with pytest.raises(ValueError, match="outside"):
        _remap().decode_action({"operation": "add_solvent", "solvent": 4})
    with pytest.raises(ValueError, match="integer"):
        _remap().decode_action({"operation": "add_solvent", "solvent": 1.5})


def test_nested_action_and_reordered_observation_preserve_keyed_semantics() -> None:
    action = {"operation": "heat", "duration_s": 60.0, "target_temperature_K": 330.0}
    nested = nested_equivalent_action(action)
    observation = {"yield": [0.2], "score": [0.1], "cost": [0.3]}

    assert nested == {
        "payload": {"target_temperature_K": 330.0, "duration_s": 60.0},
        "operation": "heat",
    }
    assert list(reordered_observation(observation)) == ["cost", "score", "yield"]
    assert reordered_observation(observation) == observation


def test_semantic_invariance_audit_passes_all_tasks_and_probes() -> None:
    report = audit_semantic_invariance(_protocol())

    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert report["paired_run_count"] == 12
    assert report["checks"]["invalid_material_code_fail_closed"] is True
    assert set(report["tasks"]) == {
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
        "electrochemical-conversion",
        "equilibrium-characterization",
    }
    for task in report["tasks"].values():
        assert task["passed"] is True
        assert task["paired_run_count"] == 2
        assert set(task["probes"]) == set(REQUIRED_PROBES)
        assert all(task["probes"].values())


def test_malformed_protocol_fails_closed_without_running_tasks() -> None:
    malformed = _protocol()
    malformed["material_code_remap"]["solvent_public_to_canonical"] = [
        0,
        1.5,
        2,
        3,
    ]

    mapping_report = audit_semantic_invariance(malformed)

    assert mapping_report["controls_ready"] is False
    assert mapping_report["paired_run_count"] == 0
    assert "must contain integers" in mapping_report["configuration_error"]

    malformed = _protocol()
    malformed["recipe_coordinate"] = "middle"
    coordinate_report = audit_semantic_invariance(malformed)
    assert coordinate_report["controls_ready"] is False
    assert coordinate_report["checks"]["recipe_coordinate"] is False
    assert coordinate_report["paired_run_count"] == 0


def test_committed_report_matches_deterministic_audit() -> None:
    committed = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    assert committed == audit_semantic_invariance(_protocol())
