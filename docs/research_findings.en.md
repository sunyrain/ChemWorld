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

## Finding 3: controlled identifiability passes; the online material family still fails

Nine task–mode controls establish deterministic execution, local response separation, bounded response,
conservation, and replay. At the preregistered four-experiment budget, the RC20 controlled matched oracle reaches
235/240 (97.92%) and passes. The separately bound online-policy-feasible oracle reaches 227/240 (94.58%) overall,
but the reaction catalyst-mapping counterfactual reaches only 22/30 and fails the per-family Wilson rule,
so Gate A remains false. The `rate_law_family` reaches 29/30 in both certificates and is not the blocker. RC20 binds that family
to the upstream primary target pathway through a pivot-normalized catalyst-activity-order stress while proving that
crystallization constitutive parameters remain unchanged. This supports controlled identifiability, not Agent-level
mechanism discovery, crystallization-kinetics discovery, or exact rate-parameter identification.

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
