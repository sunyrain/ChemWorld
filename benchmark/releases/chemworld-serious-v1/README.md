# ChemWorld serious v1 release candidate

Status: **building — not publication-ready**

This directory is the single tracked entry point for the first ChemWorld arXiv evidence package. It is not a leaderboard release and does not certify broad scientific-agent performance. The package will expose the evidence needed for the manuscript *Experimental Intelligence in Executable Chemical Worlds* while keeping private world internals and large raw provider archives outside Git.

## Included now

- a machine-readable release manifest;
- a data card with nonduplicated experiment accounting;
- explicit claim and exclusion boundaries;
- immutable paths and hashes for the formal G0 summaries and the audited G2 v0.4 development result.
- a deterministic 1,441-file G0 raw-data hash index with no absolute paths or raw content.
- a frozen single-source derived-data JSON, six deterministic CSV views, and
  Figures 1--6 generated only from that JSON;
- the terminal G2 v0.5 audit bindings, 677-file hash index, and a compact
  four-cell replay subset;
- the populated first-version manuscript, four generated main tables, six complete
  figure legends, and a 22-entry working bibliography;
- a Chinese readiness audit separating required experiments, censor-aware counts,
  generated artifacts, release gates, and the external archive dependency;
- a current 55-node evidence graph with a clean source-tree attestation.
- a release verification attestation recording the full test suite, clean-wheel
  smoke, terminal replay, and independent-checkout zero-difference rebuild.

## Still required

- durable external archive identifiers for the local raw roots;
- target-style reference formatting and final statistical-language/claim audit.

No file in this directory should be interpreted as lifting those gates unless `manifest.json` has `publication_ready: true` and every item in `gates` is `passed`.
