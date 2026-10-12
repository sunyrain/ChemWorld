"""Loopback-only workbench. Run with python -m apps.research_workbench."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import webbrowser
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from apps.research_workbench.jobs import Jobs
from apps.research_workbench.workspace_lock import WorkspaceLock
from chemworld.lab.http_security import LocalServer, RequestRejected, check_local, read_local_json
from chemworld.workbench.providers import PROVIDERS
from chemworld.workbench.service import ResearchStore, catalog, validate_design

STATIC = Path(__file__).parent / "static"
REPO = Path(__file__).resolve().parents[2]


class WorkbenchServer(LocalServer):
    def __init__(self, address: tuple[str, int], data_dir: Path) -> None:
        self.workspace_lock = WorkspaceLock(data_dir)
        try:
            super().__init__(address, Handler)
            self.store = ResearchStore(data_dir)
            self.jobs = Jobs(self.store)
        except BaseException:
            self.workspace_lock.close()
            raise

    def server_close(self) -> None:
        super().server_close()
        self.workspace_lock.close()


class Handler(BaseHTTPRequestHandler):
    server: WorkbenchServer

    def log_message(self, fmt: str, *args: Any) -> None:
        pass  # No URLs, bodies or provider errors in access logs.

    def send(
        self,
        value: Any,
        status: int = 200,
        *,
        media: str = "application/json",
        filename: str | None = None,
    ) -> None:
        body = (
            value
            if isinstance(value, bytes)
            else json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        )
        self.send_response(status)
        self.send_header(
            "Content-Type", media + ("; charset=utf-8" if media != "application/zip" else "")
        )
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; "
            "style-src 'self'; img-src 'self' data:; connect-src 'self'; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
        )
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self.dispatch(False)

    def do_POST(self) -> None:
        self.dispatch(True)

    def dispatch(self, write: bool) -> None:
        try:
            check_local(self)
            body = read_local_json(self) if write else {}
            url = urlsplit(self.path)
            path = url.path
            query = parse_qs(url.query)
            if path == "/api/catalog" and not write:
                templates = []
                for name in (
                    "composed-reaction-assay-v0.1.json",
                    "composed-equilibrium-characterization-v0.1.json",
                    "composed-reaction-purification-v0.1.json",
                ):
                    templates.append(
                        json.loads(
                            (REPO / "examples/world-authoring" / name).read_text(encoding="utf-8")
                        )
                    )
                self.send(
                    {
                        "tasks": catalog(),
                        "templates": templates,
                        "local_only": True,
                        "providers": [
                            {"id": k, **v, "live_verified": False} for k, v in PROVIDERS.items()
                        ],
                    }
                )
            elif path == "/api/health" and not write:
                self.send({"ok": True, "local_only": True, "runs": len(self.server.store.runs)})
            elif path == "/api/design/validate" and write:
                design, _ = validate_design(body)
                self.send({"valid": True, "design": design})
            elif path == "/api/runs":
                if write:
                    self.send(self.server.store.create(body).snapshot(), 201)
                else:
                    self.send({"runs": self.server.store.summaries()})
            elif match := re.fullmatch(r"/api/runs/([a-f0-9]{32})(?:/([a-z-]+))?", path):
                run_id, operation = match.groups()
                run = self.server.store.get(run_id)
                if not operation and not write:
                    self.send(run.snapshot())
                elif operation == "step" and write:
                    with run.lock:
                        if run.data["status"] != "ready":
                            raise ValueError("Manual actions require an idle manual run")
                        if type(body.get("expected_step")) is not int:
                            raise ValueError(
                                "expected_step is required to prevent stale submissions"
                            )
                        run.step(body.get("action"), expected_step=body["expected_step"])
                        self.send(run.snapshot())
                elif operation == "start" and write:
                    self.send(self.server.jobs.start(run_id, body), 202)
                elif operation == "cancel" and write:
                    self.send(self.server.jobs.cancel(run_id))
                elif operation == "replay" and write:
                    self.send(run.replay())
                elif operation == "notebook" and write:
                    author, action = body.get("author", "human"), body.get("operation", "read")
                    if author == "model" and action not in {"read", "log", "diff"}:
                        raise ValueError("Model notebook is read-only here; edit your own notes")
                    arguments = body.get("arguments", {})
                    if (
                        not isinstance(arguments, dict)
                        or len(str(arguments.get("text", ""))) > 16000
                    ):
                        raise ValueError("Notebook accepts at most 16000 characters")
                    self.send(run.notebook(author, action, arguments))
                elif operation == "measurement" and not write:
                    event_id = query.get("event", [""])[0]
                    with run.lock:
                        event = next(
                            (e for e in run.data["events"] if e.get("measurement") == event_id),
                            None,
                        )
                        if event is None:
                            raise KeyError("Unknown measurement")
                        self.send((run.root / "measurements" / (event_id + ".json")).read_bytes())
                elif operation == "export" and not write:
                    self.send(
                        run.export(),
                        media="application/zip",
                        filename=f"chemworld-{run_id[:8]}.zip",
                    )
                else:
                    self.send({"error": "Route or method not found"}, 404)
            elif path in {"/", "/index.html", "/app.js", "/style.css", "/charts.js"} and not write:
                file = STATIC / ("index.html" if path == "/" else path[1:])
                self.send(
                    file.read_bytes(), media=mimetypes.guess_type(file.name)[0] or "text/plain"
                )
            else:
                self.send({"error": "Route not found"}, 404)
        except RequestRejected as exc:
            self.send({"error": str(exc)}, exc.status)
        except KeyError:
            self.send({"error": "Record not found"}, 404)
        except (ValueError, TypeError) as exc:
            # Validation messages contain no provider response or authorization headers.
            self.send({"error": str(exc)[:1200]}, 400)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            self.send({"error": "Local service error; saved records have been retained"}, 500)


def main() -> None:
    parser = argparse.ArgumentParser(description="ChemWorld Research Workbench (local only)")
    parser.add_argument("--port", type=int, default=8892)
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "ChemWorld-workbench")
    parser.add_argument(
        "--open", action="store_true", help="Open the local workbench in your browser"
    )
    args = parser.parse_args()
    server = WorkbenchServer(("127.0.0.1", args.port), args.data_dir)
    print(f"ChemWorld Research Workbench: http://127.0.0.1:{server.server_port}", flush=True)
    print(f"Local data: {server.store.root}", flush=True)
    if args.open:
        webbrowser.open(f"http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.store.close()
        server.server_close()
