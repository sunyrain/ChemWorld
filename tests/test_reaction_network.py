from __future__ import annotations

from pathlib import Path

import pytest

from chemworld.physchem import (
    RateLawSpec,
    ReactionNetworkSpec,
    ReactionSpec,
    SpeciesSpec,
    evaluate_rate_law,
    load_mechanism,
    parse_reaction_equation,
    perturb_network_parameters,
)


def test_parse_reaction_equation_and_stoichiometric_matrix() -> None:
    stoich, reversible = parse_reaction_equation("CO2 + H2 <=> CO + H2O")
    assert reversible
    assert stoich == {"CO2": -1.0, "H2": -1.0, "CO": 1.0, "H2O": 1.0}

    network = ReactionNetworkSpec(
        network_id="water_gas_shift",
        species=(
            SpeciesSpec("CO2", "CO2", phase="gas"),
            SpeciesSpec("H2", "H2", phase="gas"),
            SpeciesSpec("CO", "CO", phase="gas"),
            SpeciesSpec("H2O", "H2O", phase="gas"),
        ),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="wgs",
                equation="CO2 + H2 <=> CO + H2O",
                rate_law=RateLawSpec(
                    "wgs_reversible",
                    "reversible_arrhenius",
                    {"A": 0.1, "Ea_J_per_mol": 1000.0, "K_eq": 1.0},
                ),
            ),
        ),
    )

    assert network.species_ids == ("CO2", "H2", "CO", "H2O")
    assert network.reaction_ids == ("wgs",)
    assert network.stoichiometric_matrix() == ((-1.0,), (-1.0,), (1.0,), (1.0,))
    assert network.check_element_balance()


def test_element_balance_catches_impossible_reaction() -> None:
    with pytest.raises(ValueError, match="not element balanced"):
        ReactionNetworkSpec(
            network_id="bad_network",
            species=(
                SpeciesSpec("A", "H2"),
                SpeciesSpec("B", "O2"),
            ),
            reactions=(
                ReactionSpec.from_equation(
                    reaction_id="bad",
                    equation="A => B",
                    rate_law=RateLawSpec("bad_rate", "mass_action", {"k": 1.0}),
                ),
            ),
        )


def test_yaml_mechanism_loads_and_reproduces_batch_qualitative_behavior() -> None:
    network = load_mechanism("configs/mechanisms/simple_batch_reaction.yaml")
    assert network.network_id == "simple_batch_reaction"
    assert network.check_element_balance()
    assert len(network.species) == 7
    assert len(network.reactions) == 5

    short = network.integrate_batch(
        {"A": 1.0, "P": 0.0, "B": 0.0, "D": 0.0, "E": 0.0, "Cat_active": 0.01},
        volume_L=1.0,
        temperature_K=360.0,
        duration_s=1000.0,
    )
    long = network.integrate_batch(
        {"A": 1.0, "P": 0.0, "B": 0.0, "D": 0.0, "E": 0.0, "Cat_active": 0.01},
        volume_L=1.0,
        temperature_K=360.0,
        duration_s=20000.0,
    )

    assert short.final_amounts_mol["P"] > 0.0
    assert long.final_amounts_mol["D"] > short.final_amounts_mol["D"]
    assert long.final_amounts_mol["Cat_dead"] > short.final_amounts_mol["Cat_dead"]
    assert long.final_amounts_mol["A"] < short.final_amounts_mol["A"]


