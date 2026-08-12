from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest
import scripts.run_work_ii_resource_calibration as calibration_runner

import chemworld.eval.work_ii_resource_calibration as calibration_module
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_c2_admission import build_c2_source_binding
from chemworld.eval.work_ii_resource_calibration import (
    RESOURCE_CALIBRATION_ARMS,
    build_resource_calibration_authorization,
    build_resource_calibration_readiness,
    build_resource_calibration_summary,
    empty_resource_calibration_summary,
    resource_calibration_summary_sha256,
    validate_resource_calibration_authorization,
    validate_resource_calibration_manifest,
    validate_resource_calibration_readiness,
    validate_resource_calibration_summary,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.1.json"
RUNNER = ROOT / "scripts/run_work_ii_resource_calibration.py"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture
def repo_tmp_path():
    path = Path(tempfile.mkdtemp(prefix=".pytest-resource-calibration-", dir=ROOT))
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _future_manifest(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    manifest = _manifest()
    for pattern in manifest["patterns"]:
        rounds = pattern["rounds"]
        config = json.loads(
            (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(
                encoding="utf-8"
            )
        )
        config["pilot_id"] = f"future-calibration-{rounds}"
        config["task_id"] = f"future-{pattern['locus'].lower()}-{rounds}"
        config["world_seed"] = rounds
        config["campaign"]["complete_experiments"] = rounds
        config["campaign"]["checkpoint_complete_experiments"] = (
            pattern["checkpoint_complete_experiments"]
        )
        config["method_resources"]["complete_experiment_limit"] = rounds
        config["method_resources"]["checkpoint_complete_experiments"] = (
            pattern["checkpoint_complete_experiments"][1:]
        )
        config_path = tmp_path / f"campaign-{rounds}.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        pattern["representative_task_status"] = "frozen"
        pattern["task_id"] = config["task_id"]
        pattern["world_seed"] = rounds
        pattern["task_specific_resource_formula_frozen"] = True
        pattern["campaign_config_binding"] = {
            "path": config_path.relative_to(ROOT).as_posix(),
            "sha256": canonical_json_sha256(config),
            "hash_kind": "canonical_json_sha256",
        }
    manifest["status"] = "ready_authorization_blocked"
    manifest["protocol_manifest_binding"] = {
        "path": MANIFEST.relative_to(ROOT).as_posix(),
        "sha256": file_sha256(MANIFEST),
        "hash_kind": "file_sha256",
    }
    manifest["c2_source_binding"] = build_c2_source_binding(ROOT)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, manifest


def _passed_cell(pattern: dict[str, object], arm: str) -> dict[str, object]:
    rounds = int(pattern["rounds"])
    return {
        "rounds": rounds,
        "locus": pattern["locus"],
        "task_id": pattern["task_id"],
        "world_seed": pattern["world_seed"],
        "arm": arm,
        "status": "passed",
        "terminal": True,
        "calibration_passed": True,
        "complete_experiments": rounds,
        "unique_recipe_count": rounds - 2,
        "exact_repeat_count": 2,
        "operation_attempts": rounds * 7,
        "committed_operations": rounds * 6,
        "checkpoint_complete_experiments": pattern[
            "checkpoint_complete_experiments"
        ],
        "checkpoint_stages": [f"checkpoint-{index}" for index in range(5)],
        "typed_checkpoints_valid": True,
        "final_recommendation_committed": True,
        "lifecycle_closed": True,
        "exact_replay_verified": True,
        "resource_ledgers_reconciled": True,
        "process_resources": {
            "process_time_used_s": rounds * 100.0,
            "required_stage_max_s": rounds * 80.0,
            "repeat_allowance_s": rounds * 20.0,
            "protected_closeout_reserve_s": rounds * 10.0,
            "protected_closeout_reserve_consumed_s": 0.0,
            "reserve_consumption_by_operation_class": {},
        },
        "provider_resources": {
            "input_tokens": rounds * 100,
            "cache_hit_input_tokens": rounds * 50,
            "uncached_input_tokens": rounds * 50,
            "output_tokens": rounds * 10,
            "provider_elapsed_s": rounds * 2.0,
            "provider_attempts": 1,
            "mcp_recovery_count": 0,
            "mcp_error_count": 0,
            "observed_currency_usd": rounds / 1000,
        },
        "failure_counts": {
            "resource_rejection": 0,
            "unsafe_outcome": 0,
            "dynamic_physical_failure": 0,
            "provider_error": 0,
            "platform_execution_failure": 0,
        },
    }


def _passed_summary(manifest: dict[str, object], source_commit: str) -> dict[str, object]:
    cells = [
        _passed_cell(pattern, arm)
        for pattern in manifest["patterns"]
        for arm in RESOURCE_CALIBRATION_ARMS
    ]
    patterns = [
        {
            "rounds": pattern["rounds"],
            "locus": pattern["locus"],
            "task_id": pattern["task_id"],
            "world_seed": pattern["world_seed"],
            "cell_count": 3,
            "cells_terminal": 3,
            "complete_experiments": int(pattern["rounds"]) * 3,
            "belief_checkpoints": 15,
            "triplet_passed": True,
            "platform_defect_detected": False,
        }
        for pattern in manifest["patterns"]
    ]
    proposals = []
    for pattern in manifest["patterns"]:
        rounds = int(pattern["rounds"])
        proposals.append(
            {
                "rounds": rounds,
                "locus": pattern["locus"],
                "observed_maxima": {
                    "operation_attempts": rounds * 7,
                    "exact_repeat_count": 2,
                    "process_time_used_s": rounds * 100.0,
                    "input_tokens": rounds * 100,
                    "uncached_input_tokens": rounds * 50,
                    "output_tokens": rounds * 10,
                    "provider_elapsed_s": rounds * 2.0,
                    "observed_currency_usd": rounds / 1000,
                },
                "protected_closeout_reserve_enforced": True,
                "proposed_hard_caps": {
                    "operation_attempt_limit": rounds * 7,
                    "protected_closeout_operation_reserve": rounds * 2,
                    "maximum_exact_repeats": 2,
                    "process_time_limit_s": rounds * 110.0,
                    "protected_closeout_reserve_s": rounds * 10.0,
                    "input_token_limit": rounds * 100,
                    "uncached_input_token_limit": rounds * 50,
                    "output_token_limit": rounds * 10,
                    "provider_wall_time_limit_s": rounds * 2.0,
                    "currency_ceiling_usd": rounds / 1000,
                },
            }
        )
    summary = {
        "schema_version": "chemworld-work-ii-resource-calibration-summary-0.1",
        "status": "passed",
        "formal_result": False,
        "provider_calls_executed": 9,
        "manifest_sha256": canonical_json_sha256(manifest),
        "source_commit": source_commit,
        "c2_source_binding": build_c2_source_binding(ROOT),
        "expected_denominators": manifest["expected_denominators"],
        "observed_denominators": {
            "pattern_triplets_started": 3,
            "pattern_triplets_terminal": 3,
            "cells_started": 9,
            "cells_terminal": 9,
            "complete_experiments": 90,
            "belief_checkpoints": 45,
            "provider_sessions": 9,
            "participant_model_calls": 9,
        },
        "pattern_summaries": patterns,
        "cell_summaries": cells,
        "all_failures": [],
        "resource_card_proposals": proposals,
        "calibration_passed": True,
        "method_qualification_may_be_authorized": True,
    }
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    return summary


def test_calibration_manifest_freezes_denominators_and_retains_as_gate() -> None:
    manifest = _manifest()
    assert validate_resource_calibration_manifest(ROOT, manifest) == []
    assert manifest["status"] == "not_ready_fail_closed"
    assert [row["rounds"] for row in manifest["patterns"]] == [8, 10, 12]
    assert manifest["expected_denominators"] == {
        "pattern_triplets": 3,
        "cells": 9,
        "complete_experiments": 90,
        "belief_checkpoints": 45,
        "accepted_provider_sessions": 9,
        "accepted_participant_model_calls": 9,
    }
    twelve = manifest["patterns"][2]
    assert twelve["locus"] == "A_S"
    assert twelve["task_id"] is None
    assert twelve["campaign_config_binding"] is None
    assert twelve["representative_task_status"] == "pending_two_terminal_AS_admissions"
    assert manifest["authorization_gate"]["twelve_round_proxy_substitution_forbidden"] is True


def test_calibration_readiness_is_deterministic_zero_call_and_not_ready() -> None:
    first = build_resource_calibration_readiness(ROOT, MANIFEST)
    second = build_resource_calibration_readiness(ROOT, MANIFEST)
    assert first == second
    assert validate_resource_calibration_readiness(first) == []
    assert first["status"] == "not_ready_fail_closed"
    assert first["provider_execution_allowed"] is False
    assert first["provider_calls_executed"] == 0
    assert first["method_qualification_may_be_authorized"] is False
    assert first["missing_pattern_rounds"] == [10, 12]


def test_future_passed_summary_is_the_only_unlock_path(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    monkeypatch.setattr(calibration_module, "git_worktree_dirty", lambda _root: False)
    assert validate_resource_calibration_manifest(ROOT, manifest) == []
    before = build_resource_calibration_readiness(ROOT, manifest_path)
    assert before["status"] == "ready_authorization_blocked"
    assert before["method_qualification_may_be_authorized"] is False
    summary = _passed_summary(manifest, before["source_commit"])
    summary_path = manifest_path.parent / "summary.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    after = build_resource_calibration_readiness(
        ROOT, manifest_path, summary_path=summary_path
    )
    assert validate_resource_calibration_readiness(after) == []
    assert after["status"] == "calibration_passed_method_qualification_eligible"
    assert after["method_qualification_may_be_authorized"] is True


def test_readiness_accepts_report_only_commit_but_rejects_c2_material_drift(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    tested_commit = "a" * 40
    current_commit = "b" * 40
    binding = build_c2_source_binding(ROOT)
    binding["tested_commit"] = tested_commit
    summary = _passed_summary(manifest, tested_commit)
    summary["c2_source_binding"] = binding
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    summary_path = repo_tmp_path / "summary.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    monkeypatch.setattr(calibration_module, "git_worktree_dirty", lambda _root: False)
    monkeypatch.setattr(calibration_module, "git_source_commit", lambda _root: current_commit)
    monkeypatch.setattr(
        "chemworld.eval.work_ii_c2_admission.git_source_commit",
        lambda _root: current_commit,
    )
    monkeypatch.setattr(
        "chemworld.eval.work_ii_c2_admission.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0),
    )

    report_only = build_resource_calibration_readiness(
        ROOT, manifest_path, summary_path=summary_path
    )
    assert report_only["calibration_summary_errors"] == []
    assert report_only["method_qualification_may_be_authorized"] is True

    summary["c2_source_binding"]["material_tree"]["sha256"] = "0" * 64
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    drifted = build_resource_calibration_readiness(
        ROOT, manifest_path, summary_path=summary_path
    )
    assert any(
        "protected material tree changed" in error
        for error in drifted["calibration_summary_errors"]
    )
    assert drifted["method_qualification_may_be_authorized"] is False


def test_passed_summary_rejects_failure_and_resource_card_tampering(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, manifest = _future_manifest(repo_tmp_path)
    summary = _passed_summary(manifest, "future-clean-source")
    assert validate_resource_calibration_summary(summary, manifest=manifest) == []
    tampered = deepcopy(summary)
    tampered["cell_summaries"][0]["failure_counts"]["provider_error"] = 1
    tampered["all_failures"] = [{"class": "provider_error"}]
    tampered["summary_sha256"] = resource_calibration_summary_sha256(tampered)
    errors = validate_resource_calibration_summary(tampered, manifest=manifest)
    assert any("platform failures" in error for error in errors)
    assert "passed resource calibration summary contains failures" in errors


def test_authorization_and_executor_are_usable_after_real_gate_inputs(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, _manifest = _future_manifest(repo_tmp_path)
    monkeypatch.setattr(calibration_module, "git_worktree_dirty", lambda _root: False)
    authorization = build_resource_calibration_authorization(
        ROOT,
        manifest_path,
        currency_ceiling_usd=100.0,
        approved_at="2026-08-12T00:00:00+08:00",
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-12T00:00:00+08:00",
        cache_hit_input_usd_per_million=0.01,
        cache_miss_input_usd_per_million=0.1,
        output_usd_per_million=0.2,
    )
    assert validate_resource_calibration_authorization(
        ROOT, authorization, manifest_path
    ) == []
    assert authorization["all_infrastructure_resumes"]["provider_process_attempts"] == 18
    assert authorization["runtime_enforcement"][
        "affected_triplet_restarts_from_first_cell"
    ] is True
    source = RUNNER.read_text(encoding="utf-8")
    assert "provider executor is not implemented" not in source
    assert calibration_runner.execute_calibration is not None


def test_summary_aggregator_invalidates_platform_defect(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, manifest = _future_manifest(repo_tmp_path)
    summary = build_resource_calibration_summary(
        manifest, [], source_commit="future-clean-source"
    )
    assert summary["status"] == "invalidated_platform_defect"
    assert summary["calibration_passed"] is False
    assert summary["method_qualification_may_be_authorized"] is False


def test_unexecuted_summary_template_cannot_claim_results() -> None:
    summary = empty_resource_calibration_summary(_manifest())
    assert validate_resource_calibration_summary(summary) == []
    assert summary["status"] == "not_executed"
    assert summary["observed_denominators"]["cells_started"] == 0
    tampered = deepcopy(summary)
    tampered["calibration_passed"] = True
    tampered["summary_sha256"] = resource_calibration_summary_sha256(tampered)
    assert "unexecuted resource calibration summary claims results" in (
        validate_resource_calibration_summary(tampered)
    )


def test_runner_rejects_provider_execution_before_creating_output(tmp_path: Path) -> None:
    output = tmp_path / "calibration"
    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--execute",
            "--manifest",
            str(MANIFEST),
            "--output",
            str(output),
            "--allow-provider-execution",
            "--authorization",
            str(tmp_path / "authorization.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "unresolved pattern rounds: 10,12" in result.stderr
    assert not output.exists()


def test_launch_decision_brief_is_explicitly_stale() -> None:
    brief = (
        ROOT
        / "workstreams/flagship_tasks/reports/work-ii-formal-launch-decision-brief.md"
    ).read_text(encoding="utf-8")
    assert "STALE — NOT AUTHORIZATION-ELIGIBLE" in brief
    assert "No calibration or method-qualification provider call is currently authorized" in brief
    assert "12 / 12" not in brief
    assert "Operation-attempt hard cap | 84" not in brief
