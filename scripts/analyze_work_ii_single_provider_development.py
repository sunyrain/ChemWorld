#!/usr/bin/env python3
"""Build a provider-isolated Work II development analysis."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_development_analysis import (
    build_single_provider_development_analysis,
)

ROOT = Path(__file__).resolve().parents[1]


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source_path = args.sources.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite development analysis: {output}")
    manifest = _load_object(source_path)
    loaded: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for source in manifest.get("sources", []):
        if not isinstance(source, dict):
            raise ValueError("development analysis source must be an object")
        path = Path(str(source["path"]))
        if not path.is_absolute():
            path = ROOT / path
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != source.get("sha256"):
            raise ValueError(f"source hash mismatch: {source['source_id']}")
        loaded.append((source, _load_object(path)))
    report = build_single_provider_development_analysis(manifest, loaded)
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": "completed",
                "analysis_sha256": report["analysis_sha256"],
                "provider_group": report["provider_group"],
                "terminal_cells": report["denominators"]["terminal_record_count"],
                "completed_cells": report["denominators"]["completed_cell_count"],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
