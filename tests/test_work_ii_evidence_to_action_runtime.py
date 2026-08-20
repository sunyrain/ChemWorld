from __future__ import annotations

import json
from copy import deepcopy
from types import SimpleNamespace

import pytest

from chemworld.eval.work_ii_evidence_to_action import build_yoked_evidence_packet
from chemworld.eval.work_ii_evidence_to_action_runtime import (
    TERMINAL_SUBMISSION_SCHEMA,
    build_donor_derivatives,
    build_recipient_context,
    execute_stratum,
    execute_terminal_recipient,
    execute_yoked_recipient,
    resolve_dependency_status,
    validate_terminal_submission,
)


def _candidate_packet() -> dict:
    return {
        "candidate_outcomes_included": False,
        "candidates": [
            {
                "query_id": f"q{index}",
                "action_plan": [
                    {"operation": "heat", "target_temperature_K": 300.0 + index},
                    {"operation": "measure", "instrument": "final_assay"},
                ],
            }
            for index in range(8)
        ],
    }


def _yoked_packet() -> dict:
    rows = []
    for experiment in range(1, 13):
        rows.append(
            {
                "action": {"operation": "measure", "instrument": "final_assay"},
                "agent_visible_observation": {
                    "observation": {"score": experiment / 12.0},
                    "observed_reward": experiment / 12.0,
                },
                "observed_keys": ["score"],
                "transaction_status": "committed",
                "rollback_reason": None,
            }
        )
    return build_yoked_evidence_packet(rows, donor_cell_id="donor-1")


def _base_kwargs() -> dict:
    return {
        "task_contract": {"task_id": "test-task", "objective": "maximize score"},
        "initial_world_model": {"arm": "opaque", "nominal_information": None},
        "candidate_packet": _candidate_packet(),
    }


def test_no_evidence_receives_candidates_but_no_evidence_or_artifact() -> None:
    context = build_recipient_context(
        condition="no_evidence",
        stage="terminal_ranking",
        **_base_kwargs(),
    )
    assert len(context["candidate_packet"]) == 8
    assert context["visible_yoked_evidence_rounds"] == []
    assert context["law_artifact"] is None
    assert context["physical_experiment_authority"] is False


def test_yoked_reveal_gate_is_cumulative_and_candidates_are_terminal_only() -> None:
    packet = _yoked_packet()
    after_three = build_recipient_context(
        condition="yoked_evidence",
        stage="after_experiment_3",
        yoked_evidence_packet=packet,
        **_base_kwargs(),
    )
    assert len(after_three["visible_yoked_evidence_rounds"]) == 3
    assert after_three["candidate_packet"] is None

    terminal = build_recipient_context(
        condition="yoked_evidence",
        stage="terminal_ranking",
        yoked_evidence_packet=packet,
        **_base_kwargs(),
    )
    assert len(terminal["visible_yoked_evidence_rounds"]) == 12
    assert len(terminal["candidate_packet"]) == 8


def test_artifact_only_context_rejects_wrong_or_candidate_leaking_artifact() -> None:
    artifact = {
        "artifact_type": "participant_final_typed_law",
        "candidate_information_included": False,
        "law_summary": {"summary_id": "donor-law"},
    }
    context = build_recipient_context(
        condition="learned_law_only",
        stage="terminal_ranking",
        law_artifact=artifact,
        **_base_kwargs(),
    )
    assert context["law_artifact"]["law_summary"]["summary_id"] == "donor-law"
    assert len(context["candidate_packet"]) == 8

    leaking = deepcopy(artifact)
    leaking["candidate_information_included"] = True
    with pytest.raises(ValueError, match="candidate blindness"):
        build_recipient_context(
            condition="learned_law_only",
            stage="terminal_ranking",
            law_artifact=leaking,
            **_base_kwargs(),
        )


def test_public_context_recursively_rejects_hidden_truth() -> None:
    packet = _candidate_packet()
    packet["candidates"][0]["candidate_truth"] = {"score": 1.0}
    with pytest.raises(ValueError, match="forbidden fields"):
        build_recipient_context(
            condition="no_evidence",
            stage="terminal_ranking",
            **{**_base_kwargs(), "candidate_packet": packet},
        )


