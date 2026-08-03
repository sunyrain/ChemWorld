"""Audit an immutable Work I known-policy matrix without executing worlds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.policy_validity_audit import audit_policy_validity_manifest


def _json_text(payload: dict[str, Any]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read and audit a source-bound known-policy matrix. This command never "
            "executes a chemical world or retunes the frozen threshold."
        )
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit path for the deterministic audit receipt.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare the deterministic receipt with --output without writing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check and args.output is None:
        raise SystemExit("--check requires --output")
    report = audit_policy_validity_manifest(args.manifest)
    report_text = _json_text(report)
    if args.check:
        if args.output.read_text(encoding="utf-8") != report_text:
            raise SystemExit("policy-validity audit receipt does not match rebuild")
    elif args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report_text, encoding="utf-8", newline="\n")
    else:
        print(report_text, end="")
    if args.output is not None:
        print(
            json.dumps(
                {
                    "audit_sha256": report["audit_sha256"],
                    "campaigns": report["counts"]["campaigns"],
                    "closed_lifecycles": report["counts"]["closed_lifecycles"],
                    "passed": report["passed"],
                    "status": report["status"],
                },
                sort_keys=True,
            )
        )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
