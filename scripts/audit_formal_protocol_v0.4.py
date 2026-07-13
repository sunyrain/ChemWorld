"""Initialize or audit the sealed ChemWorld formal protocol 0.4 cohort."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.formal_protocol_v0_4 import (
    DEFAULT_PRIVATE_MANIFEST_PATH,
    audit_formal_protocol,
    initialize_private_bench_manifest,
    load_formal_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path("configs/benchmark/formal_protocol_v0.4.json"),
    )
    parser.add_argument(
        "--private-manifest",
        type=Path,
        default=DEFAULT_PRIVATE_MANIFEST_PATH,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/formal-protocol-v0.4.json"),
    )
    parser.add_argument(
        "--initialize-private-manifest",
        action="store_true",
        help="Create the private cohort once; only its commitment is printed.",
    )
    args = parser.parse_args()
    protocol = load_formal_protocol(args.protocol)
    if args.initialize_private_manifest:
        summary = initialize_private_bench_manifest(
            protocol,
            path=args.private_manifest,
        )
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    report = audit_formal_protocol(
        protocol,
        private_manifest_path=args.private_manifest,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "formal_core_task_count": len(report["formal_core_tasks"]),
                "paired_bench_seed_count": report["private_bench"]["paired_seed_count"],
                "private_commitment_verified": report["private_bench"]["verified"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
