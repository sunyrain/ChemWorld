from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.agents.base import HistoryRecord
from chemworld.data.logging import observation_to_json
from chemworld.eval import first_paper_u05_complete_agent as evaluator

ROOT = Path(__file__).resolve().parents[1]


def _write_json(path: Path, value: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _minimal_current_repository(tmp_path: Path) -> Path:
    composition = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    u04 = {
        "passed": True,
        "pair_count": 6,
        "trace_count": 24,
        "provider_call_count": 0,
        "protocol_id": "fork-v1",
    }
    u05 = {
        "status": "passed",
        "generated_qualification": {
            "unseen_pattern": evaluator.FROZEN_PATTERN,
            "cases": [
                {
                    "composition_id": evaluator.FROZEN_COMPOSITION_ID,
                    "case_id": evaluator.FROZEN_CASE_ID,
                    "pattern": evaluator.FROZEN_PATTERN,
                    "generation_seed": evaluator.FROZEN_GENERATION_SEED,
                    "generation_index": evaluator.FROZEN_GENERATION_INDEX,
                    "composition_request_sha256": evaluator.FROZEN_REQUEST_SHA256,
                    "composition_request": composition,
                    "action_count": 12,
                    "passed": True,
                    "compile_receipt": {
                        "task_contract_sha256": (
                            evaluator.FROZEN_PUBLIC_TASK_SUBOBJECT_HASH
                        )
                    },
                    "exact_replay": {"verified": True},
                }
            ],
        },
    }
    u04_path = tmp_path / "evidence/u04.json"
    u05_path = tmp_path / "evidence/u05.json"
    u04_sha = _write_json(u04_path, u04)
    u05_sha = _write_json(u05_path, u05)
    current = {
        "evidence_dag": {
            "nodes": {
                evaluator.U04_NODE_ID: {
                    "path": "evidence/u04.json",
                    "sha256": u04_sha,
                    "artifact_state": "current",
                    "freshness": "fresh",
                    "gate_state": "passed",
                },
                evaluator.U05_NODE_ID: {
                    "path": "evidence/u05.json",
                    "sha256": u05_sha,
                    "artifact_state": "current",
                    "freshness": "fresh",
                    "gate_state": "passed",
                },
            }
        }
    }
    _write_json(tmp_path / evaluator.CURRENT_CONFIG, current)
    return tmp_path


def _verified_provider_receipt(*, step_count: int = 2) -> dict[str, Any]:
    usage = {
        "prompt_tokens": 100,
        "completion_tokens": 20,
        "total_tokens": 120,
        "prompt_cache_hit_tokens": 10,
        "prompt_cache_miss_tokens": 90,
        "prompt_cache_write_tokens": 0,
        "reasoning_output_tokens": 5,
    }
    return {
        "schema_version": "chemworld-interactive-codex-session-receipt-0.1",
        "session_id": "session-1",
        "status": "completed",
        "return_code": 0,
        "terminal_reason": "experiment_complete",
        "model_id": evaluator.FROZEN_MODEL,
        "reasoning_effort": evaluator.FROZEN_REASONING_EFFORT,
        "usage": usage,
        "usage_complete": True,
        "provider_errors": [],
        "final_payload_valid": True,
        "final_payload_status": "experiment_complete",
        "mcp_tool_calls": [
            {
                "tool": "step",
                "arguments_sha256": str(index),
                "argument_keys": ["action", "expected_step"],
            }
            for index in range(step_count)
        ],
        "mcp_tool_integrity_verified_after_session": True,
        "experiment_tool_integrity_verified_after_session": True,
        "lab_tool_integrity_verified_after_session": True,
        "private_reasoning_retained": False,
    }


def _method_usage() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-method-resource-usage-0.1",
        "accounting_complete": False,
        "provider_usage_pending": False,
        "provider_usage_accounting_complete": True,
        "provider_call_accounting_complete": True,
        "provider_token_accounting_complete": True,
        "provider_cache_accounting_complete": True,
        "monetary_accounting_complete": False,
        "model_call_count": 1,
        "input_token_count": 100,
        "output_token_count": 20,
        "monetary_cost_usd": 0.0,
        "model_provenance": {
            "provider": "OpenAI",
            "provider_base_url": "https://example.invalid",
            "pricing": {"accounting_complete": False},
        },
    }


