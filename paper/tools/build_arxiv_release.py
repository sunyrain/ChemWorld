"""Build the standard two-column arXiv source bundle and PDF."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARXIV = ROOT / "paper" / "arxiv"
MANUSCRIPT = ROOT / "paper" / "experimental_intelligence_v1_manuscript.md"
BIBLIOGRAPHY = ROOT / "paper" / "experimental_intelligence_v1_references.bib"
TEMPLATE = ARXIV / "template.tex"
BUILD = ARXIV / "build"
EXPORT = ROOT / "paper" / "exports" / "experimental-intelligence-v1-arxiv"
FIGURE_MANIFEST = (
    ROOT
    / "paper"
    / "figures"
    / "first-paper-world-instrument-v1"
    / "first-paper-publication-figure-manifest-v1.json"
)
SCHEMA = "chemworld-arxiv-release-build-manifest-0.1"
SOURCE_DATE_EPOCH = 1_785_628_800  # 2026-08-02 00:00:00 UTC
ZIP_TIMESTAMP = (2026, 8, 2, 0, 0, 0)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _optional_tool(name: str, fallback: Path | None = None) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    if fallback is not None and fallback.is_file():
        return str(fallback)
    for package_root in (
        Path.home() / "miniconda3" / "pkgs",
        Path.home() / "mambaforge" / "pkgs",
        Path.home() / "anaconda3" / "pkgs",
    ):
        if not package_root.is_dir():
            continue
        candidates = sorted(package_root.glob(f"{name}-*/bin/{name}"), reverse=True)
        if candidates:
            return str(candidates[0])
    return None


def _tool(name: str, fallback: Path | None = None) -> str:
    found = _optional_tool(name, fallback)
    if found is not None:
        return found
    raise RuntimeError(f"required build tool is unavailable: {name}")


def _run(command: list[str], *, cwd: Path) -> None:
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = str(SOURCE_DATE_EPOCH)
    environment["FORCE_SOURCE_DATE"] = "1"
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        tail = "\n".join(completed.stdout.splitlines()[-80:])
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}")


def _reset_directory(path: Path, *, allowed_root: Path) -> None:
    """Recreate a generated directory after verifying its workspace boundary."""
    resolved = path.resolve()
    root = allowed_root.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"refusing to reset path outside generated root: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def _normalize_text(path: Path) -> None:
    path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")


def _canonical_figure_pdfs() -> list[Path]:
    payload = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("first-paper publication figure manifest must be an object")
    declared = payload.pop("manifest_sha256", None)
    if declared != _canonical_sha(payload) or payload.get("status") != "PASS":
        raise RuntimeError("first-paper publication figure manifest is stale or failed")
    figures = payload.get("figures")
    if not isinstance(figures, list) or len(figures) != 3:
        raise RuntimeError("first-paper publication figure manifest must contain three figures")
    pdfs: list[Path] = []
    for order, figure in enumerate(figures, 1):
        if not isinstance(figure, dict) or figure.get("order") != order:
            raise RuntimeError("first-paper publication figure order changed")
        outputs = figure.get("outputs")
        if not isinstance(outputs, list):
            raise RuntimeError("first-paper publication figure outputs are missing")
        matches = [row for row in outputs if isinstance(row, dict) and row.get("format") == "pdf"]
        if len(matches) != 1:
            raise RuntimeError(f"figure {order} must bind exactly one PDF")
        row = matches[0]
        path_value = row.get("path")
        if not isinstance(path_value, str):
            raise RuntimeError(f"figure {order} PDF path is invalid")
        path = ROOT / path_value
        if (
            not path.is_file()
            or path.stat().st_size != row.get("bytes")
            or _sha(path) != row.get("sha256")
        ):
            raise RuntimeError(f"figure {order} PDF binding is stale")
        pdfs.append(path)
    return pdfs


def _copy_sources(bundle: Path, figure_pdfs: list[Path]) -> list[Path]:
    _reset_directory(bundle, allowed_root=EXPORT)
    (bundle / "figures").mkdir()
    copied = []
    for source, target in (
        (ARXIV / "main.tex", bundle / "main.tex"),
        (BIBLIOGRAPHY, bundle / "references.bib"),
        (BUILD / "main.bbl", bundle / "main.bbl"),
        (MANUSCRIPT, bundle / "manuscript.md"),
    ):
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        copied.append(target)
    for source in figure_pdfs:
        target = bundle / "figures" / source.name
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def _write_archives(bundle: Path, archive_base: Path) -> tuple[Path, Path]:
    """Create sorted source archives with normalized metadata."""
    members = sorted(path for path in bundle.rglob("*") if path.is_file())
    zip_path = archive_base.with_suffix(".zip")
    with zipfile.ZipFile(
        zip_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in members:
            relative = path.relative_to(bundle).as_posix()
            info = zipfile.ZipInfo(relative, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    tar_path = archive_base.with_suffix(".tar.gz")
    with (
        tar_path.open("wb") as raw,
        gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            mtime=SOURCE_DATE_EPOCH,
        ) as compressed,
        tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive,
    ):
        for path in members:
            data = path.read_bytes()
            info = tarfile.TarInfo(path.relative_to(bundle).as_posix())
            info.size = len(data)
            info.mtime = SOURCE_DATE_EPOCH
            info.mode = 0o644
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    return zip_path, tar_path


def build() -> dict[str, Any]:
    figure_pdfs = _canonical_figure_pdfs()
    pandoc = _tool(
        "pandoc",
        Path.home() / "AppData/Local/Pandoc/pandoc.exe",
    )
    miktex = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    pdflatex = _optional_tool("pdflatex", miktex / "pdflatex.exe")
    bibtex = _optional_tool("bibtex", miktex / "bibtex.exe")
    tectonic = None if pdflatex and bibtex else _tool("tectonic")
    BUILD.mkdir(parents=True, exist_ok=True)
    EXPORT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BIBLIOGRAPHY, ARXIV / "references.bib")
    _run(
        [
            pandoc,
            str(MANUSCRIPT),
            "--from=markdown+raw_tex+tex_math_dollars",
            "--to=latex",
            "--standalone",
            "--natbib",
            f"--template={TEMPLATE}",
            f"--resource-path={ARXIV};{ROOT / 'paper'};{ROOT}",
            "--output",
            str(ARXIV / "main.tex"),
        ],
        cwd=ROOT,
    )
    _normalize_text(ARXIV / "main.tex")
    main_tex = (ARXIV / "main.tex").read_text(encoding="utf-8")
    for source in figure_pdfs:
        canonical_reference = source.relative_to(ROOT / "paper").as_posix()
        bundled_reference = f"figures/{source.name}"
        if main_tex.count(canonical_reference) != 1:
            raise RuntimeError(f"manuscript must reference {canonical_reference} exactly once")
        main_tex = main_tex.replace(canonical_reference, bundled_reference)
    (ARXIV / "main.tex").write_text(main_tex, encoding="utf-8", newline="\n")
    for name in ("main.aux", "main.bbl", "main.blg", "main.log", "main.out", "main.pdf"):
        path = BUILD / name
        if path.exists():
            path.unlink()
    shutil.copy2(ARXIV / "main.tex", BUILD / "main.tex")
    shutil.copy2(ARXIV / "references.bib", BUILD / "references.bib")
    build_figures = BUILD / "figures"
    _reset_directory(build_figures, allowed_root=BUILD)
    for source in figure_pdfs:
        shutil.copy2(source, build_figures / source.name)
    if tectonic is not None:
        _run([tectonic, "-k", "--keep-logs", "main.tex"], cwd=BUILD)
    else:
        assert pdflatex is not None and bibtex is not None
        latex_args = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        _run(latex_args, cwd=BUILD)
        _run([bibtex, "main"], cwd=BUILD)
        _run(latex_args, cwd=BUILD)
        _run(latex_args, cwd=BUILD)
    _normalize_text(BUILD / "main.bbl")
    log = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    page_match = re.search(r"Output written on main\.(?:pdf|xdv) \((\d+) pages?", log)
    if page_match is None:
        raise RuntimeError("could not determine compiled PDF page count")
    pdf_page_count = int(page_match.group(1))
    pdf = EXPORT / "chemworld-experimental-agency-arxiv.pdf"
    shutil.copy2(BUILD / "main.pdf", pdf)
    bundle = EXPORT / "source"
    copied = _copy_sources(bundle, figure_pdfs)
    archive_base = EXPORT / "chemworld-experimental-agency-arxiv-source"
    zip_path, tar_path = _write_archives(bundle, archive_base)
    files = [pdf, zip_path, tar_path, ARXIV / "main.tex", *copied]
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA,
        "status": "compiled_arxiv_release",
        "pdf_page_count": pdf_page_count,
        "paper_source": MANUSCRIPT.relative_to(ROOT).as_posix(),
        "figure_manifest": FIGURE_MANIFEST.relative_to(ROOT).as_posix(),
        "figure_manifest_sha256": _sha(FIGURE_MANIFEST),
        "canonical_figure_count": len(figure_pdfs),
        "pdf": pdf.relative_to(ROOT).as_posix(),
        "source_zip": zip_path.relative_to(ROOT).as_posix(),
        "source_tar_gz": tar_path.relative_to(ROOT).as_posix(),
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha(path),
            }
            for path in sorted(set(files))
            if path.is_file()
        ],
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
    manifest_path = EXPORT / "build-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "pdf": str(pdf),
        "source_zip": str(zip_path),
        "source_tar_gz": str(tar_path),
        "manifest": str(manifest_path),
    }


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(build(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
