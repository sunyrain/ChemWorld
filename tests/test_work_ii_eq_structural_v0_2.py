from __future__ import annotations

import copy
from pathlib import Path

import pytest
import scripts.run_work_ii_eq_structural_v0_2 as eq

from chemworld.physchem.equilibrium_mechanism import (
    solve_coupled_weak_acid_precipitation,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def valid_eqs(family: str = "direct_free_ion_precipitation") -> dict:
    ion_pair = family == "aqueous_ion_pair_intermediate"
    equations = ["acid_dissociation", "free_ion_solid_equilibrium"]
    if ion_pair:
        equations.append("aqueous_ion_pair_association")
    return {
        "network_family": family,
        "aqueous_intermediate": "present" if ion_pair else "absent",
        "selected_equation_ids": equations,
        "rationale": "The concentration and dilution contrasts support this reaction network.",
        "cited_source_batches": [2, 7, 11],
    }


def test_solver_registers_distinct_mass_conserving_networks() -> None:
    direct = solve_coupled_weak_acid_precipitation(
        acid_total_mol=0.012,
        volume_L=0.024,
        pka=4.839404789086824,
        log10_ksp=-5.2,
        mechanism_family="direct_free_ion_precipitation",
    )
    paired = solve_coupled_weak_acid_precipitation(
        acid_total_mol=0.012,
        volume_L=0.024,
        pka=4.839404789086824,
        log10_ksp=-5.2,
        mechanism_family="aqueous_ion_pair_intermediate",
        association_beta_L_per_mol=6000.0,
    )

    assert direct.aqueous_pair_mol_L == 0.0
    assert paired.aqueous_pair_mol_L > 0.0
    assert direct.equilibrium_residual < 1.0e-8
    assert paired.equilibrium_residual < 1.0e-8
    assert paired.precipitation_signal != pytest.approx(
        direct.precipitation_signal
    )


def test_solver_is_scale_invariant_at_fixed_concentration() -> None:
    small = solve_coupled_weak_acid_precipitation(
        acid_total_mol=0.0003,
        volume_L=0.012,
        pka=5.019404789086824,
        log10_ksp=-5.2,
        mechanism_family="direct_free_ion_precipitation",
    )
    large = solve_coupled_weak_acid_precipitation(
        acid_total_mol=0.0018,
        volume_L=0.072,
        pka=5.019404789086824,
        log10_ksp=-5.2,
        mechanism_family="direct_free_ion_precipitation",
    )

    assert small.pH == pytest.approx(large.pH, abs=1.0e-10)
    assert small.acid_dissociation_fraction == pytest.approx(
        large.acid_dissociation_fraction, abs=1.0e-10
    )
    assert small.precipitation_signal == pytest.approx(
        large.precipitation_signal, abs=1.0e-10
    )


def test_design_is_five_world_three_arm_mechanism_characterization() -> None:
    config = eq.load_config()
    validated = eq.validate_design(config)

    assert config["prior_locus"] == "S"
    assert config["objective"] == "balanced"
    assert config["posttest_stages"] == ["K1", "Q", "K2", "EQS"]
    assert len(config["worlds"]) == 5
    assert len(validated["schedule"]) == 15
    assert len(eq.queries(config)) == 12
    assert all(
        [action["operation"] for action in query["actions"]]
        == ["add_solvent", "add_reagent", "terminate", "measure"]
        for query in eq.queries(config)
    )
    for world in config["worlds"]:
        world_id = world["world_id"]
        assert eq.public_prior(config, world_id, "Opaque") is None
        aligned = eq.public_prior(config, world_id, "Aligned")
        misindexed = eq.public_prior(config, world_id, "MisIndexed")
        assert aligned is not None and misindexed is not None
        assert aligned.keys() == misindexed.keys()
        assert aligned["network_family"] != misindexed["network_family"]


def test_repaired_worlds_share_ksp_and_use_registered_pair_strengths() -> None:
    config = eq.load_config()
    worlds = {row["world_id"]: row for row in config["worlds"]}

    assert {row["private_authoring"]["log10_ksp_nuisance"] for row in worlds.values()} == {
        -5.2
    }
    assert worlds["EQ-S-W02"]["private_authoring"][
        "aqueous_association_beta_L_per_mol"
    ] == 6000.0
    assert worlds["EQ-S-W04"]["private_authoring"][
        "aqueous_association_beta_L_per_mol"
    ] == 8000.0


def test_registered_interventions_compile_expected_hidden_topologies() -> None:
    config = eq.load_config()
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("equilibrium-characterization")
    for world in config["worlds"]:
        interventions = tuple(world["world_interventions"])
        instance = generator.generate(scenario, int(world["world_seed"]), interventions)
        metadata = instance.initial_state.metadata
        private = world["private_authoring"]
        assert metadata["equilibrium_mechanism_benchmark_version"] == "eq-s-v0.2"
        assert metadata["equilibrium_mechanism_family"] == private["mechanism_family"]
        assert metadata["hidden_equilibrium_log10_ksp"] == -5.2
        expected_beta = private["aqueous_association_beta_L_per_mol"]
        if expected_beta is None:
            assert "equilibrium_aqueous_association_beta_L_per_mol" not in metadata
        else:
            assert metadata["equilibrium_aqueous_association_beta_L_per_mol"] == expected_beta


def test_eqs_validation_and_scoring_are_fail_closed() -> None:
    direct = valid_eqs()
    ion = valid_eqs("aqueous_ion_pair_intermediate")
    assert eq.validate_posttest("EQS", direct, ())["valid"]
    assert eq.validate_posttest("EQS", ion, ())["valid"]
    assert eq.evaluate_eqs(ion, "aqueous_ion_pair_intermediate")[
        "network_family_correct"
    ]

    contradictory = copy.deepcopy(direct)
    contradictory["selected_equation_ids"].append("aqueous_ion_pair_association")
    assert not eq.validate_posttest("EQS", contradictory, ())["valid"]

    non_english = copy.deepcopy(direct)
    non_english["rationale"] = "中文"
    assert not eq.validate_posttest("EQS", non_english, ())["valid"]


def test_freeze_fails_closed_before_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = eq.load_config()
    gate = tmp_path / "provider-free-gate" / "gate.json"
    eq.write(gate, {"passed": True, "config_sha256": eq.file_sha256(eq.CONFIG)})
    monkeypatch.setattr(eq.eq_v2, "FREEZE", tmp_path / "absent.json")

    with pytest.raises(RuntimeError, match="freeze manifest is absent"):
        eq.eq_v2.validate_freeze(tmp_path, config)
