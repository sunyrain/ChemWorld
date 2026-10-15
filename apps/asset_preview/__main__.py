"""Run a local read-only preview, optionally downloading its three assets first."""

import argparse
from pathlib import Path

from .assets import DEFAULT_CACHE, download
from .server import serve


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8895)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--download-only", action="store_true")
    args = parser.parse_args()
    if args.download or args.download_only:
        download(args.cache)
    if not args.download_only:
        serve(args.cache, args.port)


if __name__ == "__main__":
    main()
