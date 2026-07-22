# ChemWorld Nature-style submission draft

There is no active publication manuscript in the current evidence DAG. The earlier NCS working
draft is preserved at `paper/archive/ncs-working-draft-2026-07-21/` as historical material while
the current work focuses on the mechanism-adaptation benchmark and its empirical gates.

This directory contains a rendered **Nature Article-style submission draft for author review**.
It is deliberately not labelled publication-ready: the architecture controls pass, but the full
method matrix, multi-seed RL evaluation, real-provider LLM runs, hidden-world generalization,
mechanism adaptation, exploit resistance and independent reproduction remain open.

The manuscript separates four evidence classes:

1. a bounded, frozen Safe-GP confirmatory slice;
2. SAC and Safe-GP development diagnostics;
3. environment and adapter controls;
4. blocked benchmark, transfer and real-world claims.

`claims.json` is the machine-readable claim ledger. `source_data/manifest.json` binds each figure to
retained evidence reports by SHA-256. `manuscript-audit.json` fails closed if a blocked claim appears
verbatim, a digest changes, a current result disappears, or upstream evidence is presented as
publication-ready.

## Build

From the repository root on Windows:

```powershell
.\paper\build.ps1
```

The build regenerates all five figures and their source tables, audits the draft before rendering,
renders with Tectonic, copies the author-review artifact to `paper/main.pdf`, and audits the final
PDF.

Before external submission, the project owner must provide authors, affiliations, corresponding
author, acknowledgements, contributions, competing interests, funding and an archival repository
DOI. Scientific submission also requires closing the formal evidence gates listed in the manuscript
and machine-readable audit.
