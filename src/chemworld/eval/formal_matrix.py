"""Manifest-driven orchestration and completeness checks for formal cell matrices."""

from __future__ import annotations

import json
import math
import os
import subprocess
import time
from collections import Counter, deque
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import (
    FIRST_COMPLETED,
    Future,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    wait,
)
from contextlib import ExitStack, suppress
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Protocol

from chemworld.eval.formal_runner import (
    FORMAL_PUBLIC_RESULT_VERSION,
    FORMAL_RUN_MANIFEST_VERSION,
    CellIdentityError,
    CellIntegrityError,
    FormalCellSpec,
    IssuedFormalCell,
    canonical_sha256,
    file_sha256,
    statistical_failure_class,
    validate_published_cell,
)
from chemworld.eval.resource_accounting_v0_4 import (
    RESOURCE_ACCOUNTING_VERSION,
    RESOURCE_AGGREGATION_VERSION,
    aggregate_resource_accounting,
    audit_rl_training_resource,
)

FORMAL_MATRIX_PLAN_VERSION = "chemworld-formal-matrix-plan-0.4"
FORMAL_MATRIX_RUN_VERSION = "chemworld-formal-matrix-run-0.4"
FORMAL_MATRIX_AUDIT_VERSION = "chemworld-formal-matrix-audit-0.4"
FORMAL_MATRIX_PROGRESS_VERSION = "chemworld-formal-matrix-progress-0.4"

QueueKind = Literal["cpu", "gpu", "api"]
ExecutionMode = Literal["parallel", "diagnostic_serial"]
ProgressCallback = Callable[[dict[str, Any]], None]


class FormalMatrixError(RuntimeError):
    """Raised when a formal matrix cannot be trusted or scheduled."""


@dataclass(frozen=True)
class GpuSlot:
    device_id: str
    slot_index: int


@dataclass(frozen=True)
class MatrixExecutionLimits:
    """Manifest-issued concurrency and API/cost limits."""

    cpu_workers: int
    gpu_slots: tuple[GpuSlot, ...]
    api_max_concurrency: int
    api_cell_starts_per_minute: int
    api_cost_usd_per_cell_limit: float
    matrix_monetary_cost_usd_limit: float


@dataclass(frozen=True)
class FormalMatrixCell:
    spec: FormalCellSpec
    queue: QueueKind

    @property
    def cell_identity_sha256(self) -> str:
        return self.spec.cell_identity_sha256


@dataclass(frozen=True)
class FormalMatrixPlan:
    """Validated public plan expanded only from an issued run manifest."""

    run_id: str
    run_manifest_sha256: str
    matrix_plan_sha256: str
    cells: tuple[FormalMatrixCell, ...]
    tasks: tuple[str, ...]
    methods: tuple[str, ...]
    pair_ids: tuple[str, ...]
    spectrum_conditions_by_method: dict[str, tuple[str, ...]]
    checkpoints: tuple[int, ...]
    limits: MatrixExecutionLimits
    rl_training_reports: tuple[dict[str, Any], ...]

    def public_summary(self) -> dict[str, Any]:
        queue_counts = Counter(cell.queue for cell in self.cells)
        return {
            "schema_version": FORMAL_MATRIX_PLAN_VERSION,
            "run_id": self.run_id,
            "run_manifest_sha256": self.run_manifest_sha256,
            "matrix_plan_sha256": self.matrix_plan_sha256,
            "cell_count": len(self.cells),
            "task_count": len(self.tasks),
            "method_count": len(self.methods),
            "opaque_pair_count": len(self.pair_ids),
            "queue_counts": {
                "cpu": queue_counts["cpu"],
                "gpu": queue_counts["gpu"],
                "api": queue_counts["api"],
            },
            "execution_limits": {
                "cpu_workers": self.limits.cpu_workers,
                "gpu_slots": [asdict(slot) for slot in self.limits.gpu_slots],
                "api_max_concurrency": self.limits.api_max_concurrency,
                "api_cell_starts_per_minute": self.limits.api_cell_starts_per_minute,
                "api_cost_usd_per_cell_limit": self.limits.api_cost_usd_per_cell_limit,
                "matrix_monetary_cost_usd_limit": (self.limits.matrix_monetary_cost_usd_limit),
            },
            "unique_rl_training_checkpoint_count": len(self.rl_training_reports),
            "raw_private_seeds_reported": False,
            "private_world_parameters_reported": False,
        }


@dataclass(frozen=True)
class FormalMatrixJob:
    """Public-safe cell request passed to a worker process or API thread."""

    cell_identity_sha256: str
    task_id: str
    method_id: str
    method_kind: str
    pair_id: str
    spectrum_condition: str
    queue: QueueKind
    gpu_device: str | None
    progress_path: str


class MatrixCellExecutor(Protocol):
    def __call__(self, job: FormalMatrixJob) -> Mapping[str, Any] | None:
        """Execute one issued cell and return public-safe worker diagnostics."""


