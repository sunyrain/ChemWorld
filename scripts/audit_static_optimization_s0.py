"""Replay and audit one S0 static optimization run."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.static_optimization_postrun import audit_static_optimization_run


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--world-seed",
        type=int,
        default=None,
        help="Override the static world seed used by the audited run.",
    )
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    if args.world_seed is not None:
        protocol = copy.deepcopy(protocol)
        protocol["world_policy"] = copy.deepcopy(protocol["world_policy"])
        protocol["world_policy"]["world_seed"] = int(args.world_seed)
    report = audit_static_optimization_run(protocol=protocol, run_root=args.run_root)
    write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "replay_verified": report["replay"]["all_verified"],
                "experiments": report["replay"]["replayed_experiment_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
