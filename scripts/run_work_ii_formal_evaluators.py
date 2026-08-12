#!/usr/bin/env python3
"""Run the provider-free public truth and blind Work II evaluators."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.work_ii_formal_evaluators import execute_formal_evaluators

ROOT = Path(__file__).resolve().parents[1]


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _progress_writer(path: Path | None):
    def emit(payload: Mapping[str, Any]) -> None:
        rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        print(rendered, flush=True)

    return emit


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Execute immutable public truth packs per task/world cluster and blind "
            "replay packs per completed formal participant session."
        )
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--execution-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Validate and reuse qualified units, then execute only missing units.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    manifest = _load_object(args.manifest.resolve())
    summary = execute_formal_evaluators(
        ROOT,
        manifest,
        args.execution_root,
        args.output_root,
        resume=bool(args.resume),
        progress=_progress_writer(
            args.progress_file.resolve() if args.progress_file is not None else None
        ),
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
