from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    C2_TASK_STAGE_ORDER,
    _task_receipt_errors,
    build_c2_outcome_blind_selection_record,
    build_c2_task_admission_receipt,
    c2_task_admission_receipt_sha256,
    validate_c2_outcome_blind_selection_pair,
)

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"


def _self_hashed(payload: dict[str, object], field: str) -> dict[str, object]:
    payload[field] = canonical_json_sha256(payload)
    return payload


def _source_binding() -> dict[str, object]:
    return {
        "schema_version": "chemworld-work-ii-c2-source-binding-0.1",
        "tested_commit": "a" * 40,
        "material_tree": {
            "relative_roots": [],
            "excluded_relative_paths": [],
            "sha256": "tree",
        },
    }


def _stage(stage: str, task_id: str) -> dict[str, object]:
    common: dict[str, object] = {
        "task_id": task_id,
        "formal_result": False,
        "source_commit": "a" * 40,
    }
    if stage == "Q1":
        common.update(
            schema_version="chemworld-work-ii-mechanism-oracle-five-world-summary-0.2",
            q0={"passed": True},
            qualification_passed=True,
            world_seeds=list(range(5)),
            worlds=[
                {"world_seed": seed, "analysis": {"passed": True}}
                for seed in range(5)
            ],
        )
    elif stage == "Q2":
        common.update(
            schema_version="chemworld-work-ii-matched-prior-five-world-summary-0.3",
            qualification_passed=True,
            provider_call_count=0,
            world_seeds=list(range(5)),
            worlds=[
                {"world_seed": seed, "qualification_passed": True}
                for seed in range(5)
            ],
        )
    else:
        common.update(
            schema_version="chemworld-work-ii-initial-model-pilot-evaluation-0.4",
            status="passed",
            participant_source_commit="a" * 40,
            denominators={
                "participant_cell_count": 3,
                "participant_completed_cell_count": 3,
                "participant_terminal_trajectory_count": 3,
                "participant_platform_failure_count": 0,
            },
        )
    return _self_hashed(common, "report_sha256")


def _fixtures(tmp_path: Path, locus: str = "A_P") -> tuple[Path, dict[str, Path], Path]:
    task_id = "synthetic-task"
    reports = tmp_path / "workstreams/flagship_tasks/reports"
    reports.mkdir(parents=True, exist_ok=True)
    campaign = {
        "schema_version": "chemworld-work-ii-campaign-pilot-0.4",
        "formal_result": False,
        "task_id": task_id,
        "campaign": {
            "complete_experiments": 10 if locus == "A_P" else 12,
            "checkpoint_complete_experiments": (
                [0, 2, 4, 7, 10] if locus == "A_P" else [0, 3, 6, 9, 12]
            ),
        },
        "intervention": {
            "locus": "parametric" if locus == "A_P" else "structural_mechanistic"
        },
        "qualification": {"q2_passed": True},
    }
    campaign_path = reports / "campaign.json"
    write_json_atomic(campaign_path, campaign)
    stages: dict[str, Path] = {}
    for stage in C2_TASK_STAGE_ORDER:
        path = reports / f"{stage.lower()}.json"
        write_json_atomic(path, _stage(stage, task_id))
        stages[stage] = path
    selection = build_c2_outcome_blind_selection_record(
        tmp_path,
        locus=locus,
        task_id=task_id,
        candidate_roster=[
            {
                "task_id": task_id,
                "frozen_rank": 1,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "terminal Q1/Q2/D1 required",
            },
            {
                "task_id": "second-terminal-candidate",
                "frozen_rank": 2,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "terminal Q1/Q2/D1 required",
            },
        ],
        selection_rule={
            "method": "eligible_then_ascending_frozen_rank",
            "formal_participant_outcomes_permitted": False,
            "selection_slot": 1,
            "required_selected_task_count": 2,
        },
        source_binding=_source_binding(),
    )
    selection_path = reports / "selection.json"
    write_json_atomic(selection_path, selection)
    return campaign_path, stages, selection_path


@pytest.fixture
def binding_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "chemworld.eval.work_ii_c2_admission.validate_c2_source_binding",
        lambda root, binding: [],
    )