def test_terminal_submission_requires_complete_permutation_and_first_selection() -> None:
    payload = {
        "schema_version": TERMINAL_SUBMISSION_SCHEMA,
        "ranking": [f"q{index}" for index in range(8)],
        "selected_query_id": "q0",
        "decision_rationale": "q0 best matches the available evidence.",
    }
    parsed = validate_terminal_submission(
        payload,
        candidate_query_ids=[f"q{index}" for index in range(8)],
    )
    assert parsed["selected_query_id"] == "q0"

    invalid = deepcopy(payload)
    invalid["selected_query_id"] = "q1"
    with pytest.raises(ValueError, match="first-ranked"):
        validate_terminal_submission(
            invalid,
            candidate_query_ids=[f"q{index}" for index in range(8)],
        )


def test_terminal_runtime_uses_one_strict_provider_turn() -> None:
    context = build_recipient_context(
        condition="no_evidence",
        stage="terminal_ranking",
        **_base_kwargs(),
    )

    class FakeClient:
        model = "fake-model"

        def __init__(self) -> None:
            self.calls: list[dict] = []

        def complete_json(self, **kwargs):
            self.calls.append(kwargs)
            return SimpleNamespace(
                payload={
                    "schema_version": TERMINAL_SUBMISSION_SCHEMA,
                    "ranking": [f"q{index}" for index in range(8)],
                    "selected_query_id": "q0",
                    "decision_rationale": "The first candidate is preferred.",
                },
                model=self.model,
                request_id="request-1",
                attempts=1,
                usage={"prompt_tokens": 100, "completion_tokens": 20},
            )

    client = FakeClient()
    result = execute_terminal_recipient(client, context)
    assert result["status"] == "completed"
    assert result["submission"]["ranking"][0] == "q0"
    assert len(client.calls) == 1
    assert client.calls[0]["output_schema"]["additionalProperties"] is False
    sent = json.loads(client.calls[0]["user_prompt"])
    assert sent["candidate_outcomes_included"] is False


def test_dependency_resolution_retains_failed_donor_without_replacement() -> None:
    cell = {"dependency_cell_ids": ["donor-1"]}
    assert resolve_dependency_status(cell, {}) == "waiting_for_donor"
    assert (
        resolve_dependency_status(cell, {"donor-1": {"status": "failed_retained"}})
        == "not_started_due_to_missing_donor"
    )
    assert (
        resolve_dependency_status(
            cell,
            {"donor-1": {"status": "completed_uncontaminated"}},
        )
        == "ready"
    )


def test_eligible_donor_builds_only_yoked_evidence_and_final_law() -> None:
    trajectory = []
    for experiment in range(1, 13):
        trajectory.append(
            {
                "action": {"operation": "measure", "instrument": "final_assay"},
                "agent_visible_observation": {
                    "observation": {"score": experiment / 12.0},
                    "observed_reward": experiment / 12.0,
                },
                "observed_keys": ["score"],
                "transaction_status": "committed",
                "rollback_reason": None,
                "agent_trace": "private donor reasoning",
            }
        )
    donor = {
        "status": "completed_uncontaminated",
        "campaign_summary": {
            "analysis": {
                "belief_snapshots": [
                    {
                        "stage": "final",
                        "law_summary": {
                            "schema_version": "chemworld-work-ii-law-summary-0.1",
                            "summary_id": "final-law",
                            "feature_ids": ["temperature"],
                            "metric_laws": [],
                            "evidence_ids": [],
                            "applicability": "candidate domain",
                            "limitations": [],
                            "confidence": 0.8,
                        },
                    }
                ]
            }
        },
    }
    derivatives = build_donor_derivatives(
        donor_cell_id="donor-1",
        donor_result=donor,
        trajectory_rows=trajectory,
        candidate_query_ids=[f"q{index}" for index in range(8)],
    )
    rendered = json.dumps(derivatives)
    assert derivatives["yoked_evidence_packet"]["complete_experiment_count"] == 12
    assert derivatives["learned_law_artifact"]["law_summary"]["summary_id"] == "final-law"
    assert "private donor reasoning" not in rendered


