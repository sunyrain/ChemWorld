from __future__ import annotations

import json

from chemworld.agents.prompt_context import build_decision_prompt


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
            "campaign_state": {"remaining_budget": 9, "cost": 0.15},
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
                }
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
    assert prompt["legal_actions"][0]["parameters"][1]["maximum"] == 0.005
    assert "replicate_signals" not in serialized
    assert "391970" in serialized
    assert str(curve[-1]) not in serialized

