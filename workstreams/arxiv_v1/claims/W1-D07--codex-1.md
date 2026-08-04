# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T02:42:21Z
heartbeat_at_utc: 2026-08-04T02:46:29Z

base_commit: "410a4aab"
branch: work1/w1-d07-arxiv-package-codex-1
worktree: ../ChemWorld-W1-D07-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/tools/build_arxiv_release.py
  - paper/tools/render_publication_v1_pdf.py
  - tests/test_arxiv_release_artifacts.py
  - tests/test_publication_v1_artifacts.py
  - paper/arxiv/main.tex
  - paper/arxiv/references.bib
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
shared_hot_file_requests:
  - "Exclusive D07 reservation: tracked arXiv and publication-proof export directories."

deliverables:
  - "Compiled two-column arXiv PDF using the integrated manuscript and canonical P09 figures"
  - "Deterministic self-contained ZIP and TAR.GZ source bundles"
  - "Rebuilt publication proof and self-hashed proof/build manifests"
  - "Release metadata updated with the actual compiled page count while external gates remain open"
validation:
  - "Run each package builder once"
  - "Run focused arXiv/proof artifact tests, Ruff, and git diff --check once"

completed_since_last_heartbeat:
  - "Rebuilt the standard two-column arXiv PDF from the integrated manuscript; the compiled artifact is 17 pages."
  - "Replaced the superseded source-bundle figures with the six canonical P09 PDFs and rebuilt deterministic ZIP/TAR.GZ archives."
  - "Rebuilt the working publication proof against the canonical P09 SVGs and synchronized display legends."
  - "Updated the data card and release manifest with the programmable-world title and actual page count while leaving external gates open."
current_validation: "PASS: 10 focused arXiv/proof artifact tests; Ruff; git diff --check; both package builders completed successfully once."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/tools/build_arxiv_release.py
  - paper/tools/render_publication_v1_pdf.py
  - tests/test_arxiv_release_artifacts.py
  - tests/test_publication_v1_artifacts.py
  - paper/arxiv/main.tex
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator acceptance and main integration."
handoff_eta: 2026-08-04T02:55:00Z

final_commit: ea05a307
reviewer: codex-1
review_result: PASS
notes: "D07 does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