def _minimal_output_report() -> dict[str, Any]:
    return {
        "status": "failed",
        "summary": {
            "submitted_action_count": 0,
            "trajectory_record_count": 0,
            "committed_action_count": 0,
            "rollback_count": 0,
            "committed_terminate_count": 0,
            "committed_final_assay_count": 0,
            "public_private_leakage_count": 0,
        },
        "provider_accounting": {
            "session_count": 0,
            "model_call_count": 0,
            "mcp_step_count": 0,
            "usage": {},
        },
        "lifecycle": {"passed": False},
        "exact_replay": {"verified": False, "max_abs_error": None},
        "environment_resource_receipt": {"resource_reconciled": False},
        "existing_evidence": {
            "U04": {"pair_count": 6, "trace_count": 24, "provider_call_count": 0}
        },
        "failures": [{"class": "test_failure"}],
        "claim_boundary": ["test"],
    }


def test_current_resolution_binds_exact_first_unseen_case() -> None:
    evidence = evaluator.resolve_existing_evidence(ROOT)

    assert evidence["U04"]["binding"]["binding_verified"] is True
    assert evidence["U04"]["provider_call_count"] == 0
    assert evidence["U05"]["case_id"] == evaluator.FROZEN_CASE_ID
    assert evidence["U05"]["generation_index"] == 0
    assert evidence["U05"]["composition_request_sha256"] == evaluator.FROZEN_REQUEST_SHA256
    assert (
        evidence["U05"]["public_compiled_task_subobject_hash"]
        == evaluator.FROZEN_PUBLIC_TASK_SUBOBJECT_HASH
    )


