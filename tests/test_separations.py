from __future__ import annotations

from math import ceil, log

import pytest

from chemworld.physchem import (
    FUGDistillationSpec,
    crystallize,
    downstream_score,
    dry_solid,
    evaporation_flash,
    fenske_underwood_gilliland_sizing,
    filter_cake,
    liquid_liquid_extraction,
    separation_model_cards,
    validate_model_card,
    vle_shortcut_distillation,
)
from chemworld.world.phase_kernel import partition_split


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
    assert three_stage.ledger.metadata["initialization_policy"] == "partition_weighted"
    assert three_stage.ledger.metadata["stability_diagnostic"]["phase_status"] == "two_liquid"


def test_partition_split_uses_lle_diagnostic_and_balances_runtime_amounts() -> None:
    split = partition_split(
        product_mol=0.8,
        impurity_mol=0.2,
        solvent=2,
        temperature_K=330.0,
        duration_s=240.0,
        stirring_speed_rpm=800.0,
        organic_volume_L=0.35,
        aqueous_volume_L=1.0,
    )

    assert split["lle_phase_status"] == "two_liquid"
    assert split["lle_partition_log_spread"] > 0.0
    assert split["organic_product_mol"] + split["aqueous_product_mol"] == pytest.approx(0.8)
    assert split["organic_impurity_mol"] + split["aqueous_impurity_mol"] == pytest.approx(0.2)
    assert split["organic_product_mol"] / 0.8 > split["organic_impurity_mol"] / 0.2


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


