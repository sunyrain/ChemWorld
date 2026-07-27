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
)
from chemworld.agents.static_optimization import (
    StaticOptimizationAgent,
    StaticOptimizationPlan,
    compile_static_optimization_plan,
)
from chemworld.eval.electrochemical_predictive import (
    build_electrochemical_prediction_queries,
)
from chemworld.eval.static_optimization_execution import StaticOptimizationExperimentSession
from chemworld.eval.static_optimization_postrun import (
    audit_static_optimization_run,
    replay_static_optimization_predictive,
    replay_static_optimization_receipt,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)
from chemworld.tasks import get_task


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
    assert context["experiment_interface"]["parameterization"] == (
        "named_physical_controls"
    )
    assert context["experiment_interface"]["recipe_parameter_schema"] == (
        crystallization_single_stage_parameter_schema()
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
        root
        / "configs/benchmark/"
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
                root
                / "configs/methods/llm_v0.5/"
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
        root
        / "configs/benchmark/"
        "scientific_optimization_s0_v0.2.1_known_horizon_paired_validation_dev.json"
    )
    methods = _load_json(
        root
        / "configs/methods/llm_v0.4/"
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
    assert receipt["primary_score"] == receipt["validation"][
        "primary_validated_recommendation_score_mean"
    ]
    for experiment in receipt["experiments"]:
        result = experiment["result"]
        assert result["operation_count"] == result["compiled_operation_count"]
        assert result["runtime_margin_used"] is False


def test_s0_predictive_mock_adds_local_paired_validation_without_model_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = _load_json(
        root
        / "configs/benchmark/"
        "scientific_optimization_s0_v0.3_named_electrochem_world_understanding_dev.json"
    )
    methods = _load_json(
        root
        / "configs/methods/llm_v0.4/"
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
    for query in predictive["queries"]:
        assert len(query["paired_replicates"]) == 2
        for pair in query["paired_replicates"]:
            assert pair["reference"]["observation_seed"] == pair["intervention"][
                "observation_seed"
            ]
            assert pair["reference"]["observation_noise_namespace"] == pair[
                "intervention"
            ]["observation_noise_namespace"]
    replay = replay_static_optimization_predictive(receipt, protocol)
    assert replay["verified"] is True
    assert replay["replayed_experiment_count"] == 12

    tampered = copy.deepcopy(receipt)
    tampered["predictive_validation"]["queries"][0]["paired_replicates"][0][
        "intervention"
    ]["observation_seed"] += 1
    tampered_replay = replay_static_optimization_predictive(tampered, protocol)
    assert tampered_replay["verified"] is False
    assert any("observation_seed" in item for item in tampered_replay["mismatches"])


def test_s0_single_stage_electrochemical_contract_executes_once() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    parameters = electrochemical_single_stage_parameters_from_unit_vector(
        np.full(6, 0.5)
    )
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
        root
        / "configs/benchmark/"
        "scientific_optimization_s0_v0.4_single_stage_high_20_formal.json"
    )
    methods = _load_json(
        root
        / "configs/methods/llm_v0.4/"
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
    assert all(
        item["result"]["compiled_operation_count"] == 8
        for item in receipt["experiments"]
    )
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
        query.standardized_measurement_slots
        == ("diagnostic-01-ph_meter", "diagnostic-02-uvvis")
        for query in queries
    )
