"""Build the deterministic public hash index for the first arXiv raw data."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "benchmark/releases/chemworld-serious-v1/"
    "g0-raw-file-index.json"
)
SCHEMA_VERSION = "chemworld-arxiv-v1-raw-file-index-0.1"


@dataclass(frozen=True)
class RawRootSpec:
    root_id: str
    relative_path: str
    source_commit: str
    expected_file_count: int
    expected_byte_count: int
    expected_campaign_index_sha256: str


RAW_ROOT_SPECS = (
    RawRootSpec(
        root_id="v10_baselines",
        relative_path="runs/formal/static-s0-v10-baselines-20260729",
        source_commit="4a72320585166f4f063749e7d06068b42f7b7b68",
        expected_file_count=1133,
        expected_byte_count=16239891581,
        expected_campaign_index_sha256=(
            "9451f67aed59481cc4c2f3c29eff241b1deea9aaccef6d43efe86cc4ca5c0238"
        ),
    ),
    RawRootSpec(
        root_id="v10_opaque",
        relative_path="runs/formal/static-s0-v10-codex-subscription-20260729",
        source_commit="555896ce3f6b6d6455ab9e0605e01063057889da",
        expected_file_count=105,
        expected_byte_count=494951408,
        expected_campaign_index_sha256=(
            "5b8acfce111109f49a736ac601ad9c197adae9313020bc61ec9ff026ed9419e8"
        ),
    ),
    RawRootSpec(
        root_id="v11_nominal",
        relative_path="runs/formal/static-s0-v11-nominal-codex-subscription-20260729",
        source_commit="52d317e49887d4b918eb65319d57542126c6bb17",
        expected_file_count=102,
        expected_byte_count=495504956,
        expected_campaign_index_sha256=(
            "744a9de8ef3a239d0fa3ff4f9e037c11a232a8cc9902342c8aec86dac6e4e511"
        ),
    ),
    RawRootSpec(
        root_id="v12_misindexed",
        relative_path="runs/formal/static-s0-v12-misindexed-codex-subscription-20260729",
        source_commit="5f5d8b51bb7b987a3de5ac57e1890abcdc4ff0f2",
        expected_file_count=101,
        expected_byte_count=495376658,
        expected_campaign_index_sha256=(
            "8cedb86a93a0c9348462b5229981085e74ed5b71511f4b8c97792b4760f05fb3"
        ),
    ),
)


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid JSON object: {path}") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON payload is not an object: {path}")
    return payload


def _index_root(repository_root: Path, spec: RawRootSpec) -> dict[str, Any]:
    root = (repository_root / spec.relative_path).resolve()
    repository_root = repository_root.resolve()
    if not root.is_dir() or not root.is_relative_to(repository_root):
        raise RuntimeError(f"raw root is missing or outside the repository: {root}")
    files = sorted(path for path in root.rglob("*") if path.is_file())
    symlinks = [path for path in files if path.is_symlink()]
    if symlinks:
        raise RuntimeError(f"raw root contains symlinked files: {symlinks[0]}")
    records = [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for path in files
    ]
    observed_bytes = sum(int(record["bytes"]) for record in records)
    campaign_index = root / "campaign_execution_index.json"
    observed_index_sha256 = file_sha256(campaign_index)
    index_payload = _load_object(campaign_index)
    checks = {
        "file_count": len(records) == spec.expected_file_count,
        "byte_count": observed_bytes == spec.expected_byte_count,
        "campaign_index_sha256": (
            observed_index_sha256 == spec.expected_campaign_index_sha256
        ),
        "source_commit": index_payload.get("source_commit") == spec.source_commit,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(
            f"raw-root identity mismatch for {spec.root_id}: {', '.join(failed)}"
        )
    return {
        "root_id": spec.root_id,
        "source_path": spec.relative_path,
        "source_commit": spec.source_commit,
        "file_count": len(records),
        "byte_count": observed_bytes,
        "campaign_index_sha256": observed_index_sha256,
        "checks": checks,
        "files": records,
    }


def build_index(
    repository_root: Path,
    *,
    specs: Sequence[RawRootSpec] = RAW_ROOT_SPECS,
) -> dict[str, Any]:
    roots = [_index_root(repository_root, spec) for spec in specs]
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "scope": "G0 raw roots used by the first ChemWorld arXiv manuscript",
        "path_policy": "repository-relative root IDs and root-relative file paths only",
        "content_included": False,
        "root_count": len(roots),
        "file_count": sum(int(root["file_count"]) for root in roots),
        "byte_count": sum(int(root["byte_count"]) for root in roots),
        "roots": roots,
    }
    payload["index_sha256"] = canonical_json_sha256(payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = build_index(args.repository_root.resolve())
    output = args.output.resolve()
    if args.check:
        if _load_object(output) != payload:
            raise RuntimeError(f"raw file index is stale: {output}")
    else:
        write_json_atomic(output, payload)
    print(
        json.dumps(
            {
                "output": str(output),
                "root_count": payload["root_count"],
                "file_count": payload["file_count"],
                "byte_count": payload["byte_count"],
                "index_sha256": payload["index_sha256"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
