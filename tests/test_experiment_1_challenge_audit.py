from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_experiment_1_challenge.py"
REGISTRY = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json"
)
PROBES = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_PROBES_V1_2.json"
)


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_challenge_audit", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_challenge_audit_uses_current_v1_2_locus_wise_outcome() -> None:
    audit = _module().build_audit(REGISTRY, PROBES)

    assert audit["candidate_loci"] == 10
    assert audit["confirmation_eligible_loci"] == 7
    assert audit["confirmation_blocked_loci"] == 3
    assert audit["participant_execution_authorized"] is False
    assert audit["provider_call_count"] == 0
    decisions = {row["block"]: row["confirmation_eligible"] for row in audit["loci"]}
    assert {block for block, eligible in decisions.items() if not eligible} == {
        "RX-S",
        "PA-P",
        "PA-S",
    }
    assert all(
        eligible for block, eligible in decisions.items() if block not in {"RX-S", "PA-P", "PA-S"}
    )
