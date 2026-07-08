from __future__ import annotations

import pytest

from chemworld.physchem import (
    build_signal_spec_from_card,
    get_mechanism_card,
    load_library_mechanism,
    synthesize_signal,
    synthesize_signal_from_card,
)
from chemworld.world.observation_kernel import raw_signal


def test_larger_product_amount_increases_hplc_product_peak_area() -> None:
    card = get_mechanism_card("simple_batch_reaction")
    network = load_library_mechanism(card)
    low = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        {"A": 0.8, "P": 0.05, "B": 0.02, "D": 0.0, "E": 0.0},
        volume_L=1.0,
        seed=1,
        replicate_count=2,
    )
    high = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        {"A": 0.4, "P": 0.35, "B": 0.02, "D": 0.0, "E": 0.0},
        volume_L=1.0,
        seed=1,
        replicate_count=2,
    )

    low_product = _peak_area(low.to_dict(), "P")
    high_product = _peak_area(high.to_dict(), "P")

    assert high_product > low_product
    assert high.to_dict()["replicate_count"] == 2


def test_byproducts_create_visible_impurity_peaks() -> None:
    card = get_mechanism_card("parallel_series_reaction")
    network = load_library_mechanism(card)
    measurement = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        {"A": 0.2, "P": 0.45, "S": 0.16, "D": 0.05, "E": 0.03},
        volume_L=1.0,
        seed=2,
    )
    peaks = measurement.to_dict()["peaks"]

    assert any(
        peak["detected"] and peak["group"] in {"byproduct", "degradation"}
        for peak in peaks
    )


def test_low_concentration_can_fall_below_detection_limit() -> None:
    card = get_mechanism_card("simple_batch_reaction")
    network = load_library_mechanism(card)
    measurement = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        {"A": 0.5, "P": 1.0e-6, "B": 0.0, "D": 0.0, "E": 0.0},
        volume_L=1.0,
        seed=3,
    )
    product_peak = _peak(measurement.to_dict(), "P")

    assert not product_peak["detected"]
    assert product_peak["area"] == 0.0


def test_processed_estimates_are_consistent_with_calibrated_raw_signal() -> None:
    card = get_mechanism_card("catalyst_deactivation")
    network = load_library_mechanism(card)
    amounts = {
        "A": 0.35,
        "P": 0.28,
        "B": 0.08,
        "D": 0.03,
        "Cat_active": 0.01,
        "Cat_dead": 0.005,
    }
    measurement = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        amounts,
        volume_L=1.0,
        seed=4,
        replicate_count=4,
    )
    packet = measurement.to_dict()

    estimate = packet["processed_estimates"]["P"]
    uncertainty = packet["uncertainty"]["P_std_mol_L"]
    assert estimate == pytest.approx(amounts["P"], abs=max(3.0 * uncertainty, 1.0e-8))
    assert packet["metadata"]["calibration_profile"] == "hplc_species_calibration_v1"
    assert packet["metadata"]["detection_limits_mol_L"]["P"] > 0.0


def test_peak_overlap_is_reported_for_close_features() -> None:
    card = get_mechanism_card("reaction_extraction")
    network = load_library_mechanism(card)
    spec = build_signal_spec_from_card("hplc", card, network)
    measurement = synthesize_signal(
        spec,
        {
            "A": 0.05,
            "P_aq": 0.20,
            "P_org": 0.25,
            "B_aq": 0.12,
            "B_org": 0.10,
            "D": 0.04,
            "E": 0.02,
        },
        volume_L=1.0,
        seed=5,
    )

    assert measurement.to_dict()["metadata"]["peak_overlap"]


def test_world_raw_signal_accepts_species_amounts_without_leaking_hidden_state() -> None:
    packet = raw_signal(
        "hplc",
        {"yield": 0.5, "conversion": 0.7, "byproduct_signal": 0.1},
        species_amounts_mol={"A": 0.25, "P": 0.45, "B": 0.08, "D": 0.02},
        volume_L=1.0,
        seed=6,
        replicate_count=2,
    )

    assert packet["kind"] == "hplc_chromatogram"
    assert packet["source"] == "species_amounts_with_calibration"
    assert "species_amounts" not in packet
    assert packet["replicate_count"] == 2
    assert "processed_estimates" in packet


def _peak(packet: dict[str, object], species_id: str) -> dict[str, object]:
    for peak in packet["peaks"]:
        if isinstance(peak, dict) and peak["species_id"] == species_id:
            return peak
    raise AssertionError(f"Missing peak for {species_id}")


def _peak_area(packet: dict[str, object], species_id: str) -> float:
    return float(_peak(packet, species_id)["area"])
