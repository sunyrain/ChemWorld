"""Build a paper-sufficient public trajectory archive for G2 v0.5."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from build_g2_v05_release_artifacts import compact_replay_record

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.verify import verify_records

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "chemworld-arxiv-v1-public-trajectory-archive-0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _read_compact(path: Path) -> list[dict[str, Any]]:
    rows = [
        compact_replay_record(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise ValueError(f"trajectory is empty: {path}")
    verification = verify_records(rows)
    if not verification.verified:
        raise ValueError(f"compact trajectory does not replay: {path}")
    return rows


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _final_assay_scores(rows: Sequence[Mapping[str, Any]]) -> list[float]:
    scores: list[float] = []
    for row in rows:
        if (
            row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        ):
            score = row.get("leaderboard_score")
            if not isinstance(score, int | float):
                raise ValueError("committed final assay is missing a leaderboard score")
            scores.append(float(score))
    return scores


def _completed_lookup(audit: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row["cell_id"]): row for row in audit["completed_cells"]}


def _right_censored_lookup(audit: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row["cell_id"]): row for row in audit["right_censored_cells"]}


def _formal_archive(run_root: Path, output_root: Path) -> dict[str, Any]:
    manifest = _load(run_root / "matrix_manifest.json")
    audit = _load(run_root / "audit.json")
    completed = _completed_lookup(audit)
    censored = _right_censored_lookup(audit)
    cells: list[dict[str, Any]] = []
    for state in manifest["cells"]:
        cell = state["cell"]
        cell_id = str(cell["cell_id"])
        attempt_dir = run_root / str(state["authoritative_attempt_dir"])
        source = attempt_dir / "trajectory.jsonl"
        rows = _read_compact(source)
        target = output_root / "formal-matrix" / "trajectories" / f"{cell_id}.jsonl"
        _write_jsonl(target, rows)
        audited = completed.get(cell_id) or censored.get(cell_id)
        if audited is None:
            raise ValueError(f"cell is absent from terminal audit: {cell_id}")
        trajectory_scores = _final_assay_scores(rows)
        audited_scores = audited.get("scores", {}).get("final_score_sequence", [])
        if state["state"] == "completed" and audited_scores != trajectory_scores:
            raise ValueError(f"completed-cell assay scores disagree with audit: {cell_id}")
        cells.append(
            {
                "cell_id": cell_id,
                "world_seed": int(cell["world_seed"]),
                "trajectory_replicate_id": str(cell["trajectory_replicate_id"]),
                "condition_id": str(cell["condition_id"]),
                "terminal_state": str(state["state"]),
                "operation_count": len(rows),
                "completed_final_assays": len(trajectory_scores),
                "final_score_sequence": trajectory_scores,
                "compact_path": target.relative_to(output_root).as_posix(),
                "compact_bytes": target.stat().st_size,
                "compact_sha256": file_sha256(target),
                "source_trajectory_sha256": file_sha256(source),
                "exact_physical_replay_verified": True,
            }
        )
    return {
        "manifest_sha256": manifest["manifest_sha256"],
        "audit_sha256": audit["audit_sha256"],
        "cell_count": len(cells),
        "completed_cell_count": sum(row["terminal_state"] == "completed" for row in cells),
        "right_censored_cell_count": sum(
            row["terminal_state"] == "right_censored" for row in cells
        ),
        "completed_final_assay_count": sum(row["completed_final_assays"] for row in cells),
        "cells": cells,
    }


def _excluded_launch_archive(run_root: Path, output_root: Path) -> dict[str, Any]:
    manifest = _load(run_root / "matrix_manifest.json")
    cells: list[dict[str, Any]] = []
    for cell_id, state in (("cell-001", "completed"), ("cell-002", "audit_required")):
        attempt_dir = run_root / cell_id / "attempt-01"
        source = attempt_dir / "trajectory.jsonl"
        rows = _read_compact(source)
        target = output_root / "excluded-first-launch" / "trajectories" / f"{cell_id}.jsonl"
        _write_jsonl(target, rows)
        config = _load(attempt_dir / "run_config.json")
        summary_path = attempt_dir / "run_summary.json"
        summary = _load(summary_path) if summary_path.is_file() else None
        trajectory_scores = _final_assay_scores(rows)
        if (
            summary is not None
            and summary["behavior"].get("terminal_scores", []) != trajectory_scores
        ):
            raise ValueError(f"first-launch assay scores disagree with summary: {cell_id}")
        cells.append(
            {
                "cell_id": cell_id,
                "world_seed": int(config["world_seed"]),
                "trajectory_replicate_id": str(config["trajectory_replicate_id"]),
                "condition_id": str(config["condition_id"]),
                "incident_state": state,
                "accepted_operation_count": len(rows),
                "completed_final_assays": len(trajectory_scores),
                "final_score_sequence": trajectory_scores,
                "compact_path": target.relative_to(output_root).as_posix(),
                "compact_bytes": target.stat().st_size,
                "compact_sha256": file_sha256(target),
                "source_trajectory_sha256": file_sha256(source),
                "exact_physical_replay_verified": True,
            }
        )
    return {
        "status": "excluded_infrastructure_incident_retained_for_transparency",
        "primary_analysis_included": False,
        "source_manifest_sha256": canonical_json_sha256(manifest),
        "cell_count": len(cells),
        "completed_final_assay_count": sum(row["completed_final_assays"] for row in cells),
        "cells": cells,
    }


def build(formal_root: Path, excluded_root: Path, output_root: Path) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "schema_version": SCHEMA,
        "status": "paper_sufficient_public_archive",
        "provider_response_content_included": False,
        "hidden_evaluator_identity_included": False,
        "scope": (
            "Compact physical-transition trajectories for all 20 terminal formal cells and "
            "both durable cells from the excluded first launch."
        ),
        "formal_matrix": _formal_archive(formal_root, output_root),
        "excluded_first_launch": _excluded_launch_archive(excluded_root, output_root),
    }
    result["archive_sha256"] = canonical_json_sha256(result)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source_root = ROOT.parent / "ChemWorld" / "runs" / "development"
    parser.add_argument(
        "--formal-root",
        type=Path,
        default=source_root / "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v2",
    )
    parser.add_argument(
        "--excluded-root",
        type=Path,
        default=source_root / "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/g2-v0.5-public-trajectory-archive",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output_root = args.output_root.resolve()
    manifest = build(
        args.formal_root.resolve(),
        args.excluded_root.resolve(),
        output_root,
    )
    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "output": str(manifest_path),
                "formal_cells": manifest["formal_matrix"]["cell_count"],
                "excluded_cells": manifest["excluded_first_launch"]["cell_count"],
                "archive_sha256": manifest["archive_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
