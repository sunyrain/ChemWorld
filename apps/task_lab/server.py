"""Dependency-free local web server for Agent progress and student feedback."""

from __future__ import annotations

import argparse
import json
import os
import threading
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from apps.task_lab.catalog import task_catalog
from apps.task_lab.classic_runner import (
    CLASSIC_AGENT_IDS,
    run_classic_task,
    supports_classic_task,
)
from apps.task_lab.deepseek_client import DeepSeekClient, ReasoningEffort
from apps.task_lab.run_evaluation import DEFAULT_TASKS
from apps.task_lab.runner import RunMode, run_task
from apps.task_lab.spectral_payload import SpectrumDisclosure
from apps.task_lab.student_session import StudentSessionManager

STATIC_ROOT = Path(__file__).with_name("static")


@dataclass
class RunJob:
    job_id: str
    tasks: list[str]
    mode: str
    model: str
    agent_backend: str
    thinking: bool
    reasoning_effort: str
    budget_multiplier: float
    campaign_override: bool
    spectrum_disclosure: str
    output_dir: Path
    events: list[dict[str, Any]] = field(default_factory=list)
    results: list[dict[str, Any]] = field(default_factory=list)
    status: str = "queued"
    error: str | None = None
    condition: threading.Condition = field(default_factory=threading.Condition)

    def emit(self, event: dict[str, Any]) -> None:
        with self.condition:
            self.events.append({"index": len(self.events), **event})
            self.condition.notify_all()

    def snapshot(self) -> dict[str, Any]:
        with self.condition:
            return {
                "job_id": self.job_id,
                "tasks": list(self.tasks),
                "mode": self.mode,
                "model": self.model,
                "agent_backend": self.agent_backend,
                "thinking": self.thinking,
                "reasoning_effort": self.reasoning_effort,
                "budget_multiplier": self.budget_multiplier,
                "campaign_override": self.campaign_override,
                "spectrum_disclosure": self.spectrum_disclosure,
                "status": self.status,
                "error": self.error,
                "event_count": len(self.events),
                "results": list(self.results),
                "output_dir": str(self.output_dir.resolve()),
            }


class RunJobManager:
    def __init__(self, output_root: Path, *, api_key: str | None = None) -> None:
        self.output_root = output_root
        self._api_key = (api_key or "").strip() or None
        self._jobs: dict[str, RunJob] = {}
        self._lock = threading.RLock()

    @property
    def deepseek_configured(self) -> bool:
        return bool(self._api_key or os.environ.get("DEEPSEEK_API_KEY", "").strip())

    @property
    def credential_source(self) -> str:
        if self._api_key:
            return "api-key-file"
        if os.environ.get("DEEPSEEK_API_KEY", "").strip():
            return "environment"
        return "missing"

    def create(
        self,
        *,
        tasks: list[str],
        mode: RunMode,
        agent_backend: str,
        model: str | None,
        thinking: bool,
        reasoning_effort: ReasoningEffort,
        seed: int | None,
        max_steps: int,
        budget_multiplier: float,
        campaign_override: bool,
        spectrum_disclosure: SpectrumDisclosure,
    ) -> RunJob:
        client: DeepSeekClient | None
        if agent_backend == "deepseek":
            deepseek_client = DeepSeekClient(
                api_key=self._api_key,
                model=model,
                thinking=thinking,
                reasoning_effort=reasoning_effort,
            )
            client = deepseek_client
            display_model = deepseek_client.model
        else:
            if agent_backend not in CLASSIC_AGENT_IDS:
                raise ValueError("unknown agent_backend")
            incompatible = [task for task in tasks if not supports_classic_task(task)]
            if incompatible:
                raise ValueError(
                    "classic active learning is incompatible with: " + ", ".join(incompatible)
                )
            client = None
            display_model = agent_backend
        job_id = uuid.uuid4().hex
        job = RunJob(
            job_id=job_id,
            tasks=tasks,
            mode=mode,
            model=display_model,
            agent_backend=agent_backend,
            thinking=thinking,
            reasoning_effort=reasoning_effort,
            budget_multiplier=budget_multiplier,
            campaign_override=campaign_override,
            spectrum_disclosure=spectrum_disclosure,
            output_dir=self.output_root / job_id,
        )
        with self._lock:
            self._jobs[job_id] = job
        thread = threading.Thread(
            target=self._run,
            args=(job, client, seed, max_steps),
            name=f"task-lab-{job_id[:8]}",
            daemon=True,
        )
        thread.start()
        return job

    def get(self, job_id: str) -> RunJob:
        with self._lock:
            try:
                return self._jobs[job_id]
            except KeyError as exc:
                raise KeyError(f"unknown run job: {job_id}") from exc

    @staticmethod
    def _run(
        job: RunJob,
        client: DeepSeekClient | None,
        seed: int | None,
        max_steps: int,
    ) -> None:
        job.status = "running"
        job.emit(
            {
                "type": "run_started",
                "tasks": job.tasks,
                "model": job.model,
                "agent_backend": job.agent_backend,
                "thinking": job.thinking if job.agent_backend == "deepseek" else False,
                "reasoning_effort": (
                    job.reasoning_effort if job.agent_backend == "deepseek" else None
                ),
                "budget_multiplier": job.budget_multiplier,
                "campaign_override": job.campaign_override,
                "spectrum_disclosure": job.spectrum_disclosure,
            }
        )
        try:
            for task_id in job.tasks:
                if job.agent_backend == "deepseek":
                    if client is None:
                        raise RuntimeError("DeepSeek client was not initialized")
                    result = run_task(
                        client=client,
                        task_id=task_id,
                        output_dir=job.output_dir,
                        seed=seed,
                        mode=job.mode,  # type: ignore[arg-type]
                        max_steps=max_steps,
                        budget_multiplier=job.budget_multiplier,
                        campaign_override=job.campaign_override,
                        spectrum_disclosure=job.spectrum_disclosure,  # type: ignore[arg-type]
                        event_callback=job.emit,
                    )
                else:
                    result = run_classic_task(
                        agent_id=job.agent_backend,
                        task_id=task_id,
                        output_dir=job.output_dir,
                        seed=seed,
                        max_steps=max_steps,
                        budget_multiplier=job.budget_multiplier,
                        campaign_override=job.campaign_override,
                        spectrum_disclosure=job.spectrum_disclosure,  # type: ignore[arg-type]
                        event_callback=job.emit,
                    )
                job.results.append(result.to_dict())
            job.status = "completed"
            job.emit({"type": "run_completed", "results": list(job.results)})
        except Exception as exc:
            job.error = str(exc)
            job.status = "error"
            job.emit({"type": "run_failed", "error": job.error})
        finally:
            with job.condition:
                job.condition.notify_all()


