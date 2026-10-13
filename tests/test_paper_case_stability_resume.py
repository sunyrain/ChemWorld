import pytest
from scripts import resume_paper_case_stability as scheduler
from scripts.run_paper_case_notebooks import write


def test_previous_launch_without_receipt_is_never_restarted(tmp_path, monkeypatch):
    monkeypatch.setattr(scheduler, "REPEATS", ("repeat-01",))
    path = tmp_path / "repeat-01/logs/references.log"
    path.parent.mkdir(parents=True)
    path.write_text("attempt retained")
    with pytest.raises(RuntimeError, match="requires explicit attachment"):
        scheduler.pending_units(tmp_path, {})


def test_case_waits_for_references_and_invalid_replay_is_rejected(tmp_path):
    assert not scheduler.eligible(tmp_path, ("repeat-01", "EC-discovery"))
    assert scheduler.eligible(tmp_path, ("repeat-01", "references"))
    path = scheduler.receipt(tmp_path, "repeat-01", "references")
    write(path, {"completed_batches": 144, "replay_verified": False})
    with pytest.raises(RuntimeError, match="reference defect"):
        scheduler.validate_receipt(tmp_path, "repeat-01", "references")


def test_four_slots_attach_current_skip_completed_and_launch_remaining_once(tmp_path, monkeypatch):
    monkeypatch.setattr(scheduler, "REPEATS", ("repeat-01",))
    write(scheduler.receipt(tmp_path, "repeat-01", "references"),
          {"completed_batches": 144, "replay_verified": True})
    write(scheduler.receipt(tmp_path, "repeat-01", "EC-optimization"),
          {"status": "retained_nonconforming", "operations": 0})
    launched, active_counts = [], []

    class Attached:
        polls = 0

        def is_running(self):
            self.polls += 1
            if self.polls < 3:
                return True
            write(scheduler.receipt(tmp_path, "repeat-01", "EC-discovery"),
                  {"status": "completed", "operations": 0})
            return False

    class NewProcess:
        pid = 123

        def __init__(self, command, **kwargs):
            self.unit = command[-1]
            self.polls = 0
            launched.append(self.unit)

        def poll(self):
            self.polls += 1
            if self.polls < 3:
                return None
            write(scheduler.receipt(tmp_path, "repeat-01", self.unit),
                  {"status": "completed", "operations": 0})
            return 0

    def progress(root, active, *args):
        active_counts.append(len(active))
        return {"completed_batches": 0}

    monkeypatch.setattr(scheduler.psutil, "Process", lambda _: Attached())
    monkeypatch.setattr(scheduler.subprocess, "Popen", NewProcess)
    monkeypatch.setattr(scheduler, "progress", progress)
    monkeypatch.setattr(scheduler.time, "sleep", lambda _: None)
    assert scheduler.resume(tmp_path, 4, [("repeat-01", "EC-discovery", 42)]) == 0
    assert max(active_counts) == 4
    assert sorted(launched) == ["C-12", "C-24", "EQ-Astra", "EQ-Sol"]
    assert len(launched) == len(set(launched))
