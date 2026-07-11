"""Audit vNext operational-risk and process-cost calibration evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.risk_cost_signal_audit import (
    DEFAULT_FORMAL_RESULTS_PATH,
    DEFAULT_RISK_COST_PROTOCOL_PATH,
    audit_risk_cost_signal,
    load_risk_cost_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_RISK_COST_PROTOCOL_PATH)
    parser.add_argument("--results", type=Path, default=DEFAULT_FORMAL_RESULTS_PATH)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/risk-cost-signal-controls.json"),
    )
    args = parser.parse_args()
    report = audit_risk_cost_signal(
        load_risk_cost_protocol(args.protocol),
        formal_results_path=args.results,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "formal_method_comparison_ready": report["formal_method_comparison_ready"],
                "measurement_policy_identifiable": report["measurement_policy_identifiable"],
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
