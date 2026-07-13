"""Fail-closed controls for the post-quarantine ChemWorld formal protocol."""

from __future__ import annotations

import hashlib
import json
import math
import secrets
import subprocess
from collections.abc import Mapping, Sequence
from contextlib import suppress
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.eval.evidence_quarantine import (
    build_exposure_inventory,
    load_evidence_quarantine_policy,
)
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.world.world_family import WORLD_FAMILY_INTERVENTION_VERSION, axes_for_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "benchmark" / "formal_protocol_v0.4.json"


def _git_common_dir() -> Path:
    dot_git = ROOT / ".git"
    if dot_git.is_dir():
        return dot_git.resolve()
    if dot_git.is_file():
        marker = dot_git.read_text(encoding="utf-8").strip()
        if marker.startswith("gitdir:"):
            raw_git_dir = Path(marker.removeprefix("gitdir:").strip())
            git_dir = (
                raw_git_dir.resolve()
                if raw_git_dir.is_absolute()
                else (ROOT / raw_git_dir).resolve()
            )
            common_marker = git_dir / "commondir"
            if common_marker.is_file():
                raw_common = Path(
                    common_marker.read_text(encoding="utf-8").strip()
                )
                return (
                    raw_common.resolve()
                    if raw_common.is_absolute()
                    else (git_dir / raw_common).resolve()
                )
            return git_dir
    return dot_git.resolve()


DEFAULT_PRIVATE_MANIFEST_PATH = (
    _git_common_dir()
    / "chemworld-private"
    / "formal-protocol-v0.4.2"
    / "bench-manifest.json"
)
PROTOCOL_VERSION = "chemworld-formal-protocol-0.4"
PRIVATE_MANIFEST_VERSION = "chemworld-private-bench-manifest-0.4"
CORE_TASKS = (
    "partition-discovery",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)
EXPLORATORY_TASKS = (
    "electrochemical-conversion",
    "equilibrium-characterization",
)
SPLIT_NAMES = ("train", "dev", "reference_search", "bench")
PUBLIC_SPLITS = ("train", "dev", "reference_search")
REQUIRED_MODES = ("interpolation", "extrapolation", "composition", "observation_noise")
CHECKPOINTS = (4, 8, 12, 20, 40)
PAIRED_BENCH_SEEDS = 100


class FormalProtocolError(RuntimeError):
    """Raised when formal-protocol state cannot be trusted."""


def load_formal_protocol(path: Path | None = None) -> dict[str, Any]:
    """Load the public protocol without resolving or exposing its private cohort."""

    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = _read_object(resolved)
    if payload.get("schema_version") != PROTOCOL_VERSION:
        raise FormalProtocolError("unsupported formal protocol schema")
    return payload


