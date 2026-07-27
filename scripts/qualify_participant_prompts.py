"""Generate the offline participant prompt-envelope qualification report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation_execution import (
    DEFAULT_PROTOCOL_PATH,
    load_protocol_object,
)
from chemworld.eval.participant_prompt_qualification import (
    qualify_participant_prompt_envelopes,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = qualify_participant_prompt_envelopes(
        load_protocol_object(args.protocol)
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "fixture_count": report["fixture_count"],
                "all_rows_passed": report["all_rows_passed"],
                "same_environment_view_across_scaffolds": report[
                    "same_environment_view_across_scaffolds"
                ],
                "suggested_development_budgets": report[
                    "suggested_development_budgets"
                ],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["all_rows_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
