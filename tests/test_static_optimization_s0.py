from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from scripts.run_static_optimization_s0 import (
    DEVELOPMENT_TEST_METHODS,
    DEVELOPMENT_TEST_PROTOCOL,
    _DeterministicStaticMockClient,
    _load_json,
    _require_external_execution_confirmation,
    _run_cell,
    canonical_sha256,
    run_s0,
)

from chemworld.agents.crystallization_single_stage import (
    crystallization_single_stage_parameter_schema,
)
from chemworld.agents.electrochemical_single_stage import (
    electrochemical_single_stage_parameter_schema,
    electrochemical_single_stage_parameters_from_unit_vector,
    electrochemical_single_stage_unit_vector_from_parameters,
)
from chemworld.agents.scientific_adaptation import ScientificPlanValidationError
from chemworld.agents.static_optimization import (
    COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_ID,
    COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V16_ID,
    COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V17_ID,
    DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN,
    STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION,
    STATIC_OPTIMIZATION_COVERAGE_PROMPT_VERSION,
    STATIC_OPTIMIZATION_NONDUPLICATE_PORTFOLIO_PROMPT_VERSION,
    STATIC_OPTIMIZATION_PORTFOLIO_PROMPT_VERSION,
    StaticFinalRecommendationValidator,
    StaticOptimizationAgent,
    StaticOptimizationPlan,
    compile_static_optimization_plan,
)
from chemworld.agents.task_recipes import task_recipe_coordinate_schema
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.electrochemical_predictive import (
    build_electrochemical_prediction_queries,
)
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
)
from chemworld.eval.static_optimization_postrun import (
    _predictive_accuracy_breakdown,
    _predictive_recommendation_overlap,
    audit_static_optimization_run,
    replay_static_optimization_predictive,
    replay_static_optimization_receipt,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)
from chemworld.tasks import get_task
from chemworld.world.phase_kernel import (
    INDEPENDENT_NOMINAL_SOLVENT_EXTRACTANT_PAIR_V1,
)
from chemworld.world.scoring import (
    DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2,
    PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
    PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
    TaskScoringContract,
)


def test_s0_context_and_plan_have_no_change_world_contract() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="s0-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=6250,
    )
    agent.reset(task_info, 0)
    context = agent.public_context([])
    plan = agent.plan_next([])

    assert context["optimization_contract"]["world_policy"] == "static_for_entire_campaign"
    assert "mechanism_candidates" not in context
    serialized_context = str(context).lower()
    assert "hidden_world" not in serialized_context
    assert "reference_claims" not in serialized_context
    assert "mechanism_candidates" not in serialized_context
    assert context["experiment_interface"]["parameterization"] == ("named_physical_controls")
    assert context["experiment_interface"]["recipe_parameter_schema"] == (
        crystallization_single_stage_parameter_schema()
    )
    assert context["experiment_interface"]["categorical_controls"] == {
        "catalyst": 4,
        "solvent": 4,
    }
    assert context["experiment_interface"]["categorical_semantics"]["unordered_nominal"] is True
    assert (
        context["experiment_interface"]["categorical_semantics"][
            "cross_control_code_equality_meaning"
        ]
        is False
    )
    assert "change" not in serialized_context
    assert set(plan.to_dict()) == {
        "experiment_intent",
        "search_vector",
        "recipe_parameters",
        "requested_measurement_slots",
        "measurement_objective",
        "expected_effect",
        "uncertainty",
    }


