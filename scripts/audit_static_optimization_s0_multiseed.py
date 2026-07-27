"""Aggregate audited S0 runs across static world seeds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from uuid import uuid4

from chemworld.eval.static_optimization_multiseed import (
    aggregate_static_optimization_runs,
)


def _write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = aggregate_static_optimization_runs(args.run_root)
    _write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "seeds": report["seeds"],
                "experiments": report["completed_experiment_count"],
                "all_audits_passed": report["all_audits_passed"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
