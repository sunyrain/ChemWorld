from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import FORMAL_ARMS, build_formal_preflight
from chemworld.eval.work_ii_qualification import (
    METHOD_QUALIFICATION_RECEIPT_VERSION,
    METHOD_QUALIFICATION_REPORT_VERSION,
    REQUIRED_CELL_QUALIFICATION_CHECKS,
    build_method_qualification_readiness,
    method_qualification_report_sha256,
    qualification_receipt_sha256,
    validate_method_qualification_readiness,
    validate_method_qualification_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _qualification_report(manifest: dict[str, object]) -> dict[str, object]:
    provider = manifest["provider_contract"]
    assert isinstance(provider, dict)
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "best public campaign evidence",
    }
    recommendation_hash = canonical_json_sha256(recommendation)
    task_binding = manifest["task_bindings"][0]
    config_file_sha256 = task_binding["campaign_config"]["sha256"]
    rows: list[dict[str, object]] = []
    for arm in FORMAL_ARMS:
        rows.append(
            {
                "arm": arm,
                "completed": True,
                "failure": None,
                "analysis": {
                    "complete_experiment_count": 4,
                    "experiments": [{"experiment_index": index} for index in range(1, 5)],
                    "right_censored_open_experiment": False,
                    "belief_snapshots": [
                        {"stage": stage}
                        for stage in (
                            "pre_evidence",
                            "after_experiment_1",
                            "after_experiment_2",
                            "final",
                        )
                    ],
                    "resource_rejection_count": 0,
                    "final_campaign_resources": {
                        "campaign_terminal": True,
                        "state": {"closed_batches": 4, "final_assays": 4},
                    },
                    "final_recommendation": recommendation,
                    "final_recommendation_sha256": recommendation_hash,
                    "execution_audit": {"passed": True},
                },
                "method_resources": {
                    "provider_session_count": 1,
                    "model_call_count": 1,
                    "provider_usage_pending": False,
                    "provider_usage_accounting_complete": True,
                    "in_flight_model_call_count": 0,
                    "input_token_count": 100,
                    "uncached_input_token_count": 50,
                    "output_token_count": 25,
                    "model_provenance": {
                        "provider_id": provider["id"],
                        "model_id": provider["model"],
                        "request_parameters": {"reasoning_effort": provider["reasoning_effort"]},
                    },
                },
                "provider_receipts": [
                    {
                        "session_scope": "campaign",
                        "status": "completed",
                        "return_code": 0,
                        "final_payload_valid": True,
                        "final_payload_status": "campaign_complete",
                        "final_recommendation_sha256": recommendation_hash,
                        "experiment_tool_integrity_verified_after_session": True,
                        "lab_tool_integrity_verified_after_session": True,
                        "mcp_tool_integrity_verified_after_session": True,
                        "model_id": provider["model"],
                        "reasoning_effort": provider["reasoning_effort"],
                        "usage_complete": True,
                    }
                ],
                "exact_replay": {"verified": True, "mismatches": []},
                "qualification": {
                    "passed": True,
                    "checks": dict.fromkeys(REQUIRED_CELL_QUALIFICATION_CHECKS, True),
                    "failed_checks": [],
                },
            }
        )
    report: dict[str, object] = {
        "schema_version": METHOD_QUALIFICATION_REPORT_VERSION,
        "pilot_id": "work-ii-electrochemical-prior-campaign",
        "formal_result": False,
        "config_sha256": "a" * 64,
        "config_file_sha256": config_file_sha256,
        "world_seed": 0,
        "cell_count": 3,
        "completed_cell_count": 3,
        "results": rows,
    }
    report["report_sha256"] = method_qualification_report_sha256(report)
    return report