@dataclass(frozen=True)
class SubprocessCellExecutor:
    """Pickle-safe launcher for the official single-cell CLI."""

    manifest_path: str
    output_root: str
    private_runtime_root: str
    adapter_factory: str
    python_executable: str
    cell_script: str
    private_diagnostic_root: str | None = None

    def __call__(self, job: FormalMatrixJob) -> Mapping[str, Any]:
        runtime_path = Path(self.private_runtime_root) / f"{job.cell_identity_sha256}.json"
        if not runtime_path.is_file():
            raise FormalMatrixError("private runtime file is missing for an issued cell")
        command = [
            self.python_executable,
            self.cell_script,
            "--manifest",
            self.manifest_path,
            "--cell-id",
            job.cell_identity_sha256,
            "--output-dir",
            self.output_root,
            "--private-runtime",
            str(runtime_path),
            "--adapter-factory",
            self.adapter_factory,
        ]
        if self.private_diagnostic_root is not None:
            command.extend(
                ["--private-diagnostic-dir", self.private_diagnostic_root]
            )
        environment = dict(os.environ)
        environment["CHEMWORLD_FORMAL_PROGRESS_PATH"] = job.progress_path
        if job.gpu_device is not None:
            environment["CHEMWORLD_FORMAL_GPU_DEVICE"] = job.gpu_device
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=environment,
        )
        stdout, stderr = process.communicate()
        del stdout, stderr
        if process.returncode not in {0, 1}:
            raise FormalMatrixError("single-cell subprocess failed before a terminal artifact")
        return {
            "worker_pid": os.getpid(),
            "cell_process_pid": process.pid,
            "cell_process_return_code": process.returncode,
        }


@dataclass(frozen=True)
class MatrixRunOutcome:
    report: dict[str, Any]
    progress_events: tuple[dict[str, Any], ...]


def build_formal_matrix_plan(manifest: Mapping[str, Any]) -> FormalMatrixPlan:
    """Validate issuance, exact Cartesian coverage, pairing, and execution limits."""

    manifest_digest = _validate_run_manifest(manifest)
    raw_cells = manifest.get("cells")
    if not isinstance(raw_cells, list) or not raw_cells:
        raise FormalMatrixError("issued run manifest contains no cells")
    try:
        specs = tuple(FormalCellSpec.from_payload(item) for item in raw_cells)
    except (CellIdentityError, TypeError) as exc:
        raise FormalMatrixError("issued run manifest contains an invalid cell") from exc
    identities = tuple(spec.cell_identity_sha256 for spec in specs)
    if len(identities) != len(set(identities)):
        raise FormalMatrixError("issued run manifest contains duplicate cell identities")

    metadata = manifest.get("metadata")
    if not isinstance(metadata, Mapping):
        raise FormalMatrixError("issued run manifest is missing metadata")
    contract = metadata.get("matrix_contract")
    orchestration = metadata.get("orchestration")
    if not isinstance(contract, Mapping) or not isinstance(orchestration, Mapping):
        raise FormalMatrixError("issued run manifest lacks matrix or orchestration contract")

    tasks = _unique_text_tuple(contract, "tasks")
    methods = _unique_text_tuple(contract, "methods")
    pair_ids = _unique_text_tuple(contract, "pair_ids")
    spectrum_conditions = _spectrum_contract(contract, methods=methods)
    checkpoints = _positive_int_tuple(contract, "checkpoints")
    expected_complete = _required_positive_int(contract, "complete_experiments_per_cell")
    if checkpoints[-1] != expected_complete or any(
        checkpoint > expected_complete for checkpoint in checkpoints
    ):
        raise FormalMatrixError("matrix checkpoints must end at the complete-experiment budget")
    operation_limits = _task_operation_limits(contract, tasks=tasks)
    limits = _execution_limits(orchestration)
    training_reports = _rl_training_reports(metadata, specs=specs)

    expected_keys = {
        (task_id, method_id, pair_id, condition)
        for task_id in tasks
        for method_id in methods
        for pair_id in pair_ids
        for condition in spectrum_conditions[method_id]
    }
    actual_keys = {
        (
            spec.task_id,
            spec.method.method_id,
            spec.pair_id,
            spec.spectrum_condition,
        )
        for spec in specs
    }
    if len(actual_keys) != len(specs) or actual_keys != expected_keys:
        missing = len(expected_keys - actual_keys)
        unexpected = len(actual_keys - expected_keys)
        raise FormalMatrixError(
            f"issued matrix is not the exact Cartesian contract: missing={missing}, "
            f"unexpected={unexpected}"
        )
    for spec in specs:
        if spec.run_id != manifest.get("run_id"):
            raise FormalMatrixError("cell run_id differs from its issued run manifest")
        if spec.complete_experiments != expected_complete:
            raise FormalMatrixError("cell complete-experiment budget differs from matrix contract")
        if spec.operation_limit != operation_limits[spec.task_id]:
            raise FormalMatrixError("cell operation limit differs from its task matrix contract")
    _validate_global_bindings(specs)
    _validate_pairing(specs, tasks=tasks, pair_ids=pair_ids)

    cells = tuple(
        sorted(
            (
                FormalMatrixCell(spec=spec, queue=_queue_for_kind(spec.method.kind))
                for spec in specs
            ),
            key=lambda cell: (
                cell.spec.task_id,
                cell.spec.method.method_id,
                cell.spec.pair_id,
                cell.spec.spectrum_condition,
            ),
        )
    )
    queue_counts = Counter(cell.queue for cell in cells)
    _validate_queue_capacity(queue_counts, limits=limits)
    expected_api_cost = queue_counts["api"] * limits.api_cost_usd_per_cell_limit
    if not math.isclose(
        expected_api_cost,
        limits.matrix_monetary_cost_usd_limit,
        rel_tol=0.0,
        abs_tol=1.0e-9,
    ):
        raise FormalMatrixError("matrix monetary cap must equal API cell count times per-cell cap")

    plan_identity = {
        "schema_version": FORMAL_MATRIX_PLAN_VERSION,
        "run_id": str(manifest["run_id"]),
        "run_manifest_sha256": manifest_digest,
        "cell_identities": [cell.cell_identity_sha256 for cell in cells],
        "matrix_contract": dict(contract),
        "orchestration": dict(orchestration),
    }
    return FormalMatrixPlan(
        run_id=str(manifest["run_id"]),
        run_manifest_sha256=manifest_digest,
        matrix_plan_sha256=canonical_sha256(plan_identity),
        cells=cells,
        tasks=tasks,
        methods=methods,
        pair_ids=pair_ids,
        spectrum_conditions_by_method=spectrum_conditions,
        checkpoints=checkpoints,
        limits=limits,
        rl_training_reports=training_reports,
    )


