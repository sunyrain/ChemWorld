"""No-bypass preflight issuer for formal ChemWorld run manifests."""

from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeGuard

from chemworld.eval.formal_matrix import build_formal_matrix_plan
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    FormalMethodBinding,
    canonical_sha256,
    issue_run_manifest,
    private_seed_commitment,
    private_world_commitment,
)
from chemworld.eval.resource_accounting_v0_4 import (
    PROVIDER_PRICING_VERSION,
    audit_rl_training_resource,
)

PREFLIGHT_REQUEST_VERSION = "chemworld-formal-preflight-request-0.4"
PREFLIGHT_REPORT_VERSION = "chemworld-formal-preflight-report-0.4"
PREFLIGHT_PRIVATE_ASSIGNMENT_VERSION = "chemworld-private-assignment-0.4"

_CONTROL_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "backend_release": {
        "schema_version": "chemworld-backend-release-manifest-0.1",
        "portable_release_ready": True,
        "release_status": "formal_candidate",
    },
    "formal_protocol": {"controls_ready": True, "formal_results_present": False},
    "interaction_strata": {"controls_ready": True, "formal_results_present": False},
    "statistical_plan": {"controls_ready": True, "formal_results_present": False},
    "reference_plan": {"controls_ready": True, "formal_results_present": False},
    "method_protocol": {"controls_ready": True, "formal_results_present": False},
    "formal_runner": {"controls_ready": True, "formal_results_present": False},
    "formal_matrix": {"controls_ready": True, "formal_results_present": False},
    "resource_accounting": {"controls_ready": True, "formal_results_present": False},
}


@dataclass(frozen=True)
class PreflightOutcome:
    """Public report plus issued artifacts when every gate passes."""

    report: dict[str, Any]
    run_manifest: dict[str, Any] | None
    private_runtimes: dict[str, dict[str, Any]] | None

    @property
    def passed(self) -> bool:
        return self.run_manifest is not None and self.report.get("passed") is True


