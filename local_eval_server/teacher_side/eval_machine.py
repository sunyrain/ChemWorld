# ruff: noqa: E402, I001
"""Local teacher-side evaluator for ChemWorld classroom deployments.

The evaluator keeps ChemWorld and private evaluation configuration in the
teacher process. Student code runs as a separate JSONL subprocess that only
receives sanitized task info, observations, rewards, and public info fields.
"""

from __future__ import annotations

import argparse
import contextlib
import csv
import json
import os
import shutil
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
STUDENT_RUNTIME = PROJECT_ROOT / "local_eval_server" / "student_side" / "student_agent_runtime.py"
DEMO_SUBMISSION = PROJECT_ROOT / "local_eval_server" / "student_side" / "team_alpha_submission"
DEFAULT_CONFIG = PROJECT_ROOT / "local_eval_server" / "teacher_side" / "eval_config.demo.json"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json
from chemworld.eval.leaderboard import aggregate_leaderboard
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task


PRIVATE_ENV_KEYS = {
    "CHEMWORLD_PRIVATE_EVAL_SALT",
    "CHEMWORLD_PRIVATE_SEEDS",
    "CHEMWORLD_PRIVATE_CONFIG",
}
SANITIZED_TASK_KEYS = {
    "world_id",
    "world_provider",
}
SANITIZED_INFO_KEYS = {
    "world_id",
    "world_provider",
    "truth",
}


@dataclass(frozen=True)
class Submission:
    team_id: str
    path: Path
    manifest: dict[str, Any]

    @property
    def agent_name(self) -> str:
        return str(self.manifest["agent_name"])

    @property
    def agent_family(self) -> str:
        return str(self.manifest["agent_family"])

    @property
    def entrypoint(self) -> str:
        return str(self.manifest["entrypoint"])


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def load_config(path: Path) -> dict[str, Any]:
    config = _read_json(path)
    config.setdefault("run_id", datetime.now(UTC).strftime("%Y%m%d_%H%M%S"))
    config.setdefault("tasks", [{"task_id": "reaction-to-assay", "seeds": [0]}])
    config.setdefault("student_timeout_s", 10.0)
    config.setdefault("runtime_python", None)
    return config


def workspace_paths(workspace: Path) -> dict[str, Path]:
    return {
        "workspace": workspace,
        "private": workspace / "teacher_private",
        "incoming": workspace / "submissions" / "incoming",
        "accepted": workspace / "submissions" / "accepted",
        "rejected": workspace / "submissions" / "rejected",
        "runs": workspace / "runs",
        "published": workspace / "published",
    }


def init_workspace(workspace: Path, config_path: Path) -> None:
    paths = workspace_paths(workspace)
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(config_path, paths["private"] / "eval_config.json")
    target = paths["incoming"] / DEMO_SUBMISSION.name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(DEMO_SUBMISSION, target)


def validate_submission(path: Path) -> Submission:
    manifest_path = path / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"{path} is missing manifest.json")
    manifest = _read_json(manifest_path)
    required = {
        "team_id",
        "agent_name",
        "agent_family",
        "entrypoint",
        "dependency_file",
        "llm_used",
        "allowed_network",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        raise ValueError(f"{manifest_path} missing required keys: {missing}")
    if bool(manifest.get("allowed_network")):
        raise ValueError(f"{manifest_path} requests network access")
    entry_module = str(manifest["entrypoint"]).split(":", maxsplit=1)[0]
    if not (path / f"{entry_module}.py").exists():
        raise ValueError(f"{path} missing entrypoint module {entry_module}.py")
    dependency_file = path / str(manifest["dependency_file"])
    if not dependency_file.exists():
        raise ValueError(f"{path} missing dependency file {dependency_file.name}")
    return Submission(team_id=str(manifest["team_id"]), path=path, manifest=manifest)


def accept_submissions(workspace: Path) -> list[Submission]:
    paths = workspace_paths(workspace)
    accepted: list[Submission] = []
    for incoming in sorted(paths["incoming"].iterdir()):
        if not incoming.is_dir():
            continue
        try:
            submission = validate_submission(incoming)
        except ValueError as exc:
            rejected = paths["rejected"] / incoming.name
            if rejected.exists():
                shutil.rmtree(rejected)
            shutil.move(str(incoming), rejected)
            (rejected / "rejection_reason.txt").write_text(str(exc), encoding="utf-8")
            continue
        destination = paths["accepted"] / submission.team_id
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(incoming), destination)
        accepted.append(validate_submission(destination))
    accepted.extend(
        validate_submission(path)
        for path in sorted(paths["accepted"].iterdir())
        if path.is_dir()
    )
    unique: dict[str, Submission] = {submission.team_id: submission for submission in accepted}
    return [unique[key] for key in sorted(unique)]


