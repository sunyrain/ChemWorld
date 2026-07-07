"""Submission manifest helpers for reproducible benchmark artifacts."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

from chemworld import __version__

SUBMISSION_SCHEMA_VERSION = "chemworld-submission-0.1"


@dataclass(frozen=True)
class SubmissionManifest:
    schema_version: str
    chemworld_version: str
    trajectory_path: str
    agent_manifest: dict[str, Any]
    command: list[str]
    dependency_versions: dict[str, str]
    platform: dict[str, str]
    source_digest: str | None
    created_at: str
    notes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "chemworld_version": self.chemworld_version,
            "trajectory_path": self.trajectory_path,
            "agent_manifest": self.agent_manifest,
            "command": self.command,
            "dependency_versions": self.dependency_versions,
            "platform": self.platform,
            "source_digest": self.source_digest,
            "created_at": self.created_at,
            "notes": self.notes,
        }


def installed_versions(packages: list[str] | None = None) -> dict[str, str]:
    packages = packages or [
        "chemworld-bench",
        "gymnasium",
        "numpy",
        "pandas",
        "scikit-learn",
    ]
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def current_platform() -> dict[str, str]:
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
    }


def git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def source_digest(root: str | Path | None = None) -> str | None:
    """Compute a deterministic digest for source files when git metadata is absent."""

    if root is None:
        root = Path(__file__).resolve().parents[3]
    root_path = Path(root)
    if not root_path.exists():
        return None

    hasher = hashlib.sha256()
    source_roots = [root_path / "src", root_path / "tests", root_path / "docs"]
    extra_files = [root_path / "pyproject.toml", root_path / "README.md", root_path / "mkdocs.yml"]
    paths: list[Path] = []
    for source_root in source_roots:
        if source_root.exists():
            paths.extend(path for path in source_root.rglob("*") if path.is_file())
    paths.extend(path for path in extra_files if path.exists())

    for path in sorted(paths):
        relative = path.relative_to(root_path).as_posix()
        hasher.update(relative.encode())
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def build_submission_manifest(
    *,
    trajectory_path: str | Path,
    agent_manifest: dict[str, Any],
    command: list[str],
    notes: dict[str, Any] | None = None,
) -> SubmissionManifest:
    enriched_agent_manifest = dict(agent_manifest)
    enriched_agent_manifest.setdefault("git_commit", git_commit())
    return SubmissionManifest(
        schema_version=SUBMISSION_SCHEMA_VERSION,
        chemworld_version=__version__,
        trajectory_path=str(trajectory_path),
        agent_manifest=enriched_agent_manifest,
        command=command,
        dependency_versions=installed_versions(),
        platform=current_platform(),
        source_digest=source_digest(),
        created_at=datetime.now(UTC).isoformat(),
        notes=notes or {},
    )


def write_submission_manifest(
    *,
    path: str | Path,
    trajectory_path: str | Path,
    agent_manifest: dict[str, Any],
    command: list[str],
    notes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = build_submission_manifest(
        trajectory_path=trajectory_path,
        agent_manifest=agent_manifest,
        command=command,
        notes=notes,
    ).to_dict()
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
    return manifest
