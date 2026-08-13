#!/usr/bin/env python3
"""Build the provider-free W2-27 selected resource-card receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_method_qualification_local import (
    build_w2_27_selected_resource_card_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


def _repository_path(path: Path, *, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"{label} must remain inside the repository") from error
    return resolved


def build_receipt(
    manifest_path: Path,
    terminal_triplet_path: Path,
    output_path: Path,
) -> tuple[dict[str, Any], Path]:
    """Build and atomically write one receipt without invoking a provider."""

    manifest = _repository_path(manifest_path, label="W2-26 manifest")
    terminal_triplet = _repository_path(
        terminal_triplet_path,
        label="A-E electrochemical terminal triplet",
    )
    output = _repository_path(output_path, label="W2-27 receipt output")
    if output.exists():
        raise FileExistsError(f"refusing to overwrite W2-27 receipt: {output}")
    receipt = build_w2_27_selected_resource_card_receipt(
        ROOT,
        manifest,
        terminal_triplet,
    )
    write_json_atomic(output, receipt)
    return receipt, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--w2-26-manifest", required=True, type=Path)
    parser.add_argument(
        "--ae-electrochemical-terminal-triplet",
        required=True,
        type=Path,
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    receipt, output = build_receipt(
        args.w2_26_manifest,
        args.ae_electrochemical_terminal_triplet,
        args.output,
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "selected_resource_card_sha256": receipt["selected_resource_card_sha256"],
                "selected_card_receipt_sha256": receipt["selected_card_receipt_sha256"],
                "output": output.relative_to(ROOT.resolve()).as_posix(),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
