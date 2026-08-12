from __future__ import annotations

import json
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import ClassVar

import pytest
import scripts.run_work_ii_method_qualification_triplet as qualification_runner

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    FORMAL_COMPLETE_EXPERIMENTS_PER_CELL,
    FORMAL_SNAPSHOT_STAGES,
    build_formal_preflight,
)
from chemworld.eval.work_ii_qualification import (
    METHOD_QUALIFICATION_REPORT_VERSION,
    REQUIRED_CELL_QUALIFICATION_CHECKS,
    build_method_qualification_readiness,
    build_method_qualification_receipt,
    build_qualification_execution_authorization,
    method_qualification_report_sha256,
    qualification_execution_journal_sha256,
    qualification_receipt_sha256,
    validate_method_qualification_readiness,
    validate_method_qualification_receipt,
    validate_method_qualification_report,
    validate_qualification_execution_authorization,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
SYNTHETIC_OBSERVED_COST_USD = 0.00004242


@pytest.fixture(autouse=True)
def _passed_resource_calibration_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    readiness = {
        "status": "calibration_passed_method_qualification_eligible",
        "method_qualification_may_be_authorized": True,
        "missing_pattern_rounds": [],
    }
    monkeypatch.setattr(
        qualification_runner,
        "build_resource_calibration_readiness",
        lambda *_args, **_kwargs: deepcopy(readiness),
    )
    monkeypatch.setattr(
        qualification_runner,
        "validate_resource_calibration_readiness",
        lambda _report: [],
    )


@pytest.fixture
def repo_tmp_path():
    path = Path(tempfile.mkdtemp(prefix=".pytest-workii-qualification-", dir=ROOT))
    try:
        yield path
    finally:
        shutil.rmtree(path)


class _FakeQualificationProcess:
    rows: ClassVar[dict[str, dict[str, object]]] = {}
    fail_once_arms: ClassVar[set[str]] = set()
    launched_arms: ClassVar[list[str]] = []

    def __init__(self, command, **kwargs) -> None:
        del kwargs
        arm = command[command.index("--prior-arm") + 1]
        output = Path(command[command.index("--output") + 1])
        attempt_path = Path(
            command[command.index("--qualification-attempt-authorization") + 1]
        )
        ledger_path = Path(command[command.index("--qualification-cost-ledger") + 1])
        type(self).launched_arms.append(arm)
        self.returncode = 0
        if arm in type(self).fail_once_arms:
            type(self).fail_once_arms.remove(arm)
            self.returncode = 1
            return
        output.mkdir(parents=True, exist_ok=False)
        row = deepcopy(type(self).rows[arm])
        attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        row["qualification_attempt_authorization_binding"] = {
            "path": attempt_path.resolve().relative_to(ROOT).as_posix(),
            "sha256": file_sha256(attempt_path),
            "attempt_authorization_sha256": attempt[
                "attempt_authorization_sha256"
            ],
            "qualification_cost_ledger_path": ledger_path.resolve()
            .relative_to(ROOT)
            .as_posix(),
            "qualification_cost_ledger_sha256": ledger[
                "qualification_cost_ledger_sha256"
            ],
        }
        (output / "summary.json").write_text(
            json.dumps(row), encoding="utf-8"
        )

    def poll(self) -> int:
        return self.returncode

    def wait(self) -> int:
        return self.returncode


def _authorization(
    manifest: dict[str, object], *, ceiling: float = 50.0
) -> dict[str, object]:
    return build_qualification_execution_authorization(
        ROOT,
        manifest,
        currency_ceiling_usd=ceiling,
        approved_at="2026-08-10T00:00:00+08:00",
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-10T00:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )


def _qualification_report(
    manifest: dict[str, object],
    authorization_path: Path | None = None,
) -> dict[str, object]:
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
                    "complete_experiment_count": FORMAL_COMPLETE_EXPERIMENTS_PER_CELL,
                    "experiments": [
                        {"experiment_index": index}
                        for index in range(1, FORMAL_COMPLETE_EXPERIMENTS_PER_CELL + 1)
                    ],
                    "unique_recipe_count": 6,
                    "exact_repeat_count": 2,
                    "right_censored_open_experiment": False,
                    "belief_snapshots": [
                        {"stage": stage}
                        for stage in FORMAL_SNAPSHOT_STAGES
                    ],
                    "resource_rejection_count": 0,
                    "final_campaign_resources": {
                        "campaign_terminal": True,
                        "state": {
                            "closed_batches": FORMAL_COMPLETE_EXPERIMENTS_PER_CELL,
                            "final_assays": FORMAL_COMPLETE_EXPERIMENTS_PER_CELL,
                        },
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
        "qualification_execution_authorized": authorization_path is not None,
        "qualification_execution_authorization_binding": (
            {
                "path": authorization_path.resolve().relative_to(ROOT).as_posix(),
                "sha256": file_sha256(authorization_path),
                "authorization_sha256": json.loads(
                    authorization_path.read_text(encoding="utf-8")
                )["authorization_sha256"],
            }
            if authorization_path is not None
            else None
        ),
        "config_sha256": "a" * 64,
        "config_file_sha256": config_file_sha256,
        "world_seed": 0,
        "cell_count": 3,
        "completed_cell_count": 3,
        "results": rows,
    }
    report["report_sha256"] = method_qualification_report_sha256(report)
    return report


def _receipt(
    tmp_path: Path,
    monkeypatch,
) -> tuple[dict[str, object], dict[str, object]]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = tmp_path / "qualification-authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    template = _qualification_report(manifest)
    _FakeQualificationProcess.rows = {
        row["arm"]: row for row in template["results"]
    }
    _FakeQualificationProcess.fail_once_arms = set()
    _FakeQualificationProcess.launched_arms = []
    monkeypatch.setattr(
        qualification_runner.subprocess, "Popen", _FakeQualificationProcess
    )
    output = tmp_path / "qualification-output"
    progress = qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=tmp_path / "qualification-progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
    )
    assert progress["status"] == "passed"
    receipt = build_method_qualification_receipt(
        ROOT,
        output / "report.json",
        manifest,
        observed_cost_usd=SYNTHETIC_OBSERVED_COST_USD,
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-10T00:00:00+08:00",
    )
    return receipt, manifest


