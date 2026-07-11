from __future__ import annotations

import json
import runpy
import subprocess
import sys


def test_release_gate_dry_run_lists_required_commands(tmp_path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_release_gate.py",
            "--dry-run",
            "--output-dir",
            str(tmp_path / "gate"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    plan = json.loads(completed.stdout)
    names = [item["name"] for item in plan]
    assert names == [
        "claims",
        "lint",
        "type_check",
        "tests",
        "docs",
        "wheel_smoke",
        "reference_validation",
        "runtime_boundary_audit",
        "model_reachability_audit",
        "model_adapter_intake",
        "vnext_staging_plan",
        "environment_audit",
        "baseline_smoke",
        "benchmark_candidate_integrity",
    ]
    flat_commands = [" ".join(item["command"]) for item in plan]
    assert any("manage_claims.py check" in command for command in flat_commands)
    assert any("ruff check ." in command for command in flat_commands)
    assert any("mypy src/chemworld" in command for command in flat_commands)
    assert any("pytest" in command for command in flat_commands)
    assert any("mkdocs build --strict" in command for command in flat_commands)
    assert any("smoke_test_wheel.py" in command for command in flat_commands)
    assert any("run_reference_validation.py" in command for command in flat_commands)
    assert any("audit_model_reachability.py" in command for command in flat_commands)
    assert any("validate_model_adapters.py" in command for command in flat_commands)
    assert any("build_vnext_integration_plan.py" in command for command in flat_commands)
    assert any("audit_environment_consistency.py" in command for command in flat_commands)
    assert any("baselines report" in command for command in flat_commands)
    assert any("check_frozen_benchmark.py" in command for command in flat_commands)
    assert any("--allow-candidate" in command for command in flat_commands)


def test_release_gate_can_require_strict_frozen_benchmark(tmp_path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_release_gate.py",
            "--dry-run",
            "--require-frozen-benchmark",
            "--output-dir",
            str(tmp_path / "gate"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    plan = json.loads(completed.stdout)
    frozen = next(item for item in plan if item["name"] == "frozen_benchmark")
    assert "--allow-candidate" not in frozen["command"]
    wheel_smoke = next(item for item in plan if item["name"] == "wheel_smoke")
    assert "--require-validated-benchmark" in wheel_smoke["command"]


def test_reference_gate_requires_every_backend_used_by_reference_tests() -> None:
    namespace = runpy.run_path("scripts/run_reference_validation.py", run_name="reference_gate")

    assert set(namespace["REFERENCE_MODULES"]) == {
        "cantera",
        "chemicals",
        "fluids",
        "thermo",
    }
