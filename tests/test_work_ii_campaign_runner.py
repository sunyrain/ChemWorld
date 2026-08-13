from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import scripts.run_work_ii_campaign_pilot as campaign_runner
import scripts.run_work_ii_five_seed_campaign as five_seed_runner
from scripts.evaluate_work_ii_catalyst_deactivation_paired_provider_campaigns import (
    _agent_system_contrast,
    _paired_analysis,
    _validate_configs,
)
from scripts.run_work_ii_campaign_pilot import (
    _agent_invalid_online_limits,
    _analyze,
    _arm_initial_world_model,
    _arm_material_information,
    _campaign_card,
    _checkpoint_contract,
    _provider_error_online_limit,
    _qualification,
    _required_operation_counts,
    _world_interventions,
)
from scripts.run_work_ii_five_seed_campaign import (
    _execution_scope,
    _heartbeat,
    _preoperation_infrastructure_failure,
    _run_with_automatic_infrastructure_resume,
    _systemic_preoperation_failure,
)

from chemworld.agents.base import BaseAgent
from chemworld.campaign_resources import CampaignResourceLedger
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_resource_calibration_v02 import (
    _materialize_runtime_config,
)

ROOT = Path(__file__).resolve().parents[1]


def test_analysis_closes_discarded_batch_without_polluting_next_recipe() -> None:
    records = [
        {
            "action": {"operation": "add_catalyst", "catalyst": 1},
            "operation_type": "add_catalyst",
            "transaction_status": "committed",
        },
        {
            "action": {"operation": "discard_batch", "reason": "abandon"},
            "operation_type": "discard_batch",
            "transaction_status": "committed",
        },
        {
            "action": {"operation": "add_solvent", "volume_L": 0.02},
            "operation_type": "add_solvent",
            "transaction_status": "committed",
        },
        {
            "action": {"operation": "measure", "instrument": "final_assay"},
            "operation_type": "measure",
            "instrument": "final_assay",
            "transaction_status": "committed",
            "leaderboard_score": 0.1,
            "observation": {"score": 0.1},
            "agent_view": {
                "tool_json": {
                    "available_actions": [],
                    "campaign_state": {
                        "campaign_resources": {"campaign_terminal": True}
                    },
                }
            },
        },
    ]

    analysis = _analyze(records, [], final_metric_ids=["score"])

    assert analysis["complete_experiment_count"] == 1
    assert analysis["right_censored_open_experiment"] is False
    assert analysis["nonterminal_no_legal_actions"] is False
    assert analysis["experiments"][0]["committed_operations"] == [
        records[2]["action"],
        records[3]["action"],
    ]


def test_analysis_does_not_call_terminal_empty_affordance_a_deadlock() -> None:
    records = [
        {
            "action": {"operation": "add_catalyst", "catalyst": 1},
            "operation_type": "add_catalyst",
            "transaction_status": "committed",
            "agent_view": {
                "tool_json": {
                    "available_actions": [],
                    "campaign_state": {
                        "campaign_resources": {"campaign_terminal": True}
                    },
                }
            },
        }
    ]

    analysis = _analyze(records, [], final_metric_ids=["score"])

    assert analysis["right_censored_open_experiment"] is True
    assert analysis["last_legal_action_count"] == 0
    assert analysis["nonterminal_no_legal_actions"] is False


def test_w226_operation_counts_have_no_historical_runner_fallback() -> None:
    assert _required_operation_counts({"qualification": {}}) == {}
    assert _required_operation_counts(
        {"qualification": {"required_operation_counts": {"step": [8, 8]}}}
    ) == {"step": [8, 8]}
    with pytest.raises(ValueError, match="requires explicit required_operation_counts"):
        _required_operation_counts(
            {"w2_26_runtime_identity": {}, "qualification": {}}
        )


