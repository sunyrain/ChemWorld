"""Persistent local research runs; public views stay separate from replay identity.

Archived runs remain readable after restart. Live environments are intentionally
not silently reconstructed: clone the saved design to start another experiment.
"""

# ruff: noqa: RUF001 -- Chinese user-facing messages use Chinese punctuation.

from __future__ import annotations

import io
import json
import re
import threading
import zipfile
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import gymnasium as gym
import numpy as np

import chemworld
from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace, _atomic_write_text
from chemworld.agents.notebook_versions import NotebookVersions
from chemworld.agents.task_recipes import task_recipe_dimension, task_recipe_from_unit_vector
from chemworld.data.logging import TrajectoryLogger, load_jsonl, to_builtin
from chemworld.eval.verify import verify_records
from chemworld.runtime.semantics import RUNTIME_SEMANTICS_ID
from chemworld.tasks import get_task, list_tasks
from chemworld.workbench.signals import chart_series


def now() -> str:
    return datetime.now(UTC).isoformat()


def integer(value: Any, name: str, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in {low}..{high}")
    return value


def write_json(path: Path, value: Any) -> None:
    _atomic_write_text(path, json.dumps(to_builtin(value), ensure_ascii=False, allow_nan=False))


def validate_design(raw: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(raw, dict) or set(raw) - {"task_id", "composition", "seed", "budget"}:
        raise ValueError("Design accepts task_id or composition, seed and budget")
    seed = integer(raw.get("seed", 0), "seed", 0, 2**32 - 1)
    budget = integer(raw.get("budget", 24), "budget", 1, 200)
    if raw.get("composition") is not None:
        if raw.get("task_id"):
            raise ValueError("Choose a reference task or a composition, not both")
        specification = deepcopy(raw["composition"])
        if not isinstance(specification, dict) or not isinstance(specification.get("task"), dict):
            raise ValueError("composition.task must be an object")
        specification["task"]["budget"] = budget
        specification["task"].setdefault("resources", {})["operation_budget"] = budget
        specification["task"]["episode_mode"] = "single_experiment"
        compiled = chemworld.compile_world_composition(specification)
        return {"composition": specification, "seed": seed, "budget": budget}, compiled.env_kwargs(
            seed=seed
        )
    task_id = raw.get("task_id", "reaction-to-assay")
    if not isinstance(task_id, str):
        raise ValueError("task_id must be a string")
    task = get_task(task_id)
    return {"task_id": task_id, "seed": seed, "budget": budget}, {
        **task.env_kwargs(seed=seed),
        "budget_override": budget,
        "episode_mode_override": "single_experiment",
    }


def catalog() -> list[dict[str, Any]]:
    return [
        {
            "task_id": t.task_id,
            "description": t.description,
            "budget": t.budget,
            "operations": list(t.allowed_operations),
            "instruments": list(t.allowed_instruments),
        }
        for t in list_tasks()
    ]


class ResearchRun:
    def __init__(self, root: Path, metadata: dict[str, Any], env: Any = None) -> None:
        self.root = root
        self.data = metadata
        self.env = env
        self.lock = threading.RLock()
        self.cancel = threading.Event()
        self.logger = TrajectoryLogger(root / "trajectory.jsonl") if env is not None else None
        self.documents = ExperimentDocumentWorkspace(root, versioned_notebook=True)
        self.documents.initialize()
        human = root / "human" / "notes.md"
        if not human.exists():
            _atomic_write_text(human, "")
        self.human = NotebookVersions(human, "")
        self.human.sync_view()
        self._provenance = (
            {**env.unwrapped.task_info(), **env.unwrapped.evaluator_provenance()}
            if env is not None
            else {}
        )

    def persist(self) -> None:
        self.data["updated_at"] = now()
        write_json(self.root / "run.json", self.data)

    def public_view(self) -> dict[str, Any]:
        view = to_builtin(self.env.unwrapped.observation_view("tool_json"))
        view.pop(
            "raw_signal", None
        )  # Raw packets are separately addressable, not repeated per poll.
        return view

    def snapshot(self, *, summary: bool = False) -> dict[str, Any]:
        with self.lock:
            result = deepcopy(self.data)
            result["live"] = self.env is not None
            if summary:
                result.pop("events", None)
                result.pop("view", None)
                result.pop("task_prompt", None)
                result.pop("recipe", None)
            else:
                result["model_notebook"] = self.documents.notebook_tool("log", limit=100)
                result["human_notebook"] = self.human.log(limit=100)
            return result

    def step(self, action: dict[str, Any], *, expected_step: int | None = None) -> dict[str, Any]:
        with self.lock:
            if self.env is None or self.data["status"] not in {"ready", "running"}:
                raise ValueError("This run is not active; clone its design to start another run")
            if self.cancel.is_set():
                raise ValueError("Run cancellation requested")
            if expected_step is not None and expected_step != len(self.data["events"]):
                raise ValueError("The run changed; refresh before submitting another action")
            if len(self.data["events"]) >= 240:
                raise ValueError("Submission limit reached")
            if not isinstance(action, dict):
                raise ValueError("action must be an object")
            base = self.env.unwrapped
            validation = to_builtin(base.validate_action(action))
            event: dict[str, Any] = {
                "event_id": f"event-{len(self.data['events']) + 1:04d}",
                "recorded_at": now(),
                "action": deepcopy(action),
                "validation": validation,
                "transaction_status": "rejected",
            }
            if validation.get("valid"):
                obs, reward, terminated, truncated, info = self.env.step(action)
                self.logger.log(
                    task_info=self._provenance,
                    step=self.data["executed_steps"] + 1,
                    action=action,
                    observation=obs,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={"agent_name": self.data["actor"]},
                )
                self.data["executed_steps"] += 1
                public = to_builtin(base.observation_view("tool_json"))
                raw = public.pop("raw_signal", {})
                event.update(
                    transaction_status=info["transaction_status"],
                    observation=public.get("observation", {}),
                    observed_mask=public.get("observed_mask", {}),
                    report=public.get("lab_report", {}),
                    cost=public.get("cost"),
                    delta=to_builtin(info.get("state_delta_summary", {})),
                    terminated=bool(terminated),
                    truncated=bool(truncated),
                )
                if raw:
                    filename = event["event_id"] + ".json"
                    write_json(self.root / "measurements" / filename, raw)
                    event["measurement"] = event["event_id"]
                    event["series"] = chart_series(raw, str(action.get("instrument", "signal")))
                self.data["view"] = public
                self.data["final_assay_count"] = public["campaign_state"]["final_assay_count"]
                if terminated or truncated:
                    self.data["status"] = (
                        "completed"
                        if self.data["final_assay_count"] > 0
                        else "truncated"
                        if truncated
                        else "stopped"
                    )
            self.data["events"].append(event)
            self.documents.append_operation({k: v for k, v in event.items() if k != "series"})
            self.data["submitted_steps"] = len(self.data["events"])
            self.data["rejected_steps"] = sum(
                e["transaction_status"] != "committed" for e in self.data["events"]
            )
            self.persist()
            if self.data["status"] in {"completed", "truncated", "stopped"}:
                self.stop(self.data["status"])
            return deepcopy(event)

    def stop(self, status: str, message: str | None = None) -> None:
        with self.lock:
            if self.data["status"] in {"ready", "running", "cancelling"}:
                self.data["status"] = status
            if message:
                self.data["message"] = message
            self.persist()
            if self.logger:
                self.logger.close()
                self.logger = None
            if self.env is not None:
                self.env.close()
                self.env = None

    def notebook(self, author: str, operation: str, arguments: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            if author not in {"human", "model"}:
                raise ValueError("Unknown notebook author")
            if author == "model":
                return self.documents.notebook_tool(operation, **arguments)
            if operation in {"write", "restore"}:
                method = self.human.commit if operation == "write" else self.human.restore
                return method(
                    public_cursor={
                        "event_count": len(self.data["events"]),
                        "last_event_id": self.data["events"][-1]["event_id"]
                        if self.data["events"]
                        else None,
                    },
                    **arguments,
                )
            if operation not in {"read", "log", "diff"}:
                raise ValueError("Unknown notebook operation")
            return getattr(self.human, operation)(**arguments)

    def replay(self) -> dict[str, Any]:
        with self.lock:
            if self.data.get("archive_only"):
                raise ValueError(
                    "Imported campaign: view its recorded replay result; no new replay is run here"
                )
            if self.data["status"] in {"running", "cancelling"}:
                raise ValueError("Wait for the worker to stop before replay")
            records = load_jsonl(self.root / "trajectory.jsonl")
            if not records:
                raise ValueError("No executed actions to replay")
            result = verify_records(records, tolerance=0.0).to_dict()
            self.data["replay"] = result
            self.persist()
            return result

    def export(self) -> bytes:
        with self.lock:
            if self.data["status"] in {"running", "cancelling"}:
                raise ValueError("Stop the worker before exporting a consistent archive")
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(self.root.rglob("*")):
                    if path.is_file() and not path.is_symlink():
                        archive.write(path, path.relative_to(self.root).as_posix())
            return output.getvalue()


class ResearchStore:
    """One local owner's workspace. Does not claim multi-user authorization."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.runs: dict[str, ResearchRun] = {}
        for path in sorted(self.root.glob("*/run.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            run = ResearchRun(path.parent, data)
            if data["status"] in {"ready", "running", "cancelling"}:
                run.stop("interrupted", "服务曾退出；已保存记录仍可查阅，请复制设计开始新批次。")
            self.runs[data["id"]] = run

    def get(self, run_id: str) -> ResearchRun:
        if not re.fullmatch(r"[a-f0-9]{32}", run_id) or run_id not in self.runs:
            raise KeyError("Unknown run")
        return self.runs[run_id]

    def create(self, payload: dict[str, Any]) -> ResearchRun:
        if not isinstance(payload, dict) or set(payload) - {
            "name",
            "project",
            "question",
            "design",
        }:
            raise ValueError("Run accepts name, project, question and design")
        design, kwargs = validate_design(payload.get("design", {}))
        strings = {}
        for field, default, limit in (
            ("name", "新实验", 120),
            ("project", "我的研究", 120),
            ("question", "", 4000),
        ):
            value = payload.get(field, default)
            if not isinstance(value, str) or len(value) > limit:
                raise ValueError(f"{field} must be text with at most {limit} characters")
            strings[field] = value.strip() or default
        with self.lock:
            if len(self.runs) >= 200:
                raise ValueError("Workspace limit: 200 runs; use another data directory")
            if sum(r.env is not None for r in self.runs.values()) >= 8:
                raise ValueError("Close an active run first (maximum 8)")
            env = gym.make("ChemWorld", **kwargs)
            try:
                env.reset(seed=design["seed"])
                run_id = uuid4().hex
                root = self.root / run_id
                root.mkdir()
                metadata = {
                    "id": run_id,
                    **strings,
                    "design": design,
                    "created_at": now(),
                    "runtime_semantics": RUNTIME_SEMANTICS_ID,
                    "status": "ready",
                    "actor": "manual",
                    "events": [],
                    "executed_steps": 0,
                    "submitted_steps": 0,
                    "rejected_steps": 0,
                    "final_assay_count": 0,
                    "model_calls": 0,
                    "usage": {"input_tokens": 0, "output_tokens": 0, "complete": True},
                    "cost_usd": None,
                    "replay": None,
                    "task_prompt": to_builtin(env.unwrapped.task_prompt()),
                }
                run = ResearchRun(root, metadata, env)
                metadata["view"] = run.public_view()
                # A deterministic reference recipe is a convenience, not an adaptive agent.
                info = env.unwrapped.task_info()
                recipe = task_recipe_from_unit_vector(
                    info, np.full(task_recipe_dimension(info), 0.5)
                )
                metadata["recipe"] = to_builtin(recipe["steps"])
                run.persist()
                self.runs[run_id] = run
                return run
            except BaseException:
                env.close()
                raise

    def summaries(self) -> list[dict[str, Any]]:
        with self.lock:
            return sorted(
                (r.snapshot(summary=True) for r in self.runs.values()),
                key=lambda r: r["created_at"],
                reverse=True,
            )

    def close(self) -> None:
        for run in list(self.runs.values()):
            run.cancel.set()
            if run.env is not None:
                run.stop("interrupted", "本机服务已关闭；数据已保留。")