def initialize_private_bench_manifest(
    protocol: Mapping[str, Any],
    *,
    path: Path = DEFAULT_PRIVATE_MANIFEST_PATH,
) -> dict[str, Any]:
    """Create the sealed Bench manifest once and return only non-secret metadata.

    The generated seed and world values are deliberately never returned. The
    caller receives only the canonical commitment and aggregate counts.
    """

    if path.exists():
        raise FormalProtocolError("private Bench manifest already exists; refusing overwrite")
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        raise FormalProtocolError("cannot initialize an unsupported protocol")
    split = protocol.get("split_contract", {})
    bench = split.get("bench", {}) if isinstance(split, Mapping) else {}
    seed_count = bench.get("paired_seed_count") if isinstance(bench, Mapping) else None
    if seed_count != PAIRED_BENCH_SEEDS:
        raise FormalProtocolError("private Bench initialization requires 100 paired seeds")

    rng = secrets.SystemRandom()
    exposed = set(
        build_exposure_inventory(load_evidence_quarantine_policy())["exposed_seeds"]
    )
    public_seeds = _public_seed_sets(protocol)
    excluded = exposed.union(*(public_seeds.values()))
    base_seeds: list[int] = []
    while len(base_seeds) < PAIRED_BENCH_SEEDS:
        candidate = rng.randrange(1 << 52, 1 << 62)
        if candidate not in excluded and candidate not in base_seeds:
            base_seeds.append(candidate)

    axes = _configured_axes(protocol)
    domains = protocol["world_family_contract"]["private_bench_severity_domains"]
    pairs: list[dict[str, Any]] = []
    for pair_index, base_seed in enumerate(base_seeds):
        task_worlds: dict[str, Any] = {}
        for task_id in CORE_TASKS:
            interventions: list[dict[str, Any]] = []
            for axis_id in axes[task_id]:
                for mode in REQUIRED_MODES:
                    low, high = _severity_domain(domains, mode)
                    magnitude = rng.uniform(low, high)
                    sign = -1.0 if rng.randrange(2) == 0 else 1.0
                    interventions.append(
                        {
                            "axis_id": axis_id,
                            "mode": mode,
                            "severity": round(sign * magnitude, 12),
                        }
                    )
            task_worlds[task_id] = {
                "base_world_seed": rng.randrange(1 << 52, 1 << 62),
                "world_stream_nonce": secrets.token_hex(16),
                "interventions": interventions,
            }
        pairs.append(
            {
                "pair_index": pair_index,
                "base_seed": base_seed,
                "method_pairing_nonce": secrets.token_hex(16),
                "task_worlds": task_worlds,
            }
        )

    private = {
        "schema_version": PRIVATE_MANIFEST_VERSION,
        "protocol_id": protocol["protocol_id"],
        "namespace_id": bench["namespace_id"],
        "created_at": datetime.now(UTC).isoformat(),
        "public_protocol_precommit_sha256": _protocol_precommit_sha256(protocol),
        "state": "sealed_unrun_unviewed_by_evaluated_methods",
        "access_state": {
            "bench_run_started": False,
            "bench_result_count": 0,
            "values_exposed_to_evaluated_methods": False,
            "used_for_tuning": False,
        },
        "paired_seed_count": PAIRED_BENCH_SEEDS,
        "base_seeds": base_seeds,
        "pairs": pairs,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(private, indent=2, sort_keys=True) + "\n"
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
        with suppress(OSError):
            path.chmod(0o600)
    except OSError as exc:
        raise FormalProtocolError("could not create private Bench manifest") from exc
    return {
        "commitment_sha256": _canonical_sha256(private),
        "paired_seed_count": PAIRED_BENCH_SEEDS,
        "task_count": len(CORE_TASKS),
        "world_assignments_per_seed": sum(
            len(axes[task_id]) * len(REQUIRED_MODES) for task_id in CORE_TASKS
        ),
        "path": str(path),
    }


def audit_formal_protocol(
    protocol: Mapping[str, Any],
    *,
    private_manifest_path: Path | None = None,
    workspace: Path = ROOT,
) -> dict[str, Any]:
    """Audit public semantics and the sealed private commitment without leaking it."""

    controls: dict[str, bool] = {}
    controls["schema_and_state_are_preregistered"] = (
        protocol.get("schema_version") == PROTOCOL_VERSION
        and protocol.get("status") == "preregistered_controls_bench_sealed"
        and protocol.get("formal_results_present") is False
        and protocol.get("benchmark_claim_allowed") is False
    )

    backend = protocol.get("backend_binding", {})
    controls["backend_release_is_exact_and_ready"] = _backend_binding_ready(
        backend, workspace
    )
    controls["all_p0_evidence_is_hash_bound_and_ready"] = _p0_evidence_ready(
        protocol.get("p0_evidence_bindings"), workspace
    )

    roles = protocol.get("task_roles", {})
    core = roles.get("formal_core", {}) if isinstance(roles, Mapping) else {}
    exploratory = roles.get("exploratory_only", ()) if isinstance(roles, Mapping) else ()
    controls["task_roles_are_exact"] = (
        isinstance(core, Mapping)
        and tuple(core) == CORE_TASKS
        and tuple(exploratory) == EXPLORATORY_TASKS
    )
    controls["core_metrics_hashes_and_thresholds_match_p0"] = _task_bindings_ready(
        core, workspace
    )

    split = protocol.get("split_contract", {})
    public_seed_sets = _public_seed_sets(protocol)
    controls["all_four_namespaces_are_unique"] = _unique_namespace_ids(split)
    controls["public_seed_splits_are_well_formed_and_disjoint"] = (
        set(public_seed_sets) == set(PUBLIC_SPLITS)
        and all(public_seed_sets.values())
        and _sets_are_disjoint(tuple(public_seed_sets.values()))
    )
    controls["public_seed_splits_were_outside_quarantine_inventory"] = (
        _public_seeds_outside_frozen_inventory(public_seed_sets, workspace)
    )
    controls["bench_public_contract_contains_no_raw_seed_or_world_values"] = (
        _bench_public_boundary_ready(protocol)
    )

    world = protocol.get("world_family_contract", {})
    controls["world_axes_and_modes_match_runtime_registry"] = _world_contract_ready(world)
    controls["public_world_grids_are_disjoint"] = _public_world_grids_are_disjoint(world)
    campaign = protocol.get("campaign_contract", {})
    controls["budget_checkpoints_and_stopping_are_frozen"] = (
        isinstance(campaign, Mapping)
        and campaign.get("complete_experiments_per_cell") == 40
        and tuple(campaign.get("anytime_checkpoints", ())) == CHECKPOINTS
        and campaign.get("early_campaign_stopping") == "not_allowed"
        and campaign.get("method_requested_early_stop")
        == "record_as_failed_incomplete_campaign"
        and campaign.get("bench_finetuning") == "prohibited"
        and campaign.get("bench_prompt_or_checkpoint_selection") == "prohibited"
        and campaign.get("automatic_action_repair_or_closeout") == "forbidden"
    )
    controls["failure_policy_is_fail_closed"] = _failure_policy_ready(
        protocol.get("failure_policy")
    )
    controls["estimand_families_are_explicit"] = _estimands_ready(
        protocol.get("estimands")
    )
    controls["legacy_0_1_through_0_3_are_diagnostic_only"] = _supersession_ready(
        protocol.get("supersession")
    )
    controls["bench_access_state_is_unrun_and_untuned"] = _public_access_state_ready(
        protocol.get("access_state")
    )

    private_summary = _audit_private_manifest(
        protocol,
        private_manifest_path,
        public_seed_sets=public_seed_sets,
        workspace=workspace,
    )
    controls["private_manifest_commitment_is_verified"] = private_summary["verified"]
    controls["private_bench_is_disjoint_and_sealed"] = private_summary[
        "disjoint_and_sealed"
    ]
    controls["private_manifest_is_not_git_tracked"] = private_summary["not_git_tracked"]

    controls_ready = all(controls.values())
    commit, dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-formal-protocol-audit-0.4",
        "protocol_id": protocol.get("protocol_id"),
        "status": "formal_protocol_frozen_bench_sealed"
        if controls_ready
        else "formal_protocol_controls_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "backend_semantic_sha256": backend.get("backend_semantic_sha256")
        if isinstance(backend, Mapping)
        else None,
        "private_bench": private_summary,
        "public_split_summary": {
            name: {
                "seed_count": len(seeds),
                "minimum_seed": min(seeds),
                "maximum_seed": max(seeds),
            }
            for name, seeds in public_seed_sets.items()
        },
        "formal_core_tasks": list(core) if isinstance(core, Mapping) else [],
        "exploratory_tasks": list(exploratory)
        if isinstance(exploratory, Sequence)
        and not isinstance(exploratory, (str, bytes, bytearray))
        else [],
        "experiment_budget": campaign.get("complete_experiments_per_cell")
        if isinstance(campaign, Mapping)
        else None,
        "checkpoints": list(campaign.get("anytime_checkpoints", ()))
        if isinstance(campaign, Mapping)
        else [],
        "controls": controls,
        "limitations": [
            "This freezes controls and an unseen cohort; it contains no method results.",
            (
                "Bench remains sealed until interaction, statistics, reference, runner, "
                "and method-freeze gates pass."
            ),
            (
                "Linux clean-wheel reproduction is an optional portability follow-up, "
                "not a formal-protocol gate."
            ),
        ],
        "next_gates": [
            "freeze recipe-level and operation-level interaction strata",
            "freeze the statistical analysis and failure denominator",
            "freeze an independent reference-search portfolio",
        ],
    }