def test_registered_distillation_context_exposes_physical_coordinate_semantics() -> None:
    task_info = get_task("reaction-to-distillation").to_dict()
    scoring_contract = TaskScoringContract.from_success_metrics(
        objective=task_info["objective"],
        success_metrics=tuple(task_info["success_metrics"]),
        contract_id=DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2,
    )
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="distillation-s0-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=9000,
        scoring_contract=scoring_contract.to_dict(),
    )
    agent.reset(task_info, 0)

    empty_context = agent.public_context([])
    assert empty_context["experiment_interface"]["parameterization"] == (
        "unit_vector_with_public_physical_coordinate_schema"
    )
    assert empty_context["experiment_interface"]["search_vector_coordinate_schema"] == list(
        task_recipe_coordinate_schema(task_info)
    )
    assert [
        item["control_id"]
        for item in empty_context["experiment_interface"]["search_vector_coordinate_schema"]
    ] == [
        "reaction_temperature_K",
        "reaction_duration_s",
        "reagent_amount_mol",
        "stirring_speed_rpm",
        "catalyst",
        "catalyst_amount_mol",
        "solvent",
        "evaporation_temperature_K",
        "evaporation_duration_s",
        "distillation_temperature_K",
        "distillation_duration_s",
        "reflux_ratio",
        "transfer_fraction",
    ]
    categorical_schema = [
        item
        for item in empty_context["experiment_interface"]["search_vector_coordinate_schema"]
        if item["kind"] == "categorical"
    ]
    assert [item["control_id"] for item in categorical_schema] == [
        "catalyst",
        "solvent",
    ]
    assert all(
        item["selection_semantics"] == "independent_unordered_nominal_choice"
        and item["numeric_order_has_scientific_meaning"] is False
        and item["numeric_distance_has_scientific_meaning"] is False
        for item in categorical_schema
    )
    assert empty_context["experiment_interface"]["categorical_semantics"] == {
        "coordinates_are_independently_selectable": True,
        "categories_are_unordered_nominal_choices": True,
        "numeric_order_has_scientific_meaning": False,
        "numeric_distance_has_scientific_meaning": False,
        "matching_codes_across_coordinates_has_scientific_meaning": False,
        "instruction": (
            "Treat every categorical coordinate as an independent unordered nominal "
            "choice. Numeric proximity and equal numeric codes across different "
            "coordinates carry no scientific meaning."
        ),
    }
    assert empty_context["optimization_contract"]["metric_roles"] == {
        "safety_risk": {
            "role": "audit_only",
            "enters_primary_score": False,
            "constrains_candidate_selection": False,
            "reference_threshold": 0.65,
            "instruction": (
                "Record and report safety_risk, but do not optimize it or treat its "
                "audit reference threshold as a candidate-selection constraint in "
                "this development pilot."
            ),
        }
    }
    assert empty_context["experiment_interface"]["required_measurement_slots"] == [
        "diagnostic-01-hplc",
        "diagnostic-02-gc",
    ]
    assert [
        (
            item["slot_id"],
            item["instrument"],
            item["after_operation"],
            item["selection_policy"],
        )
        for item in empty_context["experiment_interface"]["diagnostic_measurement_slots"]
    ] == [
        ("diagnostic-01-hplc", "hplc", "quench", "required_by_workflow"),
        (
            "diagnostic-02-gc",
            "gc",
            "collect_fraction",
            "required_by_workflow",
        ),
    ]

    plan = agent.plan_next([])
    history = [
        {
            "experiment_index": 0,
            "plan": plan.to_dict(),
            "measurement_evidence": [
                {
                    "evidence_id": "reaction-stage",
                    "measurement_slot_id": "diagnostic-01-hplc",
                    "instrument": "hplc",
                    "processed_estimate": {
                        "conversion": 0.4,
                        "yield": 0.3,
                        "selectivity": 0.8,
                        "byproduct_signal": 0.2,
                        "distillate_purity": 0.0,
                    },
                    "uncertainty": {
                        "conversion_std": 0.01,
                        "yield_std": 0.01,
                        "distillate_purity_std": 0.01,
                    },
                    "reward": 0.1,
                },
                {
                    "evidence_id": "fraction-stage",
                    "measurement_slot_id": "diagnostic-02-gc",
                    "instrument": "gc",
                    "processed_estimate": {
                        "distillate_purity": 0.6,
                        "degradation_warning": 0.1,
                        "byproduct_signal": 0.2,
                        "yield": 0.3,
                    },
                    "uncertainty": {
                        "distillate_purity_std": 0.02,
                        "yield_std": 0.01,
                    },
                    "reward": 0.2,
                },
            ],
            "terminal_summary": {
                "leaderboard_score": 0.2,
                "cost": 0.1,
                "safety_risk": 0.05,
            },
        }
    ]
    compact = agent.public_context(history)["experiment_history"][0]["plan"]
    assert compact["search_vector"] == [0.5] * 13
    assert [item["operation"] for item in compact["public_physical_controls"]] == [
        "add_solvent",
        "add_reagent",
        "add_catalyst",
        "heat",
        "quench",
        "evaporate",
        "distill",
        "collect_fraction",
    ]
    assert compact["public_physical_controls"][6]["reflux_ratio"] == pytest.approx(2.75)
    compact_evidence = agent.public_context(history)["experiment_history"][0][
        "measurement_evidence"
    ]
    assert set(compact_evidence[0]["processed_estimate"]) == {
        "conversion",
        "yield",
        "selectivity",
        "byproduct_signal",
    }
    assert set(compact_evidence[0]["uncertainty"]) == {
        "conversion_std",
        "yield_std",
    }
    assert set(compact_evidence[1]["processed_estimate"]) == {
        "distillate_purity",
        "degradation_warning",
        "byproduct_signal",
    }
    assert set(compact_evidence[1]["uncertainty"]) == {"distillate_purity_std"}


