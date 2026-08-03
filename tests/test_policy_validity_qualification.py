from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.campaign_resources import campaign_resource_event_id
from chemworld.eval.policy_validity_matrix import (
    MatrixCell,
    build_preflight,
    load_matrix_protocol,
    semantic_sha256,
    validate_formal_qualification_receipt,
)
from chemworld.eval.policy_validity_qualification import (
    PolicyQualificationError,
    assert_qualification_outputs_absent,
    build_qualification,
    build_qualification_delivery_manifest,
    derive_live_smoke_protocol,
    load_qualification_protocol,
    qualification_source_manifest,
    synthetic_qualification_execution,
    validate_live_smoke_protocol,
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


def test_live_protocol_is_self_describing_one_by_two_by_three() -> None:
    qualification_protocol = load_qualification_protocol(
        QUALIFICATION_PROTOCOL_PATH
    )
    matrix_protocol = load_matrix_protocol(MATRIX_PROTOCOL_PATH)
    live_protocol = derive_live_smoke_protocol(
        matrix_protocol, qualification_protocol
    )
    assert validate_live_smoke_protocol(live_protocol, qualification_protocol) == []
    assert live_protocol["matrix"] == {
        "world_seeds": [20_000],
        "information_arms": ["opaque_codes", "anonymous_nominal_properties"],
        "policy_ids": [
            "assay_all",
            "start_then_discard",
            "measure_then_threshold",
        ],
        "lifecycles_per_campaign": 6,
        "primary_campaign_count": 6,
        "primary_closed_lifecycle_count": 36,
        "provider_call_count": 0,
        "schedule_order": "world_then_arm_then_policy",
    }
    assert live_protocol["qualification_context"]["formal_result"] is False
    drifted = deepcopy(live_protocol)
    drifted["matrix"]["primary_campaign_count"] = 30
    assert "derived live protocol matrix is not the frozen 1 x 2 x 3 smoke" in (
        validate_live_smoke_protocol(drifted, qualification_protocol)
    )


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
    retest = synthetic_qualification_execution(
        cell,
        matrix_protocol,
        execution_role="retest",
        qualification_protocol=protocol,
    )
    identity = execution["identity"]
    assert identity["world_id"].startswith("qualification-synthetic-world-")
    assert identity["cell_id"] == cell.cell_id
    assert identity["campaign_id"] == identity["cell_id"]
    assert execution["profile_record"]["identity"]["campaign_id"] == identity[
        "campaign_id"
    ]
    assert identity["qualification_only"] is True
    assert identity["qualification_namespace"] == (
        "work-i-policy-control-runner-qualification-v0.1"
    )
    assert identity["qualification_role"] == "injected_synthetic_runner_audit"
    assert identity["observation_noise_namespace"] == (
        "injected-synthetic-keyed-v07-qualification--world-0000"
    )
    assert identity["physical_identity"]["formal_chemical_world"] is False
    assert execution["counts"]["closed_lifecycle_count"] == 6
    assert execution["counts"]["provider_call_count"] == 0
    assert retest["identity"] == identity
    expected_logical_id = (
        "work-i-policy-control-runner-qualification-v0.1--synthetic-resource--"
        "world-0000-assay_all"
    )
    assert execution["campaign_resource_ledger"]["events"][0][
        "event_id"
    ] == campaign_resource_event_id(expected_logical_id, 1)

    matched_arm = MatrixCell(
        ordinal=4,
        cell_id="cell-04-world-0000-anonymous-nominal-assay-all",
        world_seed=0,
        information_arm="anonymous_nominal_properties",
        policy_id="assay_all",
        material_information={"mode": "anonymous_nominal_properties"},
    )
    matched_execution = synthetic_qualification_execution(
        matched_arm,
        matrix_protocol,
        execution_role="original",
        qualification_protocol=protocol,
    )
    assert matched_execution["identity"]["observation_noise_namespace"] == identity[
        "observation_noise_namespace"
    ]
    assert matched_execution["identity"]["material_information_sha256"] != identity[
        "material_information_sha256"
    ]


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


def test_outer_delivery_manifest_binds_top_level_and_payload_files(
    qualification_result: tuple[dict[str, Any], dict[str, Any], str, Path],
) -> None:
    report, receipt, markdown, artifact_root = qualification_result
    protocol = load_qualification_protocol(QUALIFICATION_PROTOCOL_PATH)
    delivery = build_qualification_delivery_manifest(
        qualification_protocol=protocol,
        artifact_root=artifact_root,
        report=report,
        receipt=receipt,
        markdown=markdown,
    )
    assert delivery["status"] == "complete"
    assert delivery["entry_count"] == len(report["artifact_manifest"]) + 3
    assert delivery["delivery_manifest_sha256"] == semantic_sha256(
        {
            key: value
            for key, value in delivery.items()
            if key != "delivery_manifest_sha256"
        }
    )
    roles = [entry["role"] for entry in delivery["entries"]]
    for role in (
        "qualification_report",
        "formal_qualification_receipt",
        "qualification_markdown",
    ):
        assert roles.count(role) == 1
    nested = [
        entry for entry in delivery["entries"] if entry["role"] == "qualification_artifact"
    ]
    assert len(nested) == len(report["artifact_manifest"])
    artifact_prefix = f"{protocol['output_paths']['artifact_root']}/"
    assert [
        {
            "path": entry["path"].removeprefix(artifact_prefix),
            "file_sha256": entry["file_sha256"],
            "byte_count": entry["byte_count"],
        }
        for entry in nested
    ] == report["artifact_manifest"]


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


@pytest.mark.parametrize("occupied_field", ["artifact_root", "report", "markdown", "receipt"])
def test_noncheck_run_refuses_any_existing_output(
    tmp_path: Path, occupied_field: str
) -> None:
    protocol = load_qualification_protocol(QUALIFICATION_PROTOCOL_PATH)
    rewritten = deepcopy(protocol)
    rewritten["output_paths"] = {
        field: f"outputs/{Path(str(path)).name}"
        for field, path in protocol["output_paths"].items()
    }
    occupied = tmp_path / str(rewritten["output_paths"][occupied_field])
    if occupied_field == "artifact_root":
        occupied.mkdir(parents=True)
    else:
        occupied.parent.mkdir(parents=True, exist_ok=True)
        occupied.write_text("sentinel", encoding="utf-8")
    with pytest.raises(PolicyQualificationError, match="refusing to overwrite"):
        assert_qualification_outputs_absent(tmp_path, rewritten)
    assert occupied.exists()