def test_yoked_runtime_runs_five_cumulative_snapshots_then_terminal_ranking() -> None:
    class FakeYokedClient:
        model = "fake-yoked-model"

        def __init__(self) -> None:
            self.contexts: list[dict] = []

        def complete_json(self, **kwargs):
            context = json.loads(kwargs["user_prompt"])
            self.contexts.append(context)
            stage = context["stage"]
            if stage == "terminal_ranking":
                payload = {
                    "schema_version": TERMINAL_SUBMISSION_SCHEMA,
                    "ranking": [f"q{index}" for index in range(8)],
                    "selected_query_id": "q0",
                    "decision_rationale": "The cumulative evidence favors q0.",
                }
            else:
                evidence_ids = [
                    event["evidence_id"]
                    for round_row in context["visible_yoked_evidence_rounds"]
                    for event in round_row["events"]
                ]
                payload = {
                    "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
                    "snapshot_id": f"snapshot-{stage}",
                    "stage": stage,
                    "prior_assessment": {
                        "nominal_information_available": False,
                        "reliability_probability": None,
                        "suspected_misindexed_fields": [],
                        "rationale": "No nominal prior is visible.",
                    },
                    "predictions": [
                        {
                            "query_id": "checkpoint-q",
                            "metrics": [
                                {
                                    "metric_id": "score",
                                    "mean": 0.5,
                                    "interval_lower": 0.2,
                                    "interval_upper": 0.8,
                                    "confidence": 0.7,
                                }
                            ],
                        }
                    ],
                    "law_summary": {
                        "schema_version": "chemworld-work-ii-law-summary-0.1",
                        "summary_id": f"law-{stage}",
                        "feature_ids": ["temperature"],
                        "metric_laws": [
                            {
                                "metric_id": "score",
                                "intercept": 0.5,
                                "link": "identity",
                                "lower_bound": 0.0,
                                "upper_bound": 1.0,
                                "terms": [],
                            }
                        ],
                        "evidence_ids": evidence_ids,
                        "applicability": "registered checkpoint domain",
                        "limitations": [],
                        "confidence": 0.7,
                    },
                    "evidence_ids": evidence_ids,
                    "next_experiment_intent": "Observe the next yoked experiment.",
                    "overall_confidence": 0.7,
                }
            return SimpleNamespace(
                payload=payload,
                model=self.model,
                request_id=f"request-{len(self.contexts)}",
                attempts=1,
                usage={"prompt_tokens": 100, "completion_tokens": 40},
            )

    client = FakeYokedClient()
    result = execute_yoked_recipient(
        client,
        task_contract={"task_id": "test-task", "objective": "maximize score"},
        initial_world_model={"arm": "opaque", "nominal_information": None},
        candidate_packet=_candidate_packet(),
        yoked_evidence_packet=_yoked_packet(),
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        nominal_information_available=False,
    )
    assert result["status"] == "completed"
    assert result["snapshot_count"] == 5
    assert result["provider_call_count"] == 6
    assert result["physical_experiment_count"] == 0
    assert [
        len(context["visible_yoked_evidence_rounds"]) for context in client.contexts
    ] == [0, 3, 6, 9, 12, 12]
    assert [len(context.get("previous_belief_snapshots", [])) for context in client.contexts] == [
        0,
        1,
        2,
        3,
        4,
        5,
    ]


def _stratum_cells() -> list[dict]:
    donor_id = "stratum-1--autonomous_exploration"
    return [
        {
            "cell_id": f"stratum-1--{condition}",
            "stratum_id": "stratum-1",
            "condition": condition,
            "dependency_cell_ids": (
                [donor_id]
                if condition in {"yoked_evidence", "learned_law_only"}
                else []
            ),
        }
        for condition in (
            "no_evidence",
            "yoked_evidence",
            "autonomous_exploration",
            "learned_law_only",
            "oracle_law",
        )
    ]


def _oracle_artifact() -> dict:
    return {
        "artifact_type": "provider_free_disjoint_grid_fitted_predictive_law",
        "candidate_information_included": False,
        "law_summary": {"summary_id": "oracle-law"},
    }


