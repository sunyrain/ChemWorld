"""Build the audited world-level summary for the frozen S0 v1.0 campaign."""

from __future__ import annotations

import argparse
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.static_optimization_campaign import (
    build_static_s0_campaign_summary,
    render_static_s0_campaign_summary_zh,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "configs/benchmark/"
            "scientific_optimization_s0_v1.0_freeze_manifest.json"
        ),
    )
    parser.add_argument("--participant-root", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--bootstrap-seed", type=int, default=20260729)
    parser.add_argument("--bootstrap-draws", type=int, default=200_000)
    args = parser.parse_args()

    summary = build_static_s0_campaign_summary(
        manifest_path=args.manifest,
        participant_root=args.participant_root,
        baseline_root=args.baseline_root,
        bootstrap_seed=args.bootstrap_seed,
        bootstrap_draws=args.bootstrap_draws,
    )
    write_json_atomic(args.output, summary)
    if args.markdown_output is not None:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(
            render_static_s0_campaign_summary_zh(summary),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
