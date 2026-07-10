"""Stateful manual sessions for student operation-and-feedback exercises."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from apps.task_lab.catalog import TASK_BACKGROUNDS
from apps.task_lab.spectral_payload import spectral_payload
from chemworld.data.logging import observation_to_json, to_builtin
from chemworld.materials import action_material_display
from chemworld.tasks import get_task


@dataclass
class StudentSession:
    task_id: str
    seed: int
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        task = get_task(self.task_id)
        self._env = gym.make("ChemWorld", **task.env_kwargs(seed=self.seed))
        self._env.reset(seed=self.seed)
        self._history: list[dict[str, Any]] = []
        self._lock = threading.RLock()

    def close(self) -> None:
        with self._lock:
            self._env.close()

    def state(self) -> dict[str, Any]:
        with self._lock:
            base: Any = self._env.unwrapped
            return {
                "session_id": self.session_id,
                "task_id": self.task_id,
                "seed": self.seed,
                "background": TASK_BACKGROUNDS[self.task_id].to_dict(),
                "task_prompt": base.task_prompt(),
                "material_catalog": base.task_info().get("material_catalog", {}),
                "campaign_state": base.campaign_state(),
                "lab_report": base.observation_view("lab_report"),
                "available_actions": [
                    _student_affordance(item) for item in base.available_actions()
                ],
                "history": list(self._history),
                "done": bool(base.campaign_state().get("done")),
            }

    def step(self, action: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            base: Any = self._env.unwrapped
            validation = base.validate_action(action)
            if not validation.get("valid", False):
                return {
                    "accepted": False,
                    "validation": validation,
                    "feedback": {
                        "status": "rejected_before_execution",
                        "message": "动作未执行，实验状态和预算均未改变。",
                        "recovery_suggestion": _recovery_text(base),
                    },
                    "state": self.state(),
                }
            observation, reward, terminated, truncated, info = self._env.step(action)
            report = base.observation_view("lab_report")
            campaign = base.campaign_state()
            record = {
                "step": len(self._history) + 1,
                "action": to_builtin(validation.get("canonical_action", action)),
                "action_display": action_material_display(
                    dict(validation.get("canonical_action", action))
                ),
                "reward": float(reward),
                "leaderboard_score": info.get("leaderboard_score"),
                "best_score": campaign.get("best_score"),
                "visible_metrics": report.get("visible_metrics", {}),
                "constraint_flags": to_builtin(info.get("constraint_flags", {})),
                "observation": observation_to_json(observation),
                "status": report.get("status"),
                "spectrum": spectral_payload(
                    info.get("raw_signal", {}),
                    instrument=report.get("instrument_summary", {}).get("instrument"),
                ),
                "spectra_summary": report.get("spectra_summary", {}),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
            }
            self._history.append(record)
            return {
                "accepted": True,
                "validation": validation,
                "feedback": {
                    "status": report.get("status"),
                    "message": report.get("text"),
                    "visible_metrics": report.get("visible_metrics", {}),
                    "spectra_summary": report.get("spectra_summary", {}),
                    "spectrum": record["spectrum"],
                    "instrument_summary": report.get("instrument_summary", {}),
                    "final_assay_summary": report.get("final_assay_summary", {}),
                    "recovery_suggestion": report.get("recovery_suggestion"),
                },
                "record": record,
                "state": self.state(),
            }


class StudentSessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, StudentSession] = {}
        self._lock = threading.RLock()

    def create(self, task_id: str, seed: int | None = None) -> StudentSession:
        task = get_task(task_id)
        session = StudentSession(task_id=task_id, seed=task.seeds[0] if seed is None else seed)
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> StudentSession:
        with self._lock:
            try:
                return self._sessions[session_id]
            except KeyError as exc:
                raise KeyError(f"unknown student session: {session_id}") from exc

    def close_all(self) -> None:
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        for session in sessions:
            session.close()


def _student_affordance(entry: dict[str, Any]) -> dict[str, Any]:
    schema = dict(entry.get("schema") or {})
    return {
        "operation": entry.get("operation"),
        "required_fields": schema.get("required_fields", []),
        "fields": schema.get("fields", []),
        "preconditions": schema.get("preconditions", []),
    }


def _recovery_text(base: Any) -> str:
    operations = [str(item["operation"]) for item in base.available_actions()]
    if not operations:
        return "当前没有合法动作，请重置任务。"
    return "可尝试当前合法动作：" + "、".join(operations[:6])


__all__ = ["StudentSession", "StudentSessionManager"]
