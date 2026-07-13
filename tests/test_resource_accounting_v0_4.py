from __future__ import annotations

import copy
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from chemworld.agents.event import ScriptedChemistryAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.interaction_strata import RESOURCE_AXES
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
)
from chemworld.eval.resource_accounting_v0_4 import (
    CLASSIC_COMPUTE_EVENT_VERSION,
    PROVIDER_RECEIPT_VERSION,
    RL_TRAINING_RESOURCE_VERSION,
    ResourceAccountingError,
    aggregate_resource_accounting,
    audit_cell_resource_accounting,
    audit_rl_training_resource,
    bind_pricing_snapshot,
)
from chemworld.eval.runner import run_agent

CELL_A = "a" * 64
CELL_B = "b" * 64
CHECKPOINT = "c" * 64
SOURCE = "d" * 64


def _pricing() -> dict[str, Any]:
    return bind_pricing_snapshot(
        {
            "provider": "DeepSeek",
            "model_id": "deepseek-v4-pro",
            "access_date": "2026-07-13",
            "currency": "USD",
            "input_cache_hit_per_million_usd": 0.003625,
            "input_cache_miss_per_million_usd": 0.435,
            "output_per_million_usd": 0.87,
        }
    )


def _receipt(
    *,
    pricing: dict[str, Any],
    request_id: str,
    decision: int,
    attempt: int,
    status: str,
    input_tokens: int,
    cache_hit_tokens: int,
    output_tokens: int,
) -> dict[str, Any]:
    cache_miss_tokens = input_tokens - cache_hit_tokens
    cost = (
        Decimal(cache_hit_tokens) * Decimal("0.003625")
        + Decimal(cache_miss_tokens) * Decimal("0.435")
        + Decimal(output_tokens) * Decimal("0.87")
    ) / Decimal(1_000_000)
    return {
        "schema_version": PROVIDER_RECEIPT_VERSION,
        "request_id": request_id,
        "logical_decision_index": decision,
        "attempt_index": attempt,
        "status": status,
        "provider": "DeepSeek",
        "model_id": "deepseek-v4-pro",
        "pricing_version_sha256": pricing["pricing_version_sha256"],
        "usage_source": "provider_response",
        "usage_complete": True,
        "billable": True,
        "input_token_count": input_tokens,
        "output_token_count": output_tokens,
        "input_cache_hit_token_count": cache_hit_tokens,
        "input_cache_miss_token_count": cache_miss_tokens,
        "billed_cost_usd": float(cost),
    }


def _llm_receipts(pricing: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _receipt(
            pricing=pricing,
            request_id="request-1",
            decision=1,
            attempt=1,
            status="failed",
            input_tokens=100,
            cache_hit_tokens=40,
            output_tokens=0,
        ),
        _receipt(
            pricing=pricing,
            request_id="request-2",
            decision=1,
            attempt=2,
            status="succeeded",
            input_tokens=200,
            cache_hit_tokens=100,
            output_tokens=50,
        ),
        _receipt(
            pricing=pricing,
            request_id="request-3",
            decision=2,
            attempt=1,
            status="succeeded",
            input_tokens=80,
            cache_hit_tokens=0,
            output_tokens=20,
        ),
    ]


def _usage(
    *,
    model_calls: int = 0,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cost: float = 0.0,
    cpu_time_s: float = 0.2,
    gpu_time_s: float = 0.0,
    training_steps: int = 0,
    live: bool = False,
) -> dict[str, Any]:
    return {
        "schema_version": METHOD_RESOURCE_USAGE_VERSION,
        "accounting_complete": True,
        "usage_source": "provider_usage_and_frozen_price_snapshot" if live else "runtime",
        "model_call_count": model_calls,
        "input_token_count": input_tokens,
        "output_token_count": output_tokens,
        "monetary_cost_usd": cost,
        "training_environment_step_count": training_steps,
        "cpu_time_s": cpu_time_s,
        "gpu_time_s": gpu_time_s,
        "model_provenance": (
            {
                "provider": "DeepSeek",
                "model_id": "deepseek-v4-pro",
                "model_snapshot_or_access_date": "2026-07-13",
                "prompt_hash": "e" * 64,
                "request_parameters": {"temperature": 0.0},
                "tokenizer_or_provider_usage_source": "provider_response",
            }
            if live
            else {}
        ),
    }


def _records(
    *,
    usage: dict[str, Any] | None = None,
    operation_count: int = 2,
    wall_time_s: float = 2.0,
) -> list[dict[str, Any]]:
    records = [
        {
            "step": index,
            "action": (
                {"operation": "measure", "instrument": "uvvis"}
                if index == operation_count
                else {"operation": "wait", "duration_s": 1.0}
            ),
        }
        for index in range(1, operation_count + 1)
    ]
    records[-1]["method_resources"] = {
        "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
        "operation_count": operation_count,
        "complete_experiment_count": 1,
        "decision_wall_time_s": 0.5,
        "update_wall_time_s": 0.5,
        "run_wall_time_s": wall_time_s,
        "reached_checkpoints": [1],
        "limits": {
            "operation_limit": operation_count,
            "complete_experiment_limit": 1,
            "checkpoint_complete_experiments": [1],
        },
        "agent_usage": usage or _usage(),
        "accounting_complete": True,
    }
    return records


