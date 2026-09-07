from copy import deepcopy

import pytest
from scripts.summarize_work_ii_information_models import combine


def reports():
    result = {}
    for model in ("gpt", "deepseek"):
        rows = []
        for world in range(10):
            for arm in ("opaque", "aligned_nominal", "misindexed_nominal"):
                for info in ("original", "complete"):
                    success = int(
                        arm == "aligned_nominal"
                        or (info == "complete" and (world % 2 == 0) == (model == "gpt"))
                    )
                    rows.append(
                        {
                            "cluster_id": str(world),
                            "arm": arm,
                            "information": info,
                            "model": model,
                            "status": "completed",
                            "joint_recovery": success,
                            "normalized_regret": 0,
                            "top1": 1,
                            "tool_used": False,
                        }
                    )
        result[model] = {
            "formal_result": True,
            "status": "terminal",
            "scheduled": 60,
            "worlds": 10,
            "rows": rows,
            "provider": {},
            "budgets": {},
            "resources": {},
            "primary": {"bootstrap_seed": 90870, "bootstrap_draws": 20000},
        }
    return result


def test_shared_worlds_are_resampled_together():
    # Model-specific effects vary, but their within-world average is always 0.5.
    # Treating the models as twenty independent worlds would invent uncertainty.
    report = combine(reports())
    assert report["worlds"] == 10 and report["scheduled"] == 120
    assert report["primary"]["mean"] == 0.5
    assert report["primary"]["approximate_world_bootstrap_95"] == [0.5, 0.5]
    assert all(g["scheduled"] == 20 for g in report["groups"] if g["analysis"] == "recovery")


def test_terminal_failures_are_retained_and_partial_blocks_rejected():
    data = reports()
    row = data["deepseek"]["rows"][0]
    row.update(status="failed", failure="provider_failure", joint_recovery=0, normalized_regret=1)
    report = combine(data)
    assert report["counts"] == {"failed": 1, "completed": 119}
    assert len(report["failures"]) == 1
    original = deepcopy(data)
    data["deepseek"]["status"] = "incomplete"
    with pytest.raises(ValueError, match="terminal"):
        combine(data)
    original["deepseek"]["rows"].append(original["deepseek"]["rows"][0])
    with pytest.raises(ValueError, match="coverage"):
        combine(original)


def test_combined_report_retains_actual_budgets_and_schedule_amendments():
    data = reports()
    data["deepseek"].update(
        budgets={"block_timeout_s": 43200, "turn_timeout_s": 600},
        effective_budgets={"block_timeout_s": None, "turn_timeout_s": 600},
        schedule_amendment={"effective_deadline_epoch": None},
        parallel_schedule_amendment={"requested_workers": 3, "first_unstarted_session": 22},
    )
    report = combine(data)
    assert report["budgets"]["deepseek"]["block_timeout_s"] == 43200
    assert report["effective_budgets"]["deepseek"] == {
        "block_timeout_s": None,
        "turn_timeout_s": 600,
    }
    assert report["effective_budgets"]["gpt"] == data["gpt"]["budgets"]
    assert report["execution_schedule_amendments"]["deepseek"] == {
        "schedule_amendment": data["deepseek"]["schedule_amendment"],
        "parallel_schedule_amendment": data["deepseek"]["parallel_schedule_amendment"],
    }
    assert report["execution_schedule_amendments"]["gpt"] == {}