class _StratumClient:
    model = "fake-stratum-model"

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def complete_json(self, **kwargs):
        context = json.loads(kwargs["user_prompt"])
        self.calls.append(context)
        stage = context["stage"]
        if stage == "terminal_ranking":
            payload = {
                "schema_version": TERMINAL_SUBMISSION_SCHEMA,
                "ranking": [f"q{index}" for index in range(8)],
                "selected_query_id": "q0",
                "decision_rationale": "The visible information favors q0.",
            }
        else:
            evidence_ids = [
                event["evidence_id"]
                for round_row in context["visible_yoked_evidence_rounds"]
                for event in round_row["events"]
            ]
            payload = {
                "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
                "snapshot_id": f"snapshot-{stage}",
                "stage": stage,
                "prior_assessment": {
                    "nominal_information_available": False,
                    "reliability_probability": None,
                    "suspected_misindexed_fields": [],
                    "rationale": "No nominal prior is visible.",
                },
                "predictions": [
                    {
                        "query_id": "checkpoint-q",
                        "metrics": [
                            {
                                "metric_id": "score",
                                "mean": 0.5,
                                "interval_lower": 0.2,
                                "interval_upper": 0.8,
                                "confidence": 0.7,
                            }
                        ],
                    }
                ],
                "law_summary": {
                    "schema_version": "chemworld-work-ii-law-summary-0.1",
                    "summary_id": f"law-{stage}",
                    "feature_ids": ["temperature"],
                    "metric_laws": [
                        {
                            "metric_id": "score",
                            "intercept": 0.5,
                            "link": "identity",
                            "lower_bound": 0.0,
                            "upper_bound": 1.0,
                            "terms": [],
                        }
                    ],
                    "evidence_ids": evidence_ids,
                    "applicability": "registered checkpoint domain",
                    "limitations": [],
                    "confidence": 0.7,
                },
                "evidence_ids": evidence_ids,
                "next_experiment_intent": "Observe the next yoked experiment.",
                "overall_confidence": 0.7,
            }
        return SimpleNamespace(
            payload=payload,
            model=self.model,
            request_id=f"request-{len(self.calls)}",
            attempts=1,
            usage={"prompt_tokens": 100, "completion_tokens": 40},
        )


def _completed_donor(_cell: dict) -> dict:
    trajectory = [
        {
            "action": {"operation": "measure", "instrument": "final_assay"},
            "agent_visible_observation": {
                "observation": {"score": experiment / 12.0},
                "observed_reward": experiment / 12.0,
            },
            "observed_keys": ["score"],
            "transaction_status": "committed",
            "rollback_reason": None,
        }
        for experiment in range(1, 13)
    ]
    return {
        "status": "completed_uncontaminated",
        "physical_experiment_count": 12,
        "provider_call_count": 4,
        "participant_ranking": [f"q{index}" for index in range(8)],
        "trajectory_rows": trajectory,
        "campaign_summary": {
            "analysis": {
                "belief_snapshots": [
                    {
                        "stage": "final",
                        "law_summary": {
                            "schema_version": "chemworld-work-ii-law-summary-0.1",
                            "summary_id": "learned-law",
                            "feature_ids": ["temperature"],
                            "metric_laws": [],
                            "evidence_ids": [],
                            "applicability": "candidate domain",
                            "limitations": [],
                            "confidence": 0.7,
                        },
                    }
                ]
            }
        },
    }


def test_stratum_orchestrator_executes_all_conditions_after_eligible_donor() -> None:
    client = _StratumClient()
    result = execute_stratum(
        client,
        cells=_stratum_cells(),
        autonomous_executor=_completed_donor,
        task_contract={"task_id": "test-task", "objective": "maximize score"},
        initial_world_model={"arm": "opaque", "nominal_information": None},
        candidate_packet=_candidate_packet(),
        oracle_law_artifact=_oracle_artifact(),
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        nominal_information_available=False,
    )
    assert result["status"] == "completed"
    assert len(result["cell_results"]) == 5
    assert result["provider_call_count"] == 13
    assert result["participant_physical_experiment_count"] == 12
    assert result["blocked_cell_ids"] == []
    assert len(client.calls) == 9


def test_stratum_orchestrator_retains_failed_donor_descendants_without_calls() -> None:
    client = _StratumClient()

    def failed_donor(_cell: dict) -> dict:
        return {
            "status": "failed_retained",
            "physical_experiment_count": 3,
            "provider_call_count": 2,
        }

    result = execute_stratum(
        client,
        cells=_stratum_cells(),
        autonomous_executor=failed_donor,
        task_contract={"task_id": "test-task", "objective": "maximize score"},
        initial_world_model={"arm": "opaque", "nominal_information": None},
        candidate_packet=_candidate_packet(),
        oracle_law_artifact=_oracle_artifact(),
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        nominal_information_available=False,
    )
    assert result["status"] == "completed_with_failed_donor_dependencies_retained"
    assert len(result["cell_results"]) == 5
    assert len(result["blocked_cell_ids"]) == 2
    assert result["provider_call_count"] == 4
    assert result["participant_physical_experiment_count"] == 3
    assert len(client.calls) == 2
