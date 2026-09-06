"""Portable launcher: project Python runs services; Blender runs only its renderer."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[1]


def health(url: str) -> dict | None:
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url + "/health", timeout=0.5) as response:
            result = json.load(response)
        if result.get("integration") != "chemworld-blender-1":
            raise RuntimeError("Selected port belongs to another service; use --port")
        return result
    except (OSError, urllib.error.URLError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blender", default=os.environ.get("BLENDER_BIN") or shutil.which("blender")
    )
    parser.add_argument("--port", type=int, default=8877)
    parser.add_argument("--api-only", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be 1..65535")
    if not args.api_only and (not args.blender or not Path(args.blender).is_file()):
        parser.error("Set BLENDER_BIN, put Blender on PATH, or pass --blender /path/to/blender")
    url = f"http://127.0.0.1:{args.port}"
    data = ROOT / "runtime" / str(args.port)
    data.mkdir(parents=True, exist_ok=True)
    info = health(url)
    if info is None:
        with (data / "server.log").open("ab") as log:
            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "apps.blender_lab.server",
                    "--port",
                    str(args.port),
                    "--data-dir",
                    str(data),
                ],
                cwd=REPOSITORY,
                stdout=log,
                stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        for _ in range(100):
            info = health(url)
            if info:
                break
            time.sleep(0.1)
        if info is None:
            raise RuntimeError(f"Service failed to start; inspect {data / 'server.log'}")
    if not args.api_only and not info.get("bridge", {}).get("connected"):
        environment = {**os.environ, "CHEMLAB_API_URL": url, "CHEMWORLD_PYTHON": sys.executable}
        with (data / "blender.log").open("ab") as log:
            subprocess.Popen(
                [args.blender, str(ROOT / "ChemLab.blend"), "--python", str(ROOT / "startup.py")],
                cwd=REPOSITORY,
                env=environment,
                stdout=log,
                stderr=log,
            )
    print(f"Blender service: {url}")
    print(f"Set CHEMWORLD_BLENDER_URL={url} for Task Lab or wrap your Gym environment.")


if __name__ == "__main__":
    main()
