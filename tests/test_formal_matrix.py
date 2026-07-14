from __future__ import annotations

import json
import os
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from scripts.run_formal_matrix import main as formal_matrix_main

from chemworld.eval.formal_matrix import (
    FormalMatrixError,
    FormalMatrixJob,
    audit_formal_matrix,
    build_formal_matrix_plan,
    run_formal_matrix,
)
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    FormalMethodBinding,
    PrivateCellRuntime,
    canonical_sha256,
    file_sha256,
    issue_run_manifest,
    load_issued_cell,
    private_seed_commitment,
    private_world_commitment,
    run_formal_cell,
)
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
    MethodResourceLimitError,
)
from chemworld.eval.resource_accounting_v0_4 import (
    PROVIDER_RECEIPT_VERSION,
    RL_TRAINING_RESOURCE_VERSION,
    bind_pricing_snapshot,
)

RUN_ID = "1" * 64
SHA = "2" * 64
COMMIT = "3" * 40
TASK = "partition-discovery"
PAIRS = ("pair-opaque-000", "pair-opaque-001")
METHODS = ("random", "ppo", "live_llm_a")


def _runtime(pair_id: str) -> PrivateCellRuntime:
    index = PAIRS.index(pair_id)
    return PrivateCellRuntime(
        method_seed=41_000 + index,
        world_seed=51_000 + index,
        seed_nonce=f"method-nonce-{index}",
        world_nonce=f"world-nonce-{index}",
        world_interventions=({"axis_id": "partition.test", "severity": 0.7 + index * 0.1},),
    )


def _method(method_id: str) -> FormalMethodBinding:
    if method_id == "random":
        return FormalMethodBinding(
            method_id=method_id,
            kind="classic",
            artifact_sha256="4" * 64,
            resource_profile="classic_recipe",
        )
    if method_id == "ppo":
        return FormalMethodBinding(
            method_id=method_id,
            kind="rl",
            artifact_sha256="5" * 64,
            resource_profile="rl_evaluation",
            checkpoint_sha256="6" * 64,
        )
    return FormalMethodBinding(
        method_id=method_id,
        kind="live_llm",
        artifact_sha256="7" * 64,
        resource_profile="live_llm_evaluation",
        prompt_sha256="8" * 64,
        model_config_sha256="9" * 64,
    )


def _spectrum_conditions(method_id: str) -> tuple[str, ...]:
    return ("assigned", "masked") if method_id == "live_llm_a" else ("masked",)


def _spec(method_id: str, pair_id: str, condition: str) -> FormalCellSpec:
    runtime = _runtime(pair_id)
    return FormalCellSpec(
        run_id=RUN_ID,
        task_id=TASK,
        pair_id=pair_id,
        spectrum_condition=condition,  # type: ignore[arg-type]
        private_seed_commitment=private_seed_commitment(
            run_id=RUN_ID,
            pair_id=pair_id,
            method_seed=runtime.method_seed,
            nonce=runtime.seed_nonce,
        ),
        world_commitment=private_world_commitment(
            run_id=RUN_ID,
            task_id=TASK,
            pair_id=pair_id,
            world_seed=runtime.world_seed,
            nonce=runtime.world_nonce,
            interventions=runtime.world_interventions,
        ),
        protocol_sha256=SHA,
        backend_semantic_sha256=SHA,
        evaluator_sha256=SHA,
        interaction_protocol_sha256=SHA,
        statistics_protocol_sha256=SHA,
        reference_manifest_sha256=SHA,
        source_commit=COMMIT,
        complete_experiments=1,
        operation_limit=1,
        method=_method(method_id),
    )


