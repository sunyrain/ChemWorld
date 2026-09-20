from __future__ import annotations

from pathlib import Path

import pytest
import scripts.run_work_ii_eq_entity_gate_v0_1 as eq_e

from chemworld.physchem.equilibrium_entity_panel import solve_equilibrium_entity


def test_eq_e_is_three_entities_under_one_fixed_topology() -> None:
    config = eq_e.load_config()
    eq_e.validate_design(config)
    entity_profiles = eq_e.profiles(config)

    assert config["prior_locus"] == "E"
    assert set(entity_profiles) == {"medium-0", "medium-1", "medium-2"}
    assert config["common_private_topology"]["mechanism_family"] == (
        "direct_free_ion_precipitation"
    )
    assert config["common_private_topology"]["aqueous_intermediate_present"] is False


def test_eq_e_identity_changes_response_without_changing_species_graph() -> None:
    config = eq_e.load_config()
    outputs = []
    for profile in eq_e.profiles(config).values():
        result = solve_equilibrium_entity(
            profile=profile,
            acid_total_mol=0.2 * 0.024,
            volume_L=0.024,
            base_pka=config["base_pka_nuisance"],
        )
        outputs.append((result.pH / 14.0, result.precipitation_signal))
        assert result.mechanism_family == "direct_free_ion_precipitation"
        assert result.aqueous_pair_mol_L == 0.0
        assert result.equilibrium_residual < 1.0e-8

    assert max(row[0] for row in outputs) - min(row[0] for row in outputs) > 0.03
    assert max(row[1] for row in outputs) - min(row[1] for row in outputs) > 0.03


def test_eq_e_scale_control_is_exact_before_observation_noise() -> None:
    config = eq_e.load_config()
    for profile in eq_e.profiles(config).values():
        small = solve_equilibrium_entity(
            profile=profile,
            acid_total_mol=0.02 * 0.024,
            volume_L=0.024,
            base_pka=config["base_pka_nuisance"],
        )
        large = solve_equilibrium_entity(
            profile=profile,
            acid_total_mol=0.02 * 0.048,
            volume_L=0.048,
            base_pka=config["base_pka_nuisance"],
        )
        assert small.pH == pytest.approx(large.pH, abs=1.0e-12)
        assert small.acid_dissociation_fraction == pytest.approx(
            large.acid_dissociation_fraction, abs=1.0e-12
        )
        assert small.precipitation_signal == pytest.approx(
            large.precipitation_signal, abs=1.0e-12
        )


def test_eq_e_public_arms_are_symmetric_and_do_not_leak_private_fields() -> None:
    config = eq_e.load_config()
    aligned = eq_e.public_prior(config, "Aligned")
    wrong = eq_e.public_prior(config, "MisIndexed")

    assert eq_e.public_prior(config, "Opaque") is None
    assert aligned is not None and wrong is not None
    assert aligned.keys() == wrong.keys()
    assert aligned != wrong
    text = str([aligned, wrong]).lower()
    for field in config["public_entity_dossier"]["forbidden_public_fields"]:
        assert field.lower() not in text


def test_eq_e_small_gate_passes_without_provider(tmp_path: Path) -> None:
    report = eq_e.run_gate(tmp_path / "gate")

    assert report["passed"] is True
    assert report["provider_calls"] == 0
    assert report["completed_executions"] == 45
    assert all(report["checks"].values())
