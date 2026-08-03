from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.policy_validity_matrix import (
    MatrixCell,
    build_preflight,
    load_matrix_protocol,
    validate_formal_qualification_receipt,
)
from chemworld.eval.policy_validity_qualification import (
    PolicyQualificationError,
    build_qualification,
    load_qualification_protocol,
    qualification_source_manifest,
    synthetic_qualification_execution,
    validate_qualification_protocol,
)
from chemworld.eval.provenance import file_sha256

ROOT = Path(__file__).resolve().parents[1]
QUALIFICATION_PROTOCOL_PATH = (
    ROOT / "configs/benchmark/work_i_policy_control_qualification_v0.1.json"
)
MATRIX_PROTOCOL_PATH = (
    ROOT / "configs/benchmark/work_i_policy_control_matrix_v0.1.json"
)


@pytest.fixture(scope="module")
def qualification_result(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[dict[str, Any], dict[str, Any], str, Path]:
    artifact_root = tmp_path_factory.mktemp("v07-qualification") / "artifacts"
    report, receipt, markdown = build_qualification(
        root=ROOT,
        protocol_path=QUALIFICATION_PROTOCOL_PATH,
        artifact_root=artifact_root,
    )
    return report, receipt, markdown, artifact_root


def test_qualification_protocol_is_frozen_and_source_complete() -> None:
    protocol = load_qualification_protocol(QUALIFICATION_PROTOCOL_PATH)
    assert validate_qualification_protocol(protocol) == []
    assert protocol["formal_world_seeds_excluded"] == [0, 1, 2, 3, 4]
    assert protocol["live_smoke"]["world_seed"] == 20_000
    assert protocol["synthetic_matrix"]["execution_mode"] == "injected_test"
    sources = qualification_source_manifest(ROOT, protocol)
    assert set(sources) == set(protocol["source_paths"])
    assert sources["src/chemworld/eval/policy_validity_audit.py"] == file_sha256(
        ROOT / "src/chemworld/eval/policy_validity_audit.py"
    )


def test_protocol_rejects_formal_live_seed_and_one_branch_synthetic_vector() -> None:
    protocol = load_qualification_protocol(QUALIFICATION_PROTOCOL_PATH)
    drifted = deepcopy(protocol)
    drifted["live_smoke"]["world_seed"] = 0
    drifted["synthetic_matrix"]["threshold_signals"] = [0.02] * 6
    errors = validate_qualification_protocol(drifted)
    assert "live qualification seed overlaps a formal world" in errors
    assert "synthetic threshold vector must exercise both branches" in errors


def test_synthetic_execution_uses_qualification_only_identity() -> None:
    protocol = load_qualification_protocol(QUALIFICATION_PROTOCOL_PATH)
    matrix_protocol = load_matrix_protocol(MATRIX_PROTOCOL_PATH)
    cell = MatrixCell(
        ordinal=1,
        cell_id="cell-01-world-0000-opaque-assay-all",
        world_seed=0,
        information_arm="opaque_codes",
        policy_id="assay_all",
        material_information={"mode": "opaque_codes"},
    )
    execution = synthetic_qualification_execution(
        cell,
        matrix_protocol,
        execution_role="original",
        qualification_protocol=protocol,
    )
    identity = execution["identity"]
    assert identity["world_id"].startswith("qualification-synthetic-world-")
    assert identity["physical_identity"]["formal_chemical_world"] is False
    assert execution["counts"]["closed_lifecycle_count"] == 6
    assert execution["counts"]["provider_call_count"] == 0


def test_complete_dual_path_qualification_passes_and_is_nonformal(
    qualification_result: tuple[dict[str, Any], dict[str, Any], str, Path],
) -> None:
    report, receipt, markdown, _ = qualification_result
    assert report["status"] == "qualified_and_frozen"
    assert report["formal_result"] is False
    assert report["formal_environment_execution_count"] == 0
    assert report["formal_outcome_read_count"] == 0
    assert all(report["qualification_gates"].values())
    assert report["synthetic_matrix"]["counts"] == {
        "campaigns": 30,
        "closed_lifecycles": 180,
        "threshold_assays": 30,
        "threshold_discards": 30,
        "provider_calls": 0,
    }
    assert report["live_smoke"]["counts"] == {
        "primary_campaigns": 6,
        "primary_closed_lifecycles": 36,
        "retest_campaigns": 6,
        "retest_closed_lifecycles": 36,
        "formal_campaigns": 0,
        "formal_closed_lifecycles": 0,
        "provider_calls": 0,
    }
    assert receipt["qualification_gates"]["runner_qualified"] is True
    assert receipt["qualification_gates"]["protocol_frozen"] is True
    assert "No formal chemical world was instantiated" in markdown


def test_receipt_passes_v05_validator_and_tampering_fails(
    qualification_result: tuple[dict[str, Any], dict[str, Any], str, Path],
) -> None:
    _, receipt, _, _ = qualification_result
    preflight = build_preflight(ROOT, MATRIX_PROTOCOL_PATH)
    assert validate_formal_qualification_receipt(receipt, preflight=preflight) == []
    tampered = deepcopy(receipt)
    tampered["bindings"]["auditor_sha256"] = "0" * 64
    assert "formal qualification receipt self-hash mismatch" in (
        validate_formal_qualification_receipt(tampered, preflight=preflight)
    )


def test_artifact_manifest_binds_every_generated_file(
    qualification_result: tuple[dict[str, Any], dict[str, Any], str, Path],
) -> None:
    report, _, _, artifact_root = qualification_result
    entries = report["artifact_manifest"]
    assert entries
    assert len(entries) == len(
        [path for path in artifact_root.rglob("*") if path.is_file()]
    )
    for entry in entries:
        path = artifact_root / entry["path"]
        assert path.stat().st_size == entry["byte_count"]
        assert file_sha256(path) == entry["file_sha256"]


def test_refuses_to_overwrite_qualification_artifacts(tmp_path: Path) -> None:
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "sentinel").write_text("preserve", encoding="utf-8")
    with pytest.raises(PolicyQualificationError, match="refusing to overwrite"):
        build_qualification(
            root=ROOT,
            protocol_path=QUALIFICATION_PROTOCOL_PATH,
            artifact_root=occupied,
        )
