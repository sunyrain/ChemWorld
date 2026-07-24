"""Write v0.3 mechanism-adaptation preflight and explicit pending states."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation_preflight import (
    DEFAULT_PROTOCOL,
    ROOT,
    build_mechanism_adaptation_pending_gate_state,
    build_mechanism_adaptation_preflight,
)

DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-preflight.json"
)
DEFAULT_ONLINE_STATE_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-online-attainability-certificate-v0.8-rc24-pending.json"
)
DEFAULT_GATE_A_STATE_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-gate-a-v0.3.0-rc24-pending.json"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--online-state-output",
        type=Path,
        default=DEFAULT_ONLINE_STATE_OUTPUT,
    )
    parser.add_argument(
        "--gate-a-state-output",
        type=Path,
        default=DEFAULT_GATE_A_STATE_OUTPUT,
    )
    args = parser.parse_args()
    report = build_mechanism_adaptation_preflight(args.protocol.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    online_state, gate_a_state = build_mechanism_adaptation_pending_gate_state(
        args.protocol.resolve()
    )
    for path, payload in (
        (args.online_state_output, online_state),
        (args.gate_a_state_output, gate_a_state),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(args.output)
    print(args.online_state_output)
    print(args.gate_a_state_output)
    if not report["implementation_complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
