"""Provider smoke failures must remain diagnostic and credential-free."""

import io
import json
import urllib.error
from types import SimpleNamespace

from scripts.probe_work_ii_siliconflow_glm import codex_probe, request


def test_http_error_redacts_credentials_and_preserves_failure(monkeypatch, tmp_path):
    secret = "test-secret-never-publish"

    def rejected(req, **kwargs):
        assert req.get_header("Authorization") == f"Bearer {secret}"
        raise urllib.error.HTTPError(
            req.full_url,
            404,
            "Not Found",
            {},
            io.BytesIO(json.dumps({"error": {"message": f"upstream echo {secret}"}}).encode()),
        )

    monkeypatch.setattr("urllib.request.urlopen", rejected)
    artifact = tmp_path / "failed.json"
    result, payload = request(secret, "/responses", {"input": "test"}, artifact)
    assert result["http_status"] == 404
    assert result["attempts"] == 1
    assert payload["error"]["message"].endswith("[REDACTED]")
    assert secret not in artifact.read_text(encoding="utf-8")
    assert secret not in json.dumps(result)


def test_codex_404_is_not_a_successful_harness_and_secret_is_env_only(monkeypatch, tmp_path):
    secret = "test-secret-never-publish"

    def start(command, **kwargs):
        assert secret not in " ".join(command)
        assert kwargs["env"]["SILICONFLOW_API_KEY"] == secret
        assert "--output-schema" in command
        stdout = json.dumps({"type": "turn.failed", "error": {"message": f"404 {secret}"}})
        return SimpleNamespace(returncode=1, communicate=lambda *_a, **_kw: (stdout, secret))

    monkeypatch.setattr("subprocess.Popen", start)
    result = codex_probe(secret, "zai-org/GLM-5.3", tmp_path)
    assert result["exit_code"] == 1
    assert result["codex_turn_completed"] is False
    assert result["continuation_tested"] is False
    assert result["tool_attempts"] == 0
    assert result["usage"] == []
    for path in tmp_path.rglob("*"):
        if path.is_file():
            assert secret not in path.read_text(encoding="utf-8")
