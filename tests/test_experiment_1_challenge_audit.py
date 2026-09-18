from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_experiment_1_challenge.py"
REGISTRY = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json"
)
PROBES = ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_PROBES.json"


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_challenge_audit", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_challenge_audit_is_locus_wise_and_retains_pa_parametric_failure() -> None:
    audit = _module().build_audit(REGISTRY, PROBES)

    assert audit["candidate_loci"] == 10
    assert audit["confirmation_eligible_loci"] == 9
    assert audit["confirmation_blocked_loci"] == 1
    assert audit["participant_execution_authorized"] is False
    assert audit["provider_call_count"] == 0
    pa_parametric = next(row for row in audit["loci"] if row["block"] == "PA-P")
    assert pa_parametric["confirmation_eligible"] is False
    assert pa_parametric["checks"]["plausibility"]["status"] == "passed"
    assert pa_parametric["checks"]["information_choice"]["status"] == "passed"
    assert pa_parametric["checks"]["non_triviality"]["status"] == "failed"
    assert pa_parametric["checks"]["budget_window"]["status"] == "failed"
    assert all(
        row["confirmation_eligible"] is True for row in audit["loci"] if row["block"] != "PA-P"
    )