def test_coverage_adaptive_scaffold_balances_first_eight_flow_designs() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="flow-coverage-scaffold-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_ID,
    )
    agent.reset(task_info, 0)
    history: list[dict[str, object]] = []

    for experiment_index in range(8):
        context = agent.public_context(history)
        scaffold = context["campaign_scaffold"]
        assert scaffold["phase"] == "balanced_coverage"
        assert scaffold["initial_design_authority"] == "protocol_executor"
        vector = scaffold["executor_committed_search_vector"]
        plan = agent.plan_next(history)
        assert list(plan.search_vector) == pytest.approx(vector)
        decision_audit = agent.decision_audit()
        assert decision_audit["coverage_design_enforced"] is True
        assert decision_audit["recipe_selection_authority"] == "protocol_executor"
        history.append(
            {
                "experiment_index": experiment_index,
                "plan": plan.to_dict(),
                "measurement_evidence": [],
                "terminal_summary": {
                    "leaderboard_score": float(experiment_index) / 100.0,
                    "cost": 0.0,
                    "safety_risk": 0.0,
                },
            }
        )

    adaptive = agent.public_context(history)["campaign_scaffold"]
    assert adaptive["phase"] == "global_surrogate_discrimination"
    assert len(adaptive["model_candidate_portfolio"]) == 6
    assert {
        item["candidate_id"] for item in adaptive["model_candidate_portfolio"]
    } == {
        "gp_ei",
        "rf_ei",
        "surrogate_consensus",
        "maximin_global",
        "boundary_challenge",
        "gp_uncertainty",
    }
    audit = adaptive["coverage_audit"]
    assert audit["all_continuous_extremes_seen"] is True
    assert audit["all_nominal_categories_seen"] is True
    assert all(
        sorted(item["category_counts"].values()) == [2, 2, 2, 2]
        for item in audit["categorical_controls"]
    )
    assert len(audit["nominal_pair_coverage"]) == 1
    assert audit["nominal_pair_coverage"][0]["distinct_pair_count"] == 8
    assert (
        audit["nominal_pair_coverage"][0][
            "maximally_distinct_at_current_budget"
        ]
        is True
    )
    assert audit["all_nominal_pairs_maximally_distinct"] is True
    assert agent.manifest()["prompt_version"] == (
        STATIC_OPTIMIZATION_NONDUPLICATE_PORTFOLIO_PROMPT_VERSION
    )
    adaptive_plan = agent.plan_next(history)
    adaptive_audit = agent.decision_audit()
    assert adaptive_audit["coverage_design_enforced"] is False
    assert adaptive_audit["recipe_selection_authority"] == "model"
    assert adaptive_audit["portfolio_selection_enforced"] is True
    assert adaptive["task_neutral_default_candidate_id"] == "maximin_global"
    assert adaptive["model_candidate_portfolio"][0]["candidate_id"] == "maximin_global"
    assert adaptive_audit["portfolio_candidate_id"] == "maximin_global"
    assert (
        adaptive_audit["portfolio_candidate_generation_authority"]
        == "protocol_executor_using_public_history_only"
    )
    assert adaptive_audit["portfolio_candidate_selection_authority"] == "model"
    assert list(adaptive_plan.search_vector) != pytest.approx(vector)


def test_coverage_scaffold_keeps_named_controls_physical() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    direct = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="crystallization-direct-scaffold-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
    )
    direct.reset(task_info, 0)
    assert "campaign_scaffold" not in direct.public_context([])

    coverage = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="crystallization-coverage-scaffold-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_ID,
    )
    coverage.reset(task_info, 0)
    scaffold = coverage.public_context([])["campaign_scaffold"]
    assert "executor_committed_search_vector" not in scaffold
    assert set(scaffold["executor_committed_recipe_parameters"]) == set(
        crystallization_single_stage_parameter_schema()
    )
    plan = coverage.plan_next([])
    assert plan.recipe_parameters == pytest.approx(
        scaffold["executor_committed_recipe_parameters"]
    )
    assert coverage.decision_audit()["coverage_design_enforced"] is True


def test_portfolio_candidate_id_must_match_the_returned_recipe() -> None:
    class MismatchedPortfolioMock(_DeterministicStaticMockClient):
        def complete_json(
            self,
            *,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int = 4096,
        ):
            completion = super().complete_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
            )
            prompt = json.loads(user_prompt)
            scaffold = prompt.get("public_experiment_context", {}).get(
                "campaign_scaffold", {}
            )
            if scaffold.get("model_candidate_portfolio"):
                completion.payload["search_vector"] = [0.5] * 8
            return completion

    agent = StaticOptimizationAgent(
        MismatchedPortfolioMock(),
        role_id="portfolio-recipe-binding-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_ID,
    )
    agent.reset(get_task("flow-reaction-optimization").to_dict(), 0)
    history: list[dict[str, object]] = []
    for experiment_index in range(8):
        plan = agent.plan_next(history)
        history.append(
            {
                "experiment_index": experiment_index,
                "plan": plan.to_dict(),
                "measurement_evidence": [],
                "terminal_summary": {
                    "leaderboard_score": float(experiment_index) / 100.0,
                    "cost": 0.0,
                    "safety_risk": 0.0,
                },
            }
        )

    with pytest.raises(
        ScientificPlanValidationError,
        match="does not match the selected portfolio candidate",
    ):
        agent.plan_next(history)


def test_v16_coverage_scaffold_remains_replay_compatible() -> None:
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="v16-scaffold-compatibility-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V16_ID,
    )
    agent.reset(get_task("flow-reaction-optimization").to_dict(), 0)
    history: list[dict[str, object]] = []
    for experiment_index in range(8):
        plan = agent.plan_next(history)
        history.append(
            {
                "experiment_index": experiment_index,
                "plan": plan.to_dict(),
                "measurement_evidence": [],
                "terminal_summary": {
                    "leaderboard_score": float(experiment_index) / 100.0,
                    "cost": 0.0,
                    "safety_risk": 0.0,
                },
            }
        )

    scaffold = agent.public_context(history)["campaign_scaffold"]
    assert scaffold["scaffold_id"] == COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V16_ID
    assert scaffold["phase"] == "adaptive_discrimination"
    assert "model_candidate_portfolio" not in scaffold
    assert agent.manifest()["prompt_version"] == STATIC_OPTIMIZATION_COVERAGE_PROMPT_VERSION


