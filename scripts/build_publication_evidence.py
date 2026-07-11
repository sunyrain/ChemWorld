"""Build a compact, fail-closed evidence summary from a formal full matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.publication_evidence import build_publication_evidence_summary
from chemworld.eval.publication_protocol import (
    DEFAULT_PUBLICATION_PROTOCOL_PATH,
    load_publication_protocol,
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PUBLICATION_PROTOCOL_PATH)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "workstreams/benchmark_v1/reports/publication-classic20-full-summary.json"
        ),
    )
    args = parser.parse_args()

    manifest_path = args.run_dir / "manifest.json"
    results_path = args.run_dir / "baseline_results.json"
    validity_path = args.run_dir / "validity_power.json"
    manifest = _load_json(manifest_path)
    if _sha256(results_path) != manifest.get("baseline_results_sha256"):
        raise ValueError("baseline result digest does not match the formal run manifest")
    if _sha256(validity_path) != manifest.get("validity_power_sha256"):
        raise ValueError("validity report digest does not match the formal run manifest")
    results = _load_json(results_path)
    validity = _load_json(validity_path)
    protocol = load_publication_protocol(args.protocol)
    if not isinstance(results, list) or not isinstance(validity, dict):
        raise ValueError("formal run artifacts have invalid JSON shapes")
    summary = build_publication_evidence_summary(
        results,
        run_manifest=manifest,
        validity_report=validity,
        protocol=protocol,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(
        (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": summary["status"],
                "publication_ready": summary["publication_ready"],
                "gates": summary["gates"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
