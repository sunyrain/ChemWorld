from __future__ import annotations

import pytest

from chemworld.physchem import (
    crystallize,
    downstream_score,
    dry_solid,
    evaporation_flash,
    filter_cake,
    liquid_liquid_extraction,
    simple_distillation,
)


def test_multistage_extraction_improves_product_recovery_and_balances_material() -> None:
    feed = {"product": 1.0, "impurity": 0.25}
    one_stage = liquid_liquid_extraction(
        feed,
        partition_coefficients={"product": 5.0, "impurity": 0.4},
        aqueous_volume_L=1.0,
        organic_volume_L=0.35,
        stages=1,
        stage_efficiency=0.85,
    )
    three_stage = liquid_liquid_extraction(
        feed,
        partition_coefficients={"product": 5.0, "impurity": 0.4},
        aqueous_volume_L=1.0,
        organic_volume_L=0.35,
        stages=3,
        stage_efficiency=0.85,
    )

    assert three_stage.recovery("product", "extract", feed["product"]) > one_stage.recovery(
        "product",
        "extract",
        feed["product"],
    )
    assert three_stage.purity("product", "extract") > 0.80
    assert three_stage.ledger.material_balance_error_mol < 1e-12
    assert three_stage.ledger.cost > one_stage.ledger.cost


def test_flash_evaporation_prefers_volatile_component_and_reports_heat_duty() -> None:
    feed = {"solvent": 2.0, "product": 0.25}
    result = evaporation_flash(
        feed,
        k_values={"solvent": 2.5, "product": 0.05},
        latent_heats_J_mol={"solvent": 38_000.0, "product": 65_000.0},
        approach_to_equilibrium=0.9,
        max_vapor_fraction=0.6,
    )

    assert result.outlets["vapor"]["solvent"] > result.outlets["vapor"]["product"]
    assert result.outlets["liquid"]["product"] / sum(result.outlets["liquid"].values()) > (
        feed["product"] / sum(feed.values())
    )
    assert result.ledger.heat_duty_J > 0.0
    assert result.ledger.material_balance_error_mol < 1e-10


def test_distillation_enriches_light_key_but_high_reflux_costs_more() -> None:
    feed = {"light": 1.0, "heavy": 1.0}
    low_reflux = simple_distillation(
        feed,
        volatility_scores={"light": 4.0, "heavy": 1.0},
        distillate_cut_fraction=0.45,
        reflux_ratio=0.2,
        stage_efficiency=0.7,
    )
    high_reflux = simple_distillation(
        feed,
        volatility_scores={"light": 4.0, "heavy": 1.0},
        distillate_cut_fraction=0.45,
        reflux_ratio=3.0,
        stage_efficiency=0.7,
    )

    feed_light_purity = feed["light"] / sum(feed.values())
    assert low_reflux.purity("light", "distillate") > feed_light_purity
    assert high_reflux.purity("light", "distillate") > low_reflux.purity(
        "light",
        "distillate",
    )
    assert high_reflux.ledger.cost > low_reflux.ledger.cost
    assert high_reflux.ledger.material_balance_error_mol < 1e-12


def test_crystallization_and_filtration_reduce_impurity_with_tradeoff() -> None:
    feed = {"product": 1.2, "impurity": 0.3, "solvent": 3.0}
    crystals = crystallize(
        feed,
        target_component="product",
        solubility_mol_L=0.25,
        solvent_volume_L=2.0,
        crystal_growth_efficiency=0.9,
        impurity_occlusion_fraction=0.08,
    )
    filtered_dirty = filter_cake(
        crystals.outlet("crystals"),
        solid_component="product",
        solid_recovery=0.95,
        impurity_retention_fraction=0.40,
        wash_efficiency=0.0,
    )
    filtered_washed = filter_cake(
        crystals.outlet("crystals"),
        solid_component="product",
        solid_recovery=0.95,
        impurity_retention_fraction=0.40,
        wash_efficiency=0.8,
        solid_wash_loss_fraction=0.03,
    )

    assert crystals.outlets["crystals"]["product"] > 0.0
    assert crystals.purity("product", "crystals", ignored_components=("solvent",)) > 0.90
    assert filtered_washed.purity("product", "cake", ignored_components=("solvent",)) > (
        filtered_dirty.purity("product", "cake", ignored_components=("solvent",))
    )
    assert filtered_washed.recovery("product", "cake", crystals.outlets["crystals"]["product"]) < (
        filtered_dirty.recovery("product", "cake", crystals.outlets["crystals"]["product"])
    )
    assert filtered_washed.ledger.material_balance_error_mol < 1e-12


def test_drying_removes_solvent_but_harsh_conditions_degrade_product() -> None:
    wet = {"product": 0.8, "impurity": 0.02, "solvent": 0.4}
    mild = dry_solid(
        wet,
        solvent_component="solvent",
        target_component="product",
        residual_solvent_fraction=0.05,
        temperature_K=315.0,
        duration_h=1.0,
        degradation_rate_per_h=0.01,
    )
    harsh = dry_solid(
        wet,
        solvent_component="solvent",
        target_component="product",
        residual_solvent_fraction=0.01,
        temperature_K=390.0,
        duration_h=4.0,
        degradation_rate_per_h=0.03,
    )

    assert harsh.outlets["dried_solid"]["solvent"] < mild.outlets["dried_solid"]["solvent"]
    assert harsh.outlets["dried_solid"]["product"] < mild.outlets["dried_solid"]["product"]
    assert harsh.ledger.risk > mild.ledger.risk
    assert harsh.ledger.material_balance_error_mol < 1e-12


def test_downstream_score_penalizes_excessive_processing() -> None:
    feed = {"product": 1.0, "impurity": 0.2}
    moderate = liquid_liquid_extraction(
        feed,
        partition_coefficients={"product": 4.0, "impurity": 0.5},
        aqueous_volume_L=1.0,
        organic_volume_L=0.6,
        stages=2,
        stage_efficiency=0.9,
    )
    excessive = liquid_liquid_extraction(
        feed,
        partition_coefficients={"product": 4.0, "impurity": 0.5},
        aqueous_volume_L=1.0,
        organic_volume_L=0.6,
        stages=8,
        stage_efficiency=0.9,
        solvent_loss_fraction=0.05,
    )

    assert excessive.recovery("product", "extract", feed["product"]) >= moderate.recovery(
        "product",
        "extract",
        feed["product"],
    )
    assert excessive.ledger.cost > moderate.ledger.cost
    assert downstream_score(
        excessive,
        target_component="product",
        target_outlet="extract",
        feed_target_mol=feed["product"],
    ) < downstream_score(
        moderate,
        target_component="product",
        target_outlet="extract",
        feed_target_mol=feed["product"],
    )


def test_separation_validation_fails_fast() -> None:
    with pytest.raises(ValueError, match="stages"):
        liquid_liquid_extraction(
            {"product": 1.0},
            partition_coefficients={"product": 1.0},
            aqueous_volume_L=1.0,
            organic_volume_L=1.0,
            stages=0,
        )
    with pytest.raises(ValueError, match="distillate_cut_fraction"):
        simple_distillation(
            {"light": 1.0},
            volatility_scores={"light": 1.0},
            distillate_cut_fraction=1.5,
        )
    with pytest.raises(ValueError, match="target_component"):
        crystallize(
            {"impurity": 1.0},
            target_component="product",
            solubility_mol_L=0.1,
            solvent_volume_L=1.0,
        )
