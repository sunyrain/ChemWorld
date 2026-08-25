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

Current development status: the main text is within the nine-page initial-submission limit. The
evidence-bound action/evaluator figure integrates W2-50 cell outcomes, W2-51/W2-52 qualification
funnels and the W2-53 unit-level alignment diagnostic without introducing a participant-effect panel.
