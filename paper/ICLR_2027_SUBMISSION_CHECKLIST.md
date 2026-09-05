# ICLR 2027 submission checklist

Updated: 2026-09-05. This file owns format, deadlines, anonymity and delivery.
Scientific results belong in the [results index](../workstreams/flagship_tasks/WORK_II_PAPER_RESULTS_ZH.md);
new experiments belong in the [matrix](../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md);
execution status belongs in [Work II TODO](../workstreams/flagship_tasks/WORK_II_TODOLIST.md).

## Official requirements

Checked against the official [Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers)
and [Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines) on 2026-09-05.
Recheck these and the [AI policy](https://iclr.cc/Conferences/2027/AIPolicyForAuthors) before submitting.

| Item | Requirement |
| --- | --- |
| Abstract deadline | 2026-09-18 23:59 AoE; Beijing 2026-09-19 19:59 |
| Full paper deadline | 2026-09-25 23:59 AoE; Beijing 2026-09-26 19:59 |
| Initial review main text | At most nine pages; references/appendix follow official rules |
| Format | Official ICLR 2027 style, anonymous review mode |
| Identity | No author names, affiliations, acknowledgements or identifying repository links in the anonymous PDF/supplement |
| Statements | Required AI-use statement; reproducibility and limitations; anonymous code/data availability |
| Scientific metadata | Exact internal identifiers and provenance in evidence records, not reader-facing prose or figures |

The 2027 reviewer-guide URL returned 404 at this check. Prior-year review guidance can inform
research judgment but supplies neither current requirements nor a spotlight selection formula.

## Maintained sources and display scope

- Venue-neutral long draft: [prior_discovery_manuscript.md](prior_discovery_manuscript.md).
- Anonymous submission: [iclr2027/submission.md](iclr2027/submission.md), with
  [appendix](iclr2027/appendix.md). This is a separately maintained compact source.
- Shared [bibliography](prior_discovery_references.bib),
  [display plan](prior_discovery_display_items.md) and
  [claim/evidence map](prior_discovery_evidence_map.md).
- The long draft uses eight figure assets; the compact source selects assets 1 and 3–8,
  with B2/B3 and M1 figures in the appendix and M3 in the main text. Historical values and
  failure denominators are retained.
- The independent-world factorial block has completed with 120/120 sessions and 160/160 slots.
  The primary material benefit was unsupported; the development canary remains separate.
  Both drafts report the actual result. M3 separately supports artifact-only same-world utility;
  changed-physical-condition transfer remains untested.

## Delivery state

- [x] Official style imported and anonymous build established.
- [x] Existing data, figure assets and anonymous supplementary package prepared.
- [x] Previous 30 bibliography entries source-checked on 2026-09-03.
- [x] Two decision-focused-learning references added and DOI metadata checked on 2026-09-05.
- [x] Rebuild and visually inspect both drafts after the current story cleanup.
- [ ] Confirm the title, author order and OpenReview profiles before the abstract deadline.
- [ ] Confirm reciprocal-review eligibility, exemptions and current AI-policy compliance.
- [ ] Freeze the actual submission evidence and complete final anonymous delivery checks.
- [ ] Submit through OpenReview (user action; not performed by repository cleanup).

The M3 integration builds contain nine main-text pages and 23 total pages in the anonymous
submission, and 22 pages in the long draft. All 45 pages were rendered and visually checked;
the final M3 figure, tables and author/abstract page also passed page-scale inspection. Fonts
were not reduced to meet the main-text limit. Final builds report no horizontal/vertical
overflow, undefined citations, unstable cross-references or anonymous identity leaks.

The focused publication pass has 18 passing tests, with Ruff and diff checks clean.
The supplementary archive contains 65 files. Its M1/M3 standalone verifiers reconstruct scheduled
denominators, deterministic controls, all selection losses and eleven paired means. The full NumPy
checks reconstruct public fits, exact maximizer choices and all eleven bootstrap intervals;
M3 also verifies source reuse and recipient information isolation. Both actual exported full
verifiers passed. The M3 execution surface separately passed 36 focused checks before freeze
and its final source-binding check. Build metadata do not create new experimental outcomes or
relabel the formal source blocks.

M1 completed 200/200 physical executions and exact replays, 120/120 provider sessions and 160/160
condition slots, without failure or replacement. F-X minus L-X was −0.00538 (95% interval
[−0.01630,+0.00061]); the material-benefit criterion was not met. F-A/F-X choices agreed 40/40,
and the nearest-evidence baseline was competitive. M3 completed 160/160 recipients and 80/80
new hidden executions/replays with no failure, retry or replacement. L−none was −0.13723
(95% interval [−0.15584,−0.12257]), supporting material benefit; nearest achieved zero regret
in all ten reused worlds. There are zero additional independent worlds, and no raw/retrieval
superiority or equivalence claim. M2/M4 and changed-mechanism experiments were not executed.
Repository completion does not constitute actual OpenReview submission.

Author metadata remain Jiangjie Qiu, Yijun Li, Yaotian Yang, Honghao Chen, Wentao Li and
Xiaonan Wang; the first three share equal contribution and Xiaonan Wang is corresponding author.
These names belong in the identified draft and author records, not the anonymous submission.
