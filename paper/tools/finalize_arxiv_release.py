"""Fail-closed attachment of the durable raw-data archive to the arXiv release.

Public author metadata already lives in the canonical manuscript. This command
accepts only the remaining external archive identity. ``--check`` is read-only;
``--apply`` validates the archive before changing tracked sources, rebuilds the
current arXiv package, and marks the release ready only after integrity verification.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper" / "experimental_intelligence_v1_manuscript.md"
RELEASE_README = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "README.md"
RELEASE_MANIFEST = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "manifest.json"
ARXIV_BUILDER = ROOT / "paper" / "tools" / "build_arxiv_release.py"
ARXIV_BUILD = ROOT / "paper" / "arxiv" / "build"
ARXIV_EXPORT = ROOT / "paper" / "exports" / "experimental-intelligence-v1-arxiv"
GENERATED_ROLLBACK_TARGETS = (
    ROOT / "paper" / "arxiv" / "main.tex",
    ROOT / "paper" / "arxiv" / "references.bib",
    ARXIV_BUILD,
    ARXIV_EXPORT,
)

SCHEMA = "chemworld-arxiv-archive-metadata-0.2"
EXPECTED_RAW_INDEX_SHA256 = "f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961"
EXPECTED_RAW_BYTE_COUNT = 17_725_724_603
EXPECTED_RAW_FILE_COUNT = 1_441

_PLACEHOLDER = re.compile(
    r"(?:replace[_ -]?me|placeholder|\btodo\b|\btbd\b|\bexample\b|"
    r"\bfull name\b|\brepository name\b|department,\s*institution|chemworld authors)",
    flags=re.IGNORECASE,
)


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _nonplaceholder(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and value == value.strip()
        and all(ord(character) >= 32 for character in value)
        and _PLACEHOLDER.search(value) is None
    )


def validate_release_metadata(metadata: Any) -> list[str]:
    """Return deterministic blockers; an empty list means the release inputs are ready."""
    blockers: list[str] = []
    if not isinstance(metadata, Mapping):
        return ["metadata must be a JSON object"]
    expected_keys = {"schema_version", "status", "archive"}
    unknown = sorted(set(metadata) - expected_keys)
    missing = sorted(expected_keys - set(metadata))
    if unknown:
        blockers.append(f"unknown top-level fields: {', '.join(unknown)}")
    if missing:
        blockers.append(f"missing top-level fields: {', '.join(missing)}")
    if metadata.get("schema_version") != SCHEMA:
        blockers.append(f"schema_version must equal {SCHEMA}")
    if metadata.get("status") != "ready":
        blockers.append("status must equal ready")

    archive = metadata.get("archive")
    if not isinstance(archive, Mapping):
        blockers.append("archive must be an object")
        archive = {}
    allowed_archive = {
        "provider",
        "identifier",
        "url",
        "publicly_resolvable",
        "raw_file_index_sha256",
        "byte_count",
    }
    archive_unknown = sorted(set(archive) - allowed_archive)
    if archive_unknown:
        blockers.append(f"archive has unknown fields: {', '.join(archive_unknown)}")
    for field in ("provider", "identifier"):
        if not _nonplaceholder(archive.get(field)):
            blockers.append(f"archive.{field} must be public and non-placeholder")
    url = archive.get("url")
    parsed = urlparse(url) if isinstance(url, str) else None
    if not _nonplaceholder(url) or parsed is None or parsed.scheme != "https" or not parsed.netloc:
        blockers.append("archive.url must be a public absolute HTTPS URL")
    if archive.get("publicly_resolvable") is not True:
        blockers.append("archive.publicly_resolvable must be explicitly true")
    if archive.get("raw_file_index_sha256") != EXPECTED_RAW_INDEX_SHA256:
        blockers.append("archive.raw_file_index_sha256 does not match the frozen G0 index")
    if archive.get("byte_count") != EXPECTED_RAW_BYTE_COUNT:
        blockers.append("archive.byte_count does not match the frozen G0 byte count")
    return blockers


def _markdown_escape(value: str) -> str:
    for character in ("\\", "[", "]", "*", "_"):
        value = value.replace(character, "\\" + character)
    return value


def inject_archive_metadata(text: str, metadata: Mapping[str, Any]) -> str:
    updated = text
    archive = metadata["archive"]
    provider = _markdown_escape(str(archive["provider"]))
    identifier = _markdown_escape(str(archive["identifier"]))
    new_paragraph = (
        f"The 17.7-GB compiled-control execution logs are publicly archived by "
        f"{provider} under [{identifier}]({archive['url']}). The deposit permits inspection "
        "of the raw execution records in addition to regeneration of the reported analyses "
        "from processed data. Unrestricted provider responses remain excluded, and stochastic "
        "provider decisions are not exactly reproducible."
    )
    availability_pattern = re.compile(
        r"(?:"
        r"(?P<current>"
        r"Code, configuration, processed reports, figure source data and release tooling are\s+"
        r"available in the MIT-licensed ChemWorld repository at\s+"
        r"\[github\.com/sunyrain/ChemWorld\]\(https://github\.com/sunyrain/ChemWorld\)\. "
        r"The tracked\s+"
        r"materials regenerate the tables and figures and replay released simulator "
        r"transitions and\s+"
        r"resource changes\..*?Provider authentication,\s+unrestricted response\s+"
        r"bodies,\s+private reasoning\s+and hidden evaluator identities are excluded\."
        r")"
        r"|"
        r"(?P<current_new>"
        r"ChemWorld code, configuration files, processed experimental records, "
        r"figure source data,\s+"
        r"release tooling and public trajectories are available under the MIT License "
        r"in the project\s+"
        r"repository at \[github\.com/sunyrain/ChemWorld\]"
        r"\(https://github\.com/sunyrain/ChemWorld\)\. "
        r"The\s+repository contains the materials required to reproduce the principal "
        r"statistics and figures\s+"
        r"reported here and to replay the released simulator environment--action trajectories, "
        r"public\s+"
        r"observations and resource ledgers\..*?"
        r"numerical execution will be identical across platforms or software\s+versions\."
        r")"
        r"|"
        r"(?P<current_compact>"
        r"ChemWorld code, configuration files, processed evidence, figure data and "
        r"released trajectories\s+"
        r"are available under the MIT License at\s+"
        r"\[github\.com/sunyrain/ChemWorld\]"
        r"\(https://github\.com/sunyrain/ChemWorld\)\. The repository contains\s+"
        r"the materials required to reproduce the reported figures and statistics and "
        r"to replay the\s+"
        r"released simulator trajectories\."
        r")"
        r"|"
        r"(?P<current_public>"
        r"A frozen(?:, versioned)? public release.*?"
        r"private seeds and local\s+run caches are not included\."
        r")"
        r"|"
        r"The larger compiled-control execution logs total 17\.7 GB and are not required to\n"
        r"regenerate the reported analyses from the processed data\. "
        r"They have not yet been placed\n"
        r"in a durable public archive\. Without those logs or unrestricted provider responses, a\n"
        r"third party can verify the reported arithmetic and figures, inspect the published\n"
        r"evidence boundaries, and replay the released simulator trajectories, but cannot inspect\n"
        r"every raw provider response\."
        r"|"
        r"The 17\.7-GB compiled-control execution logs are publicly archived by .*?"
        r"provider decisions are not exactly reproducible\."
        r"|"
        r"The 17\.7-GB compiled-control raw roots are bound by the public file-level hash "
        r"index but are not\n"
        r"included in the repository and have not yet received a durable external archive\n"
        r"identifier; raw-byte access is therefore not presently available from a permanent\n"
        r"archive\. A third party without those bytes or unrestricted provider responses can "
        r"verify\n"
        r"the reported arithmetic and figures, inspect the published evidence boundaries, and\n"
        r"replay the released simulator trajectories, but cannot independently audit every raw\n"
        r"provider decision or recompute the four raw-root hashes from source bytes\."
        r"|"
        r"The 17\.7-GB G0 raw roots are bound by the public file-level hash index but are not\n"
        r"included in the repository and have not yet received a durable external archive\n"
        r"identifier; raw-byte access is therefore not presently available from a permanent\n"
        r"archive\. The tracked world-level summaries and derived-data object are sufficient\n"
        r"to regenerate the paper's reported analyses\."
        r"|"
        r"The indexed 17\.7-GB compiled-control raw roots are publicly archived by .*?"
        r"decisions are not exactly reproducible\."
        r"|"
        r"The indexed 17\.7-GB G0 raw roots are publicly archived by .*?"
        r"derived-data object regenerate the paper's reported analyses\."
        r")",
        flags=re.DOTALL,
    )
    existing_archive_pattern = re.compile(
        r"The 17\.7-GB compiled-control execution logs are publicly archived by .*?"
        r"provider decisions are not exactly reproducible\.",
        flags=re.DOTALL,
    )
    if existing_archive_pattern.search(updated):
        updated, count = existing_archive_pattern.subn(new_paragraph, updated, count=1)
    else:

        def append_archive(match: re.Match[str]) -> str:
            preserved = (
                match.group("current")
                or match.group("current_new")
                or match.group("current_compact")
                or match.group("current_public")
                or ""
            )
            return (preserved + "\n\n" if preserved else "") + new_paragraph

        updated, count = availability_pattern.subn(
            append_archive,
            updated,
            count=1,
        )
    if count != 1:
        raise ValueError("G0 Data Availability paragraph was not found exactly once")
    return updated


def render_release_readme(text: str, metadata: Mapping[str, Any]) -> str:
    archive = metadata["archive"]
    provider = _markdown_escape(str(archive["provider"]))
    identifier = _markdown_escape(str(archive["identifier"]))
    updated = re.sub(
        r"Status: \*\*.*?\*\*",
        "Status: **publication package finalized and externally archived**",
        text,
        count=1,
    )
    final_gate = (
        "## External release gate\n\n"
        f"The four indexed G0 raw roots total {EXPECTED_RAW_BYTE_COUNT:,} bytes and are "
        f"publicly archived by {provider} under "
        f"[{identifier}]({archive['url']}). The archive is bound to the frozen "
        f"{EXPECTED_RAW_FILE_COUNT:,}-file index (`{EXPECTED_RAW_INDEX_SHA256}`). Public author, "
        "affiliation and correspondence metadata remain owned by the canonical manuscript. "
        "The release manifest is marked ready only after the current PDF/source rebuild and "
        "release-artifact integrity verification succeeds.\n"
    )
    updated, count = re.subn(
        r"## External release gate\n\n.*\Z",
        final_gate,
        updated,
        flags=re.DOTALL,
        count=1,
    )
    if count != 1:
        raise ValueError("release README external-gate section was not found")
    return updated


def finalized_manifest(manifest: Mapping[str, Any], metadata: Mapping[str, Any]) -> dict[str, Any]:
    updated = copy.deepcopy(dict(manifest))
    archive = metadata["archive"]
    updated["status"] = "publication_ready"
    updated["publication_ready"] = True
    updated["evidence"]["g0_raw_data_archive"] = {
        "provider": archive["provider"],
        "identifier": archive["identifier"],
        "url": archive["url"],
        "raw_file_index_sha256": archive["raw_file_index_sha256"],
        "file_count": EXPECTED_RAW_FILE_COUNT,
        "byte_count": archive["byte_count"],
        "release_metadata_sha256": _canonical_sha(metadata),
    }
    updated["gates"]["raw_data_archive"] = "passed_durable_archive_identifier"
    updated["gates"]["author_metadata"] = "passed_canonical_manuscript_author_metadata"
    return updated


def _atomic_write_text(path: Path, value: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    _atomic_write_text(
        path,
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
    )


def _run(command: Sequence[str]) -> None:
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        tail = "\n".join(completed.stdout.splitlines()[-100:])
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}")


def _optional_release_tool(name: str, fallback: Path | None = None) -> str | None:
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


def apply_preflight_blockers() -> list[str]:
    blockers: list[str] = []
    windows_pandoc = Path.home() / "AppData/Local/Pandoc/pandoc.exe"
    windows_tex = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    if _optional_release_tool("pandoc", windows_pandoc) is None:
        blockers.append("required release build tool is unavailable: pandoc")
    pdflatex = _optional_release_tool("pdflatex", windows_tex / "pdflatex.exe")
    bibtex = _optional_release_tool("bibtex", windows_tex / "bibtex.exe")
    if not (pdflatex and bibtex) and _optional_release_tool("tectonic") is None:
        blockers.append("required release build tools are unavailable: pdflatex+bibtex or tectonic")
    return blockers


def _snapshot_generated_files(
    targets: Sequence[Path] = GENERATED_ROLLBACK_TARGETS,
) -> dict[Path, bytes]:
    snapshot: dict[Path, bytes] = {}
    for target in targets:
        if target.is_file():
            snapshot[target] = target.read_bytes()
        elif target.is_dir():
            for path in sorted(target.rglob("*")):
                if path.is_file():
                    snapshot[path] = path.read_bytes()
    return snapshot


def _restore_generated_files(
    snapshot: Mapping[Path, bytes],
    targets: Sequence[Path] = GENERATED_ROLLBACK_TARGETS,
) -> None:
    current: set[Path] = set()
    for target in targets:
        if target.is_file():
            current.add(target)
        elif target.is_dir():
            current.update(path for path in target.rglob("*") if path.is_file())
    for path in sorted(current - set(snapshot), reverse=True):
        path.unlink()
    for path, value in snapshot.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".rollback-tmp")
        temporary.write_bytes(value)
        temporary.replace(path)


def _verified_self_hashed_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256", None)
    if declared != _canonical_sha(manifest):
        raise RuntimeError(f"self-hash mismatch: {path.relative_to(ROOT).as_posix()}")
    return manifest


def _verify_file_rows(rows: Any, *, label: str) -> int:
    if not isinstance(rows, list) or not rows:
        raise RuntimeError(f"{label} has no file records")
    root = ROOT.resolve()
    for row in rows:
        path = (ROOT / row["path"]).resolve()
        if root != path and root not in path.parents:
            raise RuntimeError(f"{label} records a path outside the repository: {path}")
        if not path.is_file():
            raise RuntimeError(f"{label} output is missing: {row['path']}")
        if path.stat().st_size != row["bytes"] or _sha(path) != row["sha256"]:
            raise RuntimeError(f"{label} output hash or byte count is stale: {row['path']}")
    return len(rows)


def _extract_verified_source_zip(zip_path: Path, destination: Path) -> int:
    member_count = 0
    destination_root = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            member = PurePosixPath(info.filename)
            if (
                info.is_dir()
                or member.is_absolute()
                or ".." in member.parts
                or "\\" in info.filename
            ):
                raise RuntimeError(f"unsafe or unexpected arXiv ZIP member: {info.filename}")
            mode = (info.external_attr >> 16) & 0o170000
            if mode not in (0, 0o100000):
                raise RuntimeError(f"non-regular arXiv ZIP member: {info.filename}")
            target = (destination / Path(*member.parts)).resolve()
            if destination_root not in target.parents:
                raise RuntimeError(f"arXiv ZIP member escapes extraction root: {info.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
            member_count += 1
    return member_count


def _extract_verified_source_tar(tar_path: Path, destination: Path) -> int:
    member_count = 0
    destination_root = destination.resolve()
    with tarfile.open(tar_path, mode="r:gz") as archive:
        for info in archive.getmembers():
            member = PurePosixPath(info.name)
            if (
                not info.isfile()
                or member.is_absolute()
                or ".." in member.parts
                or "\\" in info.name
            ):
                raise RuntimeError(f"unsafe or unexpected arXiv TAR member: {info.name}")
            target = (destination / Path(*member.parts)).resolve()
            if destination_root not in target.parents:
                raise RuntimeError(f"arXiv TAR member escapes extraction root: {info.name}")
            extracted = archive.extractfile(info)
            if extracted is None:
                raise RuntimeError(f"arXiv TAR member is unreadable: {info.name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(extracted.read())
            member_count += 1
    return member_count


def _archive_member_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            rows = [
                (info.filename, archive.read(info))
                for info in archive.infolist()
                if not info.is_dir()
            ]
    else:
        rows = []
        with tarfile.open(path, mode="r:gz") as archive:
            for info in archive.getmembers():
                if not info.isfile():
                    continue
                extracted = archive.extractfile(info)
                if extracted is None:
                    raise RuntimeError(f"arXiv TAR member is unreadable: {info.name}")
                rows.append((info.name, extracted.read()))
    for name, content in rows:
        member = PurePosixPath(name)
        if member.is_absolute() or ".." in member.parts or "\\" in name:
            raise RuntimeError(f"unsafe arXiv source archive member: {name}")
        if name in hashes:
            raise RuntimeError(f"duplicate arXiv source archive member: {name}")
        hashes[name] = hashlib.sha256(content).hexdigest()
    return dict(sorted(hashes.items()))


def _verify_isolated_source_build(
    source_archive: Path, *, expected_page_count: int | None = None
) -> dict[str, Any]:
    windows_tex = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    pdflatex = _optional_release_tool("pdflatex", windows_tex / "pdflatex.exe")
    tectonic = None if pdflatex else _optional_release_tool("tectonic")
    if pdflatex is None and tectonic is None:
        raise RuntimeError(
            "pdflatex or tectonic is unavailable for isolated source-bundle verification"
        )

    with tempfile.TemporaryDirectory(prefix="chemworld-arxiv-source-") as temporary:
        directory = Path(temporary)
        member_count = (
            _extract_verified_source_zip(source_archive, directory)
            if source_archive.suffix.lower() == ".zip"
            else _extract_verified_source_tar(source_archive, directory)
        )
        environment = os.environ.copy()
        environment["SOURCE_DATE_EPOCH"] = "1785628800"
        environment["FORCE_SOURCE_DATE"] = "1"
        command = (
            [tectonic, "-k", "--keep-logs", "main.tex"]
            if tectonic is not None
            else [
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-no-shell-escape",
                "main.tex",
            ]
        )
        pass_numbers = (1,) if tectonic is not None else (1, 2)
        for pass_number in pass_numbers:
            completed = subprocess.run(
                command,
                cwd=directory,
                env=environment,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if completed.returncode != 0:
                tail = "\n".join(completed.stdout.splitlines()[-100:])
                raise RuntimeError(
                    f"isolated arXiv source compile pass {pass_number} failed\n{tail}"
                )
        log = (directory / "main.log").read_text(encoding="utf-8", errors="replace")
        unresolved = re.findall(
            r"(?:Citation .* undefined|Reference .* undefined|undefined references)",
            log,
            flags=re.IGNORECASE,
        )
        if unresolved:
            raise RuntimeError(
                "isolated arXiv source compile has unresolved citations or references"
            )
        page_match = re.search(r"Output written on main\.(?:pdf|xdv) \((\d+) pages?", log)
        if page_match is None or (
            expected_page_count is not None and int(page_match.group(1)) != expected_page_count
        ):
            raise RuntimeError(
                "isolated arXiv source compile did not produce the expected page count"
            )
        pdf = directory / "main.pdf"
        if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("isolated arXiv source compile did not produce a valid PDF")
        overfull_warning_count = len(re.findall(r"Overfull \\[hv]box", log))
        if overfull_warning_count:
            raise RuntimeError(
                f"isolated arXiv source compile contains overfull boxes: {overfull_warning_count}"
            )
        return {
            "member_count": member_count,
            "page_count": int(page_match.group(1)),
            "underfull_warning_count": len(re.findall(r"Underfull \\[hv]box", log)),
            "overfull_warning_count": overfull_warning_count,
            "undefined_reference_count": 0,
            "shell_escape": "disabled",
        }


def verify_finalized_outputs(metadata: Mapping[str, Any]) -> dict[str, Any]:
    release = json.loads(RELEASE_MANIFEST.read_text(encoding="utf-8"))
    if release.get("status") != "publication_ready" or release.get("publication_ready") is not True:
        raise RuntimeError("release manifest did not enter publication_ready state")
    archived = release.get("evidence", {}).get("g0_raw_data_archive", {})
    for field in (
        "provider",
        "identifier",
        "url",
        "raw_file_index_sha256",
        "byte_count",
    ):
        if archived.get(field) != metadata["archive"].get(field):
            raise RuntimeError(f"release manifest archive field is stale: {field}")
    if archived.get("release_metadata_sha256") != _canonical_sha(metadata):
        raise RuntimeError("release manifest metadata hash is stale")

    build_manifest_path = ARXIV_EXPORT / "build-manifest.json"
    build = _verified_self_hashed_manifest(build_manifest_path)
    if build.get("status") != "compiled_arxiv_release" or int(build.get("pdf_page_count", 0)) < 10:
        raise RuntimeError("arXiv build manifest has an unexpected status or page count")
    build_file_count = _verify_file_rows(build.get("files"), label="arXiv build manifest")
    pdf = ROOT / build["pdf"]
    if not pdf.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("arXiv PDF signature is invalid")
    zip_path = ROOT / build["source_zip"]
    tar_path = ROOT / build["source_tar_gz"]
    zip_hashes = _archive_member_hashes(zip_path)
    tar_hashes = _archive_member_hashes(tar_path)
    zip_members = set(zip_hashes)
    required = {"main.tex", "main.bbl", "manuscript.md", "references.bib"}
    if zip_hashes != tar_hashes or not required <= zip_members:
        raise RuntimeError("arXiv source archives are incomplete or disagree")
    if not all(
        any(
            member.startswith(f"figures/figure-{number}-") and member.endswith(".pdf")
            for member in zip_members
        )
        for number in range(1, 4)
    ):
        raise RuntimeError("arXiv source archive is missing a release figure")
    isolated_source = {
        "zip": _verify_isolated_source_build(
            zip_path, expected_page_count=int(build["pdf_page_count"])
        ),
        "tar_gz": _verify_isolated_source_build(
            tar_path, expected_page_count=int(build["pdf_page_count"])
        ),
        "member_hashes_match": True,
    }

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bundled_manuscript = (ARXIV_EXPORT / "source" / "manuscript.md").read_text(encoding="utf-8")
    generated_tex = (ROOT / "paper" / "arxiv" / "main.tex").read_text(encoding="utf-8")
    if metadata["archive"]["url"] not in manuscript or metadata["archive"]["url"] not in (
        bundled_manuscript
    ):
        raise RuntimeError("archive URL is absent from the canonical or bundled manuscript")
    if "pdf_author:" not in manuscript or "correspondence:" not in manuscript:
        raise RuntimeError("canonical manuscript author metadata is incomplete")
    if "ChemWorld Authors" in generated_tex:
        raise RuntimeError("generated TeX still contains the author placeholder")
    if r"\textbackslash{[}" in generated_tex or r"\[0.35em]" not in generated_tex:
        raise RuntimeError("generated TeX has an escaped or missing author-block line break")
    return {
        "arxiv_pdf_pages": build["pdf_page_count"],
        "arxiv_bound_file_count": build_file_count,
        "source_archive_member_count": len(zip_members),
        "isolated_source_build": isolated_source,
    }


def apply_release_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    blockers = validate_release_metadata(metadata)
    if blockers:
        raise ValueError("release metadata is not ready:\n- " + "\n- ".join(blockers))
    preflight_blockers = apply_preflight_blockers()
    if preflight_blockers:
        raise RuntimeError(
            "release environment is incomplete:\n- " + "\n- ".join(preflight_blockers)
        )

    originals = {
        MANUSCRIPT: MANUSCRIPT.read_text(encoding="utf-8"),
        RELEASE_README: RELEASE_README.read_text(encoding="utf-8"),
        RELEASE_MANIFEST: RELEASE_MANIFEST.read_text(encoding="utf-8"),
    }
    generated_snapshot = _snapshot_generated_files()
    manifest = json.loads(originals[RELEASE_MANIFEST])
    manuscript = inject_archive_metadata(originals[MANUSCRIPT], metadata)
    readme = render_release_readme(originals[RELEASE_README], metadata)
    ready_manifest = finalized_manifest(manifest, metadata)

    try:
        _atomic_write_text(MANUSCRIPT, manuscript)
        _atomic_write_text(RELEASE_README, readme)
        _run([sys.executable, str(ARXIV_BUILDER)])
        _atomic_write_json(RELEASE_MANIFEST, ready_manifest)
        verification = verify_finalized_outputs(metadata)
    except BaseException:
        for path, value in originals.items():
            _atomic_write_text(path, value)
        _restore_generated_files(generated_snapshot)
        raise

    return {
        "status": "publication_ready",
        "publication_ready": True,
        "release_metadata_sha256": _canonical_sha(metadata),
        "manuscript": MANUSCRIPT.relative_to(ROOT).as_posix(),
        "release_manifest": RELEASE_MANIFEST.relative_to(ROOT).as_posix(),
        "arxiv_pdf": (
            "paper/exports/experimental-intelligence-v1-arxiv/"
            "chemworld-experimental-agency-arxiv.pdf"
        ),
        "verification": verification,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "blockers": [str(exc)]}, indent=2))
        return 2
    blockers = validate_release_metadata(metadata)
    if blockers:
        print(
            json.dumps(
                {"status": "blocked", "publication_ready": False, "blockers": blockers},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    if args.check:
        print(
            json.dumps(
                {
                    "status": "ready",
                    "publication_ready": False,
                    "release_metadata_sha256": _canonical_sha(metadata),
                    "next_action": "rerun with --apply after independently confirming the URL",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    try:
        result = apply_release_metadata(metadata)
    except Exception as exc:  # keep the CLI fail-closed and machine-readable
        try:
            publication_ready = bool(
                json.loads(RELEASE_MANIFEST.read_text(encoding="utf-8")).get(
                    "publication_ready", False
                )
            )
        except (OSError, json.JSONDecodeError):
            publication_ready = False
        print(
            json.dumps(
                {
                    "status": "build_failed",
                    "publication_ready": publication_ready,
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
