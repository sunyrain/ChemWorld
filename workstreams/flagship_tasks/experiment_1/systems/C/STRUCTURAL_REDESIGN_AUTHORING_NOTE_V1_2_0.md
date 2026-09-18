# Experiment 1 C-S final structural redesign authoring note v1.2.0

Status: **AUTHORING DESIGN FROZEN BEFORE CALIBRATION EXECUTION**

## Question and redesign boundary

This is the second and final C-S redesign iteration. It does not reuse the rejected
`seed-growth-dominated` versus `primary-nucleation-dominated` candidate. The new question is
whether a cooling process is governed by transfer-proportional, supersaturation-linear impurity
occlusion or by a surface-coverage-limited occlusion law with a quadratic supersaturation term.
The two laws use the same mass-conserving population balance, public actions, instruments and
budget, but differ in executable impurity-incorporation equations rather than one scalar
multiplier.

- parent: `linear_supersaturation_transfer_v1`;
- child: `surface_saturation_occlusion_v1`, using a Langmuir-like impurity surface-coverage term,
  a frozen finite-capacity coefficient of `4`, and quadratic supersaturation dependence;
- the fork is private, deterministic, versioned, changes the private World hash, and must not
  appear in Participant-visible payloads.

The previous v1.0.1 failures and rejected v1.1.0 authoring evidence remain unchanged. If this
candidate does not satisfy the frozen calibration rule, C-S remains `failed-development`; no
third redesign is authorized.

## Provider-free calibration tournament

- non-benchmark `public-test` seeds: `401, 402, 403`;
- no formal C-W01--W05 outcome is used for selection;
- common paired grid per World and law:
  `seed mass {0.001, 0.015 g} × cooling endpoint {310, 270 K} × duration {3600, 10800 s}`;
- 16 parent/child executions per World plus a preregistered constant-capacity scalar-null
  fit/held-out block; 108 executions total; each execution requires tolerance-zero replay;
- paired laws use identical public action plans and keyed observation coordinates;
- public endpoints: crystal yield, HPLC-derived crystal purity/impurity signal, crystal size,
  CSD quality, fines fraction and score.

## Frozen scientific decision and gates

The task decision is explicitly purity-constrained. A cell is feasible when public crystal purity
is at least `0.98`. Within the feasible set, select maximum crystal yield, then CSD quality, then
minimum fines. If no cell is feasible, select the highest-purity cell. This rule is fixed before
execution and may not be replaced by yield-only optimization.

Every calibration World must satisfy all of the following:

1. complete 16/16 execution denominator, no platform failure, exact replay and truth binding;
2. matched action plans and observation-noise coordinates for every paired cell;
3. no private intervention identifier in Participant-visible payloads;
4. crystal-purity law gap at least `0.01` at one or more cells;
5. at least one additional public endpoint with paired gap at least `0.03`;
6. resolving support in at least two cells separated on two design coordinates;
7. seed-by-law or cooling-by-law interaction at least the endpoint-specific effect gate, proving
   that the raw fork is non-parallel across the grid;
8. a change in the preregistered purity-constrained seed, cooling or duration decision.
9. fit the best constant-capacity parent-law multiplier from `{1, 2, 4, 6}` on the frozen cells
   `s0-t0-d0`, `s0-t1-d1`, `s1-t0-d1`, `s1-t1-d0`, using noise-normalized squared residuals
   for purity, yield, CSD quality and fines; on the disjoint four held-out cells, at least two
   cells must retain a residual of at least `2.0` declared final-assay standard deviations.

The candidate is selected only at `3/3` Worlds. A `0/3`, `1/3` or `2/3` outcome is retained as a
scientific failure. Thresholds, calibration seeds, denominator and decision rule may not be changed
after the first data-producing execution starts. Formal W01--W05 qualification remains
unauthorized until a selected candidate is frozen in a new machine contract.

Participant/provider calls: `0`.

## Pre-calibration platform correction

Before any candidate-tournament receipt was produced, the executable-law unit test evaluated a
dimensionless surface-capacity coefficient of `2`. It changed the generic midpoint public response
by only `0.00293`, below the pre-existing world-axis response floor of `0.005`; this was a platform
qualification failure, not calibration evidence. The coefficient is now frozen at `4` and the old
value is not a result or candidate observation.

The coefficient `4` is a **synthetic authoring constant**, not an empirical estimate or a result.
It multiplies the baseline occlusion capacity `0.02 mol impurity / mol target`, so the
frozen value corresponds to `0.08 mol/mol` before the supersaturation term. The authoring-valid
dimensionless range was bounded to `[2, 6]` (`0.04--0.12 mol/mol`) to represent moderate surface
enrichment without permitting impurity uptake to dominate target transfer. Value `4` is the central
point of that range and passes the unchanged `0.005` platform response floor. No calibration World,
formal World, threshold or task decision was inspected when making this correction.

The preregistered non-benchmark sensitivity points are `2`, `4` and `6`, corresponding to
`0.04`, `0.08` and `0.12 mol impurity / mol target` before the supersaturation factor. They span
the declared moderate-enrichment range and are retained for sensitivity reporting regardless of
which tournament outcome is observed. The surface half-saturation concentration is frozen at
`0.010 mol/L`.
