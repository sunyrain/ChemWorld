# Experiment 1 challenge v1.2 deviation receipt

Status: **pre-execution repair declaration**.

## Parent evidence retained

- Source commit: `6d8a3e7e8337ac1833acac16e74d1faaf25ecd8f`.
- v1.1.1 contract file SHA-256:
  `f3f42b8e3ce1123052479894ccd0dfcc2064b7ee13308439bf268526fd8e9860`.
- restart1 probe file SHA-256:
  `6b0098728c1151fc7bb105dbac7825373f576da62a56762566a57de308c1bde4`;
  canonical probe hash:
  `ca68c82e6307a28652972438fdc8ddea5a3df86fe64bcdd522a70fe43e67fc08`.
- restart1 audit file SHA-256:
  `226b362000430dbd9bab95635ef823a70abb188d0f6f1aec0d444a337d026723`;
  canonical audit hash:
  `795f309362ac62b15b82489277eeead39f5cb3c091325fc539491e13a4998672`.

These artifacts are preserved as development attempts. They are not confirmation
eligibility evidence.

## Reason for v1.2

Independent review found that v1.1.1 did not independently verify the registry,
manifest, report, probe, and audit hash chain; PA-P and EC-S still consumed derived
qualification analysis; RX-S and PA-S accepted configured rather than receipt-derived
replicate counts and mixed paired-family outcomes into participant traces; and active
information could be credited from a later action rather than the first reliable
stop.

## Exact permitted contract delta

All action orders, budgets, and existing numerical thresholds remain unchanged.
The v1.2 contract only:

1. removes `observed_noise_replicates_per_condition` from RX-S and PA-S because
   support is now counted from raw noise identities;
2. records the already-frozen EC-S model-family constants (`effect_floor = 0.03`,
   `model_noise_multiplier = 6.0`, `minimum_disagreement_fraction = 0.4`) needed to
   recompute raw model errors; and
3. records the already-frozen PA-P decision constants
   (`minimum_prediction_gap = 0.05`, `minimum_signal_to_noise_ratio = 2.0`,
   `minimum_noise_replicates = 3`) needed to recompute the raw receipt decision.

The validator checks this exact adapter delta against the hash-bound v1.1.1 contract.
No World, prior, qualification threshold, participant budget, or action order changes.

## Restart rule

Attempt 3 must recompute all 50 rows from unit zero. It may read only the exact
hash-bound registry, manifest, reports, and raw public receipts. No confirmation salt,
realized coordinate, secret set, or participant execution is authorized.
