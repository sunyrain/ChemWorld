# W1-Q04 independent chemistry and chemical-engineering review

- Reviewer: `Yijun`
- Reviewed merged baseline: `43d27bfa14c3a813caa03b7378800bcb5ab69acf`
- Review date: `2026-08-03`
- Evidence verdict: **APPROVE** for F09, F10, the frozen world-fork certificate, and the known-policy validity report within their stated simulated-apparatus boundaries
- Current manuscript verdict: **CHANGES_REQUESTED**
- Overall W1-Q04 verdict: **CHANGES_REQUESTED** because the current manuscript exceeds the approved evidence ceiling
- Execution boundary: read-only report/source/manuscript review plus provider-free focused tests; no formal campaign, agent/provider, or latent shadow execution was run.

The F/V artifacts are internally careful about what was qualified: registered executable semantics, deterministic simulator transactions, bounded synthetic instruments, controlled single-private-component forks, and construct/discriminant-validity recovery for known policies. They do not need a chemistry rerun for this review. The current manuscript sometimes removes those qualifiers and turns a limited certificate into claims of general physical identity/replay and arbitrary component recombination. Those wording defects must be corrected by S04-S07 and rechecked by Q05 before publication integration.

## Reviewed evidence bindings

| Surface | Path | File SHA-256 | Verdict |
| --- | --- | --- | --- |
| F09 platform surface | `workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json` | `f9ad46d399bfde37389d8e93a2846a92b98e2ee405a11b04db0beef53485ba59` | **APPROVE** |
| F10 experiment semantics | `workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json` | `cce0455d11d8081a57007fc5ec47e5988bfe3c8cf9dfb1f67da583c82c7350cc` | **APPROVE** |
| F world-fork certificate | `workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json` | `8a0299b6957a700e720f46401a62b30a1da4ac2f8d71d57f00071805abcf9ad9` | **APPROVE** |
| F world-fork qualification | `workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json` | `d16981dd3937d661ae65a972bcaacd22c793f086403410f78d103078d25288b8` | **APPROVE** |
| V known-policy validity | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json` | `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee` | **APPROVE** |
| Current manuscript migration input | `paper/experimental_intelligence_v1_manuscript.md` | `0eeac2c3f3be5cb3823736a7b92869be15390d74e0240a3643af422518c44717` | **CHANGES_REQUESTED** |

The approved embedded content identities are: F09 audit `941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77`; F10 qualification `91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3`; world-fork certificate `5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78`; world-fork formal qualification `62684d414e9f9037b70d170abc6b29b442a928cf76df900a6bb53a3d60f2ee02`; V validity report `ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064`.

## F09 platform-surface counting — APPROVE

The approved statement is a capability and qualification inventory, not an experimental result:

- `15` means live registered task contracts. It does not mean 15 formal agent tasks or 15 empirically validated chemistries.
- `28` means globally unique registered typed operation kinds in the qualified operation registry. The campaign-only `discard_batch` terminal decision is not an additional member of this count.
- `5` means globally unique public instrument contracts, not five empirically calibrated devices.
- `62` means ordered task-by-metric evaluator bindings. The same metric used by multiple tasks contributes multiple bindings; the registry contains 43 unique metric identifiers, not 62 unique metrics.
- `415` means executed complete-experiment boundary recipes. These are qualification executions, not tasks, agents, independent samples, or physical experiments.

Allowed wording: “15 registered task contracts, 28 typed operation kinds, five public instrument contracts, 62 task-specific evaluator bindings, and 415 executed boundary recipes.”

Forbidden wording: “15 tested agent tasks,” “62 metrics,” “415 experiments” without the qualification/boundary-recipe unit, or any statement that these counts establish real-laboratory validity.

## F10 operations, transactions, resources, and instruments — APPROVE

### Transaction and resource semantics

The qualification supports these exact meanings:

- Only `committed` installs a candidate simulator-state transition.
- `validation_failed`, `rolled_back`, and `campaign_resource_rejected` preserve the pre-action simulator physical state; they may still preserve a declared attempt charge or process penalty in the audit trail.
- Operation attempts are reserved at preflight. Stock, vessel-start, and instrument-use debits occur only for committed outcomes under the campaign card.
- The resource ledger is an external, event-hashed accounting contract that round-trips from a snapshot. This is a simulator accounting invariant, not a material certificate for a physical laboratory.
- Instrument latency is a declared scheduling quantity and must not be described as elapsed process or device time.

The human report correctly says “candidate physical state” only inside the executable world and immediately denies physical-device and real-world-safety validation. Downstream prose should prefer “simulator state” on first use, then define any shorter “physical state” terminology explicitly as the world's hidden physical-state representation.

### Chemistry and model-maturity boundary

The executable suite includes fail-closed state constitutions, task-scoped mass/charge/energy/process diagnostics, reference tests, and maturity/model-card labels. Serious-task contracts reject proxy-allowed kernels, while individual runtime modules declare their lowest maturity level. This supports a chemistry-native, state-coupled executable apparatus with explicit invariants and maturity metadata.

It does not support these stronger claims:

- empirical calibration of HPLC, GC, UV-vis, pH, or final-assay outputs against physical instruments;
- universal conservation or predictive accuracy outside the exact registered task/runtime slice;
- industrial process fidelity, real-world safety validation, or deployment readiness;
- treating `reference_validated` as experimental validation of a device or material system.

Allowed instrument wording: “bounded state-coupled synthetic instrument semantics with declared cost, sample, scheduling, termination, and maturity contracts.”

Forbidden instrument wording: “calibrated instruments,” “measured laboratory spectra/chromatograms,” or “validated devices” unless a separate physical bridge supplies that evidence.

## F world-fork programmability — APPROVE within the frozen certificate

The certificate supports exactly two preregistered intervention classes—`material_law_counterfactual` and `mechanism_or_constitutive_law`—across three seeds each. All six parent-child pairs changed one declared private target, preserved nine declared public-contract components, executed the same fixed typed sequence, crossed the registered simulator-state and public-observation divergence thresholds, replayed exactly, and used zero providers.

Allowed wording: “ChemWorld constructed and qualified content-addressed single-private-component forks for two registered intervention classes while preserving the declared public experimental contract.”

Forbidden wording:

- arbitrary mechanisms, observation channels, instruments, resources, and failure laws have all been recombined and validated;
- the fork demonstrates agent adaptation, law learning, or a causal agent response;
- “physical response” or “physical replay” without making clear that the quantity is simulator-state response or exact executable-trajectory replay;
- direct transfer to a physical laboratory or a general third-party world-authoring language.

## V known-policy measurement validity — APPROVE within construct boundaries

The V report recovers prespecified profiles, nulls, partial orderings, resources, matched-arm invariance, and deterministic retests for three known deterministic policies in five simulated worlds and two information arms. The primary unit is an equally weighted original campaign profile; retests are reliability evidence and do not inflate the primary estimand.

This is valid bounded construct/discriminant evidence for the experimental-agency profile. It is not evidence of chemical intelligence, agent/model competence, endpoint superiority, causal information effects, stochastic-agent reliability, physical chemistry validity, or real-laboratory generalization.

## Current manuscript findings — CHANGES_REQUESTED

The current manuscript is migration input rather than the final authority, but these phrases exceed the approved F/V claim boundary and must not survive S04-S07 integration:

1. `paper/experimental_intelligence_v1_manuscript.md:90-92` claims “exact physical replay.” Replace with “exact environment/trajectory replay” and preserve the explicit exclusion of model-token regeneration.
2. `:146-149` and `:493-501` shorten the qualified counts to “28 operation types,” “415 boundary cases,” and “62 evaluator-bound endpoints.” Use the exact F09 units above, including “task-specific evaluator bindings” and “executed complete-experiment boundary recipes.”
3. Figure 1 wording at `:157-161` and later repeated “physical identity/world” wording should define these as matched hidden simulator-world identities. It must not imply a cloned material batch or physical apparatus.
4. `:465-470` says mechanisms, observation channels, material semantics, instruments, resource endowments, and failure laws “can therefore be recombined” while audit semantics stay fixed. The frozen certificate tested only two single-private-component intervention classes. Rewrite this as a bounded demonstrated result plus a clearly labeled future architecture capability; do not enumerate untested recombinations as established evidence.
5. Any mention of instruments, conservation, or maturity must retain “synthetic/state-coupled,” task/runtime scope, and model-card boundaries. Physical or high-fidelity bridging belongs to future validation, as the manuscript already acknowledges at `:481-485`.

## Bounded downstream remediation

- W1-S04 must use the approved F09/F10/fork wording and replace the overbroad programmability paragraph.
- W1-S05 must present V as a known-policy profile positive control, not chemistry or agent competence.
- W1-S07 must enforce the exact counting units and replace ambiguous “physical replay/world” shorthand at first reference.
- W1-Q05 must reject any final title, abstract, caption, or Discussion language that upgrades synthetic/reference-validated semantics into physical validation or upgrades two fork classes into arbitrary recombination.
- No F/V formal rerun is required by this review. If authors want the broader recombination or physical-calibration claims, those require new preregistration and evidence outside the current Work I claim surface.

## Validation disposition

- All six cited files exist and their SHA-256 values match the reviewed baseline.
- Provider-free focused checks for experiment semantics, world-fork public-contract/divergence, serious-task proxy policy, and state-transition invariants passed.
- Formal/agent/provider executions: `0`.
- Review write set: only this report and `workstreams/arxiv_v1/claims/W1-Q04--Yijun.md`.
- `git diff --check`: required before handoff.

## Final disposition

- W1-F09 evidence: **APPROVE**.
- W1-F10 evidence: **APPROVE**.
- W1-F world-fork evidence: **APPROVE** within two frozen single-private-component intervention classes.
- W1-V known-policy evidence: **APPROVE** within the simulated construct-validity boundary.
- Current manuscript consumption: **CHANGES_REQUESTED**.
- W1-Q04 overall: **CHANGES_REQUESTED** until S04-S07 apply the bounded wording corrections and Q05 verifies the integrated manuscript.

