from math import log
from pathlib import Path

import pytest

from chemworld.eval.experiment_1_p_assets import (
    build_extractant_dossier,
    frozen_world_truths,
    load_asset_contract,
    matched_s_star_bands,
    partition_truth,
    structural_intervention,
)
from chemworld.physchem.crystallization_units import (
    CrystallizationKineticsSpec,
    _occlude_impurity,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
P_CONTRACT = ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json"


def test_p_asset_contract_has_five_distinct_executable_world_truths() -> None:
    contract = load_asset_contract(P_CONTRACT)
    truths = frozen_world_truths(contract)
    assert len(truths) == 5
    assert len({row["truth_sha256"] for row in truths}) == 5
    assert truths[1]["partition_coefficient_multiplier"] > 1.0
    assert truths[2]["partition_coefficient_multiplier"] < 1.0
    assert truths[3]["partition_phase_volume_multiplier"] < 1.0


def test_p_entity_dossier_misindex_is_symmetric_and_has_no_fixed_point() -> None:
    contract = load_asset_contract(P_CONTRACT)
    dossier = build_extractant_dossier(contract)
    assert dossier["permutation"] == [2, 0, 3, 1]
    assert all(index != source for index, source in enumerate(dossier["permutation"]))
    assert [set(row) for row in dossier["aligned"]] == [
        set(row) for row in dossier["misspecified"]
    ]
    assert dossier["aligned_sha256"] != dossier["misspecified_sha256"]


def test_p_s_star_bands_have_equal_log_width_and_shifted_centers() -> None:
    contract = load_asset_contract(P_CONTRACT)
    bands = matched_s_star_bands(contract)
    aligned = bands["aligned"]
    misspecified = bands["misspecified"]
    assert log(aligned["center"] / aligned["lower"]) == pytest.approx(
        log(misspecified["center"] / misspecified["lower"])
    )
    assert log(aligned["upper"] / aligned["center"]) == pytest.approx(
        log(misspecified["upper"] / misspecified["center"])
    )
    assert aligned["center"] != misspecified["center"]


def test_p_structural_family_is_executable_and_composition_dependent() -> None:
    contract = load_asset_contract(P_CONTRACT)
    intervention = structural_intervention(contract)
    scenario = get_scenario("reaction-to-purification")
    generator = DefaultScenarioGenerator()
    parent = generator.generate(scenario, 0)
    child = generator.generate(scenario, 0, (intervention,))
    assert "partition_composition_coupling_multiplier" not in parent.initial_state.metadata
    assert child.initial_state.metadata["partition_composition_coupling_multiplier"] == 4.0
    assert parent.parameters.world_id != child.parameters.world_id

    parent_product_rich = partition_truth(
        contract, extractant=2, product_mol=0.012, impurity_mol=0.002
    )
    parent_impurity_rich = partition_truth(
        contract, extractant=2, product_mol=0.006, impurity_mol=0.004
    )
    child_product_rich = partition_truth(
        contract,
        extractant=2,
        product_mol=0.012,
        impurity_mol=0.002,
        composition_coupling_multiplier=4.0,
    )
    child_impurity_rich = partition_truth(
        contract,
        extractant=2,
        product_mol=0.006,
        impurity_mol=0.004,
        composition_coupling_multiplier=4.0,
    )
    assert parent_product_rich["S_star"] == pytest.approx(parent_impurity_rich["S_star"])
    assert child_product_rich["S_star"] != pytest.approx(child_impurity_rich["S_star"])


def _kinetics(law_id: str) -> CrystallizationKineticsSpec:
    return CrystallizationKineticsSpec(
        model_id="test",
        primary_nucleation_coefficient_per_L_s=1.0,
        primary_nucleation_exponent=2.0,
        growth_coefficient_m_s=1.0e-8,
        growth_exponent=1.0,
        crystal_density_kg_m3=1200.0,
        target_molecular_weight_kg_mol=0.18,
        nucleus_diameter_m=8.0e-6,
        impurity_occlusion_mol_per_mol=0.02,
        supersaturation_occlusion_factor=0.5,
        impurity_occlusion_law_id=law_id,
        impurity_surface_half_saturation_mol_L=0.01,
        provenance_id="test",
    )


def test_c_structural_occlusion_laws_are_functionally_distinct_not_scalar() -> None:
    parent = _kinetics("linear_supersaturation_transfer_v1")
    child = _kinetics("surface_saturation_occlusion_v1")

    def ratio(impurity: float, supersaturation: float) -> float:
        parent_value = _occlude_impurity(
            0.001,
            relative_supersaturation=supersaturation,
            dissolved_impurity=impurity,
            solvent_volume_L=0.05,
            kinetics=parent,
        )
        child_value = _occlude_impurity(
            0.001,
            relative_supersaturation=supersaturation,
            dissolved_impurity=impurity,
            solvent_volume_L=0.05,
            kinetics=child,
        )
        return child_value / parent_value

    assert ratio(0.001, 0.2) != pytest.approx(ratio(0.004, 0.2))
    assert ratio(0.004, 0.2) != pytest.approx(ratio(0.004, 1.0))


def test_c_occlusion_axis_switches_executable_private_law_selector() -> None:
    scenario = get_scenario("reaction-to-crystallization")
    generator = DefaultScenarioGenerator()
    parent = generator.generate(scenario, 401)
    child = generator.generate(
        scenario,
        401,
        (
            {
                "axis_id": "crystallization.impurity-occlusion-law",
                "mode": "extrapolation",
                "severity": 1.0,
            },
        ),
    )
    assert "crystallization_impurity_occlusion_law_id" not in parent.initial_state.metadata
    assert (
        child.initial_state.metadata["crystallization_impurity_occlusion_law_id"]
        == "surface_saturation_occlusion_v1"
    )
    assert parent.parameters.world_id != child.parameters.world_id
