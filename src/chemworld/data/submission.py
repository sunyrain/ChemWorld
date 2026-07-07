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
from chemworld.data.logging import load_jsonl
from chemworld.data.validation import validate_records

SUBMISSION_SCHEMA_VERSION = "chemworld-submission-0.1"
SUBMISSION_BUNDLE_SCHEMA_VERSION = "chemworld-submission-bundle-0.1"


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


@dataclass(frozen=True)
class SubmissionBundleValidation:
    valid: bool
    path: str
    errors: list[str]
    trajectory_count: int
    result_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "path": self.path,
            "errors": self.errors,
            "trajectory_count": self.trajectory_count,
            "result_count": self.result_count,
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


def init_submission_bundle(
    path: str | Path,
    *,
    agent_name: str,
    agent_family: str,
    task_id: str,
    seeds: list[int],
    command: list[str],
    dependency_file: str,
    llm_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a local submission bundle skeleton and manifest."""

    root = Path(path)
    (root / "trajectories").mkdir(parents=True, exist_ok=True)
    (root / "results").mkdir(parents=True, exist_ok=True)
    (root / "explanations").mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": SUBMISSION_BUNDLE_SCHEMA_VERSION,
        "agent_name": agent_name,
        "agent_family": agent_family,
        "platform_version": __version__,
        "commit_hash": git_commit(),
        "dependency_file": dependency_file,
        "command": command,
        "task_id": task_id,
        "seeds": seeds,
        "llm_metadata": llm_metadata or {},
        "created_at": datetime.now(UTC).isoformat(),
    }
    with (root / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
    return manifest


def _load_bundle_manifest(root: Path, errors: list[str]) -> dict[str, Any]:
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        errors.append("missing manifest.json")
        return {}
    try:
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
    except json.JSONDecodeError as exc:
        errors.append(f"manifest.json is not valid JSON: {exc}")
        return {}
    required = {
        "schema_version",
        "agent_name",
        "agent_family",
        "platform_version",
        "commit_hash",
        "dependency_file",
        "command",
        "task_id",
        "seeds",
        "llm_metadata",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        errors.append(f"manifest.json missing keys: {missing}")
    if manifest.get("schema_version") != SUBMISSION_BUNDLE_SCHEMA_VERSION:
        errors.append("manifest.json has unsupported schema_version")
    return manifest


def validate_submission_bundle(path: str | Path) -> SubmissionBundleValidation:
    """Validate a local submission bundle structure and trajectory schemas."""

    root = Path(path)
    errors: list[str] = []
    if not root.exists():
        return SubmissionBundleValidation(False, str(root), ["bundle path does not exist"], 0, 0)
    _load_bundle_manifest(root, errors)

    trajectory_dir = root / "trajectories"
    result_dir = root / "results"
    if not trajectory_dir.exists():
        errors.append("missing trajectories directory")
        trajectory_paths: list[Path] = []
    else:
        trajectory_paths = sorted(trajectory_dir.glob("*.jsonl"))
        if not trajectory_paths:
            errors.append("trajectories directory contains no .jsonl files")
    if not result_dir.exists():
        errors.append("missing results directory")
        result_paths: list[Path] = []
    else:
        result_paths = sorted(result_dir.glob("*.json"))
        if not result_paths:
            errors.append("results directory contains no .json files")

    for trajectory_path in trajectory_paths:
        try:
            validate_records(load_jsonl(trajectory_path))
        except ValueError as exc:
            errors.append(f"{trajectory_path.name}: {exc}")

    for result_path in result_paths:
        try:
            with result_path.open("r", encoding="utf-8") as handle:
                result = json.load(handle)
        except json.JSONDecodeError as exc:
            errors.append(f"{result_path.name}: invalid JSON: {exc}")
            continue
        if "total_score" not in result:
            errors.append(f"{result_path.name}: missing total_score")

    return SubmissionBundleValidation(
        valid=not errors,
        path=str(root),
        errors=errors,
        trajectory_count=len(trajectory_paths),
        result_count=len(result_paths),
    )


def summarize_submission_bundle(path: str | Path) -> dict[str, Any]:
    """Summarize score, risk, and seed coverage for a local submission bundle."""

    from chemworld.eval.metrics import evaluate_records

    root = Path(path)
    validation = validate_submission_bundle(root)
    if not validation.valid:
        return {"valid": False, "validation": validation.to_dict()}

    trajectory_paths = sorted((root / "trajectories").glob("*.jsonl"))
    evaluations = []
    seeds: set[int] = set()
    for trajectory_path in trajectory_paths:
        records = load_jsonl(trajectory_path)
        evaluations.append(evaluate_records(records).to_dict())
        seeds.update(int(record["seed"]) for record in records)

    total_scores = [float(item["total_score"]) for item in evaluations]
    risks = [float(item["mean_safety_risk"]) for item in evaluations]
    best_scores = [float(item["final_best_score"]) for item in evaluations]
    return {
        "valid": True,
        "path": str(root),
        "trajectory_count": len(trajectory_paths),
        "result_count": validation.result_count,
        "seeds": sorted(seeds),
        "mean_total_score": sum(total_scores) / len(total_scores),
        "mean_safety_risk": sum(risks) / len(risks),
        "max_final_best_score": max(best_scores),
    }
