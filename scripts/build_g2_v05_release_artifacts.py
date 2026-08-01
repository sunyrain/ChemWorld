"""Build the terminal G2 v0.5 file index and compact replay subset."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.data.schema import OUTCOME_LAYER_FIELDS
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.verify import verify_records
from chemworld.schemas.validation import TRAJECTORY_REQUIRED_KEYS

ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA = "chemworld-g2-v0.5-terminal-file-index-0.1"
SUBSET_SCHEMA = "chemworld-g2-v0.5-compact-replay-subset-0.1"
AUDIT_SCHEMA = "chemworld-autonomous-material-trajectory-replication-audit-0.1"
MANIFEST_SCHEMA = "chemworld-g2-trajectory-replication-run-0.1"
_LIVE_ONLY_FILENAMES = {"arxiv_remaining_audit.json"}
_COMPACT_BLANKS: dict[str, Any] = {
    "agent_metadata": {},
    "constitution_checks": [],
    "constraint_flags": {},
    "explanation": {},
    "preconditions": {},
    "processed_estimate": {},
    "raw_signal": {},
    "uncertainty": {},
}
_REPLAY_CONFIGURATION_FIELDS = (
    "benchmark_task_id",
    "contract_profile",
    "electrochemical_workflow_mode",
    "electrochemical_material_family_id",
    "crystallization_material_family_id",
    "scoring_contract_id",
    "observation_noise_mode",
    "observation_noise_namespace",
    "observation_seed",
    "material_information",
    "material_information_config",
    "campaign_resource_card",
)


class G2ReleaseArtifactError(RuntimeError):
    """Raised when the G2 source is incomplete or identity-inconsistent."""


def _load(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise G2ReleaseArtifactError(f"invalid {label}: {path}") from error
    if not isinstance(value, dict):
        raise G2ReleaseArtifactError(f"{label} must be a JSON object")
    return value


def _validate_terminal(
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> None:
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        raise G2ReleaseArtifactError("unsupported G2 replication manifest")
    unhashed = dict(manifest)
    declared_manifest_hash = unhashed.pop("manifest_sha256", None)
    if declared_manifest_hash != canonical_json_sha256(unhashed):
        raise G2ReleaseArtifactError("G2 replication manifest hash is invalid")
    cells = manifest.get("cells")
    if not isinstance(cells, list) or len(cells) != 20:
        raise G2ReleaseArtifactError("G2 replication manifest must contain 20 cells")
    if any(cell.get("state") not in {"completed", "right_censored"} for cell in cells):
        raise G2ReleaseArtifactError("G2 replication matrix is not terminal")
    if audit.get("schema_version") != AUDIT_SCHEMA:
        raise G2ReleaseArtifactError("unsupported G2 replication audit")
    matrix = audit.get("matrix")
    if not isinstance(matrix, dict):
        raise G2ReleaseArtifactError("G2 replication audit has no matrix")
    gates = {
        "terminal_cell_count": (
            matrix.get("completed_cell_count", 0) + matrix.get("right_censored_cell_count", 0) == 20
        ),
        "attempt_selection": matrix.get("all_attempt_selection_policies_verified") is True,
        "physical_pairs": matrix.get("all_physical_pairs_verified") is True,
        "terminal_replay": matrix.get("all_terminal_cells_resource_replay_verified") is True,
    }
    failed = [name for name, passed in gates.items() if not passed]
    if failed:
        raise G2ReleaseArtifactError("G2 replication terminal audit failed: " + ", ".join(failed))


def build_terminal_file_index(
    run_root: Path,
    *,
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    """Hash every durable terminal file without copying its content."""

    _validate_terminal(manifest, audit)
    resolved = run_root.resolve()
    if not resolved.is_dir():
        raise G2ReleaseArtifactError(f"G2 run root does not exist: {resolved}")
    files = sorted(
        path
        for path in resolved.rglob("*")
        if path.is_file() and path.name not in _LIVE_ONLY_FILENAMES
    )
    if any(path.is_symlink() for path in files):
        raise G2ReleaseArtifactError("G2 run root contains a symlinked file")
    records = [
        {
            "path": path.relative_to(resolved).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for path in files
    ]
    payload: dict[str, Any] = {
        "schema_version": INDEX_SCHEMA,
        "scope": "terminal G2 v0.5 fresh-trajectory replication",
        "source_root_id": "g2-autonomous-material-seed1-seed3-r5-v0.5",
        "content_included": False,
        "excluded_live_only_filenames": sorted(_LIVE_ONLY_FILENAMES),
        "manifest_sha256": manifest["manifest_sha256"],
        "replication_audit_sha256": audit["audit_sha256"],
        "file_count": len(records),
        "byte_count": sum(record["bytes"] for record in records),
        "files": records,
    }
    payload["index_sha256"] = canonical_json_sha256(payload)
    return payload


def compact_replay_record(source: Mapping[str, Any]) -> dict[str, Any]:
    """Convert a v0.2 record into the minimal supported v0.1 replay shape."""

    legacy_required = TRAJECTORY_REQUIRED_KEYS - {
        "run_id",
        *OUTCOME_LAYER_FIELDS,
    }
    missing = legacy_required - source.keys()
    if missing:
        raise G2ReleaseArtifactError(
            "source trajectory record lacks legacy replay fields: " + ", ".join(sorted(missing))
        )
    result = {key: source[key] for key in legacy_required}
    result["schema_version"] = "chemworld-trajectory-0.1"
    for key, value in _COMPACT_BLANKS.items():
        result[key] = value
    for key in _REPLAY_CONFIGURATION_FIELDS:
        if key in source:
            result[key] = source[key]
    return result


def _read_compact_trajectory(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise G2ReleaseArtifactError(
                    f"trajectory row {line_number} is not an object: {path}"
                )
            records.append(compact_replay_record(value))
    if not records:
        raise G2ReleaseArtifactError(f"trajectory is empty: {path}")
    return records


def _selected_cells(
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> list[dict[str, Any]]:
    cells = {cell["cell"]["cell_id"]: cell for cell in manifest["cells"]}
    complete_pair = next(
        (pair for pair in audit["paired_trajectories"] if pair["pair_complete"]),
        None,
    )
    if complete_pair is None:
        raise G2ReleaseArtifactError("no complete G2 pair is available for the replay subset")
    pair_key = (
        complete_pair["world_seed"],
        complete_pair["trajectory_replicate_id"],
    )
    selected = [
        cell
        for cell in cells.values()
        if (
            cell["cell"]["world_seed"],
            cell["cell"]["trajectory_replicate_id"],
        )
        == pair_key
    ]
    selected.extend(
        cell
        for cell in cells.values()
        if cell["state"] == "right_censored"
        and cell["cell"]["cell_id"] not in {row["cell"]["cell_id"] for row in selected}
    )
    return sorted(selected, key=lambda cell: cell["cell"]["cell_id"])


def build_compact_replay_subset(
    run_root: Path,
    output_dir: Path,
    *,
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    """Write one complete physical pair plus every right-censored trajectory."""

    _validate_terminal(manifest, audit)
    output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    selected = _selected_cells(manifest, audit)
    for state in selected:
        cell = state["cell"]
        attempt_dir = state.get("authoritative_attempt_dir")
        if not isinstance(attempt_dir, str) or not attempt_dir:
            raise G2ReleaseArtifactError(f"{cell['cell_id']} has no authoritative attempt")
        source_path = run_root / attempt_dir / "trajectory.jsonl"
        records = _read_compact_trajectory(source_path)
        verification = verify_records(records)
        if not verification.verified:
            raise G2ReleaseArtifactError(
                f"compact replay failed for {cell['cell_id']}: {verification.mismatches[:1]}"
            )
        output_path = output_dir / f"{cell['cell_id']}.jsonl"
        output_path.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
            ),
            encoding="utf-8",
        )
        entries.append(
            {
                "cell_id": cell["cell_id"],
                "world_seed": cell["world_seed"],
                "trajectory_replicate_id": cell["trajectory_replicate_id"],
                "condition_id": cell["condition_id"],
                "terminal_state": state["state"],
                "record_count": len(records),
                "source_trajectory_sha256": file_sha256(source_path),
                "compact_path": output_path.name,
                "compact_bytes": output_path.stat().st_size,
                "compact_sha256": file_sha256(output_path),
                "exact_replay": verification.to_dict(),
            }
        )
    payload: dict[str, Any] = {
        "schema_version": SUBSET_SCHEMA,
        "selection_rule": (
            "lexicographically first completed physical pair plus every right-censored cell"
        ),
        "provider_content_included": False,
        "manifest_sha256": manifest["manifest_sha256"],
        "replication_audit_sha256": audit["audit_sha256"],
        "cell_count": len(entries),
        "cells": entries,
    }
    payload["subset_sha256"] = canonical_json_sha256(payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument(
        "--index-output",
        type=Path,
        default=(ROOT / "benchmark/releases/chemworld-serious-v1/g2-v0.5-terminal-file-index.json"),
    )
    parser.add_argument(
        "--subset-output-dir",
        type=Path,
        default=(ROOT / "benchmark/releases/chemworld-serious-v1/g2-v0.5-replay-subset"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    run_root = args.run_root.resolve()
    manifest = _load(run_root / "matrix_manifest.json", label="G2 manifest")
    audit_path = args.audit.resolve() if args.audit is not None else run_root / "audit.json"
    audit = _load(audit_path, label="G2 terminal audit")
    index = build_terminal_file_index(run_root, manifest=manifest, audit=audit)
    write_json_atomic(args.index_output.resolve(), index)
    subset_dir = args.subset_output_dir.resolve()
    subset = build_compact_replay_subset(
        run_root,
        subset_dir,
        manifest=manifest,
        audit=audit,
    )
    write_json_atomic(subset_dir / "manifest.json", subset)
    print(
        json.dumps(
            {
                "terminal_file_count": index["file_count"],
                "terminal_byte_count": index["byte_count"],
                "terminal_index_sha256": index["index_sha256"],
                "replay_subset_cell_count": subset["cell_count"],
                "replay_subset_sha256": subset["subset_sha256"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
