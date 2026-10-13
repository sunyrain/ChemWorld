from scripts import run_paper_case_stability as stability
from scripts.run_paper_case_notebooks import write


def test_snapshot_keeps_failures_and_unstarted_slots(tmp_path):
    write(
        tmp_path / "repeat-01/results/EC-discovery.json",
        {
            "status": "failed",
            "failure": "provider stopped",
            "batches": [{"metrics": {}}],
            "operations": 8,
        },
    )
    result = stability.snapshot(tmp_path)
    assert len(result["cases"]) == result["planned_sources"] == 18
    assert result["terminal_sources"] == 1
    assert result["completed_sources"] == 0
    assert result["completed_batches"] == 1
    assert result["cases"][0]["failure"] == "provider stopped"
    assert sum(r["status"] == "not_started" for r in result["cases"]) == 17


def test_snapshot_does_not_double_count_a_just_finished_source(tmp_path, monkeypatch):
    write(
        tmp_path / "repeat-01/results/EC-discovery.json",
        {
            "status": "completed",
            "batches": [{}] * 12,
            "operations": 96,
        },
    )
    monkeypatch.setattr(stability, "live", lambda *_: {"batches": 12, "operations": 96})
    result = stability.snapshot(tmp_path, "repeat-01", "EC-discovery")
    assert result["completed_batches"] == 12
    assert result["active"] == {}


def test_execution_defect_stops_before_another_provider_unit(tmp_path, monkeypatch):
    prepared, launched = [], []

    def prepare(root):
        root.mkdir()
        prepared.append(root.name)

    class FailedProcess:
        returncode = 9

        def __init__(self, command, **kwargs):
            launched.append(command)

        def poll(self):
            return self.returncode

    monkeypatch.setattr(stability, "prepare", prepare)
    monkeypatch.setattr(stability.subprocess, "Popen", FailedProcess)
    root = tmp_path / "new-block"
    assert stability.run(root) == 9
    assert prepared == list(stability.REPEATS)
    assert len(launched) == 1
    assert launched[0][-1] == "references"
    assert (root / "block-stop.json").exists()
    assert stability.snapshot(root)["terminal_sources"] == 0