def run_formal_matrix(
    *,
    plan: FormalMatrixPlan,
    executor: MatrixCellExecutor,
    output_root: str | Path,
    mode: ExecutionMode = "parallel",
    progress_callback: ProgressCallback | None = None,
    stop_after_new_terminals: int | None = None,
) -> MatrixRunOutcome:
    """Run or resume a matrix while keeping private identities out of progress output."""

    if mode not in {"parallel", "diagnostic_serial"}:
        raise FormalMatrixError("unsupported matrix execution mode")
    if stop_after_new_terminals is not None and stop_after_new_terminals < 1:
        raise FormalMatrixError("stop_after_new_terminals must be positive")
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    progress_path = root / "matrix-progress.jsonl"
    inbox = root / ".progress-inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    events: list[dict[str, Any]] = []
    sequence = _last_progress_sequence(progress_path)

    def emit(cell: FormalMatrixCell | None, status: str, **extra: Any) -> None:
        nonlocal sequence
        sequence += 1
        event: dict[str, Any] = {
            "schema_version": FORMAL_MATRIX_PROGRESS_VERSION,
            "sequence": sequence,
            "status": status,
            "run_id": plan.run_id,
            "matrix_plan_sha256": plan.matrix_plan_sha256,
            "raw_private_seed_reported": False,
            "private_world_parameters_reported": False,
        }
        if cell is not None:
            event.update(
                {
                    "cell_identity_sha256": cell.cell_identity_sha256,
                    "task_id": cell.spec.task_id,
                    "method_id": cell.spec.method.method_id,
                    "pair_id": cell.spec.pair_id,
                    "spectrum_condition": cell.spec.spectrum_condition,
                    "queue": cell.queue,
                }
            )
        event.update(extra)
        _assert_public_progress_event(event)
        _append_jsonl(progress_path, event)
        events.append(event)
        if progress_callback is not None:
            progress_callback(dict(event))

    preexisting: set[str] = set()
    pending: dict[QueueKind, deque[FormalMatrixCell]] = {
        "cpu": deque(),
        "gpu": deque(),
        "api": deque(),
    }
    for cell in plan.cells:
        cell_dir = root / "cells" / cell.cell_identity_sha256
        if cell_dir.exists():
            outcome = validate_published_cell(
                cell_dir,
                expected_cell=IssuedFormalCell(cell.spec, plan.run_manifest_sha256),
            )
            preexisting.add(cell.cell_identity_sha256)
            emit(
                cell,
                outcome.status,
                cached=True,
                replay_verified=outcome.status == "succeeded",
                failure_class=outcome.failure_class,
            )
        else:
            pending[cell.queue].append(cell)
            emit(cell, "queued", cached=False, replay_verified=False)

    if mode == "diagnostic_serial":
        capacities = {"cpu": 1, "gpu": 1, "api": 1}
    else:
        capacities = {
            "cpu": plan.limits.cpu_workers,
            "gpu": len(plan.limits.gpu_slots),
            "api": plan.limits.api_max_concurrency,
        }

    futures: dict[Future[Mapping[str, Any] | None], tuple[FormalMatrixCell, FormalMatrixJob]] = {}
    active_by_queue: Counter[str] = Counter()
    gpu_slots = deque(plan.limits.gpu_slots)
    api_gate = _StartRateGate(plan.limits.api_cell_starts_per_minute)
    checkpoint_offsets: dict[str, int] = {}
    seen_checkpoints: dict[str, set[int]] = {}
    last_operation_counts: dict[str, int] = {}
    infrastructure_errors: list[dict[str, Any]] = []
    worker_pids: set[int] = set()
    new_terminals = 0
    stop_requested = False
    wall_start = time.perf_counter()

    with ExitStack() as stack:
        if mode == "diagnostic_serial":
            shared = stack.enter_context(ThreadPoolExecutor(max_workers=1))
            pools: dict[QueueKind, Any] = {"cpu": shared, "gpu": shared, "api": shared}
        else:
            pools = {
                "cpu": stack.enter_context(
                    ProcessPoolExecutor(max_workers=max(1, capacities["cpu"]))
                ),
                "gpu": stack.enter_context(
                    ProcessPoolExecutor(max_workers=max(1, capacities["gpu"]))
                ),
                "api": stack.enter_context(
                    ThreadPoolExecutor(max_workers=max(1, capacities["api"]))
                ),
            }

        def submit_available() -> None:
            for queue in ("cpu", "gpu", "api"):
                while (
                    not stop_requested
                    and pending[queue]
                    and active_by_queue[queue] < capacities[queue]
                ):
                    if queue == "api" and not api_gate.ready():
                        break
                    cell = pending[queue].popleft()
                    gpu_device = None
                    if queue == "gpu":
                        if not gpu_slots:
                            pending[queue].appendleft(cell)
                            break
                        gpu_device = gpu_slots.popleft().device_id
                    if queue == "api":
                        api_gate.consume()
                    job = FormalMatrixJob(
                        cell_identity_sha256=cell.cell_identity_sha256,
                        task_id=cell.spec.task_id,
                        method_id=cell.spec.method.method_id,
                        method_kind=cell.spec.method.kind,
                        pair_id=cell.spec.pair_id,
                        spectrum_condition=cell.spec.spectrum_condition,
                        queue=cell.queue,
                        gpu_device=gpu_device,
                        progress_path=str((inbox / f"{cell.cell_identity_sha256}.jsonl").resolve()),
                    )
                    try:
                        future = pools[queue].submit(executor, job)
                    except BaseException as exc:
                        if gpu_device is not None:
                            gpu_slots.append(GpuSlot(gpu_device, 0))
                        infrastructure_errors.append(
                            {
                                "cell_identity_sha256": cell.cell_identity_sha256,
                                "error_type": type(exc).__name__,
                                "message": "worker submission failed before execution",
                            }
                        )
                        emit(
                            cell,
                            "infrastructure_incomplete",
                            cached=False,
                            replay_verified=False,
                        )
                        continue
                    futures[future] = (cell, job)
                    active_by_queue[queue] += 1
                    emit(
                        cell,
                        "running",
                        cached=False,
                        replay_verified=False,
                        gpu_device=gpu_device,
                    )

        submit_available()
        while futures or any(pending.values()):
            if not futures:
                if stop_requested:
                    break
                time.sleep(min(api_gate.seconds_until_ready(), 0.05))
                submit_available()
                continue
            done, _ = wait(tuple(futures), timeout=0.05, return_when=FIRST_COMPLETED)
            _drain_checkpoint_inbox(
                plan,
                inbox=inbox,
                offsets=checkpoint_offsets,
                seen=seen_checkpoints,
                last_operations=last_operation_counts,
                emit=emit,
            )
            for future in done:
                cell, job = futures.pop(future)
                active_by_queue[cell.queue] -= 1
                if cell.queue == "gpu":
                    assert job.gpu_device is not None
                    gpu_slots.append(GpuSlot(job.gpu_device, 0))
                try:
                    diagnostics = future.result()
                    if isinstance(diagnostics, Mapping):
                        pid = diagnostics.get("worker_pid")
                        if isinstance(pid, int) and not isinstance(pid, bool):
                            worker_pids.add(pid)
                except BaseException as exc:
                    infrastructure_errors.append(
                        {
                            "cell_identity_sha256": cell.cell_identity_sha256,
                            "error_type": type(exc).__name__,
                            "message": "worker raised before publishing a terminal cell",
                        }
                    )
                cell_dir = root / "cells" / cell.cell_identity_sha256
                if cell_dir.exists():
                    outcome = validate_published_cell(
                        cell_dir,
                        expected_cell=IssuedFormalCell(cell.spec, plan.run_manifest_sha256),
                    )
                    emit(
                        cell,
                        outcome.status,
                        cached=False,
                        replay_verified=outcome.status == "succeeded",
                        failure_class=outcome.failure_class,
                    )
                    new_terminals += 1
                else:
                    emit(
                        cell,
                        "infrastructure_incomplete",
                        cached=False,
                        replay_verified=False,
                    )
                if (
                    stop_after_new_terminals is not None
                    and new_terminals >= stop_after_new_terminals
                ):
                    stop_requested = True
            submit_available()

    _drain_checkpoint_inbox(
        plan,
        inbox=inbox,
        offsets=checkpoint_offsets,
        seen=seen_checkpoints,
        last_operations=last_operation_counts,
        emit=emit,
    )
    elapsed_wall_time_s = time.perf_counter() - wall_start
    audit = audit_formal_matrix(
        plan=plan,
        output_root=root,
        matrix_elapsed_wall_time_s=elapsed_wall_time_s,
    )
    queued_remaining = sum(len(queue) for queue in pending.values())
    final_status = "stopped_resumable" if stop_requested and queued_remaining else audit["status"]
    emit(None, "matrix_finished", matrix_status=final_status)
    report = {
        "schema_version": FORMAL_MATRIX_RUN_VERSION,
        "status": final_status,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "execution_mode": mode,
        "plan": plan.public_summary(),
        "preexisting_terminal_count": len(preexisting),
        "new_terminal_count": new_terminals,
        "queued_remaining": queued_remaining,
        "worker_pids": sorted(worker_pids),
        "infrastructure_errors": infrastructure_errors,
        "progress_event_count": len(events),
        "elapsed_wall_time_s": elapsed_wall_time_s,
        "audit": audit,
    }
    _atomic_write_json(root / "matrix-run.json", report)
    return MatrixRunOutcome(report=report, progress_events=tuple(events))