def test_vle_shortcut_distillation_uses_vle_and_fenske_distribution() -> None:
    feed = {"light": 1.0, "heavy": 1.0}
    low_reflux = vle_shortcut_distillation(
        feed,
        vapor_pressures_Pa={"light": 80_000.0, "heavy": 20_000.0},
        pressure_Pa=101_325.0,
        temperature_K=355.0,
        light_key="light",
        heavy_key="heavy",
        distillate_cut_fraction=0.45,
        theoretical_stages=8.0,
        reflux_ratio=0.2,
        stage_efficiency=0.7,
    )
    high_reflux = vle_shortcut_distillation(
        feed,
        vapor_pressures_Pa={"light": 80_000.0, "heavy": 20_000.0},
        pressure_Pa=101_325.0,
        temperature_K=355.0,
        light_key="light",
        heavy_key="heavy",
        distillate_cut_fraction=0.45,
        theoretical_stages=8.0,
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
    assert high_reflux.ledger.metadata["k_values"] == pytest.approx(
        {"light": 80_000.0 / 101_325.0, "heavy": 20_000.0 / 101_325.0}
    )
    assert high_reflux.ledger.metadata["relative_volatilities"] == pytest.approx(
        {"light": 4.0, "heavy": 1.0}
    )
    assert high_reflux.ledger.metadata["observed_fenske_stage_count"] == pytest.approx(
        high_reflux.ledger.metadata["effective_stages"]
    )
    assert high_reflux.ledger.material_balance_error_mol < 1e-12


def test_vle_shortcut_distillation_handles_multicomponent_keys() -> None:
    feed = {"lights": 0.5, "product": 1.0, "heavies": 0.4}
    result = vle_shortcut_distillation(
        feed,
        vapor_pressures_Pa={"lights": 120_000.0, "product": 45_000.0, "heavies": 8_000.0},
        pressure_Pa=80_000.0,
        temperature_K=345.0,
        light_key="product",
        heavy_key="heavies",
        distillate_cut_fraction=0.62,
        theoretical_stages=12.0,
        reflux_ratio=2.0,
        stage_efficiency=0.65,
        latent_heats_J_mol={"lights": 28_000.0, "product": 38_000.0, "heavies": 55_000.0},
    )

    assert result.purity("lights", "distillate") > feed["lights"] / sum(feed.values())
    assert result.purity("heavies", "bottoms") > feed["heavies"] / sum(feed.values())
    assert result.ledger.heat_duty_J > 0.0
    assert result.ledger.metadata["flash_anchor"]["k_values"]["product"] == pytest.approx(
        45_000.0 / 80_000.0
    )
    assert result.ledger.material_balance_error_mol < 1e-12


def test_fug_distillation_sizing_reports_stage_and_reflux_contract() -> None:
    spec = FUGDistillationSpec(
        light_key="benzene",
        heavy_key="toluene",
        relative_volatility=2.4,
        feed_light_mole_fraction=0.50,
        distillate_light_mole_fraction=0.95,
        bottoms_light_mole_fraction=0.05,
        reflux_ratio=2.0,
        stage_efficiency=0.72,
        pressure_top_Pa=101_325.0,
        pressure_bottom_Pa=121_325.0,
        provenance_id="local-btx-shortcut",
        provenance_note="synthetic benzene/toluene-style constant alpha sanity case",
    )
    report = fenske_underwood_gilliland_sizing(spec)

    expected_nmin = log((0.95 / 0.05) * (0.95 / 0.05)) / log(2.4)
    assert report.minimum_stages == pytest.approx(expected_nmin)
    assert 1.0 < report.underwood_theta < spec.relative_volatility
    assert report.minimum_reflux_ratio > 0.0
    assert report.reflux_ratio > report.minimum_reflux_ratio
    assert report.theoretical_stages > report.minimum_stages
    assert report.actual_trays == ceil(report.theoretical_stages / spec.stage_efficiency)
    assert 1 <= report.feed_stage_from_top <= report.actual_trays
    assert "pressure_profile_may_change_relative_volatility" in report.warnings
    assert report.to_dict()["provenance_id"] == "local-btx-shortcut"


def test_fug_distillation_stage_count_decreases_with_reflux_ratio() -> None:
    base = FUGDistillationSpec(
        light_key="light",
        heavy_key="heavy",
        relative_volatility=2.2,
        feed_light_mole_fraction=0.45,
        distillate_light_mole_fraction=0.93,
        bottoms_light_mole_fraction=0.06,
        reflux_ratio=2.0,
        stage_efficiency=0.85,
        provenance_id="local-binary-alpha",
    )
    reference = fenske_underwood_gilliland_sizing(base)
    low_reflux = fenske_underwood_gilliland_sizing(
        FUGDistillationSpec(
            light_key=base.light_key,
            heavy_key=base.heavy_key,
            relative_volatility=base.relative_volatility,
            feed_light_mole_fraction=base.feed_light_mole_fraction,
            distillate_light_mole_fraction=base.distillate_light_mole_fraction,
            bottoms_light_mole_fraction=base.bottoms_light_mole_fraction,
            reflux_ratio=reference.minimum_reflux_ratio * 1.2,
            stage_efficiency=base.stage_efficiency,
            provenance_id=base.provenance_id,
        )
    )
    high_reflux = fenske_underwood_gilliland_sizing(
        FUGDistillationSpec(
            light_key=base.light_key,
            heavy_key=base.heavy_key,
            relative_volatility=base.relative_volatility,
            feed_light_mole_fraction=base.feed_light_mole_fraction,
            distillate_light_mole_fraction=base.distillate_light_mole_fraction,
            bottoms_light_mole_fraction=base.bottoms_light_mole_fraction,
            reflux_ratio=reference.minimum_reflux_ratio * 3.0,
            stage_efficiency=base.stage_efficiency,
            provenance_id=base.provenance_id,
        )
    )

    assert high_reflux.theoretical_stages < low_reflux.theoretical_stages
    assert high_reflux.actual_trays <= low_reflux.actual_trays


def test_fug_distillation_validation_fails_on_invalid_design_contracts() -> None:
    with pytest.raises(ValueError, match="relative_volatility"):
        FUGDistillationSpec(
            light_key="light",
            heavy_key="heavy",
            relative_volatility=1.0,
            feed_light_mole_fraction=0.5,
            distillate_light_mole_fraction=0.95,
            bottoms_light_mole_fraction=0.05,
            reflux_ratio=2.0,
            provenance_id="bad-alpha",
        )
    with pytest.raises(ValueError, match="bottoms_light < feed_light < distillate_light"):
        FUGDistillationSpec(
            light_key="light",
            heavy_key="heavy",
            relative_volatility=2.0,
            feed_light_mole_fraction=0.5,
            distillate_light_mole_fraction=0.45,
            bottoms_light_mole_fraction=0.05,
            reflux_ratio=2.0,
            provenance_id="bad-split",
        )
    with pytest.raises(ValueError, match="provenance_id"):
        FUGDistillationSpec(
            light_key="light",
            heavy_key="heavy",
            relative_volatility=2.0,
            feed_light_mole_fraction=0.5,
            distillate_light_mole_fraction=0.95,
            bottoms_light_mole_fraction=0.05,
            reflux_ratio=2.0,
        )
    with pytest.raises(ValueError, match="minimum reflux"):
        fenske_underwood_gilliland_sizing(
            FUGDistillationSpec(
                light_key="light",
                heavy_key="heavy",
                relative_volatility=2.0,
                feed_light_mole_fraction=0.5,
                distillate_light_mole_fraction=0.95,
                bottoms_light_mole_fraction=0.05,
                reflux_ratio=0.1,
                provenance_id="below-rmin",
            )
        )


def test_separation_model_cards_document_vle_shortcut_distillation() -> None:
    cards = {card.model_id: card for card in separation_model_cards()}
    card = cards["vle_shortcut_distillation"]
    assert card.maturity.value == "reference_validated"
    assert validate_model_card(card) == []
    assert any("IDAES" in note for note in card.reference_reading)
    assert any("thermo" in note for note in card.reference_reading)
    assert any("phasepy" in note for note in card.reference_reading)
    fug_card = cards["fenske_underwood_gilliland_sizing"]
    assert fug_card.maturity.value == "reference_validated"
    assert validate_model_card(fug_card) == []
    assert any("Underwood" in equation for equation in fug_card.equations)
    assert any("IDAES tray_column.py" in note for note in fug_card.reference_reading)


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
        vle_shortcut_distillation(
            {"light": 1.0},
            vapor_pressures_Pa={"light": 10_000.0},
            pressure_Pa=101_325.0,
            temperature_K=350.0,
            light_key="light",
            heavy_key="light",
            distillate_cut_fraction=1.5,
            theoretical_stages=3.0,
        )
    with pytest.raises(ValueError, match="more volatile"):
        vle_shortcut_distillation(
            {"light": 1.0, "heavy": 1.0},
            vapor_pressures_Pa={"light": 10_000.0, "heavy": 20_000.0},
            pressure_Pa=101_325.0,
            temperature_K=350.0,
            light_key="light",
            heavy_key="heavy",
            distillate_cut_fraction=0.5,
            theoretical_stages=4.0,
        )
    with pytest.raises(ValueError, match="target_component"):
        crystallize(
            {"impurity": 1.0},
            target_component="product",
            solubility_mol_L=0.1,
            solvent_volume_L=1.0,
        )
