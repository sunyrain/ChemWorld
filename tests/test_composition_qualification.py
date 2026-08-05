from __future__ import annotations

import tempfile
from pathlib import Path

from chemworld.eval.composition_qualification import (
    EXPECTED_COMPILE_MUTANT_COUNT,
    EXPECTED_GENERATED_CASE_COUNT,
    EXPECTED_INTERFACE_PATH_COUNT,
    EXPECTED_MODULE_PROBE_COUNT,
    EXPECTED_NEGATIVE_PROBE_COUNT,
    EXPECTED_REFERENCE_RECIPE_COUNT,
    EXPECTED_REFERENCE_UNIT_COUNT,
    build_interface_receipts,
    build_task_structure_baseline,
    run_compile_mutants,
    run_generated_qualification,
    run_module_probes,
    validate_launch_preconditions,
)
from chemworld.eval.composition_qualification_design import QUALIFICATION_DESIGN_VERSION

ROOT = Path(__file__).resolve().parents[1]


def test_launch_denominators_bind_current_registry_without_old_protocol() -> None:
    receipt = validate_launch_preconditions(ROOT, require_clean=False)
    assert receipt["status"] == "passed"
    assert receipt["qualification_design_version"] == QUALIFICATION_DESIGN_VERSION
    baseline = build_task_structure_baseline(ROOT)
    assert baseline["registered_task_count"] == 15
    assert baseline["world_unit_count"] == EXPECTED_REFERENCE_UNIT_COUNT
    assert "observation" in baseline["coverage"]["components"]
    assert baseline["coverage"]["interfaces"]
    assert baseline["coverage"]["observations"]
    assert all(task["interfaces"] for task in baseline["tasks"])
    assert all(task["observations"] for task in baseline["tasks"])


def test_compile_mutants_fail_closed_with_frozen_diagnostics() -> None:
    report = run_compile_mutants()
    assert report["passed"] == report["denominator"] == EXPECTED_COMPILE_MUTANT_COUNT
    assert all(not row["environment_constructed"] for row in report["mutants"])


def test_module_and_interface_probes_cover_frozen_denominators() -> None:
    modules = run_module_probes()
    assert modules["passed"] == modules["denominator"] == EXPECTED_MODULE_PROBE_COUNT
    legal_probes = [probe for probe in modules["probes"] if probe["probe_id"] == "legal_low_high"]
    assert len(legal_probes) == 8
    numerical = [
        probe for probe in legal_probes if probe["classification"] == "numerical_reference_fixture"
    ]
    conceptual = [
        probe for probe in legal_probes if probe["classification"] == "conceptual_or_synthetic"
    ]
    assert {probe["module_id"] for probe in conceptual} == {"crystallization"}
    assert len(numerical) == 7
    for probe in numerical:
        for boundary in ("low", "high"):
            fixture = probe["receipt"][boundary]["reference_fixture"]
            assert fixture["within_tolerance"] is True
            assert fixture["absolute_error"] <= fixture["tolerance"]
    with tempfile.TemporaryDirectory() as tmp:
        generated = run_generated_qualification(scratch_dir=Path(tmp))
    assert generated["passed"] == generated["denominator"] == EXPECTED_GENERATED_CASE_COUNT
    assert generated["unseen_reference_task_id_overlap"] == []
    assert set(generated["depth_summary"]) == {
        "component_count",
        "workflow_stage_count",
        "action_count",
    }
    assert all(
        case["execution_receipt"]
        == {
            "compiled": True,
            "executed": True,
            "closed": True,
            "resource_reconciled": True,
        }
        for case in generated["cases"]
    )
    assert all(
        len(case["step_receipts"]) == case["action_count"]
        and case["resource_receipt"]["passed"]
        and case["termination_receipt"]["post_termination_validation"]["passed"]
        and case["constitution_receipt"]["passed"]
        and case["interface_receipt"]["passed"]
        and case["public_observation_receipt"]["step_surface_count"] == case["action_count"]
        for case in generated["cases"]
    )
    unseen = [case for case in generated["cases"] if case["pattern"] == generated["unseen_pattern"]]
    assert [case["generation_index"] for case in unseen] == list(range(8))
    assert {case["generation_seed"] for case in unseen} == {105}
    assert all(case["composition_request"] for case in unseen)
    interfaces = build_interface_receipts(generated)
    assert interfaces["passed"] == interfaces["denominator"] == EXPECTED_INTERFACE_PATH_COUNT
    expected_checks = {
        "material_identity",
        "unit",
        "nonnegative_amount",
        "material_balance",
        "charge_balance",
        "energy_balance",
        "phase_balance",
        "state_identity",
        "event_propagation",
        "transaction_atomicity",
        "resource_reconciliation",
        "lifecycle_closure",
        "public_private_boundary",
        "exact_replay",
    }
    assert all(set(path["checks"]) == expected_checks for path in interfaces["paths"])
    assert all(len(path["case_receipts"]) == path["case_count"] for path in interfaces["paths"])


def test_frozen_reference_denominators_remain_exact() -> None:
    assert EXPECTED_REFERENCE_UNIT_COUNT == 64
    assert EXPECTED_REFERENCE_RECIPE_COUNT == 1786
    assert EXPECTED_NEGATIVE_PROBE_COUNT == 192
