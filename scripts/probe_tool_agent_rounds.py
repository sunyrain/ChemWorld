"""Run a multi-round ToolUsingLLMStubAgent probe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.agent_probe import run_tool_agent_probe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", default="reaction-optimization-standard")
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    parser.add_argument("--budget", type=int)
    parser.add_argument("--min-rounds", type=int, default=12)
    parser.add_argument("--output-dir", default=str(Path("runs") / "tool_agent_probe"))
    args = parser.parse_args()
    report = run_tool_agent_probe(
        task_id=args.task,
        seeds=args.seeds,
        budget=args.budget,
        min_rounds=args.min_rounds,
        output_dir=args.output_dir,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
