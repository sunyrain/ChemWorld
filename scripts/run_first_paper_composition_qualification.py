"""Run the frozen first-paper composition qualification once."""

from __future__ import annotations

import argparse
from pathlib import Path

from chemworld.eval.composition_qualification import build_report, write_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1.json",
    )
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--allow-existing-output", action="store_true")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    markdown = output.with_suffix(".md")
    if not args.allow_existing_output and (output.exists() or markdown.exists()):
        raise SystemExit(
            "qualification output already exists; refusing to replace a completed result"
        )
    report = build_report(repository_root=args.repository_root, require_clean=True)
    write_outputs(report, output_path=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
