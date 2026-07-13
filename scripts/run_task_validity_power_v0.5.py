"""Run v0.5 task-validity, calibration, behavior, and power controls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.task_validity_power_v0_5 import (
    load_task_validity_power_protocol,
    run_task_validity_power,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/world_foundation/reports/task-validity-power-v0.5.json"),
    )
    args = parser.parse_args()
    report = run_task_validity_power(load_task_validity_power_protocol())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "core_task_count": len(report["core_tasks"]),
                "formal_design_recommendation": report["formal_design_recommendation"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
