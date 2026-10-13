from collections import Counter

import pytest
from scripts import run_matched_quench as quench
from scripts import run_research_extension as extension
from scripts import run_research_formation as parent
from scripts.run_paper_case_notebooks import read, write


def test_extension_is_exact_complement_not_replacement():
    rows = extension.schedule()
    old = {(r["repeat"], r["id"]) for r in parent.schedule()}
    new = {(r["repeat"], r["id"]) for r in rows}
    assert len(new) == 42 and not old & new and len(old | new) == 90
    assert Counter(r["system"] for r in rows) == {"EQ": 15, "C": 27}
    assert Counter(r["arm"] for r in rows) == {"MisIndexed": 30, "Opaque": 6, "Aligned": 6}
    assert set(Counter(r["id"] for r in rows).values()) == {3}
    assert sum(r["batches"] for r in rows) == 504
    assert sum(4 if r["system"] == "EQ" else 3 for r in rows) == 141
    assert rows == extension.schedule()


def test_prepare_and_references_reuse_336_execute_only_missing_24(tmp_path, monkeypatch):
    from scripts import run_work_ii_c_formal as c

    previous, root = tmp_path / "parent", tmp_path / "extension"
    parent.prepare(previous)
    write(previous / "summary.json", {"terminal_sources": 48, "active_units": []})
    eq_truth = {"EQ": {"retained": [0.1, 0.2]}}
    write(previous / "references/truth.json", eq_truth)
    reused = {
        "passed": True,
        "batches": [{}] * 12,
        "operations": 55,
        "truth": [0.2] * 12,
        "exact_replay": {"verified": True},
    }
    for world in (1, 3, 5):
        write(previous / "references" / f"C-W{world:02d}/result.json", reused)
    extension.prepare(root, previous)
    assert read(root / "design.json")["planned_sources"] == 42
    assert len(read(root / "repeat-01/C/design.json")["schedule"]) == 9
    calls = []

    def fixed(path, actions, **kwargs):
        calls.append(kwargs["world_seed"])
        result = {**reused, "operations": 12}
        write(path / "result.json", result)
        return result

    monkeypatch.setattr(c, "fixed", fixed)
    extension.references(root, {})
    assert calls == [1, 3]
    assert read(root / "references/complete.json")["completed_batches"] == 24
    assert read(root / "references/complete.json")["reused_batches"] == 336
    for repeat in extension.REPEATS:
        assert read(root / repeat / "references/truth.json") == eq_truth
        for world in (1, 3, 5):
            assert (
                read(root / repeat / "C/qualification" / f"W{world:02d}/queries/result.json")
                == reused
            )
    summary = parent.snapshot(root)
    assert summary["planned_sources"] == 42
    assert summary["planned_source_batches"] == 504
    assert summary["planned_posttests"] == 141
    assert summary["planned_reference_batches"] == 24
    with pytest.raises(FileExistsError):
        extension.prepare(root, previous)


@pytest.mark.parametrize("has_quench", [False, True])
def test_matched_actions_preserve_every_nonquench_argument(has_quench):
    import copy

    actions = [
        {"operation": "heat", "temperature_K": 340, "duration_s": 3600},
        {"operation": "configure_control", "ramp_rate_K_s": 0.1},
        {"operation": "seed_crystals", "seed_mass_g": 0.01},
        {"operation": "cool_crystallize", "target_temperature_K": 270, "duration_s": 14400},
    ]
    if has_quench:
        actions.insert(1, {"operation": "quench"})
    original = copy.deepcopy(actions)
    variants, position, original_arm = quench.paired_actions(actions)
    assert variants[original_arm] == original
    assert position == (1 if has_quench else 2)
    assert [a for a in variants["present"] if a["operation"] != "quench"] == variants["absent"]
    assert actions == original
    variants["present"][-1]["duration_s"] = 10
    assert variants["absent"][-1]["duration_s"] == 14400


def test_quench_missing_measurements_are_not_zero_outcomes():
    outcome = quench.outcome(
        {
            "truth": [],
            "passed": False,
            "failure": {"type": "ValueError"},
            "operations": 2,
            "elapsed_s": 1,
            "exact_replay": {"verified": True},
        },
        [],
    )
    assert outcome["truth"] is outcome["quality"] is outcome["quality_and_recovery"] is None
