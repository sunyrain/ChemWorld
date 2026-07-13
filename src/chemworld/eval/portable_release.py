"""Build and validate the portable identity of the v0.5 backend candidate."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import platform
import subprocess
import sys
from collections.abc import Mapping, Sequence
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "foundation" / "portable_release_v0.5.json"
PROTOCOL_VERSION = "chemworld-portable-release-protocol-0.1"


class PortableReleaseError(RuntimeError):
    """Raised when portable release inputs are unsafe or internally inconsistent."""


def load_portable_release_protocol(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != PROTOCOL_VERSION:
        raise PortableReleaseError("unsupported portable release protocol")
    return payload


def file_manifest(
    workspace: Path, patterns: Sequence[str], *, excludes: Sequence[str] = ()
) -> dict[str, str]:
    """Return a stable, traversal-safe digest manifest for matching regular files."""
    root = workspace.resolve()
    excluded: set[Path] = set()
    for pattern in excludes:
        _validate_pattern(pattern)
        excluded.update(path.resolve() for path in root.glob(pattern) if path.is_file())
    files: set[Path] = set()
    for pattern in patterns:
        _validate_pattern(pattern)
        for path in root.glob(pattern):
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                raise PortableReleaseError(f"matched path escapes workspace: {path}")
            if resolved.is_file() and resolved not in excluded:
                files.add(resolved)
    if not files:
        raise PortableReleaseError("digest manifest is empty")
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(files)
    }


def semantic_identity(protocol: Mapping[str, Any], workspace: Path = ROOT) -> dict[str, Any]:
    files = file_manifest(
        workspace,
        _string_sequence(protocol, "semantic_sources"),
        excludes=_string_sequence(protocol, "semantic_excludes"),
    )
    return {
        "sha256": canonical_sha256(files),
        "file_count": len(files),
        "files": files,
    }


def documentation_identity(
    protocol: Mapping[str, Any], workspace: Path = ROOT
) -> dict[str, Any]:
    files = file_manifest(workspace, _string_sequence(protocol, "documentation_sources"))
    return {
        "sha256": canonical_sha256(files),
        "file_count": len(files),
        "files": files,
    }


def environment_fingerprint() -> dict[str, Any]:
    """Record runtime, numerical libraries, compute devices, and solver versions."""
    blas_output = io.StringIO()
    with contextlib.redirect_stdout(blas_output):
        np.show_config()
    packages = {
        name: _package_version(name)
        for name in (
            "chemworld-bench",
            "gymnasium",
            "numpy",
            "pandas",
            "scipy",
            "scikit-learn",
            "torch",
            "stable-baselines3",
        )
    }
    torch_info: dict[str, Any] = {"available": False}
    try:
        import torch

        torch_info = {
            "available": True,
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
            "device_count": torch.cuda.device_count(),
            "devices": [
                torch.cuda.get_device_name(index)
                for index in range(torch.cuda.device_count())
            ],
        }
    except ImportError:
        pass
    return {
        "platform_key": normalized_platform(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": sys.version,
        "python_implementation": platform.python_implementation(),
        "logical_cpu_count": os.cpu_count(),
        "packages": packages,
        "numpy_blas_configuration": blas_output.getvalue().strip(),
        "torch": torch_info,
    }


def evidence_inventory(
    protocol: Mapping[str, Any], workspace: Path = ROOT
) -> dict[str, dict[str, Any]]:
    evidence = protocol.get("required_evidence")
    flags = protocol.get("required_evidence_flags")
    if not isinstance(evidence, Mapping) or not isinstance(flags, Mapping):
        raise PortableReleaseError("required evidence mappings are missing")
    result: dict[str, dict[str, Any]] = {}
    for name, raw_path in evidence.items():
        if not isinstance(name, str) or not isinstance(raw_path, str):
            raise PortableReleaseError("evidence entries must map strings to paths")
        path = resolve_workspace_path(workspace, raw_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        flag = flags.get(name)
        if not isinstance(payload, dict) or not isinstance(flag, str):
            raise PortableReleaseError(f"invalid evidence contract: {name}")
        result[name] = {
            "path": path.relative_to(workspace.resolve()).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "schema_version": payload.get("schema_version"),
            "required_flag": flag,
            "required_flag_value": payload.get(flag),
            "passed": payload.get(flag) is True,
        }
    return result


def validate_platform_attestation(
    payload: Mapping[str, Any], *, semantic_sha256: str, protocol_sha256: str
) -> list[str]:
    failures: list[str] = []
    if payload.get("schema_version") != "chemworld-portable-platform-attestation-0.1":
        failures.append("unsupported platform attestation schema")
    if payload.get("backend_semantic_sha256") != semantic_sha256:
        failures.append("platform attestation binds a different backend semantic hash")
    if payload.get("protocol_sha256") != protocol_sha256:
        failures.append("platform attestation binds a different protocol hash")
    if payload.get("clean_wheel_replay_passed") is not True:
        failures.append("clean-wheel replay did not pass")
    if payload.get("exact_replay") is not True:
        failures.append("golden replay was not exact")
    environment = payload.get("environment")
    if not isinstance(environment, Mapping) or environment.get("platform_key") not in {
        "linux",
        "windows",
    }:
        failures.append("platform key is missing or unsupported")
    return failures


def build_release_audit(
    protocol: Mapping[str, Any],
    platform_attestations: Sequence[Mapping[str, Any]],
    *,
    workspace: Path = ROOT,
) -> dict[str, Any]:
    semantic = semantic_identity(protocol, workspace)
    documentation = documentation_identity(protocol, workspace)
    evidence = evidence_inventory(protocol, workspace)
    protocol_sha256 = canonical_sha256(protocol)
    attestations: dict[str, dict[str, Any]] = {}
    attestation_failures: list[str] = []
    for payload in platform_attestations:
        failures = validate_platform_attestation(
            payload,
            semantic_sha256=str(semantic["sha256"]),
            protocol_sha256=protocol_sha256,
        )
        environment = payload.get("environment")
        platform_key = (
            str(environment.get("platform_key"))
            if isinstance(environment, Mapping)
            else "unknown"
        )
        if platform_key in attestations:
            failures.append(f"duplicate platform attestation: {platform_key}")
        attestations[platform_key] = dict(payload)
        attestation_failures.extend(f"{platform_key}: {failure}" for failure in failures)
    required_platforms = set(_string_sequence(protocol, "required_platforms"))
    observed_platforms = set(attestations)
    missing_platforms = sorted(required_platforms - observed_platforms)
    lock_path = resolve_workspace_path(workspace, str(protocol["dependency_lock"]))
    controls = {
        "protocol_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False,
        "semantic_manifest_is_nonempty": int(semantic["file_count"]) > 0,
        "documentation_identity_is_separate": not set(semantic["files"]).intersection(
            documentation["files"]
        ),
        "required_evidence_passes": all(item["passed"] for item in evidence.values()),
        "dependency_lock_present": lock_path.is_file(),
        "platform_attestations_valid": not attestation_failures,
        "required_platforms_complete": not missing_platforms,
    }
    ready = all(controls.values())
    commit, dirty = git_provenance(workspace)
    return {
        "schema_version": "chemworld-portable-release-report-0.1",
        "protocol_id": protocol["protocol_id"],
        "backend_id": protocol["backend_id"],
        "status": "portable_release_passed" if ready else "portable_release_blocked",
        "portable_release_ready": ready,
        "benchmark_claim_allowed": False,
        "source_commit": commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": protocol_sha256,
        "backend_semantic_identity": semantic,
        "documentation_identity": documentation,
        "dependency_lock": {
            "path": lock_path.relative_to(workspace.resolve()).as_posix(),
            "sha256": hashlib.sha256(lock_path.read_bytes()).hexdigest(),
        },
        "evidence": evidence,
        "platform_attestations": attestations,
        "missing_platforms": missing_platforms,
        "attestation_failures": attestation_failures,
        "controls": controls,
        "limitations": [
            "This identifies a synthetic backend candidate, not real-chemistry validity.",
            "Documentation and website changes are intentionally outside the backend hash.",
            "Formal algorithm rankings remain prohibited until later protocols are frozen.",
        ],
    }


def release_manifest(report: Mapping[str, Any]) -> dict[str, Any]:
    """Create the sole machine-readable backend candidate identity."""
    return {
        "schema_version": "chemworld-backend-release-manifest-0.1",
        "backend_id": report["backend_id"],
        "release_status": (
            "formal_candidate" if report["portable_release_ready"] else "blocked_candidate"
        ),
        "backend_semantic_sha256": report["backend_semantic_identity"]["sha256"],
        "documentation_sha256": report["documentation_identity"]["sha256"],
        "dependency_lock_sha256": report["dependency_lock"]["sha256"],
        "portable_release_report_sha256": canonical_sha256(report),
        "source_commit": report["source_commit"],
        "required_platforms": sorted(report["platform_attestations"]),
        "missing_platforms": report["missing_platforms"],
        "portable_release_ready": report["portable_release_ready"],
        "benchmark_claim_allowed": False,
    }


def normalized_platform() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    return system or "unknown"


def resolve_workspace_path(workspace: Path, raw_path: str) -> Path:
    path = (workspace / raw_path).resolve()
    root = workspace.resolve()
    if not path.is_relative_to(root):
        raise PortableReleaseError(f"path escapes workspace: {raw_path}")
    if not path.is_file():
        raise PortableReleaseError(f"required file is missing: {raw_path}")
    return path


def canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None, None
    return commit, bool(status)


def _validate_pattern(pattern: str) -> None:
    candidate = Path(pattern)
    if (
        candidate.is_absolute()
        or bool(candidate.drive)
        or pattern.startswith(("/", "\\"))
        or ".." in candidate.parts
    ):
        raise PortableReleaseError(f"unsafe file pattern: {pattern}")


def _string_sequence(payload: Mapping[str, Any], key: str) -> tuple[str, ...]:
    raw = payload.get(key)
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise PortableReleaseError(f"{key} must be a string sequence")
    values = tuple(raw)
    if not values or not all(isinstance(value, str) for value in values):
        raise PortableReleaseError(f"{key} must contain strings")
    return values


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


__all__ = [
    "PortableReleaseError",
    "build_release_audit",
    "canonical_sha256",
    "documentation_identity",
    "environment_fingerprint",
    "file_manifest",
    "load_portable_release_protocol",
    "normalized_platform",
    "release_manifest",
    "semantic_identity",
    "validate_platform_attestation",
]
