"""Audit the preregistered vNext task, effect, seed, and world freeze."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.confirmatory_freeze import (
    audit_confirmatory_freeze,
    load_confirmatory_freeze,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/confirmatory-freeze-controls.json"),
    )
    args = parser.parse_args()
    report = audit_confirmatory_freeze(load_confirmatory_freeze())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "protocol_frozen": report["protocol_frozen"],
                "confirmatory_rerun_ready": report["confirmatory_rerun_ready"],
                "missing_required_methods": report["missing_required_methods"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
