#!/usr/bin/env python3
"""Build/check provider-blocked development execution configs for A-P terminal D1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ap_terminal_d1_development_execution import (
    AP_D1_PROVIDER_SPECS,
    AP_D1_TASK_SPECS,
    build_all_ap_d1_development_execution_configs,
    validate_ap_d1_development_execution_configs,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_READINESS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-ap-independent-terminal-d1-readiness-v0.1.json"
)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_or_check(path: Path, value: dict[str, object], *, check: bool) -> None:
    if check:
        if not path.is_file() or _load(path) != value:
            raise RuntimeError(f"generated development config is missing or stale: {path}")
        return
    write_json_atomic(path, value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    readiness_path = args.readiness.resolve()
    configs = build_all_ap_d1_development_execution_configs(ROOT, readiness_path)
    observed: dict[str, dict[str, object]] = {}
    outputs: list[str] = []
    for provider_id, provider_spec in AP_D1_PROVIDER_SPECS.items():
        observed = {}
        provider_outputs = provider_spec["outputs"]
        for task_id in AP_D1_TASK_SPECS:
            output = (ROOT / str(provider_outputs[task_id])).resolve()
            _write_or_check(output, configs[provider_id][task_id], check=bool(args.check))
            observed[task_id] = _load(output)
            outputs.append(output.relative_to(ROOT).as_posix())
        errors = validate_ap_d1_development_execution_configs(
            ROOT,
            readiness_path,
            observed,
            provider_id=provider_id,
        )
        if errors:
            raise RuntimeError(
                "A-P D1 development execution validation failed: "
                + "; ".join(errors)
            )
    print(
        json.dumps(
            {
                "status": "ready_development_execution_provider_blocked",
                "task_count": len(AP_D1_TASK_SPECS),
                "provider_count": len(AP_D1_PROVIDER_SPECS),
                "config_count": len(outputs),
                "provider_execution_authorized": False,
                "outputs": outputs,
                "check": bool(args.check),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
