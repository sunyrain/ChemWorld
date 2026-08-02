"""Fail-closed finalization of the ChemWorld arXiv release.

The scientific artifacts can be built while public author metadata and a durable
raw-data archive are still pending.  This command is the only supported path for
crossing those two external release gates.  ``--check`` is read-only; ``--apply``
validates all metadata before changing any tracked source, rebuilds both paper
packages, and marks the release ready only after the focused release tests pass.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
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
        "release-artifact tests succeed.\n"
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


def apply_release_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    blockers = validate_release_metadata(metadata)
    if blockers:
        raise ValueError("release metadata is not ready:\n- " + "\n- ".join(blockers))

    originals = {
        MANUSCRIPT: MANUSCRIPT.read_text(encoding="utf-8"),
        RELEASE_README: RELEASE_README.read_text(encoding="utf-8"),
        RELEASE_MANIFEST: RELEASE_MANIFEST.read_text(encoding="utf-8"),
    }
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
        _run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests/test_arxiv_release_artifacts.py",
                "--no-cov",
            ]
        )
    except Exception:
        for path, value in originals.items():
            _atomic_write_text(path, value)
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
