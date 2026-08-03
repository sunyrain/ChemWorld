# Work I story architecture v0.1

Status: **FROZEN FOR DOWNSTREAM DRAFTING**  
Owner: `codex-1`  
Task: `W1-S02`

## 1. The announcement

### One-sentence paper claim

**ChemWorld turns experimental agency from an endpoint impression into an auditable
profile by placing complete agent systems in programmable, replayable chemical worlds
where evidence acquisition, lifecycle closure, terminal policy, resource use, and
trajectory dynamics can be measured separately.**

### Reader takeaway

The paper is not a leaderboard and not a claim that virtual chemistry replaces a
self-driving laboratory. It introduces a controlled measurement apparatus, shows that
the apparatus responds correctly to known experimental policies, and then uses it to
show why a completed lifecycle or a final score does not uniquely identify the process
that produced it.

### Story in six beats

1. **Build the instrument.** Make chemical worlds stateful, identity-bound,
   resource-accounted, and replayable; show that a single component can be changed
   without silently changing the public contract.
2. **Calibrate the readout.** Run three frozen known policies and recover their expected
   experimental-agency profiles before interpreting complete agent systems.
3. **State the headline.** Two distinct complete agent systems close all 120 matched
   lifecycles, yet their terminal policies differ: 84 final assays and 36 explicit
   discards in total.
4. **Separate capabilities.** Compiled controls show that outcome, held-out prediction,
   calibration, and claim reliability are different readouts, not one latent score.
5. **Open the process record.** Primitive-control trajectories expose actions,
   measurements, failures, resources, termination, assay, and discard as a complete
   lifecycle rather than a single query.
6. **Show what endpoints omit.** Fresh matched trajectories distinguish discovery,
   retention, drawdown, recovery, and terminal quality even when endpoint summaries
   appear similar.

This order is result-independent. The latent-terminal audit may qualify the quality of
the 36 discards, but it may not decide whether the terminal-policy observation enters
the paper.

## 2. Authority and evidence ladder

Narrative decisions must follow this authority order:

1. `WORK_I_TODOLIST.md` and the Work I master plan define scope and non-goals.
2. Frozen protocol, qualification, and formal reports define permissible evidence.
3. The W1-S01 claim--evidence--figure map supplies claim-level source bindings when it
   is handed off.
4. The current manuscript is migration input, not authority for final order or wording.

The evidence ladder is cumulative:

| Level | Question answered | Evidence role | Claim ceiling |
| --- | --- | --- | --- |
| Apparatus | Can experimental choices be executed and audited? | platform qualification, transaction/resource/failure semantics, exact replay | qualified measurement surface, not agent competence on 15 tasks |
| Programmability | Can one world component be changed while identity and public interface remain controlled? | 6 parent--child fork pairs, 24 qualification traces | programmable-world apparatus, not agent rule adaptation |
| Measurement validity | Does the profile distinguish known policies whose behavior is fixed in advance? | 30 primary campaigns, 180 primary closed lifecycles; retests separate | positive-control construct validity, not an LLM performance result |
| Compiled controls | Are endpoint, prediction, calibration, and claims separable? | frozen G0 matched-world reports | capability decomposition, not an LLM-versus-optimizer contest |
| Complete systems | Do full systems expose different terminal policies under one apparatus? | 120 closed lifecycles: 84 assays plus 36 discards | descriptive complete-system policy contrast, not a model-only causal effect |
| Latent terminal | Were discarded states promising under the frozen counterfactual assay? | 36 evaluator-only shadow assays, pending W1-L05/L06 | only preregistered continuous, threshold, and censoring results; no retroactive selection |
| Fresh trajectories | Which process properties recur or vary within fixed worlds? | 8 complete matched pairs plus two right-censored pairs | within-world process evidence, not a population model ranking |

Exact replay, deterministic retest, synthetic qualification, and evaluator shadows never
inflate the corresponding primary denominators. Primitive operations are repeated
events, not independent samples.

