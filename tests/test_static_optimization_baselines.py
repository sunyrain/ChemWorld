from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from chemworld.eval.static_optimization_baselines import (
    BaselineObservation,
    aggregate_baseline_cells,
    make_optimizer,
    plan_from_baseline_decision,
    run_baseline_cell,
)
from chemworld.eval.static_optimization_execution import (
    static_optimization_workflow_mode,
)
from chemworld.eval.static_optimization_protocol import (
    static_optimization_material_family_id,
)
from chemworld.tasks import get_task
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
)
from chemworld.world.electrochemical_material_family import (
    NOMINAL_PRIOR_MATERIAL_FAMILY,
)
from chemworld.world.scoring import CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/scientific_optimization_s0_v0.3_classic_baselines_20_dev.json"
SINGLE_STAGE_PROTOCOL = (
    ROOT
    / "configs/benchmark/scientific_optimization_s0_v0.4_single_stage_classic_baselines_20.json"
)
CRYSTALLIZATION_PROTOCOL = (
    ROOT
    / "configs/benchmark/"
    "scientific_optimization_s0_v0.5_crystallization_classic_baselines_20.json"
)


def test_baseline_protocol_uses_terminal_score_not_reward_delta() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    reward = protocol["reward_contract"]
    assert reward["optimization_feedback"] == "terminal_summary.leaderboard_score"
    assert reward["fresh_measurement_score_delta_used"] is False
    assert reward["safety_is_separate_from_primary_reward"] is True


def test_all_baseline_optimizers_emit_bounded_complete_recipe_vectors() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    for algorithm_id, configuration in protocol["algorithms"].items():
        optimizer = make_optimizer(
            algorithm_id=algorithm_id,
            task_info=task_info,
            horizon=20,
            seed=0,
            configuration=configuration,
            electrochemical_material_family_id=(static_optimization_material_family_id(protocol)),
            electrochemical_workflow_mode=workflow_mode,
        )
        decision = optimizer.propose()
        vector = np.asarray(decision.vector, dtype=float)
        assert vector.shape == (9,)
        assert np.all(vector >= 0.0)
        assert np.all(vector <= 1.0)


def test_optimizer_feedback_is_terminal_score() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    optimizer = make_optimizer(
        algorithm_id="random",
        task_info=task_info,
        horizon=2,
        seed=0,
        configuration=protocol["algorithms"]["random"],
        electrochemical_material_family_id=(static_optimization_material_family_id(protocol)),
        electrochemical_workflow_mode=workflow_mode,
    )
    decision = optimizer.propose()
    plan = plan_from_baseline_decision(
        decision,
        algorithm_id="random",
        task_info=task_info,
        electrochemical_workflow_mode=workflow_mode,
    )
    optimizer.observe(
        BaselineObservation(
            experiment_index=0,
            vector=decision.vector,
            score=0.42,
            peak_safety_risk=0.11,
            plan=plan,
        )
    )
    assert optimizer.best_observation().score == 0.42
    assert optimizer.resource_usage()["model_call_count"] == 0


def test_short_random_baseline_cell_completes_and_validates() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    protocol["horizon"] = 2
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1
    cell = run_baseline_cell(
        protocol=protocol,
        algorithm_id="random",
        algorithm_seed=0,
    )
    assert cell["cell_status"] == "completed"
    assert cell["method_config_sha256"] != cell["protocol_sha256"]
    assert cell["completed_experiment_count"] == 2
    assert cell["completed_validation_experiment_count"] == 2
    assert cell["resources"]["model_call_count"] == 0
    assert cell["final_synthesis"]["recommendation"]["recommendation_type"] == "tested"
    aggregate = aggregate_baseline_cells([cell])["algorithms"][0]
    assert aggregate["first_score"]["mean"] == cell["scores"][0]
    assert aggregate["best_so_far_area_under_curve"]["mean"] >= cell["scores"][0]


