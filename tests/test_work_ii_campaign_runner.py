from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import scripts.run_work_ii_campaign_pilot as campaign_runner
import scripts.run_work_ii_five_seed_campaign as five_seed_runner
from scripts.run_work_ii_campaign_pilot import (
    _campaign_card,
    _checkpoint_contract,
    _qualification,
)
from scripts.run_work_ii_five_seed_campaign import _heartbeat

from chemworld.campaign_resources import CampaignResourceLedger
from chemworld.eval.provenance import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]


def _config() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(encoding="utf-8")
    )


def _task_config(name: str) -> dict[str, object]:
    return json.loads((ROOT / f"configs/benchmark/{name}").read_text(encoding="utf-8"))


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


def test_crystallization_process_time_policy_reserves_implicit_stages() -> None:
    config = _task_config("work_ii_crystallization_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 146_400.0
    assert card.implicit_operation_time_s == {
        "filter_crystals": 480.0,
        "quench": 120.0,
    }
    assert card.operation_repeat_limits["filter_crystals"] == 4
    assert card.operation_repeat_limits["quench"] == 4


def test_distillation_process_time_policy_includes_evaporation_and_quench() -> None:
    config = _task_config("work_ii_distillation_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 202_080.0
    assert card.implicit_operation_time_s == {"quench": 120.0}
    assert card.operation_repeat_limits["evaporate"] == 4
    assert card.operation_repeat_limits["quench"] == 4


def test_partition_process_time_policy_covers_four_lifecycles_and_one_repeat() -> None:
    config = _task_config("work_ii_partition_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 9_000.0
    assert card.operation_attempt_limit == 48
    assert card.vessel_start_limit == 4
    assert card.final_assay_limit == 4
    assert card.operation_repeat_limits == {"mix": 5, "settle": 5, "separate_phase": 4}
    assert card.stock_limits == {
        "extractant_L": 0.12,
        "phase_liquid_L": 0.096,
        "solvent_L": 0.112,
    }


def test_safety_process_time_policy_covers_four_lifecycles_and_one_repeat() -> None:
    config = _task_config("work_ii_safety_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 36_480.0
    assert card.implicit_operation_time_s == {"quench": 120.0}
    assert card.operation_attempt_limit == 40
    assert card.operation_repeat_limits == {"heat": 5, "quench": 4}


def test_all_five_campaign_cards_freeze_participant_owned_closeout_margin() -> None:
    config_names = (
        "work_ii_campaign_pilot.json",
        "work_ii_crystallization_campaign.json",
        "work_ii_distillation_campaign.json",
        "work_ii_partition_campaign.json",
        "work_ii_safety_campaign.json",
    )
    expected = {
        "planned_batches": 4,
        "final_assay_path_operations_per_batch": 2,
        "discard_path_operations_per_batch": 1,
        "final_assay_path_total_operation_reserve": 8,
        "discard_path_total_operation_reserve": 4,
        "policy": "participant_controlled_advisory_no_hidden_allocation",
        "automatic_action_repair": False,
        "automatic_closeout": False,
    }
    for config_name in config_names:
        config = _task_config(config_name)
        assert _campaign_card(config).to_dict()["metadata"]["closeout_policy"] == expected


def test_all_five_task_checkpoint_contracts_match_across_informed_arms() -> None:
    config_names = (
        "work_ii_campaign_pilot.json",
        "work_ii_crystallization_campaign.json",
        "work_ii_distillation_campaign.json",
        "work_ii_partition_campaign.json",
        "work_ii_safety_campaign.json",
    )
    for config_name in config_names:
        config = _task_config(config_name)
        assert _checkpoint_contract(config, "opaque")["snapshot_stages"] == [
            "pre_evidence",
            "after_experiment_1",
            "after_experiment_2",
            "final",
        ]
        assert _checkpoint_contract(config, "aligned_nominal") == _checkpoint_contract(
            config, "misindexed_nominal"
        )


def test_qualification_accepts_frozen_neutral_snapshot_stage_ids() -> None:
    config = _config()
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "best public campaign evidence",
    }
    recommendation_sha256 = canonical_json_sha256(recommendation)
    analysis = {
        "complete_experiment_count": 4,
        "experiments": [{"experiment_index": index} for index in range(1, 5)],
        "right_censored_open_experiment": False,
        "belief_snapshots": [{"stage": stage} for stage in config["snapshot_stages"]],
        "resource_rejection_count": 0,
        "final_campaign_resources": {
            "campaign_terminal": True,
            "state": {
                "closed_batches": 4,
                "final_assays": 4,
                "operation_committed_counts": {},
                "report_only": {"process_time_s": 7200.0},
            },
        },
        "final_recommendation": recommendation,
        "final_recommendation_sha256": recommendation_sha256,
        "execution_audit": {"passed": True},
    }
    result = _qualification(
        analysis=analysis,
        exact_replay={"verified": True},
        method_resources={
            "provider_session_count": 1,
            "provider_usage_pending": False,
            "provider_usage_accounting_complete": True,
            "in_flight_model_call_count": 0,
            "input_token_count": 1,
            "uncached_input_token_count": 1,
            "output_token_count": 1,
        },
        method_resource_limits={
            "complete_experiment_limit": 4,
            "input_token_limit": 2,
            "uncached_input_token_limit": 2,
            "output_token_limit": 2,
        },
        receipts=[
            {
                "session_scope": "campaign",
                "status": "completed",
                "return_code": 0,
                "final_payload_valid": True,
                "final_payload_status": "campaign_complete",
                "final_recommendation": recommendation,
                "final_recommendation_sha256": recommendation_sha256,
                "experiment_tool_integrity_verified_after_session": True,
                "lab_tool_integrity_verified_after_session": True,
                "mcp_tool_integrity_verified_after_session": True,
            }
        ],
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        required_snapshot_stages=config["snapshot_stages"],
    )
    assert result["passed"] is True


def test_aligned_and_misindexed_checkpoint_contracts_are_identical() -> None:
    config = _config()
    assert _checkpoint_contract(config, "aligned_nominal") == _checkpoint_contract(
        config, "misindexed_nominal"
    )


def test_cell_qualification_is_fail_closed() -> None:
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "best public campaign evidence",
    }
    recommendation_sha256 = canonical_json_sha256(recommendation)
    analysis = {
        "complete_experiment_count": 4,
        "experiments": [{"experiment_index": index} for index in range(1, 5)],
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
        "final_recommendation": recommendation,
        "final_recommendation_sha256": recommendation_sha256,
        "execution_audit": {"passed": True},
    }
    replay = {"verified": True}
    method_resources = {
        "provider_session_count": 1,
        "provider_usage_pending": False,
        "provider_usage_accounting_complete": True,
        "in_flight_model_call_count": 0,
        "input_token_count": 1_500_000,
        "uncached_input_token_count": 150_000,
        "output_token_count": 8_000,
    }
    method_resource_limits = {
        "complete_experiment_limit": 4,
        "input_token_limit": 2_400_000,
        "uncached_input_token_limit": 320_000,
        "output_token_limit": 24_000,
    }
    receipts = [
        {
            "session_scope": "campaign",
            "status": "completed",
            "return_code": 0,
            "final_payload_valid": True,
            "final_payload_status": "campaign_complete",
            "final_recommendation": recommendation,
            "final_recommendation_sha256": recommendation_sha256,
            "experiment_tool_integrity_verified_after_session": True,
            "lab_tool_integrity_verified_after_session": True,
            "mcp_tool_integrity_verified_after_session": True,
        }
    ]
    passed = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
    )
    assert passed["passed"] is True

    failed_replay = _qualification(
        analysis=analysis,
        exact_replay={"verified": False},
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
    )
    assert failed_replay["passed"] is False
    assert failed_replay["failed_checks"] == ["exact_replay"]

    rejected_analysis = deepcopy(analysis)
    rejected_analysis["resource_rejection_count"] = 1
    failed_resource = _qualification(
        analysis=rejected_analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
    )
    assert failed_resource["passed"] is False
    assert failed_resource["failed_checks"] == ["no_resource_rejection"]

    rejected_audit_analysis = deepcopy(analysis)
    rejected_audit_analysis["execution_audit"] = {"passed": False}
    failed_audit = _qualification(
        analysis=rejected_audit_analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
    )
    assert failed_audit["passed"] is False
    assert failed_audit["failed_checks"] == ["execution_audit"]

    over_limit = deepcopy(method_resources)
    over_limit["uncached_input_token_count"] = 320_001
    failed_usage = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=over_limit,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
    )
    assert failed_usage["passed"] is False
    assert failed_usage["failed_checks"] == ["provider_usage_reconciled"]


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