class TaskLabServer(ThreadingHTTPServer):
    def __init__(
        self,
        address: tuple[str, int],
        output_root: Path,
        *,
        api_key: str | None = None,
    ) -> None:
        super().__init__(address, TaskLabHandler)
        self.jobs = RunJobManager(output_root, api_key=api_key)
        self.student_sessions = StudentSessionManager()

    def server_close(self) -> None:
        self.student_sessions.close_all()
        super().server_close()


class TaskLabHandler(BaseHTTPRequestHandler):
    server: TaskLabServer

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/tasks":
            self._json(
                {
                    "tasks": task_catalog(),
                    "quick_tasks": list(DEFAULT_TASKS),
                }
            )
            return
        if path == "/api/status":
            self._json(
                {
                    "deepseek_configured": self.server.jobs.deepseek_configured,
                    "credential_source": self.server.jobs.credential_source,
                }
            )
            return
        if path.startswith("/api/runs/") and path.endswith("/events"):
            job_id = path.split("/")[3]
            self._events(job_id)
            return
        if path.startswith("/api/runs/"):
            job_id = path.split("/")[3]
            try:
                self._json(self.server.jobs.get(job_id).snapshot())
            except KeyError as exc:
                self._error(HTTPStatus.NOT_FOUND, str(exc))
            return
        if path.startswith("/api/student-sessions/"):
            session_id = path.split("/")[3]
            try:
                self._json(self.server.student_sessions.get(session_id).state())
            except KeyError as exc:
                self._error(HTTPStatus.NOT_FOUND, str(exc))
            return
        self._static(path)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            body = self._request_json()
            if path == "/api/runs":
                tasks = body.get("tasks") or list(DEFAULT_TASKS)
                known = {card["task_id"] for card in task_catalog()}
                if (
                    not isinstance(tasks, list)
                    or not tasks
                    or any(task not in known for task in tasks)
                ):
                    raise ValueError("tasks must be a non-empty list of registered task ids")
                mode = str(body.get("mode") or "adaptive")
                if mode not in {"plan", "adaptive"}:
                    raise ValueError("mode must be plan or adaptive")
                agent_backend = str(body.get("agent_backend") or "deepseek")
                if agent_backend not in {"deepseek", *CLASSIC_AGENT_IDS}:
                    raise ValueError("unsupported agent_backend")
                budget_multiplier = float(body.get("budget_multiplier", 1.0))
                if not 1.0 <= budget_multiplier <= 4.0:
                    raise ValueError("budget_multiplier must be between 1.0 and 4.0")
                reasoning_effort = str(body.get("reasoning_effort") or "max")
                if reasoning_effort not in {"high", "max"}:
                    raise ValueError("reasoning_effort must be high or max")
                spectrum_disclosure = str(body.get("spectrum_disclosure") or "unassigned")
                if spectrum_disclosure not in {"raw", "unassigned", "assigned"}:
                    raise ValueError("spectrum_disclosure must be raw, unassigned, or assigned")
                job = self.server.jobs.create(
                    tasks=[str(task) for task in tasks],
                    mode=mode,  # type: ignore[arg-type]
                    agent_backend=agent_backend,
                    model=str(body["model"]) if body.get("model") else None,
                    thinking=bool(body.get("thinking", True)),
                    reasoning_effort=reasoning_effort,  # type: ignore[arg-type]
                    seed=int(body["seed"]) if body.get("seed") is not None else None,
                    max_steps=int(body.get("max_steps", 18)),
                    budget_multiplier=budget_multiplier,
                    campaign_override=bool(body.get("campaign_override", False)),
                    spectrum_disclosure=spectrum_disclosure,  # type: ignore[arg-type]
                )
                self._json(job.snapshot(), status=HTTPStatus.ACCEPTED)
                return
            if path == "/api/student-sessions":
                task_id = str(body.get("task_id") or DEFAULT_TASKS[0])
                seed = int(body["seed"]) if body.get("seed") is not None else None
                session = self.server.student_sessions.create(task_id, seed)
                self._json(session.state(), status=HTTPStatus.CREATED)
                return
            if path.startswith("/api/student-sessions/") and path.endswith("/actions"):
                session_id = path.split("/")[3]
                action = body.get("action")
                if not isinstance(action, dict):
                    raise ValueError("request must contain an action object")
                self._json(self.server.student_sessions.get(session_id).step(action))
                return
            self._error(HTTPStatus.NOT_FOUND, "unknown endpoint")
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except (TypeError, ValueError) as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def _request_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def _events(self, job_id: str) -> None:
        try:
            job = self.server.jobs.get(job_id)
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        index = 0
        try:
            while True:
                with job.condition:
                    if index >= len(job.events) and job.status in {"queued", "running"}:
                        job.condition.wait(timeout=10.0)
                    pending = job.events[index:]
                    finished = job.status in {"completed", "error"}
                for event in pending:
                    data = json.dumps(event, ensure_ascii=False)
                    self.wfile.write(f"data: {data}\n\n".encode())
                    self.wfile.flush()
                    index += 1
                if finished and index >= len(job.events):
                    break
                if not pending:
                    self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return
        finally:
            self.close_connection = True

    def _static(self, path: str) -> None:
        route_files = {
            "": "index.html",
            "/": "index.html",
            "/agent": "agent.html",
            "/agent/": "agent.html",
            "/student": "student.html",
            "/student/": "student.html",
        }
        relative = route_files.get(path, path.lstrip("/"))
        target = (STATIC_ROOT / relative).resolve()
        try:
            target.relative_to(STATIC_ROOT.resolve())
        except ValueError:
            self._error(HTTPStatus.FORBIDDEN, "invalid static path")
            return
        if not target.is_file():
            self._error(HTTPStatus.NOT_FOUND, "not found")
            return
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
        }.get(target.suffix, "application/octet-stream")
        content = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _json(self, payload: Any, *, status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _error(self, status: HTTPStatus, message: str) -> None:
        self._json({"error": message}, status=status)

    def log_message(self, format: str, *args: Any) -> None:
        del format, args


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8876)
    parser.add_argument("--output-dir", default="runs/task_lab/web")
    parser.add_argument(
        "--api-key-file",
        type=Path,
        help="Read a local API key file into memory; the key is never sent to the browser.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = _read_api_key_file(args.api_key_file) if args.api_key_file else None
    server = TaskLabServer(
        (args.host, args.port),
        Path(args.output_dir),
        api_key=api_key,
    )
    print(f"ChemWorld Task Lab: http://{args.host}:{args.port}")
    print(f"学生实验台无需 API key；DeepSeek 凭据状态：{server.jobs.credential_source}。")
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
    return 0


def _read_api_key_file(path: Path) -> str:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"API key file does not exist: {resolved}")
    value = resolved.read_text(encoding="utf-8").strip()
    if not value or "\n" in value or "\r" in value:
        raise ValueError("API key file must contain exactly one non-empty line")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
