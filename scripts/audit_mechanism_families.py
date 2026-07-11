"""Build the vNext mechanism-family control report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.mechanism_family_audit import (
    DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH,
    audit_mechanism_families,
    load_mechanism_family_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/mechanism-family-controls.json"),
    )
    args = parser.parse_args()
    report = audit_mechanism_families(load_mechanism_family_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": report["status"],
                "controls_ready": report["controls_ready"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
