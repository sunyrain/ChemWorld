# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T05:32:16Z
heartbeat_at_utc: 2026-08-04T05:37:49Z

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
  - "Rebuilt the 17-page arXiv PDF and both deterministic source archives against accepted P09 repair 5c3595b9fafc418a6eccace2e75bd4d42d943489."
  - "Inspected the rebuilt Figure 6 page once at 150 dpi; the Figure 6C y-axis title and every panel boundary are complete."
current_validation: "PASS: arXiv builder completed once after the final P09 repair; 17 pages; build manifest adc96df3a5e17cdac8789062541c9b4c899583c1b468ddd6c757ba20d7f7717f; PDF 06982ca0acb2f1f463e9a75a17248141e22ca630d8e6a95313013b6f903d5938; ZIP 1ac9069798957b43b505eb8b13d96e4e4c7cb61e743f0ca23d9d2e62def79467; TAR.GZ 885d19c3a90c4632a71d9f0e9562834b667ae2086c69772d98cd8a584083cce9; targeted page-level visual inspection and git diff --check passed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-publication-proof.pdf
  - paper/exports/experimental-intelligence-v1/publication-proof-manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Commit and accept the final package centrally; no further build or review pass planned."
handoff_eta: 2026-08-04T05:39:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original D07 package was accepted after final commit ea05a307 and the first refined-figure rebuild after 4ea352cf. This second reopening was limited to refreshing the arXiv package against accepted P09 repairs 4262c18d and 5c3595b9; it does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
