import json

import pytest
from scripts import analyze_abductive_histories as histories


def test_cooling_rejection_cannot_become_an_executed_temperature_control():
    row = next(
        row for row in histories.sessions() if row["key"] == "C_corrected/repeat-02/C-W04-Aligned"
    )
    batches = {batch["batch"]: batch for batch in histories.batch_summary(row)}
    for batch_number, cursor in ((9, 107), (10, 118)):
        batch = batches[batch_number]
        assert not any(a["operation"] == "cool_crystallize" for a in batch["treatments"])
        rejected = next(a for a in batch["rejected_actions"] if a["cursor"] == cursor)
        assert rejected["operation"] == "cool_crystallize"
        assert rejected["transaction_status"] == "rolled_back"
        assert batch["final_assays"]
    for batch_number in (8, 11, 12):
        assert any(
            a["operation"] == "cool_crystallize" for a in batches[batch_number]["treatments"]
        )


def test_rejected_seed_repetitions_do_not_become_a_delivered_high_dose():
    checks = histories.seed_execution_checks(histories.sessions())["cases"]
    assert len(checks) == 9
    assert all(row["committed_seed_g"] == pytest.approx(0.05) for row in checks)
    largest = next(
        row
        for row in checks
        if row["key"] == "C_corrected/repeat-03/C-W02-Aligned" and row["batch"] == 12
    )
    assert largest["rejected_seed_attempts"] == 59
    assert len(largest["seed_actions"]) == 60


def test_later_explanation_cannot_be_backdated_to_an_earlier_note(tmp_path, monkeypatch):
    monkeypatch.setattr(histories, "OUTPUT", tmp_path)
    manual = {
        "records": [
            {
                "key": "example",
                "histories": [
                    {
                        "kind": "explanatory_candidate",
                        "anchors": [{"revision": 1, "contains": "post-observation explanation"}],
                    }
                ],
            }
        ]
    }
    (tmp_path / "example_manual.json").write_text(json.dumps(manual), encoding="utf-8")
    source = {
        "key": "example",
        "notes": [
            {"revision": 1, "cursor": 0, "text": "pre-observation expectation"},
            {"revision": 2, "cursor": 4, "text": "post-observation explanation"},
        ],
    }
    with pytest.raises(ValueError, match="Unverified quotation"):
        histories.verify_coding([source])
