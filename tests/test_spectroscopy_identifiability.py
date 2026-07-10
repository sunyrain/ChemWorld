from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card
from chemworld.physchem.spectroscopy import build_signal_spec, synthesize_signal
from chemworld.physchem.spectroscopy_adapter_manifest import (
    OWNED_PATHS,
    SpectralIdentifiabilityProvider,
    spectroscopy_identifiability_adapter_manifest,
    spectroscopy_identifiability_provider_contract,
)
from chemworld.physchem.spectroscopy_identifiability import (
    CHEMICALS_COMMIT,
    RMG_PY_COMMIT,
    SpectralIdentifiabilitySpec,
    evaluate_spectral_identifiability,
    spectroscopy_identifiability_model_card,
)


def _measurement(
    amounts: dict[str, float],
    *,
    instrument_id: str = "hplc",
    seed: int,
    replicate_count: int = 5,
):
    spec = build_signal_spec(
        instrument_id,
        ("reactant_secret", "target_secret", "impurity_secret"),
        target_species=("target_secret",),
        impurity_species=("impurity_secret",),
        formulas={
            "reactant_secret": "C2H6O",
            "target_secret": "C4H8O2",
            "impurity_secret": "C3H6O",
        },
    )
    return synthesize_signal(
        spec,
        amounts,
        volume_L=1.0,
        seed=seed,
        replicate_count=replicate_count,
    )


def _reference_state(*, seed: int = 11, instrument_id: str = "hplc"):
    return _measurement(
        {
            "reactant_secret": 0.75,
            "target_secret": 0.04,
            "impurity_secret": 0.02,
        },
        instrument_id=instrument_id,
        seed=seed,
    )


def _alternative_state(*, seed: int = 29, instrument_id: str = "hplc"):
    return _measurement(
        {
            "reactant_secret": 0.15,
            "target_secret": 0.62,
            "impurity_secret": 0.08,
        },
        instrument_id=instrument_id,
        seed=seed,
    )


def test_hplc_states_are_stable_and_identifiable() -> None:
    report = evaluate_spectral_identifiability(
        _reference_state(),
        _alternative_state(),
    )
    assert report.replicate_stable
    assert report.states_distinct
    assert report.identifiable
    assert report.between_state_rmse >= report.thresholds.min_between_state_rmse
    assert report.separation_ratio >= report.thresholds.min_separation_ratio


def test_uvvis_default_dilution_exposes_insufficient_state_separation() -> None:
    report = evaluate_spectral_identifiability(
        _reference_state(instrument_id="uvvis"),
        _alternative_state(instrument_id="uvvis"),
    )
    assert report.instrument_id == "uvvis"
    assert report.replicate_stable
    assert not report.states_distinct
    assert not report.identifiable
    assert "separation_ratio_below_minimum" in report.warnings


def test_same_low_signal_state_is_not_misreported_as_distinct() -> None:
    amounts = {
        "reactant_secret": 1.0e-8,
        "target_secret": 1.0e-8,
        "impurity_secret": 1.0e-8,
    }
    left = _measurement(amounts, seed=3)
    right = _measurement(amounts, seed=47)
    report = evaluate_spectral_identifiability(left, right)
    assert not report.replicate_stable
    assert not report.states_distinct
    assert not report.identifiable
    assert "replicate_instability" in report.warnings


def test_unstable_replicates_are_reported_without_hiding_state_separation() -> None:
    reference = _reference_state()
    alternative = _alternative_state()
    point_count = len(reference.axis)
    unstable = replace(
        reference,
        replicate_signals=(
            tuple(np.zeros(point_count)),
            tuple(np.ones(point_count)),
            tuple(np.zeros(point_count)),
            tuple(np.ones(point_count)),
            tuple(np.zeros(point_count)),
        ),
    )
    report = evaluate_spectral_identifiability(
        unstable,
        alternative,
        spec=SpectralIdentifiabilitySpec(max_within_state_rmse=0.05),
    )
    assert not report.replicate_stable
    assert not report.identifiable
    assert "replicate_instability" in report.warnings