def _manifest() -> dict[str, Any]:
    cells = [
        _spec(method_id, pair_id, condition)
        for method_id in METHODS
        for pair_id in PAIRS
        for condition in _spectrum_conditions(method_id)
    ]
    return issue_run_manifest(
        cells,
        metadata={
            "matrix_contract": {
                "tasks": [TASK],
                "methods": list(METHODS),
                "pair_ids": list(PAIRS),
                "spectrum_conditions_by_method": {
                    method_id: list(_spectrum_conditions(method_id)) for method_id in METHODS
                },
                "checkpoints": [1],
                "complete_experiments_per_cell": 1,
                "operation_limits_by_task": {TASK: 1},
            },
            "orchestration": {
                "cpu_workers": 2,
                "gpu_devices": [
                    {
                        "device_id": "test-gpu-0",
                        "max_concurrency": 1,
                        "quota_fraction": 1.0,
                    }
                ],
                "api_max_concurrency": 2,
                "api_cell_starts_per_minute": 60000,
                "api_cost_usd_per_cell_limit": 50.0,
                "matrix_monetary_cost_usd_limit": 200.0,
            },
            "rl_training_resources": [
                {
                    "schema_version": RL_TRAINING_RESOURCE_VERSION,
                    "accounting_complete": True,
                    "training_run_id": "synthetic-ppo-training",
                    "checkpoint_sha256": "6" * 64,
                    "source_manifest_sha256": "a" * 64,
                    "requested_training_environment_step_count": 100,
                    "training_environment_step_count": 100,
                    "cpu_time_s": 2.0,
                    "gpu_time_s": 1.0,
                    "wall_time_s": 1.5,
                }
            ],
        },
    )


def _api_only_manifest() -> dict[str, Any]:
    cells = [
        _spec("live_llm_a", pair_id, condition)
        for pair_id in PAIRS
        for condition in _spectrum_conditions("live_llm_a")
    ]
    return issue_run_manifest(
        cells,
        metadata={
            "matrix_contract": {
                "tasks": [TASK],
                "methods": ["live_llm_a"],
                "pair_ids": list(PAIRS),
                "spectrum_conditions_by_method": {
                    "live_llm_a": list(_spectrum_conditions("live_llm_a"))
                },
                "checkpoints": [1],
                "complete_experiments_per_cell": 1,
                "operation_limits_by_task": {TASK: 1},
            },
            "orchestration": {
                "cpu_workers": 1,
                "gpu_devices": [],
                "api_max_concurrency": 4,
                "api_cell_starts_per_minute": 600000000,
                "api_cost_usd_per_cell_limit": 50.0,
                "matrix_monetary_cost_usd_limit": 200.0,
            },
            "rl_training_resources": [],
        },
    )


def _resign(manifest: dict[str, Any]) -> None:
    unsigned = dict(manifest)
    unsigned.pop("run_manifest_sha256", None)
    manifest["run_manifest_sha256"] = canonical_sha256(unsigned)


def _rebind_cell(cell: dict[str, Any]) -> None:
    unsigned = dict(cell)
    unsigned.pop("cell_identity_sha256", None)
    cell["cell_identity_sha256"] = canonical_sha256(unsigned)


