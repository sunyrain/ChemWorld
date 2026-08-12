#!/usr/bin/env python3
"""Freeze the minimal Work II experiment execution surface at a clean HEAD."""

from __future__ import annotations

import argparse
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v02 import bind_release_attempt
from chemworld.eval.work_ii_execution_mode import build_release_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "runs/work-ii-release/work-ii-execution-release-manifest-v0.1.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--execution-surface",
        action="append",
        required=True,
        help="Repository-relative execution path; repeat for every runtime/evaluator input.",
    )
    parser.add_argument(
        "--bind-ae-prior-v02-attempt",
        action="store_true",
        help="bind the one canonical write-once A-E v0.2 attempt at freeze time",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite release manifest: {output}")
    manifest = build_release_manifest(root, execution_surface=args.execution_surface)
    if args.bind_ae_prior_v02_attempt:
        manifest = bind_release_attempt(manifest)
    write_json_atomic(output, manifest)
    print(
        "[work-ii-freeze] status=frozen "
        f"paths={len(manifest['execution_surface']['relative_roots'])} "
        f"freeze_id={manifest['freeze_id']} output={output}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
