from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from chemworld.eval.experiment_1_confirmation import (
    ELIGIBLE_LOCI,
    EXCLUDED_LOCI,
    EXECUTION_COUNTS,
    GATES,
    GENERATOR_VERSION,
    NOISE_VERSION,
    _development_coordinates,
    build_preflight,
    realize_secret_plan,
    validate_public_contract,
    validate_secret_plan,
    write_secret_once,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]


def _source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _minimal_contract(
    plan_path: Path, salt_path: Path, plan: dict[str, object]
) -> dict[str, object]:
    protocol = (
        ROOT / "workstreams/flagship_tasks/experiment_1/EXPERIMENT_1_CONFIRMATION_PROTOCOL_V1_0.md"
    )
    note = ROOT / "workstreams/flagship_tasks/experiment_1/EXPERIMENT_1_CONFIRMATION_NOTE_V1_0.md"
    probe_path = (
        ROOT
        / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_PROBES_V1_2.json"
    )
    audit_path = (
        ROOT
        / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CHALLENGE_AUDIT_V1_2.json"
    )
    registry_path = (
        ROOT
        / "workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json"
    )
    probe = json.loads(probe_path.read_text())
    audit = json.loads(audit_path.read_text())
    registry = json.loads(registry_path.read_text())
    development = _development_coordinates(ROOT)
    units = [
        {
            "unit_id": f"{block.split('-')[0]}-{world}:{block[-1]}",
            "block": block,
            "world_id": f"{block.split('-')[0]}-{world}",
            "truth_sha256": "a" * 64,
            "public_prior_sha256": "b" * 64,
            "q_thresholds": list(GATES),
        }
        for block in ELIGIBLE_LOCI
        for world in (f"W{index:02d}" for index in range(1, 6))
    ]
    contract: dict[str, object] = {
        "schema_version": "chemworld-experiment-1-confirmation-contract-1.0",
        "eligible_loci": list(ELIGIBLE_LOCI),
        "excluded_loci": list(EXCLUDED_LOCI),
        "source_commit": _source_commit(),
        "denominators": {
            "atomic_units": 35,
            "planned_primary_executions": sum(EXECUTION_COUNTS.values()),
        },
        "implementation_files": [],
        "source_contracts": {},
        "protocol": {
            "path": protocol.relative_to(ROOT).as_posix(),
            "file_sha256": file_sha256(protocol),
        },
        "experiment_note": {
            "path": note.relative_to(ROOT).as_posix(),
            "file_sha256": file_sha256(note),
        },
        "challenge": {
            "probe_path": probe_path.relative_to(ROOT).as_posix(),
            "probe_file_sha256": file_sha256(probe_path),
            "challenge_probe_sha256": probe["challenge_probe_sha256"],
            "audit_path": audit_path.relative_to(ROOT).as_posix(),
            "audit_file_sha256": file_sha256(audit_path),
            "audit_sha256": audit["audit_sha256"],
        },
        "convergence_registry": {
            "path": registry_path.relative_to(ROOT).as_posix(),
            "file_sha256": file_sha256(registry_path),
            "registry_sha256": registry["registry_sha256"],
        },
        "development_coordinate_contract": development,
        "development_coordinate_contract_sha256": canonical_json_sha256(development),
        "units": units,
        "generator": {
            "generator_version": GENERATOR_VERSION,
            "secret_salt_file_sha256": file_sha256(salt_path),
            "realized_plan_file_sha256": file_sha256(plan_path),
            "realized_plan_sha256": plan["plan_sha256"],
        },
        "noise": {"noise_version": NOISE_VERSION},
    }
    contract["contract_sha256"] = canonical_json_sha256(contract)
    return contract


def test_secret_generator_is_deterministic_and_excludes_blocked_loci() -> None:
    salt = bytes(range(32))
    first = realize_secret_plan(ROOT, salt, source_commit="a" * 40)
    second = realize_secret_plan(ROOT, salt, source_commit="a" * 40)

    assert first == second
    assert tuple(first["loci"]) == ELIGIBLE_LOCI
    assert tuple(first["excluded_loci"]) == EXCLUDED_LOCI
    validate_secret_plan(ROOT, first)


def test_secret_plan_tamper_and_development_overlap_fail_closed() -> None:
    plan = realize_secret_plan(ROOT, b"x" * 32, source_commit="a" * 40)
    plan["loci"]["PA-E"]["solvent_anchors"] = [0, 2]
    plan["plan_sha256"] = canonical_json_sha256(
        {key: value for key, value in plan.items() if key != "plan_sha256"}
    )
    with pytest.raises(ValueError, match="held-out solvent anchors"):
        validate_secret_plan(ROOT, plan)

    plan["plan_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="canonical self-hash"):
        validate_secret_plan(ROOT, plan)


def test_preflight_enforces_secret_permissions_and_commitments(tmp_path: Path) -> None:
    secret_dir = tmp_path / "sealed"
    secret_dir.mkdir(mode=0o700)
    os.chmod(secret_dir, 0o700)
    salt_path = secret_dir / "salt.bin"
    plan_path = secret_dir / "realized-plan.json"
    salt = b"z" * 32
    write_secret_once(salt_path, salt)
    plan = realize_secret_plan(ROOT, salt, source_commit=_source_commit())
    write_secret_once(
        plan_path,
        (json.dumps(plan, indent=2, sort_keys=True) + "\n").encode(),
    )
    contract = _minimal_contract(plan_path, salt_path, plan)
    receipt = build_preflight(
        ROOT,
        contract,
        secret_dir=secret_dir,
        output_root=tmp_path / "unused-output",
    )
    assert receipt["atomic_units"] == 35
    assert receipt["planned_primary_executions"] == 1585
    assert receipt["confirmation_execution_authorized"] is False

    os.chmod(plan_path, 0o644)
    with pytest.raises(ValueError, match="0600"):
        build_preflight(
            ROOT,
            contract,
            secret_dir=secret_dir,
            output_root=tmp_path / "another-output",
        )


def test_public_contract_rejects_denominator_or_locus_expansion() -> None:
    contract: dict[str, object] = {
        "schema_version": "chemworld-experiment-1-confirmation-contract-1.0",
        "eligible_loci": [*ELIGIBLE_LOCI, "PA-P"],
        "excluded_loci": list(EXCLUDED_LOCI),
        "denominators": {
            "atomic_units": 40,
            "planned_primary_executions": sum(EXECUTION_COUNTS.values()),
        },
        "implementation_files": [],
        "source_contracts": {},
        "units": [],
    }
    contract["contract_sha256"] = canonical_json_sha256(contract)
    with pytest.raises(ValueError, match="seven-locus denominator"):
        validate_public_contract(ROOT, contract)
