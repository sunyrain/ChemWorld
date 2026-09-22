#!/usr/bin/env python3
"""Add complete sanitized agent-visible source trajectories to EQ-S/E reports."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.export_work_ii_eq_bounded_equilibrium_reports_v2_2 as trajectory_export
import scripts.export_work_ii_eq_entity_reports_v0_2 as entity_export
import scripts.export_work_ii_eq_structural_reports_v0_3 as structural_export
import scripts.run_work_ii_eq_entity_v0_2 as entity
import scripts.run_work_ii_eq_structural_v0_3 as structural

from chemworld.data.logging import load_jsonl


def _adapter(
    locus: str,
) -> tuple[Any, Callable[[Any], None], Callable[[Sequence[Mapping[str, Any]]], list[dict[str, Any]]]]:
    if locus == "S":
        return structural, structural_export._assert_public, structural.eq_v1.shared.summaries
    if locus == "E":
        return entity, entity_export._assert_public, entity.eq_runtime.shared.summaries
    raise ValueError(f"unsupported EQ locus: {locus}")


def _candidate_trajectory_paths(
    root: Path, cell_id: str, effective_result_path: Path
) -> list[Path]:
    candidates = [effective_result_path.parent / "trajectory.jsonl"]
    recovery_record = effective_result_path.parent / "recovery.json"
    if recovery_record.is_file():
        record = json.loads(recovery_record.read_text(encoding="utf-8"))
        source_folder = record.get("source_receipt_folder")
        if source_folder:
            source_folder = Path(str(source_folder))
            if not source_folder.is_absolute():
                source_folder = root / source_folder
            candidates.append(source_folder / "trajectory.jsonl")
    candidates.append(root / "sources" / cell_id / "trajectory.jsonl")
    return list(dict.fromkeys(path.resolve() for path in candidates))


def effective_source_trajectory(
    root: Path,
    cell_id: str,
    result: Mapping[str, Any],
    effective_result_path: Path,
    summarize: Callable[[Sequence[Mapping[str, Any]]], list[dict[str, Any]]],
) -> tuple[Path, list[dict[str, Any]]]:
    expected_operations = result.get("operations")
    inspected: list[str] = []
    for path in _candidate_trajectory_paths(root, cell_id, effective_result_path):
        if not path.is_file():
            inspected.append(f"{path}:missing")
            continue
        records = load_jsonl(path)
        inspected.append(f"{path}:{len(records)}")
        if len(records) != expected_operations:
            continue
        if summarize(records) != result.get("batches", []):
            continue
        return path, records
    raise RuntimeError(
        f"no trajectory matches the effective result for {cell_id}; inspected {inspected}"
    )


def _add_report_link(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "[trajectory](trajectory.jsonl)" in text:
        return
    marker = "## K1"
    if marker not in text:
        raise RuntimeError(f"K1 marker missing from {path}")
    insertion = (
        "Complete sanitized agent-visible scientific I/O: "
        "[trajectory](trajectory.jsonl). Every attempted operation is retained in order; "
        "private provider events, credentials, session identifiers, usage accounting, and "
        "evaluator-only state are excluded.\n\n"
    )
    path.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")


def _update_reproduction(path: Path, locus: str) -> None:
    heading = "## Public agent-visible source trajectories"
    text = path.read_text(encoding="utf-8").rstrip()
    if heading in text:
        return
    addition = (
        f"\n\n{heading}\n\n"
        f"The public EQ-{locus} package contains one sanitized `trajectory.jsonl` for each "
        "effective source campaign. Every attempted operation remains in order with the public "
        "decision context, selected action and audit, complete agent-visible environment response, "
        "and transaction result. Export requires exact operation-count and twelve-batch-summary "
        "equality between the effective source trajectory, effective result, and existing public "
        "result. Authentication material, raw provider events, provider session identifiers, usage "
        "accounting, evaluator-only state, and private world parameters remain excluded. No source "
        "campaign, posttest, prediction, truth value, or score is rerun or changed.\n"
    )
    path.write_text(text + addition, encoding="utf-8")


def augment(locus: str, root: Path, destination: Path) -> dict[str, Any]:
    runner, assert_public, summarize = _adapter(locus)
    if not destination.is_dir():
        raise RuntimeError(f"public destination is missing: {destination}")
    config = runner.load_config()
    schedule = runner.validate_design(config)["schedule"]
    trajectory_index: list[dict[str, Any]] = []
    for cell in schedule:
        cell_id = str(cell["cell_id"])
        result, result_path = runner.effective_result(root, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective EQ-{locus} result for {cell_id}")

        public_result_path = destination / "sources" / cell_id / "RESULT.json"
        public_result = runner.read(public_result_path)
        if public_result.get("cell", {}).get("operations") != result.get("operations"):
            raise RuntimeError(f"operation count differs between raw and public result: {cell_id}")
        if public_result.get("source", {}).get("batches") != result.get("batches", []):
            raise RuntimeError(f"batch summaries differ between raw and public result: {cell_id}")

        source_path, source_records = effective_source_trajectory(
            root, cell_id, result, result_path, summarize
        )
        public_records = [
            trajectory_export.public_agent_io_step(cell_id, record)
            for record in source_records
        ]
        public_path = destination / "sources" / cell_id / "trajectory.jsonl"
        trajectory_export._write_jsonl(public_path, public_records)
        metadata = {
            "cell_id": cell_id,
            "operations": len(public_records),
            "completed_batches": len(result.get("batches", [])),
            "exact_replay_verified": result.get("exact_replay", {}).get("verified") is True,
            "public_path": public_path.relative_to(destination).as_posix(),
            "public_sha256": trajectory_export._sha256(public_path),
            "effective_source_trajectory_sha256": trajectory_export._sha256(source_path),
        }
        assert_public(metadata)
        trajectory_index.append(metadata)

        public_result["source"]["agent_visible_trajectory"] = {
            key: metadata[key]
            for key in (
                "operations",
                "completed_batches",
                "exact_replay_verified",
                "public_path",
                "public_sha256",
                "effective_source_trajectory_sha256",
            )
        }
        assert_public(public_result)
        runner.write(public_result_path, public_result)
        _add_report_link(destination / "sources" / cell_id / "EXPERIMENT_REPORT.md")

    manifest = {
        "schema_version": "work-ii-eq-public-agent-visible-trajectory-index-1.0",
        "locus": locus,
        "cells": trajectory_index,
        "cell_count": len(trajectory_index),
        "operation_count": sum(row["operations"] for row in trajectory_index),
        "completed_batch_count": sum(row["completed_batches"] for row in trajectory_index),
        "privacy_boundary": {
            "included": [
                "agent decision context",
                "selected action and decision audit",
                "complete agent-visible environment response",
                "transaction status and rollback reason",
            ],
            "excluded": [
                "authentication material",
                "raw provider event streams",
                "provider session identifiers",
                "usage accounting",
                "evaluator-only state",
                "private world parameters",
            ],
        },
    }
    assert_public(manifest)
    runner.write(destination / "TRAJECTORY_INDEX.json", manifest)

    index_path = destination / "INDEX.json"
    index = runner.read(index_path)
    index["trajectory_export"] = {
        "schema_version": manifest["schema_version"],
        "cell_count": manifest["cell_count"],
        "operation_count": manifest["operation_count"],
        "completed_batch_count": manifest["completed_batch_count"],
        "index_path": "TRAJECTORY_INDEX.json",
    }
    assert_public(index)
    runner.write(index_path, index)
    _update_reproduction(destination / "REPRODUCE.md", locus)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locus", choices=("S", "E"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = augment(args.locus, args.input.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "stage": "eq_public_trajectory_export_complete",
                "locus": args.locus,
                "cells": manifest["cell_count"],
                "operations": manifest["operation_count"],
                "batches": manifest["completed_batch_count"],
                "output": str(args.output.resolve()),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
