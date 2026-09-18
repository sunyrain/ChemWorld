from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_experiment_1_challenge.py"
REGISTRY = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json"
)
LEGACY_PROBES = (
    ROOT
    / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_PROBES_V1_1_1.json"
)


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_challenge_audit", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unrepaired_restart1_is_not_a_current_positive_audit_golden() -> None:
    with pytest.raises(ValueError, match="exact registry binding"):
        _module().build_audit(REGISTRY, LEGACY_PROBES)
