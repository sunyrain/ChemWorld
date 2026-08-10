from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import ClassVar

import pytest
import scripts.run_work_ii_campaign_pilot as campaign_runner
import scripts.run_work_ii_formal_matrix as formal_runner

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_blind import BLIND_EVALUATOR_VERSION
from chemworld.eval.work_ii_cost import build_formal_cost_contract
from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    FORMAL_SNAPSHOT_STAGES,
    DuplicateFormalCellError,
    InvalidFormalCellReceiptError,
    ProviderAttemptLimitError,
    WorkIIFormalCellStore,
    authorize_formal_preflight,
    build_checkpoint_contract,
    build_formal_preflight,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _fake_blind_plan(cell: dict[str, object]) -> dict[str, object]:
    target_digests = {
        "observed_incumbent": "a" * 64,
        "participant_final_recommendation": "b" * 64,
    }
    targets = [
        {"target": target, "action_plan_sha256": digest}
        for target, digest in target_digests.items()
    ]
    executions = []
    for target, digest in target_digests.items():
        for replicate_index in range(1, 4):
            executions.append(
                {
                    "target": target,
                    "replicate_index": replicate_index,
                    "action_plan_sha256": digest,
                    "paired_noise_id_sha256": f"paired-{replicate_index}",
                    "observation_seed": replicate_index,
                    "observation_noise_namespace": f"namespace-{replicate_index}",
                }
            )
    plan: dict[str, object] = {
        "schema_version": BLIND_EVALUATOR_VERSION,
        "cell_key_sha256": cell["cell_key_sha256"],
        "evaluator_provider_call_count": 0,
        "participant_operation_denominator_impact": 0,
        "participant_feedback_allowed": False,
        "targets": targets,
        "executions": executions,
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _authorized_manifest() -> dict[str, object]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    return authorize_formal_preflight(
        manifest,
        qualification_receipt_sha256="a" * 64,
        preregistration_freeze_receipt_sha256="b" * 64,
        formal_cost_contract_sha256="c" * 64,
    )


def _formal_cost_contract(manifest: dict[str, object]) -> dict[str, object]:
    return build_formal_cost_contract(
        ROOT,
        manifest,
        formal_currency_ceiling_usd=20.0,
        pricing_source="https://api-docs.deepseek.com/quick_start/pricing",
        pricing_observed_at="2026-08-10T12:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )


class _FakeFormalCellProcess:
    fail_once_keys: ClassVar[set[str]] = set()
    partial_once_keys: ClassVar[set[str]] = set()
    spawn_fail_once_keys: ClassVar[set[str]] = set()
    launched_keys: ClassVar[list[str]] = []

    def __init__(self, command, **kwargs) -> None:
        del kwargs
        key = command[command.index("--formal-cell-key") + 1]
        self.launched_keys.append(key)
        if key in self.spawn_fail_once_keys:
            self.spawn_fail_once_keys.remove(key)
            raise OSError("simulated provider process launch failure")
        output = Path(command[command.index("--output") + 1])
        manifest_path = Path(command[command.index("--formal-manifest") + 1])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        cell = next(row for row in manifest["cells"] if row["cell_key_sha256"] == key)
        if key in self.fail_once_keys:
            self.fail_once_keys.remove(key)
            self.return_code = 2
            return
        if key in self.partial_once_keys:
            self.partial_once_keys.remove(key)
            output.mkdir(parents=True)
            (output / "trajectory.jsonl").write_text("{}\n{", encoding="utf-8")
            self.return_code = 2
            return
        output.mkdir(parents=True)
        arm = cell["prior_arm"]
        completed = arm == "opaque"
        operation_attempt_count = 4 if completed else 2 if arm == "aligned_nominal" else 0
        summary = {
            "formal_result": True,
            "formal_cell": cell,
            "completed": completed,
            "analysis": {"operation_attempt_count": operation_attempt_count},
            "method_resources": {"provider_session_count": 1},
            "provider_receipts": [{"session_id": "test"}],
            "exact_replay": {"verified": completed},
            "qualification": {"passed": completed},
        }
        if completed:
            plan = _fake_blind_plan(cell)
            plan_path = output / "blind_evaluation_plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            summary["blind_evaluation_plan"] = {
                "sha256": file_sha256(plan_path),
                "plan_sha256": plan["plan_sha256"],
            }
        (output / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
        (output / "report.json").write_text("{}", encoding="utf-8")
        if operation_attempt_count:
            (output / "trajectory.jsonl").write_text("{}\n", encoding="utf-8")
        self.return_code = 0 if completed else 1

    def wait(self) -> int:
        return self.return_code

    def poll(self) -> int:
        return self.return_code


def test_formal_preflight_materializes_exact_outcome_blind_denominators() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)

    assert report["status"] == "passed_execution_blocked"
    assert report["formal_result"] is False
    assert report["formal_execution_allowed"] is False
    assert report["errors"] == []
    assert validate_formal_preflight(report) == []
    assert report["expected_counts"] == {
        "tasks": 5,
        "independent_task_world_clusters": 25,
        "participant_cells": 75,
        "provider_sessions": 75,
        "provider_attempts_initial_planned": 75,
        "provider_attempts_hard_cap": 150,
        "provider_repeats_per_cell": 1,
        "complete_experiments": 300,
        "belief_checkpoints": 300,
        "checkpoint_held_out_queries": 1200,
        "checkpoint_held_out_query_metrics": 4080,
        "evaluator_truth_executions": 100,
        "evaluator_truth_query_metrics": 340,
        "participant_final_recommendations": 75,
        "blind_validation_targets": 150,
        "blind_validation_executions": 450,
    }
    assert len(report["blocking_requirements"]) == 5
    source_paths = {row["path"] for row in report["source_bindings"]}
    assert "src/chemworld/eval/work_ii_confirmatory.py" in source_paths
    assert "scripts/analyze_work_ii_confirmatory.py" in source_paths
    assert report["held_out_evaluator_contract"] == {
        "truth_unit": "task_x_world_cluster_x_registered_query",
        "queries_per_task_world_cluster": 4,
        "public_matrix_truth_execution_count": 100,
        "public_matrix_truth_query_metric_count": 340,
        "shared_across_prior_arms_and_checkpoints": True,
        "one_frozen_complete_experiment_per_query": True,
        "keyed_observation_coordinate_per_query": True,
        "exact_replay_required": True,
        "failed_truth_executions_retained_without_replacement": True,
        "evaluator_provider_calls": 0,
        "participant_feedback_from_truth_evaluator": False,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
        "frozen_unregistered_controls": {
            "reaction-to-crystallization": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
            },
            "reaction-to-distillation": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
                "evaporation_temperature_K": 332.5,
                "evaporation_duration_s": 900.0,
                "transfer_fraction": 0.77,
            },
            "partition-discovery": {"solvent_volume_L": 0.02},
            "reaction-safety-constrained": {"stirring_speed_rpm": 675.0},
        },
        "query_field_aliases": {
            "partition-discovery": {
                "aqueous_phase_volume_L": "aqueous_volume_L"
            }
        },
    }