def run_formal_preflight(
    request: Mapping[str, Any],
    private_assignments: Mapping[str, Any],
    *,
    repository_root: str | Path,
    source_probe: Mapping[str, Any] | None = None,
    resource_probe: Mapping[str, Any] | None = None,
) -> PreflightOutcome:
    """Audit every formal dependency and issue one immutable manifest on success."""

    root = Path(repository_root).resolve()
    blockers: list[str] = []
    controls: dict[str, bool] = {}
    artifacts: dict[str, dict[str, Any]] = {}

    controls["request_schema"] = request.get("schema_version") == PREFLIGHT_REQUEST_VERSION
    purpose = request.get("purpose")
    controls["purpose"] = purpose in {"nonformal_smoke", "formal_bench"}
    cohort_nonce = request.get("cohort_nonce")
    controls["cohort_nonce"] = isinstance(cohort_nonce, str) and len(cohort_nonce) >= 16

    source = request.get("source")
    if not isinstance(source, Mapping):
        source = {}
    source_state = dict(source_probe) if source_probe is not None else probe_repository(root)
    expected_commit = source.get("expected_commit")
    controls["source_commit"] = (
        _is_git_commit(expected_commit)
        and source_state.get("commit") == expected_commit
    )
    controls["clean_source"] = source_state.get("clean") is True
    source_artifact = source.get("artifact")
    controls["source_artifact"] = _audit_file_binding(
        source_artifact,
        root=root,
        label="source_artifact",
        artifacts=artifacts,
    )
    controls["source_artifact_kind"] = (
        source.get("artifact_kind") == "wheel"
        and isinstance(source_artifact, Mapping)
        and str(source_artifact.get("path", "")).endswith(".whl")
    )
    controls["source_artifact_commit"] = (
        isinstance(source_artifact, Mapping)
        and source_artifact.get("source_commit") == expected_commit
    )
    artifact_sha = source_artifact.get("sha256") if isinstance(source_artifact, Mapping) else None
    source_manifest_valid, source_manifest_payload = _audit_json_binding(
        source.get("artifact_manifest"),
        root=root,
        label="source_artifact_manifest",
        requirements={
            "schema_version": "chemworld-source-artifact-manifest-0.4",
            "source_commit": expected_commit,
            "artifact_sha256": artifact_sha,
            "clean_build": True,
        },
        artifacts=artifacts,
    )
    controls["source_artifact_manifest"] = source_manifest_valid

    control_bindings = request.get("control_artifacts")
    if not isinstance(control_bindings, Mapping):
        control_bindings = {}
    loaded_controls: dict[str, dict[str, Any]] = {}
    for name, requirements in _CONTROL_REQUIREMENTS.items():
        valid, payload = _audit_json_binding(
            control_bindings.get(name),
            root=root,
            label=name,
            requirements=requirements,
            artifacts=artifacts,
        )
        controls[f"control_{name}"] = valid
        if payload is not None:
            loaded_controls[name] = payload
    controls["dependency_lock_binding"] = (
        source_manifest_payload is not None
        and source_manifest_payload.get("dependency_lock_sha256")
        == loaded_controls.get("backend_release", {}).get("dependency_lock_sha256")
        and _is_sha256(source_manifest_payload.get("dependency_lock_sha256"))
    )
    if purpose == "formal_bench":
        release_valid, _ = _audit_json_binding(
            request.get("formal_release_artifact"),
            root=root,
            label="formal_release_artifact",
            requirements={"controls_ready": True, "status": "bench_unsealed"},
            artifacts=artifacts,
        )
        controls["formal_release_artifact"] = release_valid
        controls["formal_method_matrix_ready"] = (
            loaded_controls.get("method_protocol", {}).get("formal_method_matrix_ready")
            is True
        )
        controls["reference_evidence_ready"] = (
            loaded_controls.get("reference_plan", {}).get("status")
            == "reference_evidence_ready"
        )
    else:
        controls["formal_release_artifact"] = True
        controls["formal_method_matrix_ready"] = True
        controls["reference_evidence_ready"] = True

    cell_bindings = request.get("cell_bindings")
    if not isinstance(cell_bindings, Mapping):
        cell_bindings = {}
    controls["cell_bindings"] = _audit_cell_bindings(
        cell_bindings,
        loaded_controls=loaded_controls,
        root=root,
        artifacts=artifacts,
    )

    matrix = request.get("matrix_contract")
    if not isinstance(matrix, Mapping):
        matrix = {}
    orchestration = request.get("orchestration")
    if not isinstance(orchestration, Mapping):
        orchestration = {}
    method_payloads = request.get("methods")
    if not isinstance(method_payloads, list):
        method_payloads = []
    methods, method_reports, training_resources = _audit_methods(
        method_payloads,
        matrix=matrix,
        registrations=loaded_controls.get("interaction_strata", {}).get(
            "capability_matrix"
        ),
        root=root,
        artifacts=artifacts,
        blockers=blockers,
    )
    controls["methods"] = len(methods) == len(method_payloads) and bool(methods)
    controls["interaction_tracks"] = {
        summary.get("track") for summary in method_reports if summary.get("formal_ready") is True
    } == {"recipe_level", "operation_level"}
    controls["matrix_contract"] = _audit_matrix_contract(
        matrix,
        methods=methods,
    )

    private, private_summary = _audit_private_assignments(
        private_assignments,
        matrix=matrix,
        public_split_summary=loaded_controls.get("formal_protocol", {}).get(
            "public_split_summary"
        ),
        blockers=blockers,
    )
    controls["private_assignments"] = private is not None

    resources = dict(resource_probe) if resource_probe is not None else probe_resources(
        root,
        request=request,
    )
    controls["infrastructure"] = _audit_infrastructure(
        resources,
        orchestration=orchestration,
        matrix=matrix,
        methods=methods,
        request=request,
        blockers=blockers,
    )

    blockers.extend(name for name, passed in controls.items() if not passed)
    blockers = sorted(set(blockers))
    request_digest = canonical_sha256(dict(request))
    public_base = {
        "schema_version": PREFLIGHT_REPORT_VERSION,
        "passed": False,
        "status": "rejected",
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "request_sha256": request_digest,
        "source_commit": (
            source_state.get("commit")
            if _is_git_commit(source_state.get("commit"))
            else None
        ),
        "source_tree_clean": source_state.get("clean") is True,
        "controls": controls,
        "blockers": blockers,
        "artifact_bindings": artifacts,
        "method_summary": method_reports,
        "private_assignment_summary": private_summary,
        "resource_probe_summary": _public_resource_summary(resources),
        "raw_private_seeds_reported": False,
        "private_world_parameters_reported": False,
        "api_secret_reported": False,
        "force_override_available": False,
    }
    if blockers or private is None:
        return PreflightOutcome(public_base, None, None)

    if not isinstance(cohort_nonce, str) or not isinstance(expected_commit, str):
        raise RuntimeError("preflight blockers failed to retain issuance identity errors")
    run_id = canonical_sha256(
        {
            "schema_version": PREFLIGHT_REPORT_VERSION,
            "request_sha256": request_digest,
            "source_commit": expected_commit,
            "cohort_nonce_sha256": hashlib.sha256(cohort_nonce.encode("utf-8")).hexdigest(),
            "unique_issuance_nonce": secrets.token_hex(16),
        }
    )
    try:
        cells, runtimes = _build_cells(
            run_id=run_id,
            matrix=matrix,
            methods=methods,
            private=private,
            cell_bindings=cell_bindings,
            source_commit=expected_commit,
        )
        manifest = issue_run_manifest(
            cells,
            metadata={
                "preflight": {
                    "schema_version": PREFLIGHT_REPORT_VERSION,
                    "request_sha256": request_digest,
                    "source_commit": expected_commit,
                    "source_artifact_sha256": artifacts["source_artifact"]["sha256"],
                    "control_artifact_sha256": {
                        name: artifacts[name]["sha256"] for name in _CONTROL_REQUIREMENTS
                    },
                    "raw_private_values_in_manifest": False,
                    "force_override_available": False,
                },
                "matrix_contract": dict(matrix),
                "orchestration": dict(orchestration),
                "rl_training_resources": training_resources,
                "method_resource_bindings": {
                    str(raw["method_id"]): {
                        "resource_profile": raw.get("resource_profile"),
                        "pricing_version_sha256": (
                            raw.get("pricing_snapshot", {}).get("pricing_version_sha256")
                            if isinstance(raw.get("pricing_snapshot"), Mapping)
                            else None
                        ),
                        "checkpoint_sha256": (
                            raw.get("checkpoint", {}).get("sha256")
                            if isinstance(raw.get("checkpoint"), Mapping)
                            else None
                        ),
                    }
                    for raw in method_payloads
                    if isinstance(raw, Mapping) and isinstance(raw.get("method_id"), str)
                },
            },
        )
        plan = build_formal_matrix_plan(manifest)
    except (KeyError, TypeError, ValueError, RuntimeError) as exc:
        failed = dict(public_base)
        failed["blockers"] = sorted(
            {*blockers, f"manifest_construction:{type(exc).__name__}"}
        )
        return PreflightOutcome(failed, None, None)

    report = {
        **public_base,
        "passed": True,
        "status": "issued_nonformal_smoke" if purpose == "nonformal_smoke" else "issued_formal",
        "blockers": [],
        "run_id": run_id,
        "run_manifest_sha256": manifest["run_manifest_sha256"],
        "matrix_plan_sha256": plan.matrix_plan_sha256,
        "issued_cell_count": len(cells),
        "private_runtime_file_count": len(runtimes),
        "private_runtime_values_in_public_report": False,
        "method_summary": method_reports,
    }
    return PreflightOutcome(report, manifest, runtimes)


