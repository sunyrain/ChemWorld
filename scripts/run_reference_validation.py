"""Require and run ChemWorld's external physical-chemistry reference checks."""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys

REFERENCE_MODULES = ("cantera", "chemicals", "fluids", "thermo")


def probe_reference_modules() -> dict[str, str]:
    """Return modules that cannot be imported, with an actionable reason."""

    failures: dict[str, str] = {}
    for name in REFERENCE_MODULES:
        try:
            importlib.import_module(name)
        except Exception as exc:  # pragma: no cover - exercised in missing-dep installs
            failures[name] = f"{type(exc).__name__}: {exc}"
    return failures


def main() -> int:
    unavailable = probe_reference_modules()
    if unavailable:
        print(
            json.dumps(
                {
                    "reference_validation": "missing_dependencies",
                    "unavailable": unavailable,
                    "install": 'python -m pip install -e ".[dev,physchem-ref]"',
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    env = os.environ.copy()
    env["CHEMWORLD_RUN_REFERENCE_TESTS"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/reference", "-q", "--no-cov"],
        env=env,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
