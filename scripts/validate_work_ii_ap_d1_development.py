#!/usr/bin/env python3
"""Validate A-P independent D1 execution configs and optional user authorization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_ap_d1_development import (
    DEFAULT_AP_D1_READINESS,
    validate_ap_d1_development_authorization,
    validate_ap_d1_development_config,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--readiness", type=Path, default=ROOT / DEFAULT_AP_D1_READINESS
    )
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()

    if (args.authorization is None) != (args.output_root is None):
        raise ValueError("authorization and output-root must be supplied together")
    if args.authorization is None:
        errors = validate_ap_d1_development_config(
            ROOT,
            args.config.resolve(),
            readiness_path=args.readiness.resolve(),
        )
        status = "config_ready_authorization_blocked" if not errors else "blocked"
    else:
        _, errors = validate_ap_d1_development_authorization(
            ROOT,
            args.authorization.resolve(),
            config_path=args.config.resolve(),
            output_root=args.output_root.resolve(),
            readiness_path=args.readiness.resolve(),
        )
        status = "authorized" if not errors else "blocked"
    print(
        json.dumps(
            {
                "status": status,
                "provider_calls_executed": 0,
                "errors": errors,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
