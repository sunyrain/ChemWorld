from __future__ import annotations

import json

from scripts.run_work_ii_campaign_pilot import _campaign_card

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.interactive_codex_experiment import (
    _CAMPAIGN_SYSTEM_PROMPT,
    _bounded_current_packet,
    _initial_prompt,
)


def _config() -> dict[str, object]:
    return {
        "pilot_id": "recipe-coverage-test",
        "task_id": "electrochemical-conversion",
        "campaign": {
            "complete_experiments": 8,
            "operation_attempt_limit": 56,
            "vessel_start_limit": 8,
            "final_assay_limit": 8,
            "nonfinal_instrument_use_limit": 0,
            "stock_limits": {"solvent_L": 1.0},
            "process_time_limit_s": 1000.0,
            "operation_repeat_limits": {"electrolyze": 8},
            "process_time_policy": {"pattern_id": "test-pattern"},
            "closeout_policy": {"planned_batches": 8},
        },
        "qualification": {
            "minimum_unique_recipes": 6,
            "maximum_exact_repeats": 2,
        },
    }


def test_campaign_card_exposes_recipe_coverage_identity_and_denominators() -> None:
    contract = _campaign_card(_config()).to_dict()["metadata"][
        "recipe_coverage_contract"
    ]

    assert contract["target_complete_experiments"] == 8
    assert contract["minimum_unique_recipes"] == 6
    assert contract["maximum_exact_repeats"] == 2
    identity = contract["recipe_identity_semantics"]
    assert identity["unit"] == "completed_experiment"
    assert identity["rejected_or_rolled_back_attempts_included"] is False
    assert "ordered committed lab action objects" in identity["identity_basis"]


def test_campaign_prompt_and_each_public_packet_keep_coverage_obligation_visible() -> None:
    contract = _campaign_card(_config()).to_dict()["metadata"][
        "recipe_coverage_contract"
    ]
    task_contract = {
        "campaign_resources": {
            "card": {"metadata": {"recipe_coverage_contract": contract}}
        }
    }
    prompt = json.loads(
        _initial_prompt(
            task_contract=task_contract,
            task_contract_manifest={},
            current_packet={},
            material_manifest={},
            session_scope="campaign",
        )
    )
    assert prompt["recipe_coverage_contract"] == contract
    assert "hard qualification obligation" in prompt["instruction"]

    context = AgentDecisionContext(
        step=1,
        task_id="electrochemical-conversion",
        decision_stage="before_operation",
        campaign_state={"remaining_budget": 56, "experiment_summaries": []},
        visible_metrics={},
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=(),
        previous_event_type=None,
    )
    packet = _bounded_current_packet(
        context,
        {"tool_json": {"available_actions": []}},
        artifact=None,
        recipe_coverage_contract=contract,
    )
    assert packet["recipe_coverage_contract"] == contract
    assert "Recipe coverage is a hard campaign qualification obligation" in (
        _CAMPAIGN_SYSTEM_PROMPT
    )