def test_qualification_execution_authorization_is_explicit_and_credential_free() -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    assert (
        validate_qualification_execution_authorization(ROOT, authorization, manifest)
        == []
    )
    assert authorization["provider_execution_allowed"] is True
    assert authorization["formal_execution_authorized"] is False
    assert authorization["user_authorization"]["credentials_present"] is False
    assert "api_key" not in json.dumps(authorization).lower()
    budget = authorization["qualification_currency_budget"]
    assert budget["initial_schedule"]["cost_cap_usd"] == 0.172032
    assert budget["all_infrastructure_resumes"]["cost_cap_usd"] == 0.344064


def test_method_qualification_report_without_precall_authorization_is_rejected(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    report = _qualification_report(manifest)
    errors = validate_method_qualification_report(ROOT, report, manifest)
    assert "method qualification report lacks pre-execution user authorization" in errors
    assert (
        "method qualification report lacks its execution-authorization binding" in errors
    )


def test_authorized_qualification_report_requires_parent_execution_journal(
    repo_tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = repo_tmp_path / "qualification-authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    report = _qualification_report(manifest, authorization_path)

    errors = validate_method_qualification_report(ROOT, report, manifest)

    assert "qualification execution journal binding is missing" in errors


def test_method_qualification_receipt_builder_round_trips_validated_triplet(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    manual_receipt, manifest = _receipt(repo_tmp_path, monkeypatch)
    report_path = repo_tmp_path / "qualification-output" / "report.json"
    built = build_method_qualification_receipt(
        ROOT,
        report_path,
        manifest,
        observed_cost_usd=SYNTHETIC_OBSERVED_COST_USD,
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-10T00:00:00+08:00",
    )
    assert validate_method_qualification_receipt(
        ROOT,
        built,
        manifest,
        currency_ceiling_usd=50.0,
    ) == []
    assert built["qualification_report_binding"] == manual_receipt[
        "qualification_report_binding"
    ]
    assert built["qualification_execution_authorization_sha256"]
    assert built["qualification_cost_accounting"]["token_totals"] == {
        "input_tokens": 300,
        "uncached_input_tokens": 150,
        "output_tokens": 75,
    }
    assert (
        built["qualification_cost_accounting"]["calculated_cost_usd"]
        == SYNTHETIC_OBSERVED_COST_USD
    )
    with pytest.raises(ValueError, match="differs from frozen prices"):
        build_method_qualification_receipt(
            ROOT,
            report_path,
            manifest,
            observed_cost_usd=0.2,
            pricing_source="https://provider.example/pricing",
            pricing_observed_at="2026-08-10T00:00:00+08:00",
        )


def test_method_qualification_receipt_is_semantic_self_hashed_and_cost_bound(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(repo_tmp_path, monkeypatch)
    assert (
        validate_method_qualification_receipt(
            ROOT,
            receipt,
            manifest,
            currency_ceiling_usd=50.0,
        )
        == []
    )
    receipt["approved_currency_ceiling_usd"] = 51.0
    errors = validate_method_qualification_receipt(
        ROOT,
        receipt,
        manifest,
        currency_ceiling_usd=51.0,
    )
    assert "method qualification receipt self-hash mismatch" in errors
    assert "method qualification receipt has invalid user currency approval" in errors


def test_shallow_passed_json_cannot_authorize_formal_execution(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(repo_tmp_path, monkeypatch)
    report_path = repo_tmp_path / "qualification-output" / "report.json"
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
        ROOT,
        receipt,
        manifest,
        currency_ceiling_usd=50.0,
    )
    assert "method qualification report does not complete three cells" in errors
    assert "method qualification report results are missing" in errors


def test_semantic_failure_is_rejected_even_after_all_hashes_are_refreshed(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(repo_tmp_path, monkeypatch)
    report_path = repo_tmp_path / "qualification-output" / "report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["results"][1]["completed"] = False
    report["report_sha256"] = method_qualification_report_sha256(report)
    report_path.write_text(json.dumps(report), encoding="utf-8")
    binding = receipt["qualification_report_binding"]
    binding["sha256"] = file_sha256(report_path)
    binding["report_sha256"] = report["report_sha256"]
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    errors = validate_method_qualification_receipt(
        ROOT,
        receipt,
        manifest,
        currency_ceiling_usd=50.0,
    )
    assert "aligned_nominal: method qualification cell did not complete" in errors


def test_receipt_rejects_rehashed_journal_that_omits_an_attempt(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    receipt, manifest = _receipt(repo_tmp_path, monkeypatch)
    output = repo_tmp_path / "qualification-output"
    journal_path = output / "execution_journal.json"
    report_path = output / "report.json"
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    journal["attempts"] = journal["attempts"][:-1]
    journal["execution_journal_sha256"] = qualification_execution_journal_sha256(
        journal
    )
    journal_path.write_text(json.dumps(journal), encoding="utf-8")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    journal_binding = report["qualification_execution_journal_binding"]
    journal_binding["sha256"] = file_sha256(journal_path)
    journal_binding["execution_journal_sha256"] = journal[
        "execution_journal_sha256"
    ]
    report["report_sha256"] = method_qualification_report_sha256(report)
    report_path.write_text(json.dumps(report), encoding="utf-8")
    report_binding = receipt["qualification_report_binding"]
    report_binding["sha256"] = file_sha256(report_path)
    report_binding["report_sha256"] = report["report_sha256"]
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)

    errors = validate_method_qualification_receipt(
        ROOT,
        receipt,
        manifest,
        currency_ceiling_usd=50.0,
    )

    assert (
        "qualification execution journal omits or adds attempt authorizations"
        in errors
    )


def test_method_qualification_readiness_is_zero_call_and_execution_blocked() -> None:
    first = build_method_qualification_readiness(ROOT, DESIGN, ANALYSIS)
    second = build_method_qualification_readiness(ROOT, DESIGN, ANALYSIS)
    assert first == second
    assert validate_method_qualification_readiness(first) == []
    assert first["status"] == "passed_provider_execution_blocked"
    assert first["provider_calls_executed"] == 0
    assert first["expected_counts"]["accepted_scientific_cells"] == 3
    assert first["expected_counts"]["operation_attempts_hard_cap"] == 168
    assert all(
        item["eligible_for_current_method_receipt"] is False
        for item in first["historical_evidence_assessment"]
    )


def test_qualification_triplet_runner_reserves_cost_and_terminalizes_all_arms(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = repo_tmp_path / "authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    template = _qualification_report(manifest)
    _FakeQualificationProcess.rows = {
        row["arm"]: row for row in template["results"]
    }
    _FakeQualificationProcess.fail_once_arms = set()
    _FakeQualificationProcess.launched_arms = []
    monkeypatch.setattr(
        qualification_runner.subprocess, "Popen", _FakeQualificationProcess
    )
    output = repo_tmp_path / "qualification-output"

    progress = qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=False,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )

    assert progress["status"] == "passed"
    assert progress["provider_attempt_count"] == 3
    assert progress["reserved_cost_usd"] == 0.172032
    assert _FakeQualificationProcess.launched_arms == list(FORMAL_ARMS)
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert validate_method_qualification_report(ROOT, report, manifest) == []


def test_qualification_triplet_runner_resumes_only_missing_infrastructure_arm(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = repo_tmp_path / "authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    template = _qualification_report(manifest)
    _FakeQualificationProcess.rows = {
        row["arm"]: row for row in template["results"]
    }
    failed_arm = "misindexed_nominal"
    _FakeQualificationProcess.fail_once_arms = {failed_arm}
    _FakeQualificationProcess.launched_arms = []
    monkeypatch.setattr(
        qualification_runner.subprocess, "Popen", _FakeQualificationProcess
    )
    output = repo_tmp_path / "qualification-output"

    first = qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=False,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )
    second = qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=True,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )

    assert first["status"] == "infrastructure_incomplete_missing_only_resume_required"
    assert first["pending_arms"] == [failed_arm]
    assert second["status"] == "passed"
    assert second["provider_attempt_count"] == 4
    assert second["provider_attempt_counts_by_arm"] == {
        "opaque": 1,
        "aligned_nominal": 1,
        "misindexed_nominal": 2,
    }
    assert _FakeQualificationProcess.launched_arms.count(failed_arm) == 2
    assert _FakeQualificationProcess.launched_arms.count("opaque") == 1
    assert _FakeQualificationProcess.launched_arms.count("aligned_nominal") == 1


def test_qualification_triplet_runner_rejects_rehashed_terminal_tampering(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = repo_tmp_path / "authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    template = _qualification_report(manifest)
    _FakeQualificationProcess.rows = {
        row["arm"]: row for row in template["results"]
    }
    _FakeQualificationProcess.fail_once_arms = set()
    _FakeQualificationProcess.launched_arms = []
    monkeypatch.setattr(
        qualification_runner.subprocess, "Popen", _FakeQualificationProcess
    )
    output = repo_tmp_path / "qualification-output"
    qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=False,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )
    terminal_path = output / "terminal_receipts" / "opaque.json"
    terminal = json.loads(terminal_path.read_text(encoding="utf-8"))
    terminal["attempt_id"] = "forged-attempt"
    terminal["terminal_receipt_sha256"] = qualification_runner._self_hash(
        terminal, "terminal_receipt_sha256"
    )
    terminal_path.write_text(json.dumps(terminal), encoding="utf-8")

    with pytest.raises(
        RuntimeError,
        match="terminal receipt lacks an authorized attempt",
    ):
        qualification_runner.execute_triplet(
            authorization_path=authorization_path,
            output_root=output,
            progress_path=repo_tmp_path / "qualification-progress.jsonl",
            resume=True,
            cell_runner=repo_tmp_path / "fake-cell-runner.py",
        )


def test_qualification_triplet_runner_rebuilds_report_after_terminal_only_crash(
    monkeypatch,
    repo_tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorization = _authorization(manifest)
    authorization_path = repo_tmp_path / "authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    template = _qualification_report(manifest)
    _FakeQualificationProcess.rows = {
        row["arm"]: row for row in template["results"]
    }
    _FakeQualificationProcess.fail_once_arms = set()
    _FakeQualificationProcess.launched_arms = []
    monkeypatch.setattr(
        qualification_runner.subprocess, "Popen", _FakeQualificationProcess
    )
    output = repo_tmp_path / "qualification-output"
    qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=False,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )
    (output / "report.json").unlink()
    launched_before_resume = list(_FakeQualificationProcess.launched_arms)

    progress = qualification_runner.execute_triplet(
        authorization_path=authorization_path,
        output_root=output,
        progress_path=repo_tmp_path / "qualification-progress.jsonl",
        resume=True,
        cell_runner=repo_tmp_path / "fake-cell-runner.py",
    )

    assert progress["status"] == "passed"
    assert _FakeQualificationProcess.launched_arms == launched_before_resume
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert validate_method_qualification_report(ROOT, report, manifest) == []
