from __future__ import annotations

import json

import numpy as np
import pytest

from chemworld.physchem.equilibrium import ActivityModelSpec
from chemworld.physchem.extraction_units import DistributionCoefficientModelSpec
from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card
from chemworld.physchem.phase_equilibrium_adapter_manifest import (
    INTEGRATION_OPERATIONS,
    OWNED_PATHS,
    REPLACED_MODEL_IDS,
    StabilityAwareLLEProvider,
    stability_aware_lle_adapter_manifest,
    stability_aware_lle_provider_contract,
)
from chemworld.physchem.phase_equilibrium_units import (
    PHASE_EQUILIBRIUM_MODEL_ID,
    PHASEPY_COMMIT,
    PHASEPY_LLE_PATH,
    PHASEPY_STABILITY_PATH,
    LLEContactorSpec,
    StabilityAwareExtractionRequest,
    ideal_organic_fraction,
    simulate_stability_aware_extraction,
    stability_aware_lle_model_card,
)


def _distribution_model(
    *,
    target_k: float = 4.0,
    impurity_k: float = 0.25,
    aqueous_activity_model: ActivityModelSpec | None = None,
    organic_activity_model: ActivityModelSpec | None = None,
) -> DistributionCoefficientModelSpec:
    return DistributionCoefficientModelSpec(
        model_id="declared_target_impurity_profile",
        component_ids=("target", "impurity"),
        intrinsic_partition_coefficients={
            "target": target_k,
            "impurity": impurity_k,
        },
        provenance_id="wf40-synthetic-analytical-profile-v1",
        aqueous_activity_model=aqueous_activity_model,
        organic_activity_model=organic_activity_model,
    )


def _contactor(**overrides: object) -> LLEContactorSpec:
    values: dict[str, object] = {
        "aqueous_volume_L": 1.0,
        "organic_volume_L": 0.5,
        "extraction_stages": 2,
        "maximum_contact_volume_L": 10.0,
    }
    values.update(overrides)
    return LLEContactorSpec(**values)  # type: ignore[arg-type]


def _request(
    *,
    feed: dict[str, float] | None = None,
    distribution_model: DistributionCoefficientModelSpec | None = None,
    contactor: LLEContactorSpec | None = None,
    stability_activity_model: ActivityModelSpec | None = None,
) -> StabilityAwareExtractionRequest:
    return StabilityAwareExtractionRequest(
        feed_amounts_mol=feed or {"target": 1.0, "impurity": 1.0},
        distribution_model=distribution_model or _distribution_model(),
        target_component="target",
        contactor=contactor or _contactor(),
        temperature_K=298.15,
        stability_activity_model=stability_activity_model,
    )


def _assert_closed(result) -> None:
    assert result.material_balance_error_mol <= 1.0e-10
    assert result.maximum_stage_material_balance_error_mol <= 1.0e-10
    for component_id, feed_amount in result.feed_amounts_mol.items():
        recovered = sum(outlet.get(component_id, 0.0) for outlet in result.outlets.values())
        assert recovered == pytest.approx(feed_amount, abs=1.0e-10)


def test_ideal_fresh_solvent_train_matches_closed_form_recovery() -> None:
    result = simulate_stability_aware_extraction(_request())
    single_stage_fraction = ideal_organic_fraction(
        4.0,
        aqueous_volume_L=1.0,
        organic_volume_L=0.5,
    )
    expected_recovery = 1.0 - (1.0 - single_stage_fraction) ** 2

    assert result.model_id == PHASE_EQUILIBRIUM_MODEL_ID
    assert result.target_recovery == pytest.approx(expected_recovery)
    assert result.outlets["raffinate"]["target"] == pytest.approx(1.0 / 9.0)
    assert result.all_stages_two_liquid is True
    assert result.all_stages_converged is True
    assert [report.stage_id for report in result.stage_reports] == [
        "extraction_1",
        "extraction_2",
    ]
    assert all(report.iterations == 1 for report in result.stage_reports)
    _assert_closed(result)


def test_single_liquid_state_is_rejected_before_a_split_is_returned() -> None:
    request = _request(
        distribution_model=_distribution_model(target_k=1.0, impurity_k=1.0),
        contactor=_contactor(extraction_stages=1),
    )
    with pytest.raises(ValueError, match="outside the two-liquid domain"):
        simulate_stability_aware_extraction(request)


def test_activity_corrected_distribution_converges_and_changes_recovery() -> None:
    aqueous_model = ActivityModelSpec(
        "aqueous_margules",
        ("target", "impurity"),
        "margules",
        {"A:target|impurity": 1.2, "A:impurity|target": 0.8},
    )
    ideal = simulate_stability_aware_extraction(_request(contactor=_contactor(extraction_stages=1)))
    nonideal = simulate_stability_aware_extraction(
        _request(
            distribution_model=_distribution_model(aqueous_activity_model=aqueous_model),
            contactor=_contactor(extraction_stages=1),
        )
    )

    stage = nonideal.stage_reports[0]
    assert stage.iterations > 1
    assert stage.aqueous_activity_coefficients["target"] > 1.0
    assert stage.distribution_coefficients["target"] > 4.0
    assert nonideal.target_recovery > ideal.target_recovery
    assert stage.distribution_residual <= 1.0e-10
    _assert_closed(nonideal)


