"""PA prediction scoring and measurement-stage regression checks."""

import json

from scripts.run_work_ii_pa_single_trial import (
    METRICS,
    SYSTEM,
    evaluate,
    observations,
    queries,
    resource_card,
    source_system,
    token_accounting,
)

from chemworld.agents.interactive_codex_experiment import _initial_prompt


def test_partition_measurement_before_removal_is_not_replaced_by_terminal_zero():
    records = [
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "instrument": "hplc",
            "processed_estimate": {"product_in_aqueous": 0.6},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "action": {"operation": "separate_phase"},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "instrument": "final_assay",
            "processed_estimate": {"product_in_aqueous": 0.0},
        },
        {
            "experiment_index": 1,
            "transaction_status": "committed",
            "instrument": "hplc",
            "processed_estimate": {"product_in_aqueous": 0.4},
        },
    ]
    rows = observations(records)
    assert [r["before_phase_removal"] for r in rows] == [True, False, True]
    assert rows[0]["values"]["product_in_aqueous"] == 0.6


def test_prediction_scoring_preserves_errors_and_rejects_duplicate_queries():
    truth = {q["query_id"]: dict.fromkeys(METRICS, 0.5) for q in queries()}
    payload = {
        "predictions": [
            {
                "query_id": q,
                **{k: {"estimate": 0.6, "lower90": 0.55, "upper90": 0.65} for k in METRICS},
            }
            for q in truth
        ],
        "D1_phase": "uncertain",
        "D2_query": "uncertain",
    }
    result = evaluate(payload, truth)
    assert result["valid"]
    assert result["metrics"][METRICS[0]]["coverage90"] == 0
    assert result["metrics"][METRICS[0]]["interval_score90"] > 1
    payload["predictions"][-1] = payload["predictions"][0]
    assert not evaluate(payload, truth)["valid"]


def test_twenty_four_budget_scales_measurement_and_operation_envelopes():
    card = resource_card(24)
    assert card.vessel_start_limit == card.final_assay_limit == 24
    assert card.nonfinal_instrument_use_limit == 24
    assert card.operation_attempt_limit == 720
    assert card.process_time_limit_s is None
    assert source_system(12) == SYSTEM
    assert "Conduct 24 independent batches" in source_system(24)
    assert "24 additional instrument uses" in source_system(24)
    assert len(queries()) == 12  # Prediction denominator is independent of research budget.


def test_free_research_prompt_does_not_override_twenty_four_with_twelve():
    prompt = json.loads(
        _initial_prompt(
            task_contract={
                "free_research_campaign": True,
                "final_recommendation_required": False,
                "study_budget": {"complete_batches": 24},
            },
            task_contract_manifest={},
            current_packet={},
            material_manifest={},
            session_scope="campaign",
        )
    )
    assert prompt["task"]["study_budget"]["complete_batches"] == 24
    assert "12" not in prompt["instruction"]
    assert "no operating recommendation is required" in prompt["instruction"]
    assert prompt["belief_checkpoint_contract"] is None


def test_token_totals_do_not_sum_cumulative_followup_snapshots():
    result = {
        "source": {
            "usage": {
                "provider_token_accounting_complete": True,
                "input_token_count": 100,
                "cached_input_token_count": 80,
                "output_token_count": 10,
            }
        },
        "posttests": {
            stage: {
                "usage": {
                    "input_tokens": value,
                    "cached_input_tokens": cache,
                    "output_tokens": output,
                }
            }
            for stage, value, cache, output in (
                ("K1", 150, 100, 20),
                ("Q", 300, 200, 50),
                ("K2", 400, 270, 60),
            )
        },
    }
    usage = token_accounting(result)
    assert usage["complete"]
    assert usage["total"] == {
        "input": 400,
        "cached_input": 270,
        "output": 60,
        "uncached_input": 130,
        "input_plus_output": 460,
    }
    assert [r["input"] for r in usage["stages"]] == [100, 50, 150, 100]
    result["posttests"]["Q"]["usage"]["input_tokens"] = 50
    assert not token_accounting(result)["valid"]