def _backend_binding_ready(binding: Any, workspace: Path) -> bool:
    if not isinstance(binding, Mapping):
        return False
    path = _resolve_workspace_path(workspace, binding.get("release_manifest_path"))
    if path is None or not path.is_file():
        return False
    manifest = _read_object(path)
    return (
        _file_sha256(path) == binding.get("release_manifest_sha256")
        and manifest.get("backend_id") == binding.get("release_manifest_id")
        and manifest.get("release_status") == "formal_candidate"
        and manifest.get("portable_release_ready") is True
        and manifest.get("backend_semantic_sha256")
        == binding.get("backend_semantic_sha256")
        and _is_sha256(binding.get("backend_semantic_sha256"))
        and manifest.get("benchmark_claim_allowed") is False
    )


def _p0_evidence_ready(raw_bindings: Any, workspace: Path) -> bool:
    if not isinstance(raw_bindings, Sequence) or isinstance(
        raw_bindings, (str, bytes, bytearray)
    ):
        return False
    expected = {
        "evidence_quarantine",
        "contract_coherence",
        "composed_runtime_stress",
        "observation_identifiability",
        "task_validity_power",
        "portable_release",
    }
    seen: set[str] = set()
    for item in raw_bindings:
        if not isinstance(item, Mapping):
            return False
        control_id = str(item.get("control_id", ""))
        path = _resolve_workspace_path(workspace, item.get("path"))
        if control_id in seen or path is None or not path.is_file():
            return False
        report = _read_object(path)
        report_ready = (
            report.get("portable_release_ready") is True
            if control_id == "portable_release"
            else report.get("controls_ready") is True
        )
        no_formal_results = (
            report.get("formal_results_present") is False
            if "formal_results_present" in report
            else control_id == "portable_release"
        )
        if (
            _file_sha256(path) != item.get("sha256")
            or not report_ready
            or not no_formal_results
            or report.get("benchmark_claim_allowed") is not False
        ):
            return False
        seen.add(control_id)
    return seen == expected


