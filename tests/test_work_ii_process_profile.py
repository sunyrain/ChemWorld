from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.campaign_resources import CampaignResourceCard, CampaignResourceLedger
from chemworld.eval.policy_validity_contract import METRICS
from chemworld.eval.work_ii_process_profile import (
    audit_work_ii_hidden_boundary,
    build_work_ii_execution_artifacts,
    build_work_ii_execution_audit,
    build_work_ii_process_profile,
    replay_work_ii_campaign_resources,
    validate_work_ii_process_profile,
)


def _records() -> list[dict[str, object]]:
    card = CampaignResourceCard(
        card_id="work-ii-process-profile-test",
        operation_attempt_limit=20,
        vessel_start_limit=3,
        final_assay_limit=3,
        nonfinal_instrument_use_limit=3,
        stock_limits={"solvent_L": 0.1},
        process_time_limit_s=100.0,
        implicit_operation_time_s={},
        operation_repeat_limits={},
        metadata={"scope": "test"},
    )
    ledger = CampaignResourceLedger(card)
    rows: list[dict[str, object]] = []
    schedule = [
        ({"operation": "add_solvent", "solvent": 0, "volume_L": 0.01}, True, "committed", {}, None),
        ({"operation": "add_reagent", "amount_mol": 0.01}, False, "validation_failed", {}, None),
        (
            {"operation": "measure", "instrument": "uvvis"},
            False,
            "committed",
            {"physical_cost": 0.2},
            None,
        ),
        (
            {"operation": "heat", "duration_s": 10.0},
            False,
            "committed",
            {"process_time_s": 10.0, "accumulated_risk": 0.1},
            None,
        ),
        ({"operation": "terminate"}, False, "committed", {}, None),
        (
            {"operation": "measure", "instrument": "final_assay"},
            False,
            "committed",
            {"physical_cost": 0.3},
            0.4,
        ),
        ({"operation": "add_solvent", "solvent": 0, "volume_L": 0.01}, True, "committed", {}, None),
        ({"operation": "discard_batch"}, False, "committed", {}, None),
        ({"operation": "add_solvent", "solvent": 0, "volume_L": 0.01}, True, "committed", {}, None),
        ({"operation": "terminate"}, False, "committed", {}, None),
        (
            {"operation": "measure", "instrument": "final_assay"},
            False,
            "committed",
            {"physical_cost": 0.4},
            0.8,
        ),
    ]
    for step, (action, starts_vessel, status, report_delta, score) in enumerate(
        schedule,
        start=1,
    ):
        event_id = f"event-{step:02d}"
        preflight = ledger.preflight(
            event_id,
            action,
            starts_vessel=starts_vessel,
        )
        outcome = {
            "transaction_status": status,
            "campaign_resource_report_delta": report_delta,
        }
        delta = ledger.record_outcome(
            event_id,
            action,
            outcome,
            starts_vessel=starts_vessel,
        )
        snapshot = ledger.snapshot()
        receipt = {
            "event_id": event_id,
            "preflight": preflight.to_dict(),
            "operation_committed": status == "committed",
            "outcome_delta": delta.to_dict(),
            "rejected": not preflight.allowed,
            "rejection_reasons": list(preflight.rejection_reasons),
            "transaction_status": status,
        }
        rows.append(
            {
                "step": step,
                "action": action,
                "operation_type": action["operation"],
                "instrument": action.get("instrument"),
                "transaction_status": status,
                "leaderboard_score": score,
                "campaign_resource_card": card.to_dict(),
                "campaign_resource_card_sha256": card.card_sha256,
                "agent_view": {
                    "tool_json": {
                        "campaign_state": {
                            "campaign_resources": {
                                "ledger_sha256": snapshot["ledger_sha256"],
                                "state": snapshot["state"],
                                "last_event_id": event_id,
                                "latest_receipt": receipt,
                            }
                        }
                    }
                },
                "agent_visible_observation": {"observation": {"score": score}},
            }
        )
    return rows


def _exact_replay(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "verified": True,
        "checked_steps": len(rows),
        "max_abs_error": 0.0,
        "mismatches": [],
    }


def test_work_ii_profile_reuses_exact_19_coordinate_surface() -> None:
    rows = _records()
    resources = replay_work_ii_campaign_resources(rows)
    assert resources["status"] == "passed"
    assert resources["resource_event_count"] == len(rows)
    assert resources["recorded_ledger_sha256"] == resources["rebuilt_ledger_sha256"]

    profile = build_work_ii_process_profile(
        rows,
        resources,
        planned_experiment_count=3,
        terminal_state="completed",
    )
    observed = {
        metric_id
        for axis in profile["construct_axes"].values()
        for metric_id in axis
    }
    assert observed == {spec.metric_id for spec in METRICS}
    assert len(observed) == 19
    assert profile["counts"] == {
        "participant_record_count": 11,
        "participant_operation_attempt_count": 11,
        "committed_operation_count": 10,
        "closed_lifecycle_count": 3,
        "final_assay_count": 2,
        "discard_count": 1,
        "open_lifecycle_record_count": 0,
        "measured_lifecycle_count": 1,
    }
    evidence = profile["construct_axes"]["evidence_acquisition"]
    assert evidence["measured_lifecycle_fraction"]["value"] == 1 / 3
    conditioned = profile["construct_axes"]["evidence_conditioned_action"]
    assert conditioned["continued_after_measurement_fraction"]["value"] == 1 / 3
    assert conditioned["threshold_eligible_fraction"]["value"] is None
    assert conditioned["threshold_eligible_fraction"]["applicable"] is False
    assert profile["endpoint_context"]["mean_assayed_score"]["value"] == pytest.approx(0.6)
    assert profile["endpoint_context"]["best_assayed_score"]["value"] == 0.8
    assert validate_work_ii_process_profile(profile) == []

    boundary = audit_work_ii_hidden_boundary(rows)
    audit = build_work_ii_execution_audit(
        rows,
        _exact_replay(rows),
        profile,
        resources,
        boundary,
    )
    assert audit["passed"] is True
    assert audit["failed_checks"] == []


def test_resource_replay_and_hidden_boundary_fail_closed() -> None:
    rows = _records()
    tampered = deepcopy(rows)
    resources = tampered[3]["agent_view"]["tool_json"]["campaign_state"][
        "campaign_resources"
    ]
    resources["latest_receipt"]["outcome_delta"]["report_only"][
        "process_time_s"
    ] = 11.0
    report = replay_work_ii_campaign_resources(tampered)
    assert report["status"] == "failed"
    assert any("ledger hash mismatch" in error for error in report["errors"])

    leaked = _records()
    leaked[0]["agent_view"]["prior_arm"] = "misindexed_nominal"
    boundary = audit_work_ii_hidden_boundary(leaked)
    assert boundary["status"] == "failed"
    assert boundary["leak_count"] >= 1


def test_execution_artifacts_reject_evaluator_owned_records() -> None:
    rows = _records()
    rows[0]["execution_role"] = "held_out_evaluator"
    artifacts = build_work_ii_execution_artifacts(
        rows,
        _exact_replay(rows),
        planned_experiment_count=3,
        terminal_state="completed",
    )
    assert artifacts["process_profile"] is None
    assert artifacts["hidden_boundary_audit"]["status"] == "failed"
    assert artifacts["execution_audit"]["passed"] is False
    assert "process_profile" in artifacts["execution_audit"]["failed_checks"]
