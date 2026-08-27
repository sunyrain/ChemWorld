from __future__ import annotations

from chemworld.eval.work_ii_reviewer_controls import analyze_w2_50


def test_w2_50_analysis_keeps_failures_and_threshold_denominators() -> None:
    rows = []
    for task_index, task in enumerate(("electrochemical", "crystallization", "safety")):
        for world in range(5):
            for arm_index, arm in enumerate(("opaque", "aligned", "misindexed")):
                rows.append(
                    {
                        "cell_id": f"cell-{task}-{world}-{arm}",
                        "cluster_id": f"study--{task}--seed{world}",
                        "world_seed": world,
                        "arm": arm,
                        "status": "completed_uncontaminated",
                        "law_normalized_mae": 0.02 * (arm_index + world + 1),
                        "normalized_regret": 0.01 * (task_index + arm_index + world),
                        "selected_rank": 1 + ((task_index + arm_index + world) % 8),
                        "top1_selected": (task_index + arm_index + world) % 4 == 0,
                    }
                )
    for index in range(3):
        rows[-(index + 1)]["status"] = "failed_retained"
    result = analyze_w2_50({"cell_rows": rows}, bootstrap_replicates=20, seed=7)
    assert result["scheduled_cell_count"] == 45
    assert result["eligible_cell_count"] == 42
    assert result["retained_failure_count"] == 3
    for threshold in result["threshold_sensitivity"]:
        assert sum(value for key, value in threshold.items() if key.endswith("_action")) == 42
