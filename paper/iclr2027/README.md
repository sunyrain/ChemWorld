# Anonymous ICLR 2027 build

This directory contains the compact anonymous review manuscript, appendix, official unmodified ICLR
assets, and the Pandoc template. The venue-neutral evidence narrative remains
`paper/prior_discovery_manuscript.md`; `submission.md` is its page-budgeted ICLR integration, not a new
scientific evidence source.

Build from the repository root with the locked environment:

```powershell
uv run --no-sync python paper/tools/build_prior_discovery_iclr.py
```

The build writes the anonymous PDF, generated TeX, and machine-readable audit to
`paper/exports/prior-discovery-iclr2027/`. Review mode must remain anonymous and
`\iclrfinalcopy` must remain disabled. The builder verifies the imported official assets, page count,
citations, cross-references, LaTeX errors, horizontal and vertical overflow, and a fixed set of direct
identity leaks.

The venue-neutral figure bundle contains six assets; the compact ICLR main text selects five of them
(assets 1 and 3--6) and renumbers that selection consecutively. Its final action/evaluator figure
combines all-scheduled four-condition outcomes, a decision-aligned executable-law-versus-participant
regret panel and the frozen unit-level ranking diagnostic. The W2-51/W2-52 qualification details stay
in the appendix and anonymous supplement rather than appearing as a
participant-effect panel.

The current verified build is anonymous, uses all nine allowed main-text pages and has 19 pages in
total. Contact-sheet and detailed figure-page review found no clipping, overlap, blank pages or float
collisions. The anonymous supplementary archive contains 45 ZIP members; its standalone verifier
checks 44 packaged files, recomputes the four-condition contrasts and C2/B3 failure-aware
denominators from cell records, and independently reruns B2 expression coding from 45 public
summaries. All bibliography records have been
resolved against source metadata. Author order, OpenReview profiles and reciprocal-review eligibility
remain manual pre-submission checks.
