#!/usr/bin/env python3
"""Build the retained Work II development baseline analysis."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_development_analysis import build_development_analysis

ROOT = Path(__file__).resolve().parents[1]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    args = _parse_args()
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
        data = path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != source.get("sha256"):
            raise ValueError(f"source hash mismatch: {source['source_id']}")
        loaded.append((source, _load_object(path)))
    report = build_development_analysis(manifest, loaded)
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": "completed",
                "analysis_sha256": report["analysis_sha256"],
                "wellau_terminal_cells": report["wellau_fallback"]["denominators"][
                    "terminal_record_count"
                ],
                "deepseek_terminal_cells": report["deepseek_attempt"]["denominators"][
                    "terminal_record_count"
                ],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
