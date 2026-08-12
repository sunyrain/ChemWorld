# Work II formal-launch decision brief

**STALE — NOT AUTHORIZATION-ELIGIBLE.** This historical decision sheet predates the W2-25
eight-experiment redesign and the W2-26 8/10/12-pattern calibration gate. It must not be used to
approve a provider call. Current counts are machine-resolved from
`work-ii-method-qualification-readiness-v0.1.json` only after W2-26 has a validated passing
calibration summary.

## Current state

- Environment qualification, fixed-law prior design, hypotheses, estimands, five-task public
  cohort, persistent-session runner, evaluator-truth compiler, blind evaluator and formal analysis
  dataset builder are complete.
- No public-formal or private-confirmation participant outcome has been collected.
- The next permitted real provider call is W2-26 resource calibration, but its 10-round A-P and
  12-round A-S representatives are not terminal-selected and hash-frozen.
- No calibration or method-qualification provider call is currently authorized.

## Retired qualification envelope

| Item | Frozen value |
|---|---:|
| Provider/model | WellAU `gpt-5.6-sol`, medium reasoning |
| Cells | 3 prior arms in one development world |
| Accepted sessions/model calls | 3 |
| Maximum provider-process attempts | 6 |
| Complete experiments/checkpoints | Retired; resolve from current readiness artifact |
| Operation-attempt hard cap | Retired; resolve from current readiness artifact |
| Accepted-cell input-token cap | 7,200,000 per cell |
| Accepted-cell uncached-input cap | 960,000 per cell |
| Accepted-cell output-token cap | 72,000 per cell |
| Accepted-cell wall-time cap | 16,200 s per cell |

The numeric entries in this historical section are non-authoritative planning values. The current
method-qualification denominators and limits must be read from the deterministic readiness builder;
resource caps remain non-authoritative until all three W2-26 triplets complete and reconcile.

## Decisions required before qualification

1. Confirm that the frozen WellAU provider/model contract remains the intended formal method.
2. Confirm that the provider credential has been rotated after any earlier exposure.
3. Provide a verifiable pricing source and observation time for cached input, uncached input and
   output tokens, each in USD per million tokens.
4. Approve a qualification-only USD hard ceiling that covers at most six provider-process
   attempts. This ceiling is separate from the later 75-cell formal budget.

No API key or credential value belongs in the decision record or Git.

## Submission-route decision required before formal data

Choose one outcome-blind route:

- **Registered Report:** submit a presubmission enquiry first; formal primary data wait for an
  invitation, Stage 1 review, in-principle acceptance and protocol registration.
- **Regular submission:** freeze the target venue and evidence threshold now, then start only after
  method qualification, current clean-release qualification and final budget/command sign-off.

The existing recommendation is the Registered Report route because the primary hypothesis and
failure rules are already frozen and formal participant outcomes remain zero. If the enquiry is not
invited, the same design and analysis can move to regular submission without outcome-driven edits.

## Minimal approval payload

The user can unblock the qualification with the following non-secret information:

```text
Route: registered-report | regular-submission
Regular target/evidence threshold: <required only for regular submission>
WellAU formal provider contract: confirmed
Credential rotated: confirmed
Pricing source and observed time: <source>, <timestamp>
Cached input USD / 1M tokens: <value>
Uncached input USD / 1M tokens: <value>
Output USD / 1M tokens: <value>
Qualification currency ceiling USD: <value>
```

This payload cannot currently unblock execution. First select and hash-freeze the 10-round A-P and
12-round A-S representatives, run W2-26 under its own future write-once authorization, and validate
its machine summary. Only then regenerate this brief from current readiness, request the separate
method-qualification authorization, and continue through clean release and final freeze.
