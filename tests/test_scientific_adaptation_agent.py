from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pytest

from chemworld.agents.prompt_context import PromptBudgetExceededError
from chemworld.agents.scientific_adaptation import (
    BoundedScientificMemory,
    DirectScaffoldPolicy,
    NullScientificMemory,
    ScientificAdaptationAgent,
    ScientificExperimentPlan,
    ScientificPlanValidationError,
    StatefulScientificScaffoldPolicy,
    compile_scientific_experiment_plan,
    scientific_measurement_slots,
)
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.tasks import get_task


@dataclass
class _Completion:
    payload: dict[str, Any]
    model: str = "development-model"
    usage: dict[str, Any] | None = None
    attempts: int = 1

    def __post_init__(self) -> None:
        if self.usage is None:
            self.usage = {"prompt_tokens": 100, "completion_tokens": 40}


class _Client:
    model = "development-model"

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.prompts: list[dict[str, Any]] = []

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> _Completion:
        self.prompts.append(
            {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "max_tokens": max_tokens,
            }
        )
        return _Completion(payload=self.payload)


def _candidate_definitions() -> dict[str, str]:
    return {
        "no_change": "The prior world law remains adequate.",
        "rate_law_family": "A public kinetic response relation changed.",
    }


def _history() -> list[dict[str, Any]]:
    return [
        {
            "schema_version": "chemworld-scientific-experiment-result-0.1-dev",
            "task_id": "reaction-to-crystallization",
            "experiment_index": 0,
            "plan": {
                "experiment_intent": "establish a reference",
                "search_vector": [0.5] * 10,
                "requested_measurement_slots": ["diagnostic-01-hplc"],
                "diagnostic_target": "reference response",
                "mechanism_distribution": {
                    "no_change": 0.5,
                    "rate_law_family": 0.5,
                },
                "expected_effect": "moderate response",
                "belief_update_rule": "compare against the next matched probe",
                "uncertainty": 0.5,
                "scientific_state": {"must_not": "enter shared public history"},
            },
            "measurement_evidence": [
                {
                    "evidence_id": "e000-diagnostic-01-hplc",
                    "measurement_slot_id": "diagnostic-01-hplc",
                    "instrument": "hplc",
                    "observation": {"conversion": 0.4},
                    "processed_estimate": {"conversion": 0.4},
                    "uncertainty": {"conversion": 0.03},
                    "reward": 0.1,
                }
            ],
            "terminal_summary": {"leaderboard_score": 0.3},
            "completed": True,
            "operation_count": 11,
        }
    ]


def _base_payload() -> dict[str, Any]:
    return {
        "experiment_intent": "test whether catalyst-dose response changed",
        "search_vector": [0.4] * 10,
        "requested_measurement_slots": ["diagnostic-02-hplc"],
        "diagnostic_target": "dose-response contrast",
        "mechanism_distribution": {
            "no_change": 0.4,
            "rate_law_family": 0.6,
        },
        "expected_effect": "a changed rate law alters the matched dose contrast",
        "belief_update_rule": "increase rate-law belief if the contrast exceeds reference",
        "uncertainty": 0.35,
    }


def _scientific_state() -> dict[str, Any]:
    return {
        "belief": {"no_change": 0.4, "rate_law_family": 0.6},
        "unresolved_question": "Is the shifted response specific to catalyst dose?",
        "next_experiment_plan": {
            "intent": "run a matched catalyst-dose contrast",
            "controlled_variables": ["temperature", "solvent"],
            "varied_variable": "catalyst dose",
        },
        "evidence_summary": [
            {
                "evidence_id": "e000-diagnostic-01-hplc",
                "observation": "The reference conversion was 0.4.",
                "interpretation": "A matched higher-dose probe is still needed.",
                "reliability": "high",
            }
        ],
    }


