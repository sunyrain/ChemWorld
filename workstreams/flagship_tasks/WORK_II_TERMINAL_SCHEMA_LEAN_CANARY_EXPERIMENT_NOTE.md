# Work II terminal prediction-schema lean canary

Status: development-only diagnostic authorized by the user. It is not formal evidence and does not
change the frozen longitudinal main experiment by itself.

## Question

When the final mechanism law and evidence are held fixed, does requiring an additional `8 x 4`
numeric prediction table change schema completion, resource use, ranking quality, or selected-action
quality relative to requiring only a complete ranking and selection?

## Units and frozen coverage

- Reuse the already provider-exposed A-S B4 world `368103785`; do not consume any fresh main-study
  world or candidate packet.
- Use all three initial-model arms. For every arm run one fresh `full_32` session and one fresh
  `lean_ranking` session: six independent persistent sessions and twelve provider turns total.
- Turn 1 reveals the fixed B4 structural evidence but not the eight terminal candidates. The
  participant commits one mechanism family, exponent, typed law, confidence, and concise summary.
- Turn 2 reveals the same eight outcome-hidden candidates in both conditions. Both conditions must
  rank all eight candidates exactly once and select the first-ranked candidate. Only `full_32` must
  additionally predict all four metrics for all eight candidates.
- No physical experiment, new truth execution, incumbent-retention option, outcome-based replacement,
  or retry after a participant/schema failure is allowed. Provider/runner infrastructure retries
  retain their predecessor receipts.

## Measurements

- Completion and failure classification; same-thread continuity; terminal elapsed time; terminal
  output and reasoning tokens.
- Selected hidden rank, normalized regret, selected-minus-random score, and Kendall agreement between
  participant and hidden rankings.
- `full_32` prediction MAE over its 32 terms. The lean condition has no fabricated counterpart.
- Matched arm-level differences are descriptive only; three arms in one world are not three
  independent scientific clusters.

## Pass, failure, and stop rules

- Stop after all six scheduled sessions reach a retained terminal record.
- The canary is operationally encouraging if lean completes all three arms without increasing mean
  selected rank or normalized regret relative to full, but no threshold upgrades the result to a
  scientific conclusion.
- Any schema, provider, or runner failure is retained. The longitudinal main protocol remains blocked
  until this diagnostic is reviewed; no main-study design is changed automatically.

## Expected outputs

Ignored development cell records, provider receipts, progress log, machine summary, and a concise
Chinese report comparing `full_32` with `lean_ranking`.
