# ChemWorld serious v1 release candidate

Status: **building — not publication-ready**

This directory is the single tracked entry point for the first ChemWorld arXiv evidence package. It is not a leaderboard release and does not certify broad scientific-agent performance. The package will expose the evidence needed for the manuscript *Experimental Intelligence in Executable Chemical Worlds* while keeping private world internals and large raw provider archives outside Git.

## Included now

- a machine-readable release manifest;
- a data card with nonduplicated experiment accounting;
- explicit claim and exclusion boundaries;
- immutable paths and hashes for the formal G0 summaries and the audited G2 v0.4 development result.

## Still required

- terminal G2 v0.5 replication audit and frozen derived table;
- figures generated only from that table;
- public file-hash indices and a compact replay subset;
- durable external archive identifiers for the local raw roots;
- refreshed evidence registry, clean-wheel, full-test, replay, and independent-checkout attestations.

No file in this directory should be interpreted as lifting those gates unless `manifest.json` has `publication_ready: true` and every item in `gates` is `passed`.
