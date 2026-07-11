"""Audit an independent reference portfolio plan and optional evidence manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.reference_portfolio import (
    DEFAULT_REFERENCE_PORTFOLIO_PLAN_PATH,
    audit_reference_portfolio,
    freeze_reference_estimates,
    load_reference_portfolio_plan,
)
from chemworld.eval.reference_regret import load_reference_regret_protocol


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_REFERENCE_PORTFOLIO_PLAN_PATH)
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/reference-portfolio-controls.json"),
    )
    parser.add_argument("--candidate-reference-output", type=Path)
    args = parser.parse_args()

    plan = load_reference_portfolio_plan(args.plan)
    protocol = load_reference_regret_protocol()
    evidence = (
        json.loads(args.evidence_manifest.read_text(encoding="utf-8"))
        if args.evidence_manifest is not None
        else None
    )
    report = audit_reference_portfolio(
        plan,
        reference_protocol=protocol,
        evidence_manifest=evidence,
        workspace_root=args.workspace_root,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.candidate_reference_output is not None:
        if evidence is None:
            raise SystemExit("--candidate-reference-output requires --evidence-manifest")
        estimates = freeze_reference_estimates(
            plan,
            protocol,
            evidence,
            workspace_root=args.workspace_root,
        )
        args.candidate_reference_output.parent.mkdir(parents=True, exist_ok=True)
        args.candidate_reference_output.write_text(
            json.dumps(estimates, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "evidence_complete": report["evidence_complete"],
                "formal_results_present": report["formal_results_present"],
                "output": str(args.output),
                "planned_source_run_count": report["planned_source_run_count"],
                "status": report["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
