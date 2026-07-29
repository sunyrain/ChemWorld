from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest
from scripts.run_static_optimization_s0 import _DeterministicStaticMockClient

from chemworld.agents.electrochemical_single_stage import (
    electrochemical_single_stage_parameters_from_unit_vector,
)
from chemworld.agents.static_optimization import StaticOptimizationAgent
from chemworld.envs.reports import build_evaluator_provenance, sanitize_agent_info
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
    build_static_optimization_agent,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)
from chemworld.foundation import equipment_settings
from chemworld.materials import (
    CRYSTALLIZATION_STATIC_MATERIAL_INFORMATION_VERSION,
    STATIC_MATERIAL_INFORMATION_MISINDEXED,
    STATIC_MATERIAL_INFORMATION_NOMINAL,
    STATIC_MATERIAL_INFORMATION_OPAQUE,
    STATIC_MATERIAL_INFORMATION_SHUFFLED,
    normalize_static_material_information_config,
    static_material_information_dossier,
)
from chemworld.tasks import get_task
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
)
from chemworld.world.electrochemical_material_family import (
    LEGACY_ELECTROCHEMICAL_MATERIAL_FAMILY,
    NOMINAL_PRIOR_MATERIAL_FAMILY,
    electrochemical_material_family,
)
from chemworld.world.parameters import load_chemworld_parameters


def _property_rows(dossier: dict[str, object], field: str) -> list[dict[str, float]]:
    choices = dossier["choices"]
    assert isinstance(choices, dict)
    return [item["nominal_properties"] for item in choices[field]]


def test_opaque_material_condition_preserves_existing_public_context() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="opaque-material-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=9000,
    )
    agent.reset(task_info, 0)

    context = agent.public_context([])

    assert "material_information" not in context["experiment_interface"]
    assert agent.manifest()["material_information_condition"] == (
        STATIC_MATERIAL_INFORMATION_OPAQUE
    )
    assert agent.manifest()["material_information_sha256"] is None


def test_nominal_dossier_is_anonymous_partial_and_runtime_synchronized() -> None:
    dossier = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id="electrochemical-conversion",
        material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )

    assert dossier is not None
    serialized = json.dumps(dossier, sort_keys=True).lower()
    for real_name in ("water", "ethanol", "acetonitrile", "toluene"):
        assert real_name not in serialized
    assert "faradaic_efficiency_multiplier" not in serialized
    assert "product_selectivity_multiplier" not in serialized
    assert "faradaic_efficiency_factor" not in serialized
    assert "product_selectivity_factor" not in serialized
    electrolyte_rows = _property_rows(dossier, "electrolyte_profile")
    solvent_rows = _property_rows(dossier, "solvent")
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)
    assert [row["bulk_conductivity_S_m"] for row in electrolyte_rows] == [
        item["electrolyte_conductivity_S_m"] for item in family.electrolyte_profiles
    ]
    assert [row["relative_diffusivity"] for row in solvent_rows] == [
        item["diffusivity_multiplier"] for item in family.solvent_profiles
    ]


def test_shuffled_dossier_is_a_blind_derangement_with_the_same_property_rows() -> None:
    nominal = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id="electrochemical-conversion",
        material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )
    shuffled = static_material_information_dossier(
        {
            "mode": STATIC_MATERIAL_INFORMATION_SHUFFLED,
            "descriptor_permutation": {
                "electrolyte_profile": [2, 3, 1, 0],
                "solvent": [1, 3, 0, 2],
            },
        },
        task_id="electrochemical-conversion",
        material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )

    assert nominal is not None and shuffled is not None
    assert "shuffled" not in json.dumps(shuffled, sort_keys=True).lower()
    for field in ("electrolyte_profile", "solvent"):
        nominal_rows = _property_rows(nominal, field)
        shuffled_rows = _property_rows(shuffled, field)
        assert all(left != right for left, right in zip(nominal_rows, shuffled_rows, strict=True))
        assert sorted(map(json.dumps, nominal_rows)) == sorted(map(json.dumps, shuffled_rows))


