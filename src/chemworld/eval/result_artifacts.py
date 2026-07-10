"""Verified evaluation-result artifacts and trajectory integrity checks."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.data.validation import validate_records
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.verify import verify_records

EVALUATION_RESULT_SCHEMA_VERSION = "chemworld-evaluation-result-0.2"


def trajectory_sha256(path: str | Path) -> str:
    hasher = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_verified_evaluation_result(
    records: list[dict[str, Any]],
    *,
    trajectory_path: str | Path,
    threshold: float = 0.75,
) -> dict[str, Any]:
    """Replay a trajectory and return an integrity-bound evaluation result."""

    path = Path(trajectory_path).resolve()
    validate_records(records)
    verification = verify_records(records).to_dict()
    if not bool(verification["verified"]):
        raise ValueError(
            "Trajectory replay verification failed; refusing to produce an evaluation result"
        )
    result = evaluate_records(records, threshold=threshold).to_dict()
    result.update(
        {
            "result_schema_version": EVALUATION_RESULT_SCHEMA_VERSION,
            "verified": True,
            "verification": verification,
            "evaluation_threshold": float(threshold),
            "trajectory_path": str(path),
            "trajectory_sha256": trajectory_sha256(path),
        }
    )
    return result


def validate_verified_evaluation_result(
    result: dict[str, Any],
    *,
    replay: bool = False,
) -> None:
    """Validate result metadata, trajectory digest, and optionally replay it."""

    if result.get("result_schema_version") != EVALUATION_RESULT_SCHEMA_VERSION:
        raise ValueError(
            "Leaderboard input must use a supported verified evaluation-result schema"
        )
    if result.get("verified") is not True:
        raise ValueError("Leaderboard input is not replay verified")
    verification = result.get("verification")
    if not isinstance(verification, dict) or verification.get("verified") is not True:
        raise ValueError("Leaderboard input is missing a successful verification report")
    trajectory_value = result.get("trajectory_path")
    expected_digest = result.get("trajectory_sha256")
    if not isinstance(trajectory_value, str) or not trajectory_value:
        raise ValueError("Leaderboard input is missing trajectory_path")
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        raise ValueError("Leaderboard input is missing a valid trajectory_sha256")
    trajectory = Path(trajectory_value)
    if not trajectory.is_file():
        raise ValueError(f"Leaderboard trajectory does not exist: {trajectory}")
    actual_digest = trajectory_sha256(trajectory)
    if actual_digest != expected_digest:
        raise ValueError("Leaderboard trajectory digest does not match evaluation result")
    if replay:
        records = load_jsonl(trajectory)
        replay_result = verify_records(records)
        if not replay_result.verified:
            raise ValueError("Leaderboard trajectory no longer passes replay verification")
        threshold = result.get("evaluation_threshold")
        if not isinstance(threshold, int | float) or isinstance(threshold, bool):
            raise ValueError("Leaderboard input is missing evaluation_threshold")
        recomputed = evaluate_records(records, threshold=float(threshold)).to_dict()
        for key, expected_value in recomputed.items():
            actual_value = result.get(key)
            if isinstance(expected_value, float) and isinstance(actual_value, int | float):
                matches = math.isclose(
                    float(actual_value),
                    expected_value,
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                )
            else:
                matches = actual_value == expected_value
            if not matches:
                raise ValueError(
                    f"Leaderboard metric {key!r} does not match trajectory evaluation"
                )


__all__ = [
    "EVALUATION_RESULT_SCHEMA_VERSION",
    "build_verified_evaluation_result",
    "trajectory_sha256",
    "validate_verified_evaluation_result",
]
