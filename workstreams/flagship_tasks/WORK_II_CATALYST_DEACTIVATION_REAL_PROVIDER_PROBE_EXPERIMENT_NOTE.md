# Work II catalyst-deactivation real-provider probe

Date: 2026-08-12

Status: frozen before provider execution

## Question and tested unit

Can one real WellAU `gpt-5.6-sol` medium Codex session use two autonomous complete experiments in
reaction-safety world seed 0 to distinguish the hidden deactivating-catalyst baseline from an
otherwise identical stable-catalyst hypothesis? The participant receives the two candidate
structures with equal status but not the hidden answer. The hidden world is fixed for the full
session; both fresh batches share the same campaign ledger and observation-noise namespace.

This is a one-cell development case study requested after the provider-free W2-33 qualification.
It neither replaces the frozen `54/54` result nor authorizes a multi-seed participant block.

## Measurements and limits

- one persistent Codex process, WellAU `gpt-5.6-sol`, medium reasoning, ChemWorld MCP only;
- exactly two participant-controlled complete experiments, each closed by committed final assay;
- at most 24 operation attempts, two heat stages, two quenches, two nonfinal measurements and two
  final assays;
- process-time ceiling `29,040 s = 2 x 14,400 s heat + 2 x 120 s quench`;
- one pre-evidence, one after-first-experiment and one final typed belief checkpoint;
- record operations, complete experiments, MCP calls and failures, exact replay, provider attempts,
  input/cached/uncached/output tokens and elapsed time.

The participant is instructed to put one of the exact labels `catalyst_deactivation_present`,
`stable_catalyst`, or `indeterminate` in its final public selection rationale, with confidence and
experiment-indexed evidence. This is a reporting contract, not a hint about the hidden answer.

## Frozen completion and interpretation rules

Operational completion requires one terminal provider session, two closed final-assay experiments,
all three checkpoints, one committed final recommendation, exact replay, no platform failure and
complete provider usage accounting within the frozen limits. Participant-selected unsafe or
physically poor conditions remain participant outcomes rather than platform failures.

The scientific probe is classified as:

- `correct` only for `catalyst_deactivation_present`;
- `incorrect` only for `stable_catalyst`;
- `indeterminate` when that label is submitted or no unique label can be extracted;
- `operational_failure` if the two-experiment/session contract does not complete.

No result from this single seed may lower the W2-33 noise/effect gates. A correct judgment is a
participant case study; an incorrect or indeterminate judgment is evidence that two autonomous
experiments did not resolve the small public effect under this harness.

## Outputs

Raw trajectories and provider receipts remain under ignored `runs/`. Tracked outputs are one
machine-readable summary with exact denominators and failures, one concise Chinese analysis and an
updated Work II TODO entry.