def test_crystallization_baseline_uses_ten_dimensional_recipe() -> None:
    protocol = json.loads(CRYSTALLIZATION_PROTOCOL.read_text(encoding="utf-8"))
    protocol["world_policy"]["crystallization_material_family_id"] = (
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY
    )
    protocol["reward_contract"]["scoring_contract_id"] = (
        CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1
    )
    protocol["horizon"] = 2
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1

    cell = run_baseline_cell(
        protocol=protocol,
        algorithm_id="random",
        algorithm_seed=0,
    )

    assert cell["cell_status"] == "completed"
    plan = cell["experiments"][0]["result"]["plan"]
    assert len(plan["search_vector"]) == 10
    assert set(plan["recipe_parameters"]) == {
        "reaction_temperature_K",
        "reaction_duration_s",
        "reagent_amount_mol",
        "stirring_speed_rpm",
        "catalyst",
        "catalyst_amount_mol",
        "solvent",
        "seed_mass_g",
        "crystallization_temperature_K",
        "crystallization_duration_s",
    }


def test_descriptor_and_one_hot_bo_share_initial_design_but_not_encoding() -> None:
    protocol = json.loads(SINGLE_STAGE_PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    shared = {
        "family": "gaussian_process_expected_improvement",
        "n_initial": 4,
        "n_candidates": 128,
        "local_candidate_fraction": 0.5,
        "local_candidate_scale": 0.12,
    }
    one_hot = make_optimizer(
        algorithm_id="structured_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=3,
        configuration={
            **shared,
            "categorical_surrogate_encoding": "nominal_one_hot",
        },
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )
    descriptor = make_optimizer(
        algorithm_id="descriptor_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=3,
        configuration={
            **shared,
            "categorical_surrogate_encoding": "nominal_properties",
        },
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )

    assert np.array_equal(one_hot.initial_design, descriptor.initial_design)
    vector = np.full(6, 0.5)
    assert one_hot._model_vector(vector).shape == (12,)
    assert descriptor._model_vector(vector).shape == (21,)
    manifest = descriptor.manifest()
    assert manifest["material_information_condition"] == ("anonymous_nominal_properties")
    assert manifest["material_information_sha256"]
    descriptor_fields = {
        field for fields in manifest["descriptor_fields_by_coordinate"].values() for field in fields
    }
    assert "bulk_conductivity_S_m" in descriptor_fields
    assert "relative_diffusivity" in descriptor_fields
    assert "faradaic_efficiency_factor" not in descriptor_fields
    assert "product_selectivity_factor" not in descriptor_fields


def test_short_descriptor_gp_cell_completes_with_nominal_manifest() -> None:
    protocol = json.loads(SINGLE_STAGE_PROTOCOL.read_text(encoding="utf-8"))
    protocol["world_policy"]["electrochemical_material_family_id"] = NOMINAL_PRIOR_MATERIAL_FAMILY
    protocol["reward_contract"]["scoring_contract_id"] = (
        "electrochemical-s0-balanced-efficiency-v2"
    )
    protocol["horizon"] = 2
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1
    protocol["algorithms"] = {
        "descriptor_gp_ei": {
            "family": "gaussian_process_expected_improvement",
            "categorical_surrogate_encoding": "nominal_properties",
            "n_initial": 2,
            "n_candidates": 128,
            "local_candidate_fraction": 0.5,
            "local_candidate_scale": 0.12,
        }
    }

    cell = run_baseline_cell(
        protocol=protocol,
        algorithm_id="descriptor_gp_ei",
        algorithm_seed=0,
    )

    assert cell["cell_status"] == "completed"
    assert cell["agent_manifest"]["categorical_surrogate_encoding"] == ("nominal_properties")
    assert cell["agent_manifest"]["material_information_sha256"]


def test_telemetry_rf_receives_only_public_processed_measurements() -> None:
    protocol = json.loads(SINGLE_STAGE_PROTOCOL.read_text(encoding="utf-8"))
    protocol["world_policy"]["electrochemical_material_family_id"] = (
        NOMINAL_PRIOR_MATERIAL_FAMILY
    )
    protocol["reward_contract"]["scoring_contract_id"] = (
        "electrochemical-s0-balanced-efficiency-v2"
    )
    protocol["horizon"] = 5
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 5
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1
    protocol["algorithms"] = {
        "telemetry_rf_ei": {
            "family": "multi_output_random_forest_expected_improvement",
            "n_initial": 4,
            "n_candidates": 64,
            "n_estimators": 32,
            "local_candidate_fraction": 0.5,
            "local_candidate_scale": 0.12,
            "telemetry_metric_ids": [
                "electrochemical_conversion",
                "selective_product_yield",
                "ohmic_efficiency",
                "transport_efficiency",
            ],
        }
    }

    cell = run_baseline_cell(
        protocol=protocol,
        algorithm_id="telemetry_rf_ei",
        algorithm_seed=0,
    )

    assert cell["cell_status"] == "completed"
    assert cell["agent_manifest"]["optimization_feedback"] == (
        "terminal_score_and_processed_telemetry"
    )
    assert cell["agent_manifest"]["telemetry_metric_ids"] == [
        "electrochemical_conversion",
        "selective_product_yield",
        "ohmic_efficiency",
        "transport_efficiency",
    ]
    assert cell["experiments"][-1]["decision_audit"]["feedback_received_after_execution"][
        "processed_telemetry"
    ]


def test_shuffled_descriptor_baseline_uses_the_frozen_derangement() -> None:
    protocol = json.loads(SINGLE_STAGE_PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    shared = {
        "family": "gaussian_process_expected_improvement",
        "categorical_surrogate_encoding": "nominal_properties",
        "n_initial": 4,
        "n_candidates": 128,
        "local_candidate_fraction": 0.5,
        "local_candidate_scale": 0.12,
    }
    nominal = make_optimizer(
        algorithm_id="descriptor_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=0,
        configuration=shared,
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )
    shuffled = make_optimizer(
        algorithm_id="shuffled_descriptor_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=0,
        configuration={
            **shared,
            "categorical_surrogate_encoding": "shuffled_properties",
            "descriptor_permutation": {
                "electrolyte_profile": [2, 3, 1, 0],
                "solvent": [1, 3, 0, 2],
            },
        },
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )

    assert shuffled.manifest()["material_information_condition"] == (
        "anonymous_shuffled_properties"
    )
    assert np.array_equal(
        shuffled.descriptor_matrix_by_coordinate[0][0],
        nominal.descriptor_matrix_by_coordinate[0][2],
    )
    assert np.array_equal(
        shuffled.descriptor_matrix_by_coordinate[1][0],
        nominal.descriptor_matrix_by_coordinate[1][1],
    )


def test_transport_prior_changes_only_first_initial_material_pair() -> None:
    protocol = json.loads(SINGLE_STAGE_PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    shared = {
        "family": "gaussian_process_expected_improvement",
        "categorical_surrogate_encoding": "nominal_properties",
        "n_initial": 4,
        "n_candidates": 128,
        "local_candidate_fraction": 0.5,
        "local_candidate_scale": 0.12,
    }
    descriptor = make_optimizer(
        algorithm_id="descriptor_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=2,
        configuration=shared,
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )
    prior = make_optimizer(
        algorithm_id="transport_prior_gp_ei",
        task_info=task_info,
        horizon=8,
        seed=2,
        configuration={
            **shared,
            "initial_material_policy": "transport_prior_v0.1",
        },
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        electrochemical_workflow_mode=workflow_mode,
    )

    assert np.array_equal(
        descriptor.initial_design[0, 2:],
        prior.initial_design[0, 2:],
    )
    assert np.array_equal(descriptor.initial_design[1:], prior.initial_design[1:])
    first_parameters = plan_from_baseline_decision(
        prior.propose(),
        algorithm_id="transport_prior_gp_ei",
        task_info=task_info,
        electrochemical_workflow_mode=workflow_mode,
    ).recipe_parameters
    assert first_parameters is not None
    assert first_parameters["electrolyte_profile"] == 1
    assert first_parameters["solvent"] == 1
    assert prior.manifest()["initial_material_policy"] == "transport_prior_v0.1"