def test_nonconverged_activity_iteration_fails_with_residual() -> None:
    aqueous_model = ActivityModelSpec(
        "aqueous_margules",
        ("target", "impurity"),
        "margules",
        {"A:target|impurity": 1.5, "A:impurity|target": 1.0},
    )
    request = _request(
        distribution_model=_distribution_model(aqueous_activity_model=aqueous_model),
        contactor=_contactor(
            extraction_stages=1,
            max_iterations=1,
            distribution_tolerance=1.0e-15,
        ),
    )
    with pytest.raises(RuntimeError, match="did not converge after 1 iterations"):
        simulate_stability_aware_extraction(request)


def test_wash_improves_purity_at_an_explicit_recovery_cost() -> None:
    unwashed = simulate_stability_aware_extraction(_request())
    washed = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                wash_aqueous_volumes_L=(0.5, 0.5),
                wash_stage_efficiency=1.0,
            )
        )
    )

    assert washed.target_purity > unwashed.target_purity
    assert washed.target_recovery < unwashed.target_recovery
    assert washed.impurity_rejection > unwashed.impurity_rejection
    assert set(washed.outlets) == {"raffinate", "wash_1", "wash_2", "extract"}
    assert [report.mode for report in washed.stage_reports] == [
        "extraction",
        "extraction",
        "wash",
        "wash",
    ]
    _assert_closed(washed)


def test_auto_aqueous_continuity_entrains_organic_into_raffinate() -> None:
    clean = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=2.0,
                organic_volume_L=0.5,
            )
        )
    )
    entrained = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=2.0,
                organic_volume_L=0.5,
                extraction_entrainment_fraction=0.10,
            )
        )
    )
    stage = entrained.stage_reports[0]

    assert stage.continuous_phase == "aqueous"
    assert stage.dispersed_phase == "organic"
    assert stage.entrained_from_phase == "organic"
    assert stage.entrained_to_phase == "aqueous"
    assert stage.entrained_volume_L == pytest.approx(0.05)
    assert stage.final_phase_volumes_L == pytest.approx({"aqueous": 2.05, "organic": 0.45})
    assert entrained.target_recovery < clean.target_recovery
    _assert_closed(entrained)


def test_auto_organic_continuity_entrains_aqueous_into_extract() -> None:
    clean = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=0.5,
                organic_volume_L=2.0,
            )
        )
    )
    entrained = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=0.5,
                organic_volume_L=2.0,
                extraction_entrainment_fraction=0.10,
            )
        )
    )
    stage = entrained.stage_reports[0]

    assert stage.continuous_phase == "organic"
    assert stage.dispersed_phase == "aqueous"
    assert stage.entrained_from_phase == "aqueous"
    assert stage.entrained_to_phase == "organic"
    assert stage.entrained_volume_L == pytest.approx(0.05)
    assert stage.final_phase_volumes_L == pytest.approx({"aqueous": 0.45, "organic": 2.05})
    assert entrained.target_recovery > clean.target_recovery
    _assert_closed(entrained)


def test_explicit_continuous_phase_overrides_volume_heuristic() -> None:
    result = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=2.0,
                organic_volume_L=0.5,
                extraction_entrainment_fraction=0.10,
                extraction_continuous_phase="organic",
            )
        )
    )
    stage = result.stage_reports[0]
    assert stage.continuous_phase == "organic"
    assert stage.entrained_volume_L == pytest.approx(0.2)
    assert "auto_continuous_phase_organic" not in stage.warnings
    _assert_closed(result)


def test_near_equal_phase_volumes_emit_inversion_boundary_warning() -> None:
    result = simulate_stability_aware_extraction(
        _request(
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=1.0,
                organic_volume_L=1.1,
            )
        )
    )
    assert "near_phase_continuity_inversion" in result.stage_reports[0].warnings


