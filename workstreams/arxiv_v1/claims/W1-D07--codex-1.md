# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: ACTIVE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T07:39:42Z
heartbeat_at_utc: 2026-08-04T07:39:42Z

base_commit: "54bdea84857a53e8d05a5da5660a24e9f4b7c5cd"
branch: main
worktree: D:/Projects/ChemWorld
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
  - "Rebuilt the 17-page arXiv PDF and both deterministic source archives against accepted P09 repair 5c3595b9fafc418a6eccace2e75bd4d42d943489."
  - "Inspected the rebuilt Figure 6 page once at 150 dpi; the Figure 6C y-axis title and every panel boundary are complete."
  - "Rebuilt the 17-page arXiv PDF and deterministic source archives against accepted S10 instrument-release / Work II explanatory-boundary prose."
  - "Inspected the rebuilt abstract, Discussion and complete two-page Conclusion continuation at 150 dpi; no overflow, clipping or incomplete text was introduced."
current_validation: "Pending one package rebuild against accepted Q07 review cleanup commit 54bdea84."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-publication-proof.pdf
  - paper/exports/experimental-intelligence-v1/publication-proof-manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Rebuild the arXiv package once, run focused tests once, and inspect only pages affected by the new title, tables and appendices."
handoff_eta: 2026-08-04T08:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original D07 package was accepted after final commit ea05a307 and subsequent figure and S10 synchronized rebuilds. This reopening changes package bytes only for accepted Q07 manuscript cleanup commit 54bdea84. It does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
