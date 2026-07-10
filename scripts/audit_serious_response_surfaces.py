"""Generate deterministic serious-task response ranges and approximate upper bounds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.response_surface import audit_serious_response_surfaces


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples-per-seed", type=int, default=12)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/benchmark_freeze/response_surface_audit.json"),
    )
    args = parser.parse_args()
    report = audit_serious_response_surfaces(samples_per_seed=args.samples_per_seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), **report}, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
