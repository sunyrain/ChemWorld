from scripts import report_research_formation as report
from scripts.run_paper_case_notebooks import write
from scripts.run_research_formation import cases, schedule


def test_report_keeps_all_slots_missing_records_and_posttest_failures(tmp_path):
    root, destination = tmp_path / "raw", tmp_path / "export"
    write(
        root / "design.json",
        {
            "mode": "prospective",
            "source_commit": "fixed",
            "schedule": schedule(),
            "cases": cases(),
        },
    )
    write(root / "references/complete.json", {"completed_batches": 336})
    unit = schedule()[0]
    write(
        root / unit["repeat"] / "results" / f"{unit['id']}.json",
        {
            "status": "retained_nonconforming",
            "operations": 0,
            "posttests": {"K1": {"failure": "provider_failure"}},
            "posttest_validation": {"K1": {"valid": False}},
        },
    )
    output = report.build(root, destination)
    assert len(output["cases"]) == 48
    assert output["terminal_sources"] == 1
    assert output["completed_sources"] == output["sealed_posttests"] == 0
    assert output["notebook_versions"] == 0
    row = output["cases"][0]
    assert row["notebook"]["initial_note_before_action"] is None
    assert row["missing_stages"] == ["K1", "Q", "K2", "EQS"]
    exported = report.read(destination / unit["repeat"] / f"{unit['id']}.json")
    assert exported["posttests"]["K1"]["failure"] == "provider_failure"
    assert "1/48" in (destination / "REPORT.md").read_text(encoding="utf-8")
    assert output["reference"]["completed_batches"] == 336
