"""Build six vNext task-validity cards and a provisional suite recommendation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.task_validity import (
    DEFAULT_TASK_VALIDITY_PROTOCOL_PATH,
    audit_task_validity,
    load_task_validity_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_TASK_VALIDITY_PROTOCOL_PATH)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/task-validity-vnext.json"),
    )
    args = parser.parse_args()
    report = audit_task_validity(load_task_validity_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "decision": report["suite_recommendation"]["decision"],
                "output": str(args.output),
                "status": report["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
