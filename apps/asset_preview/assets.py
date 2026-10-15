"""Download only three licensed display assets into an ignored, optional cache."""

import json
import struct
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE = ROOT / "reference_repos" / "chemlab-assets-preview"
UPSTREAM = "https://github.com/mbzuai-nlp/ChemLab-Assets"
CODE_REVISION = "a9826f99dd08c31837b2e5be9e68f55d13cfce88"
DATASET = "https://huggingface.co/datasets/MBZUAI/ChemLab-Assets"
INSTRUMENTS = (
    {"slug": "ika_plate_rctdigital", "title": "加热搅拌器", "subtitle": "IKA · RCT digital"},
    {"slug": "metrohm_914", "title": "pH 测定仪", "subtitle": "Metrohm · 914"},
    {"slug": "hach_dr6000", "title": "UV-Vis 分光光度计", "subtitle": "Hach · DR6000"},
)


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "ChemWorld-asset-preview/1.0"})
    with urlopen(request, timeout=25) as response:
        return response.read()


def glb_document(data: bytes) -> dict:
    """Check the container before advertising the downloaded model as available."""
    if len(data) < 20:
        raise ValueError("Incomplete GLB")
    magic, version, length, json_length, chunk_type = struct.unpack_from("<4sIIII", data)
    if magic != b"glTF" or version != 2 or length != len(data) or chunk_type != 0x4E4F534A:
        raise ValueError("Invalid GLB 2 container")
    return json.loads(data[20 : 20 + json_length])


def download(cache: Path) -> None:
    cache.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    print("Resolve asset release; 0/3 instruments", flush=True)
    revision = json.loads(fetch("https://huggingface.co/api/datasets/MBZUAI/ChemLab-Assets"))["sha"]
    raw = f"https://raw.githubusercontent.com/mbzuai-nlp/ChemLab-Assets/{CODE_REVISION}"
    for name in ("LICENSE", "LICENSE-ASSETS.md", "NOTICE.md", "CITATION.cff"):
        (cache / name).write_bytes(fetch(f"{raw}/{name}"))
        print(f"Fetched attribution: {name}", flush=True)
    entries = []
    for count, item in enumerate(INSTRUMENTS, 1):
        slug = item["slug"]
        directory = cache / slug
        directory.mkdir(exist_ok=True)
        bundle_bytes = fetch(f"{raw}/explorer/data/assets/instrument.{slug}.json")
        bundle = json.loads(bundle_bytes)
        if bundle["tid"] != f"instrument.{slug}" or not bundle["glb"].startswith("assets/"):
            raise ValueError(f"Unexpected asset identity: {slug}")
        print(f"Downloading geometry {count}/3: {slug}", flush=True)
        geometry = fetch(f"{DATASET}/resolve/{revision}/{bundle['glb']}")
        document = glb_document(geometry)
        (directory / "model.glb").write_bytes(geometry)
        (directory / "bundle.json").write_bytes(bundle_bytes)
        entries.append(
            item | {"bytes": len(geometry), "mesh_count": len(document.get("meshes", []))}
        )
        elapsed = time.monotonic() - start
        print(
            f"Assets {count}/3 | {count / elapsed:.2f} instruments/s | "
            f"ETA {(3 - count) * elapsed / count:.0f}s | {len(geometry):,} bytes",
            flush=True,
        )
    index = {
        "source": UPSTREAM,
        "dataset": DATASET,
        "code_revision": CODE_REVISION,
        "dataset_revision": revision,
        "license": "CC BY-NC 4.0",
        "attribution": (
            "Zirui Song, Jiadong Zhang, Jiahao Zhang, Xiaojun Chang, Xiaosong Ma, "
            "Xiuying Chen · MBZUAI · 2026"
        ),
        "modifications": (
            "Geometry and metadata unchanged; ChemWorld adds a separate viewer "
            "and public-record projection."
        ),
        "instruments": entries,
    }
    (cache / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Ready: {cache}; three display assets, no external runtime installed", flush=True)
