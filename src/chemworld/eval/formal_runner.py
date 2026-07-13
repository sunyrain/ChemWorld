"""Fail-closed, transactional execution of one formal benchmark cell.

The public cell identity is issued by a preflight manifest.  Private seeds and
world parameters are supplied separately at execution time and are checked
against commitments before an adapter can observe them.  A cell becomes
aggregator-visible only after its trajectory, result, replay report, failure
record, and artifact index have been written and the completion marker is the
last file created in an isolated staging directory.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
import shutil
import uuid
from collections.abc import Callable, Mapping, Sequence
from contextlib import suppress
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import TracebackType
from typing import Any, Literal, Protocol, Self

from chemworld.data.logging import load_jsonl
from chemworld.eval.resource_accounting_v0_4 import (
    RESOURCE_ACCOUNTING_VERSION,
    ResourceProfile,
    audit_cell_resource_accounting,
    unavailable_resource_accounting_report,
)
from chemworld.eval.result_artifacts import build_verified_evaluation_result

FORMAL_RUN_MANIFEST_VERSION = "chemworld-formal-run-manifest-0.4"
FORMAL_CELL_VERSION = "chemworld-formal-cell-0.4"
FORMAL_CELL_ARTIFACT_VERSION = "chemworld-formal-cell-artifacts-0.4"
FORMAL_PUBLIC_RESULT_VERSION = "chemworld-formal-public-result-0.4"
PRIVATE_RUNTIME_COMMITMENT_VERSION = "chemworld-private-runtime-commitment-0.4"
STATISTICAL_FAILURE_CLASSES = (
    "invalid_action",
    "provider_model_failure",
    "runtime_failure",
    "budget_overrun",
    "incomplete_accounting",
)

MethodKind = Literal["classic", "rl", "live_llm"]
SpectrumCondition = Literal["assigned", "unassigned", "masked"]
CellStatus = Literal["succeeded", "failed"]
FaultHook = Callable[[str, Path], None]


class FormalRunnerError(RuntimeError):
    """Base class for formal runner failures."""


class CellIdentityError(FormalRunnerError):
    """Raised when a manifest, cell identity, or private commitment is invalid."""


class CellBusyError(FormalRunnerError):
    """Raised when another process owns the same cell execution lock."""


class CellIntegrityError(FormalRunnerError):
    """Raised when an already-published cell no longer matches its digests."""


class TrajectoryContractError(FormalRunnerError):
    """Raised when a trajectory cannot represent a complete formal cell."""


class BudgetOverrunError(TrajectoryContractError):
    """Raised when the operation or complete-experiment budget is exceeded."""


class IncompleteAccountingError(TrajectoryContractError):
    """Raised when required method resource accounting is absent or incoherent."""


class ReplayMismatchError(TrajectoryContractError):
    """Raised when independent deterministic replay does not verify a trajectory."""


class MissingOrNonfiniteMetricError(TrajectoryContractError):
    """Raised when a trajectory or evaluation result contains non-finite data."""


class PrivateControlLeakError(TrajectoryContractError):
    """Raised when a public-safe control artifact contains private runtime state."""


@dataclass(frozen=True)
class FormalMethodBinding:
    """Immutable method evidence bound into a formal cell identity."""

    method_id: str
    kind: MethodKind
    artifact_sha256: str
    resource_profile: ResourceProfile
    checkpoint_sha256: str | None = None
    prompt_sha256: str | None = None
    model_config_sha256: str | None = None

    def __post_init__(self) -> None:
        if not self.method_id.strip():
            raise CellIdentityError("method_id must be non-empty")
        _require_sha256(self.artifact_sha256, "method artifact")
        expected_profiles = {
            "classic": {"classic_recipe", "operation_baseline"},
            "rl": {"rl_evaluation"},
            "live_llm": {"live_llm_evaluation"},
        }
        if self.resource_profile not in expected_profiles.get(self.kind, set()):
            raise CellIdentityError("method kind and resource profile are incoherent")
        if self.kind == "classic":
            if any(
                value is not None
                for value in (
                    self.checkpoint_sha256,
                    self.prompt_sha256,
                    self.model_config_sha256,
                )
            ):
                raise CellIdentityError("classic methods cannot bind checkpoint or prompt state")
        elif self.kind == "rl":
            _require_sha256(self.checkpoint_sha256, "RL checkpoint")
            if self.prompt_sha256 is not None or self.model_config_sha256 is not None:
                raise CellIdentityError("RL methods cannot bind live-LLM prompt state")
        elif self.kind == "live_llm":
            _require_sha256(self.prompt_sha256, "live-LLM prompt")
            _require_sha256(self.model_config_sha256, "live-LLM model configuration")
            if self.checkpoint_sha256 is not None:
                raise CellIdentityError("live-LLM methods cannot bind an RL checkpoint")
        else:
            raise CellIdentityError(f"unsupported method kind: {self.kind!r}")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> Self:
        return cls(
            method_id=_required_text(payload, "method_id"),
            kind=_required_text(payload, "kind"),  # type: ignore[arg-type]
            artifact_sha256=_required_text(payload, "artifact_sha256"),
            resource_profile=_required_text(payload, "resource_profile"),  # type: ignore[arg-type]
            checkpoint_sha256=_optional_text(payload.get("checkpoint_sha256")),
            prompt_sha256=_optional_text(payload.get("prompt_sha256")),
            model_config_sha256=_optional_text(payload.get("model_config_sha256")),
        )


@dataclass(frozen=True)
class FormalCellSpec:
    """Public identity of exactly one task-method-pair-world-spectrum cell."""

    run_id: str
    task_id: str
    pair_id: str
    spectrum_condition: SpectrumCondition
    private_seed_commitment: str
    world_commitment: str
    protocol_sha256: str
    backend_semantic_sha256: str
    evaluator_sha256: str
    interaction_protocol_sha256: str
    statistics_protocol_sha256: str
    reference_manifest_sha256: str
    source_commit: str
    complete_experiments: int
    operation_limit: int
    method: FormalMethodBinding

    def __post_init__(self) -> None:
        for field_name in ("run_id", "task_id", "pair_id"):
            if not str(getattr(self, field_name)).strip():
                raise CellIdentityError(f"{field_name} must be non-empty")
        _require_sha256(self.run_id, "run id")
        for field_name in (
            "private_seed_commitment",
            "world_commitment",
            "protocol_sha256",
            "backend_semantic_sha256",
            "evaluator_sha256",
            "interaction_protocol_sha256",
            "statistics_protocol_sha256",
            "reference_manifest_sha256",
        ):
            _require_sha256(str(getattr(self, field_name)), field_name)
        if not _is_git_commit(self.source_commit):
            raise CellIdentityError("source_commit must be a 40-character Git commit")
        if self.spectrum_condition not in {"assigned", "unassigned", "masked"}:
            raise CellIdentityError("unsupported spectrum condition")
        if isinstance(self.complete_experiments, bool) or self.complete_experiments <= 0:
            raise CellIdentityError("complete_experiments must be positive")
        if isinstance(self.operation_limit, bool) or self.operation_limit <= 0:
            raise CellIdentityError("operation_limit must be positive")
        if self.operation_limit < self.complete_experiments:
            raise CellIdentityError("operation_limit cannot be below complete_experiments")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> Self:
        if payload.get("schema_version") != FORMAL_CELL_VERSION:
            raise CellIdentityError("unsupported formal cell schema")
        method = payload.get("method")
        if not isinstance(method, Mapping):
            raise CellIdentityError("formal cell is missing method binding")
        spec = cls(
            run_id=_required_text(payload, "run_id"),
            task_id=_required_text(payload, "task_id"),
            pair_id=_required_text(payload, "pair_id"),
            spectrum_condition=_required_text(  # type: ignore[arg-type]
                payload, "spectrum_condition"
            ),
            private_seed_commitment=_required_text(payload, "private_seed_commitment"),
            world_commitment=_required_text(payload, "world_commitment"),
            protocol_sha256=_required_text(payload, "protocol_sha256"),
            backend_semantic_sha256=_required_text(payload, "backend_semantic_sha256"),
            evaluator_sha256=_required_text(payload, "evaluator_sha256"),
            interaction_protocol_sha256=_required_text(payload, "interaction_protocol_sha256"),
            statistics_protocol_sha256=_required_text(payload, "statistics_protocol_sha256"),
            reference_manifest_sha256=_required_text(payload, "reference_manifest_sha256"),
            source_commit=_required_text(payload, "source_commit"),
            complete_experiments=_required_positive_int(payload, "complete_experiments"),
            operation_limit=_required_positive_int(payload, "operation_limit"),
            method=FormalMethodBinding.from_payload(method),
        )
        supplied_identity = _required_text(payload, "cell_identity_sha256")
        if supplied_identity != spec.cell_identity_sha256:
            raise CellIdentityError("formal cell identity digest mismatch")
        return spec

    @property
    def cell_identity_sha256(self) -> str:
        return canonical_sha256(self.identity_payload())

    def identity_payload(self) -> dict[str, Any]:
        return {
            "schema_version": FORMAL_CELL_VERSION,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "pair_id": self.pair_id,
            "spectrum_condition": self.spectrum_condition,
            "private_seed_commitment": self.private_seed_commitment,
            "world_commitment": self.world_commitment,
            "protocol_sha256": self.protocol_sha256,
            "backend_semantic_sha256": self.backend_semantic_sha256,
            "evaluator_sha256": self.evaluator_sha256,
            "interaction_protocol_sha256": self.interaction_protocol_sha256,
            "statistics_protocol_sha256": self.statistics_protocol_sha256,
            "reference_manifest_sha256": self.reference_manifest_sha256,
            "source_commit": self.source_commit,
            "complete_experiments": self.complete_experiments,
            "operation_limit": self.operation_limit,
            "method": asdict(self.method),
        }

    def issued_payload(self) -> dict[str, Any]:
        return {
            **self.identity_payload(),
            "cell_identity_sha256": self.cell_identity_sha256,
        }


@dataclass(frozen=True)
class IssuedFormalCell:
    """Cell spec plus the exact preflight manifest that authorized it."""

    spec: FormalCellSpec
    run_manifest_sha256: str


@dataclass(frozen=True)
class PrivateCellRuntime:
    """Private execution state kept outside public manifests and artifacts."""

    method_seed: int
    world_seed: int
    seed_nonce: str
    world_nonce: str
    world_interventions: tuple[dict[str, Any], ...]

    def __post_init__(self) -> None:
        for field_name in ("method_seed", "world_seed"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise CellIdentityError(f"{field_name} must be a non-negative integer")
        if not self.seed_nonce or not self.world_nonce:
            raise CellIdentityError("private runtime nonces must be non-empty")
        if not all(isinstance(item, dict) for item in self.world_interventions):
            raise CellIdentityError("world interventions must be JSON objects")
        _assert_finite_json(self.world_interventions, "world interventions")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> Self:
        interventions = payload.get("world_interventions")
        if not isinstance(interventions, list | tuple):
            raise CellIdentityError("private runtime requires world_interventions")
        return cls(
            method_seed=_required_nonnegative_int(payload, "method_seed"),
            world_seed=_required_nonnegative_int(payload, "world_seed"),
            seed_nonce=_required_text(payload, "seed_nonce"),
            world_nonce=_required_text(payload, "world_nonce"),
            world_interventions=tuple(dict(item) for item in interventions),
        )

    def assert_matches(self, spec: FormalCellSpec) -> None:
        expected_seed = private_seed_commitment(
            run_id=spec.run_id,
            pair_id=spec.pair_id,
            method_seed=self.method_seed,
            nonce=self.seed_nonce,
        )
        expected_world = private_world_commitment(
            run_id=spec.run_id,
            task_id=spec.task_id,
            pair_id=spec.pair_id,
            world_seed=self.world_seed,
            nonce=self.world_nonce,
            interventions=self.world_interventions,
        )
        if expected_seed != spec.private_seed_commitment:
            raise CellIdentityError("private method seed does not match its commitment")
        if expected_world != spec.world_commitment:
            raise CellIdentityError("private world does not match its commitment")


class FormalExecutionAdapter(Protocol):
    """Method-specific execution boundary used by the transaction runner."""

    method_id: str
    kind: MethodKind

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        """Write only the requested cell trajectory; never synthesize closeout actions."""


AdapterFactory = Callable[[FormalCellSpec], FormalExecutionAdapter]
ReplayEvaluator = Callable[
    [FormalCellSpec, PrivateCellRuntime, list[dict[str, Any]], Path],
    tuple[dict[str, Any], dict[str, Any]],
]


class FormalAdapterRegistry:
    """Exact method/kind registry for classic, RL, and live-LLM adapters."""

    def __init__(self) -> None:
        self._factories: dict[tuple[str, MethodKind], AdapterFactory] = {}

    def register(self, method_id: str, kind: MethodKind, factory: AdapterFactory) -> None:
        key = (method_id, kind)
        if key in self._factories:
            raise CellIdentityError(f"duplicate formal adapter registration: {method_id}/{kind}")
        if kind not in {"classic", "rl", "live_llm"}:
            raise CellIdentityError(f"unsupported method kind: {kind!r}")
        self._factories[key] = factory

    def create(self, spec: FormalCellSpec) -> FormalExecutionAdapter:
        key = (spec.method.method_id, spec.method.kind)
        try:
            adapter = self._factories[key](spec)
        except KeyError as exc:
            raise CellIdentityError(
                f"formal adapter is not registered: {spec.method.method_id}/{spec.method.kind}"
            ) from exc
        if adapter.method_id != spec.method.method_id or adapter.kind != spec.method.kind:
            raise CellIdentityError("adapter factory returned a mismatched method identity")
        return adapter

    def registered_methods(self) -> tuple[tuple[str, MethodKind], ...]:
        return tuple(sorted(self._factories))


@dataclass(frozen=True)
class CellRunOutcome:
    """Stable locator and public status returned for first or cached execution."""

    cell_identity_sha256: str
    status: CellStatus
    cell_dir: Path
    cached: bool
    failure_class: str | None


def private_seed_commitment(*, run_id: str, pair_id: str, method_seed: int, nonce: str) -> str:
    """Commit a private method seed without putting it into a public identity."""

    return canonical_sha256(
        {
            "schema_version": PRIVATE_RUNTIME_COMMITMENT_VERSION,
            "kind": "method_seed",
            "run_id": run_id,
            "pair_id": pair_id,
            "method_seed": method_seed,
            "nonce": nonce,
        }
    )


def private_world_commitment(
    *,
    run_id: str,
    task_id: str,
    pair_id: str,
    world_seed: int,
    nonce: str,
    interventions: Sequence[Mapping[str, Any]],
) -> str:
    """Commit the complete private world assignment used by one task/pair."""

    return canonical_sha256(
        {
            "schema_version": PRIVATE_RUNTIME_COMMITMENT_VERSION,
            "kind": "task_world",
            "run_id": run_id,
            "task_id": task_id,
            "pair_id": pair_id,
            "world_seed": world_seed,
            "nonce": nonce,
            "interventions": [dict(item) for item in interventions],
        }
    )


def statistical_failure_class(protocol_failure_class: str) -> str:
    """Map protocol-granular failures to the preregistered five-class denominator."""

    mapping = {
        "invalid_action": "invalid_action",
        "provider_or_model_failure": "provider_model_failure",
        "runtime_failure": "runtime_failure",
        "budget_overrun": "budget_overrun",
        "missing_or_nonfinite_metric": "runtime_failure",
        "incomplete_resource_accounting": "incomplete_accounting",
        "replay_mismatch": "runtime_failure",
    }
    try:
        result = mapping[protocol_failure_class]
    except KeyError as exc:
        raise CellIntegrityError(
            f"unknown formal protocol failure class: {protocol_failure_class!r}"
        ) from exc
    if result not in STATISTICAL_FAILURE_CLASSES:
        raise CellIntegrityError("formal failure does not map into the statistical denominator")
    return result


def issue_run_manifest(
    cells: Sequence[FormalCellSpec], *, metadata: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Build a digest-bound manifest; the preflight gate owns when this is allowed."""

    if not cells:
        raise CellIdentityError("cannot issue an empty run manifest")
    run_ids = {cell.run_id for cell in cells}
    if len(run_ids) != 1:
        raise CellIdentityError("all issued cells must share one run_id")
    identities = [cell.cell_identity_sha256 for cell in cells]
    if len(identities) != len(set(identities)):
        raise CellIdentityError("run manifest contains duplicate cell identities")
    manifest: dict[str, Any] = {
        "schema_version": FORMAL_RUN_MANIFEST_VERSION,
        "status": "issued",
        "run_id": cells[0].run_id,
        "cells": [cell.issued_payload() for cell in cells],
        "metadata": dict(metadata or {}),
    }
    manifest["run_manifest_sha256"] = canonical_sha256(manifest)
    return manifest