def probe_repository(root: Path) -> dict[str, Any]:
    """Read the current Git commit and cleanliness without mutating the worktree."""

    try:
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "clean": False}
    return {"commit": commit, "clean": not status.strip()}


def probe_resources(root: Path, *, request: Mapping[str, Any]) -> dict[str, Any]:
    """Probe local capacity without exposing credential values."""

    infrastructure = request.get("infrastructure")
    if not isinstance(infrastructure, Mapping):
        infrastructure = {}
    api_env = infrastructure.get("api_key_env")
    gpu_env = os.getenv("CHEMWORLD_FORMAL_GPU_DEVICES", "")
    gpu_devices = [item.strip() for item in gpu_env.split(",") if item.strip()]
    return {
        "cpu_count": os.cpu_count() or 1,
        "free_disk_bytes": shutil.disk_usage(root).free,
        "gpu_devices": gpu_devices,
        "api_credential_available": (
            isinstance(api_env, str) and bool(os.getenv(api_env, "").strip())
        ),
        "api_max_concurrency": _env_positive_int("CHEMWORLD_API_MAX_CONCURRENCY"),
        "api_requests_per_minute": _env_positive_int("CHEMWORLD_API_REQUESTS_PER_MINUTE"),
        "api_monetary_quota_usd": _env_nonnegative_float("CHEMWORLD_API_COST_QUOTA_USD"),
    }


def _audit_file_binding(
    raw: Any,
    *,
    root: Path,
    label: str,
    artifacts: dict[str, dict[str, Any]],
) -> bool:
    if not isinstance(raw, Mapping):
        return False
    relative = raw.get("path")
    supplied = raw.get("sha256")
    path = _safe_repo_path(root, relative)
    if path is None or path.is_symlink() or not path.is_file() or not _is_sha256(supplied):
        return False
    observed = _file_sha256(path)
    if observed != supplied:
        return False
    artifacts[label] = {"path": str(relative), "sha256": observed}
    return True


def _audit_json_binding(
    raw: Any,
    *,
    root: Path,
    label: str,
    requirements: Mapping[str, Any],
    artifacts: dict[str, dict[str, Any]],
) -> tuple[bool, dict[str, Any] | None]:
    if not _audit_file_binding(raw, root=root, label=label, artifacts=artifacts):
        return False, None
    if not isinstance(raw, Mapping):
        return False, None
    path = _safe_repo_path(root, raw.get("path"))
    if path is None:
        return False, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False, None
    if not isinstance(payload, dict):
        return False, None
    valid = all(payload.get(field) == expected for field, expected in requirements.items())
    return valid, payload