def audit_formal_matrix(
    *,
    plan: FormalMatrixPlan,
    output_root: str | Path,
    matrix_elapsed_wall_time_s: float | None = None,
) -> dict[str, Any]:
    """Check exact terminal coverage, replay, failure denominator, and accounting."""

    root = Path(output_root).resolve()
    cells_root = root / "cells"
    expected = {cell.cell_identity_sha256: cell for cell in plan.cells}
    observed = (
        {item.name for item in cells_root.iterdir() if item.is_dir()}
        if cells_root.is_dir()
        else set()
    )
    unexpected = sorted(observed - set(expected))
    missing = sorted(set(expected) - observed)
    rows: list[dict[str, Any]] = []
    failure_counts: Counter[str] = Counter()
    replay_verified = 0
    accounting_complete = 0
    resource_reports: list[dict[str, Any]] = []
    for cell_id in sorted(observed.intersection(expected)):
        cell = expected[cell_id]
        outcome = validate_published_cell(
            cells_root / cell_id,
            expected_cell=IssuedFormalCell(cell.spec, plan.run_manifest_sha256),
        )
        trajectory_path = cells_root / cell_id / "trajectory.jsonl"
        resource_path = cells_root / cell_id / "resources.json"
        resource_report = _read_object(resource_path)
        if (
            resource_report.get("schema_version") != RESOURCE_ACCOUNTING_VERSION
            or resource_report.get("cell_identity_sha256") != cell_id
        ):
            raise CellIntegrityError("matrix cell resource report is invalid")
        resource_reports.append(resource_report)
        ledger_complete = resource_report.get("accounting_complete") is True
        ledger_reason = (
            "complete"
            if ledger_complete
            else ",".join(str(item) for item in resource_report.get("failure_reasons", []))
        )
        accounting_complete += int(ledger_complete)
        row: dict[str, Any] = {
            "cell_identity_sha256": cell_id,
            "task_id": cell.spec.task_id,
            "method_id": cell.spec.method.method_id,
            "pair_id": cell.spec.pair_id,
            "spectrum_condition": cell.spec.spectrum_condition,
            "queue": cell.queue,
            "status": outcome.status,
            "replay_verified": outcome.status == "succeeded",
            "resource_accounting_complete": ledger_complete,
            "resource_accounting_status": ledger_reason,
            "trajectory_sha256": file_sha256(trajectory_path),
            "resource_report_sha256": file_sha256(resource_path),
            "resource_axes": resource_report.get("axes"),
            "failure_class": outcome.failure_class,
        }
        if outcome.status == "succeeded":
            result = _read_object(cells_root / cell_id / "result.json")
            if result.get("result_schema_version") != FORMAL_PUBLIC_RESULT_VERSION:
                raise CellIntegrityError("matrix cell result is not a formal public result")
            replay_verified += 1
        else:
            failure = _read_object(cells_root / cell_id / "failure.json")
            statistical_class = failure.get("statistical_failure_class")
            if statistical_class != statistical_failure_class(str(outcome.failure_class)):
                raise CellIntegrityError("matrix failure taxonomy is incoherent")
            failure_counts[str(statistical_class)] += 1
            row["statistical_failure_class"] = statistical_class
        rows.append(row)

    matrix_complete = not missing and not unexpected and len(rows) == len(expected)
    denominator_complete = len(rows) == len(expected) and sum(
        row["status"] in {"succeeded", "failed"} for row in rows
    ) == len(expected)
    elapsed_for_accounting = _resolve_matrix_elapsed(
        root,
        supplied=matrix_elapsed_wall_time_s,
    )
    if elapsed_for_accounting is None:
        resource_aggregation: dict[str, Any] = {
            "schema_version": RESOURCE_AGGREGATION_VERSION,
            "status": "accounting_failure",
            "accounting_complete": False,
            "failure_reasons": ["matrix_elapsed_wall_time_missing"],
        }
    else:
        resource_aggregation = aggregate_resource_accounting(
            resource_reports,
            matrix_elapsed_wall_time_s=elapsed_for_accounting,
            rl_training_reports=plan.rl_training_reports,
        )
    all_accounting_complete = (
        accounting_complete == len(expected)
        and resource_aggregation.get("accounting_complete") is True
    )
    all_successes_replay_verified = all(
        row["status"] != "succeeded" or row["replay_verified"] for row in rows
    )
    aggregation_ready = all(
        (
            matrix_complete,
            denominator_complete,
            all_accounting_complete,
            all_successes_replay_verified,
        )
    )
    semantic_rows = [
        {
            "cell_identity_sha256": row["cell_identity_sha256"],
            "status": row["status"],
            "failure_class": row["failure_class"],
            "trajectory_sha256": row["trajectory_sha256"],
            "resource_accounting_complete": row["resource_accounting_complete"],
            "resource_report_sha256": row["resource_report_sha256"],
        }
        for row in rows
    ]
    return {
        "schema_version": FORMAL_MATRIX_AUDIT_VERSION,
        "status": "complete_aggregation_ready" if aggregation_ready else "incomplete",
        "matrix_plan_sha256": plan.matrix_plan_sha256,
        "expected_cell_count": len(expected),
        "terminal_cell_count": len(rows),
        "missing_cell_count": len(missing),
        "unexpected_cell_count": len(unexpected),
        "missing_cell_identities": missing,
        "unexpected_cell_identities": unexpected,
        "exact_cartesian_matrix_complete": matrix_complete,
        "paired_conditions_complete": matrix_complete,
        "failure_denominator_complete": denominator_complete,
        "failure_counts": dict(sorted(failure_counts.items())),
        "replay_verified_success_count": replay_verified,
        "all_successes_replay_verified": all_successes_replay_verified,
        "resource_accounting_complete_count": accounting_complete,
        "all_required_resource_accounting_complete": all_accounting_complete,
        "resource_aggregation": resource_aggregation,
        "aggregation_ready": aggregation_ready,
        "cross_resource_scalarization": None,
        "semantic_result_sha256": canonical_sha256(semantic_rows),
        "cells": rows,
        "raw_private_seeds_reported": False,
        "private_world_parameters_reported": False,
    }


