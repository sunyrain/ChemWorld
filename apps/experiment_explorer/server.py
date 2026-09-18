"""Loopback-only HTTP service for existing evidence; no provider access or file writes."""

from __future__ import annotations

import argparse
import json
import math
import mimetypes
import threading
import time
import uuid
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .catalog import Catalog

STATIC = Path(__file__).with_name("static")


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return value


class VerificationJobs:
    def __init__(self, catalog):
        self.catalog = catalog
        self.lock = threading.Lock()
        self.jobs = {}
        self.busy = False

    def start(self, file_id):
        with self.lock:
            if self.busy:
                raise ValueError("A replay verification is already running")
            if file_id not in self.catalog.files:
                raise KeyError(file_id)
            self.busy = True
            job_id = uuid.uuid4().hex
            self.jobs[job_id] = {
                "id": job_id,
                "file_id": file_id,
                "status": "running",
                "started": time.time(),
            }
        threading.Thread(target=self._run, args=(job_id, file_id), daemon=True).start()
        return {"id": job_id}

    def _run(self, job_id, file_id):
        try:
            from chemworld.eval.verify import verify_records

            payload = self.catalog.trajectory(file_id)
            if payload["errors"]:
                raise ValueError("Incomplete or corrupt file: verification requires all records")
            # Exact replay uses the native verifier and recorded contract. A stale
            # runtime or missing private intervention remains a visible failure.
            result = verify_records(payload["records"], tolerance=0.0).to_dict()
            update = {"status": "done", "result": result}
        except Exception as exc:
            update = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
        with self.lock:
            self.jobs[job_id].update(update, elapsed_s=time.time() - self.jobs[job_id]["started"])
            self.busy = False

    def get(self, job_id):
        with self.lock:
            job = dict(self.jobs[job_id])
        if job["status"] == "running":
            job["elapsed_s"] = time.time() - job["started"]
        return job


def make_server(catalog: Catalog, port: int = 8890) -> ThreadingHTTPServer:
    jobs = VerificationJobs(catalog)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            if args and str(args[1] if len(args) > 1 else "") not in {"200", "304"}:
                super().log_message(fmt, *args)

        def local_request(self):
            host = self.headers.get("Host", "")
            allowed = {
                f"127.0.0.1:{self.server.server_port}",
                f"localhost:{self.server.server_port}",
            }
            origin = self.headers.get("Origin")
            return host in allowed and (not origin or origin in {f"http://{h}" for h in allowed})

        def respond(self, payload, status=200, content_type="application/json; charset=utf-8"):
            body = (
                json.dumps(json_safe(payload), ensure_ascii=False, allow_nan=False).encode()
                if content_type.startswith("application/json")
                else payload
            )
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; "
                "style-src 'self'; script-src 'self'; img-src 'self' data:; "
                "connect-src 'self'; object-src 'none'; frame-ancestors 'none'",
            )
            self.end_headers()
            with suppress(BrokenPipeError, ConnectionResetError):
                self.wfile.write(body)

        def do_GET(self):
            if not self.local_request():
                self.respond({"error": "Local same-origin access required"}, 403)
                return
            url = urlsplit(self.path)
            query = parse_qs(url.query)
            try:
                if url.path == "/api/catalog":
                    self.respond(catalog.snapshot())
                elif url.path == "/api/experiment":
                    self.respond(catalog.detail(query["id"][0]))
                elif url.path == "/api/trajectory":
                    self.respond(catalog.trajectory(query["id"][0]))
                elif url.path == "/api/recordings":
                    self.respond(catalog.recording_summaries(query.get("id", [])))
                elif url.path == "/api/verification":
                    self.respond(jobs.get(query["id"][0]))
                elif url.path in {
                    "/",
                    "/index.html",
                    "/styles.css",
                    "/app.mjs",
                    "/replay.mjs",
                    "/viewer.mjs",
                    "/viewer.css",
                }:
                    path = STATIC / ("index.html" if url.path == "/" else url.path[1:])
                    mime = (
                        "text/javascript"
                        if path.suffix == ".mjs"
                        else (mimetypes.guess_type(path.name)[0] or "text/plain")
                    )
                    self.respond(path.read_bytes(), content_type=mime + "; charset=utf-8")
                else:
                    self.respond({"error": "Not found"}, 404)
            except (KeyError, FileNotFoundError):
                self.respond({"error": "Local record not found; refresh the catalogue"}, 404)
            except (ValueError, OSError) as exc:
                self.respond({"error": str(exc)}, 422)

        def do_POST(self):
            if not self.local_request():
                self.respond({"error": "Local same-origin access required"}, 403)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > 4096:
                    raise ValueError("Invalid request size")
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise ValueError("Expected a JSON object")
                if self.path == "/api/refresh":
                    self.respond(catalog.refresh())
                elif self.path == "/api/verify":
                    self.respond(jobs.start(body["id"]), 202)
                else:
                    self.respond({"error": "Not found"}, 404)
            except KeyError:
                self.respond({"error": "Unknown trajectory"}, 404)
            except (ValueError, OSError) as exc:
                self.respond({"error": str(exc)}, 422)

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--runs", type=Path, action="append", help="Additional local archive directory (repeatable)"
    )
    args = parser.parse_args()
    roots = [args.root / "runs", *(args.runs or [])]
    catalog = Catalog(args.root, roots)
    print("Indexing existing reports and local trajectory paths...", flush=True)
    snapshot = catalog.refresh()
    server = make_server(catalog, args.port)
    print(f"Indexed {snapshot['counts']}. Open http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
