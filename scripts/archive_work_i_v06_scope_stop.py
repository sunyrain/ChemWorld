"""Archive the administrative scope stop for the G2 v0.6 multiworld extension."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6.json")
SCHEDULE_PATH = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_schedule.json")
ANALYSIS_PATH = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_analysis_plan.json")
POWER_PATH = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_power.json")
QUALIFICATION_PATH = Path(
    "configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_world_qualification.json"
)
SCRIPT_PATH = Path("scripts/archive_work_i_v06_scope_stop.py")
RAW_MANIFEST_REPOSITORY_PATH = Path(
    "runs/development/"
    "g2-endpoint-lifecycle-confirmatory-16w-r5-codex-sol-medium-v0.6/"
    "matrix_manifest.json"
)
REPORT_JSON_PATH = Path("workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.json")
REPORT_MD_PATH = Path("workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.md")

PROTOCOL_ID = "g2-endpoint-lifecycle-confirmatory-16w-r5-v0.6"
EXPECTED_STATE_COUNTS = {"completed": 7, "pending": 152, "right_censored": 1}
EXPECTED_COMPLETED_PAIRS = ((13, "r01"), (26, "r01"), (49, "r01"))
EXPECTED_RIGHT_CENSORED_PAIR = (43, "r01")


class ScopeStopArchiveError(RuntimeError):
    """Raised when the frozen design or administrative stop state fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScopeStopArchiveError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise ScopeStopArchiveError(f"JSON root must be an object: {path}")
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ScopeStopArchiveError(f"{key} must be an object")
    return value


def _mapping_rows(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(row, Mapping) for row in value):
        raise ScopeStopArchiveError(f"{key} must be a list of objects")
    return value


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ScopeStopArchiveError(f"cannot read bound file: {path}") from exc
    return digest.hexdigest()


