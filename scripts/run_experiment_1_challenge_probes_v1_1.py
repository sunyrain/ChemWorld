#!/usr/bin/env python3
"""Run frozen Experiment 1 executable sequential challenge probes v1.2."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_challenge_v1_1 import build_probe_summary
from chemworld.eval.provenance import git_source_commit, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def render_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Experiment 1 executable challenge probe result v1.2",
        "",
        "Status: **challenge development attempt 3; not confirmation**",
        "",
        "| Block | Plausibility | Non-triviality | Information choice | Budget window | "
        "Measured costs | Decision |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary["loci"]:
        checks = row["checks"]
        decision = "challenge-passed" if row["challenge_probe_passed"] else "challenge-failed"
        lines.append(
            f"| {row['block']} | {checks['plausibility']} | {checks['non_triviality']} | "
            f"{checks['information_choice']} | {checks['budget_window']} | "
            f"`{row['measured_stopping_costs']}` | {decision} |"
        )
    denominator = summary["denominators"]
    lines.extend(
        [
            "",
            f"World-probe denominator: `{denominator['completed_world_probe_rows']}/"
            f"{denominator['planned_world_probe_rows']}` completed; "
            f"`{denominator['failed_world_probe_rows']}` rows contain a failed probe.",
            "",
            f"Loci passed: `{summary['challenge_passed_loci']}/10`; "
            f"failed: `{summary['challenge_failed_loci']}/10`.",
            "",
            "Every measured cost comes from the frozen per-step trace. A missing stopping time "
            "remains a denominator failure. No confirmation secret was generated or consumed.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    markdown = args.markdown.resolve()
    if output.exists() or markdown.exists():
        raise FileExistsError("challenge outputs are immutable; choose unused output paths")
    summary = build_probe_summary(
        _load(args.contract.resolve()),
        args.registry.resolve(),
        root=ROOT,
        evidence_roots=[path.resolve() for path in args.evidence_root],
        source_commit=git_source_commit(ROOT),
    )
    write_json_atomic(output, summary)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(summary), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "completed_world_probe_rows": summary["denominators"]["completed_world_probe_rows"],
                "challenge_passed_loci": summary["challenge_passed_loci"],
                "challenge_failed_loci": summary["challenge_failed_loci"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