def _task_bindings_ready(core: Any, workspace: Path) -> bool:
    if not isinstance(core, Mapping) or tuple(core) != CORE_TASKS:
        return False
    path = (
        workspace
        / "workstreams"
        / "world_foundation"
        / "reports"
        / "task-validity-power-v0.5.json"
    )
    if not path.is_file():
        return False
    report = _read_object(path)
    task_rows = report.get("core_tasks", {})
    if not isinstance(task_rows, Mapping):
        return False
    for task_id in CORE_TASKS:
        configured = core.get(task_id)
        observed = task_rows.get(task_id)
        if not isinstance(configured, Mapping) or not isinstance(observed, Mapping):
            return False
        surface = observed.get("surface", {})
        risk_cost = observed.get("risk_cost", {})
        if not isinstance(surface, Mapping) or not isinstance(risk_cost, Mapping):
            return False
        if not (
            configured.get("primary_metric") == observed.get("primary_metric")
            and configured.get("task_contract_hash") == observed.get("task_contract_hash")
            and configured.get("sesoi") == surface.get("sesoi")
            and configured.get("risk_limit") == risk_cost.get("proposed_risk_limit")
            and configured.get("process_cost_limit")
            == risk_cost.get("proposed_process_cost_limit")
        ):
            return False
    return True


def _public_seed_sets(protocol: Mapping[str, Any]) -> dict[str, set[int]]:
    split = protocol.get("split_contract", {})
    if not isinstance(split, Mapping):
        return {}
    output: dict[str, set[int]] = {}
    for name in PUBLIC_SPLITS:
        row = split.get(name)
        if not isinstance(row, Mapping):
            continue
        raw_range = row.get("base_seeds")
        if not isinstance(raw_range, Mapping):
            continue
        start = raw_range.get("start")
        stop = raw_range.get("stop_inclusive")
        if (
            isinstance(start, int)
            and not isinstance(start, bool)
            and isinstance(stop, int)
            and not isinstance(stop, bool)
            and start >= 0
            and start <= stop
            and stop - start < 10_000
        ):
            output[name] = set(range(start, stop + 1))
    return output


def _unique_namespace_ids(split: Any) -> bool:
    if not isinstance(split, Mapping):
        return False
    values: list[str] = []
    for name in SPLIT_NAMES:
        row = split.get(name)
        if not isinstance(row, Mapping):
            return False
        namespace = row.get("namespace_id")
        if not isinstance(namespace, str) or not namespace.strip():
            return False
        values.append(namespace)
    return len(set(values)) == len(SPLIT_NAMES)


def _sets_are_disjoint(values: tuple[set[int], ...]) -> bool:
    merged: set[int] = set()
    for value in values:
        if merged.intersection(value):
            return False
        merged.update(value)
    return True


