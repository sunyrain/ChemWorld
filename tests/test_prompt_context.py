from __future__ import annotations

import json

from chemworld.agents.prompt_context import (
    build_decision_prompt,
    serialize_prompt_payload,
)


def test_compact_prompt_is_decision_first_and_excludes_raw_arrays() -> None:
    curve = [index / 100 for index in range(241)]
    packet = build_decision_prompt(
        task_contract={
            "task_id": "reaction-to-crystallization",
            "task_goal": "Recover performance and diagnose a changed relation.",
            "method_budget_contract": {
                "operation_limit": 12,
                "complete_experiment_limit": 8,
            },
            "experiment_lifecycle": {
                "terminate_effect": "Close synthesis; it does not complete the experiment.",
                "final_assay_precondition": "Measure final_assay after termination.",
            },
        },
        decision_context={
            "step": 3,
            "decision_stage": "evidence_update",
            "campaign_state": {
                "remaining_budget": 9,
                "cost": 0.15,
                "diagnostic_actions_used_current_experiment": 7,
                "diagnostic_per_experiment_action_limit": 18,
            },
            "visible_metrics": {"yield": 0.015, "selectivity": 0.0},
            "latest_spectra": {
                "has_spectral_packet": True,
                "spectrum_id": "spectrum-e001-s0003",
                "raw_signal": {
                    "kind": "hplc_chromatogram",
                    "time_min": curve,
                    "intensity": list(reversed(curve)),
                    "replicate_signals": [curve, curve],
                    "peaks": [
                        {
                            "retention_time_min": 1.14,
                            "assignment": "reactant",
                            "area": 391970,
                        },
                        {
                            "retention_time_min": 2.64,
                            "assignment": "target",
                            "area": 5903,
                        },
                    ],
                },
                "processed_estimate": {
                    "reactant_fraction": 0.978,
                    "target_fraction": 0.015,
                },
            },
            "historical_spectrum_catalog": (
                {
                    "spectrum_id": "spectrum-e001-s0003",
                    "instrument": "hplc",
                    "measurement_step": 3,
                },
            ),
            "constraint_flags": {"low_selectivity": True},
        },
        tool_json={
            "available_actions": [
                {
                    "operation": "add_catalyst",
                    "schema": {
                        "required_fields": ["catalyst", "amount_mol"],
                        "fields": [
                            {"field": "catalyst", "choices": [0, 1, 2, 3]},
                            {
                                "field": "amount_mol",
                                "minimum": 0.0,
                                "maximum": 0.005,
                                "unit": "mol",
                            },
                        ],
                    },
                },
                {
                    "operation": "terminate",
                    "valid": False,
                    "invalid_reasons": ["terminate_requires_material"],
                    "schema": {"required_fields": [], "fields": []},
                },
            ]
        },
        experiment_memory=[],
        recent_decisions=[],
        max_estimated_tokens=1500,
    )

    prompt = json.loads(packet.text)
    serialized = json.dumps(prompt)
    assert packet.estimated_tokens <= 1500
    assert prompt["decision_state"]["latest_measurement"]["peaks"][0][
        "assignment"
    ] == "reactant"
    assert prompt["on_demand_detail"]["historical_spectrum_catalog"][0][
        "spectrum_id"
    ] == "spectrum-e001-s0003"
    assert prompt["decision_state"]["current_experiment"][
        "diagnostic_actions_used_current_experiment"
    ] == 7
    assert prompt["decision_state"]["current_experiment"][
        "diagnostic_per_experiment_action_limit"
    ] == 18
    assert prompt["decision_state"]["lifecycle"] == {
        "closeout_status": "not_started",
        "experiment_action_count": 7,
        "experiment_action_limit": 18,
        "experiment_terminated": False,
        "final_assay_available": False,
        "ordinary_action_slots_remaining": 9,
        "reserved_closeout_slots": 2,
    }
    legal = prompt["legal_actions"][0]
    assert legal["operation"] == "add_catalyst"
    assert "parameters" not in legal
    assert legal["amount_mol"]["maximum"] == 0.005
    assert legal["catalyst"]["choices"] == [0, 1, 2, 3]
    assert [item["operation"] for item in prompt["legal_actions"]] == [
        "add_catalyst"
    ]
    assert "direct sibling" in prompt["instruction"]
    assert "replicate_signals" not in serialized
    assert "391970" in serialized
    assert str(curve[-1]) not in serialized


def test_budget_reduction_keeps_prior_belief_and_drops_repeated_context() -> None:
    packet = serialize_prompt_payload(
        {
            "instruction": "Choose one legal action.",
            "decision_state": {
                "latest_metrics": {"yield": 0.2},
                "latest_measurement": {
                    "processed_estimate": {"yield": 0.2},
                    "peaks": [
                        {"assignment": f"peak-{index}", "area": index}
                        for index in range(8)
                    ],
                },
                "uncertainty": {"yield_std": 0.01},
            },
            "recent_decisions": [
                {
                    "action": {"operation": "measure", "instrument": "hplc"},
                    "expected_effect": "x" * 1_000,
                    "diagnostic_target": "y" * 500,
                    "mechanism_distribution": {
                        "no_change": 0.4,
                        "rate_law_family": 0.4,
                        "topology_family": 0.1,
                        "material_law_counterfactual": 0.1,
                    },
                    "declared_information_value": 0.4,
                    "uncertainty": 0.8,
                }
            ],
            "experiment_memory": {"historical_best": None, "recent": []},
            "on_demand_detail": {"historical_spectrum_catalog": []},
            "legal_actions": [{"operation": "terminate"}],
        },
        max_estimated_tokens=500,
    )

    previous = packet.payload["recent_decisions"][0]
    assert packet.estimated_tokens <= 500
    assert previous["mechanism_distribution"]["rate_law_family"] == 0.4
    assert "action" not in previous
    assert "expected_effect" not in previous
    assert "processed_estimate" not in packet.payload["decision_state"][
        "latest_measurement"
    ]
    assert len(packet.payload["decision_state"]["latest_measurement"]["peaks"]) == 2


def test_budget_reduction_projects_audited_scientific_state() -> None:
    packet = serialize_prompt_payload(
        {
            "instruction": "Choose one legal action.",
            "decision_state": {},
            "recent_decisions": [],
            "legal_actions": [{"operation": "measure"}],
            "prior_scientific_state": {
                "current_question": "q" * 140,
                "campaign_plan": [
                        {
                            "step": "Measure the controlled response.",
                            "purpose": "p" * 800,
                        "status": "active",
                    }
                ],
                "mechanism_distribution": {
                    "no_change": 0.4,
                    "rate_law_family": 0.4,
                    "topology_family": 0.1,
                    "material_law_counterfactual": 0.1,
                },
                "evidence_ledger": [
                    {
                        "evidence_id": "experiment-1",
                        "supports": ["rate_law_family"],
                        "contradicts": ["no_change"],
                        "interpretation": "i" * 800,
                    }
                ],
                "replan_trigger": "r" * 100,
                "uncertainty": 0.5,
            },
            "required_json_shape": {"scientific_state": "full state"},
        },
        max_estimated_tokens=500,
    )

    prior = packet.payload["prior_scientific_state"]
    assert packet.estimated_tokens <= 500
    assert "current_question" not in prior
    assert prior["current_plan_step"] == "Measure the controlled response."
    assert prior["latest_evidence"]["supports"] == ["rate_law_family"]
    assert "replan_trigger" not in prior
    assert prior["mechanism_distribution"]["no_change"] == 0.4