def test_single_arm_mode_leaves_cell_directory_creation_to_cell_runner(
    monkeypatch,
    tmp_path: Path,
) -> None:
    output = tmp_path / "seed-0" / "opaque"

    def fake_run_cell(**kwargs):
        cell_root = kwargs["cell_root"]
        assert cell_root == output.resolve()
        assert not cell_root.exists()
        cell_root.mkdir()
        return {"arm": "opaque", "completed": True}

    monkeypatch.setattr(campaign_runner, "_run_cell", fake_run_cell)
    report = campaign_runner.run(
        argparse.Namespace(
            config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
            output=output,
            progress_file=tmp_path / "progress.jsonl",
            world_seed=0,
            prior_arm="opaque",
        )
    )
    assert report["completed_cell_count"] == 1
    assert (output / "report.json").exists()


def test_three_arm_qualification_retains_the_whole_triplet_after_failure(
    monkeypatch,
    tmp_path: Path,
) -> None:
    observed: list[str] = []

    def fake_run_cell(**kwargs):
        arm = kwargs["arm"]
        observed.append(arm)
        return {
            "arm": arm,
            "completed": arm != "opaque",
            "failure": (
                {"type": "SyntheticFailure", "message": "retained"} if arm == "opaque" else None
            ),
        }

    monkeypatch.setattr(campaign_runner, "_run_cell", fake_run_cell)
    output = tmp_path / "triplet"
    report = campaign_runner.run(
        argparse.Namespace(
            config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
            output=output,
            progress_file=tmp_path / "progress.jsonl",
            world_seed=0,
            prior_arm=None,
        )
    )
    assert observed == ["opaque", "aligned_nominal", "misindexed_nominal"]
    assert report["cell_count"] == 3
    assert report["completed_cell_count"] == 2
    assert report["results"][0]["failure"]["type"] == "SyntheticFailure"


