from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest

import chemworld.eval.work_ii_private_execution as private_execution
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_private import WORK_II_PRIVATE_CELL_VERSION
from chemworld.eval.work_ii_private_execution import (
    build_private_execution_authorization,
    build_private_execution_manifest,
    execute_private_manifest,
    validate_private_execution_authorization,
    validate_private_execution_manifest,
    validate_private_execution_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _preflight() -> dict[str, object]:
    design = _load(DESIGN)
    cells: list[dict[str, object]] = []
    for task_index, task in enumerate(design["tasks"], start=1):
        task_id = str(task["task_id"])
        relative = str(task["campaign_config"])
        for world_index in range(1, 6):
            cluster_id = f"private-{task_index:02d}-{world_index:02d}"
            for arm_index, arm in enumerate(
                ("opaque", "aligned_nominal", "misindexed_nominal"), start=1
            ):
                cell: dict[str, object] = {
                    "schema_version": WORK_II_PRIVATE_CELL_VERSION,
                    "schedule_index": len(cells) + 1,
                    "cell_id": f"{cluster_id}-arm-{arm_index:02d}",
                    "world_cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_index": world_index,
                    "world_seed": 2_000_000_000 + task_index * 100 + world_index,
                    "world_split": "private_confirmation",
                    "prior_arm": arm,
                    "campaign_config_path": relative,
                    "campaign_config_sha256": file_sha256(ROOT / relative),
                    "checkpoint_contract_sha256": "1" * 64,
                    "participant_execution_contract_sha256": "2" * 64,
                    "law_summary_evaluation_contract_sha256": "3" * 64,
                    "private_confirmation_contract_sha256": "4" * 64,
                    "complete_experiment_count": 8,
                    "belief_checkpoint_count": 5,
                    "held_out_query_count_per_snapshot": 4,
                    "held_out_query_metric_count_per_snapshot": 4,
                    "provider_session_limit": 1,
                    "provider_attempt_limit": 2,
                    "provider_repeat": 1,
                    "participant_final_recommendation_count": 1,
                    "blind_validation_target_count": 2,
                    "blind_replicates_per_target": 3,
                    "blind_validation_execution_count": 6,
                    "terminal_states": ["completed", "right_censored", "failed"],
                    "public_template_cell_key_sha256": "5" * 64,
                }
                cell["cell_key_sha256"] = canonical_json_sha256(cell)
                cells.append(cell)
    preflight: dict[str, object] = {
        "schema_version": "chemworld-work-ii-private-confirmation-preflight-0.1",
        "status": "passed_private_execution_blocked",
        "formal_result": False,
        "private_confirmation_result": False,
        "private_execution_allowed": False,
        "blocking_requirements": ["authorization pending"],
        "provider_calls_executed": 0,
        "public_formal_manifest_sha256": "6" * 64,
        "public_confirmatory_analysis_sha256": "7" * 64,
        "design_sha256": "8" * 64,
        "private_seal_commitment_sha256": "9" * 64,
        "private_identity_schedule_sha256": "a" * 64,
        "expected_counts": {
            "tasks": 5,
            "independent_task_world_clusters": 25,
            "participant_cells": 75,
            "complete_experiments": 600,
            "belief_checkpoints": 375,
            "provider_sessions": 75,
            "provider_attempts_initial_planned": 75,
            "provider_attempts_hard_cap": 150,
            "evaluator_truth_executions": 100,
            "blind_validation_executions": 450,
        },
        "cells": cells,
    }
    preflight["preflight_sha256"] = canonical_json_sha256(preflight)
    return preflight


@pytest.fixture
def repo_tmp_path():
    path = Path(tempfile.mkdtemp(prefix=".pytest-private-execution-", dir=ROOT))
    try:
        yield path
    finally:
        shutil.rmtree(path)


@pytest.fixture
def private_output_root():
    path = Path(tempfile.mkdtemp(prefix="pytest-private-execution-", dir=ROOT / "runs/private"))
    shutil.rmtree(path)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _authorization(preflight: dict[str, object]) -> dict[str, object]:
    paths = sorted({str(cell["campaign_config_path"]) for cell in preflight["cells"]})
    contracts = []
    for relative in paths:
        config = _load(ROOT / relative)
        task_cells = [
            cell for cell in preflight["cells"] if cell["campaign_config_path"] == relative
        ]
        contracts.append(
            {
                "task_id": config["task_id"],
                "campaign_config_path": relative,
                "campaign_config_sha256": file_sha256(ROOT / relative),
                "participant_cell_count": len(task_cells),
                "provider_attempt_hard_cap": len(task_cells) * 2,
                "per_attempt_token_caps": {},
                "per_attempt_cost_cap_usd": 0.01,
            }
        )
    authorization: dict[str, object] = {
        "schema_version": "chemworld-work-ii-private-execution-authorization-0.1",
        "status": "authorized_private_execution_only",
        "formal_result": False,
        "private_confirmation_result": False,
        "private_execution_allowed": True,
        "base_private_preflight_sha256": preflight["preflight_sha256"],
        "source_commit": "b" * 40,
        "source_tree_clean_at_authorization": True,
        "task_attempt_contracts": contracts,
        "private_currency_ceiling_usd": 100.0,
        "authorization_sha256": "pending",
    }
    authorization["authorization_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in authorization.items()
            if key != "authorization_sha256"
        }
    )
    return authorization