@dataclass
class _SyntheticAdapter:
    method_id: str
    kind: str
    job: FormalMatrixJob
    omit_agent_usage: bool = False
    fail_with_resource_limit: bool = False

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        if not self.fail_with_resource_limit:
            operation_progress = {
                "schema_version": "chemworld-formal-cell-progress-0.1",
                "event_type": "operation_progress",
                "cell_identity_sha256": spec.cell_identity_sha256,
                "complete_experiment_count": 1,
                "operation_count": 1,
                "operation_type": "wait",
                "transaction_status": "committed",
                "trajectory_event_type": "experiment_end",
            }
            checkpoint = {
                "schema_version": "chemworld-formal-cell-progress-0.1",
                "event_type": "checkpoint",
                "cell_identity_sha256": spec.cell_identity_sha256,
                "complete_experiment_count": 1,
                "operation_count": 1,
            }
            progress = Path(self.job.progress_path)
            progress.parent.mkdir(parents=True, exist_ok=True)
            progress.write_text(
                json.dumps(operation_progress, sort_keys=True)
                + "\n"
                + json.dumps(checkpoint, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
        pricing = bind_pricing_snapshot(
            {
                "provider": "SyntheticProvider",
                "model_id": "synthetic-model",
                "access_date": "2026-07-13",
                "currency": "USD",
                "input_cache_hit_per_million_usd": 0.0,
                "input_cache_miss_per_million_usd": 100.0,
                "output_per_million_usd": 0.0,
            }
        )
        record = {
            "step": 1,
            "seed": runtime.world_seed,
            "benchmark_task_id": spec.task_id,
            "formal_cell_identity_sha256": spec.cell_identity_sha256,
            "formal_method_id": spec.method.method_id,
            "formal_pair_id": spec.pair_id,
            "formal_spectrum_condition": spec.spectrum_condition,
            "action": {"operation": "wait"},
            "observation": {"signal": 0.5},
            "reward": 0.1,
            "method_resources": {
                "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
                "accounting_complete": True,
                "operation_count": 1,
                "complete_experiment_count": (
                    0 if self.fail_with_resource_limit else 1
                ),
                "decision_wall_time_s": 0.01,
                "update_wall_time_s": 0.01,
                "run_wall_time_s": 0.02,
                "reached_checkpoints": (
                    [] if self.fail_with_resource_limit else [1]
                ),
                "limits": {
                    "operation_limit": 1,
                    "complete_experiment_limit": 1,
                    "wall_time_limit_s": 30.0,
                    "model_call_limit": 4 if spec.method.kind == "live_llm" else None,
                    "input_token_limit": 1000 if spec.method.kind == "live_llm" else None,
                    "output_token_limit": 1000 if spec.method.kind == "live_llm" else None,
                    "monetary_cost_limit_usd": (
                        50.0 if spec.method.kind == "live_llm" else None
                    ),
                    "training_environment_step_limit": None,
                    "cpu_time_limit_s": None,
                    "gpu_time_limit_s": None,
                    "checkpoint_complete_experiments": [1],
                },
                "agent_usage": {
                    "schema_version": METHOD_RESOURCE_USAGE_VERSION,
                    "accounting_complete": True,
                    "usage_source": (
                        "synthetic-provider"
                        if spec.method.kind == "live_llm"
                        else "synthetic-runtime"
                    ),
                    "model_call_count": 1 if spec.method.kind == "live_llm" else 0,
                    "input_token_count": 100 if spec.method.kind == "live_llm" else 0,
                    "output_token_count": 20 if spec.method.kind == "live_llm" else 0,
                    "training_environment_step_count": 0,
                    "monetary_cost_usd": 0.01 if spec.method.kind == "live_llm" else 0.0,
                    "cpu_time_s": 0.01,
                    "gpu_time_s": 0.01 if spec.method.kind == "rl" else 0.0,
                    "model_provenance": (
                        {
                            "provider": "synthetic-provider",
                            "model_id": "synthetic-model",
                            "model_snapshot_or_access_date": "2026-07-13",
                            "prompt_hash": "a" * 64,
                            "request_parameters": {"temperature": 0.0},
                            "tokenizer_or_provider_usage_source": "provider",
                        }
                        if spec.method.kind == "live_llm"
                        else {}
                    ),
                },
            },
            "formal_resource_evidence": (
                {
                    "pricing_snapshot": pricing,
                    "provider_receipts": [
                        {
                            "schema_version": PROVIDER_RECEIPT_VERSION,
                            "request_id": f"request-{spec.cell_identity_sha256[:16]}",
                            "logical_decision_index": 1,
                            "attempt_index": 1,
                            "status": "succeeded",
                            "provider": "SyntheticProvider",
                            "model_id": "synthetic-model",
                            "pricing_version_sha256": pricing[
                                "pricing_version_sha256"
                            ],
                            "usage_source": "provider_response",
                            "usage_complete": True,
                            "billable": True,
                            "input_token_count": 100,
                            "output_token_count": 20,
                            "input_cache_hit_token_count": 0,
                            "input_cache_miss_token_count": 100,
                            "billed_cost_usd": 0.01,
                        }
                    ],
                }
                if spec.method.kind == "live_llm"
                else {}
            ),
        }
        if self.omit_agent_usage:
            record["method_resources"].pop("agent_usage")
        trajectory_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")
        if self.fail_with_resource_limit:
            raise MethodResourceLimitError(
                "method resource limit exceeded: wall_time_s"
            )


def _synthetic_replay(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del runtime, records
    score = int(spec.cell_identity_sha256[:8], 16) / float(0xFFFFFFFF)
    return (
        {
            "result_schema_version": "synthetic-matrix-result",
            "verified": True,
            "trajectory_sha256": file_sha256(trajectory_path),
            "verification": {"verified": True},
            "score": score,
        },
        {"verified": True, "engine": "synthetic-independent-replay"},
    )


@dataclass(frozen=True)
class _SyntheticExecutor:
    manifest: dict[str, Any]
    output_root: str
    leak_progress_seed: bool = False
    omit_agent_usage: bool = False
    fail_cell_identity: str | None = None

    def __call__(self, job: FormalMatrixJob) -> dict[str, Any]:
        issued = load_issued_cell(
            self.manifest,
            cell_identity_sha256=job.cell_identity_sha256,
        )
        runtime = _runtime(job.pair_id)
        if self.leak_progress_seed:
            progress = Path(job.progress_path)
            progress.parent.mkdir(parents=True, exist_ok=True)
            progress.write_text(
                json.dumps(
                    {
                        "cell_identity_sha256": job.cell_identity_sha256,
                        "complete_experiment_count": 1,
                        "operation_count": 1,
                        "seed": runtime.world_seed,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            return {"worker_pid": os.getpid()}
        adapter = _SyntheticAdapter(
            method_id=issued.spec.method.method_id,
            kind=issued.spec.method.kind,
            job=job,
            omit_agent_usage=self.omit_agent_usage,
            fail_with_resource_limit=(
                job.cell_identity_sha256 == self.fail_cell_identity
            ),
        )
        run_formal_cell(
            issued_cell=issued,
            runtime=runtime,
            adapter=adapter,
            output_root=self.output_root,
            replay_evaluator=_synthetic_replay,
        )
        return {"worker_pid": os.getpid()}


def _fail_before_publish(job: FormalMatrixJob) -> dict[str, Any]:
    del job
    raise RuntimeError("synthetic infrastructure interruption")


def test_plan_expands_exact_manifest_grid_and_public_resource_summary() -> None:
    plan = build_formal_matrix_plan(_manifest())
    summary = plan.public_summary()
    assert summary["cell_count"] == 8
    assert summary["queue_counts"] == {"cpu": 2, "gpu": 2, "api": 4}
    assert summary["execution_limits"]["matrix_monetary_cost_usd_limit"] == 200.0
    assert summary["unique_rl_training_checkpoint_count"] == 1
    assert summary["raw_private_seeds_reported"] is False
    encoded = json.dumps(summary, sort_keys=True)
    assert "method-nonce" not in encoded
    assert "world-nonce" not in encoded


def test_cli_dry_run_uses_manifest_only_and_prints_public_plan(
    tmp_path, monkeypatch, capsys
) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_manifest(), sort_keys=True), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_formal_matrix.py",
            "--manifest",
            str(manifest_path),
            "--output-dir",
            str(tmp_path / "output"),
            "--dry-run",
        ],
    )
    assert formal_matrix_main() == 0
    output = capsys.readouterr().out
    assert '"cell_count": 8' in output
    assert "method-nonce" not in output
    assert "world-nonce" not in output


def test_plan_rejects_missing_cartesian_cell_even_when_manifest_is_resigned() -> None:
    manifest = _manifest()
    manifest["cells"].pop()
    _resign(manifest)
    with pytest.raises(FormalMatrixError, match="exact Cartesian"):
        build_formal_matrix_plan(manifest)


def test_plan_rejects_pairing_and_method_hash_drift() -> None:
    pairing = _manifest()
    pairing["cells"][0]["world_commitment"] = "a" * 64
    _rebind_cell(pairing["cells"][0])
    _resign(pairing)
    with pytest.raises(FormalMatrixError, match="seed/world commitments"):
        build_formal_matrix_plan(pairing)

    method_drift = _manifest()
    target = next(cell for cell in method_drift["cells"] if cell["method"]["method_id"] == "random")
    target["method"]["artifact_sha256"] = "b" * 64
    _rebind_cell(target)
    _resign(method_drift)
    with pytest.raises(FormalMatrixError, match="method binding changes"):
        build_formal_matrix_plan(method_drift)


def test_plan_rejects_gpu_overcommit_and_incoherent_api_cost_cap() -> None:
    overcommit = _manifest()
    gpu = overcommit["metadata"]["orchestration"]["gpu_devices"][0]
    gpu.update({"max_concurrency": 2, "quota_fraction": 0.75})
    _resign(overcommit)
    with pytest.raises(FormalMatrixError, match="device quota"):
        build_formal_matrix_plan(overcommit)

    cost = _manifest()
    cost["metadata"]["orchestration"]["matrix_monetary_cost_usd_limit"] = 199.0
    _resign(cost)
    with pytest.raises(FormalMatrixError, match="monetary cap"):
        build_formal_matrix_plan(cost)


def test_plan_rejects_missing_or_incomplete_rl_training_resource_binding() -> None:
    missing = _manifest()
    missing["metadata"]["rl_training_resources"] = []
    _resign(missing)
    with pytest.raises(FormalMatrixError, match="do not match issued checkpoints"):
        build_formal_matrix_plan(missing)

    incomplete = _manifest()
    incomplete["metadata"]["rl_training_resources"][0]["gpu_time_s"] = None
    _resign(incomplete)
    with pytest.raises(FormalMatrixError, match="resource report is incomplete"):
        build_formal_matrix_plan(incomplete)


def test_parallel_smoke_matrix_completes_with_public_progress_and_exact_audit(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    outcome = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path)),
        output_root=tmp_path,
    )
    audit = outcome.report["audit"]
    assert outcome.report["status"] == "complete_aggregation_ready"
    assert audit["exact_cartesian_matrix_complete"] is True
    assert audit["paired_conditions_complete"] is True
    assert audit["failure_denominator_complete"] is True
    assert audit["all_required_resource_accounting_complete"] is True
    assert audit["resource_aggregation"]["accounting_complete"] is True
    assert audit["resource_aggregation"]["rl_training_resource_totals_separate"][
        "training_environment_step_count"
    ] == 100
    assert audit["resource_aggregation"]["evaluation_resource_totals"][
        "training_environment_step_count"
    ] == 0
    assert audit["replay_verified_success_count"] == 8
    assert len(outcome.report["worker_pids"]) >= 2
    statuses = Counter(event["status"] for event in outcome.progress_events)
    assert statuses["queued"] == 8
    assert statuses["running"] == 8
    assert statuses["operation_progress"] == 8
    assert statuses["checkpoint"] == 8
    assert statuses["succeeded"] == 8
    assert all("seed" not in event for event in outcome.progress_events)


def test_accounted_resource_limit_failure_remains_aggregation_ready(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    failed_cell = next(
        cell.cell_identity_sha256
        for cell in plan.cells
        if cell.spec.method.kind == "live_llm"
    )
    outcome = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(
            manifest,
            str(tmp_path),
            fail_cell_identity=failed_cell,
        ),
        output_root=tmp_path,
    )

    audit = outcome.report["audit"]
    failed_row = next(
        row for row in audit["cells"] if row["cell_identity_sha256"] == failed_cell
    )
    assert outcome.report["status"] == "complete_aggregation_ready"
    assert audit["aggregation_ready"] is True
    assert audit["failure_denominator_complete"] is True
    assert audit["failure_counts"] == {"budget_overrun": 1}
    assert audit["resource_accounting_complete_count"] == len(plan.cells)
    assert failed_row["status"] == "failed"
    assert failed_row["failure_class"] == "budget_overrun"
    assert failed_row["resource_accounting_complete"] is True


def test_stopped_matrix_resumes_only_missing_cells(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    first = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path)),
        output_root=tmp_path,
        stop_after_new_terminals=2,
    )
    assert first.report["status"] == "stopped_resumable"
    assert first.report["new_terminal_count"] == 2
    assert first.report["queued_remaining"] == 6
    terminal_before = first.report["audit"]["terminal_cell_count"]

    resumed = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path)),
        output_root=tmp_path,
    )
    assert resumed.report["status"] == "complete_aggregation_ready"
    assert resumed.report["preexisting_terminal_count"] == terminal_before
    assert resumed.report["new_terminal_count"] == 8 - terminal_before
    preexisting_ids = {
        event["cell_identity_sha256"]
        for event in first.progress_events
        if event["status"] in {"succeeded", "failed"}
    }
    replayed_detail_ids = {
        event["cell_identity_sha256"]
        for event in resumed.progress_events
        if event["status"] in {"operation_progress", "checkpoint"}
    }
    assert preexisting_ids.isdisjoint(replayed_detail_ids)


