from __future__ import annotations

from chemworld.agents.scientific_adaptation import (
    ScientificExperimentPlan,
    compile_scientific_experiment_plan,
    scientific_measurement_slots,
)
from chemworld.eval.scientific_adaptation_execution import (
    ScientificAdaptationExperimentSession,
)
from chemworld.tasks import get_task


def test_executor_runs_exact_compiled_plan_and_returns_public_terminal_result() -> None:
    task_id = "reaction-to-crystallization"
    task_info = get_task(task_id).to_dict()
    selected_slot = str(scientific_measurement_slots(task_info)[0]["slot_id"])
    plan = ScientificExperimentPlan(
        experiment_intent="probe a reference catalyst condition",
        search_vector=(0.45,) * 10,
        requested_measurement_slots=(selected_slot,),
        diagnostic_target="reaction response before crystallization",
        mechanism_distribution={"no_change": 0.5, "rate_law_family": 0.5},
        expected_effect="a bounded conversion response",
        belief_update_rule="compare with a later matched probe",
        uncertainty=0.5,
        scientific_state={"private_scaffold_memory": "not shared as public history"},
    )
    compiled = compile_scientific_experiment_plan(task_info, plan)

    with ScientificAdaptationExperimentSession(
        task_id=task_id,
        seed=0,
        experiment_horizon=1,
        observation_seed=7001,
    ) as session:
        result = session.execute(plan)

    assert result.completed is True
    assert [item["action"] for item in result.executed_steps] == compiled["steps"]
    assert [item["measurement_slot_id"] for item in result.measurement_evidence] == [
        selected_slot,
        "closeout-final-assay",
    ]
    assert result.terminal_summary["final_assay"] is True
    assert result.terminal_summary["experiment_index"] == 0
    public_record = result.public_record()
    assert "scientific_state" not in public_record["plan"]
    assert public_record["completed"] is True
    assert public_record["operation_count"] == len(compiled["steps"])


def test_phase_offset_keeps_public_evidence_ids_unique() -> None:
    task_id = "reaction-to-crystallization"
    task_info = get_task(task_id).to_dict()
    selected_slot = str(scientific_measurement_slots(task_info)[0]["slot_id"])
    plan = ScientificExperimentPlan(
        experiment_intent="run a shifted phase probe",
        search_vector=(0.5,) * 10,
        requested_measurement_slots=(selected_slot,),
        diagnostic_target="shifted response",
        mechanism_distribution={"no_change": 0.5, "rate_law_family": 0.5},
        expected_effect="bounded response",
        belief_update_rule="compare with public reference",
        uncertainty=0.5,
    )

    with ScientificAdaptationExperimentSession(
        task_id=task_id,
        seed=0,
        experiment_horizon=1,
        experiment_index_offset=2,
    ) as session:
        result = session.execute(plan)

    assert result.experiment_index == 2
    assert result.terminal_summary["experiment_index"] == 2
    assert result.terminal_summary["environment_experiment_index"] == 0
    assert all(item["evidence_id"].startswith("e002-") for item in result.measurement_evidence)
