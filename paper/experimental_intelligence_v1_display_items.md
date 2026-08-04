# ChemWorld: A Programmable Virtual Instrument for Measuring Experimental Process Profiles: numeric display items

Status: `frozen_complete`.
Derived-data SHA-256: `1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4`.

Every number in the tables below is rendered from the self-hashed arXiv derived-data
object. This file is intended for direct inclusion during manuscript typesetting.

## Main tables

### Table 1 | Qualified environment surface and formal evidence scope

| Quantity | Count | Evidence level |
| --- | --- | --- |
| registered task designs | 15 | release surface |
| typed operation types | 28 | release surface |
| instrument types | 5 | release surface |
| deterministic complete-experiment cases | 415 | design qualification |
| declared endpoints bound to evaluators | 62 | design qualification |
| tasks with formal compiled-agent results | 2 | paper evidence |
| tasks with autonomous-agent results | 1 | paper evidence |

Counts for the environment surface are design qualifications, not claims of agent
competence. Formal paper evidence covers fewer tasks than the registered surface.

### Table 2 | Compiled-control capability profiles (release label G0)

| Task | Information arm | Worlds | Final score | Held-out accuracy | Brier | Structure F1 | Mechanism F1 | Unsupported claims |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| electrochemical-conversion | opaque | 10 | 0.715 | 0.744 | 0.186 | 0.389 | 0.190 | 0.611 |
| electrochemical-conversion | nominal | 10 | 0.787 | 0.778 | 0.149 | not measured | not measured | not measured |
| electrochemical-conversion | misindexed | 10 | 0.685 | 0.711 | 0.209 | not measured | not measured | not measured |
| reaction-to-crystallization | opaque | 10 | 0.535 | 0.478 | 0.298 | 0.275 | 0.144 | 0.714 |
| reaction-to-crystallization | nominal | 10 | 0.562 | 0.433 | 0.316 | not measured | not measured | not measured |
| reaction-to-crystallization | misindexed | 10 | 0.584 | 0.433 | 0.316 | not measured | not measured | not measured |

Scores are means across ten simulator worlds. Dashes indicate endpoints that were not
defined for that information arm; they are not zeroes. No composite score is formed.

### Table 3 | Primitive-control development trajectories (release label G2 v0.4)

| Arm | Cells | Completion | Operations | Best score | Batch AUC | Realized-op AUC | Fixed-budget AUC | Discovery fraction | Retention | Max drawdown | Terminal / best | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| opaque | 5 | 1.000 | 82.600 | 0.631 | 0.617 | 0.520 | 0.563 | 0.320 | 0.520 | 0.333 | 0.671 | 0.500 |
| nominal | 5 | 1.000 | 80.400 | 0.709 | 0.589 | 0.501 | 0.591 | 0.800 | 0.720 | 0.092 | 0.941 | 0.800 |

Each arm contains five simulator-world cells and six completed vessels per cell.
Operations are mean submitted primitive attempts per cell. These development data select
the worlds and endpoints for G2 v0.5 and are excluded from its replication estimand.

### Table 4 | Fresh primitive-control trajectories (release label G2 v0.5)

| World | Replicate | Opaque state | Nominal state | Δ best score | Δ raw terminal | Δ mean score | Δ discovery | Δ retention | Δ drawdown | Δ terminal / best |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | r01 | completed | right_censored | not measured | not measured | not measured | not measured | not measured | not measured | not measured |
| 1 | r02 | completed | completed | 0.285 | 0.301 | 0.304 | 0.000 | 0.200 | -0.273 | 0.035 |
| 1 | r03 | completed | completed | -0.143 | 0.003 | -0.074 | 0.400 | 0.400 | -0.306 | 0.173 |
| 1 | r04 | completed | completed | 0.170 | 0.114 | 0.144 | -0.400 | 0.000 | 0.045 | -0.073 |
| 1 | r05 | completed | completed | 0.381 | 0.473 | 0.429 | -0.400 | 0.000 | -0.040 | 0.319 |
| 3 | r01 | completed | completed | -0.167 | 0.240 | -0.121 | 0.600 | 0.400 | -0.463 | 0.486 |
| 3 | r02 | completed | completed | -0.368 | -0.372 | -0.236 | -0.800 | -0.200 | 0.057 | -0.007 |
| 3 | r03 | completed | completed | 0.001 | 0.001 | -0.009 | 0.000 | 0.000 | -0.028 | 0.000 |
| 3 | r04 | completed | completed | 0.253 | 0.204 | 0.291 | -0.200 | 0.000 | 0.030 | -0.060 |
| 3 | r05 | right_censored | completed | not measured | not measured | not measured | not measured | not measured | not measured | not measured |