def _audit_cell_bindings(
    bindings: Mapping[str, Any],
    *,
    loaded_controls: Mapping[str, Mapping[str, Any]],
    root: Path,
    artifacts: dict[str, dict[str, Any]],
) -> bool:
    expected_fields = {
        "protocol_sha256": ("formal_protocol", "protocol_sha256"),
        "backend_semantic_sha256": ("backend_release", "backend_semantic_sha256"),
        "interaction_protocol_sha256": ("interaction_strata", "protocol_sha256"),
        "statistics_protocol_sha256": ("statistical_plan", "analysis_plan_sha256"),
        "reference_manifest_sha256": ("reference_plan", "run_plan_sha256"),
    }
    valid = True
    for field, (control, source_field) in expected_fields.items():
        value = bindings.get(field)
        valid = valid and _is_sha256(value)
        payload = loaded_controls.get(control, {})
        valid = valid and payload.get(source_field) == value
    evaluator = bindings.get("evaluator_artifact")
    evaluator_valid = _audit_file_binding(
        evaluator,
        root=root,
        label="evaluator_artifact",
        artifacts=artifacts,
    )
    valid = valid and evaluator_valid
    if isinstance(evaluator, Mapping):
        valid = valid and bindings.get("evaluator_sha256") == evaluator.get("sha256")
    return bool(valid)


def _audit_methods(
    payloads: Sequence[Any],
    *,
    matrix: Mapping[str, Any],
    registrations: Any,
    root: Path,
    artifacts: dict[str, dict[str, Any]],
    blockers: list[str],
) -> tuple[dict[str, FormalMethodBinding], list[dict[str, Any]], list[dict[str, Any]]]:
    methods: dict[str, FormalMethodBinding] = {}
    summaries: list[dict[str, Any]] = []
    training_by_checkpoint: dict[str, dict[str, Any]] = {}
    spectrum_contract = matrix.get("spectrum_conditions_by_method")
    if not isinstance(spectrum_contract, Mapping):
        spectrum_contract = {}
    for index, raw in enumerate(payloads):
        if not isinstance(raw, Mapping):
            blockers.append(f"method:{index}:invalid")
            continue
        method_id = raw.get("method_id")
        if not isinstance(method_id, str) or not method_id.strip() or method_id in methods:
            blockers.append(f"method:{index}:identity_invalid")
            continue
        method_blockers: list[str] = []
        if raw.get("implementation_status") != "formal_ready":
            method_blockers.append("implementation_not_formal_ready")
        artifact_label = f"method:{method_id}:artifact"
        if not _audit_file_binding(
            raw.get("artifact"), root=root, label=artifact_label, artifacts=artifacts
        ):
            method_blockers.append("artifact_invalid")
        declared_conditions = raw.get("spectrum_conditions")
        if (
            not isinstance(declared_conditions, list)
            or declared_conditions != spectrum_contract.get(method_id)
        ):
            method_blockers.append("spectrum_contract_mismatch")
        kind = raw.get("kind")
        resource_profile = raw.get("resource_profile")
        expected_track = (
            "recipe_level" if resource_profile == "classic_recipe" else "operation_level"
        )
        if raw.get("track") != expected_track:
            method_blockers.append("track_resource_profile_mismatch")
        registration = (
            registrations.get(method_id) if isinstance(registrations, Mapping) else None
        )
        if not isinstance(registration, Mapping):
            method_blockers.append("interaction_registration_missing")
        elif any(
            registration.get(field) != raw.get(field)
            for field in ("track", "resource_profile", "spectrum_conditions")
        ):
            method_blockers.append("interaction_registration_mismatch")
        kwargs: dict[str, Any] = {}
        if kind == "rl":
            checkpoint_label = f"method:{method_id}:checkpoint"
            checkpoint = raw.get("checkpoint")
            if not _audit_file_binding(
                checkpoint,
                root=root,
                label=checkpoint_label,
                artifacts=artifacts,
            ):
                method_blockers.append("checkpoint_invalid")
            elif isinstance(checkpoint, Mapping):
                kwargs["checkpoint_sha256"] = checkpoint.get("sha256")
            training = raw.get("training_resources")
            if not isinstance(training, Mapping):
                method_blockers.append("training_resources_missing")
            else:
                audited = audit_rl_training_resource(training)
                if audited.get("accounting_complete") is not True:
                    method_blockers.append("training_resources_incomplete")
                elif audited.get("checkpoint_sha256") != kwargs.get("checkpoint_sha256"):
                    method_blockers.append("training_checkpoint_mismatch")
                else:
                    checkpoint_sha = str(audited["checkpoint_sha256"])
                    training_by_checkpoint[checkpoint_sha] = dict(training)
        elif kind == "live_llm":
            for field in ("prompt", "model_config"):
                label = f"method:{method_id}:{field}"
                binding = raw.get(field)
                if not _audit_file_binding(
                    binding,
                    root=root,
                    label=label,
                    artifacts=artifacts,
                ):
                    method_blockers.append(f"{field}_invalid")
                elif isinstance(binding, Mapping):
                    kwargs[f"{field}_sha256"] = binding.get("sha256")
            if not _valid_pricing_snapshot(
                raw.get("pricing_snapshot"),
                expected_model=raw.get("provider_model_id"),
            ):
                method_blockers.append("pricing_snapshot_invalid")
        elif kind != "classic":
            method_blockers.append("kind_invalid")
        try:
            artifact_sha = artifacts.get(artifact_label, {}).get("sha256")
            binding = FormalMethodBinding(
                method_id=method_id,
                kind=kind,  # type: ignore[arg-type]
                artifact_sha256=str(artifact_sha),
                resource_profile=raw.get("resource_profile"),  # type: ignore[arg-type]
                **kwargs,
            )
        except (TypeError, ValueError, RuntimeError):
            method_blockers.append("formal_binding_invalid")
            binding = None
        if not method_blockers and binding is not None:
            methods[method_id] = binding
        blockers.extend(f"method:{method_id}:{reason}" for reason in method_blockers)
        summaries.append(
            {
                "method_id": method_id,
                "kind": kind,
                "track": raw.get("track"),
                "resource_profile": raw.get("resource_profile"),
                "formal_ready": not method_blockers,
                "blockers": sorted(set(method_blockers)),
            }
        )
    return methods, summaries, list(training_by_checkpoint.values())


