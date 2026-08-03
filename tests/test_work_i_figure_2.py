from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.render_work_i_figure_2 import (
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    POLICY_ORDER,
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


def test_inputs_are_the_frozen_balanced_known_policy_census() -> None:
    inputs = load_figure_inputs(ROOT)
    report = inputs["report"]
    assert report["status"] == "positive_control_established"
    assert report["estimand"] == {
        "lifecycle_rows_pooled_before_profile_construction": False,
        "primary_campaigns": 30,
        "primary_closed_lifecycles": 180,
        "provider_calls": 0,
        "retest_campaigns": 30,
        "retest_closed_lifecycles": 180,
        "retest_in_primary_estimand": False,
        "unit": "one primary campaign profile",
        "weighting": "equal weight across ten world-arm campaigns per policy",
    }
    assert inputs["profile_policy_counts"] == dict.fromkeys(POLICY_ORDER, 10)
    assert inputs["profile_arm_counts"] == {
        "opaque_codes": 15,
        "anonymous_nominal_properties": 15,
    }


def test_profile_recovery_matches_the_prespecified_policy_signatures() -> None:
    summaries = load_figure_inputs(ROOT)["summaries"]
    assert summaries["assay_all"]["assay_fraction"] == 1.0
    assert summaries["assay_all"]["discard_fraction"] == 0.0
    assert summaries["start_then_discard"]["assay_fraction"] == 0.0
    assert summaries["start_then_discard"]["discard_fraction"] == 1.0
    threshold = summaries["measure_then_threshold"]
    assert threshold["assay_fraction"] == pytest.approx(28 / 60)
    assert threshold["discard_fraction"] == pytest.approx(32 / 60)
    assert threshold["measured_lifecycle_fraction"] == 1.0
    assert threshold["continued_after_measurement_fraction"] == pytest.approx(28 / 60)
    assert threshold["nonfinal_instrument_uses_per_closed_lifecycle"] == 1.0
    assert threshold["attempted_operations_per_closed_lifecycle"] == pytest.approx(
        6.933333333333333
    )


def test_manifest_is_self_hashed_and_binds_all_sources_and_outputs() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["figure_id"] == "F2"
    assert manifest["owner_task"] == "W1-P03"
    assert manifest["figure_system_sha256"] == (
        "c7abb490d247121e47fe20efca909df28527de64e7d1110699ccd104f6873643"
    )
    assert len(manifest["source_bindings"]) == 7
    for binding in manifest["source_bindings"]:
        assert _sha256(ROOT / binding["path"]) == binding["sha256"]
    outputs = manifest["outputs"]
    assert [row["format"] for row in outputs] == ["svg", "pdf", "png"]
    for row in outputs:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert _sha256(path) == row["sha256"]


def test_outputs_and_claim_boundary_keep_retests_separate() -> None:
    manifest = _manifest()
    assert manifest["evidence_census"] == {
        "worlds": 5,
        "information_arms": 2,
        "known_policies": 3,
        "primary_campaigns": 30,
        "primary_closed_lifecycles": 180,
        "retest_campaigns": 30,
        "retest_closed_lifecycles": 180,
        "retest_in_primary_estimand": False,
        "provider_calls": 0,
        "all_30_retest_pairs_match": True,
    }
    assert manifest["claim_boundary"] == {
        "bounded_construct_and_discriminant_validity": True,
        "deterministic_reliability_positive_control": True,
        "model_or_provider_capability": False,
        "endpoint_performance_ranking": False,
        "causal_material_information_effect": False,
        "scalar_experimental_intelligence": False,
        "real_laboratory_generalization": False,
    }
    output_dir = ROOT / OUTPUT_DIR
    svg = (output_dir / f"{OUTPUT_STEM}.svg").read_text(encoding="utf-8")
    pdf = (output_dir / f"{OUTPUT_STEM}.pdf").read_bytes()
    png = (output_dir / f"{OUTPUT_STEM}.png").read_bytes()
    assert "<text" in svg
    assert "Known policies validate the experimental-agency profile" not in svg
    assert pdf.startswith(b"%PDF") and b"/FontFile2" in pdf
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560

    tampered = deepcopy(manifest)
    tampered["evidence_census"]["retest_in_primary_estimand"] = True
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