def test_report_public_boundary_excludes_species_and_hidden_amounts() -> None:
    report = evaluate_spectral_identifiability(
        _reference_state(),
        _alternative_state(),
    )
    encoded = json.dumps(report.to_dict(), sort_keys=True)
    assert "reactant_secret" not in encoded
    assert "target_secret" not in encoded
    assert "impurity_secret" not in encoded
    assert "species_id" not in encoded
    assert "amounts_mol" not in encoded
    assert report.reference_detected_peak_count > 0


def test_signal_hashes_and_serialization_are_deterministic() -> None:
    reference = _reference_state()
    alternative = _alternative_state()
    left = evaluate_spectral_identifiability(reference, alternative)
    right = evaluate_spectral_identifiability(reference, alternative)
    assert left.to_dict() == right.to_dict()
    assert left.reference_signal_sha256 == right.reference_signal_sha256
    assert left.alternative_signal_sha256 == right.alternative_signal_sha256


def test_pair_validation_rejects_instrument_axis_and_replicate_mismatches() -> None:
    reference = _reference_state()
    alternative = _alternative_state()
    with pytest.raises(ValueError, match="same instrument_id"):
        evaluate_spectral_identifiability(
            reference,
            _alternative_state(instrument_id="uvvis"),
        )

    shifted_axis = replace(
        alternative,
        axis=(alternative.axis[0] + 0.1, *alternative.axis[1:]),
    )
    with pytest.raises(ValueError, match="identical axes"):
        evaluate_spectral_identifiability(reference, shifted_axis)

    single = _measurement(
        {
            "reactant_secret": 0.2,
            "target_secret": 0.4,
            "impurity_secret": 0.02,
        },
        seed=4,
        replicate_count=1,
    )
    with pytest.raises(ValueError, match="at least 3 replicates"):
        evaluate_spectral_identifiability(reference, single)


def test_identifiability_spec_rejects_invalid_thresholds() -> None:
    with pytest.raises(ValueError, match="min_replicates"):
        SpectralIdentifiabilitySpec(min_replicates=1)
    with pytest.raises(ValueError, match="min_separation_ratio"):
        SpectralIdentifiabilitySpec(min_separation_ratio=0.0)


def test_provider_distinguishes_invalid_input_from_valid_indistinguishability() -> None:
    provider = SpectralIdentifiabilityProvider()
    invalid = provider.evaluate({"reference": "bad", "alternative": "bad"})
    assert not invalid.success
    assert "SpectralMeasurement" in str(invalid.failure_reason)

    amounts = {
        "reactant_secret": 1.0e-8,
        "target_secret": 1.0e-8,
        "impurity_secret": 1.0e-8,
    }
    valid = provider.evaluate(
        {
            "reference": _measurement(amounts, seed=2),
            "alternative": _measurement(amounts, seed=3),
            "audit_spec": None,
        }
    )
    assert valid.success
    assert valid.diagnostics["identifiable"] is False
    assert valid.outputs["report"]["identifiable"] is False


def test_provider_contract_and_adapter_manifest_are_hash_bound() -> None:
    contract = spectroscopy_identifiability_provider_contract()
    manifest = spectroscopy_identifiability_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.owner_workstream == "wf-20-spectral-identifiability"
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["adapter_version"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_model_card_limits_claim_to_the_audit_calculation() -> None:
    card = spectroscopy_identifiability_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == "chemworld_spectral_identifiability_audit_vnext"
    assert any("not the synthetic spectra" in note for note in card.model_limit_notes)


def test_reference_boundary_commits_and_paths_are_auditable() -> None:
    card = spectroscopy_identifiability_model_card()
    reading = " ".join(card.reference_reading)
    assert CHEMICALS_COMMIT in reading
    assert RMG_PY_COMMIT in reading

    root = Path(__file__).resolve().parents[1]
    reference_root = root / "reference_repos"
    if not reference_root.is_dir():
        pytest.skip("optional reference_repos checkout is unavailable")
    assert (reference_root / "chemicals" / "chemicals" / "__init__.py").is_file()
    assert (reference_root / "rmg-py" / "rmgpy" / "__init__.py").is_file()
