"""Write and validate the complete WF-00 task maturity audit report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.runtime.maturity_audit import (
    DEFAULT_MATURITY_AUDIT_PATH,
    write_maturity_audit_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_MATURITY_AUDIT_PATH)
    args = parser.parse_args()
    report = write_maturity_audit_report(args.output)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "schema_version": report["schema_version"],
                "task_count": report["task_count"],
                "declaration_alignment_status": report["declaration_alignment_status"],
                "declaration_gap_count": report["declaration_gap_count"],
                "report_hash": report["report_hash"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
