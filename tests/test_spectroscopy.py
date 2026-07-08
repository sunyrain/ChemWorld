from __future__ import annotations

import pytest

from chemworld.physchem import (
    BeerLambertBandSpec,
    beer_lambert_absorbance,
    build_signal_spec_from_card,
    chromatographic_baseline_peak_width,
    chromatographic_resolution,
    chromatographic_retention_factor,
    chromatographic_retention_time,
    chromatographic_theoretical_plates,
    fit_beer_lambert_calibration,
    fit_chromatography_calibration,
    generate_beer_lambert_calibration,
    get_mechanism_card,
    load_library_mechanism,
    spectroscopy_model_cards,
    synthesize_signal,
    synthesize_signal_from_card,
    validate_model_card,
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
    assert packet["metadata"]["calibration_profile"] == "hplc_retention_plate_calibration_v1"
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


def test_chromatography_retention_equations_are_consistent() -> None:
    retention_time = chromatographic_retention_time(
        dead_time_min=0.50,
        retention_factor=3.0,
    )
    width = chromatographic_baseline_peak_width(
        retention_time_min=retention_time,
        theoretical_plates=6400.0,
    )
    plates = chromatographic_theoretical_plates(
        retention_time_min=retention_time,
        baseline_width_min=width,
    )
    resolution = chromatographic_resolution(1.5, 2.1, 0.12, 0.18)

    assert retention_time == pytest.approx(2.0)
    assert chromatographic_retention_factor(
        retention_time_min=retention_time,
        dead_time_min=0.50,
    ) == pytest.approx(3.0)
    assert width == pytest.approx(0.10)
    assert plates == pytest.approx(6400.0)
    assert resolution == pytest.approx(4.0)


def test_chromatography_calibration_recovers_retention_factor_and_plate_count() -> None:
    retention_time = chromatographic_retention_time(
        dead_time_min=0.40,
        retention_factor=2.5,
    )
    width = chromatographic_baseline_peak_width(
        retention_time_min=retention_time,
        theoretical_plates=4900.0,
    )
    result = fit_chromatography_calibration(
        (retention_time, retention_time),
        (width, width),
        species_id="P",
        instrument_id="hplc",
        dead_time_min=0.40,
    )

    assert result.retention_factor_mean == pytest.approx(2.5)
    assert result.retention_factor_std == pytest.approx(0.0)
    assert result.theoretical_plates_mean == pytest.approx(4900.0)
    assert result.theoretical_plates_std == pytest.approx(0.0)


def test_hplc_gc_signals_use_chromatography_retention_metadata() -> None:
    card = get_mechanism_card("simple_batch_reaction")
    network = load_library_mechanism(card)
    hplc = synthesize_signal_from_card(
        "hplc",
        card,
        network,
        {"A": 0.25, "P": 0.35, "B": 0.08, "D": 0.02, "E": 0.0},
        volume_L=1.0,
        seed=8,
    ).to_dict()
    gc = synthesize_signal_from_card(
        "gc",
        card,
        network,
        {"A": 0.25, "P": 0.35, "B": 0.08, "D": 0.02, "E": 0.0},
        volume_L=1.0,
        seed=8,
    ).to_dict()
    hplc_product = _peak(hplc, "P")
    gc_product = _peak(gc, "P")

    assert "chromatography_retention_plate" in hplc["metadata"]["model_ids"]
    assert hplc["metadata"]["calibration_profile"] == "hplc_retention_plate_calibration_v1"
    assert gc["metadata"]["calibration_profile"] == "gc_retention_plate_calibration_v1"
    assert hplc["metadata"]["chromatographic_resolution"]["minimum_adjacent_resolution"] > 0.0
    assert hplc_product["metadata"]["model_id"] == "chromatography_retention_plate"
    assert hplc_product["metadata"]["retention_factor"] > 0.0
    assert hplc_product["metadata"]["baseline_width_min"] > 0.0
    assert gc_product["metadata"]["model_id"] == "chromatography_retention_plate"


def test_beer_lambert_absorbance_scales_with_concentration_and_path() -> None:
    single = beer_lambert_absorbance(
        2.0e-4,
        molar_absorptivity_L_mol_cm=12_000.0,
        path_length_cm=1.0,
        blank_absorbance=0.015,
    )
    doubled = beer_lambert_absorbance(
        4.0e-4,
        molar_absorptivity_L_mol_cm=12_000.0,
        path_length_cm=1.0,
        blank_absorbance=0.015,
    )
    longer_path = beer_lambert_absorbance(
        2.0e-4,
        molar_absorptivity_L_mol_cm=12_000.0,
        path_length_cm=2.0,
        blank_absorbance=0.015,
    )

    assert single == pytest.approx(2.415)
    assert doubled - 0.015 == pytest.approx(2.0 * (single - 0.015))
    assert longer_path - 0.015 == pytest.approx(2.0 * (single - 0.015))


def test_beer_lambert_calibration_recovers_noiseless_molar_absorptivity() -> None:
    band = BeerLambertBandSpec(
        species_id="Dye",
        wavelength_nm=512.0,
        molar_absorptivity_L_mol_cm=8500.0,
        path_length_cm=1.0,
        dilution_factor=100.0,
        blank_absorbance=0.010,
    )
    standards = (0.0, 0.01, 0.02, 0.04)
    result = generate_beer_lambert_calibration(
        band,
        standards,
        noise_absorbance=0.0,
    )

    assert result.fitted_slope_absorbance_per_mol_L == pytest.approx(85.0)
    assert result.intercept_absorbance == pytest.approx(0.010)
    assert result.molar_absorptivity_L_mol_cm == pytest.approx(8500.0)
    assert result.dilution_factor == pytest.approx(100.0)
    assert result.r_squared == pytest.approx(1.0)
    assert result.detection_limit_mol_L == 0.0


def test_fit_beer_lambert_calibration_reports_residual_uncertainty() -> None:
    result = fit_beer_lambert_calibration(
        (0.0, 0.1, 0.2, 0.3),
        (0.012, 0.095, 0.182, 0.267),
        species_id="P",
        path_length_cm=1.0,
    )

    assert result.fitted_slope_absorbance_per_mol_L > 0.8
    assert result.r_squared > 0.999
    assert result.detection_limit_mol_L > 0.0
    assert result.quantitation_limit_mol_L > result.detection_limit_mol_L


def test_uvvis_signal_uses_beer_lambert_band_metadata() -> None:
    card = get_mechanism_card("simple_batch_reaction")
    network = load_library_mechanism(card)
    measurement = synthesize_signal_from_card(
        "uvvis",
        card,
        network,
        {"A": 0.2, "P": 0.30, "B": 0.04, "D": 0.0, "E": 0.0},
        volume_L=1.0,
        seed=7,
        replicate_count=3,
    )
    packet = measurement.to_dict()
    product_peak = _peak(packet, "P")
    metadata = product_peak["metadata"]

    assert packet["metadata"]["calibration_profile"] == "uvvis_beer_lambert_calibration_v1"
    assert "beer_lambert_uvvis" in packet["metadata"]["model_ids"]
    assert metadata["model_id"] == "beer_lambert_uvvis"
    assert metadata["path_length_cm"] == pytest.approx(1.0)
    assert metadata["dilution_factor"] == pytest.approx(1000.0)
    assert product_peak["estimated_concentration_mol_L"] == pytest.approx(0.30)


def test_spectroscopy_model_card_documents_beer_lambert_uvvis() -> None:
    cards = spectroscopy_model_cards()
    card = next(card for card in cards if card.model_id == "beer_lambert_uvvis")

    assert card.maturity.value == "reference_validated"
    assert not validate_model_card(card)
    assert any("Beer-Lambert" in equation for equation in card.equations)


def test_spectroscopy_model_card_documents_chromatography_retention() -> None:
    cards = spectroscopy_model_cards()
    card = next(card for card in cards if card.model_id == "chromatography_retention_plate")

    assert card.maturity.value == "reference_validated"
    assert not validate_model_card(card)
    assert any("retention factor" in equation for equation in card.equations)


def _peak(packet: dict[str, object], species_id: str) -> dict[str, object]:
    for peak in packet["peaks"]:
        if isinstance(peak, dict) and peak["species_id"] == species_id:
            return peak
    raise AssertionError(f"Missing peak for {species_id}")


def _peak_area(packet: dict[str, object], species_id: str) -> float:
    return float(_peak(packet, species_id)["area"])
