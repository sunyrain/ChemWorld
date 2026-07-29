"""Build the audited complete S0 material-information three-arm result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.static_material_information_triarm import (
    build_static_s0_material_information_triarm_result,
    render_static_s0_material_information_triarm_zh,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "configs/benchmark/"
            "scientific_optimization_s0_v1.2_"
            "misindexed_information_freeze_manifest.json"
        ),
    )
    parser.add_argument(
        "--nominal-manifest",
        type=Path,
        default=Path(
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_"
            "nominal_information_freeze_manifest.json"
        ),
    )
    parser.add_argument(
        "--opaque-root",
        type=Path,
        default=Path(
            "runs/formal/static-s0-v10-codex-subscription-20260729"
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
        "--misindexed-root",
        type=Path,
        default=Path(
            "runs/formal/static-s0-v12-misindexed-"
            "codex-subscription-20260729"
        ),
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/"
            "static-s0-v1.2-three-arm-information-campaign-summary.json"
        ),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/"
            "STATIC_S0_V1_2_THREE_ARM_INFORMATION_RESULTS_ZH.md"
        ),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    summary = build_static_s0_material_information_triarm_result(
        manifest_path=args.manifest,
        nominal_manifest_path=args.nominal_manifest,
        opaque_root=args.opaque_root,
        nominal_root=args.nominal_root,
        misindexed_root=args.misindexed_root,
    )
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(
        render_static_s0_material_information_triarm_zh(summary),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "json_output": str(args.json_output),
                "markdown_output": str(args.markdown_output),
                "all_sixty_cells_exact_replay_verified": summary[
                    "execution"
                ]["all_sixty_cells_exact_replay_verified"],
                "accounting": summary["accounting"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
