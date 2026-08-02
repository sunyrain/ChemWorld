"""Fail-closed finalization of the ChemWorld arXiv release.

The scientific artifacts can be built while public author metadata and a durable
raw-data archive are still pending.  This command is the only supported path for
crossing those two external release gates.  ``--check`` is read-only; ``--apply``
validates all metadata before changing any tracked source, rebuilds both paper
packages, and marks the release ready only after output integrity verification passes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tarfile
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper" / "experimental_intelligence_v1_manuscript.md"
RELEASE_README = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "README.md"
RELEASE_MANIFEST = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "manifest.json"
ARXIV_BUILDER = ROOT / "paper" / "tools" / "build_arxiv_release.py"
PROOF_BUILDER = ROOT / "paper" / "tools" / "render_publication_v1_pdf.py"
ARXIV_BUILD = ROOT / "paper" / "arxiv" / "build"
ARXIV_EXPORT = ROOT / "paper" / "exports" / "experimental-intelligence-v1-arxiv"
PROOF_EXPORT = ROOT / "paper" / "exports" / "experimental-intelligence-v1"
GENERATED_ROLLBACK_TARGETS = (
    ROOT / "paper" / "arxiv" / "main.tex",
    ROOT / "paper" / "arxiv" / "references.bib",
    ARXIV_BUILD,
    ARXIV_EXPORT,
    PROOF_EXPORT,
)

SCHEMA = "chemworld-arxiv-release-metadata-0.1"
EXPECTED_RAW_INDEX_SHA256 = "f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961"
EXPECTED_RAW_BYTE_COUNT = 17_725_724_603
EXPECTED_RAW_FILE_COUNT = 1_441

_ORCID = re.compile(r"^\d{4}-\d{4}-\d{4}-[\dX]{4}$")
_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_AFFILIATION_ID = re.compile(r"^[A-Za-z0-9._-]+$")
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


def _orcid_checksum_valid(value: str) -> bool:
    if _ORCID.fullmatch(value) is None:
        return False
    digits = value.replace("-", "")
    total = 0
    for character in digits[:15]:
        total = (total + int(character)) * 2
    result = (12 - total % 11) % 11
    check = "X" if result == 10 else str(result)
    return digits[-1] == check


def validate_release_metadata(metadata: Any) -> list[str]:
    """Return deterministic blockers; an empty list means the release inputs are ready."""
    blockers: list[str] = []
    if not isinstance(metadata, Mapping):
        return ["metadata must be a JSON object"]
    expected_keys = {"schema_version", "status", "authors", "affiliations", "archive"}
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

    affiliations = metadata.get("affiliations")
    affiliation_ids: set[str] = set()
    if not isinstance(affiliations, list) or not affiliations:
        blockers.append("at least one affiliation is required")
        affiliations = []
    for index, affiliation in enumerate(affiliations):
        prefix = f"affiliations[{index}]"
        if not isinstance(affiliation, Mapping):
            blockers.append(f"{prefix} must be an object")
            continue
        unknown_fields = sorted(set(affiliation) - {"id", "name"})
        if unknown_fields:
            blockers.append(f"{prefix} has unknown fields: {', '.join(unknown_fields)}")
        affiliation_id = affiliation.get("id")
        if not isinstance(affiliation_id, str) or _AFFILIATION_ID.fullmatch(affiliation_id) is None:
            blockers.append(f"{prefix}.id must be a non-empty alphanumeric identifier")
        elif affiliation_id in affiliation_ids:
            blockers.append(f"duplicate affiliation id: {affiliation_id}")
        else:
            affiliation_ids.add(affiliation_id)
        if not _nonplaceholder(affiliation.get("name")):
            blockers.append(f"{prefix}.name must be public and non-placeholder")

    authors = metadata.get("authors")
    corresponding_count = 0
    if not isinstance(authors, list) or not authors:
        blockers.append("at least one author is required")
        authors = []
    for index, author in enumerate(authors):
        prefix = f"authors[{index}]"
        if not isinstance(author, Mapping):
            blockers.append(f"{prefix} must be an object")
            continue
        allowed = {"name", "affiliation_ids", "corresponding", "email", "orcid"}
        unknown_fields = sorted(set(author) - allowed)
        if unknown_fields:
            blockers.append(f"{prefix} has unknown fields: {', '.join(unknown_fields)}")
        if not _nonplaceholder(author.get("name")):
            blockers.append(f"{prefix}.name must be public and non-placeholder")
        ids = author.get("affiliation_ids")
        if not isinstance(ids, list) or not ids:
            blockers.append(f"{prefix}.affiliation_ids must contain at least one id")
        else:
            for affiliation_id in ids:
                if not isinstance(affiliation_id, str) or affiliation_id not in affiliation_ids:
                    blockers.append(
                        f"{prefix}.affiliation_ids references unknown id: {affiliation_id!r}"
                    )
        corresponding = author.get("corresponding")
        if corresponding is True:
            corresponding_count += 1
            email = author.get("email")
            if (
                not _nonplaceholder(email)
                or not isinstance(email, str)
                or _EMAIL.fullmatch(email) is None
            ):
                blockers.append(f"{prefix}.email must be a public corresponding-author email")
        elif corresponding is not False:
            blockers.append(f"{prefix}.corresponding must be true or false")
        orcid = author.get("orcid")
        if orcid not in (None, "") and (
            not isinstance(orcid, str) or not _orcid_checksum_valid(orcid)
        ):
            blockers.append(f"{prefix}.orcid has invalid syntax or checksum")
    if corresponding_count != 1:
        blockers.append("exactly one corresponding author is required")

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


def _latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def _yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _markdown_escape(value: str) -> str:
    for character in ("\\", "[", "]", "*", "_"):
        value = value.replace(character, "\\" + character)
    return value


def render_author_metadata(metadata: Mapping[str, Any]) -> tuple[str, str, list[str]]:
    """Return PDF author metadata, the LaTeX title block, and plain author names."""
    authors = metadata["authors"]
    affiliations = metadata["affiliations"]
    names = [str(author["name"]).strip() for author in authors]
    rendered_names: list[str] = []
    for author in authors:
        markers = [str(value) for value in author["affiliation_ids"]]
        if author["corresponding"]:
            markers.append("*")
        rendered_names.append(
            f"{_latex_escape(str(author['name']).strip())}"
            rf"\textsuperscript{{{','.join(markers)}}}"
        )
    lines = [", ".join(rendered_names) + r"\\[0.35em]"]
    for affiliation in affiliations:
        lines.append(
            rf"\small \textsuperscript{{{_latex_escape(str(affiliation['id']))}}}"
            f"{_latex_escape(str(affiliation['name']).strip())}" + r"\\"
        )
    corresponding = next(author for author in authors if author["corresponding"])
    lines.append(
        r"\small *Correspondence: \texttt{"
        + _latex_escape(str(corresponding["email"]).strip())
        + "}"
    )
    return "; ".join(names), " ".join(lines), names


def inject_manuscript_metadata(text: str, metadata: Mapping[str, Any]) -> str:
    pdf_author, author_block, names = render_author_metadata(metadata)
    replacements = {
        "pdf_author": _yaml_quote(pdf_author),
        "author_block": _yaml_quote(author_block),
    }
    updated = text
    for key, value in replacements.items():
        pattern = rf"(?m)^{re.escape(key)}:\s*.*$"
        replacement = f"{key}: {value}"
        updated, count = re.subn(
            pattern,
            lambda _match, replacement=replacement: replacement,
            updated,
            count=1,
        )
        if count != 1:
            raise ValueError(f"manuscript front matter is missing {key}")
    author_lines = "author:\n" + "".join(f"  - {_yaml_quote(name)}\n" for name in names)
    updated, count = re.subn(
        r"(?m)^author:\s*\n(?:\s{2}-[^\n]*\n)+",
        lambda _match: author_lines,
        updated,
        count=1,
    )
    if count != 1:
        raise ValueError("manuscript front matter is missing the author list")

    archive = metadata["archive"]
    provider = _markdown_escape(str(archive["provider"]))
    identifier = _markdown_escape(str(archive["identifier"]))
    new_paragraph = (
        f"The indexed 17.7-GB G0 raw roots are publicly archived by "
        f"{provider} under [{identifier}]({archive['url']}). "
        f"The deposit is bound to the tracked {EXPECTED_RAW_FILE_COUNT:,}-file index by "
        f"SHA-256 `{EXPECTED_RAW_INDEX_SHA256}` and contains "
        f"{EXPECTED_RAW_BYTE_COUNT:,} bytes. The tracked world-level summaries and "
        "derived-data object regenerate the paper's reported analyses."
    )
    availability_pattern = re.compile(
        r"(?:"
        r"The 17\.7-GB G0 raw roots are bound by the public file-level hash index but are not\n"
        r"included in the repository and have not yet received a durable external archive\n"
        r"identifier; raw-byte access is therefore not presently available from a permanent\n"
        r"archive\. The tracked world-level summaries and derived-data object are sufficient\n"
        r"to regenerate the paper's reported analyses\."
        r"|"
        r"The indexed 17\.7-GB G0 raw roots are publicly archived by .*?"
        r"derived-data object regenerate the paper's reported analyses\."
        r")",
        flags=re.DOTALL,
    )
    updated, count = availability_pattern.subn(new_paragraph, updated, count=1)
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
        "affiliation and correspondence metadata have been injected into the manuscript, and "
        "the release manifest is marked ready only after the standard PDF/source rebuild and "
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
    updated["gates"]["author_metadata"] = (
        "passed_public_author_affiliation_and_correspondence_block"
    )
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


def apply_preflight_blockers() -> list[str]:
    blockers: list[str] = []
    if importlib.util.find_spec("markdown") is None:
        blockers.append(
            "Python package 'markdown' is unavailable; run with "
            "`uv run --extra paper python paper/tools/finalize_arxiv_release.py ...`"
        )
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
    if build.get("status") != "compiled_arxiv_release" or build.get("pdf_page_count") != 11:
        raise RuntimeError("arXiv build manifest has an unexpected status or page count")
    build_file_count = _verify_file_rows(build.get("files"), label="arXiv build manifest")
    pdf = ROOT / build["pdf"]
    if not pdf.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("arXiv PDF signature is invalid")
    zip_path = ROOT / build["source_zip"]
    tar_path = ROOT / build["source_tar_gz"]
    with zipfile.ZipFile(zip_path) as archive:
        zip_members = set(archive.namelist())
    with tarfile.open(tar_path, mode="r:gz") as archive:
        tar_members = {member.name for member in archive.getmembers() if member.isfile()}
    required = {"main.tex", "main.bbl", "manuscript.md", "references.bib"}
    if zip_members != tar_members or not required <= zip_members:
        raise RuntimeError("arXiv source archives are incomplete or disagree")
    if not all(
        any(
            member.startswith(f"figures/figure-{number}-") and member.endswith(".pdf")
            for member in zip_members
        )
        for number in range(1, 7)
    ):
        raise RuntimeError("arXiv source archive is missing a release figure")

    proof = _verified_self_hashed_manifest(PROOF_EXPORT / "publication-proof-manifest.json")
    if proof.get("status") != "publication_ready" or proof.get("publication_ready") is not True:
        raise RuntimeError("publication proof did not enter publication_ready state")
    proof_output_count = _verify_file_rows(proof.get("outputs"), label="publication proof manifest")
    _verify_file_rows(proof.get("sources"), label="publication proof sources")

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bundled_manuscript = (ARXIV_EXPORT / "source" / "manuscript.md").read_text(encoding="utf-8")
    generated_tex = (ROOT / "paper" / "arxiv" / "main.tex").read_text(encoding="utf-8")
    for author in metadata["authors"]:
        name = str(author["name"])
        if name not in manuscript or name not in bundled_manuscript:
            raise RuntimeError(f"author is absent from canonical or bundled manuscript: {name}")
        if _latex_escape(name) not in generated_tex:
            raise RuntimeError(f"author is absent from generated TeX: {name}")
    if metadata["archive"]["url"] not in manuscript or metadata["archive"]["url"] not in (
        PROOF_EXPORT / "experimental-intelligence-v1-publication-proof.html"
    ).read_text(encoding="utf-8"):
        raise RuntimeError("archive URL is absent from a final publication artifact")
    if "ChemWorld Authors" in generated_tex:
        raise RuntimeError("generated TeX still contains the author placeholder")
    return {
        "arxiv_pdf_pages": build["pdf_page_count"],
        "arxiv_bound_file_count": build_file_count,
        "source_archive_member_count": len(zip_members),
        "publication_proof_output_count": proof_output_count,
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
    manuscript = inject_manuscript_metadata(originals[MANUSCRIPT], metadata)
    readme = render_release_readme(originals[RELEASE_README], metadata)
    ready_manifest = finalized_manifest(manifest, metadata)

    try:
        _atomic_write_text(MANUSCRIPT, manuscript)
        _atomic_write_text(RELEASE_README, readme)
        _run([sys.executable, str(ARXIV_BUILDER)])
        _atomic_write_json(RELEASE_MANIFEST, ready_manifest)
        _run([sys.executable, str(PROOF_BUILDER)])
        verification = verify_finalized_outputs(metadata)
    except Exception:
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
