from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from scripts.run_scientific_adaptation_shakedown import (
    DEVELOPMENT_TEST_METHODS,
    DEVELOPMENT_TEST_PROTOCOL,
    _DeterministicMockClient,
    _run_cell,
    run_shakedown,
)

from chemworld.eval.mechanism_adaptation_execution import (
    load_json_object,
    load_protocol_object,
    selected_campaign_rows,
)
from chemworld.providers.deepseek import DeepSeekAPIError


class _InterruptingClient:
    model = "deepseek-v4-flash"
    thinking = False
    reasoning_effort = None

    def __init__(self) -> None:
        self.delegate = _DeterministicMockClient(model=self.model)
        self.call_count = 0

    def complete_json(self, **kwargs):
        self.call_count += 1
        if self.call_count == 2:
            raise DeepSeekAPIError(
                "temporary structured-output outage",
                attempts=1,
                usage={"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60},
                attempt_records=(
                    {
                        "attempt_index": 1,
                        "status": "failed",
                        "request_id": "test-request",
                        "model_id": self.model,
                        "usage": {
                            "prompt_tokens": 50,
                            "completion_tokens": 10,
                            "total_tokens": 60,
                        },
                        "usage_complete": True,
                        "billable": True,
                        "failure_type": "invalid_structured_output",
                    },
                ),
            )
        return self.delegate.complete_json(**kwargs)

    def pricing_snapshot(self):
        return self.delegate.pricing_snapshot()

    def estimate_cost_usd(self, usage):
        return self.delegate.estimate_cost_usd(usage)


class _InvalidResponseClient:
    model = "deepseek-v4-flash"
    thinking = False
    reasoning_effort = None

    def __init__(self) -> None:
        self.delegate = _DeterministicMockClient(model=self.model)

    def complete_json(self, **kwargs):
        completion = self.delegate.complete_json(**kwargs)
        payload = dict(completion.payload)
        payload["belief_update_rule"] = "private-response-fragment-" * 40
        return replace(completion, payload=payload)

    def pricing_snapshot(self):
        return self.delegate.pricing_snapshot()

    def estimate_cost_usd(self, usage):
        return self.delegate.estimate_cost_usd(usage)


def test_mock_shakedown_writes_complete_resumable_receipts(tmp_path: Path) -> None:
    output = tmp_path / "shakedown"
    args = argparse.Namespace(
        protocol=DEVELOPMENT_TEST_PROTOCOL,
        llm_methods=DEVELOPMENT_TEST_METHODS,
        output=output,
        provider="mock",
        allow_external_provider=False,
        task="reaction-to-crystallization",
        pair_id=None,
        pair_limit=1,
        method_id=["dev_flash_stateful"],
        pre_experiments=1,
        post_experiments=1,
        max_provider_calls=4,
        max_provider_cost_usd=0.0,
        resume=False,
    )

    report = run_shakedown(args)

    assert report["cell_count"] == 2
    assert report["experiment_count"] == 4
    assert report["completed_experiment_count"] == 4
    assert report["provider_call_count"] == 4
    assert report["provider_billed_cost_usd"] == 0.0
    assert "r4" in report["method_config_freeze_id"]
    assert len(report["method_config_sha256"]) == 64
    assert list(report["method_contract_sha256"]) == ["dev_flash_stateful"]
    assert len(report["method_contract_sha256"]["dev_flash_stateful"]) == 64
    assert len(report["runner_source_sha256"]) == 64
    assert report["prompt_budget_within_contract"] is True
    assert (
        report["max_prompt_estimated_tokens"]["dev_flash_stateful"]
        <= (report["prompt_token_estimate_cap"]["dev_flash_stateful"])
    )
    receipt_paths = sorted((output / "receipts").glob("*.json"))
    assert len(receipt_paths) == 2
    receipt = json.loads(receipt_paths[0].read_text(encoding="utf-8"))
    evidence_ids = [
        evidence["evidence_id"]
        for experiment in receipt["experiments"]
        for evidence in experiment["result"]["measurement_evidence"]
    ]
    assert len(evidence_ids) == len(set(evidence_ids))
    assert receipt["formal_result"] is False
    assert receipt["mock_provider"] is True
    assert receipt["method_config_sha256"] == report["method_config_sha256"]
    assert (
        receipt["method_contract_sha256"] == report["method_contract_sha256"][receipt["method_id"]]
    )
    assert all(
        experiment["decision_audit"]["prompt_estimated_tokens"]
        <= experiment["decision_audit"]["prompt_token_estimate_cap"]
        for experiment in receipt["experiments"]
    )

    args.resume = True
    assert run_shakedown(args)["receipt_sha256"] == report["receipt_sha256"]


def test_infrastructure_checkpoint_resumes_only_missing_experiment() -> None:
    protocol = load_protocol_object(DEVELOPMENT_TEST_PROTOCOL)
    methods = load_json_object(DEVELOPMENT_TEST_METHODS)
    row = selected_campaign_rows(
        protocol,
        tasks=["reaction-to-crystallization"],
        limit=1,
    )[0]
    interrupted = _run_cell(
        protocol=protocol,
        methods=methods,
        method_id="dev_flash_stateful",
        row=row,
        provider="mock",
        pre_experiments=1,
        post_experiments=1,
        client_override=_InterruptingClient(),
    )

    assert interrupted["cell_status"] == "infrastructure_failure"
    assert interrupted["completed_experiment_count"] == 1
    assert interrupted["failure"]["runner_missing_only_resume_supported"] is True
    assert interrupted["resources"]["model_call_count"] == 2
    assert interrupted["resources"]["provider_attempt_records"][0]["logical_decision_index"] == 2

    resumed = _run_cell(
        protocol=protocol,
        methods=methods,
        method_id="dev_flash_stateful",
        row=row,
        provider="mock",
        pre_experiments=1,
        post_experiments=1,
        resume_checkpoint=interrupted,
        client_override=_DeterministicMockClient(model="deepseek-v4-flash"),
    )

    assert resumed["cell_status"] == "completed"
    assert resumed["completed_experiment_count"] == 2
    assert resumed["resources"]["model_call_count"] == 3
    assert [item["result"]["experiment_index"] for item in resumed["experiments"]] == [0, 1]


def test_method_failure_receipt_adds_content_free_validation_diagnostics() -> None:
    protocol = load_protocol_object(DEVELOPMENT_TEST_PROTOCOL)
    methods = load_json_object(DEVELOPMENT_TEST_METHODS)
    row = selected_campaign_rows(
        protocol,
        tasks=["reaction-to-crystallization"],
        limit=1,
    )[0]

    receipt = _run_cell(
        protocol=protocol,
        methods=methods,
        method_id="dev_flash_direct",
        row=row,
        provider="mock",
        pre_experiments=1,
        post_experiments=0,
        client_override=_InvalidResponseClient(),
    )

    assert receipt["cell_status"] == "method_failure"
    assert receipt["failure"]["validation_diagnostics"] == {
        "field_path": "belief_update_rule",
        "constraint": "max_characters",
        "observed": 1040,
        "limit": 700,
    }
    assert "private-response-fragment" not in json.dumps(receipt)


def test_mock_shakedown_selects_one_pair_per_task(tmp_path: Path) -> None:
    args = argparse.Namespace(
        protocol=DEVELOPMENT_TEST_PROTOCOL,
        llm_methods=DEVELOPMENT_TEST_METHODS,
        output=tmp_path / "two-task-shakedown",
        provider="mock",
        allow_external_provider=False,
        task=["reaction-to-crystallization", "electrochemical-conversion"],
        pair_id=None,
        pair_limit=1,
        arm=None,
        method_id=["dev_flash_direct"],
        pre_experiments=1,
        post_experiments=1,
        max_provider_calls=8,
        max_provider_cost_usd=0.0,
        resume=False,
    )

    report = run_shakedown(args)

    assert report["task_ids"] == [
        "reaction-to-crystallization",
        "electrochemical-conversion",
    ]
    assert report["cell_count"] == 4
    assert report["completed_cell_count"] == 4
    assert report["completed_experiment_count"] == 8
    assert report["provider_call_count"] == 8
    assert list(report["method_contract_sha256"]) == ["dev_flash_direct"]


def test_wellau_single_backend_mock_preflight_has_64_decisions(tmp_path: Path) -> None:
    methods = (
        DEVELOPMENT_TEST_METHODS.parent
        / "participant_methods_wellau_codex_sol_development.json"
    )
    args = argparse.Namespace(
        protocol=DEVELOPMENT_TEST_PROTOCOL,
        llm_methods=methods,
        output=tmp_path / "wellau-mock-preflight",
        provider="mock",
        allow_external_provider=False,
        task=["reaction-to-crystallization", "electrochemical-conversion"],
        pair_id=None,
        pair_limit=1,
        arm=None,
        method_id=["dev_codex_sol_direct", "dev_codex_sol_stateful"],
        pre_experiments=6,
        post_experiments=2,
        max_provider_calls=64,
        max_provider_cost_usd=0.0,
        max_provider_total_tokens=1_000_000,
        max_provider_output_tokens=8_000,
        resume=False,
    )

    report = run_shakedown(args)

    assert report["cell_count"] == 8
    assert report["planned_experiment_count"] == 64
    assert report["completed_experiment_count"] == 64
    assert report["provider_call_count"] == 64
    assert report["provider_input_token_count"] > 0
    assert report["provider_output_token_count"] > 0
    assert report["provider_total_token_count"] == (
        report["provider_input_token_count"] + report["provider_output_token_count"]
    )
    assert report["provider_total_token_count"] == report["provider_reported_total_tokens"]
    assert report["prompt_budget_within_contract"] is True
    assert report["method_ids"] == ["dev_codex_sol_direct", "dev_codex_sol_stateful"]
