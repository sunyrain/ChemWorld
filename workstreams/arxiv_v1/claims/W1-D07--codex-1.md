# Work I Task Claim

```yaml
task_id: W1-D07
title: "Build the standard arXiv PDF, source bundles, and publication proof"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:42:21Z
lease_expires_at_utc: 2026-08-06T07:39:42Z
heartbeat_at_utc: 2026-08-04T07:54:27Z

base_commit: "54bdea84857a53e8d05a5da5660a24e9f4b7c5cd"
branch: main
worktree: D:/Projects/ChemWorld
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/tools/build_arxiv_release.py
  - paper/tools/finalize_arxiv_release.py
  - paper/tools/render_publication_v1_pdf.py
  - paper/arxiv/template.tex
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
  - "Rebuilt the Q07-cleaned package as a 19-page two-column PDF and synchronized deterministic ZIP/TAR.GZ source bundles plus the publication proof."
  - "Corrected directly observed Appendix C identifier overflow and bound the Appendix D label to its full-width coverage table."
  - "Visually accepted the title page and pages 17--19; author metadata, long identifiers, table caption, matrix, and references are complete with no overlap or clipping."
current_validation: "PASS: PDF SHA-256 b9899284da98c9f16aed33a4dc374c41ce6dc8c8aed7a2067a4f7676954ff974; build-manifest file SHA-256 6c7d3525d79deb1f116be332c36e1cb4c1cf07071b1d12ab340992b55c4a31cb; publication-proof PDF SHA-256 a161cb6924395aada032f272176ea4a34503e95ede93c145d286e545409bc165. Focused package contracts passed after three stale string/injection expectations were synchronized; Ruff and git diff --check passed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D07--codex-1.md
  - paper/exports/experimental-intelligence-v1-arxiv/
  - paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-publication-proof.pdf
  - paper/exports/experimental-intelligence-v1/publication-proof-manifest.json
  - paper/arxiv/template.tex
  - paper/tools/finalize_arxiv_release.py
  - paper/tools/render_publication_v1_pdf.py
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Accepted on main; no further D07 package work is pending."
handoff_eta: null

final_commit: "012de711"
reviewer: "codex-1 centralized coordinator acceptance"
review_result: "APPROVE: current 19-page PDF and self-contained source bundles reflect the supplied-review cleanup and pass targeted package, lint, integrity, and visual checks."
notes: "The original D07 package was reopened only to synchronize accepted Q07 cleanup and correct two directly observed appendix layout defects. This does not mark publication_ready and does not require the deferred 17.7 GB archive or unresolved corresponding-author metadata. The historical D08 independent-checkout attestation remains unchanged."
```
