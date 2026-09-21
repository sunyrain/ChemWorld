#!/usr/bin/env python3
"""Export EQ v2 reports with complete sanitized agent-visible scientific I/O."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import scripts.export_work_ii_eq_bounded_equilibrium_reports as legacy
import scripts.export_work_ii_eq_bounded_equilibrium_reports_v2_1 as frozen_v2_1
import scripts.recover_work_ii_eq_bounded_equilibrium_v2 as recovery
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

from chemworld.data.logging import load_jsonl

STEP_SCHEMA = "work-ii-eq-public-agent-visible-trajectory-step-1.0"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _candidate_trajectory_paths(
    root: Path, cell_id: str, effective_result_path: Path
) -> list[Path]:
    candidates = [effective_result_path.parent / "trajectory.jsonl"]
    recovery_record = effective_result_path.parent / "recovery.json"
    if recovery_record.is_file():
        record = eq.read(recovery_record)
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
        if eq.shared.summaries(records) != result.get("batches", []):
            continue
        return path, records
    raise RuntimeError(
        f"no trajectory matches the effective result for {cell_id}; inspected {inspected}"
    )


def public_agent_io_step(cell_id: str, record: Mapping[str, Any]) -> dict[str, Any]:
    explanation = record.get("explanation")
    if not isinstance(explanation, Mapping):
        explanation = {}
    agent_input = explanation.get("decision_context")
    environment_output = record.get("agent_visible_observation")
    if not isinstance(agent_input, Mapping):
        raise RuntimeError(f"trajectory step lacks public agent input for {cell_id}")
    if not isinstance(environment_output, Mapping):
        raise RuntimeError(f"trajectory step lacks agent-visible output for {cell_id}")
    payload = {
        "schema_version": STEP_SCHEMA,
        "cell_id": cell_id,
        "step": record.get("step"),
        "experiment_index": record.get("experiment_index"),
        "agent_input": agent_input,
        "agent_output": {
            "action": record.get("action"),
            "decision_audit": explanation.get("decision_audit"),
        },
        "environment_output": environment_output,
        "transaction": {
            "status": record.get("transaction_status"),
            "rollback_reason": record.get("rollback_reason"),
        },
    }
    legacy._assert_public(payload)
    return payload


def _write_jsonl(path: Path, records: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
            )


def _add_report_link(path: Path) -> None:
    marker = "## Sealed scientific account"
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        raise RuntimeError(f"report marker missing from {path}")
    insertion = (
        "Complete sanitized agent-visible scientific I/O: "
        "[trajectory](trajectory.jsonl). Every attempted operation is retained in order; "
        "private provider events, credentials, session identifiers, usage accounting, and "
        "evaluator-only state are excluded.\n\n"
    )
    path.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")


def export(root: Path, destination: Path) -> dict[str, Any]:
    index = frozen_v2_1.export(root, destination)
    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    trajectory_index: list[dict[str, Any]] = []
    for cell in schedule:
        cell_id = str(cell["cell_id"])
        result, result_path = recovery.effective_result(root, config, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective result for {cell_id}")
        source_path, source_records = effective_source_trajectory(
            root, cell_id, result, result_path
        )
        public_records = [public_agent_io_step(cell_id, record) for record in source_records]
        public_path = destination / "sources" / cell_id / "trajectory.jsonl"
        _write_jsonl(public_path, public_records)
        public_sha256 = _sha256(public_path)
        metadata = {
            "cell_id": cell_id,
            "operations": len(public_records),
            "completed_batches": len(result.get("batches", [])),
            "exact_replay_verified": result.get("exact_replay", {}).get("verified") is True,
            "public_path": public_path.relative_to(destination).as_posix(),
            "public_sha256": public_sha256,
            "effective_source_trajectory_sha256": _sha256(source_path),
        }
        legacy._assert_public(metadata)
        trajectory_index.append(metadata)

        result_public_path = destination / "sources" / cell_id / "RESULT.json"
        public_result = eq.read(result_public_path)
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
        legacy._assert_public(public_result)
        eq.write(result_public_path, public_result)
        _add_report_link(destination / "sources" / cell_id / "EXPERIMENT_REPORT.md")

    trajectory_manifest = {
        "schema_version": "work-ii-eq-public-agent-visible-trajectory-index-1.0",
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
            ],
        },
    }
    legacy._assert_public(trajectory_manifest)
    eq.write(destination / "TRAJECTORY_INDEX.json", trajectory_manifest)

    index["trajectory_export"] = {
        "schema_version": trajectory_manifest["schema_version"],
        "cell_count": trajectory_manifest["cell_count"],
        "operation_count": trajectory_manifest["operation_count"],
        "completed_batch_count": trajectory_manifest["completed_batch_count"],
        "index_path": "TRAJECTORY_INDEX.json",
    }
    legacy._assert_public(index)
    eq.write(destination / "INDEX.json", index)
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\n"
        "The source campaign, posttests, truth generation, and evaluations remain bound to the frozen EQ v2 design. "
        "Public Markdown was generated with the v2.1 rendering fix, and v2.2 adds one complete sanitized agent-visible "
        "scientific-I/O `trajectory.jsonl` per effective EQ/P source. Each file preserves every attempted operation in "
        "order, including the public decision context, selected action, decision audit, agent-visible environment "
        "response, and transaction result. Source/result equality, operation counts, twelve-batch summaries, hashes, "
        "and exact-replay status are checked during export. No source result, sealed response, prediction, truth value, "
        "or score is modified. Authentication material, raw provider event streams, provider session identifiers, "
        "usage accounting, and evaluator-only state remain outside this package.\n",
        encoding="utf-8",
    )
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = export(args.input.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "stage": "export_complete",
                "cells": len(index["cells"]),
                "trajectories": index["trajectory_export"]["cell_count"],
                "operations": index["trajectory_export"]["operation_count"],
                "output": str(args.output.resolve()),
                "exporter": "v2.2-public-agent-visible-trajectory",
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