def _receipt(tmp_path: Path) -> tuple[dict[str, object], dict[str, object]]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    report = _qualification_report(manifest)
    report_path = tmp_path / "qualification-report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    task_binding = manifest["task_bindings"][0]
    receipt: dict[str, object] = {
        "schema_version": METHOD_QUALIFICATION_RECEIPT_VERSION,
        "status": "passed",
        "formal_execution_authorized": True,
        "formal_preflight_sha256": manifest["preflight_sha256"],
        "provider_contract_sha256": canonical_json_sha256(manifest["provider_contract"]),
        "provider_attempt_contract_sha256": canonical_json_sha256(
            manifest["provider_attempt_contract"]
        ),
        "participant_execution_contract_sha256": manifest["participant_execution_contract_sha256"],
        "method_qualification_contract_sha256": manifest["method_qualification_contract_sha256"],
        "blind_evaluator_contract_sha256": canonical_json_sha256(
            manifest["blind_evaluator_contract"]
        ),
        "held_out_evaluator_contract_sha256": canonical_json_sha256(
            manifest["held_out_evaluator_contract"]
        ),
        "qualification_split": "development_seed_0",
        "qualification_task_id": "electrochemical-conversion",
        "qualification_world_seed": 0,
        "qualification_campaign_config_sha256": task_binding["campaign_config"]["sha256"],
        "qualified_prior_arms": list(FORMAL_ARMS),
        "qualified_cell_count": 3,
        "formal_participant_outcome_count_before_authorization": 0,
        "approved_provider_attempt_hard_cap": manifest["expected_counts"][
            "provider_attempts_hard_cap"
        ],
        "qualification_cost_accounting": {
            "currency": "USD",
            "accounting_complete": True,
            "observed_cost_usd": 0.2,
            "approved_ceiling_usd": 0.5,
            "approved_by": "user",
            "approved_at": "2026-08-10T00:00:00+08:00",
            "pricing_source": "provider pricing catalog",
            "pricing_observed_at": "2026-08-10T00:00:00+08:00",
            "scope_method_qualification_contract_sha256": manifest[
                "method_qualification_contract_sha256"
            ],
        },
        "approved_currency_ceiling_usd": 50.0,
        "currency_approval": {
            "approved_by": "user",
            "approved_at": "2026-08-10T00:00:00+08:00",
            "approved_currency_ceiling_usd": 50.0,
            "scope_preflight_sha256": manifest["preflight_sha256"],
        },
        "qualification_report_binding": {
            "path": report_path.name,
            "sha256": file_sha256(report_path),
            "report_sha256": report["report_sha256"],
        },
    }
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    return receipt, manifest


def test_method_qualification_receipt_is_semantic_self_hashed_and_cost_bound(
    tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(tmp_path)
    assert (
        validate_method_qualification_receipt(
            tmp_path,
            receipt,
            manifest,
            currency_ceiling_usd=50.0,
        )
        == []
    )
    receipt["approved_currency_ceiling_usd"] = 51.0
    errors = validate_method_qualification_receipt(
        tmp_path,
        receipt,
        manifest,
        currency_ceiling_usd=51.0,
    )
    assert "method qualification receipt self-hash mismatch" in errors
    assert "method qualification receipt has invalid user currency approval" in errors


def test_shallow_passed_json_cannot_authorize_formal_execution(tmp_path: Path) -> None:
    receipt, manifest = _receipt(tmp_path)
    report_path = tmp_path / "qualification-report.json"
    shallow: dict[str, object] = {
        "schema_version": METHOD_QUALIFICATION_REPORT_VERSION,
        "status": "passed",
    }
    shallow["report_sha256"] = method_qualification_report_sha256(shallow)
    report_path.write_text(json.dumps(shallow), encoding="utf-8")
    binding = receipt["qualification_report_binding"]
    binding["sha256"] = file_sha256(report_path)
    binding["report_sha256"] = shallow["report_sha256"]
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    errors = validate_method_qualification_receipt(
        tmp_path,
        receipt,
        manifest,
        currency_ceiling_usd=50.0,
    )
    assert "method qualification report does not complete three cells" in errors
    assert "method qualification report results are missing" in errors


def test_semantic_failure_is_rejected_even_after_all_hashes_are_refreshed(
    tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(tmp_path)
    report_path = tmp_path / "qualification-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["results"][1]["completed"] = False
    report["report_sha256"] = method_qualification_report_sha256(report)
    report_path.write_text(json.dumps(report), encoding="utf-8")
    binding = receipt["qualification_report_binding"]
    binding["sha256"] = file_sha256(report_path)
    binding["report_sha256"] = report["report_sha256"]
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    errors = validate_method_qualification_receipt(
        tmp_path,
        receipt,
        manifest,
        currency_ceiling_usd=50.0,
    )
    assert "aligned_nominal: method qualification cell did not complete" in errors


def test_method_qualification_readiness_is_zero_call_and_execution_blocked() -> None:
    first = build_method_qualification_readiness(ROOT, DESIGN, ANALYSIS)
    second = build_method_qualification_readiness(ROOT, DESIGN, ANALYSIS)
    assert first == second
    assert validate_method_qualification_readiness(first) == []
    assert first["status"] == "passed_provider_execution_blocked"
    assert first["provider_calls_executed"] == 0
    assert first["expected_counts"]["accepted_scientific_cells"] == 3
    assert first["expected_counts"]["operation_attempts_hard_cap"] == 84
    assert all(
        item["eligible_for_current_method_receipt"] is False
        for item in first["historical_evidence_assessment"]
    )
