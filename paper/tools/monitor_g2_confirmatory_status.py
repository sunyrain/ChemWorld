"""Outcome-blind status monitor for the prospective G2 confirmation.

This utility deliberately reads only manifest state and infrastructure metadata.
It never opens a trajectory or completed-cell audit and never emits scores,
metric values, arm differences, or provider response content.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def _load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must be a JSON object")
    return payload


def outcome_blind_status(manifest_path: Path) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    raw_cells = manifest.get("cells")
    if not isinstance(raw_cells, list):
        raise ValueError("manifest cells must be a list")

    state_counts: Counter[str] = Counter()
    attempt_counts: Counter[int] = Counter()
    censoring: list[dict[str, Any]] = []
    for raw_state in raw_cells:
        if not isinstance(raw_state, Mapping):
            raise ValueError("manifest cell state must be an object")
        state = str(raw_state.get("state"))
        state_counts[state] += 1
        attempts = raw_state.get("attempts")
        if not isinstance(attempts, list):
            raise ValueError("manifest attempts must be a list")
        attempt_counts[len(attempts)] += 1
        if state != "right_censored":
            continue
        cell = raw_state.get("cell")
        if not isinstance(cell, Mapping):
            raise ValueError("manifest cell identity must be an object")
        safe_attempts = []
        for attempt in attempts:
            if not isinstance(attempt, Mapping):
                raise ValueError("manifest attempt must be an object")
            safe_attempts.append(
                {
                    "accepted_operation_count": attempt.get("accepted_operation_count"),
                    "run_status": attempt.get("run_status"),
                }
            )
        censoring.append(
            {
                "cell_id": cell.get("cell_id"),
                "world_seed": cell.get("world_seed"),
                "trajectory_replicate_id": cell.get("trajectory_replicate_id"),
                "condition_id": cell.get("condition_id"),
                "schedule_time_block": cell.get("schedule_time_block"),
                "attempts": safe_attempts,
            }
        )

    return {
        "run_status": manifest.get("run_status"),
        "started_at": manifest.get("started_at"),
        "updated_at": manifest.get("updated_at"),
        "planned_cell_count": manifest.get("planned_cell_count"),
        "completed_cell_count": manifest.get("completed_cell_count"),
        "planned_pair_count": manifest.get("planned_pair_count"),
        "completed_pair_audit_count": manifest.get("completed_pair_audit_count"),
        "right_censored_cell_count": manifest.get("right_censored_cell_count"),
        "cell_state_counts": dict(sorted(state_counts.items())),
        "attempt_count_distribution": {
            str(key): value for key, value in sorted(attempt_counts.items())
        },
        "censoring_infrastructure_metadata": censoring,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    print(
        json.dumps(
            outcome_blind_status(args.manifest.resolve()),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