def _canonical_sha256(payload: Any, hash_field: str | None = None) -> str:
    unhashed = deepcopy(payload)
    if hash_field is not None:
        if not isinstance(unhashed, dict):
            raise ScopeStopArchiveError("self-hashed payload must be an object")
        unhashed.pop(hash_field, None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def receipt_sha256(payload: Mapping[str, Any]) -> str:
    """Return the receipt digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "receipt_sha256")


def _validate_self_hash(payload: Mapping[str, Any], field: str, label: str) -> None:
    if payload.get(field) != _canonical_sha256(payload, field):
        raise ScopeStopArchiveError(f"{label} self-hash mismatch")


def _validate_tracked_design(root: Path) -> dict[str, dict[str, Any]]:
    paths = {
        "protocol": PROTOCOL_PATH,
        "schedule": SCHEDULE_PATH,
        "analysis_plan": ANALYSIS_PATH,
        "power_report": POWER_PATH,
        "world_qualification": QUALIFICATION_PATH,
    }
    payloads = {key: _read_json(root / path) for key, path in paths.items()}
    protocol = payloads["protocol"]
    freeze = _mapping(protocol, "confirmatory_freeze")
    claim_policy = _mapping(protocol, "claim_policy")
    if (
        protocol.get("protocol_id") != PROTOCOL_ID
        or protocol.get("status") != "prospective-confirmatory-frozen"
        or freeze.get("frozen_before_first_provider_call") is not True
        or freeze.get("interim_score_inspection") is not False
        or freeze.get("outcome_dependent_stopping") is not False
        or freeze.get("outcome_dependent_expansion") is not False
        or claim_policy.get("development_runs_in_primary_analysis") is not False
    ):
        raise ScopeStopArchiveError("frozen v0.6 outcome-blind design boundary changed")

    binding_map = {
        "full_schedule": (SCHEDULE_PATH, "schedule"),
        "analysis_plan": (ANALYSIS_PATH, "analysis_plan"),
        "power_report": (POWER_PATH, "power_report"),
        "qualification_report": (QUALIFICATION_PATH, "world_qualification"),
    }
    for binding_key, (path, _payload_key) in binding_map.items():
        binding = _mapping(freeze, binding_key)
        if binding.get("path") != path.as_posix() or binding.get("sha256") != _file_sha256(
            root / path
        ):
            raise ScopeStopArchiveError(f"protocol binding changed: {binding_key}")

    schedule = payloads["schedule"]
    power = payloads["power_report"]
    qualification = payloads["world_qualification"]
    _validate_self_hash(schedule, "schedule_sha256", "schedule")
    _validate_self_hash(power, "report_sha256", "power report")
    _validate_self_hash(qualification, "report_sha256", "world qualification")
    if (
        power.get("status") != "passed"
        or power.get("passed") is not True
        or qualification.get("status") != "passed"
        or qualification.get("qualification_uses_agent_scores_or_trajectories") is not False
        or payloads["analysis_plan"].get("status")
        != "prospective-frozen-before-first-confirmatory-provider-call"
    ):
        raise ScopeStopArchiveError("v0.6 qualification, power, or analysis freeze changed")
    return payloads


def scheduled_cells(
    protocol: Mapping[str, Any],
    schedule: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Reconstruct the runner's outcome-free 160-cell schedule."""

    conditions = {
        str(row.get("condition_id")): row for row in _mapping_rows(protocol, "paired_conditions")
    }
    blocks = _mapping_rows(schedule, "pair_blocks")
    cells: list[dict[str, Any]] = []
    ordinal = 0
    for block in blocks:
        condition_order = block.get("condition_order")
        if not isinstance(condition_order, list) or len(condition_order) != 2:
            raise ScopeStopArchiveError("schedule pair block lacks two adjacent conditions")
        for within_pair_order, condition_id_value in enumerate(condition_order, start=1):
            condition_id = str(condition_id_value)
            if condition_id not in conditions:
                raise ScopeStopArchiveError(f"unknown scheduled condition: {condition_id}")
            condition = conditions[condition_id]
            ordinal += 1
            cells.append(
                {
                    "cell_id": f"cell-{ordinal:03d}",
                    "pair_order": int(block["pair_order"]),
                    "schedule_time_block": int(block.get("time_block", block["pair_order"])),
                    "world_seed": int(block["world_seed"]),
                    "trajectory_replicate_id": str(block["replicate_id"]),
                    "agent_seed": int(block["agent_seed"]),
                    "condition_id": condition_id,
                    "within_pair_order": within_pair_order,
                    "material_information": deepcopy(
                        dict(_mapping(condition, "material_information"))
                    ),
                }
            )
    if len(cells) != 160 or len({row["cell_id"] for row in cells}) != 160:
        raise ScopeStopArchiveError("frozen schedule no longer contains 160 unique cells")
    return cells


def _administrative_state(
    raw_manifest: Mapping[str, Any],
    expected_cells: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], tuple[tuple[int, str], ...], tuple[int, str]]:
    raw_rows = _mapping_rows(raw_manifest, "cells")
    if len(raw_rows) != len(expected_cells):
        raise ScopeStopArchiveError("raw matrix cell count differs from the frozen schedule")
    materialized: list[dict[str, Any]] = []
    states_by_pair: dict[tuple[int, str], list[str]] = {}
    state_counts: Counter[str] = Counter()
    for row, expected in zip(raw_rows, expected_cells, strict=True):
        cell = _mapping(row, "cell")
        if dict(cell) != expected:
            raise ScopeStopArchiveError(f"raw matrix identity differs at {expected['cell_id']}")
        state = row.get("state")
        if state not in EXPECTED_STATE_COUNTS:
            raise ScopeStopArchiveError(f"invalid raw cell state: {state}")
        state_text = str(state)
        state_counts[state_text] += 1
        pair_id = (int(cell["world_seed"]), str(cell["trajectory_replicate_id"]))
        states_by_pair.setdefault(pair_id, []).append(state_text)
        if state_text != "pending":
            materialized.append(
                {
                    "cell_id": str(cell["cell_id"]),
                    "condition_id": str(cell["condition_id"]),
                    "state": state_text,
                    "trajectory_replicate_id": pair_id[1],
                    "world_seed": pair_id[0],
                }
            )
    if dict(sorted(state_counts.items())) != EXPECTED_STATE_COUNTS:
        raise ScopeStopArchiveError(f"scope-stop administrative counts changed: {state_counts}")
    completed_pairs = tuple(
        sorted(
            pair_id
            for pair_id, states in states_by_pair.items()
            if states == ["completed", "completed"]
        )
    )
    censored_pairs = [
        pair_id
        for pair_id, states in states_by_pair.items()
        if sorted(states) == ["completed", "right_censored"]
    ]
    if completed_pairs != EXPECTED_COMPLETED_PAIRS or censored_pairs != [
        EXPECTED_RIGHT_CENSORED_PAIR
    ]:
        raise ScopeStopArchiveError("scope-stop pair disposition changed")
    return materialized, completed_pairs, censored_pairs[0]


