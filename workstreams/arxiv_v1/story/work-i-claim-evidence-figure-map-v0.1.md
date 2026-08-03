# Work I Claim–Evidence–Figure Map

Status: **story input complete; manuscript/figure/data integration pending**
Task: `W1-S01`
Owner: `Yijun`
Authority: `workstreams/arxiv_v1/WORK_I_TODOLIST.md` (`b0d881b2bb3f4922ec021433290ed01e5fd51c97aa9e37120a5e72b02023bb29`)

This map fixes the bounded wording, evidence identity, analysis unit, manuscript responsibility, and planned figure location for 37 Work I claims. It is an isolated story input: it does not replace the manuscript, derived-data layer, figure manifest, evidence DAG, experiment ledger, or release manifest.

## Evidence registry

Each claim below names a source ID. The ID resolves here to an exact repository path, current file SHA-256, artifact content hash where one is defined, and current scientific/task status.

| Source ID | Path | Current file SHA-256 | Artifact content hash | Status |
| --- | --- | --- | --- | --- |
| `platform_surface` | `workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json` | `f9ad46d399bfde37389d8e93a2846a92b98e2ee405a11b04db0beef53485ba59` | audit `941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77` | W1-F09 `DONE` |
| `experiment_semantics` | `workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json` | `cce0455d11d8081a57007fc5ec47e5988bfe3c8cf9dfb1f67da583c82c7350cc` | qualification `91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3` | W1-F10 `DONE` |
| `world_fork_certificate` | `workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json` | `8a0299b6957a700e720f46401a62b30a1da4ac2f8d71d57f00071805abcf9ad9` | certificate `5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78` | W1-F07 `DONE` |
| `known_policy_validity` | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json` | `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee` | report `ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064` | W1-V09 `DONE`; `positive_control_established` |
| `g2_system_comparison` | `workstreams/arxiv_v1/reports/g2-agent-system-comparison-v0.1.json` | `a200ba914a3d6324daa6a8c359b771aaf11346382ca3bbebb317c1913a2d67a6` | comparison `5d534615aa0eb070b1a8ddf7cf123c2548bc8e4c948a98ffe2eafb0b545ef93e` | completed audited descriptive demonstration |
| `legacy_derived_data` | `benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json` | `fa09a93df6110bb4ca119403ab720619a1b56a35efdf7628d4629d761ef67995` | derived data `62500476b1666bfc19c4b1a4f0f00b60b8fffff49cfc56495396f856248edd7c` | frozen pre-Work-I layer; D03 reintegration pending |
| `g0_formal` | `workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json` | `309db48ff0f60b6f00ad4b40ec0bb5cdba19b8810c7239cd3e3b826dfde96001` | canonical JSON `70b79e126953c4ac61b3d44e4b825909b604123de90ac6f2a628244d81a8cac3` | formal descriptive, historical source-bound |
| `g0_three_arm` | `workstreams/flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json` | `af8e56c1bd42d02efde7680dab3fa9453f7bd69d450a450a71aade1afb15d8fb` | canonical JSON `becff70ecbc33aa4c151fcdf16a7a100e2a5b032acb97a38aad4c1eddaa2e516` | formal descriptive, historical source-bound |
| `g2_v04_compact` | `workstreams/G2_CODEX_SOL_MEDIUM_MCP_5X2_V04_RESULTS_ZH.md` | `e515d355a844f0277000af7f09f618c0cbe6a13c8f3644f17ed641f17bd750ed` | source audit `bc7495315745272c95fb326b7b50fb509081ad70323354899a233abac6c7b4a9` | completed audited development/hypothesis-generating |
| `g2_v05_terminal_accounting` | `workstreams/arxiv_v1/reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json` | `c82bdfd89c4d30711d10953840803045f7003046baaf0c8fb677d9907d8b19dd` | audit `c609cd34867331d6df41e7b72a1c01429fd48c42b3400f9e9a331956b49a5563` | completed with two right-censored cells |
| `latent_contract` | `configs/benchmark/work_i_latent_terminal_contract_v0.1.json` | `e69db432f7018a3cc41287fa02335337c624caf5ba7f0b487a0695809e052ce5` | contract `55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30` | W1-L01 `REVIEW`; outcome-blind protocol only |
| `latent_reconstructability` | `workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json` | `ec18b041543f44b9c2d2f16ee56a08da727efbe0128622778a8ae6d688afcba3` | report `995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857` | W1-L02 `REVIEW`; reconstructability only |
| `latent_replay_claim` | `workstreams/arxiv_v1/claims/W1-L03--codex-1.md` | `90cd6a4057bfc723b3daa8cb42e66f91a703e866eb6ec15487a3dc9e62e26982` | n/a | W1-L03 `CLAIMED`; implementation only |
| `latent_analysis_claim` | `workstreams/arxiv_v1/claims/W1-L04--Yijun.md` | `076247ad0c4a63318e60eaf61499c4e1a0accb7be54e50c783c71176e72e4538` | n/a | W1-L04 `CLAIMED`; implementation only |
| `current_registry` | `configs/current.json` | `77fe47591b15de09918da809d7bc280a038481eeb8fdc90e757c21b298482df8` | n/a | working manuscript; publication false; stale bindings recorded |

## 1. Center thesis

### `W1-CENTRAL-01` — title-level apparatus claim

- Allowed: “Programmable chemical worlds make experimental agency measurable: ChemWorld combines executable experimental contracts, controlled single-component world forks, a known-policy positive control, and auditable complete-system trajectories.”
- Forbidden: a universal theorem, scalar intelligence score, general agent superiority, or physical-laboratory validation.
- Evidence: `experiment_semantics` (`DONE`), `world_fork_certificate` (`DONE`), `known_policy_validity` (`DONE`). Exact paths and hashes are in the registry.
- Analysis unit: apparatus-level triangulation across independently audited contracts/certificates, not a pooled statistical sample.
- Manuscript: title, abstract, Introduction, Discussion, Conclusion.
- Figure: Fig. 1A-D overview. F and V have both passed, so the programmable title is eligible.
- State: `frozen_publication_evidence`.

### `W1-CENTRAL-02` — endpoint underdetermination

- Allowed: lifecycle completion or an endpoint score does not uniquely specify the experimental policy or trajectory that produced it.
- Forbidden: endpoints are useless; every equal endpoint has a different policy; trajectory differences identify an internal mental state.
- Evidence: `g2_system_comparison` (completed descriptive) and `legacy_derived_data` (frozen, pending Work I reintegration).
- Analysis unit: complete system × matched world-arm cell for terminal policy; fresh arm pair within selected world for trajectory contrasts.
- Manuscript: Introduction; complete-system Results; process Results; Discussion.
- Figure: Fig. 3A-B and Fig. 6A-B.
- State: `completed_descriptive_evidence`.

## 2. Apparatus

### `W1-APP-01` — qualified surface

- Allowed: 15 registered task contracts, 28 operation kinds, five instruments, 415 executed boundary recipes, and 62 task-specific evaluator bindings.
- Forbidden: 15 formal agent results; 62 unique metrics; qualification proves competence.
- Evidence: `platform_surface` (`DONE`).
- Analysis unit: the count-specific registered contract, unique kind, binding, or executed recipe.
- Manuscript: Apparatus; Methods 10.1. Figure: Fig. 1B,D.
- State: `frozen_publication_evidence`.

### `W1-APP-02` — executable experiment contract

- Allowed: an experiment is a stateful sequence of typed operations and measurements with explicit termination, final assay, resources, failures, and evaluation—not a value query.
- Forbidden: every operation is physically realistic; declared latency is wall-clock process time; instruments are calibrated to real devices.
- Evidence: `experiment_semantics` (`DONE`).
- Analysis unit: typed operation/instrument contract under qualification.
- Manuscript: Apparatus 3.1; Methods 10.1/10.3. Figure: Fig. 1A-C.
- State: `frozen_publication_evidence`.

### `W1-APP-03` — transactions, failures, instruments

- Allowed: 28/28 valid operation probes committed, 28/28 invalid probes preserved physical state, and 5/5 instrument probes matched their declared semantics.
- Forbidden: invalid means zero cost/penalty; simulated failure semantics establish real safety.
- Evidence: `experiment_semantics` (`DONE`).
- Analysis unit: 28 valid/invalid probe pairs and five instrument probes.
- Manuscript: Apparatus 3.2; Methods 10.1/10.9. Figure: Fig. 1C.
- State: `frozen_publication_evidence`.

### `W1-APP-04` — identity and replay

- Allowed: environment transitions, public observations, resources, world identity, and evaluation are content-bound and exactly replayable; a fresh provider session remains a new decision trajectory.
- Forbidden: exact replay regenerates model tokens or proves the model deterministic.
- Evidence: `experiment_semantics` (`DONE`) and `legacy_derived_data` (pre-Work-I frozen layer).
- Analysis unit: stored transition/resource event; session pair for fresh trajectories.
- Manuscript: Apparatus 3.2; Methods 10.9. Figure: Fig. 1C.
- State: `frozen_publication_evidence`.

## 3. Programmability

### `W1-PROG-01` — controlled fork

- Allowed: content-addressed single-private-component forks preserve all nine declared public-contract components.
- Forbidden: arbitrary third-party DSL, multi-component causal identification, or agent law learning.
- Evidence: `world_fork_certificate` (`DONE`).
- Analysis unit: one parent-child pair with one registered private change.
- Manuscript: Programmability Results/Methods. Figure: Fig. 1A-C.
- State: `frozen_publication_evidence`.

### `W1-PROG-02` — qualification outcome

- Allowed: two intervention classes × three seeds produced six passing pairs and 24 deterministic original/replay traces; same sequence, registered divergence, exact replay, and zero providers all passed.
- Forbidden: 24 independent agent trials or extrapolation beyond the two intervention classes.
- Evidence: `world_fork_certificate` (`DONE`).
- Analysis unit: six parent-child pairs; trace count is execution accounting.
- Manuscript: Programmability Results. Figure: Fig. 1C-D.
- State: `frozen_publication_evidence`.

### `W1-PROG-03` — fork boundary

- Allowed: controlled programmability of the executable apparatus under a deterministic fixed-policy probe.
- Forbidden: agent adaptation/performance, physical transfer, or fully general world authoring.
- Evidence: `world_fork_certificate` (`DONE`).
- Analysis unit: certificate boundary.
- Manuscript: programmability close; Limitations. Figure: Fig. 1 caption.
- State: `boundary_only`.

## 4. Measurement validity

### `W1-VALID-01` — multidimensional construct

- Allowed: terminal commitment, evidence acquisition, evidence-conditioned action, resource deployment, and outcome trajectory are separate observable axes; endpoint context is separate.
- Forbidden: a scalar intelligence score or latent-state interpretation.
- Evidence: `known_policy_validity` (`DONE`).
- Analysis unit: one equally weighted campaign profile.
- Manuscript: Measurement-validity Results/Methods. Figure: Fig. 2A.
- State: `frozen_publication_evidence`.

### `W1-VALID-02` — profile recovery

- Allowed: the 5 × 2 × 3 matrix recovered registered signatures, nulls, six partial orderings, resources, and matched-arm invariance for three known deterministic policies.
- Forbidden: competitive endpoint baselines, endpoint ranking, or causal information-null inference.
- Evidence: `known_policy_validity` (`DONE`).
- Analysis unit: 30 campaign profiles / 180 closed lifecycles; construct profiles precede aggregation.
- Manuscript: Measurement-validity Results. Figure: Fig. 2B-C.
- State: `frozen_publication_evidence`.

### `W1-VALID-03` — frozen gates and non-degeneracy

- Allowed: 12/12 gates passed; `measure_then_threshold` produced 28 assays and 32 discards; providers = 0.
- Forbidden: formal-world threshold retuning or treating 180 lifecycles as independent inferential replicates.
- Evidence: `known_policy_validity` (`DONE`).
- Analysis unit: registered gate/campaign profile; branch counts are census accounting.
- Manuscript: Measurement-validity Results/Methods. Figure: Fig. 2C-D.
- State: `frozen_publication_evidence`.

### `W1-VALID-04` — deterministic reliability

- Allowed: 30/30 same-identity original/retest campaign pairs matched all registered identity/profile/component checks; retests are excluded from the primary estimand.
- Forbidden: variability across stochastic agents or external validity.
- Evidence: `known_policy_validity` (`DONE`).
- Analysis unit: 30 deterministic pairs outside the primary estimand.
- Manuscript: Measurement-validity reliability. Figure: Fig. 2D or Extended Data.
- State: `frozen_publication_evidence`.

### `W1-VALID-05` — validity boundary

- Allowed: a bounded construct/discriminant-validity positive control for the simulated apparatus.
- Forbidden: endpoint ranking, provider capability, scalar intelligence, causal information effects, or laboratory generalization.
- Evidence: `known_policy_validity` (`DONE`).
- Analysis unit: bounded positive-control matrix.
- Manuscript: Measurement-validity close; Limitations. Figure: Fig. 2 caption.
- State: `boundary_only`.

## 5. Complete-system terminal policy

### `W1-TERM-01` — closure

- Allowed: two distinct complete agent systems each closed 60/60 batch lifecycles in the same five worlds × two arms.
- Forbidden: “independently configured” if it implies model-only matching; closure equals task-quality equivalence.
- Evidence: `g2_system_comparison` (completed descriptive).
- Analysis unit: complete system × matched world-arm cell.
- Manuscript: Complete-system Results/Methods. Figure: Fig. 3A.
- State: `completed_descriptive_evidence`.

### `W1-TERM-02` — assay/discard decomposition

- Allowed: the 120 closures are 84 assays + 36 discards; Codex = 60/0, DeepSeek = 24/36.
- Forbidden: omit 84/36; label discard incomplete/failure; infer economic optimality.
- Evidence: `g2_system_comparison` (completed descriptive).
- Analysis unit: terminal-decision census per system.
- Manuscript: Abstract; Complete-system Results; Discussion. Figure: Fig. 3A-B.
- State: `completed_descriptive_evidence`.

### `W1-TERM-03` — separable policy coordinates

- Allowed: non-final instruments were 164 vs 163, operations 815 vs 889, and terminal commitment differed; evidence acquisition, continued investment, and termination remain separate.
- Forbidden: equal instrument counts imply equal evidence quality; backend-only attribution.
- Evidence: `g2_system_comparison` (completed descriptive).
- Analysis unit: ten-cell system aggregate.
- Manuscript: Complete-system Results. Figure: Fig. 3B.
- State: `completed_descriptive_evidence`.

### `W1-TERM-04` — within-DeepSeek information profile

- Allowed: nominal cells had 16 assays/14 discards versus opaque 8/22, with +67 operations; five-world descriptive profile only.
- Forbidden: population information effect or cross-system ranking.
- Evidence: `g2_system_comparison` (completed descriptive).
- Analysis unit: five paired worlds within DeepSeek.
- Manuscript: Complete-system secondary result. Figure: Fig. 3B support/Supplement.
- State: `completed_descriptive_evidence`.

### `W1-TERM-05` — complete-system boundary

- Allowed: apparatus-portability and complete-system behavior-profile demonstration.
- Forbidden: causal backend effect, because model, scaffold, transport, retry behavior, and source identities differ.
- Evidence: `g2_system_comparison` (completed descriptive).
- Analysis unit: complete system, not backend.
- Manuscript: Complete-system framing/Methods. Figure: Fig. 3 caption.
- State: `boundary_only`.

## 6. Compiled controls

### `W1-COMP-01` — scale and role

- Allowed: 29,580 nonduplicated compiled executions across two tasks calibrate task, information, outcome, prediction, calibration, and claim readouts.
- Forbidden: 29,580 independent samples or autonomous primitive-control experiments.
- Evidence: `g0_formal` and `g0_three_arm` (formal descriptive).
- Analysis unit: paired physical world; executions report apparatus use.
- Manuscript: Compiled-control Results/Methods. Figure: Fig. 4A-D.
- State: `frozen_publication_evidence`.

### `W1-COMP-02` — task-specific information outcomes

- Allowed: nominal-minus-opaque mean endpoint contrasts were +0.0724 electrochemical and +0.0260 crystallization across ten matched worlds per task, with task-specific descriptive intervals.
- Forbidden: task pooling, universal positive prior effect, or population coverage from finite-world intervals.
- Evidence: `g0_three_arm` (formal descriptive).
- Analysis unit: ten paired worlds per task.
- Manuscript: Compiled-control Results. Figure: Fig. 4A.
- State: `frozen_publication_evidence`.

### `W1-COMP-03` — misindexed control

- Allowed: the fixed wrong prior changed early actions in both tasks, but neither task passed the joint recovery rule; action correction and performance restoration differ.
- Forbidden: general misinformation correction or sampled benefit as belief-revision proof.
- Evidence: `g0_three_arm` (formal descriptive).
- Analysis unit: ten paired worlds per task under one fixed misindexing.
- Manuscript: Compiled-control Results/Methods. Figure: Fig. 4B-C.
- State: `frozen_publication_evidence`.

### `W1-COMP-04` — optimization/cognition profile

- Allowed: endpoint, held-out direction, Brier calibration, structural/mechanistic declarations, and unsupported-claim rate are separate coordinates.
- Forbidden: causal inference among diagnostics or an unregistered composite score.
- Evidence: `g0_formal` plus `legacy_derived_data` (D03 reintegration pending).
- Analysis unit: task-arm summary across ten worlds; metrics remain separate.
- Manuscript: Compiled controls. Figure: Fig. 4D.
- State: `frozen_publication_evidence`.

### `W1-COMP-05` — no leaderboard

- Allowed: classical optimizers are compiled-interface calibration controls.
- Forbidden: LLM vs BO leaderboard, G2 vs G0 superiority, or unmatched authority as method-only intervention.
- Evidence: `g0_formal` (formal descriptive).
- Analysis unit: interface-specific calibration.
- Manuscript: compiled framing; Discussion. Figure: Fig. 4 caption.
- State: `boundary_only`.

## 7. Process profiles

### `W1-PROC-01` — development profiles

- Allowed: five-world development trajectories expose discovery, retention, drawdown, recovery, terminal retention, evidence use, and resources and motivate the fresh-session questions.
- Forbidden: confirmatory prior effects from one trajectory per cell or selected examples as the replication estimand.
- Evidence: `g2_v04_compact` (development only) and `legacy_derived_data`.
- Analysis unit: one campaign per world-arm; five paired worlds.
- Manuscript: Autonomous lifecycle/process profiles. Figure: Fig. 5A-C.
- State: `completed_development_only`.

### `W1-PROC-02` — fresh-session design/accounting

- Allowed: two selected worlds × five planned arm pairs, 20 cells, 120 opportunities, 18 complete cells, two right-censored cells, 114 executed vessels, 112 assays, eight complete pairs.
- Forbidden: hide censoring, count six unstarted slots as executed, or generalize two selected worlds.
- Evidence: `g2_v05_terminal_accounting` and `legacy_derived_data`.
- Analysis unit: world × fresh replicate; complete arm pair for contrasts.
- Manuscript: Fresh-session Results/Methods. Figure: Fig. 6A-B.
- State: `completed_descriptive_evidence`.

### `W1-PROC-03` — endpoint discordance

- Allowed: best and raw-terminal contrasts were sign-discordant in 2/8 complete pairs; descriptive Pearson `r=+0.826`.
- Forbidden: terminal-to-best as an algebraically independent diagnostic, a hypothesis-test result, or “endpoints usually reverse.”
- Evidence: `legacy_derived_data` (frozen; D03 reintegration pending).
- Analysis unit: eight complete fresh-session pairs.
- Manuscript: Fresh-session Results. Figure: Fig. 6A.
- State: `completed_descriptive_evidence`.

### `W1-PROC-04` — categorical sensitivity

- Allowed: 6/8 world-by-core-lifecycle classifications were mixed at the frozen 75% rule; supporting only, while continuous contrasts and censored rows stay visible.
- Forbidden: 6/8 as the primary conclusion, eight independent units, or omission of the 2-8 sensitivity range.
- Evidence: `legacy_derived_data` (frozen; D03 reintegration pending).
- Analysis unit: eight dependent descriptive world-metric classifications.
- Manuscript: supporting Result/Methods sensitivity. Figure: Fig. 6B/Supplement.
- State: `completed_descriptive_evidence`.

### `W1-PROC-05` — fresh-trajectory boundary

- Allowed: process profiles changed across fresh sessions within the two selected physical worlds; provider sampling seed was uncontrolled.
- Forbidden: provider-causal attribution, variance dominance, or a general information effect.
- Evidence: `legacy_derived_data`.
- Analysis unit: fresh session pair within selected world.
- Manuscript: Fresh Results; Limitations. Figure: Fig. 6 caption.
- State: `boundary_only`.

## 8. Latent terminal audit — pending, not a current result

### `W1-LATENT-01` — outcome-blind contract

- Allowed now: a contract registers a finite-population evaluator-only audit of 60 DeepSeek lifecycles (24 assays + 36 discards), 36 planned shadows, fixed estimands/thresholds/denominators/censoring/entry rules.
- Forbidden now: any latent score, regret, false-discard, precision, or quality conclusion.
- Evidence: `latent_contract` (W1-L01 `REVIEW`).
- Analysis unit: 60-lifecycle census; 36 discard units; ten cells, with oracle regret on the nine discard-containing cells.
- Manuscript: protocol placeholder only. Figure: Fig. 3C placeholder, no quantitative panel.
- State: `review_pending_not_publication_claim`.

### `W1-LATENT-02` — reconstructability only

- Allowed now: L02 reports 36/36 pre-discard checkpoints reconstructable, with zero shadow evaluations, zero latent-score access, and zero providers.
- Forbidden: reconstructability equals terminal quality; historical hidden-state-digest comparison; shadow execution occurred.
- Evidence: `latent_reconstructability` (W1-L02 `REVIEW`).
- Analysis unit: 36 checkpoints across ten source trajectories.
- Manuscript: Methods qualification/Supplement only pending review. Figure: Fig. 3C annotation only.
- State: `review_pending_not_publication_claim`.

### `W1-LATENT-03` — implementation status

- Allowed now: L03 replay/replacement and L04 analysis are implementation tasks; L05 alone owns formal execution and L06 the frozen report.
- Forbidden: claimed code or synthetic qualification as formal evidence; outcome access before freeze.
- Evidence: `latent_replay_claim` and `latent_analysis_claim` (both `CLAIMED`; exact paths and file hashes are in the registry).
- Analysis unit: none; status only.
- Manuscript/Figure: no Results language and no result panel.
- State: `pending_implementation`.

### `W1-LATENT-04` — future allowable outputs

- Allowed only after L05-L06: discarded-state scores/deltas/regret, false-discard fraction, assay precision/recall, decision-time regret, registered sensitivity, and unresolved-outcome bounds.
- Forbidden always: the shadow assay was chosen/observed by the agent; discard saved real resources; general rationality/irrationality; system ranking.
- Evidence: `latent_contract` (W1-L01 `REVIEW`, protocol only).
- Analysis unit: exact frozen lifecycle/campaign estimands.
- Manuscript/Figure: future latent Results and Fig. 3C-D only after frozen L06 data.
- State: `pending_implementation`.

## 9. Scope and release boundaries

### `W1-BOUND-01` — registered versus empirical scope

- Allowed: registered surface, compiled task evidence, and autonomous task evidence are distinct scopes; current compiled evidence covers two tasks and autonomous evidence one.
- Forbidden: 15 formal agent results or arbitrary chemistry.
- Evidence: `platform_surface` (`DONE`).
- Analysis unit: scope statement. Manuscript: Apparatus/Methods/Limitations. Figure: Fig. 1D.
- State: `boundary_only`.

### `W1-BOUND-02` — physical bridge

- Allowed: ChemWorld complements physical laboratories by enabling controlled repeated studies in selected synthetic worlds.
- Forbidden: deployment, robot capability, universal fidelity, physical safety, or direct transfer.
- Evidence: `experiment_semantics` (`DONE`).
- Analysis unit: scope statement. Manuscript: Related work/Discussion. Figure: Fig. 1 caption.
- State: `boundary_only`.

### `W1-BOUND-03` — Work II separation

- Allowed: Work I covers the measurement apparatus and bounded behavior; mechanism adaptation, belief revision, model/backend ablation, and physical bridging are separate work.
- Forbidden: historical Gate A as current agent law learning or early use of Work II conclusions.
- Evidence: `current_registry` (mechanism bindings stale; publication false).
- Analysis unit: scope statement. Manuscript: Discussion/future work. Figure: none.
- State: `boundary_only`.

### `W1-BOUND-04` — integration/release state

- Allowed: the current manuscript/display/figure/derived surfaces are inputs, not final Work I release outputs; publication readiness remains false pending L, D03-D05, final S/P/Q gates, the external G0 archive, and author metadata.
- Forbidden: publication-ready language, silent reuse of the old figure order, or invented archive/author identifiers.
- Evidence: `current_registry` (`publication_ready=false`) and `legacy_derived_data` (pre-Work-I layer).
- Analysis unit: release gate. Manuscript: Data availability/internal integration. Figure: all panels pending P integration.
- State: `external_release_blocked`.

## Integration handoff

The final Work I display order is:

1. apparatus and controlled world forks;
2. known-policy measurement validity;
3. same completion, different terminal policy, with latent panels only after L06;
4. compiled information controls;
5. autonomous lifecycle/process profiles;
6. fresh-session trajectory variation.

The tracked figure manifest still uses the pre-Work-I order and has no fork, known-policy, or latent-terminal panels. The tracked derived-data object is also the earlier frozen layer and contains no F/V/L Work I outputs. S02-S10, P01-P09, and D03-D05 must reconcile those surfaces. Until L05-L06 close, the latent audit remains protocol/reconstructability text only and cannot enter the title-level empirical conclusion as terminal-quality evidence.