def _validate_run_manifest(manifest: Mapping[str, Any]) -> str:
    if manifest.get("schema_version") != FORMAL_RUN_MANIFEST_VERSION:
        raise FormalMatrixError("unsupported formal run manifest schema")
    if manifest.get("status") != "issued":
        raise FormalMatrixError("formal run manifest is not issued")
    supplied = manifest.get("run_manifest_sha256")
    if not isinstance(supplied, str) or len(supplied) != 64:
        raise FormalMatrixError("formal run manifest has no valid digest")
    unsigned = dict(manifest)
    unsigned.pop("run_manifest_sha256", None)
    if canonical_sha256(unsigned) != supplied:
        raise FormalMatrixError("formal run manifest digest mismatch")
    return supplied


def _validate_pairing(
    specs: Sequence[FormalCellSpec], *, tasks: tuple[str, ...], pair_ids: tuple[str, ...]
) -> None:
    for task_id in tasks:
        for pair_id in pair_ids:
            paired = [spec for spec in specs if spec.task_id == task_id and spec.pair_id == pair_id]
            seed_commitments = {spec.private_seed_commitment for spec in paired}
            world_commitments = {spec.world_commitment for spec in paired}
            operation_limits = {spec.operation_limit for spec in paired}
            if len(seed_commitments) != 1 or len(world_commitments) != 1:
                raise FormalMatrixError("paired methods do not share seed/world commitments")
            if len(operation_limits) != 1:
                raise FormalMatrixError("paired methods do not share the operation budget")