Deltas are nominal minus opaque within the same physical world and replicate block.
The two deliberately selected worlds are not pooled into a population-level estimate.
Terminal coverage: 18 completed cells, 2 right-censored cells, and 8 complete pairs (4 in world 1; 4 in world 3).
The frozen interpretation mapping selected `frequent_within_world_reversal`: 6 of 8 world-by-core-lifecycle classifications were mixed. Policy SHA-256: `93604ce8af7211f35c5d3b896609addef6d436f3248f45aba3cc04a11da9d67e`.
The frozen categorical lifecycle summary is supporting; the main continuous endpoint diagnostic compares best score with algebraically independent raw terminal score.
Provider sampling was not seed-controlled; the summary does not identify a causal provider effect or a variance-dominance relation.

## Figure legends

**Figure 1 | ChemWorld apparatus and controlled world forks.**
**A,** An agent selects a typed action; the executable world returns only the public
observation while recording the identity-bound transition. **B,** Hidden simulator-world
and material identity, action authority, evidence access, resource accounting and replay
are separate protocol controls. **C,** The frozen qualification changes one named private
component while preserving nine public-contract components. **D,** Six parent-child pairs
and 24 provider-free traces passed the registered programmability gates. These probes
establish the tested executable-world interventions, not agent performance, arbitrary
world recombination, rule adaptation or physical transfer.

**Figure 2 | Known policies qualify the experimental-process profile.**
**A,** Three frozen policies specify distinct evidence and terminal-decision structures.
**B,** Campaign-equal terminal profiles recover assay-all, threshold-gated and
immediate-discard signatures. **C,** Evidence acquisition, continued investment and
resource use remain separate readouts; registered undefined quantities remain null.
**D,** All 30 same-identity deterministic retests match their primary campaigns. The
primary evidence comprises 30 campaigns and 180 closed lifecycles; the additional 30
campaigns and 180 lifecycles are excluded reliability retests. This is a bounded positive
control in the simulated apparatus, not an endpoint, agent or model ranking.

**Figure 3 | Lifecycle completion does not specify terminal policy.**
**A,** The 120 closed lifecycles partition into 84 final assays and 36 explicit discards:
60 assays for the Codex-based complete system and 24 assays plus 36 discards for the
DeepSeek-based complete system. **B,** Terminal commitments by matched simulator world
and information arm; system identities include model, scaffold, transport and run
configuration. **C,** All 36 registered discard identities remain in the latent-terminal
audit, with 6 resolved and 30 unresolved after the frozen entry gate failed.
**D,** Registered censoring and finite-population bounds replace latent-dependent point
estimates; the no-discard-opportunity cell remains structurally null. Shadow assays were
evaluator-only counterfactual evaluations, were not agent choices or observations, and
did not add original agent experiments.

**Figure 4 | Compiled controls separate outcome, prediction, calibration and claims.**
**A,** All paired nominal-minus-opaque endpoint differences across ten designed worlds
per task; the ranges summarize finite-set resampling sensitivity rather than population
confidence intervals. **B,** Held-out
prediction and calibration are displayed as separate raw metrics. **C,** Opaque-arm
epistemic readouts retain registered missingness without imputation. **D,** Commit-frozen
manipulation, correction, performance-restoration and joint gates remain separate.
Classical optimizers are calibration controls, not the target competition; the figure
supports no scalar ranking or general population information effect.

**Figure 5 | Primitive-control agents expose complete experimental lifecycles.**
**A,** One descriptive seven-operation lifecycle makes a UV-visible observation available
before the next system decision and explicit final assay. **B,** The campaign resource
receipt reports units and denominators outside the prompt. **C,** Identity, resource
events and exact executable replay align the public process record with audit state.
**D,** Failed, rejected and terminal actions retain their distinct transaction and
closure
semantics. Operations are repeated events within campaigns, not independent samples;
replay concerns simulator state and records, not a physical batch or stochastic provider
decision.

**Figure 6 | Fresh trajectories reveal process structure omitted by endpoints.**
All ten pre-specified trajectory pairs are shown. **A,** The frozen selected-world design
contains eight complete matched pairs and two explicitly right-censored pairs. **B,**
Best-of-campaign and raw terminal contrasts
disagree in sign for 2/8 complete pairs; this is the primary endpoint diagnostic.
**C,** Continuous contrasts separately display discovery, retention, drawdown, recovery
and relative terminal retention. **D,** The 6/8 mixed classification is supporting and
threshold-sensitive, ranging from two to eight across the frozen sensitivity grid. These
deliberately selected worlds describe within-world process variation and are not pooled
into a population-level model or information-effect claim.
