# Experiment 1 RX-S structural redesign authoring note v1.1.0

Status: **AUTHORING DESIGN FROZEN BEFORE CALIBRATION EXECUTION**

## Failure diagnosis

The v1.0.1 stable-catalyst fork was executable and replayable, but its largest public endpoint
effects were roughly one order of magnitude below the frozen `0.05` effect gate in all five formal
Worlds. All five RX-S units therefore failed Q5, Q6, and Q7. Thresholds will not be lowered and the
deactivation rate will not be amplified merely to obtain PASS.

## Candidate question

Two executable candidates are compared on the same provider-free receipts and public design:

1. `deactivating_baseline` versus `stable_catalyst`, the v1.0.1 question;
2. `deactivating_baseline` versus `reversible_target_pathway`, which adds the explicit reverse
   channel `P -> A` to the target pathway at severity `0.8` and full-severity reverse rate constant
   `0.000625 s^-1`.

The second candidate is a genuine topology difference, not a prompt-only claim or a rescaling of
the forward rate: it adds a reaction with the opposite stoichiometric direction and a separately
bound mechanism hash. It is scientifically relevant to reaction stopping because an
equilibrium-limited target pathway can change whether additional residence time improves or erodes
yield and conversion.

## Calibration design

- non-benchmark `public-test` seeds: `201, 202, 203`;
- public grid: the existing 3 temperatures x 3 durations x 3 catalyst doses;
- laws per cell: baseline, stable catalyst, reversible target pathway;
- all laws share the same action plan and keyed observation coordinate within a cell;
- every trajectory requires tolerance-zero exact replay;
- direct endpoints: yield, conversion, selectivity;
- effect gate: `max(0.05, 3 sigma)` using the existing declared endpoint noise;
- at least two public endpoints must resolve the candidate;
- resolving support must include separated cells and at least two catalyst-dose levels;
- the product gap must show a duration-accumulation signature;
- a candidate must pass all three calibration Worlds;
- selection priority: pass count, minimum number of resolving endpoints, minimum maximum public
  effect, then the fixed candidate order shown above.

The stable candidate is retained as a negative/positive control rather than discarded after seeing
v1.0.1. If neither candidate passes all three calibration Worlds, RX-S remains failed-development;
there will be no threshold reduction or World replacement.

Calibration Worlds and noise coordinates do not enter the benchmark denominator. Formal
RX-W01..W05 are not inspected by the selection script.