def _validate_global_bindings(specs: Sequence[FormalCellSpec]) -> None:
    global_fields = (
        "run_id",
        "protocol_sha256",
        "backend_semantic_sha256",
        "evaluator_sha256",
        "interaction_protocol_sha256",
        "statistics_protocol_sha256",
        "reference_manifest_sha256",
        "source_commit",
    )
    for field in global_fields:
        if len({getattr(spec, field) for spec in specs}) != 1:
            raise FormalMatrixError(f"matrix cells disagree on global binding: {field}")
    method_bindings: dict[str, str] = {}
    for spec in specs:
        digest = canonical_sha256(asdict(spec.method))
        existing = method_bindings.setdefault(spec.method.method_id, digest)
        if existing != digest:
            raise FormalMatrixError("method binding changes across matrix cells")


def _rl_training_reports(
    metadata: Mapping[str, Any], *, specs: Sequence[FormalCellSpec]
) -> tuple[dict[str, Any], ...]:
    raw = metadata.get("rl_training_resources", [])
    if not isinstance(raw, list) or not all(isinstance(item, Mapping) for item in raw):
        raise FormalMatrixError("rl_training_resources must be a list of objects")
    reports = tuple(audit_rl_training_resource(item) for item in raw)
    if any(report.get("accounting_complete") is not True for report in reports):
        raise FormalMatrixError("RL training resource report is incomplete")
    report_checkpoints = {str(report["checkpoint_sha256"]) for report in reports}
    if len(report_checkpoints) != len(reports):
        raise FormalMatrixError("RL training resource checkpoints must be unique")
    required = {
        str(spec.method.checkpoint_sha256)
        for spec in specs
        if spec.method.kind == "rl"
    }
    if report_checkpoints != required:
        raise FormalMatrixError("RL training resource reports do not match issued checkpoints")
    return tuple(dict(report) for report in reports)


def _execution_limits(raw: Mapping[str, Any]) -> MatrixExecutionLimits:
    cpu_workers = _required_positive_int(raw, "cpu_workers")
    gpu_raw = raw.get("gpu_devices")
    if not isinstance(gpu_raw, list):
        raise FormalMatrixError("orchestration gpu_devices must be a list")
    slots: list[GpuSlot] = []
    seen_devices: set[str] = set()
    for device in gpu_raw:
        if not isinstance(device, Mapping):
            raise FormalMatrixError("GPU device declaration must be an object")
        device_id = _required_text(device, "device_id")
        concurrency = _required_positive_int(device, "max_concurrency")
        quota = device.get("quota_fraction")
        if (
            isinstance(quota, bool)
            or not isinstance(quota, int | float)
            or not 0.0 < float(quota) <= 1.0
        ):
            raise FormalMatrixError("GPU quota_fraction must be in (0, 1]")
        if device_id in seen_devices or concurrency * float(quota) > 1.0 + 1.0e-12:
            raise FormalMatrixError("GPU slots must be unique and fit the declared device quota")
        seen_devices.add(device_id)
        slots.extend(GpuSlot(device_id, index) for index in range(concurrency))
    return MatrixExecutionLimits(
        cpu_workers=cpu_workers,
        gpu_slots=tuple(slots),
        api_max_concurrency=_required_positive_int(raw, "api_max_concurrency"),
        api_cell_starts_per_minute=_required_positive_int(raw, "api_cell_starts_per_minute"),
        api_cost_usd_per_cell_limit=_required_nonnegative_float(raw, "api_cost_usd_per_cell_limit"),
        matrix_monetary_cost_usd_limit=_required_nonnegative_float(
            raw, "matrix_monetary_cost_usd_limit"
        ),
    )


