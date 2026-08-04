# Work I manuscript language-lock audit

> **SUPERSEDED 2026-08-04.** Historical audit only; its requested changes do not define current work.
> Use [`../FIRST_PAPER_TODOLIST.md`](../FIRST_PAPER_TODOLIST.md).

Historical status: **integration changes were required for the retired Work I draft**
Receipt SHA-256: `26ff46b73c8e584b65e18eff06f0440539f77a8e62a8a0e601c6aa41204e8969`

| Lock | Current result | Required result |
| --- | --- | --- |
| Figure first references | [1, 6, 3, 4, 5] | [1, 2, 3, 4, 5, 6] |
| First 120 mention | line 28; 84 absent | 120 closed lifecycles: 84 final assays and 36 explicit discards |
| 2/8 vs 6/8 | PASS | 2/8 diagnostic; 6/8 threshold-sensitive supporting evidence |
| Terminology | 3 residual findings plus figure/count locks | frozen S02 terms |

## Blocking findings for final integration

- `FIGURE_FIRST_REFERENCE_ORDER` (lines 148, 278, 296, 321, 369): integrate first textual references in the exact sequence [1, 2, 3, 4, 5, 6].
- `FIRST_120_COUNT_LOCK` (lines 28): 120 closed lifecycles: 84 final assays and 36 explicit discards.
- `TERMINOLOGY_INDEPENDENTLY_CONFIGURED` (lines 28): distinct complete agent systems.
- `TERMINOLOGY_CLOSED_VESSELS` (lines 204): closed lifecycles.
- `TERMINOLOGY_ARBITRARY_RECOMBINATION` (lines 468): preregistered, qualified interventions on named world components; no arbitrary-recombination claim.

## Integration actions

- `S07-A1` (W1-S10 manuscript integrator; lines 148, 278, 296, 321, 369): First-reference sequence must be F1 apparatus, F2 known-policy validity, F3 terminal policy, F4 compiled controls, F5 primitive lifecycle, F6 fresh process.
- `S07-A2` (W1-S03/W1-S10 abstract integration; lines 28): Two distinct complete agent systems produced 120 closed lifecycles: 84 final assays and 36 explicit discards across five matched worlds.
- `S07-A3` (W1-S10 display-item integration; lines 204): Replace '120 closed vessels' with the frozen lifecycle partition.
- `S07-A4` (W1-S09/W1-S10 limitations integration; lines 468): Replace arbitrary recombination wording with preregistered, qualified interventions on named components while authority and audit semantics remain fixed.
- `S07-A5` (W1-S10 final scan; lines final scan): Retain the current semantic hierarchy: 2/8 endpoint diagnostic; 6/8 threshold-sensitive supporting evidence; selected worlds are descriptive.

The current sensitivity language already preserves the registered hierarchy and needs
no scientific reinterpretation. W1-S07 did not edit the manuscript or any shared hot file.
