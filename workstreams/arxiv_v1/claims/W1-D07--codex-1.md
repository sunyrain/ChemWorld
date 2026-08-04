# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: ACTIVE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T02:42:21Z
heartbeat_at_utc: 2026-08-04T03:37:31Z

base_commit: "ffd11ee7"
branch: work1/w1-d07-refined-figure-package-rebuild-codex-1
worktree: ../ChemWorld-W1-D07-Figure-C1
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

completed_since_last_heartbeat: []
current_validation: "P09 refined figures were accepted on main at ffd11ee7; the existing D07 package predates those asset hashes and must be rebuilt once."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Rebuild the arXiv/proof packages once against the accepted P09 assets, run focused package validation, and hand off."
handoff_eta: 2026-08-04T04:15:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original D07 package was accepted after final commit ea05a307. This explicit rebuild is required only because P09 publication-asset hashes changed. D07 still does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
