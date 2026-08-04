# Work I Task Claim

```yaml
task_id: W1-P09
title: "Refine and synchronize the six canonical publication figures"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:22:11Z
lease_expires_at_utc: 2026-08-06T05:20:37Z
heartbeat_at_utc: 2026-08-04T05:31:22Z

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
  - "Repaired the reported final-size defects: completed Figure 1 bottom boxes; separated Figure 4 labels and added the missing pass/fail key; routed Figure 5 arrows around nodes and cleared the observation/receipt text; separated Figure 6 legend, rows, boundary statement, and extreme recovery points."
  - "Re-rendered Figures 1, 4, 5, and 6; refreshed only the source bindings for Figures 2 and 3 because their rendered assets remained byte-identical."
current_validation: "PASS: nature-figure preflight for all four changed renderers (12 PASS, 2 accepted export-format warnings, 0 FAIL each); six final PNGs inspected once at original size; publication audit 6/6 figures and 18/18 assets (f00d11484f78ca18b860800301a0f28e8d021df3b82f99d23d5d1335609d639e); integration manifest 6/6 and 18/18 (298f19c14509013ba866e34af8adeffb1726e37453e27a805ff62c119d0a5988); focused figure tests 32/32 passed after correcting one stale byte-drift expectation; git diff --check passed."
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
next_24h: "Commit and accept this layout-only repair, then rebuild D07 exactly once against the corrected PDFs."
handoff_eta: 2026-08-04T05:35:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original P09 delivery was accepted on main at 410a4aab after final commit e940c765. The first refinement used nature-figure 2.1.1 without importing third-party visual assets or changing the frozen figure-system artifact. The project owner reopened P09 on 2026-08-04 after identifying final-size clipping and overlap in Figures 1, 4, 5 and 6; this repair changes layout only and is ready for centralized acceptance."
```
