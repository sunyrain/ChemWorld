# Research Findings

!!! warning "Pre-v0.5 diagnostic results"
    The classical, Safe-GP, and early SAC numbers on this page predate the v0.5 candidate backend. They document protocols and failure modes; they are not rankings for the current 15-task release candidate.

> **ChemWorld has produced useful failures and control results, but not a completed benchmark release.**

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

## Finding 3: controlled identifiability passes; the fixed four-action online certificate does not

Nine task–mode controls establish deterministic execution, local response separation, bounded response,
conservation, and replay. At the preregistered four-experiment budget, the source-bound RC21 controlled matched
oracle reaches 239/240 (99.58%) and passes. The separately bound online-policy-feasible oracle reaches 230/240
(95.83%) overall, but the reaction `rate_law_family` reaches only 23/30, with a Wilson lower bound of 0.5907, so
Gate A remains false. The same family reaches 30/30 in the controlled certificate; the reaction material family
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
never reports change probability. `change_time={0,1,2,4}` remains a non-controlling stress track. RC23 freezes
Gate A3 truth support as `never/6/8/10`, with `tau` defined only as the number of completed old-world experiments.
The Agent sees neither the earliest change point, support, reference-certificate state, nor evaluator checkpoint.
Reference sufficiency now requires universal relation coverage, held-out old-world predictive adequacy, and bounded
reference age. Reference failures stay in the end-to-end denominator while being excluded only from conditional
attribution. Development, A2, A3, and private confirmation use disjoint cohorts. The flagship semantics audit passes
18/18 and the physical design audit passes 81/81, but a new untouched A2/A3 execution is still required. RC21 and
RC22-d cannot be promoted into v0.3 confirmatory evidence.

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
