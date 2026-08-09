#!/usr/bin/env python3
"""Create/check explicit user authorization for the Work II provider qualification triplet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_formal import build_formal_preflight, validate_formal_bindings
from chemworld.eval.work_ii_qualification import (
    build_qualification_execution_authorization,
    validate_qualification_execution_authorization,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-method-qualification-execution-authorization-v0.1.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--currency-ceiling-usd", type=float)
    parser.add_argument("--approved-at")
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError("formal binding validation failed: " + "; ".join(binding_errors))
    output = args.output.resolve()
    if args.check:
        if any(
            (
                args.currency_ceiling_usd is not None,
                args.approved_at is not None,
                args.provider_contract_confirmed_by_user,
                args.credential_rotation_confirmed_by_user,
            )
        ):
            raise RuntimeError("authorization creation options cannot be used with --check")
        if not output.is_file():
            raise RuntimeError("method-qualification execution authorization is missing")
        authorization = json.loads(output.read_text(encoding="utf-8"))
    else:
        missing = []
        if args.currency_ceiling_usd is None:
            missing.append("--currency-ceiling-usd")
        if not args.approved_at:
            missing.append("--approved-at")
        if not args.provider_contract_confirmed_by_user:
            missing.append("--provider-contract-confirmed-by-user")
        if not args.credential_rotation_confirmed_by_user:
            missing.append("--credential-rotation-confirmed-by-user")
        if missing:
            raise RuntimeError(
                "refusing provider authorization without explicit user inputs: "
                + ", ".join(missing)
            )
        authorization = build_qualification_execution_authorization(
            manifest,
            currency_ceiling_usd=float(args.currency_ceiling_usd),
            approved_at=str(args.approved_at),
        )
    errors = validate_qualification_execution_authorization(authorization, manifest)
    if errors:
        raise RuntimeError("invalid method-qualification authorization: " + "; ".join(errors))
    if not args.check:
        write_json_atomic(output, authorization)
    print(
        json.dumps(
            {
                "status": authorization["status"],
                "provider_execution_allowed": authorization["provider_execution_allowed"],
                "currency_ceiling_usd": authorization["user_authorization"][
                    "currency_ceiling_usd"
                ],
                "authorization_sha256": authorization["authorization_sha256"],
                "credentials_present": authorization["user_authorization"][
                    "credentials_present"
                ],
                "output": str(output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
