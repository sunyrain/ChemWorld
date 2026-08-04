from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.render_work_i_figure_4 import (
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    load_figure_inputs,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, object]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_current_release_resolves_the_frozen_balanced_g0_data() -> None:
    inputs = load_figure_inputs(ROOT)
    assert inputs["release_path"].as_posix() == (
        "benchmark/releases/chemworld-serious-v1/manifest.json"
    )
    assert inputs["derived"]["status"] == "frozen_complete"
    assert len(inputs["arm_profiles"]) == 6
    assert len(inputs["contrasts"]) == 2
    assert len(inputs["world_arm_rows"]) == 60
    assert {
        (row["task_id"], row["arm"], row["world_seed"]) for row in inputs["world_arm_rows"]
    } == {
        (task, arm, seed)
        for task in ("electrochemical-conversion", "reaction-to-crystallization")
        for arm in ("opaque", "nominal", "misindexed")
        for seed in range(10)
    }


def test_outcome_prediction_and_epistemic_readouts_are_exact() -> None:
    profiles = load_figure_inputs(ROOT)["arm_profiles"]
    electrochemical_nominal = profiles[("electrochemical-conversion", "nominal")]
    crystallization_opaque = profiles[("reaction-to-crystallization", "opaque")]
    assert electrochemical_nominal["primary_score_mean"] == pytest.approx(0.7873706578076737)
    assert electrochemical_nominal["heldout_directional_accuracy"] == pytest.approx(
        0.7777777777777778
    )
    assert electrochemical_nominal["heldout_brier_score"] == pytest.approx(0.14907777777777778)
    assert crystallization_opaque["declared_directional_accuracy"] == pytest.approx(0.85)
    assert crystallization_opaque["mechanism_tag_f1"] == pytest.approx(0.14440798967114757)
    assert crystallization_opaque["structural_edge_f1"] == pytest.approx(0.27549449604403164)
    assert crystallization_opaque["unsupported_claim_rate"] == pytest.approx(0.7135714285714286)


def test_component_gates_remain_non_composite() -> None:
    inputs = load_figure_inputs(ROOT)
    contrasts = inputs["contrasts"]
    assert contrasts["electrochemical-conversion"]["manipulation_check_passed"] is True
    assert contrasts["electrochemical-conversion"]["differential_action_correction_passed"] is True
    assert contrasts["electrochemical-conversion"]["performance_recovery_to_opaque_passed"] is False
    assert contrasts["reaction-to-crystallization"]["manipulation_check_passed"] is True
    assert (
        contrasts["reaction-to-crystallization"]["differential_action_correction_passed"] is False
    )
    assert contrasts["reaction-to-crystallization"]["performance_recovery_to_opaque_passed"] is True
    assert all(row["overall_recovery_claim_passed"] is False for row in contrasts.values())


def test_manifest_binds_sources_outputs_and_claim_boundary() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["figure_id"] == "F4"
    assert manifest["owner_task"] == "W1-P05"
    assert manifest["evidence_census"] == {
        "compiled_tasks": 2,
        "worlds_per_task": 10,
        "information_arms": 3,
        "participant_world_arm_cells": 60,
        "participant_physical_experiments": 2280,
        "outcome_readouts": 6,
        "heldout_prediction_readouts": 6,
        "heldout_calibration_readouts": 6,
        "opaque_epistemic_profiles": 2,
        "component_gate_profiles": 2,
        "registered_scalar_composite": False,
    }
    assert manifest["claim_boundary"]["llm_vs_optimizer_competition"] is False
    assert manifest["claim_boundary"]["scalar_experimental_intelligence"] is False
    assert manifest["source_integrity"]["g0_v1_0_declared_file_bytes_match"] is True
    assert manifest["source_integrity"]["g0_v1_2_canonical_json_matches"] is True
    assert manifest["source_integrity"]["g0_v1_2_declared_file_bytes_match"] is True
    assert len(manifest["source_bindings"]) == 8
    for binding in manifest["source_bindings"]:
        assert _sha256(ROOT / binding["path"]) == binding["sha256"]
    outputs = manifest["outputs"]
    assert [row["format"] for row in outputs] == ["svg", "pdf", "png"]
    for row in outputs:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert _sha256(path) == row["sha256"]

    output_dir = ROOT / OUTPUT_DIR
    svg = (output_dir / f"{OUTPUT_STEM}.svg").read_text(encoding="utf-8")
    pdf = (output_dir / f"{OUTPUT_STEM}.pdf").read_bytes()
    png = (output_dir / f"{OUTPUT_STEM}.png").read_bytes()
    assert "<text" in svg
    assert "Compiled controls separate outcome" not in svg
    assert pdf.startswith(b"%PDF") and b"/FontFile2" in pdf
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560

    tampered = deepcopy(manifest)
    tampered["evidence_census"]["registered_scalar_composite"] = True
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