def test_v17_portfolio_scaffold_remains_replay_compatible() -> None:
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="v17-scaffold-compatibility-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V17_ID,
    )
    agent.reset(get_task("flow-reaction-optimization").to_dict(), 0)
    history = [
        {
            "experiment_index": experiment_index,
            "plan": {
                "search_vector": [float(experiment_index % 2)] * 8,
                "requested_measurement_slots": [],
            },
            "measurement_evidence": [],
            "terminal_summary": {
                "leaderboard_score": float(experiment_index) / 100.0,
                "cost": 0.0,
                "safety_risk": 0.0,
            },
        }
        for experiment_index in range(17)
    ]

    scaffold = agent.public_context(history)["campaign_scaffold"]

    assert scaffold["scaffold_id"] == COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_V17_ID
    assert scaffold["phase"] == "robust_closeout"
    assert "model_candidate_portfolio" not in scaffold
    assert scaffold["free_model_closeout_experiment_indices"] == [17, 18, 19]
    assert agent.manifest()["prompt_version"] == (
        STATIC_OPTIMIZATION_PORTFOLIO_PROMPT_VERSION
    )


def test_v18_portfolio_keeps_all_twelve_model_rounds_novel_and_portfolio_bound() -> None:
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="v18-scaffold-nonduplicate-test",
        response_max_tokens=1000,
        history_limit=20,
        prompt_token_estimate_cap=20_000,
        experiment_horizon=20,
        horizon_visible=True,
        optimization_scaffold_id=COVERAGE_ADAPTIVE_OPTIMIZATION_SCAFFOLD_ID,
    )
    agent.reset(get_task("flow-reaction-optimization").to_dict(), 0)
    history = [
        {
            "experiment_index": experiment_index,
            "plan": {
                "search_vector": [
                    ((experiment_index + coordinate) % 19) / 18.0
                    for coordinate in range(8)
                ],
                "requested_measurement_slots": [],
            },
            "measurement_evidence": [],
            "terminal_summary": {
                "leaderboard_score": float(experiment_index) / 100.0,
                "cost": 0.0,
                "safety_risk": 0.0,
            },
        }
        for experiment_index in range(17)
    ]

    scaffold = agent.public_context(history)["campaign_scaffold"]

    assert scaffold["phase"] == "nonduplicate_bottleneck_closeout"
    assert len(scaffold["model_candidate_portfolio"]) == 6
    assert scaffold["portfolio_candidate_selection_experiment_indices"] == list(
        range(8, 20)
    )
    assert scaffold["free_model_closeout_experiment_indices"] == []
    assert scaffold["invariants"]["campaign_exploration_recipes_must_be_distinct"]
    assert scaffold["invariants"]["blind_validation_supplies_replication"]
    history_vectors = [record["plan"]["search_vector"] for record in history]
    for candidate in scaffold["model_candidate_portfolio"]:
        vector = candidate["search_vector"]
        assert all(vector != previous for previous in history_vectors)


def test_distillation_compiler_requires_stage_local_hplc_and_fraction_gc() -> None:
    task_info = get_task("reaction-to-distillation").to_dict()
    complete = StaticOptimizationPlan(
        experiment_intent="measure reaction and separation stages",
        search_vector=(0.5,) * 13,
        requested_measurement_slots=("diagnostic-01-hplc", "diagnostic-02-gc"),
        measurement_objective="separate reaction-stage and fraction-stage evidence",
        expected_effect="produce one stage-resolved terminal result",
        uncertainty=0.5,
    )

    compiled = compile_static_optimization_plan(task_info, complete)

    assert [item["operation"] for item in compiled["steps"]] == [
        "add_solvent",
        "add_reagent",
        "add_catalyst",
        "heat",
        "quench",
        "measure",
        "evaporate",
        "distill",
        "collect_fraction",
        "measure",
        "terminate",
        "measure",
    ]
    assert compiled["steps"][5] == {"operation": "measure", "instrument": "hplc"}
    assert compiled["steps"][9] == {"operation": "measure", "instrument": "gc"}
    assert compiled["metadata"]["measurement_slots_by_step"] == {
        "5": "diagnostic-01-hplc",
        "9": "diagnostic-02-gc",
        "11": "closeout-final-assay",
    }

    missing_hplc = StaticOptimizationPlan(
        experiment_intent=complete.experiment_intent,
        search_vector=complete.search_vector,
        requested_measurement_slots=("diagnostic-02-gc",),
        measurement_objective=complete.measurement_objective,
        expected_effect=complete.expected_effect,
        uncertainty=complete.uncertainty,
    )
    with pytest.raises(ValueError, match="workflow-required diagnostic"):
        compile_static_optimization_plan(task_info, missing_hplc)