## 3. Main-text order and section responsibilities

Section responsibilities in `WORK_I_TODOLIST.md` remain binding, while the six-figure
order and first-reference rule determine the final Results sequence. The downstream
draft may renumber headings, but it must preserve the following responsibility map.

| Narrative block | Must answer | Required evidence/figure | Must hand off | Must not do |
| --- | --- | --- | --- | --- |
| Introduction + relation to existing systems | Why can neither endpoint benchmarks nor physical deployment alone isolate experimental policy? | concise scope comparison; no results dump | agent-as-subject/world-as-apparatus thesis | claim replacement of SDLs or preview Work II conclusions |
| Apparatus + programmability validation | What is controlled, what is observed, and can the world be deliberately forked? | **Fig. 1**; platform surface; fork certificate | a qualified measurement instrument | present 15 registered tasks as 15 formal agent results or treat a fork as adaptation |
| Measurement validity | Does the instrument recover three policies fixed before the run? | **Fig. 2**; V01--V09 | permission to interpret profile differences | mix primary campaigns with deterministic retests or present policies as agents |
| Complete-system terminal-policy headline | What differs despite complete lifecycle closure? | **Fig. 3**; 60 Codex assays, 24 DeepSeek assays, 36 DeepSeek discards; latent slots | completion and terminal policy are distinct readouts | infer discard quality before L05/L06 or reduce systems to model backends |
| Compiled controls | Which epistemic readouts remain distinct even with a bounded interface? | **Fig. 4**; frozen G0 results | outcome alone is not the full capability profile | turn G0 into a horse race or form an unregistered composite score |
| Primitive-control lifecycle mechanics | What choices and resource consequences make one lifecycle experimentally meaningful? | **Fig. 5**; immutable trajectories and ledgers | process is directly recorded rather than inferred from endpoints | count operations as independent samples or hide failed actions |
| Fresh process profiles | What does matched re-sampling reveal beyond best or terminal value? | **Fig. 6**; continuous contrasts and censoring | discovery, retention, drawdown, recovery, and terminal quality are separable | pool deliberately selected worlds into a population estimate |
| Discussion + conclusion | What has been established, what remains bounded, and how does this complement real laboratories? | synthesis of F/V/G0/G2/L; limitations | experimental agency is a measured profile, not a scalar | claim real chemistry deployment, general model superiority, or Work II rule learning |

Methods must mirror dependency order rather than repeat the Results narrative:
apparatus and identities; world forks; known-policy validation; compiled controls;
primitive-control systems; latent-terminal protocol; fresh-session replication;
estimands/censoring; provenance and replay.

## 4. Six-figure contract

Figures are first referenced in numeric order. Each figure owns one question; later
figures may reuse identifiers but may not duplicate an earlier figure's explanatory job.

| Figure | Frozen title | Sole narrative job | Explicit exclusion |
| --- | --- | --- | --- |
| 1 | ChemWorld apparatus and controlled world forks | Establish the measurement apparatus and controlled programmability | no agent-performance comparison |
| 2 | Known policies validate the experimental-agency profile | Demonstrate discriminant and test--retest validity using frozen controls | retest evidence does not double the primary sample |
| 3 | Lifecycle completion does not specify terminal policy | Carry the 120-lifecycle headline and the preregistered latent-terminal slots | no claim that discard is good, efficient, or cost-saving without formal results |
| 4 | Compiled controls separate outcome, prediction, calibration and claims | Show why a single endpoint or composite score is inadequate | no G0 LLM-versus-BO framing |
| 5 | Primitive-control agents expose complete experimental lifecycles | Show the action/observation/resource/termination anatomy of complete-system runs | no duplicate assay/discard headline and no operation-level pseudo-replication |
| 6 | Fresh trajectories reveal process structure omitted by endpoints | Show continuous matched contrasts, censoring, and within-world variation | 2/8 is an endpoint diagnostic; 6/8 is threshold-sensitive supporting evidence |

