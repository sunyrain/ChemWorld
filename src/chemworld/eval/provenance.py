"""Solver and provenance manifests for paper artifacts."""

from __future__ import annotations

import platform
import sys
from datetime import UTC, datetime
from importlib import metadata
from typing import Any

from chemworld import __version__
from chemworld.data.submission import git_commit
from chemworld.eval.seed_suite import private_eval_salt_policy
from chemworld.tasks import get_task

PROVENANCE_SCHEMA_VERSION = "chemworld-solver-provenance-0.1"


def build_solver_provenance_manifest(
    *,
    task_ids: list[str],
    agents: list[str],
    seeds: list[int],
) -> dict[str, Any]:
    """Return a JSON-friendly manifest for reproducible benchmark artifacts."""

    return {
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "created_at": datetime.now(UTC).isoformat(),
        "chemworld_version": __version__,
        "commit_hash": git_commit(),
        "python": {
            "version": sys.version,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "dependencies": {
            package: _version_or_unavailable(package)
            for package in (
                "gymnasium",
                "numpy",
                "pandas",
                "scipy",
                "scikit-learn",
                "pytest",
                "mkdocs",
            )
        },
        "solver_tolerances": {
            "trajectory_verify_default_tolerance": 1.0e-5,
            "ode_solver": "scipy.integrate.solve_ivp where applicable",
            "acid_base_root_xtol": 1.0e-14,
            "acid_base_root_rtol": 1.0e-12,
            "precipitation_hook_max_passes": 3,
            "equilibrium_residual_public_metric": "normalized charge-balance proxy",
        },
        "tasks": [
            {
                "task_id": task.task_id,
                "contract_hash": task.contract_hash,
                "scenario_id": task.scenario_id,
                "world_split": task.world_split,
                "budget": task.budget,
                "episode_mode": task.episode_mode,
                "physics_maturity": task.kernel_maturity.lowest_level.value,
                "proxy_allowed": task.kernel_maturity.proxy_allowed,
            }
            for task in (get_task(task_id) for task_id in task_ids)
        ],
        "agents": list(agents),
        "seeds": list(seeds),
        "private_eval_salt_policy": private_eval_salt_policy(),
    }


def _version_or_unavailable(package: str) -> str:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return "unavailable"


__all__ = ["PROVENANCE_SCHEMA_VERSION", "build_solver_provenance_manifest"]