@pytest.mark.parametrize(
    ("task_id", "expected_diagnostic_metrics"),
    [
        (
            "electrochemical-conversion",
            [
                {"pH_normalized", "precipitation_signal"},
                {
                    "faradaic_efficiency",
                    "transport_efficiency",
                    "ohmic_efficiency",
                    "energy_efficiency",
                },
            ],
        ),
        (
            "reaction-to-crystallization",
            [
                {"conversion", "yield", "selectivity", "byproduct_signal"},
                {"crystal_purity", "yield", "byproduct_signal"},
            ],
        ),
        (
            "partition-discovery",
            [
                {
                    "phase_ratio",
                    "product_in_organic",
                    "product_in_aqueous",
                    "impurity_signal",
                },
                {
                    "purity",
                    "recovery",
                    "product_in_organic",
                    "product_in_aqueous",
                    "impurity_signal",
                },
            ],
        ),
        (
            "flow-reaction-optimization",
            [{"flow_conversion", "yield", "selectivity"}],
        ),
    ],
)
def test_single_seed_stage_evidence_is_filtered_before_model_context(
    task_id: str,
    expected_diagnostic_metrics: list[set[str]],
) -> None:
    task_info = get_task(task_id).to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id=f"{task_id}-stage-evidence-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=12000,
    )
    agent.reset(task_info, 0)
    empty_context = agent.public_context([])
    assert empty_context["experiment_interface"]["required_measurement_slots"] == []
    plan = agent.plan_next([])

    with StaticOptimizationExperimentSession(
        task_id=task_id,
        seed=0,
        experiment_horizon=1,
    ) as session:
        result = session.execute(plan)

    assert result.completed is True
    public_history = agent.public_context(
        [
            {
                "experiment_index": 0,
                "plan": plan.to_dict(),
                "measurement_evidence": list(result.measurement_evidence),
                "terminal_summary": result.terminal_summary,
            }
        ]
    )["experiment_history"][0]
    diagnostic_evidence = public_history["measurement_evidence"][: len(expected_diagnostic_metrics)]
    assert [
        set(item["processed_estimate"]) for item in diagnostic_evidence
    ] == expected_diagnostic_metrics


def test_partition_v3_observes_both_phase_inventories_on_a_fixed_feed_basis() -> None:
    plan = StaticOptimizationPlan(
        experiment_intent="audit the corrected partition endpoint",
        search_vector=(0.125, 0.0, 0.0, 0.875, 1.0, 1.0, 0.5, 0.5),
        requested_measurement_slots=(
            "diagnostic-01-hplc",
            "diagnostic-02-hplc",
        ),
        measurement_objective="measure organic recovery and aqueous residual",
        expected_effect="produce a mass-balanced two-phase endpoint",
        uncertainty=0.5,
    )

    with StaticOptimizationExperimentSession(
        task_id="partition-discovery",
        seed=0,
        experiment_horizon=1,
        scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
        observation_noise_namespace="partition-v3-fixed-basis-test",
    ) as session:
        result = session.execute(plan)

    first_hplc = result.measurement_evidence[0]["processed_estimate"]
    assert first_hplc["product_in_organic"] > 0.70
    assert first_hplc["product_in_aqueous"] > 0.10
    assert (
        first_hplc["product_in_organic"] + first_hplc["product_in_aqueous"]
    ) == pytest.approx(1.0, abs=0.08)
    assert result.terminal_summary["leaderboard_score"] > 0.58


def test_partition_nominal_pair_law_is_scoped_to_v3_contract() -> None:
    environments = {
        "default": ChemWorldEnv(task_id="partition-discovery", seed=0),
        "v2": ChemWorldEnv(
            task_id="partition-discovery",
            seed=0,
            scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
        ),
        "v3": ChemWorldEnv(
            task_id="partition-discovery",
            seed=0,
            scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
        ),
    }
    try:
        assert (
            environments["default"]
            .runtime.domain_services.phase_separation.nominal_pair_contract
            is None
        )
        assert (
            environments["v2"]
            .runtime.domain_services.phase_separation.nominal_pair_contract
            is None
        )
        assert (
            environments["v3"]
            .runtime.domain_services.phase_separation.nominal_pair_contract
            == INDEPENDENT_NOMINAL_SOLVENT_EXTRACTANT_PAIR_V1
        )
    finally:
        for environment in environments.values():
            environment.close()


def test_external_s0_execution_requires_exact_owner_confirmed_hashes() -> None:
    protocol = {"protocol_id": "pending", "status": "development_pending_owner_confirmation"}
    methods = {"freeze_id": "candidate", "methods": {}}

    with pytest.raises(RuntimeError, match="confirm-protocol-sha256"):
        _require_external_execution_confirmation(
            protocol=protocol,
            methods=methods,
            provider="wellau",
            allow_external_provider=True,
            confirmed_protocol_sha256=None,
            confirmed_method_sha256=None,
        )
    with pytest.raises(RuntimeError, match="confirm-method-sha256"):
        _require_external_execution_confirmation(
            protocol=protocol,
            methods=methods,
            provider="wellau",
            allow_external_provider=True,
            confirmed_protocol_sha256=canonical_sha256(protocol),
            confirmed_method_sha256=None,
        )
    _require_external_execution_confirmation(
        protocol=protocol,
        methods=methods,
        provider="wellau",
        allow_external_provider=True,
        confirmed_protocol_sha256=canonical_sha256(protocol),
        confirmed_method_sha256=canonical_sha256(methods),
    )


