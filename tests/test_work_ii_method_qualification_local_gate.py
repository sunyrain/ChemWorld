from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import chemworld.eval.work_ii_method_qualification_local as local_gate
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_task_resources import build_task_resource_formula_binding

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
ENTRYPOINTS = (
    ROOT / "scripts/run_work_ii_method_qualification.py",
    ROOT / "scripts/authorize_work_ii_method_qualification.py",
    ROOT / "scripts/run_work_ii_method_qualification_triplet.py",
    ROOT / "scripts/build_work_ii_method_qualification_receipt.py",
)


def _source_config() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(
            encoding="utf-8"
        )
    )


def _w2_27_card(source: dict[str, object]) -> dict[str, object]:
    card: dict[str, object] = {
        "card_identity": {
            **local_gate.W2_27_RESOURCE_CARD_IDENTITY,
            "calibration_campaign_binding": {
                "path": "runtime.json",
                "sha256": "1" * 64,
                "config_canonical_json_sha256": canonical_json_sha256(source),
            },
            "resource_formula_binding": build_task_resource_formula_binding(source),
        },
        "protected_closeout_reserve_enforced": True,
        "proposed_hard_caps": {
            "operation_attempt_limit": 72,
            "protected_closeout_operation_reserve": 16,
            "process_time_limit_s": 140_000.0,
            "protected_closeout_reserve_s": 20_000.0,
            "input_token_limit": 3_000_000,
            "uncached_input_token_limit": 400_000,
            "output_token_limit": 30_000,
            "provider_wall_time_limit_s": 6_000.0,
            "currency_ceiling_usd": 20.0,
            "max_recovered_mcp_tool_failures": 64,
            "max_consecutive_mcp_tool_failures": 32,
        },
    }
    card["card_sha256"] = canonical_json_sha256(card)
    return card


def _calibration_summary(card: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": local_gate.SELECTED_CARD_RECEIPT_VERSION,
        "status": "selected_card_passed",
        "selected_resource_card": card,
        "selected_resource_card_sha256": card["card_sha256"],
        "selected_pattern_summary": {"triplet_passed": True},
        "whole_w2_26_status": "invalidated_platform_defect",
        "whole_w2_26_calibration_passed": False,
    }


def _write_runtime_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, dict[str, object]]:
    source = _source_config()
    card = _w2_27_card(source)
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(_calibration_summary(card)), encoding="utf-8")
    monkeypatch.setattr(
        local_gate,
        "validate_w2_27_selected_resource_card_receipt",
        lambda *_args: [],
    )
    runtime_config = local_gate.build_w2_27_runtime_config(ROOT, DESIGN, summary_path)
    runtime_path = ROOT / f".pytest-w2-27-runtime-{tmp_path.name}.json"
    runtime_path.write_text(json.dumps(runtime_config), encoding="utf-8")
    return runtime_path, runtime_config


def test_w2_27_entrypoints_do_not_rebuild_formal_or_c2_preflight() -> None:
    for path in ENTRYPOINTS:
        source = path.read_text(encoding="utf-8")
        assert "build_formal_preflight" not in source
        assert "validate_formal_bindings" not in source
        assert "work_ii_analysis_plan" not in source


@pytest.mark.parametrize("path", ENTRYPOINTS)
def test_w2_27_entrypoints_run_directly(path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(path), "--help"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_local_manifest_keeps_only_w2_27_execution_semantics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_path, _runtime = _write_runtime_config(tmp_path, monkeypatch)
    try:
        manifest = local_gate.build_method_qualification_local_manifest(
            ROOT, DESIGN, runtime_path
        )
        assert (
            local_gate.validate_method_qualification_local_manifest(ROOT, manifest)
            == []
        )
    finally:
        runtime_path.unlink(missing_ok=True)

    assert manifest["status"] == "passed"
    assert manifest["expected_counts"] == {
        "participant_cells": 3,
        "provider_sessions": 3,
        "provider_attempts_initial_planned": 3,
        "provider_attempts_hard_cap": 6,
        "complete_experiments": 24,
        "belief_checkpoints": 15,
    }
    assert "analysis_binding" not in manifest
    assert "c2_admission" not in manifest
    assert "cells" not in manifest
    assert "prerequisite_errors" not in manifest
    assert "blocking_requirements" not in manifest
    assert "design_binding" not in manifest
    assert "blind_evaluator_contract" not in manifest
    assert "held_out_evaluator_contract" not in manifest
    assert manifest["resource_calibration_card_binding"]["card_identity"] == {
        **local_gate.W2_27_RESOURCE_CARD_IDENTITY,
        "calibration_campaign_binding": manifest["resource_calibration_card_binding"][
            "card_identity"
        ]["calibration_campaign_binding"],
        "resource_formula_binding": manifest["resource_calibration_card_binding"][
            "card_identity"
        ]["resource_formula_binding"],
    }


def test_local_readiness_accepts_exact_selected_w2_26_card(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_path, _runtime = _write_runtime_config(tmp_path, monkeypatch)
    manifest = local_gate.build_method_qualification_local_manifest(
        ROOT, DESIGN, runtime_path
    )
    receipt_path = ROOT / f".pytest-w2-27-selected-{tmp_path.name}.json"
    receipt_path.write_text(
        json.dumps(_calibration_summary(_w2_27_card(_source_config()))),
        encoding="utf-8",
    )
    try:
        readiness = local_gate.build_method_qualification_local_readiness(
            ROOT,
            manifest,
            resource_calibration_manifest_path=(
                ROOT / "workstreams/flagship_tasks/reports/manifest.json"
            ),
            resource_calibration_summary_path=receipt_path,
        )
    finally:
        runtime_path.unlink(missing_ok=True)
        receipt_path.unlink(missing_ok=True)
    assert readiness["status"] == "passed_provider_execution_blocked"
    assert readiness["internal_errors"] == []
    assert readiness["resource_calibration_readiness"][
        "method_qualification_may_be_authorized"
    ] is True
    assert local_gate.validate_method_qualification_local_readiness(readiness) == []


def test_local_manifest_rejects_qualification_contract_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_path, _runtime = _write_runtime_config(tmp_path, monkeypatch)
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    design["method_qualification_contract"]["qualification_cell_count"] = 4
    design_path = ROOT / f".pytest-w2-27-design-{tmp_path.name}.json"
    try:
        design_path.write_text(json.dumps(design), encoding="utf-8")
        manifest = local_gate.build_method_qualification_local_manifest(
            ROOT, design_path, runtime_path
        )
    finally:
        design_path.unlink(missing_ok=True)
        runtime_path.unlink(missing_ok=True)

    assert manifest["status"] == "failed"
    assert "W2-27 qualification contract drifted" in manifest["errors"]


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("world_split", "qualification"),
        ("objective", "yield_only"),
        ("electrochemical_material_family_id", "different-family"),
        ("electrochemical_workflow_mode", "different-workflow"),
        ("scoring_contract_id", "different-scoring"),
        ("observation_noise_mode", "none"),
        ("observation_noise_namespace", "different-noise"),
    ),
)
def test_local_manifest_rejects_data_generation_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
) -> None:
    runtime_path, _runtime = _write_runtime_config(tmp_path, monkeypatch)
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    runtime[field] = value
    runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
    try:
        manifest = local_gate.build_method_qualification_local_manifest(
            ROOT, DESIGN, runtime_path
        )
    finally:
        runtime_path.unlink(missing_ok=True)

    assert manifest["status"] == "failed"
    assert "W2-27 data-generation contract drifted" in manifest["errors"]


