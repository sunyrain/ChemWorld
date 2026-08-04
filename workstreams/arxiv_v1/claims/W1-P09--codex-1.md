# Work I Task Claim

```yaml
task_id: W1-P09
title: "Refine and synchronize the six canonical publication figures"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:22:11Z
lease_expires_at_utc: 2026-08-06T03:16:09Z
heartbeat_at_utc: 2026-08-04T03:36:11Z

base_commit: "e82b60df744493c2f31f848328ad42c26b08344d"
branch: work1/w1-p09-nature-figure-refinement-codex-1
worktree: ../ChemWorld-W1-P09-Nature-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
  - scripts/render_work_i_figure_1.py
  - tests/test_work_i_figure_1.py
  - scripts/render_work_i_figure_2.py
  - tests/test_work_i_figure_2.py
  - scripts/render_work_i_figure_3.py
  - tests/test_work_i_figure_3.py
  - scripts/render_work_i_figure_4.py
  - tests/test_work_i_figure_4.py
  - scripts/render_work_i_figure_5.py
  - tests/test_work_i_figure_5.py
  - scripts/render_work_i_figure_6.py
  - tests/test_work_i_figure_6.py
  - scripts/audit_work_i_publication_figures.py
  - tests/test_work_i_publication_figure_audit.py
  - scripts/audit_work_i_figure_integration.py
  - tests/test_work_i_figure_integration.py
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.*
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.*
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.*
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.*
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.*
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.*
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.json
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.md
  - paper/figures/experimental-intelligence-v1/work-i-publication-figure-manifest-v0.1.json
shared_hot_file_requests:
  - "Exclusive P09 reservation: paper/figures/experimental-intelligence-v1/ and canonical figure-integration outputs."
  - "The frozen paper/arxiv/figure-manifest.json remains a superseded migration input and will not be rewritten."

deliverables:
  - "Six refined canonical figures with a restrained semantic palette, lowercase panel labels, clearer evidence hierarchy, and readable final-size typography."
  - "Editable SVG and TrueType PDF exports plus 300 dpi PNG previews for all six figures."
  - "No change to frozen evidence, statistics, counting rules, exclusions, or manuscript claim boundaries."
  - "Updated per-figure manifests, publication audit, and canonical self-hashed 18-asset inventory."
validation:
  - "Run the six deterministic renderers once and their focused tests once."
  - "Run nature-figure static preflight once over all six plotting sources."
  - "Run publication/integration audits, Ruff, Mypy, and git diff --check once."
  - "Inspect all six final PNG previews once at publication size."

completed_since_last_heartbeat:
  - "Applied the nature-figure contract to all six canonical figures: lowercase 8.5 pt panel labels, concise claim-led headings, lighter subordinate grids, and consistent final-width typography."
  - "Preserved every frozen value, denominator, unresolved unit, censoring mark, uncertainty definition, and claim boundary; no scientific analysis was rerun."
  - "Made F1/F2 validate the immutable D01 interface freeze plus their task-specific bound sources, instead of rebuilding that pre-outcome contract from a later append-only coordinator ledger."
  - "Made F5 validate its frozen G2 v0.4 layer rather than require unrelated later ledger sections to reproduce the older whole-file bytes."
  - "Rebuilt six SVG/PDF/PNG sets, six per-figure manifests, the publication audit, and the canonical 18-asset inventory."
current_validation: "PASS: nature-figure preflight 12 PASS / 2 accepted WARN / 0 FAIL per renderer; publication audit 6/6 figures and 18/18 assets; focused tests covered 32 cases (31 passed initially, one stale F4 byte-integrity assertion updated, affected F4 suite 4/4 passed); Ruff; Mypy --explicit-package-bases; git diff --check; one final six-figure visual inspection plus one targeted F4 label-position confirmation. Accepted warnings: TIFF omitted and PNG limited to 300 dpi because editable SVG/PDF are the frozen submission masters and PNG is review-only."
files_touched:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
  - scripts/render_work_i_figure_1.py
  - scripts/render_work_i_figure_2.py
  - scripts/render_work_i_figure_3.py
  - scripts/render_work_i_figure_4.py
  - scripts/render_work_i_figure_5.py
  - scripts/render_work_i_figure_6.py
  - tests/test_work_i_figure_1.py
  - tests/test_work_i_figure_4.py
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.*
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.*
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.*
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.*
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.*
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.*
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.json
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.md
  - paper/figures/experimental-intelligence-v1/work-i-publication-figure-manifest-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Accepted on main; rebuild D07 against the refined asset hashes before resuming D08."
handoff_eta: 2026-08-04T03:35:00Z

final_commit: 2ad976c9
reviewer: codex-1
review_result: PASS
notes: "The original P09 delivery was accepted on main at 410a4aab after final commit e940c765. This project-owner-requested refinement used nature-figure 2.1.1 without importing third-party visual assets or changing the frozen figure-system artifact. The canonical publication audit is 6146773abc8cbd30775130e1f7aca88109d26c2efc587b6a27ad1ef514617fec; the integrated 18-asset manifest is d03e857d32d1dca075df9510adfa2da69b4c39be5960a31f65bfe1921be4b34d. Centralized coordinator acceptance merged at ccf01906."
```
