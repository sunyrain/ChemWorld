from __future__ import annotations

from pathlib import Path

from scripts.audit_benchmark_v1_gap import build_audit

ROOT = Path(__file__).resolve().parents[1]


def test_gap_audit_distinguishes_pipeline_readiness_from_scientific_readiness() -> None:
    report = build_audit(ROOT, generalization_report=None)
    checks = {check["check_id"]: check for check in report["checks"]}

    assert report["schema_version"] == "chemworld-benchmark-v1-gap-audit-0.1"
    assert report["release_recommendation"] == "candidate_only_do_not_submit_final_claim"
    assert checks["six_explicit_serious_tasks"]["passed"] is True
    assert checks["per_task_reporting"]["passed"] is True
    assert checks["public_observation_leakage_tests"]["passed"] is True
    assert checks["release_contract_hashes_current"]["passed"] is False
    assert checks["frozen_checker_verifies_release_manifest"]["passed"] is True
    assert checks["reinforcement_learning_baseline"]["passed"] is False
    assert checks["real_llm_agent_baseline"]["passed"] is False


def test_gap_audit_is_deterministic_without_optional_run_artifact() -> None:
    left = build_audit(ROOT, generalization_report=None)
    right = build_audit(ROOT, generalization_report=None)
    assert left == right
