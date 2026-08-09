#!/usr/bin/env python3
"""Build/check the final user-authorized Work II preregistration freeze receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_formal import build_formal_preflight, validate_formal_bindings
from chemworld.eval.work_ii_release import (
    build_preregistration_freeze_receipt,
    validate_preregistration_freeze_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
ROUTE = ROOT / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-preregistration-freeze-receipt-v0.1.json"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _route_compliance(args: argparse.Namespace, selected: object) -> dict[str, object]:
    if selected == "nature_registered_report_stage_1":
        if not (
            args.nature_stage_1_ipa_confirmed
            and args.nature_protocol_registered
            and args.registration_reference
        ):
            raise RuntimeError(
                "Nature route requires IPA, registered protocol and registration reference"
            )
        return {
            "stage_1_in_principle_acceptance": True,
            "approved_protocol_registered": True,
            "registration_reference": args.registration_reference,
        }
    if selected == "regular_submission":
        if not args.regular_target or not args.regular_evidence_threshold:
            raise RuntimeError(
                "regular route requires a frozen target and evidence threshold"
            )
        return {
            "target_and_evidence_threshold_frozen": True,
            "target": args.regular_target,
            "evidence_threshold": args.regular_evidence_threshold,
        }
    raise RuntimeError("submission route has not been selected by the user")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualification-receipt", type=Path)
    parser.add_argument("--formal-currency-ceiling-usd", type=float)
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--cache-hit-input-usd-per-million", type=float)
    parser.add_argument("--cache-miss-input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--qualified-eta-seconds", type=float)
    parser.add_argument("--authorized-at")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument("--execution-command-approved-by-user", action="store_true")
    parser.add_argument("--budget-approved-by-user", action="store_true")
    parser.add_argument("--failure-escalation-approved-by-user", action="store_true")
    parser.add_argument("--nature-stage-1-ipa-confirmed", action="store_true")
    parser.add_argument("--nature-protocol-registered", action="store_true")
    parser.add_argument("--registration-reference")
    parser.add_argument("--regular-target")
    parser.add_argument("--regular-evidence-threshold")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError("formal binding validation failed: " + "; ".join(binding_errors))
    output = args.output.resolve()
    if args.check:
        creation_values = (
            args.qualification_receipt,
            args.formal_currency_ceiling_usd,
            args.pricing_source,
            args.pricing_observed_at,
            args.cache_hit_input_usd_per_million,
            args.cache_miss_input_usd_per_million,
            args.output_usd_per_million,
            args.qualified_eta_seconds,
            args.authorized_at,
            args.registration_reference,
            args.regular_target,
            args.regular_evidence_threshold,
        )
        creation_flags = (
            args.credential_rotation_confirmed_by_user,
            args.execution_command_approved_by_user,
            args.budget_approved_by_user,
            args.failure_escalation_approved_by_user,
            args.nature_stage_1_ipa_confirmed,
            args.nature_protocol_registered,
        )
        if any(value is not None for value in creation_values) or any(creation_flags):
            raise RuntimeError("freeze-receipt creation options cannot be used with --check")
        receipt = _load(output)
        qualification_binding = receipt.get("bindings", {}).get("method_qualification", {})
        qualification_path = ROOT / str(qualification_binding.get("path", ""))
        qualification = _load(qualification_path)
        ceiling = float(
            receipt.get("user_authorization", {}).get(
                "formal_currency_ceiling_usd", 0.0
            )
        )
        errors = validate_preregistration_freeze_receipt(
            ROOT,
            receipt,
            manifest,
            qualification,
            qualification_path,
            currency_ceiling_usd=ceiling,
        )
        if errors:
            raise RuntimeError("committed preregistration freeze is invalid: " + "; ".join(errors))
    else:
        missing = []
        for value, flag in (
            (args.qualification_receipt, "--qualification-receipt"),
            (args.formal_currency_ceiling_usd, "--formal-currency-ceiling-usd"),
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
            (args.qualified_eta_seconds, "--qualified-eta-seconds"),
            (args.authorized_at, "--authorized-at"),
        ):
            if value is None:
                missing.append(flag)
        for confirmed, flag in (
            (
                args.credential_rotation_confirmed_by_user,
                "--credential-rotation-confirmed-by-user",
            ),
            (
                args.execution_command_approved_by_user,
                "--execution-command-approved-by-user",
            ),
            (args.budget_approved_by_user, "--budget-approved-by-user"),
            (
                args.failure_escalation_approved_by_user,
                "--failure-escalation-approved-by-user",
            ),
        ):
            if not confirmed:
                missing.append(flag)
        if missing:
            raise RuntimeError("final freeze user inputs are missing: " + ", ".join(missing))
        selected_route = _load(ROUTE).get("selected_option")
        compliance = _route_compliance(args, selected_route)
        receipt = build_preregistration_freeze_receipt(
            ROOT,
            manifest,
            args.qualification_receipt.resolve(),
            currency_ceiling_usd=float(args.formal_currency_ceiling_usd),
            qualified_expected_eta_seconds=float(args.qualified_eta_seconds),
            authorized_at=str(args.authorized_at),
            route_compliance=compliance,
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
        write_json_atomic(output, receipt)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "selected_submission_route": receipt["selected_submission_route"],
                "formal_execution_authorized": receipt["formal_execution_authorized"],
                "formal_currency_ceiling_usd": receipt["user_authorization"][
                    "formal_currency_ceiling_usd"
                ],
                "formal_all_attempt_cost_cap_usd": receipt["formal_currency_budget"][
                    "all_infrastructure_resumes"
                ]["cost_cap_usd"],
                "receipt_sha256": receipt["receipt_sha256"],
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