def test_private_execution_preflight_freezes_75_sessions_and_600_experiments() -> None:
    preflight = _preflight()
    assert validate_private_execution_preflight(ROOT, preflight) == []
    assert preflight["expected_counts"]["participant_cells"] == 75
    assert preflight["expected_counts"]["provider_sessions"] == 75
    assert preflight["expected_counts"]["complete_experiments"] == 600
    assert preflight["expected_counts"]["provider_attempts_hard_cap"] == 150
    tampered = json.loads(json.dumps(preflight))
    tampered["expected_counts"]["complete_experiments"] = 300
    tampered["preflight_sha256"] = canonical_json_sha256(
        {key: value for key, value in tampered.items() if key != "preflight_sha256"}
    )
    assert "private execution preflight denominators are not exact" in (
        validate_private_execution_preflight(ROOT, tampered)
    )


def test_private_authorization_requires_explicit_user_signoff_and_clean_release(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    preflight = _preflight()
    release_path = repo_tmp_path / "clean-release.json"
    release = {"receipt_sha256": "c" * 64}
    release_path.write_text(json.dumps(release), encoding="utf-8")
    monkeypatch.setattr(private_execution, "git_worktree_dirty", lambda _root: False)
    monkeypatch.setattr(private_execution, "git_source_commit", lambda _root: "b" * 40)
    monkeypatch.setattr(private_execution, "validate_clean_release_receipt", lambda *a, **k: [])
    common = {
        "approved_at": "2026-08-12T00:00:00+08:00",
        "pricing_source": "https://provider.example/pricing",
        "pricing_observed_at": "2026-08-12T00:00:00+08:00",
        "cache_hit_input_usd_per_million": 0.01,
        "cache_miss_input_usd_per_million": 0.1,
        "output_usd_per_million": 0.2,
        "private_currency_ceiling_usd": 1_000.0,
        "credential_rotation_confirmed_by_user": True,
        "private_one_shot_execution_confirmed_by_user": True,
    }
    with pytest.raises(ValueError, match="explicit user confirmations"):
        build_private_execution_authorization(
            ROOT,
            preflight,
            release_path,
            provider_contract_confirmed_by_user=False,
            **common,
        )
    authorization = build_private_execution_authorization(
        ROOT,
        preflight,
        release_path,
        provider_contract_confirmed_by_user=True,
        **common,
    )
    assert authorization["initial_schedule"]["provider_process_attempts"] == 75
    assert authorization["all_infrastructure_resumes"]["provider_process_attempts"] == 150
    assert validate_private_execution_authorization(ROOT, authorization, preflight) == []
    manifest = build_private_execution_manifest(preflight, authorization)
    assert validate_private_execution_manifest(manifest, preflight, authorization) == []
    tampered = json.loads(json.dumps(authorization))
    tampered["initial_schedule"]["cost_cap_usd"] = 0.0
    tampered["authorization_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in tampered.items()
            if key != "authorization_sha256"
        }
    )
    assert "private authorization provider or cost contract is invalid" in (
        validate_private_execution_authorization(ROOT, tampered, preflight)
    )


def test_private_preflight_rejects_rehashed_triplet_and_cell_contract_drift() -> None:
    for field, value in (
        ("prior_arm", "opaque"),
        ("complete_experiment_count", 7),
        ("provider_attempt_limit", 3),
    ):
        preflight = _preflight()
        preflight["cells"][1][field] = value
        preflight["cells"][1]["cell_key_sha256"] = canonical_json_sha256(
            {
                key: item
                for key, item in preflight["cells"][1].items()
                if key != "cell_key_sha256"
            }
        )
        preflight["expected_counts"] = {
            **preflight["expected_counts"],
            "complete_experiments": sum(
                int(cell["complete_experiment_count"]) for cell in preflight["cells"]
            ),
            "provider_attempts_hard_cap": sum(
                int(cell["provider_attempt_limit"]) for cell in preflight["cells"]
            ),
        }
        preflight["preflight_sha256"] = canonical_json_sha256(
            {
                key: item
                for key, item in preflight.items()
                if key != "preflight_sha256"
            }
        )
        assert validate_private_execution_preflight(ROOT, preflight)


