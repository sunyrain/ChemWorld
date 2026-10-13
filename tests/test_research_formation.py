from collections import Counter
from io import StringIO

import pytest
from scripts import run_research_formation as study


def test_fixed_balanced_matrix_and_counts():
    rows = study.schedule()
    assert len(rows) == 48
    assert len({(r["repeat"], r["id"]) for r in rows}) == 48
    assert Counter(r["system"] for r in rows) == {"EQ": 30, "C": 18}
    assert Counter(r["arm"] for r in rows) == {"Opaque": 24, "Aligned": 24}
    assert set(Counter(r["id"] for r in rows).values()) == {3}
    assert sum(r["batches"] for r in rows) == 576
    assert sum(4 if r["system"] == "EQ" else 3 for r in rows) == 174
    assert {r["world"] for r in rows if r["system"] == "C"} == {"W01", "W03", "W05"}
    for repeat in study.REPEATS:
        batch = [r for r in rows if r["repeat"] == repeat]
        for a, b in zip(batch[::2], batch[1::2], strict=True):
            assert (a["system"], a["world"]) == (b["system"], b["world"])
            assert a["arm"] != b["arm"]


def test_prepare_copies_original_inputs_without_running_experiments(tmp_path):
    root = tmp_path / "fresh"
    study.prepare(root)
    design = study.read(root / "design.json")
    assert design["planned_sources"] == len(design["schedule"]) == 48
    assert design["provider"]["reasoning_effort"] == "medium"
    assert "src/chemworld/agents/campaign_notebook.py" in design["runtime_surface"]
    assert not (root / "references").exists()
    for repeat in study.REPEATS:
        c = study.read(root / repeat / "C/design.json")
        assert c["protocol"] == "c-quality-recovery-formal-v3-en"
        assert len(c["schedule"]) == 6
    with pytest.raises(FileExistsError):
        study.prepare(root)


def test_shared_references_execute_once_and_distribute_identical_truth(tmp_path, monkeypatch):
    from scripts import run_work_ii_c_formal as c
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

    root = tmp_path / "fresh"
    study.prepare(root)
    calls = []

    def eq_reference(path, actions, **kwargs):
        calls.append(("EQ", kwargs["world"]["world_id"]))
        return {
            "failure": None,
            "rollbacks": [],
            "operation_attempts": 48,
            "exact_replay": {"verified": True},
            "batches": [{"metrics": dict.fromkeys(eq.METRICS, 0.1)} for _ in range(12)],
        }

    def c_reference(path, actions, **kwargs):
        calls.append(("C", kwargs["world_seed"]))
        return {
            "passed": True,
            "operations": 120,
            "batches": [{}] * 12,
            "truth": [0.2] * 12,
            "exact_replay": {"verified": True},
        }

    monkeypatch.setattr(eq, "reference_run", eq_reference)
    monkeypatch.setattr(c, "fixed", c_reference)
    study.references(root, {})
    assert len(calls) == 28
    assert Counter(s for s, w in calls) == {"EQ": 25, "C": 3}
    assert study.read(root / "references/complete.json")["completed_batches"] == 336
    assert len({(root / r / "references/truth.json").read_bytes() for r in study.REPEATS}) == 1
    for world in study.C_WORLDS:
        paths = [
            root / r / f"C/qualification/W{world:02d}/queries/result.json" for r in study.REPEATS
        ]
        assert len({p.read_bytes() for p in paths}) == 1


def test_replay_defects_stop_but_provider_failures_are_retained():
    study.validate_result({"status": "failed", "failure": "provider_failure", "operations": 0})
    with pytest.raises(RuntimeError, match="source replay"):
        study.validate_result({"source": {"operations": 2, "exact_replay": {"verified": False}}})
    with pytest.raises(RuntimeError, match="recommendation replay"):
        study.validate_result({"recommendation_retest": {"exact_replay": {"verified": False}}})


@pytest.mark.parametrize("fatal", [False, True])
def test_pool_four_slots_once_each_and_drain_on_defect(tmp_path, monkeypatch, fatal):
    units = study.schedule()[:8]
    study.write(tmp_path / "design.json", {"schedule": units})
    launches, counts = [], []

    class Process:
        def __init__(self, unit):
            self.unit, self.polls = unit, 0

        def poll(self):
            self.polls += 1
            if self.polls < 2:
                return None
            if fatal and self.unit == units[0]:
                return 1
            # Ordinary scientific/provider failure must not stop the pool.
            study.write(
                study.result_path(tmp_path, self.unit),
                {
                    "status": "failed",
                    "failure": "provider_failure",
                    "operations": 0,
                },
            )
            return 0

    def launch(root, unit):
        launches.append(unit["id"])
        return {"unit": unit, "process": Process(unit), "stream": StringIO()}

    original_snapshot = study.snapshot

    def snapshot(root, active, **kwargs):
        counts.append(len(active))
        return original_snapshot(root, active, **kwargs)

    monkeypatch.setattr(study, "launch", launch)
    monkeypatch.setattr(study, "snapshot", snapshot)
    monkeypatch.setattr(study.time, "sleep", lambda _: None)
    assert study.run_pool(tmp_path) == int(fatal)
    assert max(counts) == 4
    assert len(launches) == len(set(launches)) == (4 if fatal else 8)
    assert counts[-1] == 0
    summary = study.read(tmp_path / "summary.json")
    assert summary["terminal_sources"] == (3 if fatal else 8)
    assert bool(summary["block_stop"]) == fatal
