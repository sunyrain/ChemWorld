import json
from math import log
from pathlib import Path

import pytest
from scripts.author_experiment_1_c_structural_redesign_v1_2 import (
    _load_machine_contract,
)

from chemworld.eval.experiment_1_p_assets import (
    build_world_assets,
    frozen_world_truths,
    load_asset_contract,
    partition_truth,
    structural_intervention,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.physchem.crystallization_units import (
    CrystallizationKineticsSpec,
    _occlude_impurity,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
P_CONTRACT = ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json"
C_CONTRACT = ROOT / "configs/benchmark/experiment_1_c_structural_authoring_v1.2.1.json"
P_MANIFEST = (
    ROOT
    / "workstreams/flagship_tasks/experiment_1/systems/P/assets/"
    "P_ASSET_MANIFEST_V1_1_1.json"
)


def test_c_machine_contract_binds_frozen_design_and_sources() -> None:
    machine, benchmark = _load_machine_contract(C_CONTRACT)
    assert machine["source_binding"]["source_commit"] == (
        "f8c4ad96894d863c66f154a275ffce2466602ef0"
    )
    assert machine["scientific_constants"]["surface_saturation_max_loading_ratio"] == 4.0
    assert machine["scientific_constants"]["surface_half_saturation_mol_L"] == 0.010
    assert machine["tournament"]["planned_executions_total"] == 108
    assert benchmark["contract_id"] == "experiment-1-c-parametric-repair-v1.0.2"


def test_p_asset_manifest_is_self_hashed_source_bound_and_world_specific() -> None:
    manifest = json.loads(P_MANIFEST.read_text(encoding="utf-8"))
    expected = canonical_json_sha256(
        {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    )
    assert manifest["manifest_sha256"] == expected
    assert manifest["source_binding"]["source_commit"] == (
        "f8c4ad96894d863c66f154a275ffce2466602ef0"
    )
    assert all(
        file_sha256(ROOT / row["path"]) == row["sha256"]
        for row in manifest["source_binding"]["files"]
    )
    assets = manifest["world_assets"]
    assert [row["world_id"] for row in assets] == [f"P-W0{i}" for i in range(1, 6)]
    centers = {
        row["world_id"]: row["parametric_bands"]["aligned"]["center"] for row in assets
    }
    assert centers["P-W02"] != pytest.approx(centers["P-W01"])
    assert centers["P-W03"] != pytest.approx(centers["P-W01"])
    assert centers["P-W05"] != pytest.approx(centers["P-W01"])


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
    for asset in build_world_assets(contract):
        dossier = asset["entity_dossier"]
        assert dossier["world_id"] == asset["world_id"]
        assert dossier["permutation"] == [2, 0, 3, 1]
        assert all(index != source for index, source in enumerate(dossier["permutation"]))
        assert [set(row) for row in dossier["aligned"]] == [
            set(row) for row in dossier["misspecified"]
        ]
        assert dossier["aligned_sha256"] != dossier["misspecified_sha256"]


def test_p_s_star_bands_have_equal_log_width_and_shifted_centers() -> None:
    contract = load_asset_contract(P_CONTRACT)
    assets = build_world_assets(contract)
    for asset in assets:
        bands = asset["parametric_bands"]
        aligned = bands["aligned"]
        misspecified = bands["misspecified"]
        assert bands["world_id"] == asset["world_id"]
        assert log(aligned["center"] / aligned["lower"]) == pytest.approx(
            log(misspecified["center"] / misspecified["lower"])
        )
        assert log(aligned["upper"] / aligned["center"]) == pytest.approx(
            log(misspecified["upper"] / misspecified["center"])
        )
        assert aligned["center"] != misspecified["center"]
    centers = {
        asset["world_id"]: asset["parametric_bands"]["aligned"]["center"]
        for asset in assets
    }
    assert centers["P-W02"] != pytest.approx(centers["P-W01"])
    assert centers["P-W03"] != pytest.approx(centers["P-W01"])
    assert centers["P-W05"] != pytest.approx(centers["P-W01"])


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


@pytest.mark.parametrize(
    ("mode", "severity"),
    (("interpolation", 1.0), ("extrapolation", 0.5), ("composition", 1.0)),
)
def test_c_occlusion_law_axis_rejects_nonbinary_interventions(
    mode: str, severity: float
) -> None:
    scenario = get_scenario("reaction-to-crystallization")
    with pytest.raises(ValueError, match=r"does not support|frozen binary axis"):
        DefaultScenarioGenerator().generate(
            scenario,
            401,
            (
                {
                    "axis_id": "crystallization.impurity-occlusion-law",
                    "mode": mode,
                    "severity": severity,
                },
            ),
        )


def test_c_scalar_null_axis_sets_only_constant_capacity_multiplier() -> None:
    scenario = get_scenario("reaction-to-crystallization")
    child = DefaultScenarioGenerator().generate(
        scenario,
        401,
        (
            {
                "axis_id": "crystallization.impurity-occlusion-capacity",
                "mode": "extrapolation",
                "severity": 0.6,
            },
        ),
    )
    assert child.initial_state.metadata[
        "crystallization_impurity_occlusion_capacity_multiplier"
    ] == pytest.approx(4.0)
    assert "crystallization_impurity_occlusion_law_id" not in child.initial_state.metadata


@pytest.mark.parametrize("severity", (0.25, 0.5, 0.999))
def test_c_mechanism_occlusion_law_path_rejects_nonbinary_severity(
    severity: float,
) -> None:
    scenario = get_scenario("reaction-to-crystallization")
    intervention = {
        "kind": "mechanism_family",
        "mode": "constitutive_law_family",
        "severity": severity,
        "constitutive_law_change": {
            "transform_id": "crystallization_occlusion_response_stress_v1",
            "occlusion_law_selector_at_full_severity": 2.0,
        },
    }
    with pytest.raises(ValueError, match="requires severity 1"):
        DefaultScenarioGenerator().generate(scenario, 401, (intervention,))
