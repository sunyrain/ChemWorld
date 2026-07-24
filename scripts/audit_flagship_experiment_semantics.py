"""Generate the unified semantic audit for all flagship experiment components."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.eval.flagship_semantics_audit import (  # noqa: E402
    audit_flagship_experiment_semantics,
)
from chemworld.eval.mechanism_adaptation import (  # noqa: E402
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.provenance import write_json_atomic  # noqa: E402

DEFAULT_PROTOCOL = ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
DEFAULT_PLAN = ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "flagship-experiment-semantics-audit-rc23.json"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = load_mechanism_adaptation_protocol(args.protocol)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    graph_path = ROOT / plan["diagnostic_relation_graph"]["report"]
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    report = audit_flagship_experiment_semantics(protocol, plan, graph)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing flagship semantics audit: {args.output}")
        recorded = json.loads(args.output.read_text(encoding="utf-8"))
        if recorded != report:
            raise SystemExit("flagship experiment semantics audit is stale")
    else:
        write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "check_count": report["check_count"],
                "failure_count": report["failure_count"],
                "output": str(args.output.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