@pytest.mark.parametrize(
    ("arm", "field", "value"),
    (
        ("opaque", "mode", "anonymous_nominal_properties"),
        ("aligned_nominal", "mode", "opaque_codes"),
        ("misindexed_nominal", "descriptor_permutation", [0, 1, 2, 3]),
    ),
)
def test_local_manifest_rejects_prior_arm_payload_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    arm: str,
    field: str,
    value: object,
) -> None:
    runtime_path, _runtime = _write_runtime_config(tmp_path, monkeypatch)
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    runtime["prior_arms"][arm][field] = value
    runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
    try:
        manifest = local_gate.build_method_qualification_local_manifest(
            ROOT, DESIGN, runtime_path
        )
    finally:
        runtime_path.unlink(missing_ok=True)

    assert manifest["status"] == "failed"
    assert "W2-27 participant-visible prior-arm payload drifted" in manifest["errors"]


def test_runtime_config_materializes_only_the_exact_ae_card(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source_config()
    card = _w2_27_card(source)
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(_calibration_summary(card)), encoding="utf-8")
    monkeypatch.setattr(
        local_gate,
        "validate_w2_27_selected_resource_card_receipt",
        lambda *_args: [],
    )

    runtime = local_gate.build_w2_27_runtime_config(ROOT, DESIGN, summary_path)

    assert runtime["campaign"]["operation_attempt_limit"] == 72
    assert runtime["method_resources"]["input_token_limit"] == 3_000_000
    assert runtime["provider"]["session_wall_time_limit_s"] == 6_000.0
    assert runtime["resource_calibration_card_binding"]["card_sha256"] == card[
        "card_sha256"
    ]
    assert source["campaign"]["operation_attempt_limit"] == 56


def test_runtime_config_rejects_wrong_locus_card(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source_config()
    card = _w2_27_card(source)
    card["card_identity"]["locus"] = "A_P"
    card["card_identity"]["rounds"] = 10
    card["card_sha256"] = canonical_json_sha256(
        {key: value for key, value in card.items() if key != "card_sha256"}
    )
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(_calibration_summary(card)), encoding="utf-8")
    monkeypatch.setattr(
        local_gate,
        "validate_w2_27_selected_resource_card_receipt",
        lambda *_args: [],
    )

    with pytest.raises(ValueError, match="exactly one task resource card"):
        local_gate.build_w2_27_runtime_config(ROOT, DESIGN, summary_path)


def test_runtime_config_rejects_wrong_world_seed_card(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source_config()
    card = _w2_27_card(source)
    card["card_identity"]["world_seed"] = 1
    card["card_sha256"] = canonical_json_sha256(
        {key: value for key, value in card.items() if key != "card_sha256"}
    )
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(_calibration_summary(card)), encoding="utf-8")
    monkeypatch.setattr(
        local_gate,
        "validate_w2_27_selected_resource_card_receipt",
        lambda *_args: [],
    )

    with pytest.raises(ValueError, match="different qualification world seed"):
        local_gate.build_w2_27_runtime_config(ROOT, DESIGN, summary_path)


def test_local_design_slice_ignores_unrelated_release_contracts() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    baseline = local_gate._design_slice(design)
    design["blind_evaluator_contract"] = {"unrelated_release_change": True}
    design["held_out_evaluator_contract"] = {"unrelated_release_change": True}
    design["formal_execution_allowed"] = not design["formal_execution_allowed"]

    assert local_gate._design_slice(design) == baseline
