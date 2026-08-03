"""Build or byte-check the read-only Work I known-policy validity report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.policy_validity_report import (
    PolicyValidityReportError,
    build_delivery_manifest,
    build_policy_validity_report,
    render_policy_validity_markdown,
    rendered_json_text,
)

DEFAULT_ANALYZERS = {
    "v09_reporter_source": Path("src/chemworld/eval/policy_validity_report.py"),
    "v09_reporter_cli": Path("scripts/report_work_i_policy_control_validity.py"),
    "v06_auditor_source": Path("src/chemworld/eval/policy_validity_audit.py"),
    "provenance_helper_source": Path("src/chemworld/eval/provenance.py"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read immutable V08 evidence and report bounded known-policy validity. "
            "This command never executes a world, controller, provider, or formal cell."
        )
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--v08-claim", type=Path, required=True)
    parser.add_argument("--v08-done-commit", required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--delivery-manifest-output", type=Path, required=True)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Byte-check all three outputs without writing.",
    )
    return parser.parse_args()


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _check_text(path: Path, expected: str) -> None:
    try:
        observed = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolicyValidityReportError(f"missing output for --check: {path}") from exc
    if observed != expected:
        raise PolicyValidityReportError(f"output does not match deterministic rebuild: {path}")


def main() -> int:
    args = parse_args()
    report = build_policy_validity_report(
        args.manifest,
        args.audit,
        v08_claim_path=args.v08_claim,
        v08_done_commit=args.v08_done_commit,
        analyzer_source_paths=DEFAULT_ANALYZERS,
    )
    markdown = render_policy_validity_markdown(report)
    delivery = build_delivery_manifest(
        report=report,
        markdown=markdown,
        report_path=args.json_output,
        markdown_path=args.markdown_output,
        matrix_manifest_path=args.manifest,
        formal_audit_path=args.audit,
        v08_claim_path=args.v08_claim,
        analyzer_source_paths=DEFAULT_ANALYZERS,
    )
    outputs = {
        args.json_output: rendered_json_text(report),
        args.markdown_output: markdown,
        args.delivery_manifest_output: rendered_json_text(delivery),
    }
    for path, text in outputs.items():
        if args.check:
            _check_text(path, text)
        else:
            _write_text_atomic(path, text)
    print(
        json.dumps(
            {
                "delivery_manifest_sha256": delivery["delivery_manifest_sha256"],
                "primary_campaigns": report["estimand"]["primary_campaigns"],
                "primary_closed_lifecycles": report["estimand"]["primary_closed_lifecycles"],
                "report_sha256": report["report_sha256"],
                "status": report["status"],
            },
            sort_keys=True,
        )
    )
    return 0 if report["scientific_status"]["established"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
