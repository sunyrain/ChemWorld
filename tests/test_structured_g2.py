from __future__ import annotations

import json
from typing import Any

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.structured_g2 import StructuredG2Agent
from chemworld.providers.deepseek import JsonCompletion


class _StrictClient:
    model = "gpt-5.6-sol"
    thinking = True
    reasoning_effort = "medium"
    strict_tool_calls = True

    def __init__(self) -> None:
        self.prompts: list[dict[str, Any]] = []
        self.schemas: list[dict[str, Any]] = []

    def pricing_snapshot(self) -> dict[str, Any]:
        return {
            "provider": "WellAU",
            "model_access_date": "2026-08-01",
            "accounting_complete": False,
        }

    def complete_json(self, **kwargs: Any) -> JsonCompletion:
        self.prompts.append(json.loads(kwargs["user_prompt"]))
        self.schemas.append(dict(kwargs["output_schema"]))
        usage = {
            "prompt_tokens": 600,
            "completion_tokens": 80,
            "total_tokens": 680,
        }
        return JsonCompletion(
            payload={
                "action": {
                    "operation": "add_solvent",
                    "solvent": 1,
                    "volume_L": 0.04,
                },
                "expected_effect": "Start a bounded nominal solvent batch.",
                "diagnostic_target": "Nominal solvent prior",
                "expected_information_gain": 0.4,
                "belief_update_rule": {
                    "if_supported": "Retain this solvent family.",
                    "if_not_supported": "Challenge another solvent.",
                },
                "uncertainty": 0.6,
                "request_historical_spectrum_id": None,
            },
            model=self.model,
            usage=usage,
            request_id="request-1",
            attempts=1,
            attempt_records=(
                {
                    "attempt_index": 1,
                    "status": "succeeded",
                    "request_id": "request-1",
                    "model_id": self.model,
                    "usage": usage,
                    "usage_source": "provider_response",
                    "usage_complete": False,
                    "billable": True,
                    "failure_type": None,
                },
            ),
        )


class _JsonObjectClient(_StrictClient):
    strict_tool_calls = False


def test_structured_g2_uses_strict_schema_and_public_campaign_ledger() -> None:
    client = _StrictClient()
    agent = StructuredG2Agent(
        client,
        role_id="test",
        prompt_token_estimate_cap=3200,
        response_max_tokens=1800,
    )
    agent.reset(
        {
            "task_id": "electrochemical-conversion",
            "objective": "balanced",
            "budget": 24,
            "episode_mode": "campaign",
            "electrochemical_workflow_mode": "autonomous_open_v1",
            "material_information": {"mode": "anonymous_nominal_properties"},
            "material_catalog": {
                "solvents": [
                    {"anonymous_material_id": "solvent-S1", "index": 1}
                ]
            },
            "scoring_contract": {"contract_id": "score-v2"},
        },
        seed=0,
    )
    context = AgentDecisionContext(
        step=1,
        task_id="electrochemical-conversion",
        decision_stage="experiment_setup",
        campaign_state={
            "remaining_budget": 24,
            "experiment_index": 0,
            "campaign_resources": {
                "ledger_sha256": "ledger",
                "state": {
                    "operation_attempts": 0,
                    "vessel_starts": 0,
                    "remaining": {
                        "operation_attempts": 24,
                        "vessel_starts": 4,
                        "final_assays": 4,
                        "stocks": {"solvent_L": 0.16, "reagent_mol": 0.08},
                    },
                },
                "lifecycle_reserve": {
                    "remaining_operation_attempts": 24,
                    "future_unstarted_batches": 3,
                    "recommended_remaining_attempt_floor": {
                        "to_final_assay_all_planned_batches": 24
                    },
                },
            },
        },
        visible_metrics={"score": 0.0},
        latest_spectra={"has_spectral_packet": False},
        uncertainty={},
        constraint_flags={},
        available_operations=("add_solvent",),
        previous_event_type=None,
    )
    view = {
        "tool_json": {
            "available_actions": [
                {
                    "operation": "add_solvent",
                    "valid": True,
                    "schema": {
                        "schema_version": "chemworld-public-action-affordance-0.2",
                        "operation": "add_solvent",
                        "valid_operation_type": True,
                        "task_allowed": True,
                        "required_fields": ["solvent", "volume_L"],
                        "fields": [
                            {
                                "field": "solvent",
                                "required": True,
                                "choices": [0, 1, 2, 3],
                            },
                            {
                                "field": "volume_L",
                                "required": True,
                                "bounds": {"low": 0.0, "high": 0.08},
                                "lower_bound_inclusive": False,
                                "upper_bound_inclusive": True,
                            },
                        ],
                    },
                }
            ]
        }
    }

    action = agent.act_with_public_view(context, view)

    assert action == {"operation": "add_solvent", "solvent": 1, "volume_L": 0.04}
    prompt = client.prompts[0]
    assert prompt["task"]["material_information"]["mode"] == (
        "anonymous_nominal_properties"
    )
    assert prompt["decision_state"]["campaign_resources"]["remaining"][
        "operation_attempts"
    ] == 24
    assert client.schemas[0]["additionalProperties"] is False
    assert agent.manifest()["lab_tool_used"] is False
    assert agent.manifest()["shell_tools_enabled"] is False
    assert "provider_enforced" in agent.manifest()["structured_output_policy"]


def test_structured_g2_declares_local_validation_for_json_object_transport() -> None:
    agent = StructuredG2Agent(
        _JsonObjectClient(),
        role_id="test-json-object",
        prompt_token_estimate_cap=3200,
        response_max_tokens=1800,
    )
    agent.reset(
        {
            "task_id": "electrochemical-conversion",
            "objective": "balanced",
            "budget": 24,
            "episode_mode": "campaign",
        },
        seed=0,
    )

    manifest = agent.manifest()
    resources = agent.method_resource_usage()

    assert manifest["structured_output_policy"] == (
        "json_object_plus_locally_validated_dynamic_json_schema"
    )
    assert resources["model_provenance"]["request_parameters"]["response_format"] == (
        "json_object_plus_local_dynamic_schema_validation"
    )
