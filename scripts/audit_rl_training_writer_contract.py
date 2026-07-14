"""Run the tiny behavioral RL checkpoint-writer compatibility preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.rl_training_writer_audit import run_rl_training_writer_probe


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/rl-training-writer-contract-v0.4.json"),
    )
    args = parser.parse_args()
    report = run_rl_training_writer_probe(root=args.repo_root)
    output = args.output
    if not output.is_absolute():
        output = args.repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "writer_contract_ready": report["writer_contract_ready"],
                "formal_training_allowed": report["formal_training_allowed"],
                "output": str(output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["writer_contract_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
