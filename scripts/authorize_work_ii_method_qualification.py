#!/usr/bin/env python3
"""Create/check explicit user authorization for the Work II provider qualification triplet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_method_qualification_local import (
    build_method_qualification_local_manifest,
    build_w2_27_runtime_config,
    validate_method_qualification_local_manifest,
)
from chemworld.eval.work_ii_qualification import (
    build_qualification_execution_authorization,
    validate_qualification_execution_authorization,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-method-qualification-execution-authorization-v0.1.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resource-calibration-summary", type=Path, required=True)
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--currency-ceiling-usd", type=float)
    parser.add_argument("--approved-at")
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--cache-hit-input-usd-per-million", type=float)
    parser.add_argument("--cache-miss-input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--unlimited-spend-authorized", action="store_true")
    parser.add_argument("--pricing-unavailable-reason")
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    runtime_config_path = args.runtime_config.resolve()
    try:
        runtime_config_path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError("W2-27 runtime config must remain inside the repository") from error
    expected_runtime_config = build_w2_27_runtime_config(
        ROOT,
        DESIGN,
        args.resource_calibration_summary.resolve(),
    )
    if runtime_config_path.is_file():
        observed_runtime_config = json.loads(
            runtime_config_path.read_text(encoding="utf-8")
        )
        if observed_runtime_config != expected_runtime_config:
            raise RuntimeError("existing W2-27 runtime config differs from the W2-26 card")
    elif args.check:
        raise RuntimeError("W2-27 runtime config is missing")
    else:
        write_json_atomic(runtime_config_path, expected_runtime_config)
    manifest = build_method_qualification_local_manifest(
        ROOT, DESIGN, runtime_config_path
    )
    manifest_errors = validate_method_qualification_local_manifest(ROOT, manifest)
    if manifest_errors:
        raise RuntimeError(
            "method-qualification local manifest failed: "
            + "; ".join(manifest_errors)
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
                args.unlimited_spend_authorized,
                args.pricing_unavailable_reason is not None,
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
        if not args.approved_at:
            missing.append("--approved-at")
        common_metadata = (
            (args.pricing_source, "--pricing-source"),
            (args.pricing_observed_at, "--pricing-observed-at"),
        )
        finite_pricing = (
            (args.currency_ceiling_usd, "--currency-ceiling-usd"),
            (
                args.cache_hit_input_usd_per_million,
                "--cache-hit-input-usd-per-million",
            ),
            (
                args.cache_miss_input_usd_per_million,
                "--cache-miss-input-usd-per-million",
            ),
            (args.output_usd_per_million, "--output-usd-per-million"),
        )
        for value, flag in common_metadata:
            if value is None:
                missing.append(flag)
        if args.unlimited_spend_authorized:
            if any(value is not None for value, _flag in finite_pricing):
                raise RuntimeError(
                    "unlimited provider authorization cannot declare USD pricing or a ceiling"
                )
            if not args.pricing_unavailable_reason:
                missing.append("--pricing-unavailable-reason")
        else:
            if args.pricing_unavailable_reason is not None:
                raise RuntimeError(
                    "--pricing-unavailable-reason requires --unlimited-spend-authorized"
                )
            for value, flag in finite_pricing:
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
            currency_ceiling_usd=(
                None
                if args.currency_ceiling_usd is None
                else float(args.currency_ceiling_usd)
            ),
            approved_at=str(args.approved_at),
            pricing_source=str(args.pricing_source),
            pricing_observed_at=str(args.pricing_observed_at),
            cache_hit_input_usd_per_million=(
                None
                if args.cache_hit_input_usd_per_million is None
                else float(args.cache_hit_input_usd_per_million)
            ),
            cache_miss_input_usd_per_million=(
                None
                if args.cache_miss_input_usd_per_million is None
                else float(args.cache_miss_input_usd_per_million)
            ),
            output_usd_per_million=(
                None
                if args.output_usd_per_million is None
                else float(args.output_usd_per_million)
            ),
            unlimited_spend_authorized=bool(args.unlimited_spend_authorized),
            pricing_unavailable_reason=args.pricing_unavailable_reason,
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
                "unlimited_spend_authorized": authorization[
                    "user_authorization"
                ]["unlimited_spend_authorized"],
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