def test_five_seed_runner_uses_os_isolated_three_cell_triplets(
    monkeypatch,
    tmp_path: Path,
) -> None:
    fake_runner = tmp_path / "fake_cell_runner.py"
    fake_runner.write_text(
        """
import argparse
import json
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--config")
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--progress-file")
parser.add_argument("--world-seed", type=int, required=True)
parser.add_argument("--prior-arm", required=True)
args = parser.parse_args()
args.output.mkdir(parents=True)
started = {"stage": "cell_started", "world_seed": args.world_seed, "arm": args.prior_arm}
print(json.dumps(started), flush=True)
time.sleep(0.05)
row = {
    "arm": args.prior_arm,
    "completed": True,
    "qualification": {"passed": True, "failed_checks": []},
}
(args.output / "summary.json").write_text(json.dumps(row), encoding="utf-8")
completed = {
    "stage": "cell_completed",
    "world_seed": args.world_seed,
    "arm": args.prior_arm,
    "completed": True,
}
print(json.dumps(completed), flush=True)
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(five_seed_runner, "RUNNER", fake_runner)
    monkeypatch.setattr(five_seed_runner, "git_worktree_dirty", lambda _root: False)
    monkeypatch.setattr(five_seed_runner, "git_source_commit", lambda _root: "test-commit")
    monkeypatch.setenv("WELLAU_API_KEY", "test-key")
    output = tmp_path / "output"
    progress = tmp_path / "progress.jsonl"
    report = five_seed_runner.run(
        argparse.Namespace(
            config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
            output=output,
            progress_file=progress,
            world_seed=[0, 1, 2, 3, 4],
            heartbeat_interval_s=0.05,
            max_concurrency=3,
        )
    )
    assert report["all_cells_completed"] is True
    assert report["completed_cell_count"] == 15
    assert report["max_concurrency"] == 3
    assert len(report["seed_reports"]) == 5
    assert all(seed["completed_cell_count"] == 3 for seed in report["seed_reports"])
    events = [json.loads(line) for line in progress.read_text(encoding="utf-8").splitlines()]
    triplets = [event for event in events if event.get("event") == "seed_triplet_started"]
    assert len(triplets) == 5
    assert all(len(event["active_cells"]) == 3 for event in triplets)
