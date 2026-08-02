# Final arXiv release metadata

The scientific package is frozen and internally attested. Two external inputs
remain before upload: the public author/affiliation block and a durable archive
identifier for the indexed 17.7 GB G0 raw roots.

Copy `release-metadata.pending.json` to a private working path and fill it using
this shape:

```json
{
  "schema_version": "chemworld-arxiv-release-metadata-0.1",
  "status": "ready",
  "authors": [
    {
      "name": "Full Name",
      "affiliation_ids": ["1"],
      "corresponding": true,
      "email": "name@example.edu",
      "orcid": "0000-0000-0000-0000"
    }
  ],
  "affiliations": [
    {
      "id": "1",
      "name": "Department, Institution, City, Postal Code, Country"
    }
  ],
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
indexed deposit. The tool rejects placeholders, missing affiliations, invalid
ORCIDs, non-HTTPS archive URLs, an absent operator confirmation, mismatched
raw-index identity, mismatched byte count, and the absence of exactly one
corresponding author. It marks the release ready only after the author block and
archive citation are written, both paper packages rebuild, and the release tests
pass. A missing paper-render dependency is rejected before any mutation. If any
later build or test fails, the canonical source/status files and all generated
PDF/source/proof artifacts are restored byte-for-byte, and `publication_ready`
retains its pre-run value.
