"""Scientific boundaries for retained statement/action alignment."""

from scripts.analyze_inquiry_trajectories import path_features, timeline


def event(cursor, operation, *, batch=1, status="committed", **kwargs):
    return {
        "cursor": cursor,
        "batch": batch,
        "transaction_status": status,
        "action": {"operation": operation, **kwargs},
        "observations": {},
    }


def notes(*cursors):
    return {
        "notebook": {
            "versions": [
                {"revision": i, "public_cursor": {"event_count": cursor}}
                for i, cursor in enumerate(cursors, 1)
            ]
        }
    }


def test_no_future_measurements_are_assigned_to_an_earlier_note():
    events = [
        event(1, "add_solvent", volume_L=0.04, solvent=2),
        event(2, "measure", instrument="final_assay"),
        event(3, "add_solvent", batch=2, volume_L=0.035, solvent=2),
        event(4, "measure", batch=2, instrument="final_assay"),
    ]
    versions = timeline(notes(0, 2, 4), events, {1: "initial", 2: "later", 3: "final"})
    assert versions[0]["new_final_assays_since_previous_note"] == []
    assert versions[1]["new_final_assays_since_previous_note"] == [2]
    assert versions[0]["following_final_assay_cursors"] == [2]
    assert versions[0]["first_research_action_after_next_revision"] == 3
    assert versions[0]["structural_feedback_opportunity"]
    assert not versions[1]["structural_feedback_opportunity"]


def test_rejected_seed_is_not_an_executed_dose_or_followup_experiment():
    events = [
        event(1, "seed_crystals", seed_mass_g=0.05),
        event(2, "measure", instrument="final_assay"),
        event(3, "seed_crystals", status="rolled_back", seed_mass_g=1.95),
    ]
    batches, metrics = path_features(events)
    assert batches[0]["seed_added_g"] == 0.05
    assert metrics["rejected_attempts"] == 1
    versions = timeline(notes(0, 2), events, {1: "initial", 2: "after assay"})
    assert not versions[0]["structural_feedback_opportunity"]


def test_repeated_text_is_only_a_temporal_opportunity():
    events = [
        event(1, "measure", instrument="final_assay"),
        event(2, "add_reagent", batch=2, amount_mol=0.01),
    ]
    versions = timeline(notes(0, 1), events, {1: "same statement", 2: "same statement"})
    assert versions[0]["structural_feedback_opportunity"]
    assert versions[0]["semantic_update"] == "not_inferred_from_temporal_structure"


def test_rejected_assay_does_not_supply_evidence_for_a_window():
    events = [
        event(1, "measure", instrument="final_assay", status="rolled_back"),
        event(2, "add_reagent", batch=2, amount_mol=0.01),
    ]
    versions = timeline(notes(0, 1), events, {1: "initial", 2: "later"})
    assert not versions[0]["structural_feedback_opportunity"]
    assert versions[1]["new_final_assays_since_previous_note"] == []