The Results order follows Figures 1--6. The section-responsibility list in the master
plan is therefore interpreted as a content contract, not a requirement to preserve the
current manuscript's numbering. This resolves the otherwise incompatible requirements
that compiled controls own a separate section, terminal policy own Figure 3, and all
figures appear in first-reference order.

## 5. Result-independent latent-terminal slots

The terminal-policy headline is already supported by the frozen 84-assay/36-discard
partition. The following slots remain visibly pending until W1-L05/L06:

- continuous latent terminal score for all 36 registered discards;
- discard-to-observed-best delta and positive discard regret;
- false-discard fraction and threshold sensitivity;
- assay-commitment precision and recall;
- campaign-oracle regret over the nine cells with a discard opportunity;
- decision-time regret and the registered censoring/bounds rows.

`cell-02` has no discard opportunity, so its campaign-oracle value remains `null`, not
zero. If any shadow outcome is unresolved, all 36 identities remain in the registered
population and the frozen bounds/censoring rules apply; complete-case substitution is
forbidden. Favorable and unfavorable results occupy the same Figure 3 and Results slots.

## 6. Language and counting locks

Every downstream draft must preserve these locks:

- On first mention, write **120 closed lifecycles: 84 final assays and 36 explicit
  discards**.
- Use **distinct complete agent systems** (or an exact equivalent), not
  `independently configured` and not model-only shorthand.
- Keep model, scaffold, transport, authority, evidence access, and system identity
  distinct.
- Treat the 2/8 best-versus-raw-terminal sign discordance as the main endpoint
  diagnostic; treat the 6/8 mixed classification as threshold-sensitive supporting
  evidence.
- State that the two fresh-session worlds were deliberately selected and are not pooled
  into a population-level model comparison.
- Keep registered platform scope separate from formal empirical scope.
- Call shadow assays evaluator-only counterfactual evaluations, never agent experiments
  or agent assay decisions.
- Describe ChemWorld as virtual/executable chemical worlds, never as completed physical
  chemistry deployment.
- Reserve rule learning and adaptation-under-law-change for Work II.

## 7. Downstream handoff

| Task | Required use of this freeze |
| --- | --- |
| W1-S03 | Use the one-sentence claim and six-beat escalation for title, abstract, and introduction placeholders; do not insert pending L numbers. |
| W1-S04 | Own apparatus and programmability prose corresponding to Figure 1 and the first two evidence-ladder levels. |
| W1-S05 | Own known-policy measurement validity corresponding to Figure 2; keep retests outside the primary estimand. |
| W1-S06 | Own the Figure 3 terminal-policy headline, Figure 5 lifecycle mechanics, and result-independent L slots. |
| W1-S07 | Enforce first-reference order and all language/counting locks. |
| W1-S08 | Keep relation-to-existing-systems focused on complementarity and the measurement gap. |
| W1-S09 | Carry virtual-to-real, selection, system-boundary, and non-generalization limits. |
| W1-S10 | Replace only registered pending slots after frozen F/V/L reports; do not restructure based on result direction. |
| W1-P01 | Derive visual hierarchy, color, type, and panel grid from the six-figure contract. |
| W1-P02--P07 | Implement Figures 1--6 in the exact role order above. |
| W1-P08--P09 | Verify editability, typography, caption, first-reference, and manifest consistency without changing figure jobs. |

## 8. Acceptance checklist

- [x] One central claim can be repeated without a numerical result.
- [x] Apparatus, programmability, validity, application, process, and limitation form a
  single escalation.
- [x] All eight section responsibilities have one job and one claim ceiling.
- [x] All six figures have unique jobs and a valid first-reference order.
- [x] Existing terminal-policy evidence and pending latent-quality evidence are separate.
- [x] Frozen counts and analysis units cannot be double counted.
- [x] Work II and real-laboratory deployment remain outside the first paper.
- [x] Every downstream S/P task has an explicit handoff.
