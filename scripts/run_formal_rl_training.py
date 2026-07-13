"""Execute or resume the preregistered formal PPO Train/Dev matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.rl.formal_training import (
    DEFAULT_PLAN_PATH,
    finalize_training,
    load_execution_inputs,
    run_pending_jobs,
    scan_completed_jobs,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--task")
    parser.add_argument("--model-seed", type=int)
    parser.add_argument("--max-jobs", type=int)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--finalize-only", action="store_true")
    parser.add_argument("--skip-finalize", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    plan, formal, methods = load_execution_inputs(root=root, plan_path=args.plan)
    if args.audit_only:
        completed = scan_completed_jobs(root=root, plan=plan)
        result = {
            "schema_version": "chemworld-formal-ppo-execution-audit-0.4",
            "planned_job_count": 20,
            "completed_job_count": len(completed),
            "remaining_job_count": 20 - len(completed),
            "completed_job_ids": [job.job_id for job in completed],
        }
    elif args.finalize_only:
        result = finalize_training(
            root=root,
            plan=plan,
            formal_protocol=formal,
            methods_config=methods,
        )
    else:
        result = run_pending_jobs(
            root=root,
            plan=plan,
            formal_protocol=formal,
            task_id=args.task,
            model_seed=args.model_seed,
            max_jobs=args.max_jobs,
        )
        if result["remaining_job_count"] == 0 and not args.skip_finalize:
            result["final_report"] = finalize_training(
                root=root,
                plan=plan,
                formal_protocol=formal,
                methods_config=methods,
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
