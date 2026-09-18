# Experiment 1 executable challenge probes v1.1

Status: **FROZEN BEFORE ATTEMPT 2 EXECUTION**

## Purpose

The v1.0 probe campaign was a development attempt.  It correctly preserved the
50-World denominator, but for nine loci it declared the default outcome and a
two-condition stopping cost instead of measuring them.  Those results cannot
authorize confirmation.

Version 1.1 keeps the Worlds, priors, Q1--Q8 thresholds, participant budgets,
and raw development executions unchanged.  It changes only the challenge
measurement layer.  Every World now has:

1. one frozen executable default condition;
2. one frozen ordered policy over legal conditions;
3. public observations loaded from the exact-replay development receipts;
4. a declared sequential evidence statistic;
5. the first measured reliable stopping time, if any;
6. realized information gain relative to the default action.

Every step records its action identifier, public-observation digest, statistic
before and after the action, information gain, and stop reason.  Missing,
malformed, duplicate, non-finite, or stale evidence remains in the denominator
as a failure.

## Frozen policies

| Locus | Default | Ordered active policy | Reliable rule |
| --- | --- | --- | --- |
| EC-E | first moved electrolyte at anchor 0 | its registered transposed mate | transport-efficiency paired SNR and effect |
| EC-P | grid centre | low then high potential endpoint at centre current | cumulative held-out aligned-vs-reflected error margin |
| EC-S | centre-current validation group | low then high current validation group | standardized aligned-vs-structural-model error advantage |
| RX-P | 420 K, 3300 s | 370 K then 470 K at 3300 s | cumulative held-out score/risk reflection margin |
| RX-S | middle-temperature, short-duration, low-dose cell | middle then long duration at the same temperature/dose | two-metric paired-gap accumulation |
| PA-E | first moved extractant at solvent 0 | its registered transposed mate | organic-product paired SNR and effect |
| PA-P | reference phase point | low then high registered participant point | frozen noise-robust prior-counterexample rule |
| PA-S | solvent-0/extractant-0 | next preregistered nominal pairs | two-or-more-condition public log-ratio slope |
| C-E | first moved solvent at 290 K | its registered transposed mate | crystal-yield paired SNR and effect |
| C-P | 290 K | 310 K then 270 K | endpoint gain selects aligned band, rejects false band, and passes SNR |

The policy is identical as a rule across W01--W05 and does not select an easy
condition per World.  A locus passes only if every World has a measured stopping
cost strictly greater than one and no greater than the unchanged participant
budget.  PA-P is expected to remain fail-closed if its default reference point
is again a reliable one-shot counterexample.

## Provenance deviation

- v1.0 initial code/evidence commit: `844a8ea9eec198e7d1699b9b63a057d5662d84cd`;
- v1.0 adapter fix commit: `5a152923b2d618c7ff0dac95a2249fe2615116ce`;
- initial attempt result: 7/10 loci;
- restart1 result: 9/10 loci;
- restart1 audit commit: `5b1125c5576c70306f2cea1e61c3f3f6a6212615`.

Both v1.0 attempts remain immutable development evidence.  Attempt 2 writes a
new run directory and new result files; it does not overwrite or relabel either
earlier attempt.