def test_s0_compiler_keeps_mechanical_closeout_only() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    plan = StaticOptimizationPlan(
        experiment_intent="run a fixed-world probe",
        search_vector=(0.5,) * 10,
        requested_measurement_slots=("diagnostic-01-hplc",),
        measurement_objective="compare public yield and purity",
        expected_effect="the probe provides a fixed-world reference",
        uncertainty=0.5,
    )

    compiled = compile_static_optimization_plan(task_info, plan)

    assert compiled["metadata"]["static_world"] is True
    assert compiled["steps"][-2:] == [
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def test_s0_receipt_replays_in_static_world() -> None:
    protocol = _load_json(DEVELOPMENT_TEST_PROTOCOL)
    methods = _load_json(DEVELOPMENT_TEST_METHODS)
    short_protocol = copy.deepcopy(protocol)
    short_protocol["horizon"] = 1
    receipt = _run_cell(
        protocol=short_protocol,
        methods=methods,
        method_id="s0_flash_direct",
        task_id="reaction-to-crystallization",
        provider="mock",
        allow_external_provider=False,
    )

    replay = replay_static_optimization_receipt(receipt, short_protocol)

    assert receipt["world_policy"]["interventions"] == []
    assert receipt["agent_manifest"]["static_world"] is True
    assert replay["verified"] is True
    assert replay["replayed_experiment_count"] == 1


def test_s0_session_does_not_accept_interventions() -> None:
    session = StaticOptimizationExperimentSession(
        task_id="reaction-to-crystallization",
        seed=0,
        experiment_horizon=1,
    )
    try:
        assert not hasattr(session, "interventions")
    finally:
        session.close()


def test_formal_postrun_audit_preserves_source_lifecycle(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root / "configs/benchmark/"
        "scientific_optimization_s0_v0.5_crystallization_high_20_formal.json"
    )
    protocol["horizon"] = 1
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 1
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1
    protocol["world_understanding"]["predictive_score_enabled"] = False
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(
        json.dumps(protocol, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    run_root = tmp_path / "run"

    run_s0(
        SimpleNamespace(
            protocol=protocol_path,
            llm_methods=(
                root / "configs/methods/llm_v0.5/"
                "participant_methods_s0_wellau_codex_sol_high_crystallization_20.json"
            ),
            output=run_root,
            provider="mock",
            allow_external_provider=False,
            confirm_protocol_sha256=None,
            confirm_method_sha256=None,
            world_seed=None,
            task=None,
            method_id=None,
        )
    )
    audit = audit_static_optimization_run(protocol=protocol, run_root=run_root)

    assert audit["formal_result"] is True
    assert audit["benchmark_claim_allowed"] is False
    assert audit["descriptive_scores"]["formal_optimization_estimand"] is True
    assert audit["replay"]["all_verified"] is True
    assert audit["interpretation"].startswith("Formal S0")


def test_s0_known_horizon_context_reports_remaining_experiments() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    agent = StaticOptimizationAgent(
        _DeterministicStaticMockClient(),
        role_id="s0-known-horizon-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=7000,
        experiment_horizon=8,
        horizon_visible=True,
        final_synthesis_enabled=True,
        final_synthesis_prompt_token_estimate_cap=9000,
        include_task_operation_budget=False,
    )
    agent.reset(task_info, 0)

    first = agent.public_context([])
    budget = first["optimization_contract"]["scientific_campaign_budget"]

    assert budget == {
        "total_exploration_experiments": 8,
        "completed_experiments": 0,
        "current_experiment_number": 1,
        "remaining_experiments_after_current": 7,
        "final_synthesis_after_exploration": True,
        "validation_feedback_returned_to_agent": False,
    }
    assert "budget" not in first["task"]


def test_s0_integrated_mock_runs_synthesis_and_blind_validation() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root / "configs/benchmark/"
        "scientific_optimization_s0_v0.2.1_known_horizon_paired_validation_dev.json"
    )
    methods = _load_json(
        root / "configs/methods/llm_v0.4/"
        "participant_methods_s0_wellau_codex_sol_development_r5.json"
    )
    short_protocol = copy.deepcopy(protocol)
    short_protocol["horizon"] = 2
    short_protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    short_protocol["validation_budget"]["incumbent_replicates"] = 1
    short_protocol["validation_budget"]["recommendation_replicates"] = 1

    receipt = _run_cell(
        protocol=short_protocol,
        methods=methods,
        method_id="s0_codex_sol_direct",
        task_id="reaction-to-crystallization",
        provider="mock",
        allow_external_provider=False,
    )

    assert receipt["cell_status"] == "completed"
    assert receipt["completed_experiment_count"] == 2
    assert receipt["completed_synthesis_call_count"] == 1
    assert receipt["completed_validation_experiment_count"] == 2
    assert receipt["total_physical_experiment_count"] == 4
    assert receipt["resources"]["model_call_count"] == 3
    assert receipt["final_synthesis"]["recommendation"]["recommendation_type"] == "tested"
    assert receipt["validation"]["blind"] is True
    assert receipt["validation"]["feedback_returned_to_agent"] is False
    assert (
        receipt["primary_score"]
        == receipt["validation"]["primary_validated_recommendation_score_mean"]
    )
    for experiment in receipt["experiments"]:
        result = experiment["result"]
        assert result["operation_count"] == result["compiled_operation_count"]
        assert result["runtime_margin_used"] is False


def test_s0_final_prompt_omits_predictive_field_when_predictive_is_disabled() -> None:
    class RecordingMockClient(_DeterministicStaticMockClient):
        def __init__(self) -> None:
            super().__init__()
            self.final_prompt: dict[str, object] | None = None

        def complete_json(
            self,
            *,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int = 4096,
        ):
            prompt = json.loads(user_prompt)
            if "public_final_synthesis_context" in prompt:
                self.final_prompt = prompt
            return super().complete_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
            )

    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root / "configs/benchmark/"
        "scientific_optimization_s0_v0.2.1_known_horizon_paired_validation_dev.json"
    )
    methods = _load_json(
        root / "configs/methods/llm_v0.4/"
        "participant_methods_s0_wellau_codex_sol_development_r5.json"
    )
    short_protocol = copy.deepcopy(protocol)
    short_protocol["horizon"] = 1
    short_protocol["scientific_campaign_budget"]["exploration_experiments"] = 1
    receipt = _run_cell(
        protocol=short_protocol,
        methods=methods,
        method_id="s0_codex_sol_direct",
        task_id="reaction-to-crystallization",
        provider="mock",
        allow_external_provider=False,
    )
    client = RecordingMockClient()
    agent = StaticOptimizationAgent(
        client,
        role_id="s0-final-contract-test",
        response_max_tokens=1000,
        history_limit=8,
        prompt_token_estimate_cap=9000,
        experiment_horizon=1,
        horizon_visible=True,
        final_synthesis_enabled=True,
        final_synthesis_prompt_token_estimate_cap=9000,
        predictive_world_understanding_enabled=False,
    )
    agent.reset(get_task("reaction-to-crystallization").to_dict(), 0)

    agent.synthesize_final(receipt["public_history"])

    assert client.final_prompt is not None
    assert "counterfactual_predictions" not in client.final_prompt["required_json_shape"]


