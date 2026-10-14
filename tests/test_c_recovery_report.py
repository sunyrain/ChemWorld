"""Scientific denominators for a corrected cohort with retained missing sessions."""

import pytest
from scripts.report_c_recovery_aligned import COHORT, grouped_metrics, source_timeline


def test_equal_world_weighting_does_not_fill_missing_predictions_with_zero():
    rows = []
    for world, values in (("W01", (1, None, None)), ("W02", (0, 0, 0))):
        for value in values:
            rows.append(
                {"world": world, "arm": "Opaque", "measurements": {"crystal_yield_mae": value}}
            )
    for world in ("W03", "W04", "W05"):
        rows.extend({"world": world, "arm": "Opaque", "measurements": {}} for _ in range(3))
    group = grouped_metrics(rows)["crystal_yield_mae"]
    assert group["equal_world_means"]["Opaque"]["mean"] == 0.5
    assert group["equal_world_means"]["Opaque"]["observed"] == 2
    assert group["session_values"]["Opaque"]["mean"] == 0.25
    assert group["session_values"]["Opaque"]["observed"] == 4
    assert group["session_values"]["Opaque"]["missing"] == 11
    assert group["worlds"][0]["Opaque"]["values"] == [1, None, None]


def test_empty_source_is_retained_but_missing_nonempty_trace_is_rejected(tmp_path, monkeypatch):
    from scripts import report_c_recovery_aligned as report

    folder = tmp_path / "raw"
    folder.mkdir()
    monkeypatch.setattr(report, "case_folder", lambda *args: folder)
    notes = tmp_path / "repeat-01" / "C-W01-Opaque-notebook.md"
    notes.parent.mkdir()
    notes.write_text("# Source notebook\n\nNo notebook revision recorded.\n", encoding="utf-8")
    row = {
        "repeat": "repeat-01",
        "id": "C-W01-Opaque",
        "status": "failed",
        "failure": {"stage": "source"},
        "cohort": COHORT,
        "operations": 0,
        "completed_batches": 0,
        "notebook": {"versions": []},
    }
    result = source_timeline(row, tmp_path, tmp_path)
    assert result["status"] == "failed" and result["versions"] == []
    assert result["metrics"]["structural_feedback_opportunities"] == 0
    row["operations"] = 1
    with pytest.raises(ValueError, match="nonempty"):
        source_timeline(row, tmp_path, tmp_path)
