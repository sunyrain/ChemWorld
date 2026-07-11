from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.agents.event import ScriptedChemistryAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_USAGE_VERSION,
    MethodResourceLedger,
    MethodResourceLimitError,
    MethodResourceLimits,
    evaluation_resource_limits,
    load_method_protocol,
)
from chemworld.eval.runner import run_agent

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "method-protocol-vnext.json"


def _usage(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": METHOD_RESOURCE_USAGE_VERSION,
        "accounting_complete": True,
        "usage_source": "test",
        "model_call_count": 0,
        "input_token_count": 0,
        "output_token_count": 0,
        "monetary_cost_usd": 0.0,
        "training_environment_step_count": 0,
        "cpu_time_s": 0.0,
        "gpu_time_s": 0.0,
        "model_provenance": {},
    }
    payload.update(overrides)
    return payload


def test_method_protocol_freezes_nonclaiming_fairness_controls() -> None:
    protocol = load_method_protocol()
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["pre_freeze_result_policy"] == "diagnostic_only"
    assert protocol["paired_seed_count"] == 20
    assert protocol["confirmatory_seed_ids"] == list(range(20, 40))
    assert protocol["checkpoints"] == [4, 8, 12, 20, 40]
    assert protocol["llm_evidence_policy"]["private_chain_of_thought_required"] is False


def test_method_protocol_report_exposes_current_cross_family_gaps() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["formal_method_matrix_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["missing_required_methods"] == [
        "ppo",
        "sac",
        "live_llm_a",
        "live_llm_b",
    ]
    assert "structured_gp_pi" not in report["required_but_ineligible_methods"]
    assert report["methods"]["structured_gp_pi"]["implementation_contract_ready"] is True
    assert report["methods"]["structured_gp_ucb"]["implementation_contract_ready"] is True
    assert report["methods"]["structured_rf_ei"]["implementation_contract_ready"] is True
    assert report["methods"]["structured_gp_ei"]["implementation_contract_ready"] is True
    assert report["methods"]["llm_replay"]["formal_role"] == "excluded"
    assert len(report["interaction_failures"]) == 7
    assert set(report["evidence"]) == {
        "legacy_agent_interaction_audit",
        "five_seed_campaign_budget_curve",
        "risk_cost_calibration",
        "task_validity_cards",
    }
    assert all(item["sha256"] for item in report["evidence"].values())


def test_protocol_translates_to_family_aware_hard_limits() -> None:
    protocol = load_method_protocol()
    classic = evaluation_resource_limits(
        protocol,
        operation_limit=400,
        requires_online_model=False,
    )
    llm = evaluation_resource_limits(
        protocol,
        operation_limit=400,
        requires_online_model=True,
    )
    assert classic.complete_experiment_limit == 40
    assert classic.checkpoint_complete_experiments == (4, 8, 12, 20, 40)
    assert classic.model_call_limit is None
    assert llm.model_call_limit == 2400
    assert llm.input_token_limit == 1_000_000


def test_resource_ledger_tracks_checkpoints_and_fails_closed() -> None:
    ledger = MethodResourceLedger(
        MethodResourceLimits(
            operation_limit=1,
            complete_experiment_limit=1,
            checkpoint_complete_experiments=(1,),
        )
    )
    ledger.record_decision(elapsed_s=0.01, agent_usage=_usage())
    ledger.record_outcome(experiment_ended=True, update_elapsed_s=0.02)
    snapshot = ledger.snapshot()
    assert snapshot["operation_count"] == 1
    assert snapshot["complete_experiment_count"] == 1
    assert snapshot["reached_checkpoints"] == [1]
    assert snapshot["accounting_complete"] is True
    with pytest.raises(MethodResourceLimitError, match="operation_count"):
        ledger.record_decision(elapsed_s=0.01, agent_usage=_usage())


def test_online_model_usage_requires_complete_provenance() -> None:
    with pytest.raises(ValueError, match="explicit provider request limit"):
        MethodResourceLedger(
            MethodResourceLimits(operation_limit=2),
            requires_online_model=True,
        )

    ledger = MethodResourceLedger(
        MethodResourceLimits(operation_limit=2, model_call_limit=12),
        requires_online_model=True,
    )
    with pytest.raises(ValueError, match="provenance"):
        ledger.record_decision(
            elapsed_s=0.01,
            agent_usage=_usage(model_call_count=1),
        )

    valid = MethodResourceLedger(
        MethodResourceLimits(operation_limit=2, model_call_limit=12),
        requires_online_model=True,
    )
    valid.record_decision(
        elapsed_s=0.01,
        agent_usage=_usage(
            model_call_count=1,
            input_token_count=200,
            output_token_count=50,
            monetary_cost_usd=0.01,
            model_provenance={
                "provider": "test-provider",
                "model_id": "test-model",
                "model_snapshot_or_access_date": "2026-07-11",
                "prompt_hash": "abc123",
                "request_parameters": {"temperature": 0.0},
                "tokenizer_or_provider_usage_source": "provider",
            },
        ),
    )
    assert valid.snapshot()["agent_usage"]["model_call_count"] == 1


def test_online_model_ledger_allows_counted_retries_within_explicit_limit() -> None:
    ledger = MethodResourceLedger(
        MethodResourceLimits(operation_limit=2, model_call_limit=6),
        requires_online_model=True,
    )
    provenance = {
        "provider": "test-provider",
        "model_id": "test-model",
        "model_snapshot_or_access_date": "2026-07-11",
        "prompt_hash": "abc123",
        "request_parameters": {"max_attempts": 3},
        "tokenizer_or_provider_usage_source": "provider",
    }
    ledger.record_decision(
        elapsed_s=0.01,
        agent_usage=_usage(model_call_count=3, model_provenance=provenance),
    )
    ledger.record_outcome(experiment_ended=False, update_elapsed_s=0.01)
    ledger.record_decision(
        elapsed_s=0.01,
        agent_usage=_usage(model_call_count=6, model_provenance=provenance),
    )
    assert ledger.snapshot()["agent_usage"]["model_call_count"] == 6
    with pytest.raises(MethodResourceLimitError, match="model_call_count"):
        ledger.record_decision(
            elapsed_s=0.01,
            agent_usage=_usage(model_call_count=7, model_provenance=provenance),
        )


def test_runner_retains_method_resource_ledger(tmp_path: Path) -> None:
    output = tmp_path / "resource-ledger.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=ScriptedChemistryAgent(),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=3,
        task_id="reaction-to-assay",
        output_path=output,
        method_resource_limits={
            "complete_experiment_limit": 1,
            "checkpoint_complete_experiments": [1],
            "wall_time_limit_s": 30.0,
        },
    )
    records = load_jsonl(output)
    assert history[-1].method_resources["operation_count"] == len(history)
    assert records[-1]["method_resources"]["operation_count"] == len(records)
    assert records[-1]["method_resources"]["complete_experiment_count"] == 1
    assert records[-1]["method_resources"]["reached_checkpoints"] == [1]
    assert records[-1]["method_resources"]["agent_usage"]["model_call_count"] == 0
