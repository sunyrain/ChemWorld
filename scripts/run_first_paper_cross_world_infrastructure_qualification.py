#!/usr/bin/env python3
"""Run the frozen first-paper cross-world infrastructure qualification."""

from __future__ import annotations

import argparse
from pathlib import Path

from chemworld.eval.cross_world_infrastructure_qualification import (
    build_report,
    load_protocol,
    write_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    protocol_path = args.protocol.resolve()
    output_path = args.output.resolve()
    protocol = load_protocol(protocol_path)
    report = build_report(protocol, repository_root=root)
    report_file, markdown_file, manifest_file = write_outputs(
        report,
        protocol_path=protocol_path,
        output_path=output_path,
        repository_root=root,
    )
    print(f"status={report['status']}")
    print(f"report={report_file.relative_to(root)}")
    print(f"markdown={markdown_file.relative_to(root)}")
    print(f"manifest={manifest_file.relative_to(root)}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
