#!/usr/bin/env python3
"""Build or check the zero-call Work II pre-run evidence graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_release import (
    build_prerun_evidence_graph,
    validate_prerun_evidence_graph,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-prerun-evidence-graph-v0.2.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifact-version", choices=("v0.1", "v0.2"), default="v0.2"
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    graph = build_prerun_evidence_graph(
        ROOT, artifact_version=args.artifact_version
    )
    errors = validate_prerun_evidence_graph(ROOT, graph)
    if errors:
        raise RuntimeError("Work II pre-run evidence graph failed: " + "; ".join(errors))
    output = args.output.resolve()
    if args.check:
        if not output.is_file():
            raise RuntimeError("committed Work II pre-run evidence graph is missing")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != graph:
            raise RuntimeError("committed Work II pre-run evidence graph is stale")
    else:
        write_json_atomic(output, graph)
    print(
        json.dumps(
            {
                "status": graph["status"],
                "formal_execution_allowed": graph["formal_execution_allowed"],
                "provider_calls_executed": graph["provider_calls_executed"],
                "node_count": graph["summary"]["node_count"],
                "edge_count": graph["summary"]["edge_count"],
                "graph_sha256": graph["graph_sha256"],
                "output": str(output),
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
