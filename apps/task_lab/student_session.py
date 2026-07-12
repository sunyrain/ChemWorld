"""Stateful manual sessions for student operation-and-feedback exercises."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from apps.task_lab.catalog import TASK_BACKGROUNDS
from apps.task_lab.interaction_semantics import (
    aligned_affordance,
    public_state_effects,
    public_vessel_summary,
    validate_interactive_action,
)
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
            campaign = base.campaign_state()
            report = _student_lab_report(base.observation_view("lab_report"), self._history)
            return {
                "session_id": self.session_id,
                "task_id": self.task_id,
                "seed": self.seed,
                "background": TASK_BACKGROUNDS[self.task_id].to_dict(),
                "task_prompt": base.task_prompt(),
                "material_catalog": base.task_info().get("material_catalog", {}),
                "campaign_state": campaign,
                "lab_report": report,
                "available_actions": [
                    aligned_affordance(item, self._history) for item in base.available_actions()
                ],
                "history": list(self._history),
                "public_vessel": public_vessel_summary(self._history, campaign),
                "done": bool(campaign.get("done")),
            }

    def step(self, action: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            base: Any = self._env.unwrapped
            trace = [
                {"selected_action": dict(record.get("action") or {})} for record in self._history
            ]
            validation = validate_interactive_action(base, action, trace)
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
            campaign_before = base.campaign_state()
            observation, reward, terminated, truncated, info = self._env.step(action)
            report = base.observation_view("lab_report")
            campaign = base.campaign_state()
            canonical_action = dict(validation.get("canonical_action", action))
            spectrum = spectral_payload(
                info.get("raw_signal", {}),
                instrument=report.get("instrument_summary", {}).get("instrument"),
            )
            if spectrum["available"]:
                spectrum = {
                    **spectrum,
                    "spectrum_id": (
                        f"experiment-{int(campaign_before.get('experiment_index', 0)) + 1}:"
                        f"step-{len(self._history) + 1}:"
                        f"{spectrum.get('instrument') or spectrum.get('kind') or 'signal'}"
                    ),
                    "provenance": {
                        "source": "measurement_output",
                        "measurement_step": len(self._history) + 1,
                        "experiment_index": int(campaign_before.get("experiment_index", 0)),
                    },
                }
            record = {
                "step": len(self._history) + 1,
                "experiment_index": int(campaign_before.get("experiment_index", 0)),
                "action": to_builtin(canonical_action),
                "action_display": action_material_display(canonical_action),
                "reward": float(reward),
                "leaderboard_score": info.get("leaderboard_score"),
                "best_score": campaign.get("best_score"),
                "visible_metrics": report.get("visible_metrics", {}),
                "constraint_flags": to_builtin(info.get("constraint_flags", {})),
                "observation": observation_to_json(observation),
                "status": report.get("status"),
                "state_effects": public_state_effects(
                    canonical_action,
                    info,
                    experiment_index=int(campaign_before.get("experiment_index", 0)),
                ),
                "spectrum": spectrum,
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


def _recovery_text(base: Any) -> str:
    operations = [str(item["operation"]) for item in base.available_actions()]
    if not operations:
        return "当前没有合法动作，请重置任务。"
    return "可尝试当前合法动作：" + "、".join(operations[:6])


def _student_lab_report(report: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    """Align the report count with the rendered public spectrum series."""

    disclosed = dict(report)
    latest_spectrum = dict(history[-1].get("spectrum") or {}) if history else {}
    if not latest_spectrum.get("available"):
        return disclosed
    series = [item for item in latest_spectrum.get("series", []) if isinstance(item, dict)]
    summary = dict(disclosed.get("spectra_summary") or {})
    summary["channel_count"] = len(series)
    summary["channels"] = [str(item.get("id") or item.get("kind") or "signal") for item in series]
    disclosed["spectra_summary"] = summary
    text = str(disclosed.get("text") or "")
    disclosed["text"] = "\n".join(
        (
            f"Public spectrum: {latest_spectrum.get('kind') or 'signal'} with "
            f"{len(series)} displayed channel(s)."
            if line.startswith("Spectra packet:")
            else line
        )
        for line in text.splitlines()
    )
    return disclosed


__all__ = ["StudentSession", "StudentSessionManager"]
