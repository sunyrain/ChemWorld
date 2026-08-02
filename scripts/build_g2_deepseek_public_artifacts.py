"""Build compact replayable public artifacts for the DeepSeek G2 matrix."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from build_g2_v05_release_artifacts import compact_replay_record

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.verify import verify_records

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SCHEMA = "chemworld-g2-deepseek-v0.6-public-trajectory-archive-0.1"
INDEX_SCHEMA = "chemworld-g2-deepseek-v0.6-terminal-file-index-0.1"


class G2DeepSeekPublicArtifactError(RuntimeError):
    """Raised when formal source evidence cannot support a public artifact."""


def _load(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise G2DeepSeekPublicArtifactError(
            f"invalid {label}: {path}"
        ) from error
    if not isinstance(value, dict):
        raise G2DeepSeekPublicArtifactError(f"{label} must be an object")
    return value


def _validate_self_hash(
    payload: Mapping[str, Any],
    *,
    field: str,
    label: str,
) -> None:
    unhashed = dict(payload)
    declared = unhashed.pop(field, None)
    if declared != canonical_json_sha256(unhashed):
        raise G2DeepSeekPublicArtifactError(f"{label} self-hash is invalid")


def _validate_sources(
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    _validate_self_hash(
        manifest,
        field="manifest_sha256",
        label="matrix manifest",
    )
    _validate_self_hash(audit, field="audit_sha256", label="campaign audit")
    cells = manifest.get("cells")
    if not isinstance(cells, list) or len(cells) != 10:
        raise G2DeepSeekPublicArtifactError("matrix must contain ten cells")
    matrix = audit.get("matrix")
    gates = {
        "manifest_completed": manifest.get("run_status") == "completed",
        "execution_valid": manifest.get("execution_valid_cell_count") == 10,
        "task_target": manifest.get("task_target_met_cell_count") == 10,
        "audit_cells": isinstance(matrix, Mapping)
        and matrix.get("cell_count") == 10,
        "closed": isinstance(matrix, Mapping)
        and matrix.get("all_cells_complete") is True,
        "resources": isinstance(matrix, Mapping)
        and matrix.get("all_resource_ledgers_verified") is True,
        "replay": isinstance(matrix, Mapping)
        and matrix.get("all_exact_replays_verified") is True,
        "provider": isinstance(matrix, Mapping)
        and matrix.get("all_provider_sessions_verified") is True,
        "physical_pairs": isinstance(matrix, Mapping)
        and matrix.get("all_pairs_physically_matched") is True,
    }
    failed = [name for name, passed in gates.items() if not passed]
    if failed:
        raise G2DeepSeekPublicArtifactError(
            f"formal source gates failed: {failed}"
        )
    return [cell for cell in cells if isinstance(cell, Mapping)]


def _read_compact(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise G2DeepSeekPublicArtifactError(
                    f"trajectory row {line_number} is not an object: {path}"
                )
            records.append(compact_replay_record(value))
    if not records:
        raise G2DeepSeekPublicArtifactError(f"empty trajectory: {path}")
    return records


def build_public_archive(
    run_root: Path,
    output_dir: Path,
    *,
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    cells = _validate_sources(manifest, audit)
    output_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for cell in sorted(cells, key=lambda row: str(row["cell_id"])):
        attempt_dir = cell.get("authoritative_attempt_dir")
        if not isinstance(attempt_dir, str) or not attempt_dir:
            raise G2DeepSeekPublicArtifactError(
                f"{cell.get('cell_id')} has no authoritative attempt"
            )
        source = run_root / attempt_dir / "trajectory.jsonl"
        records = _read_compact(source)
        verification = verify_records(records)
        if not verification.verified:
            raise G2DeepSeekPublicArtifactError(
                f"compact replay failed for {cell['cell_id']}: "
                f"{verification.mismatches[:1]}"
            )
        output = output_dir / f"{cell['cell_id']}.jsonl"
        output.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in records
            ),
            encoding="utf-8",
            newline="\n",
        )
        entries.append(
            {
                "cell_id": cell["cell_id"],
                "world_seed": cell["world_seed"],
                "condition_id": cell["condition_id"],
                "record_count": len(records),
                "closed_batch_count": cell["closed_batch_count"],
                "source_trajectory_sha256": file_sha256(source),
                "compact_path": output.name,
                "compact_bytes": output.stat().st_size,
                "compact_sha256": file_sha256(output),
                "exact_replay": verification.to_dict(),
            }
        )
    payload: dict[str, Any] = {
        "schema_version": ARCHIVE_SCHEMA,
        "status": "complete_public_replay_archive",
        "scope": "DeepSeek V4 Flash G2 v0.6 matched agent-system demonstration",
        "provider_content_included": False,
        "hidden_evaluator_identity_included": False,
        "matrix_manifest_sha256": manifest["manifest_sha256"],
        "campaign_audit_sha256": audit["audit_sha256"],
        "cell_count": len(entries),
        "record_count": sum(int(entry["record_count"]) for entry in entries),
        "cells": entries,
    }
    payload["archive_sha256"] = canonical_json_sha256(payload)
    return payload


def build_terminal_index(
    run_root: Path,
    *,
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_sources(manifest, audit)
    files = sorted(path for path in run_root.rglob("*") if path.is_file())
    rows = [
        {
            "path": path.relative_to(run_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for path in files
    ]
    payload: dict[str, Any] = {
        "schema_version": INDEX_SCHEMA,
        "scope": "terminal DeepSeek G2 v0.6 formal matrix",
        "content_included": False,
        "matrix_manifest_sha256": manifest["manifest_sha256"],
        "campaign_audit_sha256": audit["audit_sha256"],
        "file_count": len(rows),
        "byte_count": sum(int(row["bytes"]) for row in rows),
        "files": rows,
    }
    payload["index_sha256"] = canonical_json_sha256(payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument(
        "--archive-output-dir",
        type=Path,
        default=(
            ROOT
            / "benchmark/releases/chemworld-serious-v1/"
            "g2-deepseek-v0.6-public-trajectory-archive"
        ),
    )
    parser.add_argument(
        "--index-output",
        type=Path,
        default=(
            ROOT
            / "benchmark/releases/chemworld-serious-v1/"
            "g2-deepseek-v0.6-terminal-file-index.json"
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    run_root = args.run_root.resolve()
    manifest = _load(run_root / "matrix_manifest.json", label="matrix manifest")
    audit = _load(args.audit.resolve(), label="campaign audit")
    archive = build_public_archive(
        run_root,
        args.archive_output_dir.resolve(),
        manifest=manifest,
        audit=audit,
    )
    write_json_atomic(args.archive_output_dir.resolve() / "manifest.json", archive)
    index = build_terminal_index(run_root, manifest=manifest, audit=audit)
    write_json_atomic(args.index_output.resolve(), index)
    print(
        json.dumps(
            {
                "archive_sha256": archive["archive_sha256"],
                "cell_count": archive["cell_count"],
                "record_count": archive["record_count"],
                "index_sha256": index["index_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