def _validate_queue_capacity(
    counts: Mapping[QueueKind, int], *, limits: MatrixExecutionLimits
) -> None:
    if counts.get("cpu", 0) and limits.cpu_workers < 1:
        raise FormalMatrixError("CPU cells have no process capacity")
    if counts.get("gpu", 0) and not limits.gpu_slots:
        raise FormalMatrixError("RL cells have no declared GPU slot")
    if counts.get("api", 0) and limits.api_max_concurrency < 1:
        raise FormalMatrixError("live-LLM cells have no API concurrency")


def _queue_for_kind(kind: str) -> QueueKind:
    if kind == "classic":
        return "cpu"
    if kind == "rl":
        return "gpu"
    if kind == "live_llm":
        return "api"
    raise FormalMatrixError(f"unsupported formal method kind: {kind!r}")


class _StartRateGate:
    def __init__(self, starts_per_minute: int) -> None:
        self._interval = 60.0 / starts_per_minute
        self._next_start = 0.0

    def ready(self) -> bool:
        return time.monotonic() >= self._next_start

    def consume(self) -> None:
        now = time.monotonic()
        self._next_start = max(now, self._next_start) + self._interval

    def seconds_until_ready(self) -> float:
        return max(0.0, self._next_start - time.monotonic())


def _drain_checkpoint_inbox(
    plan: FormalMatrixPlan,
    *,
    inbox: Path,
    offsets: dict[str, int],
    seen: dict[str, set[int]],
    last_operations: dict[str, int],
    emit: Callable[..., None],
) -> None:
    by_identity = {cell.cell_identity_sha256: cell for cell in plan.cells}
    for path in inbox.glob("*.jsonl"):
        cell_id = path.stem
        cell = by_identity.get(cell_id)
        if cell is None or path.is_symlink():
            raise FormalMatrixError("progress inbox contains an unexpected cell")
        start = offsets.get(cell_id, 0)
        with path.open("rb") as handle:
            handle.seek(start)
            chunks = handle.read().splitlines(keepends=True)
        consumed = 0
        for raw_line in chunks:
            if not raw_line.endswith(b"\n"):
                break
            consumed += len(raw_line)
            if not raw_line.strip():
                continue
            try:
                payload = json.loads(raw_line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise FormalMatrixError("worker progress is not valid JSONL") from exc
            if not isinstance(payload, Mapping):
                raise FormalMatrixError("worker progress record must be an object")
            _assert_public_progress_event(payload)
            _assert_progress_inbox_shape(payload)
            if payload.get("cell_identity_sha256") != cell_id:
                raise FormalMatrixError("worker progress identity mismatch")
            event_type = payload.get("event_type", "checkpoint")
            operation_count = payload.get("operation_count")
            if (
                isinstance(operation_count, bool)
                or not isinstance(operation_count, int)
                or operation_count < 1
                or operation_count > cell.spec.operation_limit
            ):
                raise FormalMatrixError("worker reported an invalid operation count")
            checkpoint = payload.get("complete_experiment_count")
            if event_type == "operation_progress":
                if (
                    isinstance(checkpoint, bool)
                    or not isinstance(checkpoint, int)
                    or checkpoint < 0
                    or checkpoint > cell.spec.complete_experiments
                ):
                    raise FormalMatrixError(
                        "worker operation progress has an invalid experiment count"
                    )
                previous = last_operations.get(cell_id, 0)
                if operation_count <= previous:
                    raise FormalMatrixError(
                        "worker operation counts are not strictly increasing"
                    )
                last_operations[cell_id] = operation_count
                emit(
                    cell,
                    "operation_progress",
                    operation_count=operation_count,
                    complete_experiment_count=checkpoint,
                    operation_type=payload.get("operation_type"),
                    transaction_status=payload.get("transaction_status"),
                    trajectory_event_type=payload.get("trajectory_event_type"),
                    replay_verified=False,
                )
                continue
            if (
                isinstance(checkpoint, bool)
                or not isinstance(checkpoint, int)
                or checkpoint not in plan.checkpoints
            ):
                raise FormalMatrixError("worker reported an unissued budget checkpoint")
            observed = seen.setdefault(cell_id, set())
            if checkpoint in observed:
                continue
            if observed and checkpoint <= max(observed):
                raise FormalMatrixError("worker checkpoints are not strictly increasing")
            observed.add(checkpoint)
            emit(
                cell,
                "checkpoint",
                complete_experiment_count=checkpoint,
                operation_count=operation_count,
                replay_verified=False,
            )
        offsets[cell_id] = start + consumed


def _resolve_matrix_elapsed(root: Path, *, supplied: float | None) -> float | None:
    if supplied is not None:
        if not math.isfinite(supplied) or supplied < 0.0:
            raise FormalMatrixError("matrix elapsed wall time must be finite and non-negative")
        return float(supplied)
    report_path = root / "matrix-run.json"
    if not report_path.is_file():
        return None
    report = _read_object(report_path)
    value = report.get("elapsed_wall_time_s")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(float(value)) or value < 0:
        return None
    return float(value)


def _assert_public_progress_event(event: Mapping[str, Any]) -> None:
    forbidden = {
        "seed",
        "method_seed",
        "world_seed",
        "seed_nonce",
        "world_nonce",
        "world_interventions",
        "world_commitment",
        "private_seed_commitment",
    }
    if forbidden.intersection(event):
        raise FormalMatrixError("progress event crosses the private runtime boundary")
    encoded = json.dumps(event, allow_nan=False, sort_keys=True)
    if not encoded:
        raise FormalMatrixError("progress event is empty")


def _assert_progress_inbox_shape(event: Mapping[str, Any]) -> None:
    event_type = event.get("event_type", "checkpoint")
    common = {
        "schema_version",
        "event_type",
        "cell_identity_sha256",
        "complete_experiment_count",
        "operation_count",
    }
    allowed = (
        common
        | {
            "operation_type",
            "transaction_status",
            "trajectory_event_type",
        }
        if event_type == "operation_progress"
        else common
    )
    if event_type not in {"checkpoint", "operation_progress"}:
        raise FormalMatrixError("worker reported an unsupported progress event")
    if set(event) - allowed:
        raise FormalMatrixError("worker progress contains unapproved public fields")
    for field in ("operation_type", "transaction_status", "trajectory_event_type"):
        value = event.get(field)
        if value is not None and (
            not isinstance(value, str)
            or len(value) > 80
            or any(ord(character) < 32 for character in value)
        ):
            raise FormalMatrixError("worker progress contains invalid status text")


def _unique_text_tuple(payload: Mapping[str, Any], field: str) -> tuple[str, ...]:
    raw = payload.get(field)
    if not isinstance(raw, list) or not raw:
        raise FormalMatrixError(f"matrix contract {field} must be a non-empty list")
    values = tuple(str(item) for item in raw)
    if any(not value.strip() for value in values) or len(values) != len(set(values)):
        raise FormalMatrixError(f"matrix contract {field} must be unique non-empty text")
    return values


def _positive_int_tuple(payload: Mapping[str, Any], field: str) -> tuple[int, ...]:
    raw = payload.get(field)
    if not isinstance(raw, list) or not raw:
        raise FormalMatrixError(f"matrix contract {field} must be a non-empty list")
    values = tuple(raw)
    if any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in values):
        raise FormalMatrixError(f"matrix contract {field} must contain positive integers")
    if tuple(sorted(set(values))) != values:
        raise FormalMatrixError(f"matrix contract {field} must be unique and increasing")
    return values