def test_formal_schedule_is_task_world_arm_ordered_and_unique() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    cells = report["cells"]

    assert [cell["prior_arm"] for cell in cells[:3]] == list(FORMAL_ARMS)
    assert {cell["world_cluster_id"] for cell in cells[:3]} == {
        "work-ii-public-01-01"
    }
    assert cells[0]["world_seed"] == 672326802
    assert cells[-1]["world_seed"] == 930008953
    assert len({cell["cell_id"] for cell in cells}) == 75
    assert len({cell["cell_key_sha256"] for cell in cells}) == 75
    assert all(cell["provider_session_limit"] == 1 for cell in cells)
    assert all(cell["provider_attempt_limit"] == 2 for cell in cells)
    assert all(cell["world_split"] == "public_formal" for cell in cells)
    assert all(cell["participant_final_recommendation_count"] == 1 for cell in cells)
    assert all(cell["blind_validation_execution_count"] == 6 for cell in cells)
    assert all(
        cell["terminal_states"] == ["completed", "right_censored", "failed"]
        for cell in cells
    )
    assert not any("private" in cell for cell in cells)


def test_formal_preflight_rejects_rehashed_cross_split_cell() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    tampered = deepcopy(report)
    cell = tampered["cells"][0]
    cell["world_split"] = "private_confirmation"
    cell["world_seed"] = 2_000_000_001
    cell["cell_key_sha256"] = canonical_json_sha256(
        {key: value for key, value in cell.items() if key != "cell_key_sha256"}
    )
    tampered["preflight_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in tampered.items()
            if key != "preflight_sha256"
        }
    )
    errors = validate_formal_preflight(tampered)
    assert "formal preflight contains a cross-split world identity" in errors
    assert "formal preflight cell crossed the public/private boundary" in errors


def test_all_formal_task_configs_use_neutral_checkpoint_ids() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    for binding in report["task_bindings"]:
        config_path = ROOT / binding["campaign_config"]["path"]
        config = json.loads(config_path.read_text(encoding="utf-8"))
        contract = build_checkpoint_contract(config, "opaque")
        assert tuple(contract["snapshot_stages"]) == FORMAL_SNAPSHOT_STAGES
        assert contract["physical_experiment_selection_authority"] == "participant"


def test_formal_preflight_self_hash_fails_closed() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    tampered = deepcopy(report)
    tampered["cells"][0]["world_seed"] += 1
    assert "formal preflight self-hash mismatch" in validate_formal_preflight(tampered)