def test_stop_limit_caps_api_submission_below_declared_concurrency(tmp_path) -> None:
    manifest = _api_only_manifest()
    plan = build_formal_matrix_plan(manifest)

    outcome = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path)),
        output_root=tmp_path,
        stop_after_new_terminals=1,
    )

    statuses = Counter(event["status"] for event in outcome.progress_events)
    assert outcome.report["status"] == "stopped_resumable"
    assert outcome.report["new_terminal_count"] == 1
    assert outcome.report["queued_remaining"] == 3
    assert outcome.report["audit"]["terminal_cell_count"] == 1
    assert statuses["running"] == 1
    assert statuses["succeeded"] == 1


def test_infrastructure_failure_stops_new_scheduling_and_remains_resumable(
    tmp_path,
) -> None:
    plan = build_formal_matrix_plan(_manifest())

    outcome = run_formal_matrix(
        plan=plan,
        executor=_fail_before_publish,
        output_root=tmp_path,
        mode="diagnostic_serial",
    )

    assert outcome.report["status"] == "stopped_resumable"
    assert outcome.report["new_terminal_count"] == 0
    assert outcome.report["queued_remaining"] == 5
    assert len(outcome.report["infrastructure_errors"]) == 3
    statuses = Counter(event["status"] for event in outcome.progress_events)
    assert statuses["running"] == 3
    assert statuses["infrastructure_incomplete"] == 3


