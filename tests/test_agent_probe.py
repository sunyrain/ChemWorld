from __future__ import annotations

import json

from chemworld.eval.agent_probe import (
    TOOL_AGENT_PROBE_SCHEMA_VERSION,
    run_tool_agent_probe,
)


def test_tool_agent_probe_runs_multi_seed_multi_round(tmp_path) -> None:
    report = run_tool_agent_probe(
        task_id="reaction-optimization-standard",
        seeds=[0, 1, 2],
        budget=18,
        min_rounds=12,
        output_dir=tmp_path / "probe",
    )
    payload = report.to_dict()
    assert payload["schema_version"] == TOOL_AGENT_PROBE_SCHEMA_VERSION
    assert payload["task_id"] == "reaction-optimization-standard"
    assert payload["seeds"] == [0, 1, 2]
    assert payload["aggregate"]["seed_count"] == 3
    assert payload["aggregate"]["all_min_rounds_satisfied"]
    assert payload["aggregate"]["all_trace_present"]
    assert len(payload["per_seed"]) == 3
    for row in payload["per_seed"]:
        assert row["decision_round_count"] >= 12
        assert row["agent_trace_step_count"] >= row["decision_round_count"]
        assert row["final_assay_count"] >= 1
        assert 0.0 <= row["best_score_auc"] <= 1.0
        assert 0.0 <= row["best_score"] <= 1.0
        assert "final_assay" in row["instrument_counts"]
        assert row["trajectory_path"]
        assert row["final_lab_report_text"]

    report_path = tmp_path / "probe" / "tool_agent_probe_report.json"
    csv_path = tmp_path / "probe" / "tool_agent_probe_summary.csv"
    assert report_path.exists()
    assert csv_path.exists()
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["aggregate"]["mean_decision_round_count"] >= 12
