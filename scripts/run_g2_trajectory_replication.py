"""Run the frozen seed-1/seed-3 fresh-trajectory replication matrix."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts import run_g2_autonomous_material_matrix as base

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    repository_tree_sha256,
    write_json_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT
    / "configs/benchmark/"
    "g2_autonomous_electrochemical_material_seed1_seed3_r5_v0.5_dev.json"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT
    / "runs/development/"
    "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1"
)
RUNNER_VERSION = "chemworld-g2-trajectory-replication-runner-0.1"
PROTOCOL_SCHEMA_VERSION = (
    "chemworld-g2-autonomous-material-trajectory-replication-0.5"
)
MANIFEST_SCHEMA_VERSION = "chemworld-g2-trajectory-replication-run-0.1"
EXPECTED_WORLD_SEEDS = (1, 3)
EXPECTED_REPLICATE_IDS = ("r01", "r02", "r03", "r04", "r05")
EXPECTED_CONDITIONS = (
    "anonymous_nominal_properties",
    "opaque_codes",
)
_ATTEMPT_PATTERN = re.compile(r"attempt-(\d{2})")


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid {label}: {path}") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} must be a JSON object: {path}")
    return payload


def _condition_map(protocol: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["condition_id"]): deepcopy(dict(item))
        for item in protocol["paired_conditions"]
    }


def _load_protocol(path: Path) -> dict[str, Any]:
    payload = _load_json_object(path, label="trajectory replication protocol")
    if payload.get("schema_version") != PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported trajectory replication protocol schema")
    task = payload.get("task")
    conditions = payload.get("paired_conditions")
    replication = payload.get("trajectory_replication")
    attempt_policy = payload.get("attempt_policy")
    if not all(
        isinstance(item, expected)
        for item, expected in (
            (task, dict),
            (conditions, list),
            (replication, dict),
            (attempt_policy, dict),
        )
    ):
        raise ValueError("protocol task, conditions, replication, and attempt policy are required")
    if tuple(int(seed) for seed in task["world_seeds"]) != EXPECTED_WORLD_SEEDS:
        raise ValueError("replication world seeds must be frozen to [1, 3]")
    condition_ids = tuple(
        sorted(
            str(item.get("condition_id"))
            for item in conditions
            if isinstance(item, Mapping)
        )
    )
    if condition_ids != EXPECTED_CONDITIONS:
        raise ValueError("replication requires exactly nominal and opaque conditions")
    replicate_ids = tuple(str(item) for item in replication["replicate_ids"])
    if replicate_ids != EXPECTED_REPLICATE_IDS:
        raise ValueError("replicate ids must be frozen to r01 through r05")
    if int(replication["fresh_replicates_per_world"]) != 5:
        raise ValueError("fresh_replicates_per_world must equal five")
    blocks = replication.get("pair_blocks")
    if not isinstance(blocks, list) or len(blocks) != 10:
        raise ValueError("trajectory replication requires ten explicit pair blocks")
    observed_keys: set[tuple[int, str]] = set()
    agent_seeds: set[int] = set()
    first_conditions: Counter[str] = Counter()
    for expected_order, block in enumerate(blocks, start=1):
        if not isinstance(block, Mapping):
            raise ValueError("each pair block must be an object")
        if int(block.get("pair_order", -1)) != expected_order:
            raise ValueError("pair_order must be the consecutive frozen schedule")
        world_seed = int(block["world_seed"])
        replicate_id = str(block["replicate_id"])
        key = (world_seed, replicate_id)
        if key in observed_keys:
            raise ValueError(f"duplicate world/replicate pair block: {key}")
        observed_keys.add(key)
        agent_seed = int(block["agent_seed"])
        expected_agent_seed = 120_000 + world_seed * 100 + int(replicate_id[1:])
        if agent_seed != expected_agent_seed or agent_seed in agent_seeds:
            raise ValueError("agent seeds must be unique and match the frozen formula")
        agent_seeds.add(agent_seed)
        order = tuple(str(item) for item in block["condition_order"])
        if len(order) != 2 or set(order) != set(EXPECTED_CONDITIONS):
            raise ValueError("each pair block must contain both conditions once")
        first_conditions[order[0]] += 1
    expected_keys = {
        (world_seed, replicate_id)
        for world_seed in EXPECTED_WORLD_SEEDS
        for replicate_id in EXPECTED_REPLICATE_IDS
    }
    if observed_keys != expected_keys:
        raise ValueError("pair blocks do not cover the frozen world/replicate grid")
    if first_conditions != Counter(dict.fromkeys(EXPECTED_CONDITIONS, 5)):
        raise ValueError("global first-condition order must be balanced 5/5")
    if attempt_policy.get("attempt_directories_are_immutable") is not True:
        raise ValueError("attempt directories must be immutable")
    if int(attempt_policy["maximum_pre_action_provider_attempts_per_cell"]) != 3:
        raise ValueError("pre-action provider attempt ceiling must equal three")
    if attempt_policy.get("outcome_dependent_stopping") is not False:
        raise ValueError("outcome-dependent stopping must be disabled")
    return payload


def _scheduled_cells(protocol: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions = _condition_map(protocol)
    blocks = protocol["trajectory_replication"]["pair_blocks"]
    cells: list[dict[str, Any]] = []
    cell_ordinal = 0
    for block in blocks:
        for within_pair_order, condition_id in enumerate(
            block["condition_order"],
            start=1,
        ):
            cell_ordinal += 1
            condition = conditions[str(condition_id)]
            cells.append(
                {
                    "cell_id": f"cell-{cell_ordinal:03d}",
                    "pair_order": int(block["pair_order"]),
                    "world_seed": int(block["world_seed"]),
                    "trajectory_replicate_id": str(block["replicate_id"]),
                    "agent_seed": int(block["agent_seed"]),
                    "condition_id": str(condition_id),
                    "within_pair_order": within_pair_order,
                    "material_information": deepcopy(
                        dict(condition["material_information"])
                    ),
                }
            )
    return cells


def _source_manifest(config_path: Path) -> dict[str, Any]:
    source_roots = (
        "src/chemworld",
        "scripts/run_g2_autonomous_material_matrix.py",
        "scripts/run_g2_trajectory_replication.py",
        config_path.relative_to(ROOT).as_posix(),
    )
    return {
        "git_commit": git_source_commit(ROOT),
        "worktree_dirty": git_worktree_dirty(
            ROOT,
            excluded_prefixes=("runs/development/",),
        ),
        "material_source_roots": list(source_roots),
        "material_source_tree_sha256": repository_tree_sha256(
            ROOT,
            relative_roots=source_roots,
        ),
        "protocol_file": config_path.relative_to(ROOT).as_posix(),
        "protocol_file_sha256": file_sha256(config_path),
        "runner_version": RUNNER_VERSION,
    }


def _pair_config_sha256(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cell: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
) -> str:
    return base._pair_config_sha256(
        protocol=protocol,
        source=source,
        world_seed=int(cell["world_seed"]),
        card=card,
        method_limits=method_limits,
        trajectory_replicate_id=str(cell["trajectory_replicate_id"]),
        agent_seed=int(cell["agent_seed"]),
    )


def _pair_key(cell: Mapping[str, Any]) -> tuple[int, str]:
    return int(cell["world_seed"]), str(cell["trajectory_replicate_id"])


def _dry_run_report(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    card = base._campaign_card(protocol, qualification=False)
    limits = base._method_limits(protocol, qualification=False)
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for cell in _scheduled_cells(protocol):
        inspection = base._inspect_cell_environment(
            protocol=protocol,
            cell=cell,
            card=card,
            operation_limit=int(limits["operation_limit"]),
        )
        grouped.setdefault(_pair_key(cell), []).append(
            {
                "cell": cell,
                "environment_contract": inspection,
                "pair_config_sha256": _pair_config_sha256(
                    protocol=protocol,
                    source=source,
                    cell=cell,
                    card=card,
                    method_limits=limits,
                ),
            }
        )
    audits = [
        base._pair_audit(items[0], items[1])
        for _, items in sorted(grouped.items())
        if len(items) == 2
    ]
    return {
        "schema_version": "chemworld-g2-trajectory-replication-dry-run-0.1",
        "protocol_id": protocol["protocol_id"],
        "planned_pair_blocks": len(grouped),
        "planned_cells": len(_scheduled_cells(protocol)),
        "planned_physical_experiments": (
            len(_scheduled_cells(protocol)) * int(card.vessel_start_limit)
        ),
        "campaign_resource_card_sha256": card.card_sha256,
        "schedule_sha256": canonical_json_sha256(_scheduled_cells(protocol)),
        "pair_audits": audits,
        "passed": len(audits) == 10 and all(item["passed"] for item in audits),
    }


def _attempt_directories(cell_root: Path) -> list[Path]:
    if not cell_root.exists():
        return []
    unexpected = [
        path.name
        for path in cell_root.iterdir()
        if not path.is_dir() or _ATTEMPT_PATTERN.fullmatch(path.name) is None
    ]
    if unexpected:
        raise RuntimeError(
            f"unexpected entries in immutable cell directory {cell_root}: "
            + ", ".join(sorted(unexpected))
        )
    paths = sorted(cell_root.iterdir())
    observed = [int(_ATTEMPT_PATTERN.fullmatch(path.name).group(1)) for path in paths]
    if observed != list(range(1, len(paths) + 1)):
        raise RuntimeError(f"attempt directories are not consecutive: {cell_root}")
    return paths


def _attempt_classification(summary: Mapping[str, Any]) -> str:
    status = str(summary.get("run_status") or "missing")
    accepted = _accepted_operation_count(summary)
    if status == "completed":
        return "completed"
    if status == "provider_infrastructure_failure" and accepted == 0:
        return "retryable_pre_action_provider_failure"
    if status == "provider_infrastructure_failure" and accepted > 0:
        return "terminal_right_censored_provider_failure"
    if status == "method_resource_limit_exhausted" and accepted > 0:
        return "terminal_right_censored_method_limit"
    return "audit_required"


def _accepted_operation_count(summary: Mapping[str, Any]) -> int:
    raw = summary.get("accepted_operation_count")
    if raw is None:
        behavior = summary.get("behavior")
        if isinstance(behavior, Mapping):
            raw = behavior.get("operation_count")
    return int(raw or 0)


def _attempt_entry(output_root: Path, attempt_root: Path) -> dict[str, Any]:
    summary_path = attempt_root / "run_summary.json"
    config_path = attempt_root / "run_config.json"
    if not summary_path.is_file() or not config_path.is_file():
        return {
            "attempt_id": attempt_root.name,
            "attempt_dir": attempt_root.relative_to(output_root).as_posix(),
            "classification": "audit_required",
            "audit_reason": "attempt lacks immutable run_config.json or run_summary.json",
        }
    summary = _load_json_object(summary_path, label="attempt summary")
    trajectory_path = attempt_root / "trajectory.jsonl"
    environment_contract_path = attempt_root / "environment_contract.json"
    return {
        "attempt_id": attempt_root.name,
        "attempt_dir": attempt_root.relative_to(output_root).as_posix(),
        "run_status": summary.get("run_status"),
        "accepted_operation_count": _accepted_operation_count(summary),
        "classification": _attempt_classification(summary),
        "config_sha256": file_sha256(config_path),
        "summary_sha256": file_sha256(summary_path),
        "trajectory_sha256": (
            file_sha256(trajectory_path) if trajectory_path.is_file() else None
        ),
        "environment_contract_sha256": (
            file_sha256(environment_contract_path)
            if environment_contract_path.is_file()
            else None
        ),
    }


def _cell_state(
    *,
    output_root: Path,
    cell: Mapping[str, Any],
    maximum_pre_action_attempts: int,
) -> dict[str, Any]:
    cell_root = output_root / str(cell["cell_id"])
    attempts = [
        _attempt_entry(output_root, path)
        for path in _attempt_directories(cell_root)
    ]
    if not attempts:
        state = "pending"
    else:
        classifications = [str(item["classification"]) for item in attempts]
        invalid_predecessors = [
            value
            for value in classifications[:-1]
            if value != "retryable_pre_action_provider_failure"
        ]
        if invalid_predecessors:
            raise RuntimeError(
                f"cell has an attempt after a non-retryable predecessor: "
                f"{cell['cell_id']} ({', '.join(invalid_predecessors)})"
            )
        final = classifications[-1]
        if final == "completed":
            state = "completed"
        elif final.startswith("terminal_right_censored"):
            state = "right_censored"
        elif final == "retryable_pre_action_provider_failure":
            state = (
                "pending_provider_retry"
                if len(attempts) < maximum_pre_action_attempts
                else "provider_retry_exhausted"
            )
        else:
            state = "audit_required"
    return {
        "cell": deepcopy(dict(cell)),
        "state": state,
        "attempts": attempts,
        "authoritative_attempt_dir": (
            attempts[-1]["attempt_dir"]
            if attempts and state in {"completed", "right_censored"}
            else None
        ),
    }


def _scan_matrix(
    *,
    output_root: Path,
    schedule: Sequence[Mapping[str, Any]],
    maximum_pre_action_attempts: int,
) -> list[dict[str, Any]]:
    expected_cell_ids = {str(cell["cell_id"]) for cell in schedule}
    unexpected = sorted(
        path.name
        for path in output_root.iterdir()
        if path.is_dir()
        and path.name.startswith("cell-")
        and path.name not in expected_cell_ids
    )
    if unexpected:
        raise RuntimeError(
            "output root contains cells outside the frozen schedule: "
            + ", ".join(unexpected)
        )
    return [
        _cell_state(
            output_root=output_root,
            cell=cell,
            maximum_pre_action_attempts=maximum_pre_action_attempts,
        )
        for cell in schedule
    ]


def _validate_attempt_identity(
    *,
    attempt_root: Path,
    cell: Mapping[str, Any],
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
) -> dict[str, Any]:
    config_path = attempt_root / "run_config.json"
    summary_path = attempt_root / "run_summary.json"
    config = _load_json_object(config_path, label="attempt run config")
    summary = _load_json_object(summary_path, label="attempt run summary")
    unhashed = dict(config)
    declared_hash = unhashed.pop("config_sha256", None)
    expected_pair_hash = _pair_config_sha256(
        protocol=protocol,
        source=source,
        cell=cell,
        card=card,
        method_limits=method_limits,
    )
    checks = {
        "config_hash": declared_hash == canonical_json_sha256(unhashed),
        "protocol": config.get("protocol_id") == protocol["protocol_id"],
        "cell": config.get("cell") == dict(cell),
        "world_seed": config.get("world_seed") == int(cell["world_seed"]),
        "replicate": config.get("trajectory_replicate_id")
        == cell["trajectory_replicate_id"],
        "agent_seed": config.get("agent_seed") == int(cell["agent_seed"]),
        "source": config.get("source", {}).get("material_source_tree_sha256")
        == source["material_source_tree_sha256"],
        "protocol_file": config.get("source", {}).get("protocol_file_sha256")
        == source["protocol_file_sha256"],
        "cli": config.get("codex_cli") == dict(cli),
        "pair_hash": config.get("pair_config_sha256") == expected_pair_hash,
        "summary_cell": summary.get("cell") == dict(cell),
        "summary_config": summary.get("config_sha256") == declared_hash,
        "summary_pair": summary.get("pair_config_sha256") == expected_pair_hash,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(
            f"attempt identity validation failed for {cell['cell_id']}: "
            + ", ".join(failed)
        )
    trajectory_path = attempt_root / "trajectory.jsonl"
    accepted = _accepted_operation_count(summary)
    if accepted > 0:
        if not trajectory_path.is_file():
            raise RuntimeError("accepted operations exist without a trajectory")
        records = base.load_jsonl(trajectory_path)
        if len(records) != accepted:
            raise RuntimeError("accepted operation count does not match trajectory")
        if summary.get("trajectory_sha256") != file_sha256(trajectory_path):
            raise RuntimeError("failure summary does not bind trajectory bytes")
    elif trajectory_path.is_file() and base.load_jsonl(trajectory_path):
        raise RuntimeError("zero-operation attempt contains trajectory records")
    return summary


def _load_completed_summary(
    *,
    attempt_root: Path,
    cell: Mapping[str, Any],
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
) -> dict[str, Any]:
    return base._validated_resume_result(
        cell_root=attempt_root,
        cell=cell,
        protocol=protocol,
        source=source,
        cli=cli,
        card=card,
        method_limits=method_limits,
    )


def _materialized_summaries(
    *,
    output_root: Path,
    states: Sequence[Mapping[str, Any]],
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for state in states:
        cell = state["cell"]
        authoritative = state.get("authoritative_attempt_dir")
        if authoritative is None:
            continue
        attempt_root = output_root / str(authoritative)
        if state["state"] == "completed":
            summary = _load_completed_summary(
                attempt_root=attempt_root,
                cell=cell,
                protocol=protocol,
                source=source,
                cli=cli,
                card=card,
                method_limits=method_limits,
            )
        else:
            summary = _validate_attempt_identity(
                attempt_root=attempt_root,
                cell=cell,
                protocol=protocol,
                source=source,
                cli=cli,
                card=card,
                method_limits=method_limits,
            )
        summaries[str(cell["cell_id"])] = summary
    return summaries


def _manifest_status(states: Sequence[Mapping[str, Any]]) -> str:
    state_values = [str(item["state"]) for item in states]
    if "audit_required" in state_values:
        return "audit_required"
    if "provider_retry_exhausted" in state_values:
        return "provider_retry_exhausted"
    if all(value in {"completed", "right_censored"} for value in state_values):
        return (
            "completed"
            if all(value == "completed" for value in state_values)
            else "completed_with_right_censoring"
        )
    return "running"


def _write_manifest(
    path: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    started_at: str,
    states: Sequence[Mapping[str, Any]],
    summaries: Mapping[str, Mapping[str, Any]],
    schedule: Sequence[Mapping[str, Any]],
    card: Any,
) -> dict[str, Any]:
    pair_results: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for state in states:
        cell = state["cell"]
        summary = summaries.get(str(cell["cell_id"]))
        if state["state"] == "completed" and summary is not None:
            pair_results.setdefault(_pair_key(cell), []).append(summary)
    pair_audits = [
        base._pair_audit(items[0], items[1])
        for _, items in sorted(pair_results.items())
        if len(items) == 2
    ]
    status = _manifest_status(states)
    payload: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "run_status": status,
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "started_at": started_at,
        "updated_at": _now(),
        "source": deepcopy(dict(source)),
        "codex_cli": deepcopy(dict(cli)),
        "world_seeds": list(EXPECTED_WORLD_SEEDS),
        "trajectory_replicate_ids": list(EXPECTED_REPLICATE_IDS),
        "schedule_sha256": canonical_json_sha256(schedule),
        "campaign_resource_card_sha256": card.card_sha256,
        "planned_pair_count": len(schedule) // 2,
        "planned_cell_count": len(schedule),
        "planned_physical_experiment_count": (
            len(schedule) * int(card.vessel_start_limit)
        ),
        "completed_cell_count": sum(
            state["state"] == "completed" for state in states
        ),
        "right_censored_cell_count": sum(
            state["state"] == "right_censored" for state in states
        ),
        "cells": [deepcopy(dict(state)) for state in states],
        "completed_pair_audits": pair_audits,
        "completed_pair_audit_count": len(pair_audits),
        "all_materialized_pair_audits_passed": all(
            audit["passed"] for audit in pair_audits
        ),
        "protocol_file_sha256": source["protocol_file_sha256"],
    }
    payload["manifest_sha256"] = canonical_json_sha256(payload)
    write_json_atomic(path, payload)
    return payload


def _validate_resume_manifest(
    manifest_path: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    schedule: Sequence[Mapping[str, Any]],
) -> str:
    manifest = _load_json_object(manifest_path, label="replication manifest")
    manifest_source = manifest.get("source")
    checks = {
        "schema": manifest.get("schema_version") == MANIFEST_SCHEMA_VERSION,
        "runner": manifest.get("runner_version") == RUNNER_VERSION,
        "protocol": manifest.get("protocol_id") == protocol["protocol_id"],
        "schedule": manifest.get("schedule_sha256")
        == canonical_json_sha256(schedule),
        "source": isinstance(manifest_source, Mapping)
        and manifest_source.get("material_source_tree_sha256")
        == source["material_source_tree_sha256"]
        and manifest_source.get("protocol_file_sha256")
        == source["protocol_file_sha256"],
        "cli": manifest.get("codex_cli") == dict(cli),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(
            "replication resume identity mismatch: " + ", ".join(failed)
        )
    return str(manifest.get("started_at") or _now())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate all ten frozen physical pair blocks without Codex.",
    )
    parser.add_argument(
        "--allow-external-provider",
        action="store_true",
        help="Required opt-in for native Codex execution.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume immutable attempts without replacing finalized trajectories.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config_path = args.config.resolve()
    protocol = _load_protocol(config_path)
    source = _source_manifest(config_path)
    schedule = _scheduled_cells(protocol)
    if args.dry_run:
        print(
            json.dumps(
                _dry_run_report(protocol=protocol, source=source),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")

    output_root = args.output_root.resolve()
    manifest_path = output_root / "matrix_manifest.json"
    if output_root.exists() and not args.resume:
        raise FileExistsError(
            f"refusing to overwrite existing output root: {output_root}"
        )
    output_root.mkdir(parents=True, exist_ok=True)
    cli = base._codex_cli_manifest()
    card = base._campaign_card(protocol, qualification=False)
    method_limits = base._method_limits(protocol, qualification=False)
    maximum_attempts = int(
        protocol["attempt_policy"][
            "maximum_pre_action_provider_attempts_per_cell"
        ]
    )
    started_at = _now()
    if args.resume:
        if not manifest_path.is_file():
            if any(output_root.iterdir()):
                raise RuntimeError(
                    "resume requires matrix_manifest.json in a non-empty output root"
                )
        else:
            started_at = _validate_resume_manifest(
                manifest_path,
                protocol=protocol,
                source=source,
                cli=cli,
                schedule=schedule,
            )

    while True:
        states = _scan_matrix(
            output_root=output_root,
            schedule=schedule,
            maximum_pre_action_attempts=maximum_attempts,
        )
        summaries = _materialized_summaries(
            output_root=output_root,
            states=states,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=method_limits,
        )
        manifest = _write_manifest(
            manifest_path,
            protocol=protocol,
            source=source,
            cli=cli,
            started_at=started_at,
            states=states,
            summaries=summaries,
            schedule=schedule,
            card=card,
        )
        if manifest["run_status"] in {
            "completed",
            "completed_with_right_censoring",
        }:
            return 0 if manifest["run_status"] == "completed" else 2
        if manifest["run_status"] != "running":
            raise RuntimeError(
                f"replication cannot continue: {manifest['run_status']}"
            )
        next_state = next(
            state
            for state in states
            if state["state"] in {"pending", "pending_provider_retry"}
        )
        cell = next_state["cell"]
        cell_root = output_root / str(cell["cell_id"])
        cell_root.mkdir(parents=True, exist_ok=True)
        attempt_number = len(next_state["attempts"]) + 1
        attempt_root = cell_root / f"attempt-{attempt_number:02d}"
        try:
            base._run_cell(
                protocol=protocol,
                source=source,
                cli=cli,
                cell=cell,
                cell_root=attempt_root,
                card=card,
                method_limits=method_limits,
                qualification=False,
            )
        except Exception as error:
            refreshed = _scan_matrix(
                output_root=output_root,
                schedule=schedule,
                maximum_pre_action_attempts=maximum_attempts,
            )
            refreshed_summaries = _materialized_summaries(
                output_root=output_root,
                states=refreshed,
                protocol=protocol,
                source=source,
                cli=cli,
                card=card,
                method_limits=method_limits,
            )
            failed_manifest = _write_manifest(
                manifest_path,
                protocol=protocol,
                source=source,
                cli=cli,
                started_at=started_at,
                states=refreshed,
                summaries=refreshed_summaries,
                schedule=schedule,
                card=card,
            )
            failed_cell_state = next(
                state
                for state in refreshed
                if state["cell"]["cell_id"] == cell["cell_id"]
            )["state"]
            if failed_cell_state in {
                "pending_provider_retry",
                "right_censored",
            }:
                continue
            raise RuntimeError(
                f"replication stopped after {cell['cell_id']}: "
                f"{failed_manifest['run_status']}"
            ) from error


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_CONFIG",
    "DEFAULT_OUTPUT_ROOT",
    "MANIFEST_SCHEMA_VERSION",
    "PROTOCOL_SCHEMA_VERSION",
    "RUNNER_VERSION",
    "main",
]