def test_electrochemical_misindexed_dossier_swaps_only_the_target_rows_blindly() -> None:
    nominal = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id="electrochemical-conversion",
        material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )
    misindexed = static_material_information_dossier(
        {
            "mode": STATIC_MATERIAL_INFORMATION_MISINDEXED,
            "target_field": "electrolyte_profile",
            "descriptor_permutation": [0, 3, 2, 1],
        },
        task_id="electrochemical-conversion",
        material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )

    assert nominal is not None and misindexed is not None
    serialized = json.dumps(misindexed, sort_keys=True).lower()
    for private_term in ("misindexed", "permutation", "target_field", "shuffled"):
        assert private_term not in serialized
    nominal_electrolytes = _property_rows(nominal, "electrolyte_profile")
    misindexed_electrolytes = _property_rows(misindexed, "electrolyte_profile")
    assert misindexed_electrolytes == [
        nominal_electrolytes[0],
        nominal_electrolytes[3],
        nominal_electrolytes[2],
        nominal_electrolytes[1],
    ]
    assert _property_rows(misindexed, "solvent") == _property_rows(
        nominal,
        "solvent",
    )


def test_crystallization_misindexed_dossier_swaps_only_the_target_rows_blindly() -> None:
    nominal = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id="reaction-to-crystallization",
        material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    misindexed = static_material_information_dossier(
        {
            "mode": STATIC_MATERIAL_INFORMATION_MISINDEXED,
            "target_field": "catalyst",
            "descriptor_permutation": [0, 2, 1, 3],
        },
        task_id="reaction-to-crystallization",
        material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )

    assert nominal is not None and misindexed is not None
    serialized = json.dumps(misindexed, sort_keys=True).lower()
    for private_term in ("misindexed", "permutation", "target_field", "shuffled"):
        assert private_term not in serialized
    nominal_catalysts = _property_rows(nominal, "catalyst")
    misindexed_catalysts = _property_rows(misindexed, "catalyst")
    assert misindexed_catalysts == [
        nominal_catalysts[0],
        nominal_catalysts[2],
        nominal_catalysts[1],
        nominal_catalysts[3],
    ]
    assert _property_rows(misindexed, "solvent") == _property_rows(
        nominal,
        "solvent",
    )


