# Experiment 1 C-S structural redesign authoring note v1.1.0

Status: **AUTHORING DESIGN FROZEN BEFORE CALIBRATION EXECUTION**

## Failure diagnosis

The v1.0.1 C-S candidate was a response-surface interaction test over seed mass and cooling
temperature. It failed all five formal Worlds, primarily because the fitted aligned and
misspecified feature templates did not yield stable held-out disagreement. More importantly, both
arms still executed the same private population-balance law, so the question was weaker than the
intended structural contrast.

No threshold will be lowered and the old five failures remain valid for v1.0.1.

## Executable structural fork

The v1.1 authoring candidate compares:

- `seed_growth_parent`: the current mass-conserving population-balance runtime;
- `primary_nucleation_dominated`: the same PBM with a hidden, versioned population-regime
  intervention that multiplies the four solvent-specific primary-nucleation coefficients by `4`
  and divides the four growth coefficients by `4`.

The fork changes executable private physics and produces a distinct intervention and private World
hash. It does not change public action names, instruments, budgets, or reported metrics.
It is not a prompt-only statement. Because nucleation and growth move in opposite directions, the
child is not a scalar rescaling of total crystallization speed.

## Calibration design

- non-benchmark public-test seeds: `301, 302, 303`;
- no Experiment 1 formal World IDs or formal-world intervention manifests are used for selection;
- public design per law: `2 seed masses x 2 cooling endpoints x 2 durations = 8` cells;
- seed mass: `0.000001 g` and `0.015 g`;
- cooling endpoint: `310 K` and `270 K`;
- crystallization duration: `3600 s` and `10800 s`;
- paired laws use identical action plans and keyed observation coordinates;
- every trajectory requires tolerance-zero exact replay;
- public endpoints: crystal yield, size, CSD quality, fines fraction, and score.

The candidate must pass all three calibration Worlds. Per World it must show:

1. at least two endpoints with a paired law gap `>= 0.03`;
2. resolving support in at least two separated cells;
3. a seed-by-law or cooling-by-law interaction `>= 0.03`, demonstrating that one scalar rate
   rescaling cannot absorb the fork;
4. at least one change in the yield-maximizing seed, cooling, or duration decision;
5. no platform failures, exact replay, matched action plans, matched noise coordinates, and hidden
   intervention identifiers absent from Participant-visible payloads.

If the candidate fails any calibration World, C-S remains failed-development for this iteration.
Formal C-W01..W05 will not be run and thresholds will not be reduced.
