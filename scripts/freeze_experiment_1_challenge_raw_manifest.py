#!/usr/bin/env python3
"""Freeze portable digests for the 50 raw public challenge evidence artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_challenge import EXPECTED_BLOCKS, _resolve_report
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

RAW_FILENAMES = {
    "EC-E": "receipts.json",
    "EC-P": "surface-rows.json",
    "EC-S": "rows.json",
    "RX-P": "surface-rows.json",
    "RX-S": "rows.json",
    "PA-E": "receipts.json",
    "PA-P": "receipts.json",
    "PA-S": "receipts.json",
    "C-E": "receipts.json",
    "C-P": "receipts.json",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    registry = _load(args.registry.resolve())
    rows = []
    roots = [path.resolve() for path in args.evidence_root]
    for row in registry.get("rows", []):
        block = f"{row.get('system_id', '')}-{str(row.get('prior_locus', ''))[:1].upper()}"
        if block not in EXPECTED_BLOCKS:
            continue
        evidence = row["qualification_run"]["evidence"]
        report_path = _resolve_report(str(evidence["path"]), roots)
        if file_sha256(report_path) != evidence["sha256"]:
            raise ValueError(f"report digest mismatch for {row['unit_id']}")
        raw_path = report_path.parent / RAW_FILENAMES[block]
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or not raw:
            raise ValueError(f"raw evidence missing for {row['unit_id']}")
        rows.append(
            {
                "unit_id": row["unit_id"],
                "block": block,
                "report_path": evidence["path"],
                "report_sha256": evidence["sha256"],
                "raw_filename": raw_path.name,
                "raw_sha256": file_sha256(raw_path),
                "raw_rows": len(raw),
            }
        )
    if len(rows) != 50 or len({row["unit_id"] for row in rows}) != 50:
        raise ValueError("raw manifest denominator must contain 50 unique units")
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-challenge-raw-manifest-1.1",
        "source_registry_sha256": registry["registry_sha256"],
        "portable_paths_only": True,
        "rows": rows,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output, manifest)
    print(json.dumps({"rows": len(rows), "manifest_sha256": manifest["manifest_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