def test_serial_and_parallel_execution_have_identical_semantic_results(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    serial_root = tmp_path / "serial"
    parallel_root = tmp_path / "parallel"
    serial = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(serial_root)),
        output_root=serial_root,
        mode="diagnostic_serial",
    )
    parallel = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(parallel_root)),
        output_root=parallel_root,
        mode="parallel",
    )
    assert (
        serial.report["audit"]["semantic_result_sha256"]
        == parallel.report["audit"]["semantic_result_sha256"]
    )


def test_missing_terminal_cell_forces_incomplete_audit(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    outcome = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path)),
        output_root=tmp_path,
        mode="diagnostic_serial",
    )
    victim = Path(outcome.report["audit"]["cells"][0]["cell_identity_sha256"])
    shutil.rmtree(tmp_path / "cells" / victim)
    audit = audit_formal_matrix(plan=plan, output_root=tmp_path)
    assert audit["status"] == "incomplete"
    assert audit["missing_cell_count"] == 1
    assert audit["aggregation_ready"] is False


def test_declared_complete_but_malformed_resource_ledger_fails_closed(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    outcome = run_formal_matrix(
        plan=plan,
        executor=_SyntheticExecutor(manifest, str(tmp_path), omit_agent_usage=True),
        output_root=tmp_path,
        mode="diagnostic_serial",
    )
    audit = outcome.report["audit"]
    assert all(row["resource_accounting_complete"] is False for row in audit["cells"])
    assert all(
        "agent_usage_missing" in row["resource_accounting_status"]
        for row in audit["cells"]
    )
    assert audit["aggregation_ready"] is False


def test_progress_inbox_rejects_private_seed_fields(tmp_path) -> None:
    manifest = _manifest()
    plan = build_formal_matrix_plan(manifest)
    with pytest.raises(FormalMatrixError, match="private runtime boundary"):
        run_formal_matrix(
            plan=plan,
            executor=_SyntheticExecutor(manifest, str(tmp_path), leak_progress_seed=True),
            output_root=tmp_path,
            mode="diagnostic_serial",
        )