def test_extreme_declared_partition_coefficients_remain_finite_and_closed() -> None:
    result = simulate_stability_aware_extraction(
        _request(
            distribution_model=_distribution_model(
                target_k=1.0e12,
                impurity_k=1.0e-12,
            ),
            contactor=_contactor(extraction_stages=1),
        )
    )
    assert result.target_recovery > 1.0 - 1.0e-10
    assert result.outlets["extract"]["impurity"] < 1.0e-10
    assert np.isfinite(result.minimum_tpd_like)
    _assert_closed(result)


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: LLEContactorSpec(aqueous_volume_L=0.0, organic_volume_L=1.0),
            "aqueous_volume_L",
        ),
        (
            lambda: _contactor(extraction_stages=21),
            "declared maximum",
        ),
        (
            lambda: _contactor(extraction_entrainment_fraction=1.0),
            r"lie in \[0, 1\)",
        ),
        (
            lambda: _contactor(extraction_continuous_phase="unknown"),
            "must be auto",
        ),
        (
            lambda: _contactor(maximum_contact_volume_L=1.0),
            "exceeds maximum",
        ),
        (
            lambda: _request(feed={"target": 1.0, "other": 1.0}),
            "exactly match",
        ),
        (
            lambda: _request(
                distribution_model=_distribution_model(
                    target_k=1.0e13,
                    impurity_k=0.25,
                )
            ),
            r"outside \[1e-12, 1e12\]",
        ),
        (
            lambda: StabilityAwareExtractionRequest(
                feed_amounts_mol={"target": 1.0},
                distribution_model=DistributionCoefficientModelSpec(
                    model_id="single",
                    component_ids=("target",),
                    intrinsic_partition_coefficients={"target": 2.0},
                    provenance_id="single-component",
                ),
                target_component="target",
                contactor=_contactor(extraction_stages=1),
            ),
            "at least two",
        ),
    ],
)
def test_invalid_domains_fail_explicitly(factory, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        factory()


def test_deterministic_domain_sweep_preserves_stability_and_ledgers() -> None:
    rng = np.random.default_rng(20260711)
    for _ in range(30):
        target_k = float(rng.uniform(3.0, 30.0))
        impurity_k = float(rng.uniform(0.03, 0.5))
        request = _request(
            feed={
                "target": float(rng.uniform(0.2, 3.0)),
                "impurity": float(rng.uniform(0.2, 3.0)),
            },
            distribution_model=_distribution_model(
                target_k=target_k,
                impurity_k=impurity_k,
            ),
            contactor=_contactor(
                extraction_stages=1,
                aqueous_volume_L=float(rng.uniform(0.4, 2.0)),
                organic_volume_L=float(rng.uniform(0.4, 2.0)),
                extraction_stage_efficiency=float(rng.uniform(0.6, 1.0)),
                extraction_entrainment_fraction=float(rng.uniform(0.0, 0.08)),
            ),
        )
        result = simulate_stability_aware_extraction(request)
        assert result.all_stages_two_liquid
        assert result.all_stages_converged
        assert 0.0 <= result.target_recovery <= 1.0
        assert 0.0 <= result.target_purity <= 1.0
        _assert_closed(result)


def test_provider_returns_contract_complete_success_and_failure() -> None:
    provider = StabilityAwareLLEProvider()
    success = provider.evaluate({"request": _request()})
    assert success.success is True
    assert success.outputs["phase_equilibrium_result"]["model_id"] == PHASE_EQUILIBRIUM_MODEL_ID
    assert success.diagnostics["all_stages_two_liquid"] is True
    assert success.diagnostics["material_balance_error_mol"] <= 1.0e-10

    invalid_type = provider.evaluate({"request": {}})
    assert invalid_type.success is False
    assert invalid_type.outputs == {}
    assert invalid_type.failure_reason == ("request must be a StabilityAwareExtractionRequest")

    single_liquid = provider.evaluate(
        {
            "request": _request(
                distribution_model=_distribution_model(
                    target_k=1.0,
                    impurity_k=1.0,
                ),
                contactor=_contactor(extraction_stages=1),
            )
        }
    )
    assert single_liquid.success is False
    assert "outside the two-liquid domain" in str(single_liquid.failure_reason)
    assert single_liquid.diagnostics["all_stages_two_liquid"] is False


def test_model_card_and_replacement_manifest_are_auditable() -> None:
    card = stability_aware_lle_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == PHASE_EQUILIBRIUM_MODEL_ID
    assert any(PHASEPY_COMMIT in reference for reference in card.reference_reading)
    assert any(PHASEPY_LLE_PATH in reference for reference in card.reference_reading)
    assert any(PHASEPY_STABILITY_PATH in reference for reference in card.reference_reading)
    assert any("not a rigorous" in note for note in card.model_limit_notes)

    contract = stability_aware_lle_provider_contract()
    manifest = stability_aware_lle_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.integration_operations == INTEGRATION_OPERATIONS
    assert manifest.replaces_model_ids == REPLACED_MODEL_IDS
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["adapter_version"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_result_serialization_is_deterministic() -> None:
    request = _request(
        contactor=_contactor(
            wash_aqueous_volumes_L=(0.4,),
            extraction_entrainment_fraction=0.02,
            wash_entrainment_fraction=0.01,
        )
    )
    left = json.dumps(
        simulate_stability_aware_extraction(request).to_dict(),
        sort_keys=True,
    )
    right = json.dumps(
        simulate_stability_aware_extraction(request).to_dict(),
        sort_keys=True,
    )
    assert left == right
