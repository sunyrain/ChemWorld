#!/usr/bin/env python3
"""Run the frozen first-paper deterministic use-case qualification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.deterministic_use_cases import (
    build_report,
    write_outputs,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help="JSON report path (defaults to the frozen formal result path)",
    )
    parser.add_argument(
        "--output-markdown",
        type=Path,
        default=None,
        help="Markdown summary path (defaults to OUTPUT_JSON with a .md suffix)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_json = args.output_json.resolve()
    output_markdown = (
        args.output_markdown.resolve()
        if args.output_markdown is not None
        else output_json.with_suffix(".md")
    )
    if output_json == output_markdown:
        raise SystemExit("JSON and Markdown outputs must use distinct paths")
    occupied = [path for path in (output_json, output_markdown) if path.exists()]
    if occupied:
        rendered = ", ".join(str(path) for path in occupied)
        raise SystemExit(
            "deterministic use-case output already exists; refusing to overwrite: "
            f"{rendered}"
        )

    report = build_report(repository_root=ROOT, require_clean=True)
    report_file, markdown_file = write_outputs(
        report,
        output_path=output_json,
        markdown_path=output_markdown,
        allow_existing=False,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "provider_call_count": report["provider_call_count"],
                "report": str(report_file),
                "markdown": str(markdown_file),
            },
            sort_keys=True,
        )
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
