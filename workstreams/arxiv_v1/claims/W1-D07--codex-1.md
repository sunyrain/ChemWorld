# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: ACTIVE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T05:32:16Z
heartbeat_at_utc: 2026-08-04T05:36:43Z

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

completed_since_last_heartbeat:
  - "Rebuilt the 17-page two-column arXiv PDF with the six accepted P09 refined PDFs."
  - "Rebuilt deterministic ZIP and TAR.GZ source bundles and synchronized all six bundled figure hashes."
  - "Rebuilt the publication proof PDF and its self-hashed manifest against the accepted refined SVGs."
current_validation: "ACTIVE after accepted final P09 repair 5c3595b9fafc418a6eccace2e75bd4d42d943489; package will be regenerated once against the complete Figure 6C margin."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-publication-proof.pdf
  - paper/exports/experimental-intelligence-v1/publication-proof-manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Rebuild the arXiv package once against the corrected P09 PDFs, then accept centrally."
handoff_eta: 2026-08-04T05:40:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original D07 package was accepted after final commit ea05a307 and the first refined-figure rebuild after 4ea352cf. This second reopening is limited to refreshing the arXiv package against accepted P09 repair 4262c18d; it does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
