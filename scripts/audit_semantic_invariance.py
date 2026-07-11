"""Run the candidate vNext semantic-invariance control audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.semantic_invariance import audit_semantic_invariance

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs" / "benchmark" / "semantic_invariance_vnext.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "semantic-invariance-controls.json"
)


def _read_protocol(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("semantic invariance protocol must be a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    protocol = _read_protocol(args.protocol)
    report = audit_semantic_invariance(protocol)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
