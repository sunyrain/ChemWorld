# Work II terminal schema fixed-context replay

Status: development-only follow-up authorized by the user. It is an operational isolation test, not
formal evidence and not a mechanism-discovery experiment.

## Question

With one identical evaluator-fixed correct mechanism context, evidence packet, candidate packet, and
selection rule, how does requiring an additional `8 x 4` prediction table affect terminal completion,
resource use, ranking, and selected-action quality?

## Units and frozen coverage

- Reuse the already exposed A-S B4 world `368103785`, its eight evidence rows, eight outcome-hidden
  candidates, and hidden evaluator truth. No fresh world, candidate, or truth execution is used.
- Supply the same frozen mechanism to every session: `FAMILY_B_POWER`, exponent `1.75`, with the
  reference-coefficient power law and process-factor calibration delegated to the visible evidence.
- Run three independent `full_32` sessions and three independent `lean_ranking` sessions. Every
  session is one provider turn. Both conditions receive identical scientific context and must rank
  all eight candidates exactly once and select `ranking[0]`; only `full_32` submits the 32 numeric
  outcomes.
- The deterministic schedule interleaves conditions. Replicate numbers are descriptive matching
  labels, not random seeds or independent worlds.

## Measurements

- Completion and failure classification; elapsed time; output and reasoning tokens.
- Selected hidden rank, normalized regret, selected-minus-random score, and Kendall agreement with
  the hidden ranking.
- `full_32` prediction MAE over 32 terms; no synthetic lean prediction endpoint.
- Per-replicate lean-minus-full descriptive differences when both sessions complete.

## Pass, failure, and stop rules

- Stop after all six sessions reach a retained record. Participant/schema failures are not retried;
  provider or runner infrastructure retries retain predecessor receipts.
- No outcome changes the fixed context, candidate ordering, schedule, or denominator.
- The result may diagnose terminal contract burden. It cannot establish autonomous mechanism learning,
  arm effects, or longitudinal action competence, and it does not automatically modify W2-40.

## Expected outputs

Ignored development cell records, provider receipts, progress log, machine summary, and concise
Chinese report.
