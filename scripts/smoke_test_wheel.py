"""Build and exercise ChemWorld from a non-editable wheel installation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="chemworld-wheel-smoke-") as temporary:
        workspace = Path(temporary)
        wheel_dir = workspace / "wheel"
        install_dir = workspace / "install"
        wheel_dir.mkdir()
        install_dir.mkdir()

        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                str(repository_root),
                "--no-deps",
                "--wheel-dir",
                str(wheel_dir),
            ],
            cwd=workspace,
        )
        wheels = sorted(wheel_dir.glob("chemworld_bench-*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"Expected exactly one ChemWorld wheel, found {wheels}")
        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--target",
                str(install_dir),
                str(wheels[0]),
            ],
            cwd=workspace,
        )

        smoke = (
            "import json, pathlib, chemworld, gymnasium as gym; "
            "from chemworld.task_design import serious_task_readiness_manifest; "
            "from chemworld.eval.benchmark_validation import official_validation_path; "
            "env=gym.make('ChemWorld', task_id='reaction-to-assay', seed=0); "
            "obs,info=env.reset(seed=0); "
            "readiness=serious_task_readiness_manifest(); "
            "print(json.dumps({'package': chemworld.__file__, "
            "'task_id': info['task_id'], 'observation_keys': sorted(obs), "
            "'serious_suite_status': readiness['suite_status'], "
            "'benchmark_ready_count': readiness['benchmark_ready_count'], "
            "'official_validation_path': str(official_validation_path())})); "
            "env.close()"
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(install_dir)
        completed = subprocess.run(
            [sys.executable, "-c", smoke],
            cwd=workspace,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout.strip().splitlines()[-1])
        imported_path = Path(str(payload["package"])).resolve()
        if not imported_path.is_relative_to(install_dir.resolve()):
            raise RuntimeError(f"Smoke imported editable source instead of wheel: {imported_path}")
        if payload["task_id"] != "reaction-to-assay":
            raise RuntimeError(f"Unexpected wheel smoke task payload: {payload}")
        if payload["serious_suite_status"] != "validated":
            raise RuntimeError(f"Wheel does not carry validated benchmark evidence: {payload}")
        if payload["benchmark_ready_count"] != 6:
            raise RuntimeError(f"Wheel benchmark evidence is incomplete: {payload}")
        validation_path = Path(str(payload["official_validation_path"])).resolve()
        if not validation_path.is_relative_to(install_dir.resolve()):
            raise RuntimeError(f"Wheel used validation outside installed resources: {payload}")
        print(json.dumps({"wheel_smoke": "passed", **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
