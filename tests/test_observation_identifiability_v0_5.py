from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.observation_identifiability import (
    ObservationIdentifiabilityError,
    PublicSpectrumArchive,
    apply_spectrum_condition,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = (
    ROOT
    / "workstreams"
    / "world_foundation"
    / "reports"
    / "observation-identifiability-v0.5.json"
)


def test_instrument_sensitivity_degradation_and_public_boundary() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert set(report["instruments"]) == {"hplc", "gc", "uvvis", "ir", "nmr"}
    for item in report["instruments"].values():
        assert item["identifiability"]["identifiable"] is item["expected_identifiable"]
        assert item["degraded_low_signal"]["identifiable"] is False
        assert item["degraded_low_signal"]["warnings"]
        assert 0.0 <= item["replicate_probe_accuracy"] <= 1.0
    assert report["ph_meter"]["state_pair_distinguishable"] is True
    assert report["ph_meter"]["low_contrast_degraded"] is True
    assert report["leakage_matches"] == []


def test_spectrum_conditions_preserve_pairing_and_raw_curve() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    conditions = report["spectrum_conditions"]
    assert set(conditions["condition_sha256"]) == {"assigned", "unassigned", "masked"}
    assert conditions["raw_curve_sha256"]["assigned"] == conditions[
        "raw_curve_sha256"
    ]["unassigned"]
    assert len(set(conditions["non_spectral_context_sha256"].values())) == 1


def test_condition_transform_rejects_unknown_and_removes_assignments() -> None:
    packet = {
        "kind": "test",
        "time_min": [0.0, 1.0],
        "intensity": [0.1, 0.9],
        "peaks": [{"assignment": "target_public", "species_id": "target_public"}],
        "assignments": [{"species_id": "target_public"}],
        "processed_estimates": {"target": 0.5},
    }
    unassigned = apply_spectrum_condition(packet, "unassigned")
    assert unassigned["assignments"] == []
    assert unassigned["peaks"][0]["assignment"] == "unassigned"
    assert "species_id" not in unassigned["peaks"][0]
    assert "processed_estimates" not in unassigned
    masked = apply_spectrum_condition(packet, "masked")
    assert masked["available"] is False
    assert "intensity" not in masked
    with pytest.raises(ObservationIdentifiabilityError, match="unknown spectrum condition"):
        apply_spectrum_condition(packet, "oracle")


def test_history_archive_is_catalog_only_until_explicit_request() -> None:
    archive = PublicSpectrumArchive(retrieval_cost=0.0)
    packet = {"kind": "hplc", "instrument_id": "hplc", "intensity": [0.1, 0.2]}
    archive.record(
        "s1",
        packet,
        experiment_index=1,
        measurement_step=4,
        measurement_cost=0.08,
    )
    assert "intensity" not in json.dumps(archive.catalog())
    assert archive.retrieve("s1") == packet
    with pytest.raises(ObservationIdentifiabilityError, match="unknown spectrum id"):
        archive.retrieve("missing")
    assert archive.ledger() == [
        {
            "event": "historical_spectrum_retrieval",
            "spectrum_id": "s1",
            "success": True,
            "cost": 0.0,
        },
        {
            "event": "historical_spectrum_retrieval",
            "spectrum_id": "missing",
            "success": False,
            "cost": 0.0,
        },
    ]
