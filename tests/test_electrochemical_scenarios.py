from __future__ import annotations

import pytest

from chemworld.physchem import (
    MaturityLevel,
    assess_side_reaction_thresholds,
    electrochemical_scenario_cards,
    electrochemistry_model_cards,
    generate_electrochemical_scenario,
    validate_model_card,
)
from chemworld.physchem.electrochemical_scenarios import HIDDEN_PARAMETER_IDS


def test_curated_electrochemical_cards_expose_public_contract_without_ranges() -> None:
    cards = electrochemical_scenario_cards()

    assert {card.scenario_id for card in cards} == {
        "aqueous_selective_reduction",
        "organic_anodic_coupling",
    }
    for card in cards:
        public = card.to_public_dict()
        assert set(public["hidden_parameter_policy"]) == set(HIDDEN_PARAMETER_IDS)
        assert "hidden_parameter_ranges" not in public
        assert all(
            "minimum" not in policy and "maximum" not in policy
            for policy in public["hidden_parameter_policy"].values()
        )
        assert set(card.to_private_dict()["hidden_parameter_ranges"]) == set(
            HIDDEN_PARAMETER_IDS
        )


def test_hidden_parameter_generation_is_deterministic_split_sensitive_and_bounded() -> None:
    card = electrochemical_scenario_cards()[0]
    first = generate_electrochemical_scenario(card, split="public-test", seed=7)
    repeat = generate_electrochemical_scenario(card, split="public-test", seed=7)
    other_split = generate_electrochemical_scenario(card, split="public-dev", seed=7)

    assert first.hidden_parameters == repeat.hidden_parameters
    assert first.world_id == repeat.world_id
    assert first.hidden_parameter_digest == repeat.hidden_parameter_digest
    assert first.hidden_parameters != other_split.hidden_parameters
    assert len(first.hidden_parameter_digest) == 64
    for parameter_id, value in first.hidden_parameters.to_dict().items():
        bounds = card.hidden_parameter_ranges[parameter_id]
        assert bounds.minimum <= value <= bounds.maximum


def test_private_eval_requires_salt_and_changes_with_salt() -> None:
    card = electrochemical_scenario_cards()[0]
    with pytest.raises(ValueError, match="private_salt"):
        generate_electrochemical_scenario(card, split="private-eval", seed=3)
    first = generate_electrochemical_scenario(
        card,
        split="private-eval",
        seed=3,
        private_salt="maintainer-secret-a",
    )
    second = generate_electrochemical_scenario(
        card,
        split="private-eval",
        seed=3,
        private_salt="maintainer-secret-b",
    )

    assert first.hidden_parameters != second.hidden_parameters
    public = first.to_public_dict()
    assert "maintainer-secret-a" not in str(public)
    assert "hidden_parameters" not in public


def test_generated_instance_builds_consistent_electrochemical_model_bundle() -> None:
    card = electrochemical_scenario_cards()[0]
    instance = generate_electrochemical_scenario(
        card,
        split="public-test",
        seed=11,
    )
    bundle = instance.build_model_bundle()

    assert bundle.reaction.reaction_id == card.redox.reaction_id
    assert bundle.reaction.electrode_area_m2 == pytest.approx(card.electrode_area_m2)
    assert bundle.diffusion_layer.electrode_area_m2 == pytest.approx(
        card.electrode_area_m2
    )
    assert bundle.double_layer.electrode_area_m2 == pytest.approx(card.electrode_area_m2)
    assert bundle.double_layer.series_resistance_ohm == pytest.approx(
        bundle.electrolyte_resistance.total_resistance_ohm
    )
    assert bundle.diffusion_layer.provenance_id == instance.hidden_parameter_digest


def test_side_reaction_thresholds_distinguish_selective_risk_and_window_breach() -> None:
    card = electrochemical_scenario_cards()[0]
    selective = assess_side_reaction_thresholds(card, potential_V=-0.4)
    cathodic = assess_side_reaction_thresholds(card, potential_V=-1.0)
    outside = assess_side_reaction_thresholds(card, potential_V=-1.3)

    assert selective.status == "inside_selective_window"
    assert selective.severity == pytest.approx(0.0)
    assert cathodic.status == "side_reaction_risk"
    assert cathodic.cathodic_side_reaction
    assert 0.0 < cathodic.severity < 1.0
    assert outside.status == "window_exceeded"
    assert outside.severity == pytest.approx(1.0)
    assert "electrolyte_window_exceeded" in outside.flags


def test_electrochemical_scenario_model_card_is_lite_until_runtime_bound() -> None:
    card = {
        item.model_id: item for item in electrochemistry_model_cards()
    }["electrochemical_scenario_card_generation_v1"]

    assert card.maturity is MaturityLevel.LITE
    assert validate_model_card(card) == []
