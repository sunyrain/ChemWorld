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

## Finding 3: world shifts are executable; budgeted identification is still open

Nine task–mode controls establish deterministic execution, local response separation, bounded response,
conservation, and replay. The current action/intervention audit establishes decision relevance for each material
counterfactual, and the controlled matched-identifiability certificate passes. The online-policy-feasible certificate
remains pending, so Gate A as a whole remains false and Agent-level identification claims remain closed.

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
