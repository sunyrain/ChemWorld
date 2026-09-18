from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_experiment_1_challenge.py"
REGISTRY = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json"
)
PROBES = ROOT / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_PROBES.json"


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_challenge_audit_negative", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_audit_rejects_stale_registry_binding(tmp_path: Path) -> None:
    probes = json.loads(PROBES.read_text(encoding="utf-8"))
    probes["source_registry_sha256"] = "stale"
    with pytest.raises(ValueError, match="different convergence registry"):
        _module().build_audit(REGISTRY, _write(tmp_path / "probes.json", probes))


def test_audit_rejects_missing_probe_block(tmp_path: Path) -> None:
    probes = json.loads(PROBES.read_text(encoding="utf-8"))
    probes["loci"].pop()
    with pytest.raises(ValueError, match="ten locus decisions"):
        _module().build_audit(REGISTRY, _write(tmp_path / "probes.json", probes))


def test_audit_rejects_duplicate_registry_rows(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    target = next(
        row
        for row in registry["rows"]
        if row["system_id"] == "EC" and row["prior_locus"] == "entity"
    )
    replacement_index = next(
        index
        for index, row in enumerate(registry["rows"])
        if row["system_id"] == "EC"
        and row["prior_locus"] == "entity"
        and row["unit_id"] != target["unit_id"]
    )
    registry["rows"][replacement_index] = target
    with pytest.raises(ValueError, match="duplicated"):
        _module().build_audit(_write(tmp_path / "registry.json", registry), PROBES)


def test_audit_rejects_stale_candidate_status(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    target = next(
        row
        for row in registry["rows"]
        if row["system_id"] == "EC" and row["prior_locus"] == "entity"
    )
    target["current_status"] = "blocked"
    with pytest.raises(ValueError, match="stale or non-qualified"):
        _module().build_audit(_write(tmp_path / "registry.json", registry), PROBES)
