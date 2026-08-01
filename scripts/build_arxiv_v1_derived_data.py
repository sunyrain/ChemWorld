"""Build the sole numeric source and CSV tables for arXiv v1."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from chemworld.eval.arxiv_v1_derived_data import (
    build_arxiv_v1_derived_data,
    write_arxiv_v1_tables,
    write_json,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_G2_V04 = Path(
    "runs/development/"
    "g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2/"
    "autonomous_material_campaign_audit.json"
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--g0-v1-0",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json"
        ),
    )
    parser.add_argument(
        "--g0-v1-2",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/"
            "static-s0-v1.2-three-arm-information-campaign-summary.json"
        ),
    )
    parser.add_argument(
        "--task-design",
        type=Path,
        default=Path("workstreams/flagship_tasks/reports/task-design-matrix-v1.json"),
    )
    parser.add_argument(
        "--experiment-ledger",
        type=Path,
        default=Path(
            "workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
        ),
    )
    parser.add_argument("--g2-v0-4-audit", type=Path, default=DEFAULT_G2_V04)
    parser.add_argument("--g2-v0-5-audit", type=Path)
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"),
    )
    parser.add_argument(
        "--table-output-dir",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/tables"),
    )
    return parser


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else REPOSITORY_ROOT / path


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = build_arxiv_v1_derived_data(
        g0_v10_path=_resolve(args.g0_v1_0),
        g0_v12_path=_resolve(args.g0_v1_2),
        task_design_path=_resolve(args.task_design),
        experiment_ledger_path=_resolve(args.experiment_ledger),
        g2_v04_audit_path=_resolve(args.g2_v0_4_audit),
        g2_v05_audit_path=(None if args.g2_v0_5_audit is None else _resolve(args.g2_v0_5_audit)),
    )
    output = _resolve(args.json_output)
    write_json(output, data)
    tables = write_arxiv_v1_tables(_resolve(args.table_output_dir), data)
    print(
        json.dumps(
            {
                "status": data["status"],
                "derived_data_sha256": data["derived_data_sha256"],
                "json_output": output.as_posix(),
                "table_outputs": [path.as_posix() for path in tables],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if data["status"] == "frozen_complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
