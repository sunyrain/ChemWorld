"""Validate and fingerprint the frozen ChemWorld publication protocol."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.publication_protocol import (
    DEFAULT_PUBLICATION_PROTOCOL_PATH,
    load_publication_protocol,
    publication_protocol_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=DEFAULT_PUBLICATION_PROTOCOL_PATH,
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    protocol = load_publication_protocol(args.protocol)
    manifest = publication_protocol_manifest(protocol)
    encoded = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(encoded)
    print(encoded.decode("utf-8"), end="")
    return 0 if manifest["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