def _public_seeds_outside_frozen_inventory(
    public: Mapping[str, set[int]], workspace: Path
) -> bool:
    path = workspace / "workstreams" / "benchmark_v1" / "reports" / "evidence-quarantine-v0.5.json"
    if not path.is_file():
        return False
    report = _read_object(path)
    inventory = report.get("inventory", {})
    exposed = inventory.get("exposed_seeds", ()) if isinstance(inventory, Mapping) else ()
    frozen = {value for value in exposed if isinstance(value, int) and not isinstance(value, bool)}
    return all(not seeds.intersection(frozen) for seeds in public.values())


def _bench_public_boundary_ready(protocol: Mapping[str, Any]) -> bool:
    split = protocol.get("split_contract", {})
    private = protocol.get("private_bench_manifest", {})
    bench = split.get("bench", {}) if isinstance(split, Mapping) else {}
    if not isinstance(bench, Mapping) or not isinstance(private, Mapping):
        return False
    commitment = private.get("commitment_sha256")
    path = str(private.get("relative_controlled_path", "")).replace("\\", "/")
    return (
        bench.get("paired_seed_count") == PAIRED_BENCH_SEEDS
        and bench.get("base_seeds") == "private_manifest_only"
        and bench.get("world_parameters") == "private_manifest_only"
        and bench.get("agent_access") == "sealed_until_method_freeze"
        and private.get("raw_values_in_public_artifacts") is False
        and private.get("required_state")
        == "sealed_unrun_unviewed_by_evaluated_methods"
        and _is_sha256(commitment)
        and commitment != "0" * 64
        and path == ".git/chemworld-private/formal-protocol-v0.4.2/bench-manifest.json"
    )


def _configured_axes(protocol: Mapping[str, Any]) -> dict[str, tuple[str, ...]]:
    world = protocol.get("world_family_contract", {})
    raw = world.get("axes", {}) if isinstance(world, Mapping) else {}
    if not isinstance(raw, Mapping):
        return {}
    return {
        task_id: tuple(str(axis) for axis in raw.get(task_id, ())) for task_id in CORE_TASKS
    }


def _world_contract_ready(world: Any) -> bool:
    if not isinstance(world, Mapping):
        return False
    axes = world.get("axes", {})
    return (
        world.get("intervention_contract_version") == WORLD_FAMILY_INTERVENTION_VERSION
        and tuple(world.get("required_modes", ())) == REQUIRED_MODES
        and world.get("axis_identity_visible_to_agent") is False
        and isinstance(axes, Mapping)
        and tuple(axes) == CORE_TASKS
        and all(
            tuple(axes[task_id])
            == tuple(spec.axis_id for spec in axes_for_task(task_id))
            for task_id in CORE_TASKS
        )
    )


def _public_world_grids_are_disjoint(world: Any) -> bool:
    if not isinstance(world, Mapping):
        return False
    grids = world.get("public_development_severities", {})
    if not isinstance(grids, Mapping) or set(grids) != set(PUBLIC_SPLITS):
        return False
    seen: set[tuple[str, float]] = set()
    for split_name in PUBLIC_SPLITS:
        split_grid = grids.get(split_name)
        if not isinstance(split_grid, Mapping):
            return False
        local: set[tuple[str, float]] = set()
        for mode, values in split_grid.items():
            if mode not in REQUIRED_MODES or not isinstance(values, Sequence) or isinstance(
                values, (str, bytes, bytearray)
            ):
                return False
            for value in values:
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    or not -1.0 <= float(value) <= 1.0
                    or float(value) == 0.0
                ):
                    return False
                local.add((str(mode), float(value)))
        if not local or seen.intersection(local):
            return False
        seen.update(local)
    return True


def _failure_policy_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping):
        return False
    expected = {
        "invalid_action": "retain_in_denominator_and_ledger",
        "provider_or_model_failure": "retain_in_denominator_and_classify",
        "runtime_failure": "retain_in_denominator_and_classify",
        "budget_overrun": "terminate_cell_as_failure",
        "missing_or_nonfinite_metric": "terminate_cell_as_failure",
        "incomplete_resource_accounting": "retain_trajectory_but_ineligible_for_success",
        "replay_mismatch": "invalidate_cell",
        "infrastructure_retry": (
            "allowed_only_with_same_cell_identity_and_documented_attempt_lineage"
        ),
        "silent_drop_or_imputation": "forbidden",
    }
    return dict(raw) == expected


