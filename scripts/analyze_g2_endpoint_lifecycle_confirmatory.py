"""Audit and analyze a completed prospective G2 endpoint-lifecycle matrix."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from chemworld.eval.endpoint_lifecycle_confirmatory import (
    write_endpoint_lifecycle_confirmatory_audit,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = write_endpoint_lifecycle_confirmatory_audit(
        args.manifest.resolve(),
        args.output.resolve(),
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "confirmatory_claim_allowed": report["confirmatory_claim_allowed"],
                "coverage_gate": report["coverage_gate"],
                "primary_analysis": report["primary_analysis"],
                "audit_sha256": report["audit_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
