from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.render_work_i_figure_3 import (
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    load_figure_inputs,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, Any]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_inputs_reproduce_the_complete_system_terminal_census() -> None:
    inputs = load_figure_inputs(ROOT)
    codex = inputs["codex"]
    deepseek = inputs["deepseek"]
    assert (
        codex["closed_batch_count"],
        codex["final_assay_count"],
        codex["discarded_batch_count"],
    ) == (
        60,
        60,
        0,
    )
    assert (
        deepseek["closed_batch_count"],
        deepseek["final_assay_count"],
        deepseek["discarded_batch_count"],
    ) == (60, 24, 36)
    assert 60 + 60 == 120
    assert 60 + 24 == 84


def test_world_by_arm_profiles_reproduce_24_assays_and_36_discards() -> None:
    profiles = load_figure_inputs(ROOT)["cell_profiles"]
    assert len(profiles) == 10
    assert set(profiles) == {
        (seed, arm) for seed in range(5) for arm in ("opaque_codes", "anonymous_nominal_properties")
    }
    assert all(
        row["observed_assay_count"] + row["observed_discard_count"] == 6
        for row in profiles.values()
    )
    assert sum(row["observed_assay_count"] for row in profiles.values()) == 24
    assert sum(row["observed_discard_count"] for row in profiles.values()) == 36
    assert profiles[(0, "anonymous_nominal_properties")]["cell_id"] == "cell-02"
    assert profiles[(0, "anonymous_nominal_properties")]["observed_discard_count"] == 0


def test_latent_gate_failure_is_rendered_without_complete_case_substitution() -> None:
    inputs = load_figure_inputs(ROOT)
    analysis = inputs["latent_analysis"]
    assert analysis["entry_gate"]["main_text_eligible"] is False
    assert analysis["census"]["resolved_shadow_receipts"] == 6
    assert analysis["census"]["unresolved_shadow_receipts"] == 30
    assert analysis["missingness_and_censoring"]["complete_case_primary_used"] is False
    bounds = inputs["latent_bounds"]
    assert [row["estimand"] for row in bounds] == [
        "latent score mean",
        "discard - observed best",
        "false-discard fraction",
        "campaign-oracle regret",
    ]
    assert bounds[0]["lower"] == 8.586298305923063e-05
    assert bounds[0]["upper"] == 0.8334191963163926


def test_manifest_closes_the_registered_result_slots_with_bounds() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["status"] == "frozen_latent_gate_failure_display"
    assert manifest["pending_result_panels"] == []
    assert manifest["evidence_census"] == {
        "distinct_complete_systems": 2,
        "matched_worlds": 5,
        "information_arms": 2,
        "matched_world_by_arm_cells": 10,
        "closed_lifecycles": 120,
        "final_assays": 84,
        "explicit_discards": 36,
        "complete_system_a": {"closed": 60, "assays": 60, "discards": 0},
        "complete_system_b": {"closed": 60, "assays": 24, "discards": 36},
        "registered_latent_discard_units": 36,
        "resolved_shadow_receipts": 6,
        "unresolved_shadow_receipts": 30,
        "campaign_oracle_opportunity_cells": 9,
        "structural_null_cells": ["cell-02"],
    }
    boundary = manifest["claim_boundary"]
    assert boundary["discard_quality_point_estimate_reported"] is False
    assert boundary["failed_latent_gate_reported"] is True
    assert boundary["isolated_model_backend_effect"] is False
    assert boundary["leaderboard_comparison"] is False
    result = manifest["latent_result_summary"]
    assert result["main_text_eligible"] is False
    assert result["point_estimates_withheld"] is True
    assert result["resolved_shadow_receipts"] == 6
    assert result["unresolved_shadow_receipts"] == 30
    tampered = deepcopy(manifest)
    tampered["latent_result_summary"]["resolved_shadow_receipts"] = 36
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)


def test_manifest_binds_sources_and_publication_outputs() -> None:
    manifest = _manifest()
    assert manifest["figure_id"] == "F3"
    assert manifest["owner_task"] == "W1-P09"
    assert manifest["original_owner_task"] == "W1-P04"
    assert manifest["figure_system_sha256"] == (
        "c7abb490d247121e47fe20efca909df28527de64e7d1110699ccd104f6873643"
    )
    assert len(manifest["source_bindings"]) == 9
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
    assert "Lifecycle completion does not specify terminal policy" not in svg
    assert "cell-02" not in svg
    assert "one cell is structurally undefined" in svg
    assert pdf.startswith(b"%PDF") and b"/FontFile2" in pdf
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560
