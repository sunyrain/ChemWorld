from __future__ import annotations

import pytest

from chemworld.physchem import (
    ActivityModelSpec,
    DistributionCoefficientModelSpec,
    MaturityLevel,
    activity_corrected_extraction_train,
    separation_model_cards,
    validate_model_card,
)


def _distribution_model(
    *,
    organic_activity_model: ActivityModelSpec | None = None,
) -> DistributionCoefficientModelSpec:
    return DistributionCoefficientModelSpec(
        model_id="target_impurity_partition",
        component_ids=("target", "impurity"),
        intrinsic_partition_coefficients={"target": 4.0, "impurity": 0.5},
        provenance_id="synthetic-analytical-extraction-case",
        organic_activity_model=organic_activity_model,
    )


def test_fresh_solvent_stages_match_ideal_analytical_recovery() -> None:
    result = activity_corrected_extraction_train(
        {"target": 1.0, "impurity": 1.0},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=0.5,
        extraction_stages=2,
    )

    assert result.target_recovery == pytest.approx(1.0 - (1.0 / 3.0) ** 2)
    assert result.outlets["raffinate"]["target"] == pytest.approx((1.0 / 3.0) ** 2)
    assert result.outlets["extract"]["impurity"] == pytest.approx(1.0 - 0.8**2)
    assert result.target_purity > 0.70
    assert result.material_balance_error_mol < 1.0e-12
    assert all(report.converged for report in result.stage_reports)


def test_activity_models_correct_distribution_coefficients() -> None:
    organic_model = ActivityModelSpec(
        "organic_margules",
        ("target", "impurity"),
        "margules",
        {"A:target|impurity": 1.2, "A:impurity|target": 0.8},
    )
    ideal = activity_corrected_extraction_train(
        {"target": 0.5, "impurity": 0.5},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=1.0,
    )
    nonideal = activity_corrected_extraction_train(
        {"target": 0.5, "impurity": 0.5},
        distribution_model=_distribution_model(
            organic_activity_model=organic_model,
        ),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=1.0,
    )

    report = nonideal.stage_reports[0]
    assert report.organic_activity_coefficients["target"] > 1.0
    assert report.distribution_coefficients["target"] < 4.0
    assert nonideal.target_recovery < ideal.target_recovery
    assert report.material_balance_error_mol < 1.0e-12


def test_wash_sequence_rejects_impurity_with_explicit_loss_and_balance() -> None:
    unwashed = activity_corrected_extraction_train(
        {"target": 1.0, "impurity": 1.0},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=0.5,
        extraction_stages=2,
    )
    washed = activity_corrected_extraction_train(
        {"target": 1.0, "impurity": 1.0},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=0.5,
        extraction_stages=2,
        wash_aqueous_volumes_L=(0.5, 0.5),
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
    assert washed.material_balance_error_mol < 1.0e-12


def test_entrainment_is_mass_conserving_and_can_reduce_extract_purity() -> None:
    clean = activity_corrected_extraction_train(
        {"target": 1.0, "impurity": 1.0},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=1.0,
    )
    entrained = activity_corrected_extraction_train(
        {"target": 1.0, "impurity": 1.0},
        distribution_model=_distribution_model(),
        target_component="target",
        aqueous_volume_L=1.0,
        organic_volume_L=1.0,
        extraction_entrainment_fraction=0.10,
    )

    assert entrained.target_purity < clean.target_purity
    assert entrained.entrained_aqueous_volume_L == pytest.approx(0.10)
    assert entrained.stage_reports[0].entrained_amounts_mol["impurity"] > 0.0
    assert entrained.material_balance_error_mol < 1.0e-12


def test_extraction_contract_rejects_component_and_control_errors() -> None:
    with pytest.raises(ValueError, match="exactly match"):
        activity_corrected_extraction_train(
            {"target": 1.0},
            distribution_model=_distribution_model(),
            target_component="target",
            aqueous_volume_L=1.0,
            organic_volume_L=1.0,
        )
    with pytest.raises(ValueError, match="wash_aqueous_volumes_L"):
        activity_corrected_extraction_train(
            {"target": 1.0, "impurity": 0.2},
            distribution_model=_distribution_model(),
            target_component="target",
            aqueous_volume_L=1.0,
            organic_volume_L=1.0,
            wash_aqueous_volumes_L=(0.0,),
        )


def test_extraction_model_card_is_reference_validated_and_auditable() -> None:
    card = {
        item.model_id: item for item in separation_model_cards()
    }["activity_corrected_extraction_train_v1"]

    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
    assert any("entrainment" in equation for equation in card.equations)