def test_s0_predictive_mock_adds_local_paired_validation_without_model_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root / "configs/benchmark/"
        "scientific_optimization_s0_v0.3_named_electrochem_world_understanding_dev.json"
    )
    methods = _load_json(
        root / "configs/methods/llm_v0.4/"
        "participant_methods_s0_wellau_codex_sol_development_r6.json"
    )

    receipt = _run_cell(
        protocol=protocol,
        methods=methods,
        method_id="s0_codex_sol_direct",
        task_id="electrochemical-conversion",
        provider="mock",
        allow_external_provider=False,
    )

    assert receipt["cell_status"] == "completed"
    assert receipt["completed_experiment_count"] == 8
    assert receipt["completed_synthesis_call_count"] == 1
    assert receipt["completed_validation_experiment_count"] == 6
    assert receipt["completed_predictive_validation_experiment_count"] == 12
    assert receipt["total_physical_experiment_count"] == 26
    assert receipt["resources"]["model_call_count"] == 9
    predictive = receipt["predictive_validation"]
    assert predictive["feedback_returned_to_agent"] is False
    assert predictive["model_call_count_before_execution"] == 9
    assert predictive["model_call_count_after_execution"] == 9
    overlap = _predictive_recommendation_overlap(receipt)
    assert overlap["query_visible_during_final_synthesis"] is True
    assert overlap["exactly_matches_explored_action"] is True
    assert overlap["exactly_matches_predictive_reference"] is True
    assert overlap["exactly_matches_predictive_intervention"] is False
    for query in predictive["queries"]:
        assert len(query["paired_replicates"]) == 2
        for pair in query["paired_replicates"]:
            assert pair["reference"]["observation_seed"] == pair["intervention"]["observation_seed"]
            assert (
                pair["reference"]["observation_noise_namespace"]
                == pair["intervention"]["observation_noise_namespace"]
            )
    replay = replay_static_optimization_predictive(receipt, protocol)
    assert replay["verified"] is True
    assert replay["replayed_experiment_count"] == 12

    tampered = copy.deepcopy(receipt)
    tampered["predictive_validation"]["queries"][0]["paired_replicates"][0]["intervention"][
        "observation_seed"
    ] += 1
    tampered_replay = replay_static_optimization_predictive(tampered, protocol)
    assert tampered_replay["verified"] is False
    assert any("observation_seed" in item for item in tampered_replay["mismatches"])


