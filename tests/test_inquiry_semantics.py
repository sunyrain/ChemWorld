"""Prevent temporal leakage and unsupported execution claims in manual coding."""

import json

import pytest
from scripts.analyze_inquiry_semantics import build, validate_record


def event(cursor, batch, operation, *, status="committed", **kwargs):
    return {
        "cursor": cursor,
        "batch": batch,
        "transaction_status": status,
        "action": {"operation": operation, **kwargs},
        "observations": {},
    }


@pytest.fixture
def session():
    return {
        "repeat": "repeat-01",
        "id": "case-a",
        "system": "EQ",
        "versions": [
            {
                "revision": 1,
                "public_cursor": 0,
                "structural_feedback_opportunity": True,
                "next_revision": 2,
            },
            {
                "revision": 2,
                "public_cursor": 3,
                "following_interval_end": 6,
                "text": "Local trend unresolved. Next: test dose.",
                "structural_feedback_opportunity": False,
            },
        ],
        "events": [
            event(2, 1, "measure", instrument="final_assay"),
            event(4, 2, "seed_crystals", status="rejected", seed_mass_g=2.0),
            event(5, 2, "seed_crystals", seed_mass_g=0.05),
            event(6, 2, "measure", instrument="final_assay"),
            event(7, 3, "seed_crystals", seed_mass_g=0.04),
        ],
    }


@pytest.fixture
def record():
    return {
        "repeat": "repeat-01",
        "id": "case-a",
        "from_revision": 1,
        "to_revision": 2,
        "update_types": ["unresolved"],
        "update_quote": "Local trend unresolved.",
        "new_evidence_batches": [1],
        "next_plan_quote": "Next: test dose.",
        "action_link": "matched",
        "action_cursors": [5],
        "interpretation": "Dose test executed; statement-action association only.",
    }


def test_future_assay_cannot_support_the_intermediate_judgment(record, session):
    record["new_evidence_batches"] = [2]
    with pytest.raises(ValueError, match="not newly available"):
        validate_record(record, session)


def test_action_after_next_note_is_not_an_immediate_plan_match(record, session):
    record["action_cursors"] = [7]
    with pytest.raises(ValueError, match="outside the immediate"):
        validate_record(record, session)


def test_rejected_request_cannot_count_as_executed_test(record, session):
    record["action_cursors"] = [4]
    with pytest.raises(ValueError, match="actual committed action"):
        validate_record(record, session)
    record["action_link"] = "rejected"
    verified = validate_record(record, session)
    assert verified["verified_actions"][0]["transaction_status"] == "rejected"
    assert verified["interpretation_independently_reviewed"] is False


def test_no_explicit_plan_does_not_imply_no_learning(record, session):
    record.update(next_plan_quote=None, action_link="no_explicit_plan", action_cursors=[])
    verified = validate_record(record, session)
    assert verified["update_types"] == ["unresolved"]
    assert verified["verified_evidence_cursors"] == [2]


def test_partial_coverage_cannot_publish_category_distribution(tmp_path, record, session):
    def save(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    for name in ("case-a", "case-b", "case-c"):
        session["id"] = name
        if name == "case-c":
            session["versions"][0]["structural_feedback_opportunity"] = False
        save(tmp_path / "sessions" / "repeat-01" / f"{name}.json", session)
    save(
        tmp_path / "summary.json",
        {"sessions": [{"repeat": "repeat-01", "id": n} for n in ("case-a", "case-b", "case-c")]},
    )
    coding = {"scope": "fixture", "planned_windows": 2, "records": [record]}
    save(tmp_path / "semantic_coding.json", coding)
    partial = build(tmp_path)
    assert partial["coded_windows"] == 1
    assert partial["coverage_by_system"]["EQ"]["coded_windows"] == 1
    assert partial["pending_windows"] == [("repeat-01", "case-b", 1)]
    assert "descriptive_code_counts" not in partial
    assert partial["sessions_without_observable_complete_window"] == [("repeat-01", "case-c")]
    coding["records"].append({**record, "id": "case-b"})
    save(tmp_path / "semantic_coding.json", coding)
    complete = build(tmp_path)
    assert complete["complete"]
    assert complete["descriptive_code_counts"]["action_links"] == {"matched": 2}
    assert complete["sessions_without_observable_complete_window"] == [("repeat-01", "case-c")]
