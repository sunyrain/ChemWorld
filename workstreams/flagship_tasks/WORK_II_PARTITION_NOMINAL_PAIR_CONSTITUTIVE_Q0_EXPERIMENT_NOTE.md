# Work II partition nominal-pair constitutive-law A-S Q0 — experiment note

Status: **frozen before execution; provider-free development Q0**. This is a new candidate question,
not a rerun or reinterpretation of the rejected load-by-phase-volume curvature Q0. The prior result
and its thresholds remain unchanged. Development evidence is `development_only`, cannot enter C2,
and does not authorize participant or provider execution.

## Question and tested units

Does the registered partition-coefficient exponent create a publicly distinguishable response over
the full nominal `solvent × extractant` identity table? The frozen unit is one of all `4 × 4 = 16`
nominal pairs in world seed 0. Each pair is executed under the baseline exponent `1.0` and power-law
exponent `1.75`, using an otherwise identical action plan, phase balance, mixing protocol, and keyed
observation coordinate. This produces 32 primary executions and 32 tolerance-zero exact replays.

The aqueous volume is fixed at `0.015 L`, extractant volume at `0.019 L`, solvent charge at `0.020 L`,
mixing at `420 s / 800 rpm`, and settling at `900 s`. These values are not selected from the rejected
Q0 outcome; they are the centre settings of its frozen grid. The new varying coordinates are the two
categorical identity axes on which the executable exponent law actually operates. Categories are
never treated as ordered numeric variables.

## Measurements and frozen pass rules

The paired public measurements are post-separation HPLC and final assay
`product_in_organic`, `product_in_aqueous`, and `phase_ratio`. A channel-specific effect gate remains
`max(0.03, 6 × declared_sigma)`: HPLC gates are `0.09/0.09/0.108`; final-assay gates are
`0.06/0.06/0.072`.

The candidate passes only if all 32 executions complete safely with exact replay, identical paired
action/noise coordinates, deterministic executable-law binding, and no hidden-law leakage, and all
of the following scientific conditions hold:

1. both categorical identity axes are publicly active: for at least one registered channel, varying
   solvent at fixed extractant crosses its effect gate, and varying extractant at fixed solvent does
   likewise;
2. at least eight of the sixteen nominal pairs cross the channel-specific paired-law effect gate on
   each of at least two registered public product-allocation channels;
3. the constitutive functional form is resolved from public data rather than inferred from a raw
   offset.  For each instrument, form the public allocation log-ratio
   `z = log(product_in_organic / product_in_aqueous)` (the fixed phase-volume ratio contributes only
   an intercept), then regress power-law `z` on baseline-law `z` across the 16 categorical pairs.
   At least one instrument must resolve `abs(slope - 1) >= max(0.20, 6 * SE_slope)`.  `SE_slope` is
   frozen as a first-order propagation of the declared organic/aqueous assay noise through the
   fitted slope, with each metric's keyed noise treated as shared across its paired laws and as
   independent across cells and metrics.  No ordering or distance between category labels enters
   this calculation.

`phase_ratio` is retained as a negative/control measurement and is not required to move. Any
platform failure stops this Q0 and requires a full restart after repair. Any scientific failure is
retained; pairs, laws, measurements, and gates are not changed after observing the outcome.

## Expected outputs

One self-hashed raw task report and one readable self-hashed summary under the ignored development
output root, including the exact 32/32 denominators, every failure, per-channel identity-axis ranges,
per-pair law gaps, supporting-pair counts, the derived public log-ratio slopes and propagated slope
uncertainties, and one uniform execution-context envelope. A pass authorizes only the unchanged
provider-free five-world development qualification;
it does not authorize D1, C2 admission, formal R5, or a provider call.