def _audit_matrix_contract(
    matrix: Mapping[str, Any], *, methods: Mapping[str, FormalMethodBinding]
) -> bool:
    try:
        tasks = _unique_text_list(matrix.get("tasks"))
        method_ids = _unique_text_list(matrix.get("methods"))
        pair_ids = _unique_text_list(matrix.get("pair_ids"))
        checkpoints = _positive_int_list(matrix.get("checkpoints"))
        complete = _positive_int(matrix.get("complete_experiments_per_cell"))
        operation_limits = matrix.get("operation_limits_by_task")
        spectrum = matrix.get("spectrum_conditions_by_method")
    except ValueError:
        return False
    if method_ids != list(methods) or set(method_ids) != set(methods):
        return False
    if not all(pair_id.startswith("pair-opaque-") for pair_id in pair_ids):
        return False
    if checkpoints[-1] != complete:
        return False
    if not isinstance(operation_limits, Mapping) or set(operation_limits) != set(tasks):
        return False
    if any(_positive_int(operation_limits[task]) < complete for task in tasks):
        return False
    if not isinstance(spectrum, Mapping) or set(spectrum) != set(method_ids):
        return False
    for method_id, binding in methods.items():
        try:
            conditions = _unique_text_list(spectrum[method_id])
        except ValueError:
            return False
        if binding.kind == "live_llm":
            if not {"assigned", "masked"}.issubset(conditions):
                return False
        elif conditions != ["masked"]:
            return False
    return True


