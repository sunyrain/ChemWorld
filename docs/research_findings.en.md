# Research Findings

!!! warning "Pre-v0.5 diagnostic results"
    The classical, Safe-GP, and early SAC numbers on this page predate the v0.5 candidate backend. They document protocols and failure modes; they are not rankings for the current 15-task release candidate.

> **ChemWorld has produced useful failures and control results, but not a completed benchmark release.**

!!! warning "Evidence tense"
    The RC28 numbers below are formal historical results on their frozen
    source. Static-S0 and task-contract work changed the current source
    fingerprint, so ten related bindings are now stale and
    `benchmark_ready=false`. The legacy 2026-07-27 two-task static-S0 result
    bundle is withdrawn and cannot support current paper numbers or rankings.
    Current benchmark readiness requires Gate A recertification.

## New finding: the replacement fixed-world campaigns are complete

The electrochemical replacement binds `nominal-prior-latent-v2`, an explicit
balanced-efficiency score, and anonymous material identities. Reaction-to-
crystallization now has an independent catalyst/solvent family that couples
materials to reaction kinetics and solvent identity to solubility, nucleation,
growth, and impurity occlusion. Both formal campaigns completed ten independent
worlds, twenty exploration experiments per world, paired blind validation,
full classic baselines, and exact replay.

Codex averages 0.7150 on electrochemical conversion and 0.5355 on
crystallization. The electrochemical paired descriptive difference against the
best information-matched baseline is +0.0991, while its interval against the
best privileged calibration baseline crosses zero. Crystallization trails LHS
(0.5708), so the campaign does not support a crystallization outperformance
claim. No superiority threshold or multiplicity plan was preregistered.

## New finding: information value is task-specific, and prior influence is not recovery

S0 v1.2 completes `opaque`, correct anonymous `nominal`, and fixed targeted
wrong-property `misindexed` arms on ten paired worlds. World seeds,
observation noise, the twenty-round budget, model, and blind endpoint are held
fixed:

- electrochemical nominal is 0.7874 versus 0.7150 opaque, a paired +0.0724
  with familywise 97.5% interval [+0.0074,+0.1546], confirming positive
  information value;
- crystallization nominal is 0.5615 versus 0.5355 opaque, a paired +0.0260
  with interval [−0.0130,+0.0630], so the result is inconclusive;
- electrochemical misindexed is 0.6853, 0.1020 below nominal, while
  crystallization misindexed is 0.5845, 0.0229 above nominal. Both wrong-prior
  contrasts exclude zero familywise, but in opposite directions.

Both wrong priors pass the early-action manipulation check. Electrochemistry
passes differential action correction but not performance recovery to opaque;
crystallization remains non-inferior to opaque but does not pass differential
action correction. Neither task passes the preregistered joint recovery rule.
The causal distinction matters: changing behavior does not show that the model
identified an error, and avoiding a score loss does not show correction.

All 60 cells pass exact replay: 2,280 physical experiments, 1,260 successful
subscription calls, five automatic retries, and zero method failures. The
result covers one fixed two-row swap per task and does not establish recovery
across arbitrary priors, tasks, mappings, or providers.

## Design finding: all 15 tasks need executable complete experiments

The completion audit found that three purification tasks had been mapped to a
generic reaction-only recipe and that evaporation and distillation shared
intensity coordinates. The corrected purification design has 16 independent
controls and 22 compiled operations; distillation has 13 controls with
independent temperature and time for both stages. The matrix generator executes
415 complete cases spanning midpoints, every coordinate's low/high intervention,
and all discrete categories. All 62 declared metrics bind to executable
evaluation endpoints. All 15 pass this expanded audit. This proves design executability, not formal performance
on the 13 non-confirmatory tasks.

## Evidence levels

| Level | Meaning |
| --- | --- |
| Implemented | A code path and interface exist |
| Control-validated | Executable controls establish environment behavior |
| Agent-demonstrated | An agent shows interpretable development behavior |
| Confirmatory | A frozen method is tested on an untouched cohort |
| Externally bridged | Independent backend, real data, or physical evidence supports it |

## Finding 1: objective gains can hide risk regressions

Unconstrained structured GP improved four task objectives while increasing operational-risk exceedance in three tasks.
Outcome alone was therefore insufficient.

## Finding 2: strict rules preserve meaningful failures

A frozen Safe-GP confirmation improved all four objectives and passed safety/cost rules. The flow effect was 0.018752
against a pre-registered practical threshold of 0.020000, so the all-task claim remained failed.

## Finding 3: the historical four-action certificate failed; calibrated RC28 Gate A passes

Nine task–mode controls establish deterministic execution, local response separation, bounded response,
conservation, and replay. At the preregistered four-experiment budget, the source-bound RC21 controlled matched
oracle reaches 239/240 (99.58%) and passes. The separately bound online-policy-feasible oracle reaches 230/240
(95.83%) overall, but the reaction `rate_law_family` reaches only 23/30, with a Wilson lower bound of 0.5907, so
historical RC21 Gate A remained false. The same family reaches 30/30 in the controlled certificate; the reaction material family
reaches 29/30 in both certificates.

