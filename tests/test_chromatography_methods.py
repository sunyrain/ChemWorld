from __future__ import annotations

from math import sqrt

import pytest

from chemworld.physchem import (
    EmpiricalChromatographyAnalyteSpec,
    MaturityLevel,
    evaluate_chromatography_method,
    fit_detector_response_calibration,
    gc_linear_retention_index,
    peak_shape_status,
    spectroscopy_model_cards,
    validate_model_card,
)


def _hplc_analyte(*, tailing_factor: float = 1.0) -> EmpiricalChromatographyAnalyteSpec:
    return EmpiricalChromatographyAnalyteSpec(
        analyte_id="caffeine_like",
        instrument_id="hplc",
        reference_retention_factor=4.0,
        reference_temperature_K=298.15,
        reference_mobile_phase_fraction=0.40,
        hplc_log10_k_mobile_phase_slope=3.0,
        hplc_log10_k_temperature_slope_per_K=-0.005,
        detector_response_slope=1200.0,
        detector_response_intercept=5.0,
        tailing_factor=tailing_factor,
        provenance_id="synthetic-hplc-method-card",
    )


def test_hplc_organic_fraction_and_temperature_reduce_retention() -> None:
    reference = evaluate_chromatography_method(
        _hplc_analyte(),
        dead_time_min=0.5,
        temperature_K=298.15,
        mobile_phase_fraction=0.40,
        detector_concentration=0.01,
    )
    stronger_hot = evaluate_chromatography_method(
        _hplc_analyte(),
        dead_time_min=0.5,
        temperature_K=308.15,
        mobile_phase_fraction=0.50,
        detector_concentration=0.01,
    )

    assert reference.retention_factor == pytest.approx(4.0)
    assert reference.retention_time_min == pytest.approx(2.5)
    assert stronger_hot.retention_factor < reference.retention_factor
    assert stronger_hot.retention_shift_min < 0.0
    assert reference.detector_response == pytest.approx(17.0)


def test_gc_vanthoff_temperature_sensitivity_reduces_retention_when_heated() -> None:
    analyte = EmpiricalChromatographyAnalyteSpec(
        analyte_id="alkane_like",
        instrument_id="gc",
        reference_retention_factor=8.0,
        reference_temperature_K=350.0,
        reference_mobile_phase_fraction=None,
        gc_retention_enthalpy_J_mol=-30_000.0,
        provenance_id="synthetic-gc-method-card",
    )
    reference = evaluate_chromatography_method(
        analyte,
        dead_time_min=0.4,
        temperature_K=350.0,
        detector_concentration=1.0,
    )
    hot = evaluate_chromatography_method(
        analyte,
        dead_time_min=0.4,
        temperature_K=380.0,
        detector_concentration=1.0,
    )

    assert reference.retention_factor == pytest.approx(8.0)
    assert hot.retention_factor < reference.retention_factor
    assert hot.retention_time_min < reference.retention_time_min


def test_gc_retention_index_uses_log_adjusted_time_interpolation() -> None:
    dead_time = 1.0
    lower_adjusted = 2.0
    upper_adjusted = 8.0
    unknown_adjusted = sqrt(lower_adjusted * upper_adjusted)
    index = gc_linear_retention_index(
        unknown_retention_time_min=dead_time + unknown_adjusted,
        dead_time_min=dead_time,
        lower_alkane_carbon_number=8,
        lower_alkane_retention_time_min=dead_time + lower_adjusted,
        upper_alkane_carbon_number=10,
        upper_alkane_retention_time_min=dead_time + upper_adjusted,
    )

    assert index == pytest.approx(900.0)


def test_detector_response_calibration_recovers_line_and_uncertainty() -> None:
    result = fit_detector_response_calibration(
        (0.0, 0.1, 0.2, 0.3),
        (2.0, 12.1, 21.9, 32.0),
        detector_id="uv_detector_254nm",
        provenance_id="four-point-calibration",
    )

    assert result.slope == pytest.approx(99.8, rel=0.01)
    assert result.intercept == pytest.approx(2.0, abs=0.1)
    assert result.r_squared > 0.999
    assert result.residual_standard_deviation > 0.0
    assert result.quantitation_limit > result.detection_limit > 0.0
    response = result.response(0.15)
    assert result.concentration(response) == pytest.approx(0.15)


@pytest.mark.parametrize(
    ("tailing_factor", "expected"),
    (
        (0.4, "severe_fronting"),
        (0.7, "fronting"),
        (1.0, "symmetric"),
        (1.5, "tailing"),
        (2.5, "severe_tailing"),
    ),
)
def test_peak_shape_status_flags_asymmetry(tailing_factor: float, expected: str) -> None:
    assert peak_shape_status(tailing_factor) == expected
    report = evaluate_chromatography_method(
        _hplc_analyte(tailing_factor=tailing_factor),
        dead_time_min=0.5,
        temperature_K=298.15,
        mobile_phase_fraction=0.40,
        detector_concentration=0.01,
    )
    assert report.asymmetric_peak is (expected != "symmetric")
    assert report.peak_shape_status == expected


def test_empirical_chromatography_model_card_is_auditable() -> None:
    card = {
        item.model_id: item for item in spectroscopy_model_cards()
    }["empirical_chromatography_method_sensitivity_v1"]

    assert card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(card) == []
