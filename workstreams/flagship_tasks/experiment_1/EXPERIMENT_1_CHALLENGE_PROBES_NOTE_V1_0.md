# Experiment 1 challenge probes v1.0

Status: **FROZEN BEFORE PROBE EXECUTION**

## Question

Do the ten five-World `qualified-development` loci satisfy the four challenge requirements that
were not established by Q1--Q8: system-specific false-prior plausibility, failure of a fixed
default/one-shot recipe to discriminate stably across all five Worlds, positive value from an
active information choice, and a reliable falsification cost strictly above the one-experiment
trivial lower bound but no greater than the frozen Participant budget?

## Evidence and denominator

This is a provider-free, read-only challenge probe over the immutable development reports bound by
the 105-row convergence registry. It does not create new World observations and is not confirmation.
The denominator is fixed at `10 loci x 5 Worlds = 50` World-probe rows. Every missing report, digest
mismatch, malformed value, or failed probe remains in the denominator and fails closed.

The ten loci are EC-E/P/S, RX-P/S, PA-E/P/S, and C-E/P. Their Worlds, priors, Q thresholds and
Participant budgets remain unchanged. The machine contract freezes a probe family for each locus:

- entity label exchanges require a paired entity comparison; one unpaired observation is
  analytically non-identifying under an unknown nuisance baseline;
- directional reflection priors match at their registered centre and require observations from
  separated sides of the public grid;
- response-gain and structural questions require a two-condition contrast or trend;
- PA-P is audited empirically at its frozen reference default and is allowed to fail if that single
  point already rejects the false band in every World.

## Measurements and decisions

For every World-probe row the runner records the source report digest, plausible-envelope result,
default one-shot result, active-information score/result, inferred minimum reliable unique-condition
cost, Participant budget, and all failures. A locus passes:

1. plausibility only if all five false priors remain inside the registered system-specific envelope;
2. non-triviality only if the fixed default one-shot recipe does **not** discriminate reliably in all
   five Worlds;
3. information choice only if all five Worlds contain a pre-registered active contrast with positive
   diagnostic value;
4. budget window only if every World has `1 < minimum_reliable_cost <= participant_budget`.

The existing symmetry, consequence and leakage checks continue to come from all five bound Q4, Q7
and Q3 development gates. Any failed challenge check blocks that locus from confirmation. If one or
more loci fail, the audit remains fail-closed and no confirmation salt or realized coordinate set may
be generated or consumed.

## Outputs

- raw machine summary under `runs/challenge/experiment-1-challenge-probes-v1.0/`;
- Git-tracked machine and readable summaries under
  `workstreams/flagship_tasks/experiment_1/results/`;
- refreshed challenge audit only after the probe summary is complete.