def test_tolerant_declared_claim_does_not_invalidate_final_recommendation() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    parameters = electrochemical_single_stage_parameters_from_unit_vector(np.full(6, 0.5))
    search_vector = tuple(
        float(value)
        for value in electrochemical_single_stage_unit_vector_from_parameters(parameters)
    )
    plan = StaticOptimizationPlan(
        experiment_intent="test one electrochemical condition",
        search_vector=search_vector,
        requested_measurement_slots=(
            "diagnostic-01-ph_meter",
            "diagnostic-02-uvvis",
        ),
        measurement_objective="measure the fixed-world response",
        expected_effect="establish a source method",
        uncertainty=0.5,
        recipe_parameters=parameters,
    )
    history = [
        {
            "experiment_index": 0,
            "plan": plan.to_dict(),
        }
    ]
    validator = StaticFinalRecommendationValidator(
        task_info,
        predictive_world_understanding_enabled=True,
        final_synthesis_version=(STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION),
        declared_claim_validation_policy=(DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN),
    )
    payload = {
        "schema_version": STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION,
        "recommended_recipe_parameters": parameters,
        "recommended_measurement_slots": list(plan.requested_measurement_slots),
        "recommendation_type": "tested",
        "source_experiment_indices": [0],
        "predicted_score": 0.5,
        "confidence": 0.6,
        "method_summary": "reuse the tested source method",
        "evidence_refs": ["e1"],
        "working_explanation": {
            "empirical_relationships": ["the source method was measurable"],
            "mechanistic_hypothesis": "an unsupported effect term is secondary",
            "supporting_evidence_ids": ["e1"],
            "contradicting_evidence_ids": [],
            "uncertainty": 0.4,
            "structured_claims": [
                {
                    "claim_id": "unsupported-effect",
                    "cause_variables": ["potential_V"],
                    "effect_variable": "selective_product_yield",
                    "relation": "positive",
                    "mechanism_tags": ["unsupported_mechanism_tag"],
                    "scope": "tested range",
                    "evidence_ids": ["e1"],
                    "confidence": 0.6,
                }
            ],
        },
        "remaining_risks": ["secondary claim is unscored"],
        "recommended_followup": "retain the Predictive-only evaluation",
    }

    recommendation = validator.validate(
        payload,
        history=history,
        evidence_catalog=["e1"],
    )

    explanation = recommendation.working_explanation
    assert explanation["structured_claims"] == []
    diagnostics = explanation["structured_claim_diagnostics"]
    assert diagnostics["unscored_claim_count"] == 1
    assert diagnostics["unscored_claims"][0]["reason_code"] == ("unknown_mechanism_tag")
    assert diagnostics["unscored_claims"][0]["unknown_terms"] == ["unsupported_mechanism_tag"]


def test_predictive_accuracy_breakdown_separates_effect_coverage() -> None:
    breakdown = _predictive_accuracy_breakdown(
        {
            "rows": [
                {"actual_direction": "decrease", "correct": True},
                {"actual_direction": "increase", "correct": False},
                {"actual_direction": "no_material_change", "correct": True},
                {"actual_direction": "no_material_change", "correct": False},
                {"actual_direction": "no_material_change", "correct": True},
            ]
        }
    )

    assert breakdown["nontrivial_effects"] == {
        "count": 2,
        "correct_count": 1,
        "directional_accuracy": 0.5,
    }
    assert breakdown["no_material_change"] == {
        "count": 3,
        "correct_count": 2,
        "directional_accuracy": pytest.approx(2 / 3),
    }


def test_s0_single_stage_electrochemical_contract_executes_once() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    parameters = electrochemical_single_stage_parameters_from_unit_vector(np.full(6, 0.5))
    plan = StaticOptimizationPlan(
        experiment_intent="execute one production electrolysis",
        search_vector=(0.5,) * 6,
        requested_measurement_slots=(
            "diagnostic-01-ph_meter",
            "diagnostic-02-uvvis",
        ),
        measurement_objective="measure the single-stage outcome",
        expected_effect="produce one terminal score",
        uncertainty=0.5,
        recipe_parameters=parameters,
    )

    compiled = compile_static_optimization_plan(
        task_info,
        plan,
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    )

    assert set(electrochemical_single_stage_parameter_schema()) == {
        "electrolyte_profile",
        "solvent",
        "reagent_amount_mol",
        "potential_V",
        "current_mA",
        "duration_s",
    }
    assert [step["operation"] for step in compiled["steps"]] == [
        "add_solvent",
        "add_reagent",
        "set_potential",
        "electrolyze",
        "measure",
        "measure",
        "terminate",
        "measure",
    ]
    assert sum(step["operation"] == "electrolyze" for step in compiled["steps"]) == 1

    with StaticOptimizationExperimentSession(
        task_id="electrochemical-conversion",
        seed=0,
        experiment_horizon=1,
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    ) as session:
        result = session.execute(plan)

    assert result.completed is True
    assert result.compiled_operation_count == 8
    assert [item["measurement_slot_id"] for item in result.measurement_evidence] == [
        "diagnostic-01-ph_meter",
        "diagnostic-02-uvvis",
        "closeout-final-assay",
    ]


def test_s0_single_stage_predictive_queries_use_production_controls() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root / "configs/benchmark/scientific_optimization_s0_v0.4_single_stage_high_20_formal.json"
    )
    methods = _load_json(
        root / "configs/methods/llm_v0.4/"
        "participant_methods_s0_wellau_codex_sol_high_single_stage_20.json"
    )
    short_protocol = copy.deepcopy(protocol)
    short_protocol["horizon"] = 2
    short_protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    short_protocol["validation_budget"]["incumbent_replicates"] = 1
    short_protocol["validation_budget"]["recommendation_replicates"] = 1

    receipt = _run_cell(
        protocol=short_protocol,
        methods=methods,
        method_id="s0_codex_sol_high_single_stage_20",
        task_id="electrochemical-conversion",
        provider="mock",
        allow_external_provider=False,
    )

    assert receipt["cell_status"] == "completed"
    assert all(item["result"]["compiled_operation_count"] == 8 for item in receipt["experiments"])
    queries = build_electrochemical_prediction_queries(
        receipt["public_history"],
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    )
    assert [query.intervention_variable for query in queries] == [
        "potential_V",
        "current_mA",
        "electrolyte_profile",
    ]
    assert all(
        query.standardized_measurement_slots == ("diagnostic-01-ph_meter", "diagnostic-02-uvvis")
        for query in queries
    )
