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
from chemworld.eval.work_ii_resource_calibration import (
    build_resource_calibration_readiness,
    validate_resource_calibration_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.2.json"
CALIBRATION_MANIFEST = (
    ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-method-qualification-execution-authorization-v0.1.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resource-calibration-summary", type=Path, required=True)
    parser.add_argument("--currency-ceiling-usd", type=float)
    parser.add_argument("--approved-at")
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--cache-hit-input-usd-per-million", type=float)
    parser.add_argument("--cache-miss-input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError("formal binding validation failed: " + "; ".join(binding_errors))
    calibration = build_resource_calibration_readiness(
        ROOT,
        CALIBRATION_MANIFEST,
        summary_path=args.resource_calibration_summary,
    )
    calibration_errors = validate_resource_calibration_readiness(calibration)
    if calibration_errors:
        raise RuntimeError(
            "W2-26 resource-calibration readiness failed: "
            + "; ".join(calibration_errors)
        )
    if calibration.get("method_qualification_may_be_authorized") is not True:
        missing = ",".join(
            str(item) for item in calibration.get("missing_pattern_rounds", [])
        )
        raise RuntimeError(
            "method qualification authorization is blocked until W2-26 passes; "
            f"unresolved pattern rounds: {missing}"
        )
    output = args.output.resolve()
    if args.check:
        if any(
            (
                args.currency_ceiling_usd is not None,
                args.approved_at is not None,
                args.pricing_source is not None,
                args.pricing_observed_at is not None,
                args.cache_hit_input_usd_per_million is not None,
                args.cache_miss_input_usd_per_million is not None,
                args.output_usd_per_million is not None,
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
        for value, flag in (
            (args.pricing_source, "--pricing-source"),
            (args.pricing_observed_at, "--pricing-observed-at"),
            (
                args.cache_hit_input_usd_per_million,
                "--cache-hit-input-usd-per-million",
            ),
            (
                args.cache_miss_input_usd_per_million,
                "--cache-miss-input-usd-per-million",
            ),
            (args.output_usd_per_million, "--output-usd-per-million"),
        ):
            if value is None:
                missing.append(flag)
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
            ROOT,
            manifest,
            currency_ceiling_usd=float(args.currency_ceiling_usd),
            approved_at=str(args.approved_at),
            pricing_source=str(args.pricing_source),
            pricing_observed_at=str(args.pricing_observed_at),
            cache_hit_input_usd_per_million=float(
                args.cache_hit_input_usd_per_million
            ),
            cache_miss_input_usd_per_million=float(
                args.cache_miss_input_usd_per_million
            ),
            output_usd_per_million=float(args.output_usd_per_million),
        )
    errors = validate_qualification_execution_authorization(ROOT, authorization, manifest)
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
                "all_attempt_cost_cap_usd": authorization[
                    "qualification_currency_budget"
                ]["all_infrastructure_resumes"]["cost_cap_usd"],
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
