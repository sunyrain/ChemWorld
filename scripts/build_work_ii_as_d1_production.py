#!/usr/bin/env python3
"""Materialize/check the provider-blocked five-seed Work II A-S D1 schedule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_as_d1_production import (
    build_as_d1_production_materialization,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIRECTORY = ROOT / "configs/benchmark/work_ii_as_d1_production"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_or_check(path: Path, value: dict[str, object], *, check: bool) -> None:
    if check:
        if not path.is_file() or _load(path) != value:
            raise RuntimeError(f"A-S D1 materialization is missing or stale: {path}")
        return
    write_json_atomic(path, value)


def materialize(output_directory: Path, *, check: bool) -> dict[str, object]:
    output_directory = output_directory.resolve()
    parent, children = build_as_d1_production_materialization(
        ROOT,
        output_directory=output_directory,
    )
    parent_path = output_directory / "parent.json"
    expected_paths = {parent_path.resolve(), *(ROOT / relative for relative in children)}
    existing_paths = (
        {path.resolve() for path in output_directory.glob("*.json")}
        if output_directory.is_dir()
        else set()
    )
    unexpected_paths = existing_paths - expected_paths
    if unexpected_paths:
        rendered = ", ".join(str(path) for path in sorted(unexpected_paths))
        raise RuntimeError(f"A-S D1 materialization has unexpected JSON files: {rendered}")
    for relative, child in children.items():
        _write_or_check(ROOT / relative, child, check=check)
    _write_or_check(parent_path, parent, check=check)
    return {
        "status": parent["status"],
        "parent": parent_path.relative_to(ROOT).as_posix(),
        "campaign_child_count": parent["campaign_child_count"],
        "participant_cell_count": parent["participant_cell_count"],
        "complete_experiment_count": parent["complete_experiment_count"],
        "provider_call_count": 0,
        "provider_execution_authorized": False,
        "check": check,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = materialize(args.output_directory, check=bool(args.check))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