def test_direct_and_stateful_share_exact_public_context() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    direct_client = _Client(_base_payload())
    stateful_payload = _base_payload()
    stateful_payload["scientific_state"] = _scientific_state()
    stateful_client = _Client(stateful_payload)
    direct = ScientificAdaptationAgent(
        direct_client,
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
    )
    stateful = ScientificAdaptationAgent(
        stateful_client,
        role_id="stateful",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=StatefulScientificScaffoldPolicy(),
        memory_store=BoundedScientificMemory(tuple(_candidate_definitions())),
    )
    direct.reset(task_info, 0)
    stateful.reset(task_info, 0)

    direct_plan = direct.plan_next(_history())
    stateful_plan = stateful.plan_next(_history())

    direct_prompt = json.loads(direct_client.prompts[0]["user_prompt"])
    stateful_prompt = json.loads(stateful_client.prompts[0]["user_prompt"])
    assert (
        direct_prompt["public_experiment_context"] == (stateful_prompt["public_experiment_context"])
    )
    assert direct_prompt["public_context_sha256"] == (stateful_prompt["public_context_sha256"])
    assert (
        direct.decision_audit()["public_context_sha256"]
        == (stateful.decision_audit()["public_context_sha256"])
    )
    public_history_plan = direct_prompt["public_experiment_context"]["experiment_history"][0][
        "plan"
    ]
    assert "scientific_state" not in public_history_plan
    assert set(public_history_plan) == {
        "search_vector",
        "requested_measurement_slots",
        "mechanism_distribution",
        "uncertainty",
    }
    public_evidence = direct_prompt["public_experiment_context"]["experiment_history"][0][
        "measurement_evidence"
    ][0]
    assert set(public_evidence) == {
        "evidence_id",
        "processed_estimate",
        "uncertainty",
        "reward",
    }
    assert "observation" not in public_evidence
    assert direct_prompt["public_experiment_context"]["evidence_catalog"] == [
        "e000-diagnostic-01-hplc"
    ]
    assert direct_plan.scientific_state is None
    assert stateful_plan.scientific_state == _scientific_state()
    assert direct_prompt["scaffold_context"] != stateful_prompt["scaffold_context"]
    state_contract = stateful_prompt["scaffold_context"]["scientific_state_contract"]
    assert set(state_contract["belief"]) == set(_candidate_definitions())
    assert (
        stateful_prompt["scaffold_context"]["scientific_state_constraints"][
            "controlled_variables_max_items"
        ]
        == 10
    )


def test_public_history_window_keeps_reference_and_recent_experiments() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    client = _Client(_base_payload())
    agent = ScientificAdaptationAgent(
        client,
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
        history_limit=4,
    )
    agent.reset(task_info, 0)
    history = []
    for experiment_index in range(6):
        record = _history()[0]
        record["experiment_index"] = experiment_index
        record["measurement_evidence"][0]["evidence_id"] = (
            f"e{experiment_index:03d}-diagnostic-01-hplc"
        )
        history.append(record)

    context = agent.public_context(history)

    assert context["history_window"] == {
        "selection_policy": "oldest_reference_half_plus_most_recent_half",
        "total_experiment_count": 6,
        "included_experiment_indices": [0, 1, 4, 5],
    }
    assert [item["experiment_index"] for item in context["experiment_history"]] == [
        0,
        1,
        4,
        5,
    ]


def test_prompt_budget_fails_before_provider_call() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    client = _Client(_base_payload())
    agent = ScientificAdaptationAgent(
        client,
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
        prompt_token_estimate_cap=500,
    )
    agent.reset(task_info, 0)

    with pytest.raises(PromptBudgetExceededError, match="exceeds cap 500"):
        agent.plan_next(_history())

    assert client.prompts == []
    assert agent.method_resource_usage()["model_call_count"] == 0


@pytest.mark.parametrize(
    ("evidence_summary", "match"),
    [
        (
            [
                {
                    "evidence_id": "not-public",
                    "observation": "x",
                    "interpretation": "y",
                    "reliability": "low",
                }
            ],
            "unknown public evidence ID",
        ),
        (
            [
                {
                    "evidence_id": "e1",
                    "observation": "x",
                    "interpretation": "y",
                    "reliability": "low",
                },
                {
                    "evidence_id": "e1",
                    "observation": "x2",
                    "interpretation": "y2",
                    "reliability": "medium",
                },
            ],
            "must not be duplicated",
        ),
    ],
)
def test_bounded_memory_requires_real_unique_evidence_ids(
    evidence_summary: list[dict[str, str]],
    match: str,
) -> None:
    memory = BoundedScientificMemory(("no_change", "rate_law_family"))
    state = _scientific_state()
    state["evidence_summary"] = evidence_summary
    with pytest.raises(ValueError, match=match):
        memory.write(state, available_evidence_ids={"e1"})


