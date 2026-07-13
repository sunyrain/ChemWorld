"""Audit the single v0.5 task/runtime/evaluation contract graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.contract_coherence import (
    audit_contract_coherence,
    load_contract_coherence_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/world_foundation/reports/contract-coherence-v0.5.json"),
    )
    args = parser.parse_args()
    report = audit_contract_coherence(load_contract_coherence_protocol())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "task_count": len(report["task_graph"]),
                "method_count": len(report["method_contract"]["formal_to_implementation"]),
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