def _estimands_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping) or set(raw) != {
        "primary",
        "secondary",
        "ablation",
        "exploratory",
    }:
        return False
    primary = raw.get("primary")
    return (
        isinstance(primary, Mapping)
        and primary.get("unit") == "paired_task_bench_seed"
        and primary.get("scope") == "each_formal_core_task_separately"
        and primary.get("endpoint")
        == "best_valid_primary_metric_after_40_complete_experiments"
        and all(
            isinstance(raw.get(name), Sequence)
            and not isinstance(raw.get(name), (str, bytes, bytearray))
            and bool(raw.get(name))
            for name in ("secondary", "ablation", "exploratory")
        )
    )


def _supersession_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and tuple(raw.get("diagnostic_protocol_versions", ())) == ("0.1", "0.2", "0.3")
        and raw.get("legacy_results_role") == "diagnostic_only"
        and raw.get("in_place_edits_after_bench_unseal") == "forbidden"
        and "new protocol version" in str(raw.get("change_rule", ""))
    )


def _public_access_state_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and raw.get("bench_manifest_initialized") is True
        and raw.get("bench_run_started") is False
        and raw.get("bench_results_present") is False
        and raw.get("bench_values_exposed_to_evaluated_methods") is False
        and raw.get("bench_used_for_tuning") is False
    )


def _audit_private_manifest(
    protocol: Mapping[str, Any],
    path: Path | None,
    *,
    public_seed_sets: Mapping[str, set[int]],
    workspace: Path,
) -> dict[str, Any]:
    public_private = protocol.get("private_bench_manifest", {})
    commitment = (
        public_private.get("commitment_sha256")
        if isinstance(public_private, Mapping)
        else None
    )
    summary: dict[str, Any] = {
        "commitment_sha256": commitment,
        "verified": False,
        "disjoint_and_sealed": False,
        "not_git_tracked": False,
        "paired_seed_count": None,
        "task_count": None,
        "world_assignments_per_seed": None,
        "raw_seed_values_reported": False,
        "raw_world_parameters_reported": False,
    }
    if path is None or not path.is_file() or not _is_sha256(commitment):
        return summary
    try:
        private = _read_object(path)
    except (OSError, json.JSONDecodeError, FormalProtocolError):
        return summary
    axes = _configured_axes(protocol)
    base_seeds = private.get("base_seeds")
    pairs = private.get("pairs")
    if not isinstance(base_seeds, list) or not isinstance(pairs, list):
        return summary
    private_seed_set = {
        value for value in base_seeds if isinstance(value, int) and not isinstance(value, bool)
    }
    exposed = set(
        build_exposure_inventory(
            load_evidence_quarantine_policy(), workspace=workspace
        )["exposed_seeds"]
    )
    public_union = set().union(*public_seed_sets.values()) if public_seed_sets else set()
    access = private.get("access_state", {})
    pair_rows_valid = _private_pair_rows_valid(protocol, pairs, base_seeds, axes)
    sealed = (
        private.get("schema_version") == PRIVATE_MANIFEST_VERSION
        and private.get("protocol_id") == protocol.get("protocol_id")
        and private.get("namespace_id")
        == protocol.get("split_contract", {}).get("bench", {}).get("namespace_id")
        and private.get("public_protocol_precommit_sha256")
        == _protocol_precommit_sha256(protocol)
        and private.get("state") == "sealed_unrun_unviewed_by_evaluated_methods"
        and isinstance(access, Mapping)
        and access.get("bench_run_started") is False
        and access.get("bench_result_count") == 0
        and access.get("values_exposed_to_evaluated_methods") is False
        and access.get("used_for_tuning") is False
    )
    seed_ready = (
        len(base_seeds) == PAIRED_BENCH_SEEDS
        and len(private_seed_set) == PAIRED_BENCH_SEEDS
        and all(value >= 0 for value in private_seed_set)
        and not private_seed_set.intersection(exposed)
        and not private_seed_set.intersection(public_union)
    )
    summary.update(
        {
            "verified": _canonical_sha256(private) == commitment,
            "disjoint_and_sealed": sealed and seed_ready and pair_rows_valid,
            "not_git_tracked": not _is_git_tracked(path, workspace),
            "paired_seed_count": len(base_seeds),
            "task_count": len(CORE_TASKS) if pair_rows_valid else None,
            "world_assignments_per_seed": sum(
                len(axes[task_id]) * len(REQUIRED_MODES) for task_id in CORE_TASKS
            )
            if pair_rows_valid
            else None,
        }
    )
    return summary


