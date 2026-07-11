"""Audit the vNext cross-family method protocol and current implementations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.method_protocol import audit_method_protocol, load_method_protocol
from chemworld.eval.runner import AGENT_REGISTRY


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/method-protocol-vnext.json"),
    )
    args = parser.parse_args()
    report = audit_method_protocol(load_method_protocol(), agent_registry=AGENT_REGISTRY)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "formal_method_matrix_ready": report["formal_method_matrix_ready"],
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