def _audit_private_assignments(
    raw: Mapping[str, Any],
    *,
    matrix: Mapping[str, Any],
    public_split_summary: Any,
    blockers: list[str],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    summary = {
        "schema_version": raw.get("schema_version"),
        "opaque_pair_count": 0,
        "task_count": 0,
        "raw_seed_values_reported": False,
        "private_world_parameters_reported": False,
    }
    if raw.get("schema_version") != PREFLIGHT_PRIVATE_ASSIGNMENT_VERSION:
        blockers.append("private_assignment_schema")
        return None, summary
    pairs = raw.get("pairs")
    pair_ids = matrix.get("pair_ids")
    tasks = matrix.get("tasks")
    split = raw.get("split")
    if (
        not isinstance(pairs, Mapping)
        or not isinstance(pair_ids, list)
        or set(pairs) != set(pair_ids)
        or not isinstance(tasks, list)
        or not isinstance(split, Mapping)
    ):
        blockers.append("private_assignment_grid")
        return None, summary
    namespace_id = split.get("namespace_id")
    access_state = split.get("bench_access_state")
    if (
        not isinstance(namespace_id, str)
        or not namespace_id.startswith("chemworld-v0.5-bench-private")
        or access_state != "sealed_unrun"
    ):
        blockers.append("private_split_namespace_or_state_invalid")
        return None, summary
    public_ranges = _public_seed_ranges(public_split_summary)
    if public_ranges is None:
        blockers.append("public_seed_ranges_missing_from_formal_protocol")
        return None, summary
    forbidden = split.get("forbidden_public_seeds")
    if not isinstance(forbidden, list) or not all(_is_nonnegative_int(item) for item in forbidden):
        blockers.append("private_seed_denylist_invalid")
        return None, summary
    forbidden_set = set(forbidden)
    seen_method: set[int] = set()
    seen_world: set[int] = set()
    valid = True
    normalized: dict[str, Any] = {}
    for pair_id in pair_ids:
        item = pairs[pair_id]
        if not isinstance(item, Mapping):
            valid = False
            continue
        method_seed = item.get("method_seed")
        method_nonce = item.get("seed_nonce")
        worlds = item.get("tasks")
        if (
            not _is_nonnegative_int(method_seed)
            or method_seed in forbidden_set
            or _in_seed_ranges(method_seed, public_ranges)
            or method_seed in seen_method
            or not isinstance(method_nonce, str)
            or not method_nonce
            or not isinstance(worlds, Mapping)
            or set(worlds) != set(tasks)
        ):
            valid = False
            continue
        seen_method.add(method_seed)
        normalized_worlds: dict[str, Any] = {}
        for task_id in tasks:
            world = worlds[task_id]
            if not isinstance(world, Mapping):
                valid = False
                continue
            world_seed = world.get("world_seed")
            world_nonce = world.get("world_nonce")
            interventions = world.get("world_interventions")
            if (
                not _is_nonnegative_int(world_seed)
                or world_seed in forbidden_set
                or _in_seed_ranges(world_seed, public_ranges)
                or world_seed in seen_world
                or not isinstance(world_nonce, str)
                or not world_nonce
                or not isinstance(interventions, list)
                or not all(isinstance(entry, Mapping) for entry in interventions)
            ):
                valid = False
                continue
            seen_world.add(world_seed)
            normalized_worlds[task_id] = {
                "world_seed": world_seed,
                "world_nonce": world_nonce,
                "world_interventions": [dict(entry) for entry in interventions],
            }
        normalized[pair_id] = {
            "method_seed": method_seed,
            "seed_nonce": method_nonce,
            "tasks": normalized_worlds,
        }
    summary.update({"opaque_pair_count": len(pairs), "task_count": len(tasks)})
    if not valid:
        blockers.append("private_assignment_invalid_or_not_disjoint")
        return None, summary
    return normalized, summary


def _audit_infrastructure(
    resources: Mapping[str, Any],
    *,
    orchestration: Mapping[str, Any],
    matrix: Mapping[str, Any],
    methods: Mapping[str, FormalMethodBinding],
    request: Mapping[str, Any],
    blockers: list[str],
) -> bool:
    infrastructure = request.get("infrastructure")
    if not isinstance(infrastructure, Mapping):
        blockers.append("infrastructure_contract_missing")
        return False
    try:
        cpu_workers = _positive_int(orchestration.get("cpu_workers"))
        cpu_count = _positive_int(resources.get("cpu_count"))
        free_disk = _nonnegative_int(resources.get("free_disk_bytes"))
        required_disk = _positive_int(infrastructure.get("required_free_disk_bytes"))
        bytes_per_cell = _positive_int(infrastructure.get("estimated_bytes_per_cell"))
    except ValueError:
        blockers.append("infrastructure:capacity_value_invalid")
        return False
    cell_count = _matrix_cell_count(matrix)
    cpu_valid = cpu_workers <= cpu_count
    disk_valid = required_disk >= cell_count * bytes_per_cell and free_disk >= required_disk
    if not cpu_valid:
        blockers.append("infrastructure:cpu_capacity")
    if not disk_valid:
        blockers.append("infrastructure:disk_capacity_or_estimate")
    valid = cpu_valid and disk_valid
    requested_gpu = orchestration.get("gpu_devices")
    available_gpu = resources.get("gpu_devices")
    if any(method.kind == "rl" for method in methods.values()):
        if not isinstance(requested_gpu, list) or not isinstance(available_gpu, list):
            valid = False
        else:
            requested_ids = {
                item.get("device_id") for item in requested_gpu if isinstance(item, Mapping)
            }
            gpu_valid = bool(requested_ids) and requested_ids.issubset(set(available_gpu))
            if not gpu_valid:
                blockers.append("infrastructure:gpu_device_unavailable")
            valid = valid and gpu_valid
    has_llm = any(method.kind == "live_llm" for method in methods.values())
    if has_llm:
        api_cells = _api_cell_count(matrix, methods=methods)
        expected_cap = api_cells * _finite_nonnegative(
            orchestration.get("api_cost_usd_per_cell_limit")
        )
        declared_cap = _finite_nonnegative(
            orchestration.get("matrix_monetary_cost_usd_limit")
        )
        api_concurrency = _positive_int(orchestration.get("api_max_concurrency"))
        api_rate = _positive_int(orchestration.get("api_cell_starts_per_minute"))
        provider_rate = _positive_int(
            orchestration.get("api_provider_requests_per_minute_limit")
        )
        credential_valid = resources.get("api_credential_available") is True
        cap_valid = math.isclose(expected_cap, declared_cap, abs_tol=1e-9, rel_tol=0.0)
        if not credential_valid:
            blockers.append("infrastructure:api_credential_missing")
        if not cap_valid:
            blockers.append("infrastructure:api_cost_cap_incoherent")
        valid = valid and credential_valid and cap_valid
        try:
            max_concurrency = _positive_int(resources.get("api_max_concurrency"))
            max_rate = _positive_int(resources.get("api_requests_per_minute"))
            quota = _finite_nonnegative(resources.get("api_monetary_quota_usd"))
        except ValueError:
            blockers.append("infrastructure:api_quota_value_invalid")
            return False
        concurrency_valid = api_concurrency <= max_concurrency
        rate_valid = api_rate <= max_rate and provider_rate <= max_rate
        quota_valid = declared_cap <= quota
        if not concurrency_valid:
            blockers.append("infrastructure:api_concurrency_quota")
        if not rate_valid:
            blockers.append("infrastructure:api_rate_quota")
        if not quota_valid:
            blockers.append("infrastructure:api_cost_quota")
        valid = valid and concurrency_valid and rate_valid and quota_valid
    return bool(valid)


def _build_cells(
    *,
    run_id: str,
    matrix: Mapping[str, Any],
    methods: Mapping[str, FormalMethodBinding],
    private: Mapping[str, Any],
    cell_bindings: Mapping[str, Any],
    source_commit: str,
) -> tuple[list[FormalCellSpec], dict[str, dict[str, Any]]]:
    cells: list[FormalCellSpec] = []
    runtimes: dict[str, dict[str, Any]] = {}
    for task_id in matrix["tasks"]:
        for method_id in matrix["methods"]:
            method = methods[method_id]
            for pair_id in matrix["pair_ids"]:
                pair = private[pair_id]
                world = pair["tasks"][task_id]
                for condition in matrix["spectrum_conditions_by_method"][method_id]:
                    spec = FormalCellSpec(
                        run_id=run_id,
                        task_id=task_id,
                        pair_id=pair_id,
                        spectrum_condition=condition,
                        private_seed_commitment=private_seed_commitment(
                            run_id=run_id,
                            pair_id=pair_id,
                            method_seed=pair["method_seed"],
                            nonce=pair["seed_nonce"],
                        ),
                        world_commitment=private_world_commitment(
                            run_id=run_id,
                            task_id=task_id,
                            pair_id=pair_id,
                            world_seed=world["world_seed"],
                            nonce=world["world_nonce"],
                            interventions=world["world_interventions"],
                        ),
                        protocol_sha256=cell_bindings["protocol_sha256"],
                        backend_semantic_sha256=cell_bindings["backend_semantic_sha256"],
                        evaluator_sha256=cell_bindings["evaluator_sha256"],
                        interaction_protocol_sha256=cell_bindings[
                            "interaction_protocol_sha256"
                        ],
                        statistics_protocol_sha256=cell_bindings[
                            "statistics_protocol_sha256"
                        ],
                        reference_manifest_sha256=cell_bindings[
                            "reference_manifest_sha256"
                        ],
                        source_commit=source_commit,
                        complete_experiments=matrix["complete_experiments_per_cell"],
                        operation_limit=matrix["operation_limits_by_task"][task_id],
                        method=method,
                    )
                    cells.append(spec)
                    runtimes[spec.cell_identity_sha256] = {
                        "method_seed": pair["method_seed"],
                        "world_seed": world["world_seed"],
                        "seed_nonce": pair["seed_nonce"],
                        "world_nonce": world["world_nonce"],
                        "world_interventions": world["world_interventions"],
                    }
    return cells, runtimes


def _valid_pricing_snapshot(raw: Any, *, expected_model: Any) -> bool:
    if not isinstance(raw, Mapping) or raw.get("schema_version") != PROVIDER_PRICING_VERSION:
        return False
    if raw.get("model_id") != expected_model or raw.get("currency") != "USD":
        return False
    supplied = raw.get("pricing_version_sha256")
    unsigned = dict(raw)
    unsigned.pop("pricing_version_sha256", None)
    if supplied != canonical_sha256(unsigned):
        return False
    return all(
        _is_nonnegative_finite(raw.get(field))
        for field in (
            "input_cache_hit_per_million_usd",
            "input_cache_miss_per_million_usd",
            "output_per_million_usd",
        )
    )


def _public_resource_summary(resources: Mapping[str, Any]) -> dict[str, Any]:
    gpu = resources.get("gpu_devices")
    return {
        "cpu_count": resources.get("cpu_count"),
        "free_disk_bytes": resources.get("free_disk_bytes"),
        "gpu_device_count": len(gpu) if isinstance(gpu, list) else 0,
        "api_credential_available": resources.get("api_credential_available") is True,
        "api_secret_value_reported": False,
        "api_max_concurrency": resources.get("api_max_concurrency"),
        "api_requests_per_minute": resources.get("api_requests_per_minute"),
        "api_monetary_quota_usd": resources.get("api_monetary_quota_usd"),
    }


def _api_cell_count(
    matrix: Mapping[str, Any], *, methods: Mapping[str, FormalMethodBinding]
) -> int:
    tasks = matrix.get("tasks", [])
    pairs = matrix.get("pair_ids", [])
    spectrum = matrix.get("spectrum_conditions_by_method", {})
    return sum(
        len(tasks) * len(pairs) * len(spectrum.get(method_id, []))
        for method_id, method in methods.items()
        if method.kind == "live_llm"
    )


def _matrix_cell_count(matrix: Mapping[str, Any]) -> int:
    tasks = matrix.get("tasks", [])
    pairs = matrix.get("pair_ids", [])
    spectrum = matrix.get("spectrum_conditions_by_method", {})
    methods = matrix.get("methods", [])
    if not all(isinstance(item, list) for item in (tasks, pairs, methods)):
        return 0
    if not isinstance(spectrum, Mapping):
        return 0
    return sum(
        len(tasks) * len(pairs) * len(spectrum.get(method_id, []))
        for method_id in methods
        if isinstance(spectrum.get(method_id), list)
    )


def _public_seed_ranges(value: Any) -> tuple[tuple[int, int], ...] | None:
    if not isinstance(value, Mapping) or set(value) != {"train", "dev", "reference_search"}:
        return None
    ranges: list[tuple[int, int]] = []
    for split in ("train", "dev", "reference_search"):
        item = value.get(split)
        if not isinstance(item, Mapping):
            return None
        minimum = item.get("minimum_seed")
        maximum = item.get("maximum_seed")
        if (
            not _is_nonnegative_int(minimum)
            or not _is_nonnegative_int(maximum)
            or minimum > maximum
        ):
            return None
        ranges.append((minimum, maximum))
    return tuple(ranges)


def _in_seed_ranges(seed: int, ranges: Sequence[tuple[int, int]]) -> bool:
    return any(minimum <= seed <= maximum for minimum, maximum in ranges)


def _safe_repo_path(root: Path, relative: Any) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _unique_text_list(value: Any) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item.strip() for item in value)
        or len(value) != len(set(value))
    ):
        raise ValueError("expected unique non-empty text list")
    return list(value)


