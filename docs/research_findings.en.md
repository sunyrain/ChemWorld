# Research Findings

!!! warning "Pre-v0.5 diagnostic results"
    The classical, Safe-GP, and early SAC numbers on this page predate the v0.5 candidate backend. They document protocols and failure modes; they are not rankings for the current 15-task release candidate.

> **ChemWorld has produced useful failures and control results, but not a completed benchmark release.**

!!! warning "Evidence tense"
    The RC28 numbers below are formal historical results on their frozen
    source. Static-S0 and task-contract work changed the current source
    fingerprint, so nine RC28 bindings are now stale and
    `benchmark_ready=false`. The static-S0 results are current and
    replay-verified, but do not replace Gate A recertification.

## New finding: fixed-world optimization works better than explicit mechanism understanding

The 2026-07-27 formal static-S0 runs used the same `gpt-5.6-sol high`
method, 20 complete experiments, five world seeds, a separate final synthesis,
and paired blind validation. The statistical unit is the world seed; five
algorithm seeds are first averaged within each world. Electrochemical blind
mean was 0.3902 (95% CI [0.1732, 0.6072]) versus RF-EI at 0.4798, with a
paired difference of -0.0896 ([-0.2896, 0.1104]) and two world wins against
three losses. Reaction-to-crystallization reached 0.4829 ([0.4326, 0.5332])
versus GP-EI at 0.5324, with a paired difference of -0.0495
([-0.0933, -0.0056]) and zero wins against five losses.

![Static-S0 blind final scores by world](assets/images/static-s0-blind-scores-v0.1.png)

The model did use feedback: all ten best trials appeared after round 10.
Mean best-so-far increased by 0.0548 and 0.0599 between experiments 8 and 20.
However, predictive directional accuracy was only 64.4% and 44.4%, while
Declared structural-edge F1 was 0.274 and 0.242 and unsupported-claim rates
were 68.3% and 75.1%. Finding improved conditions is therefore not evidence
that the model has correctly learned the mechanism. All ten final syntheses
submitted tested conditions: eight had zero gain, two had small negative gain,
and none improved the incumbent.

![Static-S0 optimization curves](assets/images/static-s0-optimization-curves-v0.1.png)

These are frozen formal optimization estimands on the current backend, but
cover only five sampled worlds and one LLM trajectory per world. The strongest
classic family was selected descriptively from six candidates, so the
intervals are not preregistered superiority tests. The current roadmap
prioritizes independent model/provider replication, static final-synthesis
ablations, more static tasks, and a real-world bridge. Hidden world changes and
mechanism replacement are deferred rather than part of the current S0 roadmap;
Private-E/A and real-chemistry transfer also remain open.

## Design finding: all 15 tasks need executable complete experiments

The completion audit found that three purification tasks had been mapped to a
generic reaction-only recipe and that evaporation and distillation shared
intensity coordinates. The corrected purification design has 16 independent
controls and 22 compiled operations; distillation has 13 controls with
independent temperature and time for both stages. The matrix generator now
detects dead coordinates and executes every midpoint recipe. All 15 pass with
zero dead coordinates and zero unresolved formalization blockers. This proves
design executability, not formal performance on the 13 non-confirmatory tasks.

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

Operation-level interaction, memory, spectrum disclosure, and resource accounting are implemented. No formal real
provider trajectory matrix exists; explanations alone do not prove that spectra or memory changed decisions.

**Status:** benchmark candidate. No SOTA, completed RL/LLM ranking, mechanism-adaptation, or real-world transfer claim
is supported.

See the [versioned evidence page in Chinese](https://sunyrain.github.io/ChemWorld/benchmark_release/).
