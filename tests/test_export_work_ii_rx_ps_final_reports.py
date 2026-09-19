import json
from pathlib import Path

import scripts.export_work_ii_rx_ps_final_reports as export


def test_public_result_whitelists_posttest_payloads_without_provider_metadata() -> None:
    result = {
        "cell_id": "RX-W01--P--mechanism_discovery--Opaque",
        "world_id": "RX-W01",
        "world_seed": 0,
        "locus": "P",
        "goal": "mechanism_discovery",
        "arm": "Opaque",
        "status": "completed",
        "source_status": "completed",
        "operations": 7,
        "posttest_chain_sealed": True,
        "batches": [{"ordinal": 1, "metrics": {"score": 0.5}}],
        "recommendation": {"selected_experiment_index": 1},
        "exact_replay": {"verified": True},
        "rollbacks": [],
        "posttests": {
            stage: {
                "payload": {"report": stage},
                "thread_id": "private-thread",
                "provider_errors": ["private-error"],
            }
            for stage in export.STAGES
        },
        "posttest_validation": {stage: {"valid": True} for stage in export.STAGES},
    }
    public = export.public_result(
        Path("result.json"),
        result,
        {"valid": True, "metrics": {}},
        {"Q01": [{"score": 0.5}]},
        {"batches": [{"metrics": {"score": 0.6}}], "failure": None},
    )
    serialized = json.dumps(public)

    assert public["posttests"]["K1"]["payload"] == {"report": "K1"}
    assert "private-thread" not in serialized
    assert "private-error" not in serialized
    assert "thread_id" not in serialized
    assert "provider_errors" not in serialized


def test_render_final_report_replaces_interim_scope_and_adds_final_evidence() -> None:
    result = {
        "cell_id": "RX-W01--P--mechanism_discovery--Opaque",
        "world_id": "RX-W01",
        "world_seed": 0,
        "locus": "P",
        "goal": "mechanism_discovery",
        "arm": "Opaque",
        "status": "completed",
        "source_status": "completed",
        "operations": 7,
        "rollbacks": [],
        "posttest_chain_sealed": True,
        "exact_replay": {"verified": True},
        "recommendation": {"selected_experiment_index": 1, "selection_rationale": "best"},
        "batches": [
            {
                "ordinal": 1,
                "lifecycle_index": 1,
                "end_step": 7,
                "actions": [],
                "metrics": {"score": 0.5},
            }
        ],
        "posttest_validation": {stage: {"valid": True} for stage in export.STAGES},
        "posttests": {
            "K1": {"payload": {"report": "mechanism"}},
            "Q": {
                "payload": {
                    "rationale": "prediction",
                    "predictions": [
                        {
                            "query_id": "Q01",
                            "rationale": "r",
                            "metrics": {
                                "score": {"estimate": 0.5, "lower80": 0.4, "upper80": 0.6}
                            },
                        }
                    ],
                }
            },
            "K2": {"payload": {"report": "retrospective"}},
        },
    }
    evaluation = {
        "valid": True,
        "metrics": {
            "score": {
                "mae_to_five_repeat_mean": 0.1,
                "empirical_coverage80": 0.8,
                "mean_width80": 0.2,
                "mean_interval_score_alpha_0_2": 0.3,
            }
        },
    }
    truth = {"Q01": [{"score": 0.5}] * 5}
    retest = {
        "batches": [{"metrics": {"score": 0.6}}],
        "exact_replay": {"verified": True},
        "failure": None,
    }

    report = export.render_final_report(Path("result.json"), result, evaluation, truth, retest)

    assert "Blind-prediction evaluation" in report
    assert "Predictions versus released reference truth" in report
    assert "Recommendation retest" in report
    assert "full 60-task block has not yet completed" not in report
    assert "final sanitized report" in report


def test_render_aggregate_report_groups_five_worlds() -> None:
    rows = []
    for world in export.EXPECTED_WORLDS:
        for locus in ("P", "S"):
            for goal in ("mechanism_discovery", "safety_constrained_optimization"):
                for arm in ("Opaque", "Aligned", "MisIndexed"):
                    rows.append(
                        {
                            "cell_id": f"{world}--{locus}--{goal}--{arm}",
                            "world_id": world,
                            "locus": locus,
                            "goal": goal,
                            "arm": arm,
                            "selected_source_score": 0.5,
                            "recommendation_retest_score": 0.6,
                            "recommendation_score_delta": 0.1,
                            "prediction_macro_mae": 0.2,
                            "prediction_macro_coverage80": 0.8,
                            "prediction_macro_interval_score": 0.3,
                        }
                    )
    completion = {
        "source_sessions": 60,
        "source_batches": 720,
        "posttests": 180,
        "reference_executions": 600,
        "recommendation_retests": 60,
    }

    report = export.render_aggregate_report(rows, completion)

    assert "Aggregate by locus, task, and prior arm" in report
    assert "| P | mechanism_discovery | Opaque | 5 |" in report
    assert "| RX-W05 | 12 |" in report
    assert "Highest independent recommendation retests" in report
