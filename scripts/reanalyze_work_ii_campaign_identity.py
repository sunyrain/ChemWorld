"""Reconstruct stable batch identities for historical Work II campaign results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"expected an object at {path}:{line_number}")
        rows.append(value)
    return rows


def _operation(row: dict[str, Any]) -> str | None:
    operation = row.get("operation_type")
    if isinstance(operation, str):
        return operation
    action = row.get("action")
    if isinstance(action, dict) and isinstance(action.get("operation"), str):
        return str(action["operation"])
    return None


def _is_completed(row: dict[str, Any]) -> bool:
    return (
        row.get("transaction_status") == "committed"
        and _operation(row) == "measure"
        and row.get("instrument") == "final_assay"
    )


def _is_discarded(row: dict[str, Any]) -> bool:
    return row.get("transaction_status") == "committed" and _operation(row) == "discard_batch"


def _lifecycle_index(row: dict[str, Any]) -> int:
    raw = row.get("experiment_index")
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
        raise ValueError("terminal trajectory row lacks a valid zero-based experiment_index")
    return raw + 1


def _recommendation(summary: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    receipts = summary.get("provider_receipts")
    if isinstance(receipts, list):
        for receipt in reversed(receipts):
            if not isinstance(receipt, dict):
                continue
            recommendation = receipt.get("final_recommendation")
            if isinstance(recommendation, dict):
                return recommendation, receipt
    analysis = summary.get("analysis")
    if isinstance(analysis, dict) and isinstance(analysis.get("final_recommendation"), dict):
        return dict(analysis["final_recommendation"]), {}
    return None, {}


def _cell_result(cell_root: Path) -> dict[str, Any]:
    summary = _read_object(cell_root / "summary.json")
    trajectory = _read_jsonl(cell_root / "trajectory.jsonl")
    experiments: list[dict[str, Any]] = []
    discarded_batch_indices: list[int] = []
    closed_indices: list[int] = []
    for row in trajectory:
        if not (_is_completed(row) or _is_discarded(row)):
            continue
        lifecycle_index = _lifecycle_index(row)
        if lifecycle_index in closed_indices:
            raise ValueError(f"duplicate terminal lifecycle index in {cell_root.name}")
        closed_indices.append(lifecycle_index)
        if _is_discarded(row):
            discarded_batch_indices.append(lifecycle_index)
            continue
        score = row.get("leaderboard_score")
        experiments.append(
            {
                "experiment_index": lifecycle_index,
                "lifecycle_experiment_index": lifecycle_index,
                "experiment_index_base": 1,
                "batch_id": f"batch-{lifecycle_index:04d}",
                "completed_ordinal": len(experiments) + 1,
                "leaderboard_score": (
                    float(score)
                    if isinstance(score, int | float) and not isinstance(score, bool)
                    else None
                ),
            }
        )
    recommendation, receipt = _recommendation(summary)
    selected_index = recommendation.get("selected_experiment_index") if recommendation else None
    selected = next(
        (
            item
            for item in experiments
            if item["lifecycle_experiment_index"] == selected_index
        ),
        None,
    )
    scored = [item for item in experiments if item["leaderboard_score"] is not None]
    incumbent = (
        min(
            scored,
            key=lambda item: (
                -float(item["leaderboard_score"]),
                item["lifecycle_experiment_index"],
            ),
        )
        if scored
        else None
    )
    qualification = summary.get("qualification")
    qualification = qualification if isinstance(qualification, dict) else {}
    checks = qualification.get("checks")
    checks = checks if isinstance(checks, dict) else {}
    selected_score = selected.get("leaderboard_score") if selected else None
    incumbent_score = incumbent.get("leaderboard_score") if incumbent else None
    host_committed = receipt.get("final_recommendation_source") == "host_mcp_commit"
    return {
        "cell_id": cell_root.name,
        "prior_arm": summary.get("arm"),
        "world_seed": summary.get("world_seed"),
        "closed_batch_count": len(closed_indices),
        "completed_experiment_count": len(experiments),
        "discarded_batch_count": len(discarded_batch_indices),
        "discarded_batch_indices": discarded_batch_indices,
        "experiments": experiments,
        "recommendation": recommendation,
        "recommendation_identity_valid": selected is not None,
        "selected_batch_id": selected.get("batch_id") if selected else None,
        "selected_completed_ordinal": selected.get("completed_ordinal") if selected else None,
        "selected_leaderboard_score": selected_score,
        "incumbent_lifecycle_experiment_index": (
            incumbent.get("lifecycle_experiment_index") if incumbent else None
        ),
        "incumbent_batch_id": incumbent.get("batch_id") if incumbent else None,
        "incumbent_leaderboard_score": incumbent_score,
        "recommendation_selected_public_incumbent": (
            selected is not None
            and incumbent is not None
            and selected["lifecycle_experiment_index"]
            == incumbent["lifecycle_experiment_index"]
        ),
        "recommendation_regret": (
            float(incumbent_score) - float(selected_score)
            if incumbent_score is not None and selected_score is not None
            else None
        ),
        "host_recommendation_committed": host_committed,
        "legacy_index_bound_blocked_host_commit": selected is not None and not host_committed,
        "legacy_checkpoint_timing_confounded": bool(discarded_batch_indices),
        "historical_qualification_passed": qualification.get("passed") is True,
        "historical_failed_checks": sorted(
            str(key) for key, value in checks.items() if value is not True
        ),
    }


def reanalyze(run_root: Path) -> dict[str, Any]:
    cells_root = run_root / "cells"
    cells = [_cell_result(path) for path in sorted(cells_root.iterdir()) if path.is_dir()]
    return {
        "schema_version": "chemworld-work-ii-campaign-identity-reanalysis-0.1",
        "source_run_id": run_root.name,
        "identity_contract": {
            "batch_id": "stable batch-XXXX identity",
            "lifecycle_experiment_index": "1-based batch lifecycle index used for selection",
            "completed_ordinal": "1-based order among successful final assays only",
            "evidence_id": "experiment-{completed_ordinal}-final-assay",
        },
        "cell_count": len(cells),
        "completed_experiment_count": sum(
            int(cell["completed_experiment_count"]) for cell in cells
        ),
        "discarded_batch_count": sum(int(cell["discarded_batch_count"]) for cell in cells),
        "historical_qualification_pass_count": sum(
            cell["historical_qualification_passed"] is True for cell in cells
        ),
        "recommendation_identity_valid_count": sum(
            cell["recommendation_identity_valid"] is True for cell in cells
        ),
        "recommendation_selected_public_incumbent_count": sum(
            cell["recommendation_selected_public_incumbent"] is True for cell in cells
        ),
        "host_recommendation_commit_count": sum(
            cell["host_recommendation_committed"] is True for cell in cells
        ),
        "legacy_index_bound_blocked_host_commit_count": sum(
            cell["legacy_index_bound_blocked_host_commit"] is True for cell in cells
        ),
        "legacy_checkpoint_timing_confounded_cell_count": sum(
            cell["legacy_checkpoint_timing_confounded"] is True for cell in cells
        ),
        "interpretation_limits": [
            "Raw provider payloads and historical qualification decisions are preserved.",
            "Recommendation identity and endpoint regret are corrected from raw lifecycle rows.",
            "Belief-checkpoint timing in cells with discards remains participant-affected "
            "and is not retroactively repaired.",
            "A recovered intended recommendation is not relabelled as a historical host commit.",
        ],
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = reanalyze(args.run_root.resolve(strict=True))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in result.items() if key != "cells"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
