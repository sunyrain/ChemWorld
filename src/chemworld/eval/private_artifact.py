"""Signed private-evaluation artifact helpers."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld import __version__
from chemworld.data.submission import git_commit
from chemworld.eval.leaderboard import load_results


def _canonical_json(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class SignedPrivateEvalArtifact:
    schema_version: str
    generated_at: str
    chemworld_version: str
    commit_hash: str | None
    salt_hash: str
    signature: str
    result_count: int
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "chemworld_version": self.chemworld_version,
            "commit_hash": self.commit_hash,
            "salt_hash": self.salt_hash,
            "signature": self.signature,
            "result_count": self.result_count,
            "payload": self.payload,
        }


def sign_private_eval_results(
    *,
    result_paths: list[str | Path],
    output_path: str | Path,
    salt: str | None = None,
    run_log: dict[str, Any] | None = None,
) -> SignedPrivateEvalArtifact:
    """Write a signed artifact for maintainer-side private-eval results.

    The secret salt is used only for HMAC signing. The artifact stores a
    SHA-256 salt hash, never the salt itself.
    """

    secret = salt if salt is not None else os.environ.get("CHEMWORLD_PRIVATE_EVAL_SALT")
    if not secret:
        raise ValueError(
            "CHEMWORLD_PRIVATE_EVAL_SALT is required to sign private-eval artifacts"
        )

    results = load_results(result_paths)
    payload = {
        "results": results,
        "run_log": run_log or {},
        "result_paths": [str(path) for path in result_paths],
    }
    signature = hmac.new(secret.encode("utf-8"), _canonical_json(payload), hashlib.sha256)
    artifact = SignedPrivateEvalArtifact(
        schema_version="chemworld-private-eval-signed-0.1",
        generated_at=datetime.now(UTC).isoformat(),
        chemworld_version=__version__,
        commit_hash=git_commit(),
        salt_hash=hashlib.sha256(secret.encode("utf-8")).hexdigest(),
        signature=signature.hexdigest(),
        result_count=len(results),
        payload=payload,
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(artifact.to_dict(), handle, indent=2, sort_keys=True)
    return artifact


def verify_private_eval_artifact(path: str | Path, *, salt: str) -> bool:
    with Path(path).open("r", encoding="utf-8") as handle:
        artifact = json.load(handle)
    payload = artifact.get("payload", {})
    expected = hmac.new(salt.encode("utf-8"), _canonical_json(payload), hashlib.sha256)
    return hmac.compare_digest(str(artifact.get("signature", "")), expected.hexdigest())


__all__ = [
    "SignedPrivateEvalArtifact",
    "sign_private_eval_results",
    "verify_private_eval_artifact",
]
