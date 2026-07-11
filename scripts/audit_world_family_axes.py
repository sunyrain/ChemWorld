"""Build the executable vNext world-family control audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.world_family_audit import (
    DEFAULT_WORLD_FAMILY_PROTOCOL_PATH,
    audit_world_family_controls,
    load_world_family_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=DEFAULT_WORLD_FAMILY_PROTOCOL_PATH,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/world-family-axis-controls.json"),
    )
    parser.add_argument(
        "--skip-response-probes",
        action="store_true",
        help="Validate declarations only; the resulting controls gate remains false.",
    )
    args = parser.parse_args()
    report = audit_world_family_controls(
        load_world_family_protocol(args.protocol),
        run_response_probes=not args.skip_response_probes,
    )
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
                "benchmark_claim_allowed": report["benchmark_claim_allowed"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
