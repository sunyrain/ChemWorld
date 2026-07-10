from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from scripts.manage_claims import complete_claim, create_claim

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelExecutionRole,
    ModelProviderContract,
)
from chemworld.runtime.model_adapter_intake import validate_adapter_manifests


def _prepare_claim(root: Path, *, complete: bool = False) -> None:
    (root / "claims" / "active").mkdir(parents=True)
    (root / "claims" / "completed").mkdir(parents=True)
    create_claim(
        root,
        task_id="wf-20-instruments",
        owner="instrument-team",
        branch="team/wf-20-instruments",
        scope="Instrument provider reference slice",
        owned_paths=["src/example/instrument_provider.py", "tests/example"],
    )
    if complete:
        complete_claim(
            root,
            task_id="wf-20-instruments",
            owner="instrument-team",
            summary="Provider proposal delivered",
        )


def _manifest(*, model_id: str = "instrument_reference_v2") -> ModelAdapterManifest:
    provider = ModelProviderContract(
        model_id=model_id,
        module_id="spectroscopy_instruments",
        maturity=MaturityLevel.REFERENCE_VALIDATED,
        role=ModelExecutionRole.RUNTIME,
        provider_path="chemworld.runtime.kernel_contracts.ContractModelProviderStub",
        input_fields=("sample",),
        output_fields=("signal",),
        units={"sample": "mol", "signal": "a.u."},
        validity_checks=("sample amount is non-negative",),
        diagnostic_fields=("calibration_residual",),
        failure_policy="return a typed failed result",
        provenance=("wf-20-reference-case",),
        intended_operations=("measure",),
    )
    return ModelAdapterManifest(
        adapter_id=f"{model_id}_adapter",
        adapter_version="0.1",
        owner_workstream="wf-20-instruments",
        provider_contract=provider,
        owned_paths=("src/example/instrument_provider.py", "tests/example"),
        integration_operations=("measure",),
        target_world_law="chemworld-physical-chemistry-vnext",
        replaces_model_ids=("chemworld_synthetic_instruments",),
    )


def _write_manifest(root: Path, manifest: ModelAdapterManifest) -> Path:
    path = root / "proposal.json"
    path.write_text(json.dumps(manifest.to_dict()), encoding="utf-8")
    return path


def test_adapter_intake_accepts_active_or_completed_claim(tmp_path: Path) -> None:
    _prepare_claim(tmp_path)
    path = _write_manifest(tmp_path, _manifest())
    active = validate_adapter_manifests([path], repository_root=tmp_path)
    assert active["passed"] is True
    assert active["accepted_count"] == 1
    assert active["manifests"][0]["claim_status"] == "active"

    complete_claim(
        tmp_path,
        task_id="wf-20-instruments",
        owner="instrument-team",
        summary="Provider proposal delivered",
    )
    completed = validate_adapter_manifests([path], repository_root=tmp_path)
    assert completed["passed"] is True
    assert completed["manifests"][0]["claim_status"] == "completed"


def test_adapter_intake_rejects_hash_tampering_and_claim_escape(tmp_path: Path) -> None:
    _prepare_claim(tmp_path)
    payload = _manifest().to_dict()
    payload["adapter_version"] = "tampered"
    tampered = tmp_path / "tampered.json"
    tampered.write_text(json.dumps(payload), encoding="utf-8")
    report = validate_adapter_manifests([tampered], repository_root=tmp_path)
    assert report["passed"] is False
    assert report["manifests"][0]["findings"][0]["check_id"] == "manifest_parse"

    escaped_manifest = _manifest()
    escaped_payload = escaped_manifest.to_dict()
    escaped_payload["owned_paths"] = ["src/unclaimed/provider.py"]
    escaped_payload.pop("manifest_hash")
    escaped = ModelAdapterManifest.from_dict(escaped_payload)
    escaped_path = _write_manifest(tmp_path, escaped)
    report = validate_adapter_manifests([escaped_path], repository_root=tmp_path)
    assert report["passed"] is False
    assert any(
        finding["check_id"] == "owned_path_outside_claim"
        for finding in report["manifests"][0]["findings"]
    )