def load_issued_cell(manifest: Mapping[str, Any], *, cell_identity_sha256: str) -> IssuedFormalCell:
    """Validate an entire issued manifest and resolve exactly one authorized cell."""

    if manifest.get("schema_version") != FORMAL_RUN_MANIFEST_VERSION:
        raise CellIdentityError("unsupported formal run manifest schema")
    if manifest.get("status") != "issued":
        raise CellIdentityError("formal run manifest has not been issued")
    supplied_digest = _required_text(manifest, "run_manifest_sha256")
    unsigned = dict(manifest)
    unsigned.pop("run_manifest_sha256", None)
    if canonical_sha256(unsigned) != supplied_digest:
        raise CellIdentityError("formal run manifest digest mismatch")
    _require_sha256(cell_identity_sha256, "cell identity")
    cells = manifest.get("cells")
    if not isinstance(cells, list) or not cells:
        raise CellIdentityError("formal run manifest contains no cells")
    if not all(isinstance(item, Mapping) for item in cells):
        raise CellIdentityError("formal run manifest cells must be objects")
    parsed = [FormalCellSpec.from_payload(item) for item in cells]
    identities = [item.cell_identity_sha256 for item in parsed]
    if len(identities) != len(set(identities)):
        raise CellIdentityError("formal run manifest contains duplicate cells")
    run_id = _required_text(manifest, "run_id")
    if any(item.run_id != run_id for item in parsed):
        raise CellIdentityError("cell run_id does not match its run manifest")
    matches = [item for item in parsed if item.cell_identity_sha256 == cell_identity_sha256]
    if len(matches) != 1:
        raise CellIdentityError("requested cell was not issued by this run manifest")
    return IssuedFormalCell(spec=matches[0], run_manifest_sha256=supplied_digest)


