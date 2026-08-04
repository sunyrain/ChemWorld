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

ROOT = Path(__file__).resolve().parents[1]


def test_launch_denominators_bind_current_registry_without_old_protocol() -> None:
    receipt = validate_launch_preconditions(ROOT, require_clean=False)
    assert receipt["status"] == "passed"
    assert receipt["qualification_design_version"].endswith("-v1")
    baseline = build_task_structure_baseline(ROOT)
    assert baseline["registered_task_count"] == 15
    assert baseline["world_unit_count"] == EXPECTED_REFERENCE_UNIT_COUNT
    assert "observation" in baseline["coverage"]["components"]


def test_compile_mutants_fail_closed_with_frozen_diagnostics() -> None:
    report = run_compile_mutants()
    assert report["passed"] == report["denominator"] == EXPECTED_COMPILE_MUTANT_COUNT
    assert all(not row["environment_constructed"] for row in report["mutants"])


def test_module_and_interface_probes_cover_frozen_denominators() -> None:
    modules = run_module_probes()
    assert modules["passed"] == modules["denominator"] == EXPECTED_MODULE_PROBE_COUNT
    with tempfile.TemporaryDirectory() as tmp:
        generated = run_generated_qualification(scratch_dir=Path(tmp))
    assert generated["passed"] == generated["denominator"] == EXPECTED_GENERATED_CASE_COUNT
    interfaces = build_interface_receipts(generated)
    assert interfaces["passed"] == interfaces["denominator"] == EXPECTED_INTERFACE_PATH_COUNT


def test_frozen_reference_denominators_remain_exact() -> None:
    assert EXPECTED_REFERENCE_UNIT_COUNT == 64
    assert EXPECTED_REFERENCE_RECIPE_COUNT == 1786
    assert EXPECTED_NEGATIVE_PROBE_COUNT == 192
