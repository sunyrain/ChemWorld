from __future__ import annotations

import json

import pytest

from chemworld.eval.baseline_report import (
    generate_baseline_report,
    maturity_summary_for_results,
    validate_result_maturity_consistency,
)
from chemworld.eval.runner import make_agent, run_agent


def test_baseline_runner_smoke(tmp_path) -> None:
    output = tmp_path / "random.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=3,
        output_path=output,
    )
    assert len(history) == 4
    assert output.exists()
    assert output.read_text(encoding="utf-8").count("\n") == 4
    first_record = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
    assert first_record["physics_maturity"] in {
        "proxy",
        "lite",
        "reference_validated",
        "professional_candidate",
        "professional",
    }
    assert "modules" in first_record["kernel_maturity"]
    assert isinstance(first_record["proxy_allowed"], bool)


def test_greedy_runner_smoke(tmp_path) -> None:
    output = tmp_path / "greedy.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("greedy"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=4,
        output_path=output,
    )
    assert len(history) == 4


def test_llm_replay_runner_smoke(tmp_path) -> None:
    output = tmp_path / "llm_replay.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("llm_replay"),
        world_split="public-test",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=output,
    )
    assert history
    records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert records[0]["agent_metadata"]["agent_name"] == "llm_replay"
    assert records[0]["agent_metadata"]["requires_online_model"] is False
    assert records[0]["agent_metadata"]["uses_builtin_trace"] is True
    assert any(record.get("instrument") == "final_assay" for record in records)


def test_baseline_report_summary_rows_include_pre_release_metrics(tmp_path) -> None:
    report = generate_baseline_report(
        task_ids=["reaction-to-assay"],
        agents=["random", "llm_replay"],
        seeds=[0],
        output_dir=tmp_path / "baseline_report",
    )
    assert report.schema_version == "chemworld-baseline-report-0.2"
    assert report.task_seed_plan == {"reaction-to-assay": [0]}
    assert (tmp_path / "baseline_report" / "baseline_summary_table.json").exists()
    summary_rows = {
        (row["task_id"], row["agent_name"]): row for row in report.summary_rows
    }
    assert ("reaction-to-assay", "random") in summary_rows
    assert ("reaction-to-assay", "llm_replay") in summary_rows
    llm_row = summary_rows[("reaction-to-assay", "llm_replay")]
    assert llm_row["runs"] == 1
    assert llm_row["mean_final_assay_count"] >= 1.0
    assert "mean_invalid_action_rate" in llm_row
    assert "stderr_invalid_action_rate" in llm_row
    assert "mean_auc" in llm_row
    assert "stderr_auc" in llm_row
    assert "mean_bo_acquisition_recipe_count" in llm_row
    assert llm_row["mean_bo_acquisition_recipe_count"] == 0.0


def test_baseline_report_exposes_bo_acquisition_diagnostics(tmp_path) -> None:
    report = generate_baseline_report(
        task_ids=["reaction-optimization-standard"],
        agents=["gp_bo"],
        seeds=[0],
        output_dir=tmp_path / "bo_report",
    )
    row = report.summary_rows[0]
    assert row["task_id"] == "reaction-optimization-standard"
    assert row["agent_name"] == "gp_bo"
    assert row["mean_bo_initial_recipe_count"] == 4.0
    assert row["mean_bo_acquisition_recipe_count"] >= 1.0
    assert row["mean_bo_entered_acquisition"] == 1.0
    assert row["mean_final_best_score"] < 0.95


def test_maturity_summary_rejects_silent_task_mixing() -> None:
    base = {
        "task_id": "reaction-to-assay",
        "kernel_maturity": {"lowest_level": "lite", "modules": []},
        "physics_maturity": "lite",
        "proxy_allowed": False,
    }
    summary = maturity_summary_for_results([{**base}, {**base}])
    assert summary["levels"]["lite"]["runs"] == 2
    assert summary["tasks"]["reaction-to-assay"]["runs"] == 2

    mixed = {
        **base,
        "kernel_maturity": {"lowest_level": "proxy", "modules": []},
        "physics_maturity": "proxy",
        "proxy_allowed": True,
    }
    with pytest.raises(ValueError, match="mixed maturity metadata"):
        validate_result_maturity_consistency([{**base}, mixed])