def _private_pair_rows_valid(
    protocol: Mapping[str, Any],
    pairs: list[Any],
    base_seeds: list[Any],
    axes: Mapping[str, tuple[str, ...]],
) -> bool:
    if len(pairs) != PAIRED_BENCH_SEEDS or len(base_seeds) != PAIRED_BENCH_SEEDS:
        return False
    domains = protocol.get("world_family_contract", {}).get(
        "private_bench_severity_domains", {}
    )
    if not isinstance(domains, Mapping):
        return False
    for index, pair in enumerate(pairs):
        if not isinstance(pair, Mapping):
            return False
        if pair.get("pair_index") != index or pair.get("base_seed") != base_seeds[index]:
            return False
        if not _is_hex_token(pair.get("method_pairing_nonce"), 32):
            return False
        task_worlds = pair.get("task_worlds")
        if not isinstance(task_worlds, Mapping) or set(task_worlds) != set(CORE_TASKS):
            return False
        for task_id in CORE_TASKS:
            task_world = task_worlds[task_id]
            if not isinstance(task_world, Mapping):
                return False
            base_world_seed = task_world.get("base_world_seed")
            if (
                not isinstance(base_world_seed, int)
                or isinstance(base_world_seed, bool)
                or base_world_seed < 0
                or not _is_hex_token(task_world.get("world_stream_nonce"), 32)
            ):
                return False
            interventions = task_world.get("interventions")
            if not isinstance(interventions, list):
                return False
            expected = [(axis, mode) for axis in axes[task_id] for mode in REQUIRED_MODES]
            observed: list[tuple[str, str]] = []
            for intervention in interventions:
                if not isinstance(intervention, Mapping):
                    return False
                axis_id = str(intervention.get("axis_id", ""))
                mode = str(intervention.get("mode", ""))
                severity = intervention.get("severity")
                if (
                    isinstance(severity, bool)
                    or not isinstance(severity, (int, float))
                    or not math.isfinite(float(severity))
                ):
                    return False
                low, high = _severity_domain(domains, mode)
                if not low <= abs(float(severity)) <= high:
                    return False
                observed.append((axis_id, mode))
            if observed != expected:
                return False
    return True


def _severity_domain(domains: Mapping[str, Any], mode: str) -> tuple[float, float]:
    key = f"{mode}_absolute"
    raw = domains.get(key)
    if (
        not isinstance(raw, Sequence)
        or isinstance(raw, (str, bytes, bytearray))
        or len(raw) != 2
    ):
        raise FormalProtocolError(f"invalid private severity domain: {mode}")
    low, high = float(raw[0]), float(raw[1])
    if not 0.0 < low <= high <= 1.0:
        raise FormalProtocolError(f"invalid private severity bounds: {mode}")
    return low, high


def _protocol_precommit_sha256(protocol: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(protocol))
    private = payload.get("private_bench_manifest")
    if isinstance(private, dict):
        private["commitment_sha256"] = "<private-commitment>"
    return _canonical_sha256(payload)


def _resolve_workspace_path(workspace: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    candidate = Path(raw)
    if candidate.is_absolute():
        return None
    resolved = (workspace / candidate).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return None
    return resolved


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormalProtocolError("JSON object required")
    return payload


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _is_hex_token(value: Any, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and all(
        character in "0123456789abcdef" for character in value
    )


def _is_git_tracked(path: Path, workspace: Path) -> bool:
    try:
        relative = path.resolve().relative_to(workspace.resolve())
    except ValueError:
        return False
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", relative.as_posix()],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode == 0


def _git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


__all__ = [
    "DEFAULT_PRIVATE_MANIFEST_PATH",
    "DEFAULT_PROTOCOL_PATH",
    "FormalProtocolError",
    "audit_formal_protocol",
    "initialize_private_bench_manifest",
    "load_formal_protocol",
]