@pytest.mark.parametrize("locus", ["A_P", "A_S"])
def test_builder_requires_real_stage_roster_and_supports_both_loci(
    tmp_path: Path,
    binding_stubs: None,
    locus: str,
) -> None:
    campaign, stages, selection = _fixtures(tmp_path, locus)
    receipt = build_c2_task_admission_receipt(
        tmp_path,
        locus=locus,
        task_id="synthetic-task",
        campaign_config_path=campaign,
        stage_report_paths=stages,
        selection_record_path=selection,
        source_binding=_source_binding(),
    )

    assert receipt["status"] == "passed_terminal_task_admission"
    assert receipt["stage_evidence_order"] == ["Q1", "Q2", "D1"]
    assert all(row["passed"] for row in receipt["stage_evidence"])
    assert receipt["validation_errors"] == []


def test_current_reaction_safety_evidence_cannot_generate_terminal_pass(
    binding_stubs: None,
) -> None:
    receipt = build_c2_task_admission_receipt(
        ROOT,
        locus="A_P",
        task_id="reaction-safety-constrained",
        campaign_config_path=(
            ROOT
            / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1_execution.json"
        ),
        stage_report_paths={
            "Q1": REPORTS
            / "work-ii-mechanism-oracle-reaction-safety-classified-v0.2-20260811.json",
            "Q2": REPORTS
            / "work-ii-reaction-safety-matched-prior-qualification-20260811.json",
            "D1": REPORTS
            / "work-ii-reaction-safety-matched-prior-d1-evaluation-20260811.json",
        },
        selection_record_path=(
            ROOT / "workstreams/flagship_tasks/reports/nonexistent-ap-selection.json"
        ),
        source_binding=_source_binding(),
    )

    assert receipt["status"] == "not_ready_fail_closed"
    assert receipt["terminal_qualification_passed"] is False
    assert any("runtime commit" in error for error in receipt["validation_errors"])


def test_validator_rebuilds_stage_evidence_instead_of_trusting_boolean(
    tmp_path: Path,
    binding_stubs: None,
) -> None:
    campaign, stages, selection = _fixtures(tmp_path)
    receipt = build_c2_task_admission_receipt(
        tmp_path,
        locus="A_P",
        task_id="synthetic-task",
        campaign_config_path=campaign,
        stage_report_paths=stages,
        selection_record_path=selection,
        source_binding=_source_binding(),
    )
    tampered = deepcopy(receipt)
    tampered["stage_evidence"][1]["passed"] = False
    tampered["receipt_sha256"] = c2_task_admission_receipt_sha256(tampered)

    errors = _task_receipt_errors(tmp_path, tampered, locus="A_P")

    assert any("Q2 evidence is stale" in error for error in errors)


def test_missing_stage_roster_is_rejected(
    tmp_path: Path, binding_stubs: None
) -> None:
    campaign, stages, selection = _fixtures(tmp_path)
    del stages["D1"]

    with pytest.raises(ValueError, match="exactly Q1, Q2 and D1"):
        build_c2_task_admission_receipt(
            tmp_path,
            locus="A_P",
            task_id="synthetic-task",
            campaign_config_path=campaign,
            stage_report_paths=stages,
            selection_record_path=selection,
            source_binding=_source_binding(),
        )


def test_outcome_blind_selection_builder_rejects_cherry_picking(
    tmp_path: Path,
    binding_stubs: None,
) -> None:
    roster = [
        {
            "task_id": "first-eligible",
            "frozen_rank": 1,
            "eligible_before_formal_outcomes": True,
            "eligibility_basis": "terminal qualification",
        },
        {
            "task_id": "second-eligible",
            "frozen_rank": 2,
            "eligible_before_formal_outcomes": True,
            "eligibility_basis": "terminal qualification",
        },
    ]
    with pytest.raises(ValueError, match="eligible frozen slot"):
        build_c2_outcome_blind_selection_record(
            tmp_path,
            locus="A_S",
            task_id="second-eligible",
            candidate_roster=roster,
            selection_rule={
                "method": "eligible_then_ascending_frozen_rank",
                "formal_participant_outcomes_permitted": False,
                "selection_slot": 1,
                "required_selected_task_count": 2,
            },
            source_binding=_source_binding(),
        )


def test_terminal_receipt_rejects_dynamic_evidence_inside_protected_tree(
    tmp_path: Path, binding_stubs: None
) -> None:
    campaign, stages, selection = _fixtures(tmp_path)
    protected_campaign = tmp_path / "configs/benchmark/generated-campaign.json"
    protected_campaign.parent.mkdir(parents=True, exist_ok=True)
    protected_campaign.write_bytes(campaign.read_bytes())

    receipt = build_c2_task_admission_receipt(
        tmp_path,
        locus="A_P",
        task_id="synthetic-task",
        campaign_config_path=protected_campaign,
        stage_report_paths=stages,
        selection_record_path=selection,
        source_binding=_source_binding(),
    )

    assert receipt["status"] == "not_ready_fail_closed"
    assert any(
        "campaign config must be under workstreams/flagship_tasks/reports" in error
        for error in receipt["validation_errors"]
    )


