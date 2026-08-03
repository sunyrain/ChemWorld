from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.archive_work_i_v06_scope_stop import (
    PROTOCOL_PATH,
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    SCHEDULE_PATH,
    ScopeStopArchiveError,
    _canonical_sha256,
    _file_sha256,
    _read_json,
    build_markdown_report,
    build_scope_stop_receipt,
    receipt_sha256,
    scheduled_cells,
    validate_committed_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


def _receipt() -> dict[str, Any]:
    return _read_json(ROOT / REPORT_JSON_PATH)


def _synthetic_raw_manifest(path: Path) -> Path:
    protocol = _read_json(ROOT / PROTOCOL_PATH)
    schedule = _read_json(ROOT / SCHEDULE_PATH)
    cells = scheduled_cells(protocol, schedule)
    raw_cells = []
    for index, cell in enumerate(cells):
        if index == 0:
            state = "right_censored"
        elif index < 8:
            state = "completed"
        else:
            state = "pending"
        raw_cells.append(
            {"attempts": [] if state == "pending" else [{}], "cell": cell, "state": state}
        )
    payload: dict[str, Any] = {
        "all_materialized_pair_audits_passed": True,
        "cells": raw_cells,
        "completed_cell_count": 7,
        "completed_pair_audit_count": 3,
        "completed_pair_audits": [
            {"passed": True, "trajectory_replicate_id": "r01", "world_seed": world}
            for world in (13, 26, 49)
        ],
        "confirmatory_claim_allowed": False,
        "planned_cell_count": 160,
        "planned_pair_count": 80,
        "planned_physical_experiment_count": 960,
        "protocol_file_sha256": _file_sha256(ROOT / PROTOCOL_PATH),
        "protocol_id": "g2-endpoint-lifecycle-confirmatory-16w-r5-v0.6",
        "right_censored_cell_count": 1,
        "run_status": "running",
        "schedule_sha256": _canonical_sha256(cells),
        "schema_version": "chemworld-g2-endpoint-lifecycle-confirmatory-run-0.2",
        "source": {"protocol_file_sha256": _file_sha256(ROOT / PROTOCOL_PATH)},
        "started_at": "2026-08-02T05:48:39+00:00",
        "updated_at": "2026-08-02T06:28:28+00:00",
    }
    payload["manifest_sha256"] = _canonical_sha256(payload, "manifest_sha256")
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_committed_scope_stop_receipt_is_self_hashed_and_source_bound() -> None:
    receipt = validate_committed_receipt(ROOT)
    assert receipt["receipt_sha256"] == receipt_sha256(receipt)
    assert receipt["status"] == "scope_stopped_archived"
    assert receipt["owner_task"] == "W1-M04"
    assert len(receipt["tracked_source_bindings"]) == 6
    assert receipt["local_untracked_source_binding"]["tracked_in_git"] is False
    assert (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") == build_markdown_report(receipt)


def test_receipt_preserves_exact_administrative_stop_counts_and_pair_identities() -> None:
    receipt = _receipt()
    assert receipt["administrative_stop_state"] == {
        "all_materialized_pair_identity_audits_passed": True,
        "completed_cells": 7,
        "completed_pairs": 3,
        "execution_last_updated_at": "2026-08-02T06:28:28.622507+00:00",
        "execution_started_at": "2026-08-02T05:48:39.680505+00:00",
        "pending_cells": 152,
        "raw_manifest_confirmatory_claim_allowed": False,
        "raw_manifest_run_status": "running",
        "right_censored_cells": 1,
        "right_censored_pairs": 1,
    }
    assert receipt["completed_pair_identities"] == [
        {"trajectory_replicate_id": "r01", "world_seed": 13},
        {"trajectory_replicate_id": "r01", "world_seed": 26},
        {"trajectory_replicate_id": "r01", "world_seed": 49},
    ]
    assert receipt["right_censored_pair_identity"] == {
        "trajectory_replicate_id": "r01",
        "world_seed": 43,
    }


def test_receipt_copies_no_score_contrast_or_provider_response_fields() -> None:
    receipt = _receipt()
    assert receipt["repository_hygiene"] == {
        "administrative_identity_and_state_only": True,
        "arm_contrast_fields_copied": False,
        "raw_provider_responses_copied": False,
        "raw_run_tree_tracked": False,
        "score_fields_copied": False,
    }
    assert all(
        set(row) == {"cell_id", "condition_id", "state", "trajectory_replicate_id", "world_seed"}
        for row in receipt["materialized_cells"]
    )
    serialized = json.dumps(receipt, sort_keys=True)
    for forbidden in (
        '"best_final_score"',
        '"final_score_mean"',
        '"final_score_sequence"',
        '"nominal_minus_opaque"',
        '"provider_response"',
    ):
        assert forbidden not in serialized


def test_synthetic_raw_rebuild_and_tampering_fail_closed(tmp_path: Path) -> None:
    raw_path = _synthetic_raw_manifest(tmp_path / "matrix_manifest.json")
    rebuilt = build_scope_stop_receipt(ROOT, raw_path)
    assert rebuilt["administrative_stop_state"]["completed_pairs"] == 3
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    raw["completed_cell_count"] = 8
    raw_path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ScopeStopArchiveError, match="self-hash mismatch"):
        build_scope_stop_receipt(ROOT, raw_path)

    receipt = deepcopy(_receipt())
    receipt["first_arxiv_boundary"]["confirmatory_or_population_claim_allowed"] = True
    assert receipt["receipt_sha256"] != receipt_sha256(receipt)
