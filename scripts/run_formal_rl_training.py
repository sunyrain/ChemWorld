"""Execute or resume a preregistered formal PPO/SAC Train/Dev matrix."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from chemworld.rl.formal_training import (
    DEFAULT_PLAN_PATH,
    build_formal_allocation,
    build_jobs,
    finalize_training,
    load_execution_inputs,
    run_pending_jobs,
    scan_completed_jobs,
    verify_current_contract_preflight,
)
from chemworld.rl.training import train_sb3_baseline


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
    parser.add_argument("--probe-backend", choices=("dummy", "subprocess"))
    parser.add_argument("--probe-steps", type=int, default=1024)
    parser.add_argument("--probe-torch-threads", type=int)
    args = parser.parse_args()

    root = args.root.resolve()
    plan, formal, methods = load_execution_inputs(root=root, plan_path=args.plan)
    algorithm = plan["algorithm"]
    if algorithm == "sac" and not args.probe_backend and not args.audit_only:
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
        ).strip()
        verify_current_contract_preflight(
            root=root,
            plan=plan,
            source_commit=source_commit,
        )
    if args.probe_backend:
        task_id = args.task or "partition-discovery"
        infrastructure = plan["infrastructure"]
        allocation = build_formal_allocation(formal, task_id=task_id, name="train")
        torch_threads = args.probe_torch_threads or int(infrastructure["torch_num_threads"])
        output_dir = (
            root
            / plan["execution"]["artifact_root"]
            / "throughput-probes"
            / (f"{args.probe_backend}-threads-{torch_threads}")
        )
        manifest = train_sb3_baseline(
            algorithm=algorithm,
            task_id=task_id,
            allocation=allocation,
            total_timesteps=args.probe_steps,
            model_seed=9900 + torch_threads,
            output_dir=output_dir,
            algorithm_kwargs=dict(plan["training"]["hyperparameters"]),
            operation_budget=int(plan["training"]["operation_budget"]),
            parallel_environments=int(infrastructure["parallel_environments"]),
            vectorization_backend=args.probe_backend,
            device=infrastructure["device"],
            torch_num_threads=torch_threads,
            progress_interval_steps=args.probe_steps,
        )
        result = {
            "schema_version": f"chemworld-formal-{algorithm}-throughput-probe-0.4",
            "diagnostic_only": True,
            "algorithm": algorithm,
            "backend": args.probe_backend,
            "torch_num_threads": torch_threads,
            "task_id": task_id,
            "requested_steps": args.probe_steps,
            "actual_steps": manifest["training_environment_step_count"],
            "step_budget_exact": manifest["step_budget_exact"],
            "wall_time_s": manifest["wall_time_s"],
            "cpu_time_s": manifest["cpu_time_s"],
            "environment_steps_per_wall_second": manifest["training_infrastructure"][
                "environment_steps_per_wall_second"
            ],
            "reference_search_used": False,
            "bench_accessed": False,
        }
    elif args.audit_only:
        completed = scan_completed_jobs(root=root, plan=plan)
        planned = len(build_jobs(plan))
        result = {
            "schema_version": f"chemworld-formal-{algorithm}-execution-audit-0.4",
            "algorithm": algorithm,
            "planned_job_count": planned,
            "completed_job_count": len(completed),
            "remaining_job_count": planned - len(completed),
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
