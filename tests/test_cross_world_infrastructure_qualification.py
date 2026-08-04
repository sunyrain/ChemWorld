from __future__ import annotations

import copy
from pathlib import Path

import pytest

from chemworld.eval.cross_world_infrastructure_qualification import (
    QualificationProtocolError,
    load_protocol,
    recipe_cases,
    run_negative_probes,
    run_task_world_unit,
    validate_protocol_bindings,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = (
    ROOT
    / "configs"
    / "benchmark"
    / "first_paper_cross_world_infrastructure_qualification_v0.1.json"
)


def test_frozen_protocol_binds_current_registry_and_yijun_write_set() -> None:
    protocol = load_protocol(PROTOCOL_PATH)
    receipt = validate_protocol_bindings(
        protocol,
        repository_root=ROOT,
        require_clean=False,
    )
    assert receipt["status"] == "passed"
    assert receipt["owner"] == "Yijun"
    assert receipt["task_count"] == 15
    assert receipt["task_world_unit_count"] == 64
    assert all("WORK_I_TODOLIST" not in path for path in receipt["write_set"])
    assert all("/claims/" not in path for path in receipt["write_set"])


def test_frozen_protocol_rejects_task_contract_drift() -> None:
    protocol = copy.deepcopy(load_protocol(PROTOCOL_PATH))
    protocol["source_binding"]["tasks"][0]["contract_sha256"] = "0" * 64
    with pytest.raises(QualificationProtocolError, match="task contract hash drifted"):
        validate_protocol_bindings(
            protocol,
            repository_root=ROOT,
            require_clean=False,
        )


def test_recipe_cases_cover_true_boundaries_and_all_categories() -> None:
    task = get_task("reaction-to-assay")
    cases = recipe_cases(task)
    assert {case["case_id"] for case in cases} >= {
        "midpoint",
        "coordinate-0-low",
        "coordinate-0-high",
        "coordinate-4-category-0",
        "coordinate-4-category-3",
        "coordinate-6-category-0",
        "coordinate-6-category-3",
    }
    assert next(case for case in cases if case["case_id"] == "coordinate-0-low")["vector"][0] == 0.0
    assert (
        next(case for case in cases if case["case_id"] == "coordinate-0-high")["vector"][0] == 1.0
    )
    assert all(
        case["compiled_actions"][-1] == {"operation": "measure", "instrument": "final_assay"}
        for case in cases
    )


def test_all_three_negative_probe_classes_are_atomic_and_reconciled() -> None:
    protocol = load_protocol(PROTOCOL_PATH)
    probes = run_negative_probes(get_task("reaction-to-assay"), 0, protocol)
    assert [probe["probe_id"] for probe in probes] == [
        "invalid_operation",
        "precondition_failure",
        "resource_exhaustion",
    ]
    assert all(probe["passed"] for probe in probes), probes
    assert all(probe["physical_state_preserved"] for probe in probes)
    assert all(probe["observation_rng_preserved"] for probe in probes)
    assert all(probe["expected_rejection"] for probe in probes)
    assert all(probe["observed_rejection"] for probe in probes)
    assert all(probe["ghost_state"]["ghost_state_preserved"] for probe in probes)
    assert all(probe["resource_outcome_delta"] for probe in probes)


def test_midpoint_and_boundaries_execute_with_exact_replay(tmp_path: Path) -> None:
    protocol = load_protocol(PROTOCOL_PATH)
    task = get_task("reaction-to-assay")
    unit = run_task_world_unit(task, 0, protocol, scratch_dir=tmp_path)
    assert unit["valid_recipe_case_count"] == len(recipe_cases(task))
    assert unit["negative_probe_count"] == 3
    assert unit["passed"], unit["failures"]
    assert all(unit["properties"].values())
    assert all(
        case["exact_replay"]["verified"] and case["exact_replay"]["max_abs_error"] == 0.0
        for case in unit["valid_recipe_cases"]
    )
    assert all(
        case["execution_receipt"]
        == {
            "compiled": True,
            "executed": True,
            "closed": True,
            "resource_reconciled": True,
        }
        for case in unit["valid_recipe_cases"]
    )
    assert all(
        len(case["step_receipts"]) == case["compiled_operation_count"]
        and case["resource_reconciled"]
        and case["lifecycle_receipt"]["post_termination_nonfinal_validation"]["passed"]
        and case["constitution_receipt"]["passed"]
        and case["public_observation_receipt"]["step_surface_count"]
        == case["compiled_operation_count"]
        and case["evaluation_receipt"]
        and case["elapsed_s"] >= 0.0
        and case["trajectory_bytes"] > 0
        for case in unit["valid_recipe_cases"]
    )
