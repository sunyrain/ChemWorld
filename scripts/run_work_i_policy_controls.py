"""Preflight or execute the Work I known-policy control matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.policy_validity_matrix import (
    build_preflight,
    known_policy_cell_executor,
    load_formal_qualification_receipt,
    run_matrix,
    validate_preflight,
)
from chemworld.eval.provenance import write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_i_policy_control_matrix_v0.1.json"
DEFAULT_PREFLIGHT = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-policy-control-matrix-runner-preflight-v0.1.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--preflight",
        action="store_true",
        help="Build the outcome-blind schedule/source preflight only.",
    )
    mode.add_argument(
        "--execute",
        action="store_true",
        help="Execute the formal matrix through the merged V04 controllers.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--allow-formal-execution",
        action="store_true",
        help="Required explicit opt-in for --execute.",
    )
    parser.add_argument(
        "--qualification-receipt",
        type=Path,
        help="Required self-hashed W1-V07 runner-qualification/protocol-freeze receipt.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Rebuild and compare the committed preflight without writing.",
    )
    return parser.parse_args()


def _run_preflight(args: argparse.Namespace) -> int:
    if (
        args.resume
        or args.allow_formal_execution
        or args.output_root is not None
        or args.qualification_receipt is not None
    ):
        raise RuntimeError(
            "--resume, --allow-formal-execution, --qualification-receipt, and "
            "--output-root apply only to --execute"
        )
    report = build_preflight(ROOT, args.config.resolve())
    errors = validate_preflight(report)
    if errors:
        raise RuntimeError("preflight validation failed: " + "; ".join(errors))
    output = args.output.resolve()
    if args.check:
        if not output.is_file():
            raise RuntimeError(f"missing committed preflight: {output}")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != report:
            raise RuntimeError("committed preflight differs from deterministic rebuild")
    else:
        write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "formal_result": report["formal_result"],
                "controller_status": report["dependency_bindings"]["controller"][
                    "status"
                ],
                "scheduled_campaigns": report["expected_counts"][
                    "primary_campaigns"
                ],
                "scheduled_lifecycles": report["expected_counts"][
                    "primary_closed_lifecycles"
                ],
                "preflight_sha256": report["preflight_sha256"],
                "output": str(output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_formal(args: argparse.Namespace) -> int:
    if args.check or args.output != DEFAULT_PREFLIGHT:
        raise RuntimeError("--check and --output apply only to --preflight")
    if args.output_root is None:
        raise RuntimeError("--execute requires an explicit --output-root")
    if not args.allow_formal_execution:
        raise RuntimeError("--execute requires --allow-formal-execution")
    if args.qualification_receipt is None:
        raise RuntimeError("--execute requires --qualification-receipt from W1-V07")
    receipt = load_formal_qualification_receipt(args.qualification_receipt.resolve())
    manifest = run_matrix(
        root=ROOT,
        protocol_path=args.config.resolve(),
        output_root=args.output_root.resolve(),
        executor=known_policy_cell_executor,
        resume=bool(args.resume),
        execution_mode="formal",
        allow_formal_execution=True,
        formal_qualification_receipt=receipt,
    )
    print(
        json.dumps(
            {
                "status": manifest["status"],
                "manifest_sha256": manifest["manifest_sha256"],
                "primary_campaigns": manifest["materialized_counts"][
                    "primary_campaigns"
                ],
                "primary_closed_lifecycles": manifest["materialized_counts"][
                    "primary_closed_lifecycles"
                ],
                "output_root": str(args.output_root.resolve()),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    args = parse_args()
    if args.preflight:
        return _run_preflight(args)
    return _run_formal(args)


if __name__ == "__main__":
    raise SystemExit(main())
