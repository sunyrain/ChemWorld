# Work II formal-launch decision brief

This is an execution decision sheet, not a scientific result and not an authorization by itself.

## Current state

- Environment qualification, fixed-law prior design, hypotheses, estimands, five-task public
  cohort, persistent-session runner, evaluator-truth compiler, blind evaluator and formal analysis
  dataset builder are complete.
- No public-formal or private-confirmation participant outcome has been collected.
- The next real provider call is the three-cell current-method qualification triplet. Formal
  execution remains blocked until that triplet passes and the final preregistration receipt is
  signed.

## Frozen qualification envelope

| Item | Frozen value |
|---|---:|
| Provider/model | WellAU `gpt-5.6-sol`, medium reasoning |
| Cells | 3 prior arms in one development world |
| Accepted sessions/model calls | 3 |
| Maximum provider-process attempts | 6 |
| Complete experiments/checkpoints | 12 / 12 |
| Operation-attempt hard cap | 84 |
| Accepted-cell input-token cap | 7,200,000 per cell |
| Accepted-cell uncached-input cap | 960,000 per cell |
| Accepted-cell output-token cap | 72,000 per cell |
| Accepted-cell wall-time cap | 16,200 s per cell |

The currency reservation uses the full per-attempt token envelope. Unknown billing never counts as
zero, and observed cache use cannot reduce the pre-call reservation.

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

After this approval, the sequence is fixed: generate write-once authorization, execute the three
arms with progress reporting, build the qualification receipt, calibrate expected ETA, refresh the
clean-release receipt, generate the final preregistration freeze receipt, then request the separate
formal-matrix budget and command sign-off.
