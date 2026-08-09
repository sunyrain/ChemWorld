#!/usr/bin/env python3
"""Build/check the Work II method-qualification report and authorization receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_formal import build_formal_preflight, validate_formal_bindings
from chemworld.eval.work_ii_qualification import (
    build_method_qualification_receipt,
    validate_method_qualification_receipt,
    validate_method_qualification_report,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_REPORT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-method-qualification-report-v0.3.json"
)
DEFAULT_RECEIPT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-method-qualification-receipt-v0.3.json"
)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--receipt-output", type=Path, default=DEFAULT_RECEIPT_OUTPUT)
    parser.add_argument("--observed-cost-usd", type=float)
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError("formal binding validation failed: " + "; ".join(binding_errors))
    report_output = args.report_output.resolve()
    receipt_output = args.receipt_output.resolve()
    if args.check:
        if any(
            value is not None
            for value in (
                args.source_report,
                args.observed_cost_usd,
                args.pricing_source,
                args.pricing_observed_at,
            )
        ):
            raise RuntimeError("receipt creation options cannot be used with --check")
        report = _load(report_output)
        receipt = _load(receipt_output)
        report_errors = validate_method_qualification_report(ROOT, report, manifest)
        cost = receipt.get("qualification_cost_accounting")
        cost = cost if isinstance(cost, dict) else {}
        receipt_errors = validate_method_qualification_receipt(
            ROOT,
            receipt,
            manifest,
            currency_ceiling_usd=float(receipt.get("approved_currency_ceiling_usd", 0.0)),
        )
        errors = [*report_errors, *receipt_errors]
        if errors:
            raise RuntimeError("committed qualification package is invalid: " + "; ".join(errors))
    else:
        missing = []
        if args.source_report is None:
            missing.append("--source-report")
        if args.observed_cost_usd is None:
            missing.append("--observed-cost-usd")
        if not args.pricing_source:
            missing.append("--pricing-source")
        if not args.pricing_observed_at:
            missing.append("--pricing-observed-at")
        if missing:
            raise RuntimeError("qualification receipt inputs are missing: " + ", ".join(missing))
        source_report = _load(args.source_report.resolve())
        source_errors = validate_method_qualification_report(ROOT, source_report, manifest)
        if source_errors:
            raise RuntimeError(
                "source qualification report is invalid: " + "; ".join(source_errors)
            )
        authorization_binding = source_report[
            "qualification_execution_authorization_binding"
        ]
        authorization = _load(ROOT / str(authorization_binding["path"]))
        approved_ceiling = float(
            authorization.get("user_authorization", {}).get("currency_ceiling_usd", 0.0)
        )
        if float(args.observed_cost_usd) < 0 or float(args.observed_cost_usd) > approved_ceiling:
            raise RuntimeError("observed qualification cost exceeds the user-approved ceiling")
        write_json_atomic(report_output, source_report)
        receipt = build_method_qualification_receipt(
            ROOT,
            report_output,
            manifest,
            observed_cost_usd=float(args.observed_cost_usd),
            pricing_source=str(args.pricing_source),
            pricing_observed_at=str(args.pricing_observed_at),
        )
        write_json_atomic(receipt_output, receipt)
        cost = receipt["qualification_cost_accounting"]
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "qualified_cell_count": receipt["qualified_cell_count"],
                "observed_cost_usd": cost["observed_cost_usd"],
                "approved_currency_ceiling_usd": receipt["approved_currency_ceiling_usd"],
                "receipt_sha256": receipt["receipt_sha256"],
                "report": str(report_output),
                "receipt": str(receipt_output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