def test_adapter_intake_requires_hash_target_runtime_provider_and_known_operation(
    tmp_path: Path,
) -> None:
    _prepare_claim(tmp_path)
    manifest = _manifest()

    unsigned = tmp_path / "unsigned.json"
    unsigned_payload = manifest.to_dict()
    unsigned_payload.pop("manifest_hash")
    unsigned.write_text(json.dumps(unsigned_payload), encoding="utf-8")
    report = validate_adapter_manifests([unsigned], repository_root=tmp_path)
    assert {
        finding["check_id"] for finding in report["manifests"][0]["findings"]
    } == {"manifest_hash_required"}

    invalid_provider = replace(
        manifest.provider_contract,
        role=ModelExecutionRole.REFERENCE,
        provider_path="chemworld.missing.Provider",
        intended_operations=("unknown_operation",),
    )
    invalid = replace(
        manifest,
        provider_contract=invalid_provider,
        integration_operations=("unknown_operation",),
        target_world_law="chemworld-physical-chemistry-v0.3",
    )
    invalid_path = _write_manifest(tmp_path, invalid)
    report = validate_adapter_manifests([invalid_path], repository_root=tmp_path)
    check_ids = {
        finding["check_id"] for finding in report["manifests"][0]["findings"]
    }
    assert {
        "target_world_law",
        "unknown_integration_operation",
        "reference_provider_integration",
        "provider_path_resolution",
    }.issubset(check_ids)


def test_adapter_intake_requires_claim_and_shared_path_authority(tmp_path: Path) -> None:
    _prepare_claim(tmp_path)
    missing_claim = replace(_manifest(), owner_workstream="wf-21-unclaimed")
    path = _write_manifest(tmp_path, missing_claim)
    report = validate_adapter_manifests([path], repository_root=tmp_path)
    assert any(
        finding["check_id"] == "claim_required"
        for finding in report["manifests"][0]["findings"]
    )

    shared = replace(
        _manifest(),
        owned_paths=("src/chemworld/runtime/observation_services.py",),
    )
    path = _write_manifest(tmp_path, shared)
    report = validate_adapter_manifests([path], repository_root=tmp_path)
    check_ids = {
        finding["check_id"] for finding in report["manifests"][0]["findings"]
    }
    assert "owned_path_outside_claim" in check_ids
    assert "shared_path_authority" in check_ids


def test_adapter_intake_rejects_conflicts_unknown_replacements_and_duplicates(
    tmp_path: Path,
) -> None:
    _prepare_claim(tmp_path, complete=True)
    conflict = _write_manifest(tmp_path, _manifest(model_id="chemworld_synthetic_instruments"))
    report = validate_adapter_manifests([conflict], repository_root=tmp_path)
    assert report["passed"] is False
    assert any(
        finding["check_id"] == "provider_model_id_conflict"
        for finding in report["manifests"][0]["findings"]
    )

    first_manifest = _manifest(model_id="new_instrument_a")
    first_payload = first_manifest.to_dict()
    first_payload["replaces_model_ids"] = ["missing_old_model"]
    first_payload.pop("manifest_hash")
    first_manifest = ModelAdapterManifest.from_dict(first_payload)
    first = tmp_path / "first.json"
    first.write_text(json.dumps(first_manifest.to_dict()), encoding="utf-8")
    second = tmp_path / "second.json"
    second.write_text(json.dumps(first_manifest.to_dict()), encoding="utf-8")
    report = validate_adapter_manifests([first, second], repository_root=tmp_path)
    assert report["passed"] is False
    for item in report["manifests"]:
        check_ids = {finding["check_id"] for finding in item["findings"]}
        assert "duplicate_adapter_id" in check_ids
        assert "duplicate_provider_model_id" in check_ids
        assert "proposal_owned_path_overlap" in check_ids
        assert "unknown_replacement_model" in check_ids


def test_adapter_intake_cli_allows_empty_discovery_but_can_require_proposals(
    tmp_path: Path,
) -> None:
    output = tmp_path / "intake.json"
    command = [
        sys.executable,
        "scripts/validate_model_adapters.py",
        "--root",
        str(tmp_path),
        "--output",
        str(output),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    assert completed.returncode == 0
    assert json.loads(output.read_text(encoding="utf-8"))["manifest_count"] == 0

    required = subprocess.run(
        [*command, "--require-manifests"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert required.returncode == 1
    assert json.loads(output.read_text(encoding="utf-8"))["passed"] is False