def test_w226_scripted_participant_traverses_production_semantic_path(
    tmp_path: Path,
) -> None:
    source = _config()
    config = _materialize_runtime_config(
        source,
        locus="A_E",
        task_id="electrochemical-conversion",
        rounds=8,
    )
    config["snapshot_stages"] = ["pre_evidence", "final"]
    config["campaign"].update(
        {
            "complete_experiments": 1,
            "operation_attempt_limit": 6,
            "vessel_start_limit": 1,
            "final_assay_limit": 1,
            "operation_repeat_limits": {"electrolyze": 1},
            "checkpoint_complete_experiments": [0, 1],
        }
    )
    config["campaign"]["closeout_policy"].update(
        {
            "planned_batches": 1,
            "final_assay_path_total_operation_reserve": 2,
            "discard_path_total_operation_reserve": 1,
        }
    )
    config["method_resources"].update(
        {
            "operation_limit": 6,
            "complete_experiment_limit": 1,
            "checkpoint_complete_experiments": [1],
        }
    )
    config["qualification"].update(
        {
            "minimum_unique_recipes": 1,
            "maximum_exact_repeats": 0,
        }
    )
    recommendation = {
        "selected_experiment_index": 1,
        "selection_rationale": "only completed canary experiment",
    }
    recommendation_sha256 = canonical_json_sha256(recommendation)

    class ScriptedCampaignParticipant(BaseAgent):
        name = "scripted-production-semantic-canary"

        def __init__(self, **_kwargs: Any) -> None:
            self.actions = [
                {"operation": "add_solvent", "volume_L": 0.025, "solvent": 1},
                {"operation": "add_reagent", "amount_mol": 0.012},
                {
                    "operation": "set_potential",
                    "potential_V": 1.10,
                    "current_mA": 70.0,
                    "electrolyte_profile": 2,
                },
                {"operation": "electrolyze", "duration_s": 180.0},
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]

        def act(self, history: list[Any]) -> dict[str, Any]:
            return self.actions[len(history)]

        def method_resource_usage(self) -> dict[str, Any]:
            return {
                "schema_version": "chemworld-method-resource-usage-0.1",
                "accounting_complete": True,
                "provider_usage_pending": False,
                "provider_usage_accounting_complete": True,
                "provider_call_accounting_complete": True,
                "provider_token_accounting_complete": True,
                "provider_cache_accounting_complete": True,
                "monetary_accounting_complete": True,
                "in_flight_model_call_count": 0,
                "model_call_count": 1,
                "input_token_count": 10,
                "cached_input_token_count": 0,
                "uncached_input_token_count": 10,
                "output_token_count": 5,
                "training_environment_step_count": 0,
                "monetary_cost_usd": 0.0,
                "cpu_time_s": 0.0,
                "gpu_time_s": 0.0,
                "model_provenance": {},
                "provider_session_count": 1,
                "provider_process_attempt_count": 1,
                "accepted_provider_session_count": 1,
                "accepted_participant_model_call_count": 1,
                "unattributed_pre_action_process_attempt_count": 0,
            }

        def provider_receipts(self) -> list[dict[str, Any]]:
            return [
                {
                    "session_scope": "campaign",
                    "status": "completed",
                    "return_code": 0,
                    "final_payload_valid": True,
                    "final_payload_status": "campaign_complete",
                    "final_recommendation": recommendation,
                    "final_recommendation_sha256": recommendation_sha256,
                    "belief_snapshots": [
                        {
                            "stage": "pre_evidence",
                            "prior_assessment": {
                                "reliability_probability": 0.5,
                                "suspected_misindexed_fields": [],
                            },
                        },
                        {
                            "stage": "final",
                            "prior_assessment": {
                                "reliability_probability": 0.5,
                                "suspected_misindexed_fields": [],
                            },
                        },
                    ],
                    "experiment_tool_integrity_verified_after_session": True,
                    "lab_tool_integrity_verified_after_session": True,
                    "mcp_tool_integrity_verified_after_session": True,
                    "recovered_mcp_tool_failure_count": 0,
                    "current_consecutive_mcp_tool_failure_count": 0,
                    "maximum_consecutive_mcp_tool_failure_count": 0,
                    "provider_error_event_count": 0,
                    "session_elapsed_s": 0.0,
                    "pre_action_retry_classification": "terminal_accepted",
                    "accepted_action_count": 6,
                }
            ]

    cell_root = tmp_path / "cell"
    row = campaign_runner._run_cell(
        config=config,
        world_seed=0,
        arm="opaque",
        cell_index=1,
        total_cells=1,
        cell_root=cell_root,
        progress_path=tmp_path / "progress.jsonl",
        agent_invalid_enforcement="measure_only",
        provider_error_enforcement="measure_only",
        agent_factory=ScriptedCampaignParticipant,
    )

    trajectory = [
        json.loads(line)
        for line in (cell_root / "trajectory.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [record["action"] for record in trajectory] == ScriptedCampaignParticipant().actions
    assert row["analysis"]["complete_experiment_count"] == 1
    assert row["analysis"]["committed_operation_count"] == 6
    assert row["exact_replay"]["verified"] is True
    assert row["analysis"]["execution_audit"]["passed"] is True
    assert row["qualification"]["passed"] is True
    assert row["completed"] is True
    assert json.loads((cell_root / "summary.json").read_text(encoding="utf-8")) == row
    assert "synthetic" not in json.dumps(row, sort_keys=True).lower()


def test_five_seed_runner_accepts_only_frozen_schedule_shapes() -> None:
    assert _execution_scope([0]) == "pilot_seed_triplet"
    assert _execution_scope([0, 1, 2, 3, 4]) == "five_seed_task_block"
    assert _execution_scope([1, 2, 3, 4]) == "terminal_seed0_preserving_continuation"
    with pytest.raises(ValueError, match="exact continuation"):
        _execution_scope([0, 1, 2, 3])


def test_agent_invalid_measure_only_is_resource_calibration_only() -> None:
    provider = {
        "max_recovered_mcp_tool_failures": 3,
        "max_consecutive_mcp_tool_failures": 1,
    }

    assert _agent_invalid_online_limits(
        provider, agent_invalid_enforcement=None
    ) == (3, 1)
    assert _agent_invalid_online_limits(
        provider, agent_invalid_enforcement="measure_only"
    ) == (None, None)
    with pytest.raises(RuntimeError, match="not frozen"):
        _agent_invalid_online_limits(
            provider, agent_invalid_enforcement="ignore_failures"
        )


def test_provider_error_measure_only_is_resource_calibration_only() -> None:
    provider = {"max_provider_error_events": 1}

    assert _provider_error_online_limit(
        provider, provider_error_enforcement=None
    ) == 1
    assert (
        _provider_error_online_limit(
            provider, provider_error_enforcement="measure_only"
        )
        is None
    )
    with pytest.raises(RuntimeError, match="not frozen"):
        _provider_error_online_limit(
            provider, provider_error_enforcement="ignore_failures"
        )


def _preoperation_row(
    *,
    failure_type: str = "InteractiveCodexExperimentError",
    receipt_failure_type: str = "ExperimentCodexIPCError",
) -> dict[str, object]:
    return {
        "failure": {"type": failure_type, "message": "pre-operation failure"},
        "analysis": {
            "operation_attempt_count": 0,
            "committed_operation_count": 0,
            "belief_snapshots": [],
            "final_recommendation": None,
        },
        "method_resources": {
            "provider_usage_observed": False,
            "input_token_count": 0,
            "uncached_input_token_count": 0,
            "cached_input_token_count": 0,
            "output_token_count": 0,
        },
        "provider_receipts": [
            {
                "status": "interrupted_before_next_action",
                "failure_type": receipt_failure_type,
                "usage_observed": False,
                "mcp_tool_integrity_verified_after_session": True,
                "experiment_tool_integrity_verified_after_session": True,
                "lab_tool_integrity_verified_after_session": True,
                "belief_snapshot_count": 0,
                "final_recommendation": None,
                "usage": {
                    "prompt_tokens": 0,
                    "prompt_cache_hit_tokens": 0,
                    "prompt_cache_miss_tokens": 0,
                    "prompt_cache_write_tokens": 0,
                    "completion_tokens": 0,
                    "reasoning_output_tokens": 0,
                    "total_tokens": 0,
                },
            }
        ],
    }


def test_preoperation_infrastructure_classification_is_fail_closed() -> None:
    assert _preoperation_infrastructure_failure(_preoperation_row(), records=[]) is not None
    assert (
        _preoperation_infrastructure_failure(
            _preoperation_row(failure_type="OSError", receipt_failure_type="agent_closed"),
            records=[],
        )
        is not None
    )
    agent_failure = _preoperation_row(receipt_failure_type="max_recovered_mcp_tool_failures")
    assert _preoperation_infrastructure_failure(agent_failure, records=[]) is None
    attempted = _preoperation_row()
    assert _preoperation_infrastructure_failure(
        attempted,
        records=[{"transaction_status": "campaign_resource_rejected"}],
    ) is None
    tampered = _preoperation_row()
    tampered["provider_receipts"][0]["mcp_tool_integrity_verified_after_session"] = False
    assert _preoperation_infrastructure_failure(tampered, records=[]) is None
    accounted_usage = _preoperation_row(failure_type="OSError")
    accounted_usage["method_resources"]["input_token_count"] = 1
    assert _preoperation_infrastructure_failure(accounted_usage, records=[]) is None
    receipt_usage = _preoperation_row(failure_type="OSError")
    receipt_usage["provider_receipts"][0]["usage"]["total_tokens"] = 1
    assert _preoperation_infrastructure_failure(receipt_usage, records=[]) is None


def test_automatic_infrastructure_resume_runs_only_the_missing_pass(monkeypatch) -> None:
    calls: list[bool] = []
    reports = iter(
        [
            {"automatic_infrastructure_resume_eligible": True},
            {"automatic_infrastructure_resume_eligible": False, "all_cells_terminal": True},
        ]
    )

    def fake_run(args: argparse.Namespace) -> dict[str, object]:
        calls.append(bool(args.resume))
        return next(reports)

    monkeypatch.setattr(five_seed_runner, "run", fake_run)
    args = argparse.Namespace(resume=False)
    result = _run_with_automatic_infrastructure_resume(args)
    assert calls == [False, True]
    assert result["all_cells_terminal"] is True


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


def test_nested_initial_model_arm_keeps_material_information_opaque() -> None:
    config = _config()
    config["prior_arms"]["aligned_nominal"] = {
        "material_information": {"mode": "opaque_codes"},
        "initial_world_model": {
            "schema_version": "chemworld-work-ii-initial-world-model-0.1",
            "locus": "parametric",
            "availability": "supplied_incomplete_model",
        },
    }

    assert _arm_material_information(config, "aligned_nominal") == {
        "mode": "opaque_codes"
    }
    assert _arm_initial_world_model(config, "aligned_nominal") == {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "parametric",
        "availability": "supplied_incomplete_model",
    }
    assert _arm_initial_world_model(config, "opaque") is None


def test_campaign_runner_keeps_world_interventions_host_owned() -> None:
    config = _config()
    assert _world_interventions(config) == []
    intervention = {
        "kind": "mechanism_family",
        "mode": "topology_family",
        "severity": 1.0,
        "topology_change": {
            "reaction_role": "catalyst_deactivation_pathway",
            "transform_id": "stable_catalyst_topology_v1",
        },
    }
    config["world_interventions"] = [intervention]
    assert _world_interventions(config) == [intervention]
    serialized_card = json.dumps(_campaign_card(config).to_dict(), sort_keys=True)
    assert "stable_catalyst" not in serialized_card
    assert "catalyst_deactivation_pathway" not in serialized_card


def test_catalyst_provider_configs_differ_only_by_hidden_law() -> None:
    deactivating = _task_config(
        "work_ii_catalyst_deactivation_real_provider_deactivating_campaign_seed0.json"
    )
    stable = _task_config(
        "work_ii_catalyst_deactivation_real_provider_stable_campaign_seed0.json"
    )
    audit = _validate_configs(
        {"deactivating_baseline": deactivating, "stable_catalyst": stable}
    )
    assert audit["matched_outside_hidden_law"] is True
    assert audit["participant_campaign_count"] == 2
    assert audit["complete_experiments_per_campaign"] == 8


def test_paired_catalyst_analysis_applies_frozen_gates_per_recipe() -> None:
    rows = []
    for source_law, experiment_index, gaps in (
        ("deactivating_baseline", 1, {"yield": 0.051, "conversion": 0.052, "selectivity": 0.01}),
        ("stable_catalyst", 1, {"yield": 0.01, "conversion": 0.01, "selectivity": 0.055}),
    ):
        baseline = {
            "yield": 0.20,
            "conversion": 0.40,
            "selectivity": 0.50,
            "safety_risk": 0.10,
            "score": 0.20,
        }
        stable_metrics = {
            metric: baseline[metric] + gaps.get(metric, 0.0) for metric in baseline
        }
        for target_law, metrics, mechanism_hash in (
            ("deactivating_baseline", baseline, "baseline"),
            ("stable_catalyst", stable_metrics, "stable"),
        ):
            rows.append(
                {
                    "source_law_id": source_law,
                    "experiment_index": experiment_index,
                    "target_law_id": target_law,
                    "action_plan_sha256": f"recipe-{source_law}-{experiment_index}",
                    "observation_seed": experiment_index,
                    "mechanism_hash": mechanism_hash,
                    "metrics": metrics,
                    "safe": True,
                }
            )
    report = _paired_analysis(rows)
    assert report["paired_recipe_count"] == 2
    assert report["any_primary_metric_exceeds_gate"] is True
    assert report["any_recipe_has_two_metrics_above_gate"] is True
    assert report["metric_reports"]["selectivity"]["absolute_gate_exceedance_count"] == 1


def test_agent_system_catalyst_contrast_is_separate_from_physics_effect() -> None:
    campaigns = {}
    for law_id, offset in (("deactivating_baseline", 0.0), ("stable_catalyst", 0.1)):
        campaigns[law_id] = {
            "recipes": [
                {
                    "experiment_index": index,
                    "recipe_sha256": f"{law_id}-{index}",
                    "provider_leaderboard_score": 0.1 + offset,
                    "provider_final_metrics": {
                        "yield": 0.2 + offset,
                        "conversion": 0.4 + offset,
                        "selectivity": 0.5 + offset,
                        "safety_risk": 0.1,
                        "score": 0.1 + offset,
                    },
                }
                for index in range(1, 9)
            ]
        }
    report = _agent_system_contrast(campaigns)
    assert report["closed_loop_above_reference_gate_observed"] is True
    assert report["rounds_with_two_primary_metrics_above_reference_gate"] == 8
    assert report["all_round_recipes_identical"] is False
    assert report["causal_physics_effect"] is False


def test_electrochemical_process_time_policy_allows_two_exact_repeat_stages() -> None:
    card = _campaign_card(_config())
    assert card.process_time_limit_s == 132_480.0
    assert card.operation_repeat_limits == {"electrolyze": 8}
    ledger = CampaignResourceLedger(card)
    action = {"operation": "electrolyze", "duration_s": 14_400.0}
    for index in range(1, 9):
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
    assert ledger.snapshot()["state"]["report_only"]["process_time_s"] == 115_200.0
    assert ledger.preview_rejection_reasons(action) == (
        "operation_repeat_limit:electrolyze",
    )


def test_crystallization_process_time_policy_reserves_implicit_stages() -> None:
    config = _task_config("work_ii_crystallization_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 270_336.0
    assert card.implicit_operation_time_s == {
        "filter_crystals": 480.0,
        "quench": 120.0,
    }
    assert card.operation_repeat_limits["filter_crystals"] == 8
    assert card.operation_repeat_limits["quench"] == 8


def test_distillation_process_time_policy_includes_evaporation_and_quench() -> None:
    config = _task_config("work_ii_distillation_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 398_400.0
    assert card.implicit_operation_time_s == {"quench": 120.0}
    assert card.operation_repeat_limits["evaporate"] == 8
    assert card.operation_repeat_limits["quench"] == 8


def test_partition_process_time_policy_covers_eight_lifecycles_and_two_repeats() -> None:
    config = _task_config("work_ii_partition_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 16_560.0
    assert card.operation_attempt_limit == 96
    assert card.vessel_start_limit == 8
    assert card.final_assay_limit == 8
    assert card.operation_repeat_limits == {"mix": 8, "settle": 8, "separate_phase": 8}
    assert card.stock_limits == {
        "extractant_L": 0.276,
        "phase_liquid_L": 0.2208,
        "solvent_L": 0.2576,
    }


def test_safety_process_time_policy_covers_eight_lifecycles_and_two_repeats() -> None:
    config = _task_config("work_ii_safety_campaign.json")
    card = _campaign_card(config)
    assert card.process_time_limit_s == 67_344.0
    assert card.implicit_operation_time_s == {"quench": 120.0}
    assert card.operation_attempt_limit == 80
    assert card.operation_repeat_limits == {"heat": 8, "quench": 8}


def test_all_five_campaign_cards_freeze_participant_owned_closeout_margin() -> None:
    config_names = (
        "work_ii_campaign_pilot.json",
        "work_ii_crystallization_campaign.json",
        "work_ii_distillation_campaign.json",
        "work_ii_partition_campaign.json",
        "work_ii_safety_campaign.json",
    )
    expected = {
        "planned_batches": 8,
        "final_assay_path_operations_per_batch": 2,
        "discard_path_operations_per_batch": 1,
        "final_assay_path_total_operation_reserve": 16,
        "discard_path_total_operation_reserve": 8,
        "policy": "protected_closeout_reserve_planning_pending_w2_26_enforcement",
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
            "after_experiment_2",
            "after_experiment_4",
            "after_experiment_6",
            "final",
        ]
        assert _checkpoint_contract(config, "aligned_nominal") == _checkpoint_contract(
            config, "misindexed_nominal"
        )


def test_checkpoint_contract_supports_frozen_ten_experiment_pattern() -> None:
    config = _config()
    config["campaign"]["complete_experiments"] = 10
    config["campaign"]["checkpoint_complete_experiments"] = [0, 2, 4, 7, 10]
    config["snapshot_stages"] = [
        "pre_evidence",
        "after_experiment_2",
        "after_experiment_4",
        "after_experiment_7",
        "final",
    ]
    contract = _checkpoint_contract(config, "aligned_nominal")
    assert contract["snapshot_stages"] == config["snapshot_stages"]
    assert contract["checkpoint_complete_experiments"] == [0, 2, 4, 7, 10]
    assert len(contract["evidence_catalog"]) == 10


def test_staged_snapshot_qualification_note_matches_seed2_checkpoint_configs() -> None:
    schedule = [0, 2, 4, 7, 10]
    for config_name in (
        "work_ii_electrochemical_independent_terminal_d1_execution_seed2.json",
        "work_ii_reaction_safety_independent_terminal_d1_execution_seed2.json",
    ):
        assert _task_config(config_name)["campaign"]["checkpoint_complete_experiments"] == (
            schedule
        )
    note = (
        ROOT
        / "workstreams"
        / "flagship_tasks"
        / "experiments"
        / "work-ii-staged-belief-snapshot-seed2-qualification.md"
    ).read_text(encoding="utf-8")
    assert "0/2/4/7/10" in note
    assert "60 physical experiments and 30" in note


def test_deepseek_configs_freeze_bounded_recovery_and_schedule_completion() -> None:
    for config_name in (
        "work_ii_electrochemical_deepseek_v4_flash_campaign.json",
        "work_ii_crystallization_deepseek_v4_flash_campaign.json",
        "work_ii_distillation_deepseek_v4_flash_campaign.json",
    ):
        config = _task_config(config_name)
        provider = config["provider"]
        execution = config["execution"]
        assert provider["max_recovered_mcp_tool_failures"] == 3
        assert provider["max_consecutive_mcp_tool_failures"] == 1
        assert provider["max_provider_error_events"] == 1
        assert provider["progress_interval_s"] == 30.0
        assert config["qualification"]["max_resource_rejections"] == 1
        assert execution["failure_semantics"] == (
            "retain cell failures and continue every scheduled seed triplet"
        )
        assert execution["systemic_failure_semantics"] == (
            "stop only when all three arms fail before the first committed operation"
        )


def test_systemic_preoperation_guard_does_not_stop_on_cell_local_failure() -> None:
    arms = ["opaque", "aligned_nominal", "misindexed_nominal"]
    one_failure = [{"arm": "aligned_nominal"}]
    results = [
        {"arm": "opaque", "analysis": {"committed_operation_count": 20}},
        {"arm": "aligned_nominal", "analysis": {"committed_operation_count": 0}},
        {"arm": "misindexed_nominal", "analysis": {"committed_operation_count": 22}},
    ]
    assert (
        _systemic_preoperation_failure(
            cell_failures=one_failure,
            results=results,
            arms=arms,
        )
        is False
    )

    all_failures = [{"arm": arm} for arm in arms]
    zero_operation_results = [
        {"arm": arm, "analysis": {"committed_operation_count": 0}} for arm in arms
    ]
    assert (
        _systemic_preoperation_failure(
            cell_failures=all_failures,
            results=zero_operation_results,
            arms=arms,
        )
        is True
    )

    zero_operation_results[0]["analysis"]["committed_operation_count"] = 1
    assert (
        _systemic_preoperation_failure(
            cell_failures=all_failures,
            results=zero_operation_results,
            arms=arms,
        )
        is False
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


def test_qualification_accepts_ten_experiments_and_five_checkpoints() -> None:
    stages = [
        "pre_evidence",
        "after_experiment_2",
        "after_experiment_4",
        "after_experiment_7",
        "final",
    ]
    recommendation = {
        "selected_experiment_index": 8,
        "selection_rationale": "best public campaign evidence",
    }
    recommendation_sha256 = canonical_json_sha256(recommendation)
    analysis = {
        "complete_experiment_count": 10,
        "experiments": [{"experiment_index": index} for index in range(1, 11)],
        "right_censored_open_experiment": False,
        "belief_snapshots": [{"stage": stage} for stage in stages],
        "resource_rejection_count": 0,
        "final_campaign_resources": {
            "campaign_terminal": True,
            "state": {
                "closed_batches": 10,
                "final_assays": 10,
                "operation_committed_counts": {},
                "report_only": {"process_time_s": 100_000.0},
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
            "complete_experiment_limit": 10,
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
        process_time_limit_s=145_200.0,
        required_operation_counts={},
        required_snapshot_stages=stages,
    )
    assert result["passed"] is True


def test_new_host_commit_receipt_does_not_require_trailing_final_text() -> None:
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
    receipt = {
        "schema_version": "chemworld-interactive-codex-session-receipt-0.2",
        "session_scope": "campaign",
        "status": "completed",
        "return_code": 0,
        "final_payload_valid": False,
        "final_payload_status": None,
        "final_recommendation": recommendation,
        "final_recommendation_sha256": recommendation_sha256,
        "final_recommendation_source": "host_mcp_commit",
        "mcp_tool_calls": [{"tool": "commit_final_recommendation", "status": "completed"}],
        "experiment_tool_integrity_verified_after_session": True,
        "lab_tool_integrity_verified_after_session": True,
        "mcp_tool_integrity_verified_after_session": True,
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
        receipts=[receipt],
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

    recovered_tool_failures = deepcopy(receipts)
    recovered_tool_failures[0]["recovered_mcp_tool_failure_count"] = 2
    recovered_tool_failures[0]["maximum_consecutive_mcp_tool_failure_count"] = 1
    recovered_tool_failures[0]["provider_error_event_count"] = 0
    recovered_tool_failures[0]["session_elapsed_s"] = 100.0
    failed_operational = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=recovered_tool_failures,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        operational_limits={
            "session_wall_time_limit_s": 1_800.0,
            "max_recovered_mcp_tool_failures": 1,
            "max_consecutive_mcp_tool_failures": 1,
            "max_provider_error_events": 0,
        },
    )
    assert failed_operational["passed"] is False
    assert failed_operational["failed_checks"] == ["provider_operational_limits_reconciled"]

    typed_operational = deepcopy(recovered_tool_failures)
    typed_operational[0]["recovered_mcp_tool_failure_count"] = 5
    typed_operational[0]["current_consecutive_mcp_tool_failure_count"] = 4
    typed_operational[0]["maximum_consecutive_mcp_tool_failure_count"] = 4
    typed_operational[0]["mcp_tool_failure_taxonomy"] = {
        "schema_version": "chemworld-mcp-tool-failure-taxonomy-0.1",
        "recovered_mcp_tool_failure_count": 5,
        "current_consecutive_mcp_tool_failure_count": 4,
        "maximum_consecutive_mcp_tool_failure_count": 4,
        "counts_by_category": {
            "provider_network": 0,
            "transport_ipc_os": 1,
            "agent_invalid": 1,
            "unclassified": 0,
        },
        "current_consecutive_counts_by_category": {
            "provider_network": 0,
            "transport_ipc_os": 1,
            "agent_invalid": 1,
            "unclassified": 0,
        },
        "maximum_consecutive_counts_by_category": {
            "provider_network": 0,
            "transport_ipc_os": 1,
            "agent_invalid": 1,
            "unclassified": 0,
        },
    }
    # Three unknown legacy failures are intentionally retained but cannot be
    # claimed as a valid typed taxonomy; make the map reconcile to the total.
    typed_operational[0]["mcp_tool_failure_taxonomy"]["counts_by_category"][
        "transport_ipc_os"
    ] = 4
    typed_operational[0]["mcp_tool_failure_taxonomy"][
        "maximum_consecutive_counts_by_category"
    ]["transport_ipc_os"] = 4
    typed_operational[0]["scientific_compliance_mcp_tool_failure_count"] = 1
    typed_operational[0][
        "current_consecutive_scientific_compliance_mcp_tool_failure_count"
    ] = 1
    typed_operational[0][
        "maximum_consecutive_scientific_compliance_mcp_tool_failure_count"
    ] = 1
    typed_qualification = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=typed_operational,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        operational_limits={
            "session_wall_time_limit_s": 1_800.0,
            "max_recovered_mcp_tool_failures": 4,
            "max_consecutive_mcp_tool_failures": 4,
            "max_provider_error_events": 0,
        },
    )
    assert typed_operational[0]["recovered_mcp_tool_failure_count"] == 5
    assert typed_operational[0]["maximum_consecutive_mcp_tool_failure_count"] == 4
    assert typed_qualification["passed"] is True

    provider_error_receipt = deepcopy(typed_operational)
    provider_error_receipt[0]["provider_error_event_count"] = 2
    provider_error_receipt[0]["provider_errors"] = [
        {"byte_count": 84, "sha256": "a" * 64}
    ]
    provider_error_qualification = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=provider_error_receipt,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        operational_limits={
            "session_wall_time_limit_s": 1_800.0,
            "max_recovered_mcp_tool_failures": 4,
            "max_consecutive_mcp_tool_failures": 4,
            "max_provider_error_events": 99,
        },
        provider_error_enforcement="measure_only",
    )
    assert provider_error_qualification["passed"] is False
    assert provider_error_qualification["failed_checks"] == [
        "provider_operational_limits_reconciled"
    ]
    assert provider_error_qualification["provider_error_operational_policy"] == {
        "enforcement": "measure_only",
        "online_interruption_disabled": True,
        "post_session_zero_tolerance": True,
        "observed_event_count": 2,
        "passed": False,
    }
    assert provider_error_receipt[0]["provider_errors"] == [
        {"byte_count": 84, "sha256": "a" * 64}
    ]

    missing_operational_receipt = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        operational_limits={
            "session_wall_time_limit_s": 1_800.0,
            "max_recovered_mcp_tool_failures": 1,
            "max_consecutive_mcp_tool_failures": 1,
            "max_provider_error_events": 0,
        },
    )
    assert missing_operational_receipt["passed"] is False
    assert missing_operational_receipt["failed_checks"] == [
        "provider_operational_limits_reconciled"
    ]

    missing_measure_only_receipt = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=method_resources,
        method_resource_limits=method_resource_limits,
        receipts=receipts,
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        operational_limits={
            "session_wall_time_limit_s": 1_800.0,
            "max_recovered_mcp_tool_failures": 1,
            "max_consecutive_mcp_tool_failures": 1,
            "max_provider_error_events": 99,
        },
        provider_error_enforcement="measure_only",
    )
    assert missing_measure_only_receipt["passed"] is False
    assert missing_measure_only_receipt["failed_checks"] == [
        "provider_operational_limits_reconciled"
    ]
    assert missing_measure_only_receipt["provider_error_operational_policy"] == {
        "enforcement": "measure_only",
        "online_interruption_disabled": True,
        "post_session_zero_tolerance": True,
        "observed_event_count": None,
        "passed": False,
    }


def test_repeated_heartbeats_preserve_current_cell_coordinate() -> None:
    first = _heartbeat(
        started=0.0,
        completed_cells=0,
        terminal_cells=0,
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
        terminal_cells=0,
        total_cells=15,
        last_event=first,
    )
    assert second["current_world_seed"] == 0
    assert second["current_arm"] == "opaque"
    assert second["current_stage"] == "cell_started"
    assert second["current_step"] is None
    assert second["current_complete_experiments"] == 0
    assert second["liveness_counter"] == first["liveness_counter"] + 1


def test_qualification_retains_one_resource_rejection_under_amended_policy() -> None:
    config = _config()
    recommendation = {
        "selected_experiment_index": 1,
        "selection_rationale": "retained public outcome",
    }
    digest = canonical_json_sha256(recommendation)
    analysis = {
        "complete_experiment_count": 4,
        "experiments": [{"experiment_index": index} for index in range(1, 5)],
        "right_censored_open_experiment": False,
        "belief_snapshots": [{"stage": stage} for stage in config["snapshot_stages"]],
        "resource_rejection_count": 1,
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
        "final_recommendation_sha256": digest,
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
                "final_recommendation_sha256": digest,
                "experiment_tool_integrity_verified_after_session": True,
                "lab_tool_integrity_verified_after_session": True,
                "mcp_tool_integrity_verified_after_session": True,
            }
        ],
        process_time_limit_s=72_000.0,
        required_operation_counts={},
        required_snapshot_stages=config["snapshot_stages"],
        max_resource_rejections=1,
    )
    assert result["passed"] is True
    assert result["resource_rejection_policy"] == {
        "observed": 1,
        "maximum": 1,
        "semantics": "retained_participant_behavior_no_host_repair",
        "passed": True,
    }


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


def test_qualification_execution_requires_precall_user_authorization(
    tmp_path: Path,
) -> None:
    output = tmp_path / "qualification-output"
    args = argparse.Namespace(
        config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
        output=output,
        progress_file=tmp_path / "progress.jsonl",
        world_seed=0,
        qualification_execution=True,
        qualification_authorization=None,
        formal_manifest=None,
        formal_cell_key=None,
        allow_formal_execution=False,
        prior_arm=None,
    )
    with pytest.raises(
        RuntimeError,
        match="qualification execution requires --qualification-authorization",
    ):
        campaign_runner.run(args)
    assert not output.exists()


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
parser.add_argument("--release-manifest")
args = parser.parse_args()
args.output.mkdir(parents=True)
started = {"stage": "cell_started", "world_seed": args.world_seed, "arm": args.prior_arm}
print(json.dumps(started), flush=True)
time.sleep(0.05)
row = {
    "arm": args.prior_arm,
    "completed": True,
    "analysis": {"committed_operation_count": 1},
    "qualification": {"passed": True, "failed_checks": []},
}
(args.output / "trajectory.jsonl").write_text(
    json.dumps({"transaction_status": "committed"}) + "\\n", encoding="utf-8"
)
(args.output / "summary.json").write_text(json.dumps(row), encoding="utf-8")
(args.output / "report.json").write_text(json.dumps({"results": [row]}), encoding="utf-8")
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
    monkeypatch.setattr(five_seed_runner, "git_source_commit", lambda _root: "test-commit")
    monkeypatch.setattr(
        five_seed_runner,
        "validate_development_readiness_receipt",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        five_seed_runner,
        "validate_release_d1_config",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        five_seed_runner,
        "validate_d1_qualification_evidence",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setenv("WELLAU_API_KEY", "test-key")
    output = tmp_path / "output"
    progress = tmp_path / "progress.jsonl"
    config_path = tmp_path / "release-d1.json"
    release_config = json.loads(
        (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    release_config["execution_context"] = {"execution_mode": "release"}
    release_config["legacy_source_evidence"] = False
    config_path.write_text(json.dumps(release_config), encoding="utf-8")
    report = five_seed_runner.run(
        argparse.Namespace(
            config=config_path,
            output=output,
            progress_file=progress,
            world_seed=[0, 1, 2, 3, 4],
            heartbeat_interval_s=0.05,
            max_concurrency=3,
            readiness_receipt=tmp_path / "readiness.json",
            release_manifest=tmp_path / "release.json",
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


def test_five_seed_runner_requires_readiness_before_creating_output(
    monkeypatch,
    tmp_path: Path,
) -> None:
    output = tmp_path / "must-not-exist"
    args = argparse.Namespace(
        config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
        output=output,
        progress_file=tmp_path / "progress.jsonl",
        world_seed=[0],
        heartbeat_interval_s=0.05,
        max_concurrency=3,
        readiness_receipt=None,
    )
    with pytest.raises(RuntimeError, match="zero-provider readiness receipt"):
        five_seed_runner.run(args)
    assert not output.exists()


def test_provider_runner_requires_release_manifest_before_creating_output(
    monkeypatch,
    tmp_path: Path,
) -> None:
    output = tmp_path / "must-not-exist"
    args = argparse.Namespace(
        config=ROOT / "configs/benchmark/work_ii_campaign_pilot.json",
        output=output,
        progress_file=tmp_path / "progress.jsonl",
        world_seed=[0],
        heartbeat_interval_s=0.05,
        max_concurrency=3,
        readiness_receipt=tmp_path / "readiness.json",
        release_manifest=None,
    )
    with pytest.raises(RuntimeError, match="release manifest"):
        five_seed_runner.run(args)
    assert not output.exists()


def test_direct_d1_runner_rejects_development_context_before_output(
    tmp_path: Path,
) -> None:
    source = json.loads(
        (
            ROOT / "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json"
        ).read_text(encoding="utf-8")
    )
    source["execution_context"] = {
        "execution_mode": "development",
        "evidence_status": "development_only",
        "release_eligible": False,
        "c2_admission_authorized": False,
        "tested_commit": None,
        "freeze_id": None,
        "release_manifest_sha256": None,
        "execution_surface_sha256": None,
    }
    source["legacy_source_evidence"] = False
    source["qualification"]["q2_passed"] = True
    config = tmp_path / "development-d1.json"
    config.write_text(json.dumps(source), encoding="utf-8")
    output = tmp_path / "must-not-exist"
    with pytest.raises(RuntimeError, match="requires a release manifest"):
        campaign_runner.run(
            argparse.Namespace(
                config=config,
                output=output,
                progress_file=tmp_path / "progress.jsonl",
                world_seed=0,
                prior_arm="opaque",
                formal_manifest=None,
                formal_cell_key=None,
                allow_formal_execution=False,
                qualification_execution=False,
                resource_calibration_execution=False,
                release_manifest=None,
            )
        )
    assert not output.exists()


def test_progress_files_survive_closed_stdout(monkeypatch, tmp_path: Path) -> None:
    class ClosedStdout:
        encoding = "utf-8"

        def write(self, _value: str) -> int:
            raise OSError(22, "closed")

        def flush(self) -> None:
            raise OSError(22, "closed")

    monkeypatch.setattr(five_seed_runner.sys, "stdout", ClosedStdout())
    parent_progress = tmp_path / "parent.jsonl"
    five_seed_runner._emit(parent_progress, {"stage": "alive"})
    assert json.loads(parent_progress.read_text(encoding="utf-8"))["stage"] == "alive"

    child_progress = tmp_path / "child.jsonl"
    campaign_runner._progress(child_progress, {"stage": "operation", "step": 1})
    assert json.loads(child_progress.read_text(encoding="utf-8"))["step"] == 1


def test_cell_cleanup_failure_cannot_preempt_durable_summary(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    cell_root = tmp_path / "cell"
    temporary_root = tmp_path / "temporary"
    cleanup_calls = 0

    class FailingTemporaryDirectory:
        name = str(temporary_root)

        def __init__(self, *, prefix: str) -> None:
            del prefix
            temporary_root.mkdir()

        def cleanup(self) -> None:
            nonlocal cleanup_calls
            cleanup_calls += 1
            assert (cell_root / "summary.json").exists()
            raise OSError(145, "directory not empty")

    class FakeAgent:
        def __init__(self, **kwargs: Any) -> None:
            del kwargs

        def provider_receipts(self) -> list[dict[str, Any]]:
            return [{"status": "completed"}]

        def method_resource_usage(self) -> dict[str, Any]:
            return {}

    config = _config()
    monkeypatch.setattr(campaign_runner.tempfile, "TemporaryDirectory", FailingTemporaryDirectory)
    monkeypatch.setattr(campaign_runner, "InteractiveCodexExperimentAgent", FakeAgent)
    monkeypatch.setattr(campaign_runner, "run_agent", lambda **kwargs: [])
    monkeypatch.setattr(
        campaign_runner,
        "_analyze",
        lambda records, receipts, final_metric_ids: {
            "complete_experiment_count": 0,
            "right_censored_open_experiment": False,
        },
    )
    monkeypatch.setattr(campaign_runner, "build_work_ii_execution_artifacts", lambda *a, **k: {})
    monkeypatch.setattr(
        campaign_runner,
        "_qualification",
        lambda **kwargs: {"passed": False, "failed_checks": ["complete_experiment_count"]},
    )
    monkeypatch.setattr(campaign_runner, "TEMP_DIRECTORY_CLEANUP_RETRY_LIMIT", 2)
    monkeypatch.setattr(campaign_runner.time, "sleep", lambda seconds: None)

    row = campaign_runner._run_cell(
        config=config,
        world_seed=0,
        arm="opaque",
        cell_index=1,
        total_cells=1,
        cell_root=cell_root,
        progress_path=tmp_path / "progress.jsonl",
    )

    assert cleanup_calls == 2
    assert row["temporary_workspace_cleanup"]["status"] == "deferred"
    assert json.loads((cell_root / "summary.json").read_text(encoding="utf-8")) == row


def test_parent_failure_terminates_and_reaps_active_children() -> None:
    class FakeProcess:
        def __init__(self) -> None:
            self.running = True
            self.terminated = False
            self.killed = False
            self.waited = False

        def poll(self) -> int | None:
            return None if self.running else 0

        def terminate(self) -> None:
            self.terminated = True
            self.running = False

        def kill(self) -> None:
            self.killed = True
            self.running = False

        def wait(self, timeout: float | None = None) -> int:
            del timeout
            self.waited = True
            return 0

    first = FakeProcess()
    second = FakeProcess()
    five_seed_runner._terminate_processes({"opaque": first, "aligned": second})
    assert first.terminated and first.waited and not first.killed
    assert second.terminated and second.waited and not second.killed