@pytest.mark.parametrize(
    ("task_id", "family_id", "target_field", "permutation", "message"),
    [
        (
            "electrochemical-conversion",
            NOMINAL_PRIOR_MATERIAL_FAMILY,
            "catalyst",
            [0, 3, 2, 1],
            "target_field",
        ),
        (
            "electrochemical-conversion",
            NOMINAL_PRIOR_MATERIAL_FAMILY,
            "electrolyte_profile",
            [0, 1, 2, 3],
            "two-row transposition",
        ),
        (
            "reaction-to-crystallization",
            REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
            "catalyst",
            [1, 2, 0, 3],
            "two-row transposition",
        ),
    ],
)
def test_misindexed_information_rejects_non_targeted_mappings(
    task_id: str,
    family_id: str,
    target_field: str,
    permutation: list[int],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        normalize_static_material_information_config(
            {
                "mode": STATIC_MATERIAL_INFORMATION_MISINDEXED,
                "target_field": target_field,
                "descriptor_permutation": permutation,
            },
            task_ids=(task_id,),
            material_family_id=family_id,
        )


def test_nominal_material_context_and_audit_are_hashed() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="nominal-material-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=12000,
        material_information={"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    )
    agent.reset(task_info, 0)

    context = agent.public_context([])
    agent.plan_next([])
    manifest = agent.manifest()
    audit = agent.decision_audit()

    assert "material_information" in context["experiment_interface"]
    assert manifest["material_information_condition"] == (STATIC_MATERIAL_INFORMATION_NOMINAL)
    assert manifest["material_information_sha256"]
    assert audit is not None
    assert audit["material_information_condition"] == (STATIC_MATERIAL_INFORMATION_NOMINAL)
    assert audit["material_information_sha256"] == manifest["material_information_sha256"]


def test_nominal_material_information_fails_closed_outside_audited_family() -> None:
    with pytest.raises(ValueError, match="latent material family"):
        normalize_static_material_information_config(
            {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
            task_ids=("reaction-to-crystallization",),
            material_family_id=None,
        )

    with pytest.raises(ValueError, match="requires the nominal-prior"):
        normalize_static_material_information_config(
            {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
            task_ids=("electrochemical-conversion",),
            material_family_id=LEGACY_ELECTROCHEMICAL_MATERIAL_FAMILY,
        )

    root = Path(__file__).resolve().parents[1]
    protocol = json.loads(
        (
            root
            / "configs"
            / "benchmark"
            / "scientific_optimization_s0_v0.5_crystallization_high_20_formal.json"
        ).read_text(encoding="utf-8")
    )
    invalid = copy.deepcopy(protocol)
    invalid["material_information"] = {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL}
    with pytest.raises(ValueError, match="latent material family"):
        validate_static_optimization_protocol(invalid)


def test_crystallization_nominal_dossier_is_anonymous_partial_and_audited() -> None:
    dossier = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id="reaction-to-crystallization",
        material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )

    assert dossier is not None
    assert dossier["contract_version"] == (
        CRYSTALLIZATION_STATIC_MATERIAL_INFORMATION_VERSION
    )
    assert set(dossier["choices"]) == {"catalyst", "solvent"}
    assert len(dossier["choices"]["catalyst"]) == 4
    assert len(dossier["choices"]["solvent"]) == 4
    serialized = json.dumps(dossier, sort_keys=True).lower()
    for private_term in (
        "reaction_multipliers",
        "residual_generator",
        "family_sha256",
        "world_id",
        "leaderboard_score",
        "optimal_recipe",
    ):
        assert private_term not in serialized
    catalyst_fields = set(
        dossier["choices"]["catalyst"][0]["nominal_properties"]
    )
    solvent_fields = set(
        dossier["choices"]["solvent"][0]["nominal_properties"]
    )
    assert {
        "reference_panel_activity_geomean",
        "reference_panel_activity_floor",
        "reference_panel_activity_ceiling",
        "reference_panel_log_variability",
    } == catalyst_fields
    assert {
        "relative_solubility",
        "relative_nucleation_tendency",
        "relative_crystal_growth",
        "relative_impurity_occlusion",
    }.issubset(solvent_fields)


def test_crystallization_nominal_protocol_reaches_the_participant_context() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = json.loads(
        (
            root
            / "configs"
            / "benchmark"
            / "scientific_optimization_s0_v1.0_crystallization_material_opaque_20x10_formal.json"
        ).read_text(encoding="utf-8")
    )
    methods = json.loads(
        (
            root
            / "configs"
            / "methods"
            / "llm_v1.0"
            / (
                "participant_methods_s0_codex_subscription_sol_"
                "crystallization_material_opaque_20x10_v10.json"
            )
        ).read_text(encoding="utf-8")
    )
    protocol["material_information"] = {
        "mode": STATIC_MATERIAL_INFORMATION_NOMINAL
    }
    validate_static_optimization_protocol(protocol)
    agent = build_static_optimization_agent(
        protocol,
        "reaction-to-crystallization",
        llm_methods=methods,
        method_id=protocol["method_ids"][0],
        client=_DeterministicStaticMockClient(),
    )

    material_information = agent.public_context([])["experiment_interface"][
        "material_information"
    ]
    assert material_information["contract_version"] == (
        CRYSTALLIZATION_STATIC_MATERIAL_INFORMATION_VERSION
    )
    assert agent.manifest()["hidden_world_fields_supplied"] is False
    assert agent.manifest()["material_information_sha256"]


def test_protocol_condition_reaches_the_built_agent() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = json.loads(
        (
            root
            / "configs"
            / "benchmark"
            / "scientific_optimization_s0_v0.4.1_single_stage_high_20_formal.json"
        ).read_text(encoding="utf-8")
    )
    methods = json.loads(
        (
            root
            / "configs"
            / "methods"
            / "llm_v0.4"
            / "participant_methods_s0_wellau_codex_sol_high_single_stage_20_v041.json"
        ).read_text(encoding="utf-8")
    )
    protocol["world_policy"]["electrochemical_material_family_id"] = NOMINAL_PRIOR_MATERIAL_FAMILY
    protocol["reward_contract"] = {
        "scoring_contract_id": "electrochemical-s0-balanced-efficiency-v2"
    }
    protocol["material_information"] = {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL}
    method_id = protocol["method_ids"][0]

    agent = build_static_optimization_agent(
        protocol,
        "electrochemical-conversion",
        llm_methods=methods,
        method_id=method_id,
        client=_DeterministicStaticMockClient(),
    )

    assert agent.manifest()["material_information_condition"] == (
        STATIC_MATERIAL_INFORMATION_NOMINAL
    )
    assert "material_information" in agent.public_context([])["experiment_interface"]
    scoring = agent.public_context([])["optimization_contract"]["scoring_contract"]
    assert scoring["contract_id"] == "electrochemical-s0-balanced-efficiency-v2"
    assert "reaction_score" not in scoring["component_weights"]


def _electrochemical_plan(electrolyte: int, solvent: int):
    parameters = electrochemical_single_stage_parameters_from_unit_vector(
        np.asarray(
            [
                (electrolyte + 0.5) / 4.0,
                (solvent + 0.5) / 4.0,
                0.5,
                0.55,
                0.55,
                0.5,
            ],
            dtype=float,
        )
    )
    from chemworld.agents.static_optimization import StaticOptimizationPlan

    return StaticOptimizationPlan(
        experiment_intent="test one material pair under fixed cell geometry",
        search_vector=tuple(
            float(value)
            for value in (
                (electrolyte + 0.5) / 4.0,
                (solvent + 0.5) / 4.0,
                0.5,
                0.55,
                0.55,
                0.5,
            )
        ),
        requested_measurement_slots=(
            "diagnostic-01-ph_meter",
            "diagnostic-02-uvvis",
        ),
        measurement_objective="measure the material response",
        expected_effect="materials may change response but not cell geometry",
        uncertainty=0.5,
        recipe_parameters=parameters,
    )


def test_new_family_geometry_is_world_fixed_not_material_specific() -> None:
    settings = []
    for electrolyte, solvent in ((0, 0), (3, 2)):
        with StaticOptimizationExperimentSession(
            task_id="electrochemical-conversion",
            seed=7,
            experiment_horizon=1,
            electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        ) as session:
            parameters = _electrochemical_plan(electrolyte, solvent).recipe_parameters
            assert parameters is not None
            for action in (
                {
                    "operation": "add_solvent",
                    "volume_L": 0.025,
                    "solvent": solvent,
                },
                {
                    "operation": "add_reagent",
                    "amount_mol": parameters["reagent_amount_mol"],
                },
                {
                    "operation": "set_potential",
                    "potential_V": parameters["potential_V"],
                    "current_mA": parameters["current_mA"],
                    "electrolyte_profile": electrolyte,
                },
            ):
                session.environment.step(action)
            cell = equipment_settings(
                session.environment._state.equipment,
                "electrochemical_cell",
            )
            settings.append(
                (
                    cell["electrode_gap_m"],
                    cell["electrode_area_m2"],
                    cell["contact_resistance_ohm"],
                )
            )

    assert settings[0] == settings[1]


def test_world_geometry_and_material_residuals_are_reproducible_and_seeded() -> None:
    first = load_chemworld_parameters("public-test", 3)
    repeat = load_chemworld_parameters("public-test", 3)
    other = load_chemworld_parameters("public-test", 4)

    geometry_fields = (
        "electrochemical_electrode_gap_m",
        "electrochemical_electrode_area_m2",
        "electrochemical_base_contact_resistance_ohm",
    )
    assert tuple(getattr(first, field) for field in geometry_fields) == tuple(
        getattr(repeat, field) for field in geometry_fields
    )
    assert tuple(getattr(first, field) for field in geometry_fields) != tuple(
        getattr(other, field) for field in geometry_fields
    )
    assert np.array_equal(
        first.electrochemical_electrolyte_effects,
        repeat.electrochemical_electrolyte_effects,
    )
    assert not np.array_equal(
        first.electrochemical_electrolyte_effects,
        other.electrochemical_electrolyte_effects,
    )
    for matrix in (
        first.electrochemical_electrolyte_effects,
        first.electrochemical_solvent_effects,
    ):
        assert matrix.shape == (4, 7)
        assert np.all(matrix >= 0.72)
        assert np.all(matrix <= 1.40)
    for residuals in (
        first.electrochemical_electrolyte_potential_residual_V,
        first.electrochemical_solvent_potential_residual_V,
    ):
        assert residuals.shape == (4,)
        assert np.all(np.abs(residuals) <= 0.08)
    assert 20.0 <= first.electrochemical_exchange_current_density_A_m2 <= 40.0
    assert first.electrochemical_exchange_current_density_A_m2 != (
        other.electrochemical_exchange_current_density_A_m2
    )


def test_material_family_profiles_are_deeply_immutable_and_instance_fingerprint_is_private(
) -> None:
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)
    with pytest.raises(TypeError):
        family.electrolyte_profiles[0]["electrolyte_conductivity_S_m"] = 1.0
    with StaticOptimizationExperimentSession(
        task_id="electrochemical-conversion",
        seed=11,
        experiment_horizon=1,
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
    ) as session:
        audit = build_evaluator_provenance(session.environment)
        assert audit["electrochemical_material_instance_sha256"]
        assert "electrochemical_material_instance_sha256" not in json.dumps(
            sanitize_agent_info(audit)
        )


def test_material_family_qualification_report_matches_frozen_family() -> None:
    root = Path(__file__).resolve().parents[1]
    report = json.loads(
        (
            root
            / "workstreams/flagship_tasks/reports/"
            "static-s0-material-family-v2-qualification-v0.3.json"
        ).read_text(encoding="utf-8")
    )
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)

    assert report["formal_result"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["material_family"]["family_sha256"] == family.family_sha256
    assert report["qualification_cohort_id"] == "public-qualification-q-v1"
    assert report["world_seeds"] == list(range(100, 115))
    assert report["summary"]["world_count"] == 15
    assert report["search_contract"] == {
        "material_pair_count": 16,
        "initial_continuous_design_count_per_pair": 36,
        "local_refinement_count_per_pair": 8,
        "validation_replicates_per_pair": 5,
        "standardized_mechanistic_probe_count_per_world": 16,
        "continuous_design": "scrambled_sobol_plus_four_fixed_anchors",
        "refinement": "bounded_gaussian_around_pair_incumbent",
        "observation_noise": "keyed_local_simulation",
    }
    assert report["qualification_pass"] is all(
        report["summary"]["qualification_checks"].values()
    )
    assert set(report["source_contract_sha256"]) == {
        "scripts/qualify_electrochemical_material_family.py",
        "src/chemworld/runtime/electrochemical_services.py",
        "src/chemworld/runtime/observation_services.py",
        "src/chemworld/world/electrochemical_material_family.py",
        "src/chemworld/world/parameters.py",
        "src/chemworld/world/scoring.py",
    }