def run_formal_cell(
    *,
    issued_cell: IssuedFormalCell,
    runtime: PrivateCellRuntime,
    adapter: FormalExecutionAdapter,
    output_root: str | Path,
    replay_evaluator: ReplayEvaluator | None = None,
    fault_hook: FaultHook | None = None,
) -> CellRunOutcome:
    """Execute one formal cell transaction or return its verified cached outcome."""

    spec = issued_cell.spec
    runtime.assert_matches(spec)
    if adapter.method_id != spec.method.method_id or adapter.kind != spec.method.kind:
        raise CellIdentityError("execution adapter does not match the issued cell")
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    cell_dir = root / "cells" / spec.cell_identity_sha256
    lock_path = root / ".locks" / f"{spec.cell_identity_sha256}.lock"
    evaluator = _default_replay_evaluator if replay_evaluator is None else replay_evaluator

    with _CellLock(lock_path):
        if cell_dir.exists():
            outcome = validate_published_cell(
                cell_dir,
                expected_cell=issued_cell,
            )
            return CellRunOutcome(
                cell_identity_sha256=outcome.cell_identity_sha256,
                status=outcome.status,
                cell_dir=outcome.cell_dir,
                cached=True,
                failure_class=outcome.failure_class,
            )

        attempt_id = uuid.uuid4().hex
        staging = root / ".staging" / (f"{spec.cell_identity_sha256[:16]}-{attempt_id[:16]}")
        staging.mkdir(parents=True, exist_ok=False)
        trajectory_path = staging / "trajectory.jsonl"
        started_at = _utc_now()
        manifest_artifact = {
            "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
            "artifact": "cell_manifest",
            "cell": spec.issued_payload(),
            "run_manifest_sha256": issued_cell.run_manifest_sha256,
            "attempt_id": attempt_id,
            "started_at": started_at,
            "private_runtime_values_in_artifact": False,
            "automatic_action_repair": False,
            "automatic_final_assay": False,
        }
        _atomic_write_json(staging / "manifest.json", manifest_artifact)
        manifest_artifact_sha256 = file_sha256(staging / "manifest.json")
        _call_fault_hook(fault_hook, "after_manifest", staging)
        resource_report = unavailable_resource_accounting_report(
            cell_identity_sha256=spec.cell_identity_sha256,
            method_id=spec.method.method_id,
            method_kind=spec.method.kind,
            resource_profile=spec.method.resource_profile,
            reason="execution_failed_before_resource_audit",
            rl_checkpoint_sha256=spec.method.checkpoint_sha256,
        )

        try:
            adapter.execute(spec=spec, runtime=runtime, trajectory_path=trajectory_path)
            _call_fault_hook(fault_hook, "after_execute", staging)
            if file_sha256(staging / "manifest.json") != manifest_artifact_sha256:
                raise OSError("adapter modified the runner-owned cell manifest")
            records = _validate_trajectory(trajectory_path, spec=spec, runtime=runtime)
            resource_report = _audit_formal_resource_evidence(records, spec=spec)
            _assert_public_control_safe(
                resource_report,
                runtime=runtime,
                label="resource accounting report",
            )
            _atomic_write_json(staging / "resources.json", resource_report)
            if resource_report.get("accounting_complete") is not True:
                raise IncompleteAccountingError("formal resource accounting failed")
            result, replay = evaluator(spec, runtime, records, trajectory_path)
            _validate_replay_payload(result, replay, trajectory_path=trajectory_path)
            result = _sanitize_result_for_public_control(result, spec=spec, runtime=runtime)
            _assert_public_control_safe(result, runtime=runtime, label="evaluation result")
            _assert_public_control_safe(replay, runtime=runtime, label="replay report")
            result["trajectory_path"] = str((cell_dir / "trajectory.jsonl").resolve())
            result.update(_result_binding(spec, issued_cell.run_manifest_sha256, attempt_id))
            replay = dict(replay)
            replay.update(_replay_binding(spec, trajectory_path))
            _atomic_write_json(staging / "result.json", result)
            _atomic_write_json(
                staging / "failure.json",
                {
                    "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
                    "artifact": "failure",
                    "status": "no_failure",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "attempt_id": attempt_id,
                },
            )
            _atomic_write_json(staging / "replay.json", replay)
            status: CellStatus = "succeeded"
            failure_class = None
        except Exception as exc:
            if isinstance(exc, OSError) and not isinstance(exc, TimeoutError):
                # Infrastructure interruption is retryable with the same identity.
                # The unpublished staging directory documents the attempt lineage.
                raise
            status = "failed"
            failure_class, failure_code = _classify_failure(exc, spec.method.kind)
            denominator_failure_class = statistical_failure_class(failure_class)
            if not trajectory_path.exists():
                _atomic_write_bytes(trajectory_path, b"")
            if not (staging / "resources.json").exists():
                _assert_public_control_safe(
                    resource_report,
                    runtime=runtime,
                    label="resource accounting failure report",
                )
                _atomic_write_json(staging / "resources.json", resource_report)
            _atomic_write_json(
                staging / "result.json",
                {
                    "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
                    "artifact": "result",
                    "status": "no_verified_result",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "attempt_id": attempt_id,
                },
            )
            _atomic_write_json(
                staging / "failure.json",
                {
                    "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
                    "artifact": "failure",
                    "status": "failed",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "attempt_id": attempt_id,
                    "failure_class": failure_class,
                    "statistical_failure_class": denominator_failure_class,
                    "failure_code": failure_code,
                    "exception_type": type(exc).__name__,
                    "message": _safe_failure_message(failure_code),
                    "retained_in_denominator": True,
                    "automatic_retry": False,
                },
            )
            _atomic_write_json(
                staging / "replay.json",
                {
                    "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
                    "artifact": "replay",
                    "verified": False,
                    "status": "not_available_or_failed",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "trajectory_sha256": file_sha256(trajectory_path),
                },
            )

        _call_fault_hook(fault_hook, "before_artifact_index", staging)
        artifact_index = _build_artifact_index(staging, spec=spec, status=status)
        _atomic_write_json(staging / "artifact-index.json", artifact_index)
        _call_fault_hook(fault_hook, "before_completion_marker", staging)
        completion = {
            "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
            "artifact": "completion_marker",
            "cell_identity_sha256": spec.cell_identity_sha256,
            "run_manifest_sha256": issued_cell.run_manifest_sha256,
            "attempt_id": attempt_id,
            "status": status,
            "failure_class": failure_class,
            "completed_at": _utc_now(),
            "artifact_index_sha256": file_sha256(staging / "artifact-index.json"),
            "completion_marker_written_last": True,
        }
        _atomic_write_json(staging / "completion.json", completion)
        _fsync_directory(staging)
        _call_fault_hook(fault_hook, "before_publish", staging)
        cell_dir.parent.mkdir(parents=True, exist_ok=True)
        if cell_dir.exists():
            raise CellIntegrityError("cell destination appeared during locked execution")
        os.replace(staging, cell_dir)
        _fsync_directory(cell_dir.parent)
        _call_fault_hook(fault_hook, "after_publish", cell_dir)

        return validate_published_cell(cell_dir, expected_cell=issued_cell)


