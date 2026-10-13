import pytest
from scripts import finish_research_extension as finish
from scripts import report_research_extension as report
from scripts.run_paper_case_notebooks import read, write
from scripts.run_research_extension import full_cases


def test_world_equal_three_arm_statistics_keep_missing_sessions():
    rows = []
    for c in full_cases():
        for repeat in range(3):
            value = {"Opaque": 0.1, "Aligned": 0.2, "MisIndexed": 0.3}[c["arm"]]
            if c["world"] == "W01" and c["arm"] == "MisIndexed":
                value = None if repeat == 0 else 0.9
            rows.append({**c, "measurements": {"lowest_three_macro_mae": value}})
    result = report.contrasts(rows)["EQ"]["lowest_three_macro_mae"]
    assert result["worlds"][0]["MisIndexed"]["observed"] == 2
    assert result["worlds"][0]["MisIndexed"]["planned"] == 3
    assert result["equal_world_means"]["MisIndexed"]["mean"] == pytest.approx(0.42)
    assert result["paired_world_differences"]["MisIndexed_minus_Opaque"]["mean"] == pytest.approx(
        0.32
    )


def test_pending_sources_do_not_count_as_failed_or_completed():
    rows = [{**c, "status": "pending"} for c in full_cases() for _ in range(3)]
    result = report.counts(rows)
    assert result["planned_sources"] == 90
    assert result["planned_batches"] == 1080
    assert result["planned_posttests"] == 315
    assert result["terminal_sources"] == result["valid_Q"] == result["complete_chains"] == 0


def test_final_export_rejects_changed_outcome_and_unfinished_quench(tmp_path):
    root, parent, output = tmp_path / "raw", tmp_path / "parent", tmp_path / "out"
    unit = {"repeat": "repeat-01", "id": "EQ-W01-MisIndexed"}
    write(
        root / "design.json",
        {"parent_root": str(parent), "parent_schedule": [], "schedule": [unit]},
    )
    write(
        root / unit["repeat"] / "results" / f"{unit['id']}.json",
        {"status": "failed", "source": {"batches": []}, "prediction_evaluation": None},
    )
    target = output / unit["repeat"] / f"{unit['id']}.json"
    write(target, {"status": "completed", "completed_batches": 0, "prediction_evaluation": None})
    analysis = {
        "counts": {"terminal_sources": 90},
        "quench": {"completed_trajectories": 180, "completed_pairs": 90, "block_stop": None},
    }
    with pytest.raises(ValueError, match="changed retained outcome"):
        finish.validate(root, output, analysis)
    row = read(target)
    row["status"] = "failed"
    write(target, row)
    finish.validate(root, output, analysis)
    analysis["quench"]["completed_trajectories"] = 178
    with pytest.raises(ValueError, match="not completed"):
        finish.validate(root, output, analysis)