def test_formal_cell_store_is_write_once_and_missing_only_resumable(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    first = manifest["cells"][0]
    first_key = first["cell_key_sha256"]

    store.record_infrastructure_failure(first_key, TimeoutError("provider timeout"))
    before = store.audit()
    assert before["terminal_count"] == 0
    assert before["infrastructure_attempt_count"] == 1
    assert len(store.pending_cells(resume=True)) == 75

    store.write_terminal(
        first_key,
        state="completed",
        reason_code="scientific_completed_qualified_campaign",
        result={"summary_sha256": "a" * 64, "exact_replay": True},
    )
    with pytest.raises(DuplicateFormalCellError):
        store.write_terminal(
            first_key,
            state="completed",
            reason_code="scientific_completed_qualified_campaign",
            result={"summary_sha256": "b" * 64, "exact_replay": True},
        )
    with pytest.raises(DuplicateFormalCellError):
        store.pending_cells(resume=False)
    pending = store.pending_cells(resume=True)
    assert len(pending) == 74
    assert all(cell["cell_key_sha256"] != first_key for cell in pending)
    assert store.load_terminal(first_key)["result"]["exact_replay"] is True
    after = store.audit()
    assert after["state_counts"]["completed"] == 1
    assert after["recovered_infrastructure_failure_count"] == 1


def test_formal_cell_store_preserves_right_censored_and_failed_cells(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    censored, failed = manifest["cells"][:2]
    store.write_terminal(
        censored["cell_key_sha256"],
        state="right_censored",
        reason_code="method_right_censored_provider_failure_after_operation",
        result={"operation_attempt_count": 3, "last_checkpoint": "pre_evidence"},
    )
    store.write_terminal(
        failed["cell_key_sha256"],
        state="failed",
        reason_code="method_failed_unscorable_before_first_operation",
        result={"operation_attempt_count": 0, "primary_improvement": 0.0},
    )
    audit = store.audit()
    assert audit["state_counts"] == {
        "completed": 0,
        "failed": 1,
        "right_censored": 1,
    }
    assert audit["terminal_count"] == 2
    assert len(audit["missing_cell_key_sha256"]) == 73


def test_formal_cell_store_enforces_two_launch_provider_attempt_cap(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    cell = manifest["cells"][0]
    key = cell["cell_key_sha256"]
    store.record_provider_attempt_launch(key, attempt_id="attempt-1")
    store.record_provider_attempt_launch(key, attempt_id="attempt-2")
    audit = store.audit()
    assert audit["provider_attempt_count"] == 2
    assert audit["provider_attempt_counts_by_cell_key_sha256"] == {key: 2}
    with pytest.raises(ProviderAttemptLimitError, match="exhausted provider attempt cap"):
        store.record_provider_attempt_launch(key, attempt_id="attempt-3")
    with pytest.raises(ProviderAttemptLimitError, match="missing formal cells exhausted"):
        store.pending_cells(resume=True)


def test_formal_cell_store_fails_closed_on_receipt_tampering(tmp_path: Path) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    cell = manifest["cells"][0]
    receipt = store.write_terminal(
        cell["cell_key_sha256"],
        state="completed",
        reason_code="scientific_completed_qualified_campaign",
        result={"exact_replay": True},
    )
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["result"]["exact_replay"] = False
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    audit = store.audit()
    assert audit["terminal_count"] == 0
    assert audit["invalid_receipts"] == [receipt.as_posix()]
    with pytest.raises(InvalidFormalCellReceiptError):
        store.pending_cells(resume=True)


def test_campaign_cell_formal_mode_requires_exact_authorized_binding(
    tmp_path: Path,
) -> None:
    blocked = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    cell = blocked["cells"][0]
    blocked_path = tmp_path / "blocked.json"
    blocked_path.write_text(json.dumps(blocked), encoding="utf-8")
    args = argparse.Namespace(
        formal_manifest=blocked_path,
        formal_cell_key=cell["cell_key_sha256"],
        allow_formal_execution=True,
        world_seed=cell["world_seed"],
        prior_arm=cell["prior_arm"],
    )
    with pytest.raises(RuntimeError, match="does not authorize"):
        campaign_runner._formal_cell_context(
            args,
            config_path=ROOT / cell["campaign_config_path"],
        )

    authorized = _authorized_manifest()
    authorized_cell = authorized["cells"][0]
    authorized_path = tmp_path / "authorized.json"
    authorized_path.write_text(json.dumps(authorized), encoding="utf-8")
    args.formal_manifest = authorized_path
    args.formal_cell_key = authorized_cell["cell_key_sha256"]
    context = campaign_runner._formal_cell_context(
        args,
        config_path=ROOT / authorized_cell["campaign_config_path"],
    )
    assert context is not None
    assert context[1]["cell_id"] == authorized_cell["cell_id"]
    args.world_seed += 1
    with pytest.raises(RuntimeError, match="world seed"):
        campaign_runner._formal_cell_context(
            args,
            config_path=ROOT / authorized_cell["campaign_config_path"],
        )


def test_manifest_executor_terminalizes_all_cells_without_arm_replacement(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    report = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert report["status"] == "all_cells_terminal"
    assert report["terminal_count"] == 75
    assert report["state_counts"] == {
        "completed": 25,
        "failed": 25,
        "right_censored": 25,
    }
    assert len(_FakeFormalCellProcess.launched_keys) == 75
    assert len(set(_FakeFormalCellProcess.launched_keys)) == 75
    cost_ledger = json.loads(
        (output / "formal_cost_ledger.json").read_text(encoding="utf-8")
    )
    assert cost_ledger["provider_attempt_count"] == 75
    assert cost_ledger["reserved_cost_usd"] == 7.74144
    assert cost_ledger["within_ceiling"] is True
    assert report["formal_cost_ledger_sha256"] == cost_ledger[
        "formal_cost_ledger_sha256"
    ]


def test_manifest_executor_rejects_blocked_preflight_before_creating_output(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = tmp_path / "formal-output"
    with pytest.raises(RuntimeError, match="does not authorize"):
        formal_runner.execute_manifest(
            manifest=manifest,
            manifest_path=manifest_path,
            output_root=output,
            progress_path=tmp_path / "progress.jsonl",
            resume=False,
            cell_runner=tmp_path / "fake-cell-runner.py",
        )
    assert not output.exists()


def test_formal_execute_requires_preregistration_freeze_receipt(tmp_path: Path) -> None:
    args = argparse.Namespace(
        check=False,
        output=formal_runner.DEFAULT_PREFLIGHT,
        manifest=tmp_path / "manifest.json",
        output_root=tmp_path / "output",
        qualification_receipt=tmp_path / "qualification.json",
        preregistration_freeze_receipt=None,
        formal_currency_ceiling_usd=1.0,
        progress_file=tmp_path / "progress.jsonl",
        allow_formal_execution=True,
        resume=False,
    )
    with pytest.raises(RuntimeError, match="--preregistration-freeze-receipt"):
        formal_runner._run_execute(args)


def test_manifest_executor_never_replaces_unfinalized_partial_trajectory(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    partial_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = {partial_key}
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    report = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert report["status"] == "all_cells_terminal"
    assert report["terminal_count"] == 75
    assert report["infrastructure_failure_count_this_attempt"] == 0
    assert report["state_counts"]["right_censored"] == 26
    assert _FakeFormalCellProcess.launched_keys.count(partial_key) == 1
    receipt = json.loads(
        (output / "store" / "terminal_receipts" / f"{partial_key}.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["state"] == "right_censored"
    evidence = receipt["result"]["unfinalized_trajectory_evidence"]
    assert evidence["trajectory_byte_count"] > 0
    assert {key: evidence[key] for key in evidence if key != "trajectory_byte_count"} == {
        "nonempty_line_count": 2,
        "valid_json_line_count": 1,
        "malformed_or_partial_line_count": 1,
    }


def test_manifest_executor_records_process_spawn_failure_and_resumes_once(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    failed_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = {failed_key}
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    first = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert first["terminal_count"] == 2
    assert first["infrastructure_failure_count_this_attempt"] == 1
    assert first["missing_cell_count"] == 73
    second = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=True,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert second["status"] == "all_cells_terminal"
    assert second["terminal_count"] == 75
    assert _FakeFormalCellProcess.launched_keys.count(failed_key) == 2
    audit = json.loads((output / "store_audit.json").read_text(encoding="utf-8"))
    assert audit["provider_attempt_count"] == 76
    assert audit["provider_attempt_counts_by_cell_key_sha256"][failed_key] == 2


def test_manifest_executor_resumes_only_missing_cells_after_triplet_failure(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    failed_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = {failed_key}
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    first = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert first["status"] == "infrastructure_incomplete_missing_only_resume_required"
    assert first["terminal_count"] == 2
    assert first["missing_cell_count"] == 73
    assert len(_FakeFormalCellProcess.launched_keys) == 3

    second = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=True,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert second["status"] == "all_cells_terminal"
    assert second["terminal_count"] == 75
    assert len(_FakeFormalCellProcess.launched_keys) == 76
    assert _FakeFormalCellProcess.launched_keys.count(manifest["cells"][0]["cell_key_sha256"]) == 1
    assert _FakeFormalCellProcess.launched_keys.count(manifest["cells"][1]["cell_key_sha256"]) == 1
    assert _FakeFormalCellProcess.launched_keys.count(failed_key) == 2