def _sanitize_mapping(payload: dict[str, Any], blocked: set[str]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in blocked}


class StudentProcess:
    def __init__(
        self,
        submission: Submission,
        *,
        timeout_s: float,
        runtime_python: str | None,
        stderr_path: Path,
    ) -> None:
        self.submission = submission
        self.timeout_s = timeout_s
        self.runtime_python = runtime_python or sys.executable
        self.stderr_path = stderr_path
        self._stderr_handle: TextIO | None = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._process: subprocess.Popen[str] | None = None

    def __enter__(self) -> StudentProcess:
        env = os.environ.copy()
        for key in PRIVATE_ENV_KEYS:
            env.pop(key, None)
        env["PYTHONPATH"] = os.pathsep.join(
            [
                str(self.submission.path),
                str(STUDENT_RUNTIME.parent),
                env.get("PYTHONPATH", ""),
            ]
        )
        self.stderr_path.parent.mkdir(parents=True, exist_ok=True)
        self._stderr_handle = self.stderr_path.open("w", encoding="utf-8")
        self._process = subprocess.Popen(
            [
                self.runtime_python,
                str(STUDENT_RUNTIME),
                "--entrypoint",
                self.submission.entrypoint,
            ],
            cwd=self.submission.path,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self._stderr_handle,
            text=True,
            bufsize=1,
        )
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        del exc_type, exc, tb
        try:
            if self._process and self._process.poll() is None:
                with contextlib.suppress(RuntimeError):
                    self.request({"type": "close"})
                self._process.terminate()
        finally:
            self._executor.shutdown(wait=False, cancel_futures=True)
            if self._stderr_handle is not None:
                self._stderr_handle.close()

    def request(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._process is None or self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("student process is not running")
        if self._process.poll() is not None:
            raise RuntimeError(f"student process exited with code {self._process.returncode}")
        self._process.stdin.write(json.dumps(payload, sort_keys=True) + "\n")
        self._process.stdin.flush()
        future = self._executor.submit(self._process.stdout.readline)
        try:
            line = future.result(timeout=self.timeout_s)
        except TimeoutError as exc:
            self._process.kill()
            raise RuntimeError(
                f"student process timed out after {self.timeout_s:.1f}s"
            ) from exc
        if not line:
            raise RuntimeError("student process closed stdout")
        response = json.loads(line)
        if not bool(response.get("ok", False)):
            raise RuntimeError(str(response.get("error", response)))
        return response


def _task_entries(
    config: dict[str, Any],
    tasks: list[str] | None,
    seeds: list[int] | None,
) -> list[dict[str, Any]]:
    if tasks:
        return [{"task_id": task_id, "seeds": seeds or [0]} for task_id in tasks]
    entries = []
    for entry in config["tasks"]:
        task_id = str(entry["task_id"])
        task = get_task(task_id)
        entries.append(
            {
                "task_id": task_id,
                "seeds": list(entry.get("seeds", task.seeds)),
            }
        )
    return entries


def run_trajectory(
    *,
    submission: Submission,
    task_id: str,
    seed: int,
    config: dict[str, Any],
    run_root: Path,
) -> dict[str, Any]:
    team_root = run_root / submission.team_id
    trajectory_path = (
        team_root / "trajectories" / f"{task_id}_seed{seed}.jsonl"
    )
    result_path = team_root / "results" / f"{task_id}_seed{seed}.json"
    verify_path = team_root / "verify" / f"{task_id}_seed{seed}.json"
    stderr_path = team_root / "logs" / f"{task_id}_seed{seed}.stderr.log"
    stdout_path = team_root / "logs" / f"{task_id}_seed{seed}.teacher.log"
    output_dirs = [
        trajectory_path.parent,
        result_path.parent,
        verify_path.parent,
        stderr_path.parent,
    ]
    for path in output_dirs:
        path.mkdir(parents=True, exist_ok=True)

    if config.get("private_salt"):
        os.environ["CHEMWORLD_PRIVATE_EVAL_SALT"] = str(config["private_salt"])

    env = gym.make("ChemWorld", task_id=task_id, seed=seed)
    observation, task_info = env.reset(seed=seed)
    safe_task_info = _sanitize_mapping(task_info, SANITIZED_TASK_KEYS)
    history: list[dict[str, Any]] = []
    metadata = {
        "agent_name": submission.agent_name,
        "agent_family": submission.agent_family,
        "team_id": submission.team_id,
        "execution_model": "teacher_env_student_jsonl_subprocess",
    }

    with (
        stdout_path.open("w", encoding="utf-8") as stdout_log,
        StudentProcess(
            submission,
            timeout_s=float(config["student_timeout_s"]),
            runtime_python=config.get("runtime_python"),
            stderr_path=stderr_path,
        ) as student,
        TrajectoryLogger(trajectory_path) as logger,
    ):
        stdout_log.write(json.dumps({"event": "reset", "task_id": task_id, "seed": seed}) + "\n")
        student.request({"type": "reset", "task_info": safe_task_info, "seed": seed})
        terminated = False
        truncated = False
        try:
            for step in range(1, int(task_info["budget"]) + 1):
                action = student.request({"type": "act", "history": history})["action"]
                observation, reward, terminated, truncated, info = env.step(action)
                observation_json = observation_to_json(observation)
                safe_info = _sanitize_mapping(info, SANITIZED_INFO_KEYS)
                logger.log(
                    task_info=task_info,
                    step=step,
                    action=action,
                    observation=observation,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata=metadata,
                )
                student.request(
                    {
                        "type": "update",
                        "action": action,
                        "observation": observation_json,
                        "reward": float(reward),
                        "info": safe_info,
                    }
                )
                history.append(
                    {
                        "step": step,
                        "action": action,
                        "observation": observation_json,
                        "reward": float(reward),
                        "info": safe_info,
                    }
                )
                stdout_log.write(
                    json.dumps(
                        {
                            "event": "step",
                            "step": step,
                            "operation": info.get("operation_type"),
                            "terminated": terminated,
                            "truncated": truncated,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                if terminated or truncated:
                    break
        except Exception:
            stdout_log.write(traceback.format_exc())
            raise
        finally:
            env.close()

    records = load_jsonl(trajectory_path)
    result = evaluate_records(records).to_dict()
    verification = verify_records(records).to_dict()
    verification["official_verifier"] = True
    result.update(
        {
            "team_id": submission.team_id,
            "task_id": task_id,
            "trajectory_path": str(trajectory_path),
            "verified": bool(verification["verified"]),
        }
    )
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    verify_path.write_text(
        json.dumps(verification, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return result


def run_all(
    *,
    workspace: Path,
    config: dict[str, Any],
    tasks: list[str] | None,
    seeds: list[int] | None,
) -> list[dict[str, Any]]:
    submissions = accept_submissions(workspace)
    if not submissions:
        raise RuntimeError("No accepted submissions found")
    run_root = workspace_paths(workspace)["runs"] / str(config["run_id"])
    run_root.mkdir(parents=True, exist_ok=True)
    results = []
    for submission in submissions:
        for entry in _task_entries(config, tasks, seeds):
            for seed in entry["seeds"]:
                results.append(
                    run_trajectory(
                        submission=submission,
                        task_id=str(entry["task_id"]),
                        seed=int(seed),
                        config=config,
                        run_root=run_root,
                    )
                )
    (run_root / "all_results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return results


def aggregate(workspace: Path, run_id: str) -> list[dict[str, Any]]:
    run_root = workspace_paths(workspace)["runs"] / run_id
    result_paths = sorted(run_root.glob("*/results/*.json"))
    if not result_paths:
        raise RuntimeError(f"No result JSON files found under {run_root}")
    results = [_read_json(path) for path in result_paths]
    rows = aggregate_leaderboard(results)
    published = workspace_paths(workspace)["published"]
    published.mkdir(parents=True, exist_ok=True)
    json_path = published / f"{run_id}_leaderboard.json"
    csv_path = published / f"{run_id}_leaderboard.csv"
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def summarize(workspace: Path, run_id: str) -> dict[str, Any]:
    """Summarize a teacher-side local evaluation run."""

    paths = workspace_paths(workspace)
    run_root = paths["runs"] / run_id
    result_paths = sorted(run_root.glob("*/results/*.json"))
    verify_paths = sorted(run_root.glob("*/verify/*.json"))
    if not result_paths:
        raise RuntimeError(f"No result JSON files found under {run_root}")
    results = [_read_json(path) for path in result_paths]
    verifications = [_read_json(path) for path in verify_paths]
    leaderboard_rows = aggregate(workspace, run_id)
    team_ids = sorted({str(result["team_id"]) for result in results})
    task_ids = sorted({str(result["task_id"]) for result in results})
    verified_count = sum(1 for item in verifications if bool(item.get("verified", False)))
    failed_verifications = [
        str(path.relative_to(run_root))
        for path, item in zip(verify_paths, verifications, strict=True)
        if not bool(item.get("verified", False))
    ]
    published = paths["published"]
    summary = {
        "run_id": run_id,
        "workspace": str(workspace),
        "team_count": len(team_ids),
        "teams": team_ids,
        "task_count": len(task_ids),
        "tasks": task_ids,
        "result_count": len(results),
        "verification_count": len(verifications),
        "verified_count": verified_count,
        "failed_verifications": failed_verifications,
        "leaderboard_rows": len(leaderboard_rows),
        "leaderboard_json": str(published / f"{run_id}_leaderboard.json"),
        "leaderboard_csv": str(published / f"{run_id}_leaderboard.csv"),
        "summary_json": str(published / f"{run_id}_summary.json"),
    }
    (published / f"{run_id}_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return summary


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local ChemWorld teacher-side evaluator.")
    parser.add_argument("--workspace", type=Path, default=Path("runs/local_eval_machine"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "init-demo",
        help="Create a local eval workspace with one demo submission.",
    )
    subparsers.add_parser("validate", help="Validate and accept incoming submissions.")

    run_parser = subparsers.add_parser("run", help="Run accepted submissions.")
    run_parser.add_argument("--tasks", nargs="*", default=None)
    run_parser.add_argument("--seeds", nargs="*", type=int, default=None)

    aggregate_parser = subparsers.add_parser("aggregate", help="Aggregate one run leaderboard.")
    aggregate_parser.add_argument("--run-id", default=None)

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="Summarize one run with verification and leaderboard artifacts.",
    )
    summarize_parser.add_argument("--run-id", default=None)

    demo_parser = subparsers.add_parser("demo", help="Initialize, run, and aggregate a tiny demo.")
    demo_parser.add_argument("--tasks", nargs="*", default=["reaction-to-assay"])
    demo_parser.add_argument("--seeds", nargs="*", type=int, default=[0])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    config = load_config(args.config)
    if args.command == "init-demo":
        init_workspace(args.workspace, args.config)
        print(json.dumps({"workspace": str(args.workspace), "initialized": True}, indent=2))
        return 0
    if args.command == "validate":
        accepted = accept_submissions(args.workspace)
        print(json.dumps({"accepted": [item.team_id for item in accepted]}, indent=2))
        return 0
    if args.command == "run":
        results = run_all(
            workspace=args.workspace,
            config=config,
            tasks=args.tasks,
            seeds=args.seeds,
        )
        print(json.dumps({"result_count": len(results)}, indent=2))
        return 0
    if args.command == "aggregate":
        rows = aggregate(args.workspace, args.run_id or str(config["run_id"]))
        print(json.dumps(rows, indent=2, sort_keys=True))
        return 0
    if args.command == "summarize":
        summary = summarize(args.workspace, args.run_id or str(config["run_id"]))
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "demo":
        init_workspace(args.workspace, args.config)
        results = run_all(
            workspace=args.workspace,
            config=config,
            tasks=args.tasks,
            seeds=args.seeds,
        )
        rows = aggregate(args.workspace, str(config["run_id"]))
        summary = summarize(args.workspace, str(config["run_id"]))
        print(
            json.dumps(
                {
                    "workspace": str(args.workspace),
                    "result_count": len(results),
                    "leaderboard": rows,
                    "summary": summary,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    raise AssertionError(f"Unhandled command {args.command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
