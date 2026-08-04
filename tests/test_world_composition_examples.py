from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import chemworld
from chemworld.tasks import get_task, list_tasks

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "examples" / "world-authoring"
COMPOSITION_EXAMPLES = (
    (
        "composed-equilibrium-characterization-v0.1.json",
        "phase-observation",
        {"phase", "observation"},
    ),
    (
        "composed-reaction-assay-v0.1.json",
        "reaction-thermal-observation",
        {"reaction", "thermal", "observation"},
    ),
    (
        "composed-reaction-purification-v0.1.json",
        "reaction-phase-separation-observation",
        {"reaction", "thermal", "phase", "separation", "observation"},
    ),
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


@pytest.mark.parametrize(
    ("filename", "expected_pattern", "expected_components"),
    COMPOSITION_EXAMPLES,
)
def test_public_composition_examples_compile(
    filename: str,
    expected_pattern: str,
    expected_components: set[str],
) -> None:
    request = _read_json(EXAMPLE_ROOT / filename)
    report = chemworld.check_world_composition_compatibility(request)
    compiled = chemworld.compile_world_composition(request)

    assert report.compatible
    assert report.pattern == expected_pattern
    assert compiled.compatibility == report
    assert set(compiled.spec.component_kinds) == expected_components
    assert compiled.task_spec.task_id == request["composition_id"]
    assert "terminate" in compiled.task_spec.allowed_operations
    assert "measure" in compiled.task_spec.allowed_operations
    assert "final_assay" in compiled.task_spec.allowed_instruments
    if expected_pattern == "phase-observation":
        assert set(compiled.task_spec.allowed_operations) == {"terminate", "measure"}
    json.dumps(compiled.to_public_dict(), allow_nan=False)


def test_reference_task_map_covers_registry_once_and_uses_registered_patterns() -> None:
    mapping = _read_json(EXAMPLE_ROOT / "reference-task-contract-map-v0.1.json")
    patterns = mapping["patterns"]
    assert isinstance(patterns, list)

    mapped_task_ids: list[str] = []
    for pattern in patterns:
        component_kinds = pattern["component_kinds"]
        request = {
            "schema_version": "chemworld-world-composition-0.1",
            "composition_id": f"mapping-check-{pattern['pattern_id']}",
            "world_split": "public-test",
            "components": [
                {"kind": kind, "role": kind, "parameters": {}}
                for kind in component_kinds
            ],
            "task": {},
        }
        report = chemworld.check_world_composition_compatibility(request)
        compiled = chemworld.compile_world_composition(request)
        anchor = get_task(compiled.runtime_task_profile_id)

        assert report.compatible
        assert report.pattern == pattern["pattern_id"]
        for task_id in pattern["reference_task_ids"]:
            task = get_task(task_id)
            assert task.allowed_operations == anchor.allowed_operations
            assert task.allowed_instruments == anchor.allowed_instruments
        mapped_task_ids.extend(pattern["reference_task_ids"])

    registered_task_ids = {task.task_id for task in list_tasks()}
    assert len(mapped_task_ids) == len(set(mapped_task_ids)) == 15
    assert set(mapped_task_ids) == registered_task_ids


def test_reference_task_map_preserves_claim_boundaries() -> None:
    mapping = _read_json(EXAMPLE_ROOT / "reference-task-contract-map-v0.1.json")

    assert mapping["mapping_boundary"] == {
        "component_pattern_explains_world_surface": True,
        "registered_task_contracts_remain_frozen": True,
        "byte_for_byte_reconstruction_claim": False,
        "qualification_claim": False,
        "exhaustive_task_space_claim": False,
    }
    assert set(mapping["task_overlay_fields"]) == {
        "objective",
        "budget",
        "episode_mode",
        "allowed_operations",
        "allowed_instruments",
        "observation_policy",
        "termination_policy",
        "success_metrics",
        "world_split",
        "seeds",
    }