class _FakeProcess:
    def poll(self) -> int:
        return 0

    def wait(self) -> int:
        return 0


class _SuccessfulPopen:
    def __call__(self, command: list[str], **_kwargs: object) -> _FakeProcess:
        output = Path(command[command.index("--output") + 1])
        config_path = Path(command[command.index("--config") + 1])
        config = _load(config_path)
        assert config["world_split"] == "private-eval"
        assert config_path.is_relative_to((ROOT / "runs/private").resolve())
        world_seed = int(command[command.index("--world-seed") + 1])
        arm = command[command.index("--prior-arm") + 1]
        output.mkdir(parents=True)
        (output / "trajectory.jsonl").write_text("{}\n", encoding="utf-8")
        summary = {
            "arm": arm,
            "completed": True,
            "analysis": {"complete_experiment_count": 8},
            "qualification": {"passed": True},
            "exact_replay": {"verified": True},
            "method_resources": {},
        }
        (output / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
        child_report = {
            "config_file_sha256": file_sha256(config_path),
            "world_seed": world_seed,
            "cell_count": 1,
            "results": [summary],
        }
        child_report["report_sha256"] = canonical_json_sha256(child_report)
        (output / "report.json").write_text(json.dumps(child_report), encoding="utf-8")
        return _FakeProcess()


def test_private_runner_is_manifest_bound_write_once_and_terminal_complete(
    private_output_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    preflight = _preflight()
    authorization = _authorization(preflight)
    monkeypatch.setattr(
        private_execution,
        "validate_private_execution_authorization",
        lambda *args, **kwargs: [],
    )
    report = execute_private_manifest(
        ROOT,
        preflight=preflight,
        authorization=authorization,
        output_root=private_output_root,
        progress_path=private_output_root / "progress.jsonl",
        resume=False,
        cell_runner=ROOT / "scripts/run_work_ii_campaign_pilot.py",
        popen_factory=_SuccessfulPopen(),
    )
    assert report["status"] == "all_private_cells_terminal"
    assert report["terminal_count"] == 75
    assert report["state_counts"] == {
        "completed": 75,
        "failed": 0,
        "right_censored": 0,
    }
    assert report["provider_attempt_count"] == 75
    assert report["expected_complete_experiment_count"] == 600
    with pytest.raises(FileExistsError):
        execute_private_manifest(
            ROOT,
            preflight=preflight,
            authorization=authorization,
            output_root=private_output_root,
            progress_path=private_output_root / "progress.jsonl",
            resume=False,
            cell_runner=ROOT / "scripts/run_work_ii_campaign_pilot.py",
            popen_factory=_SuccessfulPopen(),
        )


class _FailFirstPopen(_SuccessfulPopen):
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, command: list[str], **kwargs: object) -> _FakeProcess:
        self.calls += 1
        if self.calls == 1:
            raise OSError("synthetic pre-trajectory infrastructure failure")
        return super().__call__(command, **kwargs)


def test_private_resume_runs_only_missing_infrastructure_cell(
    private_output_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    preflight = _preflight()
    authorization = _authorization(preflight)
    monkeypatch.setattr(
        private_execution,
        "validate_private_execution_authorization",
        lambda *args, **kwargs: [],
    )
    progress = private_output_root / "progress.jsonl"
    first = execute_private_manifest(
        ROOT,
        preflight=preflight,
        authorization=authorization,
        output_root=private_output_root,
        progress_path=progress,
        resume=False,
        cell_runner=ROOT / "scripts/run_work_ii_campaign_pilot.py",
        popen_factory=_FailFirstPopen(),
    )
    assert first["status"] == "private_infrastructure_incomplete_missing_only_resume_required"
    assert first["terminal_count"] == 2
    assert first["missing_cell_count"] == 73
    second = execute_private_manifest(
        ROOT,
        preflight=preflight,
        authorization=authorization,
        output_root=private_output_root,
        progress_path=progress,
        resume=True,
        cell_runner=ROOT / "scripts/run_work_ii_campaign_pilot.py",
        popen_factory=_SuccessfulPopen(),
    )
    assert second["status"] == "all_private_cells_terminal"
    assert second["terminal_count"] == 75
    assert second["provider_attempt_count"] == 76
