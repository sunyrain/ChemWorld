from __future__ import annotations

import pytest

from chemworld.physchem import (
    MaturityLevel,
    ProtonNMRMethodSpec,
    ProtonNMRSignalSpec,
    simulate_proton_nmr,
    spectroscopy_model_cards,
    validate_model_card,
)


def _method(*, observed_reference_ppm: float = 0.0) -> ProtonNMRMethodSpec:
    return ProtonNMRMethodSpec(
        method_id="400MHz_cdcl3",
        spectrometer_frequency_MHz=400.0,
        solvent_id="CDCl3",
        solvent_residual_peaks_ppm=(7.26,),
        reference_id="TMS",
        expected_reference_ppm=0.0,
        observed_reference_ppm=observed_reference_ppm,
        solvent_interference_tolerance_ppm=0.03,
    )


def test_triplet_splitting_positions_and_pascal_intensities() -> None:
    signal = ProtonNMRSignalSpec(
        species_id="ethanol",
        signal_id="ethanol_ch3",
        chemical_shift_ppm=1.20,
        proton_count=3,
        multiplicity="t",
        coupling_constants_Hz=(7.0,),
        line_width_Hz=1.0,
        assignment="CH3 coupled to CH2",
        provenance_id="ethanol-anchor",
    )
    report = simulate_proton_nmr(
        (signal,),
        species_amounts_mol={"ethanol": 0.1},
        method=_method(),
    )
    lines = report.signals[0].lines

    assert [line.relative_intensity for line in lines] == pytest.approx([0.25, 0.5, 0.25])
    assert [line.chemical_shift_ppm for line in lines] == pytest.approx(
        [1.20 - 7.0 / 400.0, 1.20, 1.20 + 7.0 / 400.0]
    )


def test_integrals_follow_species_amount_proton_count_and_response() -> None:
    signals = (
        ProtonNMRSignalSpec(
            species_id="A",
            signal_id="A_methyl",
            chemical_shift_ppm=1.0,
            proton_count=3,
            multiplicity="s",
            coupling_constants_Hz=(),
            line_width_Hz=1.0,
            assignment="methyl",
            provenance_id="A-anchor",
        ),
        ProtonNMRSignalSpec(
            species_id="B",
            signal_id="B_methylene",
            chemical_shift_ppm=3.0,
            proton_count=2,
            multiplicity="s",
            coupling_constants_Hz=(),
            line_width_Hz=1.0,
            assignment="methylene",
            provenance_id="B-anchor",
        ),
    )
    report = simulate_proton_nmr(
        signals,
        species_amounts_mol={"A": 0.2, "B": 0.1},
        method=_method(),
    )

    assert report.total_integral == pytest.approx(0.8)
    assert report.signals[0].raw_integral == pytest.approx(0.6)
    assert report.signals[0].normalized_integral == pytest.approx(0.75)
    assert report.signals[1].normalized_integral == pytest.approx(0.25)


def test_reference_correction_and_solvent_residual_interference() -> None:
    signal = ProtonNMRSignalSpec(
        species_id="aromatic",
        signal_id="aromatic_h",
        chemical_shift_ppm=7.28,
        proton_count=1,
        multiplicity="s",
        coupling_constants_Hz=(),
        line_width_Hz=1.0,
        assignment="aromatic proton",
        provenance_id="aromatic-anchor",
    )
    report = simulate_proton_nmr(
        (signal,),
        species_amounts_mol={"aromatic": 1.0},
        method=_method(observed_reference_ppm=0.02),
    )
    result = report.signals[0]

    assert result.corrected_chemical_shift_ppm == pytest.approx(7.26)
    assert result.solvent_interference
    assert "solvent_residual_interference" in result.warnings


def test_close_coupled_signals_flag_overlap_and_second_order_risk() -> None:
    signals = (
        ProtonNMRSignalSpec(
            species_id="A",
            signal_id="A_d",
            chemical_shift_ppm=2.000,
            proton_count=1,
            multiplicity="d",
            coupling_constants_Hz=(8.0,),
            line_width_Hz=8.0,
            assignment="A proton",
            provenance_id="A-close-anchor",
        ),
        ProtonNMRSignalSpec(
            species_id="A",
            signal_id="B_d",
            chemical_shift_ppm=2.015,
            proton_count=1,
            multiplicity="d",
            coupling_constants_Hz=(8.0,),
            line_width_Hz=8.0,
            assignment="B proton",
            provenance_id="B-close-anchor",
        ),
    )
    report = simulate_proton_nmr(
        signals,
        species_amounts_mol={"A": 1.0},
        method=_method(),
    )

    assert report.signals[0].overlap_signal_ids == ("B_d",)
    assert report.signals[0].second_order_risk
    assert "signal_overlap" in report.warnings
    assert "second_order_splitting_risk" in report.warnings


def test_exchangeable_and_unresolved_multiplet_warnings_are_explicit() -> None:
    signal = ProtonNMRSignalSpec(
        species_id="alcohol",
        signal_id="oh",
        chemical_shift_ppm=2.5,
        proton_count=1,
        multiplicity="m",
        coupling_constants_Hz=(),
        line_width_Hz=12.0,
        assignment="exchangeable OH",
        provenance_id="oh-range-anchor",
        exchangeable=True,
    )
    result = simulate_proton_nmr(
        (signal,),
        species_amounts_mol={"alcohol": 1.0},
        method=_method(),
    ).signals[0]

    assert "exchangeable_proton_shift_and_width_variable" in result.warnings
    assert "unresolved_multiplet" in result.warnings


def test_multiplicity_contract_rejects_missing_coupling() -> None:
    with pytest.raises(ValueError, match="coupling count"):
        ProtonNMRSignalSpec(
            species_id="bad",
            signal_id="bad_doublet",
            chemical_shift_ppm=1.0,
            proton_count=1,
            multiplicity="d",
            coupling_constants_Hz=(),
            line_width_Hz=1.0,
            assignment="invalid",
            provenance_id="invalid",
        )


def test_proton_nmr_model_card_is_reference_validated() -> None:
    card = {
        item.model_id: item for item in spectroscopy_model_cards()
    }["first_order_proton_nmr_assignments_v1"]

    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