def validate_published_cell(
    cell_dir: str | Path, *, expected_cell: IssuedFormalCell | None = None
) -> CellRunOutcome:
    """Fail closed on missing, partial, identity-mismatched, or digest-tampered cells."""

    path = Path(cell_dir).resolve()
    required = {
        "manifest.json",
        "trajectory.jsonl",
        "result.json",
        "failure.json",
        "replay.json",
        "resources.json",
        "artifact-index.json",
        "completion.json",
    }
    observed = {item.name for item in path.iterdir()} if path.is_dir() else set()
    if not path.is_dir() or observed != required:
        raise CellIntegrityError("published cell artifact set is incomplete or undeclared")
    if any((path / name).is_symlink() or not (path / name).is_file() for name in required):
        raise CellIntegrityError("published cell contains a non-regular artifact")
    completion = _read_object(path / "completion.json")
    index = _read_object(path / "artifact-index.json")
    manifest = _read_object(path / "manifest.json")
    if completion.get("schema_version") != FORMAL_CELL_ARTIFACT_VERSION:
        raise CellIntegrityError("unsupported cell completion schema")
    if completion.get("completion_marker_written_last") is not True:
        raise CellIntegrityError("cell completion marker order is not certified")
    if file_sha256(path / "artifact-index.json") != completion.get("artifact_index_sha256"):
        raise CellIntegrityError("cell artifact index digest mismatch")
    files = index.get("files")
    indexed_files = required - {"artifact-index.json", "completion.json"}
    if not isinstance(files, Mapping) or set(files) != indexed_files:
        raise CellIntegrityError("cell artifact index has an invalid file set")
    for name, expected_digest in files.items():
        if not isinstance(name, str) or file_sha256(path / name) != expected_digest:
            raise CellIntegrityError(f"cell artifact digest mismatch: {name}")
    cell_payload = manifest.get("cell")
    if not isinstance(cell_payload, Mapping):
        raise CellIntegrityError("cell manifest does not contain an issued cell")
    try:
        spec = FormalCellSpec.from_payload(cell_payload)
    except CellIdentityError as exc:
        raise CellIntegrityError("published cell identity is invalid") from exc
    identity = spec.cell_identity_sha256
    if path.name != identity:
        raise CellIntegrityError("cell directory does not match its identity")
    for artifact in (completion, index, manifest):
        artifact_identity = artifact.get("cell_identity_sha256")
        if artifact is manifest:
            artifact_identity = cell_payload.get("cell_identity_sha256")
        if artifact_identity != identity:
            raise CellIntegrityError("published artifact identity mismatch")
    manifest_digest = manifest.get("run_manifest_sha256")
    if completion.get("run_manifest_sha256") != manifest_digest:
        raise CellIntegrityError("published run-manifest binding mismatch")
    if expected_cell is not None and (
        expected_cell.spec.cell_identity_sha256 != identity
        or expected_cell.run_manifest_sha256 != manifest_digest
    ):
        raise CellIntegrityError("published cell does not match the requested issued identity")
    status = completion.get("status")
    if status not in {"succeeded", "failed"} or index.get("status") != status:
        raise CellIntegrityError("published cell has an incoherent terminal status")
    result = _read_object(path / "result.json")
    failure = _read_object(path / "failure.json")
    replay = _read_object(path / "replay.json")
    resources = _read_object(path / "resources.json")
    if (
        resources.get("schema_version") != RESOURCE_ACCOUNTING_VERSION
        or resources.get("cell_identity_sha256") != identity
        or resources.get("method_id") != spec.method.method_id
        or resources.get("method_kind") != spec.method.kind
        or resources.get("resource_profile") != spec.method.resource_profile
    ):
        raise CellIntegrityError("cell resource artifact binding is invalid")
    if status == "succeeded":
        if (
            result.get("verified") is not True
            or replay.get("verified") is not True
            or failure.get("status") != "no_failure"
            or resources.get("accounting_complete") is not True
        ):
            raise CellIntegrityError("successful cell lacks verified terminal artifacts")
        if result.get("trajectory_path") != str((path / "trajectory.jsonl").resolve()):
            raise CellIntegrityError("successful result points at a different trajectory")
        if result.get("trajectory_sha256") != file_sha256(path / "trajectory.jsonl"):
            raise CellIntegrityError("successful result trajectory digest mismatch")
        failure_class = None
    else:
        failure_class = failure.get("failure_class")
        denominator_failure_class = failure.get("statistical_failure_class")
        if (
            result.get("status") != "no_verified_result"
            or failure.get("status") != "failed"
            or not isinstance(failure_class, str)
            or denominator_failure_class != statistical_failure_class(failure_class)
        ):
            raise CellIntegrityError("failed cell lacks a classified terminal artifact")
    typed_status: CellStatus = "succeeded" if status == "succeeded" else "failed"
    return CellRunOutcome(
        cell_identity_sha256=identity,
        status=typed_status,
        cell_dir=path,
        cached=False,
        failure_class=failure_class,
    )


