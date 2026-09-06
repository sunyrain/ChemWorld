import json
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from chemworld.providers.responses_header_transport import standard_headers_transport


@pytest.mark.parametrize("status", [200, 503])
def test_body_stream_error_and_auth_are_preserved_without_codex_headers(tmp_path, status):
    captured = []
    body = b'{"model":"fixture","reasoning":{"effort":"none"},"stream":true}'
    response_body = b'event: response.completed\ndata: {"type":"response.completed"}\n\n'

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            captured.append(
                (self.path, self.rfile.read(int(self.headers["Content-Length"])), self.headers)
            )
            self.send_response(status)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.write(response_body)

        def log_message(self, *_args):
            pass

    upstream = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=upstream.serve_forever, daemon=True)
    worker.start()
    audit = tmp_path / "transport.jsonl"
    try:
        with standard_headers_transport(
            f"http://127.0.0.1:{upstream.server_port}", audit, 10
        ) as base:
            request = urllib.request.Request(
                base + "responses",
                data=body,
                headers={
                    "Authorization": "Bearer local-fixture-only",
                    "Content-Type": "application/json",
                    "User-Agent": "codex-fixture",
                    "Originator": "codex-fixture",
                    "X-Codex-Turn-Metadata": "{}",
                },
            )
            try:
                response = urllib.request.urlopen(request, timeout=10)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                assert response.status == status
                assert response.read() == response_body
    finally:
        upstream.shutdown()
        upstream.server_close()
        worker.join(2)
    assert len(captured) == 1
    path, actual_body, headers = captured[0]
    assert path == "/responses" and actual_body == body
    assert headers["Authorization"] == "Bearer local-fixture-only"
    assert headers["User-Agent"] == "ChemWorld/0.2"
    assert "Originator" not in headers and "X-Codex-Turn-Metadata" not in headers
    rows = [json.loads(line) for line in audit.read_text().splitlines()]
    assert [r["event"] for r in rows] == ["started", "finished"]
    assert rows[0]["reasoning"] == {"effort": "none"}
    assert rows[1]["http_status"] == status


def test_context_exit_closes_a_stalled_upstream_without_retry(tmp_path):
    disconnected = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.flush()
            if self.connection.recv(1) == b"":
                disconnected.set()

        def log_message(self, *_args):
            pass

    upstream = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    upstream.daemon_threads = True
    worker = threading.Thread(target=upstream.serve_forever, daemon=True)
    worker.start()
    try:
        with standard_headers_transport(
            f"http://127.0.0.1:{upstream.server_port}", tmp_path / "transport.jsonl", 60
        ) as base:
            response = urllib.request.urlopen(
                urllib.request.Request(base + "responses", data=b"{}"), timeout=5
            )
            started = time.monotonic()
        assert time.monotonic() - started < 2
        assert disconnected.wait(2)
        response.close()
    finally:
        upstream.shutdown()
        upstream.server_close()
        worker.join(2)