def _validate_raw_manifest(
    raw_path: Path,
    protocol: Mapping[str, Any],
    schedule: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], tuple[tuple[int, str], ...], tuple[int, str]]:
    raw = _read_json(raw_path)
    _validate_self_hash(raw, "manifest_sha256", "local raw matrix manifest")
    expected_cells = scheduled_cells(protocol, schedule)
    source = _mapping(raw, "source")
    if (
        raw.get("protocol_id") != PROTOCOL_ID
        or raw.get("schema_version") != "chemworld-g2-endpoint-lifecycle-confirmatory-run-0.2"
        or raw.get("run_status") != "running"
        or raw.get("confirmatory_claim_allowed") is not False
        or raw.get("planned_cell_count") != 160
        or raw.get("planned_pair_count") != 80
        or raw.get("planned_physical_experiment_count") != 960
        or raw.get("completed_cell_count") != 7
        or raw.get("right_censored_cell_count") != 1
        or raw.get("completed_pair_audit_count") != 3
        or raw.get("all_materialized_pair_audits_passed") is not True
        or raw.get("protocol_file_sha256") != _file_sha256(ROOT / PROTOCOL_PATH)
        or source.get("protocol_file_sha256") != raw.get("protocol_file_sha256")
        or raw.get("schedule_sha256") != _canonical_sha256(expected_cells)
    ):
        raise ScopeStopArchiveError("local raw matrix administrative boundary changed")
    pair_audits = _mapping_rows(raw, "completed_pair_audits")
    audited_pairs = tuple(
        sorted(
            (int(row["world_seed"]), str(row["trajectory_replicate_id"]))
            for row in pair_audits
            if row.get("passed") is True
        )
    )
    if len(pair_audits) != 3 or audited_pairs != EXPECTED_COMPLETED_PAIRS:
        raise ScopeStopArchiveError("completed pair audit identities changed")
    materialized, completed_pairs, censored_pair = _administrative_state(raw, expected_cells)
    return raw, materialized, completed_pairs, censored_pair