def canonical_sha256(payload: Any) -> str:
    """Return the stable JSON SHA-256 used by manifests and private commitments."""

    _assert_finite_json(payload, "canonical payload")
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_trajectory(
    path: Path, *, spec: FormalCellSpec, runtime: PrivateCellRuntime
) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
        raise TrajectoryContractError("adapter did not produce a non-empty trajectory")
    try:
        records = load_jsonl(path)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise TrajectoryContractError("trajectory is not valid JSONL") from exc
    if not records or not all(isinstance(record, dict) for record in records):
        raise TrajectoryContractError("trajectory must contain JSON objects")
    try:
        _assert_finite_json(records, "trajectory")
    except CellIdentityError as exc:
        raise MissingOrNonfiniteMetricError("trajectory contains non-finite data") from exc
    if len(records) > spec.operation_limit:
        raise BudgetOverrunError("trajectory operation count exceeds the issued limit")
    for expected_step, record in enumerate(records, start=1):
        if record.get("step") != expected_step:
            raise TrajectoryContractError("trajectory steps must be consecutive and one-indexed")
        expected_bindings = {
            "benchmark_task_id": spec.task_id,
            "formal_cell_identity_sha256": spec.cell_identity_sha256,
            "formal_method_id": spec.method.method_id,
            "formal_pair_id": spec.pair_id,
            "formal_spectrum_condition": spec.spectrum_condition,
            "seed": runtime.world_seed,
        }
        if any(record.get(field) != value for field, value in expected_bindings.items()):
            raise TrajectoryContractError("trajectory record does not match its formal cell")
    ledger = records[-1].get("method_resources")
    if not isinstance(ledger, Mapping):
        raise IncompleteAccountingError("trajectory is missing its final method ledger")
    if ledger.get("accounting_complete") is not True:
        raise IncompleteAccountingError("trajectory method accounting is incomplete")
    operation_count = ledger.get("operation_count")
    experiment_count = ledger.get("complete_experiment_count")
    if (
        isinstance(operation_count, bool)
        or not isinstance(operation_count, int)
        or operation_count != len(records)
    ):
        raise IncompleteAccountingError("method ledger operation count is incoherent")
    if not isinstance(experiment_count, int) or isinstance(experiment_count, bool):
        raise IncompleteAccountingError("method ledger experiment count is invalid")
    if experiment_count > spec.complete_experiments:
        raise BudgetOverrunError("complete-experiment count exceeds the issued budget")
    if experiment_count < spec.complete_experiments:
        raise TrajectoryContractError("cell ended before its complete-experiment budget")
    return records


