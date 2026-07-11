# ChemWorld Nature-style review manuscript

This directory contains an evidence-gated **review draft**, not a submission-ready manuscript.
The prose and figures distinguish three evidence classes:

1. implemented and audited controls;
2. retained legacy diagnostic experiments;
3. blocked claims awaiting the frozen vNext method matrix, confirmatory rerun, exploit audit,
   independent reproduction and Train-to-Bench/Bridge transfer.

`claims.json` is the machine-readable claim ledger. `source_data/` is regenerated only from retained
reports, and `manuscript-audit.json` fails closed if blocked claims appear verbatim or upstream
publication readiness is false.

## Build

From the repository root on Windows:

```powershell
.\paper\build.ps1
```

The build requires the project virtual environment and Tectonic 0.16 or newer. It regenerates all
figures, audits the draft before rendering, writes `build/main.pdf`, copies the review artifact to
`main.pdf`, and audits the rendered artifact again.

Submission metadata remains intentionally incomplete: authors, affiliations, corresponding author,
acknowledgements, competing interests, contributions and repository DOI must be supplied by the
project owner before external submission.
