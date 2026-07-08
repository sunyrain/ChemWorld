from __future__ import annotations

import pytest

from chemworld.physchem import (
    MechanismScenarioCard,
    get_mechanism_card,
    list_mechanism_cards,
    list_mechanism_paths,
    load_library_mechanism,
    validate_mechanism_library,
)

EXPECTED_MECHANISMS = {
    "autocatalytic_reaction",
    "catalyst_deactivation",
    "cstr_multiplicity",
    "electrochemical_conversion",
    "parallel_series_reaction",
    "pfr_hotspot",
    "reaction_extraction",
    "reactive_distillation_lite",
    "reversible_reaction",
    "simple_batch_reaction",
}


def test_curated_mechanism_library_is_complete_and_valid() -> None:
    paths = {path.stem for path in list_mechanism_paths()}
    cards = list_mechanism_cards()
    report = validate_mechanism_library()

    assert paths == EXPECTED_MECHANISMS
    assert {card.mechanism_id for card in cards} == EXPECTED_MECHANISMS
    assert report.passed, report.to_dict()
    assert report.cards_checked == len(EXPECTED_MECHANISMS)
    assert report.mechanisms_checked == len(EXPECTED_MECHANISMS)


@pytest.mark.parametrize("card", list_mechanism_cards())
def test_every_mechanism_card_loads_a_balanced_network(card: MechanismScenarioCard) -> None:
    network = load_library_mechanism(card)
    species = set(network.species_ids)

    assert network.network_id == card.mechanism_id
    assert network.check_element_balance()
    assert set(card.initial_amounts_mol).issubset(species)
    assert set(card.target_species).issubset(species)
    assert set(card.impurity_species).issubset(species)
    assert card.expected_qualitative_behavior
    assert card.to_dict()["mechanism_id"] == card.mechanism_id


def test_get_mechanism_card_accepts_card_or_mechanism_id() -> None:
    by_card = get_mechanism_card("simple-batch-reaction-card")
    by_mechanism = get_mechanism_card("simple_batch_reaction")

    assert by_card == by_mechanism
    assert by_card.resolved_mechanism_path.exists()


def test_autocatalytic_mechanism_exposes_seed_sensitivity() -> None:
    network = load_library_mechanism("autocatalytic_reaction")
    unseeded = network.reaction_rates(
        {"A": 1.0, "P": 0.0},
        volume_L=1.0,
        temperature_K=335.0,
    )
    seeded = network.reaction_rates(
        {"A": 1.0, "P": 0.05},
        volume_L=1.0,
        temperature_K=335.0,
    )

    assert unseeded["autocatalytic_growth"] == 0.0
    assert seeded["autocatalytic_growth"] > seeded["slow_initiation"]


def test_catalyst_deactivation_mechanism_loses_active_catalyst_over_time() -> None:
    network = load_library_mechanism("catalyst_deactivation")
    initial = {
        "A": 1.0,
        "P": 0.0,
        "B": 0.0,
        "D": 0.0,
        "Cat_active": 0.015,
        "Cat_dead": 0.0,
    }
    short = network.integrate_batch(
        initial,
        volume_L=1.0,
        temperature_K=370.0,
        duration_s=2000.0,
    )
    long = network.integrate_batch(
        initial,
        volume_L=1.0,
        temperature_K=370.0,
        duration_s=18000.0,
    )

    assert long.final_amounts_mol["Cat_dead"] > short.final_amounts_mol["Cat_dead"]
    assert long.final_amounts_mol["Cat_active"] < short.final_amounts_mol["Cat_active"]


def test_reaction_extraction_mechanism_prefers_product_in_organic_phase() -> None:
    network = load_library_mechanism("reaction_extraction")
    result = network.integrate_batch(
        {
            "A": 1.0,
            "P_aq": 0.0,
            "P_org": 0.0,
            "B_aq": 0.0,
            "B_org": 0.0,
            "D": 0.0,
            "E": 0.0,
        },
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=18000.0,
    )

    assert result.final_amounts_mol["P_org"] > result.final_amounts_mol["B_org"]
    assert result.final_amounts_mol["P_org"] > 0.0


def test_reactive_distillation_mechanism_forms_product_and_vapor_species() -> None:
    network = load_library_mechanism("reactive_distillation_lite")
    result = network.integrate_batch(
        {
            "Acid": 1.0,
            "Alcohol": 1.25,
            "Ester": 0.0,
            "Water": 0.0,
            "Ether": 0.0,
            "Ester_vapor": 0.0,
            "Alcohol_vapor": 0.0,
            "Water_vapor": 0.0,
        },
        volume_L=1.0,
        temperature_K=370.0,
        duration_s=25000.0,
    )

    assert result.final_amounts_mol["Ester"] > 0.0
    assert result.final_amounts_mol["Alcohol_vapor"] > 0.0