def _audit_formal_resource_evidence(
    records: list[dict[str, Any]], *, spec: FormalCellSpec
) -> dict[str, Any]:
    raw_evidence = records[-1].get("formal_resource_evidence", {})
    if not isinstance(raw_evidence, Mapping):
        return unavailable_resource_accounting_report(
            cell_identity_sha256=spec.cell_identity_sha256,
            method_id=spec.method.method_id,
            method_kind=spec.method.kind,
            resource_profile=spec.method.resource_profile,
            reason="formal_resource_evidence_invalid",
            rl_checkpoint_sha256=spec.method.checkpoint_sha256,
        )
    provider_receipts = raw_evidence.get("provider_receipts", [])
    classic_events = raw_evidence.get("classic_compute_events", [])
    if not isinstance(provider_receipts, list) or not all(
        isinstance(item, Mapping) for item in provider_receipts
    ):
        return unavailable_resource_accounting_report(
            cell_identity_sha256=spec.cell_identity_sha256,
            method_id=spec.method.method_id,
            method_kind=spec.method.kind,
            resource_profile=spec.method.resource_profile,
            reason="provider_receipt_evidence_invalid",
            rl_checkpoint_sha256=spec.method.checkpoint_sha256,
        )
    if not isinstance(classic_events, list) or not all(
        isinstance(item, Mapping) for item in classic_events
    ):
        return unavailable_resource_accounting_report(
            cell_identity_sha256=spec.cell_identity_sha256,
            method_id=spec.method.method_id,
            method_kind=spec.method.kind,
            resource_profile=spec.method.resource_profile,
            reason="classic_compute_evidence_invalid",
            rl_checkpoint_sha256=spec.method.checkpoint_sha256,
        )
    pricing = raw_evidence.get("pricing_snapshot")
    if pricing is not None and not isinstance(pricing, Mapping):
        pricing = None
    classic_compute_required = spec.method.method_id.startswith(("structured_", "gp_", "rf_"))
    return audit_cell_resource_accounting(
        records,
        cell_identity_sha256=spec.cell_identity_sha256,
        method_id=spec.method.method_id,
        method_kind=spec.method.kind,
        resource_profile=spec.method.resource_profile,
        provider_receipts=provider_receipts,
        pricing_snapshot=pricing,
        classic_compute_events=classic_events,
        classic_compute_required=classic_compute_required,
        rl_checkpoint_sha256=spec.method.checkpoint_sha256,
    )


