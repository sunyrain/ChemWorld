"""Check actual read-only routes and licensed model loading without an experiment engine."""

import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from apps.asset_preview.assets import glb_document
from apps.asset_preview.server import DEMO, make_server, resolve_file


def test_preview_route_is_read_only_and_returns_existing_public_record(tmp_path):
    (tmp_path / "index.json").write_text('{"instruments": []}', encoding="utf-8")
    server = make_server(tmp_path, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base + "/api/demo", timeout=3) as response:
            assert json.load(response) == json.loads(DEMO.read_text(encoding="utf-8"))
        for path in ("/", "/app.mjs", "/vendor/loaders/GLTFLoader.js"):
            with urlopen(base + path, timeout=3) as response:
                assert response.status == 200
        with pytest.raises(HTTPError) as error:
            urlopen(Request(base + "/api/demo", data=b"{}"), timeout=3)
        assert error.value.code == 501
        with pytest.raises(HTTPError) as error:
            urlopen(Request(base + "/api/demo", headers={"Host": "external.example"}), timeout=3)
        assert error.value.code == 403
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


@pytest.mark.parametrize(
    "path",
    [
        "/../server.py",
        "/vendor/../../server.py",
        "/data/../index.json",
        "/data/metrohm_914/../../index.json",
        "/licenses/../index.json",
        "/%2e%2e/server.py",
    ],
)
def test_preview_does_not_serve_arbitrary_workspace_files(path, tmp_path):
    assert resolve_file(path, tmp_path) is None


def test_corrupt_geometry_is_not_registered_as_a_download():
    with pytest.raises(ValueError):
        glb_document(b"not a model")