def test_compiler_preserves_conditions_and_adds_only_mechanical_closeout() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    vector = tuple(index / 10 for index in range(task_recipe_dimension(task_info)))
    slots = scientific_measurement_slots(task_info)
    selected = str(slots[-1]["slot_id"])
    plan = ScientificExperimentPlan(
        experiment_intent="run one matched experiment",
        search_vector=vector,
        requested_measurement_slots=(selected,),
        diagnostic_target="late-process response",
        mechanism_distribution={"no_change": 0.5, "rate_law_family": 0.5},
        expected_effect="measurable contrast",
        belief_update_rule="update from the selected diagnostic",
        uncertainty=0.5,
    )

    compiled = compile_scientific_experiment_plan(task_info, plan)
    original = task_recipe_from_unit_vector(task_info, vector)
    expected_steps: list[dict[str, Any]] = []
    diagnostic_index = 0
    for action in original["steps"]:
        if action.get("operation") == "measure" and action.get("instrument") != "final_assay":
            diagnostic_index += 1
            slot_id = f"diagnostic-{diagnostic_index:02d}-{action['instrument']}"
            if slot_id != selected:
                continue
        expected_steps.append(action)

    assert compiled["steps"] == expected_steps
    assert compiled["metadata"]["search_vector"] == list(vector)
    assert compiled["steps"][-2:] == [
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def test_plan_validator_rejects_out_of_range_vector_instead_of_clipping() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    payload = _base_payload()
    payload["search_vector"][0] = 1.1
    agent = ScientificAdaptationAgent(
        _Client(payload),
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
    )
    agent.reset(task_info, 0)
    with pytest.raises(ValueError, match=r"in \[0, 1\]"):
        agent.plan_next([])


def test_invalid_plan_does_not_commit_stateful_memory() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    payload = _base_payload()
    payload["expected_effect"] = ""
    state = _scientific_state()
    state["evidence_summary"] = []
    payload["scientific_state"] = state
    memory = BoundedScientificMemory(tuple(_candidate_definitions()))
    agent = ScientificAdaptationAgent(
        _Client(payload),
        role_id="stateful",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=StatefulScientificScaffoldPolicy(),
        memory_store=memory,
    )
    agent.reset(task_info, 0)

    with pytest.raises(ValueError, match="expected_effect"):
        agent.plan_next([])

    assert memory.read() is None


def test_validation_error_reports_text_length_without_response_content() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    payload = _base_payload()
    secret_content = "private-response-fragment-" * 40
    payload["belief_update_rule"] = secret_content
    agent = ScientificAdaptationAgent(
        _Client(payload),
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
    )
    agent.reset(task_info, 0)

    with pytest.raises(ScientificPlanValidationError) as captured:
        agent.plan_next([])

    error = captured.value
    assert error.validation_diagnostics == {
        "field_path": "belief_update_rule",
        "constraint": "max_characters",
        "observed": len(secret_content),
        "limit": 700,
    }
    assert secret_content not in str(error)
    assert secret_content not in json.dumps(error.validation_diagnostics)


def test_validation_error_reports_empty_nested_field_without_response_content() -> None:
    memory = BoundedScientificMemory(tuple(_candidate_definitions()))
    state = _scientific_state()
    state["evidence_summary"] = []
    state["next_experiment_plan"]["varied_variable"] = "  "

    with pytest.raises(ScientificPlanValidationError) as captured:
        memory.write(state, available_evidence_ids=set())

    assert captured.value.validation_diagnostics == {
        "field_path": "scientific_state.next_experiment_plan.varied_variable",
        "constraint": "non_empty_string",
        "observed": 0,
        "limit": 1,
    }


def test_validation_error_reports_total_state_size_without_state_content() -> None:
    memory = BoundedScientificMemory(tuple(_candidate_definitions()))
    state = _scientific_state()
    evidence_ids = {f"e{index}" for index in range(6)}
    state["evidence_summary"] = [
        {
            "evidence_id": f"e{index}",
            "observation": "o" * 250,
            "interpretation": "i" * 290,
            "reliability": "high",
        }
        for index in range(6)
    ]

    with pytest.raises(ScientificPlanValidationError) as captured:
        memory.write(state, available_evidence_ids=evidence_ids)

    diagnostics = captured.value.validation_diagnostics
    assert diagnostics["field_path"] == "scientific_state"
    assert diagnostics["constraint"] == "max_json_characters"
    assert diagnostics["observed"] > 2_800
    assert diagnostics["limit"] == 2_800
    assert "o" * 250 not in str(captured.value)


def test_validation_error_reports_undeclared_fields_by_count_only() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    payload = _base_payload()
    payload["private-response-fragment"] = "must not be retained"
    agent = ScientificAdaptationAgent(
        _Client(payload),
        role_id="direct",
        candidate_definitions=_candidate_definitions(),
        scaffold_policy=DirectScaffoldPolicy(),
        memory_store=NullScientificMemory(),
    )
    agent.reset(task_info, 0)

    with pytest.raises(ScientificPlanValidationError) as captured:
        agent.plan_next([])

    assert captured.value.validation_diagnostics == {
        "field_path": "experiment_plan_response",
        "constraint": "declared_fields_only",
        "observed": 1,
        "limit": 0,
    }
    assert "private-response-fragment" not in str(captured.value)
