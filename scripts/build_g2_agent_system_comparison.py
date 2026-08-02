"""Build the audited Codex/DeepSeek G2 complete-system comparison."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from chemworld.eval.g2_agent_system_comparison import (
    write_g2_agent_system_comparison,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-audit", type=Path, required=True)
    parser.add_argument("--deepseek-audit", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = write_g2_agent_system_comparison(
        args.codex_audit,
        args.deepseek_audit,
        json_path=args.json_output,
        markdown_path=args.markdown_output,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "matched_cell_count": report["physical_matching"][
                    "matched_cell_count"
                ],
                "comparison_sha256": report["comparison_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
