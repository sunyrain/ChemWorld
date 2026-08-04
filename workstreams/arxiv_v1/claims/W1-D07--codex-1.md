# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T06:51:18Z
heartbeat_at_utc: 2026-08-04T06:53:30Z

base_commit: "2171372dbcd03e2aebf169ca26dfcb181301c580"
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
current_validation: "PASS: arXiv builder completed once; 17 pages; build manifest b185f84bca33e8e60cf21c19f6cffa973cdecef1eb51543975078c5791daec11; PDF 406d9a26eb89668b5833c66d0a1fa7f11a9edfbddae0db69c1ea63c9ebaa705a; ZIP 92b105b4fa9752b7afbe70d367852ad344a18eab38b21f814bdd983fec2b8996; TAR.GZ c2f88616513010ad1f7501c23f8917207a82f3ded32550458236e2c489ac1877; targeted visual inspection and git diff --check passed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-publication-proof.pdf
  - paper/exports/experimental-intelligence-v1/publication-proof-manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Commit and accept the final manuscript package centrally."
handoff_eta: 2026-08-04T06:56:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original D07 package was accepted after final commit ea05a307 and subsequent figure-synchronized rebuilds. This reopening changes only manuscript/package bytes for accepted S10 commit 2171372d; it does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata."
```
