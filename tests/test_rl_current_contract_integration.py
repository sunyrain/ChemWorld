from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.audit_rl_current_contract_integration as integration_audit
from scripts.audit_rl_current_contract_integration import (
    REPORT_SCHEMA,
    STATUS_SCHEMA,
    build_audit,
)

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "configs" / "methods" / "rl_v0.4" / "rl_current_contract_status.json"
REPORT_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "rl-current-contract-integration-v0.4.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _claim(task_id: str) -> dict[str, Any]:
    active = ROOT / "claims" / "active" / f"{task_id}.json"
    completed = sorted((ROOT / "claims" / "completed").glob(f"{task_id}--*.json"))
    return _load(next(path for path in reversed([*completed, active]) if path.is_file()))


def test_current_contract_integration_audit_closes_rl_fail_closed() -> None:
    report = build_audit(
        root=ROOT,
        status_path=STATUS_PATH,
        source_commit="a" * 40,
        origin_main_commit="a" * 40,
        source_tree_clean=True,
    )

    assert report["schema_version"] == REPORT_SCHEMA
    assert report["status"] == "rl_current_contract_integration_passed_selection_failed"
    assert report["failed_checks"] == []
    assert all(report["checks"].values())
    assert report["method_evidence"]["ppo"]["decision"]["status"] == "selection_failed"
    assert report["method_evidence"]["sac"]["decision"]["status"] == "selection_failed"
    assert report["current_selected_checkpoint_count"] == 0
    assert report["preflight_checkpoint_contract_and_replay_evidence_verified"] is True
    assert report["formal_results_present"] is False
    assert report["bench_accessed"] is False


def test_artifact_digest_is_invariant_to_windows_json_line_endings(
    tmp_path: Path,
) -> None:
    lf_path = tmp_path / "lf.json"
    crlf_path = tmp_path / "crlf.json"
    lf_path.write_bytes(b'{\n  "status": "selection_failed"\n}\n')
    crlf_path.write_bytes(b'{\r\n  "status": "selection_failed"\r\n}\r\n')

    assert integration_audit._sha256(lf_path) == integration_audit._sha256(crlf_path)


def test_tampered_method_decision_fails_the_integration_audit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_load = integration_audit._load

    def tampered_load(path: Path, label: str) -> dict[str, Any]:
        payload = original_load(path, label)
        if label == "RL current-contract status":
            payload = copy.deepcopy(payload)
            payload["method_decisions"]["ppo"]["status"] = "ready"
            payload["method_decisions"]["ppo"]["method_ready"] = True
        return payload

    monkeypatch.setattr(integration_audit, "_load", tampered_load)
    report = build_audit(
        root=ROOT,
        status_path=STATUS_PATH,
        source_commit="a" * 40,
        origin_main_commit="a" * 40,
        source_tree_clean=True,
    )

    assert report["status"] == "rl_current_contract_integration_audit_failed"
    assert "ppo:decision_selection_failed" in report["failed_checks"]


def test_status_separates_historical_current_and_formal_evidence() -> None:
    status = _load(STATUS_PATH)

    assert status["schema_version"] == STATUS_SCHEMA
    assert status["status"] == "rl_current_contract_selection_failed"
    assert status["evidence_tiers"]["historical_diagnostic"] == {
        "ppo_archive_eligible_for_current_runtime": False,
        "sac_archive_eligible_for_current_runtime": False,
        "eligible_for_formal_checkpoint_index": False,
    }
    assert status["evidence_tiers"]["current_train_dev"]["method_ready"] is False
    assert status["evidence_tiers"]["formal_bench"]["evidence_present"] is False
    assert status["evidence_tiers"]["formal_bench"]["bench_accessed"] is False
    assert status["parent_decision"]["parent_task_complete"] is False
    assert status["global_freeze_boundary"]["global_method_freeze_closed_by_this_claim"] is False


def test_integration_claim_does_not_overlap_live_llm_ownership() -> None:
    integration_claim = _claim("benchmark-v05-rl-current-contract-integration")
    live_llm_claim = _claim("benchmark-v05-live-llm-adapters")

    integration_paths = set(integration_claim["owned_paths"])
    live_llm_paths = set(live_llm_claim["owned_paths"])
    assert integration_paths.isdisjoint(live_llm_paths)
    assert "todolist.md" not in integration_paths
    assert "workstreams/benchmark_v1/reports/method-freeze-v0.4.json" not in integration_paths


def test_committed_integration_report_is_source_and_config_bound() -> None:
    if not REPORT_PATH.is_file():
        pytest.skip("source-bound report is generated only after implementation enters main")
    report = _load(REPORT_PATH)

    assert report["schema_version"] == REPORT_SCHEMA
    assert report["status"] == "rl_current_contract_integration_passed_selection_failed"
    assert report["failed_checks"] == []
    assert report["source_commit"] == report["origin_main_commit"]
    assert report["source_tree_clean_during_audit"] is True
    assert report["status_config_sha256"] == hashlib.sha256(STATUS_PATH.read_bytes()).hexdigest()
    assert report["benchmark_claim_allowed"] is False
    assert report["formal_results_present"] is False
