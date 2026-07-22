"""Write the frozen v0.2.1 mechanism-adaptation preflight report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation_preflight import (
    DEFAULT_PROTOCOL,
    ROOT,
    build_mechanism_adaptation_preflight,
)

DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.2.1-preflight.json"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build_mechanism_adaptation_preflight(args.protocol.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(args.output)
    if not report["implementation_complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
