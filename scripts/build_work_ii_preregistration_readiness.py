#!/usr/bin/env python3
"""Build the zero-call Work II route and preregistration readiness package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_preregistration import (
    build_preregistration_readiness,
    render_preregistration_draft,
    validate_preregistration_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROUTE = ROOT / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_PREFLIGHT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json"
)
DEFAULT_QUALIFICATION = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-method-qualification-readiness-v0.1.json"
)
DEFAULT_POWER_AUDIT = ROOT / "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"
DEFAULT_DESIGN_AUDIT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-world-prior-design-audit.json"
)
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-preregistration-readiness-v0.1.json"
)
DEFAULT_DRAFT = ROOT / "workstreams/flagship_tasks/reports/work-ii-preregistration-draft-v0.1.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", type=Path, default=DEFAULT_ROUTE)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--analysis", type=Path, default=DEFAULT_ANALYSIS)
    parser.add_argument("--formal-preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--qualification-readiness", type=Path, default=DEFAULT_QUALIFICATION)
    parser.add_argument("--power-audit", type=Path, default=DEFAULT_POWER_AUDIT)
    parser.add_argument("--design-audit", type=Path, default=DEFAULT_DESIGN_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--draft", type=Path, default=DEFAULT_DRAFT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    report = build_preregistration_readiness(
        ROOT,
        route_path=args.route.resolve(),
        design_path=args.design.resolve(),
        analysis_path=args.analysis.resolve(),
        formal_preflight_path=args.formal_preflight.resolve(),
        qualification_readiness_path=args.qualification_readiness.resolve(),
        power_audit_path=args.power_audit.resolve(),
        design_audit_path=args.design_audit.resolve(),
    )
    errors = validate_preregistration_readiness(report)
    if errors:
        raise RuntimeError("Work II preregistration readiness failed: " + "; ".join(errors))
    rendered = render_preregistration_draft(report)
    output = args.output.resolve()
    draft = args.draft.resolve()
    if args.check:
        if not output.is_file() or not draft.is_file():
            raise RuntimeError("committed preregistration readiness package is incomplete")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != report:
            raise RuntimeError("committed preregistration readiness manifest is stale")
        if draft.read_text(encoding="utf-8") != rendered:
            raise RuntimeError("committed preregistration draft differs from its manifest")
    else:
        write_json_atomic(output, report)
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_text(rendered, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": report["status"],
                "route_status": report["route_decision"]["status"],
                "recommended_route": report["route_decision"]["recommended_option"],
                "formal_execution_allowed": report["formal_execution_allowed"],
                "provider_calls_executed": report["provider_calls_executed"],
                "blocker_count": len(report["unresolved_requirement_ids"]),
                "readiness_sha256": report["readiness_sha256"],
                "output": str(output),
                "draft": str(draft),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
