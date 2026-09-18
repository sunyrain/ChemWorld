# Experiment 1 challenge v1.2 attempt 3 execution receipt

Source commit: `0680ed11c4bf918ee0150fcd41d44ffd5ac3981a`.

## Initial attempt 3 — retained incomplete

The first invocation named only the campaign and release-confirmation evidence roots.
Twenty EC/RX reports live in the pre-existing `ChemWorld-fresh` evidence root, so the
fail-closed resolver recorded 20 `probe_error` rows rather than searching an unbound
or guessed replacement. The output remains immutable and is retained as:

- summary file SHA-256:
  `d7f07eb0d7d070c784d29dd5c72b4b9434bf667c30aec1da3735cea91dc9a3fd`;
- canonical probe hash:
  `8a22d04282f4e754db71caab6bc59d58af3cf11aea0fa5d378db05607ccb5ee2`;
- denominator: 50 attempted, 30 completed, 20 probe errors.

No contract, code, registry, manifest, World, prior, threshold, budget, action order,
or evidence file changed after this attempt.

## Attempt 3 restart1 — complete unit-zero rerun

The restart added the missing read-only `ChemWorld-fresh` lookup root and recomputed
all 50 rows from unit zero under the same frozen source commit and contract:

- summary file SHA-256:
  `16cded748678b0c18cf09f690fd45fab69b85bd94ea5c3c18fc5ade494fe314c`;
- canonical probe hash:
  `71509b9f0c2067d8ab6bde1531520337d4a3b68e6b4d8cee4e7372dbaca53456`;
- denominator: 50 attempted, 50 completed, zero probe errors;
- locus result: 7 passed, 3 blocked fail-closed.

Passed loci: EC-E, EC-P, EC-S, RX-P, PA-E, C-E, C-P. Blocked loci: RX-S
and PA-S because each hidden-world condition has only one distinct receipt noise
coordinate versus three required; PA-P because every World is reliably discriminated
by the fixed default action at measured cost one.

The v1.2 audit canonical hash is
`0f9e74b756cc3bd8f5bf06fa68ca332577d9e8ec0c1a1cfcc2fa3f88fc89ec8f`.
These remain development challenge results, not confirmation evidence.