def _llm_report(
    *,
    cell_identity: str = CELL_A,
    receipts: list[dict[str, Any]] | None = None,
    pricing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pricing = _pricing() if pricing is None else pricing
    receipts = _llm_receipts(pricing) if receipts is None else receipts
    total_cost = sum(Decimal(str(item["billed_cost_usd"])) for item in receipts)
    records = _records(
        usage=_usage(
            model_calls=3,
            input_tokens=380,
            output_tokens=70,
            cost=float(total_cost),
            live=True,
        )
    )
    return audit_cell_resource_accounting(
        records,
        cell_identity_sha256=cell_identity,
        method_id="live_llm_a",
        method_kind="live_llm",
        resource_profile="live_llm_evaluation",
        provider_receipts=receipts,
        pricing_snapshot=pricing,
    )


def test_deepseek_attempt_receipts_reconcile_retries_cache_tokens_and_exact_bill() -> None:
    report = _llm_report()
    assert report["accounting_complete"] is True
    assert set(report["axes"]) == set(RESOURCE_AXES)
    assert report["axes"]["provider_request_count"] == 3
    assert report["axes"]["provider_retry_count"] == 1
    assert report["axes"]["input_token_count"] == 380
    assert report["axes"]["output_token_count"] == 70
    assert report["provider_accounting"]["failed_request_count"] == 1
    assert report["provider_accounting"]["prompt_cache_hit_token_count"] == 140
    assert report["provider_accounting"]["duplicate_request_charged"] is False
    assert report["axes"]["monetary_cost_usd"] == pytest.approx(0.0001658075)


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (lambda receipts: receipts[0].update({"usage_complete": False}), "provider_usage_missing"),
        (
            lambda receipts: receipts[0].update({"pricing_version_sha256": "f" * 64}),
            "provider_receipt_pricing_version_mismatch",
        ),
        (lambda receipts: receipts[0].update({"billable": False}), "provider_request_unbillable"),
    ],
)
def test_unknown_or_version_mismatched_deepseek_cost_fails_without_zero_estimate(
    mutation, reason: str
) -> None:
    pricing = _pricing()
    receipts = _llm_receipts(pricing)
    mutation(receipts)
    report = _llm_report(receipts=receipts, pricing=pricing)
    assert report["accounting_complete"] is False
    assert reason in report["failure_reasons"]
    assert report["axes"]["monetary_cost_usd"] is None
    assert report["retained_in_statistical_denominator"] is True


def test_duplicate_request_id_and_incoherent_cache_breakdown_fail_closed() -> None:
    pricing = _pricing()
    receipts = _llm_receipts(pricing)
    receipts[1]["request_id"] = receipts[0]["request_id"]
    receipts[2]["input_cache_miss_token_count"] = 79
    report = _llm_report(receipts=receipts, pricing=pricing)
    assert report["accounting_complete"] is False
    assert "provider_request_id_duplicate_or_missing" in report["failure_reasons"]
    assert "provider_cache_token_breakdown_incoherent" in report["failure_reasons"]
    assert report["axes"]["monetary_cost_usd"] is None


def test_classic_fit_and_acquisition_components_are_counted_without_time_double_charge() -> None:
    records = _records(usage=_usage(cpu_time_s=2.0), wall_time_s=3.0)
    events = [
        {
            "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
            "event_id": "fit-1",
            "cell_identity_sha256": CELL_A,
            "event_kind": "fit",
            "cpu_time_s": 0.4,
            "wall_time_s": 0.5,
        },
        {
            "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
            "event_id": "acquisition-1",
            "cell_identity_sha256": CELL_A,
            "event_kind": "acquisition_optimization",
            "cpu_time_s": 0.3,
            "wall_time_s": 0.4,
        },
    ]
    report = audit_cell_resource_accounting(
        records,
        cell_identity_sha256=CELL_A,
        method_id="structured_gp_ei",
        method_kind="classic",
        resource_profile="classic_recipe",
        classic_compute_events=events,
        classic_compute_required=True,
    )
    assert report["accounting_complete"] is True
    assert report["axes"]["fit_count"] == 1
    assert report["axes"]["acquisition_optimization_count"] == 1
    assert report["axes"]["cpu_time_s"] == 2.0
    assert report["classic_compute_accounting"][
        "component_times_already_in_evaluation_totals"
    ] is True