def test_rate_law_variants_return_finite_nonnegative_rates() -> None:
    concentrations = {"A": 1.0, "B": 0.5, "P": 0.2, "Cat": 0.01}
    reactions = (
        ReactionSpec.from_equation(
            reaction_id="mass_action",
            equation="A => B",
            rate_law=RateLawSpec("ma", "mass_action", {"k": 0.2}),
        ),
        ReactionSpec.from_equation(
            reaction_id="modified_arrhenius",
            equation="A => B",
            rate_law=RateLawSpec("arr", "modified_arrhenius", {"A": 0.2, "b": 0.5}),
        ),
        ReactionSpec.from_equation(
            reaction_id="catalytic",
            equation="A => B",
            rate_law=RateLawSpec(
                "cat",
                "catalytic_activity",
                {"A": 0.2, "catalyst_species": "Cat", "reference_concentration_mol_L": 0.01},
            ),
        ),
        ReactionSpec.from_equation(
            reaction_id="lh",
            equation="A + B => P",
            rate_law=RateLawSpec(
                "lh",
                "langmuir_hinshelwood",
                {"A": 0.2, "adsorption": {"A": 1.0, "B": 0.5}},
            ),
        ),
        ReactionSpec.from_equation(
            reaction_id="mm",
            equation="A => B",
            rate_law=RateLawSpec(
                "mm",
                "michaelis_menten",
                {"substrate": "A", "vmax": 0.4, "Km": 0.2},
            ),
        ),
    )

    rates = [
        evaluate_rate_law(reaction, concentrations_mol_L=concentrations, temperature_K=330.0)
        for reaction in reactions
    ]
    assert all(rate >= 0.0 for rate in rates)
    assert rates[-1] == pytest.approx(0.4 / 1.2)


def test_reversible_reaction_moves_toward_equilibrium_ratio() -> None:
    network = load_mechanism("configs/mechanisms/reversible_reaction.yaml")
    result = network.integrate_batch(
        {"A": 1.0, "B": 0.0},
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=20000.0,
    )
    ratio = result.final_amounts_mol["B"] / result.final_amounts_mol["A"]
    assert ratio == pytest.approx(4.0, rel=0.05)


def test_parameter_perturbation_is_deterministic() -> None:
    network = load_mechanism("configs/mechanisms/simple_batch_reaction.yaml")
    first = perturb_network_parameters(network, seed=123, relative_std=0.1)
    second = perturb_network_parameters(network, seed=123, relative_std=0.1)
    third = perturb_network_parameters(network, seed=456, relative_std=0.1)

    assert first.to_dict() == second.to_dict()
    assert first.to_dict() != third.to_dict()


def test_json_mechanism_loads(tmp_path: Path) -> None:
    mechanism_path = tmp_path / "simple.json"
    mechanism_path.write_text(
        """
        {
          "network_id": "json_isomerization",
          "species": [
            {"species_id": "A", "formula": "C2H4O2"},
            {"species_id": "B", "formula": "C2H4O2"}
          ],
          "reactions": [
            {
              "reaction_id": "r1",
              "equation": "A => B",
              "rate_law": {
                "rate_law_id": "r1_rate",
                "equation_id": "mass_action",
                "parameters": {"k": 0.1}
              }
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    network = load_mechanism(mechanism_path)
    assert network.network_id == "json_isomerization"
    assert network.check_element_balance()


def test_large_network_runs_deterministically() -> None:
    species = tuple(
        SpeciesSpec(f"S{i}", "H2", phase="gas")
        for i in range(20)
    )
    reactions = tuple(
        ReactionSpec.from_equation(
            reaction_id=f"r{i}",
            equation=f"S{i % 20} => S{(i + 1) % 20}",
            rate_law=RateLawSpec(f"k{i}", "mass_action", {"k": 0.001 + i * 1e-5}),
        )
        for i in range(30)
    )
    network = ReactionNetworkSpec("large_deterministic", species, reactions)

    result_a = network.integrate_batch(
        {"S0": 1.0},
        volume_L=1.0,
        temperature_K=300.0,
        duration_s=1000.0,
        evaluation_times_s=(0.0, 500.0, 1000.0),
    )
    result_b = network.integrate_batch(
        {"S0": 1.0},
        volume_L=1.0,
        temperature_K=300.0,
        duration_s=1000.0,
        evaluation_times_s=(0.0, 500.0, 1000.0),
    )

    assert result_a.to_dict() == result_b.to_dict()
    assert len(network.stoichiometric_matrix()) == 20
    assert len(network.stoichiometric_matrix()[0]) == 30