def _default_replay_evaluator(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del spec
    try:
        result = build_verified_evaluation_result(
            records,
            trajectory_path=trajectory_path,
            world_interventions=runtime.world_interventions,
        )
    except ValueError as exc:
        raise ReplayMismatchError("independent trajectory replay failed") from exc
    verification = result.get("verification")
    if not isinstance(verification, Mapping) or verification.get("verified") is not True:
        raise ReplayMismatchError("independent trajectory replay did not verify")
    replay = {
        "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
        "artifact": "replay",
        "status": "verified",
        "verified": True,
        "engine": "chemworld.eval.verify.verify_records",
        "verification": dict(verification),
    }
    return result, replay


def _validate_replay_payload(
    result: Mapping[str, Any], replay: Mapping[str, Any], *, trajectory_path: Path
) -> None:
    digest = file_sha256(trajectory_path)
    if result.get("verified") is not True or replay.get("verified") is not True:
        raise ReplayMismatchError("replay evaluator returned an unverified result")
    result_digest = result.get("trajectory_sha256")
    if result_digest is not None and result_digest != digest:
        raise ReplayMismatchError("replay result is bound to another trajectory")
    try:
        _assert_finite_json(result, "evaluation result")
        _assert_finite_json(replay, "replay report")
    except CellIdentityError as exc:
        raise MissingOrNonfiniteMetricError(
            "evaluation result or replay report contains non-finite data"
        ) from exc


def _result_binding(
    spec: FormalCellSpec, run_manifest_sha256: str, attempt_id: str
) -> dict[str, Any]:
    return {
        "formal_cell_schema_version": FORMAL_CELL_VERSION,
        "cell_identity_sha256": spec.cell_identity_sha256,
        "run_manifest_sha256": run_manifest_sha256,
        "attempt_id": attempt_id,
        "formal_bindings": {
            "protocol_sha256": spec.protocol_sha256,
            "backend_semantic_sha256": spec.backend_semantic_sha256,
            "evaluator_sha256": spec.evaluator_sha256,
            "interaction_protocol_sha256": spec.interaction_protocol_sha256,
            "statistics_protocol_sha256": spec.statistics_protocol_sha256,
            "reference_manifest_sha256": spec.reference_manifest_sha256,
            "method": asdict(spec.method),
            "source_commit": spec.source_commit,
        },
    }


def _sanitize_result_for_public_control(
    result: Mapping[str, Any], *, spec: FormalCellSpec, runtime: PrivateCellRuntime
) -> dict[str, Any]:
    """Replace the generic raw seed field with the issued opaque pair identity."""

    sanitized = dict(result)
    recorded_seed = sanitized.pop("seed", None)
    if recorded_seed is not None and recorded_seed != runtime.world_seed:
        raise PrivateControlLeakError("evaluation result seed does not match private runtime")
    source_schema = sanitized.pop("result_schema_version", None)
    sanitized.update(
        {
            "result_schema_version": FORMAL_PUBLIC_RESULT_VERSION,
            "source_result_schema_version": source_schema,
            "pair_id": spec.pair_id,
            "private_seed_commitment": spec.private_seed_commitment,
            "raw_seed_reported": False,
        }
    )
    return sanitized


def _replay_binding(spec: FormalCellSpec, trajectory_path: Path) -> dict[str, Any]:
    return {
        "cell_identity_sha256": spec.cell_identity_sha256,
        "trajectory_sha256": file_sha256(trajectory_path),
        "private_runtime_values_in_artifact": False,
    }


def _build_artifact_index(
    staging: Path, *, spec: FormalCellSpec, status: CellStatus
) -> dict[str, Any]:
    names = (
        "manifest.json",
        "trajectory.jsonl",
        "result.json",
        "failure.json",
        "replay.json",
        "resources.json",
    )
    observed = {item.name for item in staging.iterdir()}
    if observed != set(names):
        raise OSError("cannot index a staging directory with undeclared artifacts")
    if any((staging / name).is_symlink() or not (staging / name).is_file() for name in names):
        raise OSError("cannot index an incomplete cell staging directory")
    return {
        "schema_version": FORMAL_CELL_ARTIFACT_VERSION,
        "artifact": "artifact_index",
        "cell_identity_sha256": spec.cell_identity_sha256,
        "status": status,
        "files": {name: file_sha256(staging / name) for name in names},
    }


def _classify_failure(exc: Exception, kind: MethodKind) -> tuple[str, str]:
    if isinstance(exc, BudgetOverrunError):
        return "budget_overrun", "issued_budget_exceeded"
    if isinstance(exc, IncompleteAccountingError):
        return "incomplete_resource_accounting", "required_ledger_missing_or_incoherent"
    if isinstance(exc, ReplayMismatchError):
        return "replay_mismatch", "independent_replay_failed"
    if isinstance(exc, MissingOrNonfiniteMetricError):
        return "missing_or_nonfinite_metric", "nonfinite_trajectory_or_evaluation"
    if isinstance(exc, PrivateControlLeakError):
        return "runtime_failure", "private_runtime_value_in_public_control"
    if isinstance(exc, TrajectoryContractError):
        return "runtime_failure", "invalid_or_incomplete_trajectory"
    if isinstance(exc, TimeoutError) and kind == "live_llm":
        return "provider_or_model_failure", "provider_timeout"
    if isinstance(exc, json.JSONDecodeError) and kind == "live_llm":
        return "provider_or_model_failure", "provider_bad_json"
    return "runtime_failure", "adapter_exception"


def _safe_failure_message(failure_code: str) -> str:
    return f"formal cell failed ({failure_code}); raw exception text is not published"


def _assert_public_control_safe(
    payload: Mapping[str, Any], *, runtime: PrivateCellRuntime, label: str
) -> None:
    """Reject direct private runtime values in artifacts intended for public summaries."""

    forbidden_keys = {
        "base_seed",
        "seed",
        "method_seed",
        "world_seed",
        "seed_nonce",
        "world_nonce",
        "world_interventions",
    }
    forbidden_values = (runtime.seed_nonce, runtime.world_nonce)

    def visit(value: Any) -> None:
        if isinstance(value, Mapping):
            if forbidden_keys.intersection(str(key) for key in value):
                raise PrivateControlLeakError(f"{label} contains a private runtime field")
            for child in value.values():
                visit(child)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            for child in value:
                visit(child)
        elif any(type(value) is type(secret) and value == secret for secret in forbidden_values):
            raise PrivateControlLeakError(f"{label} contains a private runtime value")

    visit(payload)


class _CellLock:
    """Nonblocking OS advisory lock released automatically after process death."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle: Any = None

    def __enter__(self) -> Self:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._handle = self.path.open("a+b")
            self._handle.seek(0)
            if self._handle.read(1) == b"":
                self._handle.write(b"0")
                self._handle.flush()
            self._handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self._handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl: Any = importlib.import_module("fcntl")
                fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if self._handle is not None:
                self._handle.close()
            self._handle = None
            raise CellBusyError("formal cell is already running") from exc
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc, traceback
        if self._handle is None:
            return
        with suppress(OSError):
            self._handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl = importlib.import_module("fcntl")
                fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        self._handle.close()
        self._handle = None


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    _assert_finite_json(payload, str(path.name))
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _atomic_write_bytes(path, encoded)


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # One process owns an isolated attempt directory, so a fixed short name is
    # collision-free while avoiding Windows MAX_PATH failures in deep run roots.
    temporary = path.parent / ".tmp"
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    except BaseException:
        with suppress(OSError):
            temporary.unlink()
        raise


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    with suppress(OSError):
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _call_fault_hook(hook: FaultHook | None, stage: str, path: Path) -> None:
    if hook is not None:
        hook(stage, path)


def _read_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CellIntegrityError(f"cannot read cell artifact: {path.name}") from exc
    if not isinstance(payload, dict):
        raise CellIntegrityError(f"cell artifact is not a JSON object: {path.name}")
    return payload


def _required_text(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise CellIdentityError(f"{field} must be a non-empty string")
    return value


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise CellIdentityError("optional method bindings must be non-empty strings")
    return value


def _required_positive_int(payload: Mapping[str, Any], field: str) -> int:
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CellIdentityError(f"{field} must be a positive integer")
    return value


def _required_nonnegative_int(payload: Mapping[str, Any], field: str) -> int:
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CellIdentityError(f"{field} must be a non-negative integer")
    return value


def _require_sha256(value: Any, label: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise CellIdentityError(f"{label} must be a SHA-256 digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CellIdentityError(f"{label} must be a SHA-256 digest") from exc


def _is_git_commit(value: str) -> bool:
    if len(value) != 40:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _assert_finite_json(value: Any, label: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise CellIdentityError(f"{label} contains a non-finite number")
    if isinstance(value, Mapping):
        for child in value.values():
            _assert_finite_json(child, label)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            _assert_finite_json(child, label)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def discard_incomplete_staging(output_root: str | Path, *, cell_identity_sha256: str) -> int:
    """Explicitly remove unpublished attempts after inspection; never touch published cells."""

    _require_sha256(cell_identity_sha256, "cell identity")
    root = Path(output_root).resolve()
    staging_root = root / ".staging"
    published = root / "cells" / cell_identity_sha256
    if published.exists():
        raise CellIntegrityError("refusing to discard staging for a published cell")
    if not staging_root.is_dir():
        return 0
    candidates = sorted(staging_root.glob(f"{cell_identity_sha256[:16]}-*"))
    removed = 0
    for candidate in candidates:
        if not candidate.is_dir() or candidate.is_symlink():
            raise CellIntegrityError("incomplete staging candidate is not a regular directory")
        manifest_path = candidate / "manifest.json"
        if manifest_path.is_file():
            manifest = _read_object(manifest_path)
            cell = manifest.get("cell")
            if (
                not isinstance(cell, Mapping)
                or cell.get("cell_identity_sha256") != cell_identity_sha256
            ):
                raise CellIntegrityError("staging prefix collision or identity mismatch")
        shutil.rmtree(candidate)
        removed += 1
    return removed


__all__ = [
    "FORMAL_CELL_ARTIFACT_VERSION",
    "FORMAL_CELL_VERSION",
    "FORMAL_PUBLIC_RESULT_VERSION",
    "FORMAL_RUN_MANIFEST_VERSION",
    "STATISTICAL_FAILURE_CLASSES",
    "BudgetOverrunError",
    "CellBusyError",
    "CellIdentityError",
    "CellIntegrityError",
    "CellRunOutcome",
    "FormalAdapterRegistry",
    "FormalCellSpec",
    "FormalExecutionAdapter",
    "FormalMethodBinding",
    "FormalRunnerError",
    "IncompleteAccountingError",
    "IssuedFormalCell",
    "MissingOrNonfiniteMetricError",
    "PrivateCellRuntime",
    "PrivateControlLeakError",
    "ReplayMismatchError",
    "TrajectoryContractError",
    "canonical_sha256",
    "discard_incomplete_staging",
    "file_sha256",
    "issue_run_manifest",
    "load_issued_cell",
    "private_seed_commitment",
    "private_world_commitment",
    "run_formal_cell",
    "statistical_failure_class",
    "validate_published_cell",
]