def _spectrum_contract(
    payload: Mapping[str, Any], *, methods: tuple[str, ...]
) -> dict[str, tuple[str, ...]]:
    raw = payload.get("spectrum_conditions_by_method")
    if not isinstance(raw, Mapping) or set(raw) != set(methods):
        raise FormalMatrixError("spectrum contract must cover every method exactly")
    allowed = {"assigned", "unassigned", "masked"}
    result: dict[str, tuple[str, ...]] = {}
    for method_id in methods:
        values_raw = raw[method_id]
        if not isinstance(values_raw, list) or not values_raw:
            raise FormalMatrixError("each method requires at least one spectrum condition")
        values = tuple(str(value) for value in values_raw)
        if len(values) != len(set(values)) or not set(values).issubset(allowed):
            raise FormalMatrixError("method spectrum conditions are invalid")
        result[method_id] = values
    return result


def _task_operation_limits(payload: Mapping[str, Any], *, tasks: tuple[str, ...]) -> dict[str, int]:
    raw = payload.get("operation_limits_by_task")
    if not isinstance(raw, Mapping) or set(raw) != set(tasks):
        raise FormalMatrixError("operation limit contract must cover every task exactly")
    result: dict[str, int] = {}
    for task_id in tasks:
        value = raw[task_id]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise FormalMatrixError("task operation limits must be positive integers")
        result[task_id] = value
    return result


def _required_text(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise FormalMatrixError(f"{field} must be non-empty text")
    return value


def _required_positive_int(payload: Mapping[str, Any], field: str) -> int:
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise FormalMatrixError(f"{field} must be a positive integer")
    return value


def _required_nonnegative_float(payload: Mapping[str, Any], field: str) -> float:
    value = payload.get(field)
    if (
        isinstance(value, bool)
        or not isinstance(value, int | float)
        or not math.isfinite(float(value))
        or float(value) < 0.0
    ):
        raise FormalMatrixError(f"{field} must be a finite non-negative number")
    return float(value)


def _read_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CellIntegrityError(f"cannot read matrix cell artifact: {path.name}") from exc
    if not isinstance(payload, dict):
        raise CellIntegrityError(f"matrix cell artifact is not an object: {path.name}")
    return payload


def _append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _last_progress_sequence(path: Path) -> int:
    if not path.is_file():
        return 0
    last = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise FormalMatrixError("existing matrix progress log is invalid") from exc
            sequence = payload.get("sequence") if isinstance(payload, Mapping) else None
            if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence <= last:
                raise FormalMatrixError("existing matrix progress sequence is not increasing")
            last = sequence
    return last


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(".matrix.tmp")
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        with suppress(OSError):
            temporary.unlink()
        raise


__all__ = [
    "FORMAL_MATRIX_AUDIT_VERSION",
    "FORMAL_MATRIX_PLAN_VERSION",
    "FORMAL_MATRIX_PROGRESS_VERSION",
    "FORMAL_MATRIX_RUN_VERSION",
    "FormalMatrixCell",
    "FormalMatrixError",
    "FormalMatrixJob",
    "FormalMatrixPlan",
    "GpuSlot",
    "MatrixCellExecutor",
    "MatrixExecutionLimits",
    "MatrixRunOutcome",
    "SubprocessCellExecutor",
    "audit_formal_matrix",
    "build_formal_matrix_plan",
    "run_formal_matrix",
]
