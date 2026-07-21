"""Generate the non-destructive v0.1.1 flagship reanalysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.flagship_reanalysis import (
    ROOT,
    SOURCE_REPORT,
    build_flagship_reanalysis,
    load_v0_1_report,
    render_flagship_reanalysis_markdown,
)

DEFAULT_JSON = (
    ROOT / "workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT / "workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.1.md"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE_REPORT)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    report = build_flagship_reanalysis(
        load_v0_1_report(args.source),
        source_path=args.source.resolve(),
    )
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    args.markdown.write_text(
        render_flagship_reanalysis_markdown(report),
        encoding="utf-8",
        newline="\n",
    )
    print(args.json)
    print(args.markdown)


if __name__ == "__main__":
    main()
