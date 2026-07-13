"""Run the v0.5 composed runtime stress matrix and write its control report."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from chemworld.eval.composed_runtime_stress import (
    load_composed_runtime_stress_protocol,
    run_composed_runtime_stress,
)

ROOT = Path(__file__).resolve().parents[1]


def _replay_identity(report: dict[str, object]) -> dict[str, object]:
    profiles = report["profile_runs"]
    chains = report["composed_chains"]
    assert isinstance(profiles, list)
    assert isinstance(chains, dict)
    return {
        "profiles": {
            f"{item['task_id']}:{item['profile']}": item["trajectory_sha256"]
            for item in profiles
            if isinstance(item, dict)
        },
        "chains": {
            task_id: item["trajectory_sha256"]
            for task_id, item in chains.items()
            if isinstance(item, dict)
        },
    }


def _clean_wheel_replay(source_report: dict[str, object]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="chemworld-composed-wheel-") as temporary:
        temporary_path = Path(temporary)
        wheels = temporary_path / "wheels"
        target = temporary_path / "installed"
        wheels.mkdir()
        uv = shutil.which("uv")
        build_command = (
            [uv, "build", "--wheel", "--out-dir", str(wheels), str(ROOT)]
            if uv
            else [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-build-isolation",
                "--no-deps",
                "--wheel-dir",
                str(wheels),
                str(ROOT),
            ]
        )
        build = subprocess.run(
            build_command,
            cwd=temporary_path,
            check=False,
            capture_output=True,
            text=True,
            timeout=240,
        )
        wheel_files = sorted(wheels.glob("*.whl"))
        if build.returncode != 0 or len(wheel_files) != 1:
            return {"passed": False, "stage": "build", "returncode": build.returncode}
        install = subprocess.run(
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
            check=False,
            capture_output=True,
            text=True,
            timeout=240,
        )
        if install.returncode != 0:
            return {"passed": False, "stage": "install", "returncode": install.returncode}
        child_code = """
import json
import sys
from pathlib import Path
import chemworld
from chemworld.eval.composed_runtime_stress import (
    load_composed_runtime_stress_protocol,
    run_composed_runtime_stress,
)
report = run_composed_runtime_stress(
    load_composed_runtime_stress_protocol(), workspace=Path(sys.argv[1])
)
print(json.dumps({"package_path": str(Path(chemworld.__file__).resolve()), "report": report}))
"""
        environment = {
            key: value
            for key, value in os.environ.items()
            if key not in {"PYTHONHOME", "PYTHONPATH"}
        }
        environment["PYTHONPATH"] = str(target)
        child = subprocess.run(
            [sys.executable, "-c", child_code, str(ROOT)],
            cwd=temporary_path,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if child.returncode != 0:
            return {"passed": False, "stage": "execute", "returncode": child.returncode}
        try:
            payload = json.loads(child.stdout)
        except json.JSONDecodeError:
            return {"passed": False, "stage": "decode", "returncode": child.returncode}
        wheel_report = payload.get("report")
        package_path = Path(str(payload.get("package_path", ""))).resolve()
        if not isinstance(wheel_report, dict):
            return {"passed": False, "stage": "shape", "returncode": child.returncode}
        exact = _replay_identity(source_report) == _replay_identity(wheel_report)
        wheel_import = package_path.is_relative_to(target.resolve())
        return {
            "passed": exact and wheel_import and wheel_report.get("controls_ready") is True,
            "stage": "complete",
            "separate_process": True,
            "wheel_import": wheel_import,
            "exact_replay": exact,
            "platform": sys.platform,
            "profile_run_count": len(wheel_report.get("profile_runs", ())),
            "source_protocol_sha256": source_report.get("protocol_sha256"),
            "wheel_protocol_sha256": wheel_report.get("protocol_sha256"),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/world_foundation/reports/composed-runtime-stress-v0.5.json"),
    )
    args = parser.parse_args()
    report = run_composed_runtime_stress(load_composed_runtime_stress_protocol())
    clean_wheel = _clean_wheel_replay(report)
    report["clean_wheel_replay"] = clean_wheel
    controls = report["controls"]
    assert isinstance(controls, dict)
    controls["clean_wheel_cross_process_replay_exact"] = clean_wheel["passed"] is True
    report["controls_ready"] = all(controls.values())
    report["status"] = (
        "composed_runtime_stress_passed"
        if report["controls_ready"]
        else "composed_runtime_stress_failed"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "coverage": report["coverage"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
