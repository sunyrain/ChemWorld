"""Build the candidate reference-regret control report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.reference_regret import (
    DEFAULT_REFERENCE_REGRET_PROTOCOL_PATH,
    audit_reference_regret_protocol,
    load_reference_regret_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=DEFAULT_REFERENCE_REGRET_PROTOCOL_PATH,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/reference-regret-controls.json"),
    )
    args = parser.parse_args()
    report = audit_reference_regret_protocol(load_reference_regret_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "formal_results_present": report["formal_results_present"],
                "output": str(args.output),
                "parent_task_complete": report["parent_task_complete"],
                "probe_count": report["probe_count"],
                "status": report["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
