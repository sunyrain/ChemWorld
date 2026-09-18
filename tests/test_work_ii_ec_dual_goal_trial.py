"""Regression checks for the free-research pilot's recommendation evaluator."""

from pathlib import Path

from scripts.run_work_ii_ec_dual_goal_trial import physics, recipe, summaries

from chemworld.data.logging import load_jsonl
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent


def test_discarded_batch_does_not_enter_next_completed_recipe():
    rows = [
        {"experiment_index": 0, "action": {"operation": "add_reagent"}},
        {"experiment_index": 0, "action": {"operation": "discard_batch"}},
        {"experiment_index": 1, "action": {"operation": "add_solvent"}},
        {"experiment_index": 1, "action": {"operation": "terminate"}},
        {
            "experiment_index": 1,
            "action": {"operation": "measure", "instrument": "final_assay"},
            "instrument": "final_assay",
            "transaction_status": "committed",
            "observation": {},
        },
    ]
    completed = summaries(rows)
    assert len(completed) == 1
    assert completed[0]["lifecycle_index"] == 2
    assert [a["operation"] for a in completed[0]["actions"]] == [
        "add_solvent",
        "terminate",
        "measure",
    ]


def test_retest_accepts_long_batch_and_multiple_measurements(tmp_path: Path):
    # Both were legal in the twelve-batch source but rejected by the old single-batch card.
    actions = recipe(1, 1, -0.8, 500, 14400)
    actions[-2:-2] = [
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "measure", "instrument": "ph_meter"},
    ]
    output = tmp_path / "trajectory.jsonl"
    physics(_FrozenTruthReplayAgent(actions), output, batches=1, source_envelope=True)
    records = load_jsonl(output)
    assert len(records) == len(actions)
    assert all(r["transaction_status"] == "committed" for r in records)
    assert len(summaries(records)) == 1
    assert records[-1]["instrument"] == "final_assay"
