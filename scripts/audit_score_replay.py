"""Audit vNext score provenance, replay, and tamper controls."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from chemworld.eval.score_replay_audit import (
    audit_score_replay_protocol,
    load_score_replay_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/score-replay-controls.json"),
    )
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="chemworld-score-replay-") as temporary:
        report = audit_score_replay_protocol(
            load_score_replay_protocol(),
            workspace=temporary,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "publication_ready": report["publication_ready"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