def _selection_pair(
    tmp_path: Path,
    *,
    second_roster: list[dict[str, object]] | None = None,
    second_method: str = "eligible_then_ascending_frozen_rank",
) -> list[dict[str, object]]:
    roster = [
        {
            "task_id": "first-eligible",
            "frozen_rank": 1,
            "eligible_before_formal_outcomes": True,
            "eligibility_basis": "terminal qualification",
        },
        {
            "task_id": "second-eligible",
            "frozen_rank": 2,
            "eligible_before_formal_outcomes": True,
            "eligibility_basis": "terminal qualification",
        },
        {
            "task_id": "rejected-flow",
            "frozen_rank": 3,
            "eligible_before_formal_outcomes": False,
            "eligibility_basis": "Q0 scientific rejection retained",
        },
    ]
    records = []
    for slot, task_id in ((1, "first-eligible"), (2, "second-eligible")):
        rule = {
            "method": (
                "eligible_then_ascending_frozen_rank"
                if slot == 1
                else second_method
            ),
            "formal_participant_outcomes_permitted": False,
            "selection_slot": slot,
            "required_selected_task_count": 2,
        }
        records.append(
            build_c2_outcome_blind_selection_record(
                tmp_path,
                locus="A_S",
                task_id=task_id,
                candidate_roster=(
                    roster if slot == 1 or second_roster is None else second_roster
                ),
                selection_rule=rule,
                source_binding=_source_binding(),
            )
        )
    return records


def test_selection_pair_requires_shared_roster_rule_and_exact_slots(
    tmp_path: Path, binding_stubs: None
) -> None:
    records = _selection_pair(tmp_path)
    assert validate_c2_outcome_blind_selection_pair(records, locus="A_S") == []

    different_roster = deepcopy(records)
    different_roster[1]["candidate_roster"][2]["task_id"] = "rejected-crystallization"
    different_roster[1]["selection_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in different_roster[1].items()
            if key != "selection_sha256"
        }
    )
    assert any(
        "exact candidate roster" in error
        for error in validate_c2_outcome_blind_selection_pair(
            different_roster, locus="A_S"
        )
    )

    duplicate_slot = deepcopy(records)
    duplicate_slot[1]["selection_slot"] = 1
    duplicate_slot[1]["selection_rule"]["selection_slot"] = 1
    assert any(
        "exactly {1,2}" in error
        for error in validate_c2_outcome_blind_selection_pair(
            duplicate_slot, locus="A_S"
        )
    )


def test_selection_pair_rejects_independently_forged_rejected_task_rosters(
    tmp_path: Path, binding_stubs: None
) -> None:
    first = build_c2_outcome_blind_selection_record(
        tmp_path,
        locus="A_S",
        task_id="retained-crystallization",
        candidate_roster=[
            {
                "task_id": "retained-crystallization",
                "frozen_rank": 1,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "independent receipt claim",
            },
            {
                "task_id": "placeholder",
                "frozen_rank": 2,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "independent receipt claim",
            },
        ],
        selection_rule={
            "method": "eligible_then_ascending_frozen_rank",
            "formal_participant_outcomes_permitted": False,
            "selection_slot": 1,
            "required_selected_task_count": 2,
        },
        source_binding=_source_binding(),
    )
    second = build_c2_outcome_blind_selection_record(
        tmp_path,
        locus="A_S",
        task_id="rejected-flow",
        candidate_roster=[
            {
                "task_id": "placeholder",
                "frozen_rank": 1,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "independent receipt claim",
            },
            {
                "task_id": "rejected-flow",
                "frozen_rank": 2,
                "eligible_before_formal_outcomes": True,
                "eligibility_basis": "independent receipt claim",
            },
        ],
        selection_rule={
            "method": "eligible_then_ascending_frozen_rank",
            "formal_participant_outcomes_permitted": False,
            "selection_slot": 2,
            "required_selected_task_count": 2,
        },
        source_binding=_source_binding(),
    )

    errors = validate_c2_outcome_blind_selection_pair([first, second], locus="A_S")
    assert any("exact candidate roster" in error for error in errors)
