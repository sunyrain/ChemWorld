# Work II observation/measurement Q0 — experiment note

状态：**provider-free Q0 design freeze；尚未产生 Work II 结果**

## Question

Before adding an observation-model initial-prior block, do the existing public measurement
contracts expose bounded, falsifiable information without leaking evaluator truth? This Q0 asks
whether instrument sensitivity, low-signal degradation, disclosure conditions and historical
spectrum retrieval behave as declared. It does not evaluate a participant or authorize A-O D1.

## Tested units and coverage

- Five spectral instruments: HPLC, GC, UV/Vis, IR and NMR on one frozen high-contrast state pair and
  one independently seeded low-signal pair.
- One frozen pH high-contrast pair and one low-contrast degradation pair.
- Three public spectrum conditions: assigned, unassigned and masked, with identical non-spectral
  context and identical assigned/unassigned raw curves.
- One runtime HPLC packet from a complete public `reaction-to-assay` recipe.
- A two-packet request-only historical archive, including one successful retrieval and one unknown-ID
  failure. No provider or participant session is used.

## Measurements

- Per-instrument identifiability decision, warnings and nearest-centroid replicate accuracy.
- Low-signal degradation decision for every instrument.
- pH contrast, declared limit of quantification and low-contrast degradation.
- Spectrum-condition hashes, non-spectral pairing and public-truth leakage tokens.
- Archive catalog leakage, retrieval identity, failure semantics and retrieval ledger.
- Source cleanliness, provider-call count and exact fixed denominator.

## Pass/failure rules

Q0 passes only if all registered controls pass together:

- HPLC, GC and NMR are identifiable for the frozen high-contrast pair, while UV/Vis and IR match
  their registered non-identifiable expectation;
- all five instruments become explicitly non-identifiable with warnings in the low-signal regime;
- at least three instruments permit replicate-only public discrimination at accuracy `>= 0.75`;
- the pH high-contrast pair exceeds its declared LOQ and the low-contrast pair falls below it;
- no forbidden evaluator/private token appears in public reports;
- assigned and unassigned conditions share the exact raw curve, masked exposes no signal, and all
  three conditions preserve identical non-spectral context;
- the archive catalog contains no signal, explicit retrieval returns the exact packet, unknown IDs
  fail closed, and both outcomes are ledgered.

Any compiler, runtime, disclosure, hashing or archive-contract defect invalidates Q0 and is fixed
before a complete rerun. A scientific non-identifiability result is retained and does not authorize
changing the state pair, seeds, expected instrument classes or thresholds.

## Expected outputs

1. One machine-readable Q0 report with all controls, denominators and failures.
2. One concise stage analysis stating whether a two-task, five-world A-O screen is worth building.
3. No participant config and no provider execution authorization.