def test_retained_formal_result_detects_declared_process_time_overrun() -> None:
    report_path = (
        ROOT
        / "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v1.json"
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    receipt = evaluator._declared_resource_budget_receipt(
        composition_request=report["frozen_experiment"]["composition_request"],
        environment_resource_receipt=report["environment_resource_receipt"],
        actions=report["actions"],
    )

    assert receipt["passed"] is False
    assert receipt["exceeded_resources"] == ["process_time_s"]
    assert receipt["first_exceeded_step"] == {"process_time_s": 9}
    assert receipt["observed_usage"]["process_time_s"] == pytest.approx(
        21658.4542224647
    )
    assert receipt["declared_limits"]["process_time_s"] == 14400.0
    assert receipt["checks"]["sample_consumed_L"] is True


def test_postrun_amendment_adds_failure_without_provider_rerun() -> None:
    report_path = (
        ROOT
        / "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v1.json"
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report.pop("postrun_amendment", None)
    amended = evaluator.amend_report_with_declared_resource_audit(
        report,
        original_report_sha256="a" * 64,
        original_markdown_sha256="b" * 64,
        original_result_commit="8d2667a2",
        amendment_commit="c" * 40,
    )

    assert amended["status"] == "failed"
    assert amended["declared_resource_budget"]["passed"] is False
    assert amended["postrun_amendment"]["provider_rerun"] is False
    assert amended["postrun_amendment"]["action_or_provider_data_changed"] is False
    assert "declared_resource_budget_exceeded" in amended["failure_class_counts"]


def test_runtime_contract_binding_matches_frozen_hash() -> None:
    request = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    binding = evaluator._runtime_contract_binding(
        composition_request=request,
        campaign_card=evaluator._campaign_resource_card(request),
    )

    assert binding["task_contract_hash_matches"] is True
    assert binding["task_contract_hash"] == evaluator.FROZEN_RUNTIME_TASK_CONTRACT_HASH


def test_current_resolution_fails_on_sha_drift(tmp_path: Path) -> None:
    root = _minimal_current_repository(tmp_path)
    evidence = evaluator.resolve_existing_evidence(root)
    assert evidence["U05"]["passed"] is True

    path = root / "evidence/u05.json"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(evaluator.CompleteAgentQualificationError, match="SHA drifted"):
        evaluator.resolve_existing_evidence(root)


def test_current_resolution_fails_if_first_unseen_row_changes(tmp_path: Path) -> None:
    root = _minimal_current_repository(tmp_path)
    u05_path = root / "evidence/u05.json"
    u05 = json.loads(u05_path.read_text(encoding="utf-8"))
    wrong = copy.deepcopy(u05["generated_qualification"]["cases"][0])
    wrong["composition_id"] = "not-the-frozen-first-row"
    wrong["generation_index"] = 1
    u05["generated_qualification"]["cases"].insert(0, wrong)
    new_sha = _write_json(u05_path, u05)
    current_path = root / evaluator.CURRENT_CONFIG
    current = json.loads(current_path.read_text(encoding="utf-8"))
    current["evidence_dag"]["nodes"][evaluator.U05_NODE_ID]["sha256"] = new_sha
    _write_json(current_path, current)

    with pytest.raises(
        evaluator.CompleteAgentQualificationError,
        match="first unseen case drifted",
    ):
        evaluator.resolve_existing_evidence(root)


def test_provider_preflight_is_exact_and_retains_no_command_body(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def runner(command: Any, cwd: Path) -> subprocess.CompletedProcess[str]:
        del cwd
        calls.append(list(command))
        stdout = (
            evaluator.FROZEN_CODEX_CLI_VERSION + "\n"
            if command[-1] == "--version"
            else "Logged in using ChatGPT\n"
        )
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    receipt = evaluator.collect_provider_preflight(
        tmp_path,
        codex_executable="codex",
        runner=runner,
    )

    assert receipt["verified"] is True
    assert calls == [["codex", "--version"], ["codex", "login", "status"]]
    assert receipt["version_command"]["body_retained"] is False
    assert "Logged in using ChatGPT" not in json.dumps(receipt)


def test_provider_accounting_fails_closed_on_missing_mcp_step() -> None:
    receipt = _verified_provider_receipt(step_count=1)
    accounting, failures = evaluator._provider_accounting(
        receipts=[receipt],
        method_usage=_method_usage(),
        action_count=2,
    )

    assert accounting["passed"] is False
    assert {row["class"] for row in failures} == {"mcp_step_count_mismatch"}
    assert "monetary_cost_usd" not in accounting["method_resource_usage"]
    assert "provider_base_url" not in accounting["method_resource_usage"]["model_provenance"]


def _first_step_record(*, remaining_budget: int | None = None) -> HistoryRecord:
    request = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    card = evaluator._campaign_resource_card(request)
    env = gym.make(
        "ChemWorld",
        composition=request,
        seed=evaluator.FROZEN_WORLD_SEED,
        campaign_resource_card=card,
    )
    try:
        observation, _ = env.reset(seed=evaluator.FROZEN_WORLD_SEED)
        action = {"operation": "add_solvent", "solvent": 1, "volume_L": 0.025}
        observation, reward, _terminated, _truncated, info = env.step(action)
        view = agent_view_bundle(env, observation, info)
        if remaining_budget is not None:
            view["tool_json"]["campaign_state"]["remaining_budget"] = remaining_budget
        return HistoryRecord(
            step=1,
            action=action,
            observation=observation_to_json(observation),
            reward=float(reward),
            info=info,
            public_view=view,
            method_resources={"operation_count": 1},
        )
    finally:
        env.close()


def test_step_monitor_checks_every_record_and_emits_structured_event(
    capsys: pytest.CaptureFixture[str],
) -> None:
    request = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    monitor = evaluator._StepFailFastMonitor(
        composition_request=request,
        campaign_card=evaluator._campaign_resource_card(request),
    )
    try:
        monitor.observe(_first_step_record())
    finally:
        monitor.close()

    event = json.loads(capsys.readouterr().out.strip())
    assert event["status"] == "passed"
    assert event["step"] == 1
    assert event["remaining_operations"]["closure_reserve_required"] == 3
    assert monitor.events == [event]


def test_available_operations_reads_nested_and_compact_instrument_choices() -> None:
    nested = {
        "tool_json": {
            "available_actions": [
                {
                    "operation": "measure",
                    "schema": {
                        "fields": [
                            {"field": "instrument", "choices": ["final_assay"]}
                        ]
                    },
                }
            ]
        }
    }
    compact = {
        "tool_json": {
            "available_actions": [
                {
                    "operation": "measure",
                    "instrument": {"choices": ["hplc", "final_assay"]},
                }
            ]
        }
    }

    assert evaluator._available_operations(nested) == ({"measure"}, {"final_assay"})
    assert evaluator._available_operations(compact) == (
        {"measure"},
        {"hplc", "final_assay"},
    )


def test_step_monitor_fails_fast_before_closeout_reserve_is_lost(
    capsys: pytest.CaptureFixture[str],
) -> None:
    request = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    monitor = evaluator._StepFailFastMonitor(
        composition_request=request,
        campaign_card=evaluator._campaign_resource_card(request),
    )
    try:
        with pytest.raises(
            evaluator.CompleteAgentQualificationError,
            match="below_closeout_reserve",
        ):
            monitor.observe(_first_step_record(remaining_budget=2))
    finally:
        monitor.close()

    event = json.loads(capsys.readouterr().out.strip())
    assert event["status"] == "failed"
    assert "remaining_budget_below_closeout_reserve" in event["failures"]


def test_step_monitor_fails_fast_on_missing_resource_receipt() -> None:
    request = evaluator.resolve_existing_evidence(ROOT)["U05"]["composition_request"]
    monitor = evaluator._StepFailFastMonitor(
        composition_request=request,
        campaign_card=evaluator._campaign_resource_card(request),
    )
    record = _first_step_record()
    record.info.pop("campaign_resource_preflight")
    try:
        with pytest.raises(
            evaluator.CompleteAgentQualificationError,
            match="campaign_resource_receipt_missing",
        ):
            monitor.observe(record)
    finally:
        monitor.close()


def test_lifecycle_fails_closed_on_rollback_and_missing_final_assay() -> None:
    actions = [
        {
            "action": {"operation": "add_reagent", "amount_mol": 0.01},
            "transaction": {"status": "rolled_back"},
            "terminated": False,
            "truncated": False,
            "method_resources": {"complete_experiment_count": 0},
        }
    ]
    lifecycle, failures = evaluator._lifecycle_receipt(
        actions,
        method_usage=_method_usage(),
        termination_probe=None,
        evaluation_receipt=None,
    )

    assert lifecycle["passed"] is False
    assert lifecycle["rollback_count"] == 1
    assert failures[0]["class"] == "lifecycle_closure_failed"
    assert "all_actions_committed" in failures[0]["checks"]
    assert "exactly_one_final_assay" in failures[0]["checks"]


def test_receipt_completeness_checks_resource_leakage_and_replay() -> None:
    report = {
        "actions": [
            {
                "step": 1,
                "public_input": {},
                "action": {"operation": "terminate"},
                "action_sha256": "x",
                "schema_validation": {"valid": True},
                "transaction": {"status": "committed"},
                "constitution_checks": [],
                "world_events": [],
                "resource_preflight": {},
                "resource_outcome_delta": {},
                "resource_reconciliation": {"resource_reconciled": False},
                "public_observation": {},
                "method_resources": {},
                "provider_binding": {
                    "accepted_action_verified": True,
                    "mcp_step": {"verified": True},
                },
                "leakage_findings": [],
                "failures": [],
            }
        ],
        "provider_accounting": {"passed": True},
        "lifecycle": {"passed": True},
        "environment_resource_receipt": {"resource_reconciled": False},
        "exact_replay": {"verified": False},
        "public_boundary": {"finding_count": 1},
    }
    completeness, failures = evaluator._receipt_completeness(report)

    assert completeness["passed"] is False
    requirements = {row["requirement"] for row in completeness["errors"]}
    assert {
        "resource_reconciled",
        "environment_resources",
        "exact_replay",
        "zero_leakage",
    }.issubset(requirements)
    assert all(row["class"] == "missing_or_failed_receipt" for row in failures)


def test_sanitizer_rejects_final_summary_and_absolute_temp_path(tmp_path: Path) -> None:
    payload = {
        "provider": {"final_payload_summary": "secret summary"},
        "workspace": str(tmp_path / "agent"),
    }
    findings = evaluator._sanitization_findings(payload, temp_root=tmp_path)

    assert any(item.startswith("forbidden_key:") for item in findings)
    assert any(item.startswith("temporary_path:") for item in findings)
    assert any(item.startswith("absolute_path:") for item in findings)


def test_write_outputs_refuses_overwrite_by_default(tmp_path: Path) -> None:
    report = _minimal_output_report()
    json_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"
    evaluator.write_outputs(
        report,
        output_path=json_path,
        markdown_path=markdown_path,
    )

    with pytest.raises(FileExistsError, match="refusing to replace or overwrite"):
        evaluator.write_outputs(
            report,
            output_path=json_path,
            markdown_path=markdown_path,
        )
