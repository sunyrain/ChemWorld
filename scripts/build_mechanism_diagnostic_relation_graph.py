"""Materialize the versioned v0.3 diagnostic-relation graph."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.eval.mechanism_adaptation import (  # noqa: E402
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_relation_graph import (  # noqa: E402
    build_diagnostic_relation_graph,
)
from chemworld.eval.provenance import write_json_atomic  # noqa: E402

DEFAULT_PROTOCOL = ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc23.json"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = load_mechanism_adaptation_protocol(args.protocol)
    graph = build_diagnostic_relation_graph(protocol)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing diagnostic relation graph: {args.output}")
        recorded = json.loads(args.output.read_text(encoding="utf-8"))
        if recorded != graph:
            raise SystemExit("diagnostic relation graph is stale")
    else:
        write_json_atomic(args.output, graph)
    print(
        json.dumps(
            {
                "status": "passed",
                "graph_sha256": graph["graph_sha256"],
                "relation_count": graph["relation_count"],
                "output": str(args.output.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
