"""Prevent scope expansion and success-conditioned interviews in the EC trial."""

from pathlib import Path

import pytest
from scripts.run_work_ii_ec_dual_goal_trial import (
    physics,
    planned_units,
    posttest_context_available,
    recipe,
    resource_card,
    summaries,
)

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


def test_explicit_six_cell_scope_never_adds_other_prior_layers():
    selected = [
        f"{goal}-E-{arm}"
        for goal in ("discovery", "optimization")
        for arm in ("Opaque", "Aligned", "MisIndexed")
    ]
    assert ["-".join(unit) for unit in planned_units(selected)] == selected
    for invalid in ([], selected + selected[:1], ["discovery-Z-Opaque"]):
        with pytest.raises(ValueError):
            planned_units(invalid)


def test_failed_source_can_be_interviewed_only_with_intact_terminal_context():
    receipt = {
        "thread_id": "retained",
        "final_payload_valid": True,
        "provider_error_event_count": 0,
        "source_status": "failed",
    }
    assert posttest_context_available(receipt)
    for change in (
        {"thread_id": None},
        {"final_payload_valid": False},
        {"provider_error_event_count": 1},
    ):
        assert not posttest_context_available({**receipt, **change})


def test_ec_twelve_batch_card_has_no_unintended_process_time_limit():
    card = resource_card()
    assert card.vessel_start_limit == card.final_assay_limit == 12
    assert card.nonfinal_instrument_use_limit == 12
    assert card.process_time_limit_s is None
    # Existing legal per-operation maxima; stock cannot preempt the operation envelope.
    assert card.stock_limits["reagent_mol"] >= 0.04 * card.operation_attempt_limit
    assert card.stock_limits["solvent_L"] >= 0.08 * card.operation_attempt_limit
