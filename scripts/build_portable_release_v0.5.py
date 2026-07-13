"""Build a clean-wheel platform attestation and the v0.5 backend release manifest."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from chemworld.eval.composed_runtime_stress import (
    load_composed_runtime_stress_protocol,
    run_composed_runtime_stress,
)
from chemworld.eval.portable_release import (
    build_release_audit,
    canonical_sha256,
    environment_fingerprint,
    load_portable_release_protocol,
    normalized_platform,
    release_manifest,
    semantic_identity,
)

ROOT = Path(__file__).resolve().parents[1]


def replay_identity(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "profiles": {
            f"{item['task_id']}:{item['profile']}": item["trajectory_sha256"]
            for item in report["profile_runs"]
        },
        "chains": {
            task_id: item["trajectory_sha256"]
            for task_id, item in report["composed_chains"].items()
        },
    }


def clean_wheel_attestation() -> dict[str, Any]:
    protocol = load_portable_release_protocol()
    semantic = semantic_identity(protocol)
    stress_protocol = load_composed_runtime_stress_protocol()
    source_report = run_composed_runtime_stress(stress_protocol)
    with tempfile.TemporaryDirectory(prefix="chemworld-portable-") as temporary:
        temporary_path = Path(temporary)
        wheels = temporary_path / "wheels"
        target = temporary_path / "installed"
        wheels.mkdir()
        uv = shutil.which("uv")
        if uv is None:
            raise RuntimeError("uv is required for locked portable builds")
        _run([uv, "lock", "--check"], cwd=ROOT, timeout=120)
        _run([uv, "build", "--wheel", "--out-dir", str(wheels), str(ROOT)], cwd=ROOT)
        wheel_files = sorted(wheels.glob("*.whl"))
        if len(wheel_files) != 1:
            raise RuntimeError("portable build must produce exactly one wheel")
        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--target",
                str(target),
                str(wheel_files[0]),
            ],
            cwd=temporary_path,
        )
        child_code = """  # ruff: noqa: E501
import json
import sys
from pathlib import Path
import chemworld
from chemworld.eval.composed_runtime_stress import (
    load_composed_runtime_stress_protocol,
    run_composed_runtime_stress,
)
from chemworld.eval.portable_release import environment_fingerprint
report = run_composed_runtime_stress(
    load_composed_runtime_stress_protocol(), workspace=Path(sys.argv[1])
)
print(json.dumps({
    "package_path": str(Path(chemworld.__file__).resolve()),
    "environment": environment_fingerprint(),
    "report": report,
}))
"""
        environment = {
            key: value
            for key, value in os.environ.items()
            if key not in {"PYTHONHOME", "PYTHONPATH"}
        }
        environment["PYTHONPATH"] = str(target)
        completed = subprocess.run(
            [sys.executable, "-c", child_code, str(ROOT)],
            cwd=temporary_path,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=600,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"clean-wheel replay failed: {completed.stderr[-2000:]}")
        payload = json.loads(completed.stdout)
        wheel_report = payload["report"]
        wheel_import = Path(payload["package_path"]).resolve().is_relative_to(target.resolve())
        exact_replay = replay_identity(source_report) == replay_identity(wheel_report)
        passed = bool(wheel_import and exact_replay and wheel_report["controls_ready"])
        return {
            "schema_version": "chemworld-portable-platform-attestation-0.1",
            "platform_id": normalized_platform(),
            "protocol_sha256": canonical_sha256(protocol),
            "backend_semantic_sha256": semantic["sha256"],
            "dependency_lock_sha256": _sha256(ROOT / str(protocol["dependency_lock"])),
            "wheel_sha256": _sha256(wheel_files[0]),
            "clean_wheel_replay_passed": passed,
            "wheel_import": wheel_import,
            "exact_replay": exact_replay,
            "profile_run_count": len(wheel_report["profile_runs"]),
            "chain_run_count": len(wheel_report["composed_chains"]),
            "replay_identity_sha256": canonical_sha256(replay_identity(wheel_report)),
            "environment": payload.get("environment", environment_fingerprint()),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform-output",
        type=Path,
        default=Path("runs/portable_release/platform-attestation.json"),
    )
    parser.add_argument("--additional-platform-report", action="append", type=Path, default=[])
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("workstreams/world_foundation/reports/portable-release-v0.5.json"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("benchmark/releases/backend-v0.5-formal-candidate.json"),
    )
    parser.add_argument("--platform-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    attestation = clean_wheel_attestation()
    _write_json(args.platform_output, attestation)
    if args.platform_only:
        print(json.dumps(attestation, indent=2, sort_keys=True))
        return 0 if attestation["clean_wheel_replay_passed"] else 1
    attestations = [attestation]
    for path in args.additional_platform_report:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError(f"platform report is not an object: {path}")
        attestations.append(payload)
    report = build_release_audit(load_portable_release_protocol(), attestations)
    manifest = release_manifest(report)
    _write_json(args.report, report)
    _write_json(args.manifest, manifest)
    print(
        json.dumps(
            {
                "portable_release_ready": report["portable_release_ready"],
                "missing_platforms": report["missing_platforms"],
                "report": str(args.report),
                "manifest": str(args.manifest),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["portable_release_ready"] else 1


def _run(command: list[str], *, cwd: Path, timeout: int = 600) -> None:
    completed = subprocess.run(
        command, cwd=cwd, check=False, capture_output=True, text=True, timeout=timeout
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-1000:]}\n{completed.stderr[-2000:]}"
        )


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
