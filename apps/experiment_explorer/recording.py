"""Small read-only projections for campaign discovery, without loading full traces."""

from __future__ import annotations

import json
from pathlib import Path


def terminal_assay(row: dict) -> bool:
    action = row.get("action", {})
    status = row.get(
        "transaction_status", row.get("environment_outcome", {}).get("transaction_status")
    )
    return action.get("instrument") == "final_assay" and status == "committed"


def model_name(row: dict) -> str:
    metadata = row.get("agent_metadata") or {}
    usage = (row.get("method_resources") or {}).get("agent_usage") or {}
    provenance = usage.get("model_provenance") or metadata.get("model_provenance") or {}
    return str(
        metadata.get("provider_model")
        or metadata.get("model")
        or provenance.get("model")
        or metadata.get("agent_name")
        or "未声明控制器"
    )


def recording_summary(path: Path) -> dict:
    result = {
        "steps": 0,
        "experiments": 0,
        "final_assays": 0,
        "failed_transactions": 0,
        "decision_notes": 0,
        "error": None,
    }
    previous = None
    with path.open(encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict) or not isinstance(row.get("action"), dict):
                    raise ValueError("Missing action object")
            except ValueError as exc:
                result["error"] = f"Line {line_number}: {exc}"
                break
            if previous is None:
                result.update(
                    task=row.get("benchmark_task_id") or row.get("task_id"),
                    model=model_name(row),
                    episode_mode=row.get("episode_mode"),
                )
            changed = (
                previous is None
                or any(
                    row.get(k) is not None and previous.get(k) is not None and row[k] != previous[k]
                    for k in ("campaign_id", "experiment_index")
                )
                or terminal_assay(previous or {})
            )
            if changed:
                result["experiments"] += 1
            result["steps"] += 1
            result["final_assays"] += int(terminal_assay(row))
            status = row.get("transaction_status")
            result["failed_transactions"] += int(status not in {None, "committed", "unknown"})
            audit = (row.get("explanation") or {}).get("decision_audit") or {}
            result["decision_notes"] += int(audit.get("status") == "provided")
            previous = row
    if previous:
        result["terminated"] = previous.get("terminated") is True
        result["truncated"] = previous.get("truncated") is True
    return result
