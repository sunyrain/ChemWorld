"""Inventory exposed evaluation seeds and reject contaminated formal runs."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from functools import lru_cache
from pathlib import Path
from typing import Any

from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_POLICY_PATH = configuration_root() / "benchmark" / "evidence_quarantine_v0.5.json"
POLICY_VERSION = "chemworld-evidence-quarantine-policy-0.1"
_SEED_IN_NAME = re.compile(r"seed[-_]?([0-9]+)", re.IGNORECASE)


class EvidenceQuarantineError(RuntimeError):
    """Raised when an artifact cannot cross the formal evidence boundary."""


def load_evidence_quarantine_policy(path: Path | None = None) -> dict[str, Any]:
    """Load the public exposure and quarantine policy."""

    resolved = DEFAULT_POLICY_PATH if path is None else path
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise EvidenceQuarantineError("evidence quarantine policy must be an object")
    if payload.get("schema_version") != POLICY_VERSION:
        raise EvidenceQuarantineError("unsupported evidence quarantine policy schema")
    return payload


def build_exposure_inventory(
    policy: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    """Collect every seed already exposed by public configs or retained results."""

    sources: dict[int, set[str]] = defaultdict(set)
    world_cells: set[str] = set()
    config_files: list[Path] = []
    for pattern in policy["exposure_sources"]["public_config_globs"]:
        config_files.extend(_safe_glob(workspace, str(pattern)))
    for path in sorted(set(config_files)):
        payload = _read_object(path)
        _collect_seed_values(
            payload,
            source=path.relative_to(workspace).as_posix(),
            key_path=(),
            inherited_seed_context=False,
            output=sources,
        )
        _collect_world_cells(
            payload,
            source=path.relative_to(workspace).as_posix(),
            key_path=(),
            inherited_cell_context=False,
            output=world_cells,
        )

    history_blob_count = 0
    for object_id, historical_path, payload in _historical_json_objects(
        workspace, policy["exposure_sources"].get("git_history_pathspecs", ())
    ):
        history_blob_count += 1
        history_source = f"git:{object_id}:{historical_path}"
        _collect_seed_values(
            payload,
            source=history_source,
            key_path=(),
            inherited_seed_context=False,
            output=sources,
        )
        _collect_world_cells(
            payload,
            source=history_source,
            key_path=(),
            inherited_cell_context=False,
            output=world_cells,
        )

    result_files: list[Path] = []
    for pattern in policy["exposure_sources"]["retained_result_globs"]:
        result_files.extend(_safe_glob(workspace, str(pattern)))
    for path in sorted(set(result_files)):
        match = _SEED_IN_NAME.search(path.name)
        if match:
            sources[int(match.group(1))].add(path.relative_to(workspace).as_posix())
        payload = _read_object(path)
        seed = payload.get("seed")
        if isinstance(seed, int) and not isinstance(seed, bool):
            sources[seed].add(path.relative_to(workspace).as_posix() + "#seed")
        world_split = payload.get("world_split")
        if isinstance(world_split, str) and world_split:
            world_cells.add(
                path.relative_to(workspace).as_posix() + f"#world_split={world_split}"
            )

    exposed = sorted(sources)
    declared_retained_count = int(
        policy.get("legacy_primary_0_3_expectations", {}).get("result_count", 0)
    )
    return {
        "exposed_seed_count": len(exposed),
        "exposed_seeds": exposed,
        "minimum_exposed_seed": exposed[0] if exposed else None,
        "maximum_exposed_seed": exposed[-1] if exposed else None,
        "sources": {str(seed): sorted(sources[seed]) for seed in exposed},
        "exposed_world_cell_count": len(world_cells),
        "exposed_world_cells": sorted(world_cells),
        "public_config_count": len(set(config_files)),
        "git_history_config_blob_count": history_blob_count,
        "retained_result_count": len(set(result_files)),
        "declared_retained_result_count": declared_retained_count,
        "retained_results_locally_available": bool(result_files),
    }


def assert_formal_run_allowed(
    *,
    seed: int,
    protocol_id: str,
    protocol_benchmark_claim_allowed: bool,
    backend_id: str,
    backend_semantic_hash: str,
    private_seed_commitment: str,
    policy: Mapping[str, Any] | None = None,
    workspace: Path = ROOT,
) -> None:
    """Fail closed before an exposed or incompletely bound run can be formal."""

    active = load_evidence_quarantine_policy() if policy is None else dict(policy)
    guard = active["formal_guard"]
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise EvidenceQuarantineError("formal seed must be a non-negative integer")
    if guard["reject_any_publicly_exposed_seed"]:
        exposed = set(build_exposure_inventory(active, workspace=workspace)["exposed_seeds"])
        if seed in exposed:
            raise EvidenceQuarantineError(f"formal seed is already publicly exposed: {seed}")
    if guard["reject_quarantined_protocol_id"] and protocol_id in set(
        active["quarantined_protocol_ids"]
    ):
        raise EvidenceQuarantineError(f"protocol is quarantined: {protocol_id}")
    if guard["require_protocol_benchmark_claim_allowed"] and (
        protocol_benchmark_claim_allowed is not True
    ):
        raise EvidenceQuarantineError("formal protocol has not enabled benchmark claims")
    if guard["require_backend_id"] and not backend_id.strip():
        raise EvidenceQuarantineError("formal run requires a backend id")
    if guard["require_backend_semantic_hash"] and not _is_sha256(backend_semantic_hash):
        raise EvidenceQuarantineError("formal run requires a backend semantic sha256")
    if guard["require_private_seed_commitment"] and not _is_sha256(private_seed_commitment):
        raise EvidenceQuarantineError("formal run requires a private seed commitment sha256")


def audit_evidence_quarantine(
    policy: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    """Audit exposure coverage, legacy artifacts, docs, and the formal guard."""

    inventory = build_exposure_inventory(policy, workspace=workspace)
    exposed = set(inventory["exposed_seeds"])
    expected_cohorts: dict[str, list[int]] = {}
    for item in policy["known_consumed_cohorts"]:
        start = int(item["start"])
        stop = int(item["stop_inclusive"])
        expected_cohorts[str(item["cohort_id"])] = list(range(start, stop + 1))

    result_files = _expand_patterns(
        workspace, policy["exposure_sources"]["retained_result_globs"]
    )
    trajectory_files = _expand_patterns(
        workspace, policy["exposure_sources"]["retained_trajectory_globs"]
    )
    result_rows = [_read_object(path) for path in result_files]
    result_seed_counts = Counter(int(row["seed"]) for row in result_rows)
    expectations = policy["legacy_primary_0_3_expectations"]
    expected_result_seeds = list(
        range(
            int(expectations["seed_start"]),
            int(expectations["seed_stop_inclusive"]) + 1,
        )
    )
    trajectory_seed_counts = Counter(
        int(match.group(1))
        for path in trajectory_files
        if (match := _SEED_IN_NAME.search(path.name)) is not None
    )
    raw_artifacts_available = bool(result_files or trajectory_files)
    portable_manifest_valid = bool(
        expectations.get("raw_artifact_availability") == "optional_local_retention"
        and _is_sha256(str(expectations.get("result_manifest_sha256", "")))
        and _is_sha256(str(expectations.get("trajectory_identity_manifest_sha256", "")))
        and int(expectations["result_count"]) > 0
        and int(expectations["trajectory_count"]) > 0
        and len(expected_result_seeds) * int(expectations["results_per_seed"])
        == int(expectations["result_count"])
        == int(expectations["trajectory_count"])
    )
    raw_result_manifest_matches = bool(
        not raw_artifacts_available
        or _file_manifest_sha256(result_files, workspace)
        == expectations["result_manifest_sha256"]
    )
    raw_trajectory_manifest_matches = bool(
        not raw_artifacts_available
        or _path_manifest_sha256(trajectory_files, workspace)
        == expectations["trajectory_identity_manifest_sha256"]
    )

    protocol_status: dict[str, dict[str, Any]] = {}
    for path in _expand_patterns(
        workspace, policy["exposure_sources"]["public_config_globs"]
    ):
        payload = _read_object(path)
        protocol_id = payload.get("protocol_id")
        if protocol_id in set(policy["quarantined_protocol_ids"]):
            protocol_status[str(protocol_id)] = {
                "path": path.relative_to(workspace).as_posix(),
                "benchmark_claim_allowed": payload.get("benchmark_claim_allowed"),
                "status": payload.get("status"),
            }

    stale_doc_matches: list[dict[str, Any]] = []
    docs = policy["documentation_checks"]
    for raw_path in docs["paths"]:
        path = _resolve_workspace_path(workspace, str(raw_path))
        text = path.read_text(encoding="utf-8")
        for pattern in docs["prohibited_patterns"]:
            for match in re.finditer(str(pattern), text):
                stale_doc_matches.append(
                    {
                        "path": path.relative_to(workspace).as_posix(),
                        "pattern": pattern,
                        "match": match.group(0),
                    }
                )

    controls = {
        "policy_is_nonclaiming": policy.get("benchmark_claim_allowed") is False
        and policy.get("formal_results_present") is False,
        "known_consumed_cohorts_are_exposed": all(
            set(seeds).issubset(exposed) for seeds in expected_cohorts.values()
        ),
        "git_history_is_inventoried": inventory["git_history_config_blob_count"] > 0,
        "world_cells_are_inventoried": inventory["exposed_world_cell_count"] > 0,
        "legacy_portable_manifest_valid": portable_manifest_valid,
        "legacy_result_count_matches": not raw_artifacts_available
        or len(result_files) == int(expectations["result_count"]),
        "legacy_trajectory_count_matches": not raw_artifacts_available
        or len(trajectory_files) == int(expectations["trajectory_count"]),
        "legacy_raw_manifests_match_if_present": raw_result_manifest_matches
        and raw_trajectory_manifest_matches,
        "legacy_seed_grid_matches": not raw_artifacts_available
        or (
            sorted(result_seed_counts) == expected_result_seeds
            and all(
                result_seed_counts[seed] == int(expectations["results_per_seed"])
                for seed in expected_result_seeds
            )
            and sorted(trajectory_seed_counts) == expected_result_seeds
            and all(
                trajectory_seed_counts[seed] == int(expectations["results_per_seed"])
                for seed in expected_result_seeds
            )
        ),
        "legacy_results_replay_verified": not raw_artifacts_available
        or all(
            row.get("verified") is expectations["required_replay_verified"]
            and row.get("verification", {}).get("verified")
            is expectations["required_replay_verified"]
            for row in result_rows
        ),
        "legacy_results_bind_lite_maturity": not raw_artifacts_available
        or all(
            row.get("physics_maturity") == expectations["required_physics_maturity"]
            and row.get("kernel_maturity", {}).get("lowest_level")
            == expectations["required_physics_maturity"]
            for row in result_rows
        ),
        "quarantined_protocols_present_and_nonclaiming": set(protocol_status)
        == set(policy["quarantined_protocol_ids"])
        and all(
            item["benchmark_claim_allowed"] is False for item in protocol_status.values()
        ),
        "documentation_has_no_stale_fresh_claim": not stale_doc_matches,
        "formal_guard_has_no_force_override": policy["formal_guard"]["allow_force_override"]
        is False,
    }
    controls_ready = all(controls.values())
    source_commit, source_tree_dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-evidence-quarantine-report-0.1",
        "policy_id": policy["policy_id"],
        "status": "controls_ready_formal_protocol_0_4_pending"
        if controls_ready
        else "controls_failed",
        "controls_ready": controls_ready,
        "formal_guard_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": source_commit,
        "source_tree_dirty": source_tree_dirty,
        "policy_sha256": _canonical_sha256(policy),
        "controls": controls,
        "inventory": inventory,
        "known_consumed_cohorts": expected_cohorts,
        "quarantined_protocols": protocol_status,
        "legacy_primary_0_3": {
            "evidence_mode": "raw_artifacts_verified"
            if raw_artifacts_available
            else "portable_frozen_manifest",
            "result_count": int(expectations["result_count"]),
            "trajectory_count": int(expectations["trajectory_count"]),
            "local_result_count": len(result_files),
            "local_trajectory_count": len(trajectory_files),
            "seed_counts": {
                str(seed): (
                    result_seed_counts[seed]
                    if raw_artifacts_available
                    else int(expectations["results_per_seed"])
                )
                for seed in expected_result_seeds
            },
            "result_manifest_sha256": expectations["result_manifest_sha256"],
            "trajectory_identity_manifest_sha256": expectations[
                "trajectory_identity_manifest_sha256"
            ],
            "classification": "pre-v0.5_diagnostic_only",
            "reason": "retained results bind lite runtime maturity and an exposed cohort",
        },
        "stale_documentation_matches": stale_doc_matches,
        "limitations": [
            "This report inventories public exposure; it does not create a new private cohort.",
            (
                "Legacy raw files are optional local retention. Their frozen result/path "
                "manifest commitments preserve quarantine identity in clean clones; when "
                "raw files are present, counts, grids, maturity, verification, and both "
                "manifest digests are rechecked."
            ),
            (
                "A v0.5 formal backend semantic manifest and protocol 0.4 are still "
                "required before a formal run can start."
            ),
        ],
        "remaining_release_gates": [
            "freeze a coherent protocol 0.4 without publishing private seeds",
            "freeze the v0.5 backend semantic hash",
            "bind this guard into the formal preflight and cell runner",
        ],
    }


def _collect_seed_values(
    value: Any,
    *,
    source: str,
    key_path: tuple[str, ...],
    inherited_seed_context: bool,
    output: dict[int, set[str]],
) -> None:
    if isinstance(value, Mapping):
        if inherited_seed_context and _is_integer_range(value):
            start = int(value["start"])
            stop = int(value["stop_inclusive"])
            if stop < start or stop - start > 100_000:
                raise EvidenceQuarantineError(f"invalid exposed seed range in {source}")
            for seed in range(start, stop + 1):
                output[seed].add(source + "#" + ".".join(key_path))
        for raw_key, item in value.items():
            key = str(raw_key)
            _collect_seed_values(
                item,
                source=source,
                key_path=(*key_path, key),
                inherited_seed_context=inherited_seed_context or _is_seed_key(key),
                output=output,
            )
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            _collect_seed_values(
                item,
                source=source,
                key_path=(*key_path, str(index)),
                inherited_seed_context=inherited_seed_context,
                output=output,
            )
        return
    if inherited_seed_context and isinstance(value, int) and not isinstance(value, bool):
        output[int(value)].add(source + "#" + ".".join(key_path))


def _is_seed_key(key: str) -> bool:
    normalized = key.lower()
    if "_per_" in normalized or normalized.endswith("_seed_count"):
        return False
    return normalized == "seed" or normalized.endswith("_seed") or normalized.endswith(
        "_seeds"
    ) or normalized.endswith("_seed_ids") or normalized in {"seeds", "seed_ids", "base_seeds"}


def _is_integer_range(value: Mapping[str, Any]) -> bool:
    return (
        isinstance(value.get("start"), int)
        and not isinstance(value.get("start"), bool)
        and isinstance(value.get("stop_inclusive"), int)
        and not isinstance(value.get("stop_inclusive"), bool)
    )


def _collect_world_cells(
    value: Any,
    *,
    source: str,
    key_path: tuple[str, ...],
    inherited_cell_context: bool,
    output: set[str],
) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = str(raw_key)
            _collect_world_cells(
                item,
                source=source,
                key_path=(*key_path, key),
                inherited_cell_context=inherited_cell_context or key.lower() == "cells",
                output=output,
            )
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            _collect_world_cells(
                item,
                source=source,
                key_path=(*key_path, str(index)),
                inherited_cell_context=inherited_cell_context,
                output=output,
            )
        return
    if inherited_cell_context and isinstance(value, (str, int, float)) and not isinstance(
        value, bool
    ):
        output.add(source + "#" + ".".join(key_path) + "=" + str(value))


def _historical_json_objects(
    workspace: Path, pathspecs: Sequence[Any]
) -> list[tuple[str, str, dict[str, Any]]]:
    return list(
        _historical_json_objects_cached(
            str(workspace.resolve()), tuple(str(item) for item in pathspecs)
        )
    )


@lru_cache(maxsize=8)
def _historical_json_objects_cached(
    workspace_raw: str, pathspecs: tuple[str, ...]
) -> tuple[tuple[str, str, dict[str, Any]], ...]:
    workspace = Path(workspace_raw)
    normalized = list(pathspecs)
    if not normalized:
        return ()
    try:
        listed = subprocess.run(
            ["git", "rev-list", "--objects", "--all", "--", *normalized],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise EvidenceQuarantineError("cannot inventory git history") from exc
    candidates: dict[str, str] = {}
    for line in listed:
        object_id, separator, path = line.partition(" ")
        if separator and path.endswith(".json"):
            candidates.setdefault(object_id, path)
    rows: list[tuple[str, str, dict[str, Any]]] = []
    for object_id, path in sorted(candidates.items()):
        try:
            raw = subprocess.run(
                ["git", "cat-file", "blob", object_id],
                cwd=workspace,
                check=True,
                capture_output=True,
            ).stdout
            payload = json.loads(raw.decode("utf-8"))
        except (OSError, subprocess.CalledProcessError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            rows.append((object_id, path, payload))
    return tuple(rows)


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise EvidenceQuarantineError(f"JSON object required: {path}")
    return payload


def _safe_glob(workspace: Path, pattern: str) -> list[Path]:
    if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
        raise EvidenceQuarantineError("exposure glob must stay inside the workspace")
    return [path for path in workspace.glob(pattern) if path.is_file()]


def _expand_patterns(workspace: Path, patterns: Sequence[Any]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(_safe_glob(workspace, str(pattern)))
    return sorted(set(paths))


def _resolve_workspace_path(workspace: Path, raw_path: str) -> Path:
    path = (workspace / raw_path).resolve()
    try:
        path.relative_to(workspace.resolve())
    except ValueError as exc:
        raise EvidenceQuarantineError("path escapes workspace") from exc
    return path


def _is_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value.strip().lower()))


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_manifest_sha256(paths: Sequence[Path], workspace: Path) -> str:
    rows = [
        {
            "path": path.relative_to(workspace).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
    ]
    return _canonical_sha256({"files": rows})


def _path_manifest_sha256(paths: Sequence[Path], workspace: Path) -> str:
    return _canonical_sha256(
        {"paths": [path.relative_to(workspace).as_posix() for path in paths]}
    )


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
    "DEFAULT_POLICY_PATH",
    "EvidenceQuarantineError",
    "assert_formal_run_allowed",
    "audit_evidence_quarantine",
    "build_exposure_inventory",
    "load_evidence_quarantine_policy",
]
