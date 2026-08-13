# Final raw-archive attachment

The current arXiv package and public author/affiliation block are complete. One
external input remains: a durable archive identifier for the indexed 17.7 GB G0
raw roots. The canonical manuscript remains the sole authority for author,
affiliation and correspondence metadata.

Copy `release-metadata.pending.json` to a private working path and fill it using
this shape:

```json
{
  "schema_version": "chemworld-arxiv-archive-metadata-0.2",
  "status": "ready",
  "archive": {
    "provider": "Repository name",
    "identifier": "10.0000/example.identifier",
    "url": "https://doi.org/10.0000/example.identifier",
    "publicly_resolvable": true,
    "raw_file_index_sha256": "f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961",
    "byte_count": 17725724603
  }
}
```

Validate without changing the repository:

```powershell
uv run --extra paper python paper/tools/finalize_arxiv_release.py `
  --metadata D:\secure\chemworld-release-metadata.json --check
```

After the archive record resolves publicly, apply the metadata and rebuild the
upload package:

```powershell
uv run --extra paper python paper/tools/finalize_arxiv_release.py `
  --metadata D:\secure\chemworld-release-metadata.json --apply
```

Before setting `publicly_resolvable` to `true`, the operator must open the archive
URL in an unauthenticated session and confirm that the public record exposes the
indexed deposit. The tool rejects placeholders, non-HTTPS archive URLs, an absent
operator confirmation, mismatched raw-index identity and mismatched byte count. It
does not accept or rewrite author metadata. It marks the release ready only after
the archive citation is written, the current arXiv package rebuilds, and the built-in
release integrity verifier passes. The verifier also extracts both the source ZIP and source
TAR.GZ into separate isolated temporary directories, verifies byte-identical member
contents, and compiles each package twice with shell escape disabled, rejecting
missing files and unresolved citations or references. Missing paper-render dependencies
are rejected before any mutation. If any
later build or integrity verification fails, the canonical source/status files and all generated
PDF/source artifacts are restored byte-for-byte, and `publication_ready`
retains its pre-run value.