This family is an upstream, pivot-normalized catalyst-activity-order stress on the primary target pathway—not a
crystal nucleation or growth rate law. The design audit proves that only the `target_formation` rate law changes
and that crystallization constitutive parameters remain fixed. RC22-d then evaluated all eleven admissible
four-action sets using disjoint fit, policy-selection-validation, and development-trial namespaces. Every set
failed world-clustered selection validation; the best weakest-family result was 16/24. The selected set obtained
20/20 for rate law, 20/20 for no change, 18/20 for topology, and 12/20 for material mapping in non-controlling
development trials; all four electrochemical families obtained 20/20. RC22-d does not control Gate A and did not
trigger a formal RC22 run. It localizes the remaining problem to a fixed four-action, single-reference,
single-likelihood online decoder that cannot robustly combine temporal and cross-action relational evidence—not
to physical non-identifiability of the reaction rate-law task.

A non-controlling budget extension then reused the exact RC21 fit/trial seeds, fixed policy, and public observation
contract to evaluate `k={1,2,4,8}`. Reaction accuracy was 53/120, 77/120, 111/120, and 112/120, while rate-law
recall was 0/30, 10/30, 23/30, and 23/30. The k=4 checkpoint exactly reproduced RC21; k=8 only improved no change
from 29/30 to 30/30, leaving the rate-law Wilson lower bound at 0.5907. Because this diagnostic reused formal
seeds, it cannot become new confirmatory evidence. It rules out the claim that simply extending the same fixed
cycle from four to eight steps closes the gap: the extra rounds add repeated evidence, not a new identifying
relation.

A subsequent non-certificate screening at only four worlds per family also rejected a naive myopic
posterior-EIG plus one-step reference-acquisition policy. It generated history-dependent action paths but often
repeated one locally high-information action. Reaction diagnosis reached only 10/16 (rate law 3/4, topology 4/4,
material 1/4, and no change 2/4), while electrochemistry reached 16/16. This low-power screen cannot estimate a
formal pass rate, and its implementation was not retained. It only establishes that a future adaptive method must
jointly plan reference coverage, temporal evidence, and cross-action relations, then pass independent selection
validation before preregistration.

RC21 also exposed a more basic protocol error. Although `change_time=1` technically executes one old-world
experiment, that experiment usually lies near the weak-signal rate-law pivot and does not establish the response
reference needed to say what changed from what. Version 0.3 therefore separates static current-world
identification, early uncalibrated nonstationarity, and calibrated online change attribution. The static track
never reports change probability. `change_time={0,1,2,4}` remains a non-controlling stress track. RC24 freezes
Gate A3 as online attainability of a reference diagnostic policy with truth support `never/6/8/10`; `tau` is the
number of completed old-world experiments. Reference sufficiency uses relation closure and within-campaign
pre-change cross-fitting. Changed and never use separate denominators, and detection is reported at
`k={1,2,4,8}`. A2, A3, and private confirmation each freeze 180 independent world clusters per task/family.
After the confirmatory-task semantics audit passed 25/25 and the physical
design audit passed 83/83, any formal conclusion still had to come from a new
untouched RC28 cohort. RC21, RC22-d, and RC23 cannot be promoted into v0.3
confirmatory evidence.

RC28 subsequently executed untouched formal cohorts under the calibrated
protocol. A2 completed 4,896/4,896 receipts and passed at the primary
five-experiment budget: active-oracle and fixed-decoder top-1 accuracy were
both 98.26% (95% CI 97.45–98.82), with every task/family intersection passing.
A3 completed 2,016/2,016 receipts. By `k=8`, the frozen reference policy reached
99.17% reference sufficiency, 99.35% changed detection recall, 0.9990 AUROC,
2.80% conditional no-change FPR, 98.03% conditional attribution, and 96.57%
end-to-end success. The frozen-source joint decision was `gate_a_pass=true` and
`benchmark_ready=true`, so Gate A was true for that source; the current binding is stale.

This new result resolves the environment-attainability question, not the
participant-Agent question. Gates B–E, Private-E/Private-A, cross-method
provider results, and publication evidence remain incomplete.

These results support environment-level identifiability diagnostics, not Agent-level mechanism discovery,
crystallization-kinetics discovery, or exact rate-parameter identification.

## Finding 4: current RL evidence diagnoses contracts, not rankings

The early 100,000-step SAC pipeline ran end to end, but development behavior omitted the core flow operation and
concentrated on adding, measuring, and terminating. Action, reward, and behavioral completion contracts are being
remediated before any formal multi-seed result.

## Finding 5: LLM evidence use requires causal ablation

Operation-level interaction, memory, spectrum disclosure, and resource
accounting are implemented. Formal fixed-world provider trajectories now exist
for two tasks, but there is no formal mechanism-adaptation or paired
spectrum/memory causal-ablation matrix; explanations alone do not prove that
spectra or memory changed decisions.

**Status:** benchmark candidate. No SOTA, completed RL/LLM ranking, mechanism-adaptation, or real-world transfer claim
is supported.

See the [versioned evidence page in Chinese](https://sunyrain.github.io/ChemWorld/benchmark_release/).
