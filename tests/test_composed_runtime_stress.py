from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.composed_runtime_stress import (
    load_composed_runtime_stress_protocol,
    run_composed_runtime_stress,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = (
    ROOT / "workstreams" / "world_foundation" / "reports" / "composed-runtime-stress-v0.5.json"
)


def test_composed_stress_report_covers_full_registered_graph() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["coverage"] == {
        "operation_count": 28,
        "profile_executed_step_count": 396,
        "profile_run_count": 45,
        "provider_count": 20,
        "runtime_failure_count": 0,
        "runtime_failure_rate": 0.0,
        "task_count": 15,
        "task_operation_pair_count": 163,
    }
    assert all(report["controls"].values())
    assert report["clean_wheel_replay"]["passed"] is True
    assert report["clean_wheel_replay"]["separate_process"] is True
    assert report["clean_wheel_replay"]["wheel_import"] is True
    assert report["clean_wheel_replay"]["exact_replay"] is True


def test_boundary_nominal_and_upper_profiles_replay_exactly() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert len(report["profile_runs"]) == 45
    assert {item["profile"] for item in report["profile_runs"]} == {
        "lower_boundary",
        "nominal",
        "upper_boundary",
    }
    for item in report["profile_runs"]:
        assert item["deterministic_replay"] is True
        assert item["all_transactions_committed"] is True
        assert item["constitution_failure_count"] == 0
        assert item["precondition_failure_count"] == 0
        assert item["nonfinite_observation_count"] == 0
        assert item["runtime_failure_count"] == 0
        assert item["task_contract_hash"]
        assert item["runtime_profile_hash"]
        assert item["world_law_id"] == "chemworld-physical-chemistry-v0.5"


def test_required_multiphysics_chains_execute_and_replay() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert set(report["composed_chains"]) == {
        "reaction-to-purification",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
        "electrochemical-conversion",
        "equilibrium-characterization",
    }
    for chain in report["composed_chains"].values():
        assert chain["required_operations_present"] is True
        assert chain["required_modules_present"] is True
        assert chain["all_transactions_committed"] is True
        assert chain["deterministic_replay"] is True


def test_missing_chain_requirement_fails_closed() -> None:
    protocol = copy.deepcopy(load_composed_runtime_stress_protocol())
    protocol["required_chains"]["flow-reaction-optimization"][
        "required_operations"
    ].append("distill")
    report = run_composed_runtime_stress(protocol)
    assert report["controls_ready"] is False
    assert report["controls"]["required_composed_chains_execute"] is False


def test_stress_audit_does_not_name_runtime_reference_fixture() -> None:
    module_path = ROOT / "src" / "chemworld" / "eval" / "composed_runtime_stress.py"
    assert "reaction_reference" not in module_path.read_text(encoding="utf-8")
