"""Read-only localhost presentation routes; never import or execute experiment engines."""

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .assets import INSTRUMENTS, ROOT

STATIC = Path(__file__).parent / "static"
VENDOR = ROOT / "apps/blender_lab/static/vendor"
DEMO = ROOT / "apps/blender_lab/static/demo.json"
SLUGS = {item["slug"] for item in INSTRUMENTS}


def resolve_file(path: str, cache: Path) -> Path | None:
    """Serve just the preview, selected assets, licenses and existing renderer modules."""
    path = unquote(path)
    if path.startswith("/vendor/"):
        base, relative = VENDOR, path.removeprefix("/vendor/")
    elif path.startswith("/data/"):
        relative = path.removeprefix("/data/")
        parts = relative.split("/")
        if len(parts) != 2 or parts[0] not in SLUGS or parts[1] not in {"bundle.json", "model.glb"}:
            return None
        base = cache
    elif path.startswith("/licenses/"):
        relative = path.removeprefix("/licenses/")
        if relative not in {"LICENSE", "LICENSE-ASSETS.md", "NOTICE.md", "CITATION.cff"}:
            return None
        base = cache
    else:
        base, relative = STATIC, "index.html" if path == "/" else path.lstrip("/")
    base = base.resolve()
    file = (base / relative).resolve()
    return file if file.is_relative_to(base) and file.is_file() else None


def make_server(cache: Path, port: int = 8895) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if urlsplit("//" + self.headers.get("Host", "")).hostname not in {
                "127.0.0.1",
                "localhost",
            }:
                self.send_error(403, "Local host only")
                return
            path = urlsplit(self.path).path
            file: Path | None
            if path == "/api/catalog":
                file = cache / "index.json"
            elif path == "/api/demo":
                file = DEMO
            else:
                file = resolve_file(path, cache)
            if file is None or not file.is_file():
                self.send_error(404, "Not found; download the optional assets first")
                return
            body = file.read_bytes()
            mime = {
                ".mjs": "text/javascript",
                ".js": "text/javascript",
                ".glb": "model/gltf-binary",
            }.get(file.suffix, mimetypes.guess_type(file.name)[0] or "text/plain")
            self.send_response(200)
            self.send_header(
                "Content-Type", mime + ("; charset=utf-8" if mime.startswith("text/") else "")
            )
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-cache")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; "
                "img-src 'self' blob: data:; connect-src 'self'; worker-src 'self' blob:; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(body)

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def serve(cache: Path, port: int) -> None:
    index = cache / "index.json"
    if not index.is_file():
        raise SystemExit(
            "Assets missing. Run: uv run --no-sync python -m apps.asset_preview --download"
        )
    info = json.loads(index.read_text(encoding="utf-8"))
    server = make_server(cache, port)
    print(f"ChemWorld asset preview: http://127.0.0.1:{server.server_port}/", flush=True)
    print(f"{len(info['instruments'])} local assets; read-only; Ctrl+C to stop", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
