from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    C2_OUTCOME_BLIND_SELECTION_VERSION,
    C2_TASK_STAGE_ORDER,
    _task_receipt_errors,
    build_c2_task_admission_receipt,
    c2_outcome_blind_selection_sha256,
    c2_task_admission_receipt_sha256,
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
    campaign_path = tmp_path / "campaign.json"
    write_json_atomic(campaign_path, campaign)
    stages: dict[str, Path] = {}
    for stage in C2_TASK_STAGE_ORDER:
        path = tmp_path / f"{stage.lower()}.json"
        write_json_atomic(path, _stage(stage, task_id))
        stages[stage] = path
    selection = {
        "schema_version": C2_OUTCOME_BLIND_SELECTION_VERSION,
        "locus": locus,
        "task_id": task_id,
        "selected_before_formal_participant_outcomes": True,
        "formal_participant_outcomes_observed": 0,
        "formal_participant_outcomes_used": False,
        "selection_rule_frozen_before_evidence_review": True,
        "source_binding": _source_binding(),
    }
    selection["selection_sha256"] = c2_outcome_blind_selection_sha256(selection)
    selection_path = tmp_path / "selection.json"
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


def test_missing_stage_roster_is_rejected(tmp_path: Path) -> None:
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