def test_rl_training_is_separate_deduplicated_and_parallel_wall_is_not_summed() -> None:
    first = audit_cell_resource_accounting(
        _records(usage=_usage(cpu_time_s=0.2, gpu_time_s=0.1), wall_time_s=2.0),
        cell_identity_sha256=CELL_A,
        method_id="ppo",
        method_kind="rl",
        resource_profile="rl_evaluation",
        rl_checkpoint_sha256=CHECKPOINT,
    )
    second = audit_cell_resource_accounting(
        _records(usage=_usage(cpu_time_s=0.3, gpu_time_s=0.2), wall_time_s=2.5),
        cell_identity_sha256=CELL_B,
        method_id="ppo",
        method_kind="rl",
        resource_profile="rl_evaluation",
        rl_checkpoint_sha256=CHECKPOINT,
    )
    training = audit_rl_training_resource(
        {
            "schema_version": RL_TRAINING_RESOURCE_VERSION,
            "accounting_complete": True,
            "training_run_id": "ppo-train-1",
            "checkpoint_sha256": CHECKPOINT,
            "source_manifest_sha256": SOURCE,
            "requested_training_environment_step_count": 100,
            "training_environment_step_count": 100,
            "cpu_time_s": 20.0,
            "gpu_time_s": 10.0,
            "wall_time_s": 12.0,
        }
    )
    aggregate = aggregate_resource_accounting(
        [first, second],
        matrix_elapsed_wall_time_s=2.8,
        rl_training_reports=[training],
    )
    assert aggregate["accounting_complete"] is True
    assert aggregate["evaluation_resource_totals"]["training_environment_step_count"] == 0
    assert aggregate["evaluation_resource_totals"]["wall_time_s"] == 2.8
    assert aggregate["summed_cell_wall_time_s_diagnostic_only"] == 4.5
    assert aggregate["rl_training_resource_totals_separate"][
        "training_environment_step_count"
    ] == 100
    assert aggregate["unique_rl_checkpoint_count"] == 1
    assert aggregate["rl_training_charged_per_evaluation_cell"] is False


def test_rl_training_steps_inside_evaluation_cell_fail_closed() -> None:
    report = audit_cell_resource_accounting(
        _records(usage=_usage(training_steps=100)),
        cell_identity_sha256=CELL_A,
        method_id="ppo",
        method_kind="rl",
        resource_profile="rl_evaluation",
        rl_checkpoint_sha256=CHECKPOINT,
    )
    assert report["accounting_complete"] is False
    assert "training_resources_mixed_into_evaluation_cell" in report["failure_reasons"]


def test_duplicate_cached_cell_report_cannot_be_charged_twice() -> None:
    report = _llm_report()
    with pytest.raises(ResourceAccountingError, match="unique identities"):
        aggregate_resource_accounting(
            [report, copy.deepcopy(report)],
            matrix_elapsed_wall_time_s=2.0,
        )


def test_unreferenced_rl_training_artifact_is_not_silently_added() -> None:
    classic = audit_cell_resource_accounting(
        _records(),
        cell_identity_sha256=CELL_A,
        method_id="operation_random",
        method_kind="classic",
        resource_profile="operation_baseline",
    )
    training = audit_rl_training_resource(
        {
            "schema_version": RL_TRAINING_RESOURCE_VERSION,
            "accounting_complete": True,
            "training_run_id": "unused-train",
            "checkpoint_sha256": CHECKPOINT,
            "source_manifest_sha256": SOURCE,
            "requested_training_environment_step_count": 100,
            "training_environment_step_count": 100,
            "cpu_time_s": 20.0,
            "gpu_time_s": 10.0,
            "wall_time_s": 12.0,
        }
    )
    aggregate = aggregate_resource_accounting(
        [classic],
        matrix_elapsed_wall_time_s=2.0,
        rl_training_reports=[training],
    )
    assert aggregate["accounting_complete"] is False
    assert aggregate["rl_training_resource_totals_separate"][
        "training_environment_step_count"
    ] == 0
    assert f"checkpoint:{CHECKPOINT}:training_report_unreferenced" in aggregate[
        "failure_reasons"
    ]


def test_actual_runner_smoke_trajectory_reconciles_all_required_axes(tmp_path: Path) -> None:
    trajectory = tmp_path / "smoke.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=ScriptedChemistryAgent(),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=3,
        task_id="reaction-to-assay",
        output_path=trajectory,
        method_resource_limits={
            "complete_experiment_limit": 1,
            "checkpoint_complete_experiments": [1],
            "wall_time_limit_s": 30.0,
        },
    )
    records = load_jsonl(trajectory)
    report = audit_cell_resource_accounting(
        records,
        cell_identity_sha256=CELL_A,
        method_id="scripted-smoke",
        method_kind="classic",
        resource_profile="operation_baseline",
    )
    assert report["accounting_complete"] is True, report["failure_reasons"]
    assert set(report["axes"]) == set(RESOURCE_AXES)
    assert all(value is not None for value in report["axes"].values())
    assert report["axes"]["operation_count"] == len(records)
    assert report["axes"]["decision_count"] == len(records)
    assert report["axes"]["complete_experiment_count"] == 1
