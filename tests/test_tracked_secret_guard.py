from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_tracked_secrets.py"


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)


def _run_guard(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        check=False,
        text=True,
    )


def _repository(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    root.mkdir()
    _git(root, "init", "--quiet")
    (root / "README.md").write_text("safe fixture\n", encoding="utf-8")
    (root / ".env.example").write_text("TOKEN=replace-me\n", encoding="utf-8")
    _git(root, "add", "README.md", ".env.example")
    return root


def test_guard_accepts_safe_tracked_content_and_env_template(tmp_path: Path) -> None:
    completed = _run_guard(_repository(tmp_path))

    assert completed.returncode == 0
    assert completed.stdout.strip() == "tracked-secret guard passed"


def test_repository_git_managed_surface_has_no_secret_findings() -> None:
    root = SCRIPT.parents[1]

    completed = _run_guard(root)

    assert completed.returncode == 0, completed.stdout


def test_guard_rejects_forbidden_tracked_path_without_printing_content(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    secret = "value-that-must-not-be-printed"
    (root / "api.md").write_text(secret, encoding="utf-8")
    _git(root, "add", "api.md")

    completed = _run_guard(root)

    assert completed.returncode == 1
    assert "api.md" in completed.stdout
    assert secret not in completed.stdout


def test_guard_rejects_credential_fingerprint_without_printing_value(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    secret = "-----BEGIN " + "PRIVATE KEY-----"
    (root / "settings.txt").write_text(secret, encoding="utf-8")
    _git(root, "add", "settings.txt")

    completed = _run_guard(root)

    assert completed.returncode == 1
    assert "settings.txt" in completed.stdout
    assert "private-key block" in completed.stdout
    assert secret not in completed.stdout
