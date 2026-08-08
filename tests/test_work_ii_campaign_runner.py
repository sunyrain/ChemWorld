from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from scripts.run_work_ii_campaign_pilot import (
    _campaign_card,
    _checkpoint_contract,
    _qualification,
)
from scripts.run_work_ii_five_seed_campaign import _heartbeat

from chemworld.campaign_resources import CampaignResourceLedger

ROOT = Path(__file__).resolve().parents[1]


def _config() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(encoding="utf-8")
    )


def test_public_campaign_card_contains_no_arm_or_seed_identity() -> None:
    serialized = json.dumps(_campaign_card(_config()).to_dict(), sort_keys=True).lower()
    for forbidden in (
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
        "prior_arm",
        "world_seed",
        "seed0",
    ):
        assert forbidden not in serialized


def test_electrochemical_process_time_policy_allows_one_repeat_only() -> None:
    card = _campaign_card(_config())
    assert card.process_time_limit_s == 72_000.0
    assert card.operation_repeat_limits == {"electrolyze": 5}
    ledger = CampaignResourceLedger(card)
    action = {"operation": "electrolyze", "duration_s": 14_400.0}
    for index in range(1, 6):
        event_id = f"electrolyze-{index}"
        assert ledger.preflight(event_id, action).allowed is True
        ledger.record_outcome(
            event_id,
            action,
            {
                "transaction_status": "committed",
                "campaign_resource_report_delta": {"process_time_s": 14_400.0},
            },
        )
    assert ledger.snapshot()["state"]["report_only"]["process_time_s"] == 72_000.0
    assert ledger.preview_rejection_reasons(action) == (
        "operation_repeat_limit:electrolyze",
        "process_time_limit",
    )


def test_aligned_and_misindexed_checkpoint_contracts_are_identical() -> None:
    config = _config()
    assert _checkpoint_contract(config, "aligned_nominal") == _checkpoint_contract(
        config, "misindexed_nominal"
    )


def test_cell_qualification_is_fail_closed() -> None:
    analysis = {
        "complete_experiment_count": 4,
        "right_censored_open_experiment": False,
        "belief_snapshots": [
            {"stage": "pre_evidence"},
            {"stage": "post_neutral"},
            {"stage": "post_discriminating"},
            {"stage": "final"},
        ],
        "resource_rejection_count": 0,
        "final_campaign_resources": {
            "campaign_terminal": True,
            "state": {
                "closed_batches": 4,
                "final_assays": 4,
                "operation_committed_counts": {"electrolyze": 4},
                "report_only": {"process_time_s": 7200.0},
            },
        },
    }
    replay = {"verified": True}
    method_resources = {
        "provider_session_count": 1,
        "provider_usage_pending": False,
        "limits": {
            "input_token_limit": 2_400_000,
            "uncached_input_token_limit": 320_000,
            "output_token_limit": 24_000,
        },
        "agent_usage": {
            "in_flight_model_call_count": 0,
            "input_token_count": 1_500_000,
            "uncached_input_token_count": 150_000,
            "output_token_count": 8_000,
        },
    }
    receipts = [
        {
            "session_scope": "campaign",
            "status": "completed",
            "return_code": 0,
            "final_payload_valid": True,
            "final_payload_status": "campaign_complete",
            "experiment_tool_integrity_verified_after_session": True,
            "lab_tool_integrity_verified_after_session": True,
            "mcp_tool_integrity_verified_after_session": True,
        }
    ]
    passed = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        receipts=receipts,
        process_time_limit_s=72_000.0,
    )
    assert passed["passed"] is True

    failed_replay = _qualification(
        analysis=analysis,
        exact_replay={"verified": False},
        method_resources=method_resources,
        receipts=receipts,
        process_time_limit_s=72_000.0,
    )
    assert failed_replay["passed"] is False
    assert failed_replay["failed_checks"] == ["exact_replay"]

    rejected_analysis = deepcopy(analysis)
    rejected_analysis["resource_rejection_count"] = 1
    failed_resource = _qualification(
        analysis=rejected_analysis,
        exact_replay=replay,
        method_resources=method_resources,
        receipts=receipts,
        process_time_limit_s=72_000.0,
    )
    assert failed_resource["passed"] is False
    assert failed_resource["failed_checks"] == ["no_resource_rejection"]


def test_repeated_heartbeats_preserve_current_cell_coordinate() -> None:
    first = _heartbeat(
        started=0.0,
        completed_cells=0,
        total_cells=15,
        last_event={
            "world_seed": 0,
            "arm": "opaque",
            "stage": "cell_started",
            "step": None,
            "complete_experiments": 0,
            "liveness_counter": 1,
        },
    )
    second = _heartbeat(
        started=0.0,
        completed_cells=0,
        total_cells=15,
        last_event=first,
    )
    assert second["current_world_seed"] == 0
    assert second["current_arm"] == "opaque"
    assert second["current_stage"] == "cell_started"
    assert second["current_step"] is None
    assert second["current_complete_experiments"] == 0
    assert second["liveness_counter"] == first["liveness_counter"] + 1
