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
        "current_evidence",
        "lint",
        "type_check",
        "tests",
        "docs",
        "wheel_smoke",
        "reference_validation",
        "runtime_boundary_audit",
        "model_reachability_audit",
        "environment_audit",
        "baseline_smoke",
        "benchmark_candidate_integrity",
    ]
    flat_commands = [" ".join(item["command"]) for item in plan]
    assert any("manage_claims.py check" in command for command in flat_commands)
    assert any("evidence_pipeline.py --check" in command for command in flat_commands)
    assert any("ruff check ." in command for command in flat_commands)
    assert any("mypy src/chemworld" in command for command in flat_commands)
    assert any("pytest" in command for command in flat_commands)
    assert any("mkdocs build --strict" in command for command in flat_commands)
    assert any("smoke_test_wheel.py" in command for command in flat_commands)
    assert any("run_reference_validation.py" in command for command in flat_commands)
    assert any("audit_model_reachability.py" in command for command in flat_commands)
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


def test_release_gate_binds_the_candidate_backend_without_enabling_claims() -> None:
    namespace = runpy.run_path("scripts/run_release_gate.py", run_name="release_gate")
    evidence = namespace["_backend_evidence"]()

    assert evidence["status"] in {
        "candidate_backend_clean_attested",
        "candidate_backend_validated_dirty_tree",
    }
    assert evidence["backend_contract_validated"] is True
    if evidence["clean_release_attestation"] == "passed":
        assert evidence["backend_freeze_allowed"] is True
    else:
        assert evidence["backend_freeze_allowed"] is False
    assert evidence["benchmark_claim_allowed"] is False
    assert len(evidence["file_sha256"]) == 64


def test_release_gate_fails_when_head_changes_during_the_run() -> None:
    namespace = runpy.run_path("scripts/run_release_gate.py", run_name="release_gate")
    source_state_control = namespace["_source_state_control"]

    stable = source_state_control(
        source_commit="abc", finished_source_commit="abc", dirty_at_finish=False
    )
    changed = source_state_control(
        source_commit="abc", finished_source_commit="def", dirty_at_finish=False
    )
    dirty = source_state_control(
        source_commit="abc", finished_source_commit="abc", dirty_at_finish=True
    )
    dirty_candidate = source_state_control(
        source_commit="abc",
        finished_source_commit="abc",
        dirty_at_finish=True,
        allow_dirty_candidate=True,
    )

    assert stable["status"] == "passed"
    assert stable["source_integrity_passed"] is True
    assert stable["source_commit_stable"] is True
    assert changed["status"] == "blocked"
    assert changed["source_integrity_passed"] is False
    assert changed["source_commit_stable"] is False
    assert dirty["source_integrity_passed"] is False
    assert dirty_candidate["source_integrity_passed"] is True
    assert dirty_candidate["dirty_candidate_mode"] is True


def test_release_gate_has_one_canonical_lifecycle_status() -> None:
    namespace = runpy.run_path("scripts/run_release_gate.py", run_name="release_gate")
    release_status = namespace["_release_status"]

    assert release_status(succeeded=False, require_frozen_benchmark=False) == "blocked"
    assert (
        release_status(succeeded=True, require_frozen_benchmark=False)
        == "candidate_gate_passed"
    )
    assert release_status(succeeded=True, require_frozen_benchmark=True) == "release_ready"