def build_scope_stop_receipt(
    root: Path = ROOT,
    raw_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Build the outcome-blind administrative receipt from frozen design and local state."""

    resolved = root.resolve()
    raw_path = raw_manifest_path or (resolved / RAW_MANIFEST_REPOSITORY_PATH)
    if not raw_path.is_file():
        raise ScopeStopArchiveError(
            "local raw matrix manifest is unavailable; pass --raw-manifest to generate the receipt"
        )
    payloads = _validate_tracked_design(resolved)
    protocol = payloads["protocol"]
    schedule = payloads["schedule"]
    raw, materialized, completed_pairs, censored_pair = _validate_raw_manifest(
        raw_path, protocol, schedule
    )
    tracked_paths = (
        PROTOCOL_PATH,
        SCHEDULE_PATH,
        ANALYSIS_PATH,
        POWER_PATH,
        QUALIFICATION_PATH,
        SCRIPT_PATH,
    )
    receipt: dict[str, Any] = {
        "schema_id": "chemworld.work_i_v06_scope_stop_receipt",
        "schema_version": "0.1.0",
        "receipt_id": "g2-endpoint-lifecycle-confirmatory-v0.6-scope-stop-v0.1",
        "status": "scope_stopped_archived",
        "owner_task": "W1-M04",
        "protocol_id": PROTOCOL_ID,
        "tracked_source_bindings": [
            {"path": path.as_posix(), "sha256": _file_sha256(resolved / path)}
            for path in tracked_paths
        ],
        "local_untracked_source_binding": {
            "bytes": raw_path.stat().st_size,
            "embedded_manifest_sha256": raw["manifest_sha256"],
            "path": RAW_MANIFEST_REPOSITORY_PATH.as_posix(),
            "sha256": _file_sha256(raw_path),
            "tracked_in_git": False,
        },
        "frozen_design": {
            "planned_cells": 160,
            "planned_pairs": 80,
            "planned_physical_experiments": 960,
            "selected_worlds": 16,
            "fresh_replicates_per_world": 5,
            "conditions_per_pair": 2,
            "provider_sampling_seed_controlled": False,
            "outcome_blind_world_qualification": True,
            "frozen_before_first_provider_call": True,
        },
        "administrative_stop_state": {
            "completed_cells": 7,
            "completed_pairs": 3,
            "pending_cells": 152,
            "right_censored_cells": 1,
            "right_censored_pairs": 1,
            "raw_manifest_run_status": "running",
            "raw_manifest_confirmatory_claim_allowed": False,
            "execution_started_at": raw["started_at"],
            "execution_last_updated_at": raw["updated_at"],
            "all_materialized_pair_identity_audits_passed": True,
        },
        "materialized_cells": materialized,
        "completed_pair_identities": [
            {"trajectory_replicate_id": replicate, "world_seed": world}
            for world, replicate in completed_pairs
        ],
        "right_censored_pair_identity": {
            "trajectory_replicate_id": censored_pair[1],
            "world_seed": censored_pair[0],
        },
        "owner_scope_decision": {
            "decision_class": "scope_control_not_statistical_stopping",
            "decision_status": "scope_stopped",
            "complete_pair_scores_or_arm_contrasts_inspected_before_decision": False,
            "decision_assertion_source": "experiment owner",
            "resume_inside_work_i": False,
            "future_reuse_requires_new_scope_and_estimand_freeze": True,
            "partial_trajectories_retained": True,
        },
        "first_arxiv_boundary": {
            "execution_record_may_be_disclosed": True,
            "outcome_values_in_current_estimand": False,
            "cells_pooled_with_g2_v0_5": False,
            "scores_or_arm_contrasts_in_figures": False,
            "confirmatory_or_population_claim_allowed": False,
            "inference_role": "none",
            "historical_configs_remain_frozen": True,
        },
        "repository_hygiene": {
            "raw_provider_responses_copied": False,
            "raw_run_tree_tracked": False,
            "score_fields_copied": False,
            "arm_contrast_fields_copied": False,
            "administrative_identity_and_state_only": True,
        },
    }
    receipt["receipt_sha256"] = receipt_sha256(receipt)
    return receipt


def validate_committed_receipt(
    root: Path = ROOT,
    raw_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Validate the committed self-contained receipt and optionally its local raw binding."""

    resolved = root.resolve()
    receipt = _read_json(resolved / REPORT_JSON_PATH)
    if receipt.get("receipt_sha256") != receipt_sha256(receipt):
        raise ScopeStopArchiveError("committed scope-stop receipt self-hash mismatch")
    if receipt.get("status") != "scope_stopped_archived" or receipt.get("owner_task") != "W1-M04":
        raise ScopeStopArchiveError("committed scope-stop receipt identity changed")
    for binding in _mapping_rows(receipt, "tracked_source_bindings"):
        path_value = binding.get("path")
        sha_value = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(sha_value, str):
            raise ScopeStopArchiveError("invalid tracked source binding")
        if _file_sha256(resolved / path_value) != sha_value:
            raise ScopeStopArchiveError(f"tracked source binding mismatch: {path_value}")
    if raw_manifest_path is not None:
        raw_binding = _mapping(receipt, "local_untracked_source_binding")
        if raw_manifest_path.stat().st_size != raw_binding.get("bytes") or _file_sha256(
            raw_manifest_path
        ) != raw_binding.get("sha256"):
            raise ScopeStopArchiveError("local raw source binding mismatch")
    return receipt


def build_markdown_report(receipt: Mapping[str, Any]) -> str:
    """Render a concise human-readable scope-stop handoff."""

    state = _mapping(receipt, "administrative_stop_state")
    boundary = _mapping(receipt, "first_arxiv_boundary")
    return "\n".join(
        [
            "# G2 v0.6 multiworld extension scope-stop receipt",
            "",
            f"Status: **{receipt['status']}**  ",
            f"Receipt SHA-256: `{receipt['receipt_sha256']}`",
            "",
            "The prospective 16-world extension was stopped by owner scope decision. The raw run",
            (
                "manifest remains an immutable historical execution record; "
                "it is not a completed result."
            ),
            "",
            "| Administrative item | Frozen value |",
            "| --- | ---: |",
            "| Planned cells | 160 |",
            "| Completed cells | 7 |",
            "| Right-censored cells | 1 |",
            "| Pending cells | 152 |",
            "| Complete pairs | 3 |",
            "| Right-censored pairs | 1 |",
            f"| Raw manifest status | {state['raw_manifest_run_status']} |",
            "| Confirmatory claim allowed | no |",
            "",
            "## First-paper boundary",
            "",
            f"- Inference role: `{boundary['inference_role']}`.",
            (
                "- No v0.6 score, outcome value or arm contrast enters the current estimand "
                "or figures."
            ),
            "- No cell is pooled with the frozen G2 v0.5 analysis.",
            "- Resumption requires a new scope decision and a newly frozen estimand.",
            (
                "- Partial trajectories remain retained locally; "
                "raw provider responses remain untracked."
            ),
            "",
            "The receipt contains administrative identity and lifecycle state only.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--raw-manifest", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_path = args.raw_manifest
    default_raw = ROOT / RAW_MANIFEST_REPOSITORY_PATH
    if raw_path is None and default_raw.is_file():
        raw_path = default_raw
    if args.check:
        receipt = validate_committed_receipt(ROOT, raw_path)
        if raw_path is not None:
            rebuilt = build_scope_stop_receipt(ROOT, raw_path)
            if rebuilt != receipt:
                raise SystemExit(
                    "committed receipt differs from the local raw administrative rebuild"
                )
        if (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") != build_markdown_report(receipt):
            raise SystemExit("committed Markdown receipt differs from deterministic rebuild")
    else:
        receipt = build_scope_stop_receipt(ROOT, raw_path)
        (ROOT / REPORT_JSON_PATH).write_text(_json_text(receipt), encoding="utf-8", newline="\n")
        (ROOT / REPORT_MD_PATH).write_text(
            build_markdown_report(receipt), encoding="utf-8", newline="\n"
        )
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "completed_cells": receipt["administrative_stop_state"]["completed_cells"],
                "completed_pairs": receipt["administrative_stop_state"]["completed_pairs"],
                "raw_source_verified": raw_path is not None,
                "receipt_sha256": receipt["receipt_sha256"],
                "status": receipt["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
