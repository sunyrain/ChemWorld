"""Fail unless every official serious task has current frozen evidence."""

from __future__ import annotations

import json

from chemworld.task_design import serious_task_readiness_manifest
from chemworld.tasks import SERIOUS_TASK_IDS


def main() -> int:
    manifest = serious_task_readiness_manifest()
    expected = len(SERIOUS_TASK_IDS)
    passed = (
        manifest["suite_status"] == "validated"
        and manifest["benchmark_ready_count"] == expected
    )
    print(json.dumps({"passed": passed, **manifest}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
