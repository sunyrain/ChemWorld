"""Audit and physically replay development scientific-adaptation receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation_execution import load_protocol_object
from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.scientific_adaptation_postrun import (
    audit_scientific_adaptation_postrun,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--run-root", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-replay", action="store_true")
    parser.add_argument("--replay-workers", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = audit_scientific_adaptation_postrun(
        protocol=load_protocol_object(args.protocol),
        run_roots=args.run_root,
        replay=not args.skip_replay,
        replay_workers=args.replay_workers,
    )
    write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "cells": report["overall"]["cell_count"],
                "experiments": report["overall"]["completed_experiment_count"],
                "replay_verified": report["physical_replay"]["all_verified"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
