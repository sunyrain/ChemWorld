"""Build the audited five-world S0 v1.1 nominal-information interim report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.static_material_information_campaign import (
    build_static_s0_nominal_information_interim,
    render_static_s0_nominal_information_interim_zh,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json"
        ),
    )
    parser.add_argument(
        "--nominal-root",
        type=Path,
        default=Path(
            "runs/formal/static-s0-v11-nominal-codex-subscription-20260729"
        ),
    )
    parser.add_argument(
        "--opaque-root",
        type=Path,
        default=Path("runs/formal/static-s0-v10-codex-subscription-20260729"),
    )
    parser.add_argument(
        "--world-seed",
        action="append",
        dest="world_seeds",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/"
            "static-s0-v1.1-nominal-information-interim-5world-summary.json"
        ),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/"
            "STATIC_S0_V1_1_NOMINAL_INFORMATION_INTERIM_5WORLD_RESULTS_ZH.md"
        ),
    )
    parser.add_argument("--bootstrap-seed", type=int, default=None)
    parser.add_argument("--bootstrap-draws", type=int, default=None)
    return parser


def main() -> int:
    args = _parser().parse_args()
    summary = build_static_s0_nominal_information_interim(
        manifest_path=args.manifest,
        nominal_root=args.nominal_root,
        opaque_root=args.opaque_root,
        world_seeds=args.world_seeds or (0, 1, 2, 3, 4),
        bootstrap_seed=args.bootstrap_seed,
        bootstrap_draws=args.bootstrap_draws,
    )
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(
        render_static_s0_nominal_information_interim_zh(summary),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "json_output": str(args.json_output),
                "markdown_output": str(args.markdown_output),
                "all_selected_cells_exact_replay_verified": summary["execution"][
                    "all_selected_cells_exact_replay_verified"
                ],
                "accounting": summary["accounting"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
