"""Validate a serious baseline report and write a colocated evidence artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.benchmark_validation import (
    write_validation_artifact,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.baseline_report.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("baseline report must be a JSON object")
    output = args.output or args.baseline_report.with_name("benchmark_validation.json")
    artifact = write_validation_artifact(report, output)
    print(json.dumps({"output": str(output), **artifact}, indent=2, sort_keys=True))
    return 0 if artifact["validated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
