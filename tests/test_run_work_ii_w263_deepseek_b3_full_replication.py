from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_work_ii_w263_deepseek_b3_full_replication import (  # noqa: E402
    _completed_receipt_count,
    _halt_reasons,
    _run_summary,
    _tool_event_count,
)


def _result(*, status: str, classification: str | None, receipts: list[dict]) -> dict:
    result = {
        "cell_id": "cell-1",
        "status": status,
        "provider_receipts": receipts,
        "infrastructure_predecessors": [],
    }
    if classification is not None:
        result["failure"] = {"classification": classification}
    return result


def test_participant_schema_failure_is_retained_without_halt() -> None:
    result = _result(
        status="failed",
        classification="participant_schema",
        receipts=[{"status": "completed", "tool_event_count": 0}],
    )
    assert _halt_reasons(result) == []
    assert _completed_receipt_count(result) == 1
    assert _tool_event_count(result) == 0


def test_zero_receipt_infrastructure_and_tools_halt() -> None:
    infrastructure = _result(
        status="failed", classification="runner_infrastructure", receipts=[]
    )
    contaminated = _result(
        status="completed",
        classification=None,
        receipts=[{"status": "completed", "tool_event_count": 2}],
    )
    assert _halt_reasons(infrastructure) == ["zero_receipt_runner_infrastructure"]
    assert _halt_reasons(contaminated) == ["tool_contamination:2"]


def test_run_summary_preserves_scheduled_denominator_and_missing_slots() -> None:
    manifest = {
        "study_id": "study",
        "cells": [{"cell_id": "cell-1"}, {"cell_id": "cell-2"}],
    }
    result = _result(
        status="failed",
        classification="participant_schema",
        receipts=[{"status": "completed", "tool_event_count": 0}],
    )
    summary = _run_summary(manifest, [result], status="partial")
    assert summary["scheduled_session_count"] == 2
    assert summary["terminal_session_count"] == 1
    assert summary["failure_count"] == 1
    assert summary["missing_cell_ids"] == ["cell-2"]