def _positive_int_list(value: Any) -> list[int]:
    if not isinstance(value, list) or not value:
        raise ValueError("expected positive integer list")
    result = [_positive_int(item) for item in value]
    if result != sorted(set(result)):
        raise ValueError("expected increasing unique integer list")
    return result


def _positive_int(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("expected positive integer")
    return value


def _nonnegative_int(value: Any) -> int:
    if not _is_nonnegative_int(value):
        raise ValueError("expected non-negative integer")
    return value


def _finite_nonnegative(value: Any) -> float:
    if not _is_nonnegative_finite(value):
        raise ValueError("expected non-negative finite number")
    return float(value)


def _is_nonnegative_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_nonnegative_finite(value: Any) -> TypeGuard[int | float]:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and value >= 0
    )


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_git_commit(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _env_positive_int(name: str) -> int | None:
    value = os.getenv(name)
    try:
        return _positive_int(int(value)) if value is not None else None
    except (TypeError, ValueError):
        return None


def _env_nonnegative_float(name: str) -> float | None:
    value = os.getenv(name)
    try:
        parsed = float(value) if value is not None else None
    except (TypeError, ValueError):
        return None
    return float(parsed) if _is_nonnegative_finite(parsed) else None


__all__ = [
    "PREFLIGHT_PRIVATE_ASSIGNMENT_VERSION",
    "PREFLIGHT_REPORT_VERSION",
    "PREFLIGHT_REQUEST_VERSION",
    "PreflightOutcome",
    "probe_repository",
    "probe_resources",
    "run_formal_preflight",
]
